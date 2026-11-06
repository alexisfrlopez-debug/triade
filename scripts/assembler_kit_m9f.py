#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_m9f.py — LE KIT TERRAIN M9-(f) ASSEMBLÉ ET ÉPROUVÉ au labo.

Modèle : scripts/assembler_kit_m8d.py (D153) — le labo NE PEUT PAS
exécuter le scénario (Windows + le VRAI ntdll + le VRAI afd.sys + le
réseau exigés, le cœur même du chantier (f)) ; l'épreuve de labo est :

  1. L'ASSEMBLAGE : m9-kit/ = proxy.exe (l'artefact 1.0.0-dev.2,
     sha256 d8928934… ASSERTÉ) + scenario-m9f.py + LISEZMOI-KIT-M9F.md ;
  2. LE RECOUP DES CONSTANTES PAR AST : chaque constante du scénario
     (les adresses scellées, le trombone, l'OCTET DE L'ERRATUM n° 5,
     les fixtures transport, le motif du stub, l'empreinte épinglée,
     les dimensions de session) relue DANS L'ARTEFACT ou DANS LE PLAN —
     la source unique est le dépôt, jamais une constante gravée de tête ;
  3. LA COMPILATION : py_compile du scénario (aucune erreur de syntaxe) ;
  4. L'ÉPREUVE D'EXTRACTION VIERGE : le zip extrait dans un répertoire
     temporaire NEUF, les empreintes re-constatées, la structure exacte ;
  5. LE ZIP : kit-m9f.zip (l'archive déposée au coffre /test).

Usage : python3 scripts/assembler_kit_m9f.py
Code de sortie : 0 = kit assemblé et éprouvé ; 2 = refus nommé."""

import ast
import hashlib
import os
import pathlib
import py_compile
import random
import shutil
import sys
import tempfile
import zipfile

REPO = pathlib.Path("/home/z/my-project/triade")
KIT = "m9-kit"
SORTIE = pathlib.Path("/home/z/my-project/download")
KIT_ZIP = SORTIE / "kit-m9f.zip"

SHA_PROXY = ("d892893469608fd69e381b92b8e18623107bd2bc694f43a512"
             "bc5900773dc314")
TAILLE_PROXY = 65024
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
LISEZMOI = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md"
PROXY = REPO / "tls13" / "proxy.exe"

# l'empreinte épinglée — figée par la sonde du 06/11 (3 sessions
# consécutives contre la cible, empreinte IDENTIQUE de bout en bout :
# la pièce vit dans scripts/sonde_cible_terrain.py)
EMPREINTE = "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f"


def refus(nom, detail):
    print(f"[assemblage] REFUS {nom} : {detail}")
    sys.exit(2)


def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


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


def _litteral(noeud):
    """Littéral OU bytes.fromhex('…') — les deux formes lisibles du scénario."""
    if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute) \
            and noeud.func.attr == "fromhex" \
            and isinstance(noeud.func.value, ast.Name) \
            and noeud.func.value.id == "bytes" and len(noeud.args) == 1:
        return bytes.fromhex(ast.literal_eval(noeud.args[0]))
    return ast.literal_eval(noeud)


def _extraire_fonction(chemin, nom, namespace=None):
    """Une FunctionDef du fichier, extraite PAR AST et rendue exécutable
    (l'erratum n° 7 porte 3 rejoue l'échelle du scénario CONTRE LES
    VECTEURS OFFICIELS — aucun import du module hôte n'est requis)."""
    arbre = ast.parse(pathlib.Path(chemin).read_text(encoding="utf-8"))
    for noeud in arbre.body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == nom:
            module = ast.Module(body=[noeud], type_ignores=[])
            code = compile(module, filename=str(chemin), mode="exec")
            ns = {} if namespace is None else namespace
            exec(code, ns)
            return ns[nom]
    refus("AST", f"la fonction {nom} est absente de {chemin}")


def constantes_du_scénario(chemin):
    """Extrait les constantes nommées du scénario PAR AST (jamais gravées)."""
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    cibles = {"SHA_PROXY", "TAILLE_PROXY", "R_SYS01", "R_SYS02", "R_SYS04",
              "R_SYS05", "R_SYS06", "R_TLS27", "R_TLS28", "R_SYS_DEVICE",
              "R_SYS_NOM_CREATEFILE", "R_SYS_NOM_DEVICEIOCTL",
              "R_SYS_NOM_CLOSE", "R_TETE_CH", "OCTETS_SYS01",
              "OCTETS_TETE_CH", "NOM_DEVICE", "MOTIF_STUB",
              "EMPREINTE_EPINGLEE", "CIBLE", "CIBLE_PORT",
              "SESSION_TAILLE", "KIT96", "CH_TAILLE", "CH_RECORD",
              "TEMOIN_APPLICATIF"}
    trouves = {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name) and cible.id in cibles:
                    try:
                        trouves[cible.id] = _litteral(noeud.value)
                    except (ValueError, SyntaxError):
                        refus("AST", f"constante {cible.id} non littérale")
    manquantes = cibles - set(trouves)
    if manquantes:
        refus("AST", f"constantes absentes du scénario : {sorted(manquantes)}")
    return trouves


# --- LE CONTRÔLE PERMANENT DE L'ERRATUM n° 7 (les TROIS portes) ------------------
#
# La pièce (la console du développeur, le paste du 07/11 — l'Entrée 181
# RENVERSÉE) : le second run du 06/11 16:56 est mort d'un TypeError PYTHON
# NOMMÉ — scenario-m9f.py:593 `kit96.raw[:32] = alea` — après l'impression
# d'une « clé publique attendue » NULLE (000…0), le symptôme de la seconde
# faute ; la troisième vivait à quatre lignes en aval (r9 = la TAILLE au
# lieu du POINTEUR). Une faute par porte, le REFUS est nommé.

def _porte_e7_1_raw(arbre):
    """Porte 1 — le TypeError NOMMÉ du run : AUCUNE écriture par tranches
    sur `.raw` (une copie bytes IMMUABLE, l'échec est sur TOUTE machine)."""
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Subscript) \
                        and isinstance(cible.value, ast.Attribute) \
                        and cible.value.attr == "raw":
                    return ("ERRATUM-7 porte 1",
                            f"ligne {noeud.lineno} : écriture par tranches "
                            "sur `.raw` — une copie bytes IMMUABLE (le "
                            "TypeError NOMMÉ du second run, ligne 593 : le "
                            "kit doit poser ses tampons EN UN GESTE, "
                            "create_string_buffer)")
    return None


def _porte_e7_2_ouvrir(arbre):
    """Porte 2 — les DEUX sites OUVRIR portent LE POINTEUR des 96 o en r9
    (tls13-27 P2 É1 : « r9 = le pointeur des 96 o »), jamais la taille."""
    sites = []
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "TLS27" and len(noeud.args) >= 4 \
                and isinstance(noeud.args[1], ast.Constant) \
                and noeud.args[1].value == 1:
            r9 = noeud.args[3]
            sites.append(isinstance(r9, ast.Call)
                         and isinstance(r9.func, ast.Attribute)
                         and r9.func.attr == "addressof"
                         and isinstance(r9.func.value, ast.Name)
                         and r9.func.value.id == "ctypes"
                         and r9.args and isinstance(r9.args[0], ast.Name)
                         and r9.args[0].id in ("kit96", "kit96_2"))
    if len(sites) != 2 or not all(sites):
        return ("ERRATUM-7 porte 2",
                f"les sites OUVRIR : {len(sites)} trouvé(s), "
                f"{sites.count(True)} portant ctypes.addressof(kit…) en r9 "
                "— tls13-27 P2 É1 exige LE POINTEUR des 96 o (96 pour "
                "pointeur : la machine lirait à l'adresse 0x60, la mort au "
                "premier geste)")
    return None


def _porte_e7_3_echelle(chemin_scenario):
    """Porte 3 — l'échelle re-jouée CONTRE LES VECTEURS OFFICIELS du dépôt
    (harnais_x25519.py : RFC 7748 § 6.1 Alice/Bob, le couple RFC 8448 § 3,
    la référence ref_x25519 sur 16 clés semées) : la « clé attendue » du
    recoup doit être LA VRAIE — jamais 000…0 (x_3 né à 0 : le point à
    l'infini ; a24 = (p+1)//4 : la fausse courbe)."""
    echelle = _extraire_fonction(chemin_scenario, "x25519_echelle")
    harnais_x = REPO / "tls13" / "harnais_x25519.py"
    arbre_x = ast.parse(harnais_x.read_text(encoding="utf-8"))
    officiels, transfert = {}, {}
    for noeud in arbre_x.body:
        if isinstance(noeud, ast.Assign) and len(noeud.targets) == 1 \
                and isinstance(noeud.targets[0], ast.Name):
            nom = noeud.targets[0].id
            if nom in ("ALICE_PRIV", "ALICE_PUB", "BOB_PRIV", "BOB_PUB"):
                officiels[nom] = bytes.fromhex(ast.literal_eval(noeud.value))
            elif nom == "TRANSFERT_8448":
                transfert = {k: bytes.fromhex(v) for k, v in
                             ast.literal_eval(noeud.value).items()}
    if len(officiels) != 4 or "client_priv" not in transfert:
        return ("ERRATUM-7 porte 3",
                "les VECTEURS OFFICIELS du dépôt (harnais_x25519.py) sont "
                "introuvables — la source unique est cassée")
    if echelle(officiels["ALICE_PRIV"]) != officiels["ALICE_PUB"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle du scénario rate le vecteur OFFICIEL "
                "RFC 7748 § 6.1 Alice — la « clé attendue » du recoup "
                "serait FAUSSE (le second run imprimait 000…0)")
    if echelle(officiels["BOB_PRIV"]) != officiels["BOB_PUB"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle du scénario rate le vecteur OFFICIEL "
                "RFC 7748 § 6.1 Bob")
    if echelle(transfert["client_priv"]) != transfert["client_pub"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle du scénario rate le couple OFFICIEL "
                "RFC 8448 § 3 (le client du transfert)")
    ref = _extraire_fonction(harnais_x, "ref_x25519", {"P": 2 ** 255 - 19})
    u9 = (9).to_bytes(32, "little")
    rng = random.Random(20261107)
    for _ in range(16):
        cle = bytes(rng.randrange(256) for _ in range(32))
        if echelle(cle) != ref(cle, u9):
            return ("ERRATUM-7 porte 3",
                    "l'échelle du scénario diverge de LA RÉFÉRENCE DU "
                    "DÉPÔT (ref_x25519) sur une clé semée — les DEUX "
                    "lecteurs du recoup ne s'accorderaient pas")
    return None


def portes_erratum_7(chemin_scenario):
    """L'ERRATUM n° 7 ne peut plus dormir : TROIS portes, une faute par
    porte, le REFUS est nommé (le contrôle négatif est prouvé sur la
    pointe pré-réparation 35706ef par scripts/preuve_negative_e7.py)."""
    arbre = ast.parse(pathlib.Path(chemin_scenario).read_text(
        encoding="utf-8"))
    for porte in (_porte_e7_1_raw, _porte_e7_2_ouvrir):
        verdict = porte(arbre)
        if verdict:
            refus(*verdict)
    verdict = _porte_e7_3_echelle(chemin_scenario)
    if verdict:
        refus(*verdict)


def main():
    print("=== L'ASSEMBLAGE DU KIT TERRAIN M9-(f) (LA SESSION RÉELLE) ===")

    # -- 1. les pièces du dépôt, vérifiées ------------------------------------
    if sha256_fichier(PROXY) != SHA_PROXY:
        refus("ARTEFACT", f"proxy.exe sha256 {sha256_fichier(PROXY)[:16]}… "
                          f"!= {SHA_PROXY[:16]}…")
    print(f"[1] l'artefact : {TAILLE_PROXY} o, sha256 {SHA_PROXY[:16]}… — "
          f"la carte génération 10 prouve CES octets")

    # -- 2. le recoup des constantes (AST du scénario contre l'artefact) ------
    data = PROXY.read_bytes()
    c = constantes_du_scénario(SCENARIO)
    if c["SHA_PROXY"] != SHA_PROXY or c["TAILLE_PROXY"] != TAILLE_PROXY:
        refus("RECOUP", "l'empreinte/taille du scénario != l'artefact")
    if c["R_TLS28"] != 0x10D00:
        refus("RECOUP", f"R_TLS28 = {c['R_TLS28']:#x} != 0x10D00 "
                        "(l'erratum n° 5 : le socle DÉPLACÉ après les "
                        "fixtures)")
    attendus = {
        "R_SYS01": 0xA000, "R_SYS02": 0xA040, "R_SYS04": 0xA240,
        "R_SYS05": 0xA540, "R_SYS06": 0xA6C0, "R_TLS27": 0xFF40,
        "R_TLS28": 0x10D00, "R_SYS_DEVICE": 0x10C20,
        "R_SYS_NOM_CREATEFILE": 0x10CB0,
        "R_SYS_NOM_DEVICEIOCTL": 0x10CC0, "R_SYS_NOM_CLOSE": 0x10CE0,
        "R_TETE_CH": 0x10082,
    }
    for nom, attendu in attendus.items():
        if c[nom] != attendu:
            refus("RECOUP", f"{nom} = {c[nom]:#x} != {attendu:#x} (le plan)")
    if c["OCTETS_SYS01"] != data[rva_vers_offset(data, 0xA000):
                                 rva_vers_offset(data, 0xA000) + 6]:
        refus("RECOUP", "OCTETS_SYS01 != les octets de l'artefact @0xA000")
    if c["OCTETS_TETE_CH"] != data[rva_vers_offset(data, 0x10082):
                                    rva_vers_offset(data, 0x10082) + 12]:
        refus("RECOUP", "OCTETS_TETE_CH != les octets de l'artefact "
                        "@0x10082 (l'erratum n° 5 : l'octet 0x72)")
    if c["OCTETS_TETE_CH"][-5:] != bytes.fromhex("41c6420472") \
            or c["OCTETS_TETE_CH"][-1:] != b"\x72":
        refus("RECOUP", "l'octet de longueur du record CH != 0x72")
    fixture_attendu = c["NOM_DEVICE"].encode("utf-16le") + b"\x00\x00"
    if fixture_attendu != data[rva_vers_offset(data, 0x10C20):
                               rva_vers_offset(data, 0x10C20) + 42]:
        refus("RECOUP", "le device AFD dérivé du NOM du scénario != "
                        "l'artefact @0x10C20")
    if c["MOTIF_STUB"] != bytes.fromhex("4c8bd1b8"):
        refus("RECOUP", "MOTIF_STUB != le motif du plan")
    if c["EMPREINTE_EPINGLEE"].hex() != EMPREINTE:
        refus("RECOUP", "l'empreinte épinglée du scénario != la pièce de "
                        "la sonde du 06/11")
    if c["CIBLE"] != "www.cloudflare.com" or c["CIBLE_PORT"] != 443:
        refus("RECOUP", "la cible != la décision du labo")
    if c["TEMOIN_APPLICATIF"] != b"HTTP/1.1 200 OK":
        refus("RECOUP", "le témoin applicatif != la pièce de la sonde")
    print(f"[2] le recoup PAR AST : {len(c)} constantes du scénario == "
          f"l'artefact/le plan/la sonde — AUCUN chiffre gravé de tête "
          f"(l'octet 0x72 de l'erratum n° 5 relu DANS L'IMAGE)")

    # le plan relu (la source unique des dimensions)
    layout = (REPO / "tls13" / "layout.py").read_text(encoding="utf-8")
    if "SESSION_TAILLE = 17520" not in layout:
        refus("RECOUP", "tls13/layout.py ne porte pas SESSION_TAILLE 17520")
    if "CLIENTHELLO_TAILLE = 114" not in layout:
        refus("RECOUP", "tls13/layout.py ne porte pas CLIENTHELLO_TAILLE 114")
    if c["SESSION_TAILLE"] != 17520 or c["CH_TAILLE"] != 114 \
            or c["KIT96"] != 96:
        refus("RECOUP", "les dimensions du scénario != la spec tls13-27 P1")
    if c["CH_RECORD"] != bytes.fromhex("1603030072"):
        refus("RECOUP", "CH_RECORD != 16 03 03 00 72 (l'erratum n° 5)")
    print("    le plan relu : SESSION_TAILLE 17520, CLIENTHELLO_TAILLE 114 "
          "— le record 16 03 03 00 72")

    # -- 2b. LE CONTRÔLE PERMANENT DE L'ERRATUM n° 6 (la faute ne peut plus
    # dormir) : les lecteurs de SSN (le miroir Python ET le bloc sys-02)
    # lisent LE VRAI ntdll — l'AST exige `ntdll_base` au premier argument
    # DES TROIS sites, JAMAIS `base` (l'artefact cartographié : proxy.exe
    # n'a PAS de répertoire export — le refus -3 « répertoire export
    # absent » du premier run du 06/11 était INÉVITABLE sur toute machine).
    arbre_t1 = ast.parse(SCENARIO.read_text(encoding="utf-8"))
    sites = []
    for noeud in ast.walk(arbre_t1):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "ssn_par_deux_lecteurs":
            arg = noeud.args[0] if noeud.args else None
            sites.append(isinstance(arg, ast.Name) and arg.id == "ntdll_base")
    if len(sites) != 3 or not all(sites):
        refus("ERRATUM-6", f"les lecteurs de SSN : {len(sites)} site(s), "
                           f"{sites.count(True)} à ntdll_base — T1 doit passer "
                           "NTDLL_BASE (le VRAI ntdll lu par les DEUX "
                           "lecteurs), jamais la base de l'artefact (l'erratum "
                           "n° 6, le premier run du 06/11 l'a nommé)")
    print("[2b] LE CONTRÔLE PERMANENT erratum n° 6 : les TROIS lecteurs de "
          "SSN reçoivent `ntdll_base` — constaté PAR AST (le refus -3 du "
          "premier run ne peut plus dormir)")

    # -- 2c. LE CONTRÔLE PERMANENT DE L'ERRATUM n° 7 (la faute ne peut plus
    # dormir) : le second run du 06/11 (16:56) est mort d'un TypeError
    # PYTHON NOMMÉ sur la console du développeur — `kit96.raw[:32] = alea`
    # (ligne 593 : `.raw` est une copie bytes IMMUABLE, l'écriture par
    # tranches échoue sur TOUTE machine — le kit N'ÉTAIT PAS acquitté,
    # l'Entrée 181 est RENVERSÉE par la pièce) ; l'échelle du recoup
    # rendait la « clé attendue » NULLE (x_3 né à 0 : le point à l'infini ;
    # a24 = (p+1)//4 : la fausse courbe) ; ET les sites OUVRIR passaient
    # la TAILLE (96) en r9 où tls13-27 P2 É1 exige LE POINTEUR des 96 o
    # (la machine lirait à l'adresse 0x60). TROIS portes, une faute par
    # porte — le contrôle négatif est prouvé sur la pointe pré-réparation
    # (35706ef) par scripts/preuve_negative_e7.py : les TROIS refus.
    portes_erratum_7(SCENARIO)
    print("[2c] LE CONTRÔLE PERMANENT erratum n° 7 : AUCUNE écriture "
          "`.raw[...]` ; les DEUX sites OUVRIR portent "
          "ctypes.addressof(kit96|kit96_2) en r9 ; l'échelle re-jouée "
          "CONTRE LES VECTEURS OFFICIELS du dépôt (RFC 7748 § 6.1 "
          "Alice/Bob, le couple RFC 8448 § 3, 16 clés semées contre "
          "ref_x25519) — le TypeError du second run ne peut plus dormir")

    # -- 3. la compilation du scénario -----------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(SCENARIO), cfile=os.path.join(tmp, "s.pyc"),
                           doraise=True)
    print("[3] le scénario compile (py_compile) — stdlib seule (imports : "
          "ctypes, hashlib, os, platform, socket, struct, sys, "
          "threading, time)")

    # -- 4. l'assemblage --------------------------------------------------------
    zone = SORTIE / "vague-m9f"
    racine = zone / KIT
    if racine.exists():
        shutil.rmtree(racine)
    racine.mkdir(parents=True)
    shutil.copy2(PROXY, racine / "proxy.exe")
    shutil.copy2(SCENARIO, racine / "scenario-m9f.py")
    shutil.copy2(LISEZMOI, racine / "LISEZMOI-KIT-M9F.md")
    pieces = {
        "proxy.exe": SHA_PROXY,
        "scenario-m9f.py": sha256_fichier(racine / "scenario-m9f.py"),
        "LISEZMOI-KIT-M9F.md": sha256_fichier(racine / "LISEZMOI-KIT-M9F.md"),
    }
    for nom, attendu in pieces.items():
        if sha256_fichier(racine / nom) != attendu:
            refus("ASSEMBLAGE", f"{nom} : empreinte divergente après copie")
    print(f"[4] assemblé : {racine} ({len(pieces)} pièces, empreintes "
          f"recoupées après copie)")

    # -- 5. le zip + l'épreuve d'extraction vierge -------------------------------
    if KIT_ZIP.exists():
        KIT_ZIP.unlink()
    with zipfile.ZipFile(KIT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for nom in sorted(pieces):
            z.write(racine / nom, f"{KIT}/{nom}")
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(KIT_ZIP) as z:
            z.extractall(tmp)
        extraite = pathlib.Path(tmp) / KIT
        noms = sorted(p.name for p in extraite.iterdir())
        if noms != sorted(pieces):
            refus("ÉPREUVE", f"extraction : {noms} != {sorted(pieces)}")
        for nom, attendu in pieces.items():
            if sha256_fichier(extraite / nom) != attendu:
                refus("ÉPREUVE", f"{nom} : empreinte divergente après "
                                 f"extraction vierge")
    print(f"[5] l'épreuve d'extraction vierge : VERT — kit-m9f.zip "
          f"({KIT_ZIP.stat().st_size} o, {len(pieces)} pièces, empreintes "
          f"re-constatées)")

    print(f"\n[le kit est PRÊT AU DÉPÔT] : {KIT_ZIP}")
    print("  md5 :", hashlib.md5(KIT_ZIP.read_bytes()).hexdigest())
    print("  sha256 :", sha256_fichier(KIT_ZIP))
    print("  (le dépôt au coffre /test : scripts/deposer_kit_m9f.py)")


if __name__ == "__main__":
    main()
