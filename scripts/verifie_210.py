#!/usr/bin/env python3
"""VERIFICATION DU BUILD dev.7 (Entrée 210) — recoupement sur pièces, v2."""
import struct, hashlib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

data = open('/home/z/my-project/build-dev7/loupe.exe', 'rb').read()
dev6 = open('/home/z/my-project/loupe-kit-7/loupe.exe', 'rb').read()
md = Cs(CS_ARCH_X86, CS_MODE_64)
ok = True

def check(cond, label):
    global ok
    print(('  OK  ' if cond else '  ÉCHEC  ') + label)
    if not cond: ok = False

print('=== 1. LA PIÈCE ===')
check(len(data) == 127488, f"taille {len(data)} == 127488 (R7 tenue)")
check(struct.unpack_from('<Q', data, 0x2080)[0] == 0x00010007, "qword version @0x2E80 = 0x00010007 (dev.7)")
SHA = hashlib.sha256(data).hexdigest()
print(f'  sha256 = {SHA}')

pe = struct.unpack_from('<I', data, 0x3C)[0]
opt = pe + 24
nsec = struct.unpack_from('<H', data, pe+6)[0]
optsize = struct.unpack_from('<H', data, pe+20)[0]
secs = []
for i in range(nsec):
    s = opt+optsize+i*40
    nm = data[s:s+8].rstrip(b'\x00').decode()
    vsize, vaddr, rsize, raddr = struct.unpack_from('<IIII', data, s+8)
    secs.append((nm, vaddr, vsize, raddr, rsize))
def r2o(rva):
    for nm, va, vs, ra, rs in secs:
        if va <= rva < va + max(vs, rs): return ra + (rva-va)
    return None
def lire(rva, n): return bytes(data[r2o(rva):r2o(rva)+n])

print('=== 2. L\'HABILLAGE D\'IMPORT NEUF (le motif D54 restauré) ===')
imp_rva = struct.unpack_from('<I', data, opt+112+8)[0]
off = r2o(imp_rva)
slots = {}
descs = []
i = 0
while True:
    oft, tds, fwd, name_rva, ft = struct.unpack_from('<IIIII', data, off+i*20)
    if oft == 0 and ft == 0: break
    dll = data[r2o(name_rva):data.index(b'\x00', r2o(name_rva))].decode()
    descs.append((dll, ft, oft))
    j = 0
    while True:
        v = struct.unpack_from('<Q', data, r2o(ft)+8*j)[0]
        if v == 0: break
        slots[ft+8*j] = (dll, v)
        j += 1
    i += 1
PLAGES = [(0x3100, 10, 'kernel32.dll'), (0x3158, 18, 'user32.dll'),
          (0x31F0, 6, 'gdi32.dll'), (0x3228, 3, 'user32.dll')]
for (dll, ft, oft), (aft, an, adll) in zip(descs, PLAGES):
    check(ft == aft and dll == adll, f"descripteur {dll}: FirstThunk @{hex(ft)}")
check(all(len([1 for s in slots if p0 <= s < p0+8*n]) == n for p0, n, _ in PLAGES),
      "les quatre plages marchent au compte exact (séparateurs NULL)")
check(all(struct.unpack_from('<Q', data, r2o(s))[0] != 0 for s in slots),
      f"les {len(slots)} slots du fichier sont PRÉREMLIS (motif D54)")
check(data[r2o(0x2400):r2o(0x2510)] == b'\x00'*0x110, "vieille IAT VIDÉE")
check(data[r2o(0x2818):r2o(0x2830)] == b'\x00'*0x18, "vieille double entrée VIDÉE")
iat_rva, iat_sz = struct.unpack_from('<II', data, opt+112+12*8)
check((iat_rva, iat_sz) == (0x3100, 0x148), f"dir[12] = ({hex(iat_rva)}, {hex(iat_sz)})")

print('=== 3. LES 63 APPELS couverts + la boucle au slot neuf ===')
couverts = set(slots.keys())
def scan(rva0, rva1, foff):
    out = []
    for i in md.disasm(bytes(data[foff:foff+(rva1-rva0)]), rva0):
        if i.mnemonic in ('call','jmp') and i.op_str.startswith('qword ptr [rip'):
            disp = int(i.op_str.split('rip')[1].split(']')[0].replace(' ',''), 0)
            out.append((i.address, i.address+i.size+disp))
    return out
appels = scan(0x1000,0x2000,0x200) + scan(0x4000,0xE000,0x3200)
non_couverts = [(a,c) for a,c in appels if c not in couverts]
check(len(appels) == 63 and not non_couverts,
      f"{len(appels)} appels indirects, tous couverts"
      + (f" — HORS: {[(hex(a),hex(c)) for a,c in non_couverts]}" if non_couverts else ""))
cibles_boucle = [c for a, c in appels if 0x15C0 <= a < 0x1600]
check(cibles_boucle == [0x3228, 0x3230, 0x3238],
      f"la boucle appelle {['%#x' % c for c in cibles_boucle]} (GetMessageW, TranslateMessage, DispatchMessageW)")

print('=== 4. L\'ENTRÉE : le fil GetModuleHandleW au slot neuf ===')
off = 0x3200 + (0x5C00 - 0x4000)
cibles = []
for i in md.disasm(bytes(data[off:off+0x20]), 0x5C00):
    if i.op_str.startswith('qword ptr [rip'):
        disp = int(i.op_str.split('rip')[1].split(']')[0].replace(' ',''), 0)
        cibles.append(i.address+i.size+disp)
check(cibles == [0x3100, 0x3108], "l'entrée: [0x3100] GetModuleHandleW puis [0x3108] GetCommandLineW")

print('=== 5. LES RENDUS SIGNÉS ===')
off = 0x3200 + (0x41D0 - 0x4000)
check(bytes(data[off:off+5]) == bytes([0x6A, 0xFE, 0x58, 0x90, 0x90]), "@0x41D0: push -2 ; pop rax (ABSENT)")
off = 0x3200 + (0x57A4 - 0x4000)
check(bytes(data[off:off+5]) == bytes([0x6A, 0xFF, 0x58, 0x90, 0x90]), "@0x57A4: push -1 ; pop rax (FIN — loupe-13)")
check(lire(0x41A0, 3) == bytes.fromhex('4c63e8'), "@0x41A0: movsxd r13, eax")
check(lire(0x41A8, 3) == bytes.fromhex('4963c5'), "@0x41A8: movsxd rax, r13d")
check(lire(0x4106, 5) == bytes.fromhex('b800000080'), "@0x4106: mov eax, 0x80000000 intact (la borne 2 Go)")

print('=== 6. LES SCELLÉS INTACTS (R7) ===')
check(lire(0x1100, 6) == bytes.fromhex('57564889c848'), "memcpy @0x1100 prologue")
check(lire(0x1180, 6) == bytes.fromhex('31c04d85c074'), "memcmp @0x1180 prologue")
check(lire(0x13C0, 6) == bytes.fromhex('53574889cb48'), "memset @0x13C0 prologue")
check(struct.unpack_from('<I', data, r2o(0x2F00))[0] == 0x428A2F98, "K[64] @0x2F00 (FIPS 0x428a2f98)")
check(lire(0xE210, 8) == b'\xff'*8, "CADRE_VIERGE: poignée INVALIDE @+0x210")
check(lire(0x5DCB, 0x60) == bytes(dev6[r2o(0x5DCB):r2o(0x5DCB)+0x60]), "WndProc @0x5DCB: octets INCHANGÉS")
check(lire(0xC000, 0x2000) == bytes(dev6[r2o(0xC000):r2o(0xC000)+0x2000]),
      "la famille sha M9 @0xC000-0xE000: octets INCHANGÉS")
check(lire(0x5C00, 11) == bytes.fromhex('575641544881ecb0000000'),
      "entrée @0x5C00 prologue (push rdi,rsi,r12; sub rsp,0xb0)")
check(lire(0x4080, 13) == bytes.fromhex('5341544155415641574883ec40'),
      "loupe-01 @0x4080 prologue")
# le rendu : seuls les 10 octets des disp32 repointés diffèrent
o6, o7 = r2o(0x4B00), r2o(0x4B00)
diffs = [i for i in range(0x100) if data[o7+i] != dev6[o6+i]]
check(len(diffs) == 10, f"le rendu @0x4B00: {len(diffs)} octets diffèrent (5 disp32 repointés — attendu 10)")
# la sonde S0 : l'image reste cartographiable (aucune section ne bouge)
check([s[0] for s in secs] == ['.text', '.rdata', '.text2', '.data'], "les quatre sections en place")

print()
print('VERDICT :', 'TOUT VERT — la pièce dev.7 est prête pour le kit' if ok else 'ÉCHEC')
print(f"sha256 dev.7 = {SHA}")
