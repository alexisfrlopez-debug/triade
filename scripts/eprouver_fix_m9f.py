#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eprouver_fix_m9f.py — L'ÉPREUVE DE LABO DE LA RÉPARATION erratum n° 7 (le
kit terrain M9-(f), le run 2 du 06/11 16:56 mort d'un TypeError PYTHON).

LA PIÈCE QUI RENVERSE L'ACQUITTEMENT : la console du développeur (le paste
du 07/11, download/preuves-run-m9f-2/console-run-m9f.txt) — l'Entrée 181
avait acquitté le kit « par élimination » (console gelée ou mort du
processus) : FAUX — le run est mort d'un crash NOMMÉ DANS LE KIT :
TypeError scenario-m9f.py:593 `kit96.raw[:32] = alea` (le geste
`create_string_buffer(...).raw[...] = ...` échoue sur TOUTE machine :
`.raw` est une copie bytes IMMUABLE), après avoir imprimé une « clé
publique attendue » NULLE (000…0) — le symptôme de la seconde faute.
TROIS fautes nommées, TOUTES au kit, JAMAIS au terrain ni à l'artefact
(proxy.exe d8928934… relu INTACT au T0 du run même) :
  (1) LA POSE DU KIT : `kit96.raw[:32] = alea` — TypeError déterministe
      (la ligne 593 de la console, le crash du run) ;
  (2) L'ÉCHELLE PYTHON DU RECOUP : x_3 né à 0 (le point à l'infini tient
      le résultat NUL) ET a24 = (p+1)//4 au lieu de 121665 (la fausse
      courbe) — la « clé attendue » 000…0 imprimée par le run mort, le
      recoup T3 aurait été IMPOSSIBLE même sans le crash ;
  (3) LE SITE OUVRIR : r9 = KIT96 (la TAILLE, 96) là où tls13-27 P2 É1
      exige LE POINTEUR des 96 o — la machine aurait lu à l'adresse
      0x60 : la mort au premier geste si le crash (1) n'avait pas devancé.
      La console n'a jamais atteint ce site : les fautes (1) et (3)
      vivaient à QUATRE lignes d'écart dans le même segment Python pur.

L'épreuve (le juge est le code) :
  A. LE POST-MORTEM REPRODUIT SUR PIÈCES : (A1) le TypeError EXACT de la
     console rejoué ; (A2) la « clé attendue » NULLE reproduite — la clé
     privée du run (la console, 82a24d22…) par l'échelle PRÉ-réparation
     (la pointe git 35706ef, lue PAR AST) → 000…0 ; (A3) le site OUVRIR
     pré-réparation passait la taille — lu PAR AST sur la pointe.
  B. LA RÉPARATION ÉPROUVÉE (la source réparée lue PAR AST, jamais gravée) :
     (B1) l'échelle réparée contre LES VECTEURS OFFICIELS du dépôt
     (harnais_x25519.py : RFC 7748 § 6.1 Alice/Bob, le couple RFC 8448
     § 3) ET LA RÉFÉRENCE ref_x25519 SUR 32 clés semées ;
     (B2) la clé privée DU RUN par l'échelle réparée → LA VRAIE clé
     attendue (ce que le run mort n'a pas su imprimer) ;
     (B3) la construction CH du kit == LA RÉFÉRENCE DU HARNAIS
     (ref_construction_ch, octet pour octet, 3 essais semés : 114 o,
     l'aléa @ +6, la clé publique @ +82, le vol 119 o) ;
     (B4) la mécanique des 96 o : create_string_buffer pose exactement
     TAILLE octets, les TROIS champs relus, addressof vivant ;
     (B5) py_compile de la source réparée.
  C. L'AUDIT AST DE LA SOURCE RÉPARÉE : AUCUNE écriture `.raw[...]`, les
     DEUX sites OUVRIR portent `ctypes.addressof(kit96|kit96_2)`, KIT96
     == 96 (la garde de l'assembleur demeure).

Usage : python3 scripts/eprouver_fix_m9f.py
Code de sortie : 0 = TOUT VERT ; 2 = refus nommé."""

import ast
import ctypes
import importlib.util
import pathlib
import py_compile
import random
import subprocess
import sys
import tempfile

REPO = pathlib.Path("/home/z/my-project/triade")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
HARNAIS_X = REPO / "tls13" / "harnais_x25519.py"
HARNAIS_P = REPO / "tls13" / "harnais_poignee.py"
LAYOUT = REPO / "tls13" / "layout.py"
POINTE_PRE = "35706ef"          # la pointe pré-réparation (Entrée 181)

# la clé privée DU RUN, imprimée par la console du développeur (la pièce)
CLE_PRIV_RUN = bytes.fromhex(
    "82a24d2261ac58fcd0e76d10ed2ec08f3d54759631a3352c7183b04244d5b5b5")

REUSSITES, ECHECS = [], []


def controle(nom, ok, detail=""):
    if ok:
        REUSSITES.append(nom)
        print(f"  [ok] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append((nom, detail))
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def refus(detail):
    print(f"\n[épreuve] REFUS : {detail}", file=sys.stderr)
    sys.exit(2)


def extraire_fonction(chemin, nom, namespace=None):
    """Une FunctionDef du fichier, extraite PAR AST et rendue exécutable
    (aucun import du module hôte — keystone/unicorn jamais requis)."""
    arbre = ast.parse(pathlib.Path(chemin).read_text(encoding="utf-8"))
    for noeud in arbre.body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == nom:
            module = ast.Module(body=[noeud], type_ignores=[])
            code = compile(module, filename=str(chemin), mode="exec")
            ns = {} if namespace is None else namespace
            exec(code, ns)
            return ns[nom]
    refus(f"la fonction {nom} est absente de {chemin}")


def vecteurs_officiels():
    """Les constantes officielles du harnais x25519 lues PAR AST (la source
    unique du dépôt : RFC 7748 § 6.1 + le transfert RFC 8448 § 3)."""
    arbre = ast.parse(HARNAIS_X.read_text(encoding="utf-8"))
    simples, transfert = {}, None
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign) and len(noeud.targets) == 1 \
                and isinstance(noeud.targets[0], ast.Name):
            nom = noeud.targets[0].id
            if nom in ("ALICE_PRIV", "ALICE_PUB", "BOB_PRIV", "BOB_PUB",
                       "PARTAGE"):
                simples[nom] = ast.literal_eval(noeud.value)
            elif nom == "TRANSFERT_8448":
                transfert = ast.literal_eval(noeud.value)
    if len(simples) != 5 or not transfert:
        refus("les vecteurs officiels sont introuvables dans "
              f"harnais_x25519.py ({sorted(simples)}, transfert "
              f"{'présent' if transfert else 'ABSENT'})")
    return {k: bytes.fromhex(v) if isinstance(v, str) else v
            for k, v in simples.items()}, \
        {k: bytes.fromhex(v) for k, v in transfert.items()}


def source_pre_reparation():
    """La pointe git pré-réparation du scénario (l'histoire fait foi)."""
    r = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{POINTE_PRE}:tls13/terrain/"
         "scenario-m9f.py"],
        capture_output=True, check=True)
    chemin = pathlib.Path(tempfile.mkdtemp()) / "scenario-pre-e7.py"
    chemin.write_bytes(r.stdout)
    return chemin


def main():
    print("=== L'ÉPREUVE DE LA RÉPARATION erratum n° 7 (kit M9-(f), "
          "le run 2 du 06/11) ===\n")

    # --- A. LE POST-MORTEM REPRODUIT SUR PIÈCES -----------------------------
    print("A — LE POST-MORTEM (la console du développeur, la pointe "
          f"git {POINTE_PRE})")
    # A1 : le crash nommé, rejoué mot pour mot
    tampon = ctypes.create_string_buffer(96)
    try:
        tampon.raw[:32] = b"\x42" * 32
        controle("A1:le-crash-nommé-rejoué", False,
                 "le geste `.raw[:32] = …` a PASSE — impossible, la pièce "
                 "dit le contraire")
    except TypeError as exc:
        controle("A1:le-crash-nommé-rejoué",
                 str(exc) == "'bytes' object does not support item "
                             "assignment",
                 f"TypeError « {exc} » — LE TEXTE EXACT de la ligne 593 "
                 "de la console")
    # A2 : la « clé attendue » NULLE, par l'échelle pré-réparation
    pre = source_pre_reparation()
    echelle_pre = extraire_fonction(pre, "x25519_echelle")
    rendu_pre = echelle_pre(CLE_PRIV_RUN)
    controle("A2:la-clé-NULLE-du-run-reproduite",
             rendu_pre == bytes(32),
             f"l'échelle PRÉ-réparation rend {rendu_pre.hex()} pour la clé "
             "privée du run (la console imprimait 000…0) — x_3 né à 0 : le "
             "point à l'infini")
    # A3 : le site OUVRIR pré-réparation passait la TAILLE
    arbre_pre = ast.parse(pre.read_text(encoding="utf-8"))
    sites_pre = []
    for noeud in ast.walk(arbre_pre):
        if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name) \
                and noeud.func.id == "TLS27" and len(noeud.args) >= 4 \
                and isinstance(noeud.args[1], ast.Constant) \
                and noeud.args[1].value == 1:
            sites_pre.append(isinstance(noeud.args[3], ast.Name)
                             and noeud.args[3].id == "KIT96")
    controle("A3:le-site-OUVRIR-passait-la-taille",
             len(sites_pre) == 2 and all(sites_pre),
             f"{len(sites_pre)} site(s) OUVRIR pré-réparation, "
             f"{sites_pre.count(True)} passant la TAILLE KIT96 en r9 — la "
             "machine aurait lu à l'adresse 0x60 (le crash-to-be, devancé "
             "de quatre lignes par A1)")

    # --- B. LA RÉPARATION ÉPROUVÉE -------------------------------------------
    print("\nB — LA RÉPARATION (la source réparée, lue PAR AST)")
    echelle = extraire_fonction(SCENARIO, "x25519_echelle")
    officiels, transfert = vecteurs_officiels()

    # B1a : les vecteurs officiels RFC 7748 § 6.1 (Alice, Bob)
    controle("B1a:RFC-7748-§6.1-Alice",
             echelle(officiels["ALICE_PRIV"]) == officiels["ALICE_PUB"],
             f"→ {echelle(officiels['ALICE_PRIV']).hex()}")
    controle("B1b:RFC-7748-§6.1-Bob",
             echelle(officiels["BOB_PRIV"]) == officiels["BOB_PUB"],
             f"→ {echelle(officiels['BOB_PRIV']).hex()}")
    # B1b : le couple RFC 8448 § 3 (le client du transfert officiel)
    controle("B1c:RFC-8448-§3-le-couple-client",
             echelle(transfert["client_priv"]) == transfert["client_pub"],
             f"→ {echelle(transfert['client_priv']).hex()}")
    # B1d : LA RÉFÉRENCE DU DÉPÔT (ref_x25519) sur 32 clés semées — les
    # DEUX lecteurs d'accord octet pour octet
    arbre_x = ast.parse(HARNAIS_X.read_text(encoding="utf-8"))
    p_harnais = None
    for noeud in arbre_x.body:
        if isinstance(noeud, ast.Assign) and len(noeud.targets) == 1 \
                and isinstance(noeud.targets[0], ast.Name) \
                and noeud.targets[0].id == "P":
            p_harnais = ast.unparse(noeud.value)
    if p_harnais != "2 ** 255 - 19":
        refus(f"la constante P du harnais lit « {p_harnais} » — inattendu")
    ref = extraire_fonction(HARNAIS_X, "ref_x25519", {"P": 2 ** 255 - 19})
    u9 = (9).to_bytes(32, "little")
    rng = random.Random(20261107)
    accord = True
    for _ in range(32):
        cle = bytes(rng.randrange(256) for _ in range(32))
        accord = accord and echelle(cle) == ref(cle, u9)
    controle("B1d:la-référence-du-dépôt-32-clés-semées", accord,
             "échelle réparée == ref_x25519 (harnais_x25519, vecteurs "
             "officiels du dépôt) octet pour octet")

    # B2 : la clé privée DU RUN → LA VRAIE clé attendue
    vraie = echelle(CLE_PRIV_RUN)
    controle("B2:la-vraie-clé-attendue-du-run",
             vraie != bytes(32) and len(vraie) == 32,
             f"82a24d22… → {vraie.hex()} — ce que le run mort aurait dû "
             "imprimer (et ce que tls13-14, l'autre lecteur, émettra dans "
             "le ClientHello)")

    # B3 : la construction CH du kit == LA RÉFÉRENCE DU HARNAIS
    spec = importlib.util.spec_from_file_location("layout", LAYOUT)
    layout = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(layout)
    ns_ref = {"L": layout}
    ns_ref["u16"] = extraire_fonction(HARNAIS_P, "u16", ns_ref)
    ref_ch = extraire_fonction(HARNAIS_P, "ref_construction_ch", ns_ref)
    construction = extraire_fonction(SCENARIO, "construction_ch_reference",
                                     {"struct": __import__("struct")})
    rng2 = random.Random(20261107)
    pareil = True
    for _ in range(3):
        alea = bytes(rng2.randrange(256) for _ in range(32))
        cle = bytes(rng2.randrange(256) for _ in range(32))
        pareil = pareil and construction(alea, cle) == ref_ch(alea, cle)
    controle("B3:la-construction-CH-==-la-référence", pareil,
             "octet pour octet sur 3 essais semés (harnais_poignee."
             "ref_construction_ch, le plan L)")
    ch = construction(b"\x11" * 32, vraie)
    controle("B3b:les-positions-du-recoup",
             len(ch) == 114 and ch[6:38] == b"\x11" * 32
             and ch[82:114] == vraie,
             f"114 o, l'aléa @ +6, la clé publique @ +82 — le vol "
             "5 + 114 = 119 o (16 03 03 00 72)")

    # B4 : la mécanique des 96 o (le geste réparé, ALEA + PRIV + EMPREINTE)
    empreinte = bytes.fromhex(
        "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f")
    kit96 = ctypes.create_string_buffer(
        b"\x11" * 32 + CLE_PRIV_RUN + empreinte, 96)
    controle("B4:les-96-o-posés-en-un-geste",
             ctypes.sizeof(kit96) == 96
             and kit96.raw[:32] == b"\x11" * 32
             and kit96.raw[32:64] == CLE_PRIV_RUN
             and kit96.raw[64:96] == empreinte
             and ctypes.addressof(kit96) != 0,
             f"exactement 96 o (aucun NUL ajouté), les TROIS champs relus, "
             f"addressof {ctypes.addressof(kit96):#x} — le POINTEUR que "
             "tls13-27 É1 exige en r9")

    # B5 : la compilation
    with tempfile.TemporaryDirectory() as tmp:
        py_compile.compile(str(SCENARIO), cfile=str(pathlib.Path(tmp)
                                                    / "s.pyc"),
                           doraise=True)
    controle("B5:py_compile", True, "la source réparée compile")

    # --- C. L'AUDIT AST DE LA SOURCE RÉPARÉE ---------------------------------
    print("\nC — L'AUDIT AST DE LA SOURCE RÉPARÉE (la garde permanente)")
    arbre = ast.parse(SCENARIO.read_text(encoding="utf-8"))
    ecritures_raw = 0
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Subscript) \
                        and isinstance(cible.value, ast.Attribute) \
                        and cible.value.attr == "raw":
                    ecritures_raw += 1
    controle("C1:AUCUNE-écriture-.raw[...]", ecritures_raw == 0,
             f"{ecritures_raw} écriture(s) par tranches sur .raw — le "
             "TypeError du run ne peut plus dormir")
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
    controle("C2:les-DEUX-sites-OUVRIR-portent-le-POINTEUR",
             len(sites) == 2 and all(sites),
             f"{len(sites)} site(s), {sites.count(True)} à "
             "ctypes.addressof(kit96|kit96_2) — tls13-27 P2 É1 : r9 = LE "
             "POINTEUR des 96 o, jamais la taille")
    constante_kit96 = None
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name) and cible.id == "KIT96":
                    constante_kit96 = ast.literal_eval(noeud.value)
    controle("C3:KIT96-demeure-96", constante_kit96 == 96,
             "la garde de l'assembleur (les dimensions de la spec "
             "tls13-27 P1) demeure satisfaite")

    print(f"\n=== BILAN : {len(REUSSITES)} VERT"
          + (f", {len(ECHECS)} ÉCHEC(S) — ARRÊTER" if ECHECS else "")
          + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")
    return 0 if not ECHECS else 2


if __name__ == "__main__":
    sys.exit(main())
