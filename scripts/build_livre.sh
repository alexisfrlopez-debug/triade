#!/usr/bin/env bash
# TRIADE — Régénération systématique du LIVRE DU COFFRE (D133 → M5-a, D134).
#
# Miroir de scripts/build_pdf.sh pour la seconde chaîne PDF du dépôt : le
# Livre du Coffre (docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.1.pdf, produit par
# scripts/livre_coffre/ — figure de la chaîne Playwright @2× + couverture
# Template 03 + corps LaTeX/Tectonic fusionnés par pypdf). Le présent script
# garantit ce que D133 faisait à la main : le livre ne peut pas vieillir —
# il compare l'empreinte SHA-256 des sources au dernier build
# (.livre_build.stamp, suivi par git) et reconstruit tout si elles divergent.
#
# M5 (a), D134 — ÉTAPE 7 : le build CONSIGNE LUI-MÊME l'empreinte de son
# artefact au tableau de bord (docs/TABLEAU_BORD.md) et au journal de travail
# (scripts/empreintes_build.py consigner). Une divergence inter-build est un
# refus nommé (scripts/empreintes_build.py verifier).
#
# Usage :
#   bash scripts/build_livre.sh            # reconstruit si les sources ont changé
#   bash scripts/build_livre.sh --force    # reconstruit toujours
#   bash scripts/build_livre.sh --check    # ne construit pas ; code 2 si rebuild requis
#   bash scripts/build_livre.sh --diagramme  # force la re-capture Playwright du schéma
#
# Dépendances (poste de génération) : python3 + pypdf + pdfplumber, tectonic,
# node, éventuellement playwright (--diagramme ou schéma périmé), et le
# répertoire skills/pdf de l'espace de travail.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
BASE="${TRIADE_BASE:-/home/z/my-project}"
SKILL="$BASE/skills/pdf"

LIVRE_DIR=scripts/livre_coffre
COVER_HTML="$LIVRE_DIR/cover.html"
COVER_PDF="$LIVRE_DIR/cover.pdf"
DIAG_HTML="$LIVRE_DIR/chaine_cf.html"
DIAG_PNG="$LIVRE_DIR/chaine_cf.png"
FINAL_PDF=docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.1.pdf
STAMP=.livre_build.stamp

# Sources dont la modification déclenche la reconstruction.
SOURCES=("$LIVRE_DIR/main.tex" "$LIVRE_DIR/sec-1.tex" "$LIVRE_DIR/sec-2.tex"
         "$LIVRE_DIR/sec-3.tex" "$LIVRE_DIR/sec-4.tex" "$LIVRE_DIR/sec-5.tex"
         "$LIVRE_DIR/sec-6.tex" "$LIVRE_DIR/cover.html"
         "$LIVRE_DIR/merge_cover.py" "$LIVRE_DIR/chaine_cf.html"
         "$LIVRE_DIR/capture_diagramme.py")

hash_sources() {
  for f in "${SOURCES[@]}"; do
    if [ -f "$f" ]; then sha256sum "$f"; else echo "MISSING $f"; fi
  done | sha256sum | cut -d' ' -f1
}

FORCE=0; CHECK=0; DIAGRAMME=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    --check) CHECK=1 ;;
    --diagramme) DIAGRAMME=1 ;;
  esac
done

CURRENT="$(hash_sources)"
if [ "$CHECK" -eq 1 ]; then
  echo "[livre] stamp courant des sources : $CURRENT"
fi
if [ "$FORCE" -eq 0 ] && [ -f "$STAMP" ] && [ "$(cat "$STAMP")" = "$CURRENT" ] \
   && [ -f "$FINAL_PDF" ]; then
  echo "[livre] à jour — aucune source du livre modifiée depuis le dernier build"
  exit 0
fi
if [ "$CHECK" -eq 1 ]; then
  echo "[livre] sources du livre modifiées — reconstruction requise"
  exit 2
fi

echo "[livre] sources modifiées (ou build forcé) — régénération du Livre du Coffre v1.1"

# 1) Figure de la chaîne : re-capture Playwright si le schéma HTML est plus
#    récent que le PNG, si le PNG manque, ou si --diagramme est demandé.
if [ "$DIAGRAMME" -eq 1 ] || [ ! -f "$DIAG_PNG" ] \
   || [ "$DIAG_HTML" -nt "$DIAG_PNG" ]; then
  echo "[livre] re-capture du schéma de la chaîne (Playwright @2x)"
  python3 "$LIVRE_DIR/capture_diagramme.py" \
    "$ROOT/$DIAG_HTML" "$ROOT/$DIAG_PNG" || {
    echo "[livre] ERREUR : capture du schéma en échec" >&2; exit 1; }
fi

# 2) Validation de la couverture (HTML puis chevauchements au rendu réel)
if [ ! -d "$SKILL" ]; then
  echo "[livre] ERREUR : skill PDF introuvable ($SKILL)" >&2
  exit 1
fi
python3 "$SKILL/scripts/poster_validate.py" check-html "$COVER_HTML" || {
  echo "[livre] ERREUR : validation HTML de la couverture en échec" >&2; exit 1; }
node "$SKILL/scripts/cover_validate.js" "$COVER_HTML" || {
  echo "[livre] ERREUR : chevauchements détectés sur la couverture" >&2; exit 1; }

# 3) Rendu vectoriel de la couverture (html2poster : pages absolues)
node "$SKILL/scripts/html2poster.js" "$COVER_HTML" --output "$COVER_PDF" --width 794px || {
  echo "[livre] ERREUR : rendu de la couverture en échec" >&2; exit 1; }

# 4) Corps LaTeX (Tectonic via le wrapper du skill)
( cd "$LIVRE_DIR" && \
  PDF_SKILL_DIR="$SKILL" python3 "$SKILL/scripts/pdf.py" convert.latex main.tex --runs 2 ) \
  || { echo "[livre] ERREUR : compilation LaTeX du corps en échec" >&2; exit 1; }

# 5) Fusion couverture + corps (chemins absolus, exécutable depuis la racine)
python3 "$LIVRE_DIR/merge_cover.py" || {
  echo "[livre] ERREUR : fusion couverture + corps en échec" >&2; exit 1; }

# 6) Qualité : pages blanches, glyphes, scan global
python3 "$SKILL/scripts/pdf.py" pages.clean "$LIVRE_DIR/final.pdf" -o "$LIVRE_DIR/final.pdf.clean" >/dev/null 2>&1
if [ -f "$LIVRE_DIR/final.pdf.clean" ]; then
  if ! cmp -s "$LIVRE_DIR/final.pdf" "$LIVRE_DIR/final.pdf.clean"; then
    mv "$LIVRE_DIR/final.pdf.clean" "$LIVRE_DIR/final.pdf"
    echo "[livre] pages blanches supprimées"
  else
    rm -f "$LIVRE_DIR/final.pdf.clean"
  fi
fi
python3 "$SKILL/scripts/pdf.py" font.check "$LIVRE_DIR/final.pdf" 2>/dev/null \
  | grep -q '"total_issues": 0' || echo "[livre] AVERTISSEMENT : glyphes manquants"
python3 "$SKILL/scripts/pdf_qa.py" --skip-cover "$LIVRE_DIR/final.pdf" || {
  echo "[livre] ERREUR : contrôle qualité pdf_qa en échec" >&2; exit 1; }

# 7) Publication du livre + stamp + CONSIGNATION DE L'EMPREINTE PAR LE BUILD (M5-a)
cp "$LIVRE_DIR/final.pdf" "$FINAL_PDF"
if [ -d "$BASE/download" ]; then
  cp "$FINAL_PDF" "$BASE/download/" || true
fi
echo "$CURRENT" > "$STAMP"
if [ -f scripts/empreintes_build.py ]; then
  python3 scripts/empreintes_build.py consigner \
    --artefact "$FINAL_PDF" --build "build_livre.sh (chaîne livre_coffre)" \
    --stamp-file "$STAMP" || \
    echo "[livre] AVERTISSEMENT : consignation de l'empreinte impossible (non bloquant)"
else
  echo "[livre] AVERTISSEMENT : scripts/empreintes_build.py absent (M5-a non porté)"
fi
echo "[livre] Livre du Coffre v1.1 régénéré -> $FINAL_PDF (empreinte consignée)"
