#!/usr/bin/env bash
# verifier-kit-actions.sh — LE RECOUP DES EMPREINTES (l'édition ACTIONS).
# Le geste :  bash verifier-kit-actions.sh
# Chaque pièce du kit est recoupée contre EMPREINTES-KIT-ACTIONS.txt (la
# table posée par le labo au moment de l'assemblage du paquet). Un
# écart est un REFUS NOMMÉ : rien ne s'exécute tant que la pièce n'est
# pas la pièce du labo (le même geste que verifier-kit-collab.sh —
# l'instrument ne fait confiance à personne). NOTE : le workflow du
# dépôt exécute les enveloppes CI SANS ce recoup préalable (le dépôt
# git EST le recoup : les pièces y vivent sous les yeux du maître) ;
# ce vérificateur sert au paquet ZIP livré au coffre — le geste entier
# demeure disponible au terrain.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE RECOUP DES EMPREINTES — édition ACTIONS multisilicium v1.0.0"
echo "==================================================================="

if [ ! -f EMPREINTES-KIT-ACTIONS.txt ]; then
    echo "[REFUS] EMPREINTES-KIT-ACTIONS.txt est ABSENT du dossier —"
    echo "        dézippez le paquet COMPLET (D99)."
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "[REFUS nommé] sha256sum est introuvable — installez coreutils"
    echo "        puis relancez."
    exit 2
fi

sha256sum -c EMPREINTES-KIT-ACTIONS.txt
RC=$?
echo "==================================================================="
if [ "$RC" -eq 0 ]; then
    echo " TOUTES les pièces recoupées : le paquet est le paquet du labo."
    echo " (kit-C et kit-D sont les pièces COLLAB et TÉLÉPHONE"
    echo "  byte-pour-byte ; kit-G est la pièce neuve, dérivée nommée)"
else
    echo " UN ÉCART EST NOMMÉ CI-DESSUS : une pièce a bougé ou manque —"
    echo " re-extrayez le zip COMPLET (D99) ; si l'écart demeure,"
    echo " renvoyez cet écran TEL QUEL (D122)."
fi
echo "==================================================================="
exit $RC
