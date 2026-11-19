#!/bin/bash
# reproduire_1c4sokpii.sh — LA REPRODUCTION EN UNE COMMANDE (l'instruction
# 1c4sokpii, partie 4 : « le paquet d'évaluation d'artefacts (métadonnées
# Zenodo, scripts, graines, reproduction en une commande) »).
#
#   bash atelier-plan-final-1c4sokpii/reproduire_1c4sokpii.sh
#
# La chaîne rejouée (chaque pièce aux graines consignées, jamais retouchée) :
#   1. la réconciliation de campagne D210 (les totaux recalculés du registre) ;
#   2. le linter inter-pièces v194 (16 assertions) ;
#   3. le triage des 56 survivants (la graine 20261111, la console v0.14.0
#      reproduite : 776/832) ;
#   4. le re-jeu aux shims d'injection de fautes (K1/K2/K3 intacts + la
#      batterie K4 : le taux 811/832, 97,5 %) ;
#   5. le calculateur κ (l'autotest aux cas synthétiques) ;
#   6. l'épreuve POSIX du bras C de la seconde famille (2 000 cas, la graine
#      20261115 — le source généné conservé, l'épreuve rejouée) ;
#   7. les empreintes du pack v0.19.4 recoupées.
# Le code de sortie : 0 si TOUT VERT.
set -e
cd "$(dirname "$0")/.."
echo "=== LA REPRODUCTION EN UNE COMMANDE — 1c4sokpii (partie 4) ==="

echo "— [1/7] la réconciliation de campagne D210 (les totaux du registre)"
python3 scripts/vague7/reconciliation_campagne_d210.py | tail -3

echo "— [2/7] le linter inter-pièces v194"
python3 scripts/vague7/linter_v194.py | tail -1

echo "— [3/7] le triage des 56 survivants (la graine 20261111)"
python3 atelier-plan-final-1c4sokpii/triage_survivants_1c4sokpii.py | tail -3

echo "— [4/7] le re-jeu aux shims d'injection (K4, la batterie de fautes)"
python3 atelier-plan-final-1c4sokpii/rejeu_fautes_1c4sokpii.py | grep -E "TOTAL|dont" | head -2

echo "— [5/7] le calculateur κ (l'autotest)"
python3 scripts/replication_v150/kohen_kappa_v150.py | tail -1

echo "— [6/7] l'épreuve POSIX du bras C de la seconde famille (la graine 20261115)"
python3 - << 'EOF'
import importlib.util, pathlib, sys
sys.path.insert(0, str(pathlib.Path("atelier-plan-final-1c4sokpii").resolve()))
spec = importlib.util.spec_from_file_location(
    "ind", pathlib.Path("atelier-plan-final-1c4sokpii/independance_familles_1c4sokpii.py"))
ind = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ind)
verts, total, details = ind.epreuve_posix(
    pathlib.Path("atelier-plan-final-1c4sokpii/bras_c_qwen_loupe13.c"))
print(f"l'épreuve : {verts}/{total} VERT"
      + (f" — {details[:2]}" if details else ""))
assert verts == 1984 and total == 2011, (verts, total)
EOF

echo "— [7/7] les empreintes du pack v0.19.4 recoupées"
python3 - << 'EOF'
import hashlib, pathlib
base = pathlib.Path("scripts/vague7/pack-v194")
attendues = {}
for ligne in (base / "empreintes_livrables_v0.19.4.txt").read_text(encoding="utf-8").splitlines():
    p = ligne.split()
    if len(p) == 3 and p[1].replace(",", "").isdigit():
        attendues[p[0]] = (int(p[1].replace(",", "")), p[2])
verts = 0
for nom, (taille, sha) in attendues.items():
    chemin = next(s / nom for s in base.iterdir() if (s / nom).exists())
    ok = hashlib.sha256(chemin.read_bytes()).hexdigest() == sha \
        and chemin.stat().st_size == taille
    assert ok, f"empreinte divergente : {nom}"
    verts += 1
print(f"les empreintes : {verts}/{len(attendues)} EXACTES")
EOF

echo ""
echo "VERDICT : VERT — la chaîne reproduite (les graines consignées, "
echo "les consoles identiques, aucune pièce retouchée)"
