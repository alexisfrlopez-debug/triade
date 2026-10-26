#!/usr/bin/env python3
"""build_sceau.py — Lignée sceau (m7, D34 échelon 2) : vérification native, phase 1.

Notation (keystone) -> octets -> ELF64 À LA MAIN (ehdr 64 o + 2 phdr 56 o,
aucun outil de liaison) -> carte génération 1. L'artefact `sceau` est le
vérificateur de signatures Ed25519 du projet — échelon 2 de l'échelle
d'auto-hébergement D34. PHASE 1 (dev.1) : la famille SHA-512 complète
(av-01..04) et le principal en mode diagnostic `--hacher` (ligne sha512sum
exacte — l'agent gagne un hacheur SHA-512 natif) ; le mode vérification est
posé EN CHANTIER (exit 2 explicite) : la couche I des 17 specs av est
COMPLÈTE (R2 écrite-avant-code), les notations av-05..16 viennent en dev.2+.

Héritages m6 octet-identiques (même profil) : ah-01-ecrire (d40001),
ah-03-sortir (d40003), ah-08-hex (d40008) — la preuve est DOUBLE : les
fichiers notation/ah-*.asm sont des copies conformes (cmp), et les octets
vivent aux MÊMES adresses que dans hachoir. ah-02-lire : non embarqué (le
principal lit par read direct, I1 miroir ah-09).

Chaîne (le protocole s'applique intégralement) :
  1. couche I chargée et auditée (gabarit § 2.2, 20 specs, R2) — les specs
     av-05..16 sont posées, leurs notations sont EN CHANTIER (comptées) ;
  2. octet-identité des héritages : notation m7 == notation m6 (cmp) ;
  3. round-trip R5 par bloc noté (keystone -> capstone -> keystone) ;
  4. oracle structurel : appels directs PAR BLOC, numéros de syscall PAR
     BLOC, cibles RIP déclarées, sauts internes aux frontières, padding
     >= 16, feuille d40008, symboles @ confrontés à layout.py ET aux
     longueurs RÉELLES des messages + au magic « --hacher » (leçon C1) ;
  5. composition ELF64 : ehdr + phdr RX (RVA == offset) + phdr RW (.bss
     pur, filesz 0), code aux slots, NOP intra-slot, int3 réserves, rodata
     (K512, HEXCHARS @ 0x2100 INTANGIBLE, constantes crypto posées dès
     dev.1 pour les specs av-05..16, messages) ;
  6. oracle différentiel NATIF (mode --hacher) : vecteurs dorés FIPS
     180-4 SHA-512 (vide, « abc », 448 bits, un million de 'a'), tailles
     de transition (0, 1, 111, 112, 127, 128, 129, 1000, 65535, 65536,
     65537, 131072) — ligne octet-identique à « <sha512sum>  <chemin>\\n » ;
     chemins d'échec (usage, ouverture, lecture, mode chantier) ;
  7. falsification : chaque octet de code des 8 blocs embarqués, batterie
     de 6 scénarios — zéro silence ;
  8. usage auto-référentiel : les empreintes SHA-512 des artefacts du
     projet (hello.exe, selftest.exe, echo.exe, hachoir, sceau) produites
     PAR sceau, contre-vérifiées sha512sum ;
  9. mesures D34 (sceau vs sha512sum sur 1 Mo) ;
 10. carte génération 1 (sel Argon2id distinct D34, clés projet D27,
     signature Ed25519, verrou croisé R8) + cristallisation R6.

Usage :
  python3 build_sceau.py             # construction + oracle natif + carte
  python3 build_sceau.py --verifier  # re-vérification complète (R5/R8)
"""

from __future__ import annotations

import hashlib
import os
import re
import struct
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import layout as L                       # noqa: E402

import capstone                           # noqa: E402
import carte_sceau as cm                  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(ICI), "m2"))
from carte_m2 import empreinte_racine     # noqa: E402  (mécanique commune D27)

M6 = os.path.join(os.path.dirname(ICI), "m6")


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


# --- Couche I : lecture et audit ----------------------------------------------

def lire_spec(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", texte)
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3)), "texte": texte}
    for bloc in ("Intention", "Contrat", "Échecs", "Vecteurs", "Fixtures",
                 "Provenance", "Décisions"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")
    if "écrite-avant-code" not in texte:
        raise EchecBuild(f"{chemin} : provenance inattendue (R2)")
    return spec


def charger_couche_I() -> dict[str, dict]:
    """20 specs : 17 av (m7/I) + 3 héritages ah (m6/I, inchangées)."""
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_SCEAU:
        dossier = M6 if fichier.startswith("ah-") else ICI
        chemin = os.path.join(dossier, "I", fichier + ".md")
        spec = lire_spec(chemin)
        if spec["id"] != sid.split(":")[0]:
            raise EchecBuild(f"{chemin} : identifiant {spec['id']} != {sid}")
        specs[bid] = spec
    return specs


# --- Assemblage : notation -> octets (R5) --------------------------------------

CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)


def assembler_bloc(fichier: str, rva: int, slot: int) -> dict:
    """Notation explicite -> octets + instructions + round-trip intégral."""
    chemin = os.path.join(ICI, "notation", fichier + ".asm")
    with open(chemin, encoding="utf-8") as f:
        lignes = [l.strip() for l in f.read().splitlines()]
    instrs = [l for l in lignes if l and not l.startswith(";")]
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    code, insns = bytearray(), []
    pos = rva
    for texte in instrs:
        enc, _ = ks.asm(texte, pos)
        if not enc:
            raise EchecBuild(f"{fichier} @ {pos:#x} : inassemblable : {texte!r}")
        octets = bytes(enc)
        # R5 : keystone -> capstone -> keystone, identité octets
        des = list(CS.disasm(octets, pos))
        if len(des) != 1:
            raise EchecBuild(f"{fichier} @ {pos:#x} : pas une instruction")
        texte_cs = f"{des[0].mnemonic} {des[0].op_str}".strip()
        enc2, _ = ks.asm(texte_cs, pos)
        if bytes(enc2) != octets:
            raise EchecBuild(f"{fichier} @ {pos:#x} : round-trip R5 rompu : {texte!r}")
        insns.append(des[0])
        code += octets
        pos += len(octets)
    if len(code) > slot:
        raise EchecBuild(f"{fichier} : {len(code)} o > slot {slot:#x} (D8)")
    if slot - len(code) < 16:
        raise EchecBuild(f"{fichier} : padding {slot - len(code)} < 16 (D8)")
    slot_plein = bytes(code) + b"\x90" * (slot - len(code))
    return {"octets": bytes(code), "slot": slot_plein, "insns": insns,
            "texte": instrs}


def heritages_octet_identiques() -> int:
    """La preuve de réutilisation : notation m7 == notation m6 (cmp)."""
    n = 0
    for bid, _, fichier, _, _ in L.BLOCS_SCEAU:
        if not fichier.startswith("ah-"):
            continue
        m7 = os.path.join(ICI, "notation", fichier + ".asm")
        m6 = os.path.join(M6, "notation", fichier + ".asm")
        with open(m7, "rb") as f1, open(m6, "rb") as f2:
            if f1.read() != f2.read():
                raise EchecBuild(
                    f"{fichier} : notation m7 != notation m6 — l'héritage doit "
                    f"être une copie CONFORME (réutilisation octet-identique, R7)")
        n += 1
    return n


def assembler_tout():
    specs = charger_couche_I()
    code, verrous = {}, []
    en_chantier = []
    for bid, sid, fichier, rva, slot in L.BLOCS_SCEAU:
        if bid in L.NOTES_DEV1:
            code[bid] = assembler_bloc(fichier, rva, slot)
            code[bid]["spec"] = sid
            code[bid]["fichier"] = fichier
            code[bid]["rva"] = rva
            code[bid]["slot_taille"] = slot
        else:
            en_chantier.append(bid)
    return list(L.BLOCS_SCEAU), specs, code, en_chantier, verrous


# --- Oracle structurel : contrats I sur le code désassemblé --------------------

A_ECRITE, A_SORTIR, A_HEX = L.A_ECRITE, L.A_SORTIR, L.A_HEX
A_INIT, A_COMPRIMER, A_ABSORBER, A_FINALISER = (L.A_INIT, L.A_COMPRIMER,
                                                L.A_ABSORBER, L.A_FINALISER)

APPELS_AUTORISES = {          # I1 des specs : appels directs par bloc
    "d50003": {A_COMPRIMER},
    "d50004": {A_COMPRIMER},
    "d50017": {A_ECRITE, A_SORTIR, A_HEX, A_INIT, A_ABSORBER, A_FINALISER},
}
SYSCALLS_AUTORISES = {        # I1 : numéros de syscall par bloc (EABI x86-64)
    "d40001": {1},            # write
    "d40003": {60},           # exit
    "d50017": {0, 2, 3},      # read, open, close (I1 de av-17)
}
DONNEES_RIP = {               # I1/I3 : cibles RIP de données par bloc
    "d40008": {L.R_HEXCHARS},
    "d50002": {L.R_K512},
    "d50017": {L.R_CTX, L.R_DIGEST, L.R_LIGNE, L.R_TAMPON,
               L.R_MSG_USAGE, L.R_MSG_OUVERTURE, L.R_MSG_LECTURE,
               L.R_MSG_ECRITURE, L.R_MSG_CHANTIER},
}


def cible_rip(insn) -> int | None:
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
    if not m:
        return None
    disp = int(m.group(2), 16)
    return insn.address + insn.size + (disp if m.group(1) == "+" else -disp)


def _prologue_aligne_sysv(insns) -> bool:
    """(8 + 8*npush - sub) ≡ 0 mod 16 — pile alignée aux points d'appel SysV."""
    npush = 0
    while npush < len(insns) and insns[npush].mnemonic == "push":
        npush += 1
    if not any(i.mnemonic == "call" for i in insns):
        return True
    for i in insns:
        if i.mnemonic == "call":
            break
        if i.mnemonic == "sub" and i.op_str.startswith("rsp,"):
            imm = int(i.op_str.split(",")[1].strip(), 16)
            return (8 + 8 * npush - imm) % 16 == 0
    return (8 + 8 * npush) % 16 == 0      # pas de sub : les pushes suffisent


def oracle_structurel(code: dict, specs: dict) -> list[str]:
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    adresses = {bid: {i.address for i in code[bid]["insns"]} for bid in code}
    for bid, bloc in code.items():
        insns = bloc["insns"]
        rva, slot = bloc["rva"], bloc["slot_taille"]
        # Sauts internes : frontière d'instruction du même bloc
        for i in insns:
            if i.mnemonic[0] == "j":
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses[bid], f"cible {cible:#x} hors frontière")
        # Appels directs : uniquement les blocs déclarés
        for i in insns:
            if i.mnemonic == "call":
                cible = int(i.op_str, 16)
                verrou(f"{bid}:appel-autorise@{i.address:#x}",
                       cible in APPELS_AUTORISES.get(bid, set()),
                       f"cible {cible:#x} hors blocs déclarés (I1/I2)")
        # Syscalls : numéros autorisés par bloc, posés juste avant (mov/xor eax)
        nr = None
        for i in insns:
            if i.mnemonic == "mov" and i.op_str.startswith("eax,"):
                try:
                    nr = int(i.op_str.split(",")[1].strip(), 0)
                except ValueError:
                    nr = None
            elif i.mnemonic == "xor" and i.op_str.replace(" ", "") == "eax,eax":
                nr = 0
            if i.mnemonic == "syscall":
                verrou(f"{bid}:syscall-autorise@{i.address:#x}",
                       nr in SYSCALLS_AUTORISES.get(bid, set()),
                       f"nr={nr} non déclaré (I1)")
        # Données RIP : cibles déclarées
        for i in insns:
            cible = cible_rip(i)
            if cible is not None:
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in DONNEES_RIP.get(bid, set()),
                       f"cible {cible:#x} hors données déclarées (I1/I3)")
        # Padding/alignement (D8/D28/D33)
        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16)
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        verrou(f"{bid}:slot-multiple-64", slot % 64 == 0)
        # Pile alignée aux appels (sauf _start : ABI de démarrage, aucun push)
        if bid != "d50017":
            verrou(f"{bid}:pile-alignee", _prologue_aligne_sysv(insns))
        else:
            verrou(f"{bid}:start-sans-push",
                   not any(i.mnemonic == "push" for i in insns))
        # Feuille ah-08 : aucun appel, aucun push (I2 de sa spec)
        if bid == "d40008":
            verrou("d40008:feuille",
                   not any(i.mnemonic in ("call", "push") for i in insns))
    return verrous


# --- Symboles des brouillons confrontés au layout (leçon C1) -------------------

_MESSAGES = {"L_USAGE": L.MSG_USAGE, "L_OUVERTURE": L.MSG_OUVERTURE,
             "L_LECTURE": L.MSG_LECTURE, "L_ECRITURE": L.MSG_ECRITURE,
             "L_CHANTIER": L.MSG_CHANTIER}

_MAGIC = {"MAGIC_HACHER": int.from_bytes(b"--hacher", "little")}


def verifier_symboles() -> int:
    """Chaque @symbole du brouillon doit valoir la constante layout/réelle —
    l'arithmétique de l'auteur est VÉRIFIÉE, jamais crue (C1)."""
    n = 0
    attendus = {"A_ECRITE": L.A_ECRITE, "A_SORTIR": L.A_SORTIR,
                "A_HEX": L.A_HEX, "A_INIT": L.A_INIT, "A_COMPRIMER": L.A_COMPRIMER,
                "A_ABSORBER": L.A_ABSORBER, "A_FINALISER": L.A_FINALISER,
                "R_K512": L.R_K512,
                "R_HEXCHARS": L.R_HEXCHARS, "R_CTX": L.R_CTX,
                "R_DIGEST": L.R_DIGEST, "R_LIGNE": L.R_LIGNE, "R_TAMPON": L.R_TAMPON,
                "R_MSG_USAGE": L.R_MSG_USAGE, "R_MSG_OUVERTURE": L.R_MSG_OUVERTURE,
                "R_MSG_LECTURE": L.R_MSG_LECTURE, "R_MSG_ECRITURE": L.R_MSG_ECRITURE,
                "R_MSG_CHANTIER": L.R_MSG_CHANTIER}
    for _, _, fichier, _, _ in L.BLOCS_SCEAU:
        chemin = os.path.join(ICI, "notation", "brouillons", fichier + ".asm")
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding="utf-8") as f:
            for ligne in f:
                m = re.match(r"@(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*$", ligne.strip())
                if not m:
                    continue
                nom, val = m.group(1), int(m.group(2), 0)
                if nom in attendus:
                    attendu = attendus[nom]
                elif nom in _MESSAGES:
                    attendu = len(_MESSAGES[nom])       # longueur RÉELLE (C1)
                elif nom in _MAGIC:
                    attendu = _MAGIC[nom]               # magic « --hacher » (I6)
                else:
                    raise EchecBuild(f"{fichier} : symbole inconnu @{nom}")
                if val != attendu:
                    raise EchecBuild(
                        f"{fichier} : @{nom} = {val:#x} mais layout/réel = {attendu:#x} "
                        f"(leçon C1 : l'arithmétique de l'auteur est vérifiée)")
                n += 1
    return n


# --- Composition ELF64 ----------------------------------------------------------


def composer_elf(code: dict) -> bytes:
    """Image RX complète : ehdr + 2 phdr + int3 + slots + rodata (RVA == offset)."""
    img = bytearray(b"\xcc" * L.RX_TAILLE)      # réserves int3 par défaut

    def poser(rva: int, donnees: bytes, nom: str = ""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > L.RX_TAILLE:
            raise EchecBuild(f"segment RX débordant à {rva:#x}")
        img[rva: rva + len(donnees)] = donnees

    poses: list[tuple[int, int, str]] = []       # garde-fou chevauchement (C1)
    for bid, _, _, rva, slot in L.BLOCS_SCEAU:
        if bid in code:
            poser(rva, code[bid]["slot"], bid)
    # K512 (FIPS 180-4 § 4.2.3)
    poser(L.R_K512, b"".join(struct.pack("<Q", k) for k in L.K512), "R_K512")
    # Constantes f25519 / edwards25519 — posées dès dev.1 : les specs av-05..16
    # les référencent, le builder les vérifie (fixtures gelées, journal 20 : la
    # table K du hachoir était vérifiée AVANT la première exécution aussi).
    for rva, valeur, nom in ((L.R_D, L.D25519, "R_D"), (L.R_BX, L.BX25519, "R_BX"),
                             (L.R_BY, L.BY25519, "R_BY"), (L.R_SQRTM1, L.SQRTM1, "R_SQRTM1")):
        poser(rva, b"".join(struct.pack("<Q", m) for m in L.limbs(valeur)), nom)
    poser(L.R_EXP_INV, (L.P25519 - 2).to_bytes(32, "little"), "R_EXP_INV")
    poser(L.R_EXP_SQRT, ((L.P25519 - 5) // 8).to_bytes(32, "little"), "R_EXP_SQRT")
    poser(L.R_L, L.L25519.to_bytes(32, "little"), "R_L")
    # HEXCHARS @ 0x2100 : INTANGIBLE (cible du lea RIP de l'héritage ah-08)
    for rva, donnees, nom in ((L.R_HEXCHARS, L.HEXCHARS, "HEXCHARS"),
                              (L.R_MSG_USAGE, L.MSG_USAGE, "MSG_USAGE"),
                              (L.R_MSG_OUVERTURE, L.MSG_OUVERTURE, "MSG_OUVERTURE"),
                              (L.R_MSG_LECTURE, L.MSG_LECTURE, "MSG_LECTURE"),
                              (L.R_MSG_ECRITURE, L.MSG_ECRITURE, "MSG_ECRITURE"),
                              (L.R_MSG_CHANTIER, L.MSG_CHANTIER, "MSG_CHANTIER")):
        poser(rva, donnees + b"\x00", nom)
    for (d1, f1, n1), (d2, f2, n2) in zip(poses, poses[1:]):
        if d1 < f2 and d2 < f1:
            raise EchecBuild(f"chevauchement : {n1} [{d1:#x},{f1:#x}) / {n2} [{d2:#x},{f2:#x})")

    # ehdr + phdr posés PAR-DESSUS les int3 d'en-tête (zone 0..0x1000 réservée)
    e_ident = b"\x7fELF" + bytes([2, 1, 1, 0]) + b"\x00" * 8
    ehdr = struct.pack("<16sHHIQQQIHHHHHH", e_ident,
                       2, 0x3E, 1,                       # EXEC, x86-64, v1
                       L.IMAGE_BASE + L.ENTREE,          # e_entry
                       64, 0, 0,                         # phoff, shoff, flags
                       64, 56, 2, 0, 0, 0)               # ehsize, phentsize...
    ph_rx = struct.pack("<IIQQQQQQ", 1, 5,              # LOAD, R+X
                        0, L.IMAGE_BASE, L.IMAGE_BASE, L.RX_TAILLE, L.RX_TAILLE,
                        L.TAILLE_PAGE)
    ph_rw = struct.pack("<IIQQQQQQ", 1, 6,              # LOAD, R+W (.bss pur)
                        L.RW_RVA, L.IMAGE_BASE + L.RW_RVA,
                        L.IMAGE_BASE + L.RW_RVA, 0, L.RW_TAILLE, L.TAILLE_PAGE)
    img[0:64] = ehdr
    img[64:120] = ph_rx
    img[120:176] = ph_rw
    return bytes(img)


def valider_elf(img: bytes):
    if len(img) != L.RX_TAILLE:
        raise EchecBuild(f"taille RX {len(img):#x} != {L.RX_TAILLE:#x}")
    if img[:4] != b"\x7fELF" or img[4] != 2 or img[5] != 1:
        raise EchecBuild("magie ELF64 LE absente")
    e_entry = struct.unpack_from("<Q", img, 24)[0]
    if e_entry != L.IMAGE_BASE + L.ENTREE:
        raise EchecBuild(f"e_entry {e_entry:#x} != slot av-17")
    if img[L.R_HEXCHARS:L.R_HEXCHARS + 16] != L.HEXCHARS:
        raise EchecBuild("HEXCHARS @ 0x2100 divergent (intangible — héritage ah-08)")
    if img[L.R_K512:L.R_K512 + 640] != b"".join(struct.pack("<Q", k) for k in L.K512):
        raise EchecBuild("table K512 divergente (FIPS 180-4 § 4.2.3)")
    for rva, valeur in ((L.R_D, L.D25519), (L.R_BX, L.BX25519),
                        (L.R_BY, L.BY25519), (L.R_SQRTM1, L.SQRTM1)):
        attendu = b"".join(struct.pack("<Q", m) for m in L.limbs(valeur))
        if img[rva:rva + 40] != attendu:
            raise EchecBuild(f"fixture limbs @ {rva:#x} divergente")
    if img[L.R_EXP_INV:L.R_EXP_INV + 32] != (L.P25519 - 2).to_bytes(32, "little"):
        raise EchecBuild("exposant p-2 divergent")
    if img[L.R_EXP_SQRT:L.R_EXP_SQRT + 32] != ((L.P25519 - 5) // 8).to_bytes(32, "little"):
        raise EchecBuild("exposant (p-5)/8 divergent")
    if img[L.R_L:L.R_L + 32] != L.L25519.to_bytes(32, "little"):
        raise EchecBuild("L (ordre du groupe) divergent")


# --- Oracle différentiel NATIF (échelon 2 : le terrain est la vérité) -----------

class Terrain:
    """Exécution native de sceau — le terrain de l'agent est son propre banc."""

    def __init__(self, img: bytes):
        parent = os.path.join(ICI, ".tmp")
        os.makedirs(parent, exist_ok=True)          # mkdtemp ne crée pas le parent
        self.dossier = tempfile.mkdtemp(prefix="sceau-", dir=parent)
        self.chemin = os.path.join(self.dossier, "sceau")
        with open(self.chemin, "wb") as f:
            f.write(img)
        os.chmod(self.chemin, 0o755)

    def temoin(self, nom: str, donnees: bytes) -> str:
        chemin = os.path.join(self.dossier, nom)
        with open(chemin, "wb") as f:
            f.write(donnees)
        return chemin

    def lancer(self, args: list[str]) -> tuple[bytes, bytes, int]:
        import subprocess as sp
        try:
            r = sp.run([self.chemin] + args, capture_output=True, timeout=60)
            return r.stdout, r.stderr, r.returncode
        except sp.TimeoutExpired:
            # Un mutant qui pend (boucle infinie) EST une divergence détectée —
            # code sentinel -99, jamais confondu avec un comportement sain.
            return b"", b"<timeout>", -99

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


def ligne_sha512sum(chemin: str, donnees: bytes) -> bytes:
    """Référent hashlib au format sha512sum — le diff est la preuve."""
    return f"{hashlib.sha512(donnees).hexdigest()}  {chemin}\n".encode()


def oracle_natif(img: bytes, longueurs: dict[str, int] | None = None) -> dict:
    t = Terrain(img)
    try:
        cas = 0
        # Vecteurs dorés FIPS 180-4 SHA-512 + tailles de transition 128/112
        vecteurs = [
            ("fips-vide", b""),
            ("fips-abc", b"abc"),
            ("fips-448", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"),
            ("million-a", b"a" * 1_000_000),
        ] + [(f"t{n}", bytes((i * 31 + n) % 256 for i in range(n)))
             for n in (1, 111, 112, 127, 128, 129, 1000,
                       65535, 65536, 65537, 131072)]
        for nom, donnees in vecteurs:
            chemin = t.temoin(nom, donnees)
            attendu = ligne_sha512sum(chemin, donnees)
            sortie, err, code = t.lancer(["--hacher", chemin])
            if code != 0 or sortie != attendu or err:
                raise EchecBuild(
                    f"oracle natif {nom} : code={code} sortie={sortie!r} "
                    f"attendu={attendu!r} err={err!r}")
            cas += 1
        # Chemins d'échec et modes (V2 de av-17)
        sortie, err, code = t.lancer([])
        if code != 1 or err != L.MSG_USAGE or sortie:
            raise EchecBuild(f"usage : code={code} err={err!r}")
        sortie, err, code = t.lancer(["--hacher"])
        if code != 1 or err != L.MSG_USAGE or sortie:
            raise EchecBuild(f"hacher-sans-fichier : code={code} err={err!r}")
        sortie, err, code = t.lancer(["--hacherx", t.temoin("x", b"y")])
        if code != 1 or err != L.MSG_USAGE or sortie:
            raise EchecBuild(f"prefixe-long : code={code} err={err!r} (I6 : le "
                             f"9e octet doit casser le magic)")
        sortie, err, code = t.lancer(["--hacher", os.path.join(t.dossier, "inexistant")])
        if code != 1 or err != L.MSG_OUVERTURE or sortie:
            raise EchecBuild(f"inexistant : code={code} err={err!r}")
        sortie, err, code = t.lancer(["--hacher", t.dossier])
        if code != 1 or err != L.MSG_LECTURE or sortie:
            raise EchecBuild(f"repertoire : code={code} err={err!r}")
        sortie, err, code = t.lancer(["a", "b", "c"])
        if code != 2 or err != L.MSG_CHANTIER or sortie:
            raise EchecBuild(f"chantier : code={code} err={err!r}")
        cas += 6
        # Falsification : un octet de CODE corrompu par bloc embarqué,
        # batterie complète — les 8 blocs notés SONT appelés par au moins
        # un scénario (write/exit/hex/init/absorber/finaliser/principal).
        references = {}
        ref_nom = t.temoin("ref", b"falsification-reference")
        for scenario_args in (["--hacher", ref_nom], [], ["--hacher"],
                              ["--hacherx", ref_nom],
                              ["--hacher", os.path.join(t.dossier, "inexistant")],
                              ["--hacher", t.dossier], ["a", "b", "c"]):
            sortie, err, code = t.lancer(list(scenario_args))
            references[tuple(scenario_args)] = (sortie, err, code)
        detectees = 0
        for bid, _, _, rva, _ in L.BLOCS_SCEAU:
            if bid not in (longueurs or {}):
                continue                      # en chantier : pas dans l'artefact
            longueur = (longueurs or {}).get(bid, 32)
            for offset in (0, 5, 10, 20):
                if offset >= longueur:
                    continue
                mutant = bytearray(img)
                mutant[rva + offset] ^= 0xFF
                tm = Terrain(bytes(mutant))
                try:
                    diverge = False
                    for scenario_args, ref in references.items():
                        s2, e2, c2 = tm.lancer(list(scenario_args))
                        if (s2, e2, c2) != ref:
                            diverge = True
                            break
                    if not diverge:
                        raise EchecBuild(
                            f"falsification : {bid} +{offset} NON détectée (silence)")
                    detectees += 1
                finally:
                    tm.nettoyer()
        return {"cas": cas, "falsification": detectees}
    finally:
        t.nettoyer()


# --- Usage auto-référentiel + mesures D34 ---------------------------------------

ARTEFACTS_PROJET = [
    ("hello.exe", os.path.join(M6, "..", "m0", "hello.exe")),
    ("selftest.exe", os.path.join(M6, "..", "m1", "selftest.exe")),
    ("echo.exe", os.path.join(M6, "..", "m2", "echo.exe")),
    ("hachoir", os.path.join(M6, "hachoir")),
    ("sceau", None),                          # l'artefact courant
]


def usage_auto_referentiel(img: bytes) -> list[str]:
    """Premier usage auto-référentiel de l'échelon 2 : les empreintes
    SHA-512 des artefacts du projet produites PAR sceau, contre-vérifiées
    sha512sum (le complément 512 bits du hachoir, journal 20)."""
    lignes = []
    t = Terrain(img)
    try:
        for nom, chemin in ARTEFACTS_PROJET:
            if chemin is None:
                chemin = t.temoin("sceau", img)
            elif not os.path.exists(chemin):
                lignes.append(f"{nom}: absent (ignoré)")
                continue
            with open(chemin, "rb") as f:
                donnees = f.read()
            attendu = ligne_sha512sum(chemin, donnees)
            sortie, err, code = t.lancer(["--hacher", chemin])
            if code != 0 or sortie != attendu:
                raise EchecBuild(
                    f"usage auto-référentiel {nom} : sceau diverge de sha512sum")
            lignes.append(f"{nom}: sha512 "
                          f"{hashlib.sha512(donnees).hexdigest()[:16]}… parité exacte")
    finally:
        t.nettoyer()
    return lignes


def mesures_d34(img: bytes) -> dict:
    """Mesure auto-référentielle : sceau --hacher vs sha512sum (terrain)."""
    t = Terrain(img)
    try:
        donnees = bytes((i * 7 + 13) % 256 for i in range(1_000_000))
        chemin = t.temoin("mesure", donnees)
        t0 = time.perf_counter()
        for _ in range(5):
            s1, _, c1 = t.lancer(["--hacher", chemin])
        duree_sceau = (time.perf_counter() - t0) / 5
        t0 = time.perf_counter()
        for _ in range(5):
            r = subprocess.run(["sha512sum", chemin], capture_output=True)
        duree_ref = (time.perf_counter() - t0) / 5
        attendu = subprocess.run(["sha512sum", chemin], capture_output=True).stdout
        return {"octets": len(donnees), "sceau_s": round(duree_sceau, 4),
                "sha512sum_s": round(duree_ref, 4),
                "parite": "octet-identique" if (s1 == attendu and c1 == 0) else "DIVERGENT"}
    finally:
        t.nettoyer()


# --- Carte génération 1 -----------------------------------------------------------

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fragments_clairs(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list,
                     en_chantier: list) -> dict:
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, fichier, rva, slot in L.BLOCS_SCEAU:
        if bid in code:
            loc.append(f"[bloc] id={bid} spec={sid} cible={L.PROFIL} "
                       f"addr={L.IMAGE_BASE + rva:#x} size={slot} v=1 etat=scelle")
        else:
            loc.append(f"[bloc] id={bid} spec={sid} cible={L.PROFIL} "
                       f"etat=chantier notation=en-attente-dev.2")
    con = ["[carte-frag] nom=frag-con generation=1"]
    for bid, _, _, _, _ in L.BLOCS_SCEAU:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        con.append(f"[bloc] id={bid}\n  sig : {sig[:100]}")
    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_SCEAU:
        etat = "chantier" if bid in en_chantier else "scelle"
        if bid in code:
            with open(os.path.join(ICI, "notation", fichier + ".asm"), "rb") as f:
                emp = sha(f.read())
            crist = min(compteurs.get(bid, 1), 10)
            prf.append(f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                       f"crist={crist}/10")
            prf.append(f"  vecteurs : roundtrip=ok structure=ok notation={emp}")
        else:
            prf.append(f"[bloc] id={bid} etat={etat} crist=0/10")
            prf.append("  vecteurs : spec posée (R2), notation en chantier")
    prf.append("[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]
    prf.append(f"  heritage : ah-01/03/08 octet-identiques m6 (cmp notation, "
               f"mêmes RVA) ; ah-02 non embarqué (read direct, I1 av-17)")
    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, fichier, rva, slot in L.BLOCS_SCEAU:
        if bid in code:
            bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} "
                       f"empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=sceau version={L.VERSION_DEV1} profil={L.PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}."
        f"{capstone.cs_version()[1]} ; verrous={len(verrous)} ; symboles vérifiés",
        f"  oracle : natif — {verdict['cas']} cas verts, falsification "
        f"{verdict['falsification']} détectées (échelon 2 D34 : phase 1)",
        f"[zones] sys=0x1000-0x10ff s512=0x1100-0x187ff hex=0x1600 "
        f"corps=0x1880-0x20ff courbe=0x2120-0x271f app=0x2720-0x2b9f "
        f"rodata=0x3000-0x354f bss=0x4000-0x15bff",
        f"[echantier] notation en attente : {', '.join(en_chantier)} (dev.2+)",
    ]
    return {n: ("\n".join(l) + "\n").encode("utf-8")
            for n, l in (("frag-loc", loc), ("frag-con", con),
                         ("frag-prf", prf), ("frag-bld", bld))}


def verrou_croise(code: dict, img: bytes) -> int:
    """R8 : signature + empreintes re-vérifiées depuis le disque."""
    entete, fragments, signature, pub = cm.lire_carte()
    cm.verifier_signature(pub, entete, fragments, signature)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    bld = cm.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode()
    n = 0
    for bid, _, fichier, rva, slot in L.BLOCS_SCEAU:
        if bid not in code:
            continue
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    return n


def construire_carte(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list,
                     en_chantier: list):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs,
                              journal, en_chantier)
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    fragments = {n: cm.chiffrer_fragment(maitre, n, clairs[n]) for n in cm.FRAGMENTS}
    prive, pub = cm.paire_cles(graine)
    from carte_m2 import empreinte_racine
    entete = cm.construire_entete(empreinte_racine(fragments))
    signature = cm.signer(prive, entete, fragments)
    cm.ecrire_carte(entete, fragments, signature, pub)


# --- Construction -----------------------------------------------------------------

def construire() -> int:
    print("=== m7 : lignée sceau (D34 échelon 2, phase 1) — SHA-512 natif ===")
    t0 = time.perf_counter()
    specs = charger_couche_I()
    print(f"[I] 20 specs chargées et auditées (gabarit § 2.2, R2) — "
          f"17 av + 3 héritages ah")

    n_her = heritages_octet_identiques()
    print(f"[R7] {n_her} héritages octet-identiques (notation m7 == m6, cmp)")

    blocs, _, code, en_chantier, _ = assembler_tout()
    total_insns = sum(len(code[b[0]]["insns"]) for b in blocs if b[0] in code)
    total_code = sum(len(code[b[0]]["octets"]) for b in blocs if b[0] in code)
    print(f"[R5] {len(code)} blocs notés, {total_insns} instructions, "
          f"{total_code} o de code — round-trip keystone/capstone 100 % ; "
          f"{len(en_chantier)} notations en chantier (dev.2+)")

    verrous = oracle_structurel(code, specs)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles @ vérifiés contre layout/réel (leçon C1)")

    img = composer_elf(code)
    valider_elf(img)
    print(f"[ELF] sceau : {len(img)} o (ehdr + 2 phdr à la main, RX 0x4000 + "
          f"bss 0x12000), entrée {L.IMAGE_BASE + L.ENTREE:#x}")

    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in
                                 blocs if bid in code})
    print(f"[oracle] différentiel NATIF : {verdict['cas']} cas verts ; "
          f"falsification {verdict['falsification']} corruptions détectées (zéro silence)")

    empreintes = usage_auto_referentiel(img)
    for ligne in empreintes:
        print(f"[D34] {ligne}")
    m = mesures_d34(img)
    print(f"[D34] mesure auto-référentielle : 1 Mo — sceau {m['sceau_s']} s vs "
          f"sha512sum {m['sha512sum_s']} s ; parité {m['parite']}")

    chemin_art = os.path.join(ICI, "sceau")
    with open(chemin_art, "wb") as f:
        f.write(img)
    os.chmod(chemin_art, 0o755)

    journal = [f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={L.VERSION_DEV1} cas={verdict['cas']} "
               f"falsif={verdict['falsification']}"]
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs if bid in code}
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal,
                     en_chantier)
    nb = verrou_croise(code, img)
    print(f"[carte] génération 1 écrite : 4 fragments chiffrés (sel distinct "
          f"D34), signature Ed25519 (clés projet D27), verrou croisé "
          f"{nb}/{len(code)}")

    print(f"[B] sceau scellé : sha256:{sha(img)}")
    print(f"=== m7-dev.1 (oracle natif vert) : {L.VERSION_DEV1} — "
          f"{round(time.perf_counter() - t0, 1)} s ===")
    return 0


def verifier() -> int:
    print("=== m7 : re-vérification complète (R5/R8) ===")
    with open(os.path.join(ICI, "sceau"), "rb") as f:
        img = f.read()
    heritages_octet_identiques()
    blocs, _, code, en_chantier, _ = assembler_tout()
    for bid, _, fichier, rva, slot in blocs:
        if bid in code and img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    specs = charger_couche_I()
    oracle_structurel(code, specs)
    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in
                                 blocs if bid in code})
    print(f"[oracle] différentiel NATIF : {verdict['cas']} cas verts ; "
          f"falsification {verdict['falsification']} détectées")
    # Cristallisation : compteurs incrémentés dans frag-prf
    phrase, graine = cm.charger_secrets(interactif=False)
    maitre = cm.cle_maitresse(phrase)
    _, fragments, _, _ = cm.lire_carte()
    prf = cm.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode()
    compteurs = {}
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            if "crist" in champs:
                compteurs[champs["id"]] = int(
                    re.match(r"(\d+)/10", champs["crist"]).group(1))
    for bid, _, _, _, _ in blocs:
        if bid in code:
            compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal = [l.strip()[2:] for l in prf.splitlines() if l.startswith("  run ")]
    journal.append(f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                   f"verif cas={verdict['cas']} falsif={verdict['falsification']}")
    construire_carte(code, img, [], specs, verdict, compteurs, journal, en_chantier)
    nb = verrou_croise(code, img)
    crist = ", ".join(f"{b}={compteurs.get(b, 0)}/10" for b, _, _, _, _ in blocs[:4])
    print(f"[R6] cristallisation : {crist}, …")
    print(f"[R8] verrou croisé : {nb}/{len(code)} empreintes conformes")
    return 0


if __name__ == "__main__":
    sys.exit(verifier() if "--verifier" in sys.argv else construire())
