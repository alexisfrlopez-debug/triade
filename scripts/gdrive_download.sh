#!/bin/bash
# Télécharge un fichier Google Drive en gérant l'avertissement de scan antivirus
# Usage: gdrive_download.sh <FILE_ID> <OUTPUT_PATH>
ID="$1"
OUT="$2"
WARN_URL="https://drive.google.com/uc?export=download&id=${ID}"

PAGE=$(curl -sL "$WARN_URL")

if echo "$PAGE" | grep -q 'drive.usercontent.google.com/download'; then
  # Page d'avertissement -> extraire les champs cachés
  QUERY=$(echo "$PAGE" | grep -o '<input type="hidden" name="[^"]*" value="[^"]*"' \
    | sed -E 's/<input type="hidden" name="([^"]*)" value="([^"]*)"/\1=\2/' \
    | paste -sd'&' -)
  curl -sL "https://drive.usercontent.google.com/download?${QUERY}" -o "$OUT"
else
  # Téléchargement direct
  curl -sL "$WARN_URL" -o "$OUT"
fi
echo "OK: $OUT ($(stat -c%s "$OUT") bytes)"
