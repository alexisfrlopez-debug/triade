#!/bin/bash
# Triade Kit - lanceur Linux (double-clic ou ./LANCEUR-LINUX.sh)
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3 est introuvable. Installez-le avec :"
  echo "    sudo apt install python3 python3-tk   (Debian/Ubuntu)"
  echo "    sudo dnf install python3 python3-tkinter   (Fedora)"
  exit 1
fi
exec python3 TriadeKit.py
