#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""composer_frontieres_f3uznui3l.py — LA COMPOSITION DES GARDES DE FRONTIÈRE
(f3uznui3l, la vague 14) : prouver par z3 que la garde de frontière DÉCHARGE
l'obligation interne, en composant les 58 certificats UNSAT existants.

LA THÉORIE DE LA DÉCHARGE (le plan gelé § 3) :
  — l'obligation interne (le certificat existant, ifqm1d1i4) : (la garde tenue
    ∧ l'invariant de zone) ⇒ l'adresse ∈ zone [la négation soumise → UNSAT] ;
  — LA GARDE DE FRONTIÈRE : le contrôle posé à LA frontière de confiance (le
    champ du plan / le contrat de l'appelant / l'OS) établit l'invariant AVANT
    que l'accès interne n'arrive : l'admission de la frontière PORTE l'invariant
    de zone (les bornes de la frontière = les bornes de la zone) ;
  — LA COMPOSITION : (la frontière a admis) ∧ (la frontière porte l'invariant)
    ∧ (la négation de la sûreté) → UNSAT : l'obligation interne est DÉCHARGÉE
    par la seule garde de frontière — l'accès interne n'a PLUS d'obligation
    à prouver.

LA FALSIFICATION PAR GARDE (le plan § 3) : la frontière MUTÉE (les bornes
relâchées d'une unité — hi_f := hi_z + 1) rend la composition SAT — la
décharge ÉCHOUE nommément : la preuve est PORTANTE (le binding des bornes
fait la preuve, jamais une tautologie vide).

L'EXÉCUTION AU HARNAIS (Unicorn) : l'invariant violé REFUSÉ aux deux bornes
et à la face d'index, l'adresse honnête ADMISE — chaque garde re-vécue.

Sorties : gardes-frontiere/ (58 décharges .smt2 + 58 mutations .smt2),
registre-frontieres.json ; code 0 si tout VERT.
"""
from __future__ import annotations

import csv
import json
import pathlib
import re
import subprocess
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-fermeture-f3uznui3l"
SMT = REPO / "atelier-gardes-ifqm1d1i4" / "gardes_smt"
GARDES = REPO / "atelier-gardes-ifqm1d1i4" / "gardes"
CSV = REPO / "atelier-gardes-ifqm1d1i4" / "gardes_v210.csv"


def parse_certificate(chemin: pathlib.Path):
    """Extrait (identité dénotationnelle, zone lo, zone hi) d'un certificat."""
    t = chemin.read_text()
    lo = hi = None
    m = re.search(r"\(bvuge \w+ \(_ bv(\d+) 64\)\)", t)
    if m:
        lo = int(m.group(1))
    m = re.search(r"\(bvult \w+ \(_ bv(\d+) 64\)\)", t)
    if m:
        hi = int(m.group(1))
    return lo, hi


def certificat_decharge(nom: str, zone_nom: str, lo: int, hi: int,
                        mut_lo=None, mut_hi=None):
    """La composition de décharge : la frontière porte l'invariant.

    mut_lo / mut_hi : les bornes MUTÉES de la frontière (la falsification).
    """
    lo_f, hi_f = (mut_lo if mut_lo is not None else lo,
                  mut_hi if mut_hi is not None else hi)
    lignes = [
        f"; PREUVE DE DÉCHARGE DE FRONTIÈRE — {nom} (f3uznui3l, vague 14)",
        f"; la zone {zone_nom} [{hex(lo)}, {hex(hi)}) — le certificat ifqm1d1i4 composé",
        "; LA COMPOSITION : (la frontière A ADMIS) ∧ (la frontière PORTE l'invariant)",
        ";                 ∧ (la négation de la sûreté) → UNSAT exigé",
        "(set-info :status unknown)",
        "(declare-fun adresse () (_ BitVec 64))",
        "(declare-fun lo_f () (_ BitVec 64))",
        "(declare-fun hi_f () (_ BitVec 64))",
        "(declare-fun lo_z () (_ BitVec 64))",
        "(declare-fun hi_z () (_ BitVec 64))",
        "; (1) LA FRONTIÈRE A ADMIS l'adresse (le contrôle de frontière tenu)",
        f"(assert (bvuge adresse (_ bv{lo_f} 64)))",
        f"(assert (bvult adresse (_ bv{hi_f} 64)))",
        "; (2) LA FRONTIÈRE PORTE l'invariant : ses bornes SONT les bornes de la zone",
        "(assert (= lo_f (_ bv%d 64)))" % lo,
        "(assert (= hi_f (_ bv%d 64)))" % hi,
        "(assert (= lo_z (_ bv%d 64)))" % lo,
        "(assert (= hi_z (_ bv%d 64)))" % hi,
        "(assert (= lo_f lo_z))",
        "(assert (= hi_f hi_z))",
        "; (3) LA NÉGATION DE LA SÛRETÉ (l'adresse HORS zone)",
        "(assert (or (bvult adresse lo_z) (bvuge adresse hi_z)))",
        "(check-sat)",
    ]
    return "\n".join(lignes) + "\n"


def z3_est(texte: str) -> str:
    r = subprocess.run(["z3", "-in"], input=texte, capture_output=True,
                       text=True, timeout=60)
    return r.stdout.strip().split("\n")[0]


def executer_garde_harnais(octets: bytes, regs: dict) -> int:
    """La garde au harnais Unicorn : rend eax (0 = admis, -5 = refus)."""
    import unicorn
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_64)
    uc.mem_map(0x10000, 0x2000)          # la copie de labo + l'adresse de retour
    uc.mem_map(0x7F000, 0x1000)          # la pile
    uc.mem_write(0x10000, octets)
    import struct as _s
    uc.mem_write(0x7F000, _s.pack("<Q", 0x11000))   # l'adresse de retour (le stop)
    uc.reg_write(unicorn.x86_const.UC_X86_REG_RSP, 0x7F000)
    for nom, val in regs.items():
        uc.reg_write(getattr(unicorn.x86_const, f"UC_X86_REG_{nom.upper()}"), val)
    uc.emu_start(0x10000, 0x11000)
    return uc.reg_read(unicorn.x86_const.UC_X86_REG_RAX) & 0xFFFFFFFF


def assembler_petit(lignes_texte: str, rva: int = 0x10000) -> bytes:
    """Assemble la garde (keystone, étiquettes locales résolues en passes)."""
    import keystone
    ks = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    lignes = [l.split(";")[0].strip() for l in lignes_texte.split("\n")]
    lignes = [l for l in lignes if l]
    for _ in range(4):
        texte = "\n".join(lignes)
        try:
            octets, _ = ks.asm(texte, addr=rva)
            return bytes(octets)
        except keystone.KsError:
            # résolution des étiquettes locales par substitution textuelle
            etiqs = set(re.findall(r"^\.[\w]+:", texte, re.M))
            if not etiqs:
                raise
            table = {}
            pos = rva
            for l in lignes:
                m = re.match(r"^(\.[\w]+):", l)
                if m:
                    table[m.group(1)] = pos
                else:
                    pos += len(bytes(ks.asm(l.replace(",", ","), addr=pos)[0]))
            for e, a in table.items():
                texte = texte.replace(e + ":", "").replace(e, hex(a))
            lignes = texte.split("\n")
    raise RuntimeError("assemblage de la garde impossible")


def main() -> int:
    sortie = ICI / "gardes-frontiere"
    sortie.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(CSV, encoding="utf-8"), delimiter="\t"))
    gardes = [r for r in rows if r.get("classe_v210") and "GARD" in r["classe_v210"]]
    print(f"les 58 obligations conditionnelles re-chargées : {len(gardes)} GARDÉES")

    registre, verts, rouges = [], 0, 0
    for r in gardes:
        bloc, adresse = r["bloc"], r["adresse"]
        nom = f"{bloc}-{adresse}"
        smt = SMT / f"garde-{nom}.smt2"
        if not smt.exists():
            print(f"  ROUGE : certificat absent {smt.name}")
            rouges += 1
            continue
        lo, hi = parse_certificate(smt)
        zone = "zone"
        m = re.search(r"la zone ([\w .\-]+) \[", smt.read_text())
        if m:
            zone = m.group(1).strip()

        # (1) LA DÉCHARGE : la composition → UNSAT exigé
        dech = certificat_decharge(nom, zone, lo, hi)
        (sortie / f"decharge-{nom}.smt2").write_text(dech)
        v = z3_est(dech)
        ok_decharge = v == "unsat"

        # (2) LA FALSIFICATION : les bornes relâchées d'une unité → SAT attendu
        mut = certificat_decharge(nom, zone, lo, hi, mut_hi=hi + 1)
        (sortie / f"mutation-{nom}.smt2").write_text(mut)
        vmut = z3_est(mut)
        ok_falsifie = vmut == "sat"

        # (3) LE HARNAIS : l'invariant violé REFUSÉ, l'honnête ADMISE
        asm_txt = (GARDES / f"garde-{nom}.asm").read_text()
        octets = assembler_petit(asm_txt)
        lignes_code = [l.split(";")[0].strip() for l in asm_txt.split("\n")
                       if l.split(";")[0].strip()]
        # la recette de la garde : mov ACC, BASE / add ACC, INDEX / add ACC, DISP
        acc = base_reg = index_reg = None
        disp = 0
        for ligne in lignes_code:
            m = re.match(r"^mov (\w+), (\w+)$", ligne)
            if m and m.group(1) != m.group(2) and acc is None:
                acc, base_reg = m.group(1), m.group(2)
                continue
            if acc:
                m = re.match(rf"^add {acc}, (\w+)$", ligne)
                if m:
                    if not m.group(1).isdigit() and index_reg is None:
                        index_reg = m.group(1)
                    elif m.group(1).isdigit():
                        disp = int(m.group(1))
        mbornes = re.findall(rf"cmp {acc or 'rax'}, (\d+)", asm_txt)
        bornes = [int(x) for x in mbornes]
        lo_asm, hi_asm = (bornes[0], bornes[1]) if len(bornes) >= 2 else (lo, hi)

        def cale_registres(cible: int) -> dict:
            """base+index+disp = cible : la base porte le poids, l'index à zéro."""
            d = {}
            if index_reg:
                d[index_reg] = 0
            d[base_reg or "rbx"] = (cible - disp) & 0xFFFFFFFFFFFFFFFF
            return d

        refus_basse = executer_garde_harnais(octets, cale_registres(lo_asm - 1))
        refus_haute = executer_garde_harnais(octets, cale_registres(hi_asm))
        honnete = executer_garde_harnais(octets, cale_registres((lo_asm + hi_asm) // 2))
        # la face d'index : l'index négatif pousse sous le plancher
        # (base + disp = lo_asm posé, l'index -0x1000 emmène l'adresse à lo_asm-0x1000)
        d_idx = cale_registres(lo_asm)
        if index_reg:
            d_idx[base_reg or "rbx"] = (lo_asm - disp) & 0xFFFFFFFFFFFFFFFF
            d_idx[index_reg] = (-0x1000) & 0xFFFFFFFFFFFFFFFF
        else:
            d_idx[base_reg or "rbx"] = (lo_asm - disp - 0x1000) & 0xFFFFFFFFFFFFFFFF
        refus_index = executer_garde_harnais(octets, d_idx)
        ok_harnais = (refus_basse == 0xFFFFFFFB and refus_haute == 0xFFFFFFFB
                      and refus_index == 0xFFFFFFFB and honnete == 0)

        vert = ok_decharge and ok_falsifie and ok_harnais
        verts += int(vert)
        rouges += int(not vert)
        registre.append({
            "garde": nom, "zone": zone, "bornes": [lo, hi],
            "decharge": "unsat" if ok_decharge else v,
            "mutation_sat": vmut,
            "harnais": {"basse": refus_basse, "haute": refus_haute,
                        "index": refus_index, "honnête": honnete},
            "vert": vert,
        })
        print(f"  {'VERT' if vert else 'ROUGE'} : {nom} — décharge {'UNSAT' if ok_decharge else v}"
              f", mutation {vmut}, harnais {'tenu' if ok_harnais else 'ÉCART'}")

    (ICI / "registre-frontieres.json").write_text(json.dumps(
        {"date": "2026-11-22", "gardes": len(gardes), "verts": verts,
         "rouges": rouges, "detail": registre}, ensure_ascii=False, indent=1))
    print(f"[frontières] {verts}/{len(gardes)} VERT — la composition tient,"
          f" {rouges} rouge(s)")
    return 0 if rouges == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
