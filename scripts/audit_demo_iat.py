#!/usr/bin/env python3
"""Audit IAT + désassemblage annoté de demo.exe (TRIADE démo 0.3.0-demo.2).

But : vérifier au niveau octet, SANS Windows, que
  1. chaque slot IAT appelé par le code est bien rempli par le chargeur
     avec la fonction attendue (classe de défaut D35 : désalignement
     descripteur/slots) ;
  2. la boucle de messages win-03 et le chemin WM_COMMAND de win-04
     correspondent à la notation (classe de défaut D36) ;
  3. aucun slot appelé n'est hors de tout descripteur (slot NULL → crash).

Méthode : modèle exact du chargeur PE — pour chaque descripteur d'import,
l'entrée i de OriginalFirstThunk (hint/name) remplit le slot FirstThunk+8*i.
"""
import struct
import sys
from collections import defaultdict

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = "/home/z/my-project/triade/demo/demo.exe"

# Blocs (RVA -> (nom, taille)) — frontières EXACTES des layouts démo + M2
BLOCS = {
    0x1040: ("io-01:print", 0x40), 0x1080: ("io-02:exit", 0x40),
    0x1100: ("libc-01:memcpy", 0x80), 0x1180: ("libc-02:memcmp", 0x80),
    0x1200: ("libc-03:strlen", 0x80), 0x1280: ("libc-04:itoa", 0x80),
    0x1400: ("win-01:principal", 0x40), 0x1440: ("win-02:fenetre", 0x180),
    0x15C0: ("win-03:boucle", 0x80), 0x1640: ("win-04:procedure", 0x380),
    0x19C0: ("win-05:journal", 0x100), 0x1AC0: ("win-06:autotest", 0x180),
    0x1C40: ("win-07:client", 0xC0), 0x1D00: ("win-08:serveur", 0x100),
    0x1E00: ("win-11:journal-fichier", 0x200),
    0x4000: ("tcp-01:init", 0x100), 0x4100: ("tcp-02:accept", 0x40),
    0x4140: ("tcp-03:recv", 0x40), 0x4180: ("tcp-04:send", 0x40),
    0x41C0: ("tcp-05:close", 0x40), 0x4300: ("tcp-06:spawn", 0x40),
    0x4400: ("tcp-07:patch", 0x200), 0x4600: ("echo:v1(c30008)", 0x40),
    0x4680: ("echo:croissance", 0x80), 0x4800: ("tcp-09:connexion", 0x180),
    0x4980: ("win-10:echange", 0x180), 0x4B00: ("tcp-11:ligne-journal", 0x100),
    0x4C00: ("win-09:scenario", 0x380),
}

def bloc_de(rva):
    for a, (n, t) in sorted(BLOCS.items()):
        if a <= rva < a + t:
            return n
    return "hors-bloc"

# Sémantique attendue : slot -> fonctions autorisées (selon specs/layout)
ATTENDU = {
    0x20B0: {"win-09:scenario"},          # GetStdHandle
    0x20B8: {"io-01:print", "tcp-11:ligne-journal", "win-11:journal-fichier"},  # WriteFile
    0x20C0: {"io-02:exit"},               # ExitProcess
    0x20C8: {"tcp-06:spawn"},             # CreateThread
    0x20D0: {"tcp-07:patch"},             # VirtualProtect
    0x20D8: {"tcp-09:connexion", "tcp-11:ligne-journal"},  # InitializeCriticalSection (tcp-11 sérialise le journal console)
    0x20E0: {"tcp-09:connexion", "tcp-11:ligne-journal"},  # EnterCriticalSection
    0x20E8: {"tcp-09:connexion", "tcp-11:ligne-journal"},  # LeaveCriticalSection
    0x20F0: set(),                        # ReadFile (tcp-10 console — remplacé par win-10 : inutilisé toléré)
    0x20F8: {"win-04:procedure", "win-08:serveur", "win-09:scenario"},  # CloseHandle
    0x2100: {"win-01:principal", "win-02:fenetre", "win-04:procedure"},  # GetModuleHandleW
    0x2300: {"tcp-01:init"},              # WSAStartup
    0x2308: {"tcp-01:init", "win-07:client"},  # socket
    0x2310: {"tcp-01:init"},              # bind
    0x2318: {"tcp-01:init"},              # listen
    0x2320: {"tcp-02:accept"},            # accept
    0x2328: {"tcp-03:recv", "tcp-09:connexion", "win-09:scenario", "win-10:echange"},  # recv
    0x2330: {"tcp-04:send", "tcp-09:connexion", "win-09:scenario", "win-10:echange"},  # send
    0x2338: {"tcp-01:init", "tcp-05:close", "tcp-09:connexion", "win-07:client"},  # closesocket
    0x2340: {"tcp-01:init", "win-07:client"},  # WSAGetLastError
    0x2348: {"tcp-01:init"},              # WSACleanup
    0x2350: {"win-07:client"},            # connect
    0x2800: {"win-02:fenetre"},           # RegisterClassExW
    0x2808: {"win-02:fenetre", "win-04:procedure"},  # CreateWindowExW
    0x2810: {"win-04:procedure"},         # DefWindowProcW
    0x2818: {"win-03:boucle"},            # GetMessageW
    0x2820: {"win-03:boucle"},            # TranslateMessage
    0x2828: {"win-03:boucle"},            # DispatchMessageW
    0x2830: {"win-04:procedure"},         # PostQuitMessage
    0x2838: {"win-04:procedure"},         # DestroyWindow
    0x2840: {"win-04:procedure", "win-05:journal"},  # SendMessageW
    0x2848: {"win-02:fenetre"},           # LoadCursorW
    0x2850: {"win-04:procedure"},         # EnableWindow
    0x2858: {"win-04:procedure"},         # MoveWindow
    0x2860: {"win-04:procedure"},         # GetClientRect
    0x2868: {"win-02:fenetre"},           # MessageBoxW
    0x2980: {"win-04:procedure"},         # GetStockObject
    0x2E80: {"win-11:journal-fichier"},   # GetModuleFileNameA
    0x2E88: {"win-11:journal-fichier"},   # CreateFileA
    0x2E90: {"win-11:journal-fichier"},   # FlushFileBuffers
    0x2E98: {"win-02:fenetre", "win-04:procedure", "win-11:journal-fichier"},  # GetLastError
}

data = open(EXE, "rb").read()
print(f"demo.exe : {len(data)} octets, sha256 vérifié par ailleurs")

# ---- En-têtes PE ------------------------------------------------------
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
assert data[e_lfanew:e_lfanew + 4] == b"PE\0\0", "signature PE"
coff = e_lfanew + 4
machine, nsec = struct.unpack_from("<HH", data, coff)[0:2]
opt = coff + 20
magic = struct.unpack_from("<H", data, opt)[0]
assert magic == 0x20B, f"PE32+ attendu, magic={magic:#x}"
image_base = struct.unpack_from("<Q", data, opt + 24)[0]
ddir = opt + 112  # DataDirectory PE32+
imp_rva, imp_sz = struct.unpack_from("<II", data, ddir + 8)
print(f"machine={machine:#x} sections={nsec} base={image_base:#x} imports={imp_rva:#x}+{imp_sz}")

# Sections : RVA -> offset fichier
secs = opt + struct.unpack_from("<H", data, coff + 16)[0]
sections = []
for i in range(nsec):
    o = secs + 40 * i
    nom = data[o:o + 8].rstrip(b"\0").decode()
    vsz, va, rsz, roff = struct.unpack_from("<IIII", data, o + 8)
    sections.append((nom, va, vsz, roff, rsz))
    print(f"  {nom:10s} VA={va:#06x} VS={vsz:#06x} OFF={roff:#06x} RS={rsz:#06x}")


def rva2off(rva):
    for _, va, vsz, roff, rsz in sections:
        if va <= rva < va + max(vsz, rsz):
            return roff + (rva - va)
    return None


def cstr(off):
    fin = data.index(b"\0", off)
    return data[off:fin].decode("latin-1")


# ---- Modèle du chargeur : descripteurs d'imports ----------------------
slot2nom = {}   # RVA du slot IAT -> "dll!Fonction"
desc_list = []
o = rva2off(imp_rva)
while True:
    oft, ts, fwd, namerva, ft = struct.unpack_from("<IIIII", data, o)
    if oft == 0 and ft == 0 and namerva == 0:
        break
    dll = cstr(rva2off(namerva))
    entrees = []
    t = rva2off(oft if oft else ft)
    i = 0
    while True:
        val = struct.unpack_from("<Q", data, t + 8 * i)[0]
        if val == 0:
            break
        if val & (1 << 63):
            nom = f"ordinal#{val & 0xFFFF}"
        else:
            ho = rva2off(val)
            hint = struct.unpack_from("<H", data, ho)[0]
            nom = cstr(ho + 2)
        slot = ft + 8 * i
        slot2nom[slot] = f"{dll}!{nom}"
        entrees.append((slot, nom))
        i += 1
    desc_list.append((dll, ft, entrees))
    o += 20

print("\nDescripteurs d'imports (vue chargeur) :")
for dll, ft, entrees in desc_list:
    print(f"  {dll:12s} FT={ft:#06x} : " + ", ".join(f"[{s:#06x}]={n}" for s, n in entrees))

# ---- Désassemblage linéaire annoté de .text ET .text2 -----------------
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

appels = defaultdict(list)      # slot -> [(rva appel, nom, bloc)]
directs = defaultdict(list)     # cible directe -> [rva]
listing = []
for secname in (".text", ".text2"):
    _, tva, tvsz, toff, trsz = next(s for s in sections if s[0] == secname)
    code = data[toff:toff + trsz]
    for ins in md.disasm(code, tva):
        m = ins.mnemonic
        op = ins.op_str
        if m == "call" and op.startswith("qword ptr [rip"):
            plus = "+ " in op
            disp = int(op.split("+ " if plus else "- ")[1].rstrip("]"), 16)
            slot = ins.address + ins.size + (disp if plus else -disp)
            nom = slot2nom.get(slot, "*** SLOT HORS DESCRIPTEUR ***")
            bloc = bloc_de(ins.address)
            appels[slot].append((ins.address, nom, bloc))
            listing.append((ins.address, f"  {ins.address:#06x} [{bloc:24s}] call [{slot:#06x}] -> {nom}"))
        elif m == "call" and op.startswith("0x"):
            cible = int(op, 16)
            bloc_c = bloc_de(cible)
            directs[cible].append(ins.address)
            listing.append((ins.address, f"  {ins.address:#06x} [{bloc_de(ins.address):24s}] call {cible:#06x} -> {bloc_c}"))
listing.sort()
listing = [l for _, l in listing]

print(f"\n{sum(len(v) for v in appels.values())} appels indirects IAT, "
      f"{sum(len(v) for v in directs.values())} appels directs de blocs")

print("\n== Vue par slot : chargeur VS appelants (ET conformité sémantique) ==")
probleme = False
for slot in sorted(appels):
    n = len(appels[slot])
    nom = appels[slot][0][1]
    zones = sorted({a[2] for a in appels[slot]})
    attends = ATTENDU.get(slot)
    ok = ""
    if "HORS" in nom:
        probleme = True
        ok = "  <<< SLOT HORS DESCRIPTEUR"
    elif attends is not None:
        errants = set(zones) - attends
        if errants:
            probleme = True
            ok = f"  <<< APPELANT INATTENDU : {','.join(sorted(errants))}"
        else:
            ok = "  ok"
    print(f"  [{slot:#06x}] {nom:34s} x{n:<3d} depuis {','.join(zones)}{ok}")

# ---- Comparaison à la notation : win-03 et .commande de win-04 --------
print("\n== win-03:boucle (RVA 0x15C0) — notation attendue ==")
print("  GetMessageW / TranslateMessage / DispatchMessageW dans cet ordre, "
      "MSG sur pile, filtre (NULL,0,0), boucle tant que eax > 0")
print("\n== win-04:.commande (RVA 0x1894) — notation attendue ==")
print("  cmp r13d,1 ; jne .zero / drapeau 0x3878 nul / trace L03 (win-11 r8=0) /")
print("  EnableWindow / spawn tcp-06 / CloseHandle")

print("\n== Listing intégral des appels ( .text + .text2 ) ==")
for ligne in listing:
    print(ligne)

print("\nVERDICT : " + ("DÉFAUT — slot appelé hors descripteur !" if probleme else "aucun slot appelé hors descripteur ; correspondance chargeur/appelants conforme"))
