#!/usr/bin/env bash
# verifier-kit-arm.sh — LE RECOUP DES EMPREINTES (l'édition TÉLÉPHONE).
# Le geste :  bash verifier-kit-arm.sh
# Chaque pièce du kit est recoupée contre EMPREINTES-KIT-ARM.txt (la
# table posée par le labo au moment de l'assemblage du paquet). Un
# écart est un REFUS NOMMÉ : rien ne s'exécute tant que la pièce n'est
# pas la pièce du labo (le même geste que VERIFIER-PAQUET.bat au
# correctif 3 — l'instrument ne fait confiance à personne).

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE RECOUP DES EMPREINTES — édition TÉLÉPHONE v1.0.0"
echo "==================================================================="

if [ ! -f EMPREINTES-KIT-ARM.txt ]; then
    echo "[REFUS] EMPREINTES-KIT-ARM.txt est ABSENT du dossier — copiez le"
    echo "        paquet COMPLET dans un dossier NEUF (D99)."
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "[REFUS nommé] sha256sum est introuvable — dans Termux :"
    echo "        pkg install coreutils   puis relancez."
    exit 2
fi

sha256sum -c EMPREINTES-KIT-ARM.txt
RC=$?
echo "==================================================================="
if [ "$RC" -eq 0 ]; then
    echo " TOUTES les pièces recoupées : le paquet est le paquet du labo."
else
    echo " UN ÉCART EST NOMMÉ CI-DESSUS : une pièce a bougé ou manque —"
    echo " re-extrayez le zip COMPLET dans un dossier NEUF (D99) ; si"
    echo " l'écart demeure, renvoyez cet écran TEL QUEL (D122)."
fi
echo "==================================================================="
exit $RC
