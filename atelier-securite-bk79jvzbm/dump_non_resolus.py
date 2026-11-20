#!/usr/bin/env python3
"""dump_non_resolus.py — la vue des 463 non-résolus de la v110 : la base,
l'index, le contexte (le bloc, l'instruction) — la matière de l'extension v200."""
import sys, pathlib, importlib.util, json
from collections import Counter

REPO = pathlib.Path("/home/z/my-project/projet/triade")
sys.path.insert(0, str(REPO / "scripts"))

# charger l'analyseur v110 en mode silencieux : répliquer sa collecte
import capstone
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True

spec = importlib.util.spec_from_file_location("sm_v110", REPO / "scripts/surete_memoire_v110.py")
sm = importlib.util.module_from_spec(spec)
sys.modules["sm_v110"] = sm
spec.loader.exec_module(sm)

# le même inventaire de blocs que la v110 : reconstruire depuis ses internes
# (l'analyseur v110 a déjà tout : on ré-exécute AnalyseBloc par bloc)
B4 = sm.B4

blocs = []
# reproduire la collecte : les domaines loupe + tls13 + sys comme à la v110
def collecter():
    # les mêmes sources que la v110 (lues de son module après exécution)
    return getattr(sm, "_INVENTAIRE", None)

# la v110 expose-t-elle l'inventaire ? sinon : relire sa fonction principale
import inspect
src = inspect.getsource(sm)
# la fonction principale : analyser tous les blocs à la manière de la v110
# -> réutiliser sa logique par ré-import : on appelle les mêmes structures
# (le script v110 exécute l'analyse au module ; on relit ses sorties CSV)
import csv
rows = list(csv.DictReader(open(REPO / "scripts/preuves_v110/surete_memoire.csv")))
print(f"{len(rows)} blocs au CSV v110 ; total non_resolus =",
      sum(int(r['non_resolus']) for r in rows))
par_bloc = [(r['domaine'], r['bloc'], int(r['non_resolus'])) for r in rows
            if int(r['non_resolus']) > 0]
par_bloc.sort(key=lambda x: -x[2])
print("\nles blocs porteurs de non-résolus (desc) :")
for d, b, n in par_bloc[:25]:
    print(f"  {d}/{b}: {n}")
print(f"  ... {len(par_bloc)} blocs concernés au total")
