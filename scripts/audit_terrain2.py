#!/usr/bin/env python3
"""audit_terrain2.py — Audit chirurgical de superviseur.exe 0.5.0-terrain.2 (D49).

Le kit embarqué : « 1 seul exe qui contient tout ». Cet audit prouve :
  A. R5  — notation == artefact, bloc par bloc (23 blocs) ;
  A2. R7 — les 11 blocs hérités sont octet-identiques aux artefacts scellés ;
  B. KIT — les octets .blob embarqués SONT demo.exe 0.3.0 et proxy.exe
           0.4.0-dev.1 (comparaison directe aux fichiers scellés) ;
  C. DIFF — le diff terrain.1 -> terrain.2 est chirurgical : 21 blocs
           identiques, sup-09 révisé R2, sup-37 nouveau, .rdata limité à
           L00/table R10/version, extensions .text2 bornées ;
  D. VAR — public/livraison : écart confiné à l'emplacement annexe ;
  E. R10 — 28 entrées, zone blob couverte, emplacement annexe EXCLU ;
  F. VER — u64 0x00050102, chaînes terrain.2 ;
  G. RSC — VERSIONINFO + manifeste asInvoker présents et lisibles ;
  H. IAT — imports inchangés (aucune nouvelle dépendance OS pour le kit).

Usage : python3 scripts/audit_terrain2.py   (depuis triade/)
"""

from __future__ import annotations

import hashlib
import os
import struct
import subprocess
import sys

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ICI, "terrain"))

import importlib.util as ilu
_spec = ilu.spec_from_file_location("layout_terrain", os.path.join(ICI, "terrain", "layout.py"))
L = ilu.module_from_spec(_spec)
_spec.loader.exec_module(L)

import pefile

TERRAIN = os.path.join(ICI, "terrain")
PUBLIC = os.path.join(TERRAIN, "superviseur.exe")
LIVRAISON = os.path.join(TERRAIN, "livraison", "superviseur.exe")
TERRAIN1 = b""   # git show HEAD:terrain/superviseur.exe (0.5.0-terrain.1)


def _liste_trois(blocs):
    """Normalise la sortie assembler_tout() en (bid, spec, rva, slot)."""
    return [(bid, sid, rva, slot) for bid, sid, _f, rva, slot in blocs]


def _git_terrain1() -> bytes:
    retour = subprocess.run(["git", "-C", ICI, "show", "HEAD:terrain/superviseur.exe"],
                            capture_output=True, check=True)
    return retour.stdout


def _bloc(exe: bytes, rva: int, taille: int) -> bytes:
    """Tranche d'un bloc par RVA — offsets fichier du plan terrain.2."""
    if rva >= L.TEXT2_RVA:
        return exe[L.TEXT2_FILE + (rva - L.TEXT2_RVA):][:taille]
    return exe[L.TEXT_FILE + (rva - L.TEXT_RVA):][:taille]


def _bloc_artefact(buf: bytes, rva: int, taille: int) -> bytes:
    """Tranche dans un artefact scellé (convention fichier M2/démo)."""
    LD = None
    for nom, mod in sys.modules.items():
        if nom == "layout_demo":
            LD = mod
    if LD is None:
        _s = ilu.spec_from_file_location("layout_demo", os.path.join(ICI, "demo", "layout.py"))
        LD = ilu.module_from_spec(_s)
        _s.loader.exec_module(LD)
    if rva >= L.TEXT2_RVA:
        return buf[LD.TEXT2_FILE + (rva - L.TEXT2_RVA):][:taille]
    return buf[LD.TEXT_FILE + (rva - L.TEXT_RVA):][:taille]


def _lire(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def main() -> int:
    global TERRAIN1
    public = _lire(PUBLIC)
    livraison = _lire(LIVRAISON)
    TERRAIN1 = _git_terrain1()
    rapports, echecs = [], []

    def verif(nom: str, condition: bool, detail: str = ""):
        (rapports if condition else echecs).append(
            f"{'PASS' if condition else 'FAIL'}  {nom}" + (f" — {detail}" if detail else ""))

    # --- A. R5 : notation == artefact (ré-assemblage complet, chaîne éprouvée) -----
    sys.path.insert(0, TERRAIN)
    _sb = ilu.spec_from_file_location("bt_audit", os.path.join(TERRAIN, "build_terrain.py"))
    bt = ilu.module_from_spec(_sb)
    _sb.loader.exec_module(bt)
    blocs, _specs, code, _verrous = bt.assembler_tout()
    for bid, _, rva, slot in _liste_trois(blocs):
        verif(f"A/R5 {bid}", _bloc(public, rva, slot) == code[bid]["slot"])

    # --- A2. R7 : héritage octet-identique -------------------------------------------
    heritage = {"a10002", "a10003", "b20001", "b20002", "b20003", "b20004",
                "c30006", "d40003", "d40004", "d40005", "d40006"}
    artefacts = {"a1000": _lire(os.path.join(ICI, "m0", "hello.exe")),
                 "b2000": _lire(os.path.join(ICI, "m1", "selftest.exe")),
                 "c3000": _lire(os.path.join(ICI, "m2", "echo.exe")),
                 "d4000": _lire(os.path.join(ICI, "demo", "demo.exe"))}
    for bid, _, rva, slot, _, _ in L.BLOCS_TERRAIN:
        if bid in heritage:
            source = artefacts[bid[:4] + "0"]
            verif(f"A2/R7 {bid}", _bloc_artefact(source, rva, slot) == _bloc(public, rva, slot))

    # --- B. KIT : les octets embarqués sont les artefacts scellés --------------------
    demo = _lire(os.path.join(ICI, "demo", "demo.exe"))
    proxy = _lire(os.path.join(ICI, "m3", "proxy.exe"))
    off_demo = L.BLOB_FILE + 0x10
    off_proxy = off_demo + L.LONGUEUR_DEMO
    verif("B/KIT demo.exe embarqué == scellé M2",
          public[off_demo:off_demo + L.LONGUEUR_DEMO] == demo,
          f"md5 {hashlib.md5(demo).hexdigest()}")
    verif("B/KIT proxy.exe embarqué == scellé M3",
          public[off_proxy:off_proxy + L.LONGUEUR_PROXY] == proxy,
          f"md5 {hashlib.md5(proxy).hexdigest()}")
    verif("B/KIT longueurs en-tête", struct.unpack_from("<QQ", public, L.BLOB_FILE)
          == (L.LONGUEUR_DEMO, L.LONGUEUR_PROXY))
    verif("B/KIT slot public vide", struct.unpack_from("<Q", public,
          L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA))[0] == 0)
    verif("B/KIT slot livraison = 248", struct.unpack_from("<Q", livraison,
          L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA))[0] == L.LONGUEUR_ANNEXE)

    # --- C. DIFF chirurgical terrain.1 -> terrain.2 -----------------------------------
    blocs_inchanges, blocs_revise = [], []
    for bid, _, rva, slot, _, _ in L.BLOCS_TERRAIN:
        if bid == "f60037":
            continue                     # nouveau bloc — pas dans terrain.1
        ancien = _bloc_artefact(TERRAIN1, rva, slot)
        nouveau = _bloc(public, rva, slot)
        (blocs_inchanges if ancien == nouveau else blocs_revise).append(bid)
    verif("C/DIFF blocs intacts", set(blocs_inchanges) ==
          {b for b, *_ in L.BLOCS_TERRAIN if b not in ("f60009", "f60037")},
          f"{len(blocs_inchanges)} blocs — seuls sup-09 (R2) et sup-37 (nouveau) bougent, "
          f"obtenu : révisés={blocs_revise}")
    # .rdata : le diff doit se limiter à L00 (chaîne version), table R10, u64 version
    ld = None
    _s = ilu.spec_from_file_location("layout_demo", os.path.join(ICI, "demo", "layout.py"))
    ld = ilu.module_from_spec(_s)
    _s.loader.exec_module(ld)
    rdata_1 = TERRAIN1[ld.RDATA_FILE:ld.RDATA_FILE + ld.RDATA_VSIZE]
    rdata_2 = public[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]
    ecarts_rdata = [rva for rva in range(L.RDATA_VSIZE) if rdata_1[rva] != rdata_2[rva]]
    bornes = [(L.CHAINES_ASCII["L00"][0] - L.RDATA_RVA,
               L.CHAINES_ASCII["L00"][0] - L.RDATA_RVA + 49),
              (L.R_TAB_SUM - L.RDATA_RVA, 0x2630 - L.RDATA_RVA)]
    hors = [r for r in ecarts_rdata if not any(a <= r < b for a, b in bornes)]
    verif("C/DIFF .rdata borné (L00 version + table R10)", not hors,
          f"{len(ecarts_rdata)} octets divergents, {len(hors)} hors bornes {bornes}")

    # --- D. VAR : écart public/livraison confiné au slot ------------------------------
    off_slot = L.BLOB_FILE + (L.SLOT_JETONS - L.BLOB_RVA)
    ecarts = [i for i, (a, b) in enumerate(zip(public, livraison)) if a != b]
    verif("D/VAR écart confiné au slot annexe",
          bool(ecarts) and min(ecarts) >= off_slot and max(ecarts) < off_slot + L.TAILLE_SLOT_JETONS,
          f"{len(ecarts)} octets dans [{off_slot:#x}, {off_slot + L.TAILLE_SLOT_JETONS:#x})")
    verif("D/VAR md5 distincts", hashlib.md5(public).hexdigest()
          != hashlib.md5(livraison).hexdigest())

    # --- E. R10 : 28 entrées, blob couvert, slot exclu --------------------------------
    table = []
    rva_table = L.R_TAB_SUM
    while True:
        r, t, _s = struct.unpack_from("<IIQ", public, L.RDATA_FILE + (rva_table - L.RDATA_RVA))
        if r == 0 and t == 0:
            break
        table.append((r, t))
        rva_table += 16
    verif("E/R10 27 entrées + terminateur", len(table) == 27, f"{len(table)} entrées")
    rvas = [r for r, _ in table]
    verif("E/R10 zone blob couverte", (L.BLOB_LONGUEURS, L.SLOT_JETONS - L.BLOB_LONGUEURS) in table)
    verif("E/R10 slot annexe EXCLU", not any(r <= L.SLOT_JETONS < r + t for r, t in table))
    verif("E/R10 zone sup 3 couverte",
          any(r == L.ZONE_DATA_SUP_3[0] for r, _ in table))

    # --- F. VER : version et chaînes --------------------------------------------------
    verif("F/VER u64 0x00050102", struct.unpack_from("<Q", public,
          L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA))[0] == 0x00050102)
    verif("F/VER S00 terrain.2", b"0.5.0-terrain.2" in
          _bloc(public, L.CHAINES_SUP["S00"][0], 48))
    verif("F/VER L00 terrain.2", b"terrain 0.5.0-terrain.2" in
          _bloc(public, L.CHAINES_ASCII["L00"][0], 56))

    # --- G. RSC : VERSIONINFO + manifeste ----------------------------------------------
    pe = pefile.PE(data=public)
    fic = None
    manifeste_ok = False
    for e1 in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        if e1.id == 24:
            for e2 in e1.directory.entries:
                for e3 in e2.directory.entries:
                    brut = pe.get_data(e3.data.struct.OffsetToData, e3.data.struct.Size)
                    manifeste_ok = b"asInvoker" in brut and b"TRIADE" in brut
    for bloc_info in pe.FileInfo:
        for d in bloc_info:
            if getattr(d, "Key", b"") == b"StringFileInfo":
                for table_s in d.StringTable:
                    for k, v in table_s.entries.items():
                        if k == b"FileVersion":
                            fic = v.decode()
    verif("G/RSC FileVersion 0.5.0.2", fic == "0.5.0.2", f"obtenu {fic!r}")
    verif("G/RSC manifeste asInvoker", manifeste_ok)

    # --- H. IAT : imports inchangés -----------------------------------------------------
    comptage = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entree.dll.decode().lower()
        comptage[dll] = comptage.get(dll, 0) + len(entree.imports)
    verif("H/IAT inchangée", comptage == {"kernel32.dll": 24, "user32.dll": 17, "gdi32.dll": 1},
          str(comptage))

    # --- rapport ------------------------------------------------------------------------
    print("\n".join(rapports))
    if echecs:
        print("\n".join(echecs))
        print(f"\nAUDIT TERRAIN.2 : {len(echecs)} ÉCHEC(S) — fail-closed")
        return 1
    print(f"\nAUDIT TERRAIN.2 : TOUT CONFORME — {len(rapports)} contrôles PASS")
    print(f"  superviseur.exe publique    : {len(public)} o, md5 {hashlib.md5(public).hexdigest()}, "
          f"sha256 {hashlib.sha256(public).hexdigest()[:16]}…")
    print(f"  superviseur.exe livraison  : md5 {hashlib.md5(livraison).hexdigest()}, "
          f"sha256 {hashlib.sha256(livraison).hexdigest()[:16]}…")
    print(f"  kit embarqué : demo.exe {L.LONGUEUR_DEMO} o + proxy.exe {L.LONGUEUR_PROXY} o "
          f"+ annexe {L.LONGUEUR_ANNEXE} o (variante livraison)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
