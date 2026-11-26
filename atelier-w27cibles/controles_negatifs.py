#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les contrôles négatifs de W27CIBLES (C25 étendue) — sur COPIES du registre,
jamais sur CIBLES.md réel. Exigence du prompt : deux contrôles négatifs
(verdict TENUE sur mesure périmée non étiquetée → refus nommé) ; plus la
recomposition des ONZE lignes depuis le registre (aucune cible re-tirée)."""
import importlib.util
import pathlib
import re
import sys

R = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("linter_v4", str(R / "scripts/vague20/linter_v4.py"))
L = importlib.util.module_from_spec(spec)
spec.loader.exec_module(L)

REGISTRE = (R / "CIBLES.md").read_text(encoding="utf-8")

# --- La recomposition : ONZE lignes, aucune cible re-tirée, verdicts intacts ---
lignes = [l for l in REGISTRE.splitlines() if l.startswith("| CIB-")]
verdicts_avant = {l.split("|")[1].strip(): l.split("|")[6].strip() for l in lignes}
assert len(lignes) == 11, f"{len(lignes)} lignes ≠ 11"
VERDICTS_ORIGINAUX = {
    "CIB-ADD-COUT-4500": "MANQUÉE (de 104)", "CIB-ADD-FAISAB": "MANQUÉE",
    "CIB-ADD-STRUC": "EN ATTENTE (aucun serving à structured output)",
    "CIB-ADD-RATIO": "MANQUÉE (de 0,264)", "CIB-EDIT-BUDGET": "TENUE",
    "CIB-LOC-BUDGET": "TENUE (HISTORIQUE-DATÉ)", "CIB-ORACLE-T": "EN ATTENTE (mmap 0xC000 refusé : `vm.mmap_min_addr`)",
    "CIB-HARNAIS-200": "MANQUÉE", "CIB-AES-105": "EN ATTENTE (aucun code VAES écrit)",
    "CIB-AES-ENTRELACE": "HORS SUJET (mesuré, sans cible relative)",
    "CIB-DIFF-PLANCHER": "REPÈRE",
}
for cid, v in VERDICTS_ORIGINAUX.items():
    assert verdicts_avant[cid].startswith(v.split(" ")[0]), f"{cid} : verdict retourné !"
print(f"recomposition : {len(lignes)}/11 lignes, verdicts portés tels quels — aucune cible re-tirée")

t = L.charge(R / "pack-v310")

essais = []


def essai(nom, registre_mut):
    r = L.controles_w26(t, R, cibles_texte=registre_mut)
    refus = [x for x in r if x[0] == "C25" and x[1] == "cibles"]
    essais.append((nom, bool(refus), refus))


# (i) L'ÉTIQUETTE RETIRÉE : CIB-LOC-BUDGET retrouve la mesure M1 sans étiquette
mut1 = REGISTRE.replace(
    "| 51 M1 (HISTORIQUE-DATÉ) vs 627 adopté / 1 053 pointeur-seul | TENUE (HISTORIQUE-DATÉ) |",
    "| 51 vs 627 adopté / 1 053 pointeur-seul | TENUE |")
assert mut1 != REGISTRE
essai("CIB-LOC-BUDGET : étiquette HISTORIQUE-DATÉ retirée → refus nommé", mut1)

# (ii) LA MESURE D'UNE AUTRE ÈRE SUBSTITUÉE : CIB-EDIT-BUDGET porte le 719 M1 sans étiquette
mut2 = REGISTRE.replace("| 674 (adopté, TPL-EDIT-v1 OPT-14) | TENUE |", "| 719 | TENUE |")
assert mut2 != REGISTRE
essai("CIB-EDIT-BUDGET : la mesure M1 719 substituée sans étiquette → refus nommé", mut2)

# (iii) Le registre réel : la règle ne mord pas (les étiquettes sont en place)
r = L.controles_w26(t, R, cibles_texte=REGISTRE)
cibles_refus = [x for x in r if x[1] == "cibles"]
essais.append(("le registre réel : zéro refus côté cibles (les étiquettes en place)",
               not cibles_refus, cibles_refus))

verts = 0
print("=" * 78)
print("CONTRÔLES NÉGATIFS W27CIBLES — la règle des ères (sur copies du registre)")
print("=" * 78)
for nom, ok, refus in essais:
    verts += 1 if ok else 0
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    for c, p, m in refus[:3]:
        print(f"        → {c} {p} — {m[:110]}")
print(f"{verts}/{len(essais)}")
sys.exit(0 if verts == len(essais) else 3)
