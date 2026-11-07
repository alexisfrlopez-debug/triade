#!/usr/bin/env python3
"""build_m9.py — Jalon M9 de TRIADE : LE DOMAINE `tls13` (proxy 1.0.0-dev.1 —
D166/D167/D177, l'ère du TLS 1.3 pur).

Chaîne : notation (keystone) -> octets -> PE32+ à la main (HUIT sections :
.text/.rdata/.data/.text2/.text3/.text4/.text5 + .text6 NOUVELLE) -> carte
projet génération 9. Le chantier (e) du plan M9 sous les règles R4/R7 (le
corps 0.9.0 scellé INTACT — m8/proxy.exe sha 1492b0bc…, l'ancre R7 de l'ère,
confronté OCTET PAR OCTET à la recomposition M3+M4+M5+M8 AVANT l'extension)
et R10 (la version 0x01000002 — geste de BUILD, JAMAIS un scellage : la
1.0.0 finale attend le terrain vert du chantier (f)).

LA COMPOSITION 1.0.0-dev.1 (D166, tls13/I/README.md + le LISEZMOI du geste) :
  - le corps 0.9.0 INTACT (R7) : .text/.text2/.text3/.text4/.data octet-
    identiques au scellé ; .rdata identique SAUF la version @0x2820
    (0x00090001 -> 0x01000002 — LE delta R10, geste de BUILD, l'erratum
    n° 5 : dev.2, la sonde terrain du 06/11) et la table
    K[64] @0x2F00-0x2FFF (la réserve .rdata M8 VIERGE vérifiée dans le
    scellé — ÉPUISÉE par la table de SHA-256 de tls13-02, FIPS 180-4 § 4.2.2) ;
  - .text5 : sys-01..03 (l'héritage 0.9.0) + LE SOCLE SOCKET de M9-(d) —
    sys-04 l'établissement (676 o @0xA240, slot 0x300), sys-05 l'émission
    (289 o @0xA540, slot 0x180), sys-06 la réception (287 o @0xA6C0, slot
    0x180) — dans la réserve int3 VÉRIFIÉE du scellé ; la réserve
    [0xA840, 0xBFFF) demeure int3 ;
  - .text6 NOUVELLE (0xC000-0x10FFF, raw 0xAE00) : les 28 blocs du domaine
    tls13 (0xC000..0x10B00 — l'erratum n° 5 : le principal ré-arrêté 0xBC0,
    le socle tls13-28 DÉPLACÉ 0x10AC0 → 0x10D00, APRÈS les fixtures — la
    zone fixtures INTACTE, les 26 autres blocs byte-identiques) +
    les fixtures (U9/EXP_INV @0xFF00/0xFF20 ; les HUIT libellés du calendrier
    + la valeur magique HRR @0x10B80..0x10BF0 ; les fixtures du transport
    AFD @0x10C20..0x10CF0 — device/EA/bind + les TROIS spans de résolution) ;
  - PE : NumberOfSections 7 -> 8 ; SizeOfImage 0xC000 -> 0x11000 ; taille
    0xAE00 -> 0xFE00 (.text6 raw @0xAE00, vsize == rawsize 0x5000 — la
    convention .text5 : la zone réservée int3 DANS le fichier) ; les en-têtes
    restent <= 0x400 (8 en-têtes = 648 o ; le décalage D94 n'est PAS rejoué) ;
    entrée 0x8C80 INCHANGÉE (le principal n'est pas recâblé — la pièce
    rapportée, câblée au chantier (f)) ; AUCUN import nouveau.

L'ORACLE STRUCTUREL (le plan M9 rangée (e)) : AUCUN IAT PAR BLOC tls13, le
socket natif SANS une seule entrée d'import réseau (ws2_32 n'est JAMAIS
importé PAR LES BLOCS NOUVEAUX — l'héritage M4/M5 tls-04 Schannel demeure,
R7), AUCUN site syscall hors du domaine sys (l'unique site : sys-01
@0xA000 — le trombone ; sys-04..06 émettent PAR sys-01), les appels directs
FERMÉS au plan, les déplacements RIP = les fixtures déclarés, LES SLOTS
DISJOINTS (l'erratum n° 4 : le contrôle qui nomme — tls13-27 ré-arrêté
0xB80 SANS déplacer tls13-28 recouvrait le socle ; le contrôle est
PERMANENT désormais).

LE GARDE-SCEAU (D87) : le build REFUSE de démarrer si l'un des TREIZE
arbres d'intention a divergé de sa signature — le garde VERT 13/13 AVANT
construire() (la cérémonie du build 1.0.0 : la remise du développeur, sa
clé hors-ligne du 04/11, déposée au /test puis installée par
sceau_I.py deposer — l'atomicité de cérémonie).

Les oracles différentiels : l'héritage M4 puis M5 (la chaîne complète
rejouée), PUIS le harnais M8 sur les SIX blobs du domaine sys (le socle
socket compris — V1-V4 + V2d/V3t/V4t de M9-(d)). Le domaine tls13 fut
prouvé bloc par bloc aux gestes de notation (six harnais, 282 contrôles ×
3 graines) — le build en porte la preuve STRUCTURELLE et la composition
intégrale (chaque octet de .text6 compté : slot, fixture ou int3).

Usage :
  python3 build_m9.py                  # construction 1.0.0-dev.1 (+ carte gén. 9)
  python3 build_m9.py --verifier [--graine N] [--volume complet|reduit]
                                       # re-vérification + cristallisation R6
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import struct
import sys
from datetime import datetime, timezone

ICI = os.path.dirname(os.path.abspath(__file__))
TRIADE = os.path.dirname(ICI)
M4_DIR = os.path.join(TRIADE, "m4")
M5_DIR = os.path.join(TRIADE, "m5")
M8_DIR = os.path.join(TRIADE, "m8")
# Le builder M8 charge ses modules par imports PLAINS (carte_m8) et charge
# lui-même build_m4/build_m5/le plan M8/le harnais — ses répertoires sont
# sur le chemin AVANT son chargement (miroir du builder M8 pour le M5).
for _d in (M4_DIR, os.path.join(M4_DIR, "outils"), M5_DIR,
           os.path.join(M5_DIR, "outils"), M8_DIR,
           os.path.join(M8_DIR, "outils"), ICI, os.path.join(ICI, "outils")):
    if _d not in sys.path:
        sys.path.insert(0, _d)


class EchecBuild(Exception):
    """Tout échec de l'oracle, du round-trip ou de la construction."""


def _charger_module(nom: str, chemin: str):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


# --- La chaîne d'héritage : le builder M8 (qui charge TOUT : build_m4 ->
# build_m3, build_m5 -> oracle_m4/oracle_m5/carte_m5, le plan M8, le harnais
# sys, carte_m8) — puis le plan tls13 SOUS NOM PROPRE (leçon D158 ; le
# harnais M8 RÉUTILISE les modules déjà chargés, une seule instance).
B8 = _charger_module("build_m8", os.path.join(M8_DIR, "build_m8.py"))
B4 = B8.B4
B5 = B8.B5
L8 = B8.L                 # le plan M8 (la source unique du domaine sys)
harnais = B8.harnais      # le harnais M8 (V1-V4 + le socle socket M9-(d))
SCEAU_I = B8.SCEAU_I
L = _charger_module("layout_tls13", os.path.join(ICI, "layout.py"))  # plan tls13
import carte_m9 as cm9  # noqa: E402  # génération 9 (lignée D80, graine durable D144)

import capstone  # noqa: E402
import pefile  # noqa: E402
from keystone import Ks, KS_ARCH_X86, KS_MODE_64  # noqa: E402

# Les primitives de notation sont CELLES du builder M4 (une seule
# implémentation — la lignée entière les partage).
assembler_bloc = B8.assembler_bloc
round_trip = B8.round_trip
operande_rip_cible = B8.operande_rip_cible
deplacements_declares = B8.deplacements_declares

# --- Garde sceau de l'Intention (D87) : les TREIZE arbres -----------------------
# La cérémonie du build 1.0.0 (06/11) : la remise du développeur a re-signé
# m8 (la révision M9-(d) : README + les TROIS specs du socle socket) et
# tls13 (l'erratum n° 2) — le garde VERT 13/13 AVANT construire() (le plan
# M9 rangée (e), le modèle D162 : la remise précède le build).
ARBRES_GARDE_M9 = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8",
                   "tls13", "demo", "terrain", "v06"]


def _garde_sceau_I() -> None:
    try:
        SCEAU_I.garde(ARBRES_GARDE_M9)
        print(f"[sceau-I] garde : {len(ARBRES_GARDE_M9)} arbres d'intention "
              f"conformes à leurs signatures (le garde VERT 13/13 AVANT "
              f"construire()) ; clé déposée : {SCEAU_I.etat_cle()}")
    except SCEAU_I.EchecSceauI as exc:
        raise EchecBuild(
            f"{exc}\n  [cérémonie] la remise du développeur est requise : "
            f"v06/sceau-I/a-signer.txt (signer hors-ligne les arbres divergés "
            f"— puis : python3 v06/sceau_I.py deposer signatures-I.txt "
            f"--cle cle-publique-I.txt)") from exc


# --- Le scellé 0.9.0 (l'ancre R7 de l'ère M9) ------------------------------------

SHA_PROXY_090 = "1492b0bc0792e1ab162338b414fb20573134e84d752b9d0657292421f8eb0cd4"
# le proxy.exe 0.9.0 scellé (l'artefact du run e4 + la carte génération 8
# scellée version=0.9.0 — le scellage est un fait de carte, D104 ; l'ancre
# R7 de l'ère M9 : le corps que la 1.0.0-dev.1 étend SANS le bouger).

# --- Les dimensions de l'ère (ARRÊT au chantier du build — le miroir D162) --------

TEXT6_VA = L.TEXT6_VA              # 0xC000 (le plan tls13 — la 8e section)
TEXT6_FILE = L8.TAILLE_FICHIER     # 0xAE00 — la fin du scellé 0.9.0
TEXT6_VSIZE = 0x5000               # 0x10CF0 de contenu (blocs + fixtures)
                                   # -> la section entière 0xC000-0x10FFF
                                   # (miroir .text5 : vsize == rawsize, la
                                   # zone réservée int3 DANS le fichier)
SIZE_OF_IMAGE_M9 = 0x11000         # 0xC000 + .text6
TAILLE_FICHIER_M9 = 0xFE00         # 0xAE00 + 0x5000

# --- Les blocs du socle socket (sys-04..06 — M9-(d), la réserve .text5) -----------

BLOCS_SOCLE = [
    ("g90004", "sys-04:R1", "sys-04-transport", L8.SYS04_VA, L8.SLOTS_SYS["g90004"][1]),
    # la révision 2 étendue (l'erratum n° 9, Entrée 187) : sys-05 ET sys-06
    # re-notés — le WSABUF CANONIQUE x64 (SEIZE o : len à +0, padding 4 o,
    # buf à +8 — la pose 0x68, le MÊME encode, le slot intact)
    ("g90005", "sys-05:R2", "sys-05-emission", L8.SYS05_VA, L8.SLOTS_SYS["g90005"][1]),
    ("g90006", "sys-06:R2", "sys-06-reception", L8.SYS06_VA, L8.SLOTS_SYS["g90006"][1]),
]
assert all((b[3], b[4]) == L8.SLOTS_SYS[b[0]] for b in BLOCS_SOCLE), \
    "BLOCS_SOCLE diverge du plan M8 (layout.py, source unique — D161)"

# --- Les 28 blocs du domaine tls13 (le plan, source unique) -----------------------

BLOCS_TLS13 = [
    ("h100001", "tls13-01:R1", "tls13-01-sha256-init", L.TLS01_VA, L.SLOTS_TLS13["h100001"][1]),
    ("h100002", "tls13-02:R1", "tls13-02-sha256-comprimer", L.TLS02_VA, L.SLOTS_TLS13["h100002"][1]),
    ("h100003", "tls13-03:R1", "tls13-03-sha256-absorber", L.TLS03_VA, L.SLOTS_TLS13["h100003"][1]),
    ("h100004", "tls13-04:R1", "tls13-04-sha256-finaliser", L.TLS04_VA, L.SLOTS_TLS13["h100004"][1]),
    ("h100005", "tls13-05:R1", "tls13-05-hmac-sha256", L.TLS05_VA, L.SLOTS_TLS13["h100005"][1]),
    ("h100006", "tls13-06:R1", "tls13-06-hkdf-extract", L.TLS06_VA, L.SLOTS_TLS13["h100006"][1]),
    ("h100007", "tls13-07:R1", "tls13-07-hkdf-expand", L.TLS07_VA, L.SLOTS_TLS13["h100007"][1]),
    ("h100008", "tls13-08:R1", "tls13-08-hkdf-expand-label", L.TLS08_VA, L.SLOTS_TLS13["h100008"][1]),
    ("h100009", "tls13-09:R1", "tls13-09-f25519-add", L.TLS09_VA, L.SLOTS_TLS13["h100009"][1]),
    ("h100010", "tls13-10:R1", "tls13-10-f25519-sub", L.TLS10_VA, L.SLOTS_TLS13["h100010"][1]),
    ("h100011", "tls13-11:R1", "tls13-11-f25519-mul", L.TLS11_VA, L.SLOTS_TLS13["h100011"][1]),
    ("h100012", "tls13-12:R1", "tls13-12-f25519-propager-geler", L.TLS12_VA, L.SLOTS_TLS13["h100012"][1]),
    ("h100013", "tls13-13:R1", "tls13-13-x25519-echelle", L.TLS13_VA, L.SLOTS_TLS13["h100013"][1]),
    ("h100014", "tls13-14:R1", "tls13-14-x25519-cle-publique", L.TLS14_VA, L.SLOTS_TLS13["h100014"][1]),
    ("h100015", "tls13-15:R1", "tls13-15-aes128-cles-tour", L.TLS15_VA, L.SLOTS_TLS13["h100015"][1]),
    ("h100016", "tls13-16:R1", "tls13-16-aes128-bloc", L.TLS16_VA, L.SLOTS_TLS13["h100016"][1]),
    ("h100017", "tls13-17:R1", "tls13-17-ghash-multiplication", L.TLS17_VA, L.SLOTS_TLS13["h100017"][1]),
    ("h100018", "tls13-18:R1", "tls13-18-gcm-sceller", L.TLS18_VA, L.SLOTS_TLS13["h100018"][1]),
    ("h100019", "tls13-19:R1", "tls13-19-gcm-ouvrir", L.TLS19_VA, L.SLOTS_TLS13["h100019"][1]),
    ("h100020", "tls13-20:R1", "tls13-20-enregistrement-proteger", L.TLS20_VA, L.SLOTS_TLS13["h100020"][1]),
    ("h100021", "tls13-21:R1", "tls13-21-enregistrement-deproteger", L.TLS21_VA, L.SLOTS_TLS13["h100021"][1]),
    ("h100022", "tls13-22:R1", "tls13-22-clienthello-composer", L.TLS22_VA, L.SLOTS_TLS13["h100022"][1]),
    ("h100023", "tls13-23:R1", "tls13-23-serverhello-traiter", L.TLS23_VA, L.SLOTS_TLS13["h100023"][1]),
    ("h100024", "tls13-24:R1", "tls13-24-calendrier-cles", L.TLS24_VA, L.SLOTS_TLS13["h100024"][1]),
    ("h100025", "tls13-25:R1", "tls13-25-finished-calculer-verifier", L.TLS25_VA, L.SLOTS_TLS13["h100025"][1]),
    ("h100026", "tls13-26:R1", "tls13-26-epinglage", L.TLS26_VA, L.SLOTS_TLS13["h100026"][1]),
    ("h100027", "tls13-27:R1", "tls13-27-principal-machine-etats", L.TLS27_VA, L.SLOTS_TLS13["h100027"][1]),
    ("h100028", "tls13-28:R1", "tls13-28-socle-appel", L.TLS28_VA, L.SLOTS_TLS13["h100028"][1]),
]
assert all((b[3], b[4]) == L.SLOTS_TLS13[b[0]] for b in BLOCS_TLS13), \
    "BLOCS_TLS13 diverge du plan tls13 (layout.py, source unique — D161)"

_CLE_BLOB_SYS = {"g90001": "sys-01", "g90002": "sys-02", "g90003": "sys-03",
                 "g90004": "sys-04", "g90005": "sys-05", "g90006": "sys-06"}


def chemin_notation(repertoire: str, fichier: str) -> str:
    return os.path.join(repertoire, "notation", fichier + ".asm")


# --- Couche I : lecture et audit du gabarit (les specs sont la source, R2) --------

def lire_spec_m9(chemin: str) -> dict:
    """Le gabarit commun M8/M9 (§ 2.2) : la première ligne nomme, les CINQ
    blocs font foi — l'Intention, le Contrat, pre/post/inv PARSÉS (la carte
    en porte le condensé — la couche I est la source, jamais une copie)."""
    with open(chemin, encoding="utf-8") as f:
        lignes = f.read().splitlines()
    m = re.match(r"(\S+) · (.+?) · révision (\d+)", lignes[0])
    if not m:
        raise EchecBuild(f"{chemin} : première ligne hors gabarit § 2.2")
    spec = {"id": m.group(1), "nom": m.group(2), "rev": int(m.group(3))}
    texte = "\n".join(lignes)
    for bloc in ("Intention", "Contrat", "pre", "post", "inv"):
        if bloc not in texte:
            raise EchecBuild(f"{chemin} : bloc de gabarit manquant : {bloc}")

    def _section(marqueur: str) -> str:
        pat = re.compile(rf"^  {marqueur}\s*:\s*(.*)$")
        sortie, actif = [], False
        for ligne in lignes:
            mm = pat.match(ligne)
            if mm:
                actif = True
                if mm.group(1).strip():
                    sortie.append(mm.group(1).strip())
                continue
            if actif:
                if ligne.startswith("  ") and ligne.strip():
                    sortie.append(ligne.strip())
                else:
                    actif = False
        return " ".join(sortie)

    spec["pre"] = _section("pre")
    spec["post"] = _section("post")
    spec["inv"] = _section("inv")
    if not (spec["pre"] and spec["post"] and spec["inv"]):
        raise EchecBuild(f"{chemin} : sections pre/post/inv vides (gabarit § 2.2)")
    return spec


_FICHIERS_I_SOCLE = {
    "g90004": "sys-04-transport.md",
    "g90005": "sys-05-emission.md",
    "g90006": "sys-06-reception.md",
}


def charger_couche_I_m9() -> dict[str, dict]:
    """Les 31 spécifications nouvelles (3 socle + 28 tls13) : gabarit, id,
    révision — la charte LUE au passage (R2 : écrit-avant-code)."""
    specs = {}
    for chemin_readme, marqueur in (
            (os.path.join(M8_DIR, "I", "README.md"), "m8"),
            (os.path.join(ICI, "I", "README.md"), "tls13")):
        with open(chemin_readme, encoding="utf-8") as f:
            texte_readme = f.read()
        if "écrite-avant-code" not in texte_readme:
            raise EchecBuild(f"{chemin_readme} : la provenance écrite-avant-code "
                             f"absente de la charte {marqueur} (R2)")
    for bid, sid, fichier, _rva, _slot in BLOCS_SOCLE:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(M8_DIR, "I", _FICHIERS_I_SOCLE[bid])
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec_m9(chemin)
        if spec["id"] != ident or spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : {spec['id']}:{spec['rev']} != {sid}")
        specs[bid] = spec
    for bid, sid, fichier, _rva, _slot in BLOCS_TLS13:
        ident, rev_ref = sid.split(":")
        chemin = os.path.join(ICI, "I", fichier + ".md")
        if not os.path.exists(chemin):
            raise EchecBuild(f"spécification I introuvable pour {sid} : {chemin}")
        spec = lire_spec_m9(chemin)
        if spec["id"] != ident or spec["rev"] != int(rev_ref[1:]):
            raise EchecBuild(f"{chemin} : {spec['id']}:{spec['rev']} != {sid}")
        specs[bid] = spec
    return specs


def deps_notation(chemin_asm: str) -> str:
    """Les dépendances citées par l'en-tête de notation (l'auteur les écrit —
    le build les relit : une seule source, la notation)."""
    with open(chemin_asm, encoding="utf-8") as f:
        for ligne in f:
            if ligne.startswith(";") and "Dépendances :" in ligne:
                return ligne.split("Dépendances :", 1)[1].strip()
    return ""


# --- L'oracle structurel M9 (le plan rangée (e) — LA RÈGLE du domaine) ------------
# AUCUN IAT PAR BLOC tls13 ; le socket natif SANS une seule entrée d'import
# réseau ; AUCUN site syscall hors du domaine sys (l'unique site : sys-01) ;
# les appels directs FERMÉS au plan ; les déplacements RIP = les fixtures
# déclarés ; LES SLOTS DISJOINTS (l'erratum n° 4 : le contrôle qui nomme).

_SLOTS_IAT_COMPLETS = B8._SLOTS_IAT_COMPLETS

APPELS_FERMES_SOCLE = {L8.SYS01_VA, L8.SYS02_VA}   # la séquence mesurée mswsock
DONNEES_RIP_SOCLE = {L8.R_SYS_DEVICE, L8.R_SYS_EA, L8.R_SYS_BIND,
                     L8.R_SYS_NOM_CREATEFILE, L8.R_SYS_NOM_DEVICEIOCTL,
                     L8.R_SYS_NOM_CLOSE}
APPELS_FERMES_TLS13 = {rva for rva, _slot in L.SLOTS_TLS13.values()}
DONNEES_RIP_TLS13 = {L.R_K, L.R_U9, L.R_EXP_INV, L.R_LIB_DERIVED,
                     L.R_LIB_C_HS, L.R_LIB_S_HS, L.R_LIB_C_AP, L.R_LIB_S_AP,
                     L.R_LIB_KEY, L.R_LIB_IV, L.R_LIB_FINISHED, L.R_HRR}


def oracle_structurel_m9(specs: dict, code: dict, blocs: list[tuple],
                         appels_fermes: set, donnees_rip: set,
                         domaine: str, convention_64: bool = False) -> list[str]:
    """L'oracle structurel M9. D8 : padding >= 16, slots alignés 16 — la
    granularité d'un bloc (la décision, jamais une convention d'écriture).
    La convention multiple-de-64 est celle de l'ère M8 (vérifiée pour la
    famille socle ; l'arrêt tls13 consigné — Entry 175 — a posé 0x120/0xB0
    aux minimums alignés 16 : D8 tenu, la convention déclinée)."""
    verrous = []

    def verrou(nom, condition, detail=""):
        if not condition:
            raise EchecBuild(f"oracle structurel : {nom} {detail}")
        verrous.append(nom)

    for bid, sid, fichier, rva, slot in blocs:
        insns = code[bid]["insns"]
        adresses_insns = {i.address for i in insns}

        for i in insns:
            if i.mnemonic.startswith("j"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:saut-interne@{i.address:#x}",
                       cible in adresses_insns, f"cible {cible:#x} hors frontière")

        nb_indirects = 0
        for i in insns:
            if i.mnemonic != "call":
                continue
            if "rip" in i.op_str:
                # LA RÈGLE DU DOMAINE : aucun slot IAT n'est jamais autorisé
                # — la preuve structurelle (charte § 3/§ 7)
                cible = operande_rip_cible(i)
                slots = {v: n for n, v in _SLOTS_IAT_COMPLETS.items()}
                verrou(f"{bid}:AUCUN-IAT@{i.address:#x}",
                       cible not in slots,
                       f"iat:{slots.get(cible)} — AUCUN IAT PAR BLOC {domaine}")
                continue
            if i.op_str.startswith("0x"):
                cible = int(i.op_str, 16)
                verrou(f"{bid}:appel-ferme@{i.address:#x}",
                       cible in appels_fermes or cible in adresses_insns,
                       f"call {cible:#x} hors le jeu fermé du plan (I1)")
            elif i.op_str.startswith("r"):
                nb_indirects += 1
                verrou(f"{bid}:appel-indirect-declare@{i.address:#x}",
                       bid == "h100028",
                       "l'appel indirect DÉCLARÉ est la rotule tls13-28 "
                       "seule (I2 : la cible est une DONNÉE du contexte — "
                       "NI un import NI un syscall)")
        if bid != "h100028":
            verrou(f"{bid}:aucun-appel-indirect", nb_indirects == 0,
                   f"{nb_indirects} appel(s) indirect(s)")
        else:
            verrou("h100028:les-deux-rappels", nb_indirects == 2,
                   "la rotule : émettre + recevoir, DEUX rappels (I2)")

        # AUCUN site syscall hors du domaine sys : les blocs NOUVEAUX
        # émettent PAR sys-01 (le trombone @0xA000) — le site unique.
        nb_syscall = sum(1 for i in insns
                         if i.mnemonic in ("syscall", "sysenter", "int"))
        verrou(f"{bid}:aucun-site-syscall", nb_syscall == 0,
               f"{nb_syscall} instruction(s) syscall/int — AUCUN site "
               f"syscall hors du domaine sys (l'unique site : sys-01)")

        cibles_rip: set[int] = set()
        for i in insns:
            cible = operande_rip_cible(i)
            if cible is not None and i.mnemonic != "call":
                cibles_rip.add(cible)
                verrou(f"{bid}:donnees-autorisees@{i.address:#x}",
                       cible in donnees_rip
                       or (rva <= cible < rva + slot),
                       f"cible {cible:#x} hors fixtures déclarés du plan")

        declarees = deplacements_declares(chemin_notation(
            M8_DIR if domaine == "socle" else ICI, fichier))
        if declarees is not None:
            rip_reelles = {operande_rip_cible(i) for i in insns}
            rip_reelles.discard(None)
            verrou(f"{bid}:deplacements-rip-declares", rip_reelles == declarees,
                   f"réelles {sorted(hex(c) for c in rip_reelles - declarees)} "
                   f"non déclarées / déclarées "
                   f"{sorted(hex(c) for c in declarees - rip_reelles)} absentes")

        fin_code = insns[-1].address + insns[-1].size
        verrou(f"{bid}:padding-16", rva + slot - fin_code >= 16,
               f"écart {rva + slot - fin_code} (D8 : padding de 16 octets)")
        verrou(f"{bid}:slot-aligne-16", rva % 16 == 0)
        if convention_64:
            verrou(f"{bid}:slot-multiple-64", slot % 64 == 0,
                   f"la convention de l'ère M8 (slot {slot:#x})")

    # LES SLOTS DISJOINTS (l'erratum n° 4 — le contrôle qui nomme : jamais
    # un slot ne recouvre le suivant, jamais un fixture ne vit dans un slot)
    ordonnes = sorted(blocs, key=lambda b: b[3])
    fin_prec = 0
    for bid, _sid, _f, rva, slot in ordonnes:
        verrou(f"{bid}:slot-disjoint", rva >= fin_prec,
               f"le slot recouvre la fin {fin_prec:#x} (l'erratum n° 4 : "
               f"un ré-arrêt SANS déplacer le suivant)")
        fin_prec = rva + slot
    for rva_f in sorted(donnees_rip):
        for bid, _sid, _f, rva, slot in ordonnes:
            if rva <= rva_f < rva + slot:
                verrou(f"fixture-{rva_f:#x}-hors-slot", False,
                       f"le fixture {rva_f:#x} vit DANS le slot de {bid}")

    attendus = {b for b, *_ in blocs}
    verrou(f"tracabilite-I-{domaine}", attendus <= set(specs),
           str(attendus - set(specs)))
    return verrous


# --- Assemblage + round-trip -------------------------------------------------------

def assembler_blocs(blocs: list[tuple], repertoire: str, specs: dict) -> dict:
    ks = Ks(KS_ARCH_X86, KS_MODE_64)
    cs = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    code: dict[str, dict] = {}
    for bid, sid, fichier, rva, slot in blocs:
        chemin = chemin_notation(repertoire, fichier)
        octets, metas = assembler_bloc(ks, chemin, rva, slot)
        insns = round_trip(cs, ks, chemin, rva, octets, metas)
        slot_complet = octets + b"\x90" * (slot - len(octets))
        code[bid] = {"octets": octets, "metas": metas, "insns": insns,
                     "slot": slot_complet}
        print(f"[R5] {bid} ({sid}) : {len(octets)} o, "
              f"round-trip {len(insns)}/{len(insns)} = 100 %")
    return code


# --- L'héritage complet (M3+M4+M5+M8 re-vérifié, la preuve R7 absolue) -------------

def heritage_complet_m9() -> dict:
    """Re-vérifie TOUT l'héritage (la chaîne M3/M4/M5 par le builder M8,
    l'ancre 0.6.0) PUIS recompose l'image 0.9.0 (sys-01..03) et la confronte
    OCTET PAR OCTET au scellé m8/proxy.exe (1492b0bc…) — l'ancre R7 de l'ère
    M9 : le corps que la 1.0.0-dev.1 étend sans le bouger d'un octet."""
    h = B8.heritage_complet()
    specs_m8, code_m8, verrous_m8 = B8.assembler_tout_m8()
    sections_m8 = B8.composer_image_m8(h["sections_m5"], code_m8)
    exe_090_compose = B8.ecrire_pe32plus(*sections_m8)
    with open(os.path.join(M8_DIR, "proxy.exe"), "rb") as f:
        scelle_090 = f.read()
    if hashlib.sha256(scelle_090).hexdigest() != SHA_PROXY_090:
        raise EchecBuild("m8/proxy.exe diverge du scellé 0.9.0 (1492b0bc…) — "
                         "l'ancre R7 de l'ère M9 est rompue")
    if hashlib.sha256(exe_090_compose).hexdigest() != SHA_PROXY_090:
        raise EchecBuild("l'image 0.9.0 recomposée diverge du scellé "
                         "(1492b0bc…) — R7 : l'ère M9 ne peut pas naître "
                         "d'un corps non prouvé")
    print(f"[R7] l'image 0.9.0 recomposée == le scellé 0.9.0 OCTET PAR OCTET "
          f"(sha {SHA_PROXY_090[:16]}…) — le corps 0.9.0 INTACT, l'ancre de "
          f"l'ère M9 ; la carte génération 8 scellée prouve CES octets "
          f"(version=0.9.0, le fait de carte D104)")
    return {"h": h, "specs_m8": specs_m8, "code_m8": code_m8,
            "verrous_m8": verrous_m8, "sections_m8": sections_m8,
            "scelle_090": scelle_090}


# --- Les tranches de l'image M9 ----------------------------------------------------

def tranche_section_m9(exe: bytes, rva: int, taille: int) -> bytes:
    """La tranche d'une section aux RVA de l'ère M9 (.text5/.text6 comprises)."""
    if rva < L8.TEXT5_VA:
        return B8.tranche_section(exe, rva, taille)
    if rva < L8.TEXT5_VA + 0x2000:
        return exe[L8.TEXT5_FILE + (rva - L8.TEXT5_VA):
                   L8.TEXT5_FILE + (rva - L8.TEXT5_VA) + taille]
    if rva < TEXT6_VA + TEXT6_VSIZE:
        return exe[TEXT6_FILE + (rva - TEXT6_VA):
                   TEXT6_FILE + (rva - TEXT6_VA) + taille]
    raise EchecBuild(f"RVA {rva:#x} hors sections")


# --- Les fixtures .text6 (le plan, source unique — RE-DÉRIVÉS, jamais recopiés) ----

def fixtures_text6() -> list[tuple[int, bytes, str]]:
    """Les fixtures du domaine tls13 + du transport AFD, aux ARRÊTS consignés
    du plan (miroir D95) : U9/EXP_INV (le geste x25519), les HUIT libellés +
    HRR (le geste poignée), le device/EA/bind + les TROIS spans (M9-(d) —
    l'EA et le bind DÉRIVÉS par les fonctions du harnais, la seule source,
    jugée par verifier_specs_m9d)."""
    return [
        (L.R_U9, L.X25519_BASE.to_bytes(32, "little"),
         "U9 (le point de base, RFC 7748 § 6.1)"),
        (L.R_EXP_INV, L.X25519_EXP_INV, "EXP_INV (l'exposant p−2, LE 32 o)"),
        (L.R_LIB_DERIVED, L.LIBELLES["derived"], "libellé « derived »"),
        (L.R_LIB_C_HS, L.LIBELLES["c hs traffic"], "libellé « c hs traffic »"),
        (L.R_LIB_S_HS, L.LIBELLES["s hs traffic"], "libellé « s hs traffic »"),
        (L.R_LIB_C_AP, L.LIBELLES["c ap traffic"], "libellé « c ap traffic »"),
        (L.R_LIB_S_AP, L.LIBELLES["s ap traffic"], "libellé « s ap traffic »"),
        (L.R_LIB_KEY, L.LIBELLES["key"], "libellé « key »"),
        (L.R_LIB_IV, L.LIBELLES["iv"], "libellé « iv »"),
        (L.R_LIB_FINISHED, L.LIBELLES["finished"], "libellé « finished »"),
        (L.R_HRR, L.HRR_MAGIQUE, "la valeur magique HRR (RFC 8446 § 4.1.3)"),
        (L8.R_SYS_DEVICE, L8.TXT_AFD_DEVICE + b"\x00\x00",
         "le device AFD UTF-16LE + NUL (42 o)"),
        (L8.R_SYS_EA, harnais.ea_deterministe(),
         "le EA déterministe AfdOpenPacketXX (54 o)"),
        (L8.R_SYS_BIND, harnais.bind_wildcard(),
         "le bind implicite WILDCARD (20 o)"),
        (L8.R_SYS_NOM_CREATEFILE, L8.TXT_NT_CREATEFILE,
         "le span « NtCreateFile » (11 o)"),
        (L8.R_SYS_NOM_DEVICEIOCTL, L8.TXT_NT_DEVICEIOCTL,
         "le span « NtDeviceIoControlFile » (21 o)"),
        (L8.R_SYS_NOM_CLOSE, L8.TXT_NT_CLOSE, "le span « NtClose » (7 o)"),
    ]


# --- Composition de l'image M9 ------------------------------------------------------

def _somme_qwords(octets: bytes) -> int:
    return sum(struct.unpack(f"<{len(octets) // 8}Q", octets)) & 0xFFFFFFFFFFFFFFFF


def composer_image_m9(sections_m8: tuple, code_sys: dict, code_tls13: dict):
    """-> (texte, rdata, data, text2, text3, text4, text5, text6) — proxy M9.

    Le corps 0.9.0 INTACT (R7) : les SEPT sections héritées, les deltas
    DOCUMENTÉS uniquement — le socle socket dans la réserve int3 .text5
    (VÉRIFIÉE int3 dans le scellé avant pose), K[64] dans la réserve .rdata
    (VÉRIFIÉE vierge), la version (LE delta R10). La .text6 NOUVELLE :
    base int3, les 28 slots (code + NOP, D161/I7), les fixtures aux ARRÊTS.
    """
    texte, rdata, data, text2, text3, text4, text5 = sections_m8

    # .text5 : la réserve du scellé 0.9.0 reçoit le socle socket — la zone
    # est int3 dans le scellé (vérifiée : le corps ne bouge que là où la
    # réserve était DÉCLARÉE, m8/layout.py « la croissance du domaine »)
    text5 = bytearray(text5)
    if len(text5) != 0x2000:
        raise EchecBuild(f".text5 héritée : {len(text5)} o != 0x2000")
    for bid, _sid, _f, rva, slot in BLOCS_SOCLE:
        debut, fin = rva - L8.TEXT5_VA, rva - L8.TEXT5_VA + slot
        if any(b != 0xCC for b in text5[debut:fin]):
            raise EchecBuild(f"la réserve .text5 du socle [{rva:#x}, "
                             f"{rva + slot:#x}) n'est pas int3 dans le "
                             f"scellé 0.9.0 — R7 rompu")
        text5[debut:fin] = code_sys[bid]["slot"]

    # .rdata : la réserve M8 (VIERGE dans le scellé — vérifiée sur pièces au
    # chantier (b), Entrée 170) reçoit K[64] ; la version (LE delta R10)
    rdata = bytearray(rdata)
    if len(rdata) != B5.L.RDATA_VSIZE:
        raise EchecBuild(f".rdata héritée : {len(rdata)} o != {B5.L.RDATA_VSIZE:#x}")
    if any(rdata[L.R_K - 0x2000: 0x1000]):
        raise EchecBuild("la réserve .rdata 0x2F00-0x2FFF n'est pas vierge "
                         "dans l'héritage 0.9.0 — R7 rompu (la réserve M8 "
                         "ÉPUISÉE par K[64], Entrée 170)")
    rdata[L.R_K - 0x2000: L.R_K - 0x2000 + 256] = struct.pack("<64I", *L.K)
    struct.pack_into("<Q", rdata, B5.L4.R_VERSION - 0x2000, L.VERSION_DEV)

    # .text6 : base int3 (la convention des zones réservées), les slots
    # portent code + padding NOP (D161/I7), les fixtures aux ARRÊTS
    text6 = bytearray(b"\xcc" * TEXT6_VSIZE)
    poses: list[tuple[int, int, str]] = []

    def poser(rva_c: int, donnees: bytes, nom: str):
        debut, fin = rva_c - TEXT6_VA, rva_c - TEXT6_VA + len(donnees)
        if fin > TEXT6_VSIZE:
            raise EchecBuild(f".text6 débordante à {rva_c:#x} ({nom})")
        for rva_p, fin_p, nom_p in poses:
            if debut < fin_p and rva_p < fin:
                raise EchecBuild(f"chevauchement .text6 : {nom} "
                                 f"[{rva_c:#x}, {rva_c + len(donnees):#x}) "
                                 f"recouvre {nom_p}")
        poses.append((debut, fin, nom))
        text6[debut:fin] = donnees

    for bid, _sid, _f, rva, slot in BLOCS_TLS13:
        poser(rva, code_tls13[bid]["slot"], f"slot {bid}")
    for rva_f, octets_f, nom_f in fixtures_text6():
        poser(rva_f, octets_f, nom_f)

    return (bytes(texte), bytes(rdata), bytes(data), bytes(text2),
            bytes(text3), bytes(text4), bytes(text5), bytes(text6))


# --- Éditeur PE32+ (huit sections) ---------------------------------------------------

def ecrire_pe32plus(texte: bytes, rdata: bytes, data: bytes, text2: bytes,
                    text3: bytes, text4: bytes, text5: bytes,
                    text6: bytes) -> bytes:
    dos = b"MZ" + b"\x00" * 58 + struct.pack("<I", 0x40)
    coff = struct.pack("<HHIIIHH", 0x8664, 8, 0, 0, 0, 0xF0, 0x0002)
    opt_fixe = struct.pack(
        "<HBBIIIIIQIIHHHHHHIIIIHHQQQQII",
        0x20B, 0, 0,
        B5.L.ENTREE, len(texte) + len(text2) + len(text3) + len(text4), 0,
        B5.L.ENTREE_M5, B5.L.TEXT_RVA,  # AddressOfEntryPoint : 0x8C80 INCHANGÉ
                                       # (http-12:R3 — le principal n'est PAS
                                       # recâblé, R7 ; le domaine est la pièce
                                       # rapportée, câblée au chantier (f))
        B5.L.IMAGE_BASE,
        B5.L.SECT_ALIGN, B5.L.FILE_ALIGN,
        6, 0, 0, 1, 6, 0, 0,
        SIZE_OF_IMAGE_M9,             # 0x11000 (0xC000 + .text6)
        B5.L.TEXT_FILE,                # SizeOfHeaders : 0x400 (INCHANGÉ —
                                       # 8 en-têtes = 648 o, la marge suffit :
                                       # le décalage D94 n'est PAS rejoué)
        0,
        3,                             # Subsystem : CONSOLE
        B5.L.DLL_CHARACTERISTICS,
        0x100000, 0x1000, 0x100000, 0x1000,
        0, 16,
    )
    dirs = [(0, 0)] * 16
    dirs[1] = (B5.L.R_IMPORTS_M5, 100)   # le répertoire d'imports M5 INCHANGÉ
    dirs[5] = (B5.L4.R_RELOC, 12)
    dirs[12] = (B5.L4.L3.R_IAT, 88)
    opt = bytes(opt_fixe) + b"".join(struct.pack("<II", *d) for d in dirs)

    def sh(nom, vsize, vaddr, rawsz, rawptr, cara):
        return struct.pack("<8sIIIIIIHHI", nom, vsize, vaddr, rawsz, rawptr,
                           0, 0, 0, 0, cara)

    sections = (
        sh(b".text\x00\x00\x00", B5.L.TEXT_VSIZE, B5.L.TEXT_RVA, B5.L.TEXT_VSIZE,
           B5.L.TEXT_FILE, 0x60000020)
        + sh(b".rdata\x00\x00", B5.L.RDATA_VSIZE, B5.L.RDATA_RVA, B5.L.RDATA_VSIZE,
             B5.L.RDATA_FILE, 0x40000040)
        + sh(b".data\x00\x00\x00", B5.L.DATA_VSIZE, B5.L.DATA_RVA, B5.L.DATA_RAW,
             B5.L.DATA_FILE, 0xC0000040)
        + sh(b".text2\x00\x00", B5.L.TEXT2_VSIZE, B5.L.TEXT2_RVA, B5.L.TEXT2_VSIZE,
             B5.L.TEXT2_FILE, 0x60000020)
        + sh(b".text3\x00\x00", B5.L.TEXT3_VSIZE, B5.L.TEXT3_RVA, B5.L.TEXT3_VSIZE,
             B5.L.TEXT3_FILE, 0x60000020)
        + sh(b".text4\x00\x00", B5.L.TEXT4_VSIZE, B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE,
             B5.L.TEXT4_FILE, 0x60000020)
        + sh(b".text5\x00\x00", 0x2000, L8.TEXT5_VA, 0x2000,
             L8.TEXT5_FILE, 0x60000020)
        + sh(b".text6\x00\x00", TEXT6_VSIZE, TEXT6_VA, TEXT6_VSIZE,
             TEXT6_FILE, 0x60000020)
    )
    entetes = dos + b"PE\x00\x00" + coff + opt + sections
    assert len(entetes) == 64 + 4 + 20 + 240 + 320, len(entetes)
    assert len(entetes) <= B5.L.TEXT_FILE, "les 8 en-têtes débordent SizeOfHeaders"
    exe = bytearray(b"\x00" * TAILLE_FICHIER_M9)
    exe[0:len(entetes)] = entetes
    exe[B5.L.TEXT_FILE:B5.L.TEXT_FILE + len(texte)] = texte
    exe[B5.L.RDATA_FILE:B5.L.RDATA_FILE + len(rdata)] = rdata
    exe[B5.L.DATA_FILE:B5.L.DATA_FILE + len(data)] = data
    exe[B5.L.TEXT2_FILE:B5.L.TEXT2_FILE + len(text2)] = text2
    exe[B5.L.TEXT3_FILE:B5.L.TEXT3_FILE + len(text3)] = text3
    exe[B5.L.TEXT4_FILE:B5.L.TEXT4_FILE + len(text4)] = text4
    exe[L8.TEXT5_FILE:L8.TEXT5_FILE + len(text5)] = text5
    exe[TEXT6_FILE:TEXT6_FILE + len(text6)] = text6
    return bytes(exe)


# --- Validation PE (la composition INTEGRALE : chaque octet compté) -----------------

def valider_pe_m9(exe: bytes, code_sys: dict, code_tls13: dict):
    pe = pefile.PE(data=exe)
    assert pe.FILE_HEADER.Machine == 0x8664, "Machine != x86-64"
    assert pe.FILE_HEADER.NumberOfSections == 8, "sections != 8"
    assert pe.OPTIONAL_HEADER.Magic == 0x20B, "magic != PE32+"
    assert pe.OPTIONAL_HEADER.AddressOfEntryPoint == B5.L.ENTREE_M5, \
        f"point d'entrée != {B5.L.ENTREE_M5:#x} (http-12:R3 — INCHANGÉ, R7)"
    assert pe.OPTIONAL_HEADER.ImageBase == B5.L.IMAGE_BASE
    assert pe.OPTIONAL_HEADER.Subsystem == 3, "sous-système != CONSOLE"
    dc = pe.OPTIONAL_HEADER.DllCharacteristics
    assert dc & 0x0040 and dc & 0x0020 and dc & 0x0100, "DYNAMICBASE/HEVA/NX absents"
    assert pe.OPTIONAL_HEADER.SizeOfImage == SIZE_OF_IMAGE_M9, \
        f"SizeOfImage != {SIZE_OF_IMAGE_M9:#x}"
    noms = [s.Name.decode().rstrip("\x00") for s in pe.sections]
    assert noms == [".text", ".rdata", ".data", ".text2", ".text3", ".text4",
                    ".text5", ".text6"], noms
    assert pe.sections[7].Characteristics & 0x60000020 == 0x60000020, \
        ".text6 non RX"
    assert pe.sections[7].VirtualAddress == TEXT6_VA
    assert pe.sections[7].PointerToRawData == TEXT6_FILE, \
        f".text6 raw != {TEXT6_FILE:#x}"
    for s, attendu in zip(pe.sections, (B5.L.TEXT_FILE, B5.L.RDATA_FILE,
                                        B5.L.DATA_FILE, B5.L.TEXT2_FILE,
                                        B5.L.TEXT3_FILE, B5.L.TEXT4_FILE,
                                        L8.TEXT5_FILE, TEXT6_FILE)):
        assert s.PointerToRawData == attendu, \
            f"PointerToRawData {s.Name.decode().rstrip(chr(0))} != {attendu:#x}"
    assert pe.OPTIONAL_HEADER.SizeOfHeaders == B5.L.TEXT_FILE, "SizeOfHeaders != 0x400"
    # Les imports : INCHANGÉS (kernel32 ×2 descripteurs, ws2_32, secur32 —
    # l'héritage M4/M5 ; le socket natif SANS une seule entrée d'import
    # réseau NOUVELLE : le domaine déclare RIEN, la preuve structurelle)
    imports = {}
    for entree in pe.DIRECTORY_ENTRY_IMPORT:
        imports.setdefault(entree.dll.decode().lower(), []).extend(
            i.name.decode() for i in entree.imports)
    assert imports["kernel32.dll"] == ["GetCommandLineW"] + B5.L4.L3.KERNEL32_IMPORTS
    assert imports["ws2_32.dll"] == B5.L4.L3.WS2_IMPORTS
    assert imports["secur32.dll"] == B5.L4.SECUR32_IMPORTS
    assert pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress == B5.L.R_IMPORTS_M5
    assert len(exe) == TAILLE_FICHIER_M9, "taille de fichier inattendue"
    # Zones réservées héritées : int3 dans l'image livrée
    for rva in (0x4200, 0x45C0, 0x4800, 0x7FC0, 0x8FC0):
        assert tranche_section_m9(exe, rva, 1)[0] == 0xCC, \
            f"zone réservée @{rva:#x} != int3"
    # Version (R10 : geste de BUILD — 0x01000002 > 0x01000001 dev.1 > 0x00090001)
    version = struct.unpack("<Q", tranche_section_m9(exe, B5.L4.R_VERSION, 8))[0]
    assert version == L.VERSION_DEV, f"version {version:#x} != 0x01000002"
    assert version > L8.VERSION_U64_DEV1, "la monotonie R10 est rompue"
    assert version >= L8.VERSION_U64_MIN, "le plancher R10 est franchi"
    # R_POLITIQUE @0x3860 : l'état image reste 0 (héritage)
    politique = struct.unpack("<Q", tranche_section_m9(exe, B5.L.R_POLITIQUE, 8))[0]
    assert politique == 0, "R_POLITIQUE divergente (R7)"
    # Les fixtures .rdata du domaine M8 : concordance exacte (héritage 0.9.0)
    assert tranche_section_m9(exe, L8.R_SYS_NOM, L8.LEN_SYS_NOM) == L8.TXT_SYS_NOM
    assert tranche_section_m9(exe, L8.R_SYS_LIGNE, L8.LEN_SYS_LIGNE + 1) == \
        L8.TXT_SYS_LIGNE
    # K[64] : la réserve .rdata ÉPUISÉE par la table de SHA-256 (FIPS 180-4)
    assert tranche_section_m9(exe, L.R_K, 256) == struct.pack("<64I", *L.K), \
        "la table K[64] @0x2F00 divergente"
    # La porte M5 : UNE entrée, la somme recalculée == la somme portée
    r, t, s = struct.unpack("<IIQ", tranche_section_m9(exe, B5.L.R_TAB_SUM_M5, 16))
    assert (r, t) == (B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE), "l'entrée M5 divergente"
    assert s == _somme_qwords(tranche_section_m9(exe, r, t)), \
        "porte M5 : la somme de .text4 divergente"
    # La porte héritée R10 : la marche complète (28 entrées) auto-consistante
    k = 0
    rva_table = B5.L4.R_TAB_SUM
    while rva_table + 16 * k < B5.L4.R10_BORNE:
        r2, t2, s2 = struct.unpack("<IIQ",
                                   tranche_section_m9(exe, rva_table + 16 * k, 16))
        assert r2 != 0 and t2 != 0, \
            f"porte R10 : entrée #{k + 1} trouée (fail-closed D95)"
        assert s2 == _somme_qwords(tranche_section_m9(exe, r2, t2)), \
            f"porte R10 : somme de {r2:#x} divergente"
        k += 1
        assert k <= B5.L4.R10_NB_ENTREES, "porte R10 : borne franchie"
    assert k == B5.L4.R10_NB_ENTREES, f"porte R10 : {k} entrées != 28"
    # .text5 : les slots du SOCLE == les blobs assemblés (la composition
    # relue ; les slots sys-01..03 sont couverts par la preuve R7), la réserve
    # [0xA840, 0xBFFF) demeure int3
    for bid, _sid, _f, rva, slot in BLOCS_SOCLE:
        assert tranche_section_m9(exe, rva, slot) == code_sys[bid]["slot"], \
            f"le slot {bid} de .text5 diverge du blob assemblé"
    assert all(b == 0xCC for b in tranche_section_m9(
        exe, 0xA840, 0xC000 - 0xA840)), \
        "la réserve .text5 [0xA840, 0xBFFF) n'est pas int3"
    # .text6 : LA COMPOSITION INTÉGRALE — chaque octet compté : les 28 slots
    # == les blobs, les fixtures == les valeurs dérivées, le reste int3
    occupe = bytearray(TEXT6_VSIZE)
    for bid, _sid, _f, rva, slot in BLOCS_TLS13:
        tranche = tranche_section_m9(exe, rva, slot)
        assert tranche == code_tls13[bid]["slot"], \
            f"le slot {bid} de .text6 diverge du blob assemblé"
        occupe[rva - TEXT6_VA: rva - TEXT6_VA + slot] = b"\x01" * slot
    for rva_f, octets_f, _nom_f in fixtures_text6():
        tranche = tranche_section_m9(exe, rva_f, len(octets_f))
        assert tranche == octets_f, \
            f"le fixture @{rva_f:#x} diverge de la valeur dérivée du plan"
        occupe[rva_f - TEXT6_VA: rva_f - TEXT6_VA + len(octets_f)] = \
            b"\x01" * len(octets_f)
    libres = [i for i in range(TEXT6_VSIZE) if not occupe[i]]
    for i in libres:
        assert exe[TEXT6_FILE + i] == 0xCC, \
            f".text6 @{TEXT6_VA + i:#x} hors slot/fixture != int3 " \
            f"(la composition intégrale : chaque octet compté)"
    return True


# --- Preuve de réutilisation (R7 — l'héritage 0.9.0) -------------------------------

def preuve_reutilisation_m9(exe: bytes) -> dict:
    """proxy.exe M9 partage son squelette avec le scellé 0.9.0 : .text/
    .text2/.data/.text3/.text4 OCTET POUR OCTET ; .rdata identique SAUF la
    version @0x2820 (LE delta R10 documenté — geste de BUILD) et K[64]
    @0x2F00-0x2FFF (la réserve VIERGE vérifiée du scellé, ÉPUISÉE par la
    table) ; .text5 : sys-01..03 intacts + le socle socket dans la réserve
    int3 VÉRIFIÉE du scellé ; .text6 NOUVELLE. Les deltas PE documentés."""
    with open(os.path.join(M8_DIR, "proxy.exe"), "rb") as f:
        scelle = f.read()
    if hashlib.sha256(scelle).hexdigest() != SHA_PROXY_090:
        raise EchecBuild("m8/proxy.exe diverge du scellé 0.9.0 (1492b0bc…) — "
                         "l'ancre R7 de l'ère M9 est rompue")
    for nom, rva_base, vsize, fichier in (
            (".text", B5.L.TEXT_RVA, B5.L.TEXT_VSIZE, B5.L.TEXT_FILE),
            (".text2", B5.L.TEXT2_RVA, B5.L.TEXT2_VSIZE, B5.L.TEXT2_FILE),
            (".data", B5.L.DATA_RVA, B5.L.DATA_RAW, B5.L.DATA_FILE),
            (".text3", B5.L.TEXT3_RVA, B5.L.TEXT3_VSIZE, B5.L.TEXT3_FILE),
            (".text4", B5.L.TEXT4_RVA, B5.L.TEXT4_VSIZE, B5.L.TEXT4_FILE)):
        section = tranche_section_m9(exe, rva_base, vsize)
        scelle_section = scelle[fichier: fichier + vsize]
        if section != scelle_section:
            for k, (x, y) in enumerate(zip(section, scelle_section)):
                if x != y:
                    raise EchecBuild(f"R7 rompu : {nom} diverge du scellé "
                                     f"0.9.0 à l'octet {k:#x}")
    # .rdata : identique SAUF la version (LE delta documenté) et K[64]
    # (la réserve ÉPUISÉE — la zone était VIERGE dans le scellé)
    for debut, fin in ((0x2000, B5.L4.R_VERSION),
                       (B5.L4.R_VERSION + 8, L.R_K)):
        if tranche_section_m9(exe, debut, fin - debut) != \
                scelle[B5.L.RDATA_FILE + (debut - 0x2000):
                       B5.L.RDATA_FILE + (debut - 0x2000) + (fin - debut)]:
            raise EchecBuild(f"R7 rompu : .rdata diverge du scellé 0.9.0 "
                             f"entre {debut:#x} et {fin:#x} (hors version/K)")
    if any(scelle[B5.L.RDATA_FILE + (L.R_K - 0x2000):
                  B5.L.RDATA_FILE + 0x1000]):
        raise EchecBuild("R7 rompu : la réserve .rdata 0x2F00-0x2FFF n'est "
                         "pas vierge dans le scellé 0.9.0 — l'ancre de "
                         "l'ère M9 est fausse")
    if tranche_section_m9(exe, L.R_K, 256) != struct.pack("<64I", *L.K):
        raise EchecBuild("R7 rompu : la réserve .rdata ne porte pas "
                         "exactement K[64] (FIPS 180-4 § 4.2.2)")
    # .text5 : sys-01..03 INTACTS, le socle dans la réserve int3 du scellé,
    # la réserve [0xA840, 0xBFFF) int3 DES DEUX côtés
    if tranche_section_m9(exe, L8.TEXT5_VA, 0xA240 - L8.TEXT5_VA) != \
            scelle[L8.TEXT5_FILE: L8.TEXT5_FILE + (0xA240 - L8.TEXT5_VA)]:
        raise EchecBuild("R7 rompu : .text5 [0xA000, 0xA240) (sys-01..03) "
                         "diverge du scellé 0.9.0")
    if not all(b == 0xCC for b in scelle[L8.TEXT5_FILE + (0xA240 - L8.TEXT5_VA):
                                         L8.TEXT5_FILE + (0xA840 - L8.TEXT5_VA)]):
        raise EchecBuild("R7 rompu : la réserve .text5 [0xA240, 0xA840) n'est "
                         "pas int3 dans le scellé 0.9.0 — l'ancre est fausse")
    if not all(b == 0xCC for b in tranche_section_m9(exe, 0xA840, 0xC000 - 0xA840)):
        raise EchecBuild("R7 rompu : la réserve .text5 [0xA840, 0xBFFF) n'est "
                         "pas int3 dans l'image M9")
    # les deltas PE documentés
    pe_m9 = pefile.PE(data=exe)
    pe_s = pefile.PE(data=scelle)
    assert pe_m9.FILE_HEADER.NumberOfSections == 8
    assert pe_s.FILE_HEADER.NumberOfSections == 7
    assert pe_m9.OPTIONAL_HEADER.SizeOfImage == 0x11000
    assert pe_s.OPTIONAL_HEADER.SizeOfImage == 0xC000
    assert pe_m9.OPTIONAL_HEADER.AddressOfEntryPoint == \
        pe_s.OPTIONAL_HEADER.AddressOfEntryPoint == B5.L.ENTREE_M5
    return {"sha_proxy_090": SHA_PROXY_090,
            "blocs_reutilises": len(B8.BLOCS_EMBARQUES_M8)}       # 55


# --- Carte génération 9 : tables, fragments, verrou croisé (modèle D104/D144) -----

TOUS_BLOCS_M9 = B8.TOUS_BLOCS + [b[0] for b in BLOCS_SOCLE] \
    + [b[0] for b in BLOCS_TLS13]                                 # 86 (gén. 9)
CONTRATS_M9: dict = {}   # posé par construire()/verifier() (contrats_m9)
RVA_PAR_BLOC = dict(B8.RVA_PAR_BLOC) \
    | {b[0]: b[3] for b in BLOCS_SOCLE + BLOCS_TLS13}
SPEC_PAR_BLOC = dict(B8.SPEC_PAR_BLOC) \
    | {b[0]: b[1] for b in BLOCS_SOCLE + BLOCS_TLS13}
EXE_PAR_BLOC = dict(B8.EXE_PAR_BLOC) \
    | {b[0]: "proxy" for b in BLOCS_SOCLE + BLOCS_TLS13}
ROLES = dict(B8.ROLES) | {b[0]: b[2] for b in BLOCS_TLS13}
FICH_PAR_BID = dict(B8.FICH_PAR_BID) \
    | {b[0]: b[2] for b in BLOCS_SOCLE + BLOCS_TLS13}
EMBARQUES_M9 = B8.EMBARQUES | {b[0] for b in BLOCS_SOCLE + BLOCS_TLS13}
BLOCS_EMBARQUES_M9 = B8.BLOCS_EMBARQUES_M8 + BLOCS_SOCLE + BLOCS_TLS13


def contrats_m9(specs: dict) -> dict:
    """Les contrats des 31 blocs nouveaux — PARSÉS des spécifications I
    (la couche I est la source, R2 : jamais une copie d'écriture)."""
    contrats = {}
    for bid, sid, fichier, _rva, _slot in BLOCS_SOCLE + BLOCS_TLS13:
        spec = specs[bid]
        chemin_asm = chemin_notation(M8_DIR if bid.startswith("g9") else ICI,
                                     fichier)
        contrats[bid] = (spec["nom"], spec["pre"], spec["post"], spec["inv"],
                         deps_notation(chemin_asm))
    return contrats


_ZONES_CARTE_M9 = ("[zones] io=0x1000-0x10ff libc=0x1100-0x143f app=0x1800-0x1fff "
                   "net=0x4000-0x42ff cli=0x4400-0x45bf thr=0x4300-0x43ff "
                   "srv=0x4b00-0x4bff http=0x4c00-0x5e7f "
                   "tls=0x6000-0x733f revisions=0x7340-0x7fbf reserve-t3=0x7fc0-0x7fff "
                   "revisions-m5=0x8000-0x8fbf reserve-t4=0x8fc0-0x9fff "
                   "sys=0xa000-0xa83f reserve-t5=0xa840-0xbfff "
                   "tls13=0xc000-0x10aff socle-28=0x10d00-0x10daf "
                   "fixtures-x25519=0xff00-0xff3f "
                   "fixtures-poignee=0x10b80-0x10c1f "
                   "fixtures-transport=0x10c20-0x10cef "
                   "marge-t6=0x10b00-0x10b7f reserve-t6=0x10db0-0x10fff "
                   "reserve-libc=0x1440-0x17ff (int3 defensif)")


def fragments_clairs_m9(exe: bytes, verrous_m3: list, verrous_m4: list,
                        verrous_m5: list, verrous_m8: list,
                        verrous_socle: list, verrous_tls13: list,
                        version: str, verdict_m4: dict, verdict_m5: dict,
                        verdict_sys: dict, compteurs: dict,
                        journal_runs: list[str]) -> dict[str, bytes]:
    sha = lambda b: "sha256:" + hashlib.sha256(b).hexdigest()

    loc = ["[carte-frag] nom=frag-loc generation=10", _ZONES_CARTE_M9]
    for bid in TOUS_BLOCS_M9:
        loc.append(f"[bloc] id={bid} spec={SPEC_PAR_BLOC[bid]} cible=x86-64-win11-pe "
                   f"exe={EXE_PAR_BLOC[bid]} addr={B5.L.IMAGE_BASE + RVA_PAR_BLOC[bid]:#x} "
                   f"v=1 etat=scelle role={ROLES[bid]}")

    con = ["[carte-frag] nom=frag-con generation=10"]
    for bid in TOUS_BLOCS_M9:
        sig, pre, post, inv, deps = (CONTRATS_M9[bid] if bid in CONTRATS_M9
                                     else B8.CONTRATS[bid])
        con += [f"[bloc] id={bid}", f"  sig : {sig}", f"  pre : {pre}",
                f"  post : {post}", f"  inv : {inv}", f"  deps : {deps}"]

    prf = ["[carte-frag] nom=frag-prf generation=10"]
    for bid in TOUS_BLOCS_M9:
        chemin_asm = _chemin_notation_bid_m9(bid)
        with open(chemin_asm, "rb") as f:
            empreinte_notation = sha(f.read())
        crist = min(compteurs.get(bid, 1), 10)
        prf += [
            f"[bloc] id={bid} etat={'cristallise' if crist >= 10 else 'scelle'} crist={crist}/10",
            f"  vecteurs : roundtrip=ok structure=ok notation={empreinte_notation}",
        ]
    prf.append("[verifications] runs=" + str(len(journal_runs)))
    prf += ["  " + r for r in journal_runs[-12:]]

    bld = ["[carte-frag] nom=frag-bld generation=10"]
    for bid in TOUS_BLOCS_M9:
        rva = RVA_PAR_BLOC[bid]
        if bid in EMBARQUES_M9:
            slot = next(s for b, _sid, _f, _r, s in BLOCS_EMBARQUES_M9 if b == bid)
            empreinte = sha(tranche_section_m9(exe, rva, slot))
        else:
            with open(_chemin_notation_bid_m9(bid), "rb") as f:
                empreinte = "notation:" + sha(f.read())[7:]
        bld.append(f"[bloc] id={bid} addr={B5.L.IMAGE_BASE + rva:#x} empreinte={empreinte}")
    bld += [
        f"[build] artefact=proxy.exe version={version} profil=x86-64-win11-pe "
        f"taille={len(exe)} empreinte={sha(exe)}",
        f"  outils : keystone-engine + capstone {capstone.cs_version()[0]}.{capstone.cs_version()[1]} ; "
        f"verrous structurels : M3 {len(verrous_m3)} + M4 {len(verrous_m4)} + M5 {len(verrous_m5)} "
        f"+ M8 {len(verrous_m8)} + socle {len(verrous_socle)} + tls13 {len(verrous_tls13)} ; "
        f"oracles : M4 (heritage rejoue) {verdict_m4.get('total_cas', 0)} cas "
        f"+ M5 (scenarios etendus D136) {verdict_m5.get('total_cas', 0)} cas + sys (domaine sys "
        f"+ socle socket M9-(d), fixtures ntdll/AFD synthetiques) "
        f"{verdict_sys.get('total_cas', 0)} cas, "
        f"graine={verdict_sys.get('graine', '-')}, volume={verdict_sys.get('volume', '-')}",
        f"  heritage : proxy.exe 0.9.0 scelle (1492b0bc...) repris octet pour octet "
        f"(R7 : .text/.text2/.text3/.text4/.data intacts, .rdata identique SAUF la "
        f"version @0x2820 = 0x01000002 [LE delta R10 — geste de BUILD, jamais "
        f"scellage : la 1.0.0 finale attend le terrain vert du chantier (f)] et la "
        f"table K[64] @0x2F00-0x2FFF dans la reserve .rdata M8 VIERGE VERIFIEE "
        f"[EPUISSEE par la table de SHA-256 de tls13-02, FIPS 180-4 § 4.2.2] ; "
        f".text5 : sys-01..03 intacts + LE SOCLE SOCKET sys-04 @0xA240/0x300, "
        f"sys-05 @0xA540/0x180, sys-06 @0xA6C0/0x180 dans la reserve int3 "
        f"VERIFIEE du scelle, la reserve [0xA840, 0xBFFF) demeurant int3 ; "
        f"section .text6 NOUVELLE [0xC000-0x10FFF : les 28 blocs tls13 "
        f"0xC000..0x10B00 — l'erratum n° 5 : l'octet de longueur du record CH "
        f"[0x76 → 0x72 : la sonde terrain du 06/11 a prouvé le SILENCE des "
        f"serveurs réels sur le vol 0x76] + LE CCS HÉRITÉ AVALÉ [RFC 8446 "
        f"§ 4.1.3 : la même sonde l'a constaté chez google/github/cloudflare/"
        f"debian TOUS — l'enregistrement 14 03 03 00 01 01 avalé SANS "
        f"déverrouillage] + les verdicts internes EN 64 BITS [mov rax, la "
        f"frontière du kit] — le principal ré-arrêté 0xBC0, le socle tls13-28 "
        f"DEPLACE 0x10AC0 → 0x10D00 APRÈS les fixtures, les 26 autres blocs "
        f"byte-identiques, le harnais poignee re-joue VERT 54/54 × 3 graines "
        f"— + les fixtures (U9/EXP_INV @0xFF00/0xFF20, "
        f"les HUIT libelles du calendrier + HRR @0x10B80..0x10BF0, les fixtures "
        f"du transport AFD @0x10C20..0x10CF0)] ; PE : 8 sections, SizeOfImage "
        f"0x11000, taille 0xFE00, en-tetes <= 0x400 AUCUN decalage (le modele "
        f"D94 n'est pas rejoue) ; entree PE 0x8C80 INCHANGEE ; AUCUN import "
        f"nouveau (le socket natif SANS une seule entree d'import reseau : "
        f"ws2_32 n'est JAMAIS importe PAR LES BLOCS NOUVEAUX — l'heritage "
        f"M4/M5 tls-04 Schannel demeure, R7) ; les 44 blocs heritages "
        f"embarques octet-identiques ; hello.exe 0.1.0 + selftest.exe 0.2.0 + "
        f"echo.exe 0.3.0 + proxy.exe 0.4.0/0.5.1/0.6.0/0.9.0 (lignees "
        f"D74/D80/D144) inchanges",
        _ZONES_CARTE_M9,
    ]

    retour = {}
    for nom, lignes in (("frag-loc", loc), ("frag-con", con), ("frag-prf", prf), ("frag-bld", bld)):
        retour[nom] = ("\n".join(lignes) + "\n").encode("utf-8", errors="replace")
    return retour


def _chemin_notation_bid_m9(bid: str) -> str:
    """Notation d'un bloc indexé par la carte : le routeur M9 (les nouveaux
    par leurs répertoires), l'héritage via le routeur M8 (une seule source
    de vérité du routage par ère)."""
    if bid in {b[0] for b in BLOCS_SOCLE + BLOCS_TLS13}:
        return chemin_notation(M8_DIR if bid.startswith("g9") else ICI,
                               FICH_PAR_BID[bid])
    return B8._chemin_notation_bid(bid)


def construire_carte_m9(exe, verrous_m3, verrous_m4, verrous_m5, verrous_m8,
                        verrous_socle, verrous_tls13, version, verdict_m4,
                        verdict_m5, verdict_sys, compteurs, journal_runs):
    phrase, _ = cm9.charger_secrets(interactif=False)
    maitre = cm9.cle_maitresse(phrase)
    clairs = fragments_clairs_m9(exe, verrous_m3, verrous_m4, verrous_m5,
                                 verrous_m8, verrous_socle, verrous_tls13,
                                 version, verdict_m4, verdict_m5, verdict_sys,
                                 compteurs, journal_runs)
    fragments = {n: cm9.chiffrer_fragment(maitre, n, clairs[n]) for n in cm9.FRAGMENTS}
    racine = cm9.empreinte_racine(fragments)
    entete = cm9.construire_entete(racine, version)
    prive, pub = cm9.paire_cles(cm9.charger_secrets(interactif=False)[1])
    signature = cm9.signer(prive, entete, fragments)
    cm9.ecrire_carte(entete, fragments, signature, pub)
    return pub


# --- Verrou croisé (R8 : relecture indépendante) -----------------------------------

def verrou_croise_m9() -> tuple[int, dict]:
    phrase, _ = cm9.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm9.lire_carte()
    cm9.verifier_listes_blanches(entete.decode("ascii"))
    cm9.verifier_signature(pub, entete, fragments, signature)
    if cm9.empreinte_racine(fragments).hex() not in entete.decode("ascii"):
        raise cm9.ErreurCarte("empreinte racine divergente")
    maitre = cm9.cle_maitresse(phrase)
    bld = cm9.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    empreintes, manifestes = {}, []
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[champs["id"]] = champs["empreinte"]
        elif ligne.startswith("[build]"):
            manifestes.append(dict(re.findall(r"(\w+)=(\S+)", ligne)))
    manifeste = next((m for m in manifestes if m.get("artefact") == "proxy.exe"), {})
    for bid, _sid, _f, rva, slot in BLOCS_EMBARQUES_M9:
        sha = "sha256:" + hashlib.sha256(tranche_section_m9(exe, rva, slot)).hexdigest()
        if sha != empreintes.get(bid):
            raise cm9.ErreurCarte(f"verrou croisé : empreinte de {bid} divergente (R8)")
    sha_exe = "sha256:" + hashlib.sha256(exe).hexdigest()
    if sha_exe != manifeste.get("empreinte"):
        raise cm9.ErreurCarte("verrou croisé : empreinte de proxy.exe divergente (R8)")
    return len(empreintes), manifeste


# --- Tableau de bord (§ 15.2, métriques M9) ------------------------------------------

def _ligne_preversions_m9(version: str) -> str:
    if re.fullmatch(r"\d+\.\d+\.\d+", version):
        return (f"  preversions                   : {version} SCELLÉE sur le "
                "recoup terrain M9-(f) VERT (le fait de carte D104 ; monotonie "
                "R10 : 0x01000002 > 0x01000001 > 0x00090001 tenue)")
    return (f"  preversions                   : {version} conforme "
            f"(schema dev, monotonie R10 : 0x01000002 > 0x00090001 — la finale "
            f"1.0.0 attend le terrain vert du chantier (f), jamais un scellage ici)")


def tableau_de_bord_m9(exe: bytes, verrous_m3: list, verrous_m4: list,
                       verrous_m5: list, verrous_m8: list, verrous_socle: list,
                       verrous_tls13: list, nb_blocs_carte: int,
                       manifeste: dict, verdict_m4: dict, verdict_m5: dict,
                       verdict_sys: dict) -> str:
    sha = lambda b: hashlib.sha256(b).hexdigest()
    lignes = [
        "[tableau] jalon=M9 artefact=proxy.exe version=" + manifeste.get("version", "?"),
        f"  blocs_avec_spec_a_jour        : {nb_blocs_carte}/86 : audit de tracabilite I->C->B (8 artefacts)",
        f"  chaines_I_C_B_tests           : {nb_blocs_carte}/{nb_blocs_carte} : specs, carte, exe, vecteurs",
        f"  construction                  : 0 erreur / 0 avertissement : build script",
        f"  tests_differentiels           : oracle M4 (heritage rejoue) {verdict_m4.get('total_cas', 0)} cas verts "
        f"+ oracle M5 (scenarios etendus D136) {verdict_m5.get('total_cas', 0)} cas verts "
        f"+ harnais sys (domaine sys + socle socket AFD M9-(d)) {verdict_sys.get('total_cas', 0)} "
        f"cas verts ({verdict_sys.get('volume', '-')}, graine {verdict_sys.get('graine', '-')}) ; "
        f"oracle structurel M3 {len(verrous_m3)} + M4 {len(verrous_m4)} + M5 {len(verrous_m5)} "
        f"+ M8 {len(verrous_m8)} + socle {len(verrous_socle)} + tls13 {len(verrous_tls13)} "
        f"verrous PASS (LA RÈGLE AUCUN IAT PAR BLOC tls13 + LES SLOTS DISJOINTS "
        f"— l'erratum n° 4 : le contrôle qui nomme) ; le domaine tls13 prouvé "
        f"bloc par bloc aux gestes de notation (six harnais, 282 contrôles "
        f"× 3 graines)",
        f"  reutilisation_heritage        : 44 blocs embarques octet-identiques au scelle 0.9.0 "
        f"(R7, deltas .rdata [version + K[64] dans la reserve VIERGE VERIFIEE]/"
        f".text5 [le socle socket dans la reserve int3]/.text6 NOUVELLE/PE "
        f"documentes — version 0x01000002 : geste de BUILD [l'erratum n° 5]),",
        f"  empreintes_donnees_embarquees : conforme (fixtures http + tls + CLI/flux M5 "
        f"+ span-nom/fixture-ligne M8 + K[64] @0x2F00 + les fixtures .text6 "
        f"[U9/EXP_INV, les HUIT libelles + HRR, le transport AFD], table R10 "
        f"28 entrees archee, porte M5, version {L.VERSION_DEV:#x})",
        f"  defauts_T1_T6_ouverts         : 0 : journal des decisions D77-D177 "
        f"(l'erratum n° 4 NOMME et REPARE : tls13-28 deplace 0x10AC0, le "
        f"controle slots-disjoints PERMANENT)",
        f"  optimisations_sans_mesure     : 0 : aucune optimisation M9 (R11)",
        f"  changements_hors_journal      : 0 : D77 a D177 consignees",
        _ligne_preversions_m9(manifeste.get("version", "?")),
        f"  entrees_non_fiables           : comportement defini par contrat (les HUIT "
        f"verdicts nommes du domaine sys ET du domaine tls13 [V_TRANSPORT_ECHEC "
        f"-7 a M9-(d)], le NTSTATUS jamais muet, l'echec de resolution "
        f"= AUCUN syscall emis) ; falsification : les six harnais du domaine "
        f"(zéro silence — chaque mutation attrapee)",
        f"  artefact                      : {len(exe)} octets ; empreinte sha256:{sha(exe)[:16]}... ; "
        f"8 sections (.text6 nouvelle 0xC000 — le domaine tls13 + les fixtures) ; "
        f"AUCUN import nouveau (le socket natif SANS une seule entree d'import "
        f"reseau — la preuve structurelle : le domaine ne declare RIEN) ; "
        f"entree PE 0x8C80 inchangee",
        f"  verrou_croise                 : {nb_blocs_carte} empreintes reverifiees "
        f"(8 artefacts + notations non embarquees) + signature Ed25519 (graine "
        f"durable D144, pub e9cd8c549485... — le temoin ne bouge pas) + racine (R8/R9)",
    ]
    return "\n".join(lignes) + "\n"


# --- Anti-rollback (R6) ---------------------------------------------------------------

def _anti_rollback_m9() -> None:
    """Une carte scellée (rc/finale) interdit la reconstruction (R6). La
    1.0.0-dev.1 n'est PAS scellée (schéma dev — la finale 1.0.0 attend le
    terrain vert du chantier (f)) : la reconstruction de dev est licite
    (cristallisation R6 au fil des vérifications)."""
    try:
        _, fragments, _, _ = cm9.lire_carte()
        phrase, _ = cm9.charger_secrets(interactif=False)
        maitre = cm9.cle_maitresse(phrase)
        bld = cm9.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
        version_existante = next(
            (dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
             if "artefact=proxy.exe" in l), None)
        if version_existante and ("-rc" in version_existante
                                  or re.fullmatch(r"\d+\.\d+\.\d+", version_existante)):
            raise EchecBuild(
                f"carte scellée ({version_existante}) : reconstruction interdite — "
                f"procedure lourde R6 ou nouvelle version X.Y.Z+1 requise")
    except (cm9.ErreurCarte, FileNotFoundError):
        pass  # pas de carte lisible : première construction


def verifier_carte_possible_m9() -> str:
    """-> le motif : 'cérémonie requise' (secrets absents) ou 'prête'."""
    chemin_phrase = os.path.join(TRIADE, ".keys", "passphrase.txt")
    chemin_graine = os.path.join(TRIADE, ".keys", "ed25519.seed")
    if not os.path.exists(chemin_phrase) or not os.path.exists(chemin_graine):
        return ("cérémonie requise (D144) : relève au coffre — phrase = entrée "
                "lignee-D80, graine = entrée graine-ed25519-cartes")
    return "prête (lignée D80 + graine durable D144)"


# --- Modes -----------------------------------------------------------------------------

def construire(volume: str, graine: int) -> int:
    print("=== M9 : chaîne artefact TRIADE (profil x86-64-win11-pe, 1.0.0-dev.1) ===")
    _anti_rollback_m9()
    _garde_sceau_I()

    # 1. L'héritage M3+M4+M5+M8 re-vérifié de bout en bout, la preuve R7
    #    (l'ancre : le scellé 0.9.0 confronté à la recomposition)
    h9 = heritage_complet_m9()
    h = h9["h"]
    specs = charger_couche_I_m9()

    # 2. Le socle socket (sys-04..06) : assemblage + oracle structurel
    code_sys = assembler_blocs(BLOCS_SOCLE, M8_DIR, specs)
    for bid, *_ in B8.BLOCS_M8:
        code_sys[bid] = h9["code_m8"][bid]        # sys-01..03 (l'héritage 0.9.0)
    verrous_socle = oracle_structurel_m9(
        specs, code_sys, BLOCS_SOCLE, APPELS_FERMES_SOCLE,
        DONNEES_RIP_SOCLE, "socle", convention_64=True)
    print(f"[oracle] structurel socle : {len(verrous_socle)} verrous PASS "
          f"(la séquence create→bind→connect, les fixtures .text6 cités, "
          f"la convention M8 multiple-de-64 tenue)")

    # 3. Les 28 blocs tls13 : assemblage + oracle structurel (LA RÈGLE du
    #    domaine : AUCUN IAT, AUCUN syscall, le jeu fermé, LES SLOTS DISJOINTS)
    code_tls13 = assembler_blocs(BLOCS_TLS13, ICI, specs)
    verrous_tls13 = oracle_structurel_m9(
        specs, code_tls13, BLOCS_TLS13, APPELS_FERMES_TLS13,
        DONNEES_RIP_TLS13, "tls13")
    print(f"[oracle] structurel tls13 : {len(verrous_tls13)} verrous PASS "
          f"(LA RÈGLE AUCUN IAT PAR BLOC tls13 + LES SLOTS DISJOINTS — "
          f"l'erratum n° 4 : le contrôle qui nomme)")

    # 4. Composition de l'image M9 (deltas documentés + .text6)
    global CONTRATS_M9
    CONTRATS_M9 = contrats_m9(specs)
    sections = composer_image_m9(h9["sections_m8"], code_sys, code_tls13)
    exe = ecrire_pe32plus(*sections)
    valider_pe_m9(exe, code_sys, code_tls13)
    print(f"[PE] proxy.exe : {len(exe)} octets, 8 sections (.text5 0xA000 — le "
          f"domaine sys : les SIX blocs + la réserve int3 ; .text6 0xC000 "
          f"NOUVELLE — le domaine tls13 : les 28 blocs + les fixtures), "
          f"AUCUN import nouveau, entrée {B5.L.ENTREE_M5:#x} inchangée (R7)")

    # 5. Preuve R7 (l'héritage 0.9.0)
    heritage = preuve_reutilisation_m9(exe)
    print(f"[R7] réutilisation : {heritage['blocs_reutilises']} blocs "
          f"octet-identiques au scellé 0.9.0, deltas .rdata/.text5/.text6/PE "
          f"documentés (version 0x01000002 : geste de BUILD, jamais scellage)")

    # 6. Les oracles : l'héritage M4 puis M5 PUIS le domaine sys au complet
    #    (le socle socket compris — les blobs du build)
    blobs_m4 = B4.blobs_oracle(h["code_m3"], h["code_m4"])
    verdict_m4 = B4.od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} cas verts")
    blobs_m5 = B5.blobs_oracle(h["code_m3"], h["code_m4"], h["code_m5"])
    verdict_m5 = B5.od5.executer(blobs_m5, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 (héritage) : {verdict_m5['total_cas']} cas verts")
    blobs_sys = {_CLE_BLOB_SYS[bid]: code_sys[bid]["octets"]
                 for bid in _CLE_BLOB_SYS}
    verdict_sys = harnais.executer(blobs_sys, graine=graine, volume=volume)
    print(f"[oracle] harnais sys (le domaine + le socle socket) : "
          f"{verdict_sys['total_cas']} cas verts")

    # 7. Écriture de l'artefact
    with open(os.path.join(ICI, "proxy.exe"), "wb") as f:
        f.write(exe)

    # 8. Carte génération 9 (lignée D80, graine durable D144) + verrou croisé
    #    + tableau de bord — le scellage est un fait de carte (D104) et il
    #    N'AURA PAS LIEU ici (la 1.0.0 attend le terrain vert du chantier (f))
    version = cm9.VERSION_DEV1
    compteurs = {bid: 1 for bid in TOUS_BLOCS_M9}
    journal = [f"run graine={graine} volume={volume} "
               f"verdict-m4={verdict_m4['empreinte']} verdict-m5={verdict_m5['empreinte']} "
               f"verdict-sys={verdict_sys['empreinte']} "
               f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"build={version}"]
    construire_carte_m9(exe, h["verrous_m3"], h["verrous_m4"], h["verrous_m5"],
                        h9["verrous_m8"], verrous_socle, verrous_tls13,
                        version, verdict_m4, verdict_m5, verdict_sys,
                        compteurs, journal)
    print(f"[carte] génération 11 écrite (lignée D80, graine durable D144) : "
          f"4 fragments chiffrés, signature Ed25519, {len(TOUS_BLOCS_M9)} blocs "
          f"indexés sur 8 artefacts")
    nb, manifeste = verrou_croise_m9()
    print(f"[R8] verrou croisé : signature OK, racine OK, {nb} empreintes "
          f"revérifiées, artefact {manifeste.get('version')}")
    with open(os.path.join(cm9.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord_m9(exe, h["verrous_m3"], h["verrous_m4"],
                                   h["verrous_m5"], h9["verrous_m8"],
                                   verrous_socle, verrous_tls13, nb, manifeste,
                                   verdict_m4, verdict_m5, verdict_sys))
    print("[tableau] tableau de bord écrit (carte/tableau-de-bord.txt)")
    print(f"[B] proxy.exe {manifeste.get('version')} : "
          f"sha256:{hashlib.sha256(exe).hexdigest()}")
    print(f"=== M9-dev (oracle vert) : {version} — le domaine tls13 composé sur "
          f"le corps 0.9.0 INTACT (R7), le socle socket dans la réserve .text5, "
          f"les 28 blocs + les fixtures en .text6 NOUVELLE, carte génération 11 "
          f"vivante ; le chantier (f) (le terrain — LA GRANDE ŒUVRE : la "
          f"session RÉELLE) attend ; la finale 1.0.0 attend le terrain vert ===")
    return 0


def verifier(volume: str, graine: int) -> int:
    print(f"=== M9 : re-vérification complète (R5/R7, graine {graine}) ===")
    _garde_sceau_I()
    h9 = heritage_complet_m9()
    h = h9["h"]
    specs = charger_couche_I_m9()
    code_sys = assembler_blocs(BLOCS_SOCLE, M8_DIR, specs)
    for bid, *_ in B8.BLOCS_M8:
        code_sys[bid] = h9["code_m8"][bid]
    verrous_socle = oracle_structurel_m9(
        specs, code_sys, BLOCS_SOCLE, APPELS_FERMES_SOCLE,
        DONNEES_RIP_SOCLE, "socle")
    code_tls13 = assembler_blocs(BLOCS_TLS13, ICI, specs)
    verrous_tls13 = oracle_structurel_m9(
        specs, code_tls13, BLOCS_TLS13, APPELS_FERMES_TLS13,
        DONNEES_RIP_TLS13, "tls13")
    global CONTRATS_M9
    CONTRATS_M9 = contrats_m9(specs)
    with open(os.path.join(ICI, "proxy.exe"), "rb") as f:
        exe = f.read()
    heritage = preuve_reutilisation_m9(exe)
    print(f"[R7] {heritage['blocs_reutilises']} blocs réutilisés du scellé "
          f"0.9.0, deltas documentés")
    valider_pe_m9(exe, code_sys, code_tls13)
    blobs_m4 = B4.blobs_oracle(h["code_m3"], h["code_m4"])
    verdict_m4 = B4.od4.executer(blobs_m4, graine=graine, volume=volume)
    print(f"[oracle] différentiel M4 (héritage) : {verdict_m4['total_cas']} cas verts")
    blobs_m5 = B5.blobs_oracle(h["code_m3"], h["code_m4"], h["code_m5"])
    verdict_m5 = B5.od5.executer(blobs_m5, graine=graine, volume=volume)
    print(f"[oracle] différentiel M5 (héritage) : {verdict_m5['total_cas']} cas verts")
    blobs_sys = {_CLE_BLOB_SYS[bid]: code_sys[bid]["octets"]
                 for bid in _CLE_BLOB_SYS}
    verdict_sys = harnais.executer(blobs_sys, graine=graine, volume=volume)
    print(f"[oracle] harnais sys (le domaine + le socle socket) : "
          f"{verdict_sys['total_cas']} cas verts")
    print(f"[PE] proxy.exe re-validé (8 sections, portes R10+M5, version PE "
          f"{L.VERSION_DEV:#x})")

    # Cristallisation R6 : chaque passage incrémente les compteurs — la carte
    # est re-signée à chaque passage (fragments re-chiffrés, graine durable
    # D144), le verrou croisé re-vérifié (R8). La 10/10 sera exigée au
    # scellage de la 1.0.0 (qui attend le terrain vert du chantier (f)).
    phrase, _ = cm9.charger_secrets(interactif=False)
    maitre = cm9.cle_maitresse(phrase)
    _, fragments, _, _ = cm9.lire_carte()
    prf = cm9.dechiffrer_fragment(maitre, "frag-prf", fragments["frag-prf"]).decode("utf-8")
    compteurs, journal = {}, []
    for ligne in prf.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(re.findall(r"(\w+)=(\S+)", ligne))
            m = re.match(r"(\d+)/10", champs.get("crist", "1/10"))
            compteurs[champs["id"]] = int(m.group(1))
        elif ligne.startswith("  run "):
            journal.append(ligne.strip())
    for bid in TOUS_BLOCS_M9:
        compteurs[bid] = min(compteurs.get(bid, 0) + 1, 10)
    journal.append(f"run graine={graine} volume={volume} "
                   f"verdict-m4={verdict_m4['empreinte']} verdict-m5={verdict_m5['empreinte']} "
                   f"verdict-sys={verdict_sys['empreinte']} "
                   f"date={datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")

    bld = cm9.dechiffrer_fragment(maitre, "frag-bld", fragments["frag-bld"]).decode("utf-8")
    manifeste_v = next((dict(re.findall(r"(\w+)=(\S+)", l)).get("version") for l in bld.splitlines()
                        if "artefact=proxy.exe" in l), "?")
    version = manifeste_v if manifeste_v != "?" else cm9.VERSION_DEV1
    construire_carte_m9(exe, h["verrous_m3"], h["verrous_m4"], h["verrous_m5"],
                        h9["verrous_m8"], verrous_socle, verrous_tls13,
                        version, verdict_m4, verdict_m5, verdict_sys,
                        compteurs, journal)
    nb, manifeste = verrou_croise_m9()
    crist = {b: compteurs.get(b, 0) for b, *_ in BLOCS_SOCLE + BLOCS_TLS13}
    affiches = [f"{b}={n}/10" for b, n in list(crist.items())[:6]]
    print("[R6] cristallisation M9 (les 31 nouveaux) : " + ", ".join(affiches) + "…")
    print(f"[R8] verrou croisé : {nb} empreintes conformes ; artefact {manifeste.get('version')}")
    with open(os.path.join(cm9.CARTE_DIR, "tableau-de-bord.txt"), "w", encoding="utf-8") as f:
        f.write(tableau_de_bord_m9(exe, h["verrous_m3"], h["verrous_m4"],
                                   h["verrous_m5"], h9["verrous_m8"],
                                   verrous_socle, verrous_tls13, nb, manifeste,
                                   verdict_m4, verdict_m5, verdict_sys))
    print(f"[carte] génération 9 : {verifier_carte_possible_m9()}")
    return 0


def main() -> int:
    args = sys.argv[1:]
    graine = 20261106
    volume = "complet"
    if "--graine" in args:
        graine = int(args[args.index("--graine") + 1])
    if "--volume" in args:
        volume = args[args.index("--volume") + 1]
    if "--verifier" in args:
        return verifier(volume, graine)
    return construire(volume, graine)


if __name__ == "__main__":
    sys.exit(main())
