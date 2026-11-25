#!/usr/bin/env bash
# lancer-kit-C-CI.sh — L'ENVELOPPE CI DU KIT-C (l'édition ACTIONS, job
# x86-64 serveur, 25/11/2026). La pièce (dudect_collab.c,
# scenario-collab.py, cibles/) est BYTE-POUR-BYTE celle de l'édition
# COLLAB (Entrée 425) : le scénario ASSERTE ses scellés — la même
# question machine-ou-code, le MÊME protocole COLLAB-X86-1, un AUTRE
# silicium serveur (le runner ubuntu-latest de GitHub).
#
# L'ÉTIQUETTE (dite d'abord, pour qu'aucune lecture ne naisse grandie) :
# AUTOTEST-DISTANT — le silicium est RÉEL (le runner de GitHub), le
# geste est celui du LABO (le workflow du dépôt public, gratuit) : la
# hiérarchie d'évidence est INCHANGÉE (le banc contrôlé demeure la
# référence) ; ce run est une lecture de commodité, JAMAIS le run
# terrain du développeur. Les écrans finaux du scénario parleront des
# cellules Colab (la pièce byte-pour-byte) : au CI ils ne vivent pas —
# nommé, jamais muet.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE KIT-C SUR LE RUNNER x86-64 — ÉTIQUETTE : AUTOTEST-DISTANT"
echo " (le silicium est réel, le geste est celui du labo : AUCUN statut"
echo "  terrain n'en découle — le run Colab du maître demeure le sien.)"
echo " La question : la même que l'édition COLLAB — les trois"
echo " divergences du 24/11 suivent-elles LA MACHINE ou LE CODE ?"
echo "==================================================================="

if [ ! -f dudect_collab.c ] || [ ! -f scenario-collab.py ] || \
   [ ! -f cibles/proxy-image.bin ] || [ ! -f cibles/manifeste-c.txt ]; then
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

# l'étiquette vit AUSSI dans le réceptacle (le témoin s'auto-nomme)
mkdir -p preuves-collab
cat > preuves-collab/ETIQUETTE-AUTOTEST-DISTANT.txt <<'EOF'
ÉTIQUETTE : AUTOTEST-DISTANT (l'édition ACTIONS, job kit-C-x86-serveur)
Le silicium est RÉEL (le runner ubuntu-latest de GitHub, mutuel aux
voisins inconnus — D206 : le t mesure AUSSI eux) ; le geste est celui
du LABO (le workflow du dépôt public, gratuit). La hiérarchie
d'évidence est INCHANGÉE : le banc contrôlé (portable, téléphone)
demeure la référence ; ce run est une lecture de commodité, JAMAIS le
run terrain du développeur. La pièce est byte-pour-byte celle de
l'édition COLLAB (dudect_collab.c, proxy-image.bin, manifestes) ; le
protocole COLLAB-X86-1 pré-enregistré vit au LISEZMOI-dudect-collab
de l'édition COLLAB.
EOF

echo "[run] $PY scenario-collab.py — l'épreuve FIPS des trois lecteurs,"
echo "      puis les trois runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-collab.py
RC=$?
echo "[fin] le kit-C est TERMINÉ (code $RC) — le réceptacle preuves-collab/"
echo "      et le zip de retour attendent la collecte du workflow."
exit $RC
