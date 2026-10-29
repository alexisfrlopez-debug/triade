#!/usr/bin/env python3
"""sceau_I.py — v0.6.0 axe 3 (D87) : le sceau de l'Intention, côté dépôt.

Spécification : v06/I/README.md (R2 écrite-avant-code — CE fichier
l'instancie, aucun écart toléré). Le sceau signe l'INTENTION (les arbres
de couche I) avec la clé Ed25519 hors-ligne du développeur ; la clé
publique et les signatures par arbre vivent dans v06/sceau-I/ ; les
chaînes de build appellent garde() et refusent un arbre divergé.

Codes de sortie (nommés, fail-closed) :
  0  = tout vert
  10 = arbre divergé de son manifeste signé (diff d'intention non signé)
  11 = signature invalide
  12 = dépôt incohérent (fichier manquant, format fautif, arbre illisible)

Modes :
  preparer   — manifestes vivants -> a-signer.txt (la charge utile cérémonie)
  deposer    — installe signatures-I.txt (+ --cle la clé publique réelle)
  signer-test— signe avec la clé de TEST (lab, spec § 8) et dépose
  verifier   — la gardienne : arbre vivant == manifeste déposé == signature
  etat       — lecture seule, table des arbres (outil d'audit, jamais garde)

La graine de TEST est dérivée d'une CONSTANTE PUBLIQUE (une clé de test
n'est un secret pour personne — sa non-sécurité EST la preuve visible de
l'état laboratoire ; spec § 8). La clé RÉELLE ne passe jamais ici.
"""

import argparse
import hashlib
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCEAU_DIR = os.path.join(RACINE, "v06", "sceau-I")
DIR_MANIFESTES = os.path.join(SCEAU_DIR, "manifestes")
DIR_SIGNATURES = os.path.join(SCEAU_DIR, "signatures")
ETAT_CLE = os.path.join(SCEAU_DIR, "etat-cle.txt")

ENTETE = "TRIADE-SCEAU-I v1"

# Table des arbres (spec § 1) — l'ORDRE est canonique (codes de sortie :
# le premier arbre fautif dans l'ordre de la table nomme le code).
ARBRES = {
    "m0": ("hello.exe", "0.1.0"),
    "m1": ("minilibc (hello/selftest/echo)", "0.2.0"),
    "m2": ("echo.exe + tcp", "0.3.0"),
    "m3": ("proxy.exe", "0.4.0"),
    "m4": ("proxy.exe (tunnel)", "0.5.0"),
    "m6": ("hachoir", "hachoir.1"),
    "m7": ("sceau", "sceau.1"),
    "demo": ("demo.exe", "0.3.0"),
    "terrain": ("superviseur.exe", "terrain.19/17-H"),
    "v06": ("coffre CF2 + sceau-I (transversal)", "v0.6.0-axes2-3"),
}

# Constante publique de dérivation de la clé de TEST (spec § 8) — PAS un
# secret : quiconque la connaît peut re-signer en phase test, c'est CONSIGNÉ.
CONSTANTE_CLE_TEST = b"TRIADE cle-test-I v1 (lab, D105 - remplacee par la ceremonie reelle)"

OK = 0
CODE_DIVERGE = 10
CODE_SIGNATURE = 11
CODE_DEPOT = 12


class EchecSceauI(Exception):
    """Refus nommé de la garde (intégration chaînes de build : fail-closed)."""


# ---------------------------------------------------------------------------
# Manifeste canonique (spec § 2)
# ---------------------------------------------------------------------------

def _entrees_arbre(arbre):
    """Fichiers réguliers de <arbre>/I, tri lexicographique POSIX.

    Fail-closed structurel : lien symbolique, fichier spécial, répertoire
    vide, arbre absent ou vide -> EchecSceauI (un arbre d'intention n'est
    pas un espace arbitraire — spec § 2 règle 3).
    """
    base = os.path.join(RACINE, arbre, "I")
    if not os.path.isdir(base):
        raise EchecSceauI(f"arbre {arbre}/I absent du depôt (spec § 1)")
    entrees, repertoires_vides = [], []
    for racine_dir, dirs, fichiers in os.walk(base):
        dirs.sort()
        if not dirs and not fichiers:
            repertoires_vides.append(racine_dir)
        for nom in fichiers:
            chemin = os.path.join(racine_dir, nom)
            if os.path.islink(chemin):
                raise EchecSceauI(
                    f"lien symbolique refusé dans {arbre}/I : {nom} (spec § 2 r3)")
            if not os.path.isfile(chemin):
                raise EchecSceauI(
                    f"entrée non régulière refusée dans {arbre}/I : {nom} (spec § 2 r3)")
            rel = os.path.relpath(chemin, base).replace(os.sep, "/")
            entrees.append((rel, chemin))
    if repertoires_vides:
        raise EchecSceauI(
            f"répertoire vide refusé dans {arbre}/I : "
            f"{os.path.relpath(repertoires_vides[0], base)} (spec § 2 r3)")
    if not entrees:
        raise EchecSceauI(f"arbre {arbre}/I vide (spec § 2 r3)")
    entrees.sort(key=lambda e: e[0])
    return entrees


def manifeste(arbre):
    """Manifeste canonique de l'arbre VIVANT -> (texte, empreinte).

    L'empreinte est le SHA-256 du texte ENTIER (en-tête compris — spec § 2
    règle 4 : aucun champ hors signature).
    """
    artefact, balise = ARBRES[arbre]
    entrees = _entrees_arbre(arbre)
    lignes = [ENTETE, f"arbre: {arbre}", f"artefact: {artefact}",
              f"balise: {balise}", f"fichiers: {len(entrees)}"]
    for rel, chemin in entrees:
        with open(chemin, "rb") as f:
            condense = hashlib.sha256(f.read()).hexdigest()
        lignes.append(f"sha256:{condense}  {rel}")
    texte = "\n".join(lignes) + "\n"
    empreinte = hashlib.sha256(texte.encode("utf-8")).hexdigest()
    return texte, empreinte


# ---------------------------------------------------------------------------
# Clé publique déposée + vérification Ed25519 (côté dépôt : cryptography)
# ---------------------------------------------------------------------------

def _lire_hex(chemin, quoi, taille=32):
    with open(chemin, "r", encoding="utf-8") as f:
        hexa = f.read().strip()
    if len(hexa) != taille * 2 or any(c not in "0123456789abcdef" for c in hexa):
        raise EchecSceauI(f"{quoi} malformé : {chemin} (hexadecimal minuscule "
                          f"de {taille * 2} caracteres attendu, spec § 3)")
    return bytes.fromhex(hexa)


def cle_publique_deposee():
    return _lire_hex(os.path.join(SCEAU_DIR, "cle-publique-I.txt"),
                     "cle-publique-I.txt")


def _verifier_ed25519(message, signature, publique):
    """True ssi la signature Ed25519 (RFC 8032) est valide."""
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    try:
        Ed25519PublicKey.from_public_bytes(publique).verify(signature, message)
        return True
    except InvalidSignature:
        return False


def graine_cle_test():
    """Graine de la clé de TEST — dérivée d'une constante PUBLIQUE (spec § 8).

    Déterministe et re-dérivable partout : l'état lab survit à toute
    réinitialisation sans jamais prétendre à la moindre confidentialité.
    """
    return hashlib.sha256(CONSTANTE_CLE_TEST).digest()


# ---------------------------------------------------------------------------
# Vérification (la gardienne — spec § 6)
# ---------------------------------------------------------------------------

def _etat_arbre(arbre):
    """État nommé d'un arbre : (code, empreinte_vivante, detail).

    code 0 = vert ; 10 = divergé ; 11 = signature invalide ; 12 = dépôt
    incohérent. L'ordre des contrôles est le contrat : structure, dépôt,
    divergence, signature — le PREMIER échec nomme le code.
    """
    texte_vivant, empreinte_vivante = manifeste(arbre)
    chemin_manifeste = os.path.join(DIR_MANIFESTES, f"{arbre}.txt")
    chemin_signature = os.path.join(DIR_SIGNATURES, f"{arbre}.txt")
    if not os.path.isfile(chemin_manifeste):
        return CODE_DEPOT, empreinte_vivante, "manifeste depose absent"
    if not os.path.isfile(chemin_signature):
        return CODE_DEPOT, empreinte_vivante, "signature deposee absente"
    with open(chemin_manifeste, "r", encoding="utf-8") as f:
        texte_depose = f.read()
    empreinte_deposee = hashlib.sha256(texte_depose.encode("utf-8")).hexdigest()
    if texte_vivant != texte_depose:
        # Nommer le premier fichier divergent (l'évidence, pas juste le verdict)
        # — dictionnaires CHEMIN -> condensé (itération sur les CHEMINS :
        # un fichier modifié garde sa clé, seul le condensé diverge)
        vivantes = {}
        for l in texte_vivant.splitlines():
            if l.startswith("sha256:"):
                condense, chemin = l[8:].split("  ", 1)
                vivantes[chemin] = condense
        deposees = {}
        for l in texte_depose.splitlines():
            if l.startswith("sha256:"):
                condense, chemin = l[8:].split("  ", 1)
                deposees[chemin] = condense
        detail = "divergence d'intention"
        for chemin in sorted(set(vivantes) | set(deposees)):
            if vivantes.get(chemin) != deposees.get(chemin):
                action = ("modifie" if chemin in vivantes and chemin in deposees
                          else "ajoute" if chemin in vivantes else "supprime")
                detail = f"fichier {action} : {chemin}"
                break
        return CODE_DIVERGE, empreinte_vivante, detail
    try:
        signature = _lire_hex(chemin_signature, f"signature {arbre}", 64)
    except EchecSceauI as e:
        return CODE_DEPOT, empreinte_vivante, str(e)
    publique = cle_publique_deposee()
    if not _verifier_ed25519(bytes.fromhex(empreinte_deposee), signature, publique):
        return CODE_SIGNATURE, empreinte_vivante, "signature Ed25519 invalide"
    return OK, empreinte_vivante, "vert"


def verifier(arbres=None, silencieux=False):
    """La gardienne. Retourne le CODE DU PREMIER arbre fautif (ordre table)."""
    if not os.path.isfile(os.path.join(SCEAU_DIR, "cle-publique-I.txt")):
        print("[sceau-I] ECHEC depot : cle-publique-I.txt absent (spec § 5)")
        return CODE_DEPOT
    code_sortie = OK
    for arbre in (arbres if arbres is not None else list(ARBRES)):
        try:
            code, empreinte, detail = _etat_arbre(arbre)
        except EchecSceauI as e:
            code, empreinte, detail = CODE_DEPOT, "?", str(e)
        if code != OK:
            print(f"[sceau-I] {arbre}: CODE {code} — {detail} "
                  f"(empreinte vivante {empreinte[:16]}…)")
            if code_sortie == OK:
                code_sortie = code
        elif not silencieux:
            print(f"[sceau-I] {arbre}: vert ({empreinte[:16]}…)")
    if code_sortie == OK and not silencieux:
        print(f"[sceau-I] verifier : {len(ARBRES) if arbres is None else len(arbres)}"
              f" arbres VERTS — cle deposee {etat_cle()}")
    return code_sortie


def garde(arbres):
    """Garde pour les chaînes de build (spec § 7) — lève EchecSceauI.

    Fail-closed : un dépôt absent, un arbre divergé, une signature
    invalide — le build ne démarre JAMAIS. Les messages citent l'arbre et
    le fichier divergent (l'évidence nommée, pas un verdict muet).
    """
    if not os.path.isdir(SCEAU_DIR):
        raise EchecSceauI("depot sceau-I absent : le depôt n'est pas sous sceau "
                          "(preparer + signer-test ou ceremonie reelle, spec § 4-5)")
    manquants = [a for a in arbres if a not in ARBRES]
    if manquants:
        raise EchecSceauI(f"arbres inconnus de la table spec § 1 : {manquants}")
    for arbre in arbres:
        code, empreinte, detail = _etat_arbre(arbre)
        if code != OK:
            raise EchecSceauI(
                f"garde sceau-I : arbre {arbre} REFUSE (code {code}) — {detail} ; "
                f"diff d'intention non signe : la cle hors-ligne du developpeur "
                f"est requise (D87, spec § 7)")


# ---------------------------------------------------------------------------
# Preparer / déposer / signer-test / état
# ---------------------------------------------------------------------------

def etat_cle():
    """Écriture visible de l'état de la clé (test/réelle — spec § 8)."""
    try:
        with open(ETAT_CLE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "inconnu (etat-cle.txt absent — signer-test ou ceremonie requise)"


def preparer():
    """Écrit a-signer.txt (une ligne par arbre : arbre balise empreinte).

    Les arbres divergés de leur manifeste déposé sont RAPPORTÉS nommément :
    c'est le signal « l'intention a évolué, signature requise ».
    """
    lignes, divergences = [], []
    for arbre in ARBRES:
        texte_vivant, empreinte = manifeste(arbre)
        balise = ARBRES[arbre][1]
        lignes.append(f"{arbre} {balise} {empreinte}")
        chemin_manifeste = os.path.join(DIR_MANIFESTES, f"{arbre}.txt")
        if os.path.isfile(chemin_manifeste):
            with open(chemin_manifeste, "r", encoding="utf-8") as f:
                depose = f.read()
            if empreinte != hashlib.sha256(depose.encode("utf-8")).hexdigest():
                divergences.append(arbre)
    chemin = os.path.join(SCEAU_DIR, "a-signer.txt")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print(f"[sceau-I] preparer : {len(lignes)} arbres -> {chemin}")
    if divergences:
        print(f"[sceau-I] arbres DIVERGES de leur manifeste depose "
              f"(signature requise) : {', '.join(divergences)}")
    else:
        print("[sceau-I] aucun arbre divergé : les empreintes == signatures "
              "en place (re-signature inutile)")
    return OK


def _signer_ed25519(message, graine):
    """Signature Ed25519 côté dépôt (cryptography) — pour signer-test."""
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    return Ed25519PrivateKey.from_private_bytes(graine).sign(message)


def _deposer(lignes_signature, cle_pour_verif=None, cle_a_ecrire=None,
             label_etat=None):
    """Installe les signatures + manifestes vivants (spec § 5 rotation).

    Chaque signature est vérifiée AVANT toute écriture (une remise
    invérifiable est un échec nommé, rien n'est écrit — atomicité de
    cérémonie : clé, signatures et manifestes basculent ENSEMBLE ou pas
    du tout). Écrit : signatures/<arbre>.txt, manifestes/<arbre>.txt
    (manifeste vivant), éventuellement cle-publique-I.txt + etat-cle.txt.
    """
    a_installer = []
    for ligne in lignes_signature:
        morceaux = ligne.split()
        if len(morceaux) != 3:
            raise EchecSceauI(f"ligne de signature malformée : {ligne!r}")
        arbre, balise, signature_hex = morceaux
        if arbre not in ARBRES:
            raise EchecSceauI(f"arbre inconnu dans la remise : {arbre!r}")
        if balise != ARBRES[arbre][1]:
            raise EchecSceauI(
                f"balise divergente dans la remise pour {arbre} : "
                f"{balise!r} != {ARBRES[arbre][1]!r} (la remise et le dépôt "
                f"doivent décrire le MÊME état — spec § 5)")
        if len(signature_hex) != 128 or any(
                c not in "0123456789abcdef" for c in signature_hex):
            raise EchecSceauI(f"signature malformée pour {arbre} (128 hex attendus)")
        a_installer.append((arbre, signature_hex))
    if len(a_installer) != len(ARBRES):
        manquants = sorted(set(ARBRES) - {a for a, _ in a_installer})
        raise EchecSceauI(f"remise INCOMPLÈTE : arbres manquants {manquants} "
                          f"(une rotation couvre TOUS les arbres — spec § 5)")
    # Vérification intégrale AVANT écriture (fail-closed d'abord) — contre
    # la clé COURANTE du dépôt, ou la clé de cérémonie si rotation (la clé
    # n'est installée qu'à la PHASE D'ÉCRITURE : un échec laisse le dépôt
    # INTACT, jamais une clé neuve au-dessus de signatures mortes).
    cle_verif = cle_pour_verif if cle_pour_verif is not None \
        else cle_publique_deposee()
    for arbre, signature_hex in a_installer:
        _, empreinte = manifeste(arbre)
        if not _verifier_ed25519(bytes.fromhex(empreinte),
                                 bytes.fromhex(signature_hex),
                                 cle_verif):
            raise EchecSceauI(
                f"signature de remise INVÉRIFIABLE pour {arbre} — rien n'est "
                f"écrit (cérémonie douteuse, spec § 4)")
    # Écriture (seulement si tout est vert)
    os.makedirs(DIR_SIGNATURES, exist_ok=True)
    os.makedirs(DIR_MANIFESTES, exist_ok=True)
    for arbre, signature_hex in a_installer:
        with open(os.path.join(DIR_SIGNATURES, f"{arbre}.txt"), "w",
                  encoding="utf-8") as f:
            f.write(signature_hex + "\n")
        texte, _ = manifeste(arbre)
        with open(os.path.join(DIR_MANIFESTES, f"{arbre}.txt"), "w",
                  encoding="utf-8") as f:
            f.write(texte)
    if cle_a_ecrire is not None:
        with open(os.path.join(SCEAU_DIR, "cle-publique-I.txt"), "w",
                  encoding="utf-8") as f:
            f.write(cle_a_ecrire.hex() + "\n")
    if label_etat is not None:
        with open(ETAT_CLE, "w", encoding="utf-8") as f:
            f.write(label_etat + "\n")
    print(f"[sceau-I] deposer : {len(a_installer)} signatures installees "
          f"(manifestes vivants) ; etat cle = {etat_cle()}")
    return OK


def deposer(chemin_remise, chemin_cle=None):
    """Mode CLI : dépose signatures-I.txt [cle-publique réelle].

    Atomicité intégrale : le fichier de remise est lu et validé AVANT tout
    accès au dépôt ; en rotation, la clé de cérémonie ne s'installe qu'en
    phase d'écriture, après vérification complète de la remise.
    """
    with open(chemin_remise, "r", encoding="utf-8") as f:
        lignes = [l.strip() for l in f if l.strip()]
    cle_pour_verif = None
    if chemin_cle is not None:
        cle_pour_verif = _lire_hex(chemin_cle, "cle publique de ceremonie")
    label = "reelle (ceremonie hors-ligne, D87)" if cle_pour_verif is not None \
        else etat_cle()
    return _deposer(lignes, cle_pour_verif=cle_pour_verif,
                    cle_a_ecrire=cle_pour_verif, label_etat=label)


def signer_test():
    """Signe les manifestes VIVANTS avec la clé de TEST et dépose (spec § 8).

    Jamais présenté comme cérémonie réelle : l'état de clé est écrit
    « test », visible par etat et répété au tableau de bord.
    """
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    graine = graine_cle_test()
    publique = Ed25519PrivateKey.from_private_bytes(graine).public_key() \
        .public_bytes_raw()
    lignes = []
    for arbre in ARBRES:
        _, empreinte = manifeste(arbre)
        signature = _signer_ed25519(bytes.fromhex(empreinte), graine)
        lignes.append(f"{arbre} {ARBRES[arbre][1]} {signature.hex()}")
    # La clé de test s'installe comme clé courante — via la MÊME atomicité
    # que la cérémonie réelle (vérification intégrale avant écriture)
    return _deposer(lignes, cle_pour_verif=publique, cle_a_ecrire=publique,
                    label_etat="test (cle-test-I lab, D105/D106 — a remplacer "
                               "par la ceremonie hors-ligne du developpeur, "
                               "spec § 8)")


def etat():
    """Lecture seule : table des arbres (audit, jamais garde)."""
    print(f"[sceau-I] etat — cle deposee : {etat_cle()}")
    try:
        publique = cle_publique_deposee().hex()
        print(f"[sceau-I] cle-publique-I : {publique}")
    except (EchecSceauI, FileNotFoundError):
        print("[sceau-I] cle-publique-I : ABSENTE")
    for arbre in ARBRES:
        try:
            code, empreinte, detail = _etat_arbre(arbre)
        except EchecSceauI as e:
            code, empreinte, detail = CODE_DEPOT, "?", str(e)
        etat_txt = {OK: "SIGNE (vert)", CODE_DIVERGE: "DIVERGE",
                    CODE_SIGNATURE: "SIGNATURE INVALIDE",
                    CODE_DEPOT: "DEPOT INCOHERENT"}[code]
        print(f"  {arbre:<9} {ARBRES[arbre][1]:<22} {etat_txt:<20} {detail}")
    return OK


def main():
    parseur = argparse.ArgumentParser(
        description="Sceau de l'Intention (v0.6.0 axe 3, D87) — outil dépôt")
    parseur.add_argument("mode", choices=["preparer", "deposer", "signer-test",
                                          "verifier", "etat"])
    parseur.add_argument("fichier", nargs="?", help="deposer : signatures-I.txt")
    parseur.add_argument("--cle", help="deposer : cle-publique-I.txt de la "
                                       "cérémonie réelle (rotation, spec § 5)")
    parseur.add_argument("--arbres", help="verifier : liste restreinte "
                                          "(virgules) pour les gardes de build")
    arguments = parseur.parse_args()
    # Échec NOMMÉ au niveau CLI (le GUI streame ces lignes dans son journal) :
    # une remise douteuse s'affiche comme une phrase, pas comme un traceback
    # — l'atomicité de cérémonie garantit que rien n'a été écrit.
    try:
        if arguments.mode == "preparer":
            return preparer()
        if arguments.mode == "deposer":
            if not arguments.fichier:
                print("usage : sceau_I.py deposer signatures-I.txt "
                      "[--cle cle-publique-I.txt]")
                return CODE_DEPOT
            return deposer(arguments.fichier, arguments.cle)
        if arguments.mode == "signer-test":
            return signer_test()
        if arguments.mode == "verifier":
            arbres = arguments.arbres.split(",") if arguments.arbres else None
            return verifier(arbres)
        return etat()
    except EchecSceauI as exc:
        print(f"[sceau-I] ECHEC : {exc}")
        print("[sceau-I] rien n'a été écrit (atomicité de cérémonie)")
        return CODE_DEPOT
    except OSError as exc:
        print(f"[sceau-I] ECHEC : fichier illisible — {exc}")
        print("[sceau-I] rien n'a été écrit (atomicité de cérémonie)")
        return CODE_DEPOT


if __name__ == "__main__":
    sys.exit(main())
