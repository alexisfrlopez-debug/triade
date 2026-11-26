#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""session_ouverture.py — L'OUVERTURE DE SESSION, LA CIBLE CIB-VOL-SESSION
(W29MOTEUR, prompt 2 : le chemin critique d'ouverture de session — le
md5+sha256 du fichier témoin 196 609 o par les blocs scellés).

LA MESURE CROISÉE : le moteur NATIF (moteur_session : l'image loupe montée,
les six feuilles kernel32 en amorces natives lisant le témoin, loupe-01
appelé, L'OUVERTURE seule horlogée, n=5 passes médiane) CONTRE le JUMEAU
(l'émulateur du harnais_noyau — la même session, la référence ~10 s du
p8-m4 re-mesurée au présent bac).

LA CIBLE pré-enregistrée au plan : ≤ 1 s (1 000 000 µs). LE VERDICT : les
condensés recoupés à hashlib (le juge croisé), la médiane publiée, TENUE ou
MANQUÉE telle quelle.

LE REJEU bit-identique : deux passes du moteur natif — les condensés identiques.
"""
import hashlib
import importlib.util
import json
import pathlib
import statistics
import subprocess
import sys
import time

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent
MOTEUR = ICI / "moteur_session"
CIBLE_US = 1_000_000.0              # ≤ 1 s pré-enregistrée au plan

sys.path.insert(0, str(R))
spec = importlib.util.spec_from_file_location(
    "harnais_noyau", str(R / "loupe" / "harnais_noyau.py"))
hn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hn)


def native(passes: int) -> dict:
    """LA MESURE NATIVE : l'ouverture seule horlogée, la médiane."""
    temoin = (ICI / "temoin-3f.bin").read_bytes()
    md5 = hashlib.md5(temoin).hexdigest()
    sha = hashlib.sha256(temoin).hexdigest()
    p = subprocess.run([str(MOTEUR), str(ICI / "image-bas.bin"),
                        str(ICI / "image-data.bin"), str(ICI / "temoin-3f.bin"),
                        md5, sha, str(passes)],
                       capture_output=True, timeout=300, cwd=str(ICI))
    sortie = p.stdout.decode()
    session = [float(l.split()[1]) for l in sortie.splitlines()
               if l.startswith("SESSION")][0]
    passes_us = [float(l.split()[1]) for l in sortie.splitlines()
                 if l.startswith("PASSE")]
    md5_ok = "md5=" in sortie and "(1)" in sortie.split("md5=")[1][:40]
    ouverture = sortie.splitlines()[0] if sortie else ""
    return {"code": p.returncode, "ouverture": ouverture,
            "md5_confronte": md5_ok, "sha_confronte": "(1)" in ouverture,
            "mediane_us": session, "passes_us": passes_us}


def jumeau(passes: int = 3) -> dict:
    """LA RÉFÉRENCE JUMEAU : la même session à l'émulateur du harnais."""
    os_v = hn.OSVirtuel()
    emul = hn.Emulation(os_v)
    donnees_m9 = open(str(R / hn.SCELLE_M9), "rb").read()
    donnees_m1 = open(str(R / hn.SCELLE_M1), "rb").read()
    emul.poser_heritages(donnees_m9, donnees_m1)
    temoins = hn.composer_temoins()
    os_v.declarer("temoin-3f.bin", hn.FichierVirtuel(contenu=temoins["temoin-3f.bin"]))
    temps = []
    empreintes = None
    for _ in range(passes):
        # la session RECOMMENCÉE : le CADRE remis au vierge (la poignée
        # INVALIDE +528) — le miroir du moteur natif
        emul.uc.mem_write(hn.L.R_CADRE + 528, b"\xFF" * 8)
        t0 = time.monotonic()
        hn.emplacer_session(emul, os_v, "temoin-3f.bin")
        temps.append(time.monotonic() - t0)
        empreintes = bytes(emul.uc.mem_read(hn.L.R_EMPREINTES, 48)).hex()
    return {"mediane_s": round(statistics.median(temps), 3),
            "passes_s": [round(t, 3) for t in temps],
            "empreintes_hex": empreintes}


def main():
    natif = native(5)
    natif_2 = native(5)               # LE REJEU bit-identique
    jum = jumeau(3)
    temoin = (ICI / "temoin-3f.bin").read_bytes()
    attendu = (hashlib.md5(temoin).hexdigest() + hashlib.sha256(temoin).hexdigest())
    rejeu_identique = (natif["md5_confronte"] and natif_2["md5_confronte"]
                       and natif["sha_confronte"] and natif_2["sha_confronte"]
                       and natif["ouverture"].split("md5=")[1][:33]
                       == natif_2["ouverture"].split("md5=")[1][:33])
    registre = {
        "cible_us": CIBLE_US,
        "temoin": {"octets": len(temoin),
                   "md5": hashlib.md5(temoin).hexdigest(),
                   "sha256": hashlib.sha256(temoin).hexdigest(),
                   "graine": 20261107},
        "natif": natif,
        "natif_rejeu": natif_2,
        "jumeau": jum,
        "rejeu_bit_identique": bool(rejeu_identique),
        "verdict": ("TENUE" if natif["mediane_us"] <= CIBLE_US else "MANQUÉE"),
        "note_rax": ("rax non spécifié sur le chemin de succès (l'épilogue ne "
                     "le pose pas — les condensés sont le verdict, la "
                     "confrontation à hashlib)"),
    }
    (ICI / "session-ouverture.json").write_text(
        json.dumps(registre, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[native] médiane {natif['mediane_us']:.1f} µs "
          f"(passes {['%.1f' % u for u in natif['passes_us']]})")
    print(f"[jumeau] médiane {jum['mediane_s']:.3f} s "
          f"(passes {jum['passes_s']})")
    print(f"[verdict] CIBLE ≤ 1 s : {registre['verdict']} "
          f"({natif['mediane_us']:.1f} µs = {natif['mediane_us']/1e6:.6f} s)")
    print(f"[rejeu] bit-identique : {rejeu_identique}")
    print(f"[empreintes jumeau] {jum['empreintes_hex'][:32]}…")


if __name__ == "__main__":
    main()
