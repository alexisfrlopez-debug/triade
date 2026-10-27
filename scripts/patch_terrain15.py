#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""terrain.15 — L'ESPACE MANQUANT + HTTP/1.1 POUR LA SESSION (D69).

LE CONSTAT (run terrain.14, 00:20:20, pièce terrain_jeton.json ENFIN déposée —
elle survit désormais) : S33 dit « jeton KO code=0 » — curl a RÉUSSI, Google a
RÉPONDU, et la réponse est un SUCCÈS (jeton d'accès vivant, testé depuis le
bac : HTTP 200 sur about, utilisateur du projet). Le réseau, les identifiants,
le dossier, la chaîne : TOUT est bon. La panne est la nôtre, dans sup-35 :

  Q4 cherche l'étiquette "access_token":"  (format COMPACT, sans espace)
  or Google répond en JSON INDENTÉ       : "access_token": "ya29…"
  — UN ESPACE. sup-22 (memcmp glissant) ne trouve pas l'étiquette, rend
  rax=0, S33 déclare ÉCHEC. La faute remonte à la fixture oracle
  (REPONSE_OAUTH compacte, idéalisée) qui n'a jamais rencontré le format réel.

PREUVES (D69, toutes live) :
  - le json déposé (416 o, LF, indent 2) = octet pour octet le format d'un
    rafraîchissement frais depuis le bac (même taille, même ordre de champs) ;
  - datation par compte à rebours refresh_token_expires_in : le jeton déposé
    a été émis à 23:21:01 UTC = PENDANT le run — c'est bien la réponse du run ;
  - régression documentée : l'ancienne étiquette est ABSENTE du json réel.

SECONDE MINE DÉSAMORCÉE (sonde bac, h2 vs h1) : en HTTP/2 (défaut des curl
modernes, dont curl.exe de Windows), curl -D écrit les en-têtes EN MINUSCULES
(location:) — l'étiquette « Location: » raterait à son tour. En HTTP/1.1
forcée, Google répond « Location: » (casse classique), ligne à l'octet ~194
d'un dump de ~846 o — DANS la limite de lecture de 600 o. La chaîne complète
avec les commandes composées terrain.15 a été exécutée EN LIVE contre le vrai
Google (jeton → session h1 → PUT → fichier témoin apparu dans le dossier test,
puis retiré) : les trois exit=0.

LE CORRECTIF (borné, porte R10 recalculée) :
  P1. ETIQ_TOKEN @rva 0x4894 (16 o, contiguë aux autres étiquettes —
      allonger impossible) : "access_token":"  →  access_token": "
      (guillemet ouvrant retiré, espace inséré : MÊME LONGUEUR 16, donc
      l'immédiat r9d=0x10 du site d'appel @0x5f2d reste exact ; l'étiquette
      se termine toujours sur le guillemet OUVRANT de la valeur, la
      sémantique sup-22 est inchangée).
  P2. GABARIT_SESSION @rva 0x49EF (232 o) : --max-time 30  →  --http1.1 -m 30
      (même longueur grâce aux 8 espaces libres laissés par le retrait de
      --fail en terrain.13 ; le reste est inchangé octet par octet après
      l'octet 32). La session est forcée en HTTP/1.1 → l'étiquette
      « Location: » (casse classique, preuve h1) matche TOUJOURS, quel que
      soit le curl de la machine.
  P3. génération terrain14 → terrain15 (L00, S00, VERSIONINFO, FileVersion,
      ProductVersion).
  P4. sommes R10 recalculées pour les entrées couvrantes.

INTOUCHÉ : tout le code (un seul octet de .text ne bouge pas — ce correctif
est DONNÉES pur), GABARIT_JETON (la preuve du run terrain.14 s'applique à
l'identique), ETIQ_LOCATION, T2 ×2, PUT, démo, proxy, annexe.
"""

import hashlib
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
SRC = REPO / "terrain/livraison/superviseur-terrain14.exe"
DST = REPO / "terrain/livraison/superviseur-terrain15.exe"
DEMO9 = REPO / "demo/demo.exe"

MD5_TERRAIN14 = "1958cbfb9afb3345c2381c0dc2e135f4"
MD5_DEMO9 = "73c064fbaf4610a167bc6434dee400e4"

R10_TABLE_RVA = 0x2450

# ------------------------------------------------------------------ zones rva
RVA_ETIQ_TOKEN = 0x4894        # 16 o, entre FIX_FINAL_DEMO et ETIQ_LOCATION
RVA_GAB_SESSION = 0x49EF       # 232 o
RVA_L00_DERNIER = 0x2ADA       # dernier caractère de « terrain14 » dans L00
RVA_S00_DERNIER = 0x4366       # idem S00
RVA_SITE_APPEL = 0x5F26        # lea r8, [ETIQ_TOKEN] ; vérifié non touché
# VERSIONINFO : offsets FICHIER (zone .rdata ressources)
OFF_VI_BIN1, OFF_VI_BIN2 = 0x5CD4, 0x5CDC      # mots 16 bits = 14
OFF_VI_FV, OFF_VI_PV = 0x5DC2, 0x5ECC          # « 0.5.14 » / « rrain14 »

# --------------------------------------------------------------- octets vieux
ETIQ_VIEUX = b'"access_token":"'
GAB_SESSION_14 = (b"curl.exe -s" + b" " * 8 +
                  b"--max-time 30 -o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
GAB_JETON_14 = (b"curl.exe -s" + b" " * 8 +
                b"--max-time 30 -o terrain_jeton.json "
                b"--data @terrain_req.txt \x08\x00")
APRES_ETIQ = b"Location: \"id\"https://oa"      # suite immédiate de l'étiquette

# -------------------------------------------------------------- octets nouveaux
ETIQ_NOUVEAU = b'access_token": "'
GAB_SESSION_15 = (b"curl.exe -s --http1.1 -m 30" + b" " * 6 +
                  b"-o NUL -D terrain_session.txt "
                  b"-X POST -H \"Content-Type: application/json\" "
                  b"-H \"Authorization: Bearer \x07\" "
                  b"--data @terrain_meta.json "
                  b"https://www.googleapis.com/upload/drive/v3/files"
                  b"?uploadType=resumable\x00")
assert len(ETIQ_VIEUX) == len(ETIQ_NOUVEAU) == 16
assert len(GAB_SESSION_14) == len(GAB_SESSION_15) == 232
assert GAB_SESSION_15[32:] == GAB_SESSION_14[32:]   # suffixe octet identique
assert GAB_SESSION_15[:27] == b"curl.exe -s --http1.1 -m 30"


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


OFF = {rva: rva2off(rva) for rva in (RVA_ETIQ_TOKEN, RVA_GAB_SESSION,
                                     RVA_L00_DERNIER, RVA_S00_DERNIER)}


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
if hashlib.md5(bytes(base)).hexdigest() != MD5_TERRAIN14:
    erreur("terrain.14 : md5 inattendu (source altérée ?)")

# 1a. étiquette + gabarit anciens, exacts et uniques
if bytes(base[OFF[RVA_ETIQ_TOKEN]:OFF[RVA_ETIQ_TOKEN] + 16]) != ETIQ_VIEUX:
    erreur("ETIQ_TOKEN @0x4894 : octets inattendus")
if bytes(base[OFF[RVA_ETIQ_TOKEN] + 16:
                OFF[RVA_ETIQ_TOKEN] + 16 + len(APRES_ETIQ)]) != APRES_ETIQ:
    erreur("suite du bloc d'étiquettes inattendue (contiguïté perdue ?)")
if bytes(base[OFF[RVA_GAB_SESSION]:OFF[RVA_GAB_SESSION] + 232]) != GAB_SESSION_14:
    erreur("GABARIT_SESSION @0x49EF : octets inattendus")
for nom, motif, n in (("ETIQ_TOKEN", ETIQ_VIEUX, 1),
                      ("GABARIT_SESSION", GAB_SESSION_14, 1),
                      ("GABARIT_JETON", GAB_JETON_14, 1),
                      ("ETIQ_LOCATION", b"Location: ", 1),
                      ("ETIQ_ID", b'"id"', 1)):
    if bytes(base).count(motif) != n:
        erreur(f"{nom} : {bytes(base).count(motif)} occurrences, {n} attendue(s)")
if bytes(base).count(b"--fail") != 3:
    erreur(f"--fail : {bytes(base).count(b'--fail')} occurrences, 3 attendues")

# 1b. site d'appel sup-22 non touché : lea r8 -> 0x4894 + longueur 16 + arrêt "
site = OFF[RVA_SITE_APPEL] if RVA_SITE_APPEL < 0x4000 else rva2off(RVA_SITE_APPEL)
attendu_site = (bytes.fromhex("4c8d05") + struct.pack("<i", RVA_ETIQ_TOKEN - 0x5F2D)
                + bytes.fromhex("41b910000000")
                + bytes.fromhex("c744242022000000"))
if bytes(base[site:site + len(attendu_site)]) != attendu_site:
    erreur("site d'appel @0x5F26 : lea/mov r9d=0x10/arrêt 0x22 inattendus")

# 1c. génération courante = 14
if bytes(base[OFF[RVA_L00_DERNIER] - 8:OFF[RVA_L00_DERNIER] + 1]) != b"terrain14":
    erreur("L00 : contexte inattendu")
if bytes(base[OFF[RVA_S00_DERNIER] - 8:OFF[RVA_S00_DERNIER] + 1]) != b"terrain14":
    erreur("S00 : contexte inattendu")
for off_b in (OFF_VI_BIN1, OFF_VI_BIN2):
    if struct.unpack_from("<H", base, off_b)[0] != 14:
        erreur(f"VERSIONINFO binaire @{off_b:#x} != 14")
if base[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.14":
    erreur("FileVersion inattendue")
if base[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain14":
    erreur("ProductVersion (fin) inattendue")

# 1d. kit embarqué inchangé
demo9 = DEMO9.read_bytes()
if hashlib.md5(demo9).hexdigest() != MD5_DEMO9:
    erreur("demo/demo.exe : md5 inattendu")
if bytes(base[0x6410:0x6410 + 0x4000]) != demo9:
    erreur("la démo embarquée n'est plus demo.9")
if bytes(base[0x585F:0x585F + 32]) != MD5_DEMO9.encode():
    erreur("chaîne md5 S04C : demo.9 introuvable")

# 1e. porte : 27 entrées vertes avant patch
entrees, idx_term, table_off = lire_table(base)
if idx_term != 27:
    erreur(f"table R10 : {idx_term} entrées, 27 attendues")
for k, (rva, ln, sm) in enumerate(entrees):
    if somme_zone(bytes(base), rva, ln) != sm:
        erreur(f"terrain.14 : R10[{k}] ROUGE avant patch")
print("[gardes] terrain.14 intègre : étiquette/gabarits/site d'appel exacts, "
      "version 14, kit demo.9, porte 27/27")


def couvreurs(rva_z, ln_z):
    return {k for k, (rva, ln, sm) in enumerate(entrees)
            if not (rva + ln <= rva_z or rva_z + ln_z <= rva)}


ZONES_RVA = [(RVA_ETIQ_TOKEN, 16, "ETIQ_TOKEN"),
             (RVA_GAB_SESSION, 232, "GABARIT_SESSION"),
             (RVA_L00_DERNIER, 1, "L00"),
             (RVA_S00_DERNIER, 1, "S00")]
for rva_f in (OFF_VI_BIN1, OFF_VI_BIN2, OFF_VI_FV, OFF_VI_PV):
    ZONES_RVA.append((0x7000 + (rva_f - 0x5C00), 2, f"VI@{rva_f:#x}"))
for lab, (zr, zl, _) in [(z[2], z) for z in ZONES_RVA]:
    cov = couvreurs(zr, zl)
    # L00/VERSIONINFO vivent hors de la porte (prouvé par terrain.14 : leur
    # bump n'avait laissé aucune somme rouge) ; les zones de DONNÉES, elles,
    # DOIVENT être couvertes.
    if not cov and lab in ("ETIQ_TOKEN", "GABARIT_SESSION"):
        erreur(f"{lab} : AUCUN couvreur R10 (zone de données non protégée ?)")
    print(f"[couv] {lab:<16} couvert par R10{sorted(cov) if cov else '— (hors porte, comme terrain.14)'}")

# =============================================================================
# 2. LE PATCH
# =============================================================================
img = bytearray(base)

# P1 : l'étiquette — l'espace de Google
img[OFF[RVA_ETIQ_TOKEN]:OFF[RVA_ETIQ_TOKEN] + 16] = ETIQ_NOUVEAU

# P2 : la session — HTTP/1.1 forcée pour la casse « Location: »
img[OFF[RVA_GAB_SESSION]:OFF[RVA_GAB_SESSION] + 232] = GAB_SESSION_15

# P3 : génération terrain14 -> terrain15
img[OFF[RVA_L00_DERNIER]] = ord("5")
img[OFF[RVA_S00_DERNIER]] = ord("5")
struct.pack_into("<H", img, OFF_VI_BIN1, 15)
struct.pack_into("<H", img, OFF_VI_BIN2, 15)
img[OFF_VI_FV:OFF_VI_FV + 2] = "5".encode("utf-16-le")
img[OFF_VI_PV:OFF_VI_PV + 2] = "5".encode("utf-16-le")

# P4 : sommes R10 recalculées pour toute entrée touchée
touchés = set()
for (zr, zl, _) in ZONES_RVA:
    touchés |= couvreurs(zr, zl)
for k in sorted(touchés):
    rva, ln, _ = entrees[k]
    struct.pack_into("<Q", img, table_off + 16 * k + 8,
                     somme_zone(bytes(img), rva, ln))
print(f"[patch] {len(touchés)} sommes R10 recalculées : R10{sorted(touchés)}")

# =============================================================================
# 3. POST-VÉRIFICATIONS
# =============================================================================
autorisations = [(OFF[RVA_ETIQ_TOKEN], OFF[RVA_ETIQ_TOKEN] + 16, "étiquette"),
                 (OFF[RVA_GAB_SESSION], OFF[RVA_GAB_SESSION] + 232, "gabarit session"),
                 (OFF[RVA_L00_DERNIER], OFF[RVA_L00_DERNIER] + 1, "L00"),
                 (OFF[RVA_S00_DERNIER], OFF[RVA_S00_DERNIER] + 1, "S00"),
                 (OFF_VI_BIN1, OFF_VI_BIN1 + 2, "VI bin1"),
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
      f"(étiquette 16 + gabarit ~13 utiles + version 10 + sommes R10)")

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

# 3c. nouvelle étiquette unique, ancienne ABSENTE ; site d'appel INTACT
if bytes(img).count(ETIQ_NOUVEAU) != 1:
    erreur("nouvelle étiquette : pas unique")
if ETIQ_VIEUX in bytes(img):
    erreur("ancienne étiquette encore présente quelque part")
if bytes(img[site:site + len(attendu_site)]) != attendu_site:
    erreur("site d'appel @0x5F26 a bougé (il ne devait pas)")
if bytes(img).count(GAB_SESSION_15) != 1 or ETIQ_NOUVEAU not in bytes(img):
    erreur("gabarit session nouveau : absent ou multiple")
if bytes(img).count(GAB_JETON_14) != 1:
    erreur("GABARIT_JETON a bougé (il ne devait pas)")
print("[fix] étiquette espace en place (unique), ancienne absente, "
      "site d'appel inchangé, GABARIT_JETON intouché")

# 3d. désassemblage du site d'appel (capstone) — preuve de non-régression
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402
md = Cs(CS_ARCH_X86, CS_MODE_64)
ins = list(md.disasm(bytes(img[site:site + 40]), RVA_SITE_APPEL))
rendus = [f"{i.mnemonic} {i.op_str}" for i in ins[:3]]
if rendus != ["lea r8, [rip - 0x1699]", "mov r9d, 0x10",
              "mov dword ptr [rsp + 0x20], 0x22"]:
    erreur(f"site d'appel désassemblé inattendu : {rendus}")
if ins[0].address + ins[0].size + (-0x1699) != RVA_ETIQ_TOKEN:
    erreur("lea r8 ne vise plus ETIQ_TOKEN")
print(f"[désasm] site d'appel : {rendus[0]} (-> 0x4894) ; {rendus[1]} "
      f"(longueur 16 inchangée) ; {rendus[2]} (arrêt guillemet)")

# 3e. version 15
if bytes(img[OFF[RVA_L00_DERNIER] - 8:OFF[RVA_L00_DERNIER] + 1]) != b"terrain15":
    erreur("L00 : terrain15 attendu")
if bytes(img[OFF[RVA_S00_DERNIER] - 8:OFF[RVA_S00_DERNIER] + 1]) != b"terrain15":
    erreur("S00 : terrain15 attendu")
if img[0x5DB8:0x5DC8].decode("utf-16-le").split("\x00")[0] != "0.5.15":
    erreur("FileVersion 0.5.15 attendue")
if img[0x5EC0:0x5ECE].decode("utf-16-le") != "rrain15":
    erreur("ProductVersion terrain15 attendue")
print("[version] L00/S00 terrain15, VERSIONINFO 15, 0.5.15, rrain15")

# 3f. écriture + empreintes
DST.write_bytes(bytes(img))
print(f"\n[écrit] {DST}")
print(f"  taille  {len(img)} octets")
print(f"  md5     {hashlib.md5(bytes(img)).hexdigest()}")
print(f"  sha256  {hashlib.sha256(bytes(img)).hexdigest()}")
