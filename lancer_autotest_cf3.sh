#!/bin/sh
# TRIADE - lanceur du PUPITRE D'AUTOTEST CF3 (D122)
# ---------------------------------------------------------------------
# A garder A LA RACINE d'un clone du depot (a cote de v06/), ou du kit
# de ceremonie du Drive (le kit porte v06/ entier depuis D122), puis :
#   double-clic (apres chmod +x), ou ./lancer_autotest_cf3.sh
# Le pupitre vit dans <racine>/v06/ : il trouve coffre_cf3.py par sa
# position. Ordre de recherche : v06/autotest_cf3_gui.py (depot complet
# ou kit du Drive) d'abord, puis toute copie de autotest_cf3_gui.py
# posee a cote (copie plate - seul l'autotest embarque 28 est alors
# disponible, la suite complete exige le dossier v06/).
cd "$(dirname "$0")"
if [ -f v06/autotest_cf3_gui.py ]; then
    PUPITRE=v06/autotest_cf3_gui.py
elif [ -f autotest_cf3_gui.py ]; then
    PUPITRE=autotest_cf3_gui.py
else
    echo "autotest_cf3_gui.py introuvable (ni v06/autotest_cf3_gui.py ni ./autotest_cf3_gui.py)."
    echo "Ce lanceur vit a la racine d'un CLONE du depot triade (celui qui contient v06/)"
    echo "ou du kit de ceremonie du Drive."
    exit 1
fi
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$PUPITRE" "$@"
else
    echo "python3 introuvable - installez Python 3.8+ (python.org ou votre gestionnaire)."
    exit 1
fi
