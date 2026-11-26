#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""extraire_image.py — L'IMAGE LOUPE EXTRAITE DU HARNAIS (W29MOTEUR, geste 2 :
l'ouverture de session). L'image posée aux RVA du plan (les notations du noyau,
les héritages extraits des scellés, les tables MD5, l'IAT) — l'émulateur du
harnais_noyau la monte en mémoire : la présente passe DUMP les régions aux
octets mêmes pour le montage NATIF du moteur (le harnais est le lecteur
canonique, le moteur natif reçoit LES MÊMES OCTETS).

Écrit : image-bas.bin (0x1000..0xD000 — libc + rdata + text2 + sha héritées),
        image-data.bin (0xE000..0x20000 — .data, le CADRE vierge à la poignée
        INVALIDE +528), temoin-3f.bin (le témoin 196 609 o, graine 20261107).
"""
import importlib.util
import pathlib
import random
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ICI = pathlib.Path(__file__).resolve().parent

sys.path.insert(0, str(R))
spec = importlib.util.spec_from_file_location(
    "harnais_noyau", str(R / "loupe" / "harnais_noyau.py"))
hn = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hn)


def main():
    os_v = hn.OSVirtuel()
    emul = hn.Emulation(os_v)
    # LES HÉRITAGES des scellés posés aux slots (R7) — le geste V0/V1 du harnais
    donnees_m9 = open(str(R / hn.SCELLE_M9), "rb").read()
    donnees_m1 = open(str(R / hn.SCELLE_M1), "rb").read()
    assert (len(donnees_m9) == hn.SCELLE_M9_TAILLE
            and __import__("hashlib").sha256(donnees_m9).hexdigest()
            == hn.SCELLE_M9_SHA256), "le scellé 1.0.0 diverge"
    assert (len(donnees_m1) == hn.SCELLE_M1_TAILLE
            and __import__("hashlib").sha256(donnees_m1).hexdigest()
            == hn.SCELLE_M1_SHA256), "le scellé M1 diverge"
    emul.poser_heritages(donnees_m9, donnees_m1)
    bas = bytes(emul.uc.mem_read(0x1000, 0xD000 - 0x1000))
    donnees = bytes(emul.uc.mem_read(0xE000, 0x20000 - 0xE000))
    (ICI / "image-bas.bin").write_bytes(bas)
    (ICI / "image-data.bin").write_bytes(donnees)
    # LE TÉMOIN : la génération FIXE graine 20261107 (composer_temoins)
    temoins = hn.composer_temoins()
    (ICI / "temoin-3f.bin").write_bytes(temoins["temoin-3f.bin"])
    import hashlib
    print("image-bas.bin", len(bas), "octets · image-data.bin", len(donnees),
          "octets · temoin-3f.bin", len(temoins["temoin-3f.bin"]), "octets")
    print("md5 témoin   :", hashlib.md5(temoins["temoin-3f.bin"]).hexdigest())
    print("sha256 témoin:", hashlib.sha256(temoins["temoin-3f.bin"]).hexdigest())
    # LE CONTRÔLE : le CADRE à la poignée INVALIDE à +528 (0xFF×8), les
    # héritages posés (memset @0x13C0 non nul)
    cadre = donnees[:960]
    assert cadre[528:536] == b"\xFF" * 8, "le CADRE doit porter la poignée INVALIDE"
    assert bas[0x13C0 - 0x1000:0x13C0 - 0x1000 + 8] != b"\x00" * 8, \
        "libc-07 memset doit être posé à 0x13C0"
    print("CADRE +528 : la poignée INVALIDE présente · héritages posés (memset @0x13C0)")


if __name__ == "__main__":
    main()
