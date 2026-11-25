#!/usr/bin/env bash
# verifier-kit-kaggle.sh — LE RECOUP DES EMPREINTES (l'édition KAGGLE).
# Le geste :  bash verifier-kit-kaggle.sh
# Chaque pièce du kit est recoupée contre EMPREINTES-KIT-KAGGLE.txt (la
# table posée par le labo au moment de l'assemblage du paquet). Un
# écart est un REFUS NOMMÉ : rien ne s'exécute tant que la pièce n'est
# pas la pièce du labo (le même geste que verifier-kit-collab.sh à
# l'édition COLLAB et verifier-kit-arm.sh à l'édition TÉLÉPHONE —
# l'instrument ne fait confiance à personne).

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE RECOUP DES EMPREINTES — édition KAGGLE x86-64 v1.0.0"
echo "==================================================================="

if [ ! -f EMPREINTES-KIT-KAGGLE.txt ]; then
    echo "[REFUS] EMPREINTES-KIT-KAGGLE.txt est ABSENT du dossier —"
    echo "        dézippez le paquet COMPLET (D99)."
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "[REFUS nommé] sha256sum est introuvable — sur Kaggle :"
    echo "        !apt-get install -y coreutils   puis relancez."
    exit 2
fi

sha256sum -c EMPREINTES-KIT-KAGGLE.txt
RC=$?
echo "==================================================================="
if [ "$RC" -eq 0 ]; then
    echo " TOUTES les pièces recoupées : le paquet est le paquet du labo."
    echo " (l'image scellée cibles/proxy-image.bin EST la pièce du coffre :"
    echo "  0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff"
    echo "  — byte-pour-byte celle de l'édition COLLAB)"
else
    echo " UN ÉCART EST NOMMÉ CI-DESSUS : une pièce a bougé ou manque —"
    echo " re-extrayez le zip COMPLET (D99) ; si l'écart demeure,"
    echo " renvoyez cet écran TEL QUEL (D122)."
fi
echo "==================================================================="
exit $RC
