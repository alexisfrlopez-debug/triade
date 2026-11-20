#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""b_v_piege_epoque.py — LES VECTEURS DE L'ITEM (b) : V_piège DÉRIVÉE,
liée à S_piège ET à l'époque (l'anti-rollback au piège).

  V1  DÉRIVATION RE-PRODUCTIBLE : V_piège(é) recalculée (deux passages,
      secrets identiques) → IDENTIQUE octet pour octet ; la chaîne verif
      de l'époque courante est VERTE (l'ouverture honnête passe par la
      valeur DÉRIVÉE — le fichier piège ne porte PLUS de V_piège) ;
  V2  L'ÉPOQUE FAIT LA VALEUR : V_piège(1) ≠ V_piège(2) ≠ V_piège(3) —
      la dérivation change AVEC l'époque (le sel « piège‖époque ») ;
  V3  L'ÉPOQUE RETIRÉE REFUSÉE : après la clôture (époque 1 → 2), le
      COUPLE ANCIEN (conteneur d'époque 1 restauré + piège d'époque 1,
      intègre, tag VALIDE) est REFUSÉ NOMMÉMENT (RETOUR EN ARRIÈRE — le
      miroir local) ; le piège d'époque 1 présenté au conteneur d'époque
      2 : REFUS NOMMÉ (piège PÉRIMÉ — V_piège dérivée à l'époque) ;
  V4  LA TRICHERIE PAR S_piège : un piège FORGÉ d'époque 2 (S_piège
      réécrit, tag recalculé par l'attaquant qui a le média) : verif
      diverge → PhraseErronee — BÉNIN, réessai, JAMAIS de destruction
      (la borne CF3 : un piège entièrement forgé se présente comme une
      phrase erronée) ;
  V5  LE PIÈGE SANOSSOIS : le piège d'un AUTRE coffre (H_projet
      divergent) → REFUS NOMMÉ.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "labo"))
import coffre_labo as C                                     # noqa: E402

PHRASE = b"PHRASE-TEST-PUBLIQUE-D105-vague11-labo"
ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VECTEURS = os.path.join(ICI, "vecteurs", "b_vpiege")


def main() -> int:
    os.makedirs(VECTEURS, exist_ok=True)
    lignes = ["VECTEURS (b) — V_piège DÉRIVÉE : HKDF(S_piège ; « piège » ‖ "
              "époque), l'anti-rollback (plan (b))", ""]
    verts = 0

    # V1 — dérivation re-productible + chaîne verif à l'époque courante
    s_piege = bytes.fromhex("11" * 32)
    v1a = C.derive_v_piege(s_piege, 7)
    v1b = C.derive_v_piege(bytes.fromhex("11" * 32), 7)
    v = v1a == v1b and len(v1a) == C.TAILLE_V_PIEGE
    rep = os.path.join(VECTEURS, "v1-epoque-courante")
    os.makedirs(rep, exist_ok=True)
    ct = os.path.join(rep, "coffre.bin")
    C.init(ct, os.path.join(rep, "pieges"), PHRASE, "v1")
    r = C.ouvrir(ct, os.path.join(rep, "pieges"), PHRASE)
    # le fichier piège ne porte PAS de V_piège (elle est DÉRIVÉE) :
    texte_piege = open(C.chemin_piege(os.path.join(rep, "pieges"), 1),
                       encoding="ascii").read()
    v &= "verif:" not in texte_piege
    verts += v
    lignes += [f"V1 DÉRIVATION RE-PRODUCTIBLE : {'VERT' if v else 'ROUGE !'} "
               f"— V_piège(7) = {v1a.hex()} (16 o), recalcul IDENTIQUE ; "
               "l'ouverture honnête à l'époque courante est VERTE (la "
               "chaîne verif est calculée sur V_piège DÉRIVÉE) ; le "
               "fichier piège v2 ne PORTE PAS de V_piège (S_piège + tag "
               "seuls)", ""]

    # V2 — l'époque fait la valeur
    va, vb, vc = (C.derive_v_piege(s_piege, e) for e in (1, 2, 3))
    v = len({va.hex(), vb.hex(), vc.hex()}) == 3
    verts += v
    lignes += [f"V2 L'ÉPOQUE FAIT LA VALEUR : {'VERT' if v else 'ROUGE !'} — "
               f"V_piège(1)={va.hex()[:16]}… ≠ V_piège(2)={vb.hex()[:16]}… ≠ "
               f"V_piège(3)={vc.hex()[:16]}… (le sel « piège‖époque_le64 » "
               "lie la valeur à l'époque)", ""]

    # V3 — l'époque retirée REFUSÉE
    rep = os.path.join(VECTEURS, "v3-epoque-retiree")
    os.makedirs(rep, exist_ok=True)
    ct = os.path.join(rep, "coffre.bin")
    pieges = os.path.join(rep, "pieges")
    C.init(ct, pieges, PHRASE, "v3")
    ancien = open(ct, "rb").read()          # le canonique d'époque 1
    r = C.ouvrir(ct, pieges, PHRASE)
    cloture = C.fermer(ct, pieges, PHRASE, r["base"])      # époque 1 -> 2
    # (i) le couple ancien RESTAURÉ (conteneur d'époque 1 + son piège) :
    os.makedirs(os.path.join(rep, "restaure"), exist_ok=True)
    ct_r = os.path.join(rep, "restaure", "coffre.bin")
    open(ct_r, "wb").write(ancien)
    # LE PIÈGE D'ÉPOQUE 1 COPIÉ AU-DESSUS du conteneur restauré (le setup
    # l'omettait — le refus venait par « piège ABSENT », un refus réel mais
    # pas le NOM attendu : la faute nommée et corrigée)
    import shutil as _sh
    _sh.copy(C.chemin_piege(pieges, 1),
             C.chemin_piege(os.path.join(rep, "restaure"), 1))
    C._ecrire_miroir(ct_r, 2, "00000000")   # le miroir a vu l'époque 2
    try:
        C.ouvrir(ct_r, os.path.join(rep, "restaure"), PHRASE)
        v_i, msg_i = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg_i = str(e)
        v_i = "RETOUR EN ARRIÈRE" in msg_i
    # (ii) le piège d'époque 1 présenté au conteneur d'époque 2 :
    piege_vieux = os.path.join(rep, "piege-epoque-1-restaure.txt")
    import shutil
    shutil.copy(C.chemin_piege(pieges, 1), piege_vieux)
    blob = open(ct, "rb").read()
    ent = C.parser_entete(blob)
    try:
        # sentinelle directe : conteneur époque 2 + piège époque 1
        C.sentinelle_lcf3(blob, piege_vieux, PHRASE, ct)
        v_ii, msg_ii = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg_ii = str(e)
        v_ii = "PÉRIMÉ" in msg_ii and "V_piège DÉRIVÉE" in msg_ii
    v = v_i and v_ii
    verts += v
    lignes += [f"V3 L'ÉPOQUE RETIRÉE REFUSÉE : {'VERT' if v else 'ROUGE !'} — "
               f"(i) le couple ancien restauré : « {msg_i.split(chr(46))[0]} "
               "» ; (ii) le piège d'époque 1 au conteneur d'époque 2 : « "
               f"{msg_ii.split(chr(46))[0]} » — l'anti-rollback au piège : "
               "V_piège est DÉRIVÉE à l'époque, l'époque retirée ne vérifie "
               "PLUS (aucune relecture possible, même piège intègre, même "
               "phrase honnête)", ""]

    # V4 — le piège forgé (S_piège réécrit, tag recalculé)
    rep4 = os.path.join(VECTEURS, "v4-piege-foge")
    os.makedirs(rep4, exist_ok=True)
    ct = os.path.join(rep4, "coffre.bin")
    pieges = os.path.join(rep4, "pieges")
    C.init(ct, pieges, PHRASE, "v4")
    blob = open(ct, "rb").read()
    ent = C.parser_entete(blob)
    forge = bytearray(bytes.fromhex("22" * 32))       # S_piège réécrit
    piege_f = os.path.join(rep4, "piege-forge.txt")
    open(piege_f, "w", encoding="ascii").write(
        C.serialiser_piege(1, ent["h_projet"], forge))   # tag RECALCULÉ
    try:
        C.sentinelle_lcf3(blob, piege_f, PHRASE, ct)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.PhraseErronee as e:
        msg = str(e)
        v = "phrase ERRONÉE" in msg
    except C.ErreurCoffre as e:
        msg = str(e)
        v = False
    verts += v
    lignes += [f"V4 LE PIÈGE FORGÉ : {'VERT' if v else 'ROUGE !'} — S_piège "
               "réécrit, tag RECALCULÉ par l'attaquant qui tient le média : "
               "verif diverge (V_piège dérivée du faux S_piège) → "
               "PhraseErronee, BÉNIN : réessai, JAMAIS de destruction (la "
               "borne CF3 : un piège entièrement forgé se présente comme "
               "une phrase erronée)", ""]

    # V5 — le piège d'un autre coffre
    rep5 = os.path.join(VECTEURS, "v5-autre-coffre")
    os.makedirs(rep5, exist_ok=True)
    ct = os.path.join(rep5, "coffre.bin")
    pieges = os.path.join(rep5, "pieges")
    C.init(ct, pieges, PHRASE, "v5")
    autre = os.path.join(rep5, "piege-autre.txt")
    open(autre, "w", encoding="ascii").write(
        C.serialiser_piege(1, bytes.fromhex("ab" * 32),
                           bytes.fromhex("33" * 32)))
    blob = open(ct, "rb").read()
    try:
        C.sentinelle_lcf3(blob, autre, PHRASE, ct)
        v, msg = False, "ACCEPTÉ (BUG !)"
    except C.ErreurCoffre as e:
        msg = str(e)
        v = "AUTRE coffre" in msg or "AUTRE\ncoffre" in msg
    verts += v
    lignes += [f"V5 LE PIÈGE D'UN AUTRE COFFRE : {'VERT' if v else 'ROUGE !'} "
               f"— « {msg.split(chr(46))[0]} » (H_projet divergent, refus "
               "nommé)", ""]

    verdict = "VERT" if verts == 5 else "ROUGE"
    lignes += [f"BILAN (b) : {verts}/5 vecteurs VERTS — {verdict}",
               "AUCUN coffre réel, AUCUNE phrase réelle (D105)."]
    sortie = os.path.join(VECTEURS, "VECTEURS-b.txt")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    print(f"\n[écrit] {sortie}")
    return 0 if verts == 5 else 1


if __name__ == "__main__":
    raise SystemExit(main())
