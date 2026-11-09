#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Différentiel intégral des habillages PE : loupe dev.7 vs demo 0.3.0.
16 data directories + contenu BASERELOC + caractéristiques de sections."""
import pefile

NOMS_DIR = ["EXPORT", "IMPORT", "RESOURCE", "EXCEPTION", "SECURITY", "BASERELOC",
            "DEBUG", "ARCHITECTURE", "GLOBAL_PTR", "TLS", "LOAD_CONFIG",
            "BOUND_IMPORT", "IAT", "DELAY_IMPORT", "CLR", "RESERVED"]

res = {}
for path, nom in [("/home/z/my-project/run8/loupe.exe", "LOUPE"),
                  ("/home/z/my-project/triade/demo/demo.exe", "DEMO")]:
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories()
    d = {}
    for i, e in enumerate(pe.OPTIONAL_HEADER.DATA_DIRECTORY):
        if e.VirtualAddress or e.Size:
            d[NOMS_DIR[i]] = (e.VirtualAddress, e.Size)
    res[nom] = d
    print(f"=== {nom} : directories non nulles ===")
    for k, (va, sz) in d.items():
        print(f"  {k:<14} RVA {va:#x} · taille {sz}")
    # BASERELOC contenu
    if "BASERELOC" in d:
        rva, sz = d["BASERELOC"]
        raw = pe.get_data(rva, sz)
        print(f"  BASERELOC brut : {raw.hex()}")
        try:
            pe.parse_data_directories(
                directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_BASERELOC']])
            for bloc in pe.DIRECTORY_ENTRY_BASERELOC:
                for ent in bloc.entries:
                    print(f"    reloc {ent.rva:#x} type {ent.type}")
        except Exception as e:
            print(f"    (analyse pefile : {e})")
    print()

print("=== les directories de LOUPE absentes chez DEMO (et réciproquement) ===")
for k in set(res["LOUPE"]) | set(res["DEMO"]):
    a, b = res["LOUPE"].get(k), res["DEMO"].get(k)
    if a != b:
        print(f"  {k:<14} LOUPE {a} · DEMO {b}")
