#!/usr/bin/env bash
# lancer-kit-G-CI.sh — L'ENVELOPPE CI DU KIT-G (l'édition ACTIONS, job
# APPLE SILICON, 25/11/2026). La pièce (dudect_apple.c,
# scenario-dudect-apple.py) est NEUVE : un DÉRIVÉ NOMMÉ de dudect_arm.c
# (le kit-B téléphone) — la même mécanique, les gardes de portage
# nommées (affinité Linux-seulement, canal /proc absent sur macOS :
# L'ÉPREUVE FIPS DÉCIDE SEULE, fail-closed). Le protocole APPLE-ARM-1
# (l'égalation du TELEPHONE-ARM-1) est PRÉ-ENREGISTRÉ au
# LISEZMOI-dudect-actions.txt de cette édition.
#
# L'ÉTIQUETTE (dite d'abord, pour qu'aucune lecture ne naisse grandie) :
# AUTOTEST-DISTANT — le silicium est RÉEL (le runner macOS Apple Silicon
# de GitHub : les coeurs Firestorm/Icestorm du M1), le geste est celui
# du LABO (le workflow du dépôt public, gratuit) : la hiérarchie
# d'évidence est INCHANGÉE ; ce run est une lecture de commodité,
# JAMAIS le run terrain du développeur.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE KIT-G SUR LE RUNNER macOS APPLE SILICON — ÉTIQUETTE :"
echo " AUTOTEST-DISTANT (le silicium est réel, le geste est celui du"
echo " labo : AUCUN statut terrain n'en découle.) Les contrôles,"
echo " SHA-256 logiciel et — SI le compilateur expose +sha2 et que"
echo " l'ÉPREUVE FIPS l'accepte — FEAT_SHA256 sur Apple Silicon :"
echo " le protocole APPLE-ARM-1, le silicium APPLE pour la première"
echo " fois dans la campagne."
echo "==================================================================="
echo " NOMMÉ D'AVANCE (les écarts du portage, jamais muets) : sur macOS"
echo " le canal /proc/cpuinfo est ABSENT (l'épreuve FIPS décide seule) ;"
echo " l'affinité n'est PAS posable (le t sera bruité, constaté) ;"
echo " l'identité vit au sysctl (machdep.cpu.brand_string)."
echo "==================================================================="

if [ ! -f dudect_apple.c ] || [ ! -f scenario-dudect-apple.py ]; then
    echo "[REFUS] une pièce du kit est ABSENTE — le dépôt git est"
    echo "        incomplet (D99)."
    exit 2
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "$PY" ]; then
    echo "[REFUS nommé] python3 introuvable sur le runner."
    exit 2
fi
echo "[python] $PY"

# le sysctl nommé (l'identité du silicium, avant le run)
echo "[identite] sysctl machdep.cpu.brand_string :"
sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "(sysctl muet — nommé)"
echo "[identite] sysctl hw.model :"
sysctl -n hw.model 2>/dev/null || echo "(sysctl muet — nommé)"

# l'étiquette vit AUSSI dans le réceptacle (le témoin s'auto-nomme)
mkdir -p preuves-dudect-apple
cat > preuves-dudect-apple/ETIQUETTE-AUTOTEST-DISTANT.txt <<'EOF'
ÉTIQUETTE : AUTOTEST-DISTANT (l'édition ACTIONS, job kit-G-apple-silicon)
Le silicium est RÉEL (le runner macOS Apple Silicon de GitHub, mutuel
aux voisins inconnus — D206) ; le geste est celui du LABO (le workflow
du dépôt public, gratuit). La hiérarchie d'évidence est INCHANGÉE : le
banc contrôlé (portable, téléphone) demeure la référence ; ce run est
une lecture de commodité, JAMAIS le run terrain du développeur. La
pièce dudect_apple.c est un DÉRIVÉ NOMMÉ de dudect_arm.c (kit-B
TÉLÉPHONE) : mêmes contrôles, même équation (APPLE-ARM-1, l'égalation
du TELEPHONE-ARM-1), les gardes de portage NOMMÉES (affinité
Linux-seulement, canal /proc absent — l'épreuve FIPS décide seule).
EOF

echo "[run] $PY scenario-dudect-apple.py — l'épreuve FIPS, puis les trois"
echo "      runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-dudect-apple.py
RC=$?
echo "[fin] le kit-G est TERMINÉ (code $RC) — le réceptacle"
echo "      preuves-dudect-apple/ attend la collecte du workflow."
exit $RC
