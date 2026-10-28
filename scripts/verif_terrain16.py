#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain16 — vérification indépendante du livrable D70 (terrain.16).

  A. STATIQUE — superviseur-terrain16.exe relu de zéro : identité, génération
     terrain16, porte R10 27/27, les 4 lea repointés 0x3100 (et 0x3EA0
     définitivement orphelin — xref exhaustif), GABARIT_PUT quoté --data-binary
     @"…" + -m 120 (unique, ancien absent, --fail ×3 intacts), correctifs
     D68/D69 intacts (relais S33 code=NN, nettoyage 4 fichiers, noms
     réordonnés, étiquette espace, session --http1.1), kit byte-identique,
     diff 15->16 borné aux 70 octets autorisés, région d'accueil vierge et
     hors porte, capacité >= pires cas.
  B. ÉMULATION (unicorn, sections .text/.text2/.rsrc/.blob PROTÉGÉES contre
     l'écriture — comme le vrai Windows : c'est le manque de cette protection
     qui rendait la panne invisible à l'oracle depuis terrain.5) — le VRAI
     .gab (0x61B8) du binaire, appelé comme sup-35 l'appelle (rbx extrait du
     PROPRE lea du binaire testé, r15 = gabarit, rbp = 0) :
     E1 RÉGRESSION : terrain.15 + GABARIT_SESSION + jeton réel 254 car.
        -> FAUTE D'ÉCRITURE à 0x4000 (.text2) : LA PANNE DU RUN 00:56
        REPRODUITE SUR ÉMULATEUR ;
     E2 LE FIX : terrain.16 + même gabarit + même jeton -> 484 o composés
        à 0x3100, commande EXACTE (octet par octet) ;
     E3 LE PUT QUOTÉ : terrain.16 + GABARIT_PUT + chemin « My Drive » AVEC
        ESPACES + URL de session 286 o -> commande quotée exacte ;
     E4 RÉGRESSION : terrain.15 + même PUT -> faute d'écriture à 0x4000
        (la seconde mine, désamorcée par le même déménagement) ;
     E5 LA MARGE : terrain.16 + jeton de 480 car. (capacité TAMPON_JETON
        entière) -> commande de 710 o composée sans faute.
"""

import hashlib
import pathlib
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO = pathlib.Path("/home/z/my-project/triade")
EXE15 = REPO / "terrain/livraison/superviseur-terrain15.exe"
EXE16 = REPO / "terrain/livraison/superviseur-terrain16.exe"

MD5_16 = "34ee9f58ada0bf6cf76cc8a9c05bc869"
SHA_16 = "c7134af57276cdcc0f72389f25ab033b32c809e6567956977399b952ebf86f9e"

data = EXE16.read_bytes()
base15 = EXE15.read_bytes()
ok = 0


def check(cond, lab):
    global ok
    if not cond:
        print(f"ECHEC : {lab}")
        sys.exit(1)
    ok += 1


pe = pefile.PE(data=data, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase


def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.SizeOfRawData:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None


off = lambda r: rva2off(r)  # noqa: E731
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

# ---------------------------------------------------------------- identité
check(len(data) == 62464, "taille")
check(hashlib.md5(data).hexdigest() == MD5_16, "md5")
check(hashlib.sha256(data).hexdigest() == SHA_16, "sha256")

# ---------------------------------------------------------------- génération
check(bytes(data[off(0x2ADA) - 8:off(0x2ADA) + 1]) == b"terrain16", "L00")
check(bytes(data[off(0x4366) - 8:off(0x4366) + 1]) == b"terrain16", "S00")
check(struct.unpack_from("<H", data, 0x5CD4)[0] == 16
      and struct.unpack_from("<H", data, 0x5CDC)[0] == 16, "VERSIONINFO 16")
check(data[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.16",
      "FileVersion 0.5.16")
check(data[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain16", "ProductVersion")

# ---------------------------------------------------------------- porte R10
toff = off(0x2450)
k = 0
while struct.unpack_from("<IIQ", data, toff + 16 * k)[0] != 0:
    rva, ln, sm = struct.unpack_from("<IIQ", data, toff + 16 * k)
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    check(s == sm, f"R10[{k}] verte")
    k += 1
check(k == 27, "27 entrées R10")

# ------------------------------------- le déménagement D70 : 4 lea -> 0x3100
SITES = [(0x5E0E, "rbx", "sup-35 composition .gab"),
         (0x4F5C, "rdx", "sup-36 source WriteFile"),
         (0x68D2, "rdx", "sup-37 dest lecture vérif kit"),
         (0x6902, "rcx", "sup-37 source memcmp vérif kit")]
TAMPON_COMPO = 0x3100
FIN_COMPO = 0x3860
for rva, reg, role in SITES:
    ins = list(md.disasm(bytes(data[off(rva):off(rva) + 7]), rva))
    mem_ops = [op for op in ins[0].operands if op.type == 0x3]  # X86_OP_MEM
    cible = rva + ins[0].size + mem_ops[0].mem.disp
    check(f"{ins[0].mnemonic} {ins[0].op_str}".startswith(f"lea {reg}")
          and cible == TAMPON_COMPO, f"lea {reg} @{rva:#x} -> 0x3100 ({role})")

# xref exhaustif : plus AUCUNE référence à 0x3EA0 ; région 0x3100-0x3860 vierge
ZONES_CODE = [(0x1000, 0x400, 0x1000), (0x4000, 0x2e00, 0x300),
              (0x4300, 0x2e00 + 0x300, 0x40), (0x4C00, 0x2e00 + 0xC00, 0x200),
              (0x4E00, 0x2e00 + 0xE00, 0x1C0), (0x5000, 0x2e00 + 0x1000, 0x200),
              (0x5200, 0x2e00 + 0x1200, 0x1C0), (0x5400, 0x2e00 + 0x1400, 0x3C0),
              (0x5800, 0x2e00 + 0x1800, 0x5C0), (0x5E00, 0x2e00 + 0x1E00, 0x4C0),
              (0x6600, 0x2e00 + 0x2600, 0x400)]
for va, raw, taille in ZONES_CODE:
    for insn in md.disasm(bytes(data[raw:raw + taille]), va):
        for op in insn.operands:
            if op.type == 0x3 and op.mem.base == 41:  # X86_OP_MEM, RIP
                c = insn.address + insn.size + op.mem.disp
                check(c != 0x3EA0, f"0x3EA0 encore référencé @{insn.address:#x}")
                check(not (TAMPON_COMPO <= c < FIN_COMPO)
                      or insn.address in [s for s, _, _ in SITES],
                      f"référence inattendue vers la région libre @{insn.address:#x}")
check(all(b == 0 for b in data[off(TAMPON_COMPO):off(FIN_COMPO)]),
      "région d'accueil vierge dans le fichier")
for j in range(27):
    rva, ln, _ = struct.unpack_from("<IIQ", data, toff + 16 * j)
    check(rva + ln <= TAMPON_COMPO or FIN_COMPO <= rva,
          f"R10[{j}] ne couvre pas la région d'accueil")

# ------------------------------------- le correctif PUT : guillemets + -m 120
GAB_PUT_16 = (b'curl.exe -s --fail -m 120 -o NUL -X PUT '
              b'--data-binary @"\x06"' + b" " * 7 + b"\x07\x00")
GAB_PUT_15 = (b"curl.exe -s --fail --max-time 120 -o NUL -X PUT "
              b"--data-binary @\x06 \x07\x00")
check(len(GAB_PUT_16) == 67 and data.count(GAB_PUT_16) == 1,
      "GABARIT_PUT terrain.16 unique (67 o)")
check(GAB_PUT_15 not in data, "GABARIT_PUT terrain.15 ABSENT")
check(data[off(0x4AD7):off(0x4AD7) + 67] == GAB_PUT_16, "gabarit PUT @0x4AD7")
check(data.count(b"--fail") == 3, "--fail ×3 (T2×2 + PUT) intacts")

# ------------------------------------- périmètre intouché (D68/D69 en place)
GAB_SESSION_15 = (b"curl.exe -s --http1.1 -m 30" + b" " * 6 +
                  b"-o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
check(data[off(0x49EF):off(0x49EF) + 232] == GAB_SESSION_15,
      "GABARIT_SESSION --http1.1 (D69) intouché")
check(data[off(0x4894):off(0x4894) + 16] == b'access_token": "',
      "étiquette espace (D69) intouchée")
check(bytes(data[off(0x62AA):off(0x62AA) + 22])
      == b"S33 T3 jeton KO code=\x00", "relais S33 code=NN (D68) conservé")
check(f"{list(md.disasm(bytes(data[off(0x6113):off(0x6113) + 5]), 0x6113))[0].op_str}"
      == "0x628a", "handler S33 = jmp relais (D68)")
_ins617d = list(md.disasm(bytes(data[off(0x617D):off(0x617D) + 6]), 0x617D))[0]
check(f"{_ins617d.mnemonic} {_ins617d.op_str}" == "mov r13d, 4",
      "nettoyage 4 fichiers (D68) conservé")
for site, cible in ((0x5EFC, 0x635A), (0x5F83, 0x6323), (0x5FF8, 0x6335)):
    disp = struct.unpack_from("<i", data, off(site) + 3)[0]
    check(site + 7 + disp == cible, f"lea noms @{site:#x} -> {cible:#x} (D68)")
check(data[0x6410:0xF010] == base15[0x6410:0xF010],
      "démo + proxy + en-têtes byte-identiques à terrain.15")
check(data[0xF010:] == base15[0xF010:], "annexe jetons byte-identique")

# ------------------------------------- diff 15 -> 16 borné (70 octets)
AUTORISES = [(off(r), off(r) + 7) for r, _, _ in SITES]
AUTORISES += [(off(0x4AD7), off(0x4AD7) + 67),
              (off(0x2ADA), off(0x2ADA) + 1), (off(0x4366), off(0x4366) + 1),
              (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
              (0x5DC2, 0x5DC4), (0x5ECC, 0x5ECE)]
for j in (18, 21, 22, 23):
    AUTORISES.append((toff + 16 * j + 8, toff + 16 * j + 16))
diffs = [i for i in range(len(data)) if data[i] != base15[i]]
check(all(any(a <= i < b for a, b in AUTORISES) for i in diffs),
      f"diff borné ({len(diffs)} octets)")
check(len(diffs) <= 78, f"diff compact ({len(diffs)} octets)")
print(f"[A] STATIQUE : {ok} contrôles VERTS "
      f"(diff 15->16 : {len(diffs)} octets bornés)")

# =============================================================================
# B. ÉMULATION — le VRAI .gab du binaire, sections protégées comme Windows
# =============================================================================
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_PROT_ALL  # noqa: E402
from unicorn import (UC_HOOK_MEM_INVALID, UC_HOOK_MEM_WRITE_PROT,  # noqa: E402
                     UC_PROT_READ, UC_PROT_WRITE, UC_PROT_EXEC)
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RBX,  # noqa: E402
                               UC_X86_REG_R15, UC_X86_REG_RBP, UC_X86_REG_RAX)

GAB = 0x61B8                    # le formateur (sup-35)
MAGIC = BASE + 0x300000         # adresse de retour factice
PILE = BASE + 0x210000
# permissions réelles des sections (en-têtes PE) : c'est le monde du run
PROT_SECTIONS = [(0x1000, 0x1000, UC_PROT_READ | UC_PROT_EXEC),      # .text
                 (0x2000, 0x1000, UC_PROT_READ),                     # .rdata
                 (0x3000, 0x1000, UC_PROT_READ | UC_PROT_WRITE),     # .data
                 (0x4000, 0x2E00, UC_PROT_READ | UC_PROT_EXEC),      # .text2
                 (0x7000, 0x800, UC_PROT_READ),                      # .rsrc
                 (0x8000, 0x8D10, UC_PROT_READ),                     # .blob
                 (0x11000, 0x1000, UC_PROT_READ | UC_PROT_WRITE)]    # .idata


def extraire_rbx(exe):
    """Le PROPRE lea rbx du binaire testé (@0x5E0E) dit où composer."""
    ins = list(md.disasm(bytes(exe[off(0x5E0E):off(0x5E0E) + 7]), 0x5E0E))
    op = [o for o in ins[0].operands if o.type == 0x3][0]
    return 0x5E0E + ins[0].size + op.mem.disp


def composer(exe, rva_gabarit, champ_srcs, taille_attendue):
    """Exécute le VRAI .gab. champ_srcs : {rva: octets} posés avant l'appel.
    Retourne (faute_ou_None, tampon_lu)."""
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    uc.mem_map(BASE, 0x120000, UC_PROT_ALL)
    uc.mem_map(PILE, 0x10000, UC_PROT_ALL)          # pile d'exécution .gab
    uc.mem_map(MAGIC & ~0xFFF, 0x1000, UC_PROT_ALL)  # page de retour factice
    for s in pe.sections:                      # l'image entière d'abord
        if s.SizeOfRawData:
            uc.mem_write(BASE + s.VirtualAddress,
                         bytes(exe[s.PointerToRawData:
                                   s.PointerToRawData + s.SizeOfRawData]))
    for rva, ln, prot in PROT_SECTIONS:        # PUIS les protections réelles
        ln_align = (ln + 0xFFF) & ~0xFFF       # unicorn : tailles alignées page
        uc.mem_protect(BASE + rva, ln_align, prot)
    for rva, octets in champ_srcs.items():
        uc.mem_write(BASE + rva, octets + b"\x00")
    fautes = []

    def hook_inv(uc_, acces, adresse, taille, valeur, ud):
        fautes.append((acces, adresse))
        return False

    uc.hook_add(UC_HOOK_MEM_INVALID | UC_HOOK_MEM_WRITE_PROT, hook_inv)
    S = PILE + 0x800
    uc.mem_write(S - 8, struct.pack("<Q", MAGIC))
    uc.reg_write(UC_X86_REG_RSP, S - 8)
    uc.reg_write(UC_X86_REG_RBX, BASE + extraire_rbx(exe))
    uc.reg_write(UC_X86_REG_R15, BASE + rva_gabarit)
    uc.reg_write(UC_X86_REG_RBP, 0)
    try:
        uc.emu_start(BASE + GAB, MAGIC, count=2_000_000)
        err = None
    except Exception as e:                     # noqa: BLE001 — UcError attendu
        err = str(e)
    tampon = bytes(uc.mem_read(BASE + extraire_rbx(exe), taille_attendue))
    return err, fautes, tampon


# --- fixtures : formes RÉELLES constatées (valeurs synthétiques) -------------
JETON_REEL = b"ya29." + b"A" * 249                       # 254 car. (run 00:56)
URL_SESSION = (b"https://www.googleapis.com/upload/drive/v3/files"
               b"?uploadType=resumable&upload_id=" + b"S" * 206)   # 286 car.
CHEMIN_MYDRIVE = (b"C:\\Users\\Jean Dupont\\My Drive"
                  b"\\terrain_20261028_005629.txt")      # espaces garantis
check(len(JETON_REEL) == 254, "fixture jeton = 254 car. (taille du run)")
check(len(URL_SESSION) == 286, "fixture URL = 286 car. (constatée D69)")
check(b" " in CHEMIN_MYDRIVE, "fixture chemin avec espaces (« My Drive »)")

SESSION_ATTENDUE = (b'curl.exe -s --http1.1 -m 30      -o NUL '
                    b'-D terrain_session.txt -X POST '
                    b'-H "Content-Type: application/json" '
                    b'-H "Authorization: Bearer ' + JETON_REEL +
                    b'" --data @terrain_meta.json '
                    b'https://www.googleapis.com/upload/drive/v3/files'
                    b'?uploadType=resumable')
check(len(SESSION_ATTENDUE) == 484, "commande session attendue = 484 o")

PUT_ATTENDU = (b'curl.exe -s --fail -m 120 -o NUL -X PUT --data-binary @"'
               + CHEMIN_MYDRIVE + b'"' + b" " * 7 + URL_SESSION)

# --- E1 : RÉGRESSION — la panne du run 00:56 sur terrain.15 ------------------
err, fautes, _ = composer(base15, 0x49EF, {0x3B70: JETON_REEL}, 4)
check(err is not None, "E1 : terrain.15 .gab session -> ÉCHEC (faute)")
check(any(a == BASE + 0x4000 for _, a in fautes),
      f"E1 : faute d'ÉCRITURE à 0x4000 (.text2) — obtenue : "
      f"{[(hex(a)) for _, a in fautes]}")
print(f"[B] E1 : terrain.15 + jeton réel -> FAUTE À 0x4000 (err: {err[:60]}) "
      f"— LA PANNE DU RUN 00:56 REPRODUITE SUR ÉMULATEUR")

# --- E2 : LE FIX — la même composition sur terrain.16 ------------------------
err, fautes, tampon = composer(data, 0x49EF, {0x3B70: JETON_REEL}, 485)
check(err is None and not fautes, "E2 : terrain.16 .gab session sans faute")
check(tampon[:484] == SESSION_ATTENDUE, "E2 : commande session EXACTE (484 o)")
check(tampon[484] == 0, "E2 : NUL terminal posé à 0x3100+484")
print("[B] E2 : terrain.16 + jeton réel -> 484 o composés à 0x3100, "
      "commande octet-exacte, NUL posé")

# --- E3 : LE PUT QUOTÉ — chemin « My Drive » + URL 286 o ---------------------
err, fautes, tampon = composer(data, 0x4AD7, {0x3910: CHEMIN_MYDRIVE,
                                              0x3B70: URL_SESSION},
                               len(PUT_ATTENDU) + 1)
check(err is None and not fautes, "E3 : terrain.16 .gab PUT sans faute")
check(tampon[:len(PUT_ATTENDU)] == PUT_ATTENDU,
      "E3 : commande PUT quotée EXACTE (chemin avec espaces)")
check(tampon[len(PUT_ATTENDU)] == 0, "E3 : NUL terminal")
print(f"[B] E3 : PUT composé {len(PUT_ATTENDU)} o avec chemin « My Drive » "
      f"GUILLEMETS en place : --data-binary @\"…\"")

# --- E4 : RÉGRESSION — le PUT aurait débordé aussi sur terrain.15 ------------
err, fautes, _ = composer(base15, 0x4AD7, {0x3910: CHEMIN_MYDRIVE,
                                           0x3B70: URL_SESSION}, 4)
check(err is not None, "E4 : terrain.15 .gab PUT -> ÉCHEC (faute)")
check(any(a == BASE + 0x4000 for _, a in fautes),
      "E4 : faute d'écriture à 0x4000 — la seconde mine démontrée")
print("[B] E4 : terrain.15 + PUT réel -> FAUTE À 0x4000 : la seconde mine "
      "(372+ o > 352) désamorcée par le même déménagement")

# --- E5 : LA MARGE — jeton de 480 car. (capacité TAMPON_JETON entière) -------
JETON_MAX = b"ya29." + b"M" * 475                          # 480 car.
SESSION_MAX = (b'curl.exe -s --http1.1 -m 30      -o NUL '
               b'-D terrain_session.txt -X POST '
               b'-H "Content-Type: application/json" '
               b'-H "Authorization: Bearer ' + JETON_MAX +
               b'" --data @terrain_meta.json '
               b'https://www.googleapis.com/upload/drive/v3/files'
               b'?uploadType=resumable')
err, fautes, tampon = composer(data, 0x49EF, {0x3B70: JETON_MAX},
                               len(SESSION_MAX) + 1)
check(err is None and not fautes, "E5 : jeton 480 car. sans faute")
check(tampon[:len(SESSION_MAX)] == SESSION_MAX, "E5 : commande 710 o exacte")
print(f"[B] E5 : jeton de 480 car. -> commande de {len(SESSION_MAX)} o "
      f"composée sans faute (marge : {FIN_COMPO - TAMPON_COMPO} o)")

print(f"\n[verif] TOUT VERT : {ok} contrôles statiques + 5 émulations .gab "
      f"(2 régressions terrain.15 reproduites, 3 compositions terrain.16 exactes)")
print(f"  md5    {hashlib.md5(data).hexdigest()}")
print(f"  sha256 {hashlib.sha256(data).hexdigest()}")
