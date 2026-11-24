#!/usr/bin/env bash
# COMMENCER-ICI.sh — LA PORTE D'ENTRÉE DE L'ÉDITION TÉLÉPHONE v1.0.0
# (25/11/2026 — la commande du développeur : « tu peux me faire un kit de
# test arm/pour téléphone si nécessaire »)
#
# LE GESTE : dans Termux, tapez   bash COMMENCER-ICI.sh
# Ce script vérifie d'abord les empreintes du paquet (chaque pièce
# recoupée contre la table du labo), puis vous propose les deux kits :
#   kit-A : le CONSTAT (la machine nommée, le silicium lu par ses
#           propres canaux, le lecteur FIPS) — quelques secondes ;
#   kit-B : le TEST (les contrôles de l'instrument, l'invariance de
#           SHA-256 logiciel, et si le noyau expose « sha2 » les
#           instructions matérielles FEAT_SHA256) — quelques minutes.
# L'ordre conseillé : kit-A puis kit-B. Chaque kit écrit ses preuves
# dans son propre dossier — à dater, signer, et renvoyer ENTIERS au
# coffre /test (dossier Drive « Triade »).

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " TRIADE — LE KIT DE TEST DU TROISIÈME SILICIUM (le téléphone)"
echo " Édition TÉLÉPHONE v1.0.0 — 25/11/2026. Termux requis (F-Droid ou"
echo " Play Store ; iOS ne porte pas de Python libre). Aucun réseau"
echo " hors l'installation éventuelle des paquets (pkg). Aucun droit."
echo "==================================================================="
echo " A-LIRE-EDITION-TELEPHONE.txt dit le périmètre ; chaque LISEZMOI"
echo " de kit demeure LA RÉFÉRENCE : le lanceur fait les gestes, le"
echo " LISEZMOI dit pourquoi. Un dossier NEUF par machine (D99)."
echo "==================================================================="
echo ""
echo "[étape 0] le recoup des empreintes du paquet…"
if bash verifier-kit-arm.sh; then
    echo "[étape 0] le paquet est intègre."
else
    echo ""
    echo "[REFUS] une pièce du paquet a bougé ou manque — RIEN ne sera"
    echo "        exécuté. Re-extrayez le zip COMPLET dans un dossier"
    echo "        NEUF (D99) ; si l'écart demeure, renvoyez l'écran TEL"
    echo "        QUEL (D122)."
    exit 2
fi

echo ""
echo "QUE VOULEZ-VOUS VIVRE ?"
echo "  1) kit-A : le constat   (quelques secondes)"
echo "  2) kit-B : le test      (quelques minutes)"
echo "  3) les deux, dans l'ordre conseillé (A puis B)"
echo "  q) quitter"
printf "votre choix [1/2/3/q] : "
read -r choix || exit 0
echo ""

case "$choix" in
    1)
        bash telephone-arm/kit-A-constat/lancer-kit-constat-arm.sh
        ;;
    2)
        bash telephone-arm/kit-B-dudect-arm/lancer-kit-B-dudect-arm.sh
        ;;
    3)
        bash telephone-arm/kit-A-constat/lancer-kit-constat-arm.sh
        echo ""
        echo "[chaîne] le kit-A est vécu — le kit-B suit (Ctrl-C pour"
        echo "         vous arrêter ici : le kit-B se vit aussi seul)."
        echo ""
        bash telephone-arm/kit-B-dudect-arm/lancer-kit-B-dudect-arm.sh
        ;;
    *)
        echo "[sortie] à bientôt — les preuves déjà écrites restent aux"
        echo "        dossiers preuves-constat-arm/ et preuves-dudect-arm/."
        ;;
esac
