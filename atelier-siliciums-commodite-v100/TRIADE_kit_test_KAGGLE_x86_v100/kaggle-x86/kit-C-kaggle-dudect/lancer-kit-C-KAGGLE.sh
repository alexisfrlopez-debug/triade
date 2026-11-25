#!/usr/bin/env bash
# lancer-kit-C-KAGGLE.sh — LE LANCEUR DU KIT-C (l'édition KAGGLE x86-64 du
# kit de test, 25/11/2026 — la commande du développeur : « si tu as des
# idées pour des siliciums supplémentaires du même type que google collab
# (environnement gratuit en ligne, mais hardware différent) »).
#
# LE GESTE : dans une cellule Kaggle :
#     !bash /kaggle/working/TRIADE_kit_test_KAGGLE_x86_v100/COMMENCER-ICI.sh
# (COMMENCER-ICI.sh fait ce travail pour vous — voyez A-LIRE-EDITION-KAGGLE.txt)
#
# Ce lanceur fait pour vous les gestes du LISEZMOI-dudect-kaggle.txt SANS
# VOUS DEMANDER UNE SEULE COMMANDE :
#   1. il trouve Python (python3) — s'il est ABSENT, il tente
#      l'installation (apt-get, le geste Kaggle) ;
#   2. il trouve le compilateur (gcc/clang/cc) — s'il est ABSENT, il
#      INSTALLE gcc AUTOMATIQUEMENT (apt-get install -y gcc — le kit
#      compile la pièce SUR CETTE MACHINE depuis la source : la source
#      est la vérité ; C'EST la seule pièce à compiler : aucun exe
#      précompilé ne vit dans ce kit) ;
#   3. il vit le scénario : l'épreuve FIPS des TROIS lecteurs (logiciel,
#      SHA-NI s'il vit, ET LA PIÈCE SCELLÉE tls13-02 avec l'adversaire de
#      mutation K), puis LES TROIS RUNS dans l'ordre imposé N=60, N=200,
#      N=400 — les témoins et le ZIP DE RETOUR naissent tout seuls dans
#      preuves-kaggle/.
#
# Ce qui reste à VOTRE main : RÉCUPÉRER le zip de retour AVANT LA FIN DE
# LA SESSION (Kaggle est ÉPHÉMÈRE — sauvegardez AUSSI le notebook, le
# dossier /kaggle/working vit dans la version enregistrée), dater et
# signer la synthèse de votre main, puis téléverser le zip ET le scan au
# coffre /test (dossier Drive « Triade »).
#
# LE KIT POSE LA MÊME QUESTION QUE L'ÉDITION COLLAB (l'avis de l'Entrée
# 421) : les trois divergences |t|>5 du 24/11 au portable SUIVENT-ELLES
# LA MACHINE OU LE CODE ? Les QUATRE cibles SCELLÉES de proxy-image.bin
# sont mesurées ici, recoupées avant toute exécution, classes
# ENTRELACÉES — le deuxième point de commodité sur silicium serveur.

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
installer() {   # le geste Kaggle : apt-get (avec sudo silencieux au besoin)
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
echo " LE KIT-C DUDECT-KAGGLE — la même question que l'édition COLLAB :"
echo " les trois divergences du 24/11 suivent-elles LA MACHINE ou LE CODE ?"
echo " Les quatre cibles SCELLÉES de proxy-image.bin (recoupées avant"
echo " exécution), les contrôles de l'instrument, SHA-256 logiciel et —"
echo " si le noyau expose « sha_ni » — les instructions SHA-NI. t de"
echo " Welch, |t|>5, échantillons ENTRELACÉS : le protocole KAGGLE-X86-1"
echo " (l'égalation du COLLAB-X86-1), pré-enregistré au"
echo " LISEZMOI-dudect-kaggle.txt AVANT tout run."
echo " La machine de commodité SE NOMME : silicium MUTUALISÉ aux voisins"
echo " inconnus, accélérateur GPU/TPU CONSTATÉ jamais mesuré, DVFS opaque"
echo " sous l'hyperviseur, session ÉPHÉMÈRE."
echo "==================================================================="
echo " Le kit-C est la MÊME pièce byte-pour-byte que l'édition COLLAB"
echo " (dudect_collab.c, proxy-image.bin, manifestes) ; seul"
echo " l'orchestrateur scenario-kaggle.py est neuf."
echo "==================================================================="

if [ ! -f dudect_collab.c ] || [ ! -f scenario-kaggle.py ] || \
   [ ! -f cibles/proxy-image.bin ] || [ ! -f cibles/manifeste-c.txt ]; then
    echo "[REFUS] une pièce du kit est ABSENTE (dudect_collab.c,"
    echo "        scenario-kaggle.py, cibles/proxy-image.bin ou"
    echo "        cibles/manifeste-c.txt) — dézippez le paquet COMPLET"
    echo "        (D99 : ne mélangez jamais les runs)."
    exit 2
fi

PY="$(trouver_python || true)"
if [ -z "$PY" ]; then
    echo "[lanceur] Python est absent : tentative d'INSTALLATION (apt-get)…"
    if installer python3; then
        PY="$(trouver_python || true)"
    fi
    if [ -z "$PY" ]; then
        echo "[REFUS nommé] l'installation automatique a échoué — tapez"
        echo "        vous-même :  !apt-get install -y python3"
        echo "        puis relancez le lanceur."
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
        echo "        vous-même :  !apt-get install -y gcc"
        echo "        puis relancez le lanceur."
        exit 2
    fi
fi
echo "[compilateur] trouvé : $CC (le scénario compilera avec)"

echo "[run] $PY scenario-kaggle.py — l'épreuve FIPS des trois lecteurs,"
echo "      puis les trois runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-kaggle.py
RC=$?

echo "==================================================================="
echo " LE KIT-C EST TERMINÉ (code $RC). Les preuves vivent dans"
echo " preuves-kaggle/ ET dans le zip de retour preuves-kaggle-<...>.zip."
echo " À VOTRE MAIN, DANS CET ORDRE :"
echo "   1. RÉCUPÉREZ le zip AVANT LA FIN DE LA SESSION (Kaggle est"
echo "      ÉPHÉMÈRE) — onglet Output du panneau droit, le chemin exact"
echo "      est imprimé ci-dessus par le scénario ; SAUVEGARDEZ AUSSI le"
echo "      notebook (Save Version) : /kaggle/working vit dans la version"
echo "      enregistrée."
echo "   2. Datez et signez la synthèse de votre main."
echo "   3. Téléversez le zip ET le scan au coffre /test (dossier Drive"
echo "      « Triade » → « test »)."
echo "==================================================================="
exit $RC
