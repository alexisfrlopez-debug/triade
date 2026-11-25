#!/usr/bin/env bash
# COMMENCER-ICI.sh — LA PORTE D'ENTRÉE DE L'ÉDITION LINUXONE s390x v1.0.0
# (25/11/2026 — la commande du développeur : « si tu as des idées pour des
# siliciums supplémentaires du même type que google collab (environnement
# gratuit en ligne, mais hardware différent) fais moi les packs de test
# correspondants »)
#
# LE GESTE : sur le shell Linux s390x de la porte choisie (Z Xplore ou
# toute autre), après avoir copié le dossier dézippé :
#     bash TRIADE_kit_test_LINUXONE_s390x_v100/COMMENCER-ICI.sh
# Ce script vérifie d'abord les empreintes du paquet (chaque pièce
# recoupée contre la table du labo), puis lance le kit-E-s390x : les
# trois cibles du protocole LINUXONE-S390X-1 (les deux contrôles,
# SHA-256 logiciel — la cible matérielle REFUSÉE PAR NATURE, KIMD/KLMD
# superviseur, nommée), classes entrelacées, N=60/200/400 dans l'ordre
# imposé. AUCUNE question interactive : le run vit entier, les témoins
# naissent tout seuls dans preuves-dudect-s390x/.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " TRIADE — LE KIT-E DUDECT-S390X (l'édition LINUXONE s390x)"
echo " v1.0.0 — 25/11/2026. Le silicium IBM Z, le plus loin de la"
echo " famille : x86, ARM, puis Z. La machine de commodité se nomme"
echo " (D206) : la porte s390x du maître, la cadence gouvernée par le Z,"
echo " le compteur = l'horloge du noyau en NANOSECONDES (nommée)."
echo " Aucun réseau hors l'installation éventuelle des paquets."
echo "==================================================================="
echo " A-LIRE-EDITION-LINUXONE.txt dit le périmètre ET le guide des"
echo " portes gratuites ; le LISEZMOI-dudect-s390x.txt demeure LA"
echo " RÉFÉRENCE : le lanceur fait les gestes, le LISEZMOI dit pourquoi."
echo " Un dossier NEUF par machine (D99)."
echo "==================================================================="
echo ""
echo "[étape 0] le recoup des empreintes du paquet…"
if bash verifier-kit-linuxone.sh; then
    echo "[étape 0] le paquet est intègre."
else
    echo ""
    echo "[REFUS] une pièce du paquet a bougé ou manque — RIEN ne sera"
    echo "        exécuté. Re-extrayez le zip COMPLET (D99) ; si l'écart"
    echo "        demeure, renvoyez l'écran TEL QUEL (D122)."
    exit 2
fi

echo ""
echo "[étape 1] le kit-E-s390x : le run du silicium IBM Z (quelques"
echo "          minutes)…"
bash linuxone-s390x/kit-E-dudect-s390x/lancer-kit-E-dudect-s390x.sh
exit $?
