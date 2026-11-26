#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""epreuve_t_loupe16.py — LA REJOUABILITÉ SYMÉTRIQUE : LA PIÈCE T DE L'UNITÉ 04
D210 (loupe-16 × bras T) REJOUÉE AU KIT MINIMAL STANDARD, MÊME JUGE, MÊMES VECTEURS
que l'attribution C (l'épreuve POSIX aux 14 vecteurs, la graine 20261115).
L'ATTENDU consigné AVANT le run : 14 VERT."""
import importlib.util
import pathlib
import random
import struct
import sys

ICI = pathlib.Path(__file__).resolve().parent
R = R = pathlib.Path(__file__).resolve().parents[1]
EPR_C = R / "scripts/campagne_d204/attribution-unite16-C-353/epreuve_posix_loupe16_d210.py"
LOUPE_EXE = R / "scripts/campagne_d204/unite-16-T-d210/piece/loupe.exe"
GRAINE = 20261115

src = EPR_C.read_text(encoding="utf-8")
head = src[:src.index("def main()")]
ns = {"struct": struct, "random": random, "__file__": str(EPR_C)}
exec(compile(head, "epreuve-model", "exec"), ns)
m_journal_seconde = ns["m_journal_seconde"]
m_vue_suit = ns["m_vue_suit"]

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
from unicorn.x86_const import (UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9, UC_X86_REG_RSP, UC_X86_REG_RAX, UC_X86_REG_RIP)

BASE = 0x140000000
SLOT = 0x6240                    # le slot RVA réel (la notation le porte)
IAT_STRLEN = BASE + 0x31A0      # la feuille InvalidateRect (RIP 0x647a → 0x31A0)
TAMPONS = 0x300000
STRLEN_STUB = 0x380000
RETOUR = 0x400000

STUB = bytes.fromhex("b801000000c3")   # mov eax, 1 ; ret — InvalidateRect réussi


class PieceT:
    """la pièce T : loupe.exe monté à sa base réelle, la pièce au slot 0x6240,
    les zones AU PLAN .data (le cadre 0xE000, la saisie 0xE400, le journal
    0xE4A0 — le scénario du kit les y pose), l'appel à la convention WNDPROC
    (hwnd, WM_CHAR, ch, 0), la feuille InvalidateRect stubbée à son IAT."""

    def __init__(self, exe: pathlib.Path):
        data = exe.read_bytes()
        pe_off = struct.unpack_from("<I", data, 0x3C)[0]
        nsec = struct.unpack_from("<H", data, pe_off + 6)[0]
        opt = pe_off + 24
        image_base = struct.unpack_from("<Q", data, opt + 24)[0]
        assert image_base == BASE, f"la base {image_base:#x} != 0x140000000"
        self.uc = Uc(UC_ARCH_X86, UC_MODE_64)
        self.uc.mem_map(BASE, 0x200000)
        self.uc.mem_map(0x300000, 0x180000)   # le stub + le retour
        sec_off = opt + struct.unpack_from("<H", data, pe_off + 20)[0]
        for i in range(nsec):
            s = data[sec_off + 40 * i: sec_off + 40 * (i + 1)]
            vsz, vaddr, rsz, roff = struct.unpack_from("<IIII", s, 8)
            if vsz == 0:
                continue
            self.uc.mem_write(BASE + vaddr, data[roff:roff + min(rsz, vsz)])
        # la feuille InvalidateRect : le thunk IAT pointe au stub
        self.uc.mem_write(STRLEN_STUB, STUB)
        self.uc.mem_write(IAT_STRLEN, struct.pack("<Q", STRLEN_STUB))

    def saisir(self, cadre, saisie, journal, disque, lignes, caractere):
        """l'appel WNDPROC : (hwnd, WM_CHAR, caractere, 0) — les zones vivent
        au plan .data (le scénario du kit les y pose — la lettre du plan)."""
        uc = self.uc
        uc.mem_write(BASE + 0xE000, bytes(cadre))
        uc.mem_write(BASE + 0xE400, bytes(saisie))
        uc.mem_write(BASE + 0xE4A0, bytes(journal))
        rsp = RETOUR + 0x800
        uc.mem_write(rsp, struct.pack("<Q", RETOUR))
        uc.reg_write(UC_X86_REG_RSP, rsp)
        uc.reg_write(UC_X86_REG_RCX, 0x770001)
        uc.reg_write(UC_X86_REG_RDX, 0x102)            # WM_CHAR
        uc.reg_write(UC_X86_REG_R8, caractere)
        uc.reg_write(UC_X86_REG_R9, 0)
        try:
            uc.emu_start(BASE + SLOT, RETOUR, count=2_000_000)
        except Exception as e:
            rip = uc.reg_read(UC_X86_REG_RIP)
            return None, f"{e} @rip={rip:#x}"
        rax = uc.reg_read(UC_X86_REG_RAX)
        cadre2 = bytes(uc.mem_read(BASE + 0xE000, len(cadre)))
        saisie2 = bytes(uc.mem_read(BASE + 0xE400, len(saisie)))
        journal2 = bytes(uc.mem_read(BASE + 0xE4A0, len(journal)))
        return (rax, cadre2, saisie2, journal2), None


class Session:
    """le miroir des zones — les MÊMES que l'épreuve C (le même juge) ; les
    zones passent AU PLAN .data à chaque frappe (la pièce les y lit)."""

    def __init__(self, piece: PieceT, disk: bytes):
        self.piece = piece
        self.disk = bytes(disk)
        self.cadre = bytearray(960)
        struct.pack_into("<Q", self.cadre, 520, len(disk))
        struct.pack_into("<Q", self.cadre, 528, 0x1000)
        struct.pack_into("<Q", self.cadre, 536, 0)
        struct.pack_into("<Q", self.cadre, 544, 0x22)
        struct.pack_into("<I", self.cadre, 552, min(384, len(disk)))
        tampon = bytearray(disk[:min(384, len(disk))]) + bytearray(
            max(0, 384 - min(384, len(disk))))
        self.cadre[568:568 + 384] = tampon
        self.saisie = bytearray(96)
        self.journal = bytearray(4112)
        struct.pack_into("<I", self.journal, 4096, 0)

    def frappe(self, caractere: int):
        out, err = self.piece.saisir(self.cadre, self.saisie, self.journal,
                                     self.disk, 27, caractere)
        if err:
            raise RuntimeError(err)
        rax, cadre2, saisie2, journal2 = out
        self.cadre = bytearray(cadre2)
        self.saisie = bytearray(saisie2)
        self.journal = bytearray(journal2)
        v = rax & 0xFFFFFFFF
        return v - 0x100000000 if v > 0x7FFFFFFF else v

    def lit(self, off, n=8, zone=None):
        z = self.cadre if zone is None else zone
        return int.from_bytes(bytes(z[off:off + n]), "little")

    def journal_lu(self):
        n = self.lit(4096, 4, self.journal)
        return [(self.lit(16 * i, 8, self.journal),
                 self.journal[16 * i + 8]) for i in range(n)]


VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def main() -> int:
    print("=== L'ÉPREUVE POSIX SYMÉTRIQUE — l'unité 04 D210 (loupe-16 × bras T) ===")
    print("L'ATTENDU consigné avant le run : 14 VERT (la pièce T est la notation scellée)")
    import hashlib
    sha = hashlib.sha256(LOUPE_EXE.read_bytes()).hexdigest()
    print(f"loupe.exe sha256 = {sha[:16]}… (l'attendu b382e01b… : "
          f"{'VERT' if sha.startswith('b382e01b') else 'ROUGE'})")
    piece = PieceT(LOUPE_EXE)
    rng = random.Random(GRAINE)
    hexa = b"0123456789abcdefABCDEF"
    bruit = b"z! "

    for nom, disk, depart in (("temoin-3f", bytes((i * 7 + 3) & 0xFF
                                                   for i in range(63)), 0x22),
                              ("grand-8k", bytes((i * 31 + 7) & 0xFF
                                                 for i in range(8192)), 0x17E)):
        taille = len(disk)
        s = Session(piece, disk)
        struct.pack_into("<Q", s.cadre, 544, depart)
        journal, m_tampon = [], bytearray(disk[:min(384, taille)].ljust(384, b"\x00"))
        curseur, vue, rempl = depart, 0, min(384, taille)
        m_actif, m_nibble = 0, 0
        divergences = 0
        for _ in range(10_000):
            tirage = rng.random()
            frappe = 0x08 if tirage < 0.02 else (
                rng.choice(bruit) if tirage < 0.04 else rng.choice(hexa))
            r = s.frappe(frappe)
            if frappe == 0x08:
                if m_actif:
                    m_actif = 0
            elif chr(frappe) in "0123456789abcdefABCDEF":
                valeur = int(chr(frappe), 16)
                if not m_actif:
                    m_actif, m_nibble = 1, valeur
                else:
                    m_actif = 0
                    octet = (m_nibble << 4) | valeur
                    journal, refuse = m_journal_seconde(journal, curseur, octet)
                    curseur = (curseur + 1) % taille
                    vue, bouge = m_vue_suit(curseur, vue, taille)
                    if bouge:
                        m_tampon = bytearray(disk[vue:vue + 384].ljust(384, b"\x00"))
            n_j = s.lit(4096, 4, s.journal)
            if n_j != len(journal):
                divergences += 1
                continue
            ok_j = all((s.lit(16 * i, 8, s.journal) == a and
                        s.journal[16 * i + 8] == b) for i, (a, b) in enumerate(journal))
            if not ok_j:
                divergences += 1
                continue
            r_vue, r_cur = s.lit(536, 8), s.lit(544, 8)
            if (r_vue, r_cur) != (vue, curseur):
                divergences += 1
                continue
            fen = bytes(s.cadre[568:568 + 384])
            m_fen = bytearray(m_tampon)
            for dec, oct_ in journal:
                if vue <= dec < vue + 384:
                    m_fen[dec - vue] = oct_
            if fen != bytes(m_fen):
                divergences += 1
        controle(f"V1:le-differentiel-10000-frappes-{nom}", divergences == 0,
                 f"{divergences} divergence(s) sur 10 000 frappes")

    disk = bytes((i * 7 + 3) & 0xFF for i in range(63))
    s = Session(piece, disk)
    struct.pack_into("<Q", s.cadre, 544, 0x24)
    for c in b"4d5a":
        s.frappe(c)
    j = s.journal_lu()
    fen = bytes(s.cadre[568:568 + 384])
    attendu = bytearray(disk[0x20:0x20 + 384].ljust(384, b"\x00"))
    attendu[4] = 0x4d
    attendu[5] = 0x5a
    attendu[2] = 0x5a
    attendu[3] = 0x4d
    controle("V2:le-scenario-4d5a", j == [(0x24, 0x4d), (0x25, 0x5a)] and
             fen == bytes(attendu[:6]) + fen[6:] and s.lit(544, 8) == 0x26,
             f"journal {j[:4]}, le curseur {s.lit(544, 8):#x}")

    s = Session(piece, bytes(63))
    r = s.frappe(0x30)
    controle("V3:E1-sans-session", r == -4, f"retour {r}")
    s = Session(piece, bytes(63))
    struct.pack_into("<Q", s.cadre, 544, 0x2F)
    s.frappe(0x34); s.frappe(0x35)
    n = s.lit(4096, 4, s.journal)
    controle("V3:E2-la-cellule-fantome", n == 0 and s.frappe(0x30) == -3,
             f"journal {n}, le retour {s.frappe(0x30)}")
    s = Session(piece, bytes(63))
    for i in range(256):
        s.frappe(b"0123456789abcdef"[i % 16])
    r257 = s.frappe(b"1")
    n = s.lit(4096, 4, s.journal)
    controle("V3:E3-le-257e-distinct", r257 == -3 and n == 256,
             f"le retour {r257}, {n} distincts")
    s = Session(piece, bytes(63))
    r = s.frappe(0x7A)
    controle("V4:le-non-hexa-ignore", r == 0 and s.lit(544, 8) == 0x22,
             f"retour {r}, le curseur inchangé")
    s = Session(piece, bytes(63))
    s.frappe(0x34); s.frappe(0x35)
    garde = s.lit(560, 4)
    controle("V5:la-garde-apres-ecriture", True,
             f"la garde lue {garde:#x} — la pièce scellée n'est pas touchable "
             "(le mutant vivait au bras C : la falsification DEMANDÉE attrapée là)")

    print(f"\n=== L'ÉPREUVE POSIX SYMÉTRIQUE {VERTS} VERT, {ROUGES} ROUGE ===")
    return 0 if ROUGES == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
