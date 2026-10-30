#!/usr/bin/env bash
# TRIADE — Sauvegarde systématique : commit git + synchro Google Drive + push GitHub.
#
# Usage :
#   bash scripts/sync_backup.sh                     # message horodaté automatique
#   bash scripts/sync_backup.sh "M0 : round-trip ok"
#
# Règle D13 : à exécuter après CHAQUE modification du projet, sans exception.
# Le script est idempotent : un appel sans changement ne coûte quasiment rien.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
MSG="${1:-sauvegarde automatique du $(date '+%Y-%m-%d %H:%M:%S')}"

# 0) Réinstalle le hook post-commit s'il manque (clone frais, restauration, etc.)
if [ -d .git ] && [ ! -x .git/hooks/post-commit ] && [ -f git-hooks/post-commit ]; then
  cp git-hooks/post-commit .git/hooks/post-commit
  chmod +x .git/hooks/post-commit
  echo "[sync] hook post-commit réinstallé"
fi

# 0.5) PDF formel : régénération systématique quand les sources du protocole ont
#      changé (D17) — AVANT le commit, pour que la sauvegarde embarque un PDF à jour.
if [ -f scripts/build_pdf.sh ]; then
  if bash scripts/build_pdf.sh; then
    :
  else
    echo "[sync] AVERTISSEMENT : échec de la régénération du PDF formel (non bloquant)"
  fi
else
  echo "[sync] AVERTISSEMENT : scripts/build_pdf.sh introuvable"
fi

# 1) Commit git — le hook post-commit déclenche la synchro Drive à chaque commit
if git rev-parse --git-dir >/dev/null 2>&1; then
  git add -A
  if git diff --cached --quiet 2>/dev/null; then
    echo "[sync] rien à committer"
  else
    git commit -m "$MSG"
  fi
else
  echo "[sync] AVERTISSEMENT : pas de dépôt git dans $ROOT"
fi

# 2) Synchro Drive explicite (idempotente ; couvre le cas d'un hook absent ou contourné)
#     D130 : le kit « Cérémonie » suit le miroir dans le MÊME geste.
if [ -f scripts/drive_sync.py ]; then
  python3 scripts/drive_sync.py
else
  echo "[sync] AVERTISSEMENT : scripts/drive_sync.py introuvable"
fi
if [ -f scripts/maj_kit.py ]; then
  python3 scripts/maj_kit.py
else
  echo "[sync] AVERTISSEMENT : scripts/maj_kit.py introuvable (kit non rafraîchi)"
fi

# 3) Push GitHub si la remote est configurée
if git remote 2>/dev/null | grep -q '^origin$'; then
  if git push origin HEAD >/dev/null 2>&1; then
    echo "[sync] poussé vers GitHub"
  else
    echo "[sync] push GitHub : échec (non bloquant)"
  fi
fi

echo "[sync] sauvegarde terminée"
