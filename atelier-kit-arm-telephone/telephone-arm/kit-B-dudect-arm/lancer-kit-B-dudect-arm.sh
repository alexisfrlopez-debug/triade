#!/usr/bin/env bash
# lancer-kit-B-dudect-arm.sh — LE LANCEUR DU KIT-B (l'édition TÉLÉPHONE du
# kit de test, 25/11/2026 — la commande du développeur : « tu peux me faire
# un kit de test arm/pour téléphone si nécessaire »).
#
# LE GESTE : tapez   bash lancer-kit-B-dudect-arm.sh
# Ce lanceur fait pour vous les gestes du LISEZMOI-dudect-arm.txt SANS
# VOUS DEMANDER UNE SEULE COMMANDE :
#   1. il trouve Python (python / python3) — s'il est ABSENT, il
#      l'INSTALLE AUTOMATIQUEMENT par pkg (Termux) ;
#   2. il trouve le compilateur (clang / gcc / cc) — s'il est ABSENT, il
#      INSTALLE clang AUTOMATIQUEMENT par pkg (le kit compile la pièce
#      SUR CETTE MACHINE depuis la source — la source est la vérité ;
#      C'EST la seule pièce à compiler : aucun exe précompilé ne vit
#      dans ce kit, rien ne peut être retiré par un antivirus) ;
#   3. il vit le scénario : l'épreuve FIPS, puis LES TROIS RUNS dans
#      l'ordre imposé N=60, N=200, N=400 — les témoins naissent tout
#      seuls dans preuves-dudect-arm/ (plus rien à copier à la main :
#      l'automatisation du correctif n° 3, conduite jusqu'au bout).
#
# Ce qui reste à VOTRE main : dater et signer la synthèse de votre main,
# puis renvoyer le dossier preuves-dudect-arm/ ENTIER au coffre /test
# (dossier Drive « Triade »). Le kit ÉPROUVE : les contrôles de
# l'instrument, l'invariance de SHA-256 logiciel et — si le noyau expose
# « sha2 » — des instructions matérielles FEAT_SHA256 (UNE AUTRE famille
# que la SHA-NI x86 : les deux mondes se constatent, aucun ne se déguise).

cd "$(dirname "$0")" || exit 2

trouver_python() {
    if command -v python >/dev/null 2>&1; then echo python; return 0; fi
    if command -v python3 >/dev/null 2>&1; then echo python3; return 0; fi
    return 1
}
trouver_cc() {
    for c in clang gcc cc; do
        if command -v "$c" >/dev/null 2>&1; then echo "$c"; return 0; fi
    done
    return 1
}

echo "==================================================================="
echo " LE KIT-B DUDECT-ARM — le test du troisième silicium (le téléphone)"
echo " Les contrôles de l'instrument, SHA-256 logiciel, et — si le noyau"
echo " expose « sha2 » — les instructions FEAT_SHA256. t de Welch, |t|>5,"
echo " échantillons entrelacés : le protocole TELEPHONE-ARM-1, pré-enregistré"
echo " au LISEZMOI-dudect-arm.txt AVANT tout run."
echo "==================================================================="

if [ ! -f dudect_arm.c ] || [ ! -f scenario-dudect-arm.py ]; then
    echo "[REFUS] une pièce du kit est ABSENTE (dudect_arm.c ou"
    echo "        scenario-dudect-arm.py) — copiez le dossier"
    echo "        kit-B-dudect-arm/ ENTIER sur le téléphone (D99 : ne"
    echo "        mélangez jamais les runs)."
    exit 2
fi

PY="$(trouver_python || true)"
if [ -z "$PY" ]; then
    if command -v pkg >/dev/null 2>&1; then
        echo "[lanceur] Python est absent : INSTALLATION AUTOMATIQUE (pkg)…"
        pkg update -y && pkg install -y python
        PY="$(trouver_python || true)"
        if [ -z "$PY" ]; then
            echo "[REFUS nommé] l'installation automatique a échoué — tapez"
            echo "        vous-même :  pkg update && pkg install python"
            echo "        puis relancez :  bash lancer-kit-B-dudect-arm.sh"
            exit 2
        fi
    else
        echo "[REFUS nommé] Python est introuvable et pkg (Termux) aussi —"
        echo "        ce kit vit sous Termux (F-Droid ou Play Store) ;"
        echo "        voyez le LISEZMOI-dudect-arm.txt."
        exit 2
    fi
fi
echo "[python] trouvé : $PY"

CC="$(trouver_cc || true)"
if [ -z "$CC" ]; then
    if command -v pkg >/dev/null 2>&1; then
        echo "[lanceur] le compilateur est absent : INSTALLATION AUTOMATIQUE"
        echo "        de clang (pkg)… (quelques dizaines de Mo — le kit"
        echo "        compile la pièce SUR CETTE MACHINE : la source est la"
        echo "        vérité)"
        pkg update -y && pkg install -y clang
        CC="$(trouver_cc || true)"
        if [ -z "$CC" ]; then
            echo "[REFUS nommé] l'installation automatique a échoué — tapez"
            echo "        vous-même :  pkg install clang"
            echo "        puis relancez :  bash lancer-kit-B-dudect-arm.sh"
            exit 2
        fi
    else
        echo "[REFUS nommé] aucun compilateur (clang/gcc) et pkg (Termux)"
        echo "        aussi — ce kit vit sous Termux ; voyez le"
        echo "        LISEZMOI-dudect-arm.txt."
        exit 2
    fi
fi
echo "[compilateur] trouvé : $CC (le scénario compilera avec)"

echo "[run] $PY scenario-dudect-arm.py — l'épreuve FIPS, puis les trois"
echo "      runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-dudect-arm.py
RC=$?

echo "==================================================================="
echo " LE KIT-B EST TERMINÉ (code $RC). Les preuves vivent dans"
echo " preuves-dudect-arm/ (journal, épreuve FIPS, trois sorties, trois"
echo " csv, trois témoins, synthèse)."
echo " À VOTRE MAIN : datez et signez la synthèse de votre main, puis"
echo " renvoyez le dossier ENTIER au coffre /test (dossier Drive « Triade »)."
echo "==================================================================="
exit $RC
