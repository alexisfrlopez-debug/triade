#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_sondesys06.py — LE KIT SONDE SYS-06 (m9-(g)) ASSEMBLÉ ET
ÉPROUVÉ au labo (la sonde NOMMÉE D'AVANCE par le recoup-5 et la passation
107, OUVERTE par le recoup du sixième run : le passager éliminé sur
pièces — lire LE CODE EXACT de la première lecture réelle : n / -7 le
zéro de la demi-fin / -6 + LE NTSTATUS BRUT de rdx ; l'artefact INTACT,
JAMAIS reconstruit).

Modèle : scripts/assembler_kit_sondesys05.py (l'Entrée 185 — le miroir
exact) — le labo NE PEUT PAS exécuter la sonde (Windows + le VRAI ntdll
+ le VRAI afd.sys exigés) ; l'épreuve de labo est :

  1. L'ASSEMBLAGE : sonde-sys06-kit/ = proxy.exe (l'artefact 1.0.0-dev.3
     RÉPARÉ, sha256 de23e577… ASSERTÉ — LE MÊME que le kit m9f actuel,
     celui des runs 5/6) + scenario-sonde-sys06.py +
     LISEZMOI-KIT-SONDE-SYS06.md ;
  2. LE RECOUP DES CONSTANTES PAR AST (les adresses scellées, le
     trombone, l'octet de l'erratum n° 5, LA POSE DU WSABUF de
     l'erratum n° 9 aux DEUX blocs, les fixtures, le motif du stub,
     l'empreinte épinglée, les dimensions de session) relu DANS
     L'ARTEFACT ou DANS LE PLAN — la source unique est le dépôt ;
  3. LES PORTES DE L'ERRATUM n° 7 (aucune écriture `.raw[...]`, le site
     OUVRIR au POINTEUR, l'échelle contre les vecteurs officiels) ;
  4. LES PORTES DE LA SONDE :
     - PORTE S1 — LE TRAMPOLINE : le squelette EXACT (33 o : sub
       rsp,0x28 ; mov rax,imm64 ; call rax ; shl rdx,32 ; mov ecx,eax ;
       or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret — l'ABI msx64 :
       shadow space + pile alignée au call, démontrés) ET la pose par
       squelette[:6] + pack(base + R_SYS06) + squelette[14:] ;
     - PORTE S2 — LA TABLE NTSTATUS : les 23 valeurs == LA RÉFÉRENCE
       CANONIQUE (ntstatus.h : Wine ET ReactOS s'accordent au bit près,
       vérifiés au labo le 07/11 — la provenance est la règle, jamais un
       chiffre gravé de tête) ;
     - PORTE S3 — LE COMPAS AVANT LA MESURE : l'appel au trampoline au
       HANDLE INVALIDE précède l'appel de mesure (un instrument non
       étalonné ne mesure pas — fail-closed) ;
     - PORTE S4 — LE TÉMOIN ÉCRIT AU FUR ET À MESURE (_ecrire_temoin
       appelé après la mesure : les pièces du cœur survivent à tout
       arrêt ultérieur) ;
     - PORTE S5 — LE GESTE DÉCOMPOSÉ : l'offre (sys-05 DIRECT, le
       chemin réparé) PRÉCÈDE la lecture (le trampoline) — la sonde
       rejoue LE GESTE M9F en deux temps mesurés, elle ne réinvente
       rien.
  5. LA COMPILATION (py_compile) ;
  6. L'ÉPREUVE D'EXTRACTION VIERGE (le zip extrait NEUF, empreintes
     re-constatées) ;
  7. LE ZIP : kit-sonde-sys06.zip (l'archive déposée au coffre /test).

Usage : python3 scripts/assembler_kit_sondesys06.py
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
KIT = "sonde-sys06-kit"
SORTIE = pathlib.Path("/home/z/my-project/download")
KIT_ZIP = SORTIE / "kit-sonde-sys06.zip"

SHA_PROXY = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
             "66b29226f")
TAILLE_PROXY = 65024
SCENARIO = REPO / "tls13" / "terrain" / "scenario-sonde-sys06.py"
LISEZMOI = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-SONDE-SYS06.md"
PROXY = REPO / "tls13" / "proxy.exe"

EMPREINTE = "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f"

# LA RÉFÉRENCE CANONIQUE DES NTSTATUS (ntstatus.h — Wine et ReactOS
# s'accordent au bit près ; les valeurs réseau sont la partie qui corrige
# les fausses mémoires : INVALID_DEVICE_STATE = 0xC0000184,
# CONNECTION_RESET = 0xC000020D — vérifiés aux DEUX sources le 07/11)
NTSTATUS_REFERENCE = {
    0x00000000: "STATUS_SUCCESS", 0x00000102: "STATUS_TIMEOUT",
    0x00000103: "STATUS_PENDING", 0x80000005: "STATUS_BUFFER_OVERFLOW",
    0xC0000008: "STATUS_INVALID_HANDLE",
    0xC000000D: "STATUS_INVALID_PARAMETER",
    0xC0000010: "STATUS_INVALID_DEVICE_REQUEST",
    0xC00000A3: "STATUS_DEVICE_NOT_READY",
    0xC00000BF: "STATUS_NETWORK_BUSY",
    0xC00000D0: "STATUS_REQUEST_NOT_ACCEPTED",
    0xC0000120: "STATUS_CANCELLED",
    0xC000013B: "STATUS_LOCAL_DISCONNECT",
    0xC000013C: "STATUS_REMOTE_DISCONNECT",
    0xC0000184: "STATUS_INVALID_DEVICE_STATE",
    0xC000020C: "STATUS_CONNECTION_DISCONNECTED",
    0xC000020D: "STATUS_CONNECTION_RESET",
    0xC0000236: "STATUS_CONNECTION_REFUSED",
    0xC0000237: "STATUS_GRACEFUL_DISCONNECT",
    0xC000023A: "STATUS_CONNECTION_INVALID",
    0xC000023C: "STATUS_NETWORK_UNREACHABLE",
    0xC000023D: "STATUS_HOST_UNREACHABLE",
    0xC000023E: "STATUS_PROTOCOL_UNREACHABLE",
    0xC0000241: "STATUS_CONNECTION_ABORTED",
}

# LE SQUELETTE DU TRAMPOLINE (la PORTE S1 — l'ABI msx64 : sub 0x28 rend
# la pile alignée au `call rax`, le shadow space 0x20 couvert)
SQUELETTE_ATTENDU = (b"\x48\x83\xec\x28" + b"\x48\xb8" + b"\x00" * 8
                     + b"\xff\xd0" + b"\x48\xc1\xe2\x20" + b"\x89\xc1"
                     + b"\x48\x09\xd1" + b"\x48\x89\xc8"
                     + b"\x48\x83\xc4\x28" + b"\xc3")

# LA POSE DU WSABUF canonique (l'erratum n° 9) : buf à +8, les NEUF
# octets relus DANS L'IMAGE aux DEUX blocs (sys-05 +0x46, sys-06 +0x46)
POSE_WSABUF_OFF = 0x46
OCTETS_POSE_WSABUF = bytes.fromhex("8974246048897c2468")


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
    """RVA -> offset fichier (PE32+ de l'artefact)."""
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
    if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute) \
            and noeud.func.attr == "fromhex" \
            and isinstance(noeud.func.value, ast.Name) \
            and noeud.func.value.id == "bytes" and len(noeud.args) == 1:
        return bytes.fromhex(ast.literal_eval(noeud.args[0]))
    if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Add):
        return _litteral(noeud.left) + _litteral(noeud.right)
    if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Mult):
        return _litteral(noeud.left) * _litteral(noeud.right)
    return ast.literal_eval(noeud)


def _extraire_fonction(chemin, nom, namespace=None):
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
    """Extrait les constantes nommées de la sonde PAR AST (jamais gravées)."""
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    cibles = {"SHA_PROXY", "TAILLE_PROXY", "R_SYS01", "R_SYS02", "R_SYS04",
              "R_SYS05", "R_SYS06", "R_TLS27", "R_TLS28", "R_SYS_DEVICE",
              "R_SYS_NOM_CREATEFILE", "R_SYS_NOM_DEVICEIOCTL",
              "R_SYS_NOM_CLOSE", "R_TETE_CH", "OCTETS_SYS01",
              "OCTETS_TETE_CH", "NOM_DEVICE", "MOTIF_STUB",
              "EMPREINTE_EPINGLEE", "CIBLE", "CIBLE_PORT",
              "SESSION_TAILLE", "KIT96", "CH_TAILLE", "CH_RECORD",
              "TEMOIN_APPLICATIF", "SQUELETTE_TRAMPO", "HANDLE_INVALIDE",
              "NTSTATUS_NOMS", "POSE_WSABUF_OFF", "OCTETS_POSE_WSABUF"}
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
        refus("AST", f"constantes absentes de la sonde : {sorted(manquantes)}")
    return trouves


# --- les portes de l'erratum n° 7 (héritées du kit m9f) --------------------------

def _porte_e7_1_raw(arbre):
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Subscript) \
                        and isinstance(cible.value, ast.Attribute) \
                        and cible.value.attr == "raw":
                    return ("ERRATUM-7 porte 1",
                            f"ligne {noeud.lineno} : écriture par tranches "
                            "sur `.raw` — une copie bytes IMMUABLE")
    return None


def _porte_e7_2_ouvrir_sonde(arbre):
    """LE site OUVRIR de la sonde porte LE POINTEUR des 96 o en r9 (UN
    seul site : la sonde ne porte pas la falsification T5)."""
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
                         and r9.args[0].id == "kit96")
    if len(sites) != 1 or not all(sites):
        return ("ERRATUM-7 porte 2 (sonde)",
                f"les sites OUVRIR : {len(sites)} trouvé(s), "
                f"{sites.count(True)} portant ctypes.addressof(kit96) en r9 "
                "— tls13-27 P2 É1 exige LE POINTEUR des 96 o")
    return None


def _porte_e7_3_echelle(chemin_scenario):
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
                "les VECTEURS OFFICIELS du dépôt sont introuvables")
    if echelle(officiels["ALICE_PRIV"]) != officiels["ALICE_PUB"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle de la sonde rate le vecteur RFC 7748 § 6.1 Alice")
    if echelle(officiels["BOB_PRIV"]) != officiels["BOB_PUB"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle de la sonde rate le vecteur RFC 7748 § 6.1 Bob")
    if echelle(transfert["client_priv"]) != transfert["client_pub"]:
        return ("ERRATUM-7 porte 3",
                "l'échelle de la sonde rate le couple RFC 8448 § 3")
    ref = _extraire_fonction(harnais_x, "ref_x25519", {"P": 2 ** 255 - 19})
    u9 = (9).to_bytes(32, "little")
    rng = random.Random(20261107)
    for _ in range(16):
        cle = bytes(rng.randrange(256) for _ in range(32))
        if echelle(cle) != ref(cle, u9):
            return ("ERRATUM-7 porte 3",
                    "l'échelle de la sonde diverge de ref_x25519")
    return None


# --- les portes propres à la sonde -----------------------------------------------

def _porte_s1_trampo(c):
    """PORTE S1 — le squelette EXACT (33 o, l'ABI démontrée) et la pose
    par découpe (préfixe 6 + imm64 base+R_SYS06 + reste 19)."""
    if c["SQUELETTE_TRAMPO"] != SQUELETTE_ATTENDU:
        return ("PORTE S1",
                f"le squelette du trampoline diverge : "
                f"{c['SQUELETTE_TRAMPO'].hex()}")
    if len(c["SQUELETTE_TRAMPO"]) != 33:
        return ("PORTE S1", "le squelette ne fait pas 33 octets")
    src = SCENARIO.read_text(encoding="utf-8")
    if "SQUELETTE_TRAMPO[:6]" not in src \
            or "SQUELETTE_TRAMPO[14:]" not in src \
            or "struct.pack(\"<Q\", base + R_SYS06)" not in src:
        return ("PORTE S1",
                "la pose du trampoline n'est pas la découpe attendue "
                "(squelette[:6] + imm64 base+R_SYS06 + squelette[14:])")
    return None


def _porte_s2_table(c):
    """PORTE S2 — la table NTSTATUS == LA RÉFÉRENCE CANONIQUE."""
    table = c["NTSTATUS_NOMS"]
    if len(table) != len(NTSTATUS_REFERENCE):
        return ("PORTE S2",
                f"la table porte {len(table)} entrées != "
                f"{len(NTSTATUS_REFERENCE)} (la référence canonique)")
    for valeur, nom in NTSTATUS_REFERENCE.items():
        if table.get(valeur, "").split(" (")[0] != nom:
            return ("PORTE S2",
                    f"0x{valeur:08X} : « {table.get(valeur)} » != "
                    f"« {nom} » (la référence ntstatus.h)")
    return None


def _porte_s3_compas(arbre):
    """PORTE S3 — LE COMPAS AVANT LA MESURE : l'appel au trampoline au
    HANDLE INVALIDE précède l'appel de mesure (fail-closed)."""
    ligne_compas = ligne_mesure = None
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "trampo" and noeud.args:
            premier = noeud.args[1] if len(noeud.args) > 1 else None
            if isinstance(premier, ast.Name) and premier.id == \
                    "HANDLE_INVALIDE":
                if ligne_compas is None:
                    ligne_compas = noeud.lineno
            elif isinstance(premier, ast.Name) and premier.id == "handle_1":
                if ligne_mesure is None:
                    ligne_mesure = noeud.lineno
    if ligne_compas is None or ligne_mesure is None:
        return ("PORTE S3",
                f"le compas (ligne {ligne_compas}) ou la mesure (ligne "
                f"{ligne_mesure}) est introuvable — les DEUX appels au "
                "trampoline sont exigés")
    if ligne_compas > ligne_mesure:
        return ("PORTE S3",
                f"le compas (ligne {ligne_compas}) SUIT la mesure (ligne "
                f"{ligne_mesure}) — un instrument non étalonné ne mesure "
                "pas")
    return None


def _porte_s4_temoin_vivant(arbre):
    """PORTE S4 — LE TÉMOIN ÉCRIT AU FUR ET À MESURE : la fonction
    _ecrire_temoin existe ET est appelée au moins TROIS fois (la
    garde-chien, la mesure, le verdict : les pièces du cœur survivent à
    tout arrêt ultérieur)."""
    defs = {n.name for n in ast.walk(arbre)
            if isinstance(n, ast.FunctionDef) and n.name == "_ecrire_temoin"}
    if not defs:
        return ("PORTE S4", "la fonction _ecrire_temoin est absente")
    appels = [n.lineno for n in ast.walk(arbre)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
              and n.func.id == "_ecrire_temoin"]
    if len(appels) < 3:
        return ("PORTE S4",
                f"_ecrire_temoin n'est appelée que {len(appels)} fois — "
                "le témoin doit vivre au fil du run (la garde-chien, la "
                "mesure, le verdict)")
    return None


def _porte_s5_geste_decompose(arbre):
    """PORTE S5 — LE GESTE M9F DÉCOMPOSÉ : l'offre (sys-05 DIRECT, le
    chemin réparé) PRÉCÈDE la lecture (le trampoline) sur LA MÊME
    session (handle_1) — la sonde rejoue le geste des runs 5/6 en deux
    temps mesurés, elle ne réinvente rien."""
    ligne_offre = ligne_lecture = None
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "SYS05" and len(noeud.args) >= 2:
            second = noeud.args[1]
            if isinstance(second, ast.Name) and second.id == "handle_1" \
                    and ligne_offre is None:
                ligne_offre = noeud.lineno
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "trampo" and len(noeud.args) >= 2:
            second = noeud.args[1]
            if isinstance(second, ast.Name) and second.id == "handle_1" \
                    and ligne_lecture is None:
                ligne_lecture = noeud.lineno
    if ligne_offre is None or ligne_lecture is None:
        return ("PORTE S5",
                f"l'offre sys-05 direct (ligne {ligne_offre}) ou la "
                f"lecture par le trampoline (ligne {ligne_lecture}) est "
                "introuvable sur la session de la mesure")
    if ligne_offre > ligne_lecture:
        return ("PORTE S5",
                f"l'offre (ligne {ligne_offre}) SUIT la lecture (ligne "
                f"{ligne_lecture}) — le geste m9f est L'OFFRE PUIS LA "
                "LECTURE, la décomposition suit l'ordre du geste")
    return None


def main():
    print("=== L'ASSEMBLAGE DU KIT SONDE SYS-06 (m9-(g) — LE CODE EXACT "
          "DE LA PREMIÈRE LECTURE RÉELLE : la sonde nommée d'avance, "
          "ouverte par le recoup du sixième run) ===")

    # -- 1. les pièces du dépôt, vérifiées ------------------------------------
    if sha256_fichier(PROXY) != SHA_PROXY:
        refus("ARTEFACT", f"proxy.exe sha256 {sha256_fichier(PROXY)[:16]}… "
                          f"!= {SHA_PROXY[:16]}…")
    print(f"[1] l'artefact : {TAILLE_PROXY} o, sha256 {SHA_PROXY[:16]}… — "
          f"LE MÊME que le kit m9f RÉPARÉ (INTACT : la sonde ne reconstruit "
          f"RIEN — celui des runs 5/6)")

    # -- 2. le recoup des constantes (AST de la sonde contre l'artefact) ------
    data = PROXY.read_bytes()
    c = constantes_du_scénario(SCENARIO)
    if c["SHA_PROXY"] != SHA_PROXY or c["TAILLE_PROXY"] != TAILLE_PROXY:
        refus("RECOUP", "l'empreinte/taille de la sonde != l'artefact")
    attendus = {
        "R_SYS01": 0xA000, "R_SYS02": 0xA040, "R_SYS04": 0xA240,
        "R_SYS05": 0xA540, "R_SYS06": 0xA6C0, "R_TLS27": 0xFF40,
        "R_TLS28": 0x10D00, "R_SYS_DEVICE": 0x10C20,
        "R_SYS_NOM_CREATEFILE": 0x10CB0,
        "R_SYS_NOM_DEVICEIOCTL": 0x10CC0, "R_SYS_NOM_CLOSE": 0x10CE0,
        "R_TETE_CH": 0x10082, "POSE_WSABUF_OFF": 0x46,
    }
    for nom, attendu in attendus.items():
        if c[nom] != attendu:
            refus("RECOUP", f"{nom} = {c[nom]:#x} != {attendu:#x} (le plan)")
    if c["OCTETS_SYS01"] != data[rva_vers_offset(data, 0xA000):
                                 rva_vers_offset(data, 0xA000) + 6]:
        refus("RECOUP", "OCTETS_SYS01 != les octets de l'artefact @0xA000")
    if c["OCTETS_TETE_CH"] != data[rva_vers_offset(data, 0x10082):
                                   rva_vers_offset(data, 0x10082) + 12]:
        refus("RECOUP", "OCTETS_TETE_CH != l'artefact @0x10082")
    if c["OCTETS_TETE_CH"][-1:] != b"\x72":
        refus("RECOUP", "l'octet de longueur du record CH != 0x72")
    if c["OCTETS_POSE_WSABUF"] != OCTETS_POSE_WSABUF:
        refus("RECOUP", "OCTETS_POSE_WSABUF != la pose canonique du plan "
                        "(l'erratum n° 9)")
    for rva, nom in ((0xA540, "sys-05"), (0xA6C0, "sys-06")):
        site = rva + c["POSE_WSABUF_OFF"]
        if c["OCTETS_POSE_WSABUF"] != data[rva_vers_offset(data, site):
                                           rva_vers_offset(data, site) + 9]:
            refus("RECOUP", f"la pose du WSABUF relue dans {nom} "
                            f"@{site:#x} != l'artefact (l'erratum n° 9 : "
                            "buf à +8, JAMAIS un « packé »)")
    fixture_attendu = c["NOM_DEVICE"].encode("utf-16le") + b"\x00\x00"
    if fixture_attendu != data[rva_vers_offset(data, 0x10C20):
                               rva_vers_offset(data, 0x10C20) + 42]:
        refus("RECOUP", "le device AFD dérivé du NOM != l'artefact @0x10C20")
    if c["MOTIF_STUB"] != bytes.fromhex("4c8bd1b8"):
        refus("RECOUP", "MOTIF_STUB != le motif du plan")
    if c["EMPREINTE_EPINGLEE"].hex() != EMPREINTE:
        refus("RECOUP", "l'empreinte épinglée != la pièce de la sonde 06/11")
    if c["CIBLE"] != "www.cloudflare.com" or c["CIBLE_PORT"] != 443:
        refus("RECOUP", "la cible != la décision du labo")
    if c["TEMOIN_APPLICATIF"] != b"HTTP/1.1 200 OK":
        refus("RECOUP", "le témoin applicatif != la pièce de la sonde")
    if c["CH_RECORD"] != bytes.fromhex("1603030072"):
        refus("RECOUP", "CH_RECORD != 16 03 03 00 72 (l'erratum n° 5)")
    if c["SESSION_TAILLE"] != 17520 or c["CH_TAILLE"] != 114 \
            or c["KIT96"] != 96:
        refus("RECOUP", "les dimensions de la sonde != la spec tls13-27 P1")
    if c["HANDLE_INVALIDE"] != 0xDEAD0000:
        refus("RECOUP", "HANDLE_INVALIDE != 0xDEAD0000 (le compas)")
    print(f"[2] le recoup PAR AST : {len(c)} constantes de la sonde == "
          f"l'artefact/le plan/la sonde — dont LA POSE DU WSABUF relue "
          f"DANS L'IMAGE aux DEUX blocs (sys-05 @0x{0xA586:X} ET sys-06 "
          f"@0x{0xA706:X} — l'erratum n° 9, celui que les runs 5/6 ont "
          f"porté) — AUCUN chiffre gravé de tête")

    # -- 3. LES PORTES (l'erratum n° 7 hérité + les portes de la sonde) -------
    arbre = ast.parse(SCENARIO.read_text(encoding="utf-8"))
    for porte in (_porte_e7_1_raw, _porte_e7_2_ouvrir_sonde,
                  _porte_s3_compas, _porte_s4_temoin_vivant,
                  _porte_s5_geste_decompose):
        verdict = porte(arbre)
        if verdict:
            refus(*verdict)
    for porte in (_porte_s1_trampo, _porte_s2_table):
        verdict = porte(c)
        if verdict:
            refus(*verdict)
    verdict = _porte_e7_3_echelle(SCENARIO)
    if verdict:
        refus(*verdict)
    print("[3] LES PORTES passées : l'erratum n° 7 (aucune écriture .raw, "
          "LE site OUVRIR au POINTEUR, l'échelle contre les vecteurs "
          "officiels RFC 7748/8448 + 16 clés semées) ; LA PORTE S1 (le "
          "squelette du trampoline EXACT, 33 o, la pose par découpe vers "
          "sys-06) ; LA PORTE S2 (la table NTSTATUS == la référence "
          "canonique ntstatus.h — 23 valeurs au bit près) ; LA PORTE S3 "
          "(le compas AVANT la mesure) ; LA PORTE S4 (le témoin écrit au "
          "fil du run) ; LA PORTE S5 (LE GESTE DÉCOMPOSÉ : l'offre sys-05 "
          "direct AVANT la lecture par le trampoline — l'ordre du geste "
          "m9f)")

    # -- 4. la compilation ------------------------------------------------------
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(SCENARIO), cfile=os.path.join(tmp, "s.pyc"),
                           doraise=True)
    print("[4] la sonde compile (py_compile) — stdlib seule")

    # -- 5. l'assemblage --------------------------------------------------------
    zone = SORTIE / "vague-sonde-sys06"
    racine = zone / KIT
    if racine.exists():
        shutil.rmtree(racine)
    racine.mkdir(parents=True)
    shutil.copy2(PROXY, racine / "proxy.exe")
    shutil.copy2(SCENARIO, racine / "scenario-sonde-sys06.py")
    shutil.copy2(LISEZMOI, racine / "LISEZMOI-KIT-SONDE-SYS06.md")
    pieces = {
        "proxy.exe": SHA_PROXY,
        "scenario-sonde-sys06.py": sha256_fichier(
            racine / "scenario-sonde-sys06.py"),
        "LISEZMOI-KIT-SONDE-SYS06.md": sha256_fichier(
            racine / "LISEZMOI-KIT-SONDE-SYS06.md"),
    }
    for nom, attendu in pieces.items():
        if sha256_fichier(racine / nom) != attendu:
            refus("ASSEMBLAGE", f"{nom} : empreinte divergente après copie")
    print(f"[5] assemblé : {racine} ({len(pieces)} pièces, empreintes "
          f"recoupées après copie)")

    # -- 6. le zip + l'épreuve d'extraction vierge -------------------------------
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
    print(f"[6] l'épreuve d'extraction vierge : VERT — kit-sonde-sys06.zip "
          f"({KIT_ZIP.stat().st_size} o, {len(pieces)} pièces, empreintes "
          f"re-constatées)")

    print(f"\n[le kit sonde est PRÊT AU DÉPÔT] : {KIT_ZIP}")
    print("  md5 :", hashlib.md5(KIT_ZIP.read_bytes()).hexdigest())
    print("  sha256 :", sha256_fichier(KIT_ZIP))
    print("  (le dépôt au coffre /test : scripts/deposer_kit_sondesys06.py)")


if __name__ == "__main__":
    main()
