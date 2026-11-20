#!/bin/bash
# Pipeline de génération du Manuel du développeur — Kit Triade.
set -e
KIT=/home/z/my-project/download/kit-dev-triade
SCRIPTS=/home/z/my-project/scripts
DOCX_SCRIPTS=/home/z/my-project/skills/docx/scripts
DOCX=$KIT/docs/MANUEL_DEVELOPPEUR.docx
PDF=$KIT/docs/MANUEL_DEVELOPPEUR.pdf

echo "— 1/7 génération docx"
node "$SCRIPTS/gen_manuel.js"

echo "— 2/7 entrées du sommaire"
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" "$DOCX" --auto

echo "— 3/7 pieds de page WPS"
python3 "$SCRIPTS/patch_pieds.py" "$DOCX"

echo "— 4/7 correctif doublon première entrée"
python3 "$SCRIPTS/fix_toc_doublon.py" "$DOCX"

echo "— 5/7 PDF de mesure"
cd "$KIT/docs" && rm -f "$PDF"
soffice --headless --convert-to pdf "$DOCX" >/dev/null 2>&1

echo "— 6/7 numéros de page réels"
python3 "$SCRIPTS/fix_numeros_toc.py" "$DOCX" "$PDF"

echo "— 7/7 PDF final + postcheck"
rm -f "$PDF"
soffice --headless --convert-to pdf "$DOCX" >/dev/null 2>&1
python3 "$DOCX_SCRIPTS/postcheck.py" "$DOCX" || true
ls -la "$KIT/docs"
