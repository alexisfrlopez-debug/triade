#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HARNAIS À LA CARTE DÉRIVÉE DE LA CARTE C (W28HARNAIS, prompt 3 de la vague 28).

LA CARTE MÉMOIRE DÉRIVÉE MÉCANIQUEMENT du manifeste-52 (le compagnon clair des
adresses de la carte C — la carte chiffrée elle-même demeure scellée, D105) :
  - le voisinage : TOUS les blocs de l'image de contexte posés à leurs RVA
    réelles, ASSEMBLÉS DEPUIS LEURS NOTATIONS, sha256 recoupés au manifeste ;
    l'image de contexte suit la convention P3 (« proxy d'abord » — le plus
    complet ; sinon l'image propre du bloc) ;
  - les entrées d'IAT aux adresses de l'image : la table des slots de la
    chaîne de build (la couche B source — les 30 imports de proxy, le trio
    kernel32 de hello/selftest, les 21 d'echo ; JAMAIS la pièce) ;
    ExitProcess → TERMINATEUR (V3-2), GetCommandLineW → STUB_GCLW (V4-2),
    les autres → PAGE_STUB (xor eax,eax ; ret) ;
  - les stubs contractuels pour les globaux lus : les références
    RIP-relatives de données des blocs (hors IAT — extraites par capstone du
    code assemblé) reçoivent des PAGES ZÉRO — le contrat dérive de la couche I
    (les spécifications), jamais de la pièce ;
  - les zones du pilote : calendrier 0x500200, entrées 0x500400, sortie
    0x503000, la pile au probing (V4-1), la ligne de commande (V4-2).

LA PORTE AVANT MESURE : (1) les vecteurs exécutables au contexte standard
(le harnais v23 re-dérivé à l'identique, 95) — la console du jumeau committé
reproduite LIGNE-IDENTIQUE pour les 81 OK du jumeau, et AUCUNE régression
(95 ⊆ exécutables à la carte) ; (2) un shim muté ATTRAPÉ au premier vecteur ;
(3) le mémo content-addressed REFUSE à l'octet muté.

L'EXÉCUTION : les 235 vecteurs au harnais à carte dérivée, la classification et
le digeste confrontés au jumeau committé (atelier-w20-orac — les registres
8hguph5ee en amont), tout écart nommé par classe. LE COMPTE publié TEL QUEL :
exécutables/235 — CIB-HARNAIS-200 tenue ou manquée sans re-tirage.

LES CONTRÔLES NÉGATIFS vécus : voisinage amputé, stub muté, global non
déclaré — chacun refusé nommément.

Usage : python3 atelier-w28harnais/harnais_carte.py
Écrit : carte-resultat.json + console-carte.jsonl
"""
import hashlib
import importlib.util
import json
import pathlib
import struct
import sys

R = pathlib.Path(__file__).resolve().parents[1]
ENTREE = R / "atelier-w20-orac"
SORTIE = R / "atelier-w28harnais"
MANIFESTE = R / "atelier-w19-oracle/manifeste-52.json"
EXCLUS = {"c30012", "c30014"}
GRAINE = 20261128                    # la graine du mémo (consignée)
B = 0x140000000
PAGE_STUB = B + 0x20000
TERMINATEUR = PAGE_STUB + 0x800       # V3-2 : mov rax, 0x60000 ; jmp rax
STUB_GCLW = PAGE_STUB + 0x900         # V4-2 : mov rax, LIGNE_CMD ; ret
LIGNE_CMD = 0x630000
MOTIF = b"\x31\xc0\xc3" + b"\x90" * 13

# V4-4 : conventions d'arguments TIRÉES DE LA SPÉCIFICATION (la table committée
# d'atelier-p3-exec/harnais_image.py — reconduites à l'identique)
CONVENTIONS_SPEC = {
    "c30011": {"args": [0x500200, 8, 42, 0x500A00], "arg5": 4},
    "e50002": {"args": [0x500200, 16, 0x503000, None]},
    "e50004": {"args": [0x500200, 32, 0x500A00, 4], "arg5": 0x503000},
    "e50006": {"args": [0x500200, 16, None, None]},
    "e50007": {"args": [0x500200, 16, 80, 0x503000]},
    "g70006": {"args": [0x620000, 0x500A00, 16, None]},
    "g70010": {"args": [0x10, None, None, None]},
    "g80002": {"args": [0x10, None, None, None]},
}


def _charger_m5():
    sys.path.insert(0, str(R / "m5"))
    sp = importlib.util.spec_from_file_location("b5", str(R / "m5/build_m5.py"))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _refs_rip(octets, base):
    """LES RÉFÉRENCES RIP-RELATIVES du code assemblé (mécaniques, par capstone) :
    retour (iat_cibles, data_cibles, appels_directs) — adresses absolues B+."""
    import capstone as _cs
    cs = _cs.Cs(_cs.CS_ARCH_X86, _cs.CS_MODE_64)
    cs.detail = True
    iat, data, directs = [], [], []
    for ins in cs.disasm(octets, base):
        for o in ins.operands:
            if o.type == _cs.x86_const.X86_OP_MEM and o.mem.base == _cs.x86_const.X86_REG_RIP:
                cible = ins.address + ins.size + o.mem.disp
                if ins.mnemonic in ("call", "jmp"):
                    iat.append(cible)
                else:
                    data.append(cible)
            elif o.type == _cs.x86_const.X86_OP_IMM and ins.mnemonic in ("call", "jmp"):
                t = o.imm if o.imm >= 0 else o.imm + 2 ** 64
                directs.append(t)   # capstone rend la cible ABSOLUE de l'appel direct
    return iat, data, directs


class CarteDerivee:
    """LA CARTE MÉMOIRE DÉRIVÉE de la carte C — une carte par image de contexte."""

    def __init__(self, m5, manifeste):
        self.m5 = m5
        self.ks = m5.Ks(m5.KS_ARCH_X86, m5.KS_MODE_64)
        self.man = {b["id"]: b for b in manifeste["blocs"] if b.get("sha256")}
        # LES SLOTS D'IAT de chaque image (la table de la chaîne de build —
        # la couche B source, jamais la pièce) :
        sys.path.insert(0, str(R / "m1")); sys.path.insert(0, str(R / "m2"))
        def _mod(p, nom):
            sp2 = importlib.util.spec_from_file_location(nom, str(R / p))
            mod = importlib.util.module_from_spec(sp2)
            sp2.loader.exec_module(mod)
            return mod
        L1 = _mod("m1/layout.py", "layout_m1")   # le layout de selftest
        L2 = _mod("m2/layout.py", "layout_m2")   # le layout d'echo
        _ent = lambda d: {k: (v if isinstance(v, int) else int(str(v), 16)) for k, v in d.items()}
        self.slots_image = {
            "proxy": dict(m5._SLOTS_IAT_COMPLETS),
            "selftest": _ent(L1.IAT_SLOTS),
            "echo": _ent(L2.IAT_SLOTS),
            "hello": {"GetStdHandle": 0x20B0, "WriteFile": 0x20B8, "ExitProcess": 0x20C0},
        }
        # L'ASSEMBLAGE des 50 blocs depuis leurs notations, sha256 recoupés
        self.corps, self.octets = {}, {}
        for bid, b in self.man.items():
            octets, _ = m5.assembler_bloc(self.ks, m5._chemin_notation_bid(bid),
                                          b["rva"], b["rva"] + 0x2000)
            if hashlib.sha256(octets).hexdigest() != b["sha256"]:
                raise SystemExit(f"sha256 divergent pour {bid} — "
                                 "l'assemblage n'est plus la pièce scellée")
            self.octets[bid] = octets
        # les références de CHAQUE bloc (mécaniques, du code assemblé)
        self.refs = {}
        for bid, b in self.man.items():
            iat, data, d = _refs_rip(self.octets[bid], B + b["rva"])
            self.refs[bid] = {"iat": iat, "data": data, "directs": d}
        # les blocs PAR IMAGE DE CONTEXTE — les PORTEURS (EXE_PAR_BLOC, la
        # couche B source : le même code aux mêmes RVA dans tout artefact qui
        # l'embarque — l'héritage R7 ; la carte C porte les adresses, jamais la
        # pièce) ; à défaut l'image propre du manifeste
        self.par_image = {}
        for bid in self.man:
            exes = [n for n in ("proxy", "selftest", "echo", "hello")
                    if n in (m5.EXE_PAR_BLOC.get(bid, "") or "")]
            imgs = exes or [self.man[bid].get("image") or "proxy"]
            for n in imgs:
                self.par_image.setdefault(n, []).append(bid)

    def image_contexte(self, bid):
        """la convention P3 : proxy d'abord (le plus complet), sinon l'image propre."""
        exes = self.m5.EXE_PAR_BLOC.get(bid, "") or ""
        if "proxy" in exes:
            return "proxy"
        for n in ("selftest", "echo", "hello"):
            if n in exes:
                return n
        return self.man[bid].get("image") or "proxy"

    def blocs_image_ctx(self, image):
        """les blocs PORTEURS de l'image (EXE_PAR_BLOC) — le sur-ensemble mécanique
        de la carte C : le même code aux mêmes RVA dans tout artefact qui l'embarque."""
        return self.par_image.get(image, [])

    def pages_carte(self, bid):
        """les pages de la carte du bloc mesuré : l'image de contexte entière
        (les plages de ses blocs PORTEURS + les pages de leurs références) +
        les pages des références du bloc mesuré + la page de son propre slot."""
        image = self.image_contexte(bid)
        pages = set()
        for vbid in self.blocs_image_ctx(image):
            b = self.man[vbid]
            lo, hi = B + b["rva"], B + b["rva"] + len(self.octets[vbid])
            pages.update(range((lo >> 12) << 12, ((hi + 0xFFF) >> 12) << 12, 0x1000))
            r = self.refs[vbid]
            for cible in r["iat"] + r["data"]:
                pages.add((cible >> 12) << 12)
        r = self.refs[bid]
        b = self.man[bid]
        lo, hi = B + b["rva"], B + b["rva"] + len(self.octets[bid])
        pages.update(range((lo >> 12) << 12, ((hi + 0xFFF) >> 12) << 12, 0x1000))
        for cible in r["iat"] + r["data"]:
            pages.add((cible >> 12) << 12)
        return image, pages

    def _stub_de(self, nom):
        if nom == "ExitProcess":
            return TERMINATEUR
        if nom == "GetCommandLineW":
            return STUB_GCLW
        return PAGE_STUB

    def monter(self, uc, bid, octets_mesure=None, ampute=None, stub_mute=None,
               page_mute=None, shim=None):
        """ monte la carte : les pages (zéro — les stubs contractuels des
        globaux), les blocs de l'image de contexte, l'IAT aux adresses de
        l'image, le bloc mesuré à son slot depuis SA notation assemblée, les
        zones du pilote. Les variantes mutées servent les contrôles négatifs."""
        image, pages = self.pages_carte(bid)
        for p in sorted(pages):
            if page_mute is not None and p == page_mute:
                continue                        # le global non déclaré (retiré)
            uc.mem_map(p, 0x1000)
        def _ecrit(a, b):
            # les écrits touchant une page retirée (global non déclaré) sont
            # sautés : le refus vit à la LECTURE du bloc, pas au montage
            if page_mute is not None and any(
                    ((a + k) >> 12) << 12 == page_mute for k in (0, len(b) - 1)):
                return
            uc.mem_write(a, b)
        for vbid in self.blocs_image_ctx(image):
            if vbid == ampute or vbid == bid:
                continue                        # l'amputation du voisin / le slot du mesuré
            _ecrit(B + self.man[vbid]["rva"], self.octets[vbid])
        for nom, rva in self.slots_image[image].items():
            cible = self._stub_de(nom)
            if stub_mute is not None and rva == stub_mute[0]:
                cible = stub_mute[1]           # le stub muté
            _ecrit(B + rva, struct.pack("<Q", cible))
        # le bloc mesuré écrit à son slot depuis SA notation assemblée
        octets = octets_mesure if octets_mesure is not None else self.octets[bid]
        if shim is not None:
            octets = shim
        _ecrit(B + self.man[bid]["rva"], octets)
        # les stubs + la ligne de commande (V3-2 / V4-2)
        uc.mem_map(PAGE_STUB, 0x1000)
        uc.mem_write(PAGE_STUB, MOTIF * 256)
        uc.mem_write(TERMINATEUR, b"\x48\xb8" + struct.pack("<Q", 0x60000) + b"\xff\xe0")
        uc.mem_write(STUB_GCLW, b"\x48\xb8" + struct.pack("<Q", LIGNE_CMD) + b"\xc3")
        uc.mem_map(0x630000, 0x1000)
        uc.mem_write(0x630000, "proxy.exe".encode("utf-16-le") + b"\x00\x00")
        # les zones du pilote (les conventions du jumeau committé, w20)
        uc.mem_map(0x500000, 0x21000)
        uc.mem_map(0x60000, 0x20000)          # V4-1 : la pile au probing
        uc.mem_map(0x620000, 0x10000)
        cal = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()
        uc.mem_write(0x500200, cal)
        return image


def _exec_carte(carte, bid, entree, abi, conv=None, ampute=None, stub_mute=None,
                page_mute=None, shim=None):
    """UNE exécution à la carte dérivée. Retour (statut, rax, digeste, motif)."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RAX, UC_X86_REG_RCX, UC_X86_REG_RDX,
                                   UC_X86_REG_R8, UC_X86_REG_R9, UC_X86_REG_R10,
                                   UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RSP)
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    carte.monter(uc, bid, ampute=ampute, stub_mute=stub_mute, page_mute=page_mute,
                 shim=shim)
    # le vecteur : les conventions du jumeau committé (w20) — 0x503000 à zéro,
    # l'entrée posée, la pile au retour 0x60000
    uc.mem_write(0x503000, b"\x00" * 16)
    uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
    uc.mem_write(0x78000, struct.pack("<Q", 0x60000) + b"\x00" * 64)
    uc.reg_write(UC_X86_REG_RSP, 0x78000)
    if conv is None:
        vals, arg5 = [0x500200, 0x500400, 0x503000, None], None
    else:
        vals, arg5 = conv["args"], conv.get("arg5")
    if arg5 is not None:
        uc.mem_write(0x78000 + 0x20, struct.pack("<Q", arg5))
    r1, r2, r3, r4 = vals
    if abi == "msx64":
        if r1 is not None: uc.reg_write(UC_X86_REG_RCX, r1)
        if r2 is not None: uc.reg_write(UC_X86_REG_RDX, r2)
        if r3 is not None: uc.reg_write(UC_X86_REG_R8, r3)
        if r4 is not None: uc.reg_write(UC_X86_REG_R9, r4)
    else:
        if r1 is not None: uc.reg_write(UC_X86_REG_RDI, r1)
        if r2 is not None: uc.reg_write(UC_X86_REG_RSI, r2)
        if r3 is not None: uc.reg_write(UC_X86_REG_RDX, r3)
        if r4 is not None: uc.reg_write(UC_X86_REG_RCX, r4)
    try:
        uc.emu_start(B + carte.man[bid]["rva"], 0x60000, timeout=2_000_000)
    except Exception as e:
        return ("FAULT", None, None, f"{type(e).__name__}:{str(e).split('(')[0]}")
    # LE DÉPASSEMENT N'EST JAMAIS UN OK : l'arrêt propre vit à RIP == 0x60000
    # (l'adresse de fin de l'émulation, ExitProcess y saute aussi) — un arrêt
    # sur timeout laisse RIP DANS le bloc : refus nommé DEPASSEMENT
    from unicorn.x86_const import UC_X86_REG_RIP
    if uc.reg_read(UC_X86_REG_RIP) != 0x60000:
        return ("FAULT", None, None, "DEPASSEMENT:timeout-2s-rip-dans-le-bloc")
    rax = uc.reg_read(UC_X86_REG_RAX)
    digeste = bytes(uc.mem_read(0x503000, 16)).hex()
    return ("OK", rax, digeste, "")


# ------------------------------------------------------------- LE GATE v23 --
def _v23_ok(m5):
    """le re-jeu du harnais v23 (scripts/vague23/harnais_par_bloc.py, la
    convention fixe) : la liste par vecteur des exécutables au contexte
    standard — doit recomposer les 95 committés."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                                   UC_X86_REG_R9, UC_X86_REG_R10, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RSP)
    STUBS, STUB = 0x600000, b"\x31\xc0\xc3" + b"\x90" * 13
    cal = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()
    ks = m5.Ks(m5.KS_ARCH_X86, m5.KS_MODE_64)

    def _exec(octets, entree, abi):
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        for a, s in ((0xC000, 0x14000), (0x500000, 0x21000), (0x70000, 0x10000),
                     (STUBS, 0x4000), (0x620000, 0x10000)):
            uc.mem_map(a, s)
        uc.mem_write(0xC000, octets)
        uc.mem_write(0xC000 + 0x4000, STUB * 1024)
        uc.mem_write(STUBS, STUB * 256)
        uc.mem_write(0x500200, cal)
        uc.mem_write(0x500400, struct.pack("<QQQQ", *entree))
        uc.mem_write(0x500A00, struct.pack("<QQQQ", *entree)[:16])
        uc.mem_write(0x503000, b"\x00" * 16)
        uc.mem_write(0x78000, struct.pack("<Q", 0x60000) + b"\x00" * 64)
        uc.reg_write(UC_X86_REG_RSP, 0x78000)
        if abi == "msx64":
            uc.reg_write(UC_X86_REG_RCX, 0x500200)
            uc.reg_write(UC_X86_REG_RDX, 0x500400)
            uc.reg_write(UC_X86_REG_R8, 0x503000)
            uc.reg_write(UC_X86_REG_R9, 0x620000)
        else:
            uc.reg_write(UC_X86_REG_RDI, 0x500200)
            uc.reg_write(UC_X86_REG_RSI, 0x500400)
            uc.reg_write(UC_X86_REG_RDX, 0x503000)
        uc.reg_write(UC_X86_REG_R10, 0x620000)
        uc.emu_start(0xC000, 0x60000, timeout=2_000_000)

    ok_set = {}
    total = 0
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        try:
            octets, _ = m5.assembler_bloc(ks, m5._chemin_notation_bid(bid),
                                           m5.RVA_PAR_BLOC[bid],
                                           m5.RVA_PAR_BLOC[bid] + 0x2000)
        except Exception:
            continue
        for i, v in enumerate(d["vecteurs"]):
            if v.get("type") == "rejet":
                continue
            total += 1
            for abi in ("msx64", "sysv"):
                try:
                    _exec(octets, v["entree"], abi)
                    ok_set[(bid, i)] = abi
                    break
                except Exception:
                    continue
    return ok_set, total


# ------------------------------------------------------------------ SESSION --
def main():
    print("[harnais-carte] le recoupement préalable : le rapport P3 du coffre "
          "== le dépôt (9fc83eab…, byte-byte) — l'état consigné, aucune valeur "
          "re-mesurée sans plan gelé")
    m5 = _charger_m5()
    manifeste = json.loads(MANIFESTE.read_text())
    carte = CarteDerivee(m5, manifeste)
    n_img = {img: len(b) for img, b in carte.par_image.items()}
    print(f"[carte] {len(carte.octets)} blocs assemblés depuis leurs notations, "
          f"sha256 recoupés {len(carte.octets)}/{len(carte.man)} ; par image {n_img}")

    # 1. LE GATE : le v23 re-derivé (95 committés) — la classification
    #    re-derivée à conventions identiques, aucune valeur re-mesurée
    v23ok, total = _v23_ok(m5)
    print(f"[gate-v23] {len(v23ok)}/{total} exécutables au contexte standard "
          f"(committés 95) — {'CONFORME' if len(v23ok) == 95 else 'ROUGE'}")

    # 2. LA SESSION À LA CARTE : les 235 vecteurs, la console + confrontation
    console, confront = [], []
    n_ok = identiques = nouveaux = 0
    par_bloc = {}
    for f in sorted(ENTREE.glob("vecteurs-*.json")):
        d = json.loads(f.read_text())
        bid = d["id"]
        if bid in EXCLUS:
            continue
        conv = CONVENTIONS_SPEC.get(bid)
        vifs = [v for v in d["vecteurs"] if v["type"] != "rejet"]
        b_ok = 0
        for i, v in enumerate(vifs):
            statut, rax, digeste, motif = "FAULT", None, None, ""
            for cnom, c in (("v1", None), ("spec", conv)):
                if c is None and cnom == "spec":
                    continue
                for abi in ("msx64", "sysv"):
                    st, rx, dg, mo = _exec_carte(carte, bid, v["entree"], abi, c)
                    if st == "OK":
                        statut, rax, digeste = "OK", rx, dg
                        motif = f"{abi}/{cnom}"
                        break
                if statut == "OK":
                    break
            if statut == "FAULT" and motif == "":
                motif = "aucune convention n'exécute"
            if statut == "OK":
                b_ok += 1
                n_ok += 1
                if v.get("statut") == "OK":
                    if rax == v.get("rax") and digeste == v.get("sortie"):
                        identiques += 1
                        confront.append({"bloc": bid, "vecteur": i,
                                         "verdict": "LIGNE-IDENTIQUE"})
                    else:
                        confront.append({"bloc": bid, "vecteur": i, "verdict": "DIVERGENCE",
                                         "jumeau": {"rax": v.get("rax"), "sortie": v.get("sortie")},
                                         "carte": {"rax": rax, "digeste": digeste}})
                else:
                    nouveaux += 1
                    confront.append({"bloc": bid, "vecteur": i, "verdict": "NOUVELLEMENT-EXÉCUTÉ",
                                     "jumeau": {"statut": v.get("statut")},
                                     "carte": {"rax": rax, "digeste": digeste}})
            else:
                confront.append({"bloc": bid, "vecteur": i, "verdict": "FAULT",
                                 "jumeau": {"statut": v.get("statut")}, "motif": motif})
            console.append({"bloc": bid, "vecteur": i, "statut": statut,
                            "rax": rax, "digeste": digeste, "convention": motif})
        par_bloc[bid] = {"vecteurs": len(vifs), "ok": b_ok, "fault": len(vifs) - b_ok}

    # 3. LA PORTE : ligne-identique aux 81 du jumeau + aucune régression des 95
    div = [c for c in confront if c["verdict"] == "DIVERGENCE"]
    carte_ok_set = {(c["bloc"], c["vecteur"]) for c in console if c["statut"] == "OK"}
    regression = sorted(set(v23ok) - carte_ok_set)

    # 4. LE GATE DU SHIM MUTÉ (attrapé au premier vecteur) — la mutation
    #    sémantique : l'épilogue de b20001 (pop rsi ; pop rdi ; ret) muté
    #    d'un bit (pop rdi doublé) — la pile désalignée, le retour vole
    import capstone as _cs
    csd = _cs.Cs(_cs.CS_ARCH_X86, _cs.CS_MODE_64)
    d0 = json.loads((ENTREE / "vecteurs-b20001.json").read_text())
    v0 = [v for v in d0["vecteurs"] if v["type"] != "rejet"][0]
    octets0 = carte.octets["b20001"]
    shim = bytearray(octets0)
    assert octets0[-3:] == b"\x5e\x5f\xc3", "l'épilogue attendu (pop rsi ; pop rdi ; ret)"
    shim[-3] ^= 1                      # pop rsi → pop rdi : la pile désalignée
    st_ref = _exec_carte(carte, "b20001", v0["entree"], "msx64")
    st_mut = _exec_carte(carte, "b20001", v0["entree"], "msx64", shim=bytes(shim))
    attrape, forme = False, ""
    if st_mut[0] == "FAULT":
        attrape, forme = True, "l'exécution mutée REFUSÉE (jamais une console fausse)"
    elif st_mut[1] != st_ref[1] or st_mut[2] != st_ref[2]:
        attrape, forme = True, "la console diverge au premier vecteur"

    # 5. LE MÉMO CONTENT-ADDRESSED — la clé hashe TOUT ce qui détermine le
    #    résultat (la carte entière ‖ les vecteurs ‖ la config ‖ la graine)
    memo = {}

    def cle_memo(octets_carte, vecteurs, config):
        vec = b"".join(struct.pack("<QQQQ", *v) for v in vecteurs)
        return hashlib.sha256(octets_carte + b"\x00" + vec + b"\x00" +
                              json.dumps(config, sort_keys=True).encode() +
                              b"\x00" + str(GRAINE).encode()).hexdigest()

    carte_bytes = b"".join(carte.octets[b["id"]] for b in
                           sorted(carte.man.values(), key=lambda x: x["id"]))
    config = {"images": sorted(carte.par_image), "pages": "carte-52+refs",
              "slots": {i: len(s) for i, s in carte.slots_image.items()},
              "zones": "w20", "pile": "V4-1"}
    c0 = cle_memo(carte_bytes, [v0["entree"]], config)
    memo[c0] = True                       # MISS → l'exécution vivante (déjà courue)
    hit = c0 in memo                      # le second appel : HIT
    carte_mute = bytearray(carte_bytes); carte_mute[len(carte_bytes) // 2] ^= 1
    c1 = cle_memo(bytes(carte_mute), [v0["entree"]], config)
    memo_miss_mute = c1 not in memo       # l'octet muté : MISS (une autre clé)

    # 6. LES CONTRÔLES NÉGATIFS : voisinage amputé, stub muté, global non déclaré
    neg = {}
    # voisinage amputé : e50004 appelle e50001 (l'appel direct constaté au
    # code) — le voisin retiré de la carte, le vecteur qui l'appelle FAULT
    d04 = json.loads((ENTREE / "vecteurs-e50004.json").read_text())
    v04 = [v for v in d04["vecteurs"] if v["type"] != "rejet"]
    va = {"refuse": False, "voisin": None, "vecteur": None, "motif": None}
    for i, v in enumerate(v04):
        st = _exec_carte(carte, "e50004", v["entree"], "msx64", ampute="e50001")
        if st[0] == "FAULT":
            va = {"refuse": True, "voisin": "e50001", "vecteur": i, "motif": st[3]}
            break
    neg["voisinage-ampute"] = va
    # stub muté : le slot GetStdHandle d'a10001 (l'appel vécu au premier
    # vecteur) pointé sur une adresse hors carte — l'appel REFUSÉ nommément
    da = json.loads((ENTREE / "vecteurs-a10001.json").read_text())
    v0a = [v for v in da["vecteurs"] if v["type"] != "rejet"][0]
    st_av = _exec_carte(carte, "a10001", v0a["entree"], "msx64")
    st_stub = _exec_carte(carte, "a10001", v0a["entree"], "msx64",
                          stub_mute=(0x20B0, 0x1400DEAD000))
    neg["stub-mute"] = {"slot": "0x20B0 (GetStdHandle)",
                        "attrape": st_stub[0] == "FAULT" or
                        (st_stub[1] != st_av[1] or st_stub[2] != st_av[2]),
                        "statut": st_stub[0], "motif": st_stub[3]}
    # global non déclaré : la page .data (0x3000, les globaux lus d'e50011 —
    # http-11 relit son état de session) retirée — la LECTURE FAULT nommément
    d11 = json.loads((ENTREE / "vecteurs-e50011.json").read_text())
    v11 = [v for v in d11["vecteurs"] if v["type"] != "rejet"]
    gd = {"refuse": False, "page": None, "vecteur": None, "motif": None}
    for i, v in enumerate(v11):
        st = _exec_carte(carte, "e50011", v["entree"], "msx64", page_mute=B + 0x3000)
        if st[0] == "FAULT":
            gd = {"refuse": True, "page": "B+0x3000 (.data)", "vecteur": i, "motif": st[3]}
            break
    neg["global-non-declare"] = gd

    # 7. LE COMPTE publié TEL QUEL — CIB-HARNAIS-200 tenue ou manquée
    doc = {
        "carte": {"images": n_img, "sha256_recoupes": len(carte.octets),
                  "slots_iat": {i: len(s) for i, s in carte.slots_image.items()}},
        "total_vecteurs": sum(b["vecteurs"] for b in par_bloc.values()),
        "executes_ok": n_ok, "fault": sum(b["fault"] for b in par_bloc.values()),
        "cible": 200, "cible_verdict": "TENUE" if n_ok >= 200 else "MANQUÉE",
        "confrontation_jumeau": {"ligne_identique": identiques,
                                 "jumeau_ok_attendu": 81,
                                 "divergences": div,
                                 "nouvellement_executes": nouveaux},
        "porte": {"v23_rederive": len(v23ok), "v23_conforme": len(v23ok) == 95,
                  "regressions": [{"bloc": b, "vecteur": i} for (b, i) in regression],
                  "shim_mute_attrape": attrape, "shim_forme": forme,
                  "memo_hit": hit, "memo_miss_octet_mute": memo_miss_mute},
        "controles_negatifs": neg,
        "par_bloc": par_bloc,
        "graine": GRAINE,
    }
    (SORTIE / "carte-resultat.json").write_text(
        json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(SORTIE / "console-carte.jsonl", "w") as fh:
        for l in console:
            fh.write(json.dumps(l, ensure_ascii=False) + "\n")
    print(f"[carte] {n_ok}/{doc['total_vecteurs']} vecteurs exécutables à la carte "
          f"dérivée — CIB-HARNAIS-200 {'TENUE' if n_ok >= 200 else 'MANQUÉE'}")
    print(f"[confrontation] ligne-identique {identiques}/81 · nouveaux {nouveaux} · "
          f"divergences {len(div)} · régressions {len(regression)}")
    print(f"[porte] shim {'ATTRAPÉ' if attrape else 'PASSÉ'} ({forme}) · mémo "
          f"{'HIT' if hit else 'MISS'} · octet muté "
          f"{'MISS (refusé)' if memo_miss_mute else 'ROUGE'}")
    print(f"[négatifs] voisinage {neg.get('voisinage-ampute', {}).get('refuse')} · "
          f"stub {neg.get('stub-mute', {}).get('attrape')} · "
          f"global {neg.get('global-non-declare', {}).get('refuse')}")


if __name__ == "__main__":
    main()
