#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE SIMULATEUR DE VITRINE — loupe.exe dev.7 exécutée au labo sous Unicorn.

La méthode du scénario généralisée au CHEMIN DE L'ENTRÉE : l'image mappée,
l'IAT branchée sur des relais Python, l'entrée 0x5C00 vécue, la boucle à
messages vivante (un WM_PAINT distribué au WndProc), la peinture entière.
Toute faute d'exécution NOMME son adresse — le témoin terrain ne nomme
que 0xC0000005 ; le labo, lui, tiendra le lieu exact.
"""
import struct
import sys
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RIP, UC_X86_REG_RAX, UC_X86_REG_RCX
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/run8/loupe.exe"
BASE = 0x140000000
STACK = 0x7FF900000000
STACK_TAILLE = 0x200000
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
print(f"characteristics fichier : {chars:#06x} (DLL={bool(chars & 0x2000)}, EXE={bool(chars & 0x0002)})")

# --- la carte IAT (slot → nom) -------------------------------------------
imp_rva = struct.unpack_from("<I", d, opt + 112 + 8)[0]


def r2o(rva):
    for (nom, va, vs, ptr, raw) in sections:
        if va <= rva < va + max(vs, raw):
            return ptr + (rva - va)
    return None


slots = []  # (rva, nom)
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

# --- montage ---------------------------------------------------------------
uc = Uc(UC_ARCH_X86, UC_MODE_64)
uc.mem_map(BASE, 0x21000)
uc.mem_write(BASE, d[0:0x200])
for (nom, va, vs, ptr, raw) in sections:
    uc.mem_write(BASE + va, d[ptr:ptr + raw])
uc.mem_map(STACK, STACK_TAILLE)
uc.mem_map(PAGE_API, 0x2000)
uc.mem_map(PAGE_SCRATCH, 0x10000)

# l'IAT : chaque slot reçoit l'adresse de son relais
ADRESSE = {}
for idx, (rva, nom) in enumerate(slots):
    cible = PAGE_API + 0x20 + idx * 0x10
    uc.mem_write(BASE + rva, struct.pack("<Q", cible))
    ADRESSE[cible] = nom

# la ligne de commande (« [1/3] la vitrine vide » : aucun fichier)
CMDLINE = PAGE_SCRATCH + 0x100
uc.mem_write(CMDLINE, "loupe.exe\0".encode("utf-16-le"))
WNDPROC = {"ptr": None}
ETAT = {"getmessage": 0, "journal": []}


def lever(uc, val):
    """Simule le « ret » d'un relais : RIP = [RSP], RSP += 8, RAX = val."""
    rsp = uc.reg_read(UC_X86_REG_RSP)
    ret = struct.unpack("<Q", uc.mem_read(rsp, 8))[0]
    uc.reg_write(UC_X86_REG_RSP, rsp + 8)
    uc.reg_write(UC_X86_REG_RIP, ret)
    uc.reg_write(UC_X86_REG_RAX, val)


def lire_cstr_w(uc, a, maxn=260):
    out = b""
    while len(out) < maxn * 2:
        c = uc.mem_read(a + len(out), 2)
        if c == b"\0\0":
            break
        out += c
    return out.decode("utf-16-le", "replace")


def service(uc, nom):
    rcx = uc.reg_read(UC_X86_REG_RCX)
    if nom == "GetModuleHandleW":
        return lever(uc, BASE)
    if nom == "GetCommandLineW":
        return lever(uc, CMDLINE)
    if nom == "LoadCursorW":
        return lever(uc, 0xDEAD0001)
    if nom == "RegisterClassExW":
        # capture le WndProc (@+0x08 de la classe : cbSize@0 style@4 lpfnWndProc@8)
        WNDPROC["ptr"] = struct.unpack("<Q", uc.mem_read(rcx + 0x08, 8))[0]
        ETAT["journal"].append(f"RegisterClassExW : WndProc = {WNDPROC['ptr']:#x}")
        return lever(uc, 0x1234)
    if nom == "CreateWindowExW":
        # LA SÉQUENCE RÉELLE : CreateWindowExW ENVOIE des messages au WndProc
        # AVANT de rendre la poignée — le vitrine les vit
        if WNDPROC["ptr"]:
            for (m, wp, lp) in ((0x81, 0, PAGE_SCRATCH + 0x400),   # WM_NCCREATE
                                (0x83, 0, 0),                      # WM_NCCALCSIZE
                                (0x1, 0, PAGE_SCRATCH + 0x400),    # WM_CREATE
                                (0x5, 0, (543 << 16) | 624),       # WM_SIZE
                                (0x3, 0, (50 << 16) | 50)):        # WM_MOVE
                rsp = uc.reg_read(UC_X86_REG_RSP)
                uc.reg_write(UC_X86_REG_RSP, rsp - 8)
                uc.mem_write(rsp - 8, struct.pack("<Q", RETOUR_MAGIQUE))
                import unicorn.x86_const as x
                uc.reg_write(x.UC_X86_REG_RCX, 0x60000)
                uc.reg_write(x.UC_X86_REG_RDX, m)
                uc.reg_write(x.UC_X86_REG_R8, wp)
                uc.reg_write(x.UC_X86_REG_R9, lp)
                uc.reg_write(UC_X86_REG_RIP, WNDPROC["ptr"])
                ETAT["journal"].append(f"  [création] WndProc msg {m:#x}")
                uc.emu_start(WNDPROC["ptr"], RETOUR_MAGIQUE)
        ETAT["journal"].append("CreateWindowExW → hwnd 0x60000")
        return lever(uc, 0x60000)
    if nom == "ShowWindow":
        return lever(uc, 1)
    if nom == "GetMessageW":
        n = ETAT["getmessage"]
        if n == 0:  # UN WM_PAINT, vécu par son témoin
            uc.mem_write(rcx, struct.pack("<QIIQQ", 0x60000, 0xF, 0, 0, 0))
            ETAT["journal"].append("GetMessageW → WM_PAINT distribué")
            ETAT["getmessage"] += 1
            return lever(uc, 1)
        ETAT["journal"].append("GetMessageW → WM_QUIT")
        return lever(uc, 0)
    if nom == "TranslateMessage":
        return lever(uc, 0)
    if nom == "DispatchMessageW":
        # appelle LE WndProc de la pièce avec le message
        hwnd, msg, wp, lp = struct.unpack("<QIIQQ", uc.mem_read(rcx, 32))[:4]
        ETAT["journal"].append(f"DispatchMessageW → WndProc(hwnd={hwnd:#x}, msg={msg:#x})")
        rsp = uc.reg_read(UC_X86_REG_RSP)
        uc.reg_write(UC_X86_REG_RSP, rsp - 8)
        uc.mem_write(rsp - 8, struct.pack("<Q", RETOUR_MAGIQUE))
        import unicorn.x86_const as x
        uc.reg_write(x.UC_X86_REG_RCX, hwnd)
        uc.reg_write(x.UC_X86_REG_RDX, msg)
        uc.reg_write(x.UC_X86_REG_R8, wp)
        uc.reg_write(x.UC_X86_REG_R9, lp)
        uc.reg_write(UC_X86_REG_RIP, WNDPROC["ptr"])
        return
    if nom == "BeginPaint":
        # (hwnd en rcx, ps en rdx) — ps.hdc @+0 ; fErase @+8 ; rcPaint @+0x10
        import unicorn.x86_const as x2
        rdx = uc.reg_read(x2.UC_X86_REG_RDX)
        uc.mem_write(rdx, struct.pack("<Q", 0x70000))
        uc.mem_write(rdx + 8, b"\x01" + b"\0" * 7)
        uc.mem_write(rdx + 0x10, struct.pack("<iiii", 0, 0, 640, 480))
        return lever(uc, 0x70000)
    if nom == "GetStockObject":
        return lever(uc, 0x70001)
    if nom == "SelectObject":
        return lever(uc, 0x70002)
    if nom == "GetTextMetricsW":
        # (hdc en rcx, tm en rdx) : tmHeight @0, tmAveCharWidth @+0x14
        import unicorn.x86_const as x2
        rdx = uc.reg_read(x2.UC_X86_REG_RDX)
        tm = bytearray(0x3C)
        struct.pack_into("<i", tm, 0, 16)
        struct.pack_into("<i", tm, 0x14, 8)
        uc.mem_write(rdx, bytes(tm))
        return lever(uc, 1)
    if nom == "GetClientRect":
        # (hwnd en rcx, rc en rdx)
        import unicorn.x86_const as x2
        rdx = uc.reg_read(x2.UC_X86_REG_RDX)
        uc.mem_write(rdx, struct.pack("<iiii", 0, 0, 640, 480))
        return lever(uc, 1)
    if nom in ("TextOutW", "EndPaint", "InvalidateRect", "DefWindowProcW",
               "SetScrollInfo", "GetScrollInfo", "DestroyWindow", "PostQuitMessage",
               "MessageBeep", "SetTextColor", "SetBkColor", "MessageBoxW"):
        if nom == "MessageBoxW":
            ETAT["journal"].append(f"!! MessageBoxW : « {lire_cstr_w(uc, rcx)} »")
        return lever(uc, 1 if nom != "DefWindowProcW" else 0)
    if nom == "ExitProcess":
        ETAT["journal"].append(f"ExitProcess({rcx}) — LA SORTIE PROPRE")
        ETAT["exit"] = rcx
        uc.emu_stop()
        return
    # défaut : rend 1
    return lever(uc, 1)


def crochet_code(uc, adresse, taille, donnees_util):
    if adresse == RETOUR_MAGIQUE:
        return lever(uc, 0)  # le retour de DispatchMessageW
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
    import sys as _s
    rip = uc.reg_read(UC_X86_REG_RIP)
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    try:
        code = uc.mem_read(rip, 16)
        ins = next(md.disasm(bytes(code), rip))
        texte = f"{ins.mnemonic} {ins.op_str}"
    except Exception:
        texte = "??"
    print(f"\n*** FAUTE {'écriture' if acces == 1 else 'lecture' if acces == 0 else 'fetch'} "
          f"@ {adresse:#x} — RIP {rip:#x} : {texte} ***", flush=True)
    print(f"*** L'ADRESSE NOMMÉE : {adresse:#x} "
          f"({'BASE+' + hex(adresse - BASE) if BASE <= adresse < BASE + 0x21000 else 'hors image'}) ***",
          flush=True)
    import unicorn.x86_const as x
    for nomreg in ("RAX", "RBX", "RCX", "RDX", "RSI", "RDI", "RBP", "RSP", "R8", "R9", "R10", "R11", "R12", "R13", "R14", "R15"):
        v = uc.reg_read(getattr(x, "UC_X86_REG_" + nomreg))
        print(f"    {nomreg} = {v:#018x}", flush=True)
    return False


uc.hook_add(UC_HOOK_CODE, crochet_code, begin=PAGE_API, end=PAGE_API + 0x2000)
uc.hook_add(UC_HOOK_MEM_INVALID, crochet_faute)

# --- le départ : l'entrée telle que le chargeur l'appelle ------------------
RSP_DEPART = STACK + STACK_TAILLE - 0x10000
RETOUR_IMPOSSIBLE = 0x00DEAD0000000000
uc.reg_write(UC_X86_REG_RSP, RSP_DEPART)
uc.mem_write(RSP_DEPART, struct.pack("<Q", RETOUR_IMPOSSIBLE))
try:
    uc.emu_start(BASE + 0x5C00, RETOUR_IMPOSSIBLE)
except Exception as e:
    print(f"\n*** EXCEPTION : {e} ***")

print("\n=== LE JOURNAL DU SIMULATEUR ===")
for l in ETAT["journal"]:
    print(f"  {l}")
print(f"\nverdict : {'sortie propre ExitProcess(' + str(ETAT.get('exit')) + ')' if 'exit' in ETAT else 'MORT SANS EXITPROCESS'}")
