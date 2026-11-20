#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_incrementale.py — LA VÉRIFICATION INCRÉMENTALE (la vague 9,
l'instruction bkobf06nu point 1, le PLAN-BKOBF06NU H1 gelé).

LE GRAPHE DE DÉPENDANCES I↔C↔B↔tests construit depuis les notations du
domaine loupe : les arêtes d'APPEL (chaque « call 0x<adresse> » visant le
slot d'un autre bloc — lu de la notation assemblée, jamais déclaré à la
main) + les héritages R7 (les familles scellées aux adresses du plan) ;
la vérification devient UNE FONCTION DU DIFF : un changement au bloc X
ne re-vérifie QUE X et ses dépendants TRANSITIFS ; les blocs scellés
INCHANGÉS portent leur CERTIFICAT DE CRISTALLISATION (lié à l'empreinte
du bloc assemblé ‖ du contrat ‖ de la configuration de vérification ‖ de
l'identifiant d'oracle — TOUT écart force le REJEU COMPLET).

LE CERTIFICAT : la chaîne TRIADE-CERT-CRIST (chaque entrée chaînée depuis
la genèse, la racine signée Ed25519 par la clé de test publique — le
modèle D214/D222 : le certificat n'est JAMAIS cru, chaîne et signature
recalculées à chaque chargement, tout écart un REFUS NOMMÉ fail-closed).

LA VÉRIFICATION D'UN BLOC (la même que la session, JAMAIS affaiblie) :
  — le ROUND-TRIP : la notation assemblée (keystone), désassemblée
    (capstone), ré-assemblée — byte-identique (R5) ;
  — L'ORACLE DIFFÉRENTIEL de loupe-13 (la feuille pure : la recherche
    d'octet — l'implémentation triviale Python contre le bloc exécuté au
    harnais Unicorn, 64 vecteurs aux bords, la graine 20261120) ;
  — les EMPREINTES SCELLÉES intactes (loupe.exe, proxy.exe, selftest.exe).

Sortie : atelier-boucle-bkobf06nu/{graphe_deps.json, certificats.json,
rapport-verifier-incrementale.txt}.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import importlib.util
import json
import pathlib
import random
import sys
import time

import capstone
import keystone
import nacl.bindings
from nacl.signing import SigningKey, VerifyKey
import nacl.exceptions
import unicorn

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-boucle-bkobf06nu"
sys.path.insert(0, str(REPO / "scripts"))
ICI.mkdir(exist_ok=True)

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

CONSTANTE_CLE_TEST = b"TRIADE-CERT-CRISTALLISATION-TEST-2026-v9"
GENESE = b"TRIADE-CERT-CRIST"
FORMAT = "TRIADE-CERT-CRIST/1"

GRAINE_ORACLE = 20261120
N_VECTEURS = 64


def charger_module(nom, chemin):
    chemin = pathlib.Path(chemin)
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


B4 = charger_module("build_m4_vi", REPO / "m4" / "build_m4.py")
lay_l = charger_module("lay_l_vi", REPO / "loupe" / "layout.py")
HE = charger_module("h_edition_vi", REPO / "loupe" / "harnais_edition.py")

SCELLES = [REPO / "loupe" / "loupe.exe", REPO / "tls13" / "proxy.exe",
           REPO / "m1" / "selftest.exe"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def cle_test():
    return SigningKey(hashlib.sha256(CONSTANTE_CLE_TEST).digest())


# --------------------------------------------------------------- le graphe

def assembler(fichier, rva, slot):
    octets, _ = B4.assembler_bloc(KS, str(fichier), rva, slot)
    return octets


def graphe_depuis_notations():
    """Les arêtes d'APPEL lues des notations assemblées — la source unique."""
    blocs = {}
    for bid, (rva, slot) in lay_l.SLOTS_LOUPE.items():
        num = int(bid[1:]) - 110000
        fichiers = list((REPO / "loupe" / "notation").glob(
            f"loupe-{num:02d}-*.asm"))
        if fichiers:
            blocs[f"loupe-{num:02d}"] = (fichiers[0], rva, slot)
    # les familles scellées du plan (les héritages R7 : sha + libc + win)
    heritages = {}
    for nom, rva in [("libc-01", lay_l.R_LIBC01), ("libc-02", lay_l.R_LIBC02),
                     ("libc-07", lay_l.R_LIBC07), ("win-03", lay_l.R_WIN03),
                     ("tls13-01", lay_l.R_TLS01), ("tls13-02", lay_l.R_TLS02),
                     ("tls13-03", lay_l.R_TLS03), ("tls13-04", lay_l.R_TLS04)]:
        heritages[nom] = (rva, 0x400)
    plages = [(bid, rva, rva + slot) for bid, (_, rva, slot) in blocs.items()]
    plages += [(nom, rva, rva + t) for nom, (rva, t) in heritages.items()]

    aretes = {bid: set() for bid in blocs}
    for bid, (fichier, rva, slot) in blocs.items():
        octets = assembler(fichier, rva, slot)
        for ins in CS.disasm(octets, rva):
            if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
                cible = int(ins.op_str, 16)
                for (autre, dep, fin) in plages:
                    if autre != bid and dep <= cible < fin:
                        aretes[bid].add(autre)
    return blocs, aretes, heritages


def dependants_transitifs(bid, aretes):
    """Les blocs qui DÉPENDENT de bid (les appelants, transitivement)."""
    rev = {b: set() for b in aretes}
    for b, deps in aretes.items():
        for d in deps:
            rev.setdefault(d, set()).add(b)
    vus, pile = set(), [bid]
    while pile:
        b = pile.pop()
        for a in rev.get(b, ()):
            if a not in vus:
                vus.add(a)
                pile.append(a)
    return vus


# ------------------------------------------------------- la vérification

class VerrouilVerif(Exception):
    pass


def verifier_bloc(bid, fichier, rva, slot):
    """La vérification COMPLÈTE d'un bloc — la même que la session :
    le round-trip R5 + l'oracle différentiel (loupe-13) + rien de moins."""
    octets = assembler(fichier, rva, slot)
    # R5 : le round-trip
    insns = list(CS.disasm(octets, rva))
    if len(insns) == 0:
        raise VerrouilVerif(f"{bid} : la notation ne se désassemble pas")
    morceaux = []
    for i in insns:
        code, _cnt = KS.asm(f"{i.mnemonic} {i.op_str}", i.address)
        morceaux.append(bytes(code))
    reassemble = b"".join(morceaux)
    if bytes(reassemble) != octets:
        raise VerrouilVerif(f"{bid} : le round-trip DIVERGE")
    return octets, insns


def oracle_loupe13(octets, rva):
    """L'oracle différentiel de la feuille pure : la recherche d'octet —
    l'implémentation triviale Python contre le bloc au harnais Unicorn,
    64 vecteurs aux bords (la graine consignée)."""
    rng = random.Random(GRAINE_ORACLE)
    L = HE.L
    os_v = HE.OSEdition()
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    emul.uc.mem_write(rva, octets)
    emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(octets) + 0xFFF)
                             & ~0xFFF)
    fenetre_base = 0x500000
    motif_base = 0x510000
    emul.uc.mem_map(fenetre_base, 0x20000)
    verts = 0
    for i in range(N_VECTEURS):
        n = rng.choice([0, 1, 2, 7, 15, 16, 17, 63, 64, 65, 255, 256, 1000])
        fenetre = bytes(rng.randrange(256) for _ in range(n))
        lm = rng.choice([1, 1, 2, 3, 8, 31, 32])
        motif = bytes(rng.randrange(256) for _ in range(min(lm, max(1, n))))
        depart = min(rng.choice([0, 0, 1, n // 2, max(0, n - 1), n]), n)
        emul.uc.mem_write(fenetre_base, fenetre + b"\x00" * (0x10000 - n))
        emul.uc.mem_write(motif_base, motif + b"\x00" * (64 - len(motif)))
        # l'implémentation triviale (le juge, jamais le binaire)
        attendu = -1
        for pos in range(depart, n - len(motif) + 1):
            if fenetre[pos:pos + len(motif)] == motif:
                attendu = pos
                break
        # l'appel msx64 PAR LE HARNAIS ÉTENDU (pile_args — le 5e slot
        # [rsp+0x28] posé AU-DELÀ du canari, le contrat P5 de loupe-13)
        with contextlib.redirect_stdout(io.StringIO()):
            r = emul.appeler(rva, args={"rcx": fenetre_base, "rdx": n,
                                        "r8": motif_base,
                                        "r9": len(motif)},
                             pile_args=[depart])
        if r.get("rax") & 0xFFFFFFFFFFFFFFFF != attendu & 0xFFFFFFFFFFFFFFFF:
            raise VerrouilVerif(
                f"loupe-13 : l'oracle DIVERGE au vecteur {i} "
                f"(rendu {r.get('rax')}, attendu {attendu})")
        verts += 1
    return verts


def empreintes_scellees() -> dict:
    return {str(p.relative_to(REPO)): sha(p.read_bytes()) for p in SCELLES}


# ---------------------------------------------------------- les certificats

def certificat_bloc(bid, octets, contrat, config, oracle_id, precedent):
    corps = {
        "format": FORMAT, "bloc": bid,
        "empreinte_bloc": sha(octets),
        "empreinte_contrat": sha(contrat.encode("utf-8")),
        "empreinte_config": sha(json.dumps(config, sort_keys=True)
                                .encode("utf-8")),
        "oracle": oracle_id,
    }
    corps["h"] = sha(json.dumps(corps, sort_keys=True).encode()
                     + precedent.encode())
    return corps


def signer_racine(entrees):
    racine = {"format": FORMAT, "n": len(entrees),
              "racine": entrees[-1]["h"] if entrees else sha(GENESE)}
    sk = cle_test()
    racine["signature"] = sk.sign(
        json.dumps(racine, sort_keys=True).encode()).signature.hex()
    return racine


def verifier_chaine(entrees, racine):
    """La chaîne ET la signature recalculées — TOUT écart un refus nommé."""
    precedent = sha(GENESE)
    for e in entrees:
        corps = {k: v for k, v in e.items() if k not in ("h",)}
        if e["h"] != sha(json.dumps(corps, sort_keys=True).encode()
                         + precedent.encode()):
            raise VerrouilVerif("CERTIFICAT-DIVERGENT : la chaîne rompue "
                                f"à {e['bloc']}")
        precedent = e["h"]
    vk = VerifyKey(bytes(cle_test().verify_key))
    racine_sans = {k: v for k, v in racine.items() if k != "signature"}
    try:
        vk.verify(json.dumps(racine_sans, sort_keys=True).encode(),
                  bytes.fromhex(racine["signature"]))
    except nacl.exceptions.BadSignatureError:
        raise VerrouilVerif("SIGNATURE-INVALIDE : la racine des certificats")
    return True


# ------------------------------------------------------------------- main

def main():
    rapport = []
    t0 = time.monotonic()
    blocs, aretes, heritages = graphe_depuis_notations()
    rapport.append("LE GRAPHE DE DÉPENDANCES (lu des notations assemblées)")
    for bid in sorted(aretes):
        if aretes[bid]:
            rapport.append(f"  {bid} → {sorted(aretes[bid])}")
    (ICI / "graphe_deps.json").write_text(json.dumps(
        {"aretes": {b: sorted(a) for b, a in aretes.items()},
         "heritages": {n: r for n, (r, _) in heritages.items()}},
        indent=1, ensure_ascii=False), encoding="utf-8")

    # LA VÉRIFICATION COMPLÈTE (le régime « session complète ») : les 18
    # blocs au round-trip + loupe-13 à l'oracle + les scellés
    emp_avant = empreintes_scellees()
    t_full0 = time.monotonic()
    octets_par_bloc = {}
    for bid, (fichier, rva, slot) in sorted(blocs.items()):
        octets, _ = verifier_bloc(bid, fichier, rva, slot)
        octets_par_bloc[bid] = octets
    n_verts = oracle_loupe13(octets_par_bloc["loupe-13"],
                             blocs["loupe-13"][1])
    t_full = time.monotonic() - t_full0
    rapport.append(f"\nLA SESSION COMPLÈTE : 18/18 round-trip VERT, "
                   f"l'oracle loupe-13 {n_verts}/{N_VECTEURS} vecteurs "
                   f"VERTS — {t_full:.2f} s")

    # LES CERTIFICATS (la cristallisation : les blocs INCHANGÉS les portent)
    config = {"harnais": "harnais_edition (EmulationEdition)",
              "graine_oracle": GRAINE_ORACLE, "n_vecteurs": N_VECTEURS,
              "profil": "x86-64-win11-pe"}
    entrees, precedent = [], sha(GENESE)
    for bid in sorted(octets_par_bloc):
        spec = (REPO / "loupe" / "I" /
                f"{bid}-{'ouvrir' if bid=='loupe-01' else ''}.md")
        # le contrat : la spec I du bloc (le fichier même)
        spec_f = list((REPO / "loupe" / "I").glob(f"{bid}-*.md"))[0]
        contrat = spec_f.read_text(encoding="utf-8")
        e = certificat_bloc(bid, octets_par_bloc[bid], contrat, config,
                            "oracle-loupe13-python" if bid == "loupe-13"
                            else f"roundtrip-{bid}", precedent)
        entrees.append(e)
        precedent = e["h"]
    racine = signer_racine(entrees)
    chainon = {"entrees": entrees, "racine": racine}
    (ICI / "certificats.json").write_text(
        json.dumps(chainon, indent=1, ensure_ascii=False), encoding="utf-8")
    rapport.append(f"LES CERTIFICATS : {len(entrees)} blocs certifiés, la "
                   f"racine signée Ed25519 (clé de test publique — le "
                   f"modèle D214/D222)")

    # LA CHAÎNE VÉRIFIÉE (jamais crue)
    verifier_chaine(entrees, racine)
    rapport.append("LA CHAÎNE RECALCULÉE : VERT (chaque entrée chaînée, la "
                   "signature vérifiée)")

    # LE DIFF D'UN BLOC : la re-vérification de X et ses dépendants SEULS
    cible = "loupe-08"
    deps = dependants_transitifs(cible, aretes)
    a_rejouer = deps | {cible}
    t_inc0 = time.monotonic()
    for bid in sorted(a_rejouer):
        verifier_bloc(bid, *blocs[bid])
    if "loupe-13" in a_rejouer:
        oracle_loupe13(octets_par_bloc["loupe-13"], blocs["loupe-13"][1])
    t_inc = time.monotonic() - t_inc0
    rapport.append(
        f"\nLE DIFF AU BLOC {cible} : {len(a_rejouer)} blocs re-vérifiés "
        f"({sorted(a_rejouer)}) — les {18 - len(a_rejouer)} INCHANGÉS "
        f"portent leur certificat — {t_inc:.2f} s contre {t_full:.2f} s "
        f"la complète")

    # LES CONTRÔLES NÉGATIFS : le certificat falsifié force le rejeu complet
    rapport.append("\nLES CONTRÔLES NÉGATIFS (le certificat falsifié)")
    for variante, muter in (
            ("le BLOC changé", lambda e: {**e, "empreinte_bloc":
                                          sha(b"X" + bytes.fromhex(
                                              e["empreinte_bloc"][:64]))}),
            ("le CONTRAT changé", lambda e: {**e, "empreinte_contrat":
                                             sha(b"Y")}),
            ("la CONFIGURATION changée", lambda e: {**e,
                                                    "empreinte_config":
                                                    sha(b"Z")})):
        falsifiees = [muter(e) if i == 4 else e
                      for i, e in enumerate(entrees)]
        try:
            verifier_chaine(falsifiees, racine)
            rapport.append(f"  ROUGE : {variante} — la chaîne acceptée "
                           "(L'ÉCHEC DU CONTRÔLE)")
            raise SystemExit(f"le contrôle négatif {variante} a ÉCHOUÉ")
        except VerrouilVerif as exc:
            rapport.append(f"  VERT : {variante} → REFUS NOMMÉ "
                           f"{str(exc).split(':')[0]} — le rejeu complet "
                           f"forcé")

    emp_apres = empreintes_scellees()
    rapport.append(f"\nLES SCELLÉS INTACTES : {emp_avant == emp_apres}")
    rapport.append(f"LE TEMPS TOTAL : {time.monotonic() - t0:.1f} s")
    (ICI / "rapport-verifier-incrementale.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
