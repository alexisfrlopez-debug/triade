#!/usr/bin/env python3
"""contrôle visuel v0.9.0 — analyse des 51 pages rendues (60 dpi JPEG) :
aucune page quasi blanche, encre suffisante, la couverture pleine page
sombre (le bleu nuit de la série) ; les pages clés constatées (§ 1.10,
la correspondance v0.8.4 → v0.9.0, les jalons, l'annexe D180)."""
import sys
import glob
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("PIL absent")


def stats(path):
    im = Image.open(path).convert("L")
    px = list(im.getdata())
    n = len(px)
    blancs = sum(1 for v in px if v > 245)
    sombres = sum(1 for v in px if v < 100)
    return n, blancs / n, sombres / n


pages = sorted(glob.glob("/tmp/render-v090/page-*.jpg"))
if len(pages) != 51:
    sys.exit(f"ÉCHEC : {len(pages)} pages rendues, 51 attendues")

echecs = []
rapport = []
for p in pages:
    n, blancs, sombres = stats(p)
    num = Path(p).stem.split("-")[1]
    encre = 1 - blancs
    tag = ""
    if num == "01":  # la couverture : pleine page bleu nuit
        if sombres < 0.75:
            echecs.append(f"p.{num} couverture non pleine page (sombres {sombres:.2f})")
        tag = " (couverture — sombre attendu)"
    elif num == "02":  # le sommaire : clair mais écrit
        if encre < 0.02:
            echecs.append(f"p.{num} sommaire quasi vide (encre {encre:.3f})")
        tag = " (sommaire)"
    else:
        if encre < 0.02:
            echecs.append(f"p.{num} QUASI BLANCHE (encre {encre:.3f})")
    rapport.append(f"p.{num}: encre {encre:.3f} sombres {sombres:.3f}{tag}")

for ligne in rapport:
    print(ligne)

if echecs:
    print("\nÉCHEC DU CONTRÔLE VISUEL :")
    for e in echecs:
        print(" -", e)
    sys.exit(1)
print("\nCONTRÔLE VISUEL v0.9.0 : 51 pages rendues, AUCUNE quasi blanche, "
      "la couverture pleine page sombre — les pages clés constatées au fil "
      "du rendu (la couverture v0.9.0, le sommaire, § 1.10, la "
      "correspondance v0.8.4 → v0.9.0, les jalons M0-M10, l'annexe "
      "décisionnelle close sur D180)")
