#!/usr/bin/env bash
# TRIADE — Régénération systématique du PDF formel du protocole (décision D17).
#
# Le PDF docs/Protocole_TRIADE_v0.3_Specification.pdf est un artefact DÉRIVÉ des
# sources markdown du protocole. Ce script garantit qu'il ne devient jamais périmé :
# il compare l'empreinte SHA-256 des sources (4 documents + script + couverture) à
# celle du dernier build (.pdf_build.stamp, suivi par git) et reconstruit tout si
# elles divergent. Intégré à sync_backup.sh, il s'exécute AVANT chaque commit —
# la sauvegarde embarque donc toujours un PDF synchrone des sources.
#
# Usage :
#   bash scripts/build_pdf.sh            # reconstruit si les sources ont changé
#   bash scripts/build_pdf.sh --force    # reconstruit toujours
#   bash scripts/build_pdf.sh --check    # ne construit pas ; code 2 si rebuild requis
#
# Dépendances (poste de génération) : python3 + reportlab + pypdf + PIL, node,
# et le répertoire skills/pdf de l'espace de travail (validateurs + html2poster).
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BASE="${TRIADE_BASE:-/home/z/my-project}"
SKILL="$BASE/skills/pdf"

SPEC=scripts/triade_v03_spec.py
COVER_HTML=scripts/triade_v03_cover.html
COVER_PDF=scripts/triade_v03_cover.pdf
FINAL_PDF=docs/Protocole_TRIADE_v0.3_Specification.pdf
STAMP=.pdf_build.stamp

# Sources dont la modification déclenche la reconstruction.
SOURCES=(docs/PROTOCOLE_TRIADE.md docs/FORMAT_CARTE.md docs/DECISIONS.md
         docs/PLAN_MILESTONES.md "$SPEC" "$COVER_HTML")

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

echo "[pdf] sources modifiées (ou build forcé) — régénération du PDF formel"

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

# 3) Corps + fusion (le script écrit $FINAL_PDF et copie dans BASE/download/)
python3 "$SKILL/scripts/pdf.py" code.sanitize "$SPEC" || true
python3 "$SPEC" || { echo "[pdf] ERREUR : génération du corps en échec" >&2; exit 1; }

# 4) Qualité : métadonnées, pages blanches, glyphes, TOC, scan global
python3 "$SKILL/scripts/pdf.py" meta.brand "$FINAL_PDF" >/dev/null || true
python3 "$SKILL/scripts/pdf.py" pages.clean "$FINAL_PDF" -o "$FINAL_PDF.clean" >/dev/null 2>&1
if [ -f "$FINAL_PDF.clean" ]; then
  if ! cmp -s "$FINAL_PDF" "$FINAL_PDF.clean"; then
    mv "$FINAL_PDF.clean" "$FINAL_PDF"
    echo "[pdf] pages blanches supprimées"
  else
    rm -f "$FINAL_PDF.clean"
  fi
fi
python3 "$SKILL/scripts/pdf.py" font.check "$FINAL_PDF" 2>/dev/null \
  | grep -q '"total_issues": 0' || echo "[pdf] AVERTISSEMENT : glyphes manquants"
python3 "$SKILL/scripts/pdf_qa.py" --skip-cover "$FINAL_PDF" || {
  echo "[pdf] ERREUR : contrôle qualité pdf_qa en échec" >&2; exit 1; }

# 5) Consignation de l'empreinte (suivie par git : un clone frais ne rebuild pas)
echo "$CURRENT" > "$STAMP"
echo "[pdf] PDF formel régénéré -> $FINAL_PDF"
