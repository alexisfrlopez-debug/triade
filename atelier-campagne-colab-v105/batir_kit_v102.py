#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE KIT v102 — L'AMENDEMENT TERRAIN.10 (28/11) : le format de la réponse du
serveur llama.cpp a CHANGÉ entre b12810 et b12823 — « probs »/« prob » est
devenu « top_logprobs »/« logprob » (MESURÉ AU BORD au diagnostic du 28/11 :
la réponse rend top_logprobs, le modèle PARLE '```json\\n{\"' à la sonde
enrobée). Le moteur v101 lisait [0][\"probs\"] → KeyError → « le pas
terminal » : TOUT pas eût été lu terminal (la cause du faux BORD-MUET au
premier run v1051). L'AMENDEMENT : les DEUX formats admis (le bord fait la
loi du transport, les cibles et les plans gelés INTACTS). Les autres pièces
du kit v101 demeurent BYTE-BYTE."""
import hashlib
import pathlib
import shutil
import zipfile

SRC = pathlib.Path("/home/z/my-project/work/kit-v101")
DOS = pathlib.Path("/home/z/my-project/work/kit-v102")
if DOS.exists():
    shutil.rmtree(DOS)
shutil.copytree(SRC, DOS)

moteur = DOS / "moteur_campagne.py"
src = moteur.read_text(encoding="utf-8")

VIEUX = '''        try:
            probs = rep["completion_probabilities"][0]["probs"]
        except (KeyError, IndexError):
            # le pas terminal : le bord a rendu sa fin sans probabilités
            return [], int(rep.get("tokens_evaluated", 0))
        candidats = sorted(((int(p["id"]), float(p.get("prob", p.get("p", 0.0))))
                            for p in probs), key=lambda x: -x[1])'''

NOUVEAU = '''        try:
            entree = rep["completion_probabilities"][0]
        except (KeyError, IndexError):
            # le pas terminal : le bord a rendu sa fin sans probabilités
            return [], int(rep.get("tokens_evaluated", 0))
        # LE TERRAIN.10 (28/11) : le format de la réponse a changé à b12823 —
        # « probs »/« prob » (b12810 et avant) est devenu « top_logprobs »/
        # « logprob » (mesuré au bord au diagnostic du 28/11 : la sonde
        # enrobée PARLE, la clé a changé) — les DEUX formats admis, le bord
        # fait la loi du transport, les cibles et les plans gelés INTACTS.
        probs = entree.get("probs") or entree.get("top_logprobs")
        if not probs:
            return [], int(rep.get("tokens_evaluated", 0))
        candidats = sorted(((int(p["id"]),
                             float(p.get("prob", p.get("logprob", p.get("p", 0.0)))))
                            for p in probs), key=lambda x: -x[1])'''

if VIEUX not in src:
    raise SystemExit("AMENDEMENT-ROMPU : le bloc du parseur introuvable — vérifier.")
src = src.replace(VIEUX, NOUVEAU)
moteur.write_text(src, encoding="utf-8")
compile(src, "moteur-v102", "exec")
print("[épreuve 1] le moteur v102 compile — VERT")

# l'entête du moteur porte la version
src2 = moteur.read_text(encoding="utf-8")
print("[info] le moteur porte:", [l for l in src2.splitlines()[:6] if "v10" in l][:2])

# le LISEZMOI de l'amendement
(DOS / "LISEZMOI-V102-TERRAIN10.txt").write_text(
    "LE KIT POSTE v102 — L'AMENDEMENT TERRAIN.10 (28/11/2026)\n"
    "=" * 60 + "\n\nLA CAUSE MESURÉE AU BORD (le diagnostic du 28/11, le runtime\n"
    "gpu-t4…): le format de la réponse du serveur llama.cpp a changé entre\n"
    "b12810 (l'ère du v101) et b12823 (la release du jour) — la clé « probs »\n"
    "(et « prob » par entrée) est devenue « top_logprobs » (et « logprob »).\n"
    "Le modèle PARLE à la sonde enrobée (« ```json\\n{\\\" » — l'Entrée 451 est\n"
    "bien soignée au transport) ; le moteur v101 lisait [0][\"probs\"] → la\n"
    "clé absente → « le pas terminal » : TOUT pas eût été lu terminal — la\n"
    "cause du faux BORD-MUET au premier run du v1051.\n\n"
    "L'AMENDEMENT : BordLlama.prochain admet les DEUX formats (probs/prob et\n"
    "top_logprobs/logprob). AUCUNE cible touchée, AUCUN plan gelé touché, les\n"
    "autres pièces du kit v101 demeurent BYTE-BYTE (le manifeste-harnais\n"
    "recoupé au chargement le prouve au gate).\n", encoding="utf-8")

# le zip v102 (les mêmes chemins que le v101 — le notebook les attend)
zip_path = pathlib.Path("/home/z/my-project/work/TRIADE_kit_campagne_poste_v102.zip")
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path, "w", compresslevel=9) as z:
    for p in sorted(DOS.rglob("*")):
        if p.is_file():
            z.write(p, p.relative_to(DOS).as_posix())
sha = hashlib.sha256(zip_path.read_bytes()).hexdigest()
print(f"[kit] {zip_path.name} : {zip_path.stat().st_size} o")
print(f"[kit] sha256 : {sha}")
# la divergence au v101 : le moteur + le LISEZMOI seul
with zipfile.ZipFile("/home/z/my-project/work/TRIADE_kit_campagne_poste_v101.zip") as z1, \
     zipfile.ZipFile(zip_path) as z2:
    n1 = {i.filename for i in z1.infolist()}
    n2 = {i.filename for i in z2.infolist()}
    print(f"[épreuve 2] pièces v101 : {len(n1)} · v102 : {len(n2)} "
          f"(+{sorted(n2 - n1)})")
    divergent = [n for n in sorted(n1 & n2)
                 if z1.read(n) != z2.read(n)]
    print(f"[épreuve 2] pièces divergentes : {divergent}")
    if divergent != ["moteur_campagne.py"]:
        raise SystemExit("INVARIANT-ROMPU : d'autres pièces divergent !")
print("[épreuve 2] la SEULE pièce divergente = le moteur (l'amendement) — VERT")
