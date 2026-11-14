#!/usr/bin/env python3
"""TRIADE — LE RE-RECOUP DU LABO (la session reprise) : ce que le coffre
porte VS ce que l'Entrée 284 consigne.
1. Le kit C : chaque pièce re-téléchargée VS l'EMPREINTE gravée (10 pièces).
2. Le kit T v2 : loupe.exe == 4d119b22… (le T0 du témoin).
3. Le plan du GUI == a78caf8c… (le VERROU D204).
4. La carte OU-TROUVER : portée à 284 ?
5. Le bundle courant du miroir : contient-il le commit de l'Entrée 284 ?
"""
import hashlib
import json
import pathlib
import re
import subprocess

BAC = pathlib.Path("/home/z/my-project/download/nouveau-run")
MIR = pathlib.Path("/home/z/my-project/download/miroir-etat")

def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

print("===== 1. LE KIT C : chaque pièce VS la gravure =====")
gravure = {}
for l in (BAC / "kit-unite-loupe-01-C-20261114" / "EMPREINTES-KIT-UNITE-01-C.txt").read_text(encoding="utf-8").splitlines():
    m = re.match(r"^([0-9a-f]{64})\s+(\S+)$", l)
    if m:
        gravure[m.group(2)] = m.group(1)
vert = 0
for nom, attendu in sorted(gravure.items()):
    p = BAC / "kit-unite-loupe-01-C-20261114" / nom
    obtenu = sha(p)
    ok = obtenu == attendu
    vert += ok
    print(f"  [{'VERT' if ok else 'ROUGE'}] {nom}  {obtenu[:16]}…")
print(f"  → {vert}/{len(gravure)} pièces recoupées à la gravure")
zipc = BAC / "kit-unite-loupe-01-C-20261114" / "kit-unite-loupe-01-C-20261114.zip"
print(f"  [note] le zip du kit : {sha(zipc)[:16]}… ({zipc.stat().st_size} o)")

print("\n===== 2. LE KIT T v2 : loupe.exe == le T0 du témoin =====")
loupe = sha(BAC / "kit-unite-loupe-01-T-20261114-v2" / "loupe.exe")
temoin = (BAC / "Nouveau run" / "preuves-unite01" / "temoin-unite01.txt").read_text(encoding="utf-8")
attendu_t0 = re.search(r"sha256 ([0-9a-f]{64})", temoin).group(1)
print(f"  loupe.exe (gravure T v2) : {loupe}")
print(f"  le sha que porte le témoin : {attendu_t0}")
print(f"  [{'VERT' if loupe == attendu_t0 else 'ROUGE'}] T0 recoupé")
# et le témoin v1 kit : la même pièce ?
loupe_v1 = sha(BAC / "kit-unite-loupe-01-T-20261114" / "loupe.exe")
print(f"  [{'VERT' if loupe_v1 == loupe else 'ROUGE'}] loupe.exe du kit T v1 == v2 (la pièce n'a pas bougé)")

print("\n===== 3. LE PLAN : a78caf8c… (le VERROU) =====")
plan = sha(BAC / "Nouveau run" / "test" / "TRIADE_gui_tous_runs_v1" / "campagne-d204" / "PLAN_PREREGISTRE_COMPARAISON.md")
print(f"  plan du GUI revenu : {plan[:16]}…  [{'VERT' if plan.startswith('a78caf8c') else 'ROUGE'}] VERROUILLÉ")

print("\n===== 4. LA CARTE OU-TROUVER : portée à 284 ? =====")
for lbl, p in [("miroir", MIR / "OU-TROUVER-LES-LIVRABLES.md"),
               ("racine", MIR / "OU-TROUVER-LES-LIVRABLES-racine.md")]:
    txt = p.read_text(encoding="utf-8")
    mentions = re.findall(r"Entrée 28\d|État 28\d|284", txt)
    m284 = len(re.findall(r"284", txt))
    print(f"  {lbl}: {p.stat().st_size} o — occurrences de « 284 » : {m284} ; dernières lignes :")
    for l in txt.strip().splitlines()[-6:]:
        print(f"    | {l[:120]}")

print("\n===== 5. LE BUNDLE COURANT : les têtes =====")
res = subprocess.run(["git", "bundle", "list-heads",
                      "/home/z/my-project/work/triade-history.bundle"],
                     capture_output=True, text=True)
print(res.stdout.strip())
res2 = subprocess.run(["git", "bundle", "verify",
                       "/home/z/my-project/work/triade-history.bundle"],
                      capture_output=True, text=True, cwd="/home/z/my-project/work/triade")
print(res2.stdout.strip()[-400:] if res2.stdout else res2.stderr.strip()[-400:])
