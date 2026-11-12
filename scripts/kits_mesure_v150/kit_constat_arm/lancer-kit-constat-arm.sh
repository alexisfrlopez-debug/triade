#!/usr/bin/env bash
# lancer-kit-constat-arm.sh — LE LANCEUR DU KIT CONSTAT-ARM (l'édition
# AUTOMATISÉE du paquet multimachines, 12/11/2026 — la commande du
# développeur : « je veux que l'utilisation soit la plus simple possible,
# en automatisant au maximum »).
#
# LE GESTE : tapez   bash lancer-kit-constat-arm.sh
# Ce lanceur fait pour vous les gestes du LISEZMOI-constat-arm.txt :
#   1. il trouve Python (python / python3) ;
#   2. s'il est ABSENT, il l'INSTALLE AUTOMATIQUEMENT par pkg (Termux) —
#      c'était l'unique étape manuelle du protocole ;
#   3. il lance constat-arm.py (quelques secondes, aucun réseau, aucun
#      droit particulier).
#
# Ce qui reste à VOTRE main : dater et signer le verdict de votre main, puis
# renvoyer le dossier preuves-constat-arm/ ENTIER au coffre /test (dossier
# Drive « Triade »). Le kit CONSTATE (la machine, le silicium, le lecteur
# FIPS) — il ne mesure rien et ne fabrique aucun chiffre.

cd "$(dirname "$0")" || exit 2

trouver_python() {
    if command -v python >/dev/null 2>&1; then echo python; return 0; fi
    if command -v python3 >/dev/null 2>&1; then echo python3; return 0; fi
    return 1
}

echo "==================================================================="
echo " LE KIT CONSTAT-ARM — le troisième silicium (le téléphone)"
echo " La machine nommée, le silicium lu par ses propres canaux, le refus"
echo " des pièces x86-64 nommé, le lecteur FIPS exact. Un constat, jamais"
echo " une mesure fabriquée."
echo "==================================================================="

if [ ! -f constat-arm.py ]; then
    echo "[REFUS] constat-arm.py est ABSENT du dossier — copiez le dossier"
    echo "        kit-constat-arm/ ENTIER sur le téléphone (D99 : ne mélangez"
    echo "        jamais les runs)."
    exit 2
fi

PY="$(trouver_python || true)"
if [ -z "$PY" ]; then
    if command -v pkg >/dev/null 2>&1; then
        echo "[lanceur] Python est absent : INSTALLATION AUTOMATIQUE (pkg)…"
        pkg update -y && pkg install -y python
        PY="$(trouver_python || true)"
        if [ -z "$PY" ]; then
            echo "[REFUS nommé] l'installation automatique a échoué — tapez"
            echo "        vous-même :  pkg update && pkg install python"
            echo "        puis relancez :  bash lancer-kit-constat-arm.sh"
            exit 2
        fi
    else
        echo "[REFUS nommé] Python est introuvable et pkg (Termux) aussi — ce"
        echo "        kit vit sous Termux (F-Droid ou Play Store) ; voyez le"
        echo "        LISEZMOI-constat-arm.txt, section LE PROTOCOLE."
        exit 2
    fi
fi
echo "[python] trouvé : $PY"

echo "[run] $PY constat-arm.py — quelques secondes…"
"$PY" constat-arm.py
RC=$?

echo "==================================================================="
echo " LE RUN EST TERMINÉ (code $RC). Les preuves vivent dans"
echo " preuves-constat-arm/ (journal + verdict auto-portant)."
echo " À VOTRE MAIN : datez et signez le verdict de votre main, puis"
echo " renvoyez le dossier ENTIER au coffre /test (dossier Drive « Triade »)."
echo "==================================================================="
exit $RC
