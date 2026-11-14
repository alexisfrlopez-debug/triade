#!/usr/bin/env python3
"""99_preuve_lea_exe.py — LA PREUVE OCTET PAR OCTET sur la pièce RÉELLE
(loupe.exe 98354ff6…, la pièce du dépôt == le bac) : le lea du journal au
slot loupe-02 (RVA 0x4240) vise-t-il 0xE4A0 (le layout, la vérité D161)
ou 0xE4E0 (la constante du scénario livré) ? Le lea du cadre et les trois
appels IAT contrôlés aussi — la boucle du journal lue depuis l'EXE, pas
depuis la notation (la leçon 286 : jamais éprouver sa propre copie)."""
import hashlib
import pathlib
import struct
import sys

EXE = pathlib.Path("/home/z/my-project/work/triade/scripts/campagne_d204/"
                   "unite-02-T/kit/loupe.exe")
SLOT = 0x4240
TAILLE = 320

data = EXE.read_bytes()
print(f"[pièce] loupe.exe  {len(data)} o  sha256 {hashlib.sha256(data).hexdigest()[:16]}…")

# ---- PE : RVA → offset fichier (la table des sections) ----------------------
e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
nb_sections = struct.unpack_from("<H", data, e_lfanew + 6)[0]
taille_option = struct.unpack_from("<H", data, e_lfanew + 20)[0]
table = e_lfanew + 24 + taille_option
sections = []
for i in range(nb_sections):
    off = table + 40 * i
    nom = data[off:off + 8].rstrip(b"\x00").decode("ascii", "replace")
    vsize, vaddr, rsize, raddr = struct.unpack_from("<IIII", off and data, off + 8)
    sections.append((nom, vaddr, vsize, raddr, rsize))
    print(f"[section] {nom:<8} RVA 0x{vaddr:05X}–0x{vaddr + vsize:05X}  "
          f"fichier 0x{raddr:05X} ({rsize} o)")


def rva_vers_offset(rva):
    for nom, vaddr, vsize, raddr, rsize in sections:
        if vaddr <= rva < vaddr + vsize:
            return raddr + (rva - vaddr)
    return None


# ---- le slot : les lea RIP-relatifs et les call IAT --------------------------
off = rva_vers_offset(SLOT)
assert off is not None, "slot hors image"
code = data[off:off + TAILLE]
print(f"\n[slot] loupe-02 RVA 0x{SLOT:04X} → fichier 0x{off:05X}, {len(code)} o lus")

# parcours manuel : on cherche les motifs encodés
#   48 8D 1D dd dd dd dd   lea rbx, [rip + disp32]   (le cadre)
#   4C 8D 0D dd dd dd dd   lea r14, [rip + disp32]   (le journal)
#   4C 8D 05 dd dd dd dd   lea r8,  [rip + disp32]
#   48 8D 0D / 48 8D 15 / 48 8D 0D  lea rcx/rdx, …
#   FF 15 dd dd dd dd      call qword ptr [rip + disp32]  (l'IAT)
i = 0
trouves = []
while i < len(code) - 6:
    b0, b1, b2 = code[i], code[i + 1], code[i + 2]
    if b0 in (0x48, 0x4C) and b1 == 0x8D and (b2 & 0xC7) == 0x05:  # lea r, [rip+disp]
        disp = struct.unpack_from("<i", code, i + 3)[0]
        cible = SLOT + i + 7 + disp
        reg = ((b2 >> 3) & 7) | (8 if b0 == 0x4C else 0)
        noms = {0: "rax", 1: "rcx", 2: "rdx", 3: "rbx", 4: "rsp", 5: "rbp",
                6: "rsi", 7: "rdi", 8: "r8", 9: "r9", 10: "r10", 11: "r11",
                12: "r12", 13: "r13", 14: "r14", 15: "r15"}
        trouves.append((SLOT + i, "lea", noms[reg], cible, code[i:i + 7].hex()))
        i += 7
        continue
    if b0 == 0xFF and b1 == 0x15:  # call [rip + disp32]
        disp = struct.unpack_from("<i", code, i + 2)[0]
        cible = SLOT + i + 6 + disp
        trouves.append((SLOT + i, "call IAT", "[rip]", cible, code[i:i + 6].hex()))
        i += 6
        continue
    i += 1

IAT = {"0x3118": "CreateFileW", "0x3120": "GetFileSizeEx", "0x3128": "SetFilePointerEx",
       "0x3130": "ReadFile", "0x3140": "CloseHandle", "0x3148": "GetLastError"}
print("\n[le slot décodé — les lea et les call, depuis l'EXE RÉEL]")
for adresse, genre, reg, cible, hexa in trouves:
    etiquette = IAT.get(f"0x{cible:04X}", "")
    print(f"  0x{adresse:04X}  {genre:<8} {reg:<6} → 0x{cible:04X}  {etiquette}   "
          f"[{hexa}]")

# ---- le verdict ---------------------------------------------------------------
cibles = {c for _, _, _, c, _ in trouves}
print("\n[VERDICT]")
print(f"  le CADRE   visé par le lea : "
      f"{'0xE000' if 0xE000 in cibles else 'ABSENT'} (le scénario dit R_CADRE=0xE000)")
print(f"  le JOURNAL visé par le lea : "
      f"{'0xE4A0' if 0xE4A0 in cibles else ('0xE4E0' if 0xE4E0 in cibles else 'AUTRE')}")
print(f"  — le layout (D161, la source unique) : R_JOURNAL = 0xE4A0")
print(f"  — le scénario livré (le juge du kit) : R_JOURNAL = 0xE4E0 (+0x40)")
if 0xE4A0 in cibles:
    print("  ⇒ LA PIÈCE EST DROITE : son lea vise le layout (0xE4A0).")
    print("    LES DEUX ROUGE V2 SONT L'ÉCART DU JUGE (le scénario pose le journal")
    print("    à 0xE4E0 ; la pièce lit son journal à 0xE4A0 — le compte lu vaut")
    print("    zéro, les entrées ne sont jamais recouvertes).")
elif 0xE4E0 in cibles:
    print("  ⇒ LA PIÈCE PORTE L'ÉCART (lea à 0xE4E0 ≠ le layout 0xE4A0).")
else:
    print("  ⇒ NI L'UN NI L'AUTRE : à examiner à la main.")
sys.exit(0)
