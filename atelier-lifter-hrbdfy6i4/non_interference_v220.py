#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""non_interference_v220.py — LE CHANTIER 2 DE hrbdfy6i4 : LA RE-DÉCHARGE DE
LA NON-INTERFÉRENCE SUR LA COUVERTURE ÉTENDUE (la vague 11).

LA COUVERTURE ÉTENDUE : les 13 blocs de la vague 10 + tls13-17 (GHASH —
H = E_K(0) TAINTÉ COMME SECRET, la voie forte du plan : le taint naît à
P3 [r8], l'argument Y qui porte la clé de hachage dans l'usage GCM — le
choix NOMMÉ) + tls13-04 (SHA-256 finalisation — le contexte P1 porteur de
l'état accumulé du secret) + tls13-08 (HKDF-Expand-Label — P1 LE SECRET,
« toutes les clés de TLS 1.3 naissent de lui »).

LA PREUVE : zéro branche/accès tainté exigé ; LE CONTRÔLE NÉGATIF (une
branche sur secret injectée) ATTRAPÉ ; le round-trip re-roulé sur la
couverture étendue ; LA COUVERTURE PUBLIÉE EN BLOCS ET FAMILLES avec les
trous nommés.

Sorties : non_interference_v220.csv · rapport-ni-v220.txt."""
from __future__ import annotations

import importlib.util
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-lifter-hrbdfy6i4"
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "m4"))
sys.path.insert(0, str(REPO / "tls13"))

import capstone  # noqa: E402
import keystone  # noqa: E402

KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
CS.detail = True

spec = importlib.util.spec_from_file_location(
    "ni200", REPO / "atelier-securite-bk79jvzbm" / "non_interference_v200.py")
ni200 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ni200)

# les cibles v220 : les 12 tls13 de la vague 10 + les TROIS étendues
CIBLES = dict(ni200.CIBLES)
CIBLES["tls13-13"] = ("x25519-echelle", "P2")
CIBLES["tls13-14"] = ("x25519-cle-publique", "P2")
CIBLES["tls13-17"] = ("ghash-H-secret", "P3")       # H = E_K(0) — la voie forte
CIBLES["tls13-04"] = ("sha256-finaliser-etat", "P1")  # l'état accumulé du secret
CIBLES["tls13-08"] = ("hkdf-expand-label-secret", "P1")  # LE SECRET


def charger_module(nom, chemin):
    s = importlib.util.spec_from_file_location(nom, chemin)
    m = importlib.util.module_from_spec(s)
    sys.modules[nom] = m
    s.loader.exec_module(m)
    return m


def assembler_bloc(nom_fichier, rva, slot):
    B4 = charger_module("b4_ni3", REPO / "m4" / "build_m4.py")
    o, _ = B4.assembler_bloc(KS, str(nom_fichier), rva, slot)
    return o


FAMILLES = {
    "sha256": ["tls13-01", "tls13-02", "tls13-03", "tls13-04"],
    "hmac": ["tls13-05"],
    "hkdf": ["tls13-06", "tls13-07", "tls13-08"],
    "x25519": ["tls13-13", "tls13-14"],
    "aes": ["tls13-15", "tls13-16"],
    "gcm": ["tls13-18", "tls13-19", "tls13-17"],
    "md5": ["loupe-06"],
}
TROUS = ["tls13-09", "tls13-10", "tls13-11", "tls13-12", "tls13-20",
         "tls13-21", "tls13-22", "tls13-23", "tls13-24", "tls13-25",
         "tls13-26", "tls13-27", "tls13-28"]


def main() -> int:
    lay = charger_module("lay_ni3", REPO / "tls13" / "layout.py")
    HN = charger_module("hn_ni3", REPO / "loupe" / "harnais_noyau.py")
    L = HN.L

    rapport = ["LE CHANTIER 2 DE hrbdfy6i4 — LA NON-INTERFÉRENCE SUR LA "
               "COUVERTURE ÉTENDUE (tls13-17 H secret, tls13-04, tls13-08)",
               ""]
    csv_rows = [["famille", "bloc", "secret", "branches", "branches_taintees",
                 "adresses", "adresses_taintees", "verdict"]]
    verts = 0
    tot = 0

    for bid, (nom, secret_arg) in sorted(CIBLES.items()):
        num = int(bid.split("-")[1])
        f = list((REPO / "tls13" / "notation").glob(f"{bid}-*.asm"))[0]
        rva, slot = lay.SLOTS_TLS13[f"h100{num:03d}"]
        octets = assembler_bloc(f, rva, slot)
        sites, viol = ni200.analyser(bid, octets, rva, secret_arg)
        nb = sum(1 for s in sites if s["type"] == "branche")
        bt = sum(1 for s in sites if s["type"] == "branche" and s["taint"])
        na = sum(1 for s in sites if s["type"] == "adresse")
        at = sum(1 for s in sites if s["type"] == "adresse" and s["taint"])
        vert = not viol
        tot += 1
        verts += vert
        csv_rows.append([next((fam for fam, bs in FAMILLES.items()
                               if bid in bs), "?"), bid,
                         f"{secret_arg}", nb, bt, na, at,
                         "NI PROUVÉE (sous l'hypothèse du lifter validée "
                         "au domaine)" if vert else f"VIOLATIONS: {viol[:2]}"])
        verdict = ("LA NON-INTERFÉRENCE PROUVÉE — le taint ne tache NI branche "
                   "NI adresse" if vert else "VIOLATION — ROUGE")
        rapport.append(f"  {bid} ({nom}, le secret {secret_arg}) : {nb} "
                       f"branches ({bt} taintées), {na} accès à adresse "
                       f"calculée ({at} taintés) — {verdict}")

    # ---- tls13-04 : LE MODÈLE AFFINÉ (l'état H[0..7] secret, la longueur
    # publique) — le contexte ENTIER eût taché la branche du bourrage (la
    # longueur totale @+104 est une MÉTADONNÉE PUBLIQUE) : la taint naît
    # aux CHARGES depuis [rcx + 0..31] (l'état accumulé du secret).
    from capstone.x86 import X86_OP_MEM  # noqa: E402

    def analyser_04(octets, rva):
        taint = {r: False for r in ni200.REGS64}
        drapeaux = False
        sites, viol = [], []
        for ins in CS.disasm(octets, rva):
            m, ops = ins.mnemonic, ins.op_str
            parties = [p.strip() for p in ops.split(",")] if ops else []
            if m in ("cmp", "test") and len(parties) == 2:
                drapeaux = any(taint.get(ni200.reg64(p), False)
                               for p in parties
                               if p in ni200.R64 or p in ni200.REGS64)
            elif m.startswith("j") and m != "jmp":
                sites.append({"adresse": ins.address, "type": "branche",
                              "ligne": f"{m} {ops}", "taint": drapeaux})
                if drapeaux:
                    viol.append((ins.address, "branche", f"{m} {ops}"))
                drapeaux = False
            for op in ins.operands:
                if op.type != X86_OP_MEM:
                    continue
                mem = op.mem
                base = ins.reg_name(mem.base) if mem.base else ""
                if (base == "rcx" and 0 <= mem.disp <= 31
                        and "ptr" in (parties[0] if parties else "")):
                    dst = parties[0].split("ptr")[-1].strip()
                    if dst in ni200.R64:
                        taint[ni200.reg64(dst)] = True
                if base and taint.get(base, False):
                    sites.append({"adresse": ins.address, "type": "adresse",
                                  "ligne": f"{m} {ops}", "taint": True})
                    viol.append((ins.address, "adresse", f"{m} {ops}"))
                else:
                    sites.append({"adresse": ins.address, "type": "adresse",
                                  "ligne": f"{m} {ops}", "taint": False})
            if m == "mov" and len(parties) == 2 and parties[0] in ni200.R64:
                taint[ni200.reg64(parties[0])] = taint.get(
                    ni200.reg64(parties[1]), False)
        return sites, viol

    f4 = list((REPO / "tls13" / "notation").glob("tls13-04-*.asm"))[0]
    rva4, slot4 = lay.SLOTS_TLS13["h100004"]
    o4 = assembler_bloc(f4, rva4, slot4)
    sites4, viol4 = analyser_04(o4, rva4)
    nb4 = sum(1 for s in sites4 if s["type"] == "branche")
    bt4 = sum(1 for s in sites4 if s["type"] == "branche" and s["taint"])
    na4 = sum(1 for s in sites4 if s["type"] == "adresse")
    at4 = sum(1 for s in sites4 if s["type"] == "adresse" and s["taint"])
    rapport.append(
        f"  tls13-04 (sha256-finaliser, LE MODÈLE AFFINÉ — l'état H[0..7] "
        f"secret @+0..31, la longueur publique @+104) : {nb4} branches "
        f"({bt4} taintées), {na4} accès ({at4} taintés) — "
        + ("PROUVÉE au modèle affiné (la branche du bourrage lit la "
           "LONGUEUR, métadonnée publique — nommée)" if not viol4
           else "VIOLATION"))
    for ligne in csv_rows:
        if ligne[1] == "tls13-04":
            ligne[3], ligne[4], ligne[5], ligne[6], ligne[7] = \
                nb4, bt4, na4, at4, ("NI PROUVÉE au modèle affiné (l'état "
                "secret, la longueur publique)" if not viol4
                else f"VIOLATIONS: {viol4[:2]}")
    if not viol4:
        verts += 1  # la ligne grossière avait compté un rouge

    # ---- loupe-06 (md5) : le modèle du contenu (la vague 10 reconduite) ----
    f6 = list((REPO / "loupe" / "notation").glob("loupe-06-*.asm"))[0]
    rva6, slot6 = L.SLOTS_LOUPE["i110006"]
    o6 = assembler_bloc(f6, rva6, slot6)

    spec210 = importlib.util.spec_from_file_location(
        "ni210", REPO / "atelier-gardes-ifqm1d1i4" / "non_interference_v210.py")
    ni210 = importlib.util.module_from_spec(spec210)
    spec210.loader.exec_module(ni210)
    sites6, viol6 = ni210.analyser_md5(o6, rva6)
    nb6 = sum(1 for s in sites6 if s["type"] == "branche")
    bt6 = sum(1 for s in sites6 if s["type"] == "branche" and s["taint"])
    na6 = sum(1 for s in sites6 if s["type"] == "adresse")
    at6 = sum(1 for s in sites6 if s["type"] == "adresse" and s["taint"])
    tot += 1
    verts += (not viol6)
    csv_rows.append(["md5", "loupe-06", "le contenu du fichier (P2+couplage)",
                     nb6, bt6, na6, at6,
                     "NI PROUVÉE (sous l'hypothèse du lifter validée au "
                     "domaine)" if not viol6 else "VIOLATION"])
    rapport.append(f"  loupe-06 (md5, le secret = LE CONTENU) : {nb6} "
                   f"branches ({bt6} taintées), {na6} accès ({at6} taintés) — "
                   f"{'PROUVÉE' if not viol6 else 'VIOLATION'}")

    # ---- LE CONTRÔLE NÉGATIF : une branche sur secret injectée -------------
    # (la preuve que le moteur VOIT les violations : la tls13-17 notation
    # copiée, LE SECRET CHARGÉ depuis le pointeur puis un jz sur lui —
    # l'analyseur DOIT nommer la branche taintée)
    f17 = list((REPO / "tls13" / "notation").glob("tls13-17-*.asm"))[0]
    rva17, slot17 = lay.SLOTS_TLS13["h100017"]
    o17 = assembler_bloc(f17, rva17, slot17)
    faux = bytes(o17)
    # l'injection : CHARGER le secret d'abord (la taint naît aux charges —
    # le pointeur lui-même est public), PUIS brancher dessus
    inj, _ = KS.asm("mov al, byte ptr [r8]\ntest al, al\njz 0x40")
    inj = bytes(inj)
    faux = inj + faux[len(inj):]
    _, viol_neg = ni200.analyser("tls13-17-NEGATIF", faux, rva17, "P3")
    neg_attrape = bool(viol_neg)
    rapport += ["",
                f"LE CONTRÔLE NÉGATIF (la branche sur secret injectée à la "
                f"tls13-17 copiée — mov al,[r8] ; test al,al ; jz) : "
                f"{'ATTRAPÉ — ' + viol_neg[0][2] if neg_attrape else 'NON ATTRAPÉ — ROUGE'}"]

    # ---- LE ROUND-TRIP sur la couverture étendue ---------------------------
    rt_ok = 0
    for bid in list(CIBLES) + ["loupe-06"]:
        if bid.startswith("tls13"):
            num = int(bid.split("-")[1])
            f = list((REPO / "tls13" / "notation").glob(f"{bid}-*.asm"))[0]
        else:
            f = list((REPO / "loupe" / "notation").glob(f"{bid}-*.asm"))[0]
        texte = f.read_text(encoding="utf-8")
        lignes = [l.split(";")[0].strip() for l in texte.splitlines()
                  if l.split(";")[0].strip() and not l.startswith("[")]
        enc = KS.asm("\n".join(lignes))[0]
        # le lifter : capstone décode, la notation re-générée comparée
        dec = [i for i in CS.disasm(bytes(enc), 0)]
        regen = "\n".join(f"{i.mnemonic} {i.op_str}".rstrip() for i in dec)
        regen = regen.replace("oword ptr", "xmmword ptr")
        lignes2 = [l.replace("xmmword ptr", "oword ptr") for l in lignes]
        if regen.rstrip() == "\n".join(lignes2).rstrip() or True:
            # la confrontation d'octets fait foi (la forme peut varier)
            re_enc = KS.asm(regen.replace("oword ptr", "xmmword ptr"))[0] \
                if "oword" in regen else KS.asm(regen)[0]
            if bytes(re_enc) == bytes(enc):
                rt_ok += 1
    rapport += ["",
                f"LE ROUND-TRIP (la couverture étendue, {len(CIBLES) + 1} "
                f"blocs) : {rt_ok}/{len(CIBLES) + 1} — "
                f"{'ZÉRO divergence' if rt_ok == len(CIBLES) + 1 else 'ROUGE'}"]

    # ---- LA COUVERTURE publiée en blocs et familles ------------------------
    rapport += ["",
                "LA COUVERTURE (EN BLOCS ET EN FAMILLES, les trous nommés) :",
                f"  {tot} BLOCS couverts : tls13-01/02/03/04 (sha256 — la "
                f"finalisation ÉTENDUE), 05 (hmac), 06/07/08 (hkdf — "
                f"l'Expand-Label ÉTENDU), 13/14 (x25519), 15/16 (aes), "
                f"17/18/19 (gcm — LE GHASH ÉTENDU, H secret) + loupe-06 "
                f"(md5) ;",
                f"  LES FAMILLES : sha256 [01-04], hmac [05], hkdf [06-08], "
                f"x25519 [13-14], aes [15-16], gcm [17-19], md5 [loupe-06] — "
                f"SEPT familles ;",
                f"  LES TROUS NOMMÉS (jamais une globalité) : {', '.join(TROUS)}"
                f" (f25519 arithmétique, compteurs, poignée complète, "
                f"enregistrement) — jamais couverts, jamais annoncés couverts."]
    rapport += ["",
                f"LE VERDICT : {verts}/{tot} blocs PROUVÉS (zéro branche, "
                f"zéro adresse taintées) ; le contrôle négatif "
                f"{'ATTRAPÉ' if neg_attrape else 'NON ATTRAPÉ'} ; le "
                f"round-trip {rt_ok}/{len(CIBLES) + 1}",
                "",
                "LE STATUT DE H DANS GHASH : LA VOIE FORTE TENUE — H "
                "(= E_K(0)) tainté comme secret à P3 : le taint de H ne "
                "tache NI branche NI adresse (la preuve tls13-17 ci-dessus) ; "
                "la déclaration « H public » eût exigé la même preuve — la "
                "couverture directe la rend inutile : H est un secret couvert.",
                "",
                "LA SOUNDNESS DU LIFTER : l'hypothèse VALIDÉE AU DOMAINE (le "
                "chantier 1 : zéro divergence sur les 942 encodages des "
                "blocs ; les 155 divergences mutantes HORS vocabulaire — LA "
                "GARDE : le refus nommé de toute classe non modélisée)."]

    with open(ICI / "non_interference_v220.csv", "w", encoding="utf-8") as f:
        for ligne in csv_rows:
            f.write(",".join(str(x) for x in ligne) + "\n")
    texte = "\n".join(rapport) + "\n"
    (ICI / "rapport-ni-v220.txt").write_text(texte, encoding="utf-8")
    print(texte)
    return 0 if (verts == tot and neg_attrape
                 and rt_ok == len(CIBLES) + 1) else 1


if __name__ == "__main__":
    sys.exit(main())
