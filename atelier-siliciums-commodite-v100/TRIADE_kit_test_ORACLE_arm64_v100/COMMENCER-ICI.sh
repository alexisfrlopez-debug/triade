#!/usr/bin/env bash
# COMMENCER-ICI.sh — LA PORTE D'ENTRÉE DE L'ÉDITION ORACLE ARM64 v1.0.0
# (25/11/2026 — la commande du développeur : « si tu as des idées pour des
# siliciums supplémentaires du même type que google collab (environnement
# gratuit en ligne, mais hardware différent) fais moi les packs de test
# correspondants »)
#
# LE GESTE : sur la VM Ampere A1 (Ubuntu), après avoir dézippé le paquet :
#     bash TRIADE_kit_test_ORACLE_arm64_v100/COMMENCER-ICI.sh
# Ce script vérifie d'abord les empreintes du paquet (chaque pièce
# recoupée contre la table du labo), puis lance le kit-B-oracle : les
# quatre cibles du protocole ORACLE-ARM-1 (l'égalation du
# TELEPHONE-ARM-1 : les deux contrôles, SHA-256 logiciel et — si le noyau
# expose « sha2 » — FEAT_SHA256), classes entrelacées, N=60/200/400 dans
# l'ordre imposé. AUCUNE question interactive : le run vit entier, les
# témoins naissent tout seuls dans preuves-dudect-arm/.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " TRIADE — LE KIT-B DUDECT-ORACLE (l'édition ORACLE ARM64)"
echo " v1.0.0 — 25/11/2026. Le silicium : Ampere A1 (Neoverse N1, OCPUs"
echo " DÉDIÉS — la machine de commodité se nomme, D206 : hôte physique"
echo " mutualisé, DVFS opaque). Aucun réseau hors l'installation"
echo " éventuelle des paquets (apt-get)."
echo "==================================================================="
echo " A-LIRE-EDITION-ORACLE.txt dit le périmètre ET le guide"
echo " d'inscription Always Free ; le LISEZMOI-dudect-oracle.txt demeure"
echo " LA RÉFÉRENCE : le lanceur fait les gestes, le LISEZMOI dit"
echo " pourquoi. Un dossier NEUF par machine (D99)."
echo "==================================================================="
echo ""
echo "[étape 0] le recoup des empreintes du paquet…"
if bash verifier-kit-oracle.sh; then
    echo "[étape 0] le paquet est intègre."
else
    echo ""
    echo "[REFUS] une pièce du paquet a bougé ou manque — RIEN ne sera"
    echo "        exécuté. Re-extrayez le zip COMPLET (D99) ; si l'écart"
    echo "        demeure, renvoyez l'écran TEL QUEL (D122)."
    exit 2
fi

echo ""
echo "[étape 1] le kit-B-oracle : le run du silicium serveur ARM64"
echo "          (quelques minutes, OCPUs dédiés)…"
bash oracle-arm64/kit-B-dudect-arm-oracle/lancer-kit-B-dudect-ORACLE.sh
exit $?
