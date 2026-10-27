#!/usr/bin/env python3
"""audit_terrain2.py — Audit chirurgical de superviseur.exe 0.5.0-terrain.3 (D50).

Corrigé du 27/10 soir : terrain.2 ne lançait RIEN au double-clic — le champ
PE SizeOfHeaders valait 0x200 (L.FILE_ALIGN, coïncidence juste pour quatre
sections ou moins) alors que six sections d'en-têtes réels mesurent 0x238 :
le chargeur Windows refusait l'image. terrain.3 écrit 0x400 (règle chargeur,
D50) et re-scelle la lignée. Cet audit prouve que la correction est CHIRURGICALE :
  A. R5  — notation == artefact, bloc par bloc (23 blocs) ;
  A2. R7 — les 11 blocs hérités sont octet-identiques aux artefacts scellés ;
  B. KIT — les octets .blob embarqués SONT demo.exe 0.3.0 et proxy.exe
           0.4.0-dev.1 (comparaison directe aux fichiers scellés) ;
  C. D50 — RÈGLE CHARGEUR : SizeOfHeaders couvre la table des sections,
           aligné FILE_ALIGN, première section brute après les en-têtes ;
  C2. DIFF — le diff terrain.2 -> terrain.3 est chirurgical : 23 blocs
           identiques, .rdata limité à L00/table R10/version, .text2 limité
           à S00, en-tête limité au champ SizeOfHeaders lui-même ;
  D. VAR — public/livraison : écart confiné à l'emplacement annexe ;
  E. R10 — 28 entrées, zone blob couverte, emplacement annexe EXCLU ;
  F. VER — u64 0x00050103, chaînes terrain.3 ;
  G. RSC — VERSIONINFO 0.5.0.3 + manifeste asInvoker présents et lisibles ;
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
PRECEDENT = b""   # git show HEAD:terrain/superviseur.exe (terrain.2 tant que
                  # terrain.3 n'est pas commité ; terrain.3 ensuite — les
                  # contrôles de diff restent vrais dans les deux cas)


def _liste_trois(blocs):
    """Normalise la sortie assembler_tout() en (bid, spec, rva, slot)."""
    return [(bid, sid, rva, slot) for bid, sid, _f, rva, slot in blocs]


def _git_precedent() -> bytes:
    """terrain.2 scellé : HEAD tant que terrain.3 n'est pas commité, puis le
    commit D49 (7c6b082, dernier état terrain.2 de l'historique)."""
    retour = subprocess.run(["git", "-C", ICI, "show", "HEAD:terrain/superviseur.exe"],
                            capture_output=True, check=True)
    d = retour.stdout
    soh = struct.unpack_from("<I", d, struct.unpack_from("<I", d, 0x3C)[0] + 4 + 20 + 60)[0]
    if soh == L.SIZE_HEADERS:          # HEAD est déjà terrain.3 — remonter au D49
        retour = subprocess.run(
            ["git", "-C", ICI, "show", "7c6b082:terrain/superviseur.exe"],
            capture_output=True, check=True)
        return retour.stdout
    return d


def _bloc(exe: bytes, rva: int, taille: int) -> bytes:
    """Tranche d'un bloc par RVA — offsets fichier du plan terrain.2+."""
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
    global PRECEDENT
    public = _lire(PUBLIC)
    livraison = _lire(LIVRAISON)
    PRECEDENT = _git_precedent()
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

    # --- C. D50 : RÈGLE DU CHARGEUR RÉEL ----------------------------------------------
    # C'est le défaut qui tuait terrain.2 : SizeOfHeaders doit couvrir TOUTE
    # la table des sections (DOS 64 + PE 24 + opt 240 + 6×40 = 0x238 réels)
    # et être aligné sur FILE_ALIGN — 0x238 -> 0x400.
    e_lfanew = struct.unpack_from("<I", public, 0x3C)[0]
    nb_sec, = struct.unpack_from("<H", public, e_lfanew + 6)
    taille_opt, = struct.unpack_from("<H", public, e_lfanew + 20)
    fin_reelle = e_lfanew + 4 + 20 + taille_opt + nb_sec * 40
    opt = e_lfanew + 4 + 20
    soh, = struct.unpack_from("<I", public, opt + 60)
    fal, = struct.unpack_from("<I", public, opt + 36)
    verif("C/D50 SizeOfHeaders couvre la table des sections",
          soh >= fin_reelle, f"réels {fin_reelle:#x} <= déclaré {soh:#x}")
    verif("C/D50 SizeOfHeaders aligné FILE_ALIGN", soh % fal == 0,
          f"{soh:#x} % {fal:#x} == 0")
    verif("C/D50 SizeOfHeaders == plan", soh == L.SIZE_HEADERS,
          f"{soh:#x} == {L.SIZE_HEADERS:#x}")
    prem_brute = struct.unpack_from("<I", public, e_lfanew + 4 + 20 + taille_opt + 20)[0]
    verif("C/D50 première section brute après les en-têtes", prem_brute >= soh,
          f".text à {prem_brute:#x} >= en-têtes {soh:#x}")
    verif("C/D50 terrain.2 reproductible en échec",
          (struct.unpack_from("<I", PRECEDENT, opt + 60)[0] == 0x200
           and struct.unpack_from("<H", PRECEDENT, e_lfanew + 6)[0] == 6),
          "le scellé terrain.2 (commit D49) portait le défaut : 0x200 déclarés, "
          "6 sections, table 0x238 — le chargeur refusait l'image")

    # --- C2. DIFF chirurgical terrain.2 -> terrain.3 ----------------------------------
    blocs_inchanges, blocs_revise = [], []
    for bid, _, rva, slot, _, _ in L.BLOCS_TERRAIN:
        ancien = _bloc(PRECEDENT, rva, slot)      # terrain.2 : mêmes offsets fichier
        nouveau = _bloc(public, rva, slot)
        (blocs_inchanges if ancien == nouveau else blocs_revise).append(bid)
    verif("C2/DIFF 23 blocs intacts", not blocs_revise and len(blocs_inchanges) == 23,
          f"révisés={blocs_revise or 'aucun'} — la correction ne touche AUCUN code")
    # .rdata : le diff doit se limiter à L00 (version), table R10, u64 version
    rdata_p = PRECEDENT[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]
    rdata_n = public[L.RDATA_FILE:L.RDATA_FILE + L.RDATA_VSIZE]
    ecarts_rdata = [rva for rva in range(L.RDATA_VSIZE) if rdata_p[rva] != rdata_n[rva]]
    bornes = [(L.CHAINES_ASCII["L00"][0] - L.RDATA_RVA,
               L.CHAINES_ASCII["L00"][0] - L.RDATA_RVA + 49),
              (L.R_TAB_SUM - L.RDATA_RVA, 0x2630 - L.RDATA_RVA)]
    hors = [r for r in ecarts_rdata if not any(a <= r < b for a, b in bornes)]
    verif("C2/DIFF .rdata borné (L00 version + table R10 + u64)", not hors,
          f"{len(ecarts_rdata)} octets divergents, {len(hors)} hors bornes")
    # .text2 : le diff doit se limiter à S00 (version de l'en-tête de scénario)
    text2_p = PRECEDENT[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE]
    text2_n = public[L.TEXT2_FILE:L.TEXT2_FILE + L.TEXT2_VSIZE]
    ecarts_t2 = [rva for rva in range(L.TEXT2_VSIZE) if text2_p[rva] != text2_n[rva]]
    b_s00 = (L.CHAINES_SUP["S00"][0] - L.TEXT2_RVA,
             L.CHAINES_SUP["S00"][0] - L.TEXT2_RVA + L.LONGUEURS_ASCII["S00"])
    hors_t2 = [r for r in ecarts_t2 if not (b_s00[0] <= r < b_s00[1])]
    verif("C2/DIFF .text2 borné (S00 version)", not hors_t2,
          f"{len(ecarts_t2)} octets divergents, {len(hors_t2)} hors S00")
    # page d'en-têtes : le diff doit se limiser AU champ SizeOfHeaders (4 o)
    ecarts_hdr = [o for o in range(min(L.SIZE_HEADERS, len(PRECEDENT)))
                  if public[o] != PRECEDENT[o]]
    borne_soh = (opt + 60, opt + 64)
    hors_hdr = [o for o in ecarts_hdr if not (borne_soh[0] <= o < borne_soh[1])]
    verif("C2/DIFF en-têtes bornés au champ SizeOfHeaders", not hors_hdr,
          f"{len(ecarts_hdr)} octets divergents, {len(hors_hdr)} hors "
          f"[{borne_soh[0]:#x}, {borne_soh[1]:#x})")

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
    verif("E/R10 aucune zone ne couvre les IAT (mutées par le chargeur)",
          not any(r <= iat < r + t for r, t in table for iat in
                  (L.R_IAT, L.R_IAT_USER32, L.R_IAT_GDI32, L.R_IAT_K32B,
                   L.R_IAT_K32C, L.R_IAT_U32B)))

    # --- F. VER : version et chaînes --------------------------------------------------
    verif("F/VER u64 0x00050103", struct.unpack_from("<Q", public,
          L.RDATA_FILE + (L.R_VERSION - L.RDATA_RVA))[0] == 0x00050103)
    verif("F/VER S00 terrain.3", b"0.5.0-terrain.3" in
          _bloc(public, L.CHAINES_SUP["S00"][0], 48))
    verif("F/VER L00 terrain.3", b"terrain 0.5.0-terrain.3" in
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
                    manifeste_ok = (b"asInvoker" in brut and b"TRIADE" in brut
                                    and b'0.5.0.3' in brut)
    for bloc_info in pe.FileInfo:
        for d in bloc_info:
            if getattr(d, "Key", b"") == b"StringFileInfo":
                for table_s in d.StringTable:
                    for k, v in table_s.entries.items():
                        if k == b"FileVersion":
                            fic = v.decode()
    verif("G/RSC FileVersion 0.5.0.3", fic == "0.5.0.3", f"obtenu {fic!r}")
    verif("G/RSC manifeste asInvoker 0.5.0.3", manifeste_ok)

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
        print(f"\nAUDIT TERRAIN.3 : {len(echecs)} ÉCHEC(S) — fail-closed")
        return 1
    print(f"\nAUDIT TERRAIN.3 : TOUT CONFORME — {len(rapports)} contrôles PASS")
    print(f"  superviseur.exe publique    : {len(public)} o, md5 {hashlib.md5(public).hexdigest()}, "
          f"sha256 {hashlib.sha256(public).hexdigest()[:16]}…")
    print(f"  superviseur.exe livraison  : md5 {hashlib.md5(livraison).hexdigest()}, "
          f"sha256 {hashlib.sha256(livraison).hexdigest()[:16]}…")
    print(f"  kit embarqué : demo.exe {L.LONGUEUR_DEMO} o + proxy.exe {L.LONGUEUR_PROXY} o "
          f"+ annexe {L.LONGUEUR_ANNEXE} o (variante livraison)")
    print("  règle chargeur D50 : SizeOfHeaders "
          f"{struct.unpack_from('<I', public, opt + 60)[0]:#x} >= table {fin_reelle:#x} — "
          "terrain.2 (0x200) ne lançait rien, terrain.3 lance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
