#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Diagnostic du timeout de l'attente .curl (sup-34) dans le
superviseur terrain.

Question (née de la rétro-validation D61) : l'attente du premier curl
passe-t-elle BIEN 25 000 ms à WaitForSingleObject ? Si la constante était
INFINITE (0xFFFFFFFF), un curl zombie gèlerait le fil du scénario pour
toujours — une explication ALTERNATIVE de l'absence de S22 qui n'exigerait
aucun kill externe. Ce diagnostic tranche en résolvant le vrai slot IAT
visé par le call qui suit « mov edx, 25000 ».

Méthode :
  1. parse les en-têtes de sections du PE (mapping offset fichier <-> RVA) ;
  2. trouve « BA A8 61 00 00 » (mov edx, 25000) suivi d'un « FF 15 » ;
  3. résout la cible RIP-relative du call (offset fichier -> RVA) ;
  4. dresse la table d'imports COMPLETE (descripteurs, INT, noms) et nomme
     le slot visé ;
  5. balaye aussi les autres constantes d'attente du contrat sup-34/sup-35
     (10 s, 15 s, 25 s, 30 s, 35 s, 120 s, 130 s) pourvue la cohérence.

Usage :
  python3 scripts/diag_timeout_curl.py [EXE]
Défaut : terrain/livraison/superviseur-terrain9.exe
Code de sortie : 0 = lu, 2 = erreur.
"""

import pathlib
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DEFAUT = REPO / "terrain/livraison/superviseur-terrain9.exe"

CONSTANTES = [
    (0x2710, "10 s  (arrêt proxy quit, sup-34 Q6)"),
    (0x3A98, "15 s  (sondage bannière/événements, sup-34 Q2/Q4)"),
    (0x61A8, "25 s  (attente curl, sup-34 Q3)"),
    (0x7530, "30 s  (curl OAuth/session, sup-35 Q3/Q6)"),
    (0x88B8, "35 s  (attente curl jeton/session, sup-35)"),
    (0x1D4C0, "120 s (téléversement PUT, sup-35 Q7)"),
    (0x202A0, "130 s (attente téléversement, sup-35 I4)"),
]


def sections(data):
    """[(nom, rva, vsize, file_off, rawsize)] du PE."""
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[pe_off:pe_off + 4] == b"PE\0\0", "pas un PE"
    nsec = struct.unpack_from("<H", data, pe_off + 6)[0]
    opt_size = struct.unpack_from("<H", data, pe_off + 20)[0]
    sec0 = pe_off + 24 + opt_size
    out = []
    for i in range(nsec):
        b = sec0 + 40 * i
        nom = data[b:b + 8].rstrip(b"\0").decode(errors="replace")
        vsize, rva, rawsize, rawoff = struct.unpack_from("<IIII", data, b + 8)
        out.append((nom, rva, vsize, rawoff, rawsize))
    return out


def file_to_rva(secs, off):
    for nom, rva, vsize, rawoff, rawsize in secs:
        if rawoff <= off < rawoff + rawsize:
            return rva + (off - rawoff), nom
    return None, None


def rva_to_file(secs, rva):
    for nom, r0, vsize, rawoff, rawsize in secs:
        if r0 <= rva < r0 + max(vsize, rawsize):
            return rawoff + (rva - r0), nom
    return None, None


def imports(data, secs):
    """{rva_slot: 'dll!Fonction'} — dresse l'IAT par l'INT/OFT."""
    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    opt = pe_off + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    ddir = opt + (240 if magic == 0x20B else 224) - 128  # data directory 1
    imp_rva, imp_size = struct.unpack_from("<II", data, ddir)
    slots = {}
    if not imp_rva:
        return slots
    imp_off, _ = rva_to_file(secs, imp_rva)
    if imp_off is None:
        return slots
    i = 0
    while True:
        ent = imp_off + 20 * i
        iat_rva, ts, fwd, namerva, ft_rva = struct.unpack_from("<IIIII", data, ent)
        if not any((iat_rva, namerva, ft_rva)):
            break
        dll_off, _ = rva_to_file(secs, namerva)
        dll = data[dll_off:data.find(b"\0", dll_off)].decode(errors="replace") \
            if dll_off else "?"
        # parcours l'INT (ou FT si INT vide) pour l'ordre des slots
        int_rva = ft_rva  # motif demo D53/D54 : OFT/FT pré-remplies
        walker = ft_rva if ft_rva else iat_rva
        j = 0
        while True:
            w_off, _ = rva_to_file(secs, walker + 8 * j)
            if w_off is None:
                break
            val = struct.unpack_from("<Q", data, w_off)[0]
            if val == 0:
                break
            slot_rva = iat_rva + 8 * j
            if val & (1 << 63):
                slots[slot_rva] = f"{dll}!ordinal{val & 0xFFFF}"
            else:
                hint_off, _ = rva_to_file(secs, val & 0xFFFFFFFF)
                if hint_off:
                    fin = data.find(b"\0", hint_off + 2)
                    nom = data[hint_off + 2:fin].decode(errors="replace")
                    slots[slot_rva] = f"{dll}!{nom}"
            j += 1
        i += 1
    return slots


def main():
    chemin = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAUT
    data = chemin.read_bytes()
    secs = sections(data)
    print(f"[diag] {chemin.name} — {len(secs)} sections :")
    for nom, rva, vsize, rawoff, rawsize in secs:
        print(f"  .{nom:8s} rva 0x{rva:05x}  file 0x{rawoff:05x}  "
              f"(0x{rawsize:x} o)")

    slots = imports(data, secs)
    print(f"[diag] IAT dressée : {len(slots)} slots nommés")

    # --- le motif : mov edx, 25000 ; call [rip+disp]
    #     ⚠ le calcul RIP-relatif se fait en ADRESSES VIRTUELLES (RVA) :
    #     instruction (.text2) et cible (.rdata) ne partagent pas le même
    #     delta fichier→RVA — leçon de la fausse alerte D61.
    motif = bytes.fromhex("BAA8610000FF15")
    pos = data.find(motif)
    print(f"\n[diag] motif « mov edx,25000 ; call [rip] » : "
          + (f"offset fichier 0x{pos:x}" if pos >= 0 else "INTROUVABLE"))
    if pos >= 0:
        disp = struct.unpack_from("<i", data, pos + 7)[0]
        rva_instr, sec_instr = file_to_rva(secs, pos + 5)   # le call
        rva_rip = rva_instr + 6                              # fin du call
        cible_rva = rva_rip + disp
        cible_off, sec_cible = rva_to_file(secs, cible_rva)
        print(f"        call @rva 0x{rva_instr:x} ({sec_instr}) → cible rva 0x{cible_rva:x} ({sec_cible})")
        if cible_off is not None:
            ft = struct.unpack_from("<Q", data, cible_off)[0]
            print(f"        contenu du slot : 0x{ft:016x}")
            if ft & (1 << 63):
                print("        → ordinal (pas un nom) — inattendu ici")
            elif ft:
                hint_off, _ = rva_to_file(secs, ft & 0xFFFFFFFF)
                if hint_off is not None:
                    fin = data.find(b"\0", hint_off + 2)
                    nom = data[hint_off + 2:fin].decode(errors="replace")
                    verdict = ("CONFORME : WaitForSingleObject, timeout 25 s borné "
                               "— un curl gelé aurait rendu S22 en ≤ 25 s, "
                               "l'absence de S22 ⇒ fil mort (kill externe D59)"
                               if nom == "WaitForSingleObject"
                               else "INATTENDU : " + nom)
                    print(f"        → FT pointe vers : {nom}   [{verdict}]")
            else:
                print("        → slot VIDE (FT nulle) — le chargeur doit la "
                      "remplir")

    # --- balayage des autres constantes d'attente
    print("\n[diag] autres constantes d'attente du contrat (mov edx, imm32) :")
    for val, label in CONSTANTES:
        motif_c = b"\xBA" + struct.pack("<I", val)
        n = data.count(motif_c)
        print(f"  {label:44s} : {n} occurrence(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
