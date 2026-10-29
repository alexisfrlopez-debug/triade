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
  T3  déterminisme du manifeste (double calcul, mtime changé, dépôt réel
      vert)
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
  T4  clé de TEST déterministe + état visible (« test », jamais confondu
      avec une cérémonie réelle — défaut X8 sinon)

Les tests ne touchent JAMAIS aux vrais arbres ni au vrai dépôt : tout se
joue sur une RÉPLIQUE (copie temporaire, globaux du module patchés), et la
dernière ligne vérifie que le dépôt RÉEL est toujours vert.

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
        return self

    def __exit__(self, *args):
        for cle, valeur in self.sauves.items():
            setattr(S, cle, valeur)
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _lire_manifeste_source(self, arbre):
        """Manifeste d'origine du dépôt réel (restauration F3-c)."""
        chemin = os.path.join(self.source, "v06", "sceau-I", "manifestes",
                              f"{arbre}.txt")
        with open(chemin, "r", encoding="utf-8") as f:
            return f.read()


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
    lignes = [l[8:].split("  ", 1)[1] for l in texte1.splitlines()
              if l.startswith("sha256:")]
    verifie("T3-c lignes triées lexicographiquement (canon POSIX)",
            lignes == sorted(lignes))
    # le dépôt RÉEL est vert (aucun test précédent n'a dû le toucher)
    code = S.verifier(silencieux=True)
    verifie("T3-d dépôt réel : 10 arbres verts", code == S.OK,
            f"code={code}")


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
    with Replique() as rep:
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
        with open(os.path.join(S.DIR_MANIFESTES, "m4.txt"), "w",
                  encoding="utf-8") as f:
            f.write(rep._lire_manifeste_source("m4"))
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
    print("[T4] clé de TEST déterministe, état visible (jamais « reelle »)")
    graine1 = S.graine_cle_test()
    graine2 = S.graine_cle_test()
    verifie("T4-a graine de test stable (constante publique)",
            graine1 == graine2
            == hashlib.sha256(S.CONSTANTE_CLE_TEST).digest())
    from cryptography.hazmat.primitives.asymmetric.ed25519 import \
        Ed25519PrivateKey
    pub_calc = Ed25519PrivateKey.from_private_bytes(graine1) \
        .public_key().public_bytes_raw()
    verifie("T4-b la clé déposée du dépôt RÉEL est bien la clé de test",
            pub_calc == S.cle_publique_deposee())
    verifie("T4-c état de clé visible : « test », jamais « reelle »",
            "test" in S.etat_cle() and "reelle" not in S.etat_cle())


def main():
    print("=== v0.6.0 axe 3 — falsifiabilité du sceau de l'Intention (D105) ===")
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
    # le dépôt RÉEL est resté vert du début à la fin
    code = S.verifier(silencieux=True)
    print(f"[final] dépôt réel : {'VERT (10 arbres)' if code == S.OK else 'CODE ' + str(code)}")
    return 0 if code == S.OK else 1


if __name__ == "__main__":
    sys.exit(main())
