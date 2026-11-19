#!/bin/sh
# lancer_mesures_v190.sh — LE PILOTE PRÉ-ENREGISTRÉ (n>=10 exécutions par N)
# Le mesureur scellé dudect_v150 est appelé TEL QUEL — le pilote ne mesure
# rien lui-même ; l'ordre fixe : 10 exécutions à N=60, puis N=200 (les
# pics), puis N=400 ; l'empreinte machine gravée AVANT la première.
# Usage : sh lancer_mesures_v190.sh [repertoire_cibles] [executable_dudect]
set -e
CIBLES="${1:-cibles}"
DUD="${2:-./dudect_v150}"
mkdir -p journaux-v190
{
  echo "=== EMPREINTE MACHINE (gravée avant la première exécution) ==="
  uname -a 2>/dev/null || ver
  (cat /proc/cpuinfo 2>/dev/null | grep -m1 "model name") || echo "CPU: (à consigner)"
  (cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null \
    && echo "(l'état EFFECTIF du gouverneur ci-dessus)") || \
    echo "GOUVERNEUR: (à consigner au témoin, l'état EFFECTIF)"
} > journaux-v190/empreinte-machine.txt
for N in 60 200 400; do
  for i in $(seq 1 10); do
    echo "=== exécution $i/10 à N=$N (la graine au journal du mesureur) ==="
    "$DUD" "$CIBLES" "$N" 2>&1 | tee "journaux-v190/run-N${N}-${i}.log"
  done
done
echo "LES SÉRIES VÉCUES — agréger : python3 agreger_mesures_v190.py journaux-v190"
