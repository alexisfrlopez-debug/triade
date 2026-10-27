#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verif_terrain15 — vérification indépendante du livrable D69 (terrain.15).

  A. STATIQUE — superviseur-terrain15.exe relu de zéro : identité, génération
     terrain15, porte R10 27/27, NOUVELLE étiquette en place (unique) /
     ANCIENNE absente, GABARIT_SESSION --http1.1 -m 30 (232 o, marqueur \x07,
     suffixe identique à terrain.14), site d'appel sup-22 intouché,
     correctifs terrain.14 intacts (relais S33 code=NN, nettoyage 4 fichiers,
     noms réordonnés, leas), périmètre intouché (T2 --fail ×2, PUT --fail,
     GABARIT_JETON, démo/proxy/annexe byte-identiques à terrain.14), diff
     14→15 borné aux 46 octets autorisés.
  B. ÉMULATION (unicorn) — le VRAI sup-22 (0x1D40) du binaire patché,
     appelé comme sup-35 l'appelle (r9=16, arrêt guillemet, dest 480 o) :
     E1 json OAuth RÉEL (indenté, jeton synthétique de 254 car. — la taille
        constatée en live) + NOUVELLE étiquette -> rax=254, jeton exact,
        NUL terminal posé ;
     E2 en-têtes de session HTTP/1.1 réalistes (dump de 846 o, « Location: »
        à l'octet ~194 — la sonde bac) + étiquette « Location: » + arrêt CR
        -> rax=286, URL exacte ;
     E3 RÉGRESSION : json compact (l'ancienne fixture oracle) + nouvelle
        étiquette -> rax=0, destination intacte (échec honnête, pas de
        corruption) ;
     E4 DOCUMENTATION : json indenté + ANCIENNE étiquette -> rax=0 : la
        panne de terrain.14 reproduite sur le même émulateur.
"""

import hashlib
import pathlib
import struct
import sys

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

REPO = pathlib.Path("/home/z/my-project/triade")
EXE14 = REPO / "terrain/livraison/superviseur-terrain14.exe"
EXE15 = REPO / "terrain/livraison/superviseur-terrain15.exe"

MD5_15 = "e1240f834e6e2e9878097805eb48efb6"
SHA_15 = "7e50fbbc08d157e11212d1e05d7cacceeebdb0d8125062d8dd0f0caa829b5489"

data = EXE15.read_bytes()
base14 = EXE14.read_bytes()
ok = 0


def check(cond, lab):
    global ok
    if not cond:
        print(f"ECHEC : {lab}")
        sys.exit(1)
    ok += 1


def rva2off(rva):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress + s.SizeOfRawData:
            return s.PointerToRawData + (rva - s.VirtualAddress)
    return None


pe = pefile.PE(data=data, fast_load=True)
BASE = pe.OPTIONAL_HEADER.ImageBase
off = lambda r: rva2off(r)  # noqa: E731
md = Cs(CS_ARCH_X86, CS_MODE_64)

# ---------------------------------------------------------------- identité
check(len(data) == 62464, "taille")
check(hashlib.md5(data).hexdigest() == MD5_15, "md5")
check(hashlib.sha256(data).hexdigest() == SHA_15, "sha256")

# ---------------------------------------------------------------- génération
check(bytes(data[off(0x2ADA) - 8:off(0x2ADA) + 1]) == b"terrain15", "L00")
check(bytes(data[off(0x4366) - 8:off(0x4366) + 1]) == b"terrain15", "S00")
check(struct.unpack_from("<H", data, 0x5CD4)[0] == 15
      and struct.unpack_from("<H", data, 0x5CDC)[0] == 15, "VERSIONINFO 15")
check(data[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] == "0.5.15",
      "FileVersion 0.5.15")
check(data[0x5EC0:0x5ECE].decode("utf-16-le") == "rrain15", "ProductVersion")

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

# ------------------------------------------------- le correctif D69 en place
ETIQ_NOUVEAU = b'access_token": "'
ETIQ_VIEUX = b'"access_token":"'
check(data.count(ETIQ_NOUVEAU) == 1, "nouvelle étiquette unique")
check(ETIQ_VIEUX not in data, "ancienne étiquette ABSENTE")
check(bytes(data[off(0x4894):off(0x4894) + 16]) == ETIQ_NOUVEAU,
      "nouvelle étiquette @0x4894")
check(bytes(data[off(0x4894) + 16:off(0x4894) + 26])
      == b"Location: ", "ETIQ_LOCATION contiguë intacte")

GAB_SESSION_15 = (b"curl.exe -s --http1.1 -m 30" + b" " * 6 +
                  b"-o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
GAB_SESSION_14 = (b"curl.exe -s" + b" " * 8 +
                  b"--max-time 30 -o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
check(len(GAB_SESSION_15) == 232 and data.count(GAB_SESSION_15) == 1,
      "GABARIT_SESSION terrain.15 unique")
check(GAB_SESSION_15[32:] == GAB_SESSION_14[32:], "suffixe identique au 14")
check(data[off(0x49EF):off(0x49EF) + 232] == GAB_SESSION_15,
      "gabarit session @0x49EF")
check(b"--http1.1 -m 30" in data, "--http1.1 présent")
check(data.count(b"--fail") == 3, "--fail ×3 (T2×2 + PUT) intouchés")

# site d'appel sup-22 : octet identique à terrain.14 (aucun code touché)
check(data[off(0x5F26):off(0x5F26) + 30]
      == base14[off(0x5F26):off(0x5F26) + 30], "site d'appel intouché")
ins = list(md.disasm(bytes(data[off(0x5F26):off(0x5F26) + 40]), 0x5F26))
check(f"{ins[0].mnemonic} {ins[0].op_str}" == "lea r8, [rip - 0x1699]"
      and f"{ins[1].mnemonic} {ins[1].op_str}" == "mov r9d, 0x10"
      and f"{ins[2].mnemonic} {ins[2].op_str}"
      == "mov dword ptr [rsp + 0x20], 0x22",
      "lea -> 0x4894, longueur 16, arrêt guillemet")
check(0x5F2D - 0x1699 == 0x4894, "cible du lea = étiquette")

# ------------------------------------- correctifs terrain.14 intacts
check(list(md.disasm(bytes(data[off(0x6113):off(0x6113) + 5]), 0x6113))[0]
      .op_str == "0x628a", "handler = jmp 0x628a")
check(bytes(data[off(0x62AA):off(0x62AA) + 22])
      == b"S33 T3 jeton KO code=\x00", "chaîne S33 code=NN conservée")
check(f"{list(md.disasm(bytes(data[off(0x617D):off(0x617D) + 6]), 0x617D))[0].mnemonic} "
      f"{list(md.disasm(bytes(data[off(0x617D):off(0x617D) + 6]), 0x617D))[0].op_str}"
      == "mov r13d, 4", "nettoyage 4 fichiers conservé")
for site, cible in ((0x5EFC, 0x635A), (0x5F83, 0x6323), (0x5FF8, 0x6335)):
    disp = struct.unpack_from("<i", data, off(site) + 3)[0]
    check(site + 7 + disp == cible, f"lea @{site:#x} -> {cible:#x}")
check(data[0x6410:0xF010] == base14[0x6410:0xF010],
      "démo + proxy + en-têtes byte-identiques")
check(data[0xF010:] == base14[0xF010:], "annexe jetons byte-identique")
GAB_JETON_14 = (b"curl.exe -s" + b" " * 8 +
                b"--max-time 30 -o terrain_jeton.json "
                b"--data @terrain_req.txt \x08\x00")
check(data.count(GAB_JETON_14) == 1, "GABARIT_JETON intouché")

# ------------------------------------- diff 14 -> 15 borné (46 octets)
AUTORISES = [(off(0x4894), off(0x4894) + 16),      # étiquette
             (off(0x49EF), off(0x49EF) + 232),     # gabarit session
             (off(0x2ADA), off(0x2ADA) + 1), (off(0x4366), off(0x4366) + 1),
             (0x5CD4, 0x5CD6), (0x5CDC, 0x5CDE),
             (0x5DC2, 0x5DC4), (0x5ECC, 0x5ECE),   # versions
             (toff + 16 * 23 + 8, toff + 16 * 23 + 16)]  # somme R10[23]
diffs = [i for i in range(len(data)) if data[i] != base14[i]]
check(all(any(a <= i < b for a, b in AUTORISES) for i in diffs),
      f"diff borné ({len(diffs)} octets)")
print(f"[A] STATIQUE : {ok} contrôles VERTS "
      f"(diff 14->15 : {len(diffs)} octets bornés)")

# =============================================================================
# B. ÉMULATION — le VRAI sup-22 du binaire patché
# =============================================================================
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64  # noqa: E402
from unicorn.x86_const import (UC_X86_REG_RSP, UC_X86_REG_RCX,  # noqa: E402
                               UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_R9,
                               UC_X86_REG_RAX)

SUP22 = BASE + 0x1D40
MAGIC = BASE + 0x300000           # adresse de retour factice
DEST = BASE + 0x220000            # destination (TAMPON_JETON simulé, 480 o)
PILE = BASE + 0x210000


def monter():
    uc = Uc(UC_ARCH_X86, UC_MODE_64)
    for s in pe.sections:
        debut = (BASE + s.VirtualAddress) & ~0xFFF
        fin = (BASE + s.VirtualAddress
               + max(s.Misc_VirtualSize, s.SizeOfRawData) + 0xFFF) & ~0xFFF
        uc.mem_map(debut, fin - debut)
        if s.SizeOfRawData:
            uc.mem_write(BASE + s.VirtualAddress,
                         bytes(data[s.PointerToRawData:
                                    s.PointerToRawData + s.SizeOfRawData]))
    uc.mem_map(BASE + 0x200000, 0x100000)     # pile + tampons
    uc.mem_map(MAGIC & ~0xFFF, 0x1000)        # page de retour factice
    return uc


def balayer_sup22(tampon, etiquette, lon_etiq, arret, cap=0x1E0):
    """Appelle le sup-22 réel comme sup-35 le fait. `etiquette` : soit une
    ADRESSE (int — étiquette dans l'image), soit des OCTETS (écrits dans un
    tampon de montage). Retourne (rax, dest)."""
    uc = monter()
    if isinstance(etiquette, (bytes, bytearray)):
        ad_etiq = BASE + 0x240000
        uc.mem_write(ad_etiq, bytes(etiquette) + b"\x00")
    else:
        ad_etiq = etiquette
    S = PILE + 0x800
    uc.mem_write(S - 8, struct.pack("<Q", MAGIC))          # adresse de retour
    uc.mem_write(S + 0x20, struct.pack("<Q", arret))       # 5e arg : octet d'arrêt
    uc.mem_write(S + 0x28, struct.pack("<Q", DEST))        # 6e arg : destination
    uc.mem_write(S + 0x30, struct.pack("<Q", cap))         # 7e arg : capacité
    uc.mem_write(DEST, b"\xAA" * 512)                      # destination pré-marquée
    BUF = BASE + 0x230000
    uc.mem_write(BUF, bytes(tampon))
    uc.reg_write(UC_X86_REG_RCX, BUF)
    uc.reg_write(UC_X86_REG_RDX, len(tampon))
    uc.reg_write(UC_X86_REG_R8, ad_etiq)
    uc.reg_write(UC_X86_REG_R9, lon_etiq)
    uc.reg_write(UC_X86_REG_RSP, S - 8)
    uc.emu_start(SUP22, MAGIC, count=5_000_000)
    rax = uc.reg_read(UC_X86_REG_RAX)
    return rax, bytes(uc.mem_read(DEST, 512))


# --- fixtures réalistes (formes constatées en live, valeurs synthétiques) ----
JETON_SYNTH = b"ya29." + b"A" * 249            # 254 car. — taille réelle constatée
JSON_REEL = (b'{\n  "access_token": "' + JETON_SYNTH +
             b'",\n  "expires_in": 3599,\n'
             b'  "scope": "https://www.googleapis.com/auth/drive",\n'
             b'  "token_type": "Bearer",\n'
             b'  "refresh_token_expires_in": 117314\n}')
check(len(JETON_SYNTH) == 254, "jeton synthétique = 254 car. (taille réelle)")
check(JSON_REEL.startswith(b'{\n  "access_token": "'), "format indenté réel")
URL_SYNTH = (b"https://www.googleapis.com/upload/drive/v3/files"
             b"?uploadType=resumable&upload_id=" + b"S" * 206)   # 286 car.
check(len(URL_SYNTH) == 286, "fixture URL = 286 car. (taille réelle constatée)")
HEADERS_H1 = (b"HTTP/1.1 200 OK\r\n"
              b"Content-Type: text/plain; charset=utf-8\r\n"
              b"X-GUploader-UploadID: SYNTH-" + b"U" * 100 + b"\r\n"
              b"Location: " + URL_SYNTH + b"\r\n"
              b"Cache-Control: no-cache, no-store, max-age=0, must-revalidate\r\n"
              b"Date: Wed, 28 Oct 2026 00:00:00 GMT\r\n"
              b"Server: ESF\r\n"
              b"Content-Length: 0\r\n"
              b"Alt-Svc: h3=\":443\"; ma=2592000\r\n\r\n")
check(0 <= HEADERS_H1.find(b"Location: ") < 600,
      "« Location: » dans les 600 premiers octets (contrainte de lecture sup-35)")
print(f"[fixtures] json indenté {len(JSON_REEL)} o ; en-têtes h1 "
      f"{len(HEADERS_H1)} o ; Location à l'octet {HEADERS_H1.find(b'Location: ')}")
JSON_COMPACT = (b'{"access_token":"' + JETON_SYNTH
                + b'","expires_in":3600,"token_type":"Bearer"}')

# --- E1 : json indenté réel + nouvelle étiquette -> LE JETON ----------------
rax, dest = balayer_sup22(JSON_REEL, BASE + 0x4894, 16, 0x22)
check(rax == 254, f"E1 rax=254 (obtenu {rax})")
check(dest[:254] == JETON_SYNTH, "E1 jeton extrait exact")
check(dest[254] == 0, "E1 NUL terminal posé")
print("[B] E1 : json OAuth INDENTÉ réel + nouvelle étiquette -> rax=254, "
      "jeton exact, NUL posé — le correctif extrait ce que Google répond")

# --- E2 : en-têtes h1 + « Location: » -> l'URL de session -------------------
rax, dest = balayer_sup22(HEADERS_H1, BASE + 0x48A4, 10, 0x0D)   # ETIQ_LOCATION
check(rax == 286, f"E2 rax=286 (obtenu {rax})")
check(dest[:286] == URL_SYNTH, "E2 URL de session extraite exacte")
print("[B] E2 : en-têtes HTTP/1.1 (sonde bac) + « Location: » -> rax=286, "
      "URL exacte — la session passe avec --http1.1")

# --- E3 : régression — json compact + nouvelle étiquette -> échec honnête ---
rax, dest = balayer_sup22(JSON_COMPACT, BASE + 0x4894, 16, 0x22)
check(rax == 0, "E3 rax=0 sur json compact")
check(dest[:8] == b"\xAA" * 8, "E3 destination intacte")
print("[B] E3 : json compact (ancienne fixture oracle) -> rax=0, destination "
      "intacte — échec honnête, aucune corruption")

# --- E4 : documentation — json indenté + ANCIENNE étiquette -> la panne 14 ---
rax, dest = balayer_sup22(JSON_REEL, ETIQ_VIEUX, 16, 0x22)
check(rax == 0, "E4 rax=0 avec l'ancienne étiquette")
check(dest[:8] == b"\xAA" * 8, "E4 destination intacte")
print("[B] E4 : json indenté + ANCIENNE étiquette -> rax=0 : la panne de "
      "terrain.14 reproduite sur le même émulateur (panne d'un espace)")

print(f"\n[verif] TOUT VERT : {ok} contrôles statiques + 4 émulations sup-22 "
      f"sur le binaire patché")
print(f"  md5    {hashlib.md5(data).hexdigest()}")
print(f"  sha256 {hashlib.sha256(data).hexdigest()}")
