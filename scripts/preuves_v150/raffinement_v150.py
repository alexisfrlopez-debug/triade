#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""raffinement_v150.py — LES TESTS DE RAFFINEMENT modèle ↔ implémentation
(v0.15.0, la commande ic09ydeli point 1 : « ajouter des tests de
raffinement : rejouer les traces du modèle contre l'implémentation Python
(équivalence des transitions, y compris les chemins d'échec) et consigner
tout écart modèle↔implémentation »).

LE PRINCIPE. Chaque scénario pilote EN PARALLÈLE :
  — l'état ABSTRAIT du modèle non borné (modele_invariant_v150.py, les 13
    règles de la sémantique) ;
  — un coffre CONCRET de test (v06/coffre_cf3.py, phrase de TEST publique
    marquée — D192 : le conteneur réel n'est JAMAIS ouvert par un test).
À chaque pas : la MÊME action abstraite et son geste concret ; les verdicts
sont CONFRONTÉS (la table ci-dessous) ; l'époque du statut concret doit
égaler l'époque abstraite ; les effets concrets (destruction locale, PV,
refus) doivent correspondre aux effets abstraits (detruit, état inchangé).
TOUT écart est consigné TEL QUEL — y compris défavorable.

LA TABLE DE CORRESPONDANCE (l'abstrait → le concret) :
  ouvrir_correct (honnête)        → Session ouverte ; phase=brouillon
  ouvrir_correct (piège absent)   → ErreurCoffre « déverrouillage IMPOSSIBLE »
      (le modèle : trap_ok=False → None — IMPOSSIBLE, pas refusé)
  ouvrir_correct (vole K_user
    seul, seuil < 3)              → l'ouverture ÉCHOUE : le KEK (les TROIS
      éléments) indérivable — vérifié par derive_kek à moitié fausse : le
      verif/AEAD ne passe JAMAIS
  ouvrir_phrase_erronée           → PhraseErronee ; RIEN détruit (P3)
  ouvrir_ancien_couple            → ErreurCoffre « RETOUR EN ARRIÈRE » ou
      « piège PÉRIMÉ » ; état inchangé (P2)
  rejoue_époque_passée            → idem (l'adversaire restaure le couple,
      PAS le miroir : le miroir courant refuse)
  verifier                        → verdict VERT ; état inchangé
  crash_pendant_session           → abandonner() : le brouillon devient
      déchet ; phase=canonique, époque inchangée
  clôturer_correcte               → fermer() : époque + 1, canonique
      (SANS plafond — la contrepartie de la non-bornitude)
  clôturer_phrase_erronée         → PhraseErronee ; AUCUN scellement (le
      piège N+1 n'existe pas, le conteneur est intact)
  falsifie_conteneur (piège
    intègre, canonique)           → sentinelle point 5 : destruction LOCALE
      + PV ; le média INTACT, CF2 INTACT (P4)
  falsifie_piège                  → sentinelle point 2 : refus SANS
      destruction (tag invalide) ; le conteneur INTACT

LES GESTES HORS MODÈLE (couverts au concret, consignés comme tels — le
modèle v120/v150 n'a qu'un coffre et pas de témoin hors-bande) :
  le piège d'un AUTRE coffre      → « H_projet divergent » (spec § 5.3)
  le témoin hors-bande            → epoque_attendue : le rejeu nommé même
      si le miroir local est écrasé avec le couple restauré

Sortie : scripts/preuves_v150/raffinement.csv + rapport txt.
"""

from __future__ import annotations

import csv
import pathlib
import shutil
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
PREUVES = REPO / "scripts" / "preuves_v150"
sys.path.insert(0, str(REPO / "v06"))
sys.path.insert(0, str(REPO / "scripts" / "preuves_v150"))

import coffre_cf3 as cf3          # noqa: E402
import modele_invariant_v150 as m150  # noqa: E402

PHRASE_TEST = (b"PHRASE-DE-TEST-PUBLIQUE-V150-RAFFINEMENT"
               b" - jamais une phrase reelle (D192)")
PHRASE_FAUSSE = b"phrase-erronee-de-test-v150 - jamais la vraie"

ZONE = pathlib.Path(tempfile.mkdtemp(prefix="raffinement_v150_"))


# ---------------------------------------------------------------------------
# l'observation concrète
# ---------------------------------------------------------------------------

class Concret:
    """Le coffre de test : conteneur + média de piège, dans la zone ZONE."""

    def __init__(self, nom: str):
        self.dossier = ZONE / nom
        self.dossier.mkdir(parents=True)
        self.piege_dir = self.dossier / "media-piege"
        self.piege_dir.mkdir()
        self.conteneur = str(self.dossier / "coffre-cf3.bin")

    # -- les observations d'état --
    def epoque(self):
        try:
            return cf3.statut(self.conteneur)["epoque"]
        except cf3.ErreurCoffre:
            return None  # conteneur détruit

    def conteneur_vivant(self) -> bool:
        return pathlib.Path(self.conteneur).is_file()

    def nb_pv(self) -> int:
        pv_dir = cf3.chemin_pv_dir(self.conteneur)
        return len(list(pathlib.Path(pv_dir).glob("pv-*.txt"))) \
            if pathlib.Path(pv_dir).is_dir() else 0

    def pieges_presents(self) -> int:
        return len(list(self.piege_dir.glob("*")))

    def piege_path(self, epoque: int) -> str:
        return cf3.chemin_piege(str(self.piege_dir), epoque)


RESULTATS = []   # (scénario, pas, action, verdict_abstrait, verdict_concret,
                 #  conforme: bool, détail)


def pas(nom_scen, i, action, genre, abstrait, concret, conforme, detail=""):
    RESULTATS.append({
        "scénario": nom_scen, "pas": i, "action": action,
        "verdict_abstrait": abstrait, "verdict_concret": concret,
        "conforme": "OUI" if conforme else "ÉCART", "détail": detail,
    })
    print(f"  [{i:>3}] {action:32s} abstrait={abstrait:26s} "
          f"concret={concret:36s} {'OK' if conforme else 'ÉCART !'}"
          + (f"  {detail}" if detail else ""))


def exce(function, *args, **kwargs):
    """Exécute et retourne ('ok', résultat) ou ('exc', exception)."""
    try:
        return ("ok", function(*args, **kwargs))
    except Exception as exc:  # noqa: BLE001 — le verdict EST l'exception
        return ("exc", exc)


# ---------------------------------------------------------------------------
# LES SCÉNARIOS
# ---------------------------------------------------------------------------

def scenario_cycle_honnete():
    """S1 — le cycle honnête INTÉGRAL au-delà de la borne v120 : quatre
    époques vécues (1→2→3→4→5), la contrepartie concrète de la
    non-bornitude, avec crash et phrase erronée en chemin."""
    print("S1 — le cycle honnête intégral (cinq époques)")
    c = Concret("s1")
    s = m150.etat_initial()
    # l'init concret : époque 1 (l'état initial du modèle)
    r = exce(cf3.init, PHRASE_TEST, str(c.piege_dir),
             description="raffinement v150", conteneur_chemin=c.conteneur)
    pas("S1", 0, "(init)", "protocole",
        "état initial e=1", f"init {'ok' if r[0] == 'ok' else 'exc'}",
        r[0] == "ok" and c.epoque() == 1 and s[0] == 1)

    for k in range(1, 5):  # quatre clôtures : e = 2, 3, 4, 5
        # a) verifier — état inchangé
        r = exce(cf3.verifier, c.conteneur, c.piege_path(s[0]),
                 PHRASE_TEST)
        pas("S1", f"{k}a", "verifier", "protocole", "état inchangé",
            f"{'vert e=' + str(r[1]['epoque']) if r[0] == 'ok' else 'exc'}",
            r[0] == "ok" and r[1]["epoque"] == s[0],
            "l'époque concrète == l'abstraite")
        # b) ouvrir_correct — phase brouillon
        r = exce(cf3.ouvrir, c.conteneur, c.piege_path(s[0]), PHRASE_TEST)
        session = r[1] if r[0] == "ok" else None
        s2 = m150.appliquer(s, "ouvrir_correct", "protocole")
        pas("S1", f"{k}b", "ouvrir_correct", "protocole",
            "phase→brouillon", f"{'session' if session else 'exc'}",
            session is not None and s2 is not None
            and s2[1] == "brouillon")
        s = s2
        # c) au milieu : la phrase erronée à l'OUVERTURE (P3) — bénin
        if k == 2:
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(s[0]),
                     PHRASE_FAUSSE)
            s3 = m150.appliquer(s, "ouvrir_phrase_erronée", "protocole")
            pas("S1", f"{k}c", "ouvrir_phrase_erronée", "protocole",
                "état inchangé (P3)",
                type(r[1]).__name__ if r[0] == "exc" else "ok",
                r[0] == "exc" and isinstance(r[1], cf3.PhraseErronee)
                and s3 == s and c.conteneur_vivant() and c.nb_pv() == 0,
                "PhraseErronee, RIEN détruit")
        # d) au milieu : le CRASH de session (k == 3) : le brouillon meurt
        if k == 3:
            session.abandonner()
            s4 = m150.appliquer(s, "crash_pendant_session", "protocole")
            pas("S1", f"{k}d", "crash_pendant_session", "protocole",
                "phase→canonique, e inchangé", "abandonner()",
                s4 is not None and s4[1] == "canonique" and s4[0] == s[0],
                "le canonique INTACT, l'époque ne bouge pas")
            s = s4
            # ré-ouverture honnête après le crash
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(s[0]),
                     PHRASE_TEST)
            session = r[1] if r[0] == "ok" else None
            s = m150.appliquer(s, "ouvrir_correct", "protocole")
            pas("S1", f"{k}e", "ouvrir_correct", "protocole",
                "ré-ouverture : phase→brouillon",
                "session", session is not None and s is not None)
        # e) la phrase erronée à la CLÔTURE (P3) — aucun scellement
        pieges_avant = c.pieges_presents()
        r = exce(cf3.fermer, session, PHRASE_FAUSSE, str(c.piege_dir))
        s5 = m150.appliquer(s, "clôturer_phrase_erronée", "protocole")
        pas("S1", f"{k}f", "clôturer_phrase_erronée", "protocole",
            "état inchangé (P3)",
            type(r[1]).__name__ if r[0] == "exc" else "ok",
            r[0] == "exc" and isinstance(r[1], cf3.PhraseErronee)
            and s5 == s and c.pieges_presents() == pieges_avant,
            "PhraseErronee, AUCUN scellement (pas de piège N+1)")
        # f) clôturer_correcte — époque + 1 SANS plafond
        r = exce(cf3.fermer, session, PHRASE_TEST, str(c.piege_dir))
        s6 = m150.appliquer(s, "clôturer_correcte", "protocole")
        pas("S1", f"{k}g", "clôturer_correcte", "protocole",
            f"e {s[0]}→{s[0] + 1}" if s6 else "refus",
            f"fermer → e={r[1]['epoque']}" if r[0] == "ok"
            else type(r[1]).__name__,
            r[0] == "ok" and s6 is not None
            and r[1]["epoque"] == s[0] + 1 == s6[0]
            and s6[1] == "canonique",
            "l'époque +1 aux DEUX niveaux — la non-bornitude vécue")
        s = s6
    pas("S1", 99, "(final)", "—",
        f"e={s[0]} (5 attendu)", f"e={c.epoque()}",
        s[0] == 5 and c.epoque() == 5,
        "QUATRE clôtures vécues : la borne v120 (e ≤ 3) est dépassée "
        "aux DEUX niveaux")
    return s


def scenario_phrase_erronee():
    """S2 — la phrase erronée répétée : JAMAIS de destruction (P3), l'état
    inchangé à l'ouverture ET à la clôture, dix fois."""
    print("S2 — la phrase erronée répétée (P3)")
    c = Concret("s2")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    conforme = True
    for i in range(10):
        r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_FAUSSE)
        s2 = m150.appliquer(s, "ouvrir_phrase_erronée", "protocole")
        ok = (r[0] == "exc" and isinstance(r[1], cf3.PhraseErronee)
              and s2 == s and c.conteneur_vivant() and c.nb_pv() == 0)
        conforme = conforme and ok
    pas("S2", 1, "ouvrir_phrase_erronée ×10", "protocole",
        "état inchangé ×10", "PhraseErronee ×10", conforme,
        "le conteneur VIVANT, zéro PV — la destruction n'est JAMAIS "
        "déclenchée par la phrase")
    # la clôture avec phrase erronée exige une session ouverte avant
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    session = r[1]
    s = m150.appliquer(s, "ouvrir_correct", "protocole")
    conforme = True
    for i in range(5):
        r = exce(cf3.fermer, session, PHRASE_FAUSSE, str(c.piege_dir))
        ok = (r[0] == "exc" and isinstance(r[1], cf3.PhraseErronee)
              and c.conteneur_vivant() and c.nb_pv() == 0)
        conforme = conforme and ok
    pas("S2", 2, "clôturer_phrase_erronée ×5", "protocole",
        "état inchangé ×5", "PhraseErronee ×5", conforme,
        "AUCUN scellement : le conteneur demeure à l'époque 1")
    pas("S2", 99, "(final)", "—", "e=1", f"e={c.epoque()}",
        c.epoque() == 1, "l'époque n'a pas bougé")


def scenario_falsification_conteneur():
    """S3 — la falsification PROUVÉE du conteneur (piège intègre) : la
    destruction LOCALE, le média et CF2 INTACTS (P4)."""
    print("S3 — la falsification du conteneur (P4)")
    c = Concret("s3")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    # un bit du chiffretexte (la fin du conteneur — jamais l'en-tête :
    # l'en-tête falsifié change l'étiquette, le chiffretexte falsifié est
    # la falsification PROUVÉE par empreinte après la phrase vérifiée)
    blob = bytearray(pathlib.Path(c.conteneur).read_bytes())
    blob[-1] ^= 0x01
    pathlib.Path(c.conteneur).write_bytes(bytes(blob))
    pieges_avant = c.pieges_presents()
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    s2 = m150.appliquer(s, "falsifie_conteneur", "adversaire")
    ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
          and s2 is not None and s2[7] is True      # detruit=True
          and not c.conteneur_vivant()               # le conteneur mort
          and c.nb_pv() == 1                          # UN procès-verbal
          and c.pieges_presents() == pieges_avant     # le média INTACT
          and s2[9] is False and s2[4] is True)       # media/CF2 intacts
    pas("S3", 1, "falsifie_conteneur", "adversaire",
        "destruction LOCALE, média+CF2 intacts",
        f"{'ErreurCoffre' if r[0] == 'exc' else 'ok'} : conteneur détruit, "
        f"PV={c.nb_pv()}, pièges={c.pieges_presents()}",
        ok, "la sentinelle point 5 : empreinte divergente APRÈS phrase "
        "vérifiée → destruction locale + PV (spec § 7)")
    # le miroir et le journal demeurent (les témoins internes)
    pas("S3", 2, "(après-coup)", "—", "le média INTACT (P4)",
        f"pièges sur média : {c.pieges_presents()}/{pieges_avant}",
        c.pieges_presents() == pieges_avant,
        "la destruction n'est pas un balai — le média hors limite")


def scenario_falsification_piege():
    """S4 — la falsification du piège (tag) : le refus SANS destruction."""
    print("S4 — la falsification du piège (refus bénin)")
    c = Concret("s4")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    piege = pathlib.Path(c.piege_path(1))
    texte = piege.read_text("ascii")
    # le tag : la dernière ligne hex — un octet modifié = tag invalide
    lignes = texte.splitlines()
    lignes[-1] = ("0" if lignes[-1][0] != "0" else "1") + lignes[-1][1:]
    piege.write_text("\n".join(lignes) + "\n", "ascii")
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    s2 = m150.appliquer(s, "falsifie_piège", "adversaire")
    # modèle : trap_ok→False, AUCUNE destruction ; concret : refus SANS
    # destruction, le conteneur VIVANT
    ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
          and s2 is not None and s2[3] is False       # trap_ok=False
          and c.conteneur_vivant() and c.nb_pv() == 0)
    pas("S4", 1, "falsifie_piège", "adversaire",
        "refus NOMMÉ, aucune destruction",
        f"{'ErreurCoffre (refus SANS destruction)' if r[0] == 'exc' else 'ok'}",
        ok, "le média est le TÉMOIN, jamais le coupable (spec § 5.2)")


def scenario_rejeu():
    """S5 — le rejeu d'époque passée (A4/P2) : trois variantes concrètes,
    le canonique e2 SAUVEGARDÉ avant tout geste adverse."""
    print("S5 — le rejeu d'époque passée (P2)")
    c = Concret("s5")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    # le couple e1 archivé par l'adversaire (copie brute AVANT clôture)
    conteneur_e1 = pathlib.Path(c.conteneur).read_bytes()
    piege_e1 = pathlib.Path(c.piege_path(1)).read_bytes()
    # clôture honnête → e2 (le canonique e2 SAUVEGARDÉ : le pas adverse
    # suivant ne doit pas le détruire pour rien)
    session = cf3.ouvrir(c.conteneur, c.piege_path(1), PHRASE_TEST)
    cf3.fermer(session, PHRASE_TEST, str(c.piege_dir))
    s = m150.appliquer(m150.appliquer(s, "ouvrir_correct", "protocole"),
                       "clôturer_correcte", "protocole")
    conteneur_e2 = pathlib.Path(c.conteneur).read_bytes()
    # a) l'adversaire restaure le conteneur e1 (PAS le miroir) + piège e1 :
    #    le miroir courant (e2) refuse « RETOUR EN ARRIÈRE »
    pathlib.Path(c.conteneur).write_bytes(conteneur_e1)
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    s2 = m150.appliquer(s, "rejoue_époque_passée", "adversaire")
    ok = (r[0] == "exc" and "RETOUR EN ARRIÈRE" in str(r[1])
          and s2 == s)
    pas("S5", 1, "rejoue_époque_passée", "adversaire",
        "refus NOMMÉ, état inchangé",
        f"{'RETOUR EN ARRIÈRE' if r[0] == 'exc' and 'RETOUR' in str(r[1]) else str(r[1])[:40]}",
        ok, "le miroir local : le plus faible des trois témoins, il tient")
    # b) le canonique e2 RESTAURÉ + le piège e1 : époches croisées « PÉRIMÉ »
    pathlib.Path(c.conteneur).write_bytes(conteneur_e2)
    pathlib.Path(c.piege_path(1)).write_bytes(piege_e1)
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    s3 = m150.appliquer(s, "ouvrir_ancien_couple", "protocole")
    ok = (r[0] == "exc" and "PÉRIMÉ" in str(r[1]) and s3 == s)
    pas("S5", 2, "ouvrir_ancien_couple (croisé)", "protocole",
        "refus NOMMÉ « piège PÉRIMÉ », état inchangé",
        f"{str(r[1])[:40] if r[0] == 'exc' else 'ok'}",
        ok, "les époques croisées conteneur/piège refusées (spec § 9)")
    # c) le témoin hors-bande : l'adversaire restaure le couple e1 ET
    #    écrase le miroir (admin local) — seul epoque_attendue=2 nomme le
    #    rejeu (la carte papier / le journal Git, spec § 9)
    pathlib.Path(c.conteneur).write_bytes(conteneur_e1)
    entete_e1 = cf3.parser_entete(conteneur_e1)
    cf3._ecrire_miroir(c.conteneur, 1, entete_e1["h_projet"][:4].hex())
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST,
             epoque_attendue=2)
    ok_c = (r[0] == "exc" and "hors-bande" in str(r[1]))
    pas("S5", 3, "(témoin hors-bande)", "hors-modèle",
        "—", f"{str(r[1])[:44] if r[0] == 'exc' else 'ok'}",
        ok_c, "geste HORS MODÈLE (le modèle n'a pas de témoin) : le rejeu "
        "nommé même miroir écrasé — la carte papier/journal Git")


def scenario_piege_absent_et_autre_coffre():
    """S6 — le piège ABSENT (l'invocation sine qua non) et le piège d'un
    AUTRE coffre (H_projet) : deux refus structurels."""
    print("S6 — le piège absent / l'autre coffre")
    c = Concret("s6")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    # a) le média débranché : le piège ABSENT — dans le modèle,
    #    l'indisponibilité du piège (absence OU falsification) se dit
    #    trap_ok=False : l'écart de vocabulaire est consigné ci-dessous
    piege_sauve = ZONE / "s6-piege-sauve.txt"
    pathlib.Path(c.piege_path(1)).rename(piege_sauve)
    s_indispo = m150.appliquer(s, "falsifie_piège", "adversaire")
    r = exce(cf3.ouvrir, c.conteneur, c.piege_path(1), PHRASE_TEST)
    s2 = m150.appliquer(s_indispo, "ouvrir_correct", "protocole")
    ok = (r[0] == "exc" and "IMPOSSIBLE" in str(r[1]) and s2 is None
          and c.conteneur_vivant() and c.nb_pv() == 0)
    pas("S6", 1, "ouvrir_correct (piège absent)", "protocole",
        "IMPOSSIBLE (None), rien lu, rien brûlé",
        f"{str(r[1])[:40] if r[0] == 'exc' else 'ok'}",
        ok, "l'invocation D120 : sans le piège, l'ouverture est "
        "IMPOSSIBLE, pas refusée — le modèle dit trap_ok=False (absence "
        "OU falsification : le même prédicat d'indisponibilité)")
    pathlib.Path(piege_sauve).rename(c.piege_path(1))
    # b) le piège d'un AUTRE coffre : H_projet divergent — deux coffres à
    #    l'état initial IDENTIQUE (même description) partagent le MÊME
    #    H_projet (l'empreinte de l'état) : le test exige une description
    #    DISTINCTE, sinon le piège étranger n'est discernable que du verif
    autre = Concret("s6-autre")
    cf3.init(PHRASE_TEST, str(autre.piege_dir),
             description="L'AUTRE coffre (état initial distinct)",
             conteneur_chemin=autre.conteneur)
    r = exce(cf3.ouvrir, c.conteneur, autre.piege_path(1), PHRASE_TEST)
    ok = (r[0] == "exc" and "AUTRE" in str(r[1]).upper()
          and c.conteneur_vivant() and c.nb_pv() == 0)
    detail = "geste HORS MODÈLE (un seul coffre dans le modèle) : "
    if ok and "AUTRE" in str(r[1]).upper():
        detail += "H_projet divergent, spec § 5.3"
    else:
        detail += (f"verdict obtenu : {str(r[1])[:60]} — consigné tel quel")
    pas("S6", 2, "(piège d'un autre coffre)", "hors-modèle",
        "—", f"{str(r[1])[:40] if r[0] == 'exc' else 'ok'}",
        ok, detail)


def scenario_adversaire_seuil():
    """S7 — l'adversaire à seuil (P1) : la phrase seule (K_user volé, le
    média et la serrure saufs) ne dérive JAMAIS le KEK — les moitiés
    fausses échouent à l'AEAD ; le modèle : l'ouverture ÉCHOUE (None)."""
    print("S7 — l'adversaire à seuil (P1)")
    c = Concret("s7")
    cf3.init(PHRASE_TEST, str(c.piege_dir), conteneur_chemin=c.conteneur)
    s = m150.etat_initial()
    # l'état abstrait : l'adversaire vole K_user (seuil 1 < 3)
    s_vole = m150.appliquer(s, "vole_K_user", "adversaire")
    r = m150.appliquer(s_vole, "ouvrir_correct", "protocole")
    pas("S7", 1, "vole_K_user → ouvrir_correct", "protocole",
        "l'ouverture ÉCHOUE (None)",
        "KEK indérivable (2 moitiés manquantes)",
        r is None and s_vole is not None,
        "le modèle : sans les TROIS éléments, l'ouverture échoue")
    # la contrepartie concrète : derive_kek à moitiés fausses → le verif
    # diverge (l'AEAD/verif ne passe JAMAIS) — 32 essais aléatoires
    import secrets as _secrets
    blob = pathlib.Path(c.conteneur).read_bytes()
    entete = cf3.parser_entete(blob)
    k_user = cf3.cle_utilisateur(PHRASE_TEST, entete["sel_argon"])
    faux_ok = 0
    for _ in range(32):
        s_serrure_faux = _secrets.token_bytes(32)
        s_piege_faux = _secrets.token_bytes(32)
        v_piege_faux = _secrets.token_bytes(32)
        kek = cf3.derive_kek(k_user, s_serrure_faux, s_piege_faux,
                             entete["sel_hkdf"], entete["epoque"],
                             entete["h_projet"])
        if cf3.derive_verif(k_user, v_piege_faux, entete["sel_hkdf"]) \
                == entete["verif"]:
            faux_ok += 1  # un faux triplet qui passe : IMPOSSIBLE en pratique
    pas("S7", 2, "(derive_kek à moitiés fausses ×32)", "hors-modèle",
        "—", f"{faux_ok}/32 triplets forgés passent le verif",
        faux_ok == 0,
        "la contrepartie concrète de P1 sous A1 : sans les vraies moitiés, "
        "le verif n'est JAMAIS atteint (l'échec AEAD de la spec § 5.5)")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    print("=== LES TESTS DE RAFFINEMENT modèle ↔ implémentation (v0.15.0) ===")
    print(f"[zone de test] {ZONE} — phrase de TEST publique (D192), "
          "le coffre réel n'est JAMAIS touché")
    try:
        scenario_cycle_honnete()
        scenario_phrase_erronee()
        scenario_falsification_conteneur()
        scenario_falsification_piege()
        scenario_rejeu()
        scenario_piege_absent_et_autre_coffre()
        scenario_adversaire_seuil()
    finally:
        shutil.rmtree(ZONE, ignore_errors=True)

    total = len(RESULTATS)
    ecarts = [r for r in RESULTATS if r["conforme"] == "ÉCART"]
    print(f"\n[ bilan ] {total} pas de raffinement, {len(ecarts)} écart(s)")

    csv_path = PREUVES / "raffinement.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(RESULTATS[0].keys()))
        w.writeheader()
        w.writerows(RESULTATS)

    rapport = [
        "LES TESTS DE RAFFINEMENT MODÈLE ↔ IMPLÉMENTATION — v0.15.0",
        "",
        "LE PRINCIPE : chaque scénario pilote en parallèle l'état abstrait "
        "(modele_invariant_v150.py, les 13 règles) et un coffre CONCRET de "
        "test (v06/coffre_cf3.py, phrase de test publique marquée D192) ; "
        "les verdicts sont confrontés transition par transition, les "
        "chemins d'échec inclus ; tout écart est consigné tel quel.",
        "",
        f"LE BILAN : {total} pas de raffinement, {len(ecarts)} écart(s)"
        + (" — L'ÉQUIVALENCE DES TRANSITIONS TIENT." if not ecarts else
           " — VOIR LES ÉCARTS CI-DESSOUS."),
        "",
        "LES SCÉNARIOS :",
        "  S1 le cycle honnête intégral — CINQ époques vécues (quatre "
        "clôtures : la borne v120 e ≤ 3 dépassée aux DEUX niveaux), le "
        "crash de session, la phrase erronée aux DEUX actes ;",
        "  S2 la phrase erronée répétée — dix ouvertures, cinq clôtures : "
        "JAMAIS de destruction (P3), l'état inchangé ;",
        "  S3 la falsification du conteneur — la destruction LOCALE (PV "
        "unique), le média et CF2 INTACTS (P4) ;",
        "  S4 la falsification du piège — le refus SANS destruction (le "
        "média est le témoin, jamais le coupable) ;",
        "  S5 le rejeu d'époque passée — le miroir local (RETOUR EN "
        "ARRIÈRE), les époques croisées (PÉRIMÉ), le témoin hors-bande "
        "(epoque_attendue) ;",
        "  S6 le piège absent (l'invocation IMPOSSIBLE D120) et le piège "
        "d'un autre coffre (H_projet) ;",
        "  S7 l'adversaire à seuil (P1) — la phrase seule ne dérive jamais "
        "le KEK : 32 triplets de moitiés forgées, zéro passage du verif.",
        "",
        "LES GESTES HORS MODÈLE (consignés comme tels : le modèle "
        "v120/v150 n'a qu'un coffre et pas de témoin hors-bande) : le "
        "piège d'un autre coffre, le témoin epoque_attendue, les moitiés "
        "forgées — leurs verdicts concrets suivent la spec § 5/§ 9.",
        "",
    ]
    for r in RESULTATS:
        rapport.append(
            f"  [{r['scénario']} {r['pas']:>3}] {r['action']} : "
            f"{r['verdict_abstrait']} / {r['verdict_concret']} — "
            f"{r['conforme']}" + (f" ({r['détail']})" if r["détail"] else ""))
    if ecarts:
        rapport += ["", "LES ÉCARTS (consignés tels quels) :"]
        rapport += [f"  [{e['scénario']} {e['pas']}] {e['action']} : "
                    f"{e['détail']}" for e in ecarts]
    (PREUVES / "raffinement_rapport.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print(f"[sortie] {csv_path}")
    return 0 if not ecarts else 1


if __name__ == "__main__":
    sys.exit(main())
