#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""push_session_321_git.py — LE GESTE GIT DE LA SESSION 321 : le work clone
depuis le miroir GitHub, l'Entrée 321 consignée au worklog, les TROIS
scripts de session copiés, le commit (l'identité établie du projet), le push
GitHub (main), le miroir mis à jour, le bundle --all créé.
Le jeton vit dans /tmp/git-credentials (600, hors du dépôt, jamais affiché).
"""
import os
import shutil
import subprocess
import sys

MIROIR = "/tmp/triade-mirror.git"
TRAVAIL = "/tmp/triade-work"
DEPOT = "https://github.com/alexisfrlopez-debug/triade.git"
CRED = "/tmp/git-credentials"
BUNDLE = "/tmp/triade-history-321.bundle"
AUTEUR = ("Alexis Lopez "
          "<alexisfrlopez-debug@users.noreply.github.com>")

ENTREE_321 = """
## Task 221 — Entrée 321 : LA VAGUE 5 LIVRÉE AU COFFRE ET LES DIX
INSTRUCTIONS ARCHIVÉES (le jeton relais frais du /Tokens — la règle
permanente a servi ; le gap nommé de l'Entrée 320 FERMÉ)

Work Log:
- LE JETON RELAIS RAPATRIÉ du /Tokens du coffre (gdrive_tokens.py, la
  règle permanente du 16/11 : LA première vérification en cas de problème
  d'accès) : les QUATRE fichiers posés dans tokens/, AUCUNE valeur
  affichée, JAMAIS committés (.gitignore) ; la sonde OAuth VERTE — le
  /test répond (23 entrées), la voie d'écriture revenue.
- LA LIVRAISON À LA RACINE DU COFFRE (livraison_vague5_relais.py, la voie
  d'écriture OAuth, fail-closed à chaque geste : recoup AVANT, écriture,
  relecture recoupée) : le manuscrit TRIADE_manuscrit_v0.18.0.pdf
  (224 774 o), l'archive soumission (228 299 o), l'archive complète
  (376 593 o), le rapport d'exécution (13 571 o), le rapport de
  vérification v0.18.0 (3 449 o), les empreintes v0.18.0 (644 o) — CHAQUE
  pièce RECROUPÉE md5 par re-téléchargement après dépôt ; D143 : l'empreinte
  v0.17.0 de la racine RENOMMÉE empreintes_livrables_v0.17.0.txt avant de
  poser la v0.18.0 au nom générique (md5 recoupé au renommage).
- L'ARCHIVAGE DES DIX INSTRUCTIONS : /instructions → /ARCHIVE/
  instructions_20261116/ — 10/10 md5 recoupés AVANT le déplacement (les
  copies d'instructions-recu/), re-téléchargées et recoupées APRÈS ; le
  rapport d'exécution déposé à leurs côtés ; LE /INSTRUCTIONS VIDE
  (0 restant), l'archive à SES 19 entrées (le lot de huit + les dix + le
  rapport).
- LE PUSH MIROIR COMPLÉTÉ (les DEUX à chaque push — la règle) : le dépôt
  GitHub retrouvé (la pointe a5be18a — les archives finales v0.18.0 ;
  de44d55/af230c7 : l'Entrée 320 et son correctif honnête), le clone
  miroir reconstruit DEPUIS GITHUB SEUL (le bac recyclé avait perdu
  l'historique local — un commit initial seul : le bundle N'A JAMAIS été
  régénéré depuis le bac, l'ancien de 319 Mo remplacé sur un état COMPLET
  à jour), cette entrée consignée, le bundle --all remplacé au
  TRIADE-sauvegarde-git + le nom versionné triade-history-321.bundle, le
  worklog REMPLACÉ — recoupés par re-téléchargement.
(17/11, la session de la livraison au coffre)
"""

MESSAGE = ("Entrée 321 : LA VAGUE 5 LIVRÉE AU COFFRE — les dix instructions "
           "archivées 10/10 md5 recoupés, le manuscrit v0.18.0 + les deux "
           "archives + les rapports + empreintes déposés à la racine et "
           "recoupés byte-byte, D143 : l'empreinte v0.17.0 renommée, le "
           "bundle et le worklog remplacés au TRIADE-sauvegarde-git (le "
           "jeton relais frais du /Tokens — la règle permanente)")


def run(cmd, cwd=None, capture=True):
    r = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)
    if r.returncode != 0:
        print(f"[ROUGE] {' '.join(cmd[:4])}… : "
              f"{(r.stderr or r.stdout).strip()[:400]}")
        sys.exit(1)
    return r.stdout


def main():
    # 1) le work clone depuis le miroir
    if os.path.exists(TRAVAIL):
        shutil.rmtree(TRAVAIL)
    run(["git", "clone", MIROIR, TRAVAIL])
    print("[VERT] le work clone né depuis le miroir GitHub")

    # 2) les TROIS scripts de session copiés
    for script in ("etat_coffre.py", "configurer_git_relais.py",
                   "livraison_vague5_relais.py"):
        shutil.copy(f"/home/z/my-project/scripts/{script}",
                    f"{TRAVAIL}/scripts/{script}")
    print("[VERT] les trois scripts de session copiés (scripts/)")

    # 3) l'Entrée 321 consignée (append-only)
    with open(f"{TRAVAIL}/worklog.md", "a", encoding="utf-8") as f:
        f.write(ENTREE_321)
    taille = os.path.getsize(f"{TRAVAIL}/worklog.md")
    print(f"[VERT] l'Entrée 321 consignée au worklog "
          f"({taille:,} o au total)".replace(",", " "))

    # 4) le commit (l'identité établie)
    run(["git", "-C", TRAVAIL, "add", "worklog.md", "scripts/"])
    run(["git", "-C", TRAVAIL, "-c", f"user.name=Alexis Lopez",
         "-c", "user.email=alexisfrlopez-debug@users.noreply.github.com",
         "commit", "-m", MESSAGE])
    pointe = run(["git", "-C", TRAVAIL, "rev-parse", "--short", "HEAD"]).strip()
    print(f"[VERT] le commit de session : {pointe}")

    # 5) le push GitHub (main)
    run(["git", "-C", TRAVAIL, "-c",
         f"credential.helper=store --file={CRED}",
         "push", DEPOT, "main:main"])
    distant = run(["git", "-C", TRAVAIL, "-c",
                   f"credential.helper=store --file={CRED}",
                   "ls-remote", DEPOT, "refs/heads/main"]).strip()
    local = run(["git", "-C", TRAVAIL, "rev-parse", "main"]).strip()
    print(f"[{'VERT' if distant == local else 'ROUGE'}] le push GitHub : "
          f"main == {distant[:12]}… ({'identique' if distant == local else 'DIVERGE'})")

    # 6) le miroir mis à jour + le bundle --all
    run(["git", "-C", MIROIR, "fetch", TRAVAIL,
         f"refs/heads/main:refs/heads/main"])
    if os.path.exists(BUNDLE):
        os.remove(BUNDLE)
    run(["git", "-C", MIROIR, "bundle", "create", BUNDLE, "--all"])
    taille_bundle = os.path.getsize(BUNDLE)
    print(f"[VERT] le bundle --all né : {BUNDLE} "
          f"({taille_bundle:,} o)".replace(",", " "))
    tete_bundle = run(["git", "-C", MIROIR, "bundle", "list-heads",
                       BUNDLE]).strip().splitlines()
    for ligne in tete_bundle:
        print(f"  pointe du bundle : {ligne[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
