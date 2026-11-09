#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare les en-têtes optionnels loupe dev.7 vs demo 0.3.0 (via pefile)."""
import pefile

for path, nom in [("/home/z/my-project/run8/loupe.exe", "LOUPE dev.7"),
                  ("/home/z/my-project/triade/demo/demo.exe", "DEMO 0.3.0")]:
    pe = pefile.PE(path, fast_load=True)
    oh = pe.OPTIONAL_HEADER
    fh = pe.FILE_HEADER
    print(f"=== {nom} ===")
    print(f"  machine {fh.Machine:#x} · nsec {fh.NumberOfSections} · tds {fh.TimeDateStamp:#x}")
    print(f"  entry {oh.AddressOfEntryPoint:#x} · imgbase {oh.ImageBase:#x}")
    print(f"  SizeOfCode {oh.SizeOfCode:#x} · InitData {oh.SizeOfInitializedData:#x} · Uninit {oh.SizeOfUninitializedData:#x}")
    print(f"  SecAlign {oh.SectionAlignment:#x} · FileAlign {oh.FileAlignment:#x}")
    print(f"  ** SizeOfImage {oh.SizeOfImage:#x} ({oh.SizeOfImage}) ** · SizeOfHeaders {oh.SizeOfHeaders:#x}")
    print(f"  Checksum {oh.CheckSum:#x} · Subsystem {oh.Subsystem} · DllChars {oh.DllCharacteristics:#06x}")
    haut = max(s.VirtualAddress + s.Misc_VirtualSize for s in pe.sections)
    print(f"  besoin réel (VA+VS max des sections) : {haut:#x} ({haut})")
    print(f"  SizeOfImage couvre ? {'OUI' if oh.SizeOfImage >= haut else 'NON — HORS IMAGE !!'}")
    if "loupe" in path:
        print(f"  le peintre écrit 0xF4C0..0xFDD0, lit 0xFDE0/0xFDF0 → "
              f"{'couverts' if oh.SizeOfImage >= 0xFDF8 else 'HORS DE L IMAGE DECLAREE !!'}")
