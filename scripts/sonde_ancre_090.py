#!/usr/bin/env python3
"""sonde_ancre_090.py — vérifie l'hypothèse R7 de l'ère M9 : l'image 0.9.0
recomposée par les fonctions du build M8 (heritage_complet +
assembler_tout_m8 + composer_image_m8 + ecrire_pe32plus) est byte-identique
au scellé m8/proxy.exe (1492b0bc…). Si OUI : le build M9 compose depuis ces
mêmes sections. Si NON : l'écart est nommé AVANT d'écrire le build."""

import hashlib
import importlib.util
import os
import sys

T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _d in (os.path.join(T, "m4"), os.path.join(T, "m4", "outils"),
           os.path.join(T, "m5"), os.path.join(T, "m5", "outils"),
           os.path.join(T, "m8"), os.path.join(T, "m8", "outils")):
    if _d not in sys.path:
        sys.path.insert(0, _d)

spec = importlib.util.spec_from_file_location(
    "build_m8", os.path.join(T, "m8", "build_m8.py"))
B8 = importlib.util.module_from_spec(spec)
sys.modules["build_m8"] = B8
spec.loader.exec_module(B8)

h = B8.heritage_complet()
_specs, code_m8, _verrous = B8.assembler_tout_m8()
sections = B8.composer_image_m8(h["sections_m5"], code_m8)
exe = B8.ecrire_pe32plus(*sections)

with open(os.path.join(T, "m8", "proxy.exe"), "rb") as f:
    scelle = f.read()

sha_compose = hashlib.sha256(exe).hexdigest()
sha_scelle = hashlib.sha256(scelle).hexdigest()
print(f"composée : {len(exe)} o, sha256 {sha_compose[:16]}…")
print(f"scellée  : {len(scelle)} o, sha256 {sha_scelle[:16]}…")
if exe == scelle:
    print("ANCRE R7 TENUE : l'image 0.9.0 recomposée == le scellé "
          "OCTET PAR OCTET — le build M9 compose depuis ces sections")
    sys.exit(0)
print("ÉCART NOMMÉ : la composition M8 diverge du scellé — premier octet "
      "différent :")
for k, (x, y) in enumerate(zip(exe, scelle)):
    if x != y:
        print(f"  offset {k:#x} : composé {x:#04x} != scellé {y:#04x}")
        break
sys.exit(1)
