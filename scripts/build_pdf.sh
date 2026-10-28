#!/usr/bin/env bash
# TRIADE — Régénération systématique du PDF formel du protocole (décisions D17, D25).
#
# Depuis la v0.5.1, le PDF formel de la version courante est
# docs/Protocole_TRIADE_v0.5.1_Specification.pdf, produit par la chaîne
# LaTeX/Tectonic (scripts/spec_v051/, D75 — née spec_v040 → spec_v050) : corps
# monocolonne avec sommaire, couverture académique Template 03 fusionnée par
# pypdf. Les archives des versions précédentes (v0.2, v0.3, v0.4.0, v0.5.0)
# demeurent dans docs/ et ne sont plus régénérées. Le présent script garantit
# que le PDF courant ne devient jamais périmé : il compare l'empreinte SHA-256
# des sources (4 documents markdown + sources LaTeX + couverture + scripts de
# fusion) à celle du dernier build (.pdf_build.stamp, suivi par git) et
# reconstruit tout si elles divergent. Intégré à sync_backup.sh, il s'exécute
# AVANT chaque commit.
#
# Usage :
#   bash scripts/build_pdf.sh            # reconstruit si les sources ont changé
#   bash scripts/build_pdf.sh --force    # reconstruit toujours
#   bash scripts/build_pdf.sh --check    # ne construit pas ; code 2 si rebuild requis
#
# Dépendances (poste de génération) : python3 + pypdf + pdfplumber, tectonic,
# node, et le répertoire skills/pdf de l'espace de travail (validateurs,
# html2poster, pdf.py).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BASE="${TRIADE_BASE:-/home/z/my-project}"
SKILL="$BASE/skills/pdf"

SPEC_DIR=scripts/spec_v051
COVER_HTML="$SPEC_DIR/cover.html"
COVER_PDF="$SPEC_DIR/cover.pdf"
FINAL_PDF=docs/Protocole_TRIADE_v0.5.1_Specification.pdf
STAMP=.pdf_build.stamp

# Sources dont la modification déclenche la reconstruction.
SOURCES=(docs/PROTOCOLE_TRIADE.md docs/FORMAT_CARTE.md docs/DECISIONS.md
         docs/PLAN_MILESTONES.md
         "$SPEC_DIR/main.tex" "$SPEC_DIR/sec-a.tex" "$SPEC_DIR/sec-b.tex"
         "$SPEC_DIR/sec-c.tex" "$SPEC_DIR/sec-d.tex"
         "$SPEC_DIR/cover.html" "$SPEC_DIR/merge_cover.py")

hash_sources() {
  for f in "${SOURCES[@]}"; do
    if [ -f "$f" ]; then sha256sum "$f"; else echo "MISSING $f"; fi
  done | sha256sum | cut -d' ' -f1
}

FORCE=0; CHECK=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --check) CHECK=1 ;;
  esac
done

CURRENT="$(hash_sources)"
if [ "$FORCE" -eq 0 ] && [ -f "$STAMP" ] && [ "$(cat "$STAMP")" = "$CURRENT" ] \
   && [ -f "$FINAL_PDF" ]; then
  echo "[pdf] à jour — aucune source du protocole modifiée depuis le dernier build"
  exit 0
fi
if [ "$CHECK" -eq 1 ]; then
  echo "[pdf] sources du protocole modifiées — reconstruction requise"
  exit 2
fi

echo "[pdf] sources modifiées (ou build forcé) — régénération du PDF formel v0.5.1"

# 1) Validation de la couverture (HTML puis chevauchements au rendu réel)
if [ ! -d "$SKILL" ]; then
  echo "[pdf] ERREUR : skill PDF introuvable ($SKILL)" >&2
  exit 1
fi
python3 "$SKILL/scripts/poster_validate.py" check-html "$COVER_HTML" || {
  echo "[pdf] ERREUR : validation HTML de la couverture en échec" >&2; exit 1; }
node "$SKILL/scripts/cover_validate.js" "$COVER_HTML" || {
  echo "[pdf] ERREUR : chevauchements détectés sur la couverture" >&2; exit 1; }

# 2) Rendu vectoriel de la couverture (html2poster : pages absolues -> jamais Paged.js)
node "$SKILL/scripts/html2poster.js" "$COVER_HTML" --output "$COVER_PDF" --width 794px || {
  echo "[pdf] ERREUR : rendu de la couverture en échec" >&2; exit 1; }

# 3) Corps LaTeX (Tectonic via le wrapper du skill) + fusion couverture/corps
( cd "$SPEC_DIR" && \
  PDF_SKILL_DIR="$SKILL" python3 "$SKILL/scripts/pdf.py" convert.latex main.tex --runs 2 ) \
  || { echo "[pdf] ERREUR : compilation LaTeX du corps en échec" >&2; exit 1; }
python3 "$SPEC_DIR/merge_cover.py" || {
  echo "[pdf] ERREUR : fusion couverture + corps en échec" >&2; exit 1; }

# 4) Qualité : pages blanches, glyphes, scan global
python3 "$SKILL/scripts/pdf.py" pages.clean "$SPEC_DIR/final.pdf" -o "$SPEC_DIR/final.pdf.clean" >/dev/null 2>&1
if [ -f "$SPEC_DIR/final.pdf.clean" ]; then
  if ! cmp -s "$SPEC_DIR/final.pdf" "$SPEC_DIR/final.pdf.clean"; then
    mv "$SPEC_DIR/final.pdf.clean" "$SPEC_DIR/final.pdf"
    echo "[pdf] pages blanches supprimées"
  else
    rm -f "$SPEC_DIR/final.pdf.clean"
  fi
fi
python3 "$SKILL/scripts/pdf.py" font.check "$SPEC_DIR/final.pdf" 2>/dev/null \
  | grep -q '"total_issues": 0' || echo "[pdf] AVERTISSEMENT : glyphes manquants"
python3 "$SKILL/scripts/pdf_qa.py" --skip-cover "$SPEC_DIR/final.pdf" || {
  echo "[pdf] ERREUR : contrôle qualité pdf_qa en échec" >&2; exit 1; }

# 5) Publication du PDF formel + consignation de l'empreinte
cp "$SPEC_DIR/final.pdf" "$FINAL_PDF"
if [ -d "$BASE/download" ]; then
  cp "$FINAL_PDF" "$BASE/download/" || true
fi
echo "$CURRENT" > "$STAMP"
echo "[pdf] PDF formel v0.5.1 régénéré -> $FINAL_PDF"
