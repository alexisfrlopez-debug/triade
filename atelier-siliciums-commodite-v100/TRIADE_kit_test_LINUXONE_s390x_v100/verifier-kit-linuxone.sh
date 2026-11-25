#!/usr/bin/env bash
# verifier-kit-linuxone.sh — LE RECOUP DES EMPREINTES (l'édition LINUXONE).
# Le geste :  bash verifier-kit-linuxone.sh
# Chaque pièce du kit est recoupée contre EMPREINTES-KIT-LINUXONE.txt (la
# table posée par le labo au moment de l'assemblage du paquet). Un
# écart est un REFUS NOMMÉ : rien ne s'exécute tant que la pièce n'est
# pas la pièce du labo (le même geste que verifier-kit-arm.sh —
# l'instrument ne fait confiance à personne).

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE RECOUP DES EMPREINTES — édition LINUXONE s390x v1.0.0"
echo "==================================================================="

if [ ! -f EMPREINTES-KIT-LINUXONE.txt ]; then
    echo "[REFUS] EMPREINTES-KIT-LINUXONE.txt est ABSENT du dossier —"
    echo "        dézippez le paquet COMPLET (D99)."
    exit 2
fi
if ! command -v sha256sum >/dev/null 2>&1; then
    echo "[REFUS nommé] sha256sum est introuvable — installez coreutils"
    echo "        par le gestionnaire de paquets, puis relancez."
    exit 2
fi

sha256sum -c EMPREINTES-KIT-LINUXONE.txt
RC=$?
echo "==================================================================="
if [ "$RC" -eq 0 ]; then
    echo " TOUTES les pièces recoupées : le paquet est le paquet du labo."
    echo " (dudect_s390x.c est le DÉRIVÉ NOMMÉ de dudect_arm.c : scellé"
    echo "  a9f702a3c2d337bb50217f134a7535f16e1da0ad7afd53ba4b0cac9e56a67301)"
else
    echo " UN ÉCART EST NOMMÉ CI-DESSUS : une pièce a bougé ou manque —"
    echo " re-extrayez le zip COMPLET (D99) ; si l'écart demeure,"
    echo " renvoyez cet écran TEL QUEL (D122)."
fi
echo "==================================================================="
exit $RC
