#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diff_dev3_dev4.py — LE DIFF CONTRÔLÉ du rebuild 1.0.0-dev.4 (la
révision 3 de la spec sys-06, l'erratum n° 10 — Entrée 191/192).

Le dev.3 (de23e577…, la pièce des runs 3..6 et de la sonde sys-06)
est extrait du kit ACQUITTÉ (kit-m9f.zip md5 79d44284… — le contenu
livré au coffre /test, la source du terrain) ; le dev.4 est l'arbre
vivant (tls13/proxy.exe, sha256 446279f3…). Le précédent du dev.2 →
dev.3 (Entrée 188) : TROIS octets — la version R10 + LES DEUX POSES
DU WSABUF (0x64 → 0x68). L'ATTENTE NOMMÉE D'AVANCE pour dev.3 →
dev.4 : TROIS octets ENCORE — la version R10 @0x2820 (0x03 → 0x04,
geste de BUILD, jamais scellage) + LES DEUX IMMEDIATES DU CONTRAT
D'APPEL dans sys-06 (le seul bloc re-noté R3 : AfdFlags 0x20 → 0,
TdiFlags 0 → 0x20 — le MÊME encode mov dword 8 o, le slot intact,
la carte demeure) ; TOUT le reste byte-identique (l'héritage R7
prouvé PAR L'ÉVIDENCE, la réparation NOMMÉE à l'octet).

La relecture dans l'image : le QUATRIÈME champ porte le 0x20, le
TROISIÈME porte 0 — `c7 44 24 7c 00 00 00 00` (AfdFlags) et
`c7 44 24 80 20 00 00 00` (TdiFlags) aux DEUX sites du bloc sys-06.

Usage : python3 scripts/diff_dev3_dev4.py
Code de sortie : 0 = diff contrôlé VERT ; 2 = refus nommé."""

import hashlib
import pathlib
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
KIT_ZIP = pathlib.Path("/home/z/my-project/download/kit-m9f.zip")
KIT_MD5 = "79d44284c70261375a2b055070fda223"          # le kit ACQUITTÉ (dev.3)
SHA_DEV3 = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
            "66b29226f")
SHA_DEV4 = ("446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453d"
            "b3b00d93d")
TAILLE = 65024
RVA_VERSION = 0x2820          # .rdata — la version R10 (le delta de build)
SYS06_VA, SYS06_SLOT = 0xA6C0, 0x180   # le bloc re-noté R3 (384 o)


def refus(nom, detail):
    print(f"[diff-dev3-dev4] REFUS {nom} : {detail}")
    sys.exit(2)


def rva_vers_offset(data, rva):
    """RVA -> offset fichier (PE32+ de l'artefact, sections lues sur pièces)."""
    import struct
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, e_lfanew + 6)[0]
    opt = e_lfanew + 24
    for i in range(nsec):
        off = opt + 240 + i * 40
        vsize, va, _rs, raw = struct.unpack_from("<IIII", data, off + 8)
        if va <= rva < va + max(vsize, 0x1000):
            return raw + (rva - va)
    refus("RVA", f"le RVA {rva:#x} n'appartient à aucune section")


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def md5_fichier(chemin):
    import hashlib as _h
    h = _h.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def main() -> int:
    # -- 1. le dev.3 : la pièce du terrain, extraite du kit ACQUITTÉ --------
    if not KIT_ZIP.is_file():
        refus("KIT", f"{KIT_ZIP} absent — le kit acquitté est la source")
    if md5_fichier(KIT_ZIP) != KIT_MD5:
        refus("KIT-MD5", f"{KIT_ZIP} md5 {md5_fichier(KIT_ZIP)} != {KIT_MD5}")
    with zipfile.ZipFile(KIT_ZIP) as z:
        dev3 = z.read("m9-kit/proxy.exe")
    sha_dev3 = hashlib.sha256(dev3).hexdigest()
    if sha_dev3 != SHA_DEV3:
        refus("DEV3", f"le proxy du kit : sha256 {sha_dev3} != {SHA_DEV3}")

    # -- 2. le dev.4 : l'arbre vivant ---------------------------------------
    chemin_dev4 = REPO / "tls13" / "proxy.exe"
    if not chemin_dev4.is_file():
        refus("DEV4", "tls13/proxy.exe absent")
    dev4 = chemin_dev4.read_bytes()
    sha_dev4 = hashlib.sha256(dev4).hexdigest()
    if sha_dev4 != SHA_DEV4:
        refus("DEV4", f"tls13/proxy.exe sha256 {sha_dev4} != {SHA_DEV4}")
    if len(dev3) != TAILLE or len(dev4) != TAILLE:
        refus("TAILLE", f"dev.3 {len(dev3)} o / dev.4 {len(dev4)} o != {TAILLE}")

    # -- 3. le diff octet par octet -----------------------------------------
    divergents = [i for i in range(TAILLE) if dev3[i] != dev4[i]]
    print(f"[diff-dev3-dev4] dev.3 (pièce du kit acquitté) {sha_dev3[:16]}…")
    print(f"[diff-dev3-dev4] dev.4 (l'arbre vivant)       {sha_dev4[:16]}…")
    print(f"[diff-dev3-dev4] {len(divergents)} octet(s) divergent(s) sur "
          f"{TAILLE} : "
          + (", ".join(f"@{i:#x} ({dev3[i]:#04x} → {dev4[i]:#04x})"
                       for i in divergents) or "AUCUN"))

    # -- 4. l'attente nommée d'avance : TROIS octets, RIEN d'autre ----------
    # (les offsets fichier sont ramenés en RVA — les adresses du plan)
    off_version = rva_vers_offset(dev3, RVA_VERSION)
    off_sys06 = rva_vers_offset(dev3, SYS06_VA)
    fin_sys06 = rva_vers_offset(dev3, SYS06_VA + SYS06_SLOT - 1)
    rva_de = {i: None for i in divergents}
    print(f"[diff-dev3-dev4] (la version R10 @RVA {RVA_VERSION:#x} = offset "
          f"fichier {off_version:#x} ; le bloc sys-06 @RVA {SYS06_VA:#x} = "
          f"offset {off_sys06:#x})")

    if len(divergents) != 3:
        refus("NOMBRE", f"{len(divergents)} octets divergents — TROIS "
              f"attendus (la version R10 + LES DEUX IMMEDIATES du contrat "
              f"d'appel dans sys-06 : AfdFlags 0x20 → 0, TdiFlags 0 → 0x20)")

    sites = {}
    for i in divergents:
        if i == off_version:
            sites[i] = f"LA VERSION R10 @RVA {RVA_VERSION:#x} (.rdata)"
            if not (dev3[i] == 0x03 and dev4[i] == 0x04):
                refus("VERSION", f"@{i:#x} : {dev3[i]:#04x} → {dev4[i]:#04x} "
                      f"(0x03 → 0x04 attendu — le geste de BUILD, jamais "
                      f"scellage)")
        elif off_sys06 <= i <= fin_sys06:
            sites[i] = (f"sys-06 @RVA {SYS06_VA + (i - off_sys06):#x} (le bloc "
                        f"re-noté R3, slot [{SYS06_VA:#x}, "
                        f"{SYS06_VA + SYS06_SLOT:#x}))")
        else:
            refus("SITE", f"@offset {i:#x} hors des sites attendus (la version "
                  f"@RVA {RVA_VERSION:#x} + le slot sys-06 "
                  f"[{SYS06_VA:#x}, {SYS06_VA + SYS06_SLOT:#x})) — RIEN "
                  f"d'autre ne doit bouger (l'héritage R7)")

    # les DEUX immediates du contrat d'appel : AfdFlags 0x20 → 0 (le
    # TROISIÈME champ), TdiFlags 0 → 0x20 (le QUATRIÈME champ)
    dans_sys06 = sorted(i for i in divergents if off_sys06 <= i <= fin_sys06)
    if len(dans_sys06) != 2:
        refus("SYS06", f"{len(dans_sys06)} octets dans sys-06 — DEUX attendus")
    # l'Ancienne valeur du premier site (offset croissant) : AfdFlags
    i_afdi, i_tdi = dans_sys06
    if not (dev3[i_afdi] == 0x20 and dev4[i_afdi] == 0x00):
        refus("AFDFLAGS", f"@{i_afdi:#x} : {dev3[i_afdi]:#04x} → "
              f"{dev4[i_afdi]:#04x} (0x20 → 0 attendu — le VRAI afd.sys "
              f"REFUSE le bit 0x20 dans AfdFlags, la mesure de la sonde)")
    if not (dev3[i_tdi] == 0x00 and dev4[i_tdi] == 0x20):
        refus("TDIFLAGS", f"@{i_tdi:#x} : {dev3[i_tdi]:#04x} → "
              f"{dev4[i_tdi]:#04x} (0 → 0x20 attendu — TDI_RECEIVE_NORMAL "
              f"RETOURNE au champ TdiFlags, le placement de la littérature)")

    # -- 5. la relecture dans l'image : le contrat réparé NOMMÉ ------------
    def fenetre(off):
        return " ".join(f"{b:02x}" for b in dev4[off - 4:off + 4])
    for i, nom in ((i_afdi, "AfdFlags = 0 (le TROISIÈME champ)"),
                   (i_tdi, "TdiFlags = TDI_RECEIVE_NORMAL 0x20 "
                           "(le QUATRIÈME champ)")):
        # l'instruction mov dword ptr [rsp + disp], imm32 — DEUX formes
        # canoniques : disp8 (c7 44 24 dd ii 00 00 00, 8 o — le site
        # divergent est l'imm à +4) OU disp32 (c7 84 24 dd dd dd dd ii
        # 00 00 00, 11 o — [rsp+0x80] DÉPASSE la portée disp8, le site
        # divergent est l'imm à +7)
        for debut, attendu in ((i - 4, b"\xc7\x44\x24"), (i - 7, b"\xc7\x84\x24")):
            enc = dev4[debut:debut + (8 if attendu[1] == 0x44 else 11)]
            if enc[:3] == attendu:
                break
        else:
            refus("ENCODE", f"@{i:#x} : {fenetre(i)} — le canonique "
                  f"mov dword ptr [rsp+disp] attendu (c7 44 24 … ou "
                  f"c7 84 24 …)")
        disp = (enc[3] if attendu[1] == 0x44
                else int.from_bytes(enc[3:7], "little"))
        imm = int.from_bytes(enc[-4:], "little")
        print(f"[diff-dev3-dev4] le contrat réparé relu dans l'image "
              f"@{debut:#x} : {' '.join(f'{b:02x}' for b in enc)} "
              f"— {nom} (disp {disp:#x}, imm32 {imm:#x})")

    # le bloc sys-06 : les AUTRES octets du slot byte-identiques
    ecart_slot = sum(1 for i in range(off_sys06, fin_sys06 + 1)
                     if dev3[i] != dev4[i])
    print(f"[diff-dev3-dev4] le slot sys-06 [{SYS06_VA:#x}, "
          f"{SYS06_VA + SYS06_SLOT:#x}) : {ecart_slot} octet(s) divergent(s) "
          f"— les DEUX immediates seules, les encodes canoniques intacts "
          f"(disp8 @0x7c, disp32 @0x80 : la portée dépassée Nommée), le slot "
          f"intact")
    hors = [i for i in divergents if i != off_version
            and not (off_sys06 <= i <= fin_sys06)]
    if hors:
        refus("HORS-SITES", f"octets divergents inattendus : {hors}")

    rva_afdi = SYS06_VA + (i_afdi - off_sys06)
    rva_tdi = SYS06_VA + (i_tdi - off_sys06)
    print(f"[diff-dev3-dev4] DIFF CONTRÔLÉ VERT — TROIS octets sur "
          f"{TAILLE} : la version R10 @RVA 0x2820 (0x03 → 0x04) + LES DEUX "
          f"IMMEDIATES du contrat d'appel dans sys-06 (@RVA {rva_afdi:#x} : "
          f"AfdFlags 0x20 → 0 ; @RVA {rva_tdi:#x} : TdiFlags 0 → 0x20) ; TOUT "
          f"le reste byte-identique — l'héritage R7 prouvé PAR L'ÉVIDENCE, "
          f"la réparation NOMMÉE à l'octet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
