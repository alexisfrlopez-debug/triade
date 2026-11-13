#!/usr/bin/env bash
# lancer-voie1-m7d.sh — LE LANCEUR DE LA VOIE 1 QEMU : le kit M7D rejoué
# sous qemu-riscv64 (l'édition AUTOMATISÉE du paquet multimachines, 12/11).
#
# LE GESTE : tapez   bash lancer-voie1-m7d.sh
# Le kit M7D est AUTONOME : le qemu-riscv64 STATIQUE est EMBARQUÉ (aucun
# paquet à installer, aucun réseau, aucun root). Ce lanceur trouve Python 3
# (il tente même de l'installer si sudo vit sans mot de passe), lance le
# scénario scenario-m7d.py et vous dit où sont les preuves.
#
# LA FRONTIÈRE NOMMÉE (D149, elle demeure) : c'est une REPRODUCTION de la
# preuve M7 sous émulation TCG — jamais le métal. La question silicium du
# kit 2 v0.15.0 (fence.i sur une VRAIE carte RV64) reste OUVERTE.
#
# Ce qui reste à VOTRE main : dater et signer le témoin de votre main, puis
# renvoyer le dossier preuves-m7/ ENTIER au coffre /test (dossier Drive
# « Triade »).

cd "$(dirname "$0")/kit-m7d" || exit 2

echo "==================================================================="
echo " LA VOIE 1 QEMU — le kit M7D rejoué (la bascule fence.i, l'ISA RISC-V,"
echo " l'adversaire DEP, les refus nommés) sous le qemu-riscv64 EMBARQUÉ."
echo " La réserve instrumentale D149 DÉMEURE : le TCG n'a pas de cache"
echo " d'instructions physique — une reproduction, jamais le métal."
echo "==================================================================="

if [ ! -f scenario-m7d.py ]; then
    echo "[REFUS] scenario-m7d.py est ABSENT — extrayez le zip COMPLET du"
    echo "        paquet dans un dossier NEUF (D99 : ne mélangez jamais les"
    echo "        runs)."
    exit 2
fi
if [ ! -f qemu-riscv64 ]; then
    echo "[REFUS] le qemu-riscv64 EMBARQUÉ est ABSENT — extrayez le zip"
    echo "        COMPLET du paquet en mode BINAIRE (pas « texte »), dans un"
    echo "        dossier NEUF."
    exit 2
fi

PY3=""
command -v python3 >/dev/null 2>&1 && PY3="$(command -v python3)"
if [ -z "$PY3" ]; then
    command -v python >/dev/null 2>&1 && PY3="$(command -v python)"
fi
if [ -z "$PY3" ]; then
    echo "[lanceur] python3 est absent : tentative d'installation automatique…"
    if sudo -n true 2>/dev/null; then
        sudo apt-get install -y python3
        command -v python3 >/dev/null 2>&1 && PY3="$(command -v python3)"
    fi
fi
if [ -z "$PY3" ]; then
    echo "[REFUS nommé] python3 est introuvable — installez-le vous-même :"
    echo "        sudo apt install python3    puis relancez ce lanceur."
    exit 2
fi
echo "[python] $PY3"

echo "[run] $PY3 scenario-m7d.py — environ une minute…"
"$PY3" scenario-m7d.py
RC=$?

echo "==================================================================="
echo " LE RUN EST TERMINÉ (code $RC). Les preuves vivent dans"
echo " preuves-m7/ (témoin, journal, verdict)."
echo " À VOTRE MAIN : datez et signez le témoin de votre main, puis renvoyez"
echo " le dossier ENTIER au coffre /test (dossier Drive « Triade »)."
echo "==================================================================="
exit $RC
