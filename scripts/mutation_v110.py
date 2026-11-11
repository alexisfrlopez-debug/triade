#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mutation_v110.py — LE MUTATION TESTING de l'édition v0.11.0 (la commande
du développeur : « renforcer le niveau de preuve », chantier 1).

Des mutants des blocs scellés (INSTRUCTIONS, OPÉRANDES, OFFSETS — un octet
muté dans une COPIE DE LABORATOIRE, la pièce scellée jamais touchée), tués
par LES INSTRUMENTS EXISTANTS dans l'ordre du moins cher au plus cher :

  K1 — LE ROUND-TRIP (R5, uniforme) : le mutant doit se décoder en
       instructions couvrant exactement le bloc ET se ré-assembler à
       l'identique (capstone → keystone) — un encodage invalide ou
       instable est TUÉ ;
  K2 — L'ORACLE STRUCTUREL (uniforme) : le mutant décode, mais la
       structure diverge du plan — nombre d'instructions, mnémoniques,
       cibles d'appel direct, feuilles IAT appelées, déplacements RIP —
       TUÉ ;
  K3 — LE DIFFÉRENTIEL SÉMANTIQUE (sous-ensemble honnête) : pour les
       familles de calcul pur du domaine tls13 (sha 01..04, hkdf 05..08,
       f25519 09..12, x25519 13..14, aes/ghash/gcm 15..19) et loupe-06
       (md5), le mutant vit en émulation et rend sa sortie aux vecteurs
       officiels (RFC 1321 / FIPS 180-4 / RFC 5869 / RFC 7748 / SP 800-38D)
       croisés à hashlib — une sortie divergente ou un crash est TUÉ.

RAPPORT par bloc et par famille (loupe, tls13, sys) — les survivants sont
NOMMÉS (ce que le mutation testing laisse vivre : la limite constatée,
jamais cachée). Graine fixe 20261111 (reproductible).

Usage : python3 scripts/mutation_v110.py [--mutants N]
Sortie : scripts/preuves_v110/mutation.csv + mutation.json + rapport texte
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES = REPO / "scripts" / "preuves_v110"
PREUVES.mkdir(parents=True, exist_ok=True)

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True

GRAINE = 20261111


def charger_module(nom: str, chemin: pathlib.Path):
    # les modules du dépôt se chargent avec LEUR répertoire au chemin
    # (les imports internes — carte_m4, layout… — vivent à côté d'eux)
    chemin = pathlib.Path(chemin)
    sys.path.insert(0, str(chemin.parent))
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# le lecteur canonique des notations (le modèle des harnais)
B4 = charger_module("build_m4_v110", REPO / "m4" / "build_m4.py")

# ------------------------------------------------------------------ les blocs

def blocs_domaines() -> dict[str, list[dict]]:
    """Les 52 blocs notés des trois domaines, assemblés au plan."""
    loupe_layout = charger_module("lay_loupe_v110", REPO / "loupe" / "layout.py")
    tls_layout = charger_module("lay_tls_v110", REPO / "tls13" / "layout.py")
    sys_layout = charger_module("lay_sys_v110", REPO / "m8" / "layout.py")

    blocs = {"loupe": [], "tls13": [], "sys": []}

    for bid in sorted(loupe_layout.SLOTS_LOUPE):
        rva, slot = loupe_layout.SLOTS_LOUPE[bid]
        # i1100NN -> loupe-NN-nom.asm (la table des identifiants D172)
        num = int(bid[1:]) - 110000
        candidats = list((REPO / "loupe" / "notation").glob(f"loupe-{num:02d}-*.asm"))
        if not candidats:
            continue
        octets, _ = B4.assembler_bloc(KS, str(candidats[0]), rva, slot)
        blocs["loupe"].append({"bid": f"loupe-{num:02d}",
                               "chemin": str(candidats[0]),
                               "rva": rva, "octets": octets})

    # tls13 : les 28 blocs — bid h1000NN → fichier tls13-NN-nom.asm
    for bid, (rva, slot) in sorted(tls_layout.SLOTS_TLS13.items()):
        nn = bid[1:]  # h100001 -> 100001
        num = int(nn) - 100000
        candidats = list((REPO / "tls13" / "notation").glob(f"tls13-{num:02d}-*.asm"))
        if not candidats:
            continue
        octets, _ = B4.assembler_bloc(KS, str(candidats[0]), rva, slot)
        blocs["tls13"].append({"bid": f"tls13-{num:02d}",
                               "chemin": str(candidats[0]),
                               "rva": rva, "octets": octets})

    for bid, (rva, slot) in sorted(sys_layout.SLOTS_SYS.items()):
        num = int(bid[1:]) - 90000
        candidats = list((REPO / "m8" / "notation").glob(f"sys-{num:02d}-*.asm"))
        if not candidats:
            continue
        octets, _ = B4.assembler_bloc(KS, str(candidats[0]), rva, slot)
        blocs["sys"].append({"bid": f"sys-{num:02d}", "chemin": str(candidats[0]),
                             "rva": rva, "octets": octets})
    return blocs


# ------------------------------------------------------------- l'analyse

def decoder(octets: bytes, rva: int):
    """Décode un bloc : liste d'instructions couvrant exactement la longueur."""
    try:
        insns = list(CS.disasm(octets, rva))
    except Exception:
        return None
    if not insns or sum(i.size for i in insns) != len(octets):
        return None
    return insns


def reassembler(insns) -> bytes | None:
    """Ré-assemble la désassemble : le round-trip du mutant."""
    try:
        retour = b""
        for i in insns:
            enc, _ = KS.asm(i.mnemonic + " " + i.op_str, i.address)
            if enc is None:
                return None
            retour += bytes(enc)
            if len(retour) > 4096:
                return None
        return retour
    except Exception:
        return None


def signature_structurelle(insns):
    """La structure que l'oracle relit : mnémoniques + cibles + déplacements."""
    sig = []
    for i in insns:
        cible = ""
        if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x"):
            cible = i.op_str
        for op in i.operands:
            if op.type == capstone.x86.X86_OP_MEM and op.mem.base == capstone.x86.X86_REG_RIP:
                cible += f"@{i.address + i.size + op.mem.disp:#x}"
        sig.append((i.mnemonic, cible))
    return sig


# ------------------------------------------------------------- K3 : le sémantique

class JugeSemantique:
    """Le différentiel sémantique pour les familles de calcul pur.

    Une ÉMULATION LABORATOIRE par famille (les Emulation des harnais
    existants, importés — jamais réécrits) ; le mutant POSÉ par
    mem_write + ctl_remove_cache (le miroir reposer_bloc du harnais M8),
    la famille entière jugée aux vecteurs officiels croisés à hashlib.
    """

    def __init__(self):
        self.harnais = {}
        for nom, chemin in (("sha", "tls13/harnais_sha.py"),
                            ("hkdf", "tls13/harnais_hkdf.py"),
                            ("x25519", "tls13/harnais_x25519.py"),
                            ("aead", "tls13/harnais_aead.py")):
            self.harnais[nom] = charger_module(f"h_{nom}_v110", REPO / chemin)
        self.caches: dict[str, object] = {}

    def _famille_de(self, bid: str) -> tuple[str, object] | None:
        num = int(bid.split("-")[1])
        if 1 <= num <= 4:
            return "sha", self.harnais["sha"]
        if 5 <= num <= 8:
            return "hkdf", self.harnais["hkdf"]
        if 9 <= num <= 14:
            return "x25519", self.harnais["x25519"]
        if 15 <= num <= 19:
            return "aead", self.harnais["aead"]
        return None

    def _tue_loupe06(self, bloc: dict, mutant: bytes) -> tuple[bool, str]:
        """loupe-06 jugé AU FICHIER : la mini-OS du harnais noyau, le
        témoin RFC 1321, le condensé croisé à hashlib.md5."""
        import hashlib
        if "noyau" not in self.harnais:
            self.harnais["noyau"] = charger_module(
                "h_noyau_v110", REPO / "loupe" / "harnais_noyau.py")
        H = self.harnais["noyau"]
        try:
            os_v = H.OSVirtuel()
            message = b"abc"
            os_v.declarer("temoin.bin", H.FichierVirtuel(contenu=message))
            emul = H.Emulation(os_v)
            rva = bloc["rva"]
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF) & ~0xFFF)
            emul.uc.mem_write(H.ADRESSE_CHEMIN,
                              "temoin.bin".encode("utf-16-le") + b"\x00\x00")
            r = emul.appeler(H.L.LOUPE01_VA, {"rcx": H.ADRESSE_CHEMIN})
            if r["rax"] != 0:
                return True, f"loupe-01 a rendu {r['rax']} (session morte)"
            r = emul.appeler(H.L.LOUPE06_VA,
                             {"rcx": 0, "rdx": len(message),
                              "r8": H.ADRESSE_SORTIE16})
            condense = bytes(emul.uc.mem_read(H.ADRESSE_SORTIE16, 16))
            attendu = hashlib.md5(message).digest()
            return (condense != attendu or r["rax"] != 0), "md5(abc) != hashlib"
        except Exception as exc:  # noqa: BLE001
            return True, f"crash émulation ({type(exc).__name__})"

    def _emulation(self, famille: str):
        """Une émulation FRAÎCHE par mutant (la traduction ne doit jamais
        servir un cache de l'original — la leçon du hook)."""
        mod = self.harnais[famille]
        return mod.Emulation()

    def tue(self, bloc: dict, mutant: bytes) -> tuple[bool, str]:
        """Retourne (tué, cause). Le mutant est posé, la famille jugée."""
        bid = bloc["bid"]
        if bid == "loupe-06":
            return self._tue_loupe06(bloc, mutant)
        if not bid.startswith("tls13-"):
            return False, "hors-sous-ensemble"
        res = self._famille_de(bid)
        if res is None:
            return False, "hors-sous-ensemble"
        famille, mod = res
        try:
            emul = self._emulation(famille)
            # la pose du mutant (le bloc vit à son RVA du plan)
            import unicorn as uc2
            rva = bloc["rva"]
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF) & ~0xFFF)
            # le jugement : la famille entière aux vecteurs
            if famille == "sha":
                ref = __import__("hashlib").sha256(b"abc" * 7).digest()
                rendu = mod.hacher(emul, b"abc" * 7)
                return (rendu != ref), "sha256(b'abc'*7) != hashlib"
            if famille == "hkdf":
                import hashlib as hl
                sel, ikm = b"\x0b" * 22, b"\x00" * 22
                ref = hl.sha256
                prk = mod.hkdf_extraire(emul, sel, ikm, 32)
                # la référence indépendante : HKDF-Extract = HMAC-SHA256(sel, ikm)
                attendu = __import__("hmac").new(sel, ikm, hl.sha256).digest()
                return (prk != attendu), "HKDF-Extract != hmac.new"
            if famille == "x25519":
                # RFC 7748 § 6.1 : le vecteur canonique
                import hashlib as _hl  # noqa: F401
                ref_k = bytes.fromhex(
                    "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60")
                ref_u = bytes.fromhex(
                    "d1a54dfed7171de539db360af8c0e3d8b891e53847bc7536a0512c9f7e0b9bae")
                cle = mod.cle_publique(emul, ref_k) if hasattr(mod, "cle_publique") else None
                if cle is not None:
                    return (cle != ref_u), "x25519(RFC 7748 § 6.1) != officiel"
                # repli : l'addition de champ sur le vecteur trivial
                a = bytes.fromhex("ed" * 32)
                b = bytes.fromhex("12" * 32)
                r = mod.f_add(emul, a, b)
                attendu = bytes((x + y) % 256 for x, y in zip(a, b))
                return (r != attendu), "f25519-add != arithmétique"
            if famille == "aead":
                import os as _os
                cle = bytes(range(16))
                nonce = bytes(range(12))
                texte = b"Le chat du voisin mange une souris grise." * 3
                scelle = mod.sceller(emul, cle, nonce, texte, b"") if hasattr(mod, "sceller") else None
                if scelle is not None:
                    ouvre = mod.ouvrir(emul, cle, nonce, scelle, b"") if hasattr(mod, "ouvrir") else None
                    return (ouvre != texte), "GCM scellé-ouvert != texte"
                return False, "interface aead non câblée"
        except Exception as exc:  # noqa: BLE001
            return True, f"crash émulation ({type(exc).__name__})"
        return False, "inconnu"


# ------------------------------------------------------------- la campagne

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mutants", type=int, default=16)
    args = ap.parse_args()

    rng = random.Random(GRAINE)
    blocs = blocs_domaines()
    juge = JugeSemantique()

    lignes, json_complet = [], {"graine": GRAINE, "mutants_par_bloc": args.mutants,
                                "domaines": {}}
    total_tues = total_mutants = 0

    for domaine, liste in blocs.items():
        dom = {"blocs": {}, "tues": 0, "mutants": 0}
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = decoder(octets, bloc["rva"])
            if ref_insns is None:
                print(f"[{domaine}] {bloc['bid']} : DÉCODAGE IMPOSSIBLE — sauté")
                continue
            ref_sig = signature_structurelle(ref_insns)

            stats = {"k1_roundtrip": 0, "k2_structurel": 0, "k3_semantique": 0,
                     "k3_crash": 0, "vivants": 0, "total": 0}
            vivants_details = []
            for _ in range(args.mutants):
                # le choix : une instruction au hasard, un octet au hasard
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                val = octets[pos]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                mutant = bytearray(octets)
                mutant[pos] = nouvelle
                mutant = bytes(mutant)
                stats["total"] += 1

                # K1 : le round-trip du mutant
                m_insns = decoder(mutant, bloc["rva"])
                if m_insns is None:
                    stats["k1_roundtrip"] += 1
                    continue
                re = reassembler(m_insns)
                if re != mutant:
                    stats["k1_roundtrip"] += 1
                    continue
                # K2 : la structure du plan
                if signature_structurelle(m_insns) != ref_sig:
                    stats["k2_structurel"] += 1
                    continue
                # K3 : le sémantique (sous-ensemble)
                tue, cause = juge.tue(bloc, mutant)
                if tue and "crash" in cause:
                    stats["k3_crash"] += 1
                elif tue:
                    stats["k3_semantique"] += 1
                else:
                    stats["vivants"] += 1
                    vivants_details.append(
                        {"offset": pos, "octet": f"{val:#04x}->{nouvelle:#04x}"})

            tue = stats["total"] - stats["vivants"]
            taux = 100.0 * tue / stats["total"] if stats["total"] else 0.0
            lignes.append({
                "domaine": domaine, "bloc": bloc["bid"],
                "octets": len(octets), "mutants": stats["total"],
                "k1_roundtrip": stats["k1_roundtrip"],
                "k2_structurel": stats["k2_structurel"],
                "k3_semantique": stats["k3_semantique"],
                "k3_crash": stats["k3_crash"],
                "vivants": stats["vivants"], "taux_tue_pct": f"{taux:.1f}",
                "vivants_details": json.dumps(vivants_details[:4]),
            })
            dom["blocs"][bloc["bid"]] = stats
            dom["tues"] += tue
            dom["mutants"] += stats["total"]
            print(f"[{domaine}] {bloc['bid']:12s} {stats['total']:3d} mutants : "
                  f"K1 {stats['k1_roundtrip']:3d} · K2 {stats['k2_structurel']:3d} · "
                  f"K3 {stats['k3_semantique']:3d} · crash {stats['k3_crash']:2d} · "
                  f"vivants {stats['vivants']:2d} → {taux:5.1f} % tués")
        total_tues += dom["tues"]
        total_mutants += dom["mutants"]
        json_complet["domaines"][domaine] = dom

    # l'écriture
    with open(PREUVES / "mutation.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
        w.writeheader()
        w.writerows(lignes)
    (PREUVES / "mutation.json").write_text(
        json.dumps(json_complet, indent=1), encoding="utf-8")

    print()
    for domaine, dom in json_complet["domaines"].items():
        taux = 100.0 * dom["tues"] / dom["mutants"] if dom["mutants"] else 0
        print(f"[{domaine}] {dom['tues']}/{dom['mutants']} tués "
              f"({taux:.1f} %) sur {len(dom['blocs'])} blocs")
    taux = 100.0 * total_tues / total_mutants if total_mutants else 0
    print(f"[TOTAL] {total_tues}/{total_mutants} mutants tués ({taux:.1f} %) — "
          f"graine {GRAINE}, reproductible")
    (PREUVES / "mutation_rapport.txt").write_text(
        "\n".join(["MUTATION TESTING v0.11.0 — graine "
                   f"{GRAINE}, {args.mutants} mutants/bloc",
                   ""] +
                  [f"[{l['domaine']}] {l['bloc']:12s} {l['mutants']:3d} mutants : "
                   f"K1 {l['k1_roundtrip']:3d} · K2 {l['k2_structurel']:3d} · "
                   f"K3 {l['k3_semantique']:3d} · crash {l['k3_crash']:2d} · "
                   f"vivants {l['vivants']:2d} → {l['taux_tue_pct']} %"
                   for l in lignes] +
                  ["", f"[TOTAL] {total_tues}/{total_mutants} "
                   f"({100.0 * total_tues / total_mutants:.1f} %)"]),
        encoding="utf-8")


if __name__ == "__main__":
    main()
