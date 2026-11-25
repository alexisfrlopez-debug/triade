#!/usr/bin/env bash
# lancer-kit-D-CI.sh — L'ENVELOPPE CI DU KIT-D (l'édition ACTIONS, job
# ARM64 serveur, 25/11/2026). La pièce (dudect_arm.c,
# scenario-dudect-arm.py) est BYTE-POUR-BYTE celle du kit-B de l'édition
# TÉLÉPHONE (Entrées 424/425) : le scénario ASSERTE son scellé
# (08681278…) — la même équation TELEPHONE-ARM-1, un AUTRE silicium
# ARM64 : le runner arm64 de GitHub (l'étiquette du cpuinfo nommera la
# famille — le kit n'affirme rien, le drapeau « sha2 » du noyau
# décidera si FEAT_SHA256 y vit).
#
# L'ÉTIQUETTE (dite d'abord, pour qu'aucune lecture ne naisse grandie) :
# AUTOTEST-DISTANT — le silicium est RÉEL (le runner arm64 de GitHub),
# le geste est celui du LABO (le workflow du dépôt public, gratuit) :
# la hiérarchie d'évidence est INCHANGÉE ; ce run est une lecture de
# commodité, JAMAIS le run terrain du développeur. Les écrans finaux
# du scénario parleront du téléphone (la pièce byte-pour-byte) : au CI
# ils ne vivent pas — nommé, jamais muet.

cd "$(dirname "$0")" || exit 2

echo "==================================================================="
echo " LE KIT-D SUR LE RUNNER arm64 — ÉTIQUETTE : AUTOTEST-DISTANT"
echo " (le silicium est réel, le geste est celui du labo : AUCUN statut"
echo "  terrain n'en découle — le run téléphone du maître demeure le"
echo "  sien.) Les contrôles, SHA-256 logiciel et — si le noyau expose"
echo " « sha2 » — FEAT_SHA256 : le protocole TELEPHONE-ARM-1, sur UN"
echo " AUTRE silicium ARM64 (le serveur du runner)."
echo "==================================================================="

if [ ! -f dudect_arm.c ] || [ ! -f scenario-dudect-arm.py ]; then
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
mkdir -p preuves-dudect-arm
cat > preuves-dudect-arm/ETIQUETTE-AUTOTEST-DISTANT.txt <<'EOF'
ÉTIQUETTE : AUTOTEST-DISTANT (l'édition ACTIONS, job kit-D-arm64-serveur)
Le silicium est RÉEL (le runner arm64 Linux de GitHub, mutuel aux
voisins inconnus — D206) ; le geste est celui du LABO (le workflow du
dépôt public, gratuit). La hiérarchie d'évidence est INCHANGÉE : le
banc contrôlé (portable, téléphone) demeure la référence ; ce run est
une lecture de commodité, JAMAIS le run terrain du développeur. La
pièce est byte-pour-byte celle du kit-B TÉLÉPHONE (dudect_arm.c,
scellé 08681278…) ; l'équation TELEPHONE-ARM-1 (échauffement 100,
LOT=512/4, N=60/200/400, t de Welch, |t|>5) vit au LISEZMOI-dudect-arm
de l'édition TÉLÉPHONE, RE-ENREGISTRÉE au LISEZMOI-dudect-actions de
cette édition pour CE silicium serveur.
EOF

echo "[run] $PY scenario-dudect-arm.py — l'épreuve FIPS, puis les trois"
echo "      runs N=60, N=200, N=400 (l'ordre imposé)…"
"$PY" scenario-dudect-arm.py
RC=$?
echo "[fin] le kit-D est TERMINÉ (code $RC) — le réceptacle"
echo "      preuves-dudect-arm/ attend la collecte du workflow."
exit $RC
