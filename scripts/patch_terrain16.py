#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.16 — LE TAMPON DE COMPOSITION CHANGE DE PIECE (D70).

LE CONSTAT (run terrain.15, 00:56:29, pièces ENFIN complètes dans le dossier
test : journal + json + req + meta — et le rapport « superviseur s'est fermé
tout seul ») :

  S33 RÉUSSIT POUR LA PREMIÈRE FOIS (correctif D69 : l'étiquette espace).
  Google a répondu en 330 ms, le jeton (254 caractères — taille réelle) est
  extrait, la ligne « S33 T3 jeton OAuth obtenu » est journalisée. Puis le
  superviseur MEURT — silencieusement, sans une ligne de plus — pendant la
  composition de la commande session. Fenêtre fermée, nettoyage jamais exécuté.

LA CAUSE (prouvée au désassemblage + en-têtes PE + timeline Drive) :

  La zone de composition (rbx, posée par « lea rbx » @0x5E0E) vit à
  TAMPON_CMD+0x150 = 0x3EA0. La section .data se termine PILE à 0x4000 :
  la zone offre 352 octets. La commande session composée = 230 littéraux
  + jeton réel 254 = 484 octets. La boucle .gab (écriture octet par octet,
  memcpy du champ) dépasse 0x4000 — première page de .text2, section
  CODE|EXECUTE|READ SANS ÉCRITURE (caractéristiques 0x60000020) —
  violation d'écriture c0000005, mort instantanée du processus.

  Timeline Drive (mtimes préservés) : terrain_req.txt .595 → terrain_jeton.json
  .925 (curl OAuth) → dernière ligne journal .939 → terrain_meta.json .941 →
  plus rien, terrain_session.txt jamais créé. Le crash tient dans la fenêtre
  .941→+2 ms : pile la composition session.

  Défaut LATENT depuis terrain.5 : S33 n'avait JAMAIS réussi avant ce run —
  le chemin S34 n'avait jamais été exécuté sur machine réelle. La fixture
  oracle (jeton de 47 caractères → commande de 277 o) ne débordait pas :
  même classe de panne que D69 (fixture idéalisée masque la réalité).

DEUXIÈME MINE DU MÊME COUP (statique) : la commande PUT composée
  = 63 littéraux + chemin complet + 1 + URL de session 286 ≈ 372+ o > 352 :
  elle aurait débordé AUSSI. Et le chemin complet contient le plus souvent
  un ESPACE (« My Drive », « Jean Dupont ») : --data-binary @chemin avec
  espace casse curl. Le PUT n'a jamais tourné en réel : les deux mines
  sautent ce soir.

LE CORRECTIF (borné, 4 déplacements + 1 gabarit + version, porte R10
recalculée) :

  P1. La région .data [0x3000, 0x3860) est VIDE (2 144 o de zéros,
      aucune référence de code — scan xref exhaustif D70) et hors table R10.
      Les QUATRE références de la base de composition 0x3EA0 y déménagent :
        sup-35 @0x5E0E  lea rbx (base .gab — composition)
        sup-36 @0x4F5C  lea rdx (source WriteFile mode écriture)
        sup-37 @0x68D2  lea rdx (dest ReadFile de la vérif kit, blocs 512 o)
        sup-37 @0x6902  lea rcx (source memcmp de la vérif kit)
      Nouvelle base : TAMPON_COMPO = 0x3100 (1 888 o, chemins/lectures de
      TAMPON_CMD désormais DÉCOUPLÉS de la composition — plus aucune
      contrainte de coexistence).
  P2. GABARIT_PUT @0x4AD7 (67 o, longueur inchangée) : guillemets autour
      du chemin (--data-binary @"…") + --max-time 120 → -m 120 (8 o
      libérés, 2 pour les guillemets, 7 de bourrage). Les espaces du
      chemin (« My Drive ») ne cassent plus curl.
  P3. génération terrain15 → terrain16 (L00, S00, VERSIONINFO).
  P4. sommes R10 recalculées pour les entrées couvrantes (18, 21, 22, 23).

INTOUCHÉ : GABARIT_SESSION/JETON/OAUTH/META (éprouvés en live D69), les
étiquettes, T2 ×2, toute la logique sup-35/36/37 (seuls les 4 déplacements
de 4 octets bougent), démo, proxy, annexe.
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain15.exe"
DST = REPO / "terrain/livraison/superviseur-terrain16.exe"
DEMO9 = REPO / "demo/demo.exe"

MD5_TERRAIN15 = "e1240f834e6e2e9878097805eb48efb6"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"

R10_TABLE_RVA = 0x2450
TAMPON_COMPO = 0x3100          # la nouvelle base (région .data libre, D70)
FIN_COMPO = 0x3860             # premier octet d'état après la région libre

# ------------------------------------------------------------------ zones rva
SITES_LEA = [                  # (rva, octets exacts attendus, registre)
    (0x5E0E, bytes.fromhex("488d1d8be0ffff"), "rbx"),   # sup-35 .gab
    (0x4F5C, bytes.fromhex("488d153defffff"), "rdx"),   # sup-36 écrire
    (0x68D2, bytes.fromhex("488d15c7d5ffff"), "rdx"),   # sup-37 vérif lecture
    (0x6902, bytes.fromhex("488d0d97d5ffff"), "rcx"),   # sup-37 vérif memcmp
]
RVA_GAB_PUT = 0x4AD7           # 67 o (NUL compris)
RVA_L00_DERNIER = 0x2ADA
RVA_S00_DERNIER = 0x4366
# VERSIONINFO : offsets FICHIER (zone .rsrc)
OFF_VI_BIN1, OFF_VI_BIN2 = 0x5CD4, 0x5CDC
OFF_VI_FV, OFF_VI_PV = 0x5DC2, 0x5ECC

# --------------------------------------------------------------- octets vieux
GAB_PUT_15 = (b"curl.exe -s --fail --max-time 120 -o NUL -X PUT "
              b"--data-binary @\x06 \x07\x00")
# -------------------------------------------------------------- octets nouveaux
GAB_PUT_16 = (b'curl.exe -s --fail -m 120 -o NUL -X PUT '
              b'--data-binary @"\x06"' + b" " * 7 + b"\x07\x00")
assert len(GAB_PUT_15) == len(GAB_PUT_16) == 67
assert GAB_PUT_16.count(b'"') == 2


def rva2off(rva):
    if 0x1000 <= rva < 0x2000:
        return 0x400 + (rva - 0x1000)
    if 0x2000 <= rva < 0x3000:
        return 0x1400 + (rva - 0x2000)
    if 0x3000 <= rva < 0x4000:
        d = rva - 0x3000
        return 0x2400 + d if d < 0xA00 else None
    if 0x4000 <= rva < 0x6E00:
        return 0x2E00 + (rva - 0x4000)
    if 0x7000 <= rva < 0x7800:
        return 0x5C00 + (rva - 0x7000)
    if 0x8000 <= rva < 0x10D10:
        return 0x6400 + (rva - 0x8000)
    if 0x11000 <= rva < 0x11200:
        return 0xF200 + (rva - 0x11000)
    return None


def somme_zone(data, rva, ln):
    o = rva2off(rva)
    s = 0
    for i in range(0, ln, 8):
        s = (s + struct.unpack_from("<Q", data, o + i)[0]) & 0xFFFFFFFFFFFFFFFF
    return s


def lire_table(data):
    table_off = rva2off(R10_TABLE_RVA)
    entrees = []
    k = 0
    while True:
        rva, ln, sm = struct.unpack_from("<IIQ", data, table_off + 16 * k)
        if rva == 0:
            return entrees, k, table_off
        entrees.append((rva, ln, sm))
        k += 1
        if k > 60:
            raise ValueError("table R10 sans terminateur")


def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)


# =============================================================================
# 1. GARDES-FOUS
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN15:
    erreur("terrain.15 : md5 inattendu (source altérée ?)")

# 1a. les quatre lea anciens, exacts
for rva, attendu, reg in SITES_LEA:
    o = rva2off(rva)
    if bytes(base[o:o + 7]) != attendu:
        erreur(f"lea @{rva:#x} : octets inattendus")
    disp = struct.unpack_from("<i", attendu, 3)[0]
    if rva + 7 + disp != 0x3EA0:
        erreur(f"lea @{rva:#x} : cible != 0x3EA0")
print("[gardes] 4 lea 0x3EA0 exacts (sup-35 rbx, sup-36 rdx, sup-37 rdx+rcx)")

# 1b. xref exhaustif : les QUATRE sites sont les SEULES références de 0x3EA0
import capstone  # noqa: E402
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
ZONES_CODE = [(0x1000, 0x400, 0x1000), (0x4000, 0x2e00, 0x300),
              (0x4300, 0x2e00 + 0x300, 0x40), (0x4C00, 0x2e00 + 0xC00, 0x200),
              (0x4E00, 0x2e00 + 0xE00, 0x1C0), (0x5000, 0x2e00 + 0x1000, 0x200),
              (0x5200, 0x2e00 + 0x1200, 0x1C0), (0x5400, 0x2e00 + 0x1400, 0x3C0),
              (0x5800, 0x2e00 + 0x1800, 0x5C0), (0x5E00, 0x2e00 + 0x1E00, 0x4C0),
              (0x6600, 0x2e00 + 0x2600, 0x400)]
trouves = []
for va, raw, taille in ZONES_CODE:
    for insn in md.disasm(bytes(base[raw:raw + taille]), va):
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_MEM and \
                    op.mem.base == capstone.x86.X86_REG_RIP:
                c = insn.address + insn.size + op.mem.disp
                if c == 0x3EA0:
                    trouves.append(insn.address)
                if TAMPON_COMPO <= c < FIN_COMPO:
                    erreur(f"xref vers la région libre @{insn.address:#x} "
                           f"(cible 0x{c:x}) — la région n'est PAS libre !")
if sorted(trouves) != sorted(s for s, _, _ in SITES_LEA):
    erreur(f"xref 0x3EA0 : {sorted(hex(t) for t in trouves)} != les 4 sites connus")
print("[gardes] xref exhaustif : exactement 4 références à 0x3EA0 ; "
      "région 0x3100-0x3860 : aucune référence")

# 1c. la région d'accueil est VIDE dans le fichier et hors porte R10
o3100, o3860 = rva2off(TAMPON_COMPO), rva2off(FIN_COMPO)
if any(b != 0 for b in base[o3100:o3860]):
    erreur("région 0x3100-0x3860 : octets non nuls dans le fichier")
entrees, idx_term, table_off = lire_table(base)
for k, (rva, ln, _) in enumerate(entrees):
    if not (rva + ln <= TAMPON_COMPO or FIN_COMPO <= rva):
        erreur(f"R10[{k}] couvre la région d'accueil (0x{rva:x}+0x{ln:x})")
print("[gardes] région d'accueil : 2 144 o de zéros, AUCUNE entrée R10 couvrante")

# 1d. gabarit PUT ancien exact et unique ; --fail ×3 ; génération 15
if bytes(base[rva2off(RVA_GAB_PUT):rva2off(RVA_GAB_PUT) + 67]) != GAB_PUT_15:
    erreur("GABARIT_PUT @0x4AD7 : octets inattendus")
if bytes(base).count(GAB_PUT_15) != 1:
    erreur("GABARIT_PUT ancien : pas unique")
if bytes(base).count(b"--fail") != 3:
    erreur(f"--fail : {bytes(base).count(b'--fail')} occurrences, 3 attendues")
if bytes(base[rva2off(RVA_L00_DERNIER) - 8:rva2off(RVA_L00_DERNIER) + 1]) != b"terrain15":
    erreur("L00 : contexte inattendu")
if bytes(base[rva2off(RVA_S00_DERNIER) - 8:rva2off(RVA_S00_DERNIER) + 1]) != b"terrain15":
    erreur("S00 : contexte inattendu")
for off_b in (OFF_VI_BIN1, OFF_VI_BIN2):
    if struct.unpack_from("<H", base, off_b)[0] != 15:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 15")

# 1e. kit embarqué inchangé + porte 27/27 verte avant patch
demo9 = DEMO9.read_bytes()
if hashlib.md5(demo9).hexdigest() != MD5_DEMO9:
    erreur("demo/demo.exe : md5 inattendu")
if bytes(base[0x6410:0x6410 + 0x4000]) != demo9:
    erreur("la démo embarquée n'est plus demo.9")
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(bytes(base), rva, ln) != sm:
        erreur(f"terrain.15 : R10[{k}] ROUGE avant patch")
print("[gardes] terrain.15 intègre : porte 27/27, kit demo.9, génération 15")


def couvreurs(rva_z, ln_z):
    return {k for k, (rva, ln, sm) in enumerate(entrees)
            if not (rva + ln <= rva_z or rva_z + ln_z <= rva)}


# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# P1 : les quatre déplacements — la composition déménage à 0x3100
for rva, _, _ in SITES_LEA:
    nouveau = TAMPON_COMPO - (rva + 7)
    struct.pack_into("<i", img, rva2off(rva) + 3, nouveau)
print(f"[patch] P1 : 4 lea repointés 0x3EA0 -> 0x{TAMPON_COMPO:x} "
      f"(sup-35/sup-36/sup-37 ×2, 16 octets)")

# P2 : GABARIT_PUT — guillemets + -m 120 (chemins avec espaces)
img[rva2off(RVA_GAB_PUT):rva2off(RVA_GAB_PUT) + 67] = GAB_PUT_16
print("[patch] P2 : GABARIT_PUT quoté --data-binary @\"…\" + -m 120 (67 o)")

# P3 : génération terrain15 -> terrain16
img[rva2off(RVA_L00_DERNIER)] = ord("6")
img[rva2off(RVA_S00_DERNIER)] = ord("6")
struct.pack_into("<H", img, OFF_VI_BIN1, 16)
struct.pack_into("<H", img, OFF_VI_BIN2, 16)
img[OFF_VI_FV:OFF_VI_FV + 2] = "6".encode("utf-16-le")
img[OFF_VI_PV:OFF_VI_PV + 2] = "6".encode("utf-16-le")
print("[patch] P3 : génération terrain16")

# P4 : sommes R10 recalculées pour toute entrée touchée
ZONES_TOUCHEES = [(rva, 7, f"lea@{rva:#x}") for rva, _, _ in SITES_LEA]
ZONES_TOUCHEES.append((RVA_GAB_PUT, 67, "GABARIT_PUT"))
ZONES_TOUCHEES.append((RVA_S00_DERNIER, 1, "S00"))
touchés = set()
for zr, zl, _ in ZONES_TOUCHEES:
    touchés |= couvreurs(zr, zl)
for k in sorted(touchés):
    rva, ln, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(bytes(img), rva, ln))
print(f"[patch] P4 : {len(touchés)} sommes R10 recalculées : R10{sorted(touchés)}")

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
autorisations = [(rva2off(rva), rva2off(rva) + 7, f"lea@{rva:#x}")
                 for rva, _, _ in SITES_LEA]
autorisations.append((rva2off(RVA_GAB_PUT), rva2off(RVA_GAB_PUT) + 67, "gabarit PUT"))
autorisations.append((rva2off(RVA_L00_DERNIER), rva2off(RVA_L00_DERNIER) + 1, "L00"))
autorisations.append((rva2off(RVA_S00_DERNIER), rva2off(RVA_S00_DERNIER) + 1, "S00"))
autorisations += [(OFF_VI_BIN1, OFF_VI_BIN1 + 2, "VI bin1"),
                  (OFF_VI_BIN2, OFF_VI_BIN2 + 2, "VI bin2"),
                  (OFF_VI_FV, OFF_VI_FV + 2, "FileVersion"),
                  (OFF_VI_PV, OFF_VI_PV + 2, "ProductVersion")]
for k in sorted(touchés):
    autorisations.append((table_off + 16 * k + 8, table_off + 16 * k + 16,
                          f"somme R10[{k}]"))
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b, _ in autorisations)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous bornés "
      f"(16 lea + ~13 utiles gabarit + 2 version + 10 VI + sommes R10)")

# 3b. porte ENTIÈRE verte + terminateur intact
entrees_f, idx_term_f, _ = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(bytes(img), rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
print("[porte] R10 : 27/27 entrées VERTES")

# 3c. les 4 lea désassemblés pointent 0x3100 ; 0x3EA0 n'existe plus nulle part
for rva, _, reg in SITES_LEA:
    ins = list(md.disasm(bytes(img[rva2off(rva):rva2off(rva) + 7]), rva))
    if len(ins) != 1 or ins[0].mnemonic != "lea":
        erreur(f"lea @{rva:#x} : désassemblage inattendu")
    # opérande mémoire = [1] pour lea (dest registre en [0])
    mem_ops = [op for op in ins[0].operands
               if op.type == capstone.x86.X86_OP_MEM]
    if len(mem_ops) != 1:
        erreur(f"lea @{rva:#x} : opérande mémoire introuvable")
    cible = rva + ins[0].size + mem_ops[0].mem.disp
    if cible != TAMPON_COMPO:
        erreur(f"lea @{rva:#x} -> 0x{cible:x} != 0x{TAMPON_COMPO:x}")
    print(f"[désasm] lea {reg} @0x{rva:04X} -> 0x{cible:04X}")
for va, raw, taille in ZONES_CODE:
    for insn in md.disasm(bytes(img[raw:raw + taille]), va):
        for op in insn.operands:
            if op.type == capstone.x86.X86_OP_MEM and \
                    op.mem.base == capstone.x86.X86_REG_RIP:
                c = insn.address + insn.size + op.mem.disp
                if c == 0x3EA0:
                    erreur(f"0x3EA0 encore référencé @{insn.address:#x}")

# 3d. gabarit PUT nouveau unique, ancien ABSENT, --fail ×3 intacts
if bytes(img).count(GAB_PUT_16) != 1:
    erreur("GABARIT_PUT nouveau : absent ou multiple")
if GAB_PUT_15 in bytes(img):
    erreur("GABARIT_PUT ancien encore présent")
if bytes(img).count(b"--fail") != 3:
    erreur("--fail : périmètre modifié (T2 ×2 + PUT attendus)")
print("[fix] GABARIT_PUT quoté en place (unique), ancien absent, --fail ×3")

# 3e. version 16
if bytes(img[rva2off(RVA_L00_DERNIER) - 8:rva2off(RVA_L00_DERNIER) + 1]) != b"terrain16":
    erreur("L00 : terrain16 attendu")
if bytes(img[rva2off(RVA_S00_DERNIER) - 8:rva2off(RVA_S00_DERNIER) + 1]) != b"terrain16":
    erreur("S00 : terrain16 attendu")
if img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.16":
    erreur("FileVersion 0.5.16 attendue")
if img[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain16":
    erreur("ProductVersion terrain16 attendue")
print("[version] L00/S00 terrain16, VERSIONINFO 16, 0.5.16, rrain16")

# 3f. capacité de la nouvelle zone : commande session réelle + PUT pire cas
CMD_SESSION_REELLE = 230 + 254          # littéraux + jeton constaté (D70)
CMD_PUT_PIRES = 58 + 304 + 7 + 480      # préfixe + chemin max (BUF_CHEMIN 304) + bourrage + URL max (480)
if TAMPON_COMPO + max(CMD_SESSION_REELLE, CMD_PUT_PIRES) > FIN_COMPO:
    erreur("capacité TAMPON_COMPO insuffisante pour les pires cas")
print(f"[capacité] 0x{TAMPON_COMPO:x}-0x{FIN_COMPO:x} = "
      f"{FIN_COMPO - TAMPON_COMPO} o >= session {CMD_SESSION_REELLE} o, "
      f"PUT pire cas {CMD_PUT_PIRES} o")

# 3g. écriture + empreintes
DST.write_bytes(bytes(img))
print(f"\n[écrit] {DST}")
print(f"  taille  {len(img)} octets")
print(f"  md5     {hashlib.md5(bytes(img)).hexdigest()}")
print(f"  sha256  {hashlib.sha256(bytes(img)).hexdigest()}")
