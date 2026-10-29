#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_ceremonie_gui.py — falsifiabilité du MAÎTRE DE CÉRÉMONIE (D107,
compléments correctif D109, phrase personnelle D110).

Le GUI est un HABIT : ce qui doit être prouvé, c'est son contrôleur —
la couche qui décide, écrit ou refuse. Ce test l'attaque :

  T1   l'Ed25519 embarqué est la COPIE CONFORME de ceremonie_hors_ligne.py
       (graines aléatoires : clé publique, signature, vérification — plus
       interop avec l'implémentation auditée « cryptography » si présente) ;
  T2   generer : fichiers conformes, 0600 (POSIX), la graine NE FUITE PAS
       dans le texte retourné (le journal de la GUI reste muet) ;
  T3   signer : remise auto-vérifiée ; un octet d'intention muté change
       tout (les signatures ne correspondent plus) ;
  T4   verifier : VERT sur remise valable, ÉCHEC nommé sur signature
       mutée / balise divergente / arbre manquant ;
  T5   labo CF2 complet (répertoire temporaire, AUCUN coffre réel touché) :
       feuille d'export, CONTRÔLE DE RELECTURE vert, copie corrompue
       attrapée, copie FALSIFIÉE-COHÉRENTE (tag reforgé) attrapée par
       l'AEAD, sous-seuil refusé, doublon refusé ;
  T6   liste blanche : lecture/écriture atomique, motif invalide refusé ;
  T7   le relais CLI : verdict capturé, code de sortie honoré ;
  T8   phrase personnelle CF1 (D110) : alphanumérique exigé, faute NOMMÉE
       par position SANS divulguer le caractère, plancher 8 refusé,
       10 000 caractères acceptés (AUCUN plafond) ; bout en bout PAR LE
       RELAIS GUI : coffre labo, changer-phrase, ancienne inopérante,
       la vôtre ouvre, entrées intactes, phrase vide refusée SANS
       lancement ;
  F1   fail-closed : autotest muté => génération/signation refusées ;
       clé absente => échec nommé ; phrase vide => refus AVANT tout
       lancement ; BRÛLER sans confirmation => le CLI refuse et les
       fragments SURVIVENT ; après brûlage réel (labo), les copies
       hors-ligne relèvent le conteneur survivant (contrôle VERT) ;
  X1   import headless (aucune fenêtre créée) + selftest embarqué vert ;
  X2   cohérence des attributs (régression D109) : AST — tout self.X lu
       existe (méthode ou champ assigné), toute traversée self.app.X
       pointe sur du réel Application, et demarrer_gui ne référence que
       des attributs existants (le bogue original appelait app.mainloop()
       alors que le Tk racine vit dans app.racine ; la fumée pilotait
       Application en direct et n'exerçait jamais cette ligne — le trou
       est bouché ici, headless, sur TOUTE la classe).

Style maison : tout sur la sortie, échec nommé, exit code 0/1.
"""

import json
import os
import re
import secrets
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RACINE)

import v06.ceremonie_gui as gui          # noqa: E402
import v06.coffre_cf2 as cf2             # noqa: E402
import coffre_fort as cf1                 # noqa: E402 (relais au_racine)

try:
    import v06.ceremonie_hors_ligne as ref_hl
except ImportError:
    ref_hl = None

PASSES, ECHECS = [], []


def verifie(nom, condition, detail=""):
    ok = bool(condition)
    (PASSES if ok else ECHECS).append(nom if ok else f"{nom} ({detail})")
    print(f"  {'PASS' if ok else 'ÉCHEC'} {nom}"
          + (f" — {detail}" if detail and not ok else ""))


def refuse(nom, fonction, *a, **k):
    """PASS ssi la fonction REFUSE (ErreurCeremonie nommée)."""
    try:
        fonction(*a, **k)
        verifie(nom, False, "aucun refus levé")
    except gui.ErreurCeremonie as exc:
        verifie(nom, str(exc) != "", str(exc))


# ---------------------------------------------------------------------------
# Labo CF2 (tout en temporaire — x8_coffres_reels protège les coffres réels)
# ---------------------------------------------------------------------------

def monter_labo(rep):
    m = secrets.token_bytes(cf2.TAILLE_M)
    frags = cf2.decouper(m, 5, 3)
    base = cf2.nouvelle_base("labo test-ceremonie-gui")
    base["projets"]["labo"] = {
        "description": "entrée témoin",
        "entrees": [{"etiquette": "temoin", "octets": secrets.token_hex(8)}],
    }
    sel = secrets.token_bytes(32)
    blob = cf2.construire_conteneur(
        json.dumps(base, ensure_ascii=False).encode("utf-8"), m, sel,
        cf2._date_utc(), 3, 5)
    conteneur = os.path.join(rep, "coffre.bin")
    cf2._ecrire_atomique(conteneur, blob)
    sel_coffre = cf2._parser_entete(blob)["sel"].hex()
    gardes = [os.path.join(rep, f"g{i}") for i in range(1, 6)]
    for x, frag in frags:
        os.makedirs(gardes[x - 1], exist_ok=True)
        with open(os.path.join(gardes[x - 1], f"fragment-{x}.cf2f"), "w",
                  encoding="ascii") as f:
            f.write(cf2.serialiser_fragment(x, frag, 3, 5, sel_coffre))
    config = cf2.config_par_defaut(5, 3, os.path.join(rep, "gardes"), conteneur)
    config["gardes"] = gardes
    config["journal"] = os.path.join(rep, "journal.txt")
    config["pv_dir"] = os.path.join(rep, "pv")
    config["heartbeat"] = os.path.join(rep, "heartbeat.txt")
    config_chemin = os.path.join(rep, "config_cf2.json")
    cf2.ecrire_config(config_chemin, config)
    return {"config": config_chemin, "conteneur": conteneur,
            "gardes": gardes, "sel_coffre": sel_coffre}


def extraire_blocs(feuille):
    """Les blocs fragment (de la magic à « tag: ») d'une feuille exportée."""
    with open(feuille, "r", encoding="utf-8") as f:
        texte = f.read()
    return re.findall(r"TRIADE-CF2-FRAG.*?tag: [0-9a-f]{16}\n", texte,
                      re.DOTALL)


# ---------------------------------------------------------------------------
# T1 — Ed25519 embarqué : copie conforme + interop
# ---------------------------------------------------------------------------
def t1_ed25519():
    print("T1 — Ed25519 embarqué (copie conforme, attestée)")
    graines = [secrets.token_bytes(32) for _ in range(6)]
    ok = True
    for g in graines:
        msg = secrets.token_bytes(37)
        ok = ok and (gui.cle_publique_depuis_graine(g)
                     == gui.cle_publique_depuis_graine(g))
        sig = gui.signer_ed25519(g, msg)
        ok = ok and gui.verifier_ed25519(gui.cle_publique_depuis_graine(g),
                                         msg, sig)
        ok = ok and not gui.verifier_ed25519(
            gui.cle_publique_depuis_graine(g), msg[:-1] + bytes([msg[-1] ^ 1]),
            sig)
    verifie("t1-determinisme-mutation", ok)
    if ref_hl is not None:
        conforme = True
        for g in graines:
            msg = secrets.token_bytes(41)
            conforme = conforme and (
                gui.cle_publique_depuis_graine(g)
                == ref_hl.cle_publique_depuis_graine(g)
                and gui.signer_ed25519(g, msg) == ref_hl.signer_ed25519(g, msg)
                and gui.verifier_ed25519(gui.cle_publique_depuis_graine(g),
                                         msg, ref_hl.signer_ed25519(g, msg)))
        verifie("t1-copie-conforme-source-reference", conforme)
    else:
        verifie("t1-copie-conforme-source-reference", False,
                "ceremonie_hors_ligne.py introuvable")
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PrivateKey, Ed25519PublicKey)
        g, msg = graines[0], secrets.token_bytes(53)
        sig_ref = Ed25519PrivateKey.from_private_bytes(g).sign(msg)
        verifie("t1-interop-cryptography",
                gui.signer_ed25519(g, msg) == sig_ref
                and Ed25519PublicKey.from_public_bytes(
                    gui.cle_publique_depuis_graine(g)).verify(sig_ref, msg)
                is None)
    except ImportError:
        print("  (cryptography absente : interop sautée — vecteurs RFC "
              "suffisent ici)")
        verifie("t1-interop-cryptography", True, "(absente — sautée)")


# ---------------------------------------------------------------------------
# T2/T3/T4 — cérémonie de la clé I (profil hors-ligne)
# ---------------------------------------------------------------------------
def t234_cle_i(rep):
    print("T2 — generer (fichiers, garde, journal muet)")
    privee = os.path.join(rep, "cle-I-privee.txt")
    publique = os.path.join(rep, "cle-publique-I.txt")
    texte_gen = gui.hl_generer(privee, publique)
    verifie("t2-fichiers-ecrits", os.path.isfile(privee)
            and os.path.isfile(publique))
    if os.name == "posix":
        verifie("t2-permissions-0600",
                os.stat(privee).st_mode & 0o777 == 0o600,
                oct(os.stat(privee).st_mode & 0o777))
    graine = gui._lire_graine_privee(privee)
    verifie("t2-graine-absente-du-texte-retourne",
            graine.hex() not in texte_gen, "FUITE journal")

    print("T3 — signer (auto-vérification, sensibilité de l'intention)")
    a_signer = os.path.join(rep, "a-signer.txt")
    empreintes = [secrets.token_hex(32) for _ in range(3)]
    with open(a_signer, "w", encoding="utf-8") as f:
        for arbre, balise, emp in zip(("m0/test", "m1/test", "v06/test"),
                                      ("ALPHA", "BETA", "GAMMA"), empreintes):
            f.write(f"{arbre} {balise} {emp}\n")
    signatures = os.path.join(rep, "signatures-I.txt")
    gui.hl_signer(a_signer, privee, signatures)
    with open(signatures, "r", encoding="utf-8") as f:
        lignes = [l for l in f.read().splitlines() if l.strip()]
    verifie("t3-trois-signatures-128hex", len(lignes) == 3 and all(
        len(l.split()[2]) == 128 for l in lignes))
    # un octet d'intention muté => les signatures ne correspondent plus
    fautif = os.path.join(rep, "a-signer-mute.txt")
    emp_mute = empreintes[0][:62] + ("0" if empreintes[0][62] != "0"
                                     else "1") + empreintes[0][63:]
    with open(fautif, "w", encoding="utf-8") as f:
        f.write(f"m0/test ALPHA {emp_mute}\n"
                + "\n".join(f"{a} {b} {e}" for a, b, e in zip(
                    ("m1/test", "v06/test"), ("BETA", "GAMMA"),
                    empreintes[1:])) + "\n")
    ok_mut, _ = gui.hl_verifier(fautif, signatures, publique)
    verifie("t3-intention-mutee-rejetee", not ok_mut)

    print("T4 — verifier (falsifications nommées)")
    ok, texte = gui.hl_verifier(a_signer, signatures, publique)
    verifie("t4-remise-valable-vert", ok, texte)
    sig_mutee = os.path.join(rep, "signatures-mutees.txt")
    prem = lignes[0].split()
    prem[2] = ("0" if prem[2][0] != "0" else "1") + prem[2][1:]
    with open(sig_mutee, "w", encoding="utf-8") as f:
        f.write(" ".join(prem) + "\n" + "\n".join(lignes[1:]) + "\n")
    ok_m, texte_m = gui.hl_verifier(a_signer, sig_mutee, publique)
    verifie("t4-signature-mutee-rejetee", not ok_m
            and "INVALIDE" in texte_m, texte_m)
    balise_mute = os.path.join(rep, "signatures-balise.txt")
    prem = lignes[0].split()
    prem[1] = "OMEGA"
    with open(balise_mute, "w", encoding="utf-8") as f:
        f.write(" ".join(prem) + "\n")
    ok_b, texte_b = gui.hl_verifier(a_signer, balise_mute, publique)
    verifie("t4-balise-divergente-rejetee", not ok_b
            and "balise" in texte_b, texte_b)
    incomplet = os.path.join(rep, "signatures-incompletes.txt")
    with open(incomplet, "w", encoding="utf-8") as f:
        f.write(lignes[0] + "\n")
    ok_i, texte_i = gui.hl_verifier(a_signer, incomplet, publique)
    verifie("t4-arbre-manquant-rejetee", not ok_i
            and "sans signature" in texte_i, texte_i)


# ---------------------------------------------------------------------------
# T5/T6/T7/F1 — labo CF2 : feuille, contrôle de relecture, liste blanche,
# relais CLI, fail-closed, brûlage et relève
# ---------------------------------------------------------------------------
def t567f1(rep):
    print("T5 — labo CF2 : feuille + contrôle de relecture")
    labo = monter_labo(rep)
    cfg = labo["config"]
    feuille = os.path.join(rep, "fragments-cf2.txt")
    gui.exporter_feuille(cfg, feuille)
    blocs = extraire_blocs(feuille)
    verifie("t5-feuille-trois-blocs", len(blocs) == 3, f"{len(blocs)} blocs")
    copies = []
    for i, bloc in enumerate(blocs, 1):
        chemin = os.path.join(rep, f"copie-{i}.txt")
        with open(chemin, "w", encoding="ascii") as f:
            f.write(bloc)
        copies.append(chemin)
    ok, texte = gui.controle_lecture(cfg, copies)
    verifie("t5-relecture-verte", ok, texte)
    # copie corrompue (hex muté => tag invalide) : attrapée nommément
    corrompue = os.path.join(rep, "copie-corrompue.txt")
    with open(copies[0], "r", encoding="ascii") as f:
        contenu = f.read()
    hexa = re.search(r"fragment: ([0-9a-f]{64})", contenu).group(1)
    mauvais = ("0" if hexa[0] != "0" else "1") + hexa[1:]
    _ecrire(corrompue, contenu.replace(hexa, mauvais))
    refuse("t5-copie-corrompue-attrapee", gui.controle_lecture,
           cfg, [corrompue] + copies[1:])
    # falsification COHÉRENTE : fragment muté ET tag reforgé — seule l'AEAD
    # peut l'attraper (reconstruction => mauvaise clé => déchiffrement échoue)
    x = int(re.search(r"x: (\d+)", contenu).group(1))
    frag_mute = bytes.fromhex(mauvais)
    sel_c = re.search(r"coffre: ([0-9a-f]{64})", contenu).group(1)
    faux = cf2.serialiser_fragment(x, frag_mute, 3, 5, sel_c)
    coherente = os.path.join(rep, "copie-faussifiee.txt")
    with open(coherente, "w", encoding="ascii") as f:
        f.write(faux)
    ok_c, texte_c = gui.controle_lecture(cfg, [coherente] + copies[1:])
    verifie("t5-falsification-coherente-attrapee-par-aead", not ok_c, texte_c)
    refuse("t5-sous-seuil-deux-copies-refuse", gui.controle_lecture,
           cfg, copies[:2])
    refuse("t5-doublon-refuse", gui.controle_lecture,
           cfg, [copies[0], copies[0], copies[1]])

    print("T6 — liste blanche (atomique, motifs)")
    motifs = gui.liste_blanche_lire(cfg)
    verifie("t6-defauts-presents", len(motifs) >= 5
            and any("build_m" in m for m in motifs))
    gui.liste_blanche_ecrire(cfg, motifs + [r"[/]code\.exe"])
    relu = gui.liste_blanche_lire(cfg)
    verifie("t6-ecriture-relue", r"[/]code\.exe" in relu
            and len(relu) == len(motifs) + 1)
    verifie("t6-motif-invalide-refuse", not gui.motif_valide("("))
    verifie("t6-motif-teste", gui.motif_teste(r"[/]code\.exe",
                                              "/usr/bin/code.exe a.txt")
            and not gui.motif_teste(r"[/]code\.exe", "/bin/cat a.txt"))

    print("T7 — relais CLI (verdict, codes)")
    code, texte = gui.executer_cli("coffre_cf2.py", ["statut", "--config", cfg])
    verifie("t7-statut-code0", code == 0 and "[coffre-CF2]" in texte, texte)
    code_m, texte_m = gui.executer_cli("coffre_cf2.py",
                                       ["etat-fragments", "--config", cfg])
    verifie("t7-etat-fragments-code0", code_m == 0, texte_m)
    code_x, _ = gui.executer_cli("coffre_cf2.py", ["commande-inexistante"])
    verifie("t7-commande-invalide-code-non_nul", code_x != 0)

    print("F1 — fail-closed (autotest, phrase, brûlage, relève)")
    autotest_orig = gui.autotest
    try:
        gui.autotest = lambda: False
        refuse("f1-autotest-mute-refuse-generer", gui.hl_generer,
               os.path.join(rep, "x-privee.txt"),
               os.path.join(rep, "x-publique.txt"))
        refuse("f1-autotest-mute-refuse-signer", gui.hl_signer,
               os.path.join(rep, "a-signer.txt"),
               os.path.join(rep, "cle-I-privee.txt"),
               os.path.join(rep, "x-sig.txt"))
    finally:
        gui.autotest = autotest_orig
    refuse("f1-cle-absente-echec-nomme", gui.hl_signer,
           os.path.join(rep, "a-signer.txt"),
           os.path.join(rep, "introuvable.txt"),
           os.path.join(rep, "x-sig.txt"))
    refuse("f1-phrase-vide-refusee-sans-lancement", gui.executer_cli,
           "coffre_cf2.py", ["migrer"], phrase="   ")
    # BRÛLER sans confirmation : le CLI refuse (code 2), fragments SURVIVENT
    code_b, texte_b = gui.executer_cli("coffre_cf2.py", ["bruler",
                                                         "--config", cfg])
    verifie("f1-bruler-sans-confirmation-refuse", code_b != 0
            and "--oui-je-comprends" in texte_b, texte_b)
    verifie("f1-fragments-survivent",
            all(os.path.isfile(os.path.join(g, f"fragment-{i + 1}.cf2f"))
                for i, g in enumerate(labo["gardes"])))
    # brûlage RÉEL du labo (confirmé), puis relève par les copies
    code_br, texte_br = gui.executer_cli(
        "coffre_cf2.py", ["bruler", "--oui-je-comprends", "--config", cfg])
    pv_dir = cf2.lire_config(cfg)["pv_dir"]
    verifie("f1-brulage-labo-effectue", code_br == 0
            and os.path.isdir(pv_dir) and os.listdir(pv_dir), texte_br)
    ok_r, texte_r = gui.controle_lecture(cfg, copies)
    verifie("f1-copies-relevent-apres-brulage", ok_r, texte_r)


def _ecrire(chemin, texte):
    with open(chemin, "w", encoding="ascii") as f:
        f.write(texte)
    return chemin


# ---------------------------------------------------------------------------
# T8 — phrase personnelle CF1 (D110) : alphanumérique, sans plafond
# ---------------------------------------------------------------------------
def t8_phrase_personnelle(rep):
    print("T8 — phrase personnelle CF1 (alphanumérique, sans plafond — D110)")
    ok, m = gui.phrase_personnelle_valide("AlphaBravo123Charlie22")
    verifie("t8-valide-22car-131bits-sans-avertissement",
            ok and "sans plafond" in m and "AVERTISSEMENT" not in m, m)
    ok, m = gui.phrase_personnelle_valide("")
    verifie("t8-vide-refusee", not ok and "vide" in m, m)
    ok, m = gui.phrase_personnelle_valide("Alpha Bravo123")
    verifie("t8-espace-refuse-position-nommee", not ok
            and "position 6" in m, m)
    ok, m = gui.phrase_personnelle_valide("AlphaBrav\u00f3123")
    verifie("t8-accent-refuse-position-nommee", not ok
            and "position 10" in m, m)
    ok, m = gui.phrase_personnelle_valide("A!phaBravo123")
    verifie("t8-symbole-refuse-position-nommee", not ok
            and "position 2" in m, m)
    ok, m = gui.phrase_personnelle_valide("Abc1234")
    verifie("t8-plancher-huit-refuse", not ok and "8" in m, m)
    longue = ("aA1" * 3333 + "Zz9")[:10_000]
    ok, m = gui.phrase_personnelle_valide(longue)
    verifie("t8-aucun-plafond-10000-caracteres",
            ok and "10000" in m and "sans plafond" in m, m)
    ok, m = gui.phrase_personnelle_valide("AlphaBravo123!")
    verifie("t8-caractere-fautif-jamais-divulgue", not ok and "!" not in m, m)

    # bout en bout PAR LE RELAIS GUI (le chemin exact de l'utilisateur)
    chemin = os.path.join(rep, "coffre-labo.bin")
    code, texte = gui.executer_cli(
        "coffre_fort.py",
        ["--chemin", chemin, "init", "--generer-phrase",
         "--phrase-vers-fichier", os.path.join(rep, "ancienne.txt")],
        au_racine=True)
    verifie("t8-labo-init-code0", code == 0, texte)
    with open(os.path.join(rep, "ancienne.txt"), "rb") as f:
        ancienne = f.read().strip()
    entree = os.path.join(rep, "entree.txt")
    with open(entree, "wb") as f:
        f.write(b"SECRET-LABO-T8")
    code, texte = gui.executer_cli(
        "coffre_fort.py",
        ["--chemin", chemin, "ajouter", "LABO", "temoin",
         "--description", "temoin D110", "--depuis-fichier", entree],
        phrase=ancienne.decode("ascii"), au_racine=True)
    verifie("t8-labo-entree-ajoutee", code == 0, texte)
    mienne = "MaPhrasePersonnelle2026"
    code, texte = gui.executer_cli(
        "coffre_fort.py", ["--chemin", chemin, "changer-phrase"],
        phrase=ancienne.decode("ascii"), nouvelle_phrase=mienne,
        au_racine=True)
    verifie("t8-changer-phrase-code0", code == 0, texte)
    try:
        cf1.charger(chemin, ancienne)
        verifie("t8-ancienne-inoperante", False, "aucun refus levé")
    except cf1.ErreurCoffre as exc:
        verifie("t8-ancienne-inoperante", str(exc) != "", str(exc))
    _, base = cf1.charger(chemin, mienne.encode("utf-8"))
    verifie("t8-mienne-ouvre-entree-intacte",
            cf1._trouver(base, "LABO", "temoin") is not None)
    refuse("t8-phrase-vide-refusee-sans-lancement", gui.executer_cli,
           "coffre_fort.py", ["--chemin", chemin, "changer-phrase"],
           phrase=ancienne.decode("ascii"), nouvelle_phrase="   ")


def x1_import_headless():
    print("X1 — import headless + selftest embarqué")
    verifie("x1-import-sans-fenetre", not hasattr(gui, "_fenetre_cree")
            and callable(gui.selftest))
    verifie("x1-tkinter-disponible", gui.TKINTER_DISPONIBLE,
            gui.TKINTER_ERREUR)
    verifie("x1-selftest-embarque", gui.selftest())


# ---------------------------------------------------------------------------
# X2 — cohérence des attributs (régression D109 : « app.mainloop »)
# ---------------------------------------------------------------------------
def _noeuds_fonctions(cls):
    """AST de chaque méthode de la classe (source introuvable => vide)."""
    import ast
    import inspect
    import textwrap
    for _, f in inspect.getmembers(cls, predicate=inspect.isfunction):
        try:
            yield ast.parse(textwrap.dedent(inspect.getsource(f)))
        except (OSError, TypeError):
            continue


def _aplatir_cible(t):
    """Attributs self.X d'une cible d'affectation (tuples aplatis)."""
    import ast
    if isinstance(t, ast.Tuple):
        return [x for e in t.elts for x in _aplatir_cible(e)]
    if isinstance(t, ast.Starred):
        return _aplatir_cible(t.value)
    if (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
            and t.value.id == "self"):
        return [t.attr]
    return []


def _self_assignes(cls):
    import ast
    assignes = set()
    for arbre in _noeuds_fonctions(cls):
        for n in ast.walk(arbre):
            if isinstance(n, ast.Assign):
                cibles = n.targets
            elif isinstance(n, (ast.AugAssign, ast.AnnAssign)):
                cibles = [n.target]
            elif isinstance(n, ast.For):
                cibles = [n.target]
            else:
                continue
            for t in cibles:
                assignes.update(_aplatir_cible(t))
    return assignes


def _self_lus(cls):
    import ast
    lus = set()
    for arbre in _noeuds_fonctions(cls):
        for n in ast.walk(arbre):
            if (isinstance(n, ast.Attribute)
                    and isinstance(n.value, ast.Name)
                    and n.value.id == "self"):
                lus.add(n.attr)
    return lus


def _app_traverses(cls):
    """Attributs lus via self.app.X (l'enveloppe d'Application)."""
    import ast
    refs = set()
    for arbre in _noeuds_fonctions(cls):
        for n in ast.walk(arbre):
            if (isinstance(n, ast.Attribute)
                    and isinstance(n.value, ast.Attribute)
                    and n.value.attr == "app"
                    and isinstance(n.value.value, ast.Name)
                    and n.value.value.id == "self"):
                refs.add(n.attr)
    return refs


def x2_coherence_attributs():
    print("X2 — cohérence des attributs (régression « app.mainloop » D109)")
    import ast
    import inspect
    for cls in (gui.Executeur, gui.Journal, gui.Application):
        methodes = {nom for nom, _ in
                    inspect.getmembers(cls, predicate=inspect.isfunction)}
        fantomes = sorted(_self_lus(cls) - _self_assignes(cls) - methodes)
        verifie(f"x2-{cls.__name__.lower()}-attributs-self-connus",
                not fantomes, f"self.{fantomes} jamais assigné ni méthode")
    connus = ({nom for nom, _ in inspect.getmembers(
                gui.Application, predicate=inspect.isfunction)}
              | _self_assignes(gui.Application))
    traverses = set()
    for cls in (gui.Executeur, gui.Journal):
        traverses |= _app_traverses(cls)
    fantomes_app = sorted(traverses - connus)
    verifie("x2-traversee-self-app-application-connue",
            not fantomes_app,
            f"self.app.{fantomes_app} inexistant sur Application")
    refs = {n.attr for n in ast.walk(ast.parse(
                inspect.getsource(gui.demarrer_gui)))
            if isinstance(n, ast.Attribute)
            and isinstance(n.value, ast.Name) and n.value.id == "app"}
    fantomes = sorted(refs - connus)
    verifie("x2-demarrer_gui-app-connu", not fantomes,
            f"app.{fantomes} inexistant sur Application — "
            "le Tk racine est app.racine (bogue D109)")


def main() -> int:
    print(f"[test-ceremonie-GUI] falsifiabilité du maître de cérémonie "
          f"(D107 · D109 · D110) — dépôt {RACINE}")
    t1_ed25519()
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-test-") as rep:
        t234_cle_i(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-cf2-") as rep:
        t567f1(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t8-") as rep:
        t8_phrase_personnelle(rep)
    x1_import_headless()
    x2_coherence_attributs()
    print(f"[test-ceremonie-GUI] {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
