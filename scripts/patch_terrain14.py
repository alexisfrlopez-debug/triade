#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.14 — LA PREUVE SURVIT + LE CODE DE SORTIE ENFIN JOURNALISÉ (D68).

LE CONSTAT (capture 23:47 + run 23:07 + D66) : le développeur a exécuté la
commande fallback du LISEZMOI-terrain13 :

    curl.exe -v --max-time 30 -o terrain_jeton_reseau.txt
             --data @terrain_req.txt https://oauth2.googleapis.com/token

et curl a répondu « Failed to open terrain_req.txt ». SON INSTINCT EST
JUSTE : le fichier est absent. La cause est DE NOTRE côté (3e pièce
impossible promise en deux itérations) : le bloc sup-35 nettoie LUI-MÊME
ses 5 fichiers temporaires sur TOUT chemin de sortie (Q9 : DeleteFileA de
terrain_req.txt, terrain_jeton.json, terrain_meta.json, terrain_session.txt,
terrain_rep.json) — le superviseur supprime donc la pièce AVANT que
l'opérateur puisse la produire. La commande fallback était INAPPLICABLE.

Deux conséquences :
  1. curl lit --data AVANT toute connexion : l'échec observé ne dit RIEN
     du réseau (le bac a pourtant prouvé D66 que jeton+chaîne marchent) ;
  2. terrain_jeton.json — même écrit par terrain.13 (sans --fail) — était
     supprimé au même instant : son absence après le run 23:07 ne prouve
     PAS que curl n'a pas reçu de réponse.

LE CORRECTIF (borné, vérifié, porte R10 recalculée) :
  P1. .nettoyage : 5 fichiers -> 4 (mov r13d, 5 -> 4) ;
  P2. bloc de noms réordonné [req][meta][session][rep][jeton] : la marche
      de nettoyage supprime req/meta/session/rep et LAISSE SURVIVRE
      terrain_jeton.json — la réponse de Google (même refusée) restera sur
      disque après le run ; terrain_req.txt (SECRETS) reste supprimé en
      PREMIER ; les 3 lea (lecture jeton @0x5efc, écriture meta @0x5f83,
      lecture session @0x5ff8) sont repointées (disp32, longueurs stables) ;
  P3. le gestionnaire .jeton_ko (0x6113) devient un saut vers un relais de
      32 o posé dans le padding du slot (0x628a, 54 o de NOP) :
        lea rcx, [rip+0x19]        ; "S33 T3 jeton KO code=" (21 o)
        mov edx, 0x15              ; longueur texte (mode 1 = + nombre)
        mov r8b, 1                 ; MODE 1 (sup-11 : texte + itoa(r9d))
        mov r9d, [rip-0x2750]      ; code de sortie curl @0x3b50
        call 0x5000                ; journal
        jmp 0x615c                 ; suite inchangée (.ko S36)
      -> la ligne S33 dit ENFIN LA CLASSE d'échec : code=0 (curl a réussi,
      la réponse de Google est dans terrain_jeton.json survivant),
      code=6/7 (DNS/connexion), code=35/56 (TLS), code=26 (fichier)…
      Même schéma que S13 « termine code=3221225477 » (sup-33, r8d=1) ;
  P4. génération terrain13 -> terrain14 (L00/S00, VERSIONINFO 0.5.14.0,
      FileVersion « 0.5.14 », ProductVersion « …terrain14 ») ;
  P5. sommes R10 recalculées pour TOUTE entrée couvrant un octet touché.

INTOUCHÉS PAR DESIGN : les 4 branches vers 0x6113 (octets identiques),
les autres gestionnaires (.session_ko/.jetons_absents/.ko/.envoi_ko), la
chaîne S33 originale (donnée morte mais byte-identique), T2 ×2 + PUT
(--fail verdict-critiques), le kit, la démo 73c064fb, le proxy dd12b649,
l'annexe jetons, l'en-tête kit, le correctif sup-34 de terrain.10.

Nota : classe 1 (spawn impossible) → [0x3b50] encore à 0 (BSS vierge) →
« code=0 » — ambiguïté documentée, cas jugé quasi impossible (T2 spawn
curl.exe deux fois avec succès à chaque run).
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain13.exe"
DST = REPO / "terrain/livraison/superviseur-terrain14.exe"
DEMO9 = REPO / "demo/demo.exe"

MD5_TERRAIN13 = "8d1938b179d0dd8779fb8b2a82b17921"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"
MD5_DEMO9_B = MD5_DEMO9.encode()

R10_TABLE_RVA = 0x2450
OFF_DEMO = 0x6410            # offset fichier de BLOB_DEMO (rva 0x8010)
TAILLE_DEMO = 0x4000
OFF_MD5_DEMO = 0x585F        # chaîne md5 S04C
OFF_ENETE_KIT = (0x6400, 0x6410)
OFF_PROXY = 0xA410
OFF_ANNEXE = 0xF010

# ---------------------------------------------------------------- zones rva
RVA_L00_DERNIER = 0x2ADA     # dernier caractère de « terrain13 » dans L00
RVA_S00_DERNIER = 0x4366     # idem S00
RVA_HANDLER = 0x6113         # .jeton_ko (25 octets)
RVA_PADDING = 0x628A         # 54 NOP jusqu'à 0x62BF (fin de slot 0x62C0)
RVA_R13D_IMM = 0x617F        # octet d'immédiat de « mov r13d, 5 » @0x617D
RVA_NOMS = 0x6313            # bloc de noms, 90 octets -> 0x636D
RVA_LEA_JETON = 0x5EFC       # lecture terrain_jeton.json (disp @+3)
RVA_LEA_META = 0x5F83        # écriture terrain_meta.json
RVA_LEA_SESSION = 0x5FF8     # lecture terrain_session.txt
RVA_CODE_SORTIE = 0x3B50     # dword code de sortie curl (BSS au-delà du raw)

# ------------------------------------------------------------- octets vieux
VIEUX_HANDLER = bytes.fromhex(
    "488d0df4e5ffff"    # lea rcx, [rip-0x1a0c]  -> "S33 T3 jeton OAuth ECHEC"
    "ba18000000"        # mov edx, 0x18
    "4531c0"            # xor r8d, r8d
    "4531c9"            # xor r9d, r9d
    "e8d6eeffff"        # call 0x5000
    "eb30"              # jmp 0x615c
)
assert len(VIEUX_HANDLER) == 25
VIEUX_R13D = bytes.fromhex("41bd05000000")          # mov r13d, 5
VIEUX_LEA_JETON = bytes.fromhex("488d0d20040000")   # lea rcx,[rip+0x420] -> 0x6323
VIEUX_LEA_META = bytes.fromhex("488d0dac030000")    # lea rcx,[rip+0x3ac] -> 0x6336
VIEUX_LEA_SESSION = bytes.fromhex("488d0d49030000") # lea rcx,[rip+0x349] -> 0x6348
VIEUX_BRANCHES = {0x5EBB: "0f8452020000", 0x5EF6: "0f8517020000",
                  0x5F16: "0f84f7010000", 0x5F58: "0f84b5010000"}
NOMS_VIEUX = (b"terrain_req.txt\x00" + b"terrain_jeton.json\x00"
              + b"terrain_meta.json\x00" + b"terrain_session.txt\x00"
              + b"terrain_rep.json\x00")
assert len(NOMS_VIEUX) == 90

# ------------------------------------------------------------- octets nouveaux
NOMS_NOUVEAUX = (b"terrain_req.txt\x00" + b"terrain_meta.json\x00"
                 + b"terrain_session.txt\x00" + b"terrain_rep.json\x00"
                 + b"terrain_jeton.json\x00")
assert len(NOMS_NOUVEAUX) == 90
# nouvelles cibles : req@0x6313 meta@0x6323 session@0x6335 rep@0x6349
# jeton@0x635A (fin 0x636D inchangée)
DISP_JETON = 0x635A - (RVA_LEA_JETON + 7)      # 0x457
DISP_META = 0x6323 - (RVA_LEA_META + 7)        # 0x399
DISP_SESSION = 0x6335 - (RVA_LEA_SESSION + 7)  # 0x336

CHAINE_S33 = b"S33 T3 jeton KO code=\x00"      # 21 caractères + NUL
assert len(CHAINE_S33) == 22
NOUVEAU_HANDLER = bytes.fromhex("e972010000") + b"\x90" * 20
assert len(NOUVEAU_HANDLER) == 25              # jmp 0x628A + NOP
# relais @0x628A : lea rcx,[rip+0x19]->0x62AA ; mov edx,0x15 ; mov r8b,1 ;
# mov r9d,[rip-0x2750]->0x3B50 ; call 0x5000 ; jmp 0x615C ; chaîne @0x62AA
RELAIS = (bytes.fromhex("488d0d19000000")     # lea rcx, [rip+0x19]
          + bytes.fromhex("ba15000000")       # mov edx, 0x15
          + bytes.fromhex("41b001")           # mov r8b, 1
          + bytes.fromhex("448b0db0d8ffff")   # mov r9d, [rip-0x2750]
          + bytes.fromhex("e85bedffff")       # call 0x5000
          + bytes.fromhex("e9b2feffff")       # jmp 0x615c
          + CHAINE_S33)
assert len(RELAIS) == 54, len(RELAIS)
# auto-cohérence des disp du relais
assert 0x6291 + 0x19 == 0x62AA            # lea -> chaîne
assert 0x62A0 - 0x2750 == RVA_CODE_SORTIE  # mov r9d -> code de sortie
assert 0x62A5 - 0x12A5 == 0x5000           # call -> journal
assert 0x62AA - 0x14E == 0x615C            # jmp -> .ko (S36 KO)
assert 0x6118 + 0x172 == 0x628A            # jmp handler -> relais

# gabarits T3 tels que posés par terrain.13 (--fail retiré, espaces)
GAB_JETON_13 = (b"curl.exe -s" + b" " * 8 +
                b"--max-time 30 -o terrain_jeton.json "
                b"--data @terrain_req.txt \x08\x00")
GAB_SESSION_13 = (b"curl.exe -s" + b" " * 8 +
                  b"--max-time 30 -o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
MOT_T2_HTTP = b"-s --fail --max-time 20 -o terrain_page_http.txt"
MOT_T2_HTTPS = b"-s --fail --max-time 20 -o terrain_page_https.txt"
MOT_PUT = b"-s --fail --max-time 120 -o NUL -X PUT"

# zones rva touchées (rva, LONGUEUR) — pour couvreurs R10
ZONES_RVA = [(RVA_HANDLER, 25),
             (RVA_PADDING, 54),
             (0x617D, 6),
             (RVA_NOMS, 90),
             (RVA_LEA_JETON, 7),
             (RVA_LEA_META, 7),
             (RVA_LEA_SESSION, 7),
             (RVA_S00_DERNIER, 1),
             (0x2ADA, 1)]


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


def unique(data, motif):
    hits = [m.start() for m in range(len(data)) if False]  # placeholder
    import re
    hits = [m.start() for m in re.finditer(re.escape(motif), data)]
    if len(hits) != 1:
        raise ValueError(f"{len(hits)} occurrences de {motif[:40]!r}…")
    return hits[0]


def erreur(msg):
    print(f"ECHEC : {msg}")
    sys.exit(1)


def cible_rip(rva_instr, lon, disp):
    return rva_instr + lon + disp


def scan_xref_noms(data):
    """Cherche TOUTE référence rip-relative dont la cible tombe dans le
    bloc de noms [0x6313, 0x636D) : lea/mov REX.W (7 o) et mov r32/cmp
    (6 o). Retourne {site_rva: cible_rva}."""
    trouves = {}
    bornes = (0x6313, 0x636D)
    # zones de code possibles : .text (rva 0x1000..0x2000) et .text2
    for rva0, rva1, off0 in ((0x1000, 0x2000, 0x400), (0x4000, 0x6E00, 0x2E00)):
        blob = data[off0:off0 + (rva1 - rva0)]
        for i in range(len(blob) - 7):
            b0 = blob[i]
            # lea r64 / mov r64, [rip+disp32] : REX.W(48/4C/44/4D) 8D/8B modrm(mod=00,rm=101)
            if b0 in (0x48, 0x4C, 0x44, 0x4D) and blob[i + 1] in (0x8D, 0x8B) \
               and (blob[i + 2] & 0xC7) == 0x05:
                disp = struct.unpack_from("<i", blob, i + 3)[0]
                cible = cible_rip(rva0 + i, 7, disp)
                if bornes[0] <= cible < bornes[1]:
                    trouves[rva0 + i] = cible
                continue
            # mov r32, [rip+disp32] / cmp dword [rip+disp32] : 8B/83 3D
            if b0 in (0x8B, 0x83) and blob[i + 1] in (0x05, 0x0D, 0x15, 0x1D,
                                                       0x25, 0x2D, 0x35, 0x3D):
                if (blob[i + 1] & 0xC7) == 0x05:
                    disp = struct.unpack_from("<i", blob, i + 2)[0]
                    cible = cible_rip(rva0 + i, 6, disp)
                    if bornes[0] <= cible < bornes[1]:
                        trouves[rva0 + i] = cible
    return trouves


XREF_ATTENDUS = {0x5E70: 0x6313,   # écriture terrain_req.txt
                 0x5EFC: 0x6323,   # lecture terrain_jeton.json
                 0x5F83: 0x6336,   # écriture terrain_meta.json
                 0x5FF8: 0x6348,   # lecture terrain_session.txt
                 0x6176: 0x6313}   # marche de nettoyage (départ)


# =============================================================================
# 1. GARDES-FOUS
# =============================================================================
base = bytearray(SRC.read_bytes())
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN13:
    erreur("terrain.13 : md5 inattendu (source altérée ?)")

off = lambda r: rva2off(r)  # noqa: E731

# 1a. octets anciens exacts aux sites touchés
if bytes(base[off(RVA_HANDLER):off(RVA_HANDLER) + 25]) != VIEUX_HANDLER:
    erreur(".jeton_ko @0x6113 : octets inattendus")
if bytes(base[off(RVA_PADDING):off(RVA_PADDING) + 54]) != b"\x90" * 54:
    erreur("padding @0x628A : 54 NOP attendus")
if bytes(base[off(0x617D):off(0x617D) + 6]) != VIEUX_R13D:
    erreur("mov r13d, 5 @0x617D : octets inattendus")
for site, hexs in VIEUX_BRANCHES.items():
    if bytes(base[off(site):off(site) + 6]) != bytes.fromhex(hexs):
        erreur(f"branche @{site:#x} : octets inattendus (doit viser 0x6113)")
if bytes(base[off(RVA_LEA_JETON):off(RVA_LEA_JETON) + 7]) != VIEUX_LEA_JETON:
    erreur("lea jeton @0x5EFC : octets inattendus")
if bytes(base[off(RVA_LEA_META):off(RVA_LEA_META) + 7]) != VIEUX_LEA_META:
    erreur("lea meta @0x5F83 : octets inattendus")
if bytes(base[off(RVA_LEA_SESSION):off(RVA_LEA_SESSION) + 7]) != VIEUX_LEA_SESSION:
    erreur("lea session @0x5FF8 : octets inattendus")
if bytes(base[off(RVA_NOMS):off(RVA_NOMS) + 90]) != NOMS_VIEUX:
    erreur("bloc de noms @0x6313 : contenu inattendu")

# 1b. le slot code-sortie curl vit dans le BSS .data (zéro au chargement)
if off(RVA_CODE_SORTIE) is not None:
    erreur("0x3B50 devrait être au-delà du raw .data (BSS)")

# 1c. références croisées vers le bloc de noms : ensemble EXACT
xrefs = scan_xref_noms(bytes(base))
if xrefs != XREF_ATTENDUS:
    erreur(f"xref vers le bloc de noms : {sorted(xrefs.items())} != "
           f"attendu {sorted(XREF_ATTENDUS.items())}")

# 1d. gabarits T3 de terrain.13 intacts (--fail déjà retiré)
off_gj = unique(bytes(base), GAB_JETON_13)
off_gs = unique(bytes(base), GAB_SESSION_13)
for mot in (MOT_T2_HTTP, MOT_T2_HTTPS, MOT_PUT):
    unique(bytes(base), mot)
if bytes(base).count(b"--fail") != 3:
    erreur(f"--fail : {bytes(base).count(b'--fail')} occurrences, 3 attendues")

# 1e. blobs + empreintes (identité du kit embarqué)
demo9 = DEMO9.read_bytes()
if hashlib.md5(demo9).hexdigest() != MD5_DEMO9:
    erreur("demo/demo.exe : md5 inattendu")
if bytes(base[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo9:
    erreur("la démo embarquée n'est plus demo.9")
if bytes(base[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO9_B:
    erreur("chaîne md5 S04C : demo.9 introuvable")

# 1f. génération courante = 13 / terrain.13
OFF_L00 = off(RVA_L00_DERNIER)
OFF_S00 = off(RVA_S00_DERNIER)
if bytes(base[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain13" or base[OFF_L00 + 1:OFF_L00 + 4] != b"L01":
    erreur("L00 : contexte inattendu")
if bytes(base[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain13" or base[OFF_S00 + 1:OFF_S00 + 4] != b"S01":
    erreur("S00 : contexte inattendu")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", base, off_b)[0] != 13:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 13")
if base[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.13":
    erreur("FileVersion inattendue")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain13":
    erreur("ProductVersion (fin) inattendue")

# 1g. correctif ABI terrain.10 en place + étiquettes de verdict T3
if bytes(base[off(0x5D1E):off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("sup-34 .curl : correctif D62 absent")
for s in (b'"access_token":"', b"S33 T3 jeton OAuth ECHEC",
          b"S36 T3 VERDICT KO"):
    unique(bytes(base), s)
if b"https://oauth2.googleapis.com/token" not in bytes(base):
    erreur("URL token OAuth absente")

# 1h. porte : 27 entrées vertes avant patch
entrees, idx_term, table_off = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(bytes(base), rva, ln) != sm:
        erreur(f"terrain.13 : R10[{k}] ROUGE avant patch")

print("[gardes] terrain.13 intègre : handler/padding/leas/noms/branches "
      "exacts, xref = 5 sites attendus, blobs + version + porte 27/27")


def couvreurs(rva_z, ln_z):
    return {k for k, (rva, ln, sm) in enumerate(entrees)
            if not (rva + ln <= rva_z or rva_z + ln_z <= rva)}


for lab, (zr, zl) in {"handler": (RVA_HANDLER, 25), "relais": (RVA_PADDING, 54),
                      "r13d": (0x617D, 6), "noms": (RVA_NOMS, 90),
                      "lea jeton": (RVA_LEA_JETON, 7),
                      "lea meta": (RVA_LEA_META, 7),
                      "lea session": (RVA_LEA_SESSION, 7),
                      "S00": (RVA_S00_DERNIER, 1)}.items():
    cov = couvreurs(zr, zl)
    if not cov:
        erreur(f"{lab} : AUCUN couvreur R10 (zone non protégée ?)")
    print(f"[couv] {lab:<12} couvert par R10{sorted(cov)}")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# P1 : nettoyage 5 -> 4 fichiers
img[off(RVA_R13D_IMM)] = 0x04

# P2 : bloc de noms réordonné + 3 lea repointées
img[off(RVA_NOMS):off(RVA_NOMS) + 90] = NOMS_NOUVEAUX
struct.pack_into("<i", img, off(RVA_LEA_JETON) + 3, DISP_JETON)
struct.pack_into("<i", img, off(RVA_LEA_META) + 3, DISP_META)
struct.pack_into("<i", img, off(RVA_LEA_SESSION) + 3, DISP_SESSION)

# P3 : gestionnaire -> jmp relais ; relais + chaîne dans le padding
img[off(RVA_HANDLER):off(RVA_HANDLER) + 25] = NOUVEAU_HANDLER
img[off(RVA_PADDING):off(RVA_PADDING) + 54] = RELAIS

# P4 : génération terrain13 -> terrain14
img[OFF_L00] = ord("4")
img[OFF_S00] = ord("4")
struct.pack_into("<H", img, 0x5CD4, 14)
struct.pack_into("<H", img, 0x5CDC, 14)
img[0x5DC2:0x5DC4] = "4".encode("utf-16-le")
img[0x5ECC:0x5ECE] = "4".encode("utf-16-le")

# P5 : sommes R10 recalculées pour toute entrée touchée
touchés = set()
for (zr, zl) in ZONES_RVA:
    touchés |= couvreurs(zr, zl)
for k in sorted(touchés):
    rva, ln, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(bytes(img), rva, ln))
print(f"[patch] {len(touchés)} sommes R10 recalculées : "
      f"R10{sorted(touchés)}")

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
# 3a. diff borné
autorisations = [(off(RVA_HANDLER), off(RVA_HANDLER) + 25, "handler"),
                 (off(RVA_PADDING), off(RVA_PADDING) + 54, "relais"),
                 (off(0x617D), off(0x617D) + 6, "mov r13d (1 octet utile)"),
                 (off(RVA_NOMS), off(RVA_NOMS) + 90, "bloc de noms"),
                 (off(RVA_LEA_JETON), off(RVA_LEA_JETON) + 7, "lea jeton"),
                 (off(RVA_LEA_META), off(RVA_LEA_META) + 7, "lea meta"),
                 (off(RVA_LEA_SESSION), off(RVA_LEA_SESSION) + 7, "lea session"),
                 (OFF_L00, OFF_L00 + 1, "L00"), (OFF_S00, OFF_S00 + 1, "S00"),
                 (0x5CD4, 0x5CD6, "bin1"), (0x5CDC, 0x5CDE, "bin2"),
                 (0x5DC2, 0x5DC4, "FV"), (0x5ECC, 0x5ECE, "PV")]
for k in sorted(touchés):
    autorisations.append((table_off + 16 * k + 8, table_off + 16 * k + 16,
                          f"somme R10[{k}]"))
diffs = [i for i in range(len(base)) if base[i] != img[i]]
hors = [i for i in diffs if not any(a <= i < b for a, b, _ in autorisations)]
if hors:
    erreur(f"{len(hors)} octets hors zones autorisées : {[hex(i) for i in hors[:8]]}")
print(f"[diff] {len(diffs)} octets modifiés, tous bornés")

# 3b. porte ENTIÈRE verte
entrees_f, idx_term_f, _ = lire_table(img)
if idx_term_f != 27:
    erreur(f"table finale : {idx_term_f} entrées")
for k, (rva, ln, sm) in enumerate(entrees_f):
    if somme_zone(bytes(img), rva, ln) != sm:
        erreur(f"porte R10 ROUGE après patch à l'entrée [{k}]")
if struct.unpack_from("<IIQ", img, table_off + 16 * 27) != (0, 0, 0):
    erreur("le terminateur a bougé")
print("[porte] R10 : 27/27 entrées VERTES + terminateur intact")

# 3c. désassemblage du chemin patché (capstone)
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)


def desasm(rva, n):
    o = off(rva)
    return list(md.disasm(bytes(img[o:o + n]), rva))


# handler : jmp unique vers le relais
ins = desasm(RVA_HANDLER, 5)
if not (len(ins) == 1 and ins[0].mnemonic == "jmp"
        and ins[0].op_str == "0x628a"):
    erreur(f"handler : {[f'{i.mnemonic} {i.op_str}' for i in ins]} != jmp 0x628a")

# relais : les 6 instructions attendues puis la chaîne
ins = desasm(RVA_PADDING, 32)
attendu = ["lea rcx, [rip + 0x19]", "mov edx, 0x15", "mov r8b, 1",
           "mov r9d, dword ptr [rip - 0x2750]", "call 0x5000",
           "jmp 0x615c"]
obtenu = [f"{i.mnemonic} {i.op_str}" for i in ins]
if obtenu != attendu:
    erreur(f"relais : {obtenu} != {attendu}")
if bytes(img[off(0x62AA):off(0x62AA) + 22]) != CHAINE_S33:
    erreur("chaîne S33 @0x62AA inattendue")

# nettoyage : 4 fichiers
ins = desasm(0x6176, 14)
txt = " ; ".join(f"{i.mnemonic} {i.op_str}" for i in ins)
if "mov r13d, 4" not in txt:
    erreur(f"nettoyage : « mov r13d, 4 » introuvable ({txt})")

# leas repointées
for site, cible, lab in ((RVA_LEA_JETON, 0x635A, "jeton"),
                         (RVA_LEA_META, 0x6323, "meta"),
                         (RVA_LEA_SESSION, 0x6335, "session")):
    ins = desasm(site, 7)
    if not (len(ins) == 1 and ins[0].mnemonic == "lea"
            and "[rip" in ins[0].op_str):
        erreur(f"lea {lab} : désassemblage inattendu")
    # capstone op_str ne donne pas la cible : recalcul brut
    disp = struct.unpack_from("<i", img, off(site) + 3)[0]
    if site + 7 + disp != cible:
        erreur(f"lea {lab} : cible {hex(site + 7 + disp)} != {hex(cible)}")

# bloc de noms final
noms_f = []
cur = RVA_NOMS
for _ in range(5):
    o = off(cur)
    fin = img.index(b"\x00", o)
    noms_f.append((cur, bytes(img[o:fin]).decode()))
    cur += (fin - o) + 1
if [n for _, n in noms_f] != ["terrain_req.txt", "terrain_meta.json",
                              "terrain_session.txt", "terrain_rep.json",
                              "terrain_jeton.json"]:
    erreur(f"bloc de noms final : {noms_f}")
if cur != 0x636D:
    erreur(f"fin de bloc {hex(cur)} != 0x636D")

# 3d. xref après patch : mêmes sites, cibles réordonnées
xrefs_f = scan_xref_noms(bytes(img))
XREF_ATTENDUS_F = dict(XREF_ATTENDUS)
XREF_ATTENDUS_F[0x5EFC] = 0x635A
XREF_ATTENDUS_F[0x5F83] = 0x6323
XREF_ATTENDUS_F[0x5FF8] = 0x6335
if xrefs_f != XREF_ATTENDUS_F:
    erreur(f"xref final : {sorted(xrefs_f.items())} != "
           f"{sorted(XREF_ATTENDUS_F.items())}")

# 3e. le reste du binaire : octet pour octet identique
if img[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]] != base[OFF_ENETE_KIT[0]:OFF_ENETE_KIT[1]]:
    erreur("l'en-tête kit (longueurs) a bougé")
if img[OFF_PROXY:OFF_ANNEXE] != base[OFF_PROXY:OFF_ANNEXE]:
    erreur("le proxy embarqué a bougé")
if img[OFF_ANNEXE:] != base[OFF_ANNEXE:]:
    erreur("l'annexe jetons a bougé")
if bytes(img[OFF_DEMO:OFF_DEMO + TAILLE_DEMO]) != demo9:
    erreur("la démo embarquée != demo.9")
if bytes(img[OFF_MD5_DEMO:OFF_MD5_DEMO + 32]) != MD5_DEMO9_B:
    erreur("chaîne md5 S04C modifiée")
if bytes(img[off(0x5D1E):off(0x5D1E) + 4]) != bytes.fromhex("4883ec28"):
    erreur("correctif sup-34 altéré")
if bytes(img[off_gj:off_gj + 81]) != GAB_JETON_13:
    erreur("GABARIT_JETON altéré")
if bytes(img[off_gs:off_gs + 232]) != GAB_SESSION_13:
    erreur("GABARIT_SESSION altéré")
if bytes(img).count(b"--fail") != 3:
    erreur("--fail finaux != 3 (T2×2 + PUT)")
for site, hexs in VIEUX_BRANCHES.items():
    if bytes(img[off(site):off(site) + 6]) != bytes.fromhex(hexs):
        erreur(f"branche @{site:#x} a bougé (doit rester vers 0x6113)")
if bytes(img[off(0x612C):off(0x612C) + 25]) != bytes(base[off(0x612C):off(0x612C) + 25]):
    erreur(".session_ko a bougé")
print("[blob] kit/démo 73c064fb/proxy dd12b649/annexe/gabarits/branches/"
      ".session_ko/S04C : inchangés octet pour octet")

# 3f. identité
if bytes(img[OFF_L00 - 8:OFF_L00 + 1]) != b"terrain14" or bytes(img[OFF_S00 - 8:OFF_S00 + 1]) != b"terrain14":
    erreur("versions L00/S00 finales inattendues")
for off_b in (0x5CD4, 0x5CDC):
    if struct.unpack_from("<H", img, off_b)[0] != 14:
        erreur(f"VERSIONINFO finale @{off_b:#x} != 14")
if img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.14":
    erreur("FileVersion finale inattendue")
if img[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain14":
    erreur("ProductVersion (fin) inattendue")
print("[ident] L00/S00 « terrain14 », VERSIONINFO 0.5.14.0, "
      "FileVersion « 0.5.14 », ProductVersion « …terrain14 »")

# 3g. prologue du proxy embarqué inchangé (probing D63)
off_pro = OFF_PROXY + 0x2C00 + (0x5580 - 0x4000)
code = bytes(img[off_pro:off_pro + 0x40])
obtenu_pro = [f"{i.mnemonic} {i.op_str}".rstrip() for i in
              md.disasm(code, 0x140005580)]
attendu_pro = ["push rbx", "push r12", "push r13", "push r14", "push r15",
               "mov r10, 0xfffffffffffff000",
               "mov rax, qword ptr [rsp + r10]",
               "sub r10, 0x1000",
               "cmp r10, -0x7000",
               "jge 0x140005590",
               "mov rax, qword ptr [rsp - 0x7100]",
               "sub rsp, 0x7100"]
if obtenu_pro[:12] != attendu_pro:
    erreur("prologue http-10 embarqué inattendu")
print("[code] prologue http-10 embarqué intact : BOUCLE DE PROBING")

# 3h. empreintes + écriture
final = hashlib.md5(bytes(img)).hexdigest()
sha = hashlib.sha256(bytes(img)).hexdigest()
DST.write_bytes(bytes(img))
print(f"\n[patch] {DST} écrit ({len(img)} octets)")
print(f"  md5    {final}")
print(f"  sha256 {sha}")
