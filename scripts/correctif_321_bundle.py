#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""correctif_321_bundle.py — LE CORRECTIF HONNÊTE DE L'ENTRÉE 321 : la
découverte nommée — l'ancien triade-history.bundle du coffre (319 Mo) est
une LIGNÉE ORPHELINE (20 commits, aucun ancêtre commun avec l'histoire
canonique), pas un état antérieur de main. Le récit de l'Entrée 321 corrigé,
le commit poussé, le miroir mis à jour, le bundle régénéré.
"""
import hashlib
import os
import subprocess
import sys

TRAVAIL = "/tmp/triade-work"
MIROIR = "/tmp/triade-mirror.git"
DEPOT = "https://github.com/alexisfrlopez-debug/triade.git"
CRED = "/tmp/git-credentials"
BUNDLE = "/tmp/triade-history-321-ee65b6a.bundle"

ANCIEN_BULLET = """- LE PUSH MIROIR COMPLÉTÉ (les DEUX à chaque push — la règle) : le dépôt
  GitHub retrouvé (la pointe a5be18a — les archives finales v0.18.0 ;
  de44d55/af230c7 : l'Entrée 320 et son correctif honnête), le clone
  miroir reconstruit DEPUIS GITHUB SEUL (le bac recyclé avait perdu
  l'historique local — un commit initial seul : le bundle N'A JAMAIS été
  régénéré depuis le bac, l'ancien de 319 Mo remplacé sur un état COMPLET
  à jour), cette entrée consignée, le bundle --all remplacé au
  TRIADE-sauvegarde-git + le nom versionné triade-history-321.bundle, le
  worklog REMPLACÉ — recoupés par re-téléchargement."""

NOUVEAU_BULLET = """- LE PUSH MIROIR COMPLÉTÉ (les DEUX à chaque push — la règle) : le dépôt
  GitHub retrouvé (la pointe a5be18a — les archives finales v0.18.0 ;
  de44d55/af230c7 : l'Entrée 320 et son correctif honnête), le clone
  miroir reconstruit DEPUIS GITHUB SEUL — L'HISTOIRE CANONIQUE (415
  commits, de 86d1bcf à la pointe de session). LA DÉCOUVERTE NOMMÉE (le
  correctif honnête, le précédent af230c7) : l'ancien triade-history.bundle
  du coffre (319 Mo, 16/11 18:15) n'est PAS un ancêtre de l'histoire
  canonique — UNE LIGNÉE ORPHELINE de 20 commits (la récupération des bacs
  recyclés du 16/11 : « la lignée du matin restaurée », des instantanés
  d'arbres entiers d'où les 319 Mo ; pointe 3d94489 « la vague 4 exécutée »,
  refuges refs/bundles/b312 et h306), AUCUN ancêtre commun avec main — le
  remplacer à même les octets eût détruit la seule copie coffre de cette
  lignée ; D143 : les octets anciens PRÉSERVÉS, copiés aux archives-bundles/
  renommés triade-history-319-3d94489.bundle (md5 recoupé au téléchargement
  préalable), le slot générique (l'id de la règle permanente) porte
  désormais l'histoire canonique complète + cette entrée, le nom versionné
  triade-history-321-ee65b6a.bundle posé à côté (le précédent 308/311/312) ;
  le worklog du coffre REMPLACÉ — l'ancien RECROUPÉ byte-identique à
  l'état pré-320 de GitHub (dc51bb7), RIEN perdu, la continuité tenue ;
  le tout recoupé aux md5 du coffre."""

MESSAGE = ("Entrée 321 (correctif honnête) : l'ancien bundle du coffre est "
           "une LIGNÉE ORPHELINE (20 commits, aucun ancêtre commun avec "
           "l'histoire canonique de 415 commits) — les octets préservés aux "
           "archives-bundles renommés triade-history-319-3d94489.bundle, le "
           "slot générique porte l'histoire canonique + l'Entrée 321, le "
           "worklog remplacé (l'ancien byte-identique au pré-320 de GitHub)")


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ROUGE] {' '.join(cmd[:4])}… : "
              f"{(r.stderr or r.stdout).strip()[:400]}")
        sys.exit(1)
    return r.stdout


def main():
    chemin = f"{TRAVAIL}/worklog.md"
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    if ANCIEN_BULLET not in texte:
        print("[ROUGE] le bullet à corriger est introuvable — REFUS")
        return 1
    texte = texte.replace(ANCIEN_BULLET, NOUVEAU_BULLET)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    print("[VERT] l'Entrée 321 corrigée — la lignée orpheline nommée")

    run(["git", "-C", TRAVAIL, "add", "worklog.md"])
    run(["git", "-C", TRAVAIL, "-c", "user.name=Alexis Lopez",
         "-c", "user.email=alexisfrlopez-debug@users.noreply.github.com",
         "commit", "-m", MESSAGE])
    pointe = run(["git", "-C", TRAVAIL, "rev-parse", "--short", "HEAD"]).strip()
    print(f"[VERT] le correctif commité : {pointe}")

    run(["git", "-C", TRAVAIL, "-c",
         f"credential.helper=store --file={CRED}",
         "push", DEPOT, "main:main"])
    distant = run(["git", "-C", TRAVAIL, "-c",
                   f"credential.helper=store --file={CRED}",
                   "ls-remote", DEPOT, "refs/heads/main"]).split()[0]
    local = run(["git", "-C", TRAVAIL, "rev-parse", "main"]).strip()
    print(f"[{'VERT' if distant == local else 'ROUGE'}] le push GitHub : "
          f"main == {distant[:12]}… "
          f"({'identique' if distant == local else 'DIVERGE'})")

    run(["git", "-C", MIROIR, "fetch", TRAVAIL,
         "refs/heads/main:refs/heads/main"])
    if os.path.exists(BUNDLE):
        os.remove(BUNDLE)
    run(["git", "-C", MIROIR, "bundle", "create", BUNDLE, "--all"])
    h = hashlib.md5(open(BUNDLE, "rb").read()).hexdigest()
    print(f"[VERT] le bundle régénéré : {BUNDLE} "
          f"({os.path.getsize(BUNDLE):,} o, md5 {h[:12]}…)"
          .replace(",", " "))
    return 0


if __name__ == "__main__":
    sys.exit(main())
