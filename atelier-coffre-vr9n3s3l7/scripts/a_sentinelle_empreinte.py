#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""a_sentinelle_empreinte.py — LES VECTEURS DE L'ITEM (a) : l'empreinte du
chiffretexte AVANT l'AEAD (la sentinelle instantanée étendue).

Quatre vecteurs, les verdicts NOMMÉS :
  V1  honnête            : l'ouverture VERTE (l'empreinte liée conforme) ;
  V2  CORRUPTION         : un octet du chiffretexte muté — REFUS NOMMÉ SANS
                           DESTRUCTION, le chiffretexte CONSERVÉ octet pour
                           octet, AUCUN PV ;
  V3  FALSIFICATION À
      EMPREINTE VALIDE   : l'attaquant réécrit le chiffretexte ET son
                           empreinte (l'empreinte = sha256 NU du nouveau
                           chiffretexte — la paire « valide » sous la
                           lecture naïve) : DESTRUCTION LOCALE + PV, le
                           média du piège INTACT ;
  V4  falsification SANS
      la clé             : chiffretexte réécrit, empreinte aléatoire — la
                           paire n'est cohérente NULLE part : refus nommé
                           (classe corruption), fail-closed — LA BORNE
                           CONSIGNÉE : sans K_emp la falsification se
                           présente comme corruption, rien ne s'ouvre ;
  V5  AEAD après empreinte verte : l'altération vit dans l'EN-TÊTE (le
                           nonce muté) — l'empreinte liée du chiffretexte
                           est CONFORME, le tag AEAD échoue : DESTRUCTION
                           LOCALE + PV (l'étage AEAD reste la preuve
                           restante, miroir CF3 § 5.5).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "labo"))
import coffre_labo as C                                     # noqa: E402

PHRASE = b"PHRASE-TEST-PUBLIQUE-D105-vague11-labo"
ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTEURS = os.path.join(ICI, "vecteurs", "a_sentinelle")


def vecteur(rep: str) -> str:
    conteneur = os.path.join(rep, "coffre.bin")
    pieges = os.path.join(rep, "pieges")
    r = C.init(conteneur, pieges, PHRASE, "vecteur (a)")
    return conteneur


def main() -> int:
    os.makedirs(VECTEURS, exist_ok=True)
    lignes = ["VECTEURS (a) — L'EMPREINTE DU CHIFFRETEXTE AVANT L'AEAD "
              "(sentinelle LCF3, plan (a))",
              f"phrase de test publique D105 : {PHRASE.decode()}", ""]
    verts = 0

    # V1 — honnête
    rep = os.path.join(VECTEURS, "v1-honnete")
    os.makedirs(rep, exist_ok=True)
    ct = vecteur(rep)
    r = C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
    v = r["entete"]["epoque"] == 1 and os.path.isfile(ct)
    verts += v
    lignes += [f"V1 honnête : ouverture {'VERTE' if v else 'ROUGE !'} — "
               f"époque {r['entete']['epoque']}, empreinte liée "
               f"(HMAC-SHA256, K_emp = HKDF(K_user ‖ S_piège)) CONFORME, "
               f"AEAD VERT", ""]

    # V2 — CORRUPTION (un octet du chiffretexte muté)
    rep = os.path.join(VECTEURS, "v2-corruption")
    os.makedirs(rep, exist_ok=True)
    ct = vecteur(rep)
    blob = bytearray(open(ct, "rb").read())
    ent = C.parser_entete(bytes(blob))
    blob[-1] ^= 0x01                       # le DERNIER octet du ct muté
    corrompu = bytes(blob)
    C._ecrire_atomique(ct, corrompu)
    try:
        C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg = str(e)
        v = ("CORRUPTION" in msg and "SANS destruction" in msg)
        # le chiffretexte CONSERVÉ octet pour octet :
        v &= open(ct, "rb").read() == corrompu
        # AUCUN PV, AUCUN fichier détruit :
        v &= not os.path.isdir(C.chemin_pv_dir(ct)) or \
            not os.listdir(C.chemin_pv_dir(ct))
        # le piège INTACT :
        v &= os.path.isfile(C.chemin_piege(os.path.join(rep, "pieges"), 1))
    verts += v
    lignes += [f"V2 CORRUPTION : {'VERT' if v else 'ROUGE !'} — verdict nommé "
               f"« {msg.split(chr(46))[0]} » ; le chiffretexte est CONSERVÉ "
               f"({len(corrompu)} octets, inchangé depuis l'incident), "
               "AUCUN PV écrit (la destruction attend la preuve — jamais "
               "sur un incident), le média du piège INTACT", ""]

    # V3 — FALSIFICATION À EMPREINTE VALIDE (ct réécrit + empreinte naïve)
    rep = os.path.join(VECTEURS, "v3-falsification")
    os.makedirs(rep, exist_ok=True)
    ct = vecteur(rep)
    import hashlib
    import secrets
    blob = bytearray(open(ct, "rb").read())
    ent = C.parser_entete(bytes(blob))
    faux_ct = secrets.token_bytes(len(ent["chiffretexte"]))   # le ct réécrit
    blob[C.FIN_ENTETE:] = faux_ct
    # l'attaquant pose l'empreinte NAÏVE : sha256 nu du nouveau ct —
    # la paire est « valide » sous la lecture non liée à la clé
    blob[C.FIN_AAD:C.FIN_AAD + 32] = hashlib.sha256(faux_ct).digest()
    falsifie = bytes(blob)
    C._ecrire_atomique(ct, falsifie)
    pv_dir_avant = set(os.listdir(C.chemin_pv_dir(ct))) \
        if os.path.isdir(C.chemin_pv_dir(ct)) else set()
    try:
        C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg = str(e)
        v = "FALSIFICATION À EMPREINTE VALIDE" in msg
        # le conteneur DÉTRUIT :
        v &= not os.path.isfile(ct)
        # le PV écrit :
        pv_dir = C.chemin_pv_dir(ct)
        pvs = [f for f in os.listdir(pv_dir) if f.endswith(".txt")] \
            if os.path.isdir(pv_dir) else []
        v &= len(pvs) == 1
        # le média du piège INTACT :
        v &= os.path.isfile(C.chemin_piege(os.path.join(rep, "pieges"), 1))
    verts += v
    pv = os.path.join(C.chemin_pv_dir(ct), pvs[0]) if v else "(aucun)"
    lignes += [f"V3 FALSIFICATION À EMPREINTE VALIDE : "
               f"{'VERT' if v else 'ROUGE !'} — verdict nommé « "
               f"{msg.split(chr(46))[0]} » ; le conteneur DÉTRUIT "
               "(3 passes, PV écrit), le média du piège INTACT, la paire "
               "(ct, sha256(ct)) cohérente sous la lecture NAÏVE est "
               "réfutée par l'empreinte LIÉE À LA CLÉ (HMAC)",
               f"   PV : {pv}", ""]

    # V4 — falsification SANS la clé (empreinte aléatoire)
    rep = os.path.join(VECTEURS, "v4-falsification-sans-cle")
    os.makedirs(rep, exist_ok=True)
    ct = vecteur(rep)
    blob = bytearray(open(ct, "rb").read())
    blob[C.FIN_ENTETE:] = secrets.token_bytes(
        len(C.parser_entete(bytes(blob))["chiffretexte"]))
    blob[C.FIN_AAD:C.FIN_AAD + 32] = secrets.token_bytes(32)   # aléatoire
    sans_cle = bytes(blob)
    C._ecrire_atomique(ct, sans_cle)
    try:
        C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg = str(e)
        v = "CORRUPTION" in msg and os.path.isfile(ct)
    verts += v
    lignes += [f"V4 falsification SANS la clé : {'VERT' if v else 'ROUGE !'} "
               "— verdict nommé (classe corruption) : refus fail-closed, "
               "rien ne s'ouuvre, aucune destruction (LA BORNE CONSIGNÉE : "
               "sans K_emp la falsification n'est pas PROUVABLE, elle est "
               "refusée — la destruction attend la preuve, la cohérence "
               "naïve)", ""]

    # V5 — AEAD après empreinte verte (le nonce de l'en-tête muté)
    rep = os.path.join(VECTEURS, "v5-aead")
    os.makedirs(rep, exist_ok=True)
    ct = vecteur(rep)
    blob = bytearray(open(ct, "rb").read())
    blob[137] ^= 0x01                     # le nonce (dans l'AAD clair) muté
    C._ecrire_atomique(ct, bytes(blob))
    try:
        C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg = str(e)
        v = "tag AEAD invalide" in msg and not os.path.isfile(ct)
    verts += v
    lignes += [f"V5 AEAD après empreinte VERTE : {'VERT' if v else 'ROUGE !'} "
               "— l'empreinte liée du chiffretexte est CONFORME (ct intact), "
               "le nonce d'en-tête est altéré : le tag AEAD échoue — "
               "falsification PROUVÉE côté machine : DESTRUCTION LOCALE "
               "+ PV (l'étage AEAD reste la preuve restante, l'ordre "
               "(a) est honoré : empreinte D'ABORD, AEAD ensuite)", ""]

    verdict = "VERT" if verts == 5 else "ROUGE"
    lignes += [f"BILAN (a) : {verts}/5 vecteurs VERTS — {verdict}",
               "LE COFFRE RÉEL N'A PAS ÉTÉ TOUCHÉ (copies de laboratoire, "
               "phrase de test publique D105)."]
    sortie = os.path.join(VECTEURS, "VECTEURS-a.txt")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    print(f"\n[écrit] {sortie}")
    return 0 if verts == 5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
