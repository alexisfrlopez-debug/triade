#!/usr/bin/env python3
"""test_sceau_I.py — v0.6.0 axe 3 (D105) : la falsifiabilité du sceau de l'Intention.

Une garde qui ne rejette rien ne garde rien (leçon M3). Cette suite prouve
les critères de sortie D87 un par un :

  T1  vecteurs RFC 8032 § 7.1 par la cérémonie pure-Python (le témoin
      byte-level — la leçon D102 : deux implémentations d'accord entre
      elles ne prouvent rien contre la SPÉCIFICATION)
  T2  interopérabilité BIDIRECTIONNELLE pure-Python <-> cryptography
      (signer A vérifier B, signer B vérifier A, signatures déterministes
      IDENTIQUES, clés publiques identiques — 20 messages seedés)
  T3  déterminisme du manifeste (double calcul, mtime changé, jumelle
      CRLF IDENTIQUE — canon LF D115 : la représentation du checkout
      n'est pas l'intention —, octet muté hors fin de ligne toujours
      attrapé, dépôt réel vert OU fenêtre de re-cérémonie PROUVÉE —
      représentation seule (D115) OU contenu en attente de signature (D126))
  F1  la CÉRÉMONIE COMPLÈTE en laboratoire, sur RÉPLIQUE : generer →
      signer → verifier (script autonome, sous-processus, répertoire
      isolé) → deposer --cle → le dépôt de réplique passe vert avec
      l'état « reelle » : le flux air-gap exact du développeur, joué
  F2  falsification D'UN OCTET par arbre (10/10) — rejet + fichier
      divergent NOMMÉ (l'évidence, pas un verdict muet)
  F3  diffs d'intention NON SIGNÉS refusés par la GARDE DE BUILD :
      ajout, suppression, manifeste réécrit (l'attaquant refait le
      manifeste : la SIGNATURE doit le dénoncer — code 11), signature
      supprimée (12), lien symbolique et répertoire vide (structure),
      garde() lève le refus nommé que build_m4/build_terrain attrapent
  F4  remise douteuse REFUSÉE sans rien écrire (atomicité : mauvaise
      signature, remise incomplète, balise divergente — le dépôt reste
      INTACT, octet pour octet)
  T4  clé de TEST déterministe + COHÉRENCE état ↔ clé déposée (l'ère lab
      dépose la clé de test et dit « test » ; l'ère réelle dépose une
      clé ≠ test et dit « reelle » — mentir dans un sens comme dans
      l'autre serait le défaut X8)

Les tests ne touchent JAMAIS aux vrais arbres ni au vrai dépôt : tout se
joue sur une RÉPLIQUE (copie temporaire, globaux du module patchés,
ré-alignée VERT canonique par signer-test à l'entrée — D115 : le dépôt
réel peut porter les empreintes CRLF d'une cérémonie de terrain pendant
la fenêtre de re-cérémonie), et la dernière ligne vérifie que le dépôt
RÉEL est vert — ou, pendant la fenêtre D115, que sa divergence est de
REPRÉSENTATION seule, signatures valides — ou, pendant une fenêtre de
RE-CÉRÉMONIE de CONTENU (modèle D126 : spec CF3 entrée dans v06/I/,
erratum § 12 CF2 appliqué), que a-signer.txt est FRAIS (empreintes
vivantes, balises courantes) et que les signatures déposées restent
valides : l'intention évoluée attend sa signature, rien ne fut altéré.

Usage : python3 v06/test_sceau_I.py
"""

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import sceau_I as S                      # noqa: E402
from v06 import ceremonie_hors_ligne as C         # noqa: E402

PASSES, ECHECS = [], []


def verifie(nom, condition, detail=""):
    """Compteur project : chaque contrôle est nommé, aucun silence."""
    if condition:
        PASSES.append(nom)
        print(f"  PASS {nom}")
    else:
        ECHECS.append(f"{nom} ({detail})" if detail else nom)
        print(f"  ÉCHEC {nom} {('— ' + detail) if detail else ''}")


# ---------------------------------------------------------------------------
# Réplique : copie des arbres + du dépôt vers un répertoire temporaire,
# globaux du module sceau_I patchés — les vrais fichiers JAMAIS touchés.
# ---------------------------------------------------------------------------

class Replique:
    """Contexte : RACINE/SCEAU_DIR/… redirigés vers la copie temporaire."""

    def __init__(self, source_racine=RACINE):
        self.source = source_racine
        self.tmp = tempfile.mkdtemp(prefix="sceau-I-replique-")
        self.sauves = {}

    def __enter__(self):
        for arbre in S.ARBRES:
            src = os.path.join(self.source, arbre, "I")
            dst = os.path.join(self.tmp, arbre, "I")
            shutil.copytree(src, dst)
        src_dep = os.path.join(self.source, "v06", "sceau-I")
        dst_dep = os.path.join(self.tmp, "v06", "sceau-I")
        shutil.copytree(src_dep, dst_dep)
        self.sauves = {
            "RACINE": S.RACINE, "SCEAU_DIR": S.SCEAU_DIR,
            "DIR_MANIFESTES": S.DIR_MANIFESTES,
            "DIR_SIGNATURES": S.DIR_SIGNATURES, "ETAT_CLE": S.ETAT_CLE,
        }
        S.RACINE = self.tmp
        S.SCEAU_DIR = dst_dep
        S.DIR_MANIFESTES = os.path.join(dst_dep, "manifestes")
        S.DIR_SIGNATURES = os.path.join(dst_dep, "signatures")
        S.ETAT_CLE = os.path.join(dst_dep, "etat-cle.txt")
        # D115 — la réplique repart d'un état VERT canonique (clé de test,
        # spec § 8) : le dépôt copié peut porter les empreintes CRLF d'une
        # cérémonie de terrain (fenêtre de re-cérémonie) — F2/F3/F4 doivent
        # mesurer leurs PROPRES mutations, pas la fenêtre du dépôt réel.
        S.signer_test()
        return self

    def __exit__(self, *args):
        for cle, valeur in self.sauves.items():
            setattr(S, cle, valeur)
        shutil.rmtree(self.tmp, ignore_errors=True)


def _empreinte_depot(replique):
    """Empreinte globale du dépôt de réplique (atomicité F4)."""
    morceaux = []
    for racine_dir, dirs, fichiers in os.walk(replique.tmp + "/v06/sceau-I"):
        dirs.sort()
        for nom in sorted(fichiers):
            chemin = os.path.join(racine_dir, nom)
            with open(chemin, "rb") as f:
                morceaux.append(os.path.relpath(chemin, replique.tmp) +
                                ":" + hashlib.sha256(f.read()).hexdigest())
    return hashlib.sha256("|".join(sorted(morceaux)).encode()).hexdigest()


# ---------------------------------------------------------------------------
# T1 — vecteurs RFC 8032 par la cérémonie pure-Python
# ---------------------------------------------------------------------------

def t1_vecteurs_rfc():
    print("[T1] vecteurs RFC 8032 § 7.1 (cérémonie pure-Python)")
    for indice, (graine_hex, pub_hex, msg_hex, sig_hex) in enumerate(
            C.VECTEURS_RFC8032, 1):
        graine, message = bytes.fromhex(graine_hex), bytes.fromhex(msg_hex)
        ok = (C.cle_publique_depuis_graine(graine).hex() == pub_hex
              and C.signer_ed25519(graine, message).hex() == sig_hex
              and C.verifier_ed25519(bytes.fromhex(pub_hex), message,
                                     bytes.fromhex(sig_hex)))
        verifie(f"T1-a vecteur TEST {indice} (clé+signature+vérification)", ok)
    # passage silencieux interdit : signature de zéros, message muté
    _, pub_hex, msg_hex, sig_hex = C.VECTEURS_RFC8032[1]
    verifie("T1-b signature de zéros rejetée",
            not C.verifier_ed25519(bytes.fromhex(pub_hex),
                                   bytes.fromhex(msg_hex), bytes(64)))
    message = bytearray(bytes.fromhex(msg_hex))
    message[0] ^= 1
    verifie("T1-c un octet de message muté rejeté",
            not C.verifier_ed25519(bytes.fromhex(pub_hex), bytes(message),
                                   bytes.fromhex(sig_hex)))
    signature = bytearray(bytes.fromhex(sig_hex))
    signature[63] ^= 1
    verifie("T1-d un octet de signature muté rejeté",
            not C.verifier_ed25519(bytes.fromhex(pub_hex),
                                   bytes.fromhex(msg_hex), bytes(signature)))


# ---------------------------------------------------------------------------
# T2 — interopérabilité bidirectionnelle pure-Python <-> cryptography
# ---------------------------------------------------------------------------

def t2_interop():
    print("[T2] interop pure-Python <-> cryptography (20 messages seedés)")
    from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PrivateKey
    tout_identiques, tout_croises, tout_cles = True, True, True
    for i in range(20):
        graine = hashlib.sha256(f"TRIADE interop {i}".encode()).digest()
        message = hashlib.sha256(f"message {i} v06".encode()).digest()
        # clés publiques identiques
        pub_pur = C.cle_publique_depuis_graine(graine)
        cle_lib = Ed25519PrivateKey.from_private_bytes(graine)
        pub_lib = cle_lib.public_key().public_bytes_raw()
        if pub_pur != pub_lib:
            tout_cles = False
        # signatures déterministes identiques
        sig_pur = C.signer_ed25519(graine, message)
        sig_lib = cle_lib.sign(message)
        if sig_pur != sig_lib:
            tout_identiques = False
        # croisées : signer A, vérifier B (les deux sens)
        if not S._verifier_ed25519(message, sig_pur, pub_lib):
            tout_croises = False
        ok_lib = True
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import \
            Ed25519PublicKey
        try:
            Ed25519PublicKey.from_public_bytes(pub_pur).verify(sig_lib, message)
        except InvalidSignature:
            ok_lib = False
        if not ok_lib:
            tout_croises = False
    verifie("T2-a clés publiques identiques ×20", tout_cles)
    verifie("T2-b signatures déterministes identiques ×20", tout_identiques)
    verifie("T2-c vérifications croisées des deux sens ×20", tout_croises)


# ---------------------------------------------------------------------------
# T3 — déterminisme du manifeste + dépôt réel vert
# ---------------------------------------------------------------------------

# Hash canonique (LF) du v06/I/README.md AMENDÉ par D115 (règle § 2 :
# hachage du contenu canonique LF) — l'UNIQUE divergence de contenu
# tolérée pendant la fenêtre de re-cérémonie : l'amendement lui-même,
# en attente de re-signature par la clé physique du développeur.
HASH_README_V06_D115 = "4bd40fa591ebc9728bd900dbb74c70e21b3f4a804732548b6e2105eb8c0922f0"


def _hashes_manifeste(texte):
    """Dictionnaire chemin -> condensé (parseur « sha256: » = 7 caractères)."""
    d = {}
    for l in texte.splitlines():
        if l.startswith("sha256:"):
            condense, chemin = l[7:].split("  ", 1)
            d[chemin] = condense
    return d


def _fenetre_d115():
    """(ok, detail) — le dépôt réel pendant la fenêtre de re-cérémonie D115.

    Il porte les empreintes CRLF de la cérémonie de terrain D113 pendant
    que code et arbres vivants sont devenus canoniques LF. PREUVE exigée
    fichier par fichier : hash(CRLF(vivant)) == hash déposé — sauf
    v06/I/README.md, l'amendement D115 lui-même (hash littéral
    ci-dessus) ; et signature par signature : la clé réelle a bien signé
    l'empreinte déposée. Cette fonction MEURT à la re-cérémonie :
    verifier() re-verdit et ne l'appelle plus."""
    for arbre in S.ARBRES:
        texte_vivant, _ = S.manifeste(arbre)
        with open(os.path.join(S.DIR_MANIFESTES, f"{arbre}.txt"),
                  encoding="utf-8") as f:
            texte_depose = f.read()
        vivants = _hashes_manifeste(texte_vivant)
        deposees = _hashes_manifeste(texte_depose)
        for chemin_f in sorted(set(vivants) | set(deposees)):
            if vivants.get(chemin_f) == deposees.get(chemin_f):
                continue
            p = os.path.join(S.RACINE, arbre, "I", chemin_f)
            try:
                with open(p, "rb") as f:
                    canon = f.read().replace(b"\r\n", b"\n")
            except OSError as e:
                return False, f"{arbre}/I/{chemin_f} illisible : {e}"
            if (arbre == "v06" and chemin_f == "README.md"
                    and hashlib.sha256(canon).hexdigest()
                    == HASH_README_V06_D115):
                continue      # l'amendement D115, en attente de signature
            if hashlib.sha256(canon.replace(b"\n", b"\r\n")).hexdigest() \
                    != deposees.get(chemin_f):
                return False, (f"{arbre}/I/{chemin_f} : divergence hors "
                               f"représentation CRLF/LF")
        empreinte_deposee = hashlib.sha256(
            texte_depose.encode("utf-8")).hexdigest()
        try:
            with open(os.path.join(S.DIR_SIGNATURES, f"{arbre}.txt"),
                      encoding="utf-8") as f:
                signature = f.read().strip()
            valide = S._verifier_ed25519(bytes.fromhex(empreinte_deposee),
                                          bytes.fromhex(signature),
                                          S.cle_publique_deposee())
        except (OSError, ValueError, S.EchecSceauI) as e:
            return False, f"signature {arbre} illisible : {e}"
        if not valide:
            return False, f"signature {arbre} invalide (empreinte déposée)"
    return True, ""


def _fenetre_recemonie():
    """(ok, detail) — le dépôt réel pendant la fenêtre de RE-CÉRÉMONIE
    (modèle D126 : l'intention a évolué, la signature est EN ATTENTE).

    L'état CONÇU par preparer (spec § 6) : des arbres vivants divergent
    de leurs manifestes déposés PAR CONTENU (la spec CF3 entrée dans
    v06/I/, l'erratum § 12 du README CF2 appliqué) — mais DEUX preuves
    tiennent et font la différence avec une falsification :
    (1) a-signer.txt est FRAIS : chaque ligne porte l'empreinte VIVANTE
    de son arbre et la balise COURANTE de la table — la charge utile de
    la cérémonie est prête, la clé physique du développeur n'a plus
    qu'à signer ; (2) les signatures DÉPOSÉES restent valides contre
    les manifestes déposés et la clé déposée : l'ancien état signé est
    INTACT — rien ne fut altéré, seule la nouvelle signature manque.
    Cette fonction MEURT à la cérémonie : verifier() re-verdit et ne
    l'appelle plus (même loi que _fenetre_d115)."""
    # (1) a-signer.txt FRAIS — empreintes vivantes + balises courantes
    try:
        with open(os.path.join(S.SCEAU_DIR, "a-signer.txt"),
                  encoding="utf-8") as f:
            lignes = [l.strip() for l in f if l.strip()]
    except OSError as e:
        return False, f"a-signer.txt illisible : {e}"
    attendues = {}
    for ligne in lignes:
        morceaux = ligne.split()
        if len(morceaux) != 3:
            return False, f"a-signer.txt ligne malformée : {ligne!r}"
        arbre, balise, empreinte = morceaux
        if arbre not in S.ARBRES:
            return False, f"a-signer.txt arbre inconnu : {arbre!r}"
        if balise != S.ARBRES[arbre][1]:
            return False, (f"a-signer.txt balise périmée pour {arbre} : "
                           f"{balise!r} != {S.ARBRES[arbre][1]!r}")
        attendues[arbre] = empreinte
    if set(attendues) != set(S.ARBRES):
        return False, "a-signer.txt incomplet (arbres manquants)"
    for arbre in S.ARBRES:
        _, emp_vivante = S.manifeste(arbre)
        if attendues[arbre] != emp_vivante:
            return False, (f"a-signer.txt PÉRIMÉ pour {arbre} : "
                           "l'empreinte vivante a encore bougé depuis "
                           "preparer")
    # (2) les signatures déposées restent valides — l'ancien état signé
    # est intact (rien ne fut altéré pendant la fenêtre)
    for arbre in S.ARBRES:
        try:
            with open(os.path.join(S.DIR_MANIFESTES, f"{arbre}.txt"),
                      encoding="utf-8") as f:
                texte_depose = f.read()
            empreinte_deposee = hashlib.sha256(
                texte_depose.encode("utf-8")).hexdigest()
            with open(os.path.join(S.DIR_SIGNATURES, f"{arbre}.txt"),
                      encoding="utf-8") as f:
                signature = f.read().strip()
            valide = S._verifier_ed25519(bytes.fromhex(empreinte_deposee),
                                          bytes.fromhex(signature),
                                          S.cle_publique_deposee())
        except (OSError, ValueError, S.EchecSceauI) as e:
            return False, f"signature {arbre} illisible : {e}"
        if not valide:
            return False, (f"signature {arbre} invalide — l'ancien état "
                           "signé fut altéré (ceci n'est PAS une fenêtre "
                           "de re-cérémonie)")
    diverges = []
    for arbre in S.ARBRES:
        _, emp_vivante = S.manifeste(arbre)
        with open(os.path.join(S.DIR_MANIFESTES, f"{arbre}.txt"),
                  encoding="utf-8") as f:
            emp_deposee = hashlib.sha256(
                f.read().encode("utf-8")).hexdigest()
        if emp_vivante != emp_deposee:
            diverges.append(arbre)
    if not diverges:
        return False, "aucun arbre divergé (fenêtre de re-cérémonie impossible)"
    return True, ("divergence d'intention en attente de signature : "
                  + ", ".join(diverges))


def t3_determinisme():
    print("[T3] déterminisme du manifeste")
    texte1, emp1 = S.manifeste("m4")
    texte2, emp2 = S.manifeste("m4")
    verifie("T3-a double calcul identique", emp1 == emp2 and texte1 == texte2)
    # mtime changé, contenu identique -> manifeste identique
    chemin = os.path.join(S.RACINE, "m4", "I", "tls-02-verdicts.md")
    avant = os.stat(chemin).st_mtime
    os.utime(chemin, (avant + 1234, avant + 1234))
    texte3, emp3 = S.manifeste("m4")
    os.utime(chemin, (avant, avant))
    verifie("T3-b mtime changé, manifeste inchangé", emp3 == emp1)
    # tri indépendant du système : lignes déjà triées lexicographiquement
    lignes = [l[7:].split("  ", 1)[1] for l in texte1.splitlines()
              if l.startswith("sha256:")]
    verifie("T3-c lignes triées lexicographiquement (canon POSIX)",
            lignes == sorted(lignes))
    # D115 — jumelle CRLF : même intention, autre représentation. La
    # réplique (ré-alignée canonique en __enter__) reste VERTE sur des
    # fichiers portés en CRLF : le sceau ne voit pas la représentation.
    with Replique():
        base = os.path.join(S.RACINE, "m4", "I")
        for racine_dir, dirs, fichiers in os.walk(base):
            for nom in fichiers:
                p = os.path.join(racine_dir, nom)
                with open(p, "rb") as f:
                    brut = f.read()
                with open(p, "wb") as f:
                    f.write(brut.replace(b"\r\n", b"\n")
                            .replace(b"\n", b"\r\n"))
        texte_crlf, emp_crlf = S.manifeste("m4")
        verifie("T3-d jumelle CRLF : manifeste IDENTIQUE (canon LF, D115)",
                texte_crlf == texte1 and emp_crlf == emp1)
        verifie("T3-e jumelle CRLF : verifier VERT (représentation invisible)",
                S.verifier(["m4"], silencieux=True) == S.OK)
        # un octet VRAIMENT muté (hors paire \r\n) reste attrapé
        p = os.path.join(base, "tls-02-verdicts.md")
        with open(p, "rb") as f:
            brut = f.read()
        i = next(k for k, o in enumerate(brut) if o not in (10, 13))
        with open(p, "wb") as f:
            f.write(brut[:i] + bytes([brut[i] ^ 1]) + brut[i + 1:])
        code, _, detail = S._etat_arbre("m4")
        verifie("T3-f octet muté hors fin de ligne : divergence NOMMÉE",
                code == S.CODE_DIVERGE and "modifie" in detail
                and "tls-02-verdicts.md" in detail,
                f"code={code} {detail}")
    # le dépôt RÉEL : vert — ou fenêtre D115 (représentation seule) — ou
    # fenêtre de RE-CÉRÉMONIE (D126) : l'intention a évolué, a-signer
    # FRAIS attend la clé physique du développeur
    code = S.verifier(silencieux=True)
    if code == S.OK:
        verifie("T3-g dépôt réel : arbres verts (canon LF)", True)
    else:
        ok_f, detail = _fenetre_d115()
        if ok_f:
            verifie("T3-g dépôt réel : fenêtre D115 — divergence de "
                    "représentation seule, signatures valides", True)
        else:
            ok_r, detail_r = _fenetre_recemonie()
            verifie("T3-g dépôt réel : fenêtre de re-cérémonie — "
                    "a-signer FRAIS, anciennes signatures valides, "
                    "divergence d'intention en attente de signature",
                    ok_r, detail_r if not ok_r else detail)


# ---------------------------------------------------------------------------
# F1 — la cérémonie complète en laboratoire (flux air-gap du développeur)
# ---------------------------------------------------------------------------

def f1_ceremonie_complete():
    print("[F1] cérémonie complète air-gap sur réplique (sous-processus)")
    with Replique() as rep:
        # a-signer depuis les arbres de la réplique
        lignes = []
        for arbre in S.ARBRES:
            _, empreinte = S.manifeste(arbre)
            lignes.append(f"{arbre} {S.ARBRES[arbre][1]} {empreinte}")
        chemin_a_signer = os.path.join(rep.tmp, "a-signer.txt")
        with open(chemin_a_signer, "w", encoding="utf-8") as f:
            f.write("\n".join(lignes) + "\n")
        # 1. generer (sous-processus isolé, comme sur machine hors ligne)
        r1 = subprocess.run([sys.executable,
                             os.path.join(RACINE, "v06",
                                          "ceremonie_hors_ligne.py"),
                             "generer"], cwd=rep.tmp, capture_output=True,
                            text=True, timeout=300)
        privee = os.path.join(rep.tmp, "cle-I-privee.txt")
        publique = os.path.join(rep.tmp, "cle-publique-I.txt")
        verifie("F1-a generer vert (exit 0)", r1.returncode == 0,
                r1.stderr[-200:] if r1.returncode else "")
        verifie("F1-b cle-I-privee.txt créée (et jamais affichée)",
                os.path.isfile(privee)
                and r1.stdout.find("cle-I-privee") >= 0
                and not any(l.strip().isalnum() and len(l.strip()) == 64
                            for l in r1.stdout.splitlines()))
        # 2. signer
        r2 = subprocess.run([sys.executable,
                             os.path.join(RACINE, "v06",
                                          "ceremonie_hors_ligne.py"),
                             "signer", "a-signer.txt", "cle-I-privee.txt"],
                            cwd=rep.tmp, capture_output=True, text=True,
                            timeout=300)
        signatures = os.path.join(rep.tmp, "signatures-I.txt")
        verifie("F1-c signer vert (10 signatures auto-vérifiées)",
                r2.returncode == 0 and os.path.isfile(signatures),
                r2.stderr[-200:] if r2.returncode else "")
        # 3. verifier autonome
        r3 = subprocess.run([sys.executable,
                             os.path.join(RACINE, "v06",
                                          "ceremonie_hors_ligne.py"),
                             "verifier", "a-signer.txt", "signatures-I.txt",
                             "cle-publique-I.txt"],
                            cwd=rep.tmp, capture_output=True, text=True,
                            timeout=300)
        verifie("F1-d verifier autonome : TOUT VERT", r3.returncode == 0
                and "TOUT VERT" in r3.stdout, r3.stdout[-200:])
        # 4. deposer --cle dans le dépôt de la réplique
        code = S.deposer(signatures, publique)
        verifie("F1-e deposer --cle : rotation installée", code == S.OK)
        verifie("F1-f état de clé devient « reelle »",
                "reelle" in S.etat_cle())
        code = S.verifier(silencieux=True)
        verifie("F1-g le dépôt de réplique passe vert sous la clé de cérémonie",
                code == S.OK, f"code={code}")


# ---------------------------------------------------------------------------
# F2 — falsification d'un octet par arbre (10/10)
# ---------------------------------------------------------------------------

def f2_falsification_octet():
    print("[F2] falsification d'UN octet par arbre — rejet + fichier NOMMÉ")
    with Replique():
        for arbre in S.ARBRES:
            rel, chemin = S._entrees_arbre(arbre)[0]
            with open(chemin, "rb") as f:
                contenu = bytearray(f.read())
            contenu[len(contenu) // 2] ^= 0x01
            with open(chemin, "wb") as f:
                f.write(contenu)
            code, _, detail = S._etat_arbre(arbre)
            attendu = (code == S.CODE_DIVERGE and "modifie" in detail
                       and rel in detail)
            verifie(f"F2 {arbre}: divergence, fichier nommé", attendu,
                    f"code={code} detail={detail}")


# ---------------------------------------------------------------------------
# F3 — diffs non signés refusés par la garde de build
# ---------------------------------------------------------------------------

def f3_diffs_non_signes():
    print("[F3] diffs non signés refusés (garde de build, codes nommés)")
    with Replique():
        # (a) ajout d'un fichier — l'extension ne compte pas : tout entre
        rel, chemin = S._entrees_arbre("m4")[0]
        nouveau = os.path.join(os.path.dirname(chemin), "zz-nouveau.md")
        with open(nouveau, "w", encoding="utf-8") as f:
            f.write("intention contrebande\n")
        code, _, detail = S._etat_arbre("m4")
        verifie("F3-a fichier AJOUTÉ -> 10 + nommé",
                code == S.CODE_DIVERGE and "ajoute" in detail and "zz-nouveau"
                in detail, f"code={code} {detail}")
        os.remove(nouveau)
        # (b) suppression d'un fichier
        sauve = None
        with open(chemin, "rb") as f:
            sauve = f.read()
        os.remove(chemin)
        code, _, detail = S._etat_arbre("m4")
        verifie("F3-b fichier SUPPRIMÉ -> 10 + nommé",
                code == S.CODE_DIVERGE and "supprime" in detail and rel
                in detail, f"code={code} {detail}")
        with open(chemin, "wb") as f:
            f.write(sauve)
        # (c) l'attaquant RÉÉCRIT le manifeste déposé pour suivre l'arbre
        # muté : la SIGNATURE doit dénoncer (code 11)
        contenu = bytearray(sauve)
        contenu[len(contenu) // 2] ^= 0x01
        with open(chemin, "wb") as f:
            f.write(contenu)
        texte_vivant, _ = S.manifeste("m4")
        with open(os.path.join(S.DIR_MANIFESTES, "m4.txt"), "w",
                  encoding="utf-8") as f:
            f.write(texte_vivant)
        code, _, detail = S._etat_arbre("m4")
        verifie("F3-c manifeste RÉÉCRIT par l'attaquant -> signature "
                "invalide (11)", code == S.CODE_SIGNATURE,
                f"code={code} {detail}")
        with open(chemin, "wb") as f:
            f.write(sauve)
        # D115 : restaure le manifeste CANONIQUE de la réplique (fichier
        # rétabli) — l'ère du dépôt source n'entre plus ici.
        texte_retabli, _ = S.manifeste("m4")
        with open(os.path.join(S.DIR_MANIFESTES, "m4.txt"), "w",
                  encoding="utf-8") as f:
            f.write(texte_retabli)
        # (d) signature supprimée -> dépôt incohérent (12)
        chemin_sig = os.path.join(S.DIR_SIGNATURES, "m4.txt")
        with open(chemin_sig, "r", encoding="utf-8") as f:
            sig_sauve = f.read()
        os.remove(chemin_sig)
        code, _, detail = S._etat_arbre("m4")
        verifie("F3-d signature SUPPRIMÉE -> 12",
                code == S.CODE_DEPOT and "absente" in detail,
                f"code={code} {detail}")
        with open(chemin_sig, "w", encoding="utf-8") as f:
            f.write(sig_sauve)
        # (e) lien symbolique dans l'arbre -> refus structurel
        cible = os.path.join(S.RACINE, "m4", "I", "raccourci.md")
        os.symlink("/etc/hostname", cible)
        try:
            S._entrees_arbre("m4")
            verifie("F3-e lien symbolique refusé", False, "aucune exception")
        except S.EchecSceauI:
            verifie("F3-e lien symbolique refusé", True)
        os.remove(cible)
        # (f) répertoire vide dans l'arbre -> refus structurel
        vide = os.path.join(S.RACINE, "m4", "I", "sous-rep-vide")
        os.mkdir(vide)
        try:
            S._entrees_arbre("m4")
            verifie("F3-f répertoire vide refusé", False, "aucune exception")
        except S.EchecSceauI:
            verifie("F3-f répertoire vide refusé", True)
        os.rmdir(vide)
        # (g) la GARDE DE BUILD : arbre muté -> EchecSceauI nommé (c'est le
        # refus que build_m4/build_terrain attrapent — code 11 en sortie)
        with open(chemin, "rb") as f:
            original = f.read()
        contenu = bytearray(original)
        contenu[10] ^= 0x01
        with open(chemin, "wb") as f:
            f.write(contenu)
        try:
            S.garde(["m0", "m1", "m2", "m3", "m4"])
            verifie("F3-g garde() refuse le build (exception nommée)", False,
                    "aucune exception levée")
        except S.EchecSceauI as e:
            message = str(e)
            verifie("F3-g garde() refuse le build (exception nommée)",
                    "m4" in message and "REFUSE" in message
                    and "cle hors-ligne" in message, message[:120])
        with open(chemin, "wb") as f:
            f.write(original)
        # (h) après restauration : la garde repasse verte (pas de rémanence)
        try:
            S.garde(["m0", "m1", "m2", "m3", "m4"])
            verifie("F3-h garde verte après restauration (rémanence nulle)",
                    True)
        except S.EchecSceauI as e:
            verifie("F3-h garde verte après restauration (rémanence nulle)",
                    False, str(e)[:120])


# ---------------------------------------------------------------------------
# F4 — remise douteuse : rien n'est écrit (atomicité)
# ---------------------------------------------------------------------------

def f4_remise_douteuse():
    print("[F4] remise douteuse refusée SANS ÉCRIRE (atomicité)")
    with Replique() as rep:
        empreinte_avant = _empreinte_depot(rep)
        # signature d'un arbre remplacée par des zéros
        avec = []
        for arbre in S.ARBRES:
            _, empreinte = S.manifeste(arbre)
            signature = ("00" * 64) if arbre == "m7" else \
                S._signer_ed25519(bytes.fromhex(empreinte),
                                  S.graine_cle_test()).hex()
            avec.append(f"{arbre} {S.ARBRES[arbre][1]} {signature}")
        try:
            S._deposer(avec)
            verifie("F4-a mauvaise signature refusée", False,
                    "aucune exception")
        except S.EchecSceauI as e:
            verifie("F4-a mauvaise signature refusée", "INVÉRIFIABLE" in str(e))
        verifie("F4-b dépôt INTACT après refus",
                _empreinte_depot(rep) == empreinte_avant)
        # remise incomplète (un arbre manquant)
        incomplete = [f"{a} {S.ARBRES[a][1]} "
                      + S._signer_ed25519(bytes.fromhex(S.manifeste(a)[1]),
                                          S.graine_cle_test()).hex()
                      for a in S.ARBRES if a != "demo"]
        try:
            S._deposer(incomplete)
            verifie("F4-c remise incomplète refusée", False,
                    "aucune exception")
        except S.EchecSceauI as e:
            verifie("F4-c remise incomplète refusée", "INCOMPLÈTE" in str(e))
        verifie("F4-d dépôt INTACT après refus incomplet",
                _empreinte_depot(rep) == empreinte_avant)
        # balise divergente dans la remise
        balises = [f"{a} balise-fausse "
                   + S._signer_ed25519(bytes.fromhex(S.manifeste(a)[1]),
                                       S.graine_cle_test()).hex()
                   for a in S.ARBRES]
        try:
            S._deposer(balises)
            verifie("F4-e balise divergente refusée", False,
                    "aucune exception")
        except S.EchecSceauI as e:
            verifie("F4-e balise divergente refusée",
                    "balise divergente" in str(e))
        verifie("F4-f dépôt INTACT après refus de balise",
                _empreinte_depot(rep) == empreinte_avant)


# ---------------------------------------------------------------------------
# T4 — clé de TEST : déterminisme + état visible
# ---------------------------------------------------------------------------

def t4_cle_test():
    print("[T4] clé de TEST déterministe, cohérence état ↔ clé (défaut X8)")
    graine1 = S.graine_cle_test()
    graine2 = S.graine_cle_test()
    verifie("T4-a graine de test stable (constante publique)",
            graine1 == graine2
            == hashlib.sha256(S.CONSTANTE_CLE_TEST).digest())
    from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PrivateKey
    pub_test = Ed25519PrivateKey.from_private_bytes(graine1) \
        .public_key().public_bytes_raw()
    deposee = S.cle_publique_deposee()
    etat = S.etat_cle()
    # D115 : les DEUX ères sont honnêtes — lab : clé de test déposée +
    # état « test » ; cérémonie réelle : clé ≠ test + état « reelle ».
    # Dire « reelle » sur la clé du lab (ou l'inverse) serait le défaut
    # X8 : affirmer une preuve non faite.
    verifie("T4-b cohérence état ↔ clé déposée (X8 : jamais « reelle » "
            "sur la clé de test, jamais « test » sur une clé réelle)",
            ("reelle" in etat) == (deposee != pub_test)
            and ("test" in etat) == (deposee == pub_test))
    verifie("T4-c l'état de clé NOMME l'ère (test/reelle, jamais muet)",
            ("test" in etat) or ("reelle" in etat))


def main():
    print("=== v0.6.0 axe 3 — falsifiabilité du sceau de l'Intention "
          "(D105, canon LF D115) ===")
    t1_vecteurs_rfc()
    t2_interop()
    t3_determinisme()
    f1_ceremonie_complete()
    f2_falsification_octet()
    f3_diffs_non_signes()
    f4_remise_douteuse()
    t4_cle_test()
    total = len(PASSES) + len(ECHECS)
    print(f"\n=== BILAN : {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC "
          f"sur {total} contrôles ===")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    # le dépôt RÉEL : vert — ou fenêtre D115 PROUVÉE — ou fenêtre de
    # re-cérémonie (D126) PROUVÉE
    code = S.verifier(silencieux=True)
    if code == S.OK:
        print(f"[final] dépôt réel : VERT ({len(S.ARBRES)} arbres, canon LF D115)")
        return 0
    ok_f, detail = _fenetre_d115()
    if ok_f:
        print("[final] dépôt réel : FENÊTRE D115 — empreintes déposées de "
              "la cérémonie de terrain (CRLF), divergence de représentation "
              "SEULE, signatures valides ; la re-cérémonie du développeur "
              "(clé physique) re-signera les manifestes canoniques")
        return 0
    ok_r, detail_r = _fenetre_recemonie()
    if ok_r:
        print(f"[final] dépôt réel : FENÊTRE DE RE-CÉRÉMONIE — {detail_r} ; "
              "a-signer.txt est FRAIS (empreintes vivantes, balises "
              "courantes) et les signatures déposées restent valides : "
              "l'ancien état signé est INTACT, seule la nouvelle signature "
              "manque — la clé physique du développeur signera la nouvelle "
              "intention (ceremonie_hors_ligne.py signer, puis sceau_I.py "
              "deposer)")
        return 0
    print(f"[final] dépôt réel : CODE {code} — divergence NON expliquée : "
              f"{detail_r or detail}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
