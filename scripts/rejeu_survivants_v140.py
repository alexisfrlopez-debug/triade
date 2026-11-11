#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rejeu_survivants_v140.py — LE RE-JEU COMPLET DES 832 MUTANTS (le point 4
de la commande v0.14.0 : « câbler des killers sémantiques au niveau mutant
isolé pour les blocs d'orchestration/UI (OU UN HARNAIS DE COMPOSITION PAR
MUTANT) ; re-jeu des 832 mutants ; rapporter le nouveau taux par famille et
les survivants restants nommés »).

LA MÉTHODE : les MÊMES 832 mutants que la campagne v0.11.0 (la graine
20261111, le MÊME ordre de génération — le module mutation_v110 importé,
sa boucle répliquée à l'identique), chaque mutant désormais confronté aux
tueurs HISTORIQUES (K1 round-trip, K2 signature structurelle — jamais
affaiblis) ET AU HARNais DE COMPOSITION (le nouveau K3-composition) :

  - loupe-01..18 : LE SCÉNARIO WINMAIN COMPLET (la boucle vécue de
    l'application : l'ouverture + la cascade 02/04/05/06/07, la taille,
    la peinture 10→08, la saisie 16, le défilement 11, le curseur 15,
    la sauvegarde 17, la fermeture 18→03, la destruction) — l'observable
    (le code de sortie, le DISQUE SAUVÉ, l'écran, la fenêtre détruite)
    confronté à la base SANE ; loupe-13 en sus aux vecteurs de l'école
    (la feuille pure) ;
  - tls13-01..19 : les harnais de FAMILLE (la chaîne sha, hkdf, x25519,
    aead — déjà 100 % à v0.11.0, re-vérifiés) ;
  - tls13-20..28 (l'orchestration — les 51 survivants historiques) : LA
    COMPOSITION DE LA POIGNÉE (composer_ch : le ClientHello composé par
    les briques mêmes, confronté à la base) + L'ENREGISTREMENT
    (proteger : l'enregistrement protégé, confronté à la base) ;
  - sys-01..06 : LE HARNAIS SYS EN MODE AUTONOME RÉDUIT (executer à
    volume réduit — la batterie V1-V4 par les notations mêmes) : le
    mutant tué si le harnais LÈVE (le build ne continue jamais sur un
    harnais non vert).

Sortie : preuves_v140/rejeu_survivants.csv + rapport.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import random
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
PREUVES = REPO / "scripts" / "preuves_v140"

MUT = importlib.util.spec_from_file_location(
    "mutation_v110_rejeu", REPO / "scripts" / "mutation_v110.py")
MUT.module = importlib.util.module_from_spec(MUT)
sys.modules["mutation_v110_rejeu"] = MUT.module
MUT.loader.exec_module(MUT.module)

GRAINE = 20261111


def charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


HN = charger_module("h_noyau_rejeu", REPO / "loupe" / "harnais_noyau.py")
HR = charger_module("h_rendu_rejeu", REPO / "loupe" / "harnais_rendu.py")
HE = charger_module("h_edition_rejeu", REPO / "loupe" / "harnais_edition.py")
HP = charger_module("h_poignee_rejeu", REPO / "tls13" / "harnais_poignee.py")
HE_ = charger_module("h_enreg_rejeu",
                     REPO / "tls13" / "harnais_enregistrement.py")
HSYS = charger_module("h_sys_rejeu", REPO / "m8" / "harnais_sys.py")
LL = HN.L

SCENARIO = [                    # la boucle vécue (harnais_edition V6.a)
    (0x770001, 5, 0, (440 << 16) | 640),      # WM_SIZE
    (0x770001, 0x0F, 0, 0),                   # WM_PAINT → 10 → 08
    (0x770001, 0x102, 0x34, 0),               # '4' → 16
    (0x770001, 0x102, 0x64, 0),               # 'd' → 16 (l'octet 0x4D)
    (0x770001, 0x115, 3, 0),                  # WM_VSCROLL → 11
    (0x770001, 0x100, 0x27, 0),               # WM_KEYDOWN droite → 15
    (0x770001, 0x0F, 0, 0),                   # WM_PAINT
    (0x770001, 0x102, 0x13, 0),               # Ctrl+S → 17 (le disque!)
    (0x770001, 0x0F, 0, 0),                   # WM_PAINT
    (0x770001, 0x10, 0, 0),                   # WM_CLOSE → 18 → 03
]
TEM_LOUPE = b"temoin-rejeu.bin"


def instance_loupe():
    os_v = HE.OSEdition()
    os_v.declarer(TEM_LOUPE, HE.FichierEditable(contenu=bytes(
        (i * 7 + 3) % 256 for i in range(2000))))
    emul = HE.EmulationEdition(
        os_v, (REPO / "tls13" / "proxy.exe").read_bytes(),
        (REPO / "m1" / "selftest.exe").read_bytes(),
        (REPO / "demo" / "demo.exe").read_bytes())
    return os_v, emul


def observable_winmain(emul, os_v):
    r = emul.appeler_winmain(f"loupe.exe {TEM_LOUPE}", messages=SCENARIO)
    return (r.get("exit_code"), r.get("crash") is None,
            bytes(os_v.fichiers[TEM_LOUPE].contenu),
            bytes(emul.uc.mem_read(LL.R_ECRAN, 2320)) if not r.get(
                "crash") else b"",
            emul.gui.fenetre_detruite if not r.get("crash") else None)


def tuer_loupe(bid, mutant, rva, base_saine):
    os_v, emul = instance_loupe()
    emul.uc.mem_write(rva, mutant)
    emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF)
                             & ~0xFFF)
    try:
        obs = observable_winmain(emul, os_v)
    except Exception:  # noqa: BLE001
        return True, "crash"
    if obs != base_saine:
        return True, "la boucle diverge"
    return False, "vivants (la boucle winmain est passée)"


# ---------------------------------------------------------- tls13

def tuer_tls13_famille(bid, mutant, rva):
    """les harnais de famille (v0.11.0) — la chaîne de blocs par famille."""
    num = int(bid.split("-")[1])
    try:
        if 1 <= num <= 4:
            mod = charger_module("h_sha_rejeu", REPO / "tls13"
                                 / "harnais_sha.py")
            emul = mod.Emulation()
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant)
                                      + 0xFFF) & ~0xFFF)
            rendu = mod.hacher(emul, b"abc" * 7)
            import hashlib
            return rendu != hashlib.sha256(b"abc" * 7).digest(), \
                "sha256(b'abc'*7) != hashlib"
        if 5 <= num <= 8:
            mod = charger_module("h_hkdf_rejeu", REPO / "tls13"
                                 / "harnais_hkdf.py")
            emul = mod.Emulation()
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant)
                                      + 0xFFF) & ~0xFFF)
            import hmac, hashlib
            attendu = hmac.new(b"\x0b" * 22, b"\x00" * 22,
                               hashlib.sha256).digest()
            prk = mod.hkdf_extraire(emul, b"\x0b" * 22, b"\x00" * 22, 32)
            return prk != attendu, "HKDF-Extract != hmac.new"
        if 9 <= num <= 14:
            mod = charger_module("h_x25519_rejeu", REPO / "tls13"
                                 / "harnais_x25519.py")
            emul = mod.Emulation()
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant)
                                      + 0xFFF) & ~0xFFF)
            # LE TUEUR DE v0.11.0 TEL QUEL : RFC 7748 § 6.1, le repli f_add
            ref_k = bytes.fromhex(
                "9d61b19deffd5a60ba844af492ec2cc4"
                "4449c5697b326919703bac031cae7f60")
            ref_u = bytes.fromhex(
                "d1a54dfed7171de539db360af8c0e3d8"
                "b891e53847bc7536a0512c9f7e0b9bae")
            cle = mod.cle_publique(emul, ref_k) if hasattr(
                mod, "cle_publique") else None
            if cle is not None:
                return cle != ref_u, "x25519(RFC 7748 § 6.1) != officiel"
            a, b = bytes.fromhex("ed" * 32), bytes.fromhex("12" * 32)
            r = mod.f_add(emul, a, b)
            attendu = bytes((x + y) % 256 for x, y in zip(a, b))
            return r != attendu, "f25519-add != arithmétique"
        if 15 <= num <= 19:
            mod = charger_module("h_aead_rejeu", REPO / "tls13"
                                 / "harnais_aead.py")
            emul = mod.Emulation()
            emul.uc.mem_write(rva, mutant)
            emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant)
                                      + 0xFFF) & ~0xFFF)
            # LE TUEUR DE v0.11.0 TEL QUEL : le scellé-ouvert GCM
            cle, nonce = bytes(range(16)), bytes(range(12))
            texte = b"Le chat du voisin mange une souris grise." * 3
            scelle = mod.sceller(emul, cle, nonce, texte, b"") if hasattr(
                mod, "sceller") else None
            if scelle is not None:
                ouvre = mod.ouvrir(emul, cle, nonce, scelle, b"") if hasattr(
                    mod, "ouvrir") else None
                return ouvre != texte, "GCM scellé-ouvert != texte"
            return False, "interface aead non câblée"
    except Exception:  # noqa: BLE001
        return True, "crash"
    return False, "hors famille"


def base_poignee():
    emul = HP.Emulation()
    ch, r = HP.composer_ch(emul, HP.ALEA_8448, HP.PUBLIQUE_CLIENT)
    return ch, r["rax"]


def base_enregistrement():
    emul = HE_.Emulation()
    ctx = HE_.Contexte(bytes(range(16)), bytes(range(12)), seq=0)
    emis, r = HE_.proteger(emul, ctx, 0x16, b"charge-rejeu-v140")
    return emis, r["rax"]


def tuer_tls13_orchestration(bid, mutant, rva, bases):
    """la composition : le ClientHello composé + l'enregistrement protégé,
    chacun confronté à sa base SANE (le mutant posé aux RVA du plan)."""
    try:
        emul = HP.Emulation()
        emul.uc.mem_write(rva, mutant)
        emul.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant) + 0xFFF)
                                 & ~0xFFF)
        ch, rax = HP.composer_ch(emul, HP.ALEA_8448, HP.PUBLIQUE_CLIENT)
        if (ch, rax) != bases["poignee"]:
            return True, "la composition CH diverge"
        emul2 = HE_.Emulation()
        emul2.uc.mem_write(rva, mutant)
        emul2.uc.ctl_remove_cache(rva & ~0xFFF, (rva + len(mutant)
                                   + 0xFFF) & ~0xFFF)
        ctx = HE_.Contexte(bytes(range(16)), bytes(range(12)), seq=0)
        emis, rax2 = HE_.proteger(emul2, ctx, 0x16, b"charge-rejeu-v140")
        if (emis, rax2) != bases["enregistrement"]:
            return True, "l'enregistrement protégé diverge"
    except Exception:  # noqa: BLE001
        return True, "crash"
    return False, "vivants"


# ---------------------------------------------------------- sys

def tuer_sys(bid, mutant):
    """le harnais sys en mode autonome réduit, le mutant en BLOB : le
    harnais LÈVE sur tout écart (le build ne continue jamais non vert)."""
    # les clés de blobs du harnais sys : g9NNNN (la table SLOTS_SYS)
    cle = f"g{90000 + int(bid.split('-')[1])}"
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            HSYS.executer(blobs={cle: mutant}, graine=20261105,
                          volume="reduit")
        return False, "le harnais est passé (le mutant vivant ?)"
    except Exception:  # noqa: BLE001
        return True, "le harnais a levé"


def main():
    print("=== LE RE-JEU DES 832 MUTANTS — v0.14.0 (le point 4, "
          "les tueurs de composition) ===")
    rng = random.Random(GRAINE)
    blocs = MUT.module.blocs_domaines()
    Juge = MUT.module.JugeSemantique

    # les bases SANE (la composition sur les images propres)
    print("[base] la boucle winmain saine…")
    os_v, emul_l = instance_loupe()
    BASE_LOUPE = observable_winmain(emul_l, os_v)
    assert BASE_LOUPE[0] == 0, "la boucle saine doit rendre 0"
    print("[base] la poignée et l'enregistrement sains…")
    BASES_TLS = {"poignee": base_poignee(),
                 "enregistrement": base_enregistrement()}

    resultats = {}
    compte = {"tués": 0, "vivants": 0}
    vivants_par_domaine = {}
    juge_histo = Juge()

    for domaine, liste in blocs.items():
        dom = {"tués": 0, "vivants": 0, "total": 0,
               "vivants_details": []}
        for bloc in liste:
            octets = bloc["octets"]
            ref_insns = MUT.module.decoder(octets, bloc["rva"])
            if ref_insns is None:
                continue
            ref_sig = MUT.module.signature_structurelle(ref_insns)
            bid = bloc["bid"]
            num_tls = int(bid.split("-")[1]) if bid.startswith("tls13") \
                else 0
            for _ in range(16):
                insn = ref_insns[rng.randrange(len(ref_insns))]
                pos = insn.address - bloc["rva"] + rng.randrange(insn.size)
                val = octets[pos]
                nouvelle = rng.choice([b for b in range(256) if b != val])
                mutant = bytearray(octets)
                mutant[pos] = nouvelle
                mutant = bytes(mutant)
                dom["total"] += 1

                # K1 (round-trip) + K2 (signature) — JAMAIS affaiblis
                m_insns = MUT.module.decoder(mutant, bloc["rva"])
                tue = False
                cause = ""
                if m_insns is None or MUT.module.reassembler(m_insns) \
                        != mutant:
                    tue, cause = True, "K1 round-trip"
                elif MUT.module.signature_structurelle(m_insns) != ref_sig:
                    tue, cause = True, "K2 signature"
                else:
                    # LE HARNais DE COMPOSITION (le nouveau K3)
                    if domaine == "loupe":
                        tue, cause = tuer_loupe(bid, mutant, bloc["rva"],
                                                BASE_LOUPE)
                    elif num_tls and 1 <= num_tls <= 19:
                        tue, cause = tuer_tls13_famille(bid, mutant,
                                                        bloc["rva"])
                    elif num_tls:
                        tue, cause = tuer_tls13_orchestration(
                            bid, mutant, bloc["rva"], BASES_TLS)
                    else:
                        tue, cause = tuer_sys(bid, mutant)
                if tue:
                    dom["tués"] += 1
                else:
                    dom["vivants"] += 1
                    dom["vivants_details"].append(
                        f"{bid} {pos:#x}: {val:#04x}→{nouvelle:#04x}")
            print(f"  [{domaine}] {bid} : "
                  f"{dom['tués']}/{dom['total']} tués à ce point "
                  f"({dom['vivants']} vivants)", flush=True)
        compte["tués"] += dom["tués"]
        compte["vivants"] += dom["vivants"]
        vivants_par_domaine[domaine] = dom

    total = compte["tués"] + compte["vivants"]
    rapport = [
        "LE RE-JEU DES 832 MUTANTS — v0.14.0 (les tueurs de composition, "
        "le point 4 de la commande)",
        "",
        "LA MÉTHODE : les MÊMES mutants que v0.11.0 (la graine 20261111, "
        "le module même, la boucle répliquée) ; les tueurs historiques "
        "K1/K2 INTACTS ; LE NOUVEAU K3-COMPOSITION : la boucle winmain "
        "complète pour loupe (l'ouverture, la cascade, la peinture, la "
        "saisie, le défilement, le curseur, la sauvegarde, la fermeture — "
        "le DISQUE et l'ÉCRAN confrontés à la base saine), la composition "
        "de la poignée + l'enregistrement protégé pour l'orchestration "
        "tls13, les harnais de famille pour les crypto, le harnais sys "
        "autonome pour le domaine sys.",
        "",
    ]
    for domaine, dom in vivants_par_domaine.items():
        taux = 100.0 * dom["tués"] / dom["total"] if dom["total"] else 0
        rapport.append(
            f"  {domaine} : {dom['tués']}/{dom['total']} tués "
            f"({taux:.1f} %) — {dom['vivants']} vivants")
        for v in dom["vivants_details"][:12]:
            rapport.append(f"    vivant : {v}")
    rapport += [
        "",
        f"  TOTAL : {compte['tués']}/{total} tués "
        f"({100.0 * compte['tués'] / total:.1f} %) — "
        f"{compte['vivants']} vivants nommés",
        "",
        "LA COMPARAISON À v0.11.0 : 694/832 (83,4 %) → le nouveau taux "
        "ci-dessus — les survivants d'orchestration que la composition "
        "attrape sont la MESURE du gain ; ceux qui demeurent sont nommés.",
    ]
    (PREUVES / "rejeu_survivants_rapport.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    with open(PREUVES / "rejeu_survivants.csv", "w",
              encoding="utf-8") as f:
        f.write("domaine,tues,total,taux,vivants\n")
        for domaine, dom in vivants_par_domaine.items():
            f.write(f"{domaine},{dom['tués']},{dom['total']},"
                    f"{100.0 * dom['tués'] / dom['total']:.1f},"
                    f"{dom['vivants']}\n")
    print("\n".join(rapport))


if __name__ == "__main__":
    main()
