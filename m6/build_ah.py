#!/usr/bin/env python3
"""build_ah.py — Lignée auto-hôte (m6, D34 échelon 1) : hachoir, SHA-256 natif.

Notation (keystone) -> octets -> ELF64 À LA MAIN (ehdr 64 o + 2 phdr 56 o,
aucun outil de liaison) -> carte auto-hôte génération 1. L'agent utilise
TRIADE pour son propre travail : cet artefact REMPLACE sha256sum dans la
chaîne de l'agent, et l'oracle différentiel s'exécute SUR LE TERRAIN NATIF —
l'échelon 1 de D34 : les outils de l'agent tournent en code machine nu sur
sa propre machine (le bac à sable Linux x86-64).

Chaîne (le protocole s'applique intégralement, profil inversé) :
  1. couche I chargée et auditée (gabarit § 2.2, 9 specs, R2 écrite-avant-code) ;
  2. round-trip R5 par bloc (keystone -> capstone -> keystone, WYSIWYG octets) ;
  3. oracle structurel : contrats I vérifiés sur le code désassemblé — appels
     directs autorisés PAR BLOC, numéros de syscall autorisés PAR BLOC (I1),
     cibles RIP déclarées, sauts internes aux frontières, padding >= 16,
     feuille ah-08, symboles @ des brouillons confrontés à layout.py ET les
     longueurs @L_* confrontées aux messages RÉELS (leçon C1 : l'arithmétique
     de l'auteur est vérifiée par la machine, jamais crue) ;
  4. composition ELF64 : ehdr + phdr RX (RVA == offset fichier) + phdr RW
     (.bss pur, filesz 0), code aux slots, NOP intra-slot, int3 réserves ;
  5. oracle différentiel NATIF : vecteurs dorés FIPS 180-4 (vide, « abc »,
     448 bits, un million de 'a'), tailles de transition (0, 1, 55, 56, 63,
     64, 65, 127, 128, 1000, 65535, 65536, 65537, 131072) — la ligne émise
     est octet-identique à « <hashlib>  <chemin>\\n », code 0 ;
  6. chemins d'échec : usage / inexistant / répertoire — messages exacts sur
     stderr, code 1 (V3) ;
  7. falsification : un octet corrompu dans le CODE de chaque bloc, batterie
     complète (nominal + 3 échecs) — au MOINS une divergence, zéro silence ;
  8. carte génération 1 auto-hôte (sel Argon2id distinct D34, clés projet
     partagées D27, signature Ed25519, verrou croisé R8).

Usage :
  python3 build_ah.py             # construction + oracle natif + carte
  python3 build_ah.py --verifier  # re-vérification complète (R5/R8) + cristallisation
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
import carte_ah as cm                     # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(ICI), "m2"))
from carte_m2 import empreinte_racine     # noqa: E402  (mécanique commune D27)


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
    specs = {}
    for bid, sid, fichier, _, _ in L.BLOCS_AH:
        chemin = os.path.join(ICI, "I", fichier + ".md")
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


def assembler_tout() -> tuple[list, dict, dict, list]:
    specs = charger_couche_I()
    code, verrous = {}, []
    for bid, sid, fichier, rva, slot in L.BLOCS_AH:
        code[bid] = assembler_bloc(fichier, rva, slot)
        code[bid]["spec"] = sid
        code[bid]["fichier"] = fichier
        code[bid]["rva"] = rva
        code[bid]["slot_taille"] = slot
    return list(L.BLOCS_AH), specs, code, verrous


# --- Oracle structurel : contrats I sur le code désassemblé --------------------

A_ECRITE, A_LIRE, A_SORTIR = L.A_ECRITE, L.A_LIRE, L.A_SORTIR
A_INIT, A_COMPRIMER, A_ABSORBER = L.A_INIT, L.A_COMPRIMER, L.A_ABSORBER
A_FINALISER, A_HEX = L.A_FINALISER, L.A_HEX

APPELS_AUTORISES = {          # I1/I2 des specs : appels directs par bloc
    "d40006": {A_COMPRIMER},
    "d40007": {A_COMPRIMER},
    "d40009": {A_ECRITE, A_SORTIR, A_INIT, A_ABSORBER, A_FINALISER, A_HEX},
}
SYSCALLS_AUTORISES = {        # I1 : numéros de syscall par bloc (EABI x86-64)
    "d40001": {1},            # write
    "d40002": {0},            # read
    "d40003": {60},           # exit
    "d40009": {0, 2, 3},      # read, open, close (I1 de ah-09)
}
DONNEES_RIP = {               # I1/I3 : cibles RIP de données par bloc
    "d40005": {L.R_K},
    "d40008": {L.R_HEXCHARS},
    "d40009": {L.R_CTX, L.R_DIGEST, L.R_LIGNE, L.R_TAMPON,
               L.R_MSG_USAGE, L.R_MSG_OUVERTURE, L.R_MSG_LECTURE, L.R_MSG_ECRITURE},
}


def cible_rip(insn) -> int | None:
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", insn.op_str)
    if not m:
        return None
    disp = int(m.group(2), 16)
    return insn.address + insn.size + (disp if m.group(1) == "+" else -disp)


def _prologue_aligne_sysv(insns) -> bool:
    """(8 + 8*npush - sub) ≡ 0 mod 16 — pile alignée aux points d'appel SysV.
    Sans sous-cadre (sub absent), l'alignement vient des seuls pushes."""
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
        if bid != "d40009":
            verrou(f"{bid}:pile-alignee", _prologue_aligne_sysv(insns))
        else:
            verrou(f"{bid}:start-sans-push",
                   not any(i.mnemonic == "push" for i in insns))
        # Feuille ah-08 : aucun appel, aucun push (I2)
        if bid == "d40008":
            verrou("d40008:feuille",
                   not any(i.mnemonic in ("call", "push") for i in insns))
    return verrous


# --- Symboles des brouillons confrontés au layout (leçon C1) -------------------

_MESSAGES = {"L_USAGE": L.MSG_USAGE, "L_OUVERTURE": L.MSG_OUVERTURE,
             "L_LECTURE": L.MSG_LECTURE, "L_ECRITURE": L.MSG_ECRITURE}


def verifier_symboles() -> int:
    """Chaque @symbole du brouillon doit valoir la constante layout/longueur
    réelle — l'arithmétique de l'auteur est VÉRIFIÉE, jamais crue (C1)."""
    n = 0
    attendus = {"A_ECRITE": L.A_ECRITE, "A_LIRE": L.A_LIRE, "A_SORTIR": L.A_SORTIR,
                "A_INIT": L.A_INIT, "A_COMPRIMER": L.A_COMPRIMER,
                "A_ABSORBER": L.A_ABSORBER, "A_FINALISER": L.A_FINALISER,
                "A_HEX": L.A_HEX,
                "k": L.R_K, "R_K": L.R_K,        # @k : nom spec de la table FIPS
                "R_HEXCHARS": L.R_HEXCHARS, "R_CTX": L.R_CTX,
                "R_DIGEST": L.R_DIGEST, "R_LIGNE": L.R_LIGNE, "R_TAMPON": L.R_TAMPON,
                "R_MSG_USAGE": L.R_MSG_USAGE, "R_MSG_OUVERTURE": L.R_MSG_OUVERTURE,
                "R_MSG_LECTURE": L.R_MSG_LECTURE, "R_MSG_ECRITURE": L.R_MSG_ECRITURE}
    for _, _, fichier, _, _ in L.BLOCS_AH:
        chemin = os.path.join(ICI, "notation", "brouillons", fichier + ".asm")
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
                else:
                    raise EchecBuild(f"{fichier} : symbole inconnu @{nom}")
                if val != attendu:
                    raise EchecBuild(
                        f"{fichier} : @{nom} = {val:#x} mais layout/réel = {attendu:#x} "
                        f"(leçon C1 : l'arithmétique de l'auteur est vérifiée)")
                n += 1
    return n


# --- Composition ELF64 ----------------------------------------------------------

K_FIPS = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
    0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
    0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
    0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
    0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
    0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]


def composer_elf(code: dict) -> bytes:
    """Image RX complète : ehdr + 2 phdr + int3 + slots + rodata (RVA == offset)."""
    img = bytearray(b"\xcc" * L.RX_TAILLE)      # réserves int3 par défaut

    def poser(rva: int, donnees: bytes, nom: str = ""):
        poses.append((rva, rva + len(donnees), nom or hex(rva)))
        if rva + len(donnees) > L.RX_TAILLE:
            raise EchecBuild(f"segment RX débordant à {rva:#x}")
        img[rva: rva + len(donnees)] = donnees

    poses: list[tuple[int, int, str]] = []       # garde-fou chevauchement (C1)
    for bid, _, _, rva, slot in L.BLOCS_AH:
        poser(rva, code[bid]["slot"], bid)
    poser(L.R_K, b"".join(struct.pack("<I", k) for k in K_FIPS), "R_K")
    for rva, donnees, nom in ((L.R_HEXCHARS, L.HEXCHARS, "HEXCHARS"),
                              (L.R_MSG_USAGE, L.MSG_USAGE, "MSG_USAGE"),
                              (L.R_MSG_OUVERTURE, L.MSG_OUVERTURE, "MSG_OUVERTURE"),
                              (L.R_MSG_LECTURE, L.MSG_LECTURE, "MSG_LECTURE"),
                              (L.R_MSG_ECRITURE, L.MSG_ECRITURE, "MSG_ECRITURE")):
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
        raise EchecBuild(f"e_entry {e_entry:#x} != slot ah-09")
    for rva, attendu in ((L.R_K, K_FIPS), (L.R_HEXCHARS, L.HEXCHARS)):
        if img[rva:rva + len(attendu) * (4 if rva == L.R_K else 1)] != (
                b"".join(struct.pack("<I", k) for k in attendu) if rva == L.R_K
                else attendu):
            raise EchecBuild(f"fixture .rodata @ {rva:#x} divergente")


# --- Oracle différentiel NATIF (échelon 1 : le terrain est la vérité) -----------

class Terrain:
    """Exécution native de hachoir — le terrain de l'agent est son propre banc."""

    def __init__(self, img: bytes):
        parent = os.path.join(ICI, ".tmp")
        os.makedirs(parent, exist_ok=True)          # mkdtemp ne crée pas le parent
        self.dossier = tempfile.mkdtemp(prefix="hachoir-", dir=parent)
        self.chemin = os.path.join(self.dossier, "hachoir")
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
            r = sp.run([self.chemin] + args, capture_output=True, timeout=30)
            return r.stdout, r.stderr, r.returncode
        except sp.TimeoutExpired:
            # Un mutant qui pend (boucle infinie) EST une divergence détectée —
            # code sentinel -99, jamais confondu avec un comportement sain.
            return b"", b"<timeout>", -99

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


def ligne_sha256sum(chemin: str, donnees: bytes) -> bytes:
    """Référent hashlib au format sha256sum — le diff est la preuve."""
    return f"{hashlib.sha256(donnees).hexdigest()}  {chemin}\n".encode()


def oracle_natif(img: bytes, longueurs: dict[str, int] | None = None) -> dict:
    t = Terrain(img)
    try:
        cas = 0
        # Vecteurs dorés FIPS 180-4 + tailles de transition
        vecteurs = [
            ("fips-vide", b""),
            ("fips-abc", b"abc"),
            ("fips-448", b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"),
            ("million-a", b"a" * 1_000_000),
        ] + [(f"t{n}", bytes((i * 31 + n) % 256 for i in range(n)))
             for n in (1, 55, 56, 63, 64, 65, 127, 128, 1000,
                       65535, 65536, 65537, 131072)]
        for nom, donnees in vecteurs:
            chemin = t.temoin(nom, donnees)
            attendu = ligne_sha256sum(chemin, donnees)
            sortie, err, code = t.lancer([chemin])
            if code != 0 or sortie != attendu or err:
                raise EchecBuild(
                    f"oracle natif {nom} : code={code} sortie={sortie!r} "
                    f"attendu={attendu!r} err={err!r}")
            cas += 1
        # Chemins d'échec (V3)
        sortie, err, code = t.lancer([])
        if code != 1 or err != L.MSG_USAGE or sortie:
            raise EchecBuild(f"usage : code={code} err={err!r}")
        sortie, err, code = t.lancer([os.path.join(t.dossier, "inexistant")])
        if code != 1 or err != L.MSG_OUVERTURE or sortie:
            raise EchecBuild(f"inexistant : code={code} err={err!r}")
        sortie, err, code = t.lancer([t.dossier])
        if code != 1 or err != L.MSG_LECTURE or sortie:
            raise EchecBuild(f"repertoire : code={code} err={err!r}")
        cas += 3
        # Falsification : un octet de CODE corrompu par bloc, batterie complète.
        # d40002 (ah-02) est EXCLU de la batterie artefact : jamais appelé par
        # hachoir (ah-09 I1 : read direct) — indétectable par l'artefact PAR
        # CONSTRUCTION ; falsifié au niveau bloc (falsifier_bloc_non_appel).
        references = {}
        ref_nom = t.temoin("ref", b"falsification-reference")
        for scenario_args in ([ref_nom], [], [os.path.join(t.dossier, "inexistant")],
                              [t.dossier]):
            sortie, err, code = t.lancer(scenario_args)
            references[tuple(scenario_args)] = (sortie, err, code)
        detectees = 0
        for bid, _, _, rva, _ in L.BLOCS_AH:
            if bid == "d40002":
                continue          # non appelé — falsification bloc-niveau ci-dessous
            longueur = (longueurs or {}).get(bid, 32)
            for offset in (0, 5, 10):
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
        detectees += falsifier_bloc_non_appel(img, L.A_LIRE,
                                              (longueurs or {}).get("d40002", 5))
        return {"cas": cas, "falsification": detectees}
    finally:
        t.nettoyer()


def falsifier_bloc_non_appel(img: bytes, rva: int, longueur: int) -> int:
    """Falsification BLOC-NIVEAU pour un bloc jamais appelé par l'artefact
    (d40002 : ah-09 fait ses read directement, spec I1) — indétectable par
    l'artefact PAR CONSTRUCTION. Appel direct sous Unicorn avec crochet
    syscall : toute corruption d'un octet de CODE diverge (crash, mauvais
    numéro, ou non-retour) — zéro silence, la couverture reste intégrale."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UcError, UC_HOOK_INSN
    from unicorn.x86_const import (UC_X86_INS_SYSCALL,
                                   UC_X86_REG_RAX, UC_X86_REG_RDI,
                                   UC_X86_REG_RSI, UC_X86_REG_RDX,
                                   UC_X86_REG_RSP)
    base, pile, sent = L.IMAGE_BASE, 0x7ffe0000, 0xfeedfacefeedface
    detectees = 0
    for offset in range(longueur):           # CHAQUE octet de code, pas un échantillon
        mutant = bytearray(img)
        mutant[rva + offset] ^= 0xFF
        uc = Uc(UC_ARCH_X86, UC_MODE_64)
        uc.mem_map(base, 0x5000)
        uc.mem_map(pile, 0x2000)
        uc.mem_write(base, bytes(mutant))
        nrs: list[int] = []

        def crochet(uc_, *_):
            nrs.append(uc_.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFFFFFFFFFF)
            uc_.reg_write(UC_X86_REG_RAX, 1)      # retour de read simulé
        uc.hook_add(UC_HOOK_INSN, crochet, None, 1, 0, UC_X86_INS_SYSCALL)
        uc.reg_write(UC_X86_REG_RDI, 3)
        uc.reg_write(UC_X86_REG_RSI, base + 0x4300)
        uc.reg_write(UC_X86_REG_RDX, 16)
        uc.reg_write(UC_X86_REG_RSP, pile + 0x1000 - 8)
        uc.mem_write(pile + 0x1000 - 8, sent.to_bytes(8, "little"))
        try:
            uc.emu_start(base + rva, sent, count=1000)
            sain = (nrs == [0])                  # un seul syscall, nr = read
        except UcError:
            sain = False                          # crash = divergence détectée
        if sain:
            raise EchecBuild(
                f"falsification bloc-niveau : {rva:#x} +{offset} NON détectée (silence)")
        detectees += 1
    return detectees


# --- Mesures D34 : l'agent mesure son propre outil ------------------------------

def mesures_d34(img: bytes) -> dict:
    """Première mesure auto-référentielle : hachoir vs sha256sum (terrain)."""
    t = Terrain(img)
    try:
        donnees = bytes((i * 7 + 13) % 256 for i in range(1_000_000))
        chemin = t.temoin("mesure", donnees)
        t0 = time.perf_counter()
        for _ in range(5):
            s1, _, c1 = t.lancer([chemin])
        duree_hachoir = (time.perf_counter() - t0) / 5
        t0 = time.perf_counter()
        for _ in range(5):
            r = subprocess.run(["sha256sum", chemin], capture_output=True)
        duree_ref = (time.perf_counter() - t0) / 5
        attendu = subprocess.run(["sha256sum", chemin], capture_output=True).stdout
        return {"octets": len(donnees), "hachoir_s": round(duree_hachoir, 4),
                "sha256sum_s": round(duree_ref, 4),
                "parite": "octet-identique" if (s1 == attendu and c1 == 0) else "DIVERGENT"}
    finally:
        t.nettoyer()


# --- Carte génération 1 -----------------------------------------------------------

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fragments_clairs(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list) -> dict:
    loc = ["[carte-frag] nom=frag-loc generation=1"]
    for bid, sid, fichier, rva, slot in L.BLOCS_AH:
        loc.append(f"[bloc] id={bid} spec={sid} cible={L.PROFIL} "
                   f"addr={L.IMAGE_BASE + rva:#x} size={slot} v=1 etat=scelle")
    con = ["[carte-frag] nom=frag-con generation=1"]
    for bid in code:
        spec = specs[bid]["texte"]
        sig = re.search(r"Intention : (.+?)\n", spec).group(1)
        con.append(f"[bloc] id={bid}\n  sig : {sig[:100]}")
    prf = ["[carte-frag] nom=frag-prf generation=1"]
    for bid, _, fichier, _, _ in L.BLOCS_AH:
        with open(os.path.join(ICI, "notation", fichier + ".asm"), "rb") as f:
            emp = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} "
                f"crist={crist}/10",
                f"  vecteurs : roundtrip=ok structure=ok notation={emp}",
                f"  differentiel : natif ok ({verdict['cas']} cas, "
                f"falsification {verdict['falsification']})"]
    prf.append("[verifications] runs=" + str(len(journal)))
    prf += ["  " + r for r in journal[-12:]]
    bld = ["[carte-frag] nom=frag-bld generation=1"]
    for bid, _, fichier, rva, slot in L.BLOCS_AH:
        bld.append(f"[bloc] id={bid} addr={L.IMAGE_BASE + rva:#x} "
                   f"empreinte={sha(code[bid]['slot'])}")
    bld += [
        f"[build] artefact=hachoir version={L.VERSION_DEV1} profil={L.PROFIL} "
        f"taille={len(img)} empreinte={sha(img)}",
        f"  outils : keystone + capstone {capstone.cs_version()[0]}."
        f"{capstone.cs_version()[1]} ; verrous={len(verrous)} ; symboles vérifiés",
        f"  oracle : natif — {verdict['cas']} cas verts, falsification "
        f"{verdict['falsification']} détectées (échelon 1 D34 : terrain = vérité)",
        f"[zones] sys=0x1000-0x10ff sha=0x1100-0x15ff hex=0x1600-0x167f "
        f"app=0x1680-0x187f rodata=0x2000-0x21ff bss=0x3000-0x142ff",
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
    for bid, _, fichier, rva, slot in L.BLOCS_AH:
        m = re.search(rf"\[bloc\] id={bid} addr=\S+ empreinte=(\S+)", bld)
        if not m or m.group(1) != sha(img[rva:rva + slot]):
            raise EchecBuild(f"verrou croisé : {bid} divergent (R8)")
        n += 1
    return n


def construire_carte(code: dict, img: bytes, verrous: list, specs: dict,
                     verdict: dict, compteurs: dict, journal: list):
    clairs = fragments_clairs(code, img, verrous, specs, verdict, compteurs, journal)
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
    print("=== m6 : lignée auto-hôte (D34 échelon 1) — hachoir, SHA-256 natif ===")
    t0 = time.perf_counter()
    specs = charger_couche_I()
    print(f"[I] 9 specs chargées et auditées (gabarit § 2.2, R2)")

    blocs, _, code, _ = assembler_tout()
    total_insns = sum(len(code[b[0]]["insns"]) for b in blocs)
    total_code = sum(len(code[b[0]]["octets"]) for b in blocs)
    print(f"[R5] 9 blocs, {total_insns} instructions, {total_code} o de code — "
          f"round-trip keystone/capstone 100 %")

    verrous = oracle_structurel(code, specs)
    n_symboles = verifier_symboles()
    print(f"[oracle] structurel : {len(verrous)} verrous PASS ; "
          f"{n_symboles} symboles @ vérifiés contre layout/réel (leçon C1)")

    img = composer_elf(code)
    valider_elf(img)
    print(f"[ELF] hachoir : {len(img)} o (ehdr + 2 phdr à la main, RX 0x3000 + "
          f"bss 0x11300), entrée {L.IMAGE_BASE + L.ENTREE:#x}")

    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
    print(f"[oracle] différentiel NATIF : {verdict['cas']} cas verts ; "
          f"falsification {verdict['falsification']} corruptions détectées (zéro silence)")
    m = mesures_d34(img)
    print(f"[D34] mesure auto-référentielle : 1 Mo — hachoir {m['hachoir_s']} s vs "
          f"sha256sum {m['sha256sum_s']} s ; parité {m['parite']}")

    chemin_art = os.path.join(ICI, "hachoir")
    with open(chemin_art, "wb") as f:
        f.write(img)
    os.chmod(chemin_art, 0o755)

    journal = [f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={L.VERSION_DEV1} cas={verdict['cas']} "
               f"falsif={verdict['falsification']}"]
    compteurs = {bid: 1 for bid, _, _, _, _ in blocs}
    construire_carte(code, img, verrous, specs, verdict, compteurs, journal)
    nb = verrou_croise(code, img)
    print(f"[carte] génération 1 auto-hôte écrite : 4 fragments chiffrés "
          f"(sel distinct D34), signature Ed25519 (clés projet D27), "
          f"verrou croisé {nb}/9")

    print(f"[B] hachoir scellé : sha256:{sha(img)}")
    print(f"=== m6-dev (oracle natif vert) : {L.VERSION_DEV1} — "
          f"{round(time.perf_counter() - t0, 1)} s ===")
    return 0


def verifier() -> int:
    print("=== m6 : re-vérification complète (R5/R8) ===")
    with open(os.path.join(ICI, "hachoir"), "rb") as f:
        img = f.read()
    blocs, _, code, _ = assembler_tout()
    for bid, _, fichier, rva, slot in blocs:
        if img[rva:rva + slot] != code[bid]["slot"]:
            raise EchecBuild(f"{bid} : notation et artefact divergent (R5)")
    specs = charger_couche_I()
    oracle_structurel(code, specs)
    verdict = oracle_natif(img, {bid: len(code[bid]["octets"]) for bid, _, _, _, _ in blocs})
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
            compteurs[champs["id"]] = int(
                re.match(r"(\d+)/10", champs.get("crist", "1/10")).group(1))
    for bid, _, _, _, _ in blocs:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal = [l.strip() for l in prf.splitlines() if l.startswith("  run ")]
    journal.append(f"run natif date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                   f"verif cas={verdict['cas']} falsif={verdict['falsification']}")
    construire_carte(code, img, [], specs, verdict, compteurs, journal)
    nb = verrou_croise(code, img)
    crist = ", ".join(f"{b}={compteurs.get(b, 0)}/10" for b, _, _, _, _ in blocs[:4])
    print(f"[R6] cristallisation : {crist}, …")
    print(f"[R8] verrou croisé : {nb}/9 empreintes conformes")
    return 0


if __name__ == "__main__":
    sys.exit(verifier() if "--verifier" in sys.argv else construire())
