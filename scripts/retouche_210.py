#!/usr/bin/env python3
"""
ENTRÉE 210 — LA RETOUCHE DOUBLE DU BUILD dev.7 (sur la pièce dev.6).

[D54-QUATRIÈME / IAT-SANS-SÉPARATEURS] : le build dev.6 posait les quatre
plages FirstThunk CONTIGUËS (kernel32@0x2400, user32@0x2450, gdi32@0x24E0,
double@0x2818) — le chargeur du terrain (Win11 26300, le chemin FirstThunk
de la leçon D97) marche chaque plage jusqu'au slot NULL : la marche de
kernel32 déborde dans les noms user32, RegisterClassExW résout à NULL,
l'entrée appelle le NUL — 0xC0000005 sur les deux vitrines, sans dialogue.
LA RETOUCHE : l'IAT ENTIERE relogée à 0x3100 (région née zéro), quatre
plages SÉPARÉES PAR NULL, préremplies des RVA de noms (le motif D54),
descripteurs dirigés, dir[12] mis à jour, les 63 sites d'appel repointés,
les vieilles plages VIDÉES. Aucune adresse scellée ne bouge (R7) — la
taille demeure 127488 octets.

[EAX-SANS-SIGNE] : les blocs rendaient leurs codes d'échec par
« mov eax, imm32 » — EAX seul, les 32 bits hauts de RAX à zéro : le contrat
publié (c_int64 au scénario) lisait 0xfffffffe != -2. LA RETOUCHE : chaque
« mov eax, nég » devient « push imm8 ; pop rax » (5 octets, extension de
signe 64 bits native) ; les deux passages 32 bits de loupe-01 deviennent
movsxd. loupe-03 ne rend jamais négatif (vérifié) — intact.

Le qword version @0x2E80 : 0x00010006 -> 0x00010007.
"""
import struct, hashlib, sys

SRC = '/home/z/my-project/loupe-kit-7/loupe.exe'
DST = '/home/z/my-project/build-dev7/loupe.exe'

data = bytearray(open(SRC, 'rb').read())
assert len(data) == 127488, f"taille inattendue {len(data)}"

# --- la carte des sections (.rdata: RVA 0x2000 -> fichier 0x1200) --------------
def r2o(rva): return rva - 0x2000 + 0x1200     # dans .rdata
def o2r(off): return off - 0x1200 + 0x2000

# --- 1. LES QUATRE PLAGES : anciennes bornes, nouvelles bornes ------------------
# (index des feuilles dans l'ordre des OFT du fichier)
PLAGES = [
    # (rva_old, n, rva_new)  — l'ordre des feuilles suit l'OFT
    (0x2400, 10, 0x3100),   # kernel32
    (0x2450, 18, 0x3158),   # user32
    (0x24E0,  6, 0x31F0),   # gdi32
    (0x2818,  3, 0x3228),   # user32 — la double entrée démo
]
OFT = {0x2400: 0x28A0, 0x2450: 0x2900, 0x24E0: 0x29A0, 0x2818: 0x29E0}

# la table de correspondance slot ancien -> slot neuf
slot_map = {}
for old, n, new in PLAGES:
    for i in range(n):
        slot_map[old + 8*i] = new + 8*i

# --- 2. LA NOUVELLE IAT : préremplie des RVA de noms (le motif D54) -------------
nouvelle = bytearray(b'\x00' * 0x148)          # 0x3100 .. 0x3248
for old, n, new in PLAGES:
    oft_rva = OFT[old]
    for i in range(n):
        # la valeur OFT (RVA hint/nom) — lue dans le fichier
        val = struct.unpack_from('<Q', data, r2o(oft_rva) + 8*i)[0]
        assert val != 0 and val & (1 << 63) == 0, f"OFT invalide @ {hex(oft_rva+8*i)}"
        off_new = new - 0x3100
        struct.pack_into('<Q', nouvelle, off_new + 8*i, val)
# les séparateurs NULL sont déjà posés (région née zéro entre les plages)
# vérifie les bornes des séparateurs :
assert struct.unpack_from('<Q', nouvelle, 0x3150-0x3100)[0] == 0
assert struct.unpack_from('<Q', nouvelle, 0x31E8-0x3100)[0] == 0
assert struct.unpack_from('<Q', nouvelle, 0x3220-0x3100)[0] == 0
assert struct.unpack_from('<Q', nouvelle, 0x3240-0x3100)[0] == 0

# pose la nouvelle IAT (la région 0x3100-0x3248 est née zéro — vérifiée)
assert data[r2o(0x3100):r2o(0x3248)] == b'\x00' * 0x148, "la région n'est pas libre"
data[r2o(0x3100):r2o(0x3248)] = nouvelle

# --- 3. LES DESCRIPTEURS : FirstThunk redirigés (OFT/Name intacts) --------------
DESC = r2o(0x2830)
for k, (old, n, new) in enumerate(PLAGES):
    off = DESC + 20*k
    oft, tds, fwd, name_rva, ft = struct.unpack_from('<IIIII', data, off)
    assert ft == old, f"descripteur #{k}: FT={hex(ft)} != {hex(old)}"
    # OFT et Name demeurent ; SEUL FirstThunk bouge
    struct.pack_into('<I', data, off + 16, new)
# le terminateur (5e descripteur) est déjà zéro

# --- 4. dir[12] (l'IAT déclarée) : la plage neuve contiguë -----------------------
opt = struct.unpack_from('<I', data, 0x3C)[0] + 24
struct.pack_into('<II', data, opt + 112 + 12*8, 0x3100, 0x148)

# --- 5. LES VIEILLES PLAGES VIDÉES (un slot mort doit être VIDE) -----------------
data[r2o(0x2400):r2o(0x2510)] = b'\x00' * 0x110
data[r2o(0x2818):r2o(0x2830)] = b'\x00' * 0x18

# --- 6. LES 63 SITES D'APPEL repointés (FF 15 disp32) ---------------------------
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)

def sites_indirects(rva0, rva1, foff):
    """rend [(rva_site, cible_ancienne)] pour chaque call/jmp [rip+X]"""
    out = []
    for i in md.disasm(bytes(data[foff:foff + (rva1 - rva0)]), rva0):
        if i.mnemonic in ('call', 'jmp') and i.op_str.startswith('qword ptr [rip'):
            disp = int(i.op_str.split('rip')[1].split(']')[0].replace(' ', ''), 0)
            out.append((i.address, i.address + i.size + disp, i.size))
    return out

tous = sites_indirects(0x1000, 0x2000, 0x200) + sites_indirects(0x4000, 0xE000, 0x3200)
repoints = 0
for site, cible, taille in tous:
    if cible in slot_map:
        assert taille == 6, f"taille inattendue à {hex(site)}"
        off = None
        if 0x1000 <= site < 0x2000:  off = 0x200 + (site - 0x1000)
        else:                        off = 0x3200 + (site - 0x4000)
        # vérifie l'encodage FF 15
        assert data[off] == 0xFF and data[off+1] == 0x15, f"encodage à {hex(site)}"
        nouveau_disp = slot_map[cible] - (site + 6)
        assert -2**31 <= nouveau_disp < 2**31, "disp32 hors bornes"
        struct.pack_into('<i', data, off + 2, nouveau_disp)
        repoints += 1
print(f"[IAT] {repoints} sites d'appel repointés (sur {len(tous)} indirects scannés)")
assert repoints >= 60, "trop peu de sites repointés — vérifier"

# --- 7. [EAX-SANS-SIGNE] : mov eax, nég -> push imm8 ; pop rax ------------------
BLOCS = [(0x4080, 0x4380), (0x4240, 0x4380), (0x4380, 0x4440), (0x4940, 0x49C0),
         (0x5740, 0x5800), (0x6240, 0x6500), (0x6500, 0x6740)]
patche = 0
for rva0, rva1 in dict.fromkeys(BLOCS):
    off0 = 0x3200 + (rva0 - 0x4000)
    for i in md.disasm(bytes(data[off0:off0 + (rva1 - rva0)]), rva0):
        if i.mnemonic == 'mov' and i.op_str.startswith('eax, 0x'):
            v = int(i.op_str.split(', ')[1], 16)
            # SEULS les rendus : valeur imm8 ([-128,-1]) — exclut les
            # constantes de comparaison (ex. le 0x80000000 de la limite
            # 2 Go @0x4106, hors plage imm8). Les verdicts nommés du
            # build sont TOUS dans [-7,-1] (FIN..VERROUILLÉ).
            if v >= 0xFFFFFF80:
                off = 0x3200 + (i.address - 0x4000)
                assert data[off] == 0xB8, f"encodage mov eax à {hex(i.address)}"
                imm8 = v - (1 << 32)          # la valeur signée
                # push imm8 ; pop rax ; nop ; nop  (5 octets -> 5 octets)
                data[off:off+5] = bytes([0x6A, imm8 & 0xFF, 0x58, 0x90, 0x90])
                patche += 1
print(f"[SIGNE] {patche} rendus négatifs étendus au 64 bits")

# les DEUX passages de loupe-01 (les erreurs des sous-blocs remontent) :
# 0x41A0: mov r13d, eax  (41 89 C5) -> movsxd r13, eax (4C 63 D8)
# 0x41A8: mov eax, r13d  (44 89 E8) -> movsxd rax, r13d (49 63 C5)
off = 0x3200 + (0x41A0 - 0x4000)
assert data[off:off+3] == bytes.fromhex('4189c5'), "0x41A0 inattendu"
data[off:off+3] = bytes.fromhex('4c63e8')   # movsxd r13, eax
off = 0x3200 + (0x41A8 - 0x4000)
assert data[off:off+3] == bytes.fromhex('4489e8'), "0x41A8 inattendu"
data[off:off+3] = bytes.fromhex('4963c5')   # movsxd rax, r13d
print("[SIGNE] les deux passages de loupe-01 passés en movsxd")

# --- 8. LE QWORD VERSION : dev.7 ------------------------------------------------
off = r2o(0x2E80)
assert struct.unpack_from('<Q', data, off)[0] == 0x00010006
struct.pack_into('<Q', data, off, 0x00010007)

# --- 9. LA PIÈCE NEUVE -----------------------------------------------------------
assert len(data) == 127488, "LA TAILLE A CHANGÉ — R7 ROMPUE"
open(DST, 'wb').write(bytes(data))
print(f"[OK] {DST} — {len(data)} octets, sha256 {hashlib.sha256(bytes(data)).hexdigest()}")
