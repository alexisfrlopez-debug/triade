#!/bin/sh
# TRIADE - lanceur du MAITRE DE CEREMONIE (D118, edition depot git)
# ---------------------------------------------------------------------
# A garder A LA RACINE d'un clone du depot (a cote de v06/), puis :
#   double-clic (apres chmod +x), ou ./lancer_ceremonie.sh
# Le GUI vit dans <depot>/v06/ : il trouve le depot par sa position.
# Ordre de recherche : v06/ceremonie_gui.py (depot complet) d'abord,
# puis toute copie de ceremonie_gui.py posee a cote (kit du Drive
# reduit, copie "fichier seul sur clef USB" - profil hors-ligne pur).
cd "$(dirname "$0")"
if [ -f v06/ceremonie_gui.py ]; then
    GUI=v06/ceremonie_gui.py
elif [ -f ceremonie_gui.py ]; then
    GUI=ceremonie_gui.py
else
    echo "ceremonie_gui.py introuvable (ni v06/ceremonie_gui.py ni ./ceremonie_gui.py)."
    echo "Ce lanceur vit a la racine d'un CLONE du depot triade (celui qui contient v06/)."
    exit 1
fi
if command -v python3 >/dev/null 2>&1; then
    exec python3 "$GUI" "$@"
else
    echo "python3 introuvable - installez Python 3.8+ (python.org ou votre gestionnaire)."
    exit 1
fi
