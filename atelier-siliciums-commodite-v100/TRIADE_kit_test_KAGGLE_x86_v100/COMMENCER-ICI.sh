#!/usr/bin/env bash
# COMMENCER-ICI.sh — LA PORTE D'ENTRÉE DE L'ÉDITION KAGGLE x86-64 v1.0.0
# (25/11/2026 — la commande du développeur : « si tu as des idées pour des
# siliciums supplémentaires du même type que google collab (environnement
# gratuit en ligne, mais hardware différent) fais moi les packs de test
# correspondants »)
#
# LE GESTE : dans une cellule Kaggle :
#     !bash /kaggle/working/TRIADE_kit_test_KAGGLE_x86_v100/COMMENCER-ICI.sh
# Ce script vérifie d'abord les empreintes du paquet (chaque pièce
# recoupée contre la table du labo), puis lance le kit-C-kaggle : LA
# QUESTION du paquet — la même que l'édition COLLAB — vit ses huit cibles
# (les contrôles, SHA-256 logiciel et SHA-NI, et LES QUATRE SCELLÉES de
# proxy-image.bin, recoupées avant exécution), classes entrelacées,
# N=60/200/400 dans l'ordre imposé. AUCUNE question interactive (la
# cellule Kaggle n'a pas d'entrée) : le run vit entier, les témoins et
# le zip de retour naissent tout seuls dans preuves-kaggle/.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " TRIADE — LE KIT-C DUDECT-KAGGLE (l'édition KAGGLE x86-64)"
echo " v1.0.0 — 25/11/2026. La question : la même que l'édition COLLAB —"
echo " les trois divergences du 24/11 suivent-elles LA MACHINE ou LE CODE ?"
echo " La machine de commodité se nomme : silicium MUTUALISÉ, accélérateur"
echo " GPU/TPU CONSTATÉ jamais mesuré, DVFS opaque, session ÉPHÉMÈRE."
echo " Aucun réseau hors l'installation éventuelle des paquets (apt-get)."
echo "==================================================================="
echo " A-LIRE-EDITION-KAGGLE.txt dit le périmètre ; le LISEZMOI-dudect-"
echo " kaggle.txt demeure LA RÉFÉRENCE : le lanceur fait les gestes, le"
echo " LISEZMOI dit pourquoi. Un dossier NEUF par machine (D99)."
echo "==================================================================="
echo ""
echo "[étape 0] le recoup des empreintes du paquet…"
if bash verifier-kit-kaggle.sh; then
    echo "[étape 0] le paquet est intègre."
else
    echo ""
    echo "[REFUS] une pièce du paquet a bougé ou manque — RIEN ne sera"
    echo "        exécuté. Re-extrayez le zip COMPLET (D99) ; si l'écart"
    echo "        demeure, renvoyez l'écran TEL QUEL (D122)."
    exit 2
fi

echo ""
echo "[étape 1] le kit-C-kaggle : le run de LA QUESTION (quelques minutes"
echo "          à silicium partagé)…"
bash kaggle-x86/kit-C-kaggle-dudect/lancer-kit-C-KAGGLE.sh
exit $?
