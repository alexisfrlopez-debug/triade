#!/usr/bin/env bash
# lancer-kit-B-dudect-ORACLE.sh — LE LANCEUR DU KIT-B (l'édition ORACLE
# ARM64 du kit de test, 25/11/2026 — la commande du développeur : « si tu
# as des idées pour des siliciums supplémentaires du même type que google
# collab (environnement gratuit en ligne, mais hardware différent) »).
#
# LE GESTE : tapez   bash lancer-kit-B-dudect-ORACLE.sh
# (dans la VM :  bash TRIADE_kit_test_ORACLE_arm64_v100/COMMENCER-ICI.sh
#  fait ce travail pour vous — voyez A-LIRE-EDITION-ORACLE.txt)
#
# Ce lanceur fait pour vous les gestes du LISEZMOI-dudect-oracle.txt SANS
# VOUS DEMANDER UNE SEULE COMMANDE :
#   1. il trouve Python (python3) — s'il est ABSENT, il l'INSTALLE
#      AUTOMATIQUEMENT (apt-get) ;
#   2. il trouve le compilateur (gcc/clang) — s'il est ABSENT, il
#      INSTALLE gcc AUTOMATIQUEMENT (apt-get install -y gcc — le kit
#      compile la pièce SUR CETTE MACHINE depuis la source : la source
#      est la vérité ; C'EST la seule pièce à compiler : aucun exe
#      précompilé ne vit dans ce kit, rien ne peut être retiré par un
#      antivirus) ;
#   3. il vit le scénario : l'épreuve FIPS, puis LES TROIS RUNS dans
#      l'ordre imposé N=60, N=200, N=400 — les témoins naissent tout
#      seuls dans preuves-dudect-arm/ (la pièce scenario-dudect-arm.py
#      est BYTE-POUR-BYTE celle du kit-B téléphone : ses écrans finaux
#      parleront du téléphone — le geste Oracle est LE MÊME, nommé).

cd "$(dirname "$0")" || exit 2

trouver_python() {
    if command -v python3 >/dev/null 2>&1; then echo python3; return 0; fi
    if command -v python >/dev/null 2>&1; then echo python; return 0; fi
    return 1
}
trouver_cc() {
    for c in gcc clang cc; do
        if command -v "$c" >/dev/null 2>&1; then echo "$c"; return 0; fi
    done
    return 1
}
installer() {   # le geste serveur : apt-get (sudo silencieux au besoin)
    if command -v apt-get >/dev/null 2>&1; then
        if command -v sudo >/dev/null 2>&1; then
            sudo -n apt-get update -y && sudo -n apt-get install -y "$@"
        else
            apt-get update -y && apt-get install -y "$@"
        fi
        return $?
    fi
    return 1
}

echo "==================================================================="
echo " LE KIT-B DUDECT-ORACLE — le test du silicium serveur ARM64"
echo " (Ampere A1, offre Always Free d'Oracle Cloud)."
echo " Les contrôles de l'instrument, SHA-256 logiciel, et — si le noyau"
echo " expose « sha2 » — les instructions FEAT_SHA256. t de Welch, |t|>5,"
echo " échantillons entrelacés : le protocole ORACLE-ARM-1 (l'égalation du"
echo " TELEPHONE-ARM-1), pré-enregistré au LISEZMOI-dudect-oracle.txt"
echo " AVANT tout run."
echo " La machine de commodité SE NOMME (D206) : OCPUs DÉDIÉS (pas de"
echo " voisins de session), hôte physique mutualisé, DVFS opaque."
echo "==================================================================="
echo " La pièce est BYTE-POUR-BYTE celle du kit-B téléphone (dudect_arm.c"
echo " scellé 08681278…) ; seul le présent lanceur et son LISEZMOI sont"
echo " neufs. Un dossier NEUF par machine (D99)."
echo "==================================================================="

if [ ! -f dudect_arm.c ] || [ ! -f scenario-dudect-arm.py ]; then
    echo "[REFUS] une pièce du kit est ABSENTE (dudect_arm.c ou"
    echo "        scenario-dudect-arm.py) — dézippez le paquet COMPLET"
    echo "        (D99 : ne mélangez jamais les runs)."
    exit 2
fi

PY="$(trouver_python || true)"
if [ -z "$PY" ]; then
    echo "[lanceur] Python est absent : INSTALLATION AUTOMATIQUE (apt-get)…"
    if installer python3; then
        PY="$(trouver_python || true)"
    fi
    if [ -z "$PY" ]; then
        echo "[REFUS nommé] l'installation automatique a échoué — tapez"
        echo "        vous-même :  sudo apt-get install -y python3"
        echo "        puis relancez :  bash lancer-kit-B-dudect-ORACLE.sh"
        exit 2
    fi
fi
echo "[python] trouvé : $PY"

CC="$(trouver_cc || true)"
if [ -z "$CC" ]; then
    echo "[lanceur] le compilateur est absent : INSTALLATION AUTOMATIQUE"
    echo "        de gcc (apt-get)… (le kit compile la pièce SUR CETTE"
    echo "        MACHINE : la source est la vérité)"
    if installer gcc; then
        CC="$(trouver_cc || true)"
    fi
    if [ -z "$CC" ]; then
        echo "[REFUS nommé] l'installation automatique a échoué — tapez"
        echo "        vous-même :  sudo apt-get install -y gcc"
        echo "        puis relancez :  bash lancer-kit-B-dudect-ORACLE.sh"
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
echo " (NOTE : scenario-dudect-arm.py est la pièce du kit-B téléphone —"
echo "  ses écrans finaux parlent du téléphone : LE GESTE Oracle est le"
echo "  même, nommé, jamais muet.)"
echo " À VOTRE MAIN : datez et signez la synthèse de votre main, puis"
echo " renvoyez le dossier ENTIER au coffre /test (dossier Drive"
echo " « Triade ») — et RAPATRIEZ les pièces de la VM : la gratuité"
echo " d'Oracle peut réclamer les machines inactives, nommé."
echo "==================================================================="
exit $RC
