#!/usr/bin/env bash
# lancer-kit-E-dudect-s390x.sh — LE LANCEUR DU KIT-E (l'édition LINUXONE
# s390x du kit de test, 25/11/2026 — la commande du développeur : « si tu
# as des idées pour des siliciums supplémentaires du même type que google
# collab (environnement gratuit en ligne, mais hardware différent) »).
#
# LE GESTE : tapez   bash lancer-kit-E-dudect-s390x.sh
# Ce lanceur fait pour vous les gestes du LISEZMOI-dudect-s390x.txt SANS
# VOUS DEMANDER UNE SEULE COMMANDE :
#   1. il trouve Python (python3) — s'il est ABSENT, il tente
#      l'installation par le gestionnaire de paquets disponible
#      (apt-get/dnf/zypper — selon la distribution du shell) ;
#   2. il trouve le compilateur (gcc/clang) — s'il est ABSENT, il tente
#      l'installation de gcc (le kit compile la pièce SUR CETTE MACHINE
#      depuis la source : la source est la vérité ; C'EST la seule pièce
#      à compiler : aucun exe précompilé ne vit dans ce kit) ;
#      SI aucune installation n'est possible (porte d'apprentissage aux
#      paquets figés) : REFUS NOMMÉ — le kit ne mesure rien, il refuse ;
#      l'écran se renvoie TEL QUEL (D122) ;
#   3. il vit le scénario : l'épreuve FIPS, puis LES TROIS RUNS dans
#      l'ordre imposé N=60, N=200, N=400 — les témoins naissent tout
#      seuls dans preuves-dudect-s390x/.

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
installer() {   # le geste selon la distribution du shell
    for pkg in apt-get dnf zypper; do
        if command -v "$pkg" >/dev/null 2>&1; then
            case "$pkg" in
                apt-get)
                    if command -v sudo >/dev/null 2>&1; then
                        sudo -n apt-get update -y && sudo -n apt-get install -y "$@"
                    else
                        apt-get update -y && apt-get install -y "$@"
                    fi ;;
                dnf)
                    if command -v sudo >/dev/null 2>&1; then
                        sudo -n dnf install -y "$@"
                    else
                        dnf install -y "$@"
                    fi ;;
                zypper)
                    if command -v sudo >/dev/null 2>&1; then
                        sudo -n zypper --non-interactive install "$@"
                    else
                        zypper --non-interactive install "$@"
                    fi ;;
            esac
            return $?
        fi
    done
    return 1
}

echo "==================================================================="
echo " LE KIT-E DUDECT-S390X — le test du silicium IBM Z (le plus loin"
echo " de la famille). Les contrôles de l'instrument et SHA-256 logiciel"
echo " — la cible matérielle est REFUSÉE PAR NATURE (KIMD/KLMD sont"
echo " SUPERVISEUR — nommée, jamais muette). t de Welch, |t|>5,"
echo " échantillons entrelacés, compteur = l'horloge du noyau en"
echo " NANOSECONDES (nommée) : le protocole LINUXONE-S390X-1,"
echo " pré-enregistré au LISEZMOI-dudect-s390x.txt AVANT tout run."
echo " La machine de commodité SE NOMME (D206) : la porte s390x du"
echo " maître (Z Xplore ou toute autre), la cadence gouvernée par le Z."
echo "==================================================================="
echo " La pièce dudect_s390x.c est un DÉRIVÉ NOMMÉ de dudect_arm.c (le"
echo " kit-B téléphone) : la même mécanique, les écarts nommés au"
echo " LISEZMOI. Un dossier NEUF par machine (D99)."
echo "==================================================================="

if [ ! -f dudect_s390x.c ] || [ ! -f scenario-dudect-s390x.py ]; then
    echo "[REFUS] une pièce du kit est ABSENTE (dudect_s390x.c ou"
    echo "        scenario-dudect-s390x.py) — copiez le dossier"
    echo "        kit-E-dudect-s390x/ ENTIER (D99 : ne mélangez jamais"
    echo "        les runs)."
    exit 2
fi

PY="$(trouver_python || true)"
if [ -z "$PY" ]; then
    echo "[lanceur] Python est absent : tentative d'INSTALLATION…"
    if installer python3; then
        PY="$(trouver_python || true)"
    fi
    if [ -z "$PY" ]; then
        echo "[REFUS nommé] Python est introuvable et l'installation a"
        echo "        échoué (une porte d'apprentissage peut figer les"
        echo "        paquets) — installez-le vous-même puis relancez ;"
        echo "        sinon l'écran se renvoie TEL QUEL (D122)."
        exit 2
    fi
fi
echo "[python] trouvé : $PY"

CC="$(trouver_cc || true)"
if [ -z "$CC" ]; then
    echo "[lanceur] le compilateur est absent : tentative d'INSTALLATION"
    echo "        de gcc… (le kit compile la pièce SUR CETTE MACHINE :"
    echo "        la source est la vérité)"
    if installer gcc; then
        CC="$(trouver_cc || true)"
    fi
    if [ -z "$CC" ]; then
        echo "[REFUS nommé] aucun compilateur et l'installation a échoué"
        echo "        (une porte d'apprentissage peut figer les paquets)"
        echo "        — le kit ne peut RIEN mesurer : il REFUSE. Renvoyez"
        echo "        cet écran TEL QUEL au coffre /test (D122) : l'écart"
        echo "        est un résultat, D189."
        exit 2
    fi
fi
echo "[compilateur] trouvé : $CC (le scénario compilera avec)"

echo "[run] $PY scenario-dudect-s390x.py — l'épreuve FIPS, puis les trois"
echo "      runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-dudect-s390x.py
RC=$?

echo "==================================================================="
echo " LE KIT-E EST TERMINÉ (code $RC). Les preuves vivent dans"
echo " preuves-dudect-s390x/ (journal, épreuve FIPS, trois sorties, trois"
echo " csv, trois témoins, synthèse)."
echo " À VOTRE MAIN : datez et signez la synthèse de votre main, puis"
echo " renvoyez le dossier ENTIER au coffre /test (dossier Drive"
echo " « Triade » → « test »)."
echo "==================================================================="
exit $RC
