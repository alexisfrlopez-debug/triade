#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE SIMULATEUR DE VITRINE v2 — loupe.exe dev.7 au labo sous Unicorn.

Deux gestes du témoin terrain :
  [1/3] la vitrine vide        (mode « vide »)
  [2/3] la vitrine avec fichier (mode « fichier » — la session NÉE,
         les branches WndProc-avec-session VÉCUES pour la première
         fois hors terrain : WM_SIZE, WM_PAINT lecteur, WM_VSCROLL)

La ligne de commande, les APIs fichier (CreateFileW/GetFileSizeEx/
ReadFile/SetFilePointerEx/WriteFile), la boucle à messages — tout est
relayé. Toute faute NOMME son adresse.
"""
import struct
import sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX,
                               UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9)
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

MODE = sys.argv[1] if len(sys.argv) > 1 else "vide"
EXE = "/home/z/my-project/run8/loupe.exe"
BASE = 0x140000000
STACK = 0x7FF900000000
STACK_TAILLE = 0x400000
PAGE_API = 0x50000000
PAGE_SCRATCH = 0x40000000
RETOUR_MAGIQUE = 0x50001000

d = open(EXE, "rb").read()
e_lfanew = struct.unpack_from("<I", d, 0x3C)[0]
coff = e_lfanew + 4
machine, nsec, tds, ps, ns, optsz, chars = struct.unpack_from("<HHIIIHH", d, coff)
opt = coff + 20
sec_off = opt + optsz
sections = []
for i in range(nsec):
    s = sec_off + 40 * i
    nom = d[s:s + 8].rstrip(b"\0").decode()
    vs = struct.unpack_from("<I", d, s + 8)[0]
    va = struct.unpack_from("<I", d, s + 12)[0]
    raw = struct.unpack_from("<I", d, s + 16)[0]
    ptr = struct.unpack_from("<I", d, s + 20)[0]
    sections.append((nom, va, vs, ptr, raw))

imp_rva = struct.unpack_from("<I", d, opt + 112 + 8)[0]


def r2o(rva):
    for (nom, va, vs, ptr, raw) in sections:
        if va <= rva < va + max(vs, raw):
            return ptr + (rva - va)
    return None


slots = []
off = r2o(imp_rva)
i = 0
while True:
    oft, tds, fwd, namerva, ft = struct.unpack_from("<IIIII", d, off + 20 * i)
    if oft == 0 and namerva == 0 and ft == 0:
        break
    o = r2o(ft)
    n = 0
    while True:
        v = struct.unpack_from("<Q", d, o + 8 * n)[0]
        if v == 0:
            break
        no = r2o(v)
        fin = d.find(b"\0", no + 2)
        slots.append((ft + 8 * n, d[no + 2:fin].decode()))
        n += 1
    i += 1

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 0x21000)
uc.mem_write(BASE, d[0:0x200])
for (nom, va, vs, ptr, raw) in sections:
    uc.mem_write(BASE + va, d[ptr:ptr + raw])
uc.mem_map(STACK, STACK_TAILLE)
uc.mem_map(PAGE_API, 0x2000)
uc.mem_map(PAGE_SCRATCH, 0x100000)

ADRESSE = {}
for idx, (rva, nom) in enumerate(slots):
    cible = PAGE_API + 0x20 + idx * 0x10
    uc.mem_write(BASE + rva, struct.pack("<Q", cible))
    ADRESSE[cible] = nom

CMDLINE = PAGE_SCRATCH + 0x100
if MODE == "fichier":
    uc.mem_write(CMDLINE, "loupe.exe temoin-fichier.bin\0".encode("utf-16-le"))
    uc.mem_write(PAGE_SCRATCH + 0x400, "temoin-fichier.bin\0".encode("utf-16-le"))
else:
    uc.mem_write(CMDLINE, "loupe.exe\0".encode("utf-16-le"))

WNDPROC = {"ptr": None}
FICHIER = {"pos": 0, "donnees": d}   # l'OMBRE : la pièce elle-même comme fichier
ETAT = {"msgs": [], "journal": [], "exit": None}


def lever(uc, val):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RAX, val)


def service(uc, nom):
    rcx = uc.reg_read(UC_X86_REG_RCX)
    rdx = uc.reg_read(UC_X86_REG_RDX)
    r8 = uc.reg_read(UC_X86_REG_R8)
    r9 = uc.reg_read(UC_X86_REG_R9)
    if nom == "GetModuleHandleW":
        return lever(uc, BASE)
    if nom == "GetCommandLineW":
        return lever(uc, CMDLINE)
    if nom == "LoadCursorW":
        return lever(uc, 0xDEAD0001)
    if nom == "RegisterClassExW":
        WNDPROC["ptr"] = struct.unpack("<Q", uc.mem_read(rcx + 0x08, 8))[0]
        ETAT["journal"].append(f"RegisterClassExW : WndProc = {WNDPROC['ptr']:#x}")
        return lever(uc, 0x1234)
    if nom == "CreateWindowExW":
        ETAT["journal"].append("CreateWindowExW → hwnd 0x60000")
        return lever(uc, 0x60000)
    if nom == "ShowWindow":
        ETAT["journal"].append("ShowWindow(5)")
        return lever(uc, 1)
    if nom == "GetMessageW":
        if ETAT["msgs"]:
            m, wp, lp = ETAT["msgs"].pop(0)
            uc.mem_write(rcx, struct.pack("<QIIQQ", 0x60000, m, wp, lp, 0))
            ETAT["journal"].append(f"GetMessageW → msg {m:#x}")
            return lever(uc, 1)
        ETAT["journal"].append("GetMessageW → WM_QUIT")
        return lever(uc, 0)
    if nom == "TranslateMessage":
        return lever(uc, 0)
    if nom == "DispatchMessageW":
        hwnd, msg, wp, lp = struct.unpack("<QIIQQ", uc.mem_read(rcx, 32))[:4]
        ETAT["journal"].append(f"DispatchMessageW → WndProc(msg={msg:#x})")
        appeler_wndproc(uc, hwnd, msg, wp, lp)
        return
    if nom == "BeginPaint":
        uc.mem_write(rdx, struct.pack("<Q", 0x70000))
        uc.mem_write(rdx + 8, b"\x01" + b"\0" * 7)
        uc.mem_write(rdx + 0x10, struct.pack("<iiii", 0, 0, 640, 480))
        return lever(uc, 0x70000)
    if nom == "GetStockObject":
        return lever(uc, 0x70001)
    if nom == "SelectObject":
        return lever(uc, 0x70002)
    if nom == "GetTextMetricsW":
        tm = bytearray(0x3C)
        struct.pack_into("<i", tm, 0, 16)      # tmHeight
        struct.pack_into("<i", tm, 0x14, 8)    # tmAveCharWidth
        uc.mem_write(rdx, bytes(tm))
        return lever(uc, 1)
    if nom == "GetClientRect":
        uc.mem_write(rdx, struct.pack("<iiii", 0, 0, 640, 480))
        return lever(uc, 1)
    if nom == "GetScrollInfo":
        # SCROLLINFO : cbSize@0 fMask@4 nMin@8 nMax@12 nPage@16 nPos@20
        si = bytearray(28)
        struct.pack_into("<I", si, 0, 28)
        struct.pack_into("<I", si, 4, 0x17)
        struct.pack_into("<i", si, 8, 0)
        struct.pack_into("<i", si, 12, 100)
        struct.pack_into("<I", si, 16, 20)
        struct.pack_into("<i", si, 20, 0)
        uc.mem_write(rdx, bytes(si))
        return lever(uc, 1)
    if nom == "CreateFileW":
        ETAT["journal"].append(f"CreateFileW → 0x310 (l'OMBRE)")
        return lever(uc, 0x310)
    if nom == "GetFileSizeEx":
        uc.mem_write(rdx, struct.pack("<Q", len(d)))
        return lever(uc, 1)
    if nom == "ReadFile":
        tampon = FICHIER["donnees"][FICHIER["pos"]:FICHIER["pos"] + r8]
        uc.mem_write(rdx, bytes(tampon))
        FICHIER["pos"] += len(tampon)
        if r9:
            uc.mem_write(r9, struct.pack("<Q", len(tampon)))
        return lever(uc, 1)
    if nom == "SetFilePointerEx":
        if r9:
            uc.mem_write(r9, struct.pack("<Q", rdx))
        FICHIER["pos"] = rdx
        return lever(uc, 1)
    if nom == "WriteFile":
        if r9:
            uc.mem_write(r9, struct.pack("<Q", r8))
        return lever(uc, 1)
    if nom == "CloseHandle":
        return lever(uc, 1)
    if nom == "GetLastError":
        return lever(uc, 0)
    if nom == "ExitProcess":
        ETAT["journal"].append(f"ExitProcess({rcx}) — LA SORTIE")
        ETAT["exit"] = rcx
        uc.emu_stop()
        return
    if nom == "MessageBoxW":
        ETAT["journal"].append(f"!! MessageBoxW : « {lire_w(uc, rcx)} »")
        return lever(uc, 1)
    return lever(uc, 1)


def lire_w(uc, a, maxn=260):
    out = b""
    while len(out) < maxn * 2:
        c = uc.mem_read(a + len(out), 2)
        if c == b"\0\0":
            break
        out += c
    return out.decode("utf-16-le", "replace")


def appeler_wndproc(uc, hwnd, msg, wp, lp):
    rsp = uc.reg_read(UC_X86_REG_RSP)
    uc.reg_write(UC_X86_REG_RSP, rsp - 8)
    uc.mem_write(rsp - 8, struct.pack("<Q", RETOUR_MAGIQUE))
    uc.reg_write(UC_X86_REG_RCX, hwnd)
    uc.reg_write(UC_X86_REG_RDX, msg)
    uc.reg_write(UC_X86_REG_R8, wp)
    uc.reg_write(UC_X86_REG_R9, lp)
    uc.reg_write(UC_X86_REG_RIP, WNDPROC["ptr"])


def crochet_code(uc, adresse, taille, donnees_util):
    if adresse == RETOUR_MAGIQUE:
        return lever(uc, 0)
    if adresse in ADRESSE:
        try:
            service(uc, ADRESSE[adresse])
        except Exception:
            import traceback
            print(f"\n*** ERREUR DANS LE RELAIS {ADRESSE[adresse]} ***", flush=True)
            traceback.print_exc()
            uc.emu_stop()
        return


def crochet_faute(uc, acces, adresse, taille, valeur, donnees_util):
    rip = uc.reg_read(UC_X86_REG_RIP)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    try:
        code = bytes(uc.mem_read(rip, 16))
        ins = next(md.disasm(code, rip))
        texte = f"{ins.mnemonic} {ins.op_str}"
    except Exception:
        texte = "??"
    nature = {0: "lecture", 1: "écriture", 16: "fetch"}.get(acces, str(acces))
    print(f"\n*** FAUTE {nature} @ {adresse:#x} — RIP {rip:#x} : {texte} ***", flush=True)
    print(f"*** L'ADRESSE NOMMÉE : {adresse:#x} "
          f"({'BASE+' + hex(adresse - BASE) if BASE <= adresse < BASE + 0x21000 else 'HORS IMAGE'}) ***",
          flush=True)
    import unicorn.x86_const as x
    for nomreg in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
                   "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"):
        v = uc.reg_read(getattr(x, "UC_X86_REG_" + nomreg))
        print(f"    {nomreg} = {v:#018x}", flush=True)
    return False


uc.hook_add(UC_HOOK_CODE, crochet_code, begin=PAGE_API, end=PAGE_API + 0x2000)
uc.hook_add(UC_HOOK_MEM_INVALID, crochet_faute)

# LE CHASSEUR D'ÉCRITURES ILLÉGALES : toute écriture dans .text/.rdata/.text2
# (les pages LECTURE SEULE du vrai système) est NOMMÉE — Unicorn mappe tout RW
# et pardonne ce que le vrai Windows punit de 0xC0000005.
from unicorn import UC_HOOK_MEM_WRITE


def crochet_ecriture(uc, acces, adresse, taille, valeur, donnees_util):
    if BASE <= adresse < BASE + 0xE000:  # tout sauf .data (RW légitime)
        rip = uc.reg_read(UC_X86_REG_RIP)
        md = Cs(CS_ARCH_X86, CS_MODE_64)
        try:
            code = bytes(uc.mem_read(rip, 16))
            ins = next(md.disasm(code, rip))
            texte = f"{ins.mnemonic} {ins.op_str}"
        except Exception:
            texte = "??"
        print(f"\n*** ÉCRITURE EN PAGE LECTURE-SEULE @ {adresse:#x} "
              f"(BASE+{adresse - BASE:#x}) — RIP {rip:#x} : {texte} ***", flush=True)
        import unicorn.x86_const as x
        for nomreg in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP",
                       "R12", "R13", "R14", "R15"):
            v = uc.reg_read(getattr(x, "UC_X86_REG_" + nomreg))
            print(f"    {nomreg} = {v:#018x}", flush=True)
        uc.emu_stop()


uc.hook_add(UC_HOOK_MEM_WRITE, crochet_ecriture, begin=BASE, end=BASE + 0xE000)

# la file des messages : WM_SIZE (avec session, la branche jamais testée),
# WM_PAINT (le peintre lecteur), WM_VSCROLL, puis WM_QUIT
ETAT["msgs"] = [(0x5, 0, (543 << 16) | 624),   # WM_SIZE
                (0xF, 0, 0),                     # WM_PAINT
                (0x115, 0, 0x10),               # WM_VSCROLL (SB_PAGEDOWN)
                (0xF, 0, 0)]                    # WM_PAINT encore

RSP_DEPART = STACK + STACK_TAILLE - 0x100000
RETOUR_IMPOSSIBLE = 0x00DEAD0000000000
uc.reg_write(UC_X86_REG_RSP, RSP_DEPART)
uc.mem_write(RSP_DEPART, struct.pack("<Q", RETOUR_IMPOSSIBLE))
try:
    uc.emu_start(BASE + 0x5C00, RETOUR_IMPOSSIBLE)
except Exception as e:
    print(f"\n*** EXCEPTION : {e} ***")

print(f"\n=== LE JOURNAL DU SIMULATEUR (mode {MODE}) ===")
for l in ETAT["journal"]:
    print(f"  {l}")
if "exit" in ETAT and ETAT["exit"] is not None:
    print(f"\nverdict : SORTIE PROPRE ExitProcess({ETAT['exit']})")
else:
    print("\nverdict : MORT SANS EXITPROCESS — la faute ci-dessus NOMME le défaut")
