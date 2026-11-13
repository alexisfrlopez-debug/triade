#!/usr/bin/env bash
# lancer-voie2-shani.sh — LE LANCEUR DE LA VOIE 2 QEMU : le kit-shani sous
# qemu-x86_64 -cpu max (l'émulation SHA-NI — l'édition AUTOMATISÉE du
# paquet multimachines, 12/11/2026).
#
# LE GESTE : tapez   bash lancer-voie2-shani.sh
# Ce lanceur fait pour vous la voie du LISEZMOI-qemu.txt :
#   1. il trouve qemu-x86_64 (il tente même de l'installer par apt si sudo
#      vit sans mot de passe ; sinon il vous donne LA commande exacte) ;
#   2. il lance le kit-1-shani EXACT du paquet sous émulation ;
#   3. les preuves naissent dans pc-windows/kit-1-shani/preuves-shani/.
#
# LA FRONTIÈRE NOMMÉE : cette voie EXERCE LA CHAÎNE (le refus ne peut plus
# exister — qemu présente SHA-NI au CPUID), elle NE MESURE PAS : le rapport
# rendu est l'ARTEFACT TCG (le labo l'a constaté : 0,19× — chaque
# sha256rnds2 traduit en dizaines d'opérations hôtes). La mesure avant/après
# n'a de sens que sur le VRAI silicium (le geste B demeure).
#
# Ce qui reste à VOTRE main : dater et signer le témoin en écrivant sous
# votre main « run sous qemu-x86_64 -cpu max, ÉMULATION, pas le silicium »,
# puis renvoyer le dossier preuves-shani/ ENTIER au coffre /test.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LA VOIE 2 QEMU — le kit-shani SOUS ÉMULATION (qemu-x86_64 -cpu max)"
echo " La chaîne complète sans le refus : le CPU virtuel présente SHA-NI."
echo " Le rapport rendu est l'ARTEFACT TCG, consigné TEL QUEL — jamais une"
echo " vérité de silicium."
echo "==================================================================="

QEMU="$(command -v qemu-x86_64 || true)"
if [ -z "$QEMU" ]; then
    echo "[lanceur] qemu-x86_64 est absent : tentative d'installation automatique…"
    if sudo -n true 2>/dev/null; then
        sudo apt-get install -y qemu-user
        QEMU="$(command -v qemu-x86_64 || true)"
    fi
fi
if [ -z "$QEMU" ]; then
    echo "[REFUS nommé] qemu-x86_64 est introuvable — la commande exacte :"
    echo "        sudo apt install qemu-user     (ou qemu-user-static)"
    echo "        puis relancez :  bash lancer-voie2-shani.sh"
    exit 2
fi
echo "[qemu] $QEMU"

KIT="../pc-windows/kit-1-shani"
if [ ! -f "$KIT/scenario-shani.py" ]; then
    echo "[REFUS] le kit-1-shani est introuvable au voisinage ($KIT) —"
    echo "        extrayez le zip COMPLET du paquet dans un dossier NEUF"
    echo "        (D99 : ne mélangez jamais les runs)."
    exit 2
fi

PY3=""
command -v python3 >/dev/null 2>&1 && PY3="$(command -v python3)"
if [ -z "$PY3" ]; then
    command -v python >/dev/null 2>&1 && PY3="$(command -v python)"
fi
if [ -z "$PY3" ]; then
    echo "[REFUS nommé] python3 est introuvable — installez-le vous-même :"
    echo "        sudo apt install python3    puis relancez ce lanceur."
    exit 2
fi

echo "[run] le kit-1-shani sous émulation — une à deux minutes…"
cd "$KIT" || exit 2
"$QEMU" -cpu max "$PY3" scenario-shani.py
RC=$?

echo "==================================================================="
echo " LE RUN EST TERMINÉ (code $RC). Les preuves vivent dans preuves-shani/"
echo " (du dossier kit-1-shani)."
echo " À VOTRE MAIN : datez et signez le témoin en écrivant sous votre main :"
echo "   « run sous qemu-x86_64 -cpu max, ÉMULATION, pas le silicium »"
echo " Le rapport rendu (probablement < 1) est l'artefact TCG : consignez-le"
echo " tel quel. Renvoyez le dossier ENTIER au coffre /test."
echo "==================================================================="
exit $RC
