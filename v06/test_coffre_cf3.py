#!/usr/bin/env python3
"""test_coffre_cf3.py — D121 : la falsifiabilité de la serrure CF3.

Une garde qui ne rejette rien ne garde rien (leçon M3). Cette suite prouve
les critères de sortie D121 un par un (spec docs/I/CF3/README.md § 13) :

  T1  le cycle en deux actes CONTRE TÉMOIN INDÉPENDANT : round-trip complet,
      époque incrémentée, checksum == sha256 recalculé par le TEST (pas par
      l'outil), moitiés serrure ET piège remplacées, sel_argon INVARIANT
      (la clé utilisateur ne change pas — la demande), piège ancien RELÈVE,
      re-scellement SANS changement (rotation pure), checksum de clôture ==
      checksum du verdict à froid, miroir local + journal consignés
  T2  phrase erronée (acte I) : PhraseErronee NOMMÉE, conteneur octet pour
      octet INTACT, AUCUN PV, journal nommé, délais croissants 1-2-4-8-8 ;
      borne : un piège ENTIÈREMENT FORGÉ (tag valide recomposé) se présente
      comme une phrase erronée — bénin, jamais de destruction
  T3  phrase erronée (acte II) : AUCUN scellement (média inchangé, conteneur
      md5 inchangé, brouillon lisible) PUIS le RÉESSAI réussit
  T4  piège absent (acte I, verdict, clôture) : IMPOSSIBLE nommé, rien lu,
      conteneur intact — sine qua non D120 réalisé sans démon
  T5  anti retour-en-arrière : piège PÉRIMÉ nommé ; couple restauré
      (conteneur@N + piège@N) REFUSÉ par le miroir local ; témoin
      hors-bande (--epoque-attendue) ; miroir corrompu = atteinte nommée
  T6  tag du piège invalide : refus SANS destruction (média hors limite de
      confiance — corruption bénigne possible)
  T7  falsification PROUVÉE côté machine (chiffretexte altéré) : destruction
      LOCALE (conteneur effacé, PV avec raison nommée, journal) ; média du
      piège octet pour octet INTACT ; COEXISTENCE : un fragment CF2 voisin
      et la config CF2 INTACTS ; relève nommée après mort
  T8  LA COURSE DE CLÔTURE : le KEK de clôture VOLÉ (dérivé par l'attaquant
      de laboratoire depuis les artefacts publics + la phrase — l'équivalent
      d'une scrape RAM) ne scelle RIEN d'ouvrable — variante 1a « étiquette
      menteuse, média intact » (en-tête H(B), chiffretexte B) : la cohérence
      H_projet du piège attrape le faux AVANT l'AEAD (défense en profondeur,
      refus sans effusion) ; variante 1b « étiquette menteuse + piège forgé
      sur le média » : l'AEAD REFUSE (KEK dérivé d'une autre info) ;
      variante 2 « étiquette honnête, contenu substitué » (en-tête H(A),
      chiffretexte B) : l'ÉTIQUETTE démasque (sha256(B) ≠ H(A)) — 1b et 2
      DÉTRUITES, jamais une ouverture
  T9  panne injectée à CHAQUE phase de la clôture : refus nommé, canonique
      INTACT, staging détruit, piège orphelin inoffensif, clôture rejouable ;
      panne APRÈS le replace : canonique à N+1, miroir en retard, réouverture
      VERTE (crash-cohérence) ; l'ordre d'init (piège avant conteneur) rend
      l'init rejouable après orphelin
  T10 brouillon falsifié en session : clôture REFUSÉE nommée, canonique
      intact, rien scellé
  T11 session : le brouillon est INDISSOCIABLE de sa clé de session (clé
      nulle → illisible), une session morte est écrasée avec l'aveu, l'abandon
      efface
  T12 CLI complet (sous-processus, comme le terrain) : init/statut/verifier/
      bruler/autotest — codes de sortie et refus NOMMÉS

Aucun conteneur réel ni phrase réelle n'est touché (répertoires temporaires
— discipline D105). Le sceau-I n'est pas touché : CE fichier vit hors v06/I/.
"""

import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import coffre_cf3 as C                     # noqa: E402

PHRASE = b"phrase-de-laboratoire-cf3-D121"
RESULTATS = []


def _verifie(temoin: str, condition: bool) -> None:
    RESULTATS.append((temoin, bool(condition)))
    print(f"[test-CF3] {temoin} : {'PASS' if condition else 'ECHEC'}")


def _octets(chemin: str) -> bytes:
    with open(chemin, "rb") as f:
        return f.read()


def _texte(chemin: str) -> str:
    with open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def _md5(chemin: str) -> str:
    return hashlib.md5(_octets(chemin)).hexdigest()


class Bac:
    """Répertoire temporaire : conteneur + média du piège séparés."""

    def __init__(self):
        self.rep = tempfile.mkdtemp(prefix="test-cf3-")
        self.conteneur = os.path.join(self.rep, "coffre_cf3.bin")
        self.media = os.path.join(self.rep, "media-piege")
        os.makedirs(self.media)

    def piege(self, epoque: int) -> str:
        return C.chemin_piege(self.media, epoque)

    def nettoyer(self):
        shutil.rmtree(self.rep, ignore_errors=True)


# ---------------------------------------------------------------------------
# T1 — le cycle en deux actes contre témoin indépendant
# ---------------------------------------------------------------------------

def t1_cycle_deux_actes():
    bac = Bac()
    try:
        res_init = C.init(PHRASE, bac.media, "suite-t1", bac.conteneur)
        _verifie("t1-init-epoque-1", res_init["epoque"] == 1)
        _verifie("t1-init-piege-sur-media",
                 os.path.isfile(bac.piege(1)))
        entete1 = C.parser_entete(_octets(bac.conteneur))
        piege1 = C.parser_piege(_texte(bac.piege(1)))

        # --- premier cycle : modification réelle
        session = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        base = session.lire()
        base["projets"]["triade"] = {"entrees": {"sceau-I": "vert"}}
        md5_avant = _md5(bac.conteneur)
        session.ecrire(base)
        _verifie("t1-canonique-intouchable-en-session",
                 _md5(bac.conteneur) == md5_avant)
        res = C.fermer(session, PHRASE, bac.media)

        _verifie("t1-epoque-incrementee", res["epoque"] == 2)
        # TÉMOIN INDÉPENDANT : le checksum est recalculé par le TEST
        _verifie("t1-checksum-temoin-independant",
                 res["checksum"] == hashlib.sha256(
                     C._serialiser(base)).digest()[:4].hex())
        entete2 = C.parser_entete(_octets(bac.conteneur))
        piege2 = C.parser_piege(_texte(bac.piege(2)))
        _verifie("t1-moitie-serrure-remplacee",
                 entete1["s_serrure"] != entete2["s_serrure"])
        _verifie("t1-moitie-piege-remplacee",
                 piege1["s_piege"] != piege2["s_piege"])
        _verifie("t1-cle-utilisateur-invariante",
                 entete1["sel_argon"] == entete2["sel_argon"])
        _verifie("t1-piege-ancien-releve", os.path.isfile(bac.piege(1)))

        # --- deuxième cycle : re-scellement SANS changement (rotation pure)
        session2 = C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
        _verifie("t1-contenu-exact-apres-cycle",
                 session2.lire()["projets"]["triade"]["entrees"]["sceau-I"]
                 == "vert")
        res2 = C.fermer(session2, PHRASE, bac.media)
        _verifie("t1-rotation-pure-epoque-3", res2["epoque"] == 3)
        _verifie("t1-rotation-pure-contenu-identique",
                 res2["checksum"] == res["checksum"]
                 and res2["empreinte"] == res["empreinte"])

        # --- le verdict à froid rend LE MÊME checksum (la carte recoupe)
        verdict = C.verifier(bac.conteneur, bac.piege(3), PHRASE)
        _verifie("t1-checksum-cloture-egal-verdict-froid",
                 verdict["checksum"] == res2["checksum"])

        # --- miroir local + journal consignés (aucun secret)
        miroir = _texte(C.chemin_miroir(bac.conteneur)).strip().split()
        _verifie("t1-miroir-local-consigne",
                 miroir[0] == "3" and miroir[1] == res2["checksum"])
        journal = _texte(C.chemin_journal(bac.conteneur))
        _verifie("t1-journal-clotures-consignees",
                 "CLÔTURE : époque 2" in journal
                 and "CLÔTURE : époque 3" in journal)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T2 — phrase erronée (acte I) : BÉNIGNE
# ---------------------------------------------------------------------------

def t2_phrase_erronee_acte1():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t2", bac.conteneur)
        octets_avant = _octets(bac.conteneur)
        try:
            C.ouvrir(bac.conteneur, bac.piege(1), b"mauvaise-phrase")
            _verifie("t2-phrase-erronee-refusee", False)
        except C.PhraseErronee as exc:
            _verifie("t2-phrase-erronee-refusee",
                     "phrase ERRONÉE" in str(exc))
        _verifie("t2-phrase-erronee-benigne",
                 _octets(bac.conteneur) == octets_avant
                 and not os.path.isdir(C.chemin_pv_dir(bac.conteneur)))
        journal = _texte(C.chemin_journal(bac.conteneur))
        _verifie("t2-journal-nomme-la-faute",
                 "phrase ERRONÉE" in journal)

        # délais croissants : 1, 2, 4, 8, 8 (le plafond borne l'auto-verrou)
        _verifie("t2-delais-croissants-plafonnes",
                 [C._delai_essai(i) for i in (1, 2, 3, 4, 5)]
                 == [1.0, 2.0, 4.0, 8.0, 8.0])

        # borne : un piège ENTIÈREMENT FORGÉ (tag recomposé valide) se
        # présente comme une phrase erronée — bénin
        entete = C.parser_entete(octets_avant)
        faux = C.serialiser_piege(entete["epoque"], entete["h_projet"],
                                  secrets.token_bytes(32),
                                  secrets.token_bytes(16))
        chemin_faux = os.path.join(bac.rep, "piege-forge.txt")
        with open(chemin_faux, "w", encoding="ascii") as f:
            f.write(faux)
        try:
            C.ouvrir(bac.conteneur, chemin_faux, PHRASE)
            _verifie("t2-piege-forge-refuse", False)
        except C.PhraseErronee:
            _verifie("t2-piege-forge-refuse", True)
        _verifie("t2-piege-forge-benigne",
                 _octets(bac.conteneur) == octets_avant
                 and not os.path.isdir(C.chemin_pv_dir(bac.conteneur)))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T3 — phrase erronée (acte II) : aucun scellement, réessai réussi
# ---------------------------------------------------------------------------

def t3_phrase_erronee_acte2():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t3", bac.conteneur)
        session = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        base = session.lire()
        base["projets"]["x"] = {"entrees": {"a": "b"}}
        session.ecrire(base)
        md5_avant = _md5(bac.conteneur)
        media_avant = sorted(os.listdir(bac.media))
        brouillon_avant = _octets(C.chemin_brouillon(bac.conteneur))
        try:
            C.fermer(session, b"mauvaise-phrase", bac.media)
            _verifie("t3-cloture-refusee", False)
        except C.PhraseErronee as exc:
            _verifie("t3-cloture-refusee",
                     "phrase ERRONÉE à la CLOTURE" in str(exc))
        _verifie("t3-aucun-scellage",
                 _md5(bac.conteneur) == md5_avant
                 and sorted(os.listdir(bac.media)) == media_avant
                 and not os.path.isfile(bac.conteneur + ".staging"))
        _verifie("t3-brouillon-intact",
                 _octets(C.chemin_brouillon(bac.conteneur))
                 == brouillon_avant)

        # le RÉESSAI avec la bonne phrase réussit
        res = C.fermer(session, PHRASE, bac.media)
        _verifie("t3-reessai-reussi", res["epoque"] == 2)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T4 — piège absent : le déverrouillage est IMPOSSIBLE
# ---------------------------------------------------------------------------

def t4_piege_absent():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t4", bac.conteneur)
        octets_avant = _octets(bac.conteneur)
        absent = os.path.join(bac.rep, "média-débranché")
        for appel, temoin in (
                (lambda: C.ouvrir(bac.conteneur, absent, PHRASE),
                 "t4-ouverture-impossible"),
                (lambda: C.verifier(bac.conteneur, absent, PHRASE),
                 "t4-verdict-impossible")):
            try:
                appel()
                _verifie(temoin, False)
            except C.ErreurCoffre as exc:
                _verifie(temoin, "ABSENTE" in str(exc)
                         and "IMPOSSIBLE" in str(exc))
        _verifie("t4-rien-lu-rien-brûlé",
                 _octets(bac.conteneur) == octets_avant
                 and not os.path.isdir(C.chemin_pv_dir(bac.conteneur)))

        # clôture : média débranché (le répertoire disparaît)
        session = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        shutil.rmtree(bac.media)
        try:
            C.fermer(session, PHRASE, bac.media)
            _verifie("t4-cloture-impossible", False)
        except C.ErreurCoffre as exc:
            _verifie("t4-cloture-impossible",
                     "clôture IMPOSSIBLE" in str(exc))
        _verifie("t4-cloture-sans-scellage",
                 _md5(bac.conteneur) == hashlib.md5(octets_avant).hexdigest())
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T5 — anti retour-en-arrière
# ---------------------------------------------------------------------------

def t5_retour_en_arriere():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t5", bac.conteneur)
        s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        C.fermer(s, PHRASE, bac.media)               # époque 2
        couple_conteneur = _octets(bac.conteneur)    # instantané époque 2
        couple_piege = _texte(bac.piege(2))
        s = C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
        C.fermer(s, PHRASE, bac.media)               # époque 3
        conteneur_epoque3 = _octets(bac.conteneur)

        # piège périmé : piège 2 contre conteneur 3
        with open(bac.piege(2), "w", encoding="ascii") as f:
            f.write(couple_piege)
        try:
            C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
            _verifie("t5-piege-perime-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t5-piege-perime-refuse", "PÉRIMÉ" in str(exc))

        # roll-back du COUPLE entier (conteneur@2 + piège@2) : le miroir
        # local dit 3 — REFUS nommé
        with open(bac.conteneur, "wb") as f:
            f.write(couple_conteneur)
        try:
            C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
            _verifie("t5-couple-restaure-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t5-couple-restaure-refuse",
                     "RETOUR EN ARRIÈRE" in str(exc))
        journal = _texte(C.chemin_journal(bac.conteneur))
        _verifie("t5-roll-back-journalise", "RETOUR EN ARR" in journal)

        # témoin hors-bande : le conteneur courant dit 3, la carte dit 2
        with open(bac.conteneur, "wb") as f:
            f.write(conteneur_epoque3)
        try:
            C.verifier(bac.conteneur, bac.piege(3), PHRASE,
                       epoque_attendue=2)
            _verifie("t5-temoin-hors-bande-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t5-temoin-hors-bande-refuse",
                     "témoin hors-bande" in str(exc))

        # miroir corrompu : une atteinte, pas une panne (écriture atomique)
        with open(C.chemin_miroir(bac.conteneur), "w", encoding="ascii") as f:
            f.write("xx\n")
        try:
            C.ouvrir(bac.conteneur, bac.piege(3), PHRASE)
            _verifie("t5-miroir-corrompu-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t5-miroir-corrompu-refuse",
                     "miroir d'époque corrompu" in str(exc))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T6 — tag du piège invalide : refus SANS destruction
# ---------------------------------------------------------------------------

def t6_tag_piege_invalide():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t6", bac.conteneur)
        octets_avant = _octets(bac.conteneur)
        piege_texte = _texte(bac.piege(1))
        # un hex du champ piege: basculé — le tag diverge
        lignes = piege_texte.splitlines()
        for i, l in enumerate(lignes):
            if l.startswith("piege: "):
                ancien = l[len("piege: "):]
                bascule = ("0" if ancien[0] != "0" else "1") + ancien[1:]
                lignes[i] = "piege: " + bascule
        with open(bac.piege(1), "w", encoding="ascii") as f:
            f.write("\n".join(lignes) + "\n")
        try:
            C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
            _verifie("t6-tag-invalide-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t6-tag-invalide-refuse",
                     "tag du piège INVALIDE" in str(exc)
                     and "refus SANS destruction" in str(exc))
        _verifie("t6-sans-destruction",
                 _octets(bac.conteneur) == octets_avant
                 and not os.path.isdir(C.chemin_pv_dir(bac.conteneur)))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T7 — falsification prouvée côté machine : destruction locale + coexistence
# ---------------------------------------------------------------------------

def t7_falsification_prouvee():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t7", bac.conteneur)
        # voisins CF2 (coexistence spec § 12) : un fragment et une config
        fragment_cf2 = os.path.join(bac.rep, "fragment-3.cf2f")
        config_cf2 = os.path.join(bac.rep, "config_cf2.json")
        with open(fragment_cf2, "w", encoding="ascii") as f:
            f.write("TRIADE-CF2-FRAG v1\ncoffre: aaa\n")
        with open(config_cf2, "w", encoding="utf-8") as f:
            f.write('{"conteneur": "x"}')
        fragment_avant = _octets(fragment_cf2)
        config_avant = _octets(config_cf2)

        blob = bytearray(_octets(bac.conteneur))
        blob[-1] ^= 0x01                    # un octet du chiffretexte
        with open(bac.conteneur, "wb") as f:
            f.write(bytes(blob))
        media_avant = _octets(bac.piege(1))
        try:
            C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
            _verifie("t7-falsification-detruite", False)
        except C.ErreurCoffre as exc:
            _verifie("t7-falsification-detruite",
                     "destruction LOCALE" in str(exc))
        _verifie("t7-conteneur-detruit", not os.path.isfile(bac.conteneur))
        _verifie("t7-media-intact", _octets(bac.piege(1)) == media_avant)
        _verifie("t7-fragments-cf2-intacts",
                 _octets(fragment_cf2) == fragment_avant
                 and _octets(config_cf2) == config_avant)
        pvs = os.listdir(C.chemin_pv_dir(bac.conteneur))
        _verifie("t7-pv-ecrit", len(pvs) == 1)
        pv = _texte(os.path.join(C.chemin_pv_dir(bac.conteneur), pvs[0]))
        _verifie("t7-pv-raison-nommee",
                 "PROUVÉE" in pv and "DETRUIT" in pv
                 and "le MÉDIA du piège est INTACT" in pv)
        journal = _texte(C.chemin_journal(bac.conteneur))
        _verifie("t7-journal-destruction", "DESTRUCTION LOCALE" in journal)
        # après la mort : la relève est nommée, pas muette
        try:
            C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
            _verifie("t7-coffre-mort-nomme", False)
        except C.ErreurCoffre as exc:
            _verifie("t7-coffre-mort-nomme", "conteneur ABSENT" in str(exc))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T8 — la course de clôture : KEK volé, les deux variantes du faux conteneur
# ---------------------------------------------------------------------------

def t8_course_de_cloture():
    bac = Bac()
    try:
        # état A (contenu que l'humain a vu et approuvé)
        C.init(PHRASE, bac.media, "suite-t8", bac.conteneur)
        s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        base_a = s.lire()
        base_a["projets"]["etat"] = {"entrees": {"contenu": "A"}}
        s.ecrire(base_a)
        res = C.fermer(s, PHRASE, bac.media)          # époque 2 — contenu A
        vrai = _octets(bac.conteneur)
        entete2 = C.parser_entete(vrai)
        piege2 = C.parser_piege(_texte(bac.piege(2)))
        h_a = entete2["h_projet"]

        # L'ATTAQUANT (white-box de laboratoire — l'équivalent d'une scrape
        # RAM à la clôture) : il connaît le format publié, la phrase (keylogger),
        # les artefacts publics et derive LE KEK DE CLÔTURE qui vient de servir.
        k_user = C.cle_utilisateur(PHRASE, entete2["sel_argon"])
        kek_vole = C.derive_kek(k_user, entete2["s_serrure"],
                                piege2["s_piege"], entete2["sel_hkdf"],
                                entete2["epoque"], h_a)

        # contenu B (l'état que le malware veut substituer)
        base_b = json.loads(json.dumps(base_a))
        base_b["projets"]["etat"]["entrees"]["contenu"] = "B-MALVEILLANT"
        clair_b = C._serialiser(base_b)
        h_b = hashlib.sha256(clair_b).digest()

        # variante 1a — étiquette MENTEUSE, média INTACT : en-tête H(B),
        # chiffretexte B sous le KEK volé (dérivé pour H(A)). Le VRAI piège
        # porte H(A) : la cohérence des champs publics attrape le faux
        # AVANT même l'AEAD (défense en profondeur) — refus SANS effusion.
        faux_menteur = C._sceller_avec_kek(
            clair_b, kek_vole, entete2["verif"], entete2["sel_argon"],
            entete2["sel_hkdf"], entete2["s_serrure"], entete2["epoque"],
            h_b)
        with open(bac.conteneur, "wb") as f:
            f.write(faux_menteur)
        try:
            C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
            _verifie("t8-etiquette-menteuse-refusee", False)
        except C.ErreurCoffre as exc:
            _verifie("t8-etiquette-menteuse-refusee",
                     "AUTRE coffre" in str(exc))
        _verifie("t8-etiquette-menteuse-refusee-sans-effusion",
                 os.path.isfile(bac.conteneur))

        # variante 1b — étiquette MENTEUSE + piège forgé sur le média
        # (l'attaquant a pu écrire le média pendant qu'il était branché —
        # la borne consignée) : même V_piège et S_piège RÉELS (sinon verif
        # diverge), étiquette H(B) — l'ouverture honnête dérive un KEK
        # AUTRE (info = H(B)) → AEAD REFUSÉ → destruction.
        piege_forges = os.path.join(bac.rep, "piege-forge-1b.txt")
        with open(piege_forges, "w", encoding="ascii") as f:
            f.write(C.serialiser_piege(entete2["epoque"], h_b,
                                       piege2["s_piege"], piege2["v_piege"]))
        with open(bac.conteneur, "wb") as f:
            f.write(faux_menteur)
        try:
            C.ouvrir(bac.conteneur, piege_forges, PHRASE)
            _verifie("t8-etiquette-menteuse-aead-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t8-etiquette-menteuse-aead-refuse",
                     "tag AEAD invalide" in str(exc))
        _verifie("t8-etiquette-menteuse-detruite",
                 not os.path.isfile(bac.conteneur))

        # variante 2 — étiquette HONNÊTE, contenu SUBSTITUÉ : en-tête H(A)
        # (copié du vrai), chiffretexte B sous le KEK volé : l'AEAD PASSE
        # (même KEK) mais l'ÉTIQUETTE démasque — sha256(B) ≠ H(A).
        with open(bac.conteneur, "wb") as f:
            f.write(vrai)                              # le vrai revient…
        faux_substitue = C._sceller_avec_kek(
            clair_b, kek_vole, entete2["verif"], entete2["sel_argon"],
            entete2["sel_hkdf"], entete2["s_serrure"], entete2["epoque"],
            h_a)
        with open(bac.conteneur, "wb") as f:
            f.write(faux_substitue)                    # …et repart substitué
        try:
            C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
            _verifie("t8-contenu-substitue-refuse", False)
        except C.ErreurCoffre as exc:
            _verifie("t8-contenu-substitue-refuse",
                     "étiquette H_projet" in str(exc))
        _verifie("t8-contenu-substitue-detruit",
                 not os.path.isfile(bac.conteneur))
        # D123 : DEUX destructions → DEUX PV DISTINCTS. Le rapport terrain
        # D122 a prouvé l'écrasement même-seconde (t8 rendait DEUX fois le
        # MÊME chemin) : l'ancien pvs[-1] ne passait QUE par ce bug —
        # chaque destruction laisse SON procès-verbal, les DEUX raisons
        # (AEAD refusé, substitution démasquée) restent lisibles.
        pvs = os.listdir(C.chemin_pv_dir(bac.conteneur))
        _verifie("t8-deux-destructions-deux-pv", len(pvs) == 2)
        pv_union = "\n".join(
            _texte(os.path.join(C.chemin_pv_dir(bac.conteneur), p))
            for p in pvs)
        _verifie("t8-pv-course-nommee", "course de clôture" in pv_union)
        _verifie("t8-pv-aead-et-substitution-tous-deux-ecrits",
                 "tag AEAD invalide" in pv_union
                 and "substitution PROUVÉE" in pv_union)

        # JAMAIS une ouverture : le vrai conteneur remis OUVRABLE, le faux
        # ne l'a jamais été — et le KEK volé ne scelle QUE l'état vu
        with open(bac.conteneur, "wb") as f:
            f.write(vrai)
        s = C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
        _verifie("t8-le-vrai-reste-ouvrable",
                 s.lire()["projets"]["etat"]["entrees"]["contenu"] == "A")
        _verifie("t8-jamais-une-ouverture-de-b",
                 s.lire()["projets"]["etat"]["entrees"]["contenu"] != "B")
        s.abandonner()
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T9 — panne injectée à chaque phase de la clôture + ordre d'init
# ---------------------------------------------------------------------------

def t9_pannes_de_cloture():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t9", bac.conteneur)
        md5_epoque1 = _md5(bac.conteneur)
        for point in ("avant-piege", "apres-piege", "apres-staging",
                      "avant-replace"):
            C._DEFAUT_SIMULE = point
            s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
            try:
                C.fermer(s, PHRASE, bac.media)
                _verifie(f"t9-panne-{point}-refusee", False)
            except C.ErreurCoffre as exc:
                _verifie(f"t9-panne-{point}-refusee",
                         "DÉFAUT SIMULÉ" in str(exc))
            C._DEFAUT_SIMULE = None
            _verifie(f"t9-panne-{point}-canonique-intact",
                     _md5(bac.conteneur) == md5_epoque1)
            _verifie(f"t9-panne-{point}-staging-detruit",
                     not os.path.isfile(bac.conteneur + ".staging"))
            # le piège orphelin est INOFFENSIF : le canonique N s'ouvre
            # toujours avec SON piège
            s2 = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
            _verifie(f"t9-panne-{point}-canonique-rejouable",
                     s2.lire()["description"] == "suite-t9")
            s2.abandonner()

        # panne APRÈS le replace, AVANT le miroir : canonique à N+1, miroir
        # en retard — la réouverture est VERTE (crash-cohérence spec § 6)
        C._DEFAUT_SIMULE = "apres-replace"
        s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        try:
            C.fermer(s, PHRASE, bac.media)
        except C.ErreurCoffre:
            pass
        C._DEFAUT_SIMULE = None
        _verifie("t9-apres-replace-canonical-a-n+1",
                 C.parser_entete(_octets(bac.conteneur))["epoque"] == 2)
        _verifie("t9-apres-replace-miroir-en-retard",
                 C._lire_miroir(bac.conteneur) == 1)
        s3 = C.ouvrir(bac.conteneur, bac.piege(2), PHRASE)
        _verifie("t9-apres-replace-reouverture-verte",
                 s3.lire()["description"] == "suite-t9")
        s3.abandonner()

        # l'ordre d'init (piège AVANT conteneur) : un orphelin de piège ne
        # bloque JAMAIS un init rejoué (pas de conteneur → coffre neuf)
        bac2 = Bac()
        try:
            with open(bac2.piege(1), "w", encoding="ascii") as f:
                f.write(C.serialiser_piege(1, secrets.token_bytes(32),
                                           secrets.token_bytes(32),
                                           secrets.token_bytes(16)))
            res = C.init(PHRASE, bac2.media, "rejoue", bac2.conteneur)
            _verifie("t9-init-rejouable-apres-orphelin",
                     res["epoque"] == 1
                     and os.path.isfile(bac2.conteneur))
        finally:
            bac2.nettoyer()
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T10 — brouillon falsifié en session : clôture refusée
# ---------------------------------------------------------------------------

def t10_brouillon_falsifie():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t10", bac.conteneur)
        s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        md5_avant = _md5(bac.conteneur)
        media_avant = sorted(os.listdir(bac.media))
        # un octet du brouillon altéré : sans K_session, indéchiffrable —
        # la clôture NE PEUT PAS sceller ce qu'elle ne relit pas
        blob = bytearray(_octets(C.chemin_brouillon(bac.conteneur)))
        blob[-1] ^= 0x01
        with open(C.chemin_brouillon(bac.conteneur), "wb") as f:
            f.write(bytes(blob))
        try:
            C.fermer(s, PHRASE, bac.media)
            _verifie("t10-cloture-refusee", False)
        except C.ErreurCoffre as exc:
            _verifie("t10-cloture-refusee",
                     "brouillon ILLISIBLE" in str(exc))
        _verifie("t10-rien-scellé",
                 _md5(bac.conteneur) == md5_avant
                 and sorted(os.listdir(bac.media)) == media_avant
                 and not os.path.isfile(bac.conteneur + ".staging"))
        s.abandonner()
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T11 — session : auto-nettoyage par panne
# ---------------------------------------------------------------------------

def t11_session():
    bac = Bac()
    try:
        C.init(PHRASE, bac.media, "suite-t11", bac.conteneur)
        s = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        blob = _octets(C.chemin_brouillon(bac.conteneur))
        # la clé de session meurt avec le processus : le brouillon devient
        # un déchet indéchiffrable (clé nulle = ce que sait un lecteur tiers)
        try:
            C._dechiffrer_brouillon(blob, bytearray(32))
            _verifie("t11-brouillon-déchet-sans-clé", False)
        except C.ErreurCoffre:
            _verifie("t11-brouillon-déchet-sans-clé", True)
        # le canonique est INTACT pendant que le brouillon vit
        _verifie("t11-canonique-scellé-pendant-la-session",
                 C.parser_entete(_octets(bac.conteneur))["epoque"] == 1)
        # une session morte est écrasée AVEC L'AVEU (l'avertissement est
        # le témoin — capturé sur stderr)
        s2 = C.ouvrir(bac.conteneur, bac.piege(1), PHRASE)
        _verifie("t11-nouvelle-session-écrase-le-déchet",
                 os.path.isfile(C.chemin_brouillon(bac.conteneur)))
        s2.abandonner()
        _verifie("t11-abandon-efface",
                 not os.path.isfile(C.chemin_brouillon(bac.conteneur)))
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------
# T12 — CLI complet (sous-processus, comme le terrain)
# ---------------------------------------------------------------------------

def _cli(conteneur, media, *args, stdin: bytes = b""):
    """conteneur/media = None → l'option n'est pas passée (statut, bruler,
    autotest ne portent pas --piege-dir ; autotest ne porte rien)."""
    commande = [sys.executable, os.path.join("v06", "coffre_cf3.py"), *args]
    if conteneur:
        commande += ["--conteneur", conteneur]
    if media:
        commande += ["--piege-dir", media]
    r = subprocess.run(commande, input=stdin, cwd=RACINE,
                       capture_output=True, timeout=600)
    return SimpleNamespace(code=r.returncode,
                           out=r.stdout.decode("utf-8", "replace"),
                           err=r.stderr.decode("utf-8", "replace"))


def t12_cli():
    bac = Bac()
    try:
        r = _cli(bac.conteneur, bac.media, "init", "--phrase-stdin",
                 "--description", "cli", stdin=PHRASE)
        _verifie("t12-init-code-0", r.code == 0)
        _verifie("t12-init-nomme-le-piege",
                 "piège posé sur le média" in r.out
                 and "checksum" in r.out)

        r = _cli(bac.conteneur, None, "statut")
        _verifie("t12-statut-etiquette",
                 r.code == 0 and "époque : 1" in r.out
                 and "BORNE" in r.out)

        r = _cli(bac.conteneur, bac.media, "verifier", "--phrase-stdin",
                 stdin=PHRASE)
        _verifie("t12-verifier-vert",
                 r.code == 0 and "VERDICT : VERT" in r.out
                 and "checksum" in r.out)

        r = _cli(bac.conteneur, bac.media, "verifier", "--phrase-stdin",
                 "--epoque-attendue", "2", stdin=PHRASE)
        _verifie("t12-verifier-temoin-divergent",
                 r.code == 1 and "témoin hors-bande" in r.err)

        r = _cli(bac.conteneur, bac.media, "verifier", "--phrase-stdin",
                 stdin=b"fausse-phrase")
        _verifie("t12-verifier-fausse-phrase",
                 r.code == 1 and "phrase ERRONÉE" in r.err)

        r = _cli(bac.conteneur, bac.media, "ouvrir", "--phrase-stdin",
                 stdin=PHRASE)
        _verifie("t12-ouvrir-vert",
                 r.code == 0 and "ACTE I : VERT" in r.out
                 and "DÉBRANCHER" in r.out)

        r = _cli(bac.conteneur, None, "bruler")
        _verifie("t12-bruler-exige-l-affirmation",
                 r.code == 1 and "--oui-je-comprends" in r.err)
        r = _cli(bac.conteneur, None, "bruler", "--oui-je-comprends")
        _verifie("t12-bruler-detruit-nommemment",
                 r.code == 0 and "DESTRUCTION LOCALE" in r.out
                 and not os.path.isfile(bac.conteneur))

        r = _cli(None, None, "autotest")
        _verifie("t12-autotest-vert", r.code == 0
                 and "0 ÉCHEC" in r.out)
    finally:
        bac.nettoyer()


# ---------------------------------------------------------------------------

def main() -> int:
    print("[test-CF3] suite de falsifiabilité D121 — spec docs/I/CF3/README.md § 13")
    for groupe in (t1_cycle_deux_actes, t2_phrase_erronee_acte1,
                   t3_phrase_erronee_acte2, t4_piege_absent,
                   t5_retour_en_arriere, t6_tag_piege_invalide,
                   t7_falsification_prouvee, t8_course_de_cloture,
                   t9_pannes_de_cloture, t10_brouillon_falsifie,
                   t11_session, t12_cli):
        print(f"\n[test-CF3] --- {groupe.__name__} ---")
        groupe()
    echecs = [t for t, ok in RESULTATS if not ok]
    print(f"\n[test-CF3] {len(RESULTATS) - len(echecs)} PASS / "
          f"{len(echecs)} ÉCHEC")
    if echecs:
        for t in echecs:
            print(f"[test-CF3] ÉCHEC : {t}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
