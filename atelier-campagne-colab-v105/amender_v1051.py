#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'AMENDEMENT v1051 — LE TERRAIN.9 DU 28/11 : l'emballage des releases
llama.cpp a SÉPARÉ les binaires CUDA du cudart (l'asset « cudart-…tar.gz » ne
porte PLUS les binaires — MESURÉ AU BAC : 3 libs seules : libcudart.so.12,
libcublas.so.12, libcublasLt.so.12) ; les binaires CUDA vivent à
« llama-<tag>-bin-ubuntu-cuda-12.8-x64.tar.gz » (llama-server + les .so
frères — vérifié au bac, 227 Mio). LE V105 pointait le cudart → AUCUN
llama-server → la bascule silencieuse à la SOURCE (25-40 min de compilation)
→ la MORT dans les runtes recyclés (15-45 min de vie — le terrain du 28/11
matin, deux fois).

L'AMENDEMENT (minimal, NOMMÉ) : la cellule serving du v105 porte le choix
bin-ubuntu-cuda-12 + cudart (les DEUX assets, LD_LIBRARY_PATH aux deux),
le repli source demeure. AUCUNE AUTRE cellule touchée — le reste du notebook
demeure BYTE-BYTE le v105 (l'épreuve l'asserte)."""
import json
import pathlib

V105 = pathlib.Path("/home/z/my-project/work/Campagne-Colab-v105-VIVANTE.ipynb")
DEST = pathlib.Path("/home/z/my-project/work/Campagne-Colab-v1051-VIVANTE.ipynb")

nb = json.loads(V105.read_text(encoding="utf-8"))
# la cellule serving (code, contenant « asset_de_la_release »)
idx = next(i for i, c in enumerate(nb["cells"])
           if c["cell_type"] == "code" and "asset_de_la_release" in "".join(c["source"]))
src = "".join(nb["cells"][idx]["source"])

VIEUX_ASSET = '''    for rel in releases:
        nu, cudarts = None, []
        for a in rel["assets"]:
            n = a["name"].lower()
            if "ubuntu" not in n or "x64" not in n or not n.endswith((".zip", ".tar.gz")):
                continue
            exclus = ("arm64", "s390x", "vulkan", "rocm", "sycl", "openvino", "opencl")
            if any(x in n for x in exclus):
                continue
            if n.startswith("cudart-") and "cuda" in n:
                cudarts.append(a)
            if "cuda" not in n and not n.startswith("cudart-"):
                nu = a
        if GPU and cudarts:
            # le cudart CUDA-12 d'abord (plus tolérant au driver du poste que le 13)
            choix = next((a for a in cudarts if "cuda-12" in a["name"].lower()), cudarts[0])
            return rel["tag_name"], choix
        if not GPU and nu is not None:
            return rel["tag_name"], nu
    return None'''

NOUVEAU_ASSET = '''    for rel in releases:
        nu, bins_cuda, cudarts = None, [], []
        for a in rel["assets"]:
            n = a["name"].lower()
            if "ubuntu" not in n or "x64" not in n or not n.endswith((".zip", ".tar.gz")):
                continue
            exclus = ("arm64", "s390x", "vulkan", "rocm", "sycl", "openvino", "opencl")
            if any(x in n for x in exclus):
                continue
            # LE TERRAIN.9 (28/11) : l'emballage a SÉPARÉ binaires et cudart —
            # l'asset « cudart-… » ne porte PLUS les binaires (3 libs seules,
            # mesuré au bac) ; les binaires CUDA vivent à « …-bin-ubuntu-cuda-… ».
            if n.startswith("cudart-") and "cuda" in n:
                cudarts.append(a)
            elif "cuda" in n and n.startswith("llama-") and "-bin-ubuntu-cuda-" in n:
                bins_cuda.append(a)
            elif "cuda" not in n and not n.startswith("cudart-"):
                nu = a
        if GPU and bins_cuda:
            # les BINAIRES CUDA-12 d'abord (le cudart CUDA-12 en accompagnement,
            # plus tolérant au driver du poste que le 13)
            bin_ = next((a for a in bins_cuda if "cuda-12" in a["name"].lower()), bins_cuda[0])
            lib = next((a for a in cudarts if "cuda-12" in a["name"].lower()),
                       cudarts[0] if cudarts else None)
            return rel["tag_name"], bin_, lib
        if not GPU and nu is not None:
            return rel["tag_name"], nu, None
    return None'''

VIEUX_EXTRAIS = '''    tag_asset = asset_de_la_release()
    if tag_asset is None:
        return None
    tag, asset = tag_asset
    print(f"[serving] la release prébattue {tag} : {asset['name']} "
          f"({asset['size'] / 2**20:.0f} Mio)")
    archive = pathlib.Path("/content") / asset["name"]
    if archive.exists():
        archive.unlink()
    urllib.request.urlretrieve(asset["browser_download_url"], archive)
    if asset["name"].endswith(".zip"):
        with zipfile.ZipFile(archive) as z:
            z.extractall(DOS_LLAMA)
    else:
        with tarfile.open(archive) as t:
            try:
                t.extractall(DOS_LLAMA, filter="data")
            except TypeError:
                t.extractall(DOS_LLAMA)     # le Python d'avant 3.12 ignore le filtre
    trouves = list(DOS_LLAMA.rglob("llama-server"))
    return trouves[0] if trouves else None'''

NOUVEAU_EXTRAIS = '''    tag_asset = asset_de_la_release()
    if tag_asset is None:
        return None
    tag, asset, asset_lib = tag_asset
    print(f"[serving] la release prébattue {tag} : {asset['name']} "
          f"({asset['size'] / 2**20:.0f} Mio)"
          + (f" + le cudart {asset_lib['name']} ({asset_lib['size'] / 2**20:.0f} Mio)"
             if asset_lib else ""))
    for ass in (asset, asset_lib):
        if ass is None:
            continue
        archive = pathlib.Path("/content") / ass["name"]
        if archive.exists():
            archive.unlink()
        urllib.request.urlretrieve(ass["browser_download_url"], archive)
        if ass["name"].endswith(".zip"):
            with zipfile.ZipFile(archive) as z:
                z.extractall(DOS_LLAMA if ass is asset else DOS_LLAMA / "cudart")
        else:
            with tarfile.open(archive) as t:
                try:
                    t.extractall(DOS_LLAMA if ass is asset else DOS_LLAMA / "cudart",
                                 filter="data")
                except TypeError:
                    t.extractall(DOS_LLAMA if ass is asset else DOS_LLAMA / "cudart")
    trouves = list(DOS_LLAMA.rglob("llama-server"))
    return trouves[0] if trouves else None'''

VIEUX_LANCE = '''    env["LD_LIBRARY_PATH"] = str(binaire.parent) + (
        ":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")'''

NOUVEAU_LANCE = '''    dos_cudart = DOS_LLAMA / "cudart"
    chemins_lib = [str(binaire.parent)]
    for sous in dos_cudart.rglob("*"):
        if sous.is_dir() and (sous / "libcudart.so.12").exists():
            chemins_lib.append(str(sous))      # le terrain.9 : le cudart EXTRACT à part
    env["LD_LIBRARY_PATH"] = ":".join(chemins_lib) + (
        ":" + env["LD_LIBRARY_PATH"] if env.get("LD_LIBRARY_PATH") else "")'''

VIEUX_TITRE = "# CELLULE 5 — LE SERVING SELON L'ENVIRONNEMENT : llama.cpp au runtime + le GGUF"
NOUVEAU_TITRE = ("# CELLULE 5 — LE SERVING SELON L'ENVIRONNEMENT (v1051 — LE TERRAIN.9 DU\n"
                 "# 28/11 : l'emballage des releases llama.cpp a séparé binaires CUDA et cudart,\n"
                 "# l'asset « cudart- » ne porte PLUS les binaires — le choix pointe « -bin-\n"
                 "# ubuntu-cuda- » + le cudart en accompagnement, la source demeure le repli) :\n"
                 "# llama.cpp au runtime + le GGUF")

for vieux, nouveau in ((VIEUX_TITRE, NOUVEAU_TITRE), (VIEUX_ASSET, NOUVEAU_ASSET),
                       (VIEUX_EXTRAIS, NOUVEAU_EXTRAIS), (VIEUX_LANCE, NOUVEAU_LANCE)):
    if vieux not in src:
        raise SystemExit(f"AMENDEMENT-ROMPU : bloc introuvable — {vieux[:70]!r}")
    src = src.replace(vieux, nouveau)

nb["cells"][idx]["source"] = [src]
DEST.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")

# ── LES ÉPREUVES ──
compile(src, "cellule-serving-v1051", "exec")
print("[épreuve 1] la cellule serving amendée compile — VERT")
orig = json.loads(V105.read_text(encoding="utf-8"))
nb2 = json.loads(DEST.read_text(encoding="utf-8"))
assert len(nb2["cells"]) == len(orig["cells"])
div = [i for i, (a, b) in enumerate(zip(orig["cells"], nb2["cells"]))
       if "".join(a["source"]) != "".join(b["source"])]
if div != [idx]:
    raise SystemExit(f"[épreuve 2] INVARIANT-ROMPU : cellules divergentes {div} ≠ [{idx}]")
print(f"[épreuve 2] la SEULE cellule touchée = la serving (#{idx}) — VERT")
for marque in ("bins_cuda", "-bin-ubuntu-cuda-", "cudart", "terrain.9"):
    if marque not in src:
        raise SystemExit(f"[épreuve 3] MARQUE-ABSENTE : {marque}")
print("[épreuve 3] les marques du terrain.9 présentes — VERT")
import hashlib
print(f"\nv1051 VIVANTE : {DEST} ({DEST.stat().st_size} o)")
print(f"sha256 : {hashlib.sha256(DEST.read_bytes()).hexdigest()}")
