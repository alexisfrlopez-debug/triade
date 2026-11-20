#!/bin/bash
# rejeu_sequence.sh — LA SÉQUENCE DE RE-PRODUCTION (H2 de bk79jvzbm) :
# (1) la console v0.14.0 (rejeu_survivants_v140.py → 776/832) ;
# (2) la console courante (rejeu_fautes_1c4sokpii.py → 811/832) ;
# les MÊMES graines, l'ordre inchangé — AVANT toute nouvelle injection.
cd /home/z/my-project/depot
export PYTHONUNBUFFERED=1
echo "=== (1) LA CONSOLE v0.14.0 — le rejeu des 832 (graine 20261111) ==="
date -u +%Y-%m-%dT%H:%M:%SZ
python3 scripts/rejeu_survivants_v140.py > atelier-securite-bk79jvzbm/console-v0140-rejeu.txt 2>&1
echo "exit=$? — $(tail -5 atelier-securite-bk79jvzbm/console-v0140-rejeu.txt | head -2)"
echo "=== (2) LA CONSOLE COURANTE — la batterie K4 (graine 20261111) ==="
date -u +%Y-%m-%dT%H:%M:%SZ
python3 atelier-plan-final-1c4sokpii/rejeu_fautes_1c4sokpii.py > atelier-securite-bk79jvzbm/console-k4-rejeu.txt 2>&1
echo "exit=$? — $(tail -8 atelier-securite-bk79jvzbm/console-k4-rejeu.txt | head -4)"
date -u +%Y-%m-%dT%H:%M:%SZ
echo "=== SÉQUENCE TERMINÉE ==="
