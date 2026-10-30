#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ceremonie_gui.py — TRIADE v0.6.0 : le MAÎTRE DE CÉRÉMONIE graphique.

UN SEUL FICHIER PYTHON, ZÉRO LIGNE DE COMMANDE (si ce n'est le lancer) :
    python3 ceremonie_gui.py            (ou double-clic via lancer_ceremonie)

Il couvre les DEUX cérémonies de souveraineté v0.6.0 (D105/D106) :

  PROFIL « HORS-LIGNE » (machine air-gap, cérémonie de la clé I, D87) :
    - stdlib PURE + tkinter — rien à installer, aucun réseau, aucun pip ;
    - l'implémentation Ed25519 RFC 8032 est EMBARQUÉE (copie conforme de
      v06/ceremonie_hors_ligne.py, attestée par test_ceremonie_gui.py T1 :
      vecteurs RFC § 7.1 + interop « cryptography » quand elle existe) ;
    - générée / signe / vérifie EXACTEMENT les mêmes fichiers que le script
      console (interopérable : la remise GUI entre dans sceau_I.py tel quel).

  PROFIL « DÉPÔT » (machine connectée, à côté du dépôt triade) :
    - le dépôt est trouvé par ordre D111 : --depot CHEMIN sur la ligne de
      lancement, sinon la variable d'environnement TRIADE_DEPOT, sinon la
      position du fichier lui-même (le dépôt complet : ce fichier vit dans
      <dépôt>/v06/) — un chemin faux est un échec NOMMÉ (code 2), un
      dossier sans v06/coffre_cf2.py laisse le profil désactivé avec la
      cause affichée à l'accueil (fail-closed, jamais deviné) ;
    - D112 : les TROIS chemins se choisissent DANS LA FENÊTRE — le dossier
      du dépôt (bouton « Choisir le dossier du dépôt… », garde
      v06/coffre_cf2.py, re-attachement à chaud, échec nommé), le coffre
      CF1 (champ + Parcourir, câblé à --chemin pour statut/verifier/
      changer-phrase et à --depuis pour la migration), et la clé privée I
      (onglet Signer : fichier OU saisie manuelle des 64 hex — entrée
      masquée, validée vivante, effacée après l'acte, jamais affichée) ;
    - phrase de contrôle CF1 : mettez la VÔTRE — alphanumérique (A-Z a-z
      0-9), 8 caractères minimum, AUCUN plafond de longueur (D110) ;
      l'ancienne devient inopérante, la remise D81 se remplace après ;
    - sceau I : preparer / deposer / verifier / etat (CLI sous-jacent) ;
    - coffre CF2 : statut / verifier / migrer (phrase masquée) / export des
      fragments en feuille imprimable / CONTRÔLE DE RELECTURE des copies
      hors-ligne / liste blanche éditée par formulaire / sentinelle
      (démarrage détaché + santé) / restaurer / brûler (confirmation tapée) ;
    - les commandes passent par les CLI existants en sous-processus et la
      sortie coule dans le journal : le fail-closed des CLI reste LA loi,
      le GUI n'est qu'un habit (aucune logique critique dupliquée) ;
    - D113 — BOÎTE NOIRE : tout ce que la fenêtre affiche, chaque dialogue
      posé (et sa réponse), chaque verdict et CHAQUE CRASH de rappel
      tkinter atterrit dans v06/ceremonie-journal.log (fichier local,
      horodaté, AUCUN réseau — la discipline hors-ligne reste entière) ; le
      bouton « Envoyer le rapport… » constitue le fichier à remettre À LA
      MAIN à l'assistant (glisser dans la conversation) : le GUI ne prend
      pas de réseau pour se faire débugger ;
    - D113 — le journal ne peut plus être évincé : barre de verdict et
      journal se packent AVANT le corps (l'ordre de pack est la priorité
      d'espace — avant, la page dépôt, ~1000 px demandés, poussait le
      journal hors de la fenêtre : « aucun journal qui s'affiche »), et le
      corps DÉFILE (une page plus haute que la fenêtre reste entièrement
      atteignable) ; les dialogues passent TOUJOURS au-dessus de la fenêtre
      (parent explicite — un dialogue sans parent peut naître DERRIÈRE et
      faire croire le GUI mort : « je clique, rien ne se passe ») ;
    - D116 — LA FENÊTRE SUIT SON CONTENU : plus de géométrie fixe —
      chaque page affichée redimensionne la fenêtre (clampée à l'écran,
      minsize 880x600) ; « ← Accueil » vit dans le BANDEAU, toujours
      visible (jamais plus chassé en bas d'une page trop haute) ;
    - D116 — FIL DE CÉRÉMONIE : les cinq étapes du sceau I (Préparer →
      Générer la clé → Signer → Déposer → Git) s'auto-détectent par
      PREUVES en lecture seule (a-signer frais ? paire de clés ? remise
      vérifiée ? arbres verts ? git propre ?) ; l'étape satisfaite
      s'efface, la suivante s'affiche — ré-évaluation après chaque
      verdict ET validation manuelle possible (« Marquer faite (à la
      main) » — la preuve de fichier reste la vérité) ;
    - D116 — GIT : « Pousser v06/sceau-I sur git… » (add ciblé SEUL —
      jamais « add -A », la clé privée vit hors du dépôt — commit nommé,
      pull --rebase AVANT push : le push rejeté du terrain D113-115 ne se
      reproduira plus silencieusement, échecs nommés étape par étape) ;
    - D117 — LE SCÉNARIO AVANT TOUT : l'accueil s'ouvre sur le CHOIX entre
      deux scénarios qui déterminent les étapes affichées par le fil de
      cérémonie — « DOSSIER LOCAL » (le dépôt vit déjà sur cette machine :
      on l'attache, fil de CINQ étapes) et « REPO GIT » (le dépôt vient
      d'un distant : fil de SIX étapes avec « Cloner le dépôt » en tête,
      prouvé lecture seule par git rev-parse + origin) ; le scénario git
      donne un panneau « Cloner en local… » (URL + dossier parent + nom,
      destination non vide refusée NOMMÉ, URL ou destination commençant
      par « - » refusée : un argument git déguisé est une injection,
      git absent : code 127 nommé, jeton éventuel de l'URL MASQUÉ dans
      journal, verdict et boîte noire) et « Attacher un clone
      EXISTANT… » (garde D111 + preuve git/origin exigée) ; après un
      clone réussi le dépôt est ATTACHÉ et les pages REBÂTIES (le profil
      dépôt s'ouvre directement — le journal survit, discipline D112) ;

DISCIPLINE (inchangée — le GUI ne l'assouplit JAMAIS) :
  - la clé privée I ne traverse ni le bac à sable, ni le réseau, ni git ;
  - toute action destructrice exige une confirmation EXPLICITE (brûler :
    taper « BRULER » en toutes lettres) ;
  - la graine n'est JAMAIS affichée à l'écran : le fichier est la remise ;
  - fail-closed d'abord : l'autotest RFC 8032 précède toute génération ou
    signature ; un échec nommé n'écrit rien.

DÉPENDANCES : tkinter (inclus dans python.org Windows/macOS ; Linux :
  sudo apt install python3-tk — c'est la SEULE pièce hors pip). Le profil
  dépôt veut la PILE DU DÉPÔT (pynacl + cryptography, cf. coffre_cf2.py) :
  le GUI la vérifie et propose de l'installer (pip, avec votre accord) si
  elle manque ; le profil hors-ligne reste stdlib pure, sans exception.

BORNES HONNÊTES : le profil hors-ligne n'exige RIEN et n'installe RIEN
  (c'est le point D87). tkinter lui-même ne s'installe pas via pip : si
  absent, le script affiche la commande exacte de votre plateforme et
  s'arrête proprement. La sentinelle démarrée depuis le GUI vit détachée :
  sa santé se contrôle par le bouton « Santé » (heart-beat).

Modes : (aucun) → GUI ; --selftest → batterie embarquée headless ;
  --profil hors-ligne|depot → saute l'écran d'accueil ;
  --depot CHEMIN → attache le GUI à ce dépôt triade (D111 : le GUI
  peut vivre N'IMPORTE OÙ — clef USB, kit du Drive, bureau — tant que
  CHEMIN désigne la racine d'un clone du dépôt : v06/coffre_cf2.py y
  est vérifié AVANT d'activer le profil dépôt). D112 : le même
  attachement se fait AUSSI depuis la fenêtre (accueil, bouton
  « Choisir le dossier du dépôt… ») — la ligne de commande devient un
  RACCOURCI, plus une obligation.
"""

import argparse
import datetime   # D113 : horodatage de la boîte noire
import os
import platform   # D113 : environnement du rapport
import sys
import traceback  # D113 : crashes complets dans la boîte noire

# --- confort console Windows (accents français) ---------------------------
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


class ErreurCeremonie(RuntimeError):
    """Échec NOMMÉ de cérémonie — le GUI l'affiche, rien n'est écrit."""


VERSION_GUI = "ceremonie-GUI v1.7 (D117)"   # scénarios dossier local / repo git + clonage


# ===========================================================================
# SECTION 0 — D113 : L'ENREGISTREUR DE VOL (boîte noire). Tout ce que le GUI
# dit, fait, et chaque crash atterrit dans un journal LOCAL horodaté, à
# côté du fichier lui-même (ceremonie-journal.log). AUCUN réseau ; aucune
# donnée secrète : la phrase de contrôle passe par des fichiers temporaires
# détruits, la graine n'est JAMAIS affichée (D87/D110). Le rapport part par
# la main de l'humain (bouton « Envoyer le rapport… »), pas par le fil.
# ===========================================================================

CHEMIN_JOURNAL_VOL = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ceremonie-journal.log")


class Enregistreur:
    """Boîte noire locale : append horodaté, une ligne = un fait. Un échec
    d'écriture (disque en lecture seule, clef USB pleine) ne gêne JAMAIS la
    cérémonie : la boîte noire est un témoin, pas une dépendance."""

    def __init__(self, chemin):
        self.chemin = chemin
        self.fichier = None
        try:
            self.fichier = open(chemin, "a", encoding="utf-8", buffering=1)
        except OSError:
            pass

    def ligne(self, texte, genre="info"):
        if not self.fichier:
            return
        horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.fichier.write(f"[{horodatage}] [{genre:<8}] {texte}\n")
        except OSError:
            pass

    def traceback(self):
        """Le traceback COMPLET de l'exception en cours, ligne par ligne."""
        for ligne in traceback.format_exc().splitlines():
            self.ligne(ligne, "crash")

    def entete(self, racine=None):
        self.ligne("=" * 72, "entete")
        self.ligne(f"DEMARRAGE {VERSION_GUI}", "entete")
        self.ligne(f"python {sys.version.split()[0]} — "
                   f"{platform.platform()} — argv : {' '.join(sys.argv)!r}",
                   "entete")
        if racine is not None:
            try:
                self.ligne(
                    f"Tk {racine.tk.call('info', 'patchlevel')} — écran "
                    f"{racine.winfo_screenwidth()}x"
                    f"{racine.winfo_screenheight()}", "entete")
            except Exception:
                pass
        self.ligne(f"dépôt attaché : {RACINE_DEPOT} (source : {SOURCE_DEPOT})",
                   "entete")


ENREGISTREUR = Enregistreur(CHEMIN_JOURNAL_VOL)


# ===========================================================================
# SECTION A — Ed25519 en Python pur (RFC 8032), copie CONFORME de
# v06/ceremonie_hors_ligne.py § crypto. La conformité est attestée par
# test_ceremonie_gui.py (T1 : vecteurs RFC § 7.1 TEST 1-3 + interop avec
# l'implémentation auditée « cryptography » quand elle est présente).
# Duplication CONSCIENTE et CONSIGNÉE : le profil hors-ligne doit vivre
# sans le dépôt — c'est la même posture que gf_mult_independant dans
# test_cf2.py (réimplémentation attestée, pas une réécriture).
# ===========================================================================

P = 2 ** 255 - 19                                   # corps premier
L = 2 ** 252 + 27742317777372353535851937790883648493   # ordre du point de base
D = (-121665 * pow(121666, P - 2, P)) % P           # paramètre de courbe
SQRT_M1 = pow(2, (P - 1) // 4, P)                   # racine de -1
G = (15112221349535400772501151409588531511454012693041857206046113283949847762202,
     46316835694926478169428394003475163141307993866256225615783033603165251855960)  # base

import hashlib  # noqa: E402  (import local à la section, ordre voulu)


def _sha512(donnees):
    return hashlib.sha512(donnees).digest()


def _inv(x):
    return pow(x, P - 2, P)


def _pt_add(P1, P2):
    """Addition de points, coordonnées homogènes étendues (RFC 8032 § 5.1.4)."""
    X1, Y1, Z1, T1 = P1
    X2, Y2, Z2, T2 = P2
    A = (Y1 - X1) * (Y2 - X2) % P
    B = (Y1 + X1) * (Y2 + X2) % P
    C = 2 * T1 * D * T2 % P
    Ee = 2 * Z1 * Z2 % P
    E, F, Gg, H = B - A, Ee - C, Ee + C, B + A
    return (E * F % P, Gg * H % P, F * Gg % P, E * H % P)


def _pt_mul(s, point):
    """Multiplication scalaire (double-and-add ; s supposé dans [0, L))."""
    Q = (0, 1, 1, 0)                                # élément neutre
    Pp = point
    while s > 0:
        if s & 1:
            Q = _pt_add(Q, Pp)
        Pp = _pt_add(Pp, Pp)
        s >>= 1
    return Q


def _pt_compress(point):
    x, y, z, _ = point
    zi = _inv(z)
    x = x * zi % P
    y = y * zi % P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _pt_decompress(octets):
    y = int.from_bytes(octets, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    if y >= P:
        return None
    x2 = (y * y - 1) * _inv(D * y * y + 1) % P
    if x2 == 0:
        if sign:
            return None
        x = 0
    else:
        x = pow(x2, (P + 3) // 8, P)
        if (x * x - x2) % P != 0:
            x = x * SQRT_M1 % P
        if (x * x - x2) % P != 0:
            return None
        if (x & 1) != sign:
            x = P - x
    return (x, y, 1, x * y % P)


_G_EXT = (G[0], G[1], 1, G[0] * G[1] % P)


def _pt_equal(P1, P2):
    """Égalité projective : x1/z1 == x2/z2 ET y1/z1 == y2/z2."""
    x1, y1, z1, _ = P1
    x2, y2, z2, _ = P2
    return (x1 * z2 - x2 * z1) % P == 0 and (y1 * z2 - y2 * z1) % P == 0


def cle_publique_depuis_graine(graine):
    """Clé publique (32 octets) depuis la graine (32 octets) — RFC 8032 § 5.1.5."""
    h = _sha512(graine)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    return _pt_compress(_pt_mul(a, _G_EXT))


def signer_ed25519(graine, message):
    """Signature Ed25519 (64 octets) — RFC 8032 § 5.1.6."""
    h = _sha512(graine)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= 1 << 254
    prefixe = h[32:]
    r = int.from_bytes(_sha512(prefixe + message), "little") % L
    R = _pt_compress(_pt_mul(r, _G_EXT))
    A = _pt_compress(_pt_mul(a, _G_EXT))
    k = int.from_bytes(_sha512(R + A + message), "little") % L
    s = (r + k * a) % L
    return R + int.to_bytes(s, 32, "little")


def verifier_ed25519(cle_publique, message, signature):
    """Vérification Ed25519 — RFC 8032 § 5.1.7. True ssi valide."""
    if len(cle_publique) != 32 or len(signature) != 64:
        return False
    A = _pt_decompress(cle_publique)
    if A is None:
        return False
    Rs = signature[:32]
    R = _pt_decompress(Rs)
    if R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= L:
        return False
    k = int.from_bytes(_sha512(Rs + cle_publique + message), "little") % L
    sG = _pt_mul(s, _G_EXT)
    kA = _pt_mul(k, A)
    return _pt_equal(sG, _pt_add(R, kA))


VECTEURS_RFC8032 = [
    # (graine, clé publique, message, signature)
    ("9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60",
     "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a",
     "",
     "e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555f"
     "b8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"),
    ("4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb",
     "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c",
     "72",
     "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da0"
     "85ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"),
    ("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7",
     "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025",
     "af82",
     "6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac1"
     "8ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"),
]


def autotest():
    """True ssi les TROIS vecteurs RFC passent (clé, signature, vérification)."""
    tout = True
    for indice, (graine_hex, pub_hex, msg_hex, sig_hex) in enumerate(
            VECTEURS_RFC8032, 1):
        graine = bytes.fromhex(graine_hex)
        message = bytes.fromhex(msg_hex)
        signature = bytes.fromhex(sig_hex)
        publique_calculee = cle_publique_depuis_graine(graine)
        signature_calculee = signer_ed25519(graine, message)
        ok = (publique_calculee.hex() == pub_hex
              and signature_calculee.hex() == sig_hex
              and verifier_ed25519(bytes.fromhex(pub_hex), message, signature)
              and not verifier_ed25519(bytes.fromhex(pub_hex), message,
                                       bytes(64)))
        tout = tout and ok
    # Mutation ciblée : un octet de message changé => signature invalide
    graine, _, msg_hex, sig_hex = VECTEURS_RFC8032[1]
    message = bytes.fromhex(msg_hex)
    mauvaise = bytes([message[0] ^ 1]) + message[1:]
    mutation = not verifier_ed25519(bytes.fromhex(
        VECTEURS_RFC8032[1][1]), mauvaise, bytes.fromhex(sig_hex))
    return tout and mutation


# ===========================================================================
# SECTION B — contrôleur du profil HORS-LIGNE (machine air-gap, D87).
# Mêmes formats de fichiers que v06/ceremonie_hors_ligne.py (interop),
# mais chemins PARAMÉTRABLES et résultat en (ok, texte) : la GUI habille,
# le contrôleur décide. La graine ne paraît JAMAIS dans les textes retournés.
# ===========================================================================

HEX_MIN = set("0123456789abcdef")


def _est_hex_min(texte, taille):
    return (len(texte) == taille and all(c in HEX_MIN for c in texte))


def _lire_graine_privee(chemin):
    """Extrait la graine (64 hex minuscules) de cle-I-privee.txt."""
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            lignes = f.read().splitlines()
    except OSError as exc:
        raise ErreurCeremonie(f"clé privée illisible : {chemin} ({exc})")
    for ligne in lignes:
        cand = ligne.strip()
        if _est_hex_min(cand, 64):
            return bytes.fromhex(cand)
    raise ErreurCeremonie(f"aucune graine (64 hex minuscules) lisible "
                          f"dans {chemin}")


def _graine_depuis_saisie(texte):
    """D112 — la clé tapée à la main (récupération papier) : 64 hex.

    La SAISIE accepte majuscules ET minuscules (une retape depuis le
    papier ne mérite pas un refus de casse — hex est hex), mais RIEN
    d'autre : longueur fausse, caractère non hex = échec NOMMÉ avec la
    nature de la faute (jamais le contenu — la graine ne paraît ni dans
    le message d'erreur ni dans le journal).
    """
    cand = texte.strip()
    if not cand:
        raise ErreurCeremonie("saisie manuelle vide — entrez les 64 hex de "
                              "la graine (ligne imprimée de "
                              "cle-I-privee.txt) ou choisissez le FICHIER")
    if len(cand) != 64:
        raise ErreurCeremonie(
            f"saisie manuelle : {len(cand)} caractère(s) au lieu de 64 — "
            "la graine Ed25519 est la ligne de 64 hexadécimaux")
    position = next((i for i, c in enumerate(cand)
                     if c not in "0123456789abcdefABCDEF"), None)
    if position is not None:
        raise ErreurCeremonie(
            f"saisie manuelle : caractère non hexadécimal en position "
            f"{position + 1} — la graine n'accepte QUE 0-9 a-f A-F")
    return bytes.fromhex(cand.lower())


def _lire_hex_fichier(chemin, quoi, taille):
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            texte = f.read().strip()
    except OSError as exc:
        raise ErreurCeremonie(f"{quoi} illisible : {chemin} ({exc})")
    if not _est_hex_min(texte, taille * 2):
        raise ErreurCeremonie(f"{quoi} malformé dans {chemin} "
                              f"({taille * 2} hexadécimaux minuscules attendus)")
    return bytes.fromhex(texte)


def _lire_lignes_a_signer(chemin):
    """Lignes « arbre balise empreinte » -> [(arbre, balise, empreinte_hex)]."""
    entrees = []
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            lignes_enum = list(enumerate(f, 1))
    except OSError as exc:
        raise ErreurCeremonie(f"remise illisible : {chemin} ({exc})")
    for numero, ligne in lignes_enum:
        ligne = ligne.strip()
        if not ligne:
            continue
        morceaux = ligne.split()
        if (len(morceaux) != 3 or not _est_hex_min(morceaux[2], 64)):
            raise ErreurCeremonie(
                f"a-signer ligne {numero} malformée : {ligne!r} "
                f"(format « arbre balise empreinte »)")
        entrees.append((morceaux[0], morceaux[1], morceaux[2]))
    if not entrees:
        raise ErreurCeremonie(f"{chemin} vide — rien à signer")
    return entrees

def hl_generer(chemin_privee, chemin_publique):
    """Génère la clé I (première cérémonie). Fail-closed : autotest d'abord.

    Le contenu des fichiers est IDENTIQUE à mode_generer (interop), la
    graine n'est JAMAIS retournée dans le texte (le fichier est la remise).
    """
    if not autotest():
        raise ErreurCeremonie("AUTOTEST RFC 8032 : ÉCHEC — cérémonie refusée "
                              "(fail-closed, rien n'est écrit)")
    graine = os.urandom(32)
    publique = cle_publique_depuis_graine(graine)
    try:
        with open(chemin_privee, "w", encoding="utf-8") as f:
            f.write(
            "# TRIADE — clé I PRIVÉE (sceau de l'Intention, D87)\n"
            "# Générée HORS LIGNE ; ne doit JAMAIS entrer dans le bac à sable\n"
            "# de l'assistant, ni être synchronisée, ni être commitée.\n"
            "#\n"
            "# GARDE : imprimez la ligne de 64 caractères ci-dessous, conservez\n"
            "# le papier en lieu sûr (deux copies, deux lieux). Une graine perdue\n"
            "# = toute évolution future de l'intention devient impossible ; une\n"
            "# graine volée = la souveraineté est morte. Détruisez ce fichier\n"
            "# après copie papier, ou conservez-le chiffré sur le média dédié.\n"
            "#\n"
            + graine.hex() + "\n")
        try:
            os.chmod(chemin_privee, 0o600)
        except OSError:
            pass  # Windows : attributs ACL, le fichier reste privé par posture
        with open(chemin_publique, "w", encoding="utf-8") as f:
            f.write(publique.hex() + "\n")
    except OSError as exc:
        raise ErreurCeremonie(f"impossible d'écrire la clé : {exc} "
                              f"(vérifiez les chemins choisis)")
    return (f"[ceremonie] generer : clé I créée.\n"
            f"  {chemin_privee}   — LA garde (voir l'en-tête du fichier : "
            f"impression papier recommandée)\n"
            f"  {chemin_publique} — à remettre au dépôt (publique, sans "
            f"risque)\n"
            f"  La graine ne s'affiche jamais ici : le fichier est la remise.")


def hl_signer(chemin_a_signer, chemin_privee, chemin_sortie,
              graine_texte=None):
    """Signe la remise a-signer.txt avec la clé privée — chaque signature
    est auto-vérifiée AVANT écriture (une cérémonie douteuse n'écrit rien).

    D112 — la clé vient du FICHIER (chemin_privee, comportement historique)
    OU de la SAISIE MANUELLE (graine_texte : les 64 hex retapés depuis la
    copie papier). Les DEUX sources produisent les MÊMES signatures (la
    graine est la graine) ; l'échec de l'une ou l'autre est NOMMÉ et
    n'écrit rien. La graine ne paraît jamais dans le texte de retour.
    """
    if not autotest():
        raise ErreurCeremonie("AUTOTEST RFC 8032 : ÉCHEC — cérémonie refusée "
                              "(fail-closed, rien n'est écrit)")
    if graine_texte is not None:
        graine = _graine_depuis_saisie(graine_texte)
    elif not (chemin_privee and chemin_privee.strip()):
        raise ErreurCeremonie(
            "aucune clé privée — choisissez le FICHIER cle-I-privee.txt "
            "ou cochez la saisie manuelle (D112)")
    else:
        graine = _lire_graine_privee(chemin_privee)
    publique = cle_publique_depuis_graine(graine)
    entrees = _lire_lignes_a_signer(chemin_a_signer)
    lignes = []
    for arbre, balise, empreinte_hex in entrees:
        message = bytes.fromhex(empreinte_hex)
        signature = signer_ed25519(graine, message)
        if not verifier_ed25519(publique, message, signature):
            raise ErreurCeremonie(
                f"signature auto-vérification invalide pour {arbre} — "
                f"RIEN n'est écrit (cérémonie douteuse, spec § 4)")
        lignes.append(f"{arbre} {balise} {signature.hex()}")
    try:
        with open(chemin_sortie, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
    except OSError as exc:
        raise ErreurCeremonie(f"impossible d'écrire les signatures : {exc}")
    return (f"[ceremonie] signer : {len(lignes)} signatures -> "
            f"{chemin_sortie}\n"
            "  Clé privée : "
            + ("saisie manuelle (D112) — la remise est signée par la graine "
               "retapée ; effacez le champ (déjà fait) et gardez le papier"
               if graine_texte is not None else chemin_privee)
            + "\n"
            f"  Chaque signature a été VÉRIFIÉE avec la clé publique avant "
            f"écriture.\n"
            f"  Remettez {os.path.basename(chemin_sortie)} au dépôt "
            f"(profil dépôt, onglet Sceau de l'Intention, bouton Déposer).")


def hl_verifier(chemin_a_signer, chemin_signatures, chemin_publique):
    """Re-vérifie une remise de façon autonome (True, texte) / (False, texte)."""
    entrees = _lire_lignes_a_signer(chemin_a_signer)
    try:
        with open(chemin_signatures, "r", encoding="utf-8") as f:
            lignes_sig = [l.strip() for l in f if l.strip()]
    except OSError as exc:
        raise ErreurCeremonie(f"signatures illisibles : {chemin_signatures} "
                              f"({exc})")
    publique = _lire_hex_fichier(chemin_publique, "clé publique", 32)
    vues, tout, texte = set(), True, []
    for ligne in lignes_sig:
        morceaux = ligne.split()
        if len(morceaux) != 3 or not _est_hex_min(morceaux[2], 128):
            texte.append(f"  ECHEC : ligne de signature malformée : {ligne!r}")
            tout = False
            continue
        arbre, balise, signature_hex = morceaux
        correspond = [e for e in entrees if e[0] == arbre]
        if not correspond:
            texte.append(f"  ECHEC : {arbre} absent de "
                         f"{os.path.basename(chemin_a_signer)}")
            tout = False
            continue
        if correspond[0][1] != balise:
            texte.append(f"  ECHEC : balise divergente pour {arbre} : "
                         f"{balise!r}")
            tout = False
            continue
        ok = verifier_ed25519(publique, bytes.fromhex(correspond[0][2]),
                              bytes.fromhex(signature_hex))
        texte.append(f"  {arbre}: {'VERT' if ok else 'SIGNATURE INVALIDE'}")
        vues.add(arbre)
        tout = tout and ok
    manquants = sorted({a for a, _, _ in entrees} - vues)
    if manquants:
        texte.append(f"  ECHEC : arbres sans signature : {', '.join(manquants)}")
        tout = False
    texte.append("[ceremonie] verifier : " + ("TOUT VERT" if tout else "ÉCHEC"))
    return tout, "\n".join(texte)


# ===========================================================================
# SECTION C — socle du profil DÉPÔT (machine connectée, à côté du dépôt).
# Les actions passent par les CLI existants en sous-processus : le
# fail-closed des CLI reste la loi, le GUI n'est qu'un habit. Les NOUVELLES
# capacités (contrôle de relecture, feuille d'export, éditeur de liste
# blanche) importent v06/coffre_cf2.py directement et sont attestées par
# test_ceremonie_gui.py (T5-T7).
# ===========================================================================

import subprocess  # noqa: E402
import tempfile   # noqa: E402

def _racine_depot_defaut():
    """Le dépôt par défaut : le PARENT du dossier qui contient ce fichier
    (ce fichier vit dans <dépôt>/v06/ — posture D107/D108, inchangée)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resoudre_racine_depot(argument=None):
    """Ordre de résolution D111 — le dépôt N'EST PLUS deviné, il est NOMMÉ :
        1. --depot CHEMIN (ligne de lancement) ;
        2. la variable d'environnement TRIADE_DEPOT ;
        3. le défaut D107 : ce fichier vit dans <dépôt>/v06/.
    Retourne (racine_absolue, source). Un chemin donné mais introuvable est
    un ÉCHEC NOMMÉ (ErreurCeremonie) — jamais un repli silencieux : la
    discipline fail-closed s'applique AUSSI à la connexion au dépôt.
    Un dossier valide mais sans v06/coffre_cf2.py n'est PAS une erreur ici :
    depot_disponible() rendra son verdict, l'accueil affichera la cause."""
    if argument:
        candidat = os.path.abspath(os.path.expanduser(argument))
        if not os.path.isdir(candidat):
            raise ErreurCeremonie(
                f"--depot : dossier introuvable : {candidat} — donnez la "
                "RACINE du clone du dépôt triade (celui qui contient v06/)")
        return candidat, "--depot"
    env = os.environ.get("TRIADE_DEPOT", "").strip()
    if env:
        candidat = os.path.abspath(os.path.expanduser(env))
        if not os.path.isdir(candidat):
            raise ErreurCeremonie(
                f"TRIADE_DEPOT : dossier introuvable : {candidat} — la "
                "variable doit désigner la RACINE du clone du dépôt triade "
                "(celui qui contient v06/), ou retirez-la")
        return candidat, "TRIADE_DEPOT"
    return _racine_depot_defaut(), "position du fichier"


RACINE_DEPOT = _racine_depot_defaut()
SOURCE_DEPOT = "position du fichier"


def definir_racine_depot(racine, source):
    """Fixe le dépôt résolu (appelé par main() AVANT toute construction).
    Les CLI, l'import v06.coffre_cf2 et la sentinelle lisent RACINE_DEPOT
    À L'APPEL — tout le profil dépôt suit, sans autre câblage."""
    global RACINE_DEPOT, SOURCE_DEPOT
    RACINE_DEPOT = racine
    SOURCE_DEPOT = source

# Journalisation de la sentinelle démarrée en détaché (append, jamais le
# journal des PV qui appartient au coffre) :
def _chemin_log_sentinelle(chemin_config):
    return os.path.join(os.path.dirname(os.path.abspath(chemin_config)),
                        "sentinelle-stdout.txt")


def depot_disponible() -> bool:
    """True si le dépôt résolu est complet (v06/coffre_cf2.py présent).
    D111 : le dépôt résolu vient de --depot / TRIADE_DEPOT / la position
    du fichier — la GARDE est la même dans les trois cas."""
    return os.path.isfile(os.path.join(RACINE_DEPOT, "v06", "coffre_cf2.py"))


def _module_cf2():
    """Import paresseux de v06/coffre_cf2 (la pile du dépôt est requise —
    l'absence est un échec NOMMÉ avec sa consigne, jamais un crash brut)."""
    if not depot_disponible():
        raise ErreurCeremonie(
            "le profil dépôt exige un dépôt triade complet "
            f"(v06/coffre_cf2.py introuvable dans {RACINE_DEPOT}) — "
            "lancez le GUI depuis <dépôt>/v06/ceremonie_gui.py, ou pointez "
            "un clone avec --depot CHEMIN (ou TRIADE_DEPOT) ; pour la "
            "machine hors-ligne, utilisez le profil hors-ligne")
    manquants = _paquets_manquants()
    if manquants:
        raise ErreurCeremonie(
            f"pile du dépôt incomplète (absents : {', '.join(manquants)}) — "
            "installez-la depuis l'accueil du profil dépôt, ou : "
            "pip install pynacl cryptography argon2-cffi")
    if RACINE_DEPOT not in sys.path:
        sys.path.insert(0, RACINE_DEPOT)
    import v06.coffre_cf2 as cf2
    return cf2


def _paquets_manquants():
    """La pile du dépôt : pynacl (AEAD XChaCha20) + cryptography (HKDF,
    Ed25519 de vérification) + argon2-cffi (le KDF du coffre CF1 — requis
    par migrer ET changer-phrase depuis D110, cf. coffre_fort.py)."""
    manquants = []
    for module, paquet in (("nacl", "pynacl"),
                           ("cryptography", "cryptography"),
                           ("argon2", "argon2-cffi")):
        try:
            __import__(module)
        except ImportError:
            manquants.append(paquet)
    return manquants


def dependances_disponibles() -> bool:
    return not _paquets_manquants()


def installer_dependances(emit=None):
    """Installe la pile du dépôt (pynacl + cryptography) AVEC l'accord de
    l'utilisateur (le consentement est demandé par la GUI AVANT l'appel).
    Dans un venv, pip refuse --user : l'essai retombe sans --user. Retour
    (ok, texte) — l'échec est nommé, avec la parade si nécessaire."""
    if not _paquets_manquants():
        return True, ("[pip] pile du dépôt déjà présente (pynacl + "
                      "cryptography + argon2-cffi)")
    manquants = _paquets_manquants()
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    dans_venv = (sys.prefix != getattr(sys, "base_prefix", sys.prefix))
    essais = [[sys.executable, "-m", "pip", "install"] + manquants]
    if not dans_venv:
        essais.insert(0, [sys.executable, "-m", "pip", "install", "--user"]
                      + manquants)
    lignes = []
    for cmd in essais:
        if emit:
            emit(f"[pip] {' '.join(cmd)}")
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True,
                                    encoding="utf-8", errors="replace", env=env)
            for ligne in proc.stdout:
                lignes.append(ligne.rstrip("\n"))
                if emit:
                    emit(ligne.rstrip("\n"))
            proc.wait()
        except OSError as exc:
            return False, f"pip indisponible : {exc}"
        if dependances_disponibles():
            return True, ("[pip] pile du dépôt installée et importable : "
                          "+ ".join(manquants))
        sortie = "\n".join(lignes)
        if "--user' install" not in sortie and \
                "user site-packages" not in sortie:
            break       # pas un souci de --user : inutile de réessayer
    sortie = "\n".join(lignes)
    if "externally-managed-environment" in sortie:
        return False, ("environnement Python « externally-managed » (Debian "
                       "récent) : créez un venv — python3 -m venv ~/venv-triade "
                       "&& ~/venv-triade/bin/pip install pynacl cryptography "
                       "argon2-cffi — "
                       "puis relancez le GUI avec ~/venv-triade/bin/python")
    return False, ("l'installation a échoué — sortie pip ci-dessus ; remède "
                   "manuel : pip install pynacl cryptography argon2-cffi")


def _detruire_fichier(chemin):
    """Écrase puis supprime (best effort) — pour le fichier-phrase temporaire."""
    try:
        taille = os.path.getsize(chemin)
        with open(chemin, "wb") as f:
            f.write(b"\x00" * taille)
    except OSError:
        pass
    try:
        os.unlink(chemin)
    except OSError:
        pass


def _pomper(proc, emit=None):
    """D116 — pompe commune de sortie : streame ligne à ligne (emit),
    retourne (code de sortie, texte complet). Partagée par les CLI du
    dépôt et par git — aucune logique de flux dupliquée."""
    lignes = []
    for ligne in proc.stdout:
        propre = ligne.rstrip("\n")
        lignes.append(propre)
        if emit:
            emit(propre)
    return proc.wait(), "\n".join(lignes)


def executer_cli(module, args, emit=None, phrase=None, nouvelle_phrase=None,
                au_racine=False):
    """Exécute un CLI du dépôt et streame sa sortie.

    Retour (code_sortie, texte_complet). Le fail-closed appartient au CLI :
    le GUI ne fait que RELAYER son verdict (et sa phrase d'échec nommée).
    « phrase » (non None) passe par --phrase-fichier sur un temporaire 0600,
    écrasé puis détruit — la phrase ne paraît ni dans la commande ni dans
    le journal. « nouvelle_phrase » (D110, changer-phrase) passe par
    --nouvelle-depuis-fichier, même discipline de temporaire détruit.
    « au_racine » : le module vit à la RACINE du dépôt (coffre_fort.py)
    au lieu de v06/ (le kit /Cérémonie pose l'un et l'autre).
    """
    relatif = module if au_racine else os.path.join("v06", module)
    chemin_module = os.path.join(RACINE_DEPOT, relatif)
    if not os.path.isfile(chemin_module):
        raise ErreurCeremonie(f"module du dépôt introuvable : {chemin_module}")
    cmd = [sys.executable, chemin_module] + [str(a) for a in args]
    fichier_phrase = None
    fichier_nouvelle = None
    if phrase is not None:
        if not phrase.strip():
            raise ErreurCeremonie("phrase de contrôle vide — refus "
                                  "(fail-closed)")
        fd, fichier_phrase = tempfile.mkstemp(prefix="phrase-cf1-",
                                              suffix=".txt")
        try:
            os.write(fd, phrase.strip().encode("utf-8"))
        finally:
            os.close(fd)
        cmd += ["--phrase-fichier", fichier_phrase]
    if nouvelle_phrase is not None:
        if not nouvelle_phrase.strip():
            raise ErreurCeremonie("nouvelle phrase vide — refus "
                                  "(fail-closed)")
        fd, fichier_nouvelle = tempfile.mkstemp(prefix="phrase-votre-",
                                                suffix=".txt")
        try:
            os.write(fd, nouvelle_phrase.strip().encode("utf-8"))
        finally:
            os.close(fd)
        cmd += ["--nouvelle-depuis-fichier", fichier_nouvelle]
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUNBUFFERED", "1")
    try:
        proc = subprocess.Popen(
            cmd, cwd=RACINE_DEPOT, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, text=True, encoding="utf-8",
            errors="replace", env=env)
        code, texte = _pomper(proc, emit)
    finally:
        if fichier_phrase:
            _detruire_fichier(fichier_phrase)
        if fichier_nouvelle:
            _detruire_fichier(fichier_nouvelle)
    return code, texte


# ---------------------------------------------------------------------------
# D116 — GIT + FIL DE CÉRÉMONIE : pousser les fichiers générés (add
# ciblé, commit, pull --rebase, push — échecs nommés étape par étape) et
# l'AUTO-DÉTECTION des cinq étapes du sceau I (lecture seule, par preuves).
# ---------------------------------------------------------------------------

def executer_git(args, emit=None, cwd=None):
    """git dans le dossier du dépôt attaché (ou CWD explicite — D117 :
    preuve/clonage sur un chemin QUELCONQUE) — même discipline de flux que
    les CLI (sortie streamee ligne à ligne, code de retour honnête). git
    absent du système : (127, échec nommé), jamais un traceback."""
    dossier = cwd if cwd is not None else RACINE_DEPOT
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        proc = subprocess.Popen(
            ["git"] + [str(a) for a in args], cwd=dossier,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            encoding="utf-8", errors="replace", env=env)
    except FileNotFoundError:
        return 127, ("git introuvable sur cette machine — installez-le "
                     "(git-scm.com) ou poussez depuis votre terminal")
    except OSError as exc:      # cwd inexistant, entre autres
        return 128, f"git : dossier de travail invalide ({exc})"
    return _pomper(proc, emit)


def git_pousser(chemins, message, emit=None):
    """D116 — pousse les fichiers générés de la cérémonie sur git.

    add (UNIQUEMENT les chemins donnés — jamais « add -A » : la clé privée
    vit hors du dépôt et les journaux *.log sont ignorés par .gitignore)
    → commit (message exigé — un commit de cérémonie se NOMME) →
    pull --rebase (le push rejeté du terrain D113-115 ne se reproduira
    plus : le dépôt distant est intégré AVANT de pousser) → push. Chaque
    étape refuse NOMMÉ ; rien n'est forcé, rien n'est deviné.
    """
    chemins = [str(c).strip() for c in chemins if c and str(c).strip()]
    if not chemins:
        raise ErreurCeremonie("git : aucun chemin à pousser — refus "
                              "(fail-closed, D116)")
    message = (message or "").strip()
    if not message:
        raise ErreurCeremonie("git : message de commit vide — refus (un "
                              "commit de cérémonie se NOMME, D116)")

    def git(args, cause=None):
        code, texte = executer_git(args, emit=emit)
        if code != 0:
            lignes = texte.strip().splitlines()
            premiere = lignes[0] if lignes else f"code {code}"
            raise ErreurCeremonie(
                f"git {' '.join(args)} : {cause or premiere}")
        return texte

    git(["rev-parse", "--is-inside-work-tree"],
        "le dossier attaché n'est pas un dépôt git")
    git(["add", "--"] + chemins)
    code_diff, _ = executer_git(["diff", "--cached", "--quiet"])
    commits = 0
    if code_diff == 0:
        if emit:
            emit(f"[git] rien à committer ({', '.join(chemins)} inchangé) "
                 "— synchronisation seule")
    else:
        git(["commit", "-m", message])
        commits = 1
        if emit:
            emit(f"[git] commit : {message}")
    code_pull, texte_pull = executer_git(["pull", "--rebase"], emit=emit)
    if code_pull != 0:
        lignes_pull = texte_pull.strip().splitlines()
        raise ErreurCeremonie(
            "git pull --rebase a échoué — push ANNULÉ ; si git signale un "
            "rebase en cours, « git rebase --abort » remet votre dépôt "
            "tel quel (première ligne : "
            f"{lignes_pull[0] if lignes_pull else '?'})")
    git(["push"], "push refusé (authentification GitHub ? branche amont ?)")
    if commits:
        return True, (f"[git] poussé : 1 commit ({', '.join(chemins)}) — "
                      f"« {message} »")
    return True, (f"[git] rien à committer — dépôt synchronisé "
                  f"({', '.join(chemins)})")


FIL_ETAPES = (
    (1, "Préparer a-signer.txt (dépôt)"),
    (2, "Générer la clé I (hors-ligne)"),
    (3, "Signer la remise (hors-ligne)"),
    (4, "Déposer la remise (dépôt)"),
    (5, "Enregistrer sur git"),
)

FIL_HINTS = {
    1: "Bouton « Préparer a-signer.txt » ci-dessous (onglet Sceau de "
       "l'Intention).",
    2: "Bouton « ← Accueil » (bandeau, toujours visible) → profil "
       "hors-ligne → onglet « 1 · Générer la clé ».",
    3: "Profil hors-ligne → onglet « 2 · Signer une remise » (a-signer.txt "
       "y est transporté, la clé n'en part jamais).",
    4: "Champ « Remise à déposer » ci-dessous + bouton « Déposer la "
       "remise (acte souverain) ».",
    5: "Bouton « Pousser v06/sceau-I sur git… » ci-dessous (commit + "
       "pull --rebase + push).",
}


# D117 — le scénario AVANT TOUT : deux façons d'amener le dépôt sur la
# machine, deux fils d'étapes. « dossier local » : le dépôt existe déjà
# (attachement D112), fil de CINQ étapes. « repo git » : le dépôt vient
# d'un distant — fil de SIX étapes, « Cloner le dépôt » en tête, prouvé
# lecture seule (git rev-parse + origin).
SCENARIOS = ("dossier local", "repo git")
SCENARIO_DOSSIER, SCENARIO_GIT = SCENARIOS
TITRE_ETAPE_CLONE = "Cloner le dépôt (repo git)"


def masquer_jeton(url):
    """D117 — masque les IDENTIFIANTS d'une URL (user:pass@ ou jeton@)
    pour le journal, le verdict et la boîte noire : une URL de clone peut
    porter un jeton d'accès (https://<jeton>@github.com/…) et le GUI ne
    le consigne JAMAIS en clair. Formes ssh scp-like (git@hôte:…) sans
    schéma : inchangées (l'utilisateur « git » y est public)."""
    import re   # noqa: E402 (usage local, ordre voulu)
    return re.sub(r"(?<=://)[^/@:]+(?::[^/@]*)?@", "***@", str(url))


def preuve_clone(chemin=None):
    """D117 — preuve LECTURE SEULE que le dossier attaché (ou donné) est
    un CLONE : racine d'un arbre git AVEC un remote origin. Retour
    (faite, detail) — les refus sont NOMMÉS (pas un dépôt git / sans
    origin / git absent / dossier absent), jamais devinés."""
    cible = os.path.abspath(chemin if chemin is not None else RACINE_DEPOT)
    if not os.path.isdir(cible):
        return False, f"dossier absent — aucun dépôt à sonder : {cible}"
    code_r, texte_r = executer_git(["rev-parse", "--show-toplevel"],
                                   cwd=cible)
    if code_r == 127:
        return False, "git introuvable sur cette machine — clone impossible à prouver"
    if code_r != 0:
        premiere = texte_r.strip().splitlines()
        premiere = premiere[0] if premiere else f"code {code_r}"
        return False, f"pas un dépôt git ({premiere}) : {cible}"
    racine_git = texte_r.strip().splitlines()[0].strip()
    if os.path.abspath(racine_git) != cible:
        return (False, f"sous-dossier d'un dépôt git (racine : "
                       f"{racine_git}) — attachez la RACINE du clone, "
                       f"pas un sous-dossier : {cible}")
    code_o, texte_o = executer_git(["remote", "get-url", "origin"],
                                   cwd=cible)
    if code_o != 0:
        return (False, "dépôt git SANS origin — le scénario repo git veut "
                       "un CLONE (git clone pose l'origin ; un dépôt "
                       "localement « init » n'en a pas)")
    origin = texte_o.strip().splitlines()[0].strip() if texte_o.strip() \
        else "(origine muette)"
    return True, f"dépôt git cloné — origin : {masquer_jeton(origin)}"


def cloner_depot(url, destination, emit=None):
    """D117 — clone le dépôt distant vers DESTINATION (le dossier qui
    DEVIENT la racine du clone). Refus NOMMÉS AVANT tout lancement : URL
    vide, URL commençant par « - » (un argument git déguisé est une
    injection), destination vide / commençant par « - » / NON VIDE
    (fail-closed : rien n'y est touché). git absent : code 127 nommé.
    Le jeton éventuel de l'URL est MASQUÉ partout (journal, verdict,
    boîte noire). Après le clone, la PREUVE (rev-parse + origin) doit
    passer — sinon échec nommé (un clone que l'on ne peut pas prouver
    n'est pas un clone)."""
    url = str(url or "").strip()
    destination = str(destination or "").strip()
    if not url:
        raise ErreurCeremonie(
            "cloner : URL du dépôt VIDE — donnez l'adresse git (ex. "
            "https://github.com/alexisfrlopez-debug/triade.git ou "
            "git@github.com:alexisfrlopez-debug/triade.git)")
    if url.startswith("-"):
        raise ErreurCeremonie(
            f"cloner : URL refusée (elle commence par « - » — un argument "
            f"git déguisé est une INJECTION, refus fail-closed) : "
            f"{masquer_jeton(url)}")
    if not destination:
        raise ErreurCeremonie(
            "cloner : destination VIDE — choisissez le dossier parent et le "
            "nom du clone (le dossier qui DEVIENT la racine du dépôt)")
    if destination.startswith("-"):
        raise ErreurCeremonie(
            f"cloner : destination refusée (commence par « - » — argument "
            f"git déguisé, injection) : {destination}")
    destination = os.path.abspath(os.path.expanduser(destination))
    if os.path.exists(destination) and os.listdir(destination):
        raise ErreurCeremonie(
            f"cloner : destination NON VIDE — {destination} contient déjà "
            f"des fichiers ; git clone veut un chemin LIBRE et le refus "
            f"est NOMMÉ avant tout lancement (fail-closed, rien n'y est "
            f"touché)")
    if emit:
        emit(f"[git] clone {masquer_jeton(url)} → {destination}")
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        proc = subprocess.Popen(
            ["git", "clone", "--", url, destination], cwd=None,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
            encoding="utf-8", errors="replace", env=env)
    except FileNotFoundError:
        return False, ("git introuvable sur cette machine — installez-le "
                       "(git-scm.com) ou clonez depuis votre terminal")
    code, texte = _pomper(proc, emit)
    if code != 0:
        lignes = texte.strip().splitlines()
        premiere = lignes[0] if lignes else f"code {code}"
        return False, (f"git clone a échoué (code {code}) — {premiere} ; "
                       f"URL : {masquer_jeton(url)}")
    faite, detail = preuve_clone(destination)
    if not faite:
        return False, (f"clone posé mais PREUVE refusée : {detail} — "
                       "un clone que l'on ne peut pas prouver n'est pas "
                       "un clone (échec nommé, rien n'est attaché)")
    return True, (f"[git] clone terminé : {destination} — {detail}")


def cloner_et_attacher(url, destination, emit=None):
    """D117 — clone PUIS attache (la chaîne du bouton « Cloner en
    local… ») : après un clone prouvé, la garde D111 (v06/coffre_cf2.py)
    décide de l'attachement — un clone qui n'est pas un dépôt triade
    complet reste sur le disque mais n'est PAS attaché (échec nommé,
    aucun attachement partiel). L'attachement réussi re-pointe TOUT le
    profil dépôt (config, coffre CF1, CLI) sur le clone — les pages sont
    rebâties par le fil tkinter (cf. _sur_fin_action), jamais depuis le
    fil ouvrier."""
    ok, texte = cloner_depot(url, destination, emit=emit)
    if not ok:
        return False, texte
    destination = os.path.abspath(os.path.expanduser(str(destination)))
    if not os.path.isfile(os.path.join(destination, "v06", "coffre_cf2.py")):
        return False, (f"{texte}\n[ceremonie] v06/coffre_cf2.py introuvable "
                       "dans le clone : ce n'est pas (pas encore) un dépôt "
                       "triade complet — attachement REFUSÉ (fail-closed "
                       "D111) ; le clone reste sur le disque, il s'attachera "
                       "par « Choisir le dossier du dépôt… » s'il se "
                       "complète")
    definir_racine_depot(destination, "clone choisi (GUI, D117)")
    if emit:
        emit(f"[ceremonie] dépôt attaché : {RACINE_DEPOT} — clone (D117), "
             "garde v06/coffre_cf2.py VERTE")
    return True, f"{texte} ; dépôt ATTACHÉ : {RACINE_DEPOT}"


def hint_fil(scenario, numero):
    """D117 — le GESTE de l'étape NUMERO sous le SCÉNARIO courant : en
    repo git l'étape 1 est le CLONAGE et les étapes du sceau sont décalées
    d'un rang ; sinon la table FIL_HINTS d'origine."""
    if scenario == SCENARIO_GIT:
        if numero == 1:
            return ("Accueil → scénario REPO GIT → bouton « Cloner en "
                    "local… » (ou « Attacher un clone existant… » si le "
                    "clone vit déjà sur cette machine).")
        numero -= 1
    return FIL_HINTS[numero]


def _lire_a_signer(chemin):
    """Lignes « arbre balise empreinte » d'un a-signer.txt → dictionnaire
    arbre → empreinte (64 hex). Absent ou illisible : {}."""
    lignes = {}
    if chemin and os.path.isfile(chemin):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                for ligne in f:
                    morceaux = ligne.split()
                    if len(morceaux) == 3:
                        lignes[morceaux[0]] = morceaux[2]
        except OSError:
            return {}
    return lignes


def fil_ceremonie(a_signer=None, privee=None, publique=None,
                  signatures=None, chemins_git=("v06/sceau-I",),
                  scenario=None):
    """D116/D117 — l'état des étapes de la cérémonie du sceau I, par
    PREUVES (lecture seule : fichiers présents, CLI read-only, git
    status — aucune écriture, aucune clé touchée). Retour
    [(numéro, titre, faite, detail)] ; ce que la détection ne peut pas
    PROUVER, elle le nomme « à faire » avec la cause — jamais deviné.
    D117 : scenario="repo git" prépose « Cloner le dépôt » (preuve
    rev-parse + origin) et décale les cinq étapes du sceau d'un rang
    (fil de SIX) ; tout autre scénario (dont None) rend le fil de CINQ
    d'origine — le scénario ne change AUCUNE preuve du sceau, seulement
    la tête du fil."""
    import re   # noqa: E402 (usage local au fil, ordre voulu)
    re_verifier = re.compile(
        r"^\[sceau-I\] (\S+): CODE (\d+) — .*empreinte vivante "
        r"([0-9a-f]{16})")
    pile_ok = not _paquets_manquants()
    code_verif, texte_verif = None, ""
    if pile_ok:
        try:
            code_verif, texte_verif = executer_cli("sceau_I.py", ["verifier"])
        except ErreurCeremonie as exc:
            code_verif, texte_verif = None, str(exc)
    vivantes = {}
    for ligne in texte_verif.splitlines():
        trouve = re_verifier.match(ligne)
        if trouve:
            vivantes[trouve.group(1)] = trouve.group(3)
    cause = "verifier indisponible"
    if not pile_ok:
        cause = "pile du dépôt manquante (pynacl/cryptography)"
    elif code_verif is None and texte_verif:
        cause = texte_verif.strip().splitlines()[0]
    # É1 — Préparer : a-signer FRAIS (chaque arbre divergé porte, dans
    # a-signer.txt, l'empreinte VIVANTE — sinon la remise signée ne
    # correspondra plus au dépôt au moment de déposer)
    if code_verif == 0:
        e1 = True, "tout est signé — préparer inutile"
    elif code_verif in (10, 11, 12) and vivantes:
        deposees = _lire_a_signer(a_signer)
        if not deposees:
            e1 = False, f"a-signer.txt absent ou vide : {a_signer}"
        else:
            perimes = sorted(
                arbre for arbre, empreinte in vivantes.items()
                if arbre not in deposees
                or deposees[arbre][:16] != empreinte[:16])
            if perimes:
                e1 = (False, f"a-signer PÉRIMÉ pour {', '.join(perimes)} — "
                             f"relancez Préparer")
            else:
                e1 = True, f"a-signer.txt frais ({len(deposees)} arbres)"
    else:
        e1 = False, f"état des arbres inconnu — {cause}"
    # É2 — Générer la clé : les DEUX fichiers existent (côté hors-ligne)
    manquants = [nom for nom, chemin in
                 (("clé privée", privee), ("clé publique", publique))
                 if not (chemin and os.path.isfile(chemin))]
    if manquants:
        e2 = (False, f"absent(es) : {', '.join(manquants)} — privée "
                     f"{privee}, publique {publique}")
    else:
        e2 = True, f"paire présente ({privee})"
    # É3 — Signer : la remise VÉRIFIÉE contre a-signer + clé publique
    # (ceremonie_hors_ligne.py verifier — pur standard, aucune pile)
    if not all(chemin and os.path.isfile(chemin)
               for chemin in (a_signer, signatures, publique)):
        e3 = (False, f"fichiers manquants — a-signer : {a_signer} ; "
                     f"signatures : {signatures} ; clé publique : "
                     f"{publique}")
    else:
        try:
            code_h, _ = executer_cli(
                "ceremonie_hors_ligne.py",
                ["verifier", a_signer, signatures, publique])
            e3 = ((code_h == 0),
                  "remise vérifiée (signatures == a-signer == clé publique)"
                  if code_h == 0 else
                  "la remise ne correspond pas (a-signer changé depuis la "
                  "signature ? re-signez)")
        except ErreurCeremonie as exc:
            e3 = False, str(exc)
    # É4 — Déposer : le vérificateur du dépôt dit VERT
    e4 = {0: (True, "10 arbres VERTS sous la clé déposée"),
          10: (False, "signature requise (arbres divergés de leur "
                      "manifeste déposé)"),
          11: (False, "signature déposée invalide"),
          12: (False, "dépôt incohérent (code 12)")}.get(
              code_verif, (False, f"état inconnu — {cause}"))
    # É5 — Git : sceau-I commité ET poussé (status --porcelain -b)
    code_g, texte_g = executer_git(
        ["status", "--porcelain", "-b", "--"] + list(chemins_git))
    if code_g == 127:
        e5 = False, "git introuvable sur cette machine"
    elif code_g != 0:
        e5 = False, "le dossier attaché n'est pas un dépôt git"
    else:
        lignes_g = texte_g.splitlines()
        branche = lignes_g[0] if lignes_g and lignes_g[0].startswith("##") \
            else ""
        sales = [ligne for ligne in lignes_g[1:] if ligne.strip()]
        if sales:
            e5 = (False, f"{len(sales)} changement(s) non commité(s) dans "
                         f"{', '.join(chemins_git)}")
        elif "ahead" in branche:
            e5 = (False, f"commit(s) local(aux) NON POUSSÉ(S) "
                         f"({branche.strip(' #')})")
        else:
            e5 = True, f"{', '.join(chemins_git)} propre et poussé"
    etats_sceau = (e1, e2, e3, e4, e5)
    if scenario == SCENARIO_GIT:
        lignes = [(1, TITRE_ETAPE_CLONE, *preuve_clone())]
        lignes += [(i + 2, FIL_ETAPES[i][1], *etat)
                   for i, etat in enumerate(etats_sceau)]
        return lignes
    return [(FIL_ETAPES[i][0], FIL_ETAPES[i][1], *etat)
            for i, etat in enumerate(etats_sceau)]


# ---------------------------------------------------------------------------
# CF1 : la phrase de contrôle à VOUS (D110) — alphanumérique, sans plafond
# ---------------------------------------------------------------------------

LOG2_62 = 5.954196310386875     # log2(62) — l'alphabet A-Z a-z 0-9
PLANCHER_PHRASE = 8             # fail-closed ; recommandé : 22 ≈ 128 bits


def entropie_bits(longueur):
    """Entropie ESTIMÉE d'une phrase alphanumérique (bits) — estimation
    honnête pour un choix UNIFORME ; un choix humain mémorisable (mots,
    suites logiques) vaut typiquement MOINS : la longueur est un plafond,
    pas une promesse."""
    return longueur * LOG2_62


def phrase_personnelle_valide(phrase):
    """Valide la phrase de contrôle CHOISIE par l'utilisateur (D110).

    Retour (ok, message). Le message NOMME la règle violée — il ne révèle
    JAMAIS le caractère fautif (seule sa POSITION : corriger sans que le
    journal n'apprenne le contenu).

    Règles (la demande développeur D110, telle quelle) :
      - alphanumérique ASCII : A-Z, a-z, 0-9 — espaces, accents, symboles
        refusés PAR CONCEPTION, échec nommé avec position ;
      - plancher 8 caractères (fail-closed : en dessous, Argon2id ne
        sauvera pas une phrase devinable) ;
      - AUCUN plafond de longueur : Argon2id digère toute taille
        (10 000 caractères passent — prouvé par test_ceremonie_gui.py T8).
    """
    if not phrase:
        return False, "phrase vide — refus (fail-closed)"
    for i, caractere in enumerate(phrase):
        if not (caractere.isascii() and caractere.isalnum()):
            if caractere.isspace():
                genre = "une espace"
            elif not caractere.isascii():
                genre = ("une lettre accentuée ou non latine"
                         if caractere.isalpha() else
                         "un chiffre ou symbole non ASCII")
            else:
                genre = "un symbole ou signe de ponctuation"
            return False, (f"caractère non alphanumérique en position "
                           f"{i + 1} ({genre}) — la phrase personnelle "
                           "n'accepte QUE A-Z, a-z, 0-9 (espaces et "
                           "accents refusés par conception, D110)")
    if len(phrase) < PLANCHER_PHRASE:
        return False, (f"{len(phrase)} caractère(s) — plancher fail-closed : "
                       f"{PLANCHER_PHRASE} minimum (recommandé : "
                       "22 caractères ≈ 128 bits)")
    bits = entropie_bits(len(phrase))
    if bits < 128:
        return True, (f"alphanumérique, {len(phrase)} caractères — "
                      f"≈ {bits:.0f} bits d'entropie, sans plafond de "
                      "longueur — AVERTISSEMENT : moins de 128 bits "
                      "(22 caractères)")
    return True, (f"alphanumérique, {len(phrase)} caractères — ≈ {bits:.0f} "
                  "bits d'entropie, sans plafond de longueur")


# ---------------------------------------------------------------------------
# CF2 : nouvelles capacités de cérémonie (attestées par test_ceremonie_gui)
# ---------------------------------------------------------------------------

def controle_lecture(chemin_config, fichiers_copies, emit=None):
    """Le CONTRÔLE DE RELECTURE : vérifie que les copies hors-ligne de
    l'utilisateur reconstituent bien le seuil — SANS rien écrire nulle part.

    Méthode : fragments des copies -> gardes virtuelles (temporaire) ->
    deverrouiller() : reconstitution Shamir + vérification + AEAD du
    conteneur RÉEL. Si le déverrouillage passe, la relève après brûlage
    est garantie (les copies sont la loi). m est effacé aussitôt (spec § 8).
    """
    cf2 = _module_cf2()
    config = cf2.lire_config(chemin_config)
    conteneur = config["conteneur"]
    if not os.path.isfile(conteneur):
        raise ErreurCeremonie(f"conteneur CF2 introuvable : {conteneur}")
    with open(conteneur, "rb") as f:
        entete = cf2._parser_entete(f.read())
    t, n = entete["t"], entete["n"]
    sel_coffre = entete["sel"].hex()
    if len(fichiers_copies) != t:
        raise ErreurCeremonie(
            f"le contrôle exige EXACTEMENT le seuil de copies : {t} "
            f"(reçu : {len(fichiers_copies)}) — ni moins (impossible), "
            f"ni plus (le contrôle mesure le pire cas de brûlage)")
    parses, xs = [], []
    for chemin in fichiers_copies:
        try:
            with open(chemin, "r", encoding="ascii") as f:
                texte = f.read()
        except (OSError, UnicodeDecodeError) as exc:
            raise ErreurCeremonie(f"copie illisible : {chemin} ({exc})")
        try:
            d = cf2.parser_fragment(texte)
        except cf2.ErreurCoffre as exc:
            raise ErreurCeremonie(f"copie INVALIDE {os.path.basename(chemin)} "
                                  f"corrompue ou falsifiée : {exc}")
        if d["coffre"] != sel_coffre:
            raise ErreurCeremonie(
                f"copie {os.path.basename(chemin)} : sel du coffre divergent "
                f"— fragment d'un AUTRE coffre (spec § 4)")
        if (d["t"], d["n"]) != (t, n):
            raise ErreurCeremonie(
                f"copie {os.path.basename(chemin)} : seuil divergent "
                f"{d['t']}/{d['n']} (conteneur : {t}/{n})")
        parses.append((chemin, texte, d))
        xs.append(d["x"])
    if len(set(xs)) != len(xs):
        raise ErreurCeremonie(
            f"les {t} copies doivent porter {t} indices x DISTINCTS "
            f"(reçu : {sorted(xs)}) — deux fois la même copie ne relève rien")
    if emit:
        emit(f"[ceremonie] contrôle de relecture : {t} copies, indices "
             f"x={sorted(xs)} — reconstitution en cours…")
    with tempfile.TemporaryDirectory(prefix="cf2-relecture-") as tmp:
        gardes_virtuelles = []
        for chemin, texte, d in parses:
            garde = os.path.join(tmp, f"g{d['x']}")
            os.makedirs(garde, exist_ok=True)
            with open(os.path.join(garde, f"fragment-{d['x']}.cf2f"), "w",
                      encoding="ascii") as f:
                f.write(texte)
            gardes_virtuelles.append(garde)
        try:
            base, _, m, _ = cf2.deverrouiller(conteneur, gardes_virtuelles)
            cf2._effacer(m)
            del m
        except cf2.ErreurCoffre as exc:
            return False, (f"[ceremonie] contrôle de relecture : ÉCHEC — {exc}\n"
                           f"  Les copies ne reconstituent PAS le seuil : après "
                           f"un brûlage, la relève serait IMPOSSIBLE avec ces "
                           f"copies. Recopiez depuis les gardes du coffre.")
    nb = sum(len(p.get("entrees", [])) for p in base["projets"].values())
    return True, (f"[ceremonie] contrôle de relecture : VERT — les {t} copies "
                  f"reconstituent la clé maîtresse et le conteneur s'ouvre "
                  f"(AEAD vert, {len(base['projets'])} projet(s), {nb} "
                  f"entrée(s))\n  La relève après brûlage est garantie avec "
                  f"ces copies. m a été effacée de la RAM (spec § 8).")


def exporter_feuille(chemin_config, chemin_sortie, numeros=None):
    """Feuille IMPRIMABLE des fragments à copier hors-ligne (= le seuil).

    Par défaut les TROIS dernières gardes (g3, g4, g5 — écho du LISEZMOI).
    Le fragment sérialisé est déjà du texte hexadécimal transportable à la
    main : la feuille ajoute les consignes de garde (deux lieux, le seuil
    est la loi)."""
    cf2 = _module_cf2()
    config = cf2.lire_config(chemin_config)
    t, n = config["t"], config["n"]
    if numeros is None:
        numeros = list(range(n - t + 1, n + 1))
    if len(numeros) != t:
        raise ErreurCeremonie(
            f"la feuille exporte le SEUIL de fragments ({t}), reçu : "
            f"{len(numeros)}")
    blocs, manquantes = [], []
    for i in numeros:
        if not 1 <= i <= n:
            raise ErreurCeremonie(f"garde hors bornes : g{i} (coffre : {n})")
        chemin_frag = os.path.join(config["gardes"][i - 1],
                                   f"fragment-{i}.cf2f")
        if not os.path.isfile(chemin_frag):
            manquantes.append(chemin_frag)
            continue
        with open(chemin_frag, "r", encoding="ascii") as f:
            texte = f.read().strip()
        try:
            cf2.parser_fragment(texte)      # tag vérifié avant impression
        except cf2.ErreurCoffre as exc:
            raise ErreurCeremonie(f"fragment g{i} INVALIDE — {exc}")
        blocs.append(f"--- COPIE {blocs and len(blocs) + 1 or 1} "
                     f"(garde g{i}) ---\n{texte}\n")
    if manquantes:
        raise ErreurCeremonie("fragments absents des gardes : "
                              + ", ".join(manquantes))
    try:
        with open(chemin_sortie, "w", encoding="utf-8") as f:
            f.write(
            "TRIADE — FRAGMENTS HORS-LIGNE DU COFFRE CF2 (D86)\n"
            "=================================================\n"
            f"\n{t} fragments ci-dessous (= le seuil {t}/{n}). Chaque bloc\n"
            "entre « --- COPIE » et la ligne « tag: » EST une copie complète :\n"
            "imprimez cette feuille (ou copiez les blocs sur USB), DEUX lieux\n"
            "distincts de préférence. ATTENTION : le seuil est la loi — avec\n"
            "moins de ces copies, un brûlage laisse le coffre MORT pour de\n"
            "bonne.\n"
            "\nPour relever le coffre après un brûlage (profil dépôt,\n"
            "bouton Restaurer, ou python3 v06/coffre_cf2.py restaurer\n"
            "copie-1 copie-2 copie-3) :\n"
            + "\n".join(blocs) +
            "\nCONSIGNE FINALE : ce papier OUVRE le coffre s'il survit au\n"
            "brûlage — traitez-le comme la clé qu'il est.\n")
    except OSError as exc:
        raise ErreurCeremonie(f"impossible d'écrire la feuille : {exc}")
    return (f"[ceremonie] feuille exportée : {chemin_sortie} ({t} fragments, "
            f"gardes g{numeros[0]}…g{numeros[-1]}, tags vérifiés avant "
            f"impression)")


def liste_blanche_lire(chemin_config):
    cf2 = _module_cf2()
    return list(cf2.lire_config(chemin_config).get("liste_blanche", []))


def liste_blanche_ecrire(chemin_config, motifs):
    """Réécrit la liste blanche via ecrire_config (atomique, 0600) —
    le reste de la config est préservé tel quel."""
    cf2 = _module_cf2()
    config = cf2.lire_config(chemin_config)
    config["liste_blanche"] = list(motifs)
    cf2.ecrire_config(chemin_config, config)


def motif_valide(motif):
    try:
        import re
        re.compile(motif)
        return bool(motif.strip())
    except re.error:
        return False


def motif_teste(motif, chaine):
    """re.search du motif contre une image/ligne de commande COMPLÈTE."""
    import re
    return re.search(motif, chaine) is not None


def sentinelle_demarrer_detachee(chemin_config, attente_max=5.0):
    """Démarre la sentinelle DÉTACHÉE du GUI (elle vit tant que la machine
    vit) et attend son heart-beat (borne labo : 5 s). Retour (ok, texte)."""
    import time
    cf2 = _module_cf2()
    config = cf2.lire_config(chemin_config)
    chemin_sentinelle = os.path.join(RACINE_DEPOT, "v06", "sentinelle_cf2.py")
    chemin_log = _chemin_log_sentinelle(chemin_config)
    kwargs = {}
    if os.name == "nt":
        kwargs["creationflags"] = (subprocess.DETACHED_PROCESS
                                   | subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        kwargs["start_new_session"] = True
    with open(chemin_log, "ab") as f_log:
        f_log.write(f"\n--- demarrage GUI {time.strftime('%Y-%m-%dT%H:%M:%S')}"
                    f" ---\n".encode("utf-8"))
        f_log.flush()
        proc = subprocess.Popen(
            [sys.executable, chemin_sentinelle, "demarrer",
             "--config", chemin_config],
            cwd=RACINE_DEPOT, stdout=f_log, stderr=subprocess.STDOUT,
            env=dict(os.environ, PYTHONIOENCODING="utf-8",
                     PYTHONUNBUFFERED="1"), **kwargs)
    import json
    t0 = time.time()
    while time.time() - t0 < attente_max:
        hb = config.get("heartbeat")
        if hb and os.path.isfile(hb):
            try:
                with open(hb, "r", encoding="utf-8") as f:
                    if time.time() - json.load(f)["ts"] < 1.0:
                        return True, (f"[ceremonie] sentinelle VIVANTE "
                                      f"(pid {proc.pid}, heart-beat frais, "
                                      f"sortie journalisée dans {chemin_log}) "
                                      f"— elle vit détachée du GUI : fermer la "
                                      f"fenêtre ne la tue pas")
            except (OSError, ValueError):
                pass
        time.sleep(0.05)
    return False, (f"[ceremonie] sentinelle SANS heart-beat frais après "
                   f"{attente_max:.0f} s (pid {proc.pid}) — consultez "
                   f"{chemin_log}")


# ===========================================================================
# SECTION D — la GUI (tkinter, import PROTÉGÉ : --selftest et le profil
# hors-ligne restent utilisables sur une machine sans tkinter ; l'aide
# d'installation exacte s'affiche alors en console).
# ===========================================================================

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    TKINTER_DISPONIBLE, TKINTER_ERREUR = True, ""
except ImportError as _exc:
    TKINTER_DISPONIBLE, TKINTER_ERREUR = False, str(_exc)

COULEUR_VERTE = "#1a7f37"
COULEUR_ROUGE = "#b42318"
COULEUR_ENCRE = "#1f2328"
COULEUR_ATTENTE = "#9a6700"
POLICE_FIXE = ("TkFixedFont", 10)


def _message_tkinter_manquant():
    if sys.platform.startswith("linux"):
        aide = ("Linux : sudo apt install python3-tk   (Debian/Ubuntu) ; "
                "sudo dnf install python3-tkinter   (Fedora)")
    elif sys.platform == "darwin":
        aide = ("macOS : brew install python-tk   — ou réinstallez Python "
                "depuis python.org (installeur incluant « Tcl/Tk »)")
    else:
        aide = ("Windows : réinstallez Python depuis python.org en cochant "
                "« tcl/tk and IDLE » (inclus par défaut)")
    print("tkinter est absent de ce Python — la GUI ne peut pas s'ouvrir.\n"
          f"  {aide}\n  (tkinter ne s'installe PAS via pip : c'est une "
          f"composante de Python elle-même.)")
    print(f"  détail : {TKINTER_ERREUR}")
    try:
        import time
        time.sleep(20)      # double-clic Windows : laisse lire le message
    except Exception:
        pass


def demarrer_gui(profil=None):
    """Construit et lance la fenêtre. Retour 0/1 (pour exit())."""
    if not TKINTER_DISPONIBLE:
        _message_tkinter_manquant()
        return 1
    app = Application(profil=profil)
    app.racine.mainloop()          # Application est une enveloppe : le Tk est racine
    return 0


# ---------------------------------------------------------------------------
# Exécution asynchrone : les cérémonies (pip, migration, autotest CLI) ne
# gèlent JAMAIS la fenêtre ; la sortie coule ligne à ligne dans le journal.
# ---------------------------------------------------------------------------
import queue   # noqa: E402
import threading   # noqa: E402


class Executeur:
    """Un fil d'exécution + une file : marshal vers le fil tkinter via
    racine.after (tkinter n'est PAS thread-safe — la file est la frontière)."""

    def __init__(self, application):
        self.app = application
        self.file = queue.Queue()
        self.occupe = False
        self.fil = None

    def lancer(self, titre, fonction, args=()):
        if self.occupe:
            return False
        self.occupe = True
        self.app.journal.ajoute(f"── {titre} ──", "titre")
        self.app.verdict(None, f"{titre} : en cours…")
        self.fil = threading.Thread(target=self._fil, args=(fonction, args),
                                     daemon=True)
        self.fil.start()
        return True

    def _fil(self, fonction, args):
        emit = self.emit
        try:
            r = fonction(*args, emit=emit) if _exige_emit(fonction) else \
                fonction(*args)
        except ErreurCeremonie as exc:
            ENREGISTREUR.ligne(f"échec nommé : {exc}", "echec")
            r = (False, f"ÉCHEC : {exc}")
        except Exception as exc:            # garde-fou : nommé, jamais muet
            ENREGISTREUR.ligne(
                f"échec inattendu ({type(exc).__name__}) : {exc}", "crash")
            ENREGISTREUR.traceback()
            r = (False, f"échec inattendu ({type(exc).__name__}) : {exc}")
        r = _normalise(r)
        self.file.put(("fin", r))

    def emit(self, ligne):
        self.file.put(("ligne", str(ligne)))

    def pompe(self):
        try:
            while True:
                genre, donnees = self.file.get_nowait()
                if genre == "ligne":
                    self.app.journal.ajoute(donnees)
                else:
                    ok, texte = donnees
                    self.occupe = False
                    self.app.verdict(ok, texte)
                    fin_action = getattr(self.app, "_sur_fin_action", None)
                    if callable(fin_action):
                        fin_action()   # D116 : le fil se ré-évalue
        except queue.Empty:
            pass
        self.app.racine.after(80, self.pompe)


def _exige_emit(fonction):
    """Les contrôleurs déclarant un paramètre « emit » le reçoivent (uniforme)."""
    import inspect
    try:
        return "emit" in inspect.signature(fonction).parameters
    except (TypeError, ValueError):
        return False


def _normalise(r):
    if isinstance(r, str):
        return True, r
    if isinstance(r, bool):
        return r, ("VERT" if r else "ÉCHEC")
    if isinstance(r, int):
        return r == 0, ("" if r == 0 else f"code de sortie {r}")
    if isinstance(r, tuple) and len(r) == 2:
        return bool(r[0]), str(r[1])
    return True, str(r)


class Journal:
    """Le journal de cérémonie : trace TEXTUELLE de tout ce qui s'est passé
    (la preuve de passage reste aux CLI et tests — le journal est pour
    l'humain)."""

    def __init__(self, parent, application):
        self.app = application
        cadre = ttk.LabelFrame(parent, text="Journal de cérémonie")
        cadre.pack(side="bottom", fill="both", expand=True, padx=10, pady=(4, 10))
        self.cadre = cadre    # D116 : mesure pour la fenêtre au contenu
        barre = ttk.Frame(cadre)
        barre.pack(side="top", fill="x", padx=6, pady=(2, 0))
        ttk.Button(barre, text="Envoyer le rapport…", width=20,
                   command=lambda: self.app.envoyer_rapport()).pack(
                       side="right", padx=(6, 0))   # D113 : la main tendue
        ttk.Button(barre, text="Copier tout", width=12,
                   command=self.copier).pack(side="right", padx=(6, 0))
        ttk.Button(barre, text="Effacer", width=8,
                   command=self.effacer).pack(side="right")
        self.texte = tk.Text(cadre, height=9, wrap="word", state="disabled",
                             font=POLICE_FIXE, background="#ffffff",
                             relief="flat", highlightthickness=1,
                             highlightbackground="#d0d7de")
        self.texte.pack(side="top", fill="both", expand=True, padx=6, pady=4)
        for tag, couleur in (("titre", "#0969da"), ("info", COULEUR_ENCRE),
                             ("pip", "#8250df"), ("vert", COULEUR_VERTE),
                             ("rouge", COULEUR_ROUGE)):
            self.texte.tag_configure(tag, foreground=couleur)
        self.texte.tag_configure("titre", font=(POLICE_FIXE[0], 10, "bold"))

    def ajoute(self, ligne, genre="info"):
        ENREGISTREUR.ligne(str(ligne), genre)   # D113 : tout voit la boîte noire
        self.texte.configure(state="normal")
        self.texte.insert("end", str(ligne) + "\n", genre)
        self.texte.see("end")
        self.texte.configure(state="disabled")

    def copier(self):
        self.app.racine.clipboard_clear()
        self.app.racine.clipboard_append(self.texte.get("1.0", "end"))

    def effacer(self):
        ENREGISTREUR.ligne("journal d'écran effacé (la boîte noire garde tout)",
                           "info")
        self.texte.configure(state="normal")
        self.texte.delete("1.0", "end")
        self.texte.configure(state="disabled")


# ---------------------------------------------------------------------------
# L'application
# ---------------------------------------------------------------------------
class Application:

    def __init__(self, profil=None):
        self.racine = tk.Tk()
        self.racine.title("TRIADE — Maître de cérémonie")
        # D116 — plus de géométrie fixe : chaque page affichée redimensionne
        # la fenêtre à son contenu (_ajuster_taille_fenetre, clampée à
        # l'écran) ; l'ancienne fenêtre fixe (1020x740) pouvait laisser le
        # bouton « Retour à l'accueil » hors de vue, en bas d'une page plus
        # haute qu'elle.
        self.racine.minsize(880, 600)
        self._batir_style()
        self._batir_header()
        # D113 — ORDRE DE PACK = PRIORITÉ D'ESPACE. Avant : le corps (packé
        # en premier, expand) évinçait le journal et la barre de verdict hors
        # de la fenêtre dès que la page demandait plus de haut que l'écran
        # (page dépôt : ~1000 px) — « aucun journal qui s'affiche ». Désormais
        # verdict et journal se packent AVANT (garantis) ; le corps, packé en
        # DERNIER, DÉFILE au lieu d'évincer (_batir_corps_defilant).
        self._batir_statut()
        self.journal = Journal(self.racine, self)
        self._batir_corps_defilant()
        self.pages = {}
        self.executeur = Executeur(self)
        # D113 — un crash dans un rappel tkinter (bouton, trace, after) va
        # dans le journal VISIBLE et la boîte noire : plus jamais un
        # traceback muet vers stderr (invisible lancé via .bat sans console).
        self.racine.report_callback_exception = self._sur_crash_rappel
        ENREGISTREUR.entete(self.racine)
        self.depot_pret = depot_disponible()
        self.scenario = None            # D117 : aucun scénario choisi AVANT TOUT
        self._batir_accueil()
        self._batir_hors_ligne()
        self._batir_depot()
        self._racine_pages = RACINE_DEPOT   # D117 : détecte un attachement post-clone
        self.executeur.pompe()
        self._autotest_demarrage()
        cible = {"hors-ligne": "hors-ligne", "depot": "depot"}.get(profil)
        self.montrer(cible if (cible and (cible != "depot" or self.depot_pret))
                     else "accueil")

    # --- squelette ---------------------------------------------------------
    def _batir_style(self):
        style = ttk.Style(self.racine)
        try:
            style.theme_use("clam")     # rendu homogène multi-plateformes
        except tk.TclError:
            pass
        style.configure(".", background="#f6f8fa", foreground=COULEUR_ENCRE,
                        font=("Segoe UI", 10))
        style.configure("Titre.TLabel", font=("Segoe UI", 15, "bold"))
        style.configure("Sous.TLabel", foreground="#57606a")
        style.configure("Carte.TLabelframe", borderwidth=1,
                        relief="solid", padding=8)
        style.configure("Verdict.TLabel", font=("Segoe UI", 10, "bold"))

    def _batir_header(self):
        cadre = ttk.Frame(self.racine)
        cadre.pack(side="top", fill="x", padx=10, pady=(10, 0))
        self.cadre_header = cadre          # D116 : mesure de la fenêtre
        ttk.Label(cadre, text="TRIADE — Maître de cérémonie",
                  style="Titre.TLabel").pack(side="left")
        ttk.Button(cadre, text="Envoyer le journal…", width=20,
                   command=self.envoyer_rapport).pack(
                       side="right", padx=(0, 12))   # D113 : toujours visible
        self.badge_autotest = ttk.Label(cadre, text="autotest RFC 8032 : …",
                                        style="Sous.TLabel")
        self.badge_autotest.pack(side="right")
        ttk.Label(cadre, text=VERSION_GUI + "   ·   "
                  "la clé privée ne traverse jamais la machine connectée",
                  style="Sous.TLabel").pack(side="right", padx=12)
        # D116 — le retour à l'accueil vit dans le BANDEAU : TOUJOURS
        # visible, hors du corps défilant (jamais plus chassé en bas d'une
        # page trop haute par la fenêtre fixe d'avant).
        self.bouton_accueil = ttk.Button(cadre, text="← Accueil", width=10,
                                         state="disabled",
                                         command=self._retour_accueil)
        self.bouton_accueil.pack(side="right")

    def _batir_statut(self):
        self.var_verdict = tk.StringVar(value="")
        self.label_verdict = ttk.Label(self.racine, textvariable=self.var_verdict,
                                       style="Verdict.TLabel", anchor="w",
                                       padding=(12, 4))
        self.label_verdict.pack(side="bottom", fill="x")
        self.label_verdict.configure(foreground=COULEUR_ATTENTE)

    def montrer(self, nom):
        for page in self.pages.values():
            page.pack_forget()
        self.pages[nom].pack(fill="both", expand=True)
        # D116 — le bandeau porte le retour à l'accueil (visible PARTOUT),
        # la fenêtre prend la taille de la page affichée, et l'entrée du
        # profil dépôt ré-évalue le fil de cérémonie.
        self.bouton_accueil.configure(
            state="disabled" if nom == "accueil" else "normal")
        self._ajuster_taille_fenetre()
        if nom == "depot":
            self._rafraichir_fil()

    def verdict(self, ok, texte):
        prem = texte.strip().splitlines()[0] if texte.strip() else ""
        etat = "…" if ok is None else ("VERT" if ok else "ÉCHEC")
        ENREGISTREUR.ligne(f"verdict {etat} : {prem if prem else '—'}",
                           "verdict")
        self.var_verdict.set(prem if prem else ("VERT" if ok else "ÉCHEC"))
        self.label_verdict.configure(
            foreground=COULEUR_VERTE if ok else COULEUR_ROUGE
            if ok is not None else COULEUR_ATTENTE)
        if texte.strip():
            self.journal.ajoute(texte, "vert" if ok else "rouge")

    def action(self, titre, fonction, *args):
        """Point d'entrée UNIFIÉ : refuse pendant qu'une cérémonie tourne."""
        if self.executeur.occupe:
            self._dialogue("showinfo", 
                "Cérémonie en cours",
                "Une action est déjà en cours — attendez son verdict "
                "dans le journal avant d'en lancer une autre.")
            return
        self.executeur.lancer(titre, fonction, args)

    def _cli(self, module, args, phrase=None, emit=None,
             nouvelle_phrase=None, au_racine=False):
        """Adaptateur : le verdict du CLI (code 0) devient le verdict GUI.
        reçoit l'émetteur de l'exécuteur (streaming ligne à ligne) quand la
        signature le demande (cf. _exige_emit) — functools.partial le
        transmet. D114 : quand la sortie a déjà coulé ligne à ligne dans le
        journal (emit), le verdict ne la RÉPÈTE plus en bloc — une seule
        ligne d'ancrage (la première, celle de la barre), le détail vit
        au-dessus dans l'ordre du flux ; sans emit (pas de flux), le texte
        entier reste la remise du verdict."""
        code, texte = executer_cli(module, args, emit=emit, phrase=phrase,
                                   nouvelle_phrase=nouvelle_phrase,
                                   au_racine=au_racine)
        ok = code == 0
        if emit is not None and texte.strip():
            texte = texte.strip().splitlines()[0]
        return ok, (texte if texte.strip() else
                    ("VERT" if ok else f"code de sortie {code}"))

    def _autotest_demarrage(self):
        ok = autotest()
        self.badge_autotest.configure(
            text="autotest RFC 8032 : " + ("VERT" if ok else "ÉCHEC"),
            foreground=COULEUR_VERTE if ok else COULEUR_ROUGE)
        self.journal.ajoute(
            "[ceremonie] autotest RFC 8032 : " + ("VERT" if ok else "ÉCHEC"),
            "vert" if ok else "rouge")

    # ------------------------------------------------------------------
    # D113 — corps défilant, crashes, dialogues, rapport (boîte noire)
    # ------------------------------------------------------------------
    def _batir_corps_defilant(self):
        """Le corps vit dans un canevas défilant : une page plus haute que
        la fenêtre reste ENTÈREMENT atteignable (molette + barre), sans
        jamais rogner le journal (garanti par l'ordre de pack)."""
        conteneur = ttk.Frame(self.racine)
        conteneur.pack(side="top", fill="both", expand=True, padx=10, pady=6)
        self.zone_defilement = tk.Canvas(conteneur, highlightthickness=0,
                                         background="#f6f8fa")
        self.zone_defilement.pack(side="left", fill="both", expand=True)
        self.barre_defilement = ttk.Scrollbar(
            conteneur, orient="vertical",
            command=self.zone_defilement.yview)
        self.barre_defilement.pack(side="left", fill="y")
        self.zone_defilement.configure(
            yscrollcommand=self.barre_defilement.set)
        self.corps = ttk.Frame(self.zone_defilement)
        self._fenetre_interne = self.zone_defilement.create_window(
            (0, 0), window=self.corps, anchor="nw")
        self.corps.bind("<Configure>", self._sur_taille_corps)
        self.zone_defilement.bind("<Configure>", self._sur_taille_canevas)
        # molette multi-plateformes : Windows/macOS <MouseWheel>, Linux
        # <Button-4>/<Button-5> — le journal Text garde sa propre molette.
        self.racine.bind_all("<MouseWheel>", self._sur_molette)
        self.racine.bind_all("<Button-4>", self._sur_molette)
        self.racine.bind_all("<Button-5>", self._sur_molette)

    def _sur_taille_corps(self, evenement):
        self.zone_defilement.configure(
            scrollregion=self.zone_defilement.bbox("all"))

    def _sur_taille_canevas(self, evenement):
        # le contenu s'étire à la LARGEUR de la fenêtre : jamais de coupe
        # horizontale, la barre ne sert qu'au vertical.
        self.zone_defilement.itemconfigure(self._fenetre_interne,
                                           width=evenement.width)

    def _sur_molette(self, evenement):
        try:
            vise = self.zone_defilement.winfo_containing(evenement.x_root,
                                                         evenement.y_root)
        except tk.TclError:
            vise = None
        if isinstance(vise, tk.Text):    # le journal défile tout seul
            return
        delta = int(getattr(evenement, "delta", 0) or 0)
        if delta:
            pas = -(delta // 120) if abs(delta) >= 120 else -delta
        else:
            pas = -1 if int(getattr(evenement, "num", 0) or 0) == 4 else 1
        self.zone_defilement.yview_scroll(int(pas), "units")

    def _sur_crash_rappel(self, type_exc, valeur, tb):
        """report_callback_exception : le crash d'un rappel tkinter, avant
        MUET (stderr — invisible lancé via .bat sans console), devient un
        échec NOMMÉ à l'écran + traceback complet dans la boîte noire."""
        ENREGISTREUR.ligne("CRASH dans un rappel tkinter :", "crash")
        for ligne in "".join(traceback.format_exception(type_exc, valeur,
                                                        tb)).splitlines():
            ENREGISTREUR.ligne(ligne, "crash")
        self.journal.ajoute(
            f"CRASH CAPTURÉ ({type_exc.__name__}) : {valeur} — détail "
            "complet dans le rapport (bouton « Envoyer le rapport… »)",
            "rouge")
        self.verdict(False, f"crash capturé : {valeur}")

    def _dialogue(self, genre, titre, message, **options):
        """D113 — TOUTE boîte de dialogue passe par ici : parent EXPLICITE
        (un dialogue sans parent peut naître DERRIÈRE la fenêtre — sur
        Windows, le GUI semblait mort : « je clique, rien ne se passe ») et
        posée/résolue dans la boîte noire (titre + réponse ; les dialogues
        ne contiennent jamais un secret)."""
        ENREGISTREUR.ligne(f"dialogue « {titre} » posé", "dialogue")
        reponse = getattr(messagebox, genre)(titre, message,
                                             parent=self.racine, **options)
        ENREGISTREUR.ligne(f"dialogue « {titre} » → {reponse!r}", "dialogue")
        return reponse

    def constituer_rapport(self):
        """Rapport complet : environnement + journal d'écran + journal de
        vol brut. Aucun secret n'y figure (phrase par temporaires détruits,
        graine jamais affichée — D87/D110)."""
        lignes = [
            "RAPPORT DE CÉRÉMONIE — " + VERSION_GUI,
            "généré le "
            + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            f"python {sys.version.split()[0]} — {platform.platform()}",
            f"dépôt attaché : {RACINE_DEPOT} (source : {SOURCE_DEPOT})",
            "pile du dépôt : "
            + ("présente" if dependances_disponibles() else "ABSENTE"),
            f"boîte noire : {CHEMIN_JOURNAL_VOL}",
            "=" * 72,
            "JOURNAL D'ÉCRAN (ce que la fenêtre a affiché) :",
            self.journal.texte.get("1.0", "end").rstrip() or "(vide)",
            "=" * 72,
            "JOURNAL DE VOL (boîte noire, horodatée) :",
        ]
        try:
            with open(CHEMIN_JOURNAL_VOL, "r", encoding="utf-8") as f:
                brut = f.read().splitlines()
            if len(brut) > 3000:   # garde-fou : le récent suffit au diagnostic
                lignes.append(f"… ({len(brut) - 3000} lignes plus anciennes "
                              "tronquées)")
                brut = brut[-3000:]
            lignes.extend(brut)
        except OSError as exc:
            lignes.append(f"(boîte noire illisible : {exc})")
        return "\n".join(lignes)

    def envoyer_rapport(self):
        """D113 — le rapport part par la main de l'humain : fichier .txt +
        presse-papiers + dossier ouvert. AUCUN réseau (discipline hors-ligne
        : la cérémonie ne prend pas de réseau pour se faire débugger) ; le
        transport, c'est vous (glisser le fichier dans la conversation)."""
        ENREGISTREUR.ligne("bouton « Envoyer le rapport » actionné", "envoi")
        rapport = self.constituer_rapport()
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("Envoyer le rapport de cérémonie (D113)")
        fenetre.geometry("880x560")
        fenetre.transient(self.racine)
        zone = ttk.Frame(fenetre, padding=8)
        zone.pack(fill="both", expand=True)
        barre = ttk.Frame(zone)
        barre.pack(fill="x", pady=(0, 4))

        def copier():
            self.racine.clipboard_clear()
            self.racine.clipboard_append(rapport)
            self.journal.ajoute("[ceremonie] rapport copié dans le "
                                "presse-papiers (D113)", "info")
            ENREGISTREUR.ligne("rapport copié dans le presse-papiers", "envoi")

        def enregistrer():
            horodatage = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            bureau = os.path.join(os.path.expanduser("~"), "Desktop")
            chemin = filedialog.asksaveasfilename(
                parent=fenetre, title="Enregistrer le rapport de cérémonie",
                defaultextension=".txt",
                initialfile=f"rapport-ceremonie-{horodatage}.txt",
                initialdir=bureau if os.path.isdir(bureau)
                else os.path.expanduser("~"),
                filetypes=[("Rapport", "*.txt"), ("Tout", "*.*")])
            if not chemin:
                return
            try:
                with open(chemin, "w", encoding="utf-8") as f:
                    f.write(rapport + "\n")
            except OSError as exc:
                self._dialogue("showerror", "Écriture impossible",
                               f"{chemin} :\n{exc}")
                return
            self.journal.ajoute(f"[ceremonie] rapport écrit : {chemin} "
                                "(D113)", "info")
            ENREGISTREUR.ligne(f"rapport écrit : {chemin}", "envoi")
            self._dialogue(
                "showinfo", "Rapport écrit",
                f"Rapport écrit :\n  {chemin}\n\nPour l'envoyer à "
                "l'assistant : glissez ce fichier dans la conversation "
                "(ou collez le presse-papiers).")

        def ouvrir_dossier():
            dossier = (os.path.dirname(CHEMIN_JOURNAL_VOL)
                       or os.path.expanduser("~"))
            ENREGISTREUR.ligne(f"dossier de la boîte noire ouvert : {dossier}",
                               "envoi")
            try:
                if sys.platform.startswith("win"):
                    os.startfile(dossier)   # noqa: S606 — ouverture dossier
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", dossier])
                else:
                    subprocess.Popen(["xdg-open", dossier])
            except OSError as exc:
                self._dialogue("showwarning", "Ouverture impossible",
                               f"{dossier} :\n{exc}")

        ttk.Button(barre, text="Copier tout le rapport",
                   command=copier).pack(side="left")
        ttk.Button(barre, text="Enregistrer sous (.txt)…",
                   command=enregistrer).pack(side="left", padx=6)
        ttk.Button(barre, text="Ouvrir le dossier de la boîte noire",
                   command=ouvrir_dossier).pack(side="left")
        texte = tk.Text(zone, wrap="word", font=POLICE_FIXE)
        barre_d = ttk.Scrollbar(zone, orient="vertical", command=texte.yview)
        texte.configure(yscrollcommand=barre_d.set)
        barre_d.pack(side="right", fill="y")
        texte.pack(side="left", fill="both", expand=True)
        texte.insert("1.0", rapport)
        texte.configure(state="disabled")
        ttk.Label(zone, style="Sous.TLabel", wraplength=820, justify="left",
                  text=("AUCUN réseau — le rapport part par vos mains : "
                        "glissez le fichier .txt dans la conversation de "
                        "l'assistant (ou collez le presse-papiers). Aucun "
                        "secret n'y figure : phrase et graine ne traversent "
                        "jamais les journaux (D87/D110).")
                  ).pack(fill="x", pady=(4, 0))

    # --- composants réutilisables -------------------------------------------
    def _ligne_fichier(self, parent, etiquette, mode="open", defaut="",
                       types=None):
        cadre = ttk.Frame(parent)
        ttk.Label(cadre, text=etiquette, width=26, anchor="w").pack(side="left")
        var = tk.StringVar(value=defaut)
        ttk.Entry(cadre, textvariable=var).pack(side="left", fill="x",
                                                expand=True, padx=(0, 6))

        def choisir():
            if mode == "save":
                chemin = filedialog.asksaveasfilename(
                    initialfile=os.path.basename(var.get() or defaut),
                    filetypes=types or [("Texte", "*.txt"), ("Tout", "*.*")])
            else:
                chemin = filedialog.askopenfilename(filetypes=types or
                                                     [("Texte", "*.txt"),
                                                      ("Tout", "*.*")])
            if chemin:
                var.set(chemin)

        ttk.Button(cadre, text="Parcourir…", width=11,
                   command=choisir).pack(side="left")
        cadre.pack(fill="x", pady=2)
        return var

    def _section(self, parent, titre):
        return ttk.LabelFrame(parent, text=titre, style="Carte.TLabelframe")

    def _note(self, parent, texte, couleur="#57606a"):
        ttk.Label(parent, text=texte, style="Sous.TLabel",
                  foreground=couleur, wraplength=880,
                  justify="left").pack(anchor="w", pady=(2, 4))

    # ------------------------------------------------------------------
    # PAGE ACCUEIL — choix du profil
    # ------------------------------------------------------------------
    def _batir_accueil(self):
        page = ttk.Frame(self.corps)
        self.pages["accueil"] = page
        ttk.Label(page, text="Quelle machine êtes-vous ?",
                  style="Titre.TLabel").pack(anchor="w", pady=(6, 2))
        self._note(page, "La clé privée de l'Intention naît et signe "
                         "HORS-LIGNE ; le dépôt connecté vérifie et installe "
                         "les remises. Les deux profils partagent ce fichier "
                         "mais jamais leurs secrets.")

        # --- D117 : LE SCÉNARIO AVANT TOUT -------------------------------
        # Deux scénarios déterminent les étapes affichées par le fil de
        # cérémonie (profil dépôt) : DOSSIER LOCAL (cinq étapes — le dépôt
        # vit déjà ici, on l'attache) et REPO GIT (six étapes — « Cloner le
        # dépôt » en tête, prouvé lecture seule ; bouton de clonage).
        scen = self._section(
            page, "Scénario de cérémonie — AVANT TOUT, comment le dépôt "
                  "arrive-t-il ici ? (D117)")
        scen.pack(fill="x", pady=6)
        self.cadre_scen_section = scen   # D117 : le panneau s'y re-bâtit
        self._note(scen, "Le scénario détermine les étapes affichées par le "
                         "fil de cérémonie du profil dépôt : DOSSIER LOCAL → "
                         "cinq étapes (le dépôt vit déjà sur cette machine) ; "
                         "REPO GIT → six étapes, « Cloner le dépôt » en tête "
                         "(le dépôt vient d'un distant — GitHub ou autre). "
                         "Changer de scénario se fait ici, à tout moment.")
        barre_sc = ttk.Frame(scen)
        barre_sc.pack(fill="x", pady=2)
        self.bouton_scen_dossier = ttk.Button(
            barre_sc, text="DOSSIER LOCAL — le dépôt est déjà ici",
            command=lambda: self._choisir_scenario(SCENARIO_DOSSIER))
        self.bouton_scen_dossier.pack(side="left", padx=(0, 6))
        self.bouton_scen_git = ttk.Button(
            barre_sc, text="REPO GIT — cloner depuis un distant",
            command=lambda: self._choisir_scenario(SCENARIO_GIT))
        self.bouton_scen_git.pack(side="left")
        self.label_scenario = ttk.Label(scen, style="Sous.TLabel",
                                        wraplength=880, justify="left")
        self.label_scenario.pack(anchor="w", pady=(4, 0))
        self.cadre_scen_panels = ttk.Frame(scen)
        self.cadre_scen_panels.pack(fill="x", pady=(4, 0))
        self._montrer_panels_scenario()

        hors_ligne = self._section(page, "Machine HORS-LIGNE — cérémonie de la clé I (D87)")
        hors_ligne.pack(fill="x", pady=6)
        self._note(hors_ligne, "Générer la clé (première fois), signer les "
                               "remises d'intention, re-vérifier une remise. "
                               "Python standard SEUL : rien à installer, "
                               "aucun réseau, la clé ne quitte jamais cette "
                               "machine.")
        ttk.Button(hors_ligne, text="Ouvrir le profil hors-ligne",
                   command=lambda: self.montrer("hors-ligne")).pack(anchor="w",
                                                                    pady=4)
        depot = self._section(page, "Machine du DÉPÔT (connectée) — sceau I + coffre CF2")
        depot.pack(fill="x", pady=6)
        self._note(depot, "Préparer/signer les arbres d'intention, déposer les "
                          "remises ; migrer le coffre CF1 vers CF2, exporter "
                          "les fragments, éditer la liste blanche, démarrer "
                          "la sentinelle, relever ou brûler.")
        self.bouton_depot = ttk.Button(
            depot, text="Ouvrir le profil dépôt",
            command=self._ouvrir_depot)
        self.bouton_depot.pack(anchor="w", pady=4)
        if self.depot_pret:
            ttk.Label(depot, style="Sous.TLabel", wraplength=880,
                      justify="left",
                      text=(f"dépôt attaché : {RACINE_DEPOT} "
                            f"(source : {SOURCE_DEPOT})")).pack(anchor="w")
        else:
            self.bouton_depot.configure(state="disabled")
            ttk.Label(depot, style="Sous.TLabel", foreground="#9a6700",
                      wraplength=880, justify="left",
                      text=(f"(indisponible : v06/coffre_cf2.py introuvable "
                            f"dans {RACINE_DEPOT} — source : "
                            f"{SOURCE_DEPOT}). Le GUI peut vivre n'importe "
                            "où : CHOISISSEZ le dossier du dépôt par le "
                            "bouton ci-dessous (D112 — plus besoin de "
                            "relancer), ou --depot CHEMIN / la variable "
                            "TRIADE_DEPOT au lancement, ou téléchargez le "
                            "dossier /Cérémonie du Drive ENTIÈREMENT (le "
                            "sous-dossier v06/ fait du kit un mini-dépôt). "
                            "Copié seul sur une clef USB, il ne donne QUE le "
                            "profil hors-ligne — c'est voulu)")
            ).pack(anchor="w")
        ttk.Button(depot, text="Choisir le dossier du dépôt…",
                   command=self._sur_choisir_depot).pack(anchor="w",
                                                          pady=(4, 2))
        ttk.Button(page, text="← Retour à l'accueil",
                   command=lambda: self.montrer("accueil")).pack(anchor="w",
                                                                 pady=8)

    # ------------------------------------------------------------------
    # D117 — LE SCÉNARIO AVANT TOUT : choix, panneau, clonage
    # ------------------------------------------------------------------
    def _choisir_scenario(self, scenario):
        """Retient le scénario (consigné au journal et à la boîte noire —
        un choix de cérémonie n'est pas un secret) et rebâtit son panneau.
        Le fil de cérémonie suit AU PROCHAIN RAFRAÎCHISSEMENT (montrer le
        profil dépôt, ré-évaluer, fin d'action) : la preuve reste la
        vérité, l'affichage la suit."""
        if scenario not in SCENARIOS:
            return
        if self.scenario != scenario:
            self.scenario = scenario
            ENREGISTREUR.ligne(f"scénario choisi : {scenario}", "scenario")
            self.journal.ajoute(
                f"[ceremonie] scénario de cérémonie : {scenario} (D117 — il "
                "détermine les étapes affichées par le fil)", "info")
        self._montrer_panels_scenario()
        if getattr(self, "label_fil_courant", None) is not None:
            self._rafraichir_fil()

    def _montrer_panels_scenario(self):
        """Le panneau du scénario courant : dossier local → l'attache
        D112 ; repo git → le CLONAGE (URL + parent + nom) et l'attache
        d'un clone existant ; aucun → l'invitation à choisir AVANT TOUT."""
        panneau = getattr(self, "cadre_scen_panels", None)
        if panneau is not None:
            panneau.destroy()
        panneau = ttk.Frame(self.cadre_scen_section)
        panneau.pack(fill="x", pady=(4, 0))
        self.cadre_scen_panels = panneau
        if self.scenario == SCENARIO_GIT:
            self.label_scenario.configure(
                text="Scénario retenu : REPO GIT — fil de SIX étapes "
                     "(« Cloner le dépôt » en tête, prouvé par git rev-parse "
                     "+ origin). Le jeton éventuel de l'URL est MASQUÉ dans "
                     "le journal et la boîte noire.")
            self._note(panneau, "Le bouton ci-dessous exécute git clone "
                                "(réseau) vers le dossier parent + nom choisis "
                                "— la destination doit être LIBRE (un dossier "
                                "non vide est un refus NOMMÉ, rien n'y est "
                                "touché) ; après un clone prouvé, le dépôt est "
                                "ATTACHÉ et le profil dépôt s'ouvre. Un dépôt "
                                "privé peut demander votre authentification "
                                "GitHub.")
            cadre_u = ttk.Frame(panneau)
            cadre_u.pack(fill="x", pady=2)
            ttk.Label(cadre_u, text="URL du dépôt git :", width=26,
                      anchor="w").pack(side="left")
            self.var_clone_url = tk.StringVar()
            ttk.Entry(cadre_u, textvariable=self.var_clone_url).pack(
                side="left", fill="x", expand=True, padx=(0, 6))
            cadre_p = ttk.Frame(panneau)
            cadre_p.pack(fill="x", pady=2)
            ttk.Label(cadre_p, text="Dossier parent du clone :", width=26,
                      anchor="w").pack(side="left")
            self.var_clone_parent = tk.StringVar(
                value=os.path.expanduser("~"))
            ttk.Entry(cadre_p, textvariable=self.var_clone_parent).pack(
                side="left", fill="x", expand=True, padx=(0, 6))

            def choisir_parent():
                chemin = filedialog.askdirectory(
                    title="Dossier PARENT qui recevra le clone",
                    initialdir=self.var_clone_parent.get()
                    if os.path.isdir(self.var_clone_parent.get()) else
                    os.path.expanduser("~"))
                if chemin:
                    self.var_clone_parent.set(chemin)

            ttk.Button(cadre_p, text="Parcourir…", width=11,
                       command=choisir_parent).pack(side="left")
            cadre_n = ttk.Frame(panneau)
            cadre_n.pack(fill="x", pady=2)
            ttk.Label(cadre_n, text="Nom du dossier local :", width=26,
                      anchor="w").pack(side="left")
            self.var_clone_nom = tk.StringVar()
            ttk.Entry(cadre_n, textvariable=self.var_clone_nom).pack(
                side="left", fill="x", expand=True, padx=(0, 6))
            self._nom_auto_clone = ""
            self.var_clone_url.trace_add(
                "write", lambda *_: self._maj_nom_auto_clone())
            barre_clone = ttk.Frame(panneau)
            barre_clone.pack(fill="x", pady=(4, 0))
            ttk.Button(barre_clone, text="Cloner en local…",
                       command=self._sur_clone).pack(side="left")
            ttk.Button(barre_clone, text="Attacher un clone EXISTANT…",
                       command=lambda: self._sur_choisir_depot(
                           exige_clone=True)).pack(side="left", padx=6)
        elif self.scenario == SCENARIO_DOSSIER:
            self.label_scenario.configure(
                text="Scénario retenu : DOSSIER LOCAL — fil de CINQ étapes "
                     "(le dépôt vit déjà sur cette machine, on l'attache).")
            ttk.Button(panneau, text="Choisir le dossier du dépôt…",
                       command=self._sur_choisir_depot).pack(anchor="w",
                                                            pady=2)
        else:
            self.label_scenario.configure(
                text="Aucun scénario choisi — AVANT TOUT, choisissez ci-dessus "
                     "(le fil affichera cinq étapes en dossier local, six en "
                     "repo git avec « Cloner le dépôt » en tête).")

    def _maj_nom_auto_clone(self, *_):
        """Pré-remplit le nom du clone depuis l'URL (triade.git → triade) —
        SANS écraser un nom retapé à la main : la main garde le dernier "
        mot tant qu'elle a touché le champ."""
        url = self.var_clone_url.get().strip()
        nom = url.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        if nom.endswith(".git"):
            nom = nom[:-4]
        nom_auto = nom if nom else ""
        if not self.var_clone_nom.get().strip() \
                or self.var_clone_nom.get().strip() == self._nom_auto_clone:
            self.var_clone_nom.set(nom_auto)
        self._nom_auto_clone = nom_auto

    def _sur_clone(self):
        """« Cloner en local… » : validations LOCALES nommées AVANT tout
        lancement (URL, parent, nom, destination libre), confirmation
        explicite (l'URL y est MASQUÉE — un jeton ne paraît pas à l'écran
        plus qu'au journal), puis l'action asynchrone cloner_et_attacher
        (le fil ouvrier clone et attache ; le fil tkinter rebâtit les
        pages au verdict — cf. _sur_fin_action)."""
        if self.executeur.occupe:
            self._dialogue("showinfo", "Cérémonie en cours",
                "Attendez le verdict de l'action en cours avant de cloner "
                "(les chemins se suivent à l'attachement).")
            return
        url = self.var_clone_url.get().strip()
        parent = self.var_clone_parent.get().strip()
        nom = self.var_clone_nom.get().strip()
        if not url:
            self._dialogue("showwarning", "Clone — URL vide",
                "Donnez l'URL du dépôt git à cloner (ex. "
                "https://github.com/alexisfrlopez-debug/triade.git).")
            return
        if not parent or not os.path.isdir(parent):
            self._dialogue("showwarning", "Clone — dossier parent",
                "Choisissez le dossier PARENT EXISTANT qui recevra le clone "
                "(bouton Parcourir…).")
            return
        if not nom:
            self._dialogue("showwarning", "Clone — nom du dossier",
                "Donnez le nom du dossier local du clone (pré-rempli depuis "
                "l'URL).")
            return
        destination = os.path.join(parent, nom)
        if os.path.exists(destination) and os.listdir(destination):
            self._dialogue("showerror", "Clone — destination NON VIDE",
                f"{destination} contient déjà des fichiers — git clone veut "
                "un chemin LIBRE. Refus nommé (fail-closed) : rien n'y est "
                "touché.")
            return
        if not self._dialogue(
                "askyesno", "Cloner le dépôt (D117)",
                f"git clone {masquer_jeton(url)}\n→ {destination}\n\n"
                "Le réseau est utilisé ; l'authentification d'un dépôt privé "
                "peut ouvrir votre navigateur. Le jeton éventuel de l'URL est "
                "MASQUÉ dans le journal et la boîte noire. Continuer ?"):
            return
        self.action("Git — cloner le dépôt", cloner_et_attacher, url,
                    destination)

    def _sur_choisir_depot(self, exige_clone=False):
        """D112/D117 — le dossier du dépôt se choisit DANS la fenêtre. La
        garde D111 est inchangée : v06/coffre_cf2.py doit y vivre (échec
        NOMMÉ, aucun attachement partiel). EXIGE_CLONE (scénario repo git,
        « Attacher un clone EXISTANT… ») ajoute la preuve git : le dossier
        doit ÊTRE la racine d'un clone AVEC origin (refus nommé sinon —
        le fil de ce scénario l'exigerait de toute façon). Le
        re-attachement REBÂTIT les pages : config, coffre CF1 et
        disponibilité suivent le nouveau dépôt."""
        if self.executeur.occupe:
            self._dialogue("showinfo", 
                "Cérémonie en cours",
                "Attendez le verdict de l'action en cours avant de changer "
                "de dépôt (les CLI lancés lisent le dépôt à leur départ).")
            return
        initial = RACINE_DEPOT if os.path.isdir(RACINE_DEPOT) else \
            os.path.expanduser("~")
        chemin = filedialog.askdirectory(
            title="Dossier RACINE du dépôt triade (celui qui contient v06/)",
            initialdir=initial)
        if not chemin:
            return                      # annulé : rien ne bouge
        candidat = os.path.abspath(chemin)
        if not os.path.isfile(os.path.join(candidat, "v06", "coffre_cf2.py")):
            self._dialogue("showerror", 
                "Pas un dépôt triade complet",
                f"v06/coffre_cf2.py introuvable dans :\n  {candidat}\n\n"
                "Le dossier doit être la RACINE d'un clone du dépôt triade "
                "(celui qui contient v06/). Refus nommé, attachement "
                "inchangé (fail-closed) : le profil dépôt reste ce qu'il "
                "était.")
            return
        if exige_clone:
            faite, detail = preuve_clone(candidat)
            if not faite:
                self._dialogue("showerror",
                    "Pas un CLONE (scénario repo git)",
                    f"{detail}\n\nLe scénario REPO GIT exige la racine d'un "
                    "dépôt git AVEC origin (le fil de ce scénario le prouve "
                    "à chaque étape). Refus nommé, attachement inchangé.")
                return
        definir_racine_depot(candidat, "dossier choisi (GUI)")
        self.journal.ajoute(
            f"[ceremonie] dépôt attaché : {RACINE_DEPOT} — dossier choisi "
            "dans la fenêtre (D112), garde v06/coffre_cf2.py VERTE", "titre")
        self._rebâtir_pages()

    def _rebâtir_pages(self, cible="accueil"):
        """Détruit et reconstruit les trois pages : tout ce qui capture le
        dépôt À LA CONSTRUCTION (config CF2, coffre CF1, disponibilité,
        textes de l'accueil, panneau du scénario D117) suit le
        re-attachement. Le journal, l'exécuteur et la barre de verdict
        vivant HORS des pages, ils survivent — l'historique de cérémonie
        n'est jamais effacé par un changement de dépôt. D117 : CIBLE
        permet d'ouvrir DIRECTEMENT le profil dépôt après un clone (la
        cérémonie commence) ; le marqueur _racine_pages dit au
        _sur_fin_action quand un attachement a eu lieu HORS des pages."""
        for page in self.pages.values():
            page.destroy()
        self.pages = {}
        self.depot_pret = depot_disponible()
        self._batir_accueil()
        self._batir_hors_ligne()
        self._batir_depot()
        self._racine_pages = RACINE_DEPOT
        self.montrer(cible if (cible == "depot" and self.depot_pret)
                     else "accueil")

    # ------------------------------------------------------------------
    # PAGE HORS-LIGNE — clé I : générer / signer / vérifier
    # ------------------------------------------------------------------
    def _batir_hors_ligne(self):
        page = ttk.Frame(self.corps)
        self.pages["hors-ligne"] = page
        cahier = ttk.Notebook(page)
        cahier.pack(fill="both", expand=True, pady=4)

        # --- onglet générer ------------------------------------------------
        generer = ttk.Frame(cahier, padding=8)
        cahier.add(generer, text=" 1 · Générer la clé (première fois) ")
        self._note(generer, "La clé I signera TOUTE évolution future de "
                            "l'intention. Elle naît ici, hors ligne, et ne "
                            "doit jamais quitter cette machine : le fichier "
                            "est la remise, le papier est la garde.")
        self.var_hl_privee = self._ligne_fichier(
            generer, "Clé privée (à écrire) :", mode="save",
            defaut="cle-I-privee.txt")
        self.var_hl_publique = self._ligne_fichier(
            generer, "Clé publique (à écrire) :", mode="save",
            defaut="cle-publique-I.txt")
        ttk.Label(generer, foreground=COULEUR_ROUGE, wraplength=880,
                  justify="left",
                  text=("GARDE — après génération : imprimez la ligne de 64 "
                        "caractères du fichier privé (deux copies, deux "
                        "lieux). Graine perdue = plus aucune évolution de "
                        "l'intention ; graine volée = souveraineté morte. La "
                        "graine ne s'affiche jamais à l'écran.")
                  ).pack(anchor="w", pady=6)
        ttk.Button(generer, text="Générer la clé I",
                   command=self._sur_hl_generer).pack(anchor="w", pady=4)

        # --- onglet signer -------------------------------------------------
        signer = ttk.Frame(cahier, padding=8)
        cahier.add(signer, text=" 2 · Signer une remise ")
        self._note(signer, "Recevez a-signer.txt depuis le dépôt (profil "
                           "dépôt, bouton Préparer), puis signez-le ici. "
                           "Chaque signature est auto-vérifiée avant "
                           "écriture : une cérémonie douteuse n'écrit rien.")
        self.var_hl_a_signer = self._ligne_fichier(
            signer, "Remise à signer (a-signer.txt) :", mode="open")

        # --- source de la clé privée : FICHIER ou SAISIE MANUELLE (D112) ---
        source = self._section(
            signer, "Clé privée — fichier OU saisie manuelle (D112)")
        source.pack(fill="x", pady=2)
        self.var_hl_cle_manuelle = tk.BooleanVar(value=False)
        modes = ttk.Frame(source)
        modes.pack(fill="x", pady=(0, 2))
        ttk.Radiobutton(modes, text="Depuis un FICHIER (cle-I-privee.txt)",
                        variable=self.var_hl_cle_manuelle, value=False,
                        command=self._basculer_source_cle).pack(side="left")
        ttk.Radiobutton(modes, text="SAISIE MANUELLE (récupération papier)",
                        variable=self.var_hl_cle_manuelle, value=True,
                        command=self._basculer_source_cle).pack(
                            side="left", padx=(12, 0))
        cadre_f = ttk.Frame(source)
        cadre_f.pack(fill="x", pady=2)
        ttk.Label(cadre_f, text="Clé privée (fichier) :", width=26,
                  anchor="w").pack(side="left")
        self.var_hl_cle = tk.StringVar(value="cle-I-privee.txt")
        self.entry_hl_cle = ttk.Entry(cadre_f, textvariable=self.var_hl_cle)
        self.entry_hl_cle.pack(side="left", fill="x", expand=True,
                               padx=(0, 6))

        def choisir_cle():
            chemin = filedialog.askopenfilename(
                filetypes=[("Texte", "*.txt"), ("Tout", "*.*")])
            if chemin:
                self.var_hl_cle.set(chemin)

        self.bouton_hl_cle = ttk.Button(cadre_f, text="Parcourir…", width=11,
                                         command=choisir_cle)
        self.bouton_hl_cle.pack(side="left")
        cadre_m = ttk.Frame(source)
        cadre_m.pack(fill="x", pady=2)
        ttk.Label(cadre_m, text="Graine (64 hex, masquée) :", width=26,
                  anchor="w").pack(side="left")
        self.var_hl_cle_saisie = tk.StringVar(value="")
        self.entry_hl_cle_saisie = ttk.Entry(
            cadre_m, textvariable=self.var_hl_cle_saisie, show="\u2022",
            font=POLICE_FIXE)
        self.entry_hl_cle_saisie.pack(side="left", fill="x", expand=True,
                                      padx=(0, 6))
        self.var_hl_voir_saisie = tk.BooleanVar(value=False)
        ttk.Checkbutton(cadre_m, text="afficher",
                        variable=self.var_hl_voir_saisie,
                        command=self._basculer_voir_saisie).pack(side="left")
        self.label_saisie_verdict = ttk.Label(
            source, style="Sous.TLabel", wraplength=880, justify="left")
        self.label_saisie_verdict.pack(anchor="w", pady=(2, 0))
        self.var_hl_cle_saisie.trace_add("write", self._maj_saisie_cle)
        self._basculer_source_cle()

        self.var_hl_signatures = self._ligne_fichier(
            signer, "Signatures produites (à écrire) :", mode="save",
            defaut="signatures-I.txt")
        ttk.Button(signer, text="Signer la remise",
                   command=self._sur_hl_signer).pack(anchor="w", pady=4)

        # --- onglet vérifier -----------------------------------------------
        verifier = ttk.Frame(cahier, padding=8)
        cahier.add(verifier, text=" 3 · Vérifier une remise (contrôle) ")
        self._note(verifier, "Re-vérification autonome d'une remise : les "
                             "signatures correspondent-elles à a-signer.txt "
                             "ET à la clé publique ? (aucune écriture)")
        self.var_hl_v_a_signer = self._ligne_fichier(
            verifier, "Remise de référence (a-signer.txt) :", mode="open")
        self.var_hl_v_signatures = self._ligne_fichier(
            verifier, "Signatures (signatures-I.txt) :", mode="open")
        self.var_hl_v_publique = self._ligne_fichier(
            verifier, "Clé publique (cle-publique-I.txt) :", mode="open",
            defaut="cle-publique-I.txt")
        ttk.Button(verifier, text="Vérifier la remise",
                   command=self._sur_hl_verifier).pack(anchor="w", pady=4)

        ttk.Button(page, text="← Retour à l'accueil",
                   command=lambda: self.montrer("accueil")).pack(anchor="w",
                                                                 pady=6)

    def _sur_hl_generer(self):
        privee, publique = self.var_hl_privee.get().strip(), \
            self.var_hl_publique.get().strip()
        if not privee or not publique:
            self._dialogue("showwarning", "Champs manquants",
                                   "Choisissez où écrire la clé privée ET la "
                                   "clé publique.")
            return
        if os.path.exists(privee) and not self._dialogue("askyesno", 
                "Écraser ?", f"{privee} existe déjà — une clé DÉJÀ générée "
                f"à cet endroit serait perdue si vous écrasez. Continuer ?"):
            return
        self.action("Hors-ligne — générer la clé I", hl_generer, privee,
                    publique)

    def _sur_hl_signer(self):
        a_signer, sortie = (self.var_hl_a_signer.get().strip(),
                            self.var_hl_signatures.get().strip())
        if not (a_signer and sortie):
            self._dialogue("showwarning", "Champs manquants",
                                   "La remise à signer et le fichier de "
                                   "signatures sont requis.")
            return
        if self.var_hl_cle_manuelle.get():
            saisie = self.var_hl_cle_saisie.get()
            if not saisie.strip():
                self._dialogue("showwarning", 
                    "Saisie manuelle vide",
                    "La graine saisie est vide — entrez les 64 hexadécimaux "
                    "(ligne imprimée de cle-I-privee.txt) ou basculez sur le "
                    "FICHIER.")
                return
            try:
                _graine_depuis_saisie(saisie)   # fail-closed AVANT l'acte
            except ErreurCeremonie as exc:
                self._dialogue("showwarning", "Saisie refusée (fail-closed)",
                                       str(exc))
                return
            self.action("Hors-ligne — signer (clé saisie à la main)",
                        hl_signer, a_signer, None, sortie, saisie)
            # la graine ne s'attarde pas dans le champ ni dans un état
            # « afficher » oublié : effacée dès l'acte lancé (D112)
            self.var_hl_cle_saisie.set("")
            self.var_hl_voir_saisie.set(False)
            self._basculer_voir_saisie()
        else:
            cle = self.var_hl_cle.get().strip()
            if not cle:
                self._dialogue("showwarning", 
                    "Champ manquant",
                    "Choisissez le fichier de clé privée — ou basculez sur "
                    "la saisie manuelle (D112).")
                return
            self.action("Hors-ligne — signer la remise", hl_signer, a_signer,
                        cle, sortie)

    def _basculer_source_cle(self):
        """Active la ligne choisie (fichier OU saisie) et gris l'autre —
        une seule source de vérité visible à la fois (D112)."""
        manuelle = self.var_hl_cle_manuelle.get()
        for widget in (self.entry_hl_cle, self.bouton_hl_cle):
            widget.configure(state="disabled" if manuelle else "normal")
        self.entry_hl_cle_saisie.configure(
            state="normal" if manuelle else "disabled")

    def _basculer_voir_saisie(self):
        self.entry_hl_cle_saisie.configure(
            show="" if self.var_hl_voir_saisie.get() else "\u2022")

    def _maj_saisie_cle(self, *_):
        """Verdict vivant sous la saisie manuelle — longueur et nature des
        caractères, JAMAIS le contenu (la graine ne se paraphrase pas)."""
        cand = self.var_hl_cle_saisie.get().strip()
        if not cand:
            self.label_saisie_verdict.configure(text="",
                                                foreground="#57606a")
            return
        faux = next((i for i, c in enumerate(cand)
                     if c not in "0123456789abcdefABCDEF"), None)
        if faux is not None:
            self.label_saisie_verdict.configure(
                text=f"caractère non hexadécimal en position {faux + 1}",
                foreground=COULEUR_ROUGE)
        elif len(cand) == 64:
            self.label_saisie_verdict.configure(
                text="64 hexadécimaux — graine COMPLÈTE (masquée)",
                foreground=COULEUR_VERTE)
        elif len(cand) > 64:
            self.label_saisie_verdict.configure(
                text=f"{len(cand)} caractères — TROP LONG (64 attendus)",
                foreground=COULEUR_ROUGE)
        else:
            self.label_saisie_verdict.configure(
                text=f"{len(cand)}/64 hexadécimaux",
                foreground=COULEUR_ATTENTE)

    def _sur_hl_verifier(self):
        a_signer, signatures, publique = (
            self.var_hl_v_a_signer.get().strip(),
            self.var_hl_v_signatures.get().strip(),
            self.var_hl_v_publique.get().strip())
        if not (a_signer and signatures and publique):
            self._dialogue("showwarning", "Champs manquants",
                                   "Les trois chemins sont requis.")
            return
        self.action("Hors-ligne — vérifier la remise", hl_verifier, a_signer,
                    signatures, publique)

    # ------------------------------------------------------------------
    # PAGE DÉPÔT — sceau I + coffre CF2 + liste blanche
    # ------------------------------------------------------------------
    def _batir_depot(self):
        import functools
        self._functools = functools
        page = ttk.Frame(self.corps)
        self.pages["depot"] = page
        if not self.depot_pret:
            self._note(page, f"Aucun dépôt triade complet n'est attaché "
                             f"(v06/coffre_cf2.py introuvable dans "
                             f"{RACINE_DEPOT}, source : {SOURCE_DEPOT}) : "
                             "le profil dépôt est désactivé. Choisissez le "
                             "dossier du dépôt par le bouton ci-dessous "
                             "(D112), ou relancez avec --depot CHEMIN (ou "
                             "la variable TRIADE_DEPOT) désignant la racine "
                             "d'un clone du dépôt. Pour la cérémonie "
                             "hors-ligne, utilisez le profil hors-ligne.")
            ttk.Button(page, text="Choisir le dossier du dépôt…",
                       command=self._sur_choisir_depot).pack(anchor="w",
                                                            pady=4)
            ttk.Button(page, text="← Retour à l'accueil",
                       command=lambda: self.montrer(
                           "accueil")).pack(anchor="w", pady=8)
            return
        # champ configuration CF2 (partagé par les actions du coffre)
        zone = self._section(page, "Configuration du coffre CF2")
        zone.pack(fill="x", pady=(4, 6))
        self.var_config = tk.StringVar(
            value=os.path.join(RACINE_DEPOT, ".keys", "config_cf2.json"))
        cadre = ttk.Frame(zone)
        cadre.pack(fill="x", pady=2)
        ttk.Label(cadre, text="config_cf2.json :", width=26,
                  anchor="w").pack(side="left")
        ttk.Entry(cadre, textvariable=self.var_config).pack(
            side="left", fill="x", expand=True, padx=(0, 6))

        def choisir_config():
            chemin = filedialog.askopenfilename(
                filetypes=[("Config CF2", "config_cf2.json"),
                           ("JSON", "*.json"), ("Tout", "*.*")])
            if chemin:
                self.var_config.set(chemin)
                self._maj_etat_config()

        ttk.Button(cadre, text="Parcourir…", width=11,
                   command=choisir_config).pack(side="left")
        self.label_etat_config = ttk.Label(zone, style="Sous.TLabel")
        self.label_etat_config.pack(anchor="w")
        self._maj_etat_config()

        cahier = ttk.Notebook(page)
        cahier.pack(fill="both", expand=True, pady=4)

        # --- onglet Sceau de l'Intention -----------------------------------
        sceau = ttk.Frame(cahier, padding=8)
        cahier.add(sceau, text=" Sceau de l'Intention (D87) ")
        self._note(sceau, "L'intention du dépôt est signée par la clé "
                          "hors-ligne. Préparer écrit v06/sceau-I/"
                          "a-signer.txt (~1 Ko, dix lignes « arbre balise "
                          "empreinte ») : transportez-le vers la machine "
                          "hors-ligne, faites-le signer (profil hors-ligne), "
                          "puis déposez la remise ici.")
        # --- fil de cérémonie (D116) : l'étape satisfaite s'efface, la
        # suivante s'affiche — auto-détection par PREUVES, lecture seule
        fil = self._section(sceau, "Fil de cérémonie — Sceau I (D116)")
        fil.pack(fill="x", pady=(0, 4))
        self.cadre_fil = fil      # D117 : le titre porte le scénario courant
        self.fil_manuel = set()
        self._fil_etat = None
        self.label_fil_resume = ttk.Label(
            fil, style="Sous.TLabel", wraplength=880, justify="left",
            foreground="#8b949e")
        self.label_fil_resume.pack(anchor="w")
        self.label_fil_courant = ttk.Label(
            fil, style="Sous.TLabel", wraplength=880, justify="left",
            font=("Segoe UI", 10, "bold"), foreground=COULEUR_ENCRE)
        self.label_fil_courant.pack(anchor="w", pady=(2, 0))
        self.label_fil_detail = ttk.Label(
            fil, style="Sous.TLabel", wraplength=880, justify="left",
            foreground="#57606a")
        self.label_fil_detail.pack(anchor="w")
        self.label_fil_suite = ttk.Label(
            fil, style="Sous.TLabel", wraplength=880, justify="left",
            foreground="#8b949e")
        self.label_fil_suite.pack(anchor="w")
        barre_fil = ttk.Frame(fil)
        barre_fil.pack(fill="x", pady=(4, 0))
        ttk.Button(barre_fil, text="Ré-évaluer l'étape",
                   command=self._sur_fil_reevaluer).pack(side="left")
        ttk.Button(barre_fil, text="Marquer faite (à la main)",
                   command=self._sur_fil_manuel).pack(side="left", padx=6)

        barre = ttk.Frame(sceau)
        barre.pack(fill="x", pady=2)
        ttk.Button(barre, text="Préparer a-signer.txt",
                   command=self._sur_sceau_preparer).pack(side="left")
        ttk.Button(barre, text="Vérifier les dix arbres",
                   command=self._sur_sceau_verifier).pack(side="left", padx=6)
        ttk.Button(barre, text="État de la clé",
                   command=lambda: self.action(
                       "Sceau I — état", self._cli, "sceau_I.py",
                       ["etat"])).pack(side="left")
        self.var_sceau_signatures = self._ligne_fichier(
            sceau, "Remise à déposer (signatures-I.txt) :", mode="open")
        self.var_sceau_cle = self._ligne_fichier(
            sceau, "Clé publique (PREMIÈRE remise seulement) :", mode="open")
        ttk.Button(sceau, text="Déposer la remise (acte souverain)",
                   command=self._sur_sceau_deposer).pack(anchor="w", pady=4)

        # --- git (D116) : enregistrer la cérémonie sur le dépôt distant --
        gitcadre = self._section(
            sceau, "Git — enregistrer la cérémonie (D116)")
        gitcadre.pack(fill="x", pady=(6, 0))
        self._note(gitcadre,
                   "add v06/sceau-I (SEUL — jamais « add -A » : la clé "
                   "privée vit hors du dépôt, les journaux sont ignorés) "
                   "→ commit → pull --rebase → push. Chaque échec est "
                   "NOMMÉ dans le journal ; l'authentification GitHub peut "
                   "ouvrir votre navigateur.")
        ttk.Button(gitcadre, text="Pousser v06/sceau-I sur git…",
                   command=self._sur_git_pousser).pack(anchor="w", pady=4)

        # --- onglet Coffre CF2 ---------------------------------------------
        cf2 = ttk.Frame(cahier, padding=8)
        cahier.add(cf2, text=" Coffre CF2 — homme mort (D86) ")

        coffre_cf1 = self._section(
            cf2, "Coffre CF1 — conteneur et phrase (D112)")
        coffre_cf1.pack(fill="x", pady=2)
        self._note(coffre_cf1,
                   "Le conteneur CF1 que la cérémonie LIT (verifier, "
                   "changer-phrase, migrer) — le champ est la VÉRITÉ : "
                   "aucun repli silencieux vers .keys/. Choisissez-le "
                   "(Parcourir…) s'il vit ailleurs : copie du Drive, clef "
                   "USB, autre clone. La phrase de contrôle CI-DESSOUS "
                   "sert à VÉRIFIER le coffre PUIS à la migration : une "
                   "seule frappe, les deux actes.")
        cadre_o = ttk.Frame(coffre_cf1)
        cadre_o.pack(fill="x", pady=2)
        ttk.Label(cadre_o, text="coffre_fort.bin :", width=26,
                  anchor="w").pack(side="left")
        self.var_coffre_cf1 = tk.StringVar(
            value=os.path.join(RACINE_DEPOT, ".keys", "coffre_fort.bin"))
        ttk.Entry(cadre_o, textvariable=self.var_coffre_cf1).pack(
            side="left", fill="x", expand=True, padx=(0, 6))

        def choisir_coffre():
            chemin = filedialog.askopenfilename(
                title="Conteneur CF1 (coffre_fort.bin)",
                filetypes=[("Coffre CF1", "coffre_fort.bin"),
                           ("Binaire", "*.bin"), ("Tout", "*.*")])
            if chemin:
                self.var_coffre_cf1.set(chemin)

        ttk.Button(cadre_o, text="Parcourir…", width=11,
                   command=choisir_coffre).pack(side="left")
        self.label_etat_coffre = ttk.Label(coffre_cf1, style="Sous.TLabel",
                                           wraplength=880, justify="left")
        self.label_etat_coffre.pack(anchor="w")
        self.var_coffre_cf1.trace_add("write", self._maj_etat_coffre)
        self._maj_etat_coffre()
        cadre_p = ttk.Frame(coffre_cf1)
        cadre_p.pack(fill="x", pady=2)
        ttk.Label(cadre_p, text="Phrase de contrôle CF1 :", width=26,
                  anchor="w").pack(side="left")
        self.var_phrase = tk.StringVar(value="")
        self.entry_phrase = ttk.Entry(cadre_p, textvariable=self.var_phrase,
                                      show="\u2022")
        self.entry_phrase.pack(side="left", fill="x", expand=True,
                               padx=(0, 6))
        self.var_voir_phrase = tk.BooleanVar(value=False)
        ttk.Checkbutton(cadre_p, text="afficher",
                        variable=self.var_voir_phrase,
                        command=self._basculer_phrase).pack(side="left")
        barre_cf1 = ttk.Frame(coffre_cf1)
        barre_cf1.pack(fill="x", pady=2)
        ttk.Button(barre_cf1, text="Statut CF1",
                   command=self._sur_cf1_statut).pack(side="left")
        ttk.Button(barre_cf1, text="Vérifier CF1 (phrase)",
                   command=self._sur_cf1_verifier).pack(side="left", padx=6)

        inspection = self._section(cf2, "Inspection CF2 (aucune clé touchée)")
        inspection.pack(fill="x", pady=2)
        barre = ttk.Frame(inspection)
        barre.pack(fill="x", pady=2)
        ttk.Button(barre, text="Statut",
                   command=self._sur_cf2_statut).pack(side="left")
        ttk.Button(barre, text="Vérifier",
                   command=self._sur_cf2_verifier).pack(side="left", padx=6)
        ttk.Button(barre, text="État fragments",
                   command=self._sur_cf2_etat_fragments).pack(side="left")
        ttk.Button(barre, text="Autotest (labo)",
                   command=self._sur_cf2_autotest).pack(side="left", padx=6)

        phrase_vous = self._section(
            cf2, "Phrase de contrôle CF1 — mettez la VÔTRE (D110)")
        phrase_vous.pack(fill="x", pady=2)
        self._note(phrase_vous,
                   "La phrase actuelle est celle de D81 — remise : "
                   "PHRASE-CONTROLE-COFFRE.txt, dépôt ET racine du Drive "
                   "« Triade » (si vous la perdez, rouvrez ce fichier : "
                   "c'est LA copie de secours). Remplacez-la par la vôtre : "
                   "alphanumérique (A-Z a-z 0-9), 8 caractères minimum, "
                   "AUCUN plafond de longueur. L'ancienne devient INOPÉRANTE ; "
                   "après le changement, remplacez la remise (discipline "
                   "D81 — le journal vous le rappellera).")
        cadre_a = ttk.Frame(phrase_vous)
        cadre_a.pack(fill="x", pady=2)
        ttk.Label(cadre_a, text="Ancienne phrase :", width=26,
                  anchor="w").pack(side="left")
        self.var_cf1_ancienne = tk.StringVar(value="")
        self.entry_cf1_ancienne = ttk.Entry(
            cadre_a, textvariable=self.var_cf1_ancienne, show="\u2022")
        self.entry_cf1_ancienne.pack(side="left", fill="x", expand=True,
                                     padx=(0, 6))
        cadre_n = ttk.Frame(phrase_vous)
        cadre_n.pack(fill="x", pady=2)
        ttk.Label(cadre_n, text="Nouvelle (la vôtre) :", width=26,
                  anchor="w").pack(side="left")
        self.var_cf1_nouvelle = tk.StringVar(value="")
        self.entry_cf1_nouvelle = ttk.Entry(
            cadre_n, textvariable=self.var_cf1_nouvelle, show="\u2022")
        self.entry_cf1_nouvelle.pack(side="left", fill="x", expand=True,
                                     padx=(0, 6))
        cadre_c = ttk.Frame(phrase_vous)
        cadre_c.pack(fill="x", pady=2)
        ttk.Label(cadre_c, text="Confirmation :", width=26,
                  anchor="w").pack(side="left")
        self.var_cf1_confirmation = tk.StringVar(value="")
        self.entry_cf1_confirmation = ttk.Entry(
            cadre_c, textvariable=self.var_cf1_confirmation, show="\u2022")
        self.entry_cf1_confirmation.pack(side="left", fill="x", expand=True,
                                          padx=(0, 6))
        self.var_cf1_voir = tk.BooleanVar(value=False)
        ttk.Checkbutton(phrase_vous, text="afficher (vérifiez votre frappe)",
                        variable=self.var_cf1_voir,
                        command=self._basculer_cf1).pack(anchor="w")
        self.label_cf1_verdict = ttk.Label(phrase_vous, style="Sous.TLabel",
                                           wraplength=880, justify="left")
        self.label_cf1_verdict.pack(anchor="w", pady=(2, 0))
        self.var_cf1_nouvelle.trace_add("write", self._maj_entropie_cf1)
        ttk.Button(phrase_vous, text="Changer la phrase (la vôtre)",
                   command=self._sur_cf1_changer_phrase).pack(
                       anchor="w", pady=4)

        migration = self._section(cf2, "Migration CF1 → CF2 (cérémonie réelle)")
        migration.pack(fill="x", pady=2)
        self._note(migration, "Part d'un coffre CF1 SAIN — vérifiez-le "
                              "d'abord (section « Coffre CF1 » ci-dessus : "
                              "bouton Vérifier, la même phrase). La "
                              "migration lit le conteneur choisi dans cette "
                              "section et le laisse INTACT ; le CF2 naît "
                              "coupé en 5 fragments (seuil 3) chez des "
                              "gardes distinctes.")
        ttk.Button(migration, text="Migrer vers CF2",
                   command=self._sur_cf2_migrer).pack(anchor="w", pady=4)

        fragments = self._section(cf2, "Fragments hors-ligne (le seuil est la loi)")
        fragments.pack(fill="x", pady=2)
        self._note(fragments, "Exportez la feuille des TROIS fragments, "
                              "imprimez-la (ou copiez-la sur USB, deux "
                              "lieux). Puis CONTRÔLEZ vos copies : l'assistant "
                              "relit vos trois fichiers et prouve qu'ils "
                              "reconstituent le seuil (AEAD vert) — sans "
                              "rien écrire.")
        self.var_feuille = self._ligne_fichier(
            fragments, "Feuille à écrire :", mode="save",
            defaut="fragments-cf2.txt")
        ttk.Button(fragments, text="Exporter la feuille des fragments",
                   command=self._sur_cf2_feuille).pack(anchor="w", pady=2)
        self.var_copie_1 = self._ligne_fichier(
            fragments, "Copie 1 relue (fragment-*.cf2f) :", mode="open",
            types=[("Fragment CF2", "*.cf2f"), ("Texte", "*.txt"),
                   ("Tout", "*.*")])
        self.var_copie_2 = self._ligne_fichier(
            fragments, "Copie 2 relue :", mode="open",
            types=[("Fragment CF2", "*.cf2f"), ("Texte", "*.txt"),
                   ("Tout", "*.*")])
        self.var_copie_3 = self._ligne_fichier(
            fragments, "Copie 3 relue :", mode="open",
            types=[("Fragment CF2", "*.cf2f"), ("Texte", "*.txt"),
                   ("Tout", "*.*")])
        ttk.Button(fragments, text="Contrôler les trois copies",
                   command=self._sur_cf2_controle).pack(anchor="w", pady=2)

        sentinelle = self._section(cf2, "Sentinelle (elle vit tant que la machine vit)")
        sentinelle.pack(fill="x", pady=2)
        barre = ttk.Frame(sentinelle)
        barre.pack(fill="x", pady=2)
        ttk.Button(barre, text="Démarrer (détachée)",
                   command=self._sur_sentinelle).pack(side="left")
        ttk.Button(barre, text="Santé",
                   command=self._sur_sentinelle_sante).pack(side="left", padx=6)

        releve = self._section(cf2, "Relever… ou détruire")
        releve.pack(fill="x", pady=2)
        barre = ttk.Frame(releve)
        barre.pack(fill="x", pady=2)
        ttk.Button(barre, text="Restaurer (3 copies)",
                   command=self._sur_cf2_restaurer).pack(side="left")
        ttk.Button(barre, text="BRÛLER (irréversible)",
                   command=self._sur_cf2_bruler).pack(side="left", padx=6)

        # --- onglet Liste blanche ------------------------------------------
        blanche = ttk.Frame(cahier, padding=8)
        cahier.add(blanche, text=" Liste blanche (D86) ")
        self._note(blanche, "Un processus NON blanchi qui lit la couche C "
                            "détériore le coffre : BRÛLAGE. La liste juge la "
                            "ligne de commande COMPLÈTE (jamais « tout "
                            "python3 ») — réfléchissez avant d'ajouter un "
                            "motif : une fausse alerte est une perte "
                            "auto-infligée.")
        cadre = ttk.Frame(blanche)
        cadre.pack(fill="both", expand=True, pady=2)
        self.liste_blanche = tk.Listbox(cadre, height=7,
                                        font=POLICE_FIXE)
        self.liste_blanche.pack(side="left", fill="both", expand=True)
        barre_d = ttk.Frame(cadre, width=34)
        barre_d.pack(side="left", fill="y", padx=(6, 0))
        self.var_motif = tk.StringVar()
        ttk.Entry(barre_d, textvariable=self.var_motif).pack(
            fill="x", pady=(0, 2))
        ttk.Button(barre_d, text="Ajouter", width=10,
                   command=self._sur_motif_ajouter).pack(fill="x", pady=2)
        ttk.Button(barre_d, text="Retirer la sélection", width=10,
                   command=self._sur_motif_retirer).pack(fill="x", pady=2)
        ttk.Button(barre_d, text="Recharger", width=10,
                   command=self._charger_liste_blanche).pack(fill="x", pady=2)
        ttk.Label(barre_d, text="tester contre :",
                  style="Sous.TLabel").pack(fill="x", pady=(8, 0))
        self.var_essai = tk.StringVar(
            value="/usr/bin/code.exe /home/dev/triade/m0/carte/x.txt")
        ttk.Entry(barre_d, textvariable=self.var_essai).pack(fill="x")
        ttk.Button(barre_d, text="Tester", width=10,
                   command=self._sur_motif_tester).pack(fill="x", pady=2)
        self.label_motif_verdict = ttk.Label(barre_d, style="Sous.TLabel",
                                              wraplength=230, justify="left")
        self.label_motif_verdict.pack(fill="x")
        ttk.Button(blanche, text="Enregistrer la liste (acte de déploiement)",
                   command=self._sur_liste_blanche_ecrire).pack(
                       anchor="w", pady=4)
        self._charger_liste_blanche()

        ttk.Button(page, text="← Retour à l'accueil",
                   command=lambda: self.montrer("accueil")).pack(anchor="w",
                                                                 pady=6)

    def _cfg_args(self):
        cfg = self.var_config.get().strip()
        return [cfg] if cfg else []

    def _sur_cf2_statut(self):
        if not self._pile_prete("Le statut du coffre"):
            return
        self.action("CF2 — statut", self._cli, "coffre_cf2.py",
                    ["statut"] + self._cfg())

    def _sur_cf2_verifier(self):
        if not self._pile_prete("La vérification du coffre"):
            return
        self.action("CF2 — verifier", self._cli, "coffre_cf2.py",
                    ["verifier"] + self._cfg())

    def _sur_cf2_etat_fragments(self):
        if not self._pile_prete("L'état des fragments"):
            return
        self.action("CF2 — état fragments", self._cli, "coffre_cf2.py",
                    ["etat-fragments"] + self._cfg())

    def _sur_cf2_autotest(self):
        if not self._pile_prete("L'autotest du coffre"):
            return
        self.action("CF2 — autotest", self._cli, "coffre_cf2.py", ["autotest"])

    def _sur_sentinelle_sante(self):
        if not self._pile_prete("La santé de la sentinelle"):
            return
        self.action("Sentinelle — santé", self._cli, "sentinelle_cf2.py",
                    ["sante", "--config"] + self._cfg_args())

    def _cfg(self):
        return ["--config"] + self._cfg_args() if self._cfg_args() else []

    def _basculer_phrase(self):
        self.entry_phrase.configure(
            show="" if self.var_voir_phrase.get() else "\u2022")

    def _basculer_cf1(self):
        affiche = "" if self.var_cf1_voir.get() else "\u2022"
        for entree in (self.entry_cf1_ancienne, self.entry_cf1_nouvelle,
                       self.entry_cf1_confirmation):
            entree.configure(show=affiche)

    def _maj_entropie_cf1(self, *_):
        """Verdict vivant sous la nouvelle phrase (validation D110) :"""
        phrase = self.var_cf1_nouvelle.get()
        if not phrase:
            self.label_cf1_verdict.configure(text="",
                                             foreground="#57606a")
            return
        ok, message = phrase_personnelle_valide(phrase)
        bits = entropie_bits(len(phrase))
        couleur = (COULEUR_VERTE if ok and bits >= 128 else
                   COULEUR_ATTENTE if ok else COULEUR_ROUGE)
        self.label_cf1_verdict.configure(text=message, foreground=couleur)

    def _coffre_cf1_exige(self, pour_quoi):
        """D112 — le chemin CF1 choisi, ou None (avec l'échec nommé affiché).
        Le champ est la VÉRITÉ : vide = refus, AUCUN repli silencieux vers
        .keys/ (contrairement au CLI qui, lui, garde son défaut)."""
        coffre = self.var_coffre_cf1.get().strip()
        if not coffre:
            self._dialogue("showwarning", 
                "Champ manquant",
                f"{pour_quoi} exige le chemin du coffre CF1 — remplissez le "
                "champ coffre_fort.bin (bouton Parcourir…).")
            return None
        return coffre

    def _sur_cf1_statut(self):
        """Statut CF1 : l'en-tête CLAIR du conteneur choisi (aucune phrase,
        aucune clé — la commande la plus sûre pour nommer un conteneur)."""
        if not self._pile_prete("Le statut du coffre CF1"):
            return
        coffre = self._coffre_cf1_exige("Le statut CF1")
        if coffre is None:
            return
        self.action("CF1 — statut",
                    self._functools.partial(
                        self._cli, "coffre_fort.py",
                        ["--chemin", coffre, "statut"], au_racine=True))

    def _sur_cf1_verifier(self):
        """Vérifier CF1 : déchiffre le conteneur choisi avec la phrase —
        LE préalable de la migration (un coffre non vérifié ne migre pas)."""
        if not self._pile_prete("La vérification du coffre CF1"):
            return
        coffre = self._coffre_cf1_exige("La vérification CF1")
        if coffre is None:
            return
        phrase = self.var_phrase.get()
        if not phrase.strip():
            self._dialogue("showwarning", 
                "Phrase vide",
                "La phrase de contrôle CF1 est requise (fail-closed) — "
                "remplissez le champ « Phrase de contrôle CF1 » de la "
                "section « Coffre CF1 ».")
            return
        self.action(
            "CF1 — verifier",
            self._functools.partial(
                self._cli, "coffre_fort.py",
                ["--chemin", coffre, "verifier"],
                phrase=phrase, au_racine=True))

    def _sur_cf1_changer_phrase(self):
        if not self._pile_prete("Le changement de phrase CF1"):
            return
        ancienne = self.var_cf1_ancienne.get()
        nouvelle = self.var_cf1_nouvelle.get().strip()
        confirmation = self.var_cf1_confirmation.get().strip()
        coffre = self._coffre_cf1_exige("Le changement de phrase")
        if coffre is None:
            return
        if not ancienne.strip():
            self._dialogue("showwarning", 
                "Champ manquant",
                "L'ANCIENNE phrase de contrôle est requise (fail-closed) —\n"
                "c'est elle qui prouve que le coffre est le vôtre.\n"
                "Perdue ? Elle vit dans PHRASE-CONTROLE-COFFRE.txt\n"
                "(dépôt triade ET racine du Drive « Triade »).")
            return
        ok, message = phrase_personnelle_valide(nouvelle)
        if not ok:
            self._dialogue("showwarning", "Phrase refusée (fail-closed)", message)
            return
        if nouvelle != confirmation:
            self._dialogue("showwarning", 
                "Divergence",
                "La nouvelle phrase et sa confirmation divergent —\n"
                "refus (fail-closed). Retapez la confirmation.")
            return
        if nouvelle == ancienne.strip():
            self._dialogue("showwarning", 
                "Refus",
                "La nouvelle phrase est IDENTIQUE à l'ancienne —\n"
                "il n'y a rien à changer.")
            return
        bits = entropie_bits(len(nouvelle))
        avertissement = (""
                         if bits >= 128 else
                         "\n\nATTENTION : ≈ " + f"{bits:.0f} bits seulement "
                         "(recommandé ≥ 22 caractères ≈ 128 bits) —\n"
                         "une phrase plus courte est plus faible : Argon2id "
                         "ne compensera pas un dictionnaire.")
        if not self._dialogue("askyesno", 
                "Changer la phrase de contrôle — acte souverain",
                "Le coffre sera OUVERT avec l'ancienne phrase puis "
                "RE-SCCELLÉ avec la vôtre (sel Argon2id neuf).\n\n"
                "L'ANCIENNE phrase deviendra INOPÉRANTE immédiatement.\n"
                "APRÈS : remplacez la remise PHRASE-CONTROLE-COFFRE.txt "
                "(votre phrase, ligne unique),\ncommit « AVANT TOUT » + "
                "push git + racine Drive — sinon vous la PERDREZ comme la "
                "précédente.\n\n"
                f"Votre phrase : {len(nouvelle)} caractères, "
                f"≈ {bits:.0f} bits d'entropie."
                + avertissement + "\n\nContinuer ?"):
            return
        self.action(
            "CF1 — changer la phrase (la vôtre)",
            self._functools.partial(
                self._cli, "coffre_fort.py",
                ["--chemin", coffre, "changer-phrase"],
                phrase=ancienne, nouvelle_phrase=nouvelle, au_racine=True))
        self.var_cf1_ancienne.set("")
        self.var_cf1_nouvelle.set("")
        self.var_cf1_confirmation.set("")
        self.journal.ajoute(
            "[ceremonie] DISCIPLINE D81 (rappel) : la remise est le FICHIER — "
            "remplacez la ligne unique de PHRASE-CONTROLE-COFFRE.txt par "
            "votre nouvelle phrase, puis commit « AVANT TOUT » et push "
            "(git ET racine du Drive « Triade »).", "titre")

    def _maj_etat_coffre(self, *_):
        if not getattr(self, "label_etat_coffre", None):
            return
        coffre = self.var_coffre_cf1.get().strip()
        if not coffre:
            self.label_etat_coffre.configure(
                text="coffre CF1 : (vide — statut/vérifier/migrer seront "
                     "refusés, aucun repli silencieux)",
                foreground="#57606a")
            return
        if os.path.isfile(coffre):
            taille = os.path.getsize(coffre)
            self.label_etat_coffre.configure(
                text=f"coffre CF1 : TROUVÉ ({coffre} · {taille} o)",
                foreground=COULEUR_VERTE)
        else:
            self.label_etat_coffre.configure(
                text=f"coffre CF1 : ABSENT ({coffre}) — verifier, migrer et "
                     "changer-phrase le refuseront (fail-closed)",
                foreground="#9a6700")

    def _maj_etat_config(self):
        if not getattr(self, "label_etat_config", None):
            return
        cfg = self.var_config.get().strip()
        if not cfg:
            self.label_etat_config.configure(
                text="config : (vide — le CLI utilisera ses défauts)",
                foreground="#57606a")
            return
        if os.path.isfile(cfg):
            self.label_etat_config.configure(
                text=f"config : trouvée ({cfg})", foreground=COULEUR_VERTE)
        else:
            self.label_etat_config.configure(
                text=f"config : absente ({cfg}) — la migration la créera ; "
                     f"les autres commandes la refuseront",
                foreground="#9a6700")

    def _ouvrir_depot(self):
        """Entrée du profil dépôt : si la pile (pynacl + cryptography) manque,
        on PROPOSE de l'installer avant d'entrer (sinon tout le panneau CF2
        échouerait — mieux vaut le dire tout de suite)."""
        if _paquets_manquants() and not self._pile_prete(
                "Le profil dépôt (coffre CF2 + sceau I)"):
            return      # installation refusée ou en cours : on n'entre pas
        self.montrer("depot")

    def _pile_prete(self, pour_quoi):
        manquants = _paquets_manquants()
        if not manquants:
            return True
        if self._dialogue("askyesno", 
                "Pile du dépôt manquante",
                f"{pour_quoi} exige {' + '.join(manquants)} (absent(s) de "
                f"ce Python).\n\nL'installer maintenant via pip ?\n"
                f"(votre accord requis — c'est la seule dépendance pip de "
                f"la cérémonie)"):
            self.action("pip — installation de la pile du dépôt",
                        installer_dependances)
            self.journal.ajoute("[ceremonie] relancez l'action (ou rouvrez le "
                                "profil) après l'installation, si elle a "
                                "réussi", "info")
        return False

    def _sur_sceau_preparer(self):
        self.action("Sceau I — preparer", self._cli, "sceau_I.py",
                    ["preparer"])

    def _sur_sceau_verifier(self):
        if not self._pile_prete("La vérification des arbres"):
            return
        self.action("Sceau I — verifier", self._cli, "sceau_I.py", ["verifier"])

    def _sur_sceau_deposer(self):
        signatures = self.var_sceau_signatures.get().strip()
        if not signatures:
            self._dialogue("showwarning", "Champ manquant",
                                   "Choisissez la remise signatures-I.txt.")
            return
        if not self._pile_prete("Le dépôt de la remise"):
            return
        args = ["deposer", signatures]
        cle = self.var_sceau_cle.get().strip()
        if cle:
            args += ["--cle", cle]
            detail = ("PREMIÈRE remise : la clé publique sera installée — "
                      "l'assistant ne pourra plus faire évoluer une "
                      "spécification sans votre signature.")
        else:
            detail = ("rotation ordinaire : les signatures seront vérifiées "
                      "contre la clé publique DÉJÀ installée.")
        if not self._dialogue("askyesno", "Acte souverain — déposer la remise",
                                   f"{detail}\n\nSignatures : "
                                   f"{signatures}\nContinuer ?"):
            return
        self.action("Sceau I — deposer", self._cli, "sceau_I.py", args)

    # ------------------------------------------------------------------
    # D116 — fil de cérémonie (auto-détection), git, fenêtre au contenu
    # ------------------------------------------------------------------
    def _sur_fin_action(self):
        """Chaque verdict relance l'auto-détection du fil : l'étape
        satisfaite s'efface, la suivante prend la lumière (D116). D117 :
        si l'action vient d'ATTACHER un nouveau dépôt (clone réussi, ou
        dossier choisi ailleurs), les pages sont rebâties SUR LE FIL
        tkinter — jamais depuis le fil ouvrier — et le profil dépôt
        s'ouvre directement (la cérémonie commence)."""
        if getattr(self, "_racine_pages", RACINE_DEPOT) != RACINE_DEPOT:
            cible = "depot" if depot_disponible() else "accueil"
            self._rebâtir_pages(cible=cible)
            return
        if getattr(self, "label_fil_courant", None) is not None:
            self.racine.after(300, self._rafraichir_fil)

    def _collecter_chemins_fil(self):
        """Les chemins que le fil SONDE : champs remplis par
        l'utilisateur, à défaut les défauts du dépôt attaché (aucune
        invention — le détail des étapes nomme les chemins testés)."""
        def premier(*valeurs):
            for valeur in valeurs:
                if valeur and str(valeur).strip():
                    return str(valeur).strip()
            return None
        sceau_dir = os.path.join(RACINE_DEPOT, "v06", "sceau-I")
        a_signer = premier(self.var_hl_a_signer.get(),
                           os.path.join(sceau_dir, "a-signer.txt"))
        privee = premier(
            None if self.var_hl_cle_manuelle.get() else self.var_hl_cle.get(),
            self.var_hl_privee.get())
        publique = premier(self.var_hl_v_publique.get(),
                           self.var_hl_publique.get(),
                           os.path.join(sceau_dir, "cle-publique-I.txt"))
        signatures = premier(self.var_sceau_signatures.get(),
                             self.var_hl_signatures.get())
        return a_signer, privee, publique, signatures

    def _rafraichir_fil(self):
        """Ré-évalue les étapes par PREUVES (lecture seule) et redessine
        le fil — le TITRE porte le scénario (D117 : cinq étapes en dossier
        local, six en repo git). Les marques MANUELLES survivent (l'union
        l'emporte — seul « Ré-évaluer l'étape » les efface)."""
        if getattr(self, "label_fil_courant", None) is None:
            return
        try:
            self.cadre_fil.configure(
                text="Fil de cérémonie — Sceau I (D117 · scénario : "
                     f"{self.scenario or 'non choisi'})")
        except tk.TclError:
            pass    # page en cours de destruction : le prochain passage suivra
        self.label_fil_courant.configure(
            text="▶ Fil de cérémonie : évaluation en cours (lecture "
                 "seule)…", foreground=COULEUR_ATTENTE)
        self.label_fil_detail.configure(text="", foreground="#57606a")
        self.racine.update_idletasks()
        a_signer, privee, publique, signatures = self._collecter_chemins_fil()
        try:
            etat = fil_ceremonie(a_signer=a_signer, privee=privee,
                                 publique=publique, signatures=signatures,
                                 scenario=self.scenario)
        except Exception as exc:      # jamais muet, même ici
            ENREGISTREUR.ligne(
                f"fil : échec inattendu ({type(exc).__name__}) : {exc}",
                "crash")
            ENREGISTREUR.traceback()
            self.label_fil_courant.configure(
                text="▶ Fil indisponible — échec nommé (rapport : bouton "
                     "« Envoyer le journal… »)", foreground=COULEUR_ROUGE)
            self.label_fil_detail.configure(text=str(exc)[:200])
            return
        self._montrer_fil(etat)

    def _montrer_fil(self, etat):
        """Dessine le fil : faites (une ligne), étape COURANTE (détail +
        geste), à venir (une ligne) — l'étape satisfaite DISPARAÎT pour
        laisser la suivante s'afficher (D116)."""
        self._fil_etat = etat
        faites, suite, courante = [], [], None
        for numero, titre, faite, detail in etat:
            if faite or numero in self.fil_manuel:
                faites.append(f"{numero} · {titre}"
                              + ("" if faite else " (à la main)"))
            elif courante is None:
                courante = (numero, titre, faite, detail)
            else:
                suite.append(f"{numero} · {titre}")
        if faites:
            self.label_fil_resume.configure(
                text="✓ Faites : " + "  ·  ".join(faites),
                foreground=COULEUR_VERTE)
        else:
            self.label_fil_resume.configure(
                text="✓ Faites : (aucune pour l'instant)",
                foreground="#8b949e")
        if courante is None:
            self.label_fil_courant.configure(
                text="✓ CÉRÉMONIE COMPLETE — sceau signé et enregistré sur "
                     "git", foreground=COULEUR_VERTE)
            self.label_fil_detail.configure(
                text="Vérification à froid conseillée sur un clone frais "
                     "(bouton « Vérifier les dix arbres »).",
                foreground="#57606a")
        else:
            numero, titre, _, detail = courante
            self.label_fil_courant.configure(
                text=f"▶ ÉTAPE {numero} — {titre}", foreground=COULEUR_ENCRE)
            self.label_fil_detail.configure(
                text=f"{detail}\n   Geste : {hint_fil(self.scenario, numero)}",
                foreground="#57606a")
        if suite:
            self.label_fil_suite.configure(
                text="· À venir : " + "  ·  ".join(suite))
        else:
            self.label_fil_suite.configure(text="")
        ENREGISTREUR.ligne(
            f"fil : courante={courante[0] if courante else '—'} ; "
            f"manuelles={sorted(self.fil_manuel) or '—'}", "fil")

    def _sur_fil_reevaluer(self):
        """« Ré-évaluer l'étape » : les marques manuelles meurent, les
        PREUVES reprennent seules la parole (la preuve de fichier reste
        la vérité — le clic manuel n'est qu'un aveugle secours)."""
        self.fil_manuel.clear()
        self._rafraichir_fil()

    def _sur_fil_manuel(self):
        """« Marquer faite (à la main) » : l'utilisateur valide l'étape
        courante lui-même (récupération papier, machine sans le dépôt…).
        La marque survit aux ré-évaluations automatiques et meurt au
        « Ré-évaluer » — honnêteté conservée."""
        etat = getattr(self, "_fil_etat", None)
        if not etat:
            return
        for numero, titre, faite, _ in etat:
            if not faite and numero not in self.fil_manuel:
                self.fil_manuel.add(numero)
                self.journal.ajoute(
                    f"[fil] étape {numero} · {titre} — marquée faite À LA "
                    f"MAIN (la preuve de fichier reste la vérité)", "info")
                break
        self._montrer_fil(etat)

    def _demander_texte(self, titre, etiquette, defaut=""):
        """D116 — petit dialogue modal de saisie (message de commit) :
        parent explicite + grab_set (leçon D113 : jamais derrière). La
        saisie part dans la boîte noire (un message de commit n'est pas
        un secret). Retour None si annulé."""
        fenetre = tk.Toplevel(self.racine)
        fenetre.title(titre)
        fenetre.transient(self.racine)
        fenetre.resizable(False, False)
        var = tk.StringVar(value=defaut)
        ttk.Label(fenetre, text=etiquette, wraplength=430,
                  justify="left").pack(anchor="w", padx=12, pady=(10, 2))
        entree = ttk.Entry(fenetre, textvariable=var, width=54)
        entree.pack(fill="x", padx=12, pady=(2, 6))
        entree.focus_set()
        reponse = {"texte": None}

        def valider():
            reponse["texte"] = var.get()
            fenetre.destroy()

        ttk.Button(fenetre, text="Annuler",
                   command=fenetre.destroy).pack(
                       side="right", padx=(4, 12), pady=(2, 10))
        ttk.Button(fenetre, text="Valider",
                   command=valider).pack(side="right", padx=(4, 0),
                                         pady=(2, 10))
        fenetre.bind("<Return>", lambda _e: valider())
        fenetre.bind("<Escape>", lambda _e: fenetre.destroy())
        fenetre.grab_set()
        self.racine.wait_window(fenetre)
        ENREGISTREUR.ligne(f"dialogue « {titre} » → {reponse['texte']!r}",
                           "dialogue")
        return reponse["texte"]

    def _sur_git_pousser(self):
        """Pousser v06/sceau-I sur git : add ciblé → commit → pull
        --rebase → push (échecs nommés — le push rejeté du terrain
        D113-115 ne se reproduira plus silencieusement)."""
        chemin_sceau = os.path.join("v06", "sceau-I")
        if not self._dialogue(
                "askyesno", "Pousser sur git (D116)",
                "Étapes : git add " + chemin_sceau + " → commit → "
                "pull --rebase → push.\n\nSEUL " + chemin_sceau + " sera "
                "ajouté (jamais « add -A » : la clé privée vit hors du "
                "dépôt, les journaux sont ignorés par .gitignore).\n"
                "L'authentification GitHub peut ouvrir votre navigateur.\n"
                "Continuer ?"):
            return
        message = self._demander_texte(
            "Message du commit de cérémonie",
            "Message du commit (il se nomme — fail-closed) :",
            "sceau-I : remise de ceremonie (" +
            datetime.date.today().isoformat() + ")")
        if message is None or not message.strip():
            return      # annulé : aucun lancement, rien n'est écrit
        self.action("Git — pousser v06/sceau-I", git_pousser,
                    [chemin_sceau], message)

    def _ajuster_taille_fenetre(self):
        """D116 — la fenêtre prend la taille de son CONTENU, clampée à
        l'écran. L'ancienne géométrie fixe (1020x740) cachait « Retour à
        l'accueil » quand la page exigeait plus haut ; désormais chaque
        page affichée redimensionne la fenêtre, et si l'écran est trop
        petit le corps DÉFILE (D113) — tout reste atteignable, le bouton
        « ← Accueil » du bandeau aussi (toujours visible, hors du corps
        défilant)."""
        try:
            self.racine.update_idletasks()
            fixe_h = (self.cadre_header.winfo_reqheight()
                      + self.label_verdict.winfo_reqheight()
                      + self.journal.cadre.winfo_reqheight() + 70)
            besoin_h = self.corps.winfo_reqheight() + fixe_h
            besoin_w = max(self.corps.winfo_reqwidth(),
                           self.cadre_header.winfo_reqwidth(),
                           self.journal.cadre.winfo_reqwidth()) + 40
            hauteur = max(600, min(besoin_h,
                                   self.racine.winfo_screenheight() - 120))
            largeur = max(880, min(besoin_w,
                                   self.racine.winfo_screenwidth() - 60))
            self.racine.geometry(f"{largeur}x{hauteur}")
        except tk.TclError:
            pass    # fenêtre en cours de destruction : peu importe

    def _retour_accueil(self):
        self.montrer("accueil")

    def _sur_cf2_migrer(self):
        if not self._pile_prete("La migration CF1 vers CF2"):
            return
        coffre = self._coffre_cf1_exige("La migration CF1 vers CF2")
        if coffre is None:
            return
        phrase = self.var_phrase.get()
        if not phrase.strip():
            self._dialogue("showwarning", "Phrase vide",
                                   "La phrase de contrôle du coffre CF1 est "
                                   "requise (fail-closed) — champ « Phrase "
                                   "de contrôle CF1 » de la section « Coffre "
                                   "CF1 ».")
            return
        if not self._dialogue("askyesno", 
                "Migration CF1 → CF2",
                "Le coffre CF1 sera lu (il restera INTACT) et le CF2 sera "
                "créé : conteneur + 5 fragments chez des gardes + config.\n"
                "Conteneur CF1 lu : " + coffre + "\n"
                "Après la migration : exportez la feuille, contrôlez vos "
                "trois copies hors-ligne, PUIS démarrez la sentinelle.\n"
                "Continuer ?"):
            return
        self.action(
            "CF2 — migrer",
            self._functools.partial(
                self._cli, "coffre_cf2.py",
                ["migrer", "--depuis", coffre] + self._cfg(),
                phrase=phrase))
        self.var_phrase.set("")

    def _sur_cf2_feuille(self):
        if not self._pile_prete("L'export de la feuille"):
            return
        sortie = self.var_feuille.get().strip()
        if not sortie:
            self._dialogue("showwarning", "Champ manquant",
                                   "Choisissez où écrire la feuille.")
            return
        cfg = self.var_config.get().strip()
        if not cfg:
            self._dialogue("showwarning", "Champ manquant",
                                   "Renseignez la config CF2 (bouton "
                                   "Parcourir…).")
            return
        self.action("CF2 — export de la feuille", exporter_feuille, cfg,
                    sortie)

    def _sur_cf2_controle(self):
        if not self._pile_prete("Le contrôle de relecture"):
            return
        copies = [self.var_copie_1.get().strip(),
                  self.var_copie_2.get().strip(),
                  self.var_copie_3.get().strip()]
        if not all(copies):
            self._dialogue("showwarning", "Champs manquants",
                                   "Les TROIS copies relues sont requises "
                                   "(le seuil est la loi).")
            return
        cfg = self.var_config.get().strip()
        if not cfg:
            self._dialogue("showwarning", "Champ manquant",
                                   "Renseignez la config CF2.")
            return
        self.action("CF2 — contrôle de relecture", controle_lecture, cfg,
                    copies)

    def _sur_sentinelle(self):
        if not self._pile_prete("Le démarrage de la sentinelle"):
            return
        cfg = self.var_config.get().strip()
        if not os.path.isfile(cfg):
            self._dialogue("showwarning", "Config absente",
                                   f"config introuvable : {cfg} — migrez "
                                   f"d'abord le coffre.")
            return
        if not self._dialogue("askyesno", 
                "Démarrer la sentinelle",
                "Elle surveillera la couche C et BRÛLERA les fragments si "
                "un processus non blanchi lit une carte.\nElle vivra "
                "DÉTACHÉE : fermer cette fenêtre ne la tuera pas.\n"
                "Vérifiez d'abord la liste blanche (onglet dédié) — une "
                "fausse alerte est une perte auto-infligée.\n\nContinuer ?"):
            return
        self.action("Sentinelle — démarrage détaché",
                    sentinelle_demarrer_detachee, cfg)

    def _sur_cf2_restaurer(self):
        if not self._pile_prete("La restauration des fragments"):
            return
        fichiers = list(filedialog.askopenfilenames(
            title="Choisissez vos copies hors-ligne (au moins le seuil)",
            filetypes=[("Fragment CF2", "*.cf2f"), ("Texte", "*.txt"),
                       ("Tout", "*.*")]))
        if not fichiers:
            return
        if not self._dialogue("askyesno", 
                "Restaurer les fragments",
                f"Les {len(fichiers)} copie(s) choisies seront réécrites "
                f"chez les gardes (atomique : tout ou rien).\nContinuer ?"):
            return
        self.action("CF2 — restaurer", self._cli, "coffre_cf2.py",
                    ["restaurer"] + fichiers + self._cfg())

    def _sur_cf2_bruler(self):
        if not self._pile_prete("Le brûlage"):
            return
        if not self._confirmer_bruler():
            return
        self.action("CF2 — BRÛLAGE (irréversible)", self._cli,
                    "coffre_cf2.py", ["bruler", "--oui-je-comprends"]
                    + self._cfg())

    def _confirmer_bruler(self):
        """Dialogue modal : l'utilisateur doit taper BRULER en toutes lettres
        (l'équivalent GUI de --oui-je-comprends, en plus fort)."""
        fenetre = tk.Toplevel(self.racine)
        fenetre.title("BRÛLAGE — confirmation finale")
        fenetre.transient(self.racine)
        fenetre.grab_set()
        fenetre.resizable(False, False)
        reponse = {"ok": False}
        ttk.Label(fenetre, wraplength=420, justify="left", padding=10,
                  foreground=COULEUR_ROUGE,
                  text=("La destruction est IRRÉVERSIBLE PAR CONSTRUCTION : "
                        "les fragments seront écrasés (trois passes) et un "
                        "procès-verbal sera écrit. La relève exigera vos "
                        "TROIS copies hors-ligne.\n\nPour confirmer, tapez "
                        "BRULER en toutes lettres :")
                  ).pack()
        var = tk.StringVar()
        entree = ttk.Entry(fenetre, textvariable=var, width=24,
                           font=POLICE_FIXE)
        entree.pack(pady=(0, 8))
        entree.focus_set()

        def autoriser(*_):
            bouton.configure(state="normal" if var.get().strip() == "BRULER"
                             else "disabled")

        var.trace_add("write", autoriser)
        barre = ttk.Frame(fenetre)
        barre.pack(pady=(0, 10))

        def oui():
            reponse["ok"] = True
            fenetre.destroy()

        bouton = ttk.Button(barre, text="Je comprends : BRÛLER le coffre",
                            state="disabled", command=oui)
        bouton.pack(side="left", padx=6)
        ttk.Button(barre, text="Annuler",
                   command=fenetre.destroy).pack(side="left", padx=6)
        fenetre.wait_window()
        return reponse["ok"]

    # --- liste blanche ------------------------------------------------------
    def _charger_liste_blanche(self):
        self.liste_blanche.delete(0, "end")
        try:
            motifs = liste_blanche_lire(self.var_config.get().strip())
        except Exception as exc:
            self._note_blanche(f"liste illisible : {exc}")
            return
        for motif in motifs:
            self.liste_blanche.insert("end", motif)

    def _note_blanche(self, texte, couleur=COULEUR_ROUGE):
        self.label_motif_verdict.configure(text=texte, foreground=couleur)

    def _sur_motif_ajouter(self):
        motif = self.var_motif.get().strip()
        if not motif:
            return
        if not motif_valide(motif):
            self._note_blanche(f"motif regex INVALIDE : {motif}")
            return
        if motif in self.liste_blanche.get(0, "end"):
            self._note_blanche(f"déjà présent : {motif}")
            return
        self.liste_blanche.insert("end", motif)
        self.var_motif.set("")
        self._note_blanche("motif AJOUTÉ (non enregistré — bouton "
                           "Enregistrer)", COULEUR_ATTENTE)

    def _sur_motif_retirer(self):
        sel = self.liste_blanche.curselection()
        if not sel:
            return
        self.liste_blanche.delete(sel[0])

    def _sur_motif_tester(self):
        sel = self.liste_blanche.curselection()
        motif = self.var_motif.get().strip() or (
            self.liste_blanche.get(sel[0]) if sel else "")
        essai = self.var_essai.get().strip()
        if not (motif and essai):
            self._note_blanche("sélectionnez (ou saisissez) un motif et une "
                               "ligne à tester")
            return
        if motif_teste(motif, essai):
            self._note_blanche(f"BLANCHI : « {essai} » matche « {motif} »",
                               COULEUR_VERTE)
        else:
            self._note_blanche(f"NON blanchi : « {essai} » ne matche PAS "
                               f"« {motif} » — une telle lecture BRÛLERAIT",
                               COULEUR_ROUGE)

    def _sur_liste_blanche_ecrire(self):
        if not self._pile_prete("L'enregistrement de la liste blanche"):
            return
        motifs = list(self.liste_blanche.get(0, "end"))
        if not self._dialogue("askyesno", 
                "Enregistrer la liste blanche",
                f"{len(motifs)} motif(s) seront écrits dans la config "
                f"(atomique). Une erreur ici arme le brûlage ou l'ouvre "
                f"aux fausses alertes.\nContinuer ?"):
            return
        self.action("Liste blanche — enregistrement", liste_blanche_ecrire,
                    self.var_config.get().strip(), motifs)


# [SUITE-4]

# ===========================================================================
# SECTION E — selftest embarqué (headless : sans tkinter, sans dépôt, sans
# réseau — utilisable sur la machine hors-ligne AVANT la cérémonie) +
# point d'entrée. La batterie COMPLÈTE de falsifiabilité vit dans
# v06/test_ceremonie_gui.py (côté dépôt).
# ===========================================================================

import tempfile   # noqa: E402  (déjà importé en section C si profil dépôt —
                   # l'import est idempotent, et le selftest y a droit aussi)


def _coherence_demarrer_gui():
    """Régression D109 : demarrer_gui ne doit toucher sur « app » QUE des
    attributs qui EXISTENT sur Application (méthodes, ou champs assignés
    dans __init__). Le bogue original appelait app.mainloop() alors que le
    Tk racine vit dans app.racine — la fenêtre mourait à la naissance.
    Contrôle STATIQUE (ast) : fonctionne sur la machine hors-ligne, sans
    aucun affichage. False avec diagnostic imprimé s'il reste un fantôme."""
    import ast
    import inspect
    import textwrap
    try:
        refs = {n.attr for n in ast.walk(ast.parse(textwrap.dedent(
            inspect.getsource(demarrer_gui))))
            if isinstance(n, ast.Attribute)
            and isinstance(n.value, ast.Name) and n.value.id == "app"}
        assignes = set()
        for n in ast.walk(ast.parse(textwrap.dedent(
                inspect.getsource(Application.__init__)))):
            cibles = getattr(n, "targets", None) or (
                [n.target] if isinstance(n, getattr(ast, "AnnAssign", ()))
                and hasattr(n, "target") else [])
            for t in cibles:
                if (isinstance(t, ast.Attribute)
                        and isinstance(t.value, ast.Name)
                        and t.value.id == "self"):
                    assignes.add(t.attr)
        methodes = {nom for nom, _ in inspect.getmembers(
            Application, predicate=inspect.isfunction)}
    except (OSError, TypeError, ValueError) as exc:
        print(f"  selftest : introspection impossible ({exc})")
        return False
    fantomes = sorted(r for r in refs if r not in assignes
                      and r not in methodes)
    if fantomes:
        print(f"  selftest : app.{fantomes} inexistant sur Application — "
              "demarrer_gui planterait (le Tk est app.racine)")
        return False
    return True


def selftest():
    """Batterie de sanité de l'utilisateur final : vecteurs RFC 8032, cycle
    complet générer → signer → vérifier en répertoire temporaire, et
    falsification nommée (un octet de signature muté doit être attrapé).
    True ssi tout passe."""
    import secrets
    passes, echecs = [], []

    def controle(nom, ok, detail=""):
        (passes if ok else echecs).append(nom)
        print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
              + (f" — {detail}" if detail and not ok else ""))

    controle("rfc8032-vecteurs-test1-3", autotest())
    with tempfile.TemporaryDirectory(prefix="ceremonie-selftest-") as tmp:
        privee = os.path.join(tmp, "cle-I-privee.txt")
        publique = os.path.join(tmp, "cle-publique-I.txt")
        a_signer = os.path.join(tmp, "a-signer.txt")
        signatures = os.path.join(tmp, "signatures-I.txt")
        with open(a_signer, "w", encoding="utf-8") as f:
            f.write("m0/test ALPHA " + secrets.token_hex(32) + "\n"
                    "m4/test BETA " + secrets.token_hex(32) + "\n")
        try:
            hl_generer(privee, publique)
            controle("generer-fichiers-ecrits",
                     os.path.isfile(privee) and os.path.isfile(publique))
            with open(privee, "r", encoding="utf-8") as f:
                contenu = f.read()
            controle("generer-entete-garde-present",
                     "clé I PRIVÉE" in contenu and "GARDE" in contenu)
            hl_signer(a_signer, privee, signatures)
            with open(signatures, "r", encoding="utf-8") as f:
                lignes = [l for l in f.read().splitlines() if l.strip()]
            controle("signer-deux-signatures", len(lignes) == 2,
                     f"{len(lignes)} lignes")
            ok, texte = hl_verifier(a_signer, signatures, publique)
            controle("verifier-remise-valable", ok, texte)
            # falsification : un octet de signature muté => ÉCHEC nommé
            fautif = os.path.join(tmp, "signatures-fausses.txt")
            premiere = lignes[0].split()
            premiere[2] = ("0" if premiere[2][0] != "0" else "1") \
                + premiere[2][1:]
            with open(fautif, "w", encoding="utf-8") as f:
                f.write(" ".join(premiere) + "\n" + "\n".join(lignes[1:])
                        + "\n")
            ok_f, _ = hl_verifier(a_signer, fautif, publique)
            controle("falsification-un-octet-attrapee", not ok_f,
                     "la remise falsifiée a été acceptée !")
        except ErreurCeremonie as exc:
            controle("cycle-sans-erreur", False, str(exc))
    # régression D109 : le point d'entrée ne référence que du réel
    controle("demarrer_gui-attributs-coherents",
             _coherence_demarrer_gui())
    # D113 : la boîte noire écrit et restitue (le rapport aura du fond)
    marque = "selftest-boite-noire-" + secrets.token_hex(8)
    ENREGISTREUR.ligne(marque, "selftest")
    try:
        with open(CHEMIN_JOURNAL_VOL, "r", encoding="utf-8") as f:
            retrouvé = marque in f.read()
    except OSError:
        retrouvé = False
    controle("boite-noire-ecrit-et-restitue", retrouvé)
    # D117 : le scénario AVANT TOUT — masquage de jeton, preuve clone,
    # gestes du fil qui suivent le scénario
    controle("d117-masque-jeton-url",
             masquer_jeton("https://jeton@github.com/u/r.git")
             == "https://***@github.com/u/r.git"
             and masquer_jeton("https://user:pass@h/x.git")
             == "https://***@h/x.git"
             and masquer_jeton("git@github.com:u/r.git")
             == "git@github.com:u/r.git")
    with tempfile.TemporaryDirectory(prefix="ceremonie-selftest-scen-") as tmp:
        faite, detail = preuve_clone(tmp)
        controle("d117-preuve-refusee-hors-git-nommee", not faite
                 and "pas un dépôt git" in detail, detail)
    controle("d117-hints-suivent-le-scenario",
             "Cloner en local" in hint_fil(SCENARIO_GIT, 1)
             and hint_fil(SCENARIO_GIT, 2) == FIL_HINTS[1]
             and hint_fil(SCENARIO_DOSSIER, 1) == FIL_HINTS[1]
             and hint_fil(None, 5) == FIL_HINTS[5])
    print(f"[ceremonie-GUI] selftest : "
          f"{len(passes)} PASS / {len(echecs)} ÉCHEC")
    return not echecs


def main():
    parseur = argparse.ArgumentParser(
        description="TRIADE — Maître de cérémonie (GUI). Sans argument : "
                    "fenêtre. --selftest : batterie headless (machine "
                    "hors-ligne incluse). --depot CHEMIN : attache le GUI "
                    "à un clone du dépôt triade (D111), où qu'il vive.")
    parseur.add_argument("--selftest", action="store_true",
                         help="batterie embarquée (aucune GUI requise)")
    parseur.add_argument("--profil", choices=["hors-ligne", "depot"],
                         default=None,
                         help="ouvrir directement ce profil (sinon : accueil)")
    parseur.add_argument("--depot", metavar="CHEMIN", default=None,
                         help="racine d'un clone du dépôt triade (celui qui "
                              "contient v06/) — priorité sur TRIADE_DEPOT "
                              "et sur la position de ce fichier ; un chemin "
                              "introuvable est un échec nommé (code 2)")
    arguments = parseur.parse_args()
    try:
        racine, source = _resoudre_racine_depot(arguments.depot)
    except ErreurCeremonie as exc:
        print(f"[ceremonie-GUI] ÉCHEC — {exc}", file=sys.stderr)
        return 2
    definir_racine_depot(racine, source)
    if arguments.selftest:
        ok = selftest()
        return 0 if ok else 1
    return demarrer_gui(profil=arguments.profil)


if __name__ == "__main__":
    sys.exit(main())
