#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_specs_m9a.py — LA PREUVE SUR PIÈCES DU CHANTIER M9-(a) COMPLET :
les 28 spécifications présentes ET cohérentes avec le plan d'adressage, les
constantes du plan RE-DÉRIVÉES par arithmétique au geste même (le juge est le
code), la construction du ClientHello re-jouée en Python (114 o), la
disposition de session recomptée. Échec nommé sur toute divergence.

Usage : python3 scripts/verifier_specs_m9a.py
Code de sortie : 0 = 28/28 + constantes VERTES ; 2 = refus nommé."""

import hashlib
import importlib.util
import pathlib
import re
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DOSSIER = REPO / "tls13" / "I"
LAYOUT = REPO / "tls13" / "layout.py"

# La table des 28 (le README fait foi — les identifiants machine h10xxxx sont
# DÉCIMAUX, miroir des g9xxxx du M8 : h100001..h100028)
ATTENDUS = {
    1: "tls13-01-sha256-init.md",
    2: "tls13-02-sha256-comprimer.md",
    3: "tls13-03-sha256-absorber.md",
    4: "tls13-04-sha256-finaliser.md",
    5: "tls13-05-hmac-sha256.md",
    6: "tls13-06-hkdf-extract.md",
    7: "tls13-07-hkdf-expand.md",
    8: "tls13-08-hkdf-expand-label.md",
    9: "tls13-09-f25519-add.md",
    10: "tls13-10-f25519-sub.md",
    11: "tls13-11-f25519-mul.md",
    12: "tls13-12-f25519-propager-geler.md",
    13: "tls13-13-x25519-echelle.md",
    14: "tls13-14-x25519-cle-publique.md",
    15: "tls13-15-aes128-cles-tour.md",
    16: "tls13-16-aes128-bloc.md",
    17: "tls13-17-ghash-multiplication.md",
    18: "tls13-18-gcm-sceller.md",
    19: "tls13-19-gcm-ouvrir.md",
    20: "tls13-20-enregistrement-proteger.md",
    21: "tls13-21-enregistrement-deproteger.md",
    22: "tls13-22-clienthello-composer.md",
    23: "tls13-23-serverhello-traiter.md",
    24: "tls13-24-calendrier-cles.md",
    25: "tls13-25-finished-calculer-verifier.md",
    26: "tls13-26-epinglage.md",
    27: "tls13-27-principal-machine-etats.md",
    28: "tls13-28-socle-appel.md",
}

# La table des blocs machine du README (h100001..h100028, DÉCIMAL)
IDENTIFIANTS = {i: 100000 + i for i in ATTENDUS}

echecs = []


def controle(nom, ok, detail=""):
    print(f"[m9a] {'PASS' if ok else 'ÉCHEC'} : {nom}"
          + (f" ({detail})" if detail else ""))
    if not ok:
        echecs.append(nom)


# --- (1) les 28 fichiers, chaque tête porte son numéro et sa révision --------
for num, nom in sorted(ATTENDUS.items()):
    chemin = DOSSIER / nom
    if not chemin.exists():
        controle(f"tls13-{num:02d} présent ({nom})", False)
        continue
    texte = chemin.read_text(encoding="utf-8")
    tete = texte.splitlines()[0]
    ok_tete = tete.startswith(f"tls13-{num:02d} ·") and "· révision 1" in tete
    ok_sections = all(s in texte for s in ("Intention :", "Contrat :",
                                           "pre  :", "post :", "inv  :"))
    ok_iat = ("AUCUNE entrée IAT" in texte) or ("AUCUN site syscall" in texte)
    controle(f"tls13-{num:02d} ({nom})", ok_tete and ok_sections and ok_iat,
             tete[:60])

# --- (2) le README porte la table des 28 et les identifiants h100xxx ----------
readme = (DOSSIER / "README.md").read_text(encoding="utf-8")
for num in ATTENDUS:
    controle(f"la table porte tls13-{num:02d} → h{IDENTIFIANTS[num]}",
             f"| tls13-{num:02d} | h{IDENTIFIANTS[num]} |" in readme)
controle("le README dit le chantier (a) COMPLET",
         "chantier (a) est\nCOMPLET" in readme or "COMPLET : les 28" in readme)
controle("le README porte l'erratum av-10",
         "Erratum (M9, sur pièces" in readme)

# --- (3) le plan d'adressage : les constantes RE-DÉRIVÉES au geste même -------
spec_mod = importlib.util.spec_from_file_location("layout_m9", LAYOUT)
lay = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(lay)

M51 = (1 << 51) - 1
P = (1 << 255) - 19
membres_p = tuple((P >> (51 * i)) & M51 for i in range(5))
controle("F25519_M51 == 2^51 − 1", lay.F25519_M51 == M51, hex(lay.F25519_M51))
controle("F25519_P_MEMBRES == les membres de p (RE-DÉRIVÉS)",
         lay.F25519_P_MEMBRES == membres_p,
         " · ".join(hex(m) for m in lay.F25519_P_MEMBRES))
controle("le membre 0 a TREIZE chiffres hex (l'erratum)",
         len(hex(lay.F25519_P_MEMBRES[0])[2:]) == 13,
         hex(lay.F25519_P_MEMBRES[0]))
controle("X25519_EXP_INV == p − 2 en 32 o little-endian",
         lay.X25519_EXP_INV == (P - 2).to_bytes(32, "little"),
         lay.X25519_EXP_INV.hex()[:16] + "…")
controle("X25519_A24 == (486662 − 2) / 4", lay.X25519_A24 == 121665)
controle("X25519_BASE == 9", lay.X25519_BASE == 9)
controle("GCM_R == 0xE1 || 0^15",
         lay.GCM_R == (0xE1 << 120).to_bytes(16, "big"), lay.GCM_R.hex())
controle("HRR_MAGIQUE == SHA-256('HelloRetryRequest')",
         lay.HRR_MAGIQUE == hashlib.sha256(b"HelloRetryRequest").digest(),
         lay.HRR_MAGIQUE.hex()[:16] + "…")
controle("HMAC_BLOC == 64", lay.HMAC_BLOC == 64)
controle("HKDF_MAX_L == 255 × 32", lay.HKDF_MAX_L == 255 * 32)
controle("AES_CLES_TOUR == 11 × 16", lay.AES_CLES_TOUR == 176)
controle("CHARGE_MAX == 2^14", lay.CHARGE_MAX == 1 << 14)
controle("ENREGISTREMENT_CTX == 176 + 12 + 4 + 8",
         lay.ENREGISTREMENT_CTX == 200)
controle("ALERTE_CLOSE_NOTIFY == 01 00", lay.ALERTE_CLOSE_NOTIFY == b"\x01\x00")
controle("la suite et le groupe arrêtés",
         lay.SUITE == 0x1301 and lay.GROUPE == 0x001D)
controle("les versions de l'ère",
         lay.VERSION_DEV == 0x01000004 and lay.VERSION_FINALE == 0x01000000,
         "dev.4 : le dernier build de la ligne 1.0.0 [la révision 3 du "
         "terrain — les DEUX immédiates du contrat d'appel de sys-06, "
         "l'Entrée 192] ; dev.1 le premier build, dev.2 l'erratum n° 5, "
         "dev.3 la révision 2 de l'instrument — la finale 1.0.0 SCELLÉE "
         "est un fait de carte (D170), le qword de l'artefact demeure")
controle("la table des SEPT verdicts (0, −1..−7)",
         sorted(lay.VERDICTS) == list(range(-7, 1)))
controle("le préfixe d'étiquette « tls13 » + espace",
         lay.PREFIXE_ETIQUETTE == b"tls13 ")
for libelle, octets in lay.LIBELLES.items():
    totale = lay.PREFIXE_ETIQUETTE + octets
    controle(f"le libellé « {libelle} » : 7 ≤ {len(totale)} ≤ 255",
             7 <= len(totale) <= 255, f"{len(totale)} o avec le préfixe")

# --- (4) la construction du ClientHello re-jouée : 114 o ----------------------
def u16(x):
    return struct.pack(">H", x)


def u24(x):
    return struct.pack(">I", x)[1:]


exts = b""
exts += u16(lay.EXT_SUPPORTED_VERSIONS) + u16(3) + bytes([2]) + u16(lay.VERSION_TLS13)
exts += u16(lay.EXT_SUPPORTED_GROUPS) + u16(4) + u16(2) + u16(lay.GROUPE)
exts += u16(lay.EXT_SIG_ALGS) + u16(2 + 2 * len(lay.SIG_ALGOS))
exts += u16(2 * len(lay.SIG_ALGOS)) + b"".join(u16(a) for a in lay.SIG_ALGOS)
entree = u16(lay.GROUPE) + u16(32) + bytes(32)
exts += u16(lay.EXT_KEY_SHARE) + u16(len(entree) + 2) + u16(len(entree)) + entree
corps = (u16(lay.VERSION_HERITAGE) + bytes(32) + bytes([0])
         + u16(2) + u16(lay.SUITE) + bytes([1, 0])
         + u16(len(exts)) + exts)
ch = bytes([1]) + u24(len(corps)) + corps
controle("CLIENTHELLO_TAILLE == la construction re-jouée",
         lay.CLIENTHELLO_TAILLE == len(ch), f"{len(ch)} o == {lay.CLIENTHELLO_TAILLE}")

# le ServerHello minimal
sh_exts = u16(lay.EXT_SUPPORTED_VERSIONS) + u16(2) + u16(lay.VERSION_TLS13)
sh_exts += u16(lay.EXT_KEY_SHARE) + u16(36) + u16(lay.GROUPE) + u16(32) + bytes(32)
sh_corps = (u16(lay.VERSION_HERITAGE) + bytes(32) + bytes([0])
            + u16(lay.SUITE) + bytes([0]) + u16(len(sh_exts)) + sh_exts)
sh = bytes([2]) + u24(len(sh_corps)) + sh_corps
controle("SERVERHELLO_MIN == la construction re-jouée",
         lay.SERVERHELLO_MIN == len(sh), f"{len(sh)} o == {lay.SERVERHELLO_MIN}")

# --- (5) la disposition de session recomptée -----------------------------------
attendu_session = (112 + 48 + 32 + 32 + 200 * 4 + 32 * 3 + 4 + 4 + 8
                   + lay.SESSION_POIGNEE_MAX)
controle("SESSION_TAILLE == la disposition recomptée",
         lay.SESSION_TAILLE == attendu_session,
         f"{attendu_session} o == {lay.SESSION_TAILLE}")
controle("SESSION_TAILLE alignée 16", lay.SESSION_TAILLE % 16 == 0)
controle("CALENDRIER_CTX == 32 + 4 (+ réserve)", lay.CALENDRIER_CTX >= 36
         and lay.CALENDRIER_CTX % 16 == 0, str(lay.CALENDRIER_CTX))

# --- (6) les verdicts cités dans les specs vivent dans la table ----------------
table_verdicts = set(lay.VERDICTS)
for num, nom in sorted(ATTENDUS.items()):
    chemin = DOSSIER / nom
    if not chemin.exists():
        continue
    texte = chemin.read_text(encoding="utf-8")
    cites = {int(m) for m in re.findall(r"verdict (-\d+)", texte)}
    cites |= {int(m) for m in re.findall(r"rax = (-\d+)", texte)}
    cites |= {int(m) for m in re.findall(r"→ (-\d+)", texte)}
    hors = cites - table_verdicts
    controle(f"tls13-{num:02d} : les verdicts cités vivent dans la table",
             not hors, f"cités : {sorted(cites) if cites else 'aucun'}"
             + (f" · HORS TABLE : {sorted(hors)}" if hors else ""))

# --- le verdict ----------------------------------------------------------------
print()
if echecs:
    print(f"VERDICT : ROUGE — {len(echecs)} échec(s) nommé(s) : {echecs}")
    sys.exit(2)
print("VERDICT : VERT — les 28 spécifications sont posées et cohérentes ; "
      "les constantes du plan sont RE-DÉRIVÉES par arithmétique au geste "
      "même ; le chantier M9-(a) est COMPLET sur pièces.")
sys.exit(0)
