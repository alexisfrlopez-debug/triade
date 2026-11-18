#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pe_inspect.py — l'inspection PURE-FICHIER d'un PE (les lois du bac) :
exports (la table), imports (les descripteurs aux CINQ champs, les feuilles
par plages FT), sections. Aucun Windows requis."""
import struct
import sys


def rva_of(sections, rva):
    for nom, va, vsize, raw, rsize in sections:
        if va <= rva < va + max(vsize, rsize):
            return raw + (rva - va)
    return None


def inspect(chemin):
    data = open(chemin, "rb").read()
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[e_lfanew:e_lfanew + 4] == b"PE\x00\x00", "pas un PE"
    machine = struct.unpack_from("<H", data, e_lfanew + 4)[0]
    nb_sections = struct.unpack_from("<H", data, e_lfanew + 6)[0]
    opt_size = struct.unpack_from("<H", data, e_lfanew + 20)[0]
    opt = e_lfanew + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    entry = struct.unpack_from("<I", data, opt + 16)[0]
    base_image = struct.unpack_from("<Q", data, opt + 24)[0]
    print(f"machine={machine:#x} sections={nb_sections} magic={magic:#x} "
          f"entry_rva={entry:#x} base={base_image:#x}")
    secs = []
    for i in range(nb_sections):
        s = opt + opt_size + 40 * i
        nom = data[s:s + 8].rstrip(b"\x00").decode("latin1")
        vsize, va, rsize, raw = struct.unpack_from("<IIII", data, s + 8)
        secs.append((nom, va, vsize, raw, rsize))
        print(f"  section {nom:10s} va={va:#010x} vsize={vsize:#x} raw={raw:#010x} rsize={rsize:#x}")

    def octets(rva, n):
        o = rva_of(secs, rva)
        return data[o:o + n] if o is not None else None

    def chaine(rva):
        o = rva_of(secs, rva)
        if o is None:
            return None
        e = data.index(b"\x00", o)
        return data[o:e].decode("latin1")

    # répertoires
    rep_export = struct.unpack_from("<I", data, opt + 112)[0]
    rep_import = struct.unpack_from("<I", data, opt + 120)[0]
    print(f"rep_export={rep_export:#x} rep_import={rep_import:#x}")

    print("\n== EXPORTS ==")
    if rep_export:
        nb_noms = struct.unpack_from("<I", octets(rep_export + 24, 4))[0]
        tab_f = struct.unpack_from("<I", octets(rep_export + 28, 4))[0]
        tab_n = struct.unpack_from("<I", octets(rep_export + 32, 4))[0]
        tab_o = struct.unpack_from("<I", octets(rep_export + 36, 4))[0]
        noms = []
        for i in range(nb_noms):
            nom = chaine(struct.unpack_from("<I", octets(tab_n + 4 * i, 4))[0])
            ordinal = struct.unpack_from("<H", octets(tab_o + 2 * i, 2))[0]
            rva_f = struct.unpack_from("<I", octets(tab_f + 4 * ordinal, 4))[0]
            noms.append((nom, rva_f))
            print(f"  {nom} @+{rva_f:#x}")
    else:
        print("  (aucun)")

    print("\n== IMPORTS (le parse aux CINQ champs, la marche des plages FT) ==")
    feuilles = {}
    if rep_import:
        num = 0
        while True:
            desc = rep_import + 20 * num
            champs = octets(desc, 20)
            if champs is None:
                print("  [hors sections — REFUS]")
                break
            ilt, horodatage, forwarder, rva_dll, iat = struct.unpack("<IIIII", champs)
            if ilt == 0 and iat == 0:
                break
            dll = chaine(rva_dll)
            marche = ilt if ilt else iat   # la doctrine D54 : les plages FT
            noms_ft = []
            k = 0
            while True:
                entree = struct.unpack("<Q", octets(marche + 8 * k, 8))[0]
                if entree == 0:
                    break
                if entree & (1 << 63):
                    noms_ft.append(f"ordinal#{entree & 0xFFFF}")
                else:
                    noms_ft.append(chaine(entree + 2))
                k += 1
            # les valeurs sur disque de la plage IAT
            sur_disque = [struct.unpack("<Q", octets(iat + 8 * j, 8))[0]
                          for j in range(len(noms_ft))]
            feuilles[dll] = list(zip(noms_ft, sur_disque))
            print(f"  {dll} : {len(noms_ft)} feuilles — {noms_ft}")
            for j, (n, v) in enumerate(zip(noms_ft, sur_disque)):
                print(f"      slot @+{iat + 8 * j:#x} {n:20s} sur-disque {v:#x}")
            num += 1
    return secs, feuilles


if __name__ == "__main__":
    inspect(sys.argv[1])
