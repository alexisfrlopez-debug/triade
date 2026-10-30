#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_ceremonie_gui.py — falsifiabilité du MAÎTRE DE CÉRÉMONIE (D107,
compléments correctif D109, phrase personnelle D110, attachement --depot
D111, chemins choisis dans la fenêtre D112).

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
       est bouché ici, headless, sur TOUTE la classe) ;
  X3   attachement au dépôt (D111) : ordre de résolution --depot >
       TRIADE_DEPOT > position du fichier ; chemin introuvable = échec
       NOMMÉ (code 2 par le point d'entrée, jamais un repli silencieux) ;
       dossier sans v06/coffre_cf2.py = profil désactivé (garde intacte) ;
       définir_racine_depot bascule TOUT le profil (disponibilité, import
       v06.coffre_cf2) et le rétablissement est vérifié ;
  T9   clé à la main (D112) : graine_texte signe IDENTIQUEMENT au fichier
       (majuscules acceptées), les saisies fautives (63 hex, non-hex,
       espace interne, vide, aucun des deux) sont des refus NOMMÉS sans
       écriture, et la graine ne paraît JAMAIS dans le texte de retour ;
  T10  chemins coffre CF1 par le relais (D112) : --chemin choisi pour
       statut/verifier (argument GLOBAL du parseur, avant la
       sous-commande), migrer --depuis le conteneur choisi — bout en bout
       sur coffre labo à chemin PERSONNALISÉ, CF1 laissé INTACT ;
  T11  verdict sans répétition (D114) : quand la sortie CLI a déjà coulé
       ligne à ligne dans le journal (emit), _cli rend UNE ligne d'ancrage
       (la première — le détail vit au-dessus, dans l'ordre du flux) ;
       sans emit, le texte ENTIER reste la remise du verdict ;
  T12  git (D116) : pousser les fichiers générés — add ciblé (JAMAIS
       « -A »), message vide refusé AVANT tout, rien-à-committer =
       synchronisation VERTE, commit+push PROUVÉS sur un origin NU de
       laboratoire (le dépôt distant a bien reçu le commit), statut
       propre après, dossier hors-git refus NOMMÉ ;
  T13  fil de cérémonie (D116/D117) : les étapes s'auto-détectent par
       PREUVES en lecture seule, et les témoins e1/e4 sont ÈRE-COHÉRENTS
       — le fil suit l'ère du dépôt réel (re-cérémonie passée → « tout
       est signé — préparer inutile » / « arbres VERTS » ; fenêtre D115
       vivante → « a-signer PÉRIMÉ » / « signature requise ») : mentir
       dans un sens comme dans l'autre serait attrapé ; clé absente
       nommée, fichiers manquants nommés, git propre ET poussé ;
  T14  scénarios et clonage (D117) : le choix AVANT TOUT (dossier local
       / repo git) détermine les étapes — fil de CINQ d'un côté, de SIX
       avec « Cloner le dépôt » en tête (preuve rev-parse + origin)
       de l'autre ; masquage du jeton d'URL ; preuve clone refusée
       NOMMÉE (hors git / sans origin) ; cloner_depot refuse URL vide,
       URL « - » (injection), destination vide / « - » / NON VIDE
       (intacte après refus), git absent (127 nommé, simulation sans
       réseau) ; clone de LABORATOIRE (origin nu local, AUCUN réseau
       réel) : réussite → dépôt ATTACHÉ + origin prouvé ; clone sans
       garde D111 → attachement REFUSÉ, clone conservé sur disque ;
  T15  fusion D118 (une seule page) : le DOSSIER DE CÉRÉMONIE naît
       HORS du dépôt (sœur du dépôt attaché, il suit le re-attachement),
       les QUATRE chemins de travail (clé privée, clé publique,
       a-signer, signatures) vivent dedans ; la COPIE de la remise vers
       ce dossier est verte (dossier créé, contenu identique) et ses
       refus sont NOMMÉS (source absente) ; les gestes du fil ne
       référencent PLUS aucun « profil » (plus d'allers-retours par
       l'accueil) et nomment le dossier de cérémonie ;
  T16  D119 — le dossier naît AVEC LA CLÉ (rapport du terrain v1.8 :
       « générer » mourait en Errno 2 tant que « Préparer » n'avait pas
       créé le dossier via la copie de la remise) : hl_generer et
       hl_signer CRÉENT le dossier de sortie avant d'écrire (clé,
       signatures, y compris un SOUS-dossier), l'interop historique
       reste intacte (graine = une ligne de 64 hex), refus NOMMÉ si le
       dossier est impossible (parent-fichier) et RIEN n'est écrit ;
       exporter_feuille suit la même loi sur un mini-coffre de labo
       (feuille écrite dans un dossier ABSENT) ;

Style maison : tout sur la sortie, échec nommé, exit code 0/1.
"""

import json
import os
import re
import secrets
import sys
import tempfile
import time

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
    # D120 : le labo du test ne fait pas vivre de sentinelle — la porte y
    # est donc muette (exiger=false). La porte ELLE-MÊME est prouvée à
    # part : T5b ci-dessous l'arme exprès sur ce labo, et test_cf2.py T7
    # la prouve au niveau CLI (refus nommé, VERT avec sentinelle vivante,
    # morte visible, ère sans moteur).
    config["exiger_sentinelle"] = False
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

    print("T5b — porte D120 : le contrôle de relecture EST un déverrouillage")
    # la porte armée (exiger=true) SANS sentinelle vivante => refus NOMMÉ
    # (ErreurCeremonie — le contrat du contrôleur), AVANT toute lecture
    c = cf2.lire_config(cfg)
    c["exiger_sentinelle"] = True
    c["heartbeat"] = os.path.join(rep, "heartbeat-t5b.txt")
    cf2.ecrire_config(cfg, c)
    refuse("t5b-porte-refuse-sans-sentinelle", gui.controle_lecture,
           cfg, copies)
    # heart-beat FRAIS (forgé — discipline du labo) => le contrôle repasse
    with open(c["heartbeat"], "w", encoding="utf-8") as f:
        f.write(json.dumps({"ts": time.time()}))
    ok_p, texte_p = gui.controle_lecture(cfg, copies)
    verifie("t5b-porte-verte-heartbeat-frais", ok_p, texte_p)
    # la porte redevient muette pour la suite du labo (T6/F1 utilisent
    # le même config)
    c["exiger_sentinelle"] = False
    cf2.ecrire_config(cfg, c)

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

    print("T11 — D114 : le verdict ne répète plus le flux (une ligne d'ancrage)")
    class _Boite:      # self factice : _cli ne touche que executer_cli
        pass
    captes = []
    code_v, texte_v = gui.Application._cli(
        _Boite(), "coffre_cf2.py", ["statut", "--config", cfg],
        emit=captes.append)
    verifie("t11-avec-flux-verdict-une-seule-ligne",
            code_v and "\n" not in texte_v and len(captes) > 1
            and texte_v.strip() == captes[0].strip(), texte_v)
    code_p, texte_p = gui.Application._cli(
        _Boite(), "coffre_cf2.py", ["statut", "--config", cfg])
    verifie("t11-sans-flux-texte-entier-reste",
            code_p and "\n" in texte_p, texte_p)

    print("T12 — D116 : pousser sur git (labo — add ciblé, commit, "
          "pull --rebase, push)")
    import subprocess
    labo_git = tempfile.mkdtemp(prefix="git-labo-")
    origin_git = os.path.join(labo_git, "origin.git")
    clone_git = os.path.join(labo_git, "triade")
    os.makedirs(os.path.join(clone_git, "v06", "sceau-I"))
    _ecrire(os.path.join(clone_git, "v06", "sceau-I", "x.txt"),
            "premier\n")

    def git_labo(args, cwd):
        return subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                              text=True, timeout=60)

    git_labo(["init", "--bare", "-q", origin_git], labo_git)
    git_labo(["init", "-q"], clone_git)
    git_labo(["config", "user.email", "lab@triade.test"], clone_git)
    git_labo(["config", "user.name", "lab-triade"], clone_git)
    git_labo(["add", "."], clone_git)
    git_labo(["commit", "-q", "-m", "init"], clone_git)
    git_labo(["branch", "-M", "main"], clone_git)
    git_labo(["remote", "add", "origin", origin_git], clone_git)
    git_labo(["push", "-q", "-u", "origin", "main"], clone_git)
    racine_sauvee = gui.RACINE_DEPOT
    gui.RACINE_DEPOT = clone_git
    try:
        refuse("t12-message-vide-refuse-avant-tout", gui.git_pousser,
               ["v06/sceau-I"], "   ")
        refuse("t12-aucun-chemin-refuse-avant-tout", gui.git_pousser, [],
               "message")
        captes_git = []
        ok_git, texte_git = gui.git_pousser(["v06/sceau-I"], "sync seule",
                                            emit=captes_git.append)
        verifie("t12-rien-a-committer-sync-seule-verte",
                ok_git and any("rien à committer" in l for l in captes_git),
                texte_git)
        _ecrire(os.path.join(clone_git, "v06", "sceau-I", "x.txt"),
                "second\n")
        ok_git2, texte_git2 = gui.git_pousser(["v06/sceau-I"],
                                             "sceau-I : test D116")
        verifie("t12-commit-pousse-vert", ok_git2 and "poussé" in texte_git2
                and "1 commit" in texte_git2, texte_git2)
        sujet = git_labo(["--git-dir", origin_git, "log", "-1", "main",
                          "--format=%s"], labo_git).stdout.strip()
        verifie("t12-origin-a-bien-recu-le-commit",
                sujet == "sceau-I : test D116", sujet)
        code_st, texte_st = gui.executer_git(
            ["status", "--porcelain", "-b"])
        lignes_st = [l for l in texte_st.splitlines() if l.strip()]
        verifie("t12-statut-propre-apres-push",
                code_st == 0 and len(lignes_st) == 1
                and "ahead" not in lignes_st[0], texte_st)
        gui.RACINE_DEPOT = tempfile.mkdtemp(prefix="pas-un-depot-")
        refuse("t12-hors-depot-git-refus-nomme", gui.git_pousser,
               ["v06/sceau-I"], "message")
    finally:
        gui.RACINE_DEPOT = racine_sauvee

    print("T13 — D116/D117 : fil de cérémonie (lecture seule, dépôt réel)")
    a_signer = os.path.join(RACINE, "v06", "sceau-I", "a-signer.txt")
    etat_fil = gui.fil_ceremonie(a_signer=a_signer)
    verifie("t13-cinq-etapes-titrees", len(etat_fil) == 5
            and [e[0] for e in etat_fil] == [1, 2, 3, 4, 5])
    par_etape = {numero: (faite, detail)
                 for numero, _, faite, detail in etat_fil}
    # D117 : les témoins e1/e4 suivent l'ÈRE du dépôt réel — après la
    # re-cérémonie (59b7ddc) le sceau est VERT et le fil doit le DIRE
    # (« préparer inutile », « arbres VERTS ») ; pendant la fenêtre D115
    # il devait nommer « PÉRIMÉ » / « signature requise ». Le fil qui
    # mentirait dans UN sens comme dans l'autre serait attrapé ICI.
    code_ere, _ = gui.executer_cli("sceau_I.py", ["verifier"])
    if code_ere == 0:
        verifie("t13-e1-ere-signee-preparer-inutile",
                par_etape[1][0] is True
                and "préparer inutile" in par_etape[1][1].lower(),
                par_etape[1][1])
        verifie("t13-e4-ere-signee-arbres-verts",
                par_etape[4][0] is True and "VERTS" in par_etape[4][1],
                par_etape[4][1])
    else:
        verifie("t13-e1-fenetre-d115-a-signer-perime-nomme",
                par_etape[1][0] is False and "PÉRIMÉ" in par_etape[1][1],
                par_etape[1][1])
        verifie("t13-e4-signature-requise-nomme",
                par_etape[4][0] is False and "signature requise" in
                par_etape[4][1], par_etape[4][1])
    verifie("t13-e2-cle-absente-nomme",
            par_etape[2][0] is False and "absent" in par_etape[2][1],
            par_etape[2][1])
    verifie("t13-e3-fichiers-manquants-nommes",
            par_etape[3][0] is False and "manquants" in par_etape[3][1],
            par_etape[3][1])
    verifie("t13-e5-git-propre-et-pousse",
            par_etape[5][0] is True and "propre" in par_etape[5][1],
            par_etape[5][1])


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


def t14_scenarios_clone(rep):
    """T14 — D117 : le scénario AVANT TOUT (dossier local / repo git) et
    le CLONAGE. Tout en laboratoire : l'origin est un dépôt nu LOCAL, la
    panne de git est SIMULÉE (faux Popen, aucun processus lancé) — aucune
    dépendance au réseau, aucune clé touchée."""
    import io
    import subprocess
    import types

    print("T14 — D117 : scénarios (dossier local / repo git) + clonage")
    verifie("t14-scenarios-nommes",
            gui.SCENARIOS == ("dossier local", "repo git"))
    verifie("t14-masque-jeton",
            gui.masquer_jeton("https://jeton@github.com/u/r.git")
            == "https://***@github.com/u/r.git"
            and gui.masquer_jeton("https://user:pass@h/x.git")
            == "https://***@h/x.git"
            and gui.masquer_jeton("git@github.com:u/r.git")
            == "git@github.com:u/r.git")

    # --- la preuve clone (lecture seule, refus nommés) -------------------
    pas_git = os.path.join(rep, "pas-un-depot")
    os.makedirs(pas_git, exist_ok=True)
    faite, detail = gui.preuve_clone(pas_git)
    verifie("t14-preuve-hors-git-refusee-nommee", not faite
            and "pas un dépôt git" in detail, detail)
    init_seul = os.path.join(rep, "init-seul")
    os.makedirs(init_seul, exist_ok=True)
    subprocess.run(["git", "init", "-q", init_seul], check=True,
                   capture_output=True, timeout=60)
    faite_i, detail_i = gui.preuve_clone(init_seul)
    verifie("t14-preuve-sans-origin-refusee-nommee", not faite_i
            and "origin" in detail_i, detail_i)
    faite_a, detail_a = gui.preuve_clone()   # le dépôt des tests est un clone
    verifie("t14-preuve-vrai-clone-verte", faite_a
            and "origin" in detail_a, detail_a)

    # --- le scénario détermine les étapes du fil ------------------------
    a_signer = os.path.join(RACINE, "v06", "sceau-I", "a-signer.txt")
    fil_cinq = gui.fil_ceremonie(a_signer=a_signer)
    fil_six = gui.fil_ceremonie(a_signer=a_signer, scenario="repo git")
    verifie("t14-fil-dossier-cinq-etapes", len(fil_cinq) == 5
            and fil_cinq[0][1].startswith("Préparer"))
    verifie("t14-fil-git-six-etapes-clone-en-tete", len(fil_six) == 6
            and [e[0] for e in fil_six] == [1, 2, 3, 4, 5, 6]
            and "Cloner" in fil_six[0][1]
            and fil_six[0][2] is True
            and fil_six[1][1] == fil_cinq[0][1],
            f"{fil_six[0]} / {fil_six[1]}")
    verifie("t14-hints-suivent-le-scenario",
            "Cloner en local" in gui.hint_fil("repo git", 1)
            and gui.hint_fil("repo git", 2) == gui.FIL_HINTS[1]
            and gui.hint_fil("dossier local", 1) == gui.FIL_HINTS[1]
            and gui.hint_fil(None, 5) == gui.FIL_HINTS[5])

    # --- cloner_depot : refus NOMMÉS avant tout lancement ----------------
    refuse("t14-clone-url-vide-refusee", gui.cloner_depot, "",
           os.path.join(rep, "c1"))
    refuse("t14-clone-url-tiret-injection-refusee", gui.cloner_depot,
           "--upload-pack=x", os.path.join(rep, "c2"))
    refuse("t14-clone-destination-vide-refusee", gui.cloner_depot,
           "https://example.invalid/x.git", "")
    refuse("t14-clone-destination-tiret-refusee", gui.cloner_depot,
           "https://example.invalid/x.git", "-opt")
    prise = os.path.join(rep, "destination-prise")
    os.makedirs(prise, exist_ok=True)
    _ecrire(os.path.join(prise, "deja.txt"), "contenu\n")
    refuse("t14-clone-destination-prise-refusee", gui.cloner_depot,
           "https://example.invalid/x.git", prise)
    verifie("t14-destination-prise-intacte",
            os.path.isfile(os.path.join(prise, "deja.txt")))

    # --- git ABSENT (127) et ÉCHEC de clone : SIMULÉS, aucun réseau -----
    class _ProcFaux:
        def __init__(self, code, sortie=""):
            self.stdout = io.StringIO(sortie)
            self._code = code

        def wait(self):
            return self._code

    subprocess_reel = gui.subprocess
    try:
        # git ABSENT : Popen LÈVE FileNotFoundError (c'est exactement ce que
        # fait subprocess quand le binaire manque — le faux proc ne suffit
        # pas, l'exception est le chemin réel du code 127)
        def _popen_absent(*a, **k):
            raise FileNotFoundError("git absent (simulation T14)")

        gui.subprocess = types.SimpleNamespace(
            Popen=_popen_absent, PIPE=-1, STDOUT=-2)
        ok_127, texte_127 = gui.cloner_depot(
            "https://example.invalid/x.git", os.path.join(rep, "c3"))
        verifie("t14-clone-git-absent-127-nomme",
                not ok_127 and "git introuvable" in texte_127, texte_127)
        gui.subprocess = types.SimpleNamespace(
            Popen=lambda *a, **k: _ProcFaux(
                128, "fatal: échec simulé par T14 (aucun réseau)\n"),
            PIPE=-1, STDOUT=-2)
        captes_tok = []
        ok_tok, texte_tok = gui.cloner_depot(
            "https://jetonsecret@exemple.invalid/x.git",
            os.path.join(rep, "c4"), emit=captes_tok.append)
        tout_tok = texte_tok + "\n" + "\n".join(captes_tok)
        verifie("t14-jeton-masque-dans-l-echec",
                not ok_tok and "jetonsecret" not in tout_tok
                and "***@" in tout_tok, tout_tok[:200])
    finally:
        gui.subprocess = subprocess_reel

    # --- cloner_et_attacher : clone de LABORATOIRE (origin nu local) ----
    def git_labo(args, cwd):
        return subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                              text=True, timeout=60)

    def monter_source(nom, avec_garde):
        labo = os.path.join(rep, nom)
        origin = os.path.join(labo, "origin.git")
        travail = os.path.join(labo, "source-travail")
        os.makedirs(os.path.join(travail, "v06"), exist_ok=True)
        if avec_garde:
            _ecrire(os.path.join(travail, "v06", "coffre_cf2.py"),
                    "# garde D111 factice\n")
        _ecrire(os.path.join(travail, "x.txt"), "contenu\n")
        subprocess.run(["git", "init", "-q", "--bare", origin],
                       check=True, capture_output=True, timeout=60)
        # le dépôt nu naît la tête sur « master » (défaut git) : on y pousse
        # « main » — sans ce symbolic-ref, un clone de l'origin nu est vide
        # (checkout impossible : « remote HEAD refers to nonexistent ref »)
        subprocess.run(["git", "--git-dir", origin, "symbolic-ref", "HEAD",
                       "refs/heads/main"], check=True, capture_output=True,
                       timeout=60)
        git_labo(["init", "-q"], travail)
        git_labo(["config", "user.email", "lab@triade.test"], travail)
        git_labo(["config", "user.name", "lab-triade"], travail)
        git_labo(["add", "."], travail)
        git_labo(["commit", "-q", "-m", "init"], travail)
        git_labo(["branch", "-M", "main"], travail)
        git_labo(["push", "-q", origin, "main"], travail)
        return origin

    origin_garde = monter_source("labo-avec-garde", True)
    racine_sauvee, source_sauvee = gui.RACINE_DEPOT, gui.SOURCE_DEPOT
    destination = os.path.join(rep, "labo-avec-garde", "triade-clone")
    try:
        captes = []
        ok_c, texte_c = gui.cloner_et_attacher(origin_garde, destination,
                                               emit=captes.append)
        verifie("t14-clone-labo-vert-et-attache",
                ok_c and "ATTACHÉ" in texte_c
                and gui.RACINE_DEPOT == os.path.abspath(destination)
                and gui.SOURCE_DEPOT == "clone choisi (GUI, D117)",
                texte_c)
        verifie("t14-clone-labo-preuve-origin",
                os.path.isdir(os.path.join(destination, ".git"))
                and gui.preuve_clone()[0] is True)
        verifie("t14-clone-labo-fil-git-vert-sur-clone",
                gui.fil_ceremonie(scenario="repo git")[0][2] is True)
        origin_sans_garde = monter_source("labo-sans-garde", False)
        destination2 = os.path.join(rep, "labo-sans-garde", "clone")
        ok_d, texte_d = gui.cloner_et_attacher(origin_sans_garde, destination2)
        verifie("t14-clone-sans-garde-attachement-refuse",
                not ok_d and "v06/coffre_cf2.py introuvable" in texte_d
                and "attachement REFUSÉ" in texte_d
                and gui.RACINE_DEPOT == os.path.abspath(destination)
                and os.path.isdir(os.path.join(destination2, ".git")),
                texte_d[:200])
    finally:
        gui.definir_racine_depot(racine_sauvee, source_sauvee)
    verifie("t14-restauration-depot-des-tests",
            gui.RACINE_DEPOT == racine_sauvee)


def t15_fusion_d118(rep):
    """T15 — D118 : UNE seule page de cérémonie. Le dossier de cérémonie
    (clé + remises) naît HORS du dépôt, suit le re-attachement ; la copie
    de la remise vers ce dossier est verte et ses refus nommés ; les
    gestes du fil ne référencent plus aucun profil. Tout en laboratoire."""
    print("T15 — D118 : fusion des profils, dossier de cérémonie, remise "
          "à côté des clés")

    # --- le dossier de cérémonie : HORS du dépôt, sœur, il suit --------
    defaut = gui.dossier_ceremonie_defaut()
    verifie("t15-dossier-hors-du-depot",
            not defaut.startswith(os.path.abspath(gui.RACINE_DEPOT) + os.sep)
            and os.path.dirname(os.path.abspath(defaut))
            == os.path.dirname(os.path.abspath(gui.RACINE_DEPOT)),
            defaut)
    verifie("t15-dossier-nomme",
            os.path.basename(defaut) == gui.NOM_DOSSIER_CEREMONIE)
    # le dossier VIDE retombe sur le défaut (jamais d'invention ailleurs)
    verifie("t15-chemins-dossier-vide-retombe-defaut",
            gui.chemins_ceremonie("")["a_signer"]
            == os.path.join(defaut, "a-signer.txt"))
    chemins = gui.chemins_ceremonie(rep)
    verifie("t15-quatre-chemins-sous-le-dossier",
            chemins == {"privee": os.path.join(rep, "cle-I-privee.txt"),
                        "publique": os.path.join(rep, "cle-publique-I.txt"),
                        "a_signer": os.path.join(rep, "a-signer.txt"),
                        "signatures": os.path.join(rep, "signatures-I.txt")},
            str(chemins))
    # le re-attachement déplace le défaut : sœur du NOUVEAU dépôt
    racine_sauvee, source_sauvee = gui.RACINE_DEPOT, gui.SOURCE_DEPOT
    autre = os.path.join(rep, "autre-depot")
    os.makedirs(os.path.join(autre, "v06"), exist_ok=True)
    try:
        gui.definir_racine_depot(autre, "--depot")
        verifie("t15-dossier-suit-le-re-attachement",
                gui.dossier_ceremonie_defaut()
                == os.path.join(rep, gui.NOM_DOSSIER_CEREMONIE),
                gui.dossier_ceremonie_defaut())
    finally:
        gui.definir_racine_depot(racine_sauvee, source_sauvee)
    verifie("t15-dossier-retabli-avec-le-depot",
            gui.dossier_ceremonie_defaut() == defaut)

    # --- la copie de la remise vers le dossier de cérémonie ------------
    source = os.path.join(rep, "source-a-signer.txt")
    empreinte = secrets.token_hex(32)
    with open(source, "w", encoding="utf-8") as f:
        f.write(f"m0/test ALPHA {empreinte}\nm4/test BETA {empreinte}\n")
    cible_dir = os.path.join(rep, "sous-dossier-cree")
    ok_c, texte_c = gui.copier_remise_vers_dossier(source, cible_dir)
    cible = os.path.join(cible_dir, "a-signer.txt")
    pareil = False
    if os.path.isfile(cible):
        with open(cible, "r", encoding="utf-8") as f:
            pareil = f.read() == f"m0/test ALPHA {empreinte}\n" \
                     f"m4/test BETA {empreinte}\n"
    verifie("t15-copie-verte-dossier-cree-contenu-identique",
            ok_c and pareil and "COPIÉE" in texte_c, texte_c)
    verifie("t15-copie-source-intacte",
            os.path.isfile(source))
    ok_f, texte_f = gui.copier_remise_vers_dossier(
        os.path.join(rep, "jamais-ecrit.txt"), cible_dir)
    verifie("t15-copie-source-absente-refus-nomme",
            not ok_f and "source absente" in texte_f, texte_f)
    # dossier VIDE : retombe sur le défaut — attaché au LABO pour que la
    # copie atterrit DANS le temporaire (aucun dossier réel touché)
    try:
        gui.definir_racine_depot(autre, "--depot")
        ok_v, texte_v = gui.copier_remise_vers_dossier(source, "")
        verifie("t15-copie-dossier-vide-retombe-defaut-sandboxe",
                ok_v and os.path.isfile(
                    os.path.join(rep, gui.NOM_DOSSIER_CEREMONIE,
                                 "a-signer.txt")),
                texte_v)
    finally:
        gui.definir_racine_depot(racine_sauvee, source_sauvee)

    # --- les gestes du fil : plus aucun profil, le dossier nommé -------
    verifie("t15-gestes-sans-profil",
            all("profil" not in h.lower() for h in gui.FIL_HINTS.values()),
            str(gui.FIL_HINTS))
    verifie("t15-gestes-nomment-le-dossier-de-ceremonie",
            "dossier de cérémonie" in gui.FIL_HINTS[1]
            and "dossier de cérémonie" in gui.FIL_HINTS[3])
    verifie("t15-geste-cle-hors-aller-retour",
            "ci-contre" in gui.FIL_HINTS[2].lower())

    # --- la version porte la fusion (ère-cohérente : D118 ou après) ----
    verifie("t15-version-d118-ou-posterieure",
            any(f"D{d}" in gui.VERSION_GUI for d in (118, 119, 120)),
            gui.VERSION_GUI)


# ---------------------------------------------------------------------------
# T16 — D119 : le dossier de cérémonie NAÎT AVEC LA CLÉ (rapport du
# terrain v1.8 : « générer » mourait en Errno 2 tant que « Préparer »
# n'avait pas créé le dossier via la copie de la remise D118)
# ---------------------------------------------------------------------------

def t16_dossier_avec_la_cle(rep):
    """T16 — D119 : hl_generer / hl_signer / exporter_feuille créent le
    dossier de sortie AVANT d'écrire ; refus NOMMÉ si le dossier est
    impossible (rien n'est écrit). Tout en laboratoire temporaire."""
    print("T16 — D119 : le dossier de cérémonie naît avec la clé")
    dossier = os.path.join(rep, "ceremonie-triade")      # ABSENT au départ
    verifie("t16-dossier-absent-au-depart", not os.path.isdir(dossier))
    privee = os.path.join(dossier, "cle-I-privee.txt")
    publique = os.path.join(dossier, "cle-publique-I.txt")
    gui.hl_generer(privee, publique)
    verifie("t16-generer-cree-dossier-et-cle",
            os.path.isdir(dossier) and os.path.isfile(privee)
            and os.path.isfile(publique))
    # l'interop historique est intacte : graine = UNE ligne de 64 hex
    with open(privee, "r", encoding="utf-8") as f:
        texte = f.read()
    hexa = [l.strip() for l in texte.splitlines()
            if l.strip() and not l.startswith("#")]
    verifie("t16-cle-privee-format-interop",
            len(hexa) == 1 and len(hexa[0]) == 64
            and all(c in "0123456789abcdef" for c in hexa[0]))
    # signer : sortie dans un SOUS-dossier ABSENT
    remise = os.path.join(dossier, "a-signer.txt")
    empreinte = secrets.token_hex(32)
    with open(remise, "w", encoding="utf-8") as f:
        f.write(f"m0/test ALPHA {empreinte}\nm4/test BETA {empreinte}\n")
    sortie = os.path.join(dossier, "sous-dossier", "signatures-I.txt")
    gui.hl_signer(remise, privee, sortie)
    verifie("t16-signer-cree-le-sous-dossier", os.path.isfile(sortie))
    ok, texte_v = gui.hl_verifier(remise, sortie, publique)
    verifie("t16-signatures-verify-vertes", ok, texte_v)
    # refus NOMMÉ : le parent est un FICHIER, le dossier est impossible
    bloqueur = os.path.join(rep, "un-fichier.txt")
    with open(bloqueur, "w", encoding="utf-8") as f:
        f.write("bloqueur")
    refus = None
    try:
        gui.hl_generer(os.path.join(bloqueur, "sous", "cle-I-privee.txt"),
                       os.path.join(bloqueur, "sous", "cle-publique-I.txt"))
    except gui.ErreurCeremonie as exc:
        refus = str(exc)
    verifie("t16-dossier-impossible-refus-nomme",
            refus is not None
            and "impossible de créer le dossier" in refus,
            refus or "aucun refus levé")
    # fail-closed : le refus n'écrit RIEN
    verifie("t16-rien-ecrit-sur-refus",
            not os.path.exists(os.path.join(bloqueur, "sous")))
    # exporter_feuille (D119) : même loi — mini-coffre de LABORATOIRE, la
    # feuille naît dans un dossier ABSENT (rien de réel n'est touché)
    labo = os.path.join(rep, "labo-cf2-d119")
    racine_gardes = os.path.join(labo, "gardes")
    conteneur = os.path.join(labo, "coffre_cf2.bin")
    m = bytearray(secrets.token_bytes(cf2.TAILLE_M))
    sel = secrets.token_bytes(32)
    try:
        fragments = cf2.decouper(bytes(m), 5, 3)
        clair = json.dumps(cf2.nouvelle_base("labo T16 D119"),
                           ensure_ascii=False).encode("utf-8")
        blob = cf2.construire_conteneur(clair, bytes(m), sel,
                                        cf2._date_utc(), 3, 5)
        cf2._ecrire_atomique(conteneur, blob)
        sel_coffre = cf2._parser_entete(blob)["sel"].hex()
        for x, frag in fragments:
            garde = os.path.join(racine_gardes, f"g{x}")
            os.makedirs(garde, exist_ok=True)
            cf2._ecrire_atomique(
                os.path.join(garde, f"fragment-{x}.cf2f"),
                cf2.serialiser_fragment(x, frag, 3, 5, sel_coffre)
                .encode("ascii"))
        config = cf2.config_par_defaut(5, 3, racine_gardes, conteneur)
        chemin_config = os.path.join(labo, "config_cf2.json")
        cf2.ecrire_config(chemin_config, config)
        feuille = os.path.join(rep, "dossier-feuille", "feuille.txt")
        texte_feuille = gui.exporter_feuille(chemin_config, feuille)
    finally:
        cf2._effacer(m)
    verifie("t16-feuille-cree-son-dossier-de-sortie",
            os.path.isfile(feuille)
            and "feuille exportée" in texte_feuille,
            texte_feuille)
    # la version porte l'ère D119
    verifie("t16-version-d119", "D119" in gui.VERSION_GUI, gui.VERSION_GUI)


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


# ---------------------------------------------------------------------------
# T9 — clé à la main (D112) : la graine retapée signe pareil, les fautes
# sont nommées, rien ne fuite
# ---------------------------------------------------------------------------
def t9_cle_a_la_main(rep):
    print("T9 — clé à la main (graine_texte, D112)")
    privee = os.path.join(rep, "cle-I-privee.txt")
    publique = os.path.join(rep, "cle-publique-I.txt")
    a_signer = os.path.join(rep, "a-signer.txt")
    gui.hl_generer(privee, publique)
    graine = gui._lire_graine_privee(privee)        # le TEST peut lire : le GUI, jamais
    with open(a_signer, "w", encoding="ascii") as f:
        f.write("m0/test ALPHA " + secrets.token_hex(32) + "\n"
                "m4/test BETA " + secrets.token_hex(32) + "\n")

    # 1. la saisie manuelle signe IDENTIQUEMENT au fichier (même graine)
    sig_fichier = os.path.join(rep, "sig-fichier.txt")
    sig_manuelle = os.path.join(rep, "sig-manuelle.txt")
    texte_f = gui.hl_signer(a_signer, privee, sig_fichier)
    texte_m = gui.hl_signer(a_signer, None, sig_manuelle,
                            graine_texte=graine.hex())
    with open(sig_fichier, "r", encoding="ascii") as f:
        lignes_f = f.read()
    with open(sig_manuelle, "r", encoding="ascii") as f:
        lignes_m = f.read()
    verifie("t9-saisie-signe-identiquement-au-fichier",
            lignes_f == lignes_m and len(lignes_f.splitlines()) == 2,
            f"fichier={lignes_f[:40]!r} main={lignes_m[:40]!r}")
    verifie("t9-texte-mentionne-la-source-manuelle",
            "saisie manuelle" in texte_m and privee not in texte_m,
            texte_m[:120])
    verifie("t9-texte-fichier-mentionne-le-fichier", privee in texte_f)

    # 2. majuscules acceptées (retype papier), mêmes octets de graine
    sig_maj = os.path.join(rep, "sig-maj.txt")
    gui.hl_signer(a_signer, None, sig_maj,
                  graine_texte=graine.hex().upper())
    with open(sig_maj, "r", encoding="ascii") as f:
        verifie("t9-majuscules-acceptees-memes-signatures",
                f.read() == lignes_f)

    # 3. la graine ne paraît JAMAIS dans les textes de retour
    hexa = graine.hex()
    verifie("t9-graine-absente-des-textes",
            hexa not in texte_m and hexa not in texte_f
            and hexa.upper() not in texte_m)

    # 4. saisies fautives : refus NOMMÉS, RIEN d'écrit (fail-closed)
    fautives = {
        "t9-soixante-trois-hex-refuses": graine.hex()[:-1],
        "t9-caractere-non-hex-refuse": graine.hex()[:63] + "z",
        "t9-espace-interne-refuse": graine.hex()[:32] + " "
                                    + graine.hex()[32:],
        "t9-soixante-cinq-refuse": graine.hex() + "0",
    }
    for nom, saisie in fautives.items():
        cible = os.path.join(rep, nom + ".txt")
        refuse(nom, gui.hl_signer, a_signer, None, cible,
               graine_texte=saisie)
        verifie(nom + "-rien-ecrit", not os.path.exists(cible))
    refuse("t9-saisie-vide-refusee", gui.hl_signer, a_signer, None,
           os.path.join(rep, "x.txt"), graine_texte="   ")
    refuse("t9-fichier-ni-saisie-refuses", gui.hl_signer, a_signer, None,
           os.path.join(rep, "x.txt"))
    refuse("t9-fichier-introuvable-refuse", gui.hl_signer, a_signer,
           os.path.join(rep, "introuvable-cle.txt"),
           os.path.join(rep, "x.txt"))

    # 5. la vérification croise les DEUX sources (interop claire)
    ok, texte = gui.hl_verifier(a_signer, sig_manuelle, publique)
    verifie("t9-remise-manuelle-verifiee-verte", ok, texte)


# ---------------------------------------------------------------------------
# T10 — chemins coffre CF1 choisis (D112) : --chemin/--depuis par le relais
# ---------------------------------------------------------------------------
def t10_chemins_coffre(rep):
    print("T10 — chemins coffre CF1 (--chemin / --depuis par le relais, D112)")
    # un coffre labo à un chemin PERSONNALISÉ (nulle part dans .keys/)
    coffre = os.path.join(rep, "ailleurs", "mon-coffre.bin")
    os.makedirs(os.path.dirname(coffre), exist_ok=True)
    phrase_f = os.path.join(rep, "phrase.txt")
    code, texte = gui.executer_cli(
        "coffre_fort.py",
        ["--chemin", coffre, "init", "--generer-phrase",
         "--phrase-vers-fichier", phrase_f],
        au_racine=True)
    verifie("t10-init-chemin-personnalise-code0", code == 0, texte)
    with open(phrase_f, "rb") as f:
        phrase = f.read().strip()
    entree = os.path.join(rep, "entree.txt")
    with open(entree, "wb") as f:
        f.write(b"SECRET-LABO-T10")
    code, texte = gui.executer_cli(
        "coffre_fort.py",
        ["--chemin", coffre, "ajouter", "LABO", "temoin",
         "--depuis-fichier", entree],
        phrase=phrase.decode("ascii"), au_racine=True)
    verifie("t10-entree-ajoutee-chemin-personnalise", code == 0, texte)

    # la forme EXACTE des boutons GUI : --chemin AVANT la sous-commande
    code, texte = gui.executer_cli(
        "coffre_fort.py", ["--chemin", coffre, "statut"], au_racine=True)
    verifie("t10-statut-chemin-avant-souscommande-code0",
            code == 0 and "coffre-fort" in texte.lower(), texte)
    code, texte = gui.executer_cli(
        "coffre_fort.py", ["--chemin", coffre, "verifier"],
        phrase=phrase.decode("ascii"), au_racine=True)
    verifie("t10-verifier-chemin-choisi-code0", code == 0, texte)

    # un chemin FAUX reste un échec nommé (le champ est la vérité — pas de
    # repli silencieux vers .keys/ : le relais nomme le conteneur absent)
    code, texte = gui.executer_cli(
        "coffre_fort.py",
        ["--chemin", os.path.join(rep, "coffre-absent.bin"), "statut"],
        au_racine=True)
    verifie("t10-chemin-faux-echec-nomme", code != 0
            and "coffre-absent.bin" in texte, texte[:160])

    # migrer --depuis le conteneur choisi : conteneur/gardes/config labo
    conteneur_cf2 = os.path.join(rep, "coffre-cf2.bin")
    config = os.path.join(rep, "config_cf2.json")
    gardes = os.path.join(rep, "gardes")
    code, texte = gui.executer_cli(
        "coffre_cf2.py",
        ["migrer", "--depuis", coffre, "--conteneur", conteneur_cf2,
         "--racine-gardes", gardes, "--config", config],
        phrase=phrase.decode("ascii"))
    verifie("t10-migrer-depuis-chemin-choisi-code0", code == 0, texte)
    verifie("t10-cf1-laisse-intact", os.path.isfile(coffre))
    verifie("t10-cf2-ne-chez-les-gardes",
            all(os.path.isfile(os.path.join(gardes, f"g{i}",
                                            f"fragment-{i}.cf2f"))
                for i in range(1, 6)))
    code, texte = gui.executer_cli(
        "coffre_cf2.py", ["statut", "--config", config])
    verifie("t10-cf2-statut-config-choisie-code0", code == 0, texte)
    _, base = cf1.charger(coffre, phrase)
    verifie("t10-entree-cf1-migree",
            cf1._trouver(base, "LABO", "temoin") is not None)


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


def x3_attachement_depot():
    print("X3 — D111 : le GUI s'attache au dépôt (--depot / TRIADE_DEPOT)")
    import subprocess

    # Le défaut D107 ne bouge pas : ce fichier vit dans <dépôt>/v06/.
    racine_defaut, source_defaut = gui._resoudre_racine_depot()
    verifie("x3-defaut-position-du-fichier",
            racine_defaut == gui._racine_depot_defaut()
            and source_defaut == "position du fichier")

    # --depot CHEMIN : résolution absolue + source nommée.
    racine_arg, source_arg = gui._resoudre_racine_depot(RACINE)
    verifie("x3-argument-depot-resolu",
            os.path.abspath(racine_arg) == os.path.abspath(RACINE)
            and source_arg == "--depot")

    # Un chemin introuvable est un ÉCHEC NOMMÉ — jamais un repli silencieux.
    refuse("x3-argument-introuvable-nomme", gui._resoudre_racine_depot,
           os.path.join(RACINE, "absent-totalement"))
    env_avant = os.environ.get("TRIADE_DEPOT")
    os.environ.pop("TRIADE_DEPOT", None)
    try:
        os.environ["TRIADE_DEPOT"] = os.path.join(RACINE, "introuvable-aussi")
        refuse("x3-env-introuvable-nomme", gui._resoudre_racine_depot, None)
        # précédence : l'argument GAGNE sur l'environnement
        racine_p, source_p = gui._resoudre_racine_depot(RACINE)
        verifie("x3-precedence-argument-sur-env",
                source_p == "--depot"
                and os.path.abspath(racine_p) == os.path.abspath(RACINE))
        # l'environnement seul résout aussi
        os.environ["TRIADE_DEPOT"] = RACINE
        racine_e, source_e = gui._resoudre_racine_depot(None)
        verifie("x3-env-triade-depot-resolu",
                source_e == "TRIADE_DEPOT"
                and os.path.abspath(racine_e) == os.path.abspath(RACINE))
    finally:
        if env_avant is None:
            os.environ.pop("TRIADE_DEPOT", None)
        else:
            os.environ["TRIADE_DEPOT"] = env_avant

    # définir_racine_depot : tout le profil suit (disponibilité + garde).
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-x3-") as rep:
        gui.definir_racine_depot(rep, "--depot")
        verifie("x3-dossier-sans-v06-fail-ferme",
                not gui.depot_disponible())
        refuse("x3-module-cf2-refuse-hors-depot", gui._module_cf2)
        # un v06 factice SANS coffre_cf2.py ne suffit pas (garde intacte)
        os.makedirs(os.path.join(rep, "v06"), exist_ok=True)
        verifie("x3-v06-factice-incomplet-refuse",
                not gui.depot_disponible())
        gui.definir_racine_depot(RACINE, "--depot")
        verifie("x3-retablissement-depot-disponible",
                gui.depot_disponible() and gui.RACINE_DEPOT == RACINE)
        try:
            gui._module_cf2()      # la pile du dépôt est présente ici
            verifie("x3-module-cf2-charge-une-fois-attache", True)
        except gui.ErreurCeremonie as exc:
            verifie("x3-module-cf2-charge-une-fois-attache", False, str(exc))

    # Le point d'entrée : chemin faux => code 2 avec la cause nommée ;
    # --depot valide + --selftest => la batterie reste verte.
    env = dict(os.environ)
    env.pop("TRIADE_DEPOT", None)
    chemin_gui = os.path.join(RACINE, "v06", "ceremonie_gui.py")
    proc = subprocess.run(
        [sys.executable, chemin_gui, "--selftest",
         "--depot", os.path.join(RACINE, "encore-absent")],
        capture_output=True, text=True, env=env, timeout=300)
    verifie("x3-main-chemin-faux-code-2-nomme",
            proc.returncode == 2 and "dossier introuvable" in proc.stderr,
            f"code={proc.returncode} stderr={proc.stderr[:120]!r}")
    proc = subprocess.run(
        [sys.executable, chemin_gui, "--selftest", "--depot", RACINE],
        capture_output=True, text=True, env=env, timeout=300)
    verifie("x3-main-depot-valide-selftest-vert",
            proc.returncode == 0,
            f"code={proc.returncode} stderr={proc.stderr[:120]!r}")
    env_faux = dict(env)
    env_faux["TRIADE_DEPOT"] = os.path.join(RACINE, "toujours-absent")
    proc = subprocess.run(
        [sys.executable, chemin_gui, "--selftest"],
        capture_output=True, text=True, env=env_faux, timeout=300)
    verifie("x3-main-env-fausse-code-2-nomme",
            proc.returncode == 2 and "TRIADE_DEPOT" in proc.stderr,
            f"code={proc.returncode} stderr={proc.stderr[:120]!r}")
    # état restauré pour les séries suivantes
    gui.definir_racine_depot(gui._racine_depot_defaut(), "position du fichier")


def main() -> int:
    print(f"[test-ceremonie-GUI] falsifiabilité du maître de cérémonie "
          f"(D107 · D109 · D110 · D111 · D112 · D117 · D118 · D119) — "
          f"dépôt {RACINE}")
    t1_ed25519()
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-test-") as rep:
        t234_cle_i(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-cf2-") as rep:
        t567f1(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t8-") as rep:
        t8_phrase_personnelle(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t9-") as rep:
        t9_cle_a_la_main(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t10-") as rep:
        t10_chemins_coffre(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t14-") as rep:
        t14_scenarios_clone(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t15-") as rep:
        t15_fusion_d118(rep)
    with tempfile.TemporaryDirectory(prefix="ceremonie-gui-t16-") as rep:
        t16_dossier_avec_la_cle(rep)
    x1_import_headless()
    x2_coherence_attributs()
    x3_attachement_depot()
    print(f"[test-ceremonie-GUI] {len(PASSES)} PASS / {len(ECHECS)} ÉCHEC")
    if ECHECS:
        for e in ECHECS:
            print(f"  ÉCHEC : {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
