#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_dev6.py — LA RETOUCHE DE L'ENTRÉE 209 : [HINSTANCE-PEB] CHASSÉ.

Le build dev.6 : le bloc d'entrée (RVA 0x5C00, R7 — aucune adresse scellée
ne bouge) réécrit EN PLACE : r12 = GetModuleHandleW(NULL) — LE VRAI module —
au lieu du RCX brut du point d'entrée (le PEB). La lignée prouvée (demo.exe
0.3.0, le scellé M2 dont la fenêtre VÉCUT au terrain) câble ainsi ; le slot
0x2400 était importé mais JAMAIS appelé — le fil manquant, l'Entrée 209.

Tout encodage est attesté par les octets du bloc original ; le produit est
revérifié par désassemblage complet (capstone) et diff byte-à-byte contre
dev.5 (seuls l'entrée et le qword version @0x2E80 changent : 0x00010005 ->
0x00010006, la porte R10).
"""
import hashlib
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

SRC = "/home/z/my-project/upload/triade/loupe.exe"
DST = "/home/z/my-project/download/loupe-kit-7/loupe.exe"

ENTRY = 0x5C00          # RVA du bloc d'entrée (scellé, R7)
WNDPROC = 0x5DCB        # le WndProc suit immédiatement — INTACT
ENTRY_FILE = 0x4E00     # offset fichier du bloc ( .text2 VA 0x4000, raw 0x3200 )
VER_FILE = 0x2080       # offset fichier du qword version ( .rdata VA 0x2000, raw 0x1200 )

# --- cibles (RVA) ----------------------------------------------------------------
T_GMHW = 0x2400         # GetModuleHandleW  — LE FIL QUI MANQUAIT
T_GCLW = 0x2408         # GetCommandLineW
T_EXIT = 0x2410         # ExitProcess
T_REG = 0x2450          # RegisterClassExW
T_CREATE = 0x2458       # CreateWindowExW
T_SHOW = 0x2460         # ShowWindow
T_CURSOR = 0x24C8       # LoadCursorW
T_MSGBOX = 0x24D8       # MessageBoxW
T_LOUPE01 = 0x4080      # ouvrir
T_MEMSET = 0x13C0       # memset M1 (le scellé)
T_WIN03 = 0x15C0        # la boucle de messages (le scellé demo.exe)
T_MSGPOSE = 0x6046      # pose le message d'état
S_ABSENT = 0x23E6       # "fichier introuvable"
S_REFUS = 0x23D8        # "refus système"
S_CLASS = 0x2600        # L"LoupeHexa"
S_TITLE = 0x2614        # L"Loupe — l'éditeur hexadécimal"
S_FAIL = 0x2650         # L"La fenêtre de Loupe ne peut pas être cré…"
G_HWND = 0xFDE0         # le hwnd global (.data)

# --- le mini-assembleur : items (longueur, émetteur) -----------------------------


def B(*bs):
    return bytes(bs)


class Asm:
    def __init__(self):
        self.items = []       # (nom, longueur, emit(addr, resolve)->bytes)
        self.labels = {}

    def raw(self, data):
        self.items.append((None, len(data), lambda a, r, d=data: d))

    def label(self, name):
        self.labels[name] = len(self.items)

    def jrel8(self, opcode, target):
        def emit(a, r, op=opcode, t=target):
            rel = r(t) - (a + 2)
            assert -128 <= rel <= 127, f"jrel8 hors bornes : {rel}"
            return B(op, rel & 0xFF)
        self.items.append((None, 2, emit))

    def jrel32(self, op2, target):
        def emit(a, r, o=op2, t=target):
            rel = r(t) - (a + 6)
            return B(*o) + struct.pack("<i", rel)
        self.items.append((None, 6, emit))

    def callrel(self, target):
        def emit(a, r, t=target):
            return B(0xE8) + struct.pack("<i", r(t) - (a + 5))
        self.items.append((None, 5, emit))

    def ripcall(self, target):
        def emit(a, r, t=target):
            return B(0xFF, 0x15) + struct.pack("<i", r(t) - (a + 6))
        self.items.append((None, 6, emit))

    def riplea(self, reg, target):
        # reg : (rex, modrm) — rax: (48,0x05) rcx: (48,0x0D) rdx: (48,0x15)
        #       r8: (4C,0x05) rsi: (48,0x35)
        def emit(a, r, g=reg, t=target):
            return B(g[0], 0x8D, g[1]) + struct.pack("<i", r(t) - (a + 7))
        self.items.append((None, 7, emit))

    def assemble(self, origin):
        # passe 1 : adresses
        addrs = []
        a = origin
        for _, ln, _e in self.items:
            addrs.append(a)
            a += ln
        total = a - origin

        def resolve(t):
            if isinstance(t, str):
                return addrs[self.labels[t]]
            return t
        # passe 2 : octets
        out = bytearray()
        for (idx, (_, ln, emit)) in enumerate(self.items):
            b = emit(addrs[idx], resolve)
            assert len(b) == ln, f"longueur {len(b)} != {ln} à {addrs[idx]:#x}"
            out += b
        return bytes(out), total


a = Asm()
# --- le prologue : LE VRAI MODULE (la retouche de l'Entrée 209) -------------------
a.raw(B(0x57))                       # push rdi
a.raw(B(0x56))                       # push rsi
a.raw(B(0x41, 0x54))                 # push r12
a.raw(B(0x48, 0x81, 0xEC, 0xB0, 0x00, 0x00, 0x00))  # sub rsp, 0xB0
a.raw(B(0x31, 0xC9))                 # xor ecx, ecx
a.ripcall(T_GMHW)                    # call [GetModuleHandleW]  <- LE FIL CÂBLÉ
a.raw(B(0x49, 0x89, 0xC4))           # mov r12, rax  (LE VRAI HMODULE)
# --- la ligne de commande : l'argument fichier, s'il vit --------------------------
a.ripcall(T_GCLW)                    # call [GetCommandLineW]
a.raw(B(0x48, 0x89, 0xC2))           # mov rdx, rax
a.raw(B(0x66, 0x83, 0x3A, 0x22))     # cmp word [rdx], '"'
a.jrel8(0x75, "unq")
a.raw(B(0x48, 0x83, 0xC2, 0x02))     # add rdx, 2
a.label("q")
a.raw(B(0x0F, 0xB7, 0x02))           # movzx eax, word [rdx]
a.raw(B(0x85, 0xC0))                 # test eax, eax
a.jrel8(0x74, "noarg")
a.raw(B(0x83, 0xF8, 0x22))           # cmp eax, '"'
a.jrel8(0x74, "skip")
a.raw(B(0x48, 0x83, 0xC2, 0x02))     # add rdx, 2
a.jrel8(0xEB, "q")
a.label("unq")
a.raw(B(0x0F, 0xB7, 0x02))           # movzx eax, word [rdx]
a.raw(B(0x85, 0xC0))                 # test eax, eax
a.jrel8(0x74, "noarg")
a.raw(B(0x83, 0xF8, 0x20))           # cmp eax, ' '
a.jrel8(0x74, "skip")
a.raw(B(0x48, 0x83, 0xC2, 0x02))     # add rdx, 2
a.jrel8(0xEB, "unq")
a.label("skip")
a.raw(B(0x0F, 0xB7, 0x02))           # movzx eax, word [rdx]
a.raw(B(0x83, 0xF8, 0x20))           # cmp eax, ' '
a.jrel8(0x75, "chk")
a.raw(B(0x48, 0x83, 0xC2, 0x02))     # add rdx, 2
a.jrel8(0xEB, "skip")
a.label("chk")
a.raw(B(0x85, 0xC0))                 # test eax, eax
a.jrel8(0x74, "noarg")
a.raw(B(0x48, 0x89, 0xD1))           # mov rcx, rdx
a.callrel(T_LOUPE01)                 # call loupe-01 (ouvrir)
a.raw(B(0x85, 0xC0))                 # test eax, eax
a.jrel8(0x79, "noarg")               # jns — le vert passe
a.raw(B(0x83, 0xF8, 0xFE))           # cmp eax, -2
a.jrel8(0x75, "gen")
a.riplea((0x48, 0x35), S_ABSENT)     # lea rsi, "fichier introuvable"
a.callrel(T_MSGPOSE)                 # call 0x6046
a.jrel8(0xEB, "noarg")
a.label("gen")
a.riplea((0x48, 0x35), S_REFUS)      # lea rsi, "refus système"
a.callrel(T_MSGPOSE)
# --- la classe : le CADRE WNDCLASSEX né memset-zéro, puis les champs vifs --------
a.label("noarg")
a.raw(B(0x48, 0x8D, 0x4C, 0x24, 0x60))   # lea rcx, [rsp+0x60]
a.raw(B(0x31, 0xD2))                     # xor edx, edx
a.raw(B(0x41, 0xB8, 0x50, 0x00, 0x00, 0x00))  # mov r8d, 0x50
a.callrel(T_MEMSET)                      # memset(&wc, 0, 0x50) — le scellé M1
a.raw(B(0xC7, 0x44, 0x24, 0x60, 0x50, 0x00, 0x00, 0x00))  # cbSize = 0x50
a.riplea((0x48, 0x05), WNDPROC)      # lea rax, [WndProc @0x5DCB]
a.raw(B(0x48, 0x89, 0x44, 0x24, 0x68))       # lpfnWndProc
a.raw(B(0x4C, 0x89, 0x64, 0x24, 0x78))       # hInstance = LE VRAI MODULE
a.raw(B(0x31, 0xC9))                     # xor ecx, ecx
a.raw(B(0xBA, 0x00, 0x7F, 0x00, 0x00))   # mov edx, IDC_ARROW
a.ripcall(T_CURSOR)                      # LoadCursorW(NULL, IDC_ARROW)
a.raw(B(0x48, 0x89, 0x84, 0x24, 0x88, 0x00, 0x00, 0x00))   # hCursor
a.raw(B(0x48, 0xC7, 0x84, 0x24, 0x90, 0x00, 0x00, 0x00,
        0x05, 0x00, 0x00, 0x00))          # hbrBackground = COLOR_WINDOW+1
a.riplea((0x48, 0x05), S_CLASS)      # lea rax, L"LoupeHexa"
a.raw(B(0x48, 0x89, 0x84, 0x24, 0xA0, 0x00, 0x00, 0x00))   # lpszClassName
a.raw(B(0x48, 0x8D, 0x4C, 0x24, 0x60))   # lea rcx, &wc
a.ripcall(T_REG)                         # RegisterClassExW
a.raw(B(0x85, 0xC0))                     # test eax, eax
a.jrel32((0x0F, 0x84), "fail")           # je fail
# --- la fenêtre : 640x480, la même vitrine ---------------------------------------
a.raw(B(0xB8, 0x00, 0x00, 0x00, 0x80))   # mov eax, CW_USEDEFAULT
a.raw(B(0x48, 0x89, 0x44, 0x24, 0x20))   # X
a.raw(B(0x48, 0x89, 0x44, 0x24, 0x28))   # Y
a.raw(B(0x48, 0xC7, 0x44, 0x24, 0x30, 0x80, 0x02, 0x00, 0x00))  # 0x280
a.raw(B(0x48, 0xC7, 0x44, 0x24, 0x38, 0xE0, 0x01, 0x00, 0x00))  # 0x1E0
a.raw(B(0x48, 0xC7, 0x44, 0x24, 0x40, 0x00, 0x00, 0x00, 0x00))  # parent
a.raw(B(0x48, 0xC7, 0x44, 0x24, 0x48, 0x00, 0x00, 0x00, 0x00))  # menu
a.raw(B(0x4C, 0x89, 0x64, 0x24, 0x50))   # hInstance = LE VRAI MODULE
a.raw(B(0x48, 0xC7, 0x44, 0x24, 0x58, 0x00, 0x00, 0x00, 0x00))  # param
a.raw(B(0x31, 0xC9))                     # xor ecx, ecx (exStyle)
a.riplea((0x48, 0x15), S_CLASS)      # lea rdx, L"LoupeHexa"
a.riplea((0x4C, 0x05), S_TITLE)      # lea r8, le titre
a.raw(B(0x41, 0xB9, 0x00, 0x00, 0xEF, 0x00))   # WS_OVERLAPPEDWINDOW
a.ripcall(T_CREATE)                      # CreateWindowExW
a.raw(B(0x48, 0x85, 0xC0))               # test rax, rax
a.jrel8(0x74, "fail")                    # je fail
a.riplea((0x48, 0x0D), G_HWND)       # lea rcx, le hwnd global
a.raw(B(0x48, 0x89, 0x01))               # mov [rcx], rax
a.raw(B(0x48, 0x89, 0xC1))               # mov rcx, rax
a.raw(B(0xBA, 0x05, 0x00, 0x00, 0x00))   # mov edx, SW_SHOW
a.ripcall(T_SHOW)                        # ShowWindow
a.callrel(T_WIN03)                       # la boucle scellée demo.exe
a.raw(B(0x31, 0xC9))                     # xor ecx, ecx
a.ripcall(T_EXIT)                        # ExitProcess(0)
# --- l'échec expliqué ------------------------------------------------------------
a.label("fail")
a.raw(B(0x31, 0xC9))                     # xor ecx, ecx
a.riplea((0x48, 0x15), S_FAIL)       # lea rdx, le message
a.riplea((0x4C, 0x05), S_TITLE)      # lea r8, le titre
a.raw(B(0x41, 0xB9, 0x10, 0x00, 0x00, 0x00))   # MB_ICONERROR
a.ripcall(T_MSGBOX)                      # MessageBoxW
a.raw(B(0xB9, 0x01, 0x00, 0x00, 0x00))   # mov ecx, 1
a.ripcall(T_EXIT)                        # ExitProcess(1)


def main():
    bloc, total = a.assemble(ENTRY)
    limite = WNDPROC - ENTRY
    assert total <= limite, f"bloc trop long : {total} > {limite}"
    bloc = bloc + b"\x90" * (limite - total)   # le padding du plan
    print(f"[build] bloc d'entrée : {total} o utiles + {limite-total} o de "
          f"padding — la limite R7 : {limite} o (WndProc @0x5DCB INTACT)")

    orig = open(SRC, "rb").read()
    assert len(orig) == 127488, "la pièce dev.5 : taille inattendue"
    img = bytearray(orig)
    img[ENTRY_FILE:ENTRY_FILE + limite] = bloc
    img[VER_FILE:VER_FILE + 8] = struct.pack("<Q", 0x00010006)   # la porte R10
    out = bytes(img)
    assert len(out) == 127488

    # --- le diff : SEULS l'entrée et le qword version changent -------------------
    diffs = [i for i in range(len(orig)) if orig[i] != out[i]]
    hors = [i for i in diffs
            if not (ENTRY_FILE <= i < ENTRY_FILE + limite)
            and not (VER_FILE <= i < VER_FILE + 8)]
    assert not hors, f"octets changés hors périmètre : {hors[:8]}"
    print(f"[build] diff dev.5 -> dev.6 : {len(diffs)} octets — "
          f"l'entrée [{ENTRY_FILE:#x}..{ENTRY_FILE+limite:#x}) + le qword "
          f"version @0x2E80 (0x00010005 -> 0x00010006)")

    sha = hashlib.sha256(out).hexdigest()
    print(f"[build] loupe.exe dev.6 : {len(out)} o, sha256 {sha}")

    import os
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    open(DST, "wb").write(out)

    # --- la revérification : désassemblage complet du bloc ------------------------
    pe = pefile.PE(DST, fast_load=True)
    data = pe.get_memory_mapped_image()
    assert struct.unpack_from("<Q", data, 0x2E80)[0] == 0x00010006
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    lignes = list(md.disasm(bytes(data[ENTRY:WNDPROC]), ENTRY))
    print(f"[verif] désassemblage du bloc : {len(lignes)} instructions, "
          f"fin à {lignes[-1].address:#x}")
    cibles = set()
    ok = True
    for i in lignes:
        if i.mnemonic in ("call", "jmp", "je", "jne", "jns") and i.op_str.startswith("0x"):
            cibles.add(int(i.op_str, 16))
    attendus = {T_LOUPE01, T_MEMSET, T_WIN03, T_MSGPOSE}  # cibles d'appel direct
    manquants = attendus - cibles
    assert not manquants, f"cibles directes manquantes : {[hex(m) for m in manquants]}"
    # les lea [rip+disp] : le WndProc et les chaînes
    import re
    leas = set()
    for i in lignes:
        if i.mnemonic == "lea" and "rip" in i.op_str:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
            if m:
                d = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
                leas.add(i.address + i.size + d)
    assert WNDPROC in leas, "le lea du WndProc ne pointe pas @0x5DCB"
    for s in (S_ABSENT, S_REFUS, S_CLASS, S_TITLE, S_FAIL, G_HWND):
        assert s in leas, f"lea manquant vers {s:#x}"
    # les appels [rip+disp] : vérifier chaque slot
    import re
    slots = {}
    for i in lignes:
        if i.mnemonic == "call" and "rip" in i.op_str:
            m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", i.op_str)
            d = int(m.group(2), 16) * (1 if m.group(1) == "+" else -1)
            slots.setdefault(i.address + i.size + d, []).append(i.address)
    print("[verif] slots IAT appelés par l'entrée :")
    noms = {0x2400: "GetModuleHandleW", 0x2408: "GetCommandLineW",
            0x2410: "ExitProcess", 0x2450: "RegisterClassExW",
            0x2458: "CreateWindowExW", 0x2460: "ShowWindow",
            0x24C8: "LoadCursorW", 0x24D8: "MessageBoxW"}
    for t, srcs in sorted(slots.items()):
        print(f"    {noms.get(t, hex(t)):20s} <- {[hex(s) for s in srcs]}")
    assert 0x2400 in slots, "GetModuleHandleW TOUJOURS pas câblé ?!"
    print("[verif] GetModuleHandleW CÂBLÉ — le fil de l'Entrée 209 est posé")

    # le WndProc et tous les blocs scellés : intacts
    for nom, rva in [("WndProc", 0x5DCB), ("loupe-01", 0x4080),
                     ("loupe-17", 0x6500), ("paint", 0x4B00)]:
        assert data[rva:rva+8] == pefile.PE(SRC, fast_load=True).get_memory_mapped_image()[rva:rva+8]
    print("[verif] WndProc @0x5DCB, loupe-01, loupe-17, paint : octets IDENTIQUES à dev.5")
    print(f"\n[ENTRÉE 209] loupe.exe 0.1.0-dev.6 NÉ : {len(out)} o, "
          f"sha256\n  {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
