#!/bin/bash
# Triade Kit - lanceur macOS (double-clic)
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3 est introuvable."
  echo "    Installez les Command Line Tools avec : xcode-select --install"
  echo "    puis relancez ce fichier."
  read -n 1 -s -r -p "Appuyez sur une touche pour fermer..."
  echo
  exit 1
fi
python3 TriadeKit.py
code=$?
if [ $code -ne 0 ]; then
  echo
  read -n 1 -s -r -p "Appuyez sur une touche pour fermer..."
  echo
fi
exit $code
