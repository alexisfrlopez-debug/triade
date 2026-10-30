#!/usr/bin/env python3
"""test_cf2.py — v0.6.0 axe 2 (D106) : la falsifiabilité du coffre CF2.

Une garde qui ne rejette rien ne garde rien (leçon M3). Cette suite prouve
les critères de sortie D86 un par un (spec v06/I/CF2/README.md § 13) :

  T1  Shamir CONTRE TÉMOIN INDÉPENDANT : vecteur à aléa fixé recalculé par
      l'évaluation en SOMME DE PUISSANCES (et multiplication GF bit-à-bit —
      une SECONDE implémentation du corps, rien de partagé avec les tables
      log/exp : la leçon D102 « d'accord entre eux, faux contre le monde »),
      1 000 secrets × les DIX combinaisons C(5,3), reconstitution croisée
      par ÉLIMINATION DE GAUSS (algorithme encore différent), refus des
      bornes (t=1, t>n, n>255, x dupliqués, taille fausse)
  T2  sous T : informationnellement MORT — deux M′ arbitraires, chacun
      rendu COMPATIBLE avec T−1 fragments réels par un troisième fragment
      forgé : la réconstitution rend M′ sans erreur (aucune discrimination
      n'est possible), c'est le champ verif qui NOMME le mensonge
  T3  conteneur fail-closed : round-trip, verif faux, AEAD altéré,
      algorithme hors liste blanche, conteneur tronqué — refus NOMMÉS
  T4  fausses alertes NULLES : lecteur BLANCHI (même binaire que l'attaquant,
      seule la LIGNE DE COMMANDE distingue — la liste blanche juge la
      commande, pas l'image) 1,5 s de lecture soutenue : RIEN ne brûle ;
      accès par ATTRIBUTS seuls (stat, listage) : aucun signal
  F1  EXFILTRATION SIMULÉE (critère D86) : lecteur non blanchi → PV écrit
      avec déclencheur NOMMÉ (pid, image, fichier), fragments détruits,
      coffre MORT (refus nommé), latence mesurée < 2 s (borne consignée),
      relève : T copies restaurées → vie (le cycle complet)
  F2  remise douteuse REFUSÉE sans écrire : tag corrompu dans le lot,
      indice déjà présent, fragment d'un AUTRE coffre — gardes INTACTES
      octet pour octet (atomicité D105 [11])
  T5  santé de la sentinelle : heart-beat frais en vie, MORT visible après
      décès (sante exit 1)
  T6  D119 Windows : os.open() sur un dossier = PermissionError errno 13
      (le crash du terrain v1.8 : « CF2 — migrer » mourait en écrivant
      .keys/coffre_cf2.bin) — le fsync de répertoire est POSIX-seul
      (sous 'nt' il ne touche JAMAIS os.open), l'écriture atomique SURVIT
      à la simulation fidèle du refus Windows (contenu exact, pas de .tmp),
      et sous POSIX un dossier impossible à ouvrir est toléré (le replace
      est déjà fait — la durabilité du dossier est mieux-disante)
  T7  D120 la PORTE de sentinelle (la demande du terrain : « si le
      déverrouillage est tenté et qu'elle n'est pas lancée, tous nos
      efforts sont inutiles ») : exiger=true + sentinelle ABSENTE →
      `verifier` refuse NOMMÉ avec parade, journalise le refus, ne touche
      RIEN ; sentinelle VIVANTE → le MÊME verifier passe VERT ; sentinelle
      TUÉE → heart-beat périmé, refus NOMMÉ (la mort est visible) ;
      exiger=false (ère Windows sans moteur, spec § 9) → AVERTIT et
      passe ; la BORNE consignée : un heart-beat fraîchement FORGÉ ouvre
      la porte — discipline, pas cryptographie (l'aveu est le contrôle)
  X8  les coffres RÉELS ne sont pas touchés : md5 de .keys/coffre_fort.bin
      inchangé, aucun .keys/coffre_cf2.bin créé ; coffre réel ABSENT
      (clone frais, kit du Drive) : l'absence est un état NOMMÉ qui doit
      subsister — jamais un crash (le verdict CF2 à froid clone GitHub,
      .keys/ n'y vit jamais)

Usage : python3 v06/test_cf2.py
"""

import glob
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)
from v06 import coffre_cf2 as C                     # noqa: E402
from v06 import sentinelle_cf2 as S                 # noqa: E402

PASSES, ECHECS = [], []


def verifie(nom, condition, detail=""):
    if condition:
        PASSES.append(nom)
        print(f"  PASS {nom}")
    else:
        ECHECS.append(f"{nom} ({detail})" if detail else nom)
        print(f"  ÉCHEC {nom} {('— ' + detail) if detail else ''}")


def refuse(nom, fonction, *a, **k):
    """Un refus NOMMÉ est un PASS muet interdit (leçon M3)."""
    try:
        fonction(*a, **k)
        verifie(nom, False, "aucun refus levé")
    except C.ErreurCoffre as exc:
        verifie(nom, len(str(exc)) > 0, f"refus muet : {exc!r}")


# ---------------------------------------------------------------------------
# GF(2^8) INDÉPENDANT — multiplication bit-à-bit, zéro table partagée (T1)
# ---------------------------------------------------------------------------

def gf_mult_independant(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B
        b >>= 1
    return r


def gf_inv_independant(a: int) -> int:
    for b in range(1, 256):
        if gf_mult_independant(a, b) == 1:
            return b
    raise AssertionError("inverse introuvable — corps cassé")


def reconstituer_gauss(fragments):
    """Élimination de Gauss sur GF(2^8) — algorithme INDÉPENDANT de Lagrange.

    Système résolu OCTET PAR OCTET : Vandermonde [1, x, x², …] , inconnues
    les coefficients, M = coefficient CONSTANT de la solution.
    """
    n = len(fragments)
    base = []
    for x, _ in fragments:
        puissances = [1]
        for _ in range(n - 1):
            puissances.append(gf_mult_independant(puissances[-1], x))
        base.append(puissances)
    m = bytearray(32)
    for k in range(32):
        matrice = [base[j][:] + [fragments[j][1][k]] for j in range(n)]
        for colonne in range(n):
            pivot = next((l for l in range(colonne, n)
                          if matrice[l][colonne] != 0), None)
            if pivot is None:
                raise AssertionError("système singulier — points dupliqués ?")
            matrice[colonne], matrice[pivot] = matrice[pivot], matrice[colonne]
            inv = gf_inv_independant(matrice[colonne][colonne])
            matrice[colonne] = [gf_mult_independant(v, inv)
                                for v in matrice[colonne]]
            for l in range(n):
                if l != colonne and matrice[l][colonne] != 0:
                    facteur = matrice[l][colonne]
                    matrice[l] = [v ^ gf_mult_independant(facteur, w)
                                  for v, w in zip(matrice[l],
                                                  matrice[colonne])]
        m[k] = matrice[0][n]     # coefficient constant après réduction identité
    return bytes(m)


# ---------------------------------------------------------------------------
# Laboratoire : tout se joue sous scripts/cf2-labo — JAMAIS dans .keys/
# ---------------------------------------------------------------------------

LABO = os.path.join(os.path.dirname(RACINE), "scripts", "cf2-labo")


def monter_labo(n=5, t=3, description="falsifiabilité D106", racine=None):
    """Conteneur + gardes + couche C + config de test -> dict d'état."""
    racine = racine or LABO
    shutil.rmtree(racine, ignore_errors=True)
    os.makedirs(racine)
    couche = os.path.join(racine, "couche-c")
    os.makedirs(couche)
    for nom in ("frag-loc.bin", "frag-con.bin", "frag-prf.bin"):
        with open(os.path.join(couche, nom), "wb") as f:
            f.write(secrets.token_bytes(64) + b"carte de laboratoire")
    conteneur = os.path.join(racine, "coffre.bin")
    racine_gardes = os.path.join(racine, "gardes")
    m = secrets.token_bytes(C.TAILLE_M)
    fragments = C.decouper(m, n, t)
    base = C.nouvelle_base(description)
    blob = C.construire_conteneur(
        json.dumps(base, ensure_ascii=False).encode("utf-8"), m,
        secrets.token_bytes(32), "2026-10-29T00:00:00Z", t, n)
    C._ecrire_atomique(conteneur, blob)
    sel_coffre = C._parser_entete(blob)["sel"].hex()
    chemins_gardes = []
    for x, frag in fragments:
        garde = os.path.join(racine_gardes, f"g{x}")
        os.makedirs(garde)
        with open(os.path.join(garde, f"fragment-{x}.cf2f"), "w",
                  encoding="ascii") as f:
            f.write(C.serialiser_fragment(x, frag, t, n, sel_coffre))
        chemins_gardes.append(garde)
    config = C.config_par_defaut(n, t, racine_gardes, conteneur)
    config["gardes"] = chemins_gardes
    config["couche_c"] = [couche]
    config["journal"] = os.path.join(racine, "journal.txt")
    config["pv_dir"] = os.path.join(racine, "pv")
    config["heartbeat"] = os.path.join(racine, "heartbeat.txt")
    config["liste_blanche"] = [r"[/]sentinelle_cf2\.py", r"[/]test_cf2\.py",
                               r"LECTEUR-BLANCHI-CF2"]
    chemin_config = os.path.join(racine, "config.json")
    C.ecrire_config(chemin_config, config)
    return {"m": m, "fragments": fragments, "base": base, "blob": blob,
            "conteneur": conteneur, "gardes": chemins_gardes,
            "racine_gardes": racine_gardes, "couche": couche,
            "config": config, "config_chemin": chemin_config,
            "sel": sel_coffre, "t": t, "n": n}


def fragments_fichiers(etat):
    return sorted(glob.glob(os.path.join(etat["racine_gardes"],
                                         "*", "fragment-*.cf2f")))


def empreintes_gardes(etat):
    return {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
            for p in fragments_fichiers(etat)}


def demarrer_sentinelle(etat):
    proc = subprocess.Popen(
        [sys.executable, os.path.join(RACINE, "v06", "sentinelle_cf2.py"),
         "demarrer", "--config", etat["config_chemin"]],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t0 = time.time()
    while time.time() - t0 < 5:
        if os.path.isfile(etat["config"]["heartbeat"]):
            try:
                with open(etat["config"]["heartbeat"]) as f:
                    if time.time() - json.load(f)["ts"] < 1.0:
                        return proc
            except (OSError, ValueError):
                pass
        time.sleep(0.05)
    proc.kill()
    raise AssertionError("sentinelle sans heart-beat frais après 5 s")


def tuer_sentinelle(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def lire_journal(etat):
    chemin = etat["config"]["journal"]
    if not os.path.isfile(chemin):
        return ""
    with open(chemin, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# T1 — Shamir contre témoin indépendant
# ---------------------------------------------------------------------------

def t1_shamir():
    print("T1 — Shamir contre témoin indépendant (somme de puissances, "
          "Gauss, 1 000 × C(5,3))")
    m = bytes(range(32))
    alea_fixe = bytes([0x5A, 0xC3])
    frags = C.decouper(m, 5, 3, alea=lambda k: alea_fixe)
    # attendu : évaluation DIRECTE en somme de puissances, corps indépendant
    attendu = []
    for x in range(1, 6):
        x2 = gf_mult_independant(x, x)
        octets = []
        for k in range(32):
            octets.append(m[k]
                          ^ gf_mult_independant(0x5A, x)
                          ^ gf_mult_independant(0xC3, x2))
        attendu.append(bytes(octets))
    verifie("kat-somme-de-puissances-5-fragments",
            [f for _, f in frags] == attendu)
    from itertools import combinations
    err = 0
    for _ in range(1000):
        secret = secrets.token_bytes(32)
        fs = C.decouper(secret, 5, 3)
        for c in combinations(range(5), 3):
            points = [fs[i] for i in c]
            if C.reconstituer(points) != secret:
                err += 1
    verifie("1000-secrets-x-10-combinaisons", err == 0, f"{err} erreurs")
    err_gauss = 0
    for _ in range(50):
        secret = secrets.token_bytes(32)
        fs = C.decouper(secret, 5, 3)
        if reconstituer_gauss(fs[:3]) != secret:
            err_gauss += 1
    verifie("gauss-independant-50-croisements", err_gauss == 0,
            f"{err_gauss} divergences")
    refuse("t1-refuse", C.decouper, m, 5, 1)
    refuse("t-sup-n-refuse", C.decouper, m, 2, 3)
    refuse("n-256-refuse", C.decouper, m, 256, 3)
    try:
        C.reconstituer([(1, b"\x00" * 32), (1, b"\x01" * 32)])
        verifie("x-duplique-refuse", False, "aucun refus")
    except C.ErreurCoffre as exc:
        verifie("x-duplique-refuse", "dupliqu" in str(exc), str(exc))
    refuse("fragment-court-refuse", C.reconstituer,
           [(1, b"\x00" * 31), (2, b"\x01" * 32)])


# ---------------------------------------------------------------------------
# T2 — sous T : informationnellement mort (aucune discrimination)
# ---------------------------------------------------------------------------

def t2_informationnel():
    print("T2 — sous le seuil : sécurité INFORMATIONNELLE (tout M′ "
          "compatible, verif nomme le mensonge)")
    m_reel = secrets.token_bytes(32)
    sel = secrets.token_bytes(32)
    blob = C.construire_conteneur(b"charge utile", m_reel, sel,
                                  "2026-10-29T00:00:00Z", 3, 5)
    f1, f2 = C.decouper(m_reel, 5, 3)[:2]
    x1, y1 = f1
    x2, y2 = f2
    # poids de Lagrange pour les points (x1,y1),(x2,y2),(3,y3)
    x3 = 3
    poids = {}
    for j, xj in ((0, x1), (1, x2), (2, x3)):
        p = 1
        for m_, xm in ((0, x1), (1, x2), (2, x3)):
            if m_ == j:
                continue
            p = gf_mult_independant(
                p, gf_mult_independant(xm, gf_inv_independant(xj ^ xm)))
        poids[j] = p

    def forger_troisieme(cible: bytes) -> bytes:
        """y3 tel que L(0) == cible, À PARTIR des DEUX fragments réels."""
        octets = []
        w0, w1, w2 = poids[0], poids[1], poids[2]
        inv_w2 = gf_inv_independant(w2)
        for k in range(32):
            reste = (cible[k] ^ gf_mult_independant(y1[k], w0)
                     ^ gf_mult_independant(y2[k], w1))
            octets.append(gf_mult_independant(reste, inv_w2))
        return bytes(octets)

    m_a, m_b = secrets.token_bytes(32), secrets.token_bytes(32)
    y3_a, y3_b = forger_troisieme(m_a), forger_troisieme(m_b)
    recon_a = C.reconstituer([f1, f2, (3, y3_a)])
    recon_b = C.reconstituer([f1, f2, (3, y3_b)])
    verifie("m-prime-a-compatible", recon_a == m_a,
            "la récomposition a divergé — la forge est fausse")
    verifie("m-prime-b-compatible", recon_b == m_b,
            "idem pour le second candidat")
    refuse("verif-nomme-le-mensonge-a", C.dechiffrer, blob, m_a)
    refuse("verif-nomme-le-mensonge-b", C.dechiffrer, blob, m_b)
    verifie("m-reel-distinct-des-forges",
            m_a != m_reel and m_b != m_reel and m_a != m_b,
            "candidats non distincts — test vide")


# ---------------------------------------------------------------------------
# T3 — conteneur fail-closed
# ---------------------------------------------------------------------------

def t3_conteneur():
    print("T3 — conteneur : round-trip + falsifications NOMMÉES")
    etat = monter_labo()
    base, _, mram, _ = C.deverrouiller(etat["conteneur"], etat["gardes"])
    verifie("roundtrip-base", base == etat["base"])
    C._effacer(mram)
    with open(etat["conteneur"], "rb") as f:
        blob = f.read()
    ent = C._parser_entete(blob)
    verifie("entete-champs", (ent["t"], ent["n"]) == (3, 5)
            and ent["date"] == "2026-10-29T00:00:00Z")
    mauvais_m = bytearray(etat["m"])
    mauvais_m[7] ^= 0x40
    refuse("verif-cle-fausse-nomme", C.dechiffrer, blob, bytes(mauvais_m))
    tampon = bytearray(blob)
    tampon[-1] ^= 0x01
    refuse("aead-chiffretexte-altéré", C.dechiffrer, bytes(tampon), etat["m"])
    tampon = bytearray(blob)
    tampon[20] ^= 0x01                        # champ hachage de l'en-tête
    refuse("liste-blanche-algorithmes", C.dechiffrer, bytes(tampon), etat["m"])
    refuse("conteneur-tronqué", C.dechiffrer, blob[:60], etat["m"])
    refuse("magic-faux", C.dechiffrer, b"XRIADE-CF2" + blob[10:], etat["m"])
    # falsification D'UN OCTET de fragment — la custodie répartie : un
    # fautif est NOMMÉ et ÉCARTÉ, les quatre valides demeurent (spec § 5)
    def fausser(indice_garde: int) -> None:
        chemin = os.path.join(etat["gardes"][indice_garde],
                              f"fragment-{indice_garde + 1}.cf2f")
        with open(chemin, encoding="ascii") as f:
            texte = f.read()
        lignes = texte.splitlines()
        hexa = [l for l in lignes if l.startswith("fragment:")][0]
        faux = bytearray(bytes.fromhex(hexa.split()[1]))
        faux[0] ^= 1
        lignes = [f"fragment: {bytes(faux).hex()}"
                  if l.startswith("fragment:") else l for l in lignes]
        with open(chemin, "w", encoding="ascii") as f:
            f.write("\n".join(lignes) + "\n")

    fausser(0)
    import io
    import contextlib
    tampon_err = io.StringIO()
    with contextlib.redirect_stderr(tampon_err):
        base4, _, mram4, _ = C.deverrouiller(etat["conteneur"], etat["gardes"])
    verifie("un-fautif-nommé-les-autres-tiennent",
            base4 == etat["base"]
            and "tag du fragment x=1 INVALIDE" in tampon_err.getvalue())
    C._effacer(mram4)
    fausser(1)
    fausser(2)
    refuse("trois-fautifs-coffre-refusé", C.deverrouiller, etat["conteneur"],
           etat["gardes"])
    shutil.rmtree(LABO, ignore_errors=True)


# ---------------------------------------------------------------------------
# T4 — fausses alertes NULLES
# ---------------------------------------------------------------------------

def t4_fausses_alertes():
    print("T4 — fausses alertes nulles : lecteur BLANCHI, accès par attributs")
    etat = monter_labo()
    empreintes_avant = empreintes_gardes(etat)
    proc = demarrer_sentinelle(etat)
    carte = os.path.join(etat["couche"], "frag-loc.bin")
    # même BINAIRE que l'attaquant (python3), seule la ligne de commande
    # porte le marqueur blanchi — la liste juge la COMMANDE, pas l'image
    lecteur = subprocess.Popen([sys.executable, "-c",
        "# LECTEUR-BLANCHI-CF2\n"
        f"import time; f=open({carte!r},'rb'); f.read(); time.sleep(1.5)"])
    lecteur.wait()
    time.sleep(0.6)                            # laisse le balayage s'exprimer
    journal = lire_journal(etat)
    verifie("lecture-blanchie-journalisée", "BLANCHIE" in journal)
    verifie("rien-ne-brûle-blanchi",
            empreintes_gardes(etat) == empreintes_avant
            and not glob.glob(os.path.join(LABO, "pv", "*.txt")))
    # accès par attributs SEULS : stat + listage — aucun signal
    attribut = subprocess.run([sys.executable, "-c",
        f"import os; os.stat({carte!r}); os.listdir({etat['couche']!r}); "
        f"os.stat({carte!r})"], capture_output=True, timeout=10)
    verifie("attributs-silencieux", attribut.returncode == 0)
    time.sleep(0.6)
    verifie("rien-ne-brûle-attributs",
            empreintes_gardes(etat) == empreintes_avant
            and "non attribu" not in lire_journal(etat).lower())
    tuer_sentinelle(proc)
    shutil.rmtree(LABO, ignore_errors=True)


# ---------------------------------------------------------------------------
# F1 — exfiltration simulée : le critère de sortie D86, complet
# ---------------------------------------------------------------------------

BORNE_LATENCE = 2.0     # consigne (spec § 13 : mesurée et bornée)


def f1_exfiltration():
    print("F1 — exfiltration simulée : brûlage NOMMÉ, mort, latence, relève")
    etat = monter_labo()
    # copies hors-ligne de TROIS fragments (= le seuil — spec § 5)
    copies = []
    for x in (3, 4, 5):
        source = os.path.join(etat["gardes"][x - 1], f"fragment-{x}.cf2f")
        copie = os.path.join(LABO, f"hors-ligne-{x}.txt")
        shutil.copy2(source, copie)
        copies.append(copie)
    proc = demarrer_sentinelle(etat)
    carte = os.path.join(etat["couche"], "frag-loc.bin")
    marqueur = os.path.join(LABO, "t0.txt")
    attaquant = subprocess.Popen([sys.executable, "-c",
        f"import time, os; open({marqueur!r},'w').write('t0'); "
        f"f=open({carte!r},'rb'); f.read(); time.sleep(1.5)"])
    t0 = None
    fin_attente = time.time() + 5
    while t0 is None and time.time() < fin_attente:
        if os.path.isfile(marqueur):
            t0 = time.time()
            break
        time.sleep(0.005)
    brule_a, latence = None, None
    while time.time() - (t0 or time.time()) < 8:
        if not fragments_fichiers(etat):
            brule_a = time.time()
            latence = brule_a - t0
            break
        time.sleep(0.02)
    attaquant.wait()
    verifie("fragments-détruits", brule_a is not None, "pas de brûlage observé")
    verifie("latence-bornée", latence is not None and latence < BORNE_LATENCE,
            f"latence {latence}")
    pvs = glob.glob(os.path.join(LABO, "pv", "*.txt"))
    verifie("pv-écrit", len(pvs) == 1, f"{len(pvs)} PV")
    if pvs:
        with open(pvs[0], encoding="utf-8") as f:
            pv = f.read()
        verifie("pv-déclencheur-nommé", "pid " in pv and "frag-loc.bin" in pv
                and "hors liste blanche" in pv)
        verifie("pv-fragments-détaillés", pv.count("DETRUIT") == 5)
    refuse("coffre-mort-refus-nommé", C.deverrouiller, etat["conteneur"],
           etat["gardes"])
    # RELÈVE : les T copies franchissent le seuil -> vie (le cycle complet)
    C.restaurer(etat["config"], copies)
    base, _, mram, _ = C.deverrouiller(etat["conteneur"], etat["gardes"])
    verifie("relève-restaure-la-vie", base == etat["base"])
    C._effacer(mram)
    tuer_sentinelle(proc)
    shutil.rmtree(LABO, ignore_errors=True)


# ---------------------------------------------------------------------------
# F2 — remise douteuse : R I E N n'est écrit
# ---------------------------------------------------------------------------

def f2_atomicite():
    print("F2 — remise douteuse refusée SANS ÉCRIRE (atomicité)")
    etat = monter_labo()
    empreintes_avant = empreintes_gardes(etat)
    # un fragment CORROMPU au milieu d'un lot valide
    corrompu = os.path.join(LABO, "corrompu.txt")
    with open(os.path.join(etat["gardes"][3], "fragment-4.cf2f"),
              encoding="ascii") as f:
        texte = f.read()
    hexa = [l for l in texte.splitlines() if l.startswith("fragment:")][0]
    faux = bytearray(bytes.fromhex(hexa.split()[1]))
    faux[9] ^= 0xFF
    with open(corrompu, "w", encoding="ascii") as f:
        f.write(texte.replace(hexa, f"fragment: {bytes(faux).hex()}"))
    refuse("lot-corrompu-refusé", C.restaurer, etat["config"],
           [os.path.join(etat["gardes"][2], "fragment-3.cf2f"), corrompu])
    verifie("gardes-intactes-corrompu", empreintes_gardes(etat)
            == empreintes_avant)
    # indice DÉJÀ présent
    refuse("indice-déjà-présent-refusé", C.restaurer, etat["config"],
           [os.path.join(etat["gardes"][0], "fragment-1.cf2f")])
    # fragment d'un AUTRE coffre (labo séparé — le montage ne détruit pas
    # le laboratoire en cours)
    autre = monter_labo(racine=LABO + "-autre")
    refuse("fragment-d-autre-coffre-refusé", C.restaurer, etat["config"],
           [os.path.join(autre["gardes"][4], "fragment-5.cf2f")])
    verifie("gardes-intactes-tout-court", empreintes_gardes(etat)
            == empreintes_avant)
    shutil.rmtree(LABO, ignore_errors=True)
    shutil.rmtree(LABO + "-autre", ignore_errors=True)


# ---------------------------------------------------------------------------
# T5 — santé de la sentinelle
# ---------------------------------------------------------------------------

def t5_sante():
    print("T5 — heart-beat : VIVANTE fraîche, MORT visible")
    etat = monter_labo()
    proc = demarrer_sentinelle(etat)
    vivante = subprocess.run(
        [sys.executable, os.path.join(RACINE, "v06", "sentinelle_cf2.py"),
         "sante", "--config", etat["config_chemin"], "--age-max", "1.0"],
        capture_output=True, text=True, timeout=10)
    verifie("sante-vivante-exit-0", vivante.returncode == 0
            and "VIVANTE" in vivante.stdout, vivante.stdout.strip())
    tuer_sentinelle(proc)
    time.sleep(1.3)                            # heart-beat périmé
    morte = subprocess.run(
        [sys.executable, os.path.join(RACINE, "v06", "sentinelle_cf2.py"),
         "sante", "--config", etat["config_chemin"], "--age-max", "1.0"],
        capture_output=True, text=True, timeout=10)
    verifie("sante-morte-exit-1", morte.returncode == 1
            and "MORTE" in morte.stdout, morte.stdout.strip())
    shutil.rmtree(LABO, ignore_errors=True)


# ---------------------------------------------------------------------------
# T6 — D119 : Windows refuse os.open() sur un dossier — l'écriture
# atomique survit au crash du terrain v1.8 (« CF2 — migrer » mourait sur
# .keys/, PermissionError errno 13 au rapport de cérémonie)
# ---------------------------------------------------------------------------

def t6_windows():
    print("T6 — D119 : Windows refuse os.open(dossier), l'atome tient")
    import tempfile
    import unittest.mock as mock
    vrai_open = os.open

    def windows_open(chemin, flags, *a, **k):
        # simulation FIDÈLE du terrain : un DOSSIER lève PermissionError 13
        if os.path.isdir(chemin):
            raise PermissionError(
                13, "Permission denied (dossier — simulation Windows "
                "D119)", chemin)
        return vrai_open(chemin, flags, *a, **k)

    with tempfile.TemporaryDirectory(prefix="cf2-t6-") as tmp:
        # (1) sous 'nt', le fsync de dossier ne touche JAMAIS os.open
        appels = []

        def espion(chemin, flags, *a, **k):
            if os.path.isdir(chemin):
                appels.append(chemin)
            return vrai_open(chemin, flags, *a, **k)

        os.open = espion
        try:
            with mock.patch("os.name", "nt"):
                C._fsync_repertoire(tmp)
        finally:
            os.open = vrai_open
        verifie("nt-fsync-dossier-sans-os-open", not appels, str(appels))
        # (2) le crash du terrain, reproduit : PermissionError 13 sur le
        # dossier — _ecrire_atomique écrit quand même, contenu exact
        cible = os.path.join(tmp, "sous-dossier", "coffre_cf2.bin")
        donnees = secrets.token_bytes(64)
        os.open = windows_open
        try:
            C._ecrire_atomique(cible, donnees)
            crash = None
        except PermissionError as exc:
            crash = str(exc)
        finally:
            os.open = vrai_open
        verifie("ecrire-atomique-survit-au-refus-windows",
                crash is None and os.path.isfile(cible)
                and open(cible, "rb").read() == donnees
                and not os.path.exists(cible + ".tmp"), crash or "")
        # (3) POSIX : répertoire impossible à ouvrir = toléré (le replace
        # est déjà fait — la durabilité du dossier est mieux-disante)
        os.open = windows_open
        try:
            C._fsync_repertoire(tmp)
            leve = None
        except PermissionError as exc:
            leve = str(exc)
        finally:
            os.open = vrai_open
        verifie("posix-ouverture-dossier-impossible-toleree",
                leve is None, leve or "")
        # (4) D120 collatéral (démo) : un chemin NU — sans composant de
        # dossier — donnait os.makedirs('') -> traceback anonyme ; la
        # garde nomme le cas et l'atome tient
        cwd_avant = os.getcwd()
        os.chdir(tmp)
        try:
            C._ecrire_atomique("fichier-nu.bin", donnees)
        finally:
            os.chdir(cwd_avant)
        nu = os.path.join(tmp, "fichier-nu.bin")
        verifie("ecrire-atomique-chemin-nu",
                os.path.isfile(nu) and open(nu, "rb").read() == donnees
                and not os.path.exists(nu + ".tmp"))


# ---------------------------------------------------------------------------
# T7 — D120 : la PORTE de sentinelle — aucun déverrouillage sans témoin
# ---------------------------------------------------------------------------

def t7_porte():
    print("T7 — D120 : la porte — refus NOMMÉ sans sentinelle, VERT avec, "
          "morte visible, ère sans moteur, heart-beat falsifiable CONSIGNÉ")
    etat = monter_labo()
    etat["config"]["heartbeat_age_max"] = 1.0
    C.ecrire_config(etat["config_chemin"], etat["config"])
    empreintes_avant = empreintes_gardes(etat)

    def cli(*mots):
        return subprocess.run(
            [sys.executable, os.path.join(RACINE, "v06", "coffre_cf2.py"),
             *mots, "--config", etat["config_chemin"]],
            capture_output=True, text=True, timeout=60)

    # (1) exiger=true, sentinelle ABSENTE : refus NOMMÉ + parade + journal,
    #     et le refus ne touche RIEN (gardes octet pour octet)
    r1 = cli("verifier")
    verifie("porte-refus-nommé-avec-parade",
            r1.returncode == 1 and "NON VIVANTE" in r1.stderr
            and "demarrer" in r1.stderr, r1.stderr.strip()[:200])
    verifie("porte-refus-journalisé",
            "PORTE" in lire_journal(etat)
            and "REFUSÉ" in lire_journal(etat))
    verifie("porte-refus-ne-touche-rien",
            empreintes_gardes(etat) == empreintes_avant)
    # (2) sentinelle VIVANTE : le MÊME verifier passe VERT (la chaîne
    #     complète : porte -> fragments -> M -> verif -> AEAD)
    proc = demarrer_sentinelle(etat)
    r2 = cli("verifier")
    verifie("porte-sentinelle-vivante-verifier-vert",
            r2.returncode == 0 and "verifier : VERT" in r2.stdout,
            (r2.stdout + r2.stderr).strip()[:200])
    tuer_sentinelle(proc)
    time.sleep(1.3)                            # heart-beat périmé (borne 1.0)
    # (3) sentinelle TUÉE : la mort est VISIBLE — refus NOMMÉ « MORTE »
    r3 = cli("verifier")
    verifie("porte-sentinelle-morte-refus-nommé",
            r3.returncode == 1 and "MORTE" in r3.stderr
            and "borne 1 s" in r3.stderr, r3.stderr.strip()[:200])
    # (4) l'ère SANS moteur (Windows : exigence consignée spec § 9) :
    #     exiger=false → la porte AVERTIT fort et PASSE (jamais un refus
    #     qui scellerait le coffre derrière un moteur non livré)
    etat["config"]["exiger_sentinelle"] = False
    C.ecrire_config(etat["config_chemin"], etat["config"])
    r4 = cli("verifier")
    verifie("porte-ère-sans-moteur-avertit-et-passe",
            r4.returncode == 0 and "SANS sentinelle" in r4.stderr
            and "verifier : VERT" in r4.stdout,
            (r4.stdout + r4.stderr).strip()[:200])
    # (5) la BORNE CONSIGNÉE (D120) : le heart-beat est falsifiable — un
    #     ts fraîchement forgé ouvre la porte sans sentinelle. La porte
    #     est une exigence de CÉRÉMONIE, pas une barrière cryptographique
    #     (la sécurité DURE reste Shamir + ACL + brûlage). L'aveu EST le
    #     contrôle : prouver la limite, pas la cacher.
    etat["config"]["exiger_sentinelle"] = True
    C.ecrire_config(etat["config_chemin"], etat["config"])
    with open(etat["config"]["heartbeat"], "w", encoding="utf-8") as f:
        json.dump({"ts": time.time()}, f)
    r5 = cli("verifier")
    verifie("porte-heartbeat-falsifiable-borne-consignée",
            r5.returncode == 0 and "verifier : VERT" in r5.stdout,
            (r5.stdout + r5.stderr).strip()[:200])
    shutil.rmtree(LABO, ignore_errors=True)


# ---------------------------------------------------------------------------
# X8 — les coffres réels ne sont JAMAIS touchés
# ---------------------------------------------------------------------------

def _md5_si_present(chemin):
    """md5 du coffre réel, None si ABSENT : le coffre réel CF1 ne vit que
    sur la machine du développeur (.keys/ est gitignore) — un clone frais
    ou un kit du Drive n'en porte PAS. L'absence est un état NOMMÉ, jamais
    un crash muet (leçon du verdict CF2 à froid, D117)."""
    if not os.path.isfile(chemin):
        return None
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


def x8_coffres_reels():
    print("X8 — coffres réels intacts")
    chemin_cf1 = os.path.join(RACINE, ".keys", "coffre_fort.bin")
    md5_avant = _md5_si_present(chemin_cf1)
    yield_verdict = not os.path.exists(C.CHEMIN_CONTENEUR_DEFAUT)
    verifie("aucun-coffre-cf2-réel-créé", yield_verdict,
            f"{C.CHEMIN_CONTENEUR_DEFAUT} existe")
    md5_apres = _md5_si_present(chemin_cf1)
    if md5_avant is None:
        verifie("coffre-cf1-réel-absent-nomme-et-subistant",
                md5_apres is None,
                "le coffre réel CF1 était ABSENT (clone frais / kit) : la "
                "suite n'en crée JAMAIS — l'absence doit subsister")
    else:
        verifie("coffre-cf1-réel-inchangé", md5_avant == md5_apres)


def main() -> int:
    chemin_reel = os.path.join(RACINE, ".keys", "coffre_fort.bin")
    empreinte_avant = _md5_si_present(chemin_reel)
    t1_shamir()
    t2_informationnel()
    t3_conteneur()
    t4_fausses_alertes()
    f1_exfiltration()
    f2_atomicite()
    t5_sante()
    t6_windows()
    t7_porte()
    x8_coffres_reels()
    empreinte_apres = _md5_si_present(chemin_reel)
    if empreinte_avant is None:
        verifie("md5-coffre-réel-absent-avant-et-après",
                empreinte_apres is None,
                "absent avant la suite, PRÉSENT après : la suite l'a créé !")
    else:
        verifie("md5-coffre-réel-pre-post-suite",
                empreinte_avant == empreinte_apres)
    print(f"\n[test-cf2] FALSIFIABILITÉ : {len(PASSES)} PASS, "
          f"{len(ECHECS)} ÉCHEC(s)")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
