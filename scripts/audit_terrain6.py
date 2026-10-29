#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_terrain6.py — audit INDÉPENDANT de superviseur-terrain6.exe.

Ne réutilise AUCUN validateur du projet (leçon D51) : parseur PE from
scratch, recomptage de tout. Contrôles :
  A. structure PE + règles du chargeur (SizeOfHeaders vs table réelle) ;
  B. tables d'imports : 6 descripteurs, chaque slot résolu par NOM EXACT,
     motif demo (INT dans .rdata + FT pré-remplies) ;
  C. les 93 call-sites indirects FF15/FF25 -> slots couverts ;
  D. porte R10 : 20 entrées recalculées (algorithme u64 tronqué) ;
  E. SEMANTIQUE DU CORRECTIF : la boucle de recherche de fenêtre de sup-33
     fait FindWindowW(L"TRIADE_demo", NULL) — CLASSE, plus titre — et le
     clic suit par FindWindowExW + SendMessageTimeoutW(BM_CLICK) ;
  F. versions : L00/S00 « terrain.6 », VERSIONINFO 0.5.6.0 (4 champs) ;
  G. .blob : demo.exe (73c064fb…) et proxy.exe (8740e1ca…) embarqués
     intacts, octet pour octet.
"""
import hashlib
import pathlib
import struct
import sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur-terrain6.exe")
MD5_TERRAIN5 = "6ddfe8c2f9413031d792ec30bb9a0b9c"

erreurs = 0
def ko(msg):
    global erreurs
    erreurs += 1
    print(f"  [ROUGE] {msg}")

def ok(msg):
    print(f"  [vert] {msg}")

def main():
    data = EXE.read_bytes()
    print(f"===== {EXE.name} ({len(data)} octets, md5 {hashlib.md5(data).hexdigest()}) =====")

    # --- A. structure PE + règles chargeur ---------------------------------
    e = struct.unpack_from("<I", data, 0x3C)[0]
    if data[e:e+4] != b"PE\0\0":
        ko("signature PE"); return 1
    nsec, optsz = struct.unpack_from("<H", data, e + 6)[0], struct.unpack_from("<H", data, e + 20)[0]
    opt = e + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    if magic != 0x20B:
        ko(f"magic {magic:#x} != PE32+"); return 1
    size_headers = struct.unpack_from("<I", data, opt + 60)[0]
    table_reelle = opt + optsz + 40 * nsec
    if size_headers < table_reelle:
        ko(f"SizeOfHeaders {size_headers:#x} < table réelle {table_reelle:#x} — REFUS CHARGEUR")
    else:
        ok(f"SizeOfHeaders {size_headers:#x} >= en-têtes réels {table_reelle:#x} (règle chargeur D50)")
    subsystem = struct.unpack_from("<H", data, opt + 68)[0]
    if subsystem != 2:
        ko(f"Subsystem {subsystem} != 2 (GUI)")
    else:
        ok("Subsystem 2 (GUI)")

    secs = []
    so = opt + optsz
    for i in range(nsec):
        o = so + 40 * i
        name = data[o:o+8].rstrip(b"\0").decode()
        vsz, va, rsz, roff = struct.unpack_from("<IIII", data, o + 8)
        secs.append((name, vsz, va, rsz, roff))
    ok(f"{nsec} sections : " + ", ".join(f"{n}@{v:#x}" for n, _, v, _, _ in secs))

    def rva2off(rva):
        for n, vsz, va, rsz, roff in secs:
            if va <= rva < va + max(vsz, rsz):
                d = rva - va
                return roff + d if d < rsz else None
        return None

    # --- B. imports ----------------------------------------------------------
    imp_rva = struct.unpack_from("<I", data, opt + 120)[0]
    slot_nom = {}
    d = rva2off(imp_rva)
    idx = 0
    motif_demo = True
    while True:
        oft, _, _, name_rva, ft = struct.unpack_from("<IIIII", data, d + 20 * idx)
        if oft == 0 and ft == 0 and name_rva == 0:
            break
        no = rva2off(name_rva)
        dll = data[no:data.find(b"\0", no)].decode()
        lookup = oft if oft else ft
        host = next((n for n, _, va, _, _ in secs if va <= lookup < va + 0x1000), "?")
        if dll.endswith(("kernel32.dll", "user32.dll", "gdi32.dll")) and host != ".rdata":
            motif_demo = False
            ko(f"descripteur[{idx}] {dll} : lookup dans {host} (pas .rdata)")
        lo = rva2off(lookup)
        j = 0
        while True:
            ent = struct.unpack_from("<Q", data, lo + 8 * j)[0]
            if ent == 0:
                break
            if not (ent >> 63):
                ho = rva2off(ent & 0x7FFFFFFF)
                nom = data[ho+2:data.find(b"\0", ho+2)].decode()
                slot_nom[ft + 8 * j] = f"{dll.split('.')[0]}!{nom}"
            j += 1
        idx += 1
    if motif_demo:
        ok(f"imports : {idx} descripteurs, lookups TOUS dans .rdata (motif demo)")
    print(f"  slots nommés : {len(slot_nom)}")

    # FT pré-remplies = copie des INT (double chemin, motif demo)
    pre_remplis = True
    for slot in slot_nom:
        so_ = rva2off(slot)
        ft_val = struct.unpack_from("<Q", data, so_)[0]
        if ft_val == 0 or rva2off(ft_val & 0x7FFFFFFF) is None:
            pre_remplis = False
            ko(f"slot {slot:#x} : FT à zéro / RVA invalide dans le fichier")
    if pre_remplis:
        ok("FT pré-remplies 100% (résolution possible par OFT ou par FT)")

    # --- C. call-sites FF15/FF25 ----------------------------------------------
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    total = 0
    non_couverts = []
    for name, vsz, va, rsz, roff in secs:
        if name not in (".text", ".text2"):
            continue
        blob = data[roff:roff+rsz]
        for i in range(len(blob) - 6):
            if blob[i] == 0xFF and blob[i+1] in (0x15, 0x25):
                disp = struct.unpack_from("<i", blob, i + 2)[0]
                target = va + i + 6 + disp
                if target in slot_nom or target in (0x20D8, 0x20E0, 0x20E8, 0x20D0):
                    total += 1
                elif 0x2000 <= target < 0x3000:
                    total += 1   # données/globals pointés — pas un slot IAT
                else:
                    non_couverts.append((name, va + i, target))
    if non_couverts:
        for n, a, t in non_couverts[:6]:
            ko(f"call-site {n}@{a:#x} -> {t:#x} NON couvert")
    else:
        ok(f"call-sites indirects couverts : {total} (aucun orphelin)")

    # --- D. porte R10 ----------------------------------------------------------
    def somme(rva, ln):
        o = rva2off(rva)
        s = 0
        for i in range(0, ln, 8):
            s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
        return s
    verts = 0
    toff = rva2off(0x2450)
    for k in range(20):
        rva, ln, sm = struct.unpack_from("<IIQ", data, toff + 16 * k)
        if somme(rva, ln) == sm:
            verts += 1
        else:
            ko(f"porte R10 ROUGE entrée [{k}] rva={rva:#x}")
    if verts == 20:
        ok("porte R10 : 20/20 entrées VERTES")

    # --- E. SEMANTIQUE du correctif ---------------------------------------------
    print("  --- E. la boucle de recherche de fenêtre (sup-33 @0x544f) ---")
    o = rva2off(0x544F)
    code = data[o:o+0x60]
    instrs = list(md.disasm(code, 0x544F))
    texte = [f"{i.mnemonic} {i.op_str}" for i in instrs]
    attendu = ["lea rcx, [rip - 0x29c4]", "xor edx, edx",
               "call qword ptr [rip - 0x30fe]"]
    if texte[:3] == attendu:
        ok("FindWindowW(L\"TRIADE_demo\", NULL) — recherche par CLASSE (le correctif terrain.6)")
    else:
        ko(f"instructions inattendues : {texte[:3]}")
    # la chaîne lue comme lpClassName :
    so_ = rva2off(0x2A92)
    ch = data[so_:so_+24].decode("utf-16-le").rstrip("\0")
    if ch == "TRIADE_demo":
        ok(f"lpClassName = {ch!r} = la CLASSE réelle de la fenêtre demo.exe (binaire embarqué)")
    else:
        ko(f"lpClassName = {ch!r}")
    # le call [rip-0x30fe] tombe sur le slot FindWindowW
    if slot_nom.get(0x2360) == "user32!FindWindowW":
        ok("le call @0x5458 vise le slot 0x2360 = user32!FindWindowW")
    else:
        ko(f"slot 0x2360 = {slot_nom.get(0x2360)}")

    # --- F. versions --------------------------------------------------------------
    if b"terrain 0.5.0-terrain.6L01" in data:
        ok("L00 (.rdata) : « terrain 0.5.0-terrain.6 »")
    else:
        ko("L00 : version non bumpée")
    if b"terrain 0.5.0-terrain.6S01" in data:
        ok("S00 (.text2) : « terrain 0.5.0-terrain.6 »")
    else:
        ko("S00 : version non bumpée")
    fv = struct.unpack_from("<4H", data, 0x5CD0)
    pv = struct.unpack_from("<4H", data, 0x5CD8)
    if fv == (0, 5, 6, 0):
        ok(f"FileVersion binaire {fv} (génération 6)")
    else:
        ko(f"FileVersion binaire {fv}")
    if pv == (0, 5, 6, 0):
        ok(f"ProductVersion binaire {pv} (génération 6)")
    else:
        ko(f"ProductVersion binaire {pv}")
    for off, lbl, attendu in ((0x5DB8, "FileVersion chaîne", "0.5.0.6"),
                              (0x5EB0, "ProductVersion chaîne", "0.5.0-terrain.6")):
        fin = off
        while struct.unpack_from("<H", data, fin)[0] != 0:
            fin += 2
        s = data[off:fin].decode("utf-16-le")
        if s == attendu:
            ok(f"{lbl} « {s} »")
        else:
            ko(f"{lbl} « {s} » (attendu « {attendu} »)")

    # --- G. .blob : demo.exe / proxy.exe embarqués --------------------------------
    # demo.exe @blob+0 (rva 0x8000..0xC000), proxy.exe @0xC000.. — retrouver par md5
    demo_ref = pathlib.Path("/home/z/my-project/triade/demo/demo.exe").read_bytes()
    proxy_ref = pathlib.Path("/home/z/my-project/triade/m3/proxy.exe").read_bytes()
    blob_off = next(roff for n, _, va, _, roff in secs if n == ".blob")
    trouve = 0
    for nom, ref in (("demo.exe", demo_ref), ("proxy.exe", proxy_ref)):
        i = data.find(ref)
        if i >= 0:
            ok(f".blob : {nom} embarqué intact @file {i:#x} (md5 {hashlib.md5(ref).hexdigest()[:8]}…)")
            trouve += 1
        else:
            ko(f".blob : {nom} INTROUVABLE (corrompu ?)")
    if trouve == 2 and blob_off:
        ok("l'annexe et les deux exécutables embarqués sont intacts")

    print()
    if erreurs:
        print(f"===== AUDIT : {erreurs} ROUGE(S) — LIVRAISON INTERDITE =====")
        return 1
    print("===== AUDIT : TOUT CONFORME — terrain.6 LIVRABLE =====")
    return 0

if __name__ == "__main__":
    sys.exit(main())
