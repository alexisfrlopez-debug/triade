#!/bin/sh
# TRIADE - lanceur du GUI DE CEREMONIE DE MIGRATION CF2 - CF3 (D127)
# ---------------------------------------------------------------------
# A garder A LA RACINE d'un clone du depot (a cote de v06/), ou du kit
# de ceremonie du Drive (le kit porte v06/ entier depuis D122), puis :
#   double-clic (apres chmod +x), ou ./lancer_migration_cf3.sh
# Le GUI vit dans <racine>/v06/ : il trouve coffre_cf3.py par sa
# position. Ordre de recherche : v06/migration_cf3_gui.py (depot complet
# ou kit du Drive) d'abord, puis toute copie posee a cote (copie plate).
cd "$(dirname "$0")"
if [ -f v06/migration_cf3_gui.py ]; then
    GUI=v06/migration_cf3_gui.py
elif [ -f migration_cf3_gui.py ]; then
    GUI=migration_cf3_gui.py
else
    echo "migration_cf3_gui.py introuvable (ni v06/migration_cf3_gui.py ni ./migration_cf3_gui.py)."
    echo "Ce lanceur vit a la racine d'un CLONE du depot triade (celui qui contient v06/)"
    echo "ou du kit de ceremonie du Drive."
    exit 1
fi
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$GUI" "$@"
else
    echo "python3 introuvable - installez Python 3.8+ (python.org ou votre gestionnaire)."
    exit 1
fi
