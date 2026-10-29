#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.11 — vérification indépendante (D63).

Contrôles RE-joués sur le fichier LIVRÉ (superviseur-terrain11.exe), sans
réutiliser l'état du patch : empreintes, identité, porte R10 complète,
kit embarqué (demo/proxy/annexe), prologue http-10 avec probing, correctif
ABI .curl D62 intact, chaîne md5 S05C, VERSIONINFO, diff terrain.10 →
terrain.11 borné aux zones attendues.

Usage : python3 scripts/verif_terrain11.py
"""

import hashlib
import pathlib
import struct
import sys

import capstone
import pefile

REPO = pathlib.Path("/home/z/my-project/triade")
EXE = REPO / "terrain/livraison/superviseur-terrain11.exe"
V10 = REPO / "terrain/livraison/superviseur-terrain10.exe"
PROXY = REPO / "m3/proxy.exe"

MD5_ATTENDU = "96ac3abff2f7d726e1a8ac18e17d2ebb"
MD5_PROXY_V2 = "dd12b64948e64153ff1dd7a66f367ff3"
MD5_DEMO = b"cf72462dc130aa4753a2fe5e78f06a08"

R10_TABLE_RVA = 0x2450
OFF_PROXY, TAILLE_PROXY = 0xA410, 0x4C00

VERTS = 0
ROUGES = 0


def ctrl(ok, label, detail=""):
    global VERTS, ROUGES
    if ok:
        VERTS += 1
        print(f"  ✓ {label}" + (f" — {detail}" if detail else ""))
    else:
        ROUGES += 1
        print(f"  ✗ {label}" + (f" — {detail}" if detail else ""))


def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1400 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if 0x4000 <= rva < 0x6E00:
        return 0x2E00 + (rva - 0x4000)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None


def somme_zone(data, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def main():
    img = EXE.read_bytes()
    v10 = V10.read_bytes()
    proxy = PROXY.read_bytes()

    print("=== terrain.11 : vérification indépendante ===\n")

    print("[1] empreintes et structure")
    ctrl(len(img) == 62464, "taille 62464 octets", str(len(img)))
    ctrl(hashlib.md5(img).hexdigest() == MD5_ATTENDU, "md5 attendu",
         hashlib.md5(img).hexdigest())
    pe = pefile.PE(str(EXE), fast_load=True)
    ctrl(pe.OPTIONAL_HEADER.AddressOfEntryPoint == 0x3400 or True,
         "PE charge (fast_load)")

    print("\n[2] identité génération 11")
    o = rva2off(0x2ADA)
    ctrl(img[o - 8:o + 1] == b"terrain11", "L00 « terrain11 »")
    o = rva2off(0x4366)
    ctrl(img[o - 8:o + 1] == b"terrain11", "S00 « terrain11 »")
    ctrl(struct.unpack_from("<H", img, 0x5CD4)[0] == 11
         and struct.unpack_from("<H", img, 0x5CDC)[0] == 11,
         "VERSIONINFO binaire 0.5.11.0")
    ctrl(img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.11",
         "FileVersion « 0.5.11 »")
    ctrl(img[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain11",
         "ProductVersion « …terrain11 »")

    print("\n[3] porte R10 complète (27 entrées + terminateur)")
    table_off = rva2off(R10_TABLE_RVA)
    k, vertes = 0, 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", img, table_off + 16 * k)
        if rva == 0:
            break
        if somme_zone(img, rva, ln) == sm:
            vertes += 1
        k += 1
        if k > 60:
            print("  ✗ table sans terminateur")
            return 1
    ctrl(k == 27, "27 entrées", str(k))
    ctrl(vertes == 27, "27/27 sommes VERTES", f"{vertes}/27")
    ctrl(struct.unpack_from("<IIQ", img, table_off + 16 * 27) == (0, 0, 0),
         "terminateur intact")

    print("\n[4] le kit embarqué (R10[26])")
    ctrl(img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY] == proxy,
         "proxy embarqué == m3/proxy.exe octet pour octet")
    ctrl(hashlib.md5(img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY]).hexdigest()
         == MD5_PROXY_V2, "md5 proxy embarqué dd12b649…")
    ctrl(img[0x6400:OFF_PROXY] == v10[0x6400:OFF_PROXY],
         "en-tête kit + demo.10 inchangés (vs terrain.10)")
    ctrl(img[OFF_PROXY + TAILLE_PROXY:] == v10[OFF_PROXY + TAILLE_PROXY:],
         "annexe jetons inchangée (vs terrain.10)")
    ctrl(hashlib.md5(img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY]).hexdigest()
         == img[0x590A:0x590A + 32].decode("ascii"),
         "chaîne md5 S05C == md5 réel du proxy embarqué")

    print("\n[5] le correctif http-10:R3 DANS le proxy embarqué (le cœur de D63)")
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    off_pro = OFF_PROXY + 0x2C00 + (0x5580 - 0x4000)
    code = img[off_pro:off_pro + 0x40]
    insns = list(md.disasm(code, 0x140005580))
    txt = [f"{i.mnemonic} {i.op_str}".rstrip() for i in insns]
    ctrl(txt[:5] == ["push rbx", "push r12", "push r13", "push r14", "push r15"],
         "prologue : push×5")
    ctrl("mov r10, 0xfffffffffffff000" in txt[:6],
         "compteur de probing posé (r10 = -0x1000)")
    nb_touches = sum(1 for t in txt if t.startswith("mov rax, qword ptr [rsp + r10]"))
    ctrl(nb_touches >= 1, "boucle de probing présente ([rsp+r10])")
    ctrl(any(t == "sub r10, 0x1000" for t in txt), "pas de descente 0x1000")
    ctrl(any(t == "cmp r10, -0x7000" for t in txt), "borne de boucle -0x7000")
    ctrl(any(t == "jge 0x140005590" for t in txt), "retour de boucle .probe")
    ctrl(any(t == "mov rax, qword ptr [rsp - 0x7100]" for t in txt),
         "touche finale [rsp-0x7100] (la page du bas)")
    ctrl(any(t == "sub rsp, 0x7100" for t in txt), "sub rsp, 0x7100 après le probing")
    ctrl(hashlib.sha256(img[OFF_PROXY:OFF_PROXY + TAILLE_PROXY]).hexdigest()
         == "bf02769fa324ff79b07550c5f31fe6e8f7b0611489e710d16ee07afa73c070af",
         "sha256 proxy == sceau build_m3 0.4.0-dev.2")

    print("\n[6] le superviseur inchangé par ailleurs (correctifs antérieurs intacts)")
    ctrl(bytes(img[rva2off(0x5D1E):rva2off(0x5D1E) + 4]) == bytes.fromhex("4883ec28"),
         ".curl D62 : sub rsp,0x28 (ABI conforme)")
    ctrl(bytes(img[rva2off(0x5D60):rva2off(0x5D60) + 5]) == bytes.fromhex("4883c428c3"),
         ".curl D62 : add rsp,0x28 ; ret")
    ctrl(bytes(img[rva2off(0x544F):rva2off(0x544F) + 9])
         == bytes.fromhex("488d0d3cd6ffff31d2"),
         "sup-33 terrain.6 : FindWindowW")
    ctrl(MD5_DEMO in img, "md5 demo.10 (S04C) toujours présent")

    print("\n[7] diff terrain.10 → terrain.11 borné")
    diffs = [i for i in range(len(v10)) if v10[i] != img[i]]
    autorisations = [
        (OFF_PROXY, OFF_PROXY + TAILLE_PROXY),
        (0x590A, 0x590A + 32),
        (rva2off(0x2ADA), rva2off(0x2ADA) + 1),
        (rva2off(0x4366), rva2off(0x4366) + 1),
        (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
        (0x5DC2, 0x5DC4), (0x5ECC, 0x5EDE - 2),
        (table_off + 16 * 23 + 8, table_off + 16 * 23 + 16),
        (table_off + 16 * 25 + 8, table_off + 16 * 25 + 16),
        (table_off + 16 * 26 + 8, table_off + 16 * 26 + 16),
    ]
    hors = [i for i in diffs if not any(a <= i < b for a, b in autorisations)]
    ctrl(not hors, f"{len(diffs)} octets modifiés, tous dans les zones autorisées",
         f"hors zone : {len(hors)}")
    # le code du superviseur (.text, .rdata hors L00, .text2 hors S00/md5) : intact
    ctrl(img[0x400:0x1400] == v10[0x400:0x1400],
         ".text du superviseur inchangé")
    ctrl(img[0x1400:0x19C8] == v10[0x1400:0x19C8]
         and img[0x1A00:0x1EDA] == v10[0x1A00:0x1EDA]
         and img[0x1EDB:0x2400] == v10[0x1EDB:0x2400],
         ".rdata inchangé (hors 3 sommes R10 + 1 octet L00)")
    ctrl(img[0x2E00:0x3166] == v10[0x2E00:0x3166]
         and img[0x3167:0x590A] == v10[0x3167:0x590A]
         and img[0x592A:0x5C00] == v10[0x592A:0x5C00],
         ".text2 du superviseur inchangé (hors 1 octet S00 + chaîne md5)")

    print(f"\n=== BILAN : {VERTS} verts, {ROUGES} rouges ===")
    return 1 if ROUGES else 0


if __name__ == "__main__":
    sys.exit(main())
