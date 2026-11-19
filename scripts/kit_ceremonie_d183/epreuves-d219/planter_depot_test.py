#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""planter_depot_test.py — LE DÉPÔT DE TEST À SECRETS PLANTÉS (le dry-run
de la PROCÉTURE-SCAN-SECRETS, D219).

Plante DÉTERMINISTEMENT un dépôt git jetable (sous /tmp) avec CINQ secrets
FACTICES clairement construits pour l'épreuve — puis SUPPRIME deux d'entre
eux à la tête : le scan de l'historique complet doit les attraper QUAND
MÊME (c'est la leçon de D81 : un secret commis y demeure à vie). Les
fichiers propres (le bruit zéro) voisinent les plantés.

Les valeurs factices sont ASSEMBLÉES PAR CONCATÉNATION : le présent script
(réputé commis au dépôt réel) ne contient AUCUN motif complet — le scan du
vrai dépôt ne se signale pas lui-même."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

CIBLE = pathlib.Path("/tmp/depot-test-secrets-d219")

# --- les six secrets plantés (factices, assemblés par concaténation) ---
# (les longueurs respectent les seuils des règles : ≥ 36 car. après ghp_,
#  ≥ 27 car. après GOCSPX-, ≥ 28 car. d'assignation, l'en-tête PEM entier)
JETON_GH = ("gh" + "p_" + "FAUXJETONPLANTEPOURDRYRUN" + "X9zK2mQ7vB4nR8tW3cY1uH6")
SECRET_OAUTH = ("GOCSPX-" + "FAUXSECRETPLANTEPOURDRYRUN" + "7kQ2vN9xZ4mJ8")
CLE_API = ("ZFpjX2mQ" + "7vB4nR8tW3cY1uJ5hG" + "9kL2pQw6eR")  # 42 car. + padding
PHRASE = "PHRASE-FAUX-TEST-NON-SECRETE-DRYRUN-D219"
DEBUT_CLE = "-----BEGIN RSA " + "PRIVATE KEY-----"
CORPS_CLE = "MIIEowIBAAOCAQ8AMIIBCgKCAQEAFAUXFAUXFAUXDRYRUN" + "D219x7Qk"


def sh(*args: str, cwd=None):
    return subprocess.run(args, cwd=cwd, capture_output=True, check=True)


def main() -> int:
    if CIBLE.exists():
        sh("rm", "-rf", str(CIBLE))
    CIBLE.mkdir(parents=True)
    sh("git", "init", "-q", str(CIBLE))
    sh("git", "-C", str(CIBLE), "config", "user.email", "labo@triade.test")
    sh("git", "-C", str(CIBLE), "config", "user.name", "labo dry-run")

    def commit(msg: str):
        sh("git", "-C", str(CIBLE), "add", "-A")
        sh("git", "-C", str(CIBLE), "commit", "-q", "-m", msg)

    # --- commit 1 : les fichiers PROPRES (le bruit zéro) + deux plantés ---
    propre = CIBLE / "propre"
    propre.mkdir()
    (propre / "README.md").write_text(
        "# Dépôt de test\n\nOn y parle de jetons (le mot, en prose) et de "
        "secrets dans les phrases, sans jamais en commettre un.\n"
        "Le budget de tokens du projet est consigné au journal.\n",
        encoding="utf-8")
    (propre / "outil.py").write_text(
        'SEUIL = 3.8\nNOM = "outil"\n'
        'def calcule(x):\n    return x * 2 + len(NOM)\n',
        encoding="utf-8")
    (CIBLE / "config.ini").write_text(
        "[application]\nnom = demonstration\n"
        f"client_secret = {SECRET_OAUTH}\n",
        encoding="utf-8")
    (CIBLE / "reglages.py").write_text(
        f"API_KEY = '{CLE_API}=='  # la fausse clé plantée (padding base64)\n"
        "SEUIL = 3\n",
        encoding="utf-8")
    env = CIBLE / ".env"
    env.write_text("MODE=test\n", encoding="utf-8")
    commit("commit 1 : fichiers propres + config, reglages et env")

    # --- commit 2 : les trois autres plantés ---
    (CIBLE / "token_helper.py").write_text(
        f"JETON = '{JETON_GH}'  # le faux jeton planté\n"
        "def aide():\n    return JETON[:4]\n",
        encoding="utf-8")
    notes = CIBLE / "notes"
    notes.mkdir()
    (notes / "cle-serveur.txt").write_text(
        f"la clé du serveur de test :\n{DEBUT_CLE}\n{CORPS_CLE}\n"
        "-----END RSA PRIVATE KEY-----\n",
        encoding="utf-8")
    (CIBLE / "PHRASE-CONTROLE-COFFRE.txt").write_text(PHRASE + "\n",
                                                      encoding="utf-8")
    commit("commit 2 : trois secrets de plus")

    # --- commit 3 : SUPPRESSION de deux plantés à la tête ---
    (CIBLE / "token_helper.py").unlink()
    (notes / "cle-serveur.txt").unlink()
    (CIBLE / "propre" / "suite.md").write_text(
        "Suite propre : le contenu supprimé demeure à l'historique.\n",
        encoding="utf-8")
    commit("commit 3 : deux secrets supprimés de la tête (l'historique demeure)")

    # --- le manifeste des attendus (l'assertion du dry-run) ---
    attends = [
        {"regle": "SECRET-OAUTH-GOOGLE", "fragment": "config.ini"},
        {"regle": "ASSIGNATION-SECREE", "fragment": "reglages.py"},
        {"regle": "JETON-GITHUB", "fragment": "token_helper.py"},
        {"regle": "CLE-PRIVEE", "fragment": "cle-serveur.txt"},
        {"regle": "PHRASE-CONTROLE", "fragment": "PHRASE-CONTROLE-COFFRE.txt"},
        {"regle": "FICHIER-JETON", "fragment": ".env"},
    ]
    manifeste = pathlib.Path(__file__).parent / "attendus-dryrun.json"
    manifeste.write_text(json.dumps(attends, indent=1), encoding="utf-8")

    nb = subprocess.run(["git", "-C", str(CIBLE), "rev-list", "--count",
                         "HEAD"], capture_output=True, check=True
                        ).stdout.decode().strip()
    print(f"DÉPÔT DE TEST planté : {CIBLE} ({nb} commits)")
    print(f"  secrets plantés    : 6 (dont 2 SUPPRIMÉS de la tête)")
    print(f"  fichiers propres   : propre/README.md, propre/outil.py, "
          "propre/suite.md")
    print(f"  manifeste d'attendus : {manifeste.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
