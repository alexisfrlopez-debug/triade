#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pbt_raffinement_v150.py — LE TEST PROPERTY-BASED MODÈLE ↔ IMPLÉMENTATION
(l'instruction 6zqo2h60n : « remplace le raffinement par scénarios par un
test property-based modèle↔implémentation : génération de ≥10 000 traces
aléatoires (graine consignée), vérification pas à pas, shrinking sur tout
écart, couverture des 13 règles et des chemins d'échec mesurée »).

LE PRINCIPE. Chaque trace pilote EN PARALLÈLE l'état ABSTRAIT du modèle
non borné (modele_invariant_v150.py, les 13 règles) et un coffre CONCRET
de test (v06/coffre_cf3.py, phrase de TEST publique marquée — D192 : le
coffre réel n'est JAMAIS ouvert par un test). À chaque pas : la MÊME
action abstraite et son geste concret (la table de correspondance du
raffinement_v150, étendue aux chemins de refus) ; les verdicts CONFRONTÉS
(époque, phase, destruction, PV, média) ; TOUT écart consigné, classé par
signature, RÉDUIT (shrinking ddmin) et archivé.

LA GRAINE : chaque trace i tire de random.Random((GRAIN, i)) — le
rejeu à graine identique reproduit les MÊMES tirages ; les verdicts ne
dépendent d'AUCUNE aléa du coffre (les sels/klés du coffre varient, les
verdicts qualitatifs non — l'égalité des condensés par trace le prouve
au rejeu).

LA TABLE DE CORRESPONDANCE (l'abstrait → le concret — gardes comprises,
l'ORDRE DE LA SENTINELLE respecté : la porte du piège avant la phrase) :

  ouvrir_correct (honnête)        → Session ouverte ; phase=brouillon
  ouvrir_correct (vole, seuil 3)  → Session ouverte ; le secret LU
      (session.lire() — le vol complet)
  ouvrir_correct refusé (piège)   → la PORTE refuse : IMPOSSIBLE (absent)
      ou refus SANS destruction (tag)
  ouvrir_correct refusé (seuil)   → le KEK indérivable : derive_verif à
      moitié forgée ≠ verif (le témoin de l'échec)
  ouvrir_phrase_erronée           → PhraseErronee (piège intègre) ou la
      PORTE (piège indisponible) — RIEN détruit (P3)
  ouvrir_ancien_couple            → « piège PÉRIMÉ » (époques croisées :
      conteneur courant + piège d'époque passée, la relève sur le média)
  rejoue_époque_passée             → « RETOUR EN ARRIÈRE » (le couple
      restauré contre le miroir courant)
  verifier                        → VERT (piège intègre) ou la PORTE —
      état inchangé
  crash_pendant_session           → abandonner() (brouillon) ou no-op
      (canonique) ; l'époque ne bouge pas
  clôturer_correcte               → fermer() : époque + 1 SANS plafond
  clôturer_correcte refusée       → la PORTE refuse (piège) : AUCUN
      scellement, l'époque ne bouge pas
  clôturer_phrase_erronée         → PhraseErronee (ou la PORTE) : AUCUN
      scellement
  falsifie_conteneur (piège intègre, canonique) → bit du chiffretexte
      + ouverture : destruction LOCALE + PV, le média INTACT (P4) — la
      trace s'ARRÊTE (le conteneur est mort)
  falsifie_conteneur refusée (piège indisponible) → la PORTE refuse :
      RIEN détruit, le bit altéré ne franchit jamais l'empreinte
  falsifie_piège                  → tag altéré ou fichier supprimé ; la
      PORTE refuse ensuite SANS destruction
  vole_K_user / vole_S_serrure / vole_S_piège → gestes abstraits (le
      savoir adverse) ; la contrepartie concrète vit aux ouvertures

LA FRONTIÈRE CONSIGNÉE : la falsification du conteneur pendant une
SESSION (phase brouillon, piège intègre) — le modèle REFUSE la règle (la
garde exige le canonique), le concret DÉTRUIT (la sentinelle court sur
le canonique, pas sur le brouillon) : l'ÉCART attendu, classé, réduit,
consigné comme la découverte de la campagne (les propriétés P1-P4 ne
sont pas en cause : la destruction reste PROUVÉE et LOCALE).

LE COÛT : le harnais MÉMORISE le KDF déterministe (phrase, sel) →
k_user (Argon2id déterministe : mêmes entrées, mêmes octets) — un appel
Argon2 par coffre, le reste en HKDF/AEAD.

Sorties : scripts/preuves_v150/pbt_raffinement.csv (une ligne par trace),
pbt_couverture.txt, pbt_ecarts.txt (les écarts réduits + analyses).
"""

from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import json
import pathlib
import random
import shutil
import sys
import tempfile
import time

REPO = pathlib.Path(__file__).resolve().parents[2]
PREUVES = REPO / "scripts" / "preuves_v150"
sys.path.insert(0, str(REPO / "v06"))
sys.path.insert(0, str(REPO / "scripts" / "preuves_v150"))

import coffre_cf3 as cf3          # noqa: E402
import modele_invariant_v150 as m150  # noqa: E402

PHRASE_TEST = (b"PHRASE-DE-TEST-PUBLIQUE-PBT-V150"
               b" - jamais une phrase reelle (D192)")
PHRASE_FAUSSE = b"phrase-erronee-pbt-v150 - jamais la vraie"

GRAIN = 20261112   # LA GRAINE CONSIGNÉE (le rejeu l'exige)

# le KDF déterministe mémoïsé (phrase, sel) → k_user
_KDF_CACHE: dict[tuple[bytes, bytes], bytes] = {}
_KDF_ORIG = cf3.cle_utilisateur


def cle_utilisateur_memo(phrase: bytes, sel: bytes) -> bytes:
    cle = (phrase, sel)
    if cle not in _KDF_CACHE:
        _KDF_CACHE[cle] = _KDF_ORIG(phrase, sel)
    return _KDF_CACHE[cle]


# ---------------------------------------------------------------------------
# le coffre de test concret
# ---------------------------------------------------------------------------

class CoffreTest:
    """Un coffre CONCRET de test : conteneur + média de piège + relèves."""

    def __init__(self, base: pathlib.Path, nom: str):
        self.dossier = base / nom
        shutil.rmtree(self.dossier, ignore_errors=True)  # résidu d'un run tué
        self.dossier.mkdir(parents=True)
        self.piege_dir = self.dossier / "media-piege"
        self.piege_dir.mkdir()
        self.conteneur = str(self.dossier / "coffre-cf3.bin")
        self.snapshots: dict[int, tuple[bytes, bytes]] = {}   # époque → (conteneur, piège)
        self.piege_supprime = False    # le piège COURANT supprimé (falsifie)
        self.session = None            # la Session ouverte (phase brouillon)

    # -- les observations --
    def epoque(self):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                return cf3.statut(self.conteneur)["epoque"]
        except cf3.ErreurCoffre:
            return None

    def vivant(self) -> bool:
        return pathlib.Path(self.conteneur).is_file()

    def nb_pv(self) -> int:
        pv_dir = cf3.chemin_pv_dir(self.conteneur)
        return len(list(pathlib.Path(pv_dir).glob("pv-*.txt"))) \
            if pathlib.Path(pv_dir).is_dir() else 0

    def nb_pieges(self) -> int:
        return len(list(self.piege_dir.glob("*")))

    def piege_path(self, epoque: int) -> str:
        return cf3.chemin_piege(str(self.piege_dir), epoque)

    def brouillon_existe(self) -> bool:
        return pathlib.Path(cf3.chemin_brouillon(self.conteneur)).is_file()

    # -- les gestes --
    def instant(self):
        with contextlib.redirect_stdout(io.StringIO()):
            cf3.init(PHRASE_TEST, str(self.piege_dir),
                     description="pbt v150", conteneur_chemin=self.conteneur)
        self.snapshot(1)

    def snapshot(self, epoque: int):
        self.snapshots[epoque] = (
            pathlib.Path(self.conteneur).read_bytes(),
            pathlib.Path(self.piege_path(epoque)).read_bytes())

    def flip_bit_conteneur(self):
        blob = bytearray(pathlib.Path(self.conteneur).read_bytes())
        blob[-1] ^= 0x01
        pathlib.Path(self.conteneur).write_bytes(bytes(blob))

    def corrompre_piege(self, epoque: int):
        piege = pathlib.Path(self.piege_path(epoque))
        lignes = piege.read_text("ascii").splitlines()
        lignes[-1] = ("0" if lignes[-1][0] != "0" else "1") + lignes[-1][1:]
        piege.write_text("\n".join(lignes) + "\n", "ascii")

    def supprimer_piege(self, epoque: int):
        p = pathlib.Path(self.piege_path(epoque))
        if p.is_file():
            p.unlink()
        self.piege_supprime = True

    def restaurer_piege(self, epoque: int):
        """Remet le piège courant dans l'état mémoire (corrompu/supprimé)."""
        p = pathlib.Path(self.piege_path(epoque))
        if self.piege_supprime:
            if p.is_file():
                p.unlink()
        # corrompu : le fichier altéré est déjà en place — rien à faire


def exce(fonction, *args, **kwargs):
    """Exécute et retourne ('ok', résultat) ou ('exc', exception).
    Les flux du coffre (stdout ET stderr) sont capturés : les verdicts
    vivent dans le retour, pas dans les journaux du coffre."""
    try:
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            return ("ok", fonction(*args, **kwargs))
    except Exception as exc:  # noqa: BLE001 — le verdict EST l'exception
        return ("exc", exc)


# ---------------------------------------------------------------------------
# le pas de trace : l'action abstraite + le geste concret + la confrontation
# ---------------------------------------------------------------------------

def pas(action, s, c, rng, journal: list):
    """Retourne (s_nouveau_ou_None_modèle, conforme, detail, trace_finie)."""
    genre = "adversaire" if action.startswith(("vole_", "falsifie_",
                                               "rejoue_")) else "protocole"
    s2 = m150.appliquer(s, action, genre)
    e, phase = s[0], s[1]
    conforme = True
    detail = ""
    fin = False

    def jg(texte):
        journal.append(f"{action}:{texte}")

    if action in ("vole_K_user", "vole_S_serrure", "vole_S_piège"):
        # geste abstrait ; la contrepartie vit aux ouvertures
        jg("savoir adverse" if s2 is not None else "refusé")
        if s2 is None:
            conforme, detail = False, "un vol ne peut pas être refusé"

    elif action == "falsifie_conteneur":
        pieges_avant = c.nb_pieges()
        c.flip_bit_conteneur()
        r = exce(cf3.ouvrir, c.conteneur, c.piege_path(e), PHRASE_TEST)
        if s2 is not None:
            # le modèle : destruction LOCALE — le concret DOIT détruire
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and not c.vivant() and c.nb_pv() == 1
                  and c.nb_pieges() == pieges_avant)
            conforme, fin = ok, True
            detail = ("destruction LOCALE + PV, média INTACT" if ok
                      else f"attendu detruit=True ; concret {r[0]} "
                           f"{str(r[1])[:60]} vivant={c.vivant()} "
                           f"PV={c.nb_pv()}")
            jg("detruit" if ok else "ÉCART-destruction")
        elif not s[3]:   # refusé : piège indisponible (trap_ok=False)
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.nb_pv() == 0)
            conforme = ok
            detail = ("la PORTE refuse : le bit altéré ne franchit jamais "
                      "l'empreinte" if ok else
                      f"attendu refus bénin ; concret {r[0]} "
                      f"{str(r[1])[:60]}")
            jg("refus-piège" if ok else "ÉCART-refus-piège")
        else:
            # refusé pour PHASE=brouillon, piège intègre : le concret
            # DÉTRUIT (la sentinelle court sur le canonique) — L'ÉCART
            # ATTENDU, la découverte consignée de la campagne
            detruit_concret = (r[0] == "exc" and not c.vivant()
                               and c.nb_pv() == 1)
            conforme, fin = False, True
            detail = ("ÉCART CLASSE brouillon-falsification : le modèle "
                      "refuse (garde canonique), le concret DÉTRUIT "
                      "(sentinelle sur le canonique, PV=1, média intact) — "
                      "P3/P4 non en cause : destruction PROUVÉE et LOCALE"
                      if detruit_concret else
                      f"ÉCART brouillon : concret inattendu {r[0]} "
                      f"{str(r[1])[:60]}")
            jg("ÉCART-brouillon-falsification")

    elif action == "falsifie_piège":
        if s2 is not None:
            mode = rng.choice(["corrompt", "supprime"])
            if mode == "corrompt":
                c.corrompre_piege(e)
            else:
                c.supprimer_piege(e)
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(e), PHRASE_TEST)
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.nb_pv() == 0
                  and c.epoque() == e)
            conforme = ok
            detail = (f"tag {mode} → la PORTE refuse SANS destruction"
                      if ok else f"attendu refus bénin ; {str(r[1])[:60]}")
            jg(f"{mode}-refus" if ok else "ÉCART")
        else:
            jg("déjà indisponible")
            conforme = c.vivant() and c.nb_pv() == 0

    elif action == "rejoue_époque_passée":
        if s2 is not None:
            eo = rng.choice([x for x in sorted(c.snapshots) if x < e])
            conteneur_cur = pathlib.Path(c.conteneur).read_bytes()
            piege_cur_existe = pathlib.Path(c.piege_path(e)).is_file()
            piege_cur = (pathlib.Path(c.piege_path(e)).read_bytes()
                         if piege_cur_existe else None)
            pathlib.Path(c.conteneur).write_bytes(c.snapshots[eo][0])
            pathlib.Path(c.piege_path(eo)).write_bytes(c.snapshots[eo][1])
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(eo), PHRASE_TEST)
            # restauration de l'état courant (conteneur + piège courant)
            pathlib.Path(c.conteneur).write_bytes(conteneur_cur)
            if piege_cur_existe:
                pathlib.Path(c.piege_path(e)).write_bytes(piege_cur)
            ok = (r[0] == "exc" and "RETOUR EN ARRIÈRE" in str(r[1])
                  and c.vivant() and c.nb_pv() == 0 and c.epoque() == e)
            conforme = ok
            detail = (f"couple d'époque {eo} restauré → RETOUR EN ARRIÈRE, "
                      "état inchangé" if ok else
                      f"attendu RETOUR EN ARRIÈRE ; {str(r[1])[:60]}")
            jg("rejeté-nommé" if ok else "ÉCART")
        else:
            jg("rien à rejouer (e=1)")
            conforme = c.vivant() and c.nb_pv() == 0

    elif action == "ouvrir_correct":
        if not s[3]:   # piège indisponible : la PORTE
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(e), PHRASE_TEST)
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.nb_pv() == 0)
            conforme = ok
            detail = ("la PORTE refuse (piège indisponible)" if ok
                      else f"attendu refus porte ; {str(r[1])[:60]}")
            jg("refus-piège" if ok else "ÉCART")
        elif s2 is None:   # K_user volé seul : le KEK indérivable
            blob = pathlib.Path(c.conteneur).read_bytes()
            entete = cf3.parser_entete(blob)
            k_user = cle_utilisateur_memo(PHRASE_TEST, entete["sel_argon"])
            faux_v = rng.randbytes(32)
            if cf3.derive_verif(k_user, faux_v, entete["sel_hkdf"]) \
                    == entete["verif"]:
                conforme, detail = False, ("une moitié forgée PASSE le "
                                           "verif — IMPOSSIBLE (P1 rompue)")
            else:
                detail = "le KEK indérivable : verif jamais atteint (P1)"
            jg("refus-seuil" if conforme else "ÉCART-P1")
        else:
            r = exce(cf3.ouvrir, c.conteneur, c.piege_path(e), PHRASE_TEST)
            session = r[1] if r[0] == "ok" else None
            lu = None
            if session is not None:
                with contextlib.redirect_stdout(io.StringIO()):
                    lu = session.lire()
            ok = (session is not None and session.epoque == e
                  and c.vivant() and c.nb_pv() == 0 and lu is not None
                  and c.brouillon_existe())
            conforme = ok
            c.session = session
            detail = ("session époque " + str(e) + " ; le clair LU"
                      + (" — le vol au seuil COMPLET" if s2[5] else "")
                      if ok else f"attendu session ; {r[0]} {str(r[1])[:60]}")
            jg("session" if ok else "ÉCART")

    elif action == "ouvrir_phrase_erronée":
        r = exce(cf3.ouvrir, c.conteneur, c.piege_path(e), PHRASE_FAUSSE)
        if s[3]:   # piège intègre : PhraseErronee
            ok = (r[0] == "exc" and isinstance(r[1], cf3.PhraseErronee)
                  and c.vivant() and c.nb_pv() == 0 and c.epoque() == e)
            detail = "PhraseErronee, RIEN détruit (P3)" if ok \
                else f"attendu PhraseErronee ; {str(r[1])[:60]}"
        else:      # la PORTE (le piège indisponible passe AVANT la phrase)
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.nb_pv() == 0)
            detail = ("la PORTE refuse avant la phrase (le piège "
                      "indisponible — le modèle dit : état inchangé)"
                      if ok else f"attendu refus porte ; {str(r[1])[:60]}")
        conforme = ok
        jg("phrase-erronée" if ok else "ÉCART")

    elif action == "ouvrir_ancien_couple":
        eo = rng.choice([x for x in sorted(c.snapshots) if x < e])
        r = exce(cf3.ouvrir, c.conteneur, c.piege_path(eo), PHRASE_TEST)
        ok = (r[0] == "exc" and "PÉRIMÉ" in str(r[1])
              and c.vivant() and c.nb_pv() == 0 and c.epoque() == e)
        conforme = ok
        detail = (f"piège d'époque {eo} contre conteneur {e} → PÉRIMÉ"
                  if ok else f"attendu PÉRIMÉ ; {str(r[1])[:60]}")
        jg("périmé" if ok else "ÉCART")

    elif action == "verifier":
        r = exce(cf3.verifier, c.conteneur, c.piege_path(e), PHRASE_TEST)
        if s[3]:
            ok = (r[0] == "ok" and r[1]["epoque"] == e
                  and c.vivant() and c.nb_pv() == 0)
            detail = f"VERT époque {e}" if ok \
                else f"attendu VERT ; {r[0]} {str(r[1])[:60]}"
        else:
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.nb_pv() == 0)
            detail = "la PORTE refuse (piège indisponible)" if ok \
                else f"attendu refus porte ; {str(r[1])[:60]}"
        conforme = ok
        jg("vert" if ok else "ÉCART")

    elif action == "crash_pendant_session":
        if phase == "brouillon" and c.session is not None:
            with contextlib.redirect_stdout(io.StringIO()):
                c.session.abandonner()
            c.session = None
            ok = (c.vivant() and c.epoque() == e and not c.brouillon_existe())
            detail = "abandonner() : le brouillon meurt, l'époque tient"
        else:
            ok = c.vivant() and c.epoque() == e
            detail = "no-op au canonique (le modèle : identité)"
        conforme = ok
        jg("crash" if ok else "ÉCART")

    elif action == "clôturer_correcte":
        r = exce(cf3.fermer, c.session, PHRASE_TEST, str(c.piege_dir)) \
            if c.session is not None else ("exc", "pas de session")
        if s2 is not None:
            ok = (r[0] == "ok" and r[1]["epoque"] == e + 1
                  and c.vivant() and c.nb_pv() == 0
                  and pathlib.Path(c.piege_path(e + 1)).is_file()
                  and not c.brouillon_existe())
            if ok:
                c.session = None
                c.piege_supprime = False    # le piège NEUF est posé
                c.snapshot(e + 1)
                detail = f"fermer : époque {e}→{e + 1} SANS plafond"
            else:
                detail = f"attendu e={e + 1} ; {r[0]} {str(r[1])[:60]}"
        else:   # refusée : la PORTE (piège indisponible)
            ok = (r[0] == "exc" and isinstance(r[1], cf3.ErreurCoffre)
                  and c.vivant() and c.epoque() == e
                  and c.nb_pv() == 0
                  and not pathlib.Path(c.piege_path(e + 1)).is_file())
            detail = ("la PORTE refuse : AUCUN scellement" if ok
                      else f"attendu refus ; {str(r[1])[:60]}")
        conforme = ok
        jg("clôture" if ok else "ÉCART")

    elif action == "clôturer_phrase_erronée":
        r = exce(cf3.fermer, c.session, PHRASE_FAUSSE, str(c.piege_dir)) \
            if c.session is not None else ("exc", "pas de session")
        ok = (r[0] == "exc" and c.vivant() and c.epoque() == e
              and c.nb_pv() == 0
              and not pathlib.Path(c.piege_path(e + 1)).is_file())
        conforme = ok
        detail = ("PhraseErronee (ou la PORTE) : AUCUN scellement" if ok
                  else f"attendu refus bénin ; {str(r[1])[:60]}")
        jg("phrase-erronée-clôture" if ok else "ÉCART")

    else:
        conforme, detail = False, f"action INCONNUE {action}"
        jg("inconnue")

    # la contre-vérification permanente (l'état concret ↔ l'abstrait,
    # à L'ÉTAT POST-PAS : s2 si l'action vit, s sinon)
    s_ref = s2 if s2 is not None else s
    if c.vivant():
        if c.epoque() != s_ref[0]:
            conforme, detail = False, \
                f"ÉPOQUE divergente : concret {c.epoque()} ≠ modèle {s_ref[0]}"
        attendu_pv = 1 if (s_ref[7]) else 0
        if c.nb_pv() != attendu_pv:
            conforme, detail = False, \
                f"PV divergent : {c.nb_pv()} ≠ {attendu_pv}"
        if c.brouillon_existe() != (s_ref[1] == "brouillon"):
            conforme, detail = False, \
                (f"PHASE divergente : brouillon={c.brouillon_existe()} "
                 f"≠ modèle {s_ref[1]}")
    return s2, conforme, detail, fin


# ---------------------------------------------------------------------------
# la génération des traces (les tirages de actions_possibles, pondérés)
# ---------------------------------------------------------------------------

def action_offertes(s) -> list[tuple[str, int]]:
    e, phase = s[0], s[1]
    offres: list[tuple[str, int]] = []
    if phase == "canonique":
        offres += [("ouvrir_correct", 2), ("ouvrir_phrase_erronée", 1),
                   ("verifier", 1), ("crash_pendant_session", 1)]
        if e > 1:
            offres += [("ouvrir_ancien_couple", 1)]
    else:
        offres += [("clôturer_correcte", 2), ("clôturer_phrase_erronée", 1),
                   ("crash_pendant_session", 1)]
    offres += [("vole_K_user", 1), ("vole_S_serrure", 1), ("vole_S_piège", 1),
               ("falsifie_conteneur", 1), ("falsifie_piège", 1),
               ("rejoue_époque_passée", 1)]
    return offres


def jouer_trace(idx: int, base: pathlib.Path, actions_forcees=None):
    """Joue la trace idx ; retourne (lignes_journal, écarts, fin, couverture,
    actions). Si actions_forcees : rejoue la liste donnée (le shrinking)."""
    rng = random.Random(f"{GRAIN}:{idx}")
    c = CoffreTest(base, f"t{idx}")
    try:
        c.instant()
    except Exception as exc:  # noqa: BLE001
        return ([f"init ÉCHEC {exc}"], [(f"init", str(exc))], True, {})
    s = m150.etat_initial()
    journal: list[str] = []
    écarts = []
    couverture = {}
    fin = "longueur"
    actions_jouees = []
    try:
        n_pas = rng.randint(3, 8) if actions_forcees is None \
            else len(actions_forcees)
        for i in range(n_pas):
            if actions_forcees is None:
                offres = action_offertes(s)
                actions = [a for a, _ in offres]
                poids = [p for _, p in offres]
                action = rng.choices(actions, weights=poids, k=1)[0]
            else:
                if i >= len(actions_forcees):
                    break
                action = actions_forcees[i]
            actions_jouees.append(action)
            s_avant = s
            s2, conforme, detail, fini = pas(action, s, c, rng, journal)
            couverture.setdefault(action, {"tirés": 0, "acceptés": 0,
                                           "refusés": 0})
            couverture[action]["tirés"] += 1
            if s2 is None:
                couverture[action]["refusés"] += 1
            else:
                couverture[action]["acceptés"] += 1
            if not conforme:
                écarts.append((i, action, detail,
                               sig_écart(action, s_avant, s2)))
            if fini:
                fin = "destruction"
                break
            if s2 is not None:
                s = s2
    finally:
        shutil.rmtree(c.dossier, ignore_errors=True)
    return journal, écarts, fin, couverture, actions_jouees


def sig_écart(action, s, s2) -> str:
    """La signature de classe d'un écart (pour le regroupement)."""
    return (f"{action}|phase={s[1]}|trap={s[3]}|"
            f"seuil={len(s[2] & m150.ELEMENTS)}")


# ---------------------------------------------------------------------------
# MAIN (par plages : --debut/--fin — le rejeu à graine identique)
# ---------------------------------------------------------------------------

def reduire_trace(idx, base, actions, action_cible, phase_cible):
    """Le shrinking glouton : retire un pas à la fois tant que l'écart de
    la classe cible (action, phase) survient — la trace minimale."""
    def ecart_classe_presente(lst):
        _, écarts, _, _, _ = jouer_trace(idx, base, actions_forcees=lst)
        return any(e[1] == action_cible
                   and e[3].split("|")[1] == f"phase={phase_cible}"
                   for e in écarts)

    courante = list(actions)
    if not ecart_classe_presente(courante):
        return courante, False
    i = 0
    while i < len(courante):
        essai = courante[:i] + courante[i + 1:]
        if essai and ecart_classe_presente(essai):
            courante = essai
        else:
            i += 1
    return courante, True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--debut", type=int, default=0)
    ap.add_argument("--fin", type=int, default=200)
    ap.add_argument("--base", default=str(PREUVES / "pbt_zone"))
    ap.add_argument("--shrink", action="store_true",
                    help="réduit TOUTES les traces à écarts (ddmin glouton)")
    ap.add_argument("--shrink-saute", type=int, default=0,
                    help="saute les N premières traces à écarts (découpage)")
    ap.add_argument("--replay", action="store_true",
                    help="rejoue à graine identique vers pbt_traces_rejeu.csv")
    args = ap.parse_args()

    cf3.cle_utilisateur = cle_utilisateur_memo
    base = pathlib.Path(args.base)
    base.mkdir(parents=True, exist_ok=True)
    csv_path = PREUVES / ("pbt_traces_rejeu.csv" if args.replay
                          else "pbt_traces.csv")

    t0 = time.time()
    nouvelles = []
    couv_globale: dict[str, dict] = {}
    écarts_globaux = []
    act_path = PREUVES / "pbt_traces_ecarts.jsonl"
    for idx in range(args.debut, args.fin):
        journal, écarts, fin, couverture, actions = jouer_trace(idx, base)
        digest = hashlib.sha256(
            "|".join(journal).encode("utf-8")).hexdigest()
        nouvelles.append({"trace": idx, "pas": len(journal),
                          "digest": digest, "écarts": len(écarts),
                          "fin": fin})
        for a, d in couverture.items():
            g = couv_globale.setdefault(a, {"tirés": 0, "acceptés": 0,
                                            "refusés": 0})
            for k in g:
                g[k] += d[k]
        for (i, action, detail, sig) in écarts:
            écarts_globaux.append({"trace": idx, "pas": i,
                                   "action": action, "signature": sig,
                                   "détail": detail})
        if écarts:
            with open(act_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({"trace": idx, "actions": actions,
                                    "signatures": [e[3] for e in écarts]})
                        + "\n")
    duree = time.time() - t0

    existe = csv_path.is_file()
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["trace", "pas", "digest",
                                          "écarts", "fin"])
        if not existe:
            w.writeheader()
        w.writerows(nouvelles)

    if args.replay:
        # la comparaison des verdicts trace à trace (la STABILITÉ exigée)
        orig = {int(r["trace"]): r for r in csv.DictReader(
            open(PREUVES / "pbt_traces.csv", encoding="utf-8"))}
        stables = divergents = 0
        for n in nouvelles:
            o = orig.get(n["trace"])
            if o and o["digest"] == n["digest"] and o["fin"] == n["fin"]:
                stables += 1
            else:
                divergents += 1
                print(f"[rejeu] DIVERGENCE trace {n['trace']}")
        print(f"[rejeu] {stables} stables, {divergents} divergentes "
              f"(sur {len(nouvelles)})")
        return 0 if divergents == 0 else 1

    ec_path = PREUVES / "pbt_ecarts_brut.csv"
    existe_ec = ec_path.is_file()
    with open(ec_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["trace", "pas", "action",
                                          "signature", "détail"])
        if not existe_ec:
            w.writeheader()
        w.writerows(écarts_globaux)

    if args.shrink:
        act_path = PREUVES / "pbt_traces_ecarts.jsonl"
        if not act_path.is_file():
            print("[shrink] aucune trace à écarts")
            return 0
        lignes = [json.loads(x) for x in
                  act_path.read_text(encoding="utf-8").splitlines() if x]
        resultats = []
        vus = set()
        for ent in lignes[args.shrink_saute:]:
            print(f"[shrink] trace {ent['trace']}…", flush=True)
            cle = tuple(ent["signatures"])
            sig0 = ent["signatures"][0].split("|")
            action_cible, phase_cible = sig0[0], sig0[1][len("phase="):]
            if (ent["trace"], cle) in vus:
                continue
            vus.add((ent["trace"], cle))
            minimal, ok = reduire_trace(ent["trace"], base, ent["actions"],
                                        action_cible, phase_cible)
            resultats.append({"trace": ent["trace"], "classe": sig0[0],
                              "phase": phase_cible,
                              "minimale": minimal, "réduite": ok})
        sortie = PREUVES / ("pbt_ecarts_minimaux.json"
                            if args.shrink_saute == 0 else
                            f"pbt_ecarts_minimaux_{args.shrink_saute}.json")
        with open(sortie, "w", encoding="utf-8") as f:
            json.dump(resultats, f, ensure_ascii=False, indent=1)
        print(f"[shrink] {len(resultats)} trace(s) à écarts réduites "
              f"→ {sortie.name}")
        return 0

    print(f"[pbt] traces {args.debut}..{args.fin - 1} : "
          f"{len(nouvelles)} traces en {duree:.1f} s "
          f"({duree / max(1, len(nouvelles)) * 1000:.0f} ms/trace), "
          f"{len(écarts_globaux)} écart(s)")
    for a in sorted(couv_globale):
        d = couv_globale[a]
        print(f"  {a:26s} tirés={d['tirés']:>6} acceptés={d['acceptés']:>6} "
              f"refusés={d['refusés']:>6}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
