#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE D52h — harnais d'emulation FORENSIQUE du lancement reel de
superviseur-terrain3.exe, independant de l'oracle.

Fidelite chargeur :
  - base RELOGEE (ASLR) ;
  - IAT remplie UNIQUEMENT par la marche des 6 descripteurs (42 slots) ;
  - en-tete mappe, .data zero-apad, sections aux RVA.

Fidelite user32 :
  - RegisterClassExW valide la WNDCLASSEX et enregistre la classe ;
  - CreateWindowExW RAPPELLE le wndproc (WM_NCCREATE puis WM_CREATE),
    comme le vrai user32 — chemin JAMAIS emulate par l'oracle ;
  - GetMessageW -> 0 (WM_QUIT) ; GetStdHandle -> 0 (GUI sans console).

Instrumentation :
  - chaque appel d'API est journalise (nom, arguments, retour) ;
  - toute faute memoire -> dump RIP + dernier appel + pile.
"""

import pathlib
import struct
import sys

from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX,
                               UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8,
                               UC_X86_REG_R9)

EXE = pathlib.Path("/home/z/my-project/triade/terrain/livraison/superviseur.exe")
data = EXE.read_bytes()

# ---------------- plan PE ----------------
e = struct.unpack_from("<I", data, 0x3C)[0]
coff = e + 4
machine, nsec, _, _, _, opt_sz, _ = struct.unpack_from("<HHIIIHH", data, coff)
opt = coff + 20
entry_rva = struct.unpack_from("<I", data, opt + 16)[0]
imp_rva = struct.unpack_from("<I", data, opt + 120)[0]
secs = []
so = coff + 20 + opt_sz
for i in range(nsec):
    o = so + 40 * i
    nom = data[o:o + 8].rstrip(b"\x00").decode()
    vs, va, rs, ra = struct.unpack_from("<IIII", data, o + 8)
    fl = struct.unpack_from("<I", data, o + 36)[0]
    secs.append((nom, va, vs, ra, rs))

BASE = 0x7FF6A0000000            # base relogee (ASLR)
TRAMP = 0x600000000              # fausses API
MAGIC_RET = 0x500000000          # retour de callback wndproc
STACK = 0x7FF000000000
STACK_SZ = 0x100000

uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 0x11000)
uc.mem_map(TRAMP, 0x2000)
uc.mem_map(MAGIC_RET, 0x1000)
uc.mem_map(STACK, STACK_SZ)

# headers (premiere page)
uc.mem_write(BASE, data[:0x400])
for nom, va, vs, ra, rs in secs:
    if rs:
        uc.mem_write(BASE + va, data[ra:ra + rs])
    if vs > rs:
        uc.mem_write(BASE + va + rs, b"\x00" * (vs - rs))

# ---------------- IAT par la marche des descripteurs ----------------
def rva2off(rva):
    for nom, va, vs, ra, rs in secs:
        if va <= rva < va + max(vs, rs):
            return ra + (rva - va)
    return None

slots = {}
off = rva2off(imp_rva)
n = 0
api_ordres = []
while True:
    oft, _, _, nomrva, ft = struct.unpack_from("<IIIII", data, off + 20 * n)
    if oft == nomrva == ft == 0:
        break
    i = 0
    while True:
        val = struct.unpack_from("<Q", data, rva2off(oft + 8 * i))[0]
        if val == 0:
            break
        no = rva2off(val)
        fname = data[no + 2:].split(b"\x00")[0].decode("ascii", "replace")
        slots[ft + 8 * i] = fname
        api_ordres.append(fname)
        i += 1
    n += 1

FAUX = {}
for i, nom in enumerate(sorted(set(api_ordres))):
    FAUX[nom] = TRAMP + 0x10 + i * 0x10
for rva, nom in slots.items():
    uc.mem_write(BASE + rva, struct.pack("<Q", FAUX[nom]))
FAUX_REV = {v: k for k, v in FAUX.items()}
uc.mem_write(TRAMP, b"\xc3" * 0x2000)       # chaque fausse API = RET

# ---------------- etat du harnais ----------------
journal = []
classes = {}
hwnd_courant = 0x3000
wndproc_attente = []     # pile d'etats CreateWindowExW en cours
gle = 0
profondeur = 0

def log(*a):
    journal.append(" ".join(str(x) for x in a))
    print("[emu]", *a)

def lire_cstr(ptr):
    if not ptr:
        return None
    out = b""
    while True:
        c = uc.mem_read(ptr + len(out), 1)
        if c == b"\x00" or len(out) > 260:
            break
        out += bytes(c)
    return out.decode("latin1", "replace")

def lire_wstr(ptr):
    if not ptr:
        return None
    out = b""
    while True:
        w = uc.mem_read(ptr + len(out), 2)
        if w == b"\x00\x00" or len(out) > 520:
            break
        out += bytes(w)
    return out.decode("utf-16-le", "replace")

# ---------------- stubs ----------------
def api_GetLocalTime(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    st = struct.pack("<8H", 2026, 10, 27, 2, 15, 3, 57, 123)
    uc_.mem_write(rcx, st)
    log("GetLocalTime -> 27/10/2026 15:03:57")

def api_GetModuleHandleW(uc_):
    uc_.reg_write(UC_X86_REG_RAX, BASE)
    log("GetModuleHandleW(0) ->", hex(BASE))

def api_RegisterClassExW(uc_):
    global wndproc_attente
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    cbsize = struct.unpack_from("<I", uc_.mem_read(rcx, 4))[0]
    wndproc = struct.unpack_from("<Q", uc_.mem_read(rcx + 8, 8))[0]
    hinst = struct.unpack_from("<Q", uc_.mem_read(rcx + 0x18, 8))[0]
    ptr_nom = struct.unpack_from("<Q", uc_.mem_read(rcx + 0x40, 8))[0]
    nom = lire_wstr(ptr_nom)
    log(f"RegisterClassExW cbSize={cbsize} wndproc={wndproc:#x} "
        f"hInst={hinst:#x} classe={nom!r}")
    if cbsize != 80:
        log("  !!! cbSize != 80")
    classes[nom] = (wndproc, rcx)
    uc_.reg_write(UC_X86_REG_RAX, 0x1234)

def api_LoadCursorW(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 0x10001)
    log("LoadCursorW -> 0x10001")

TAMPON_CREATESTRUCT = 0x520000000
uc.mem_map(TAMPON_CREATESTRUCT, 0x1000)
TAMPON_MSG = 0x520001000
uc.mem_map(TAMPON_MSG, 0x1000)
file_messages = [    # (message, wparam, lparam) livres par GetMessageW
    (5, 0, (600 << 16) | 800),     # WM_SIZE
    (0x18, 1, 0),                   # WM_SHOWWINDOW
    (0x000F, 0, 0),                 # WM_PAINT
    (0x200, 0, 0),                  # WM_MOUSEMOVE
    (0x111, 0x3030, 0),             # WM_COMMAND (clic bouton TOUT DEMARRER)
]


def api_CreateWindowExW(uc_):
    """Rappelle le wndproc (WM_NCCREATE puis WM_CREATE) comme user32."""
    global hwnd_courant, profondeur
    profondeur += 1
    rdx = uc_.reg_read(UC_X86_REG_RDX)
    r8 = uc_.reg_read(UC_X86_REG_R8)
    r9 = uc_.reg_read(UC_X86_REG_R9)
    nom = lire_wstr(rdx)
    log(f"CreateWindowExW classe={nom!r} exStyle={uc_.reg_read(UC_X86_REG_RCX):#x} "
        f"style={r9:#x} nom={lire_wstr(r8)!r} (prof {profondeur})")
    hwnd_courant += 0x10
    hwnd = hwnd_courant
    if nom in classes and classes[nom][0]:
        wndproc = classes[nom][0]
        # CREATESTRUCTW pour le lparam de WM_NCCREATE/WM_CREATE
        hinst = struct.unpack_from(
            "<Q", uc_.mem_read(BASE + 0x3860, 8))[0] if False else BASE
        cs = struct.pack("<QQQQiiiiQQQI",
                         0, BASE, 0, 0, 600, 800, 0, 0,   # params,inst,menu,parent,cy,cx,y,x
                         r9, r8, rdx, uc_.reg_read(UC_X86_REG_RCX))
        uc_.mem_write(TAMPON_CREATESTRUCT, cs)
        wndproc_attente.append({"wndproc": wndproc, "hwnd": hwnd,
                                "etape": 0, "nom": nom,
                                "rsp": uc_.reg_read(UC_X86_REG_RSP)})
        appeler_wndproc(uc_, wndproc, hwnd, 0x81, 0, TAMPON_CREATESTRUCT)  # WM_NCCREATE
    else:
        log(f"  classe systeme {nom!r} -> hwnd {hwnd:#x} sans callback")
        uc_.reg_write(UC_X86_REG_RAX, hwnd)
        uc_.reg_write(UC_X86_REG_RIP, FAUX["CreateWindowExW"] + 1)  # -> ret

def api_GetStdHandle(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 0)
    log("GetStdHandle -> 0 (GUI, pas de console)")

def api_CreateFileA(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    nom = lire_cstr(rcx)
    log(f"CreateFileA({nom!r}) -> handle 0x200")
    uc_.reg_write(UC_X86_REG_RAX, 0x200)

def api_WriteFile(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    rdx = uc_.reg_read(UC_X86_REG_RDX)
    r8 = uc_.reg_read(UC_X86_REG_R8)
    try:
        contenu = bytes(uc_.mem_read(rdx, r8))
    except Exception:
        contenu = b"<illisible>"
    log(f"WriteFile(h={rcx:#x}, {r8} o) : {contenu[:80]!r}")
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_ReadFile(uc_):
    log("ReadFile -> 0")
    uc_.reg_write(UC_X86_REG_RAX, 0)

def api_CloseHandle(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_GetModuleFileNameA(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    rdx = uc_.reg_read(UC_X86_REG_RDX)
    chemin = b"c:\\Users\\Alek\\Downloads\\superviseur-terrain3.exe\x00"
    uc_.mem_write(rdx, chemin)
    uc_.reg_write(UC_X86_REG_RAX, len(chemin) - 1)
    log("GetModuleFileNameA ->", chemin[:-1].decode())

def api_FlushFileBuffers(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_GetLastError(uc_):
    uc_.reg_write(UC_X86_REG_RAX, gle)

def api_FindWindowW(uc_):
    log("FindWindowW -> 0 (aucune autre instance)")
    uc_.reg_write(UC_X86_REG_RAX, 0)

def api_FindWindowExW(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 0)

def api_SendMessageTimeoutW(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 0)

def api_SendMessageW(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    rdx = uc_.reg_read(UC_X86_REG_RDX)
    log(f"SendMessageW(hwnd={rcx:#x}, msg={rdx:#x}) -> 0")
    uc_.reg_write(UC_X86_REG_RAX, 0)

def api_GetMessageW(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    if file_messages:
        msg, wp, lp = file_messages.pop(0)
        uc_.mem_write(rcx, struct.pack("<QIIIQQ", 0x3010, msg, wp, lp, 0, 0))
        log(f"GetMessageW -> 1 (msg={msg:#x})")
        uc_.reg_write(UC_X86_REG_RAX, 1)
    else:
        log("GetMessageW -> 0 (WM_QUIT)")
        uc_.reg_write(UC_X86_REG_RAX, 0)

def api_TranslateMessage(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_DispatchMessageW(uc_):
    rcx = uc_.reg_read(UC_X86_REG_RCX)
    hwnd, msg, wp, lp = struct.unpack_from("<QIII", uc_.mem_read(rcx, 24))
    log(f"DispatchMessageW hwnd={hwnd:#x} msg={msg:#x} wparam={wp:#x}")
    wndproc = classes.get("TRIADE_superviseur", (None,))[0]
    if wndproc and msg != 0x12:      # pas WM_QUIT
        wndproc_attente.append({"wndproc": wndproc, "hwnd": hwnd,
                                "etape": 90, "nom": "dispatch",
                                "rsp": uc_.reg_read(UC_X86_REG_RSP)})
        appeler_wndproc(uc_, wndproc, hwnd, msg, wp, lp)
    else:
        uc_.reg_write(UC_X86_REG_RAX, 0)

def api_DefWindowProcW(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 0)
    log("DefWindowProcW -> 0")

def api_PostQuitMessage(uc_):
    log("PostQuitMessage")

def api_DestroyWindow(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_MoveWindow(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_GetClientRect(uc_):
    rdx = uc_.reg_read(UC_X86_REG_RDX)      # lpRect (2e argument)
    uc_.mem_write(rdx, struct.pack("<4i", 0, 0, 800, 600))
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_EnableWindow(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_MessageBoxW(uc_):
    rdx = uc_.reg_read(UC_X86_REG_RDX)
    r8 = uc_.reg_read(UC_X86_REG_R8)
    log(f"!!! MessageBoxW({lire_wstr(rdx)!r}, {lire_wstr(r8)!r}) -> IDOK")
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_ExitProcess(uc_):
    log("ExitProcess(", uc_.reg_read(UC_X86_REG_RCX), ") — FIN PROPRE")
    uc_.emul_stop()

def api_Sleep(uc_):
    pass

def api_CreateThread(uc_):
    log("!!! CreateThread appele")
    uc_.reg_write(UC_X86_REG_RAX, 0x777)

def api_VirtualProtect(uc_):
    uc_.reg_write(UC_X86_REG_RAX, 1)

def api_generic(uc_, nom):
    log(f"(stub generique) {nom}")
    uc_.reg_write(UC_X86_REG_RAX, 1)

APIS = {
    "GetLocalTime": api_GetLocalTime, "GetModuleHandleW": api_GetModuleHandleW,
    "RegisterClassExW": api_RegisterClassExW, "LoadCursorW": api_LoadCursorW,
    "CreateWindowExW": api_CreateWindowExW, "GetStdHandle": api_GetStdHandle,
    "CreateFileA": api_CreateFileA, "WriteFile": api_WriteFile,
    "ReadFile": api_ReadFile, "CloseHandle": api_CloseHandle,
    "GetModuleFileNameA": api_GetModuleFileNameA,
    "FlushFileBuffers": api_FlushFileBuffers, "GetLastError": api_GetLastError,
    "FindWindowW": api_FindWindowW, "FindWindowExW": api_FindWindowExW,
    "SendMessageTimeoutW": api_SendMessageTimeoutW,
    "SendMessageW": api_SendMessageW, "GetMessageW": api_GetMessageW,
    "TranslateMessage": api_TranslateMessage,
    "DispatchMessageW": api_DispatchMessageW,
    "DefWindowProcW": api_DefWindowProcW, "PostQuitMessage": api_PostQuitMessage,
    "DestroyWindow": api_DestroyWindow, "MoveWindow": api_MoveWindow,
    "GetClientRect": api_GetClientRect, "EnableWindow": api_EnableWindow,
    "MessageBoxW": api_MessageBoxW, "ExitProcess": api_ExitProcess,
    "Sleep": api_Sleep, "CreateThread": api_CreateThread,
    "VirtualProtect": api_VirtualProtect,
}

def rsp_depuis(uc_):
    return uc_.reg_read(UC_X86_REG_RSP)

def appeler_wndproc(uc_, wndproc, hwnd, msg, wparam, lparam):
    """Bascule l'execution vers le wndproc ; le retour atterrit sur MAGIC_RET."""
    rsp = uc_.reg_read(UC_X86_REG_RSP)
    nouvelle = (rsp - 0x800) & ~0xF
    nouvelle -= 8                       # comme un call qui pousse l'adresse de retour
    uc_.mem_write(nouvelle, struct.pack("<Q", MAGIC_RET))
    uc_.reg_write(UC_X86_REG_RSP, nouvelle)
    uc_.reg_write(UC_X86_REG_RCX, hwnd)
    uc_.reg_write(UC_X86_REG_RDX, msg)
    uc_.reg_write(UC_X86_REG_R8, wparam)
    uc_.reg_write(UC_X86_REG_R9, lparam)
    uc_.reg_write(UC_X86_REG_RIP, wndproc)
    log(f"  -> appel wndproc {wndproc:#x} (hwnd={hwnd:#x}, msg={msg:#x})")

etat = {"fini": False, "raison": ""}

def crochet_code(uc_, adresse, taille, user):
    if etat["fini"]:
        return
    if adresse == MAGIC_RET:
        # retour d'un callback wndproc
        rax = uc_.reg_read(UC_X86_REG_RAX)
        log(f"  <- wndproc retourne {rax:#x} ({rax})")
        if wndproc_attente:
            et = wndproc_attente[-1]
            if et["etape"] == 90:      # retour de DispatchMessageW
                wndproc_attente.pop()
                uc_.reg_write(UC_X86_REG_RSP, et["rsp"])
                uc_.reg_write(UC_X86_REG_RIP, FAUX["DispatchMessageW"] + 1)
                return
            if rax == 0xFFFFFFFF or rax == -1:
                log(f"  !!! wndproc a refuse le message — CreateWindow echoue")
                et = wndproc_attente.pop()
                uc_.reg_write(UC_X86_REG_RSP, et["rsp"])
                uc_.reg_write(UC_X86_REG_RAX, 0)
                uc_.reg_write(UC_X86_REG_RIP, FAUX["CreateWindowExW"] + 1)
                return
            if et["etape"] == 0:      # apres WM_NCCREATE -> WM_NCCALCSIZE
                et["etape"] = 1
                appeler_wndproc(uc_, et["wndproc"], et["hwnd"], 0x83, 1,
                                TAMPON_CREATESTRUCT + 0x80)
                return
            if et["etape"] == 1:      # apres WM_NCCALCSIZE -> WM_CREATE
                et["etape"] = 2
                appeler_wndproc(uc_, et["wndproc"], et["hwnd"], 1, 0,
                                TAMPON_CREATESTRUCT)
                return
            if et["etape"] == 2:      # apres WM_CREATE -> WM_SIZE (800x600)
                et["etape"] = 3
                appeler_wndproc(uc_, et["wndproc"], et["hwnd"], 5, 0,
                                (600 << 16) | 800)
                return
            if et["etape"] == 3:      # apres WM_SIZE -> WM_MOVE
                et["etape"] = 4
                appeler_wndproc(uc_, et["wndproc"], et["hwnd"], 3, 0,
                                (100 << 16) | 100)
                return
            if et["etape"] == 4:      # apres WM_MOVE -> WM_SHOWWINDOW
                et["etape"] = 5
                appeler_wndproc(uc_, et["wndproc"], et["hwnd"], 0x18, 1, 0)
                return
            # apres WM_CREATE -> CreateWindowExW retourne hwnd
            et = wndproc_attente.pop()
            log(f"  -> CreateWindowExW retourne hwnd {et['hwnd']:#x}")
            uc_.reg_write(UC_X86_REG_RSP, et["rsp"])
            uc_.reg_write(UC_X86_REG_RAX, et["hwnd"])
            uc_.reg_write(UC_X86_REG_RIP, FAUX["CreateWindowExW"] + 1)  # ret
            return
        log("  MAGIC_RET inattendu -> stop")
        uc_.emul_stop()
        return
    nom = FAUX_REV.get(adresse)
    if not nom:
        return
    fn = APIS.get(nom)
    if fn:
        fn(uc_)
        # les stubs qui gerent RIP eux-memes (CreateWindowExW) posent RIP ;
        # les autres laissent le RET (0xC3) du trampoline s'executer
        if uc_.reg_read(UC_X86_REG_RIP) == adresse:
            pass
    else:
        api_generic(uc_, nom)

uc.hook_add(UC_HOOK_CODE, crochet_code, begin=TRAMP, end=TRAMP + 0x2000)
uc.hook_add(UC_HOOK_CODE, crochet_code, begin=MAGIC_RET, end=MAGIC_RET + 0x10)

def crochet_faute(uc_, acces, adresse, taille, valeur, user):
    rip = uc_.reg_read(UC_X86_REG_RIP)
    print(f"\n[FAUTE] acces={acces} adresse={adresse:#x} taille={taille} RIP={rip:#x}")
    off = rip - BASE
    print(f"        RIP - BASE = {off:#x} " +("(dans l'image)" if 0 <= off < 0x11000 else "(HORS IMAGE !)"))
    print(f"        dernieres actions :")
    for l in journal[-15:]:
        print("          ", l)
    etat["fini"] = True
    etat["raison"] = f"faute {acces} a {adresse:#x} depuis RIP {rip:#x}"
    return False

uc.hook_add(UC_HOOK_MEM_INVALID, crochet_faute)

# ---------------- lancement ----------------
sp = STACK + STACK_SZ - 0x1000
sp &= ~0xF
uc.mem_write(sp - 8, struct.pack("<Q", MAGIC_RET + 0x100))   # sortie de secours
sp -= 8
uc.reg_write(UC_X86_REG_RSP, sp)
uc.reg_write(UC_X86_REG_RCX, BASE)      # hInstance
uc.reg_write(UC_X86_REG_RDX, 1)         # DLL_PROCESS_ATTACH
uc.reg_write(UC_X86_REG_R8, 0)
print(f"[emu] base={BASE:#x} entree={BASE + entry_rva:#x} "
      f"({len(slots)} slots IAT remplis)")
try:
    uc.emu_start(BASE + entry_rva, MAGIC_RET + 0x100, timeout=30_000_000)
except Exception as exc:
    print(f"\n[EXCEPTION] {exc}")
    rip = uc.reg_read(UC_X86_REG_RIP)
    print(f"  RIP final = {rip:#x} (offset image {rip - BASE:#x})")
    for l in journal[-15:]:
        print("   ", l)

print(f"\n[emu] fini : {etat['raison'] or 'propre'} ; "
      f"{len(journal)} appels journalises")
