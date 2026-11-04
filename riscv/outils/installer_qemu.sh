#!/bin/sh
# installer_qemu.sh — qemu-riscv64 AU LABO, extraction locale SANS privilèges.
#
# Le constat fiche § 10 (04/11/2026) : aucun binaire qemu-riscv64 dans le
# bac à sable — le prérequis du chantier M7-(a). Le bac n'a PAS de sudo :
# la voie est le paquet Debian qemu-user (binaires STATIQUES), téléchargé
# et extrait LOCALEMENT dans riscv/.tmp/ (gitignoré — le binaire est un
# INSTRUMENT, pas une pièce du dépôt ; la PROCÉDURE est la pièce, elle vit
# ici). Re-vérifié avant usage par build_m7.py (la réserve instrumentale
# D149 : qemu-riscv64 exécute l'ISA par TCG, le noyau et les syscalls sont
# RÉELS — jamais déguisés en exécution native).
set -e
RISCV="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$RISCV/.tmp"
BIN="$DEST/qemu-extract/usr/bin/qemu-riscv64"
QEMU_URL_Miroir=""
if [ -n "$QEMU_RISCV64" ] && [ -x "$QEMU_RISCV64" ]; then
    echo "qemu-riscv64 fourni par l'environnement : $QEMU_RISCV64"
    "$QEMU_RISCV64" --version | head -1
    exit 0
fi
if [ -x "$BIN" ]; then
    echo "qemu-riscv64 déjà extrait : $BIN"
    "$BIN" --version | head -1
    exit 0
fi
echo "téléchargement du paquet qemu-user (binaires statiques)…"
mkdir -p "$DEST"
cd "$DEST"
apt-get download qemu-user
dpkg-deb -x qemu-user_*.deb qemu-extract
rm -f qemu-user_*.deb
echo "extraction : $BIN"
"$BIN" --version | head -1
