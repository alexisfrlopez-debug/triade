#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Déploiement CANONIQUE du KIT de cérémonie (dossier « Cérémonie »).

D130 — LE KIT NE DÉRIVE PLUS DU MIROIR. Constat fondateur (retour du
terrain du 30/10) : « le dossier du drive /cérémonie et
/TRIADE-sauvegarde-git/V06 ont encore des contenus différents, ça porte
à confusion ». Cause racine : le MIROIR git se synchronise à CHAQUE
COMMIT (hook post-commit → drive_sync.py) mais le KIT ne se mettait à
jour que MANUELLEMENT (maj_kit_d122…d128.py) — dès qu'une décision
touchait v06/ sans relancer le dépôt manuel, le kit reprennait un coup
de retard (arrivé à D129 : le miroir portait le pilier droit, le kit
non). Le correctif est STRUCTUREL :

  1. le v06/ du kit est déployé DEPUIS `git ls-files v06/` — la MÊME
     source que le miroir (drive_sync.py) : identité par construction,
     octet pour octet, y compris I/ et sceau-I/ (les arbres du sceau) ;
  2. ce script est appelé par le hook post-commit IMMÉDIATEMENT APRÈS
     drive_sync.py : les deux dossiers sont rafraîchis dans le MÊME
     geste, sur le MÊME arbre de travail — plus de fenêtre de dérive ;
  3. MANIFESTE.txt porte le COMMIT de référence : le terrain peut
     toujours dire à quelle génération son kit correspond.

Racine du kit (ce que le miroir n'a pas) : copies plates de
ceremonie_gui.py / ceremonie_hors_ligne.py (posture « fichier seul sur
clef USB », D87), coffre_fort.py (CF1), lanceurs .bat/.sh (D118),
LISEZMOI-*.txt (download/ du labo — ignorés sans échec ailleurs).

Propriétés :
  - idempotent : md5 identique → aucun téléversement ;
  - prudent : ne supprime JAMAIS rien côté Drive ;
  - sûr : aucun secret (les arbres sceau-I/ ne portent que des preuves
    publiques : remise, clé PUBLIQUE, état, manifestes, signatures) ;
  - vérifié : aller-retour md5 de TOUTES les entrées après dépôt ;
  - autonome : réutilise drive_sync.py (stdlib uniquement).

Usage :
  python3 scripts/maj_kit.py            # dépose + vérifie (verbeux)
  python3 scripts/maj_kit.py --quiet    # mode hook (bilan seul)
Code de sortie : 0 = vert, 1 = divergences, 2 = erreur fatale nommée.
"""

import argparse
import datetime
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ESPACE = pathlib.Path("/home/z/my-project")
DOWNLOAD = ESPACE / "download"
JOURNAL = ESPACE / "scripts" / "maj_kit.log"
DOSSIER = "Cérémonie"
SOUS_V06 = "v06"

# Racine du kit : (nom distant, chemin local, requis) — les LISEZMOI
# vivent dans download/ (labo) : absents ailleurs → ignorés SANS échec
# (jamais supprimés côté Drive pour autant).
RACINE_KIT = [
    ("ceremonie_gui.py", REPO / "v06" / "ceremonie_gui.py", True),
    ("ceremonie_hors_ligne.py", REPO / "v06" / "ceremonie_hors_ligne.py", True),
    ("coffre_fort.py", REPO / "coffre_fort.py", True),
    ("lancer_ceremonie.bat", REPO / "lancer_ceremonie.bat", True),
    ("lancer_ceremonie.sh", REPO / "lancer_ceremonie.sh", True),
    ("lancer_autotest_cf3.bat", REPO / "lancer_autotest_cf3.bat", True),
    ("lancer_autotest_cf3.sh", REPO / "lancer_autotest_cf3.sh", True),
    ("lancer_migration_cf3.bat", REPO / "lancer_migration_cf3.bat", True),
    ("lancer_migration_cf3.sh", REPO / "lancer_migration_cf3.sh", True),
    ("LISEZMOI-ceremonie-GUI.txt", DOWNLOAD / "LISEZMOI-ceremonie-GUI.txt", False),
    ("LISEZMOI-cle-I.txt", DOWNLOAD / "LISEZMOI-cle-I.txt", False),
    ("LISEZMOI-coffre-CF2.txt", DOWNLOAD / "LISEZMOI-coffre-CF2.txt", False),
    ("LISEZMOI-coffre-CF3.txt", DOWNLOAD / "LISEZMOI-coffre-CF3.txt", False),
    ("LISEZMOI-kit.txt", DOWNLOAD / "LISEZMOI-kit.txt", False),
    # L'ÈRE M8 (M8-(c), D162) : la cérémonie de re-signature m0 + m8 — la
    # remise fraîche vit déjà dans v06/sceau-I/a-signer.txt (source git) ;
    # ce LISEZMOI est le mode d'emploi qui va avec (règle d'or : JAMAIS
    # « generer », la clé du 04/11 est réutilisée — 173fae9c…).
    ("LISEZMOI-ceremonie-ere-M8.txt",
     DOWNLOAD / "LISEZMOI-ceremonie-ere-M8.txt", False),
    # LE BUILD 1.0.0 (chantier (e) M9, Task 95) : la cérémonie de
    # re-signature m8 + tls13 qui PRÉCÈDE construire() — la notation est
    # COMPLÈTE (les 28 blocs + le socle socket), la couche I est FINALE,
    # la remise fraîche vit dans v06/sceau-I/a-signer.txt (source git,
    # 13 arbres) ; ce LISEZMOI est le mode d'emploi qui va avec (règle
    # d'or : JAMAIS « generer », la clé du 04/11 est réutilisée —
    # 173fae9c…).
    ("LISEZMOI-ceremonie-build-1.0.0.txt",
     DOWNLOAD / "LISEZMOI-ceremonie-build-1.0.0.txt", False),
    # LA RE-CÉRÉMONIE DE LA RÉVISION 2 (Entrée 186, la rangée (f)) : la
    # révision 2 de la spec sys-05 (le WSABUF canonique 16 o — la mesure
    # de la sonde, Entrée 185 : 0xC0000005) fait évoluer l'arbre m8 : la
    # remise régénérée (m8 3e778fa0…) attend la signature HORS LIGNE du
    # développeur AVANT le rebuild 1.0.0-dev.3 (construire() suit le
    # garde VERT — LE SIGNAL, pas la panne) ; ce LISEZMOI est le mode
    # d'emploi qui va avec (règle d'or : JAMAIS « generer », la clé du
    # 04/11 est réutilisée — 173fae9c…).
    ("LISEZMOI-ceremonie-revision2-sys05.txt",
     DOWNLOAD / "LISEZMOI-ceremonie-revision2-sys05.txt", False),
]

NOTE_D130 = (
    "KIT UNIQUE DE CÉRÉMONIE TRIADE — D130 : LE KIT NE DÉRIVE PLUS DU\n"
    "MIROIR. Le sous-dossier v06/ de CE dossier est EXACTEMENT le v06/\n"
    "du dépôt git (git ls-files v06/) : mêmes fichiers, mêmes empreintes\n"
    "que « TRIADE-sauvegarde-git/v06 », octet pour octet — y compris I/\n"
    "(la spec scellée) et sceau-I/ (les preuves publiques du sceau :\n"
    "remise, clé publique, état, manifestes, signatures — AUCUN secret).\n"
    "Il est rafraîchi À CHAQUE COMMIT, dans le MÊME geste que le miroir\n"
    "(hook post-commit : drive_sync.py PUIS maj_kit.py) : les deux\n"
    "dossiers ne peuvent plus diverger d'une génération de code.\n"
    "La RACINE du kit reste propre au kit : lanceurs .bat/.sh, copies\n"
    "plates (posture « fichier seul sur clef USB » D87), coffre_fort.py\n"
    "(CF1), LISEZMOI-*.txt, MANIFESTE.txt.\n"
    "Entrée : double-cliquez lancer_ceremonie (le maître de cérémonie\n"
    "v2.2 — pilier droit D129 : la liste des étapes et le journal vivent\n"
    "dans l'encart à droite, visibles quel que soit l'onglet ; D131 : le\n"
    "bouton d'attachement vit UNE fois par page — l'ex doublon de\n"
    "l'accueil est mort),\n"
    "lancer_autotest_cf3 (prouver la serrure CF3) ou\n"
    "lancer_migration_cf3 (migrer le coffre réel CF2 → CF3, spec § 12).\n"
    "En cas de problème : bouton « Envoyer le rapport… » dans le GUI,\n"
    "glissez le .txt dans la conversation (règle systématique D122).\n"
    "Le sceau I signe l'INTENTION (v06/I/ — spec CF2/CF3, table\n"
    "normative), PAS le code : une évolution du code (D131 aujourd'hui)\n"
    "ne diverge RIEN — seule une évolution de v06/I/ appellerait la\n"
    "re-cérémonie (verifier le dirait : « signature requise » sur v06 —\n"
    "le SIGNAL, pas la panne).\n"
    "\n"
    "RE-CÉRÉMONIE DE LA RÉVISION 2 (Entrée 186, la suite du chantier\n"
    "(f)) : la révision 2 de la spec sys-05 (le WSABUF canonique 16 o —\n"
    "la mesure de la sonde, Entrée 185) a fait évoluer l'arbre m8 : le\n"
    "garde REFUSE le rebuild 1.0.0-dev.3 (LE SIGNAL « signature\n"
    "requise », pas la panne). Suivez LISEZMOI-ceremonie-revision2-\n"
    "sys05.txt : la remise est v06/sceau-I/a-signer.txt (TREIZE arbres,\n"
    "UNE seule empreinte nouvelle — m8 3e778fa0…), à signer HORS LIGNE\n"
    "avec votre clé du 04/11 — la règle d'or : JAMAIS « generer » (la\n"
    "clé 173fae9c… est réutilisée). Le dépôt de signatures-I.txt au\n"
    "/test débloque : LE REBUILD 1.0.0-dev.3 (le bloc sys-05 réparé),\n"
    "LE KIT M9F RÉPARÉ au /test, le run du développeur — ET SI LE VERT\n"
    "TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE ŒUVRE.")


# ---------------------------------------------------------------- utilitaires

def journaliser(texte, quiet=False):
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"[{horodatage}] {texte}"
    if not quiet:
        print(ligne)
    try:
        JOURNAL.parent.mkdir(parents=True, exist_ok=True)
        with open(JOURNAL, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")
    except OSError:
        pass  # le journal d'audit est un témoin, pas une dépendance


def commit_courant():
    out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                         cwd=REPO, capture_output=True, text=True)
    return out.stdout.strip() or "aucun-commit"


def fichiers_git_v06():
    """v06/ suivi par git -> {nom distant kit: chemin local} (source miroir)."""
    out = subprocess.run(["git", "ls-files", "-z", "--", "v06/"],
                         cwd=REPO, capture_output=True)
    fichiers = {}
    for rel in out.stdout.decode(errors="replace").split("\0"):
        if not rel:
            continue
        chemin = REPO / rel
        if chemin.is_file():
            fichiers[f"{SOUS_V06}/{rel[len('v06/'):]}"] = chemin
    return fichiers


def carte_du_kit(folder_id, prefix=""):
    """Carte {nom relatif: métadonnées} du dossier kit (récursive)."""
    carte = {}
    for f in ds.list_folder(folder_id).values():
        if f.get("mimeType") == ds.FOLDER_MIME:
            carte.update(carte_du_kit(f["id"], prefix + f["name"] + "/"))
        else:
            carte[prefix + f["name"]] = f
    return carte


# ---------------------------------------------------------------- manifeste

def constituer_manifeste(emp, commit):
    lignes = [
        "MANIFESTE du KIT UNIQUE DE CÉRÉMONIE TRIADE (D130)",
        "=" * 62,
        NOTE_D130,
        "=" * 62,
        f"Commit de référence : {commit} — le v06/ de ce kit est identique",
        "octet pour octet à TRIADE-sauvegarde-git/v06 à CE commit.",
        f"Généré le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} — empreintes md5 :",
        "",
    ]
    for nom, valeur in emp.items():
        lignes.append(f"{valeur}  {nom}")
    lignes += [
        "",
        "MANIFESTE.txt : ce fichier même — non listé (auto-référence).",
        "Un fichier qui diverge de son empreinte est un kit altéré :",
        "ne lancez rien, signalez-le.",
        "",
        "AUCUN SECRET ICI : ni clé privée, ni phrase de contrôle, ni",
        "coffre. sceau-I/ ne porte que des preuves publiques.",
    ]
    return "\n".join(lignes) + "\n"


# ---------------------------------------------------------------- gardes

def gardes(quiet):
    problemes = []
    for nom, chemin, requis in RACINE_KIT:
        if requis and not chemin.is_file():
            problemes.append(f"{nom} absent ({chemin})")
    if problemes:
        raise ds.SyncError("gardes rouges : " + " ; ".join(problemes))
    # copies plates : la racine du kit EST v06/ (une seule vérité) ;
    # la copie de la zone download/ du labo se répare d'elle-même.
    for nom in ("ceremonie_gui.py", "ceremonie_hors_ligne.py"):
        source = REPO / "v06" / nom
        copie = DOWNLOAD / nom
        if copie.parent.is_dir():
            if copie.is_file() and ds.md5_of(copie) != ds.md5_of(source):
                copie.write_bytes(source.read_bytes())
                journaliser(f"zone download/ réparée : {nom} "
                            "resynchronisé sur v06/", quiet)
            elif not copie.is_file():
                copie.write_bytes(source.read_bytes())
                journaliser(f"zone download/ complétée : {nom}", quiet)
    n_v06 = len(fichiers_git_v06())
    journaliser(f"gardes vertes : {n_v06} fichiers v06/ suivis par git, "
                f"{sum(1 for _, _, r in RACINE_KIT if r)} fichiers racine",
                quiet)
    return n_v06


# ---------------------------------------------------------------- dépôt

def trouver_dossier_ceremonie():
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)   # valide aussi le jeton
    trouves = [f for f in racine.values()
               if f.get("mimeType") == ds.FOLDER_MIME and f["name"] == DOSSIER]
    if not trouves:
        raise ds.SyncError(
            f"dossier « {DOSSIER} » introuvable à la racine du Drive "
            f"« Triade » — créez-le ou reprenez maj_kit_d128.py")
    return trouves[0]["id"]


def deployer(quiet=False):
    commit = commit_courant()
    journaliser(f"=== déploiement du kit (D130) — commit {commit} ===",
                quiet)
    gardes(quiet)

    cibles = {}
    cibles.update(fichiers_git_v06())           # v06/ == miroir, par construction
    for nom, chemin, requis in RACINE_KIT:
        if chemin.is_file():
            cibles[nom] = chemin
        elif not requis:
            journaliser(f"note : {nom} absent localement — "
                        "conservé tel quel côté Drive", quiet)

    manifeste_txt = constituer_manifeste(
        {nom: ds.md5_of(c) for nom, c in sorted(cibles.items())}, commit)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="maj_kit_"))
    chemin_man = tmp / "MANIFESTE.txt"
    chemin_man.write_text(manifeste_txt, encoding="utf-8")
    if DOWNLOAD.is_dir():                       # copie d'audit du labo
        (DOWNLOAD / "MANIFESTE.txt").write_text(manifeste_txt,
                                                encoding="utf-8")
    cibles["MANIFESTE.txt"] = chemin_man

    cer_id = trouver_dossier_ceremonie()
    dist = carte_du_kit(cer_id)
    journaliser(f"{len(cibles)} entrées attendues "
                f"({len(dist)} déjà présentes au total)", quiet)

    cache = {}

    def parent_de(nom):
        """Id du dossier Drive parent d'une entrée (crée la chaîne)."""
        parties = pathlib.PurePosixPath(nom).parts[:-1]
        parent = cer_id
        for partie in parties:
            parent = ds.ensure_folder(parent, partie, cache)
        return parent

    televerses, maj, inchanges, erreurs = 0, 0, 0, []
    for nom, chemin in sorted(cibles.items()):
        md5 = ds.md5_of(chemin)
        distant = dist.get(nom)
        if distant and distant.get("md5Checksum") == md5:
            inchanges += 1
            continue
        try:
            if distant:
                ds.upload_update(distant["id"], chemin)
                maj += 1
                journaliser(f"mis à jour : {nom}", quiet)
            else:
                ds.upload_create(parent_de(nom),
                                 pathlib.PurePosixPath(nom).name, chemin)
                televerses += 1
                journaliser(f"téléversé : {nom}", quiet)
        except ds.SyncError as exc:
            erreurs.append(nom)
            journaliser(f"ERREUR {nom} : {exc}", quiet)

    # ---------------- vérification aller-retour (la preuve du dépôt)
    journaliser("— vérification aller-retour md5 —", quiet)
    fin = carte_du_kit(cer_id)
    attendus = {nom: ds.md5_of(c) for nom, c in cibles.items()}
    divergents = [nom for nom, md5 in sorted(attendus.items())
                  if fin.get(nom, {}).get("md5Checksum") != md5]
    for nom in divergents:
        journaliser(f"ÉCHEC : {nom} — distant "
                    f"{fin.get(nom, {}).get('md5Checksum', 'ABSENT')} "
                    f"≠ local {attendus[nom]}", quiet)

    journaliser(
        f"KIT D130 déployé (commit {commit}) : {televerses} téléversés, "
        f"{maj} mis à jour, {inchanges} inchangés, "
        f"{len(attendus) - len(divergents)}/{len(attendus)} vérifiés "
        f"aller-retour", quiet)
    if divergents or erreurs:
        journaliser(f"DIVERGENCES : {divergents or erreurs}", quiet)
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="Déploiement du kit de cérémonie (D130) — v06/ "
                    "identique au miroir git, par construction")
    ap.add_argument("--quiet", action="store_true",
                    help="mode hook : bilan seul au stdout, tout au journal")
    args = ap.parse_args()
    try:
        return deployer(quiet=args.quiet)
    except ds.SyncError as exc:
        journaliser(f"ÉCHEC NOMMÉ : {exc}", args.quiet)
        if not args.quiet:
            print("Parades : (1) le refresh OAuth relais expire ~05/11 — "
                  "reprenez-le (scripts/oauth_echange.py) ; (2) partagez le "
                  "dossier en Éditeur au compte de service ; (3) le compte "
                  "de service seul est LECTEUR — il ne peut pas écrire.",
                  file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
