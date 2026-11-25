#!/usr/bin/env bash
# verifier-kit-oracle.sh — LE RECOUP DES EMPREINTES (l'édition ORACLE).
# Le geste :  bash verifier-kit-oracle.sh
# Chaque pièce du kit est recoupée contre EMPREINTES-KIT-ORACLE.txt (la
# table posée par le labo au moment de l'assemblage du paquet). Un
# écart est un REFUS NOMMÉ : rien ne s'exécute tant que la pièce n'est
# pas la pièce du labo (le même geste que verifier-kit-arm.sh à
# l'édition TÉLÉPHONE — l'instrument ne fait confiance à personne).

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE RECOUP DES EMPREINTES — édition ORACLE ARM64 v1.0.0"
echo "==================================================================="

if [ ! -f EMPREINTES-KIT-ORACLE.txt ]; then
    echo "[REFUS] EMPREINTES-KIT-ORACLE.txt est ABSENT du dossier —"
    echo "        dézippez le paquet COMPLET (D99)."
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "[REFUS nommé] sha256sum est introuvable — sur Ubuntu :"
    echo "        sudo apt-get install -y coreutils   puis relancez."
    exit 2
fi

sha256sum -c EMPREINTES-KIT-ORACLE.txt
RC=$?
echo "==================================================================="
if [ "$RC" -eq 0 ]; then
    echo " TOUTES les pièces recoupées : le paquet est le paquet du labo."
    echo " (dudect_arm.c EST la pièce du kit-B téléphone, byte-pour-byte :"
    echo "  08681278e0efe013ff9e6379eff8ea02219f04a6bdbcb59b4a5d2a1016474a32)"
else
    echo " UN ÉCART EST NOMMÉ CI-DESSUS : une pièce a bougé ou manque —"
    echo " re-extrayez le zip COMPLET (D99) ; si l'écart demeure,"
    echo " renvoyez cet écran TEL QUEL (D122)."
fi
echo "==================================================================="
exit $RC
