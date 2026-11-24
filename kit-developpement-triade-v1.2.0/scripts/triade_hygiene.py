#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scanner d'hygiène de publication — Protocole Triade.

Dernier filet automatique avant toute publication publique (cérémonies C4 et
C5). Détecte les motifs de jetons courants et les fichiers sensibles présents
dans le périmètre scanné. Ne remplace jamais la relecture humaine : il ne voit
ni les captures d'écran, ni les PDF embarqués, ni les métadonnées.

Usage :
    python3 scripts/triade_hygiene.py [chemin] [--json]

Codes retour : 0 = rien détecté ; 1 = au moins une alerte ; 2 = erreur d'usage.
Faux positifs assumés : ajouter « # triade:autorisé » en fin de ligne concernée
(à documenter dans la fiche de cérémonie).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

MARQUEUR_AUTORISE = "triade:autorisé"
DOSSIERS_IGNORES = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    ".mypy_cache", ".pytest_cache", ".idea", ".vscode",
}
TAILLE_MAX_OCTETS = 2 * 1024 * 1024  # 2 Mo

MOTIFS: list[tuple[str, re.Pattern[str]]] = [
    ("Clé d'API Google", re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("Jeton d'accès Google", re.compile(r"ya29\.[0-9A-Za-z_\-]{20,}")),
    ("Jeton GitHub", re.compile(r"\bgh[posuv]_[0-9A-Za-z]{36}\b")),
    ("Jeton GitHub fine-grained", re.compile(r"\bgithub_pat_[0-9A-Za-z_]{22,}\b")),
    ("Clé privée (PEM)", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Jeton Slack", re.compile(r"\bxox[baprs]-[0-9A-Za-z\-]{10,}")),
    ("Jeton Bearer", re.compile(r"(?i)\bbearer\s+[0-9A-Za-z_\-\.=]{20,}")),
    (
        "Affectation de secret",
        re.compile(
            r"(?i)\b[a-z0-9_]*(?:token|jeton|secret|password|"
            r"mot_de_passe|motdepasse|api_?key)"
            r"\s*[:=]\s*['\"]?[0-9A-Za-z_\-\.=/+]{16,}"
        ),
    ),
]


def masque(extrait: str) -> str:
    """N'affiche jamais plus de 4 caractères d'un extrait suspect."""
    return extrait[:4] + "…" if len(extrait) > 8 else "…"


def nom_fichier_suspect(chemin: Path) -> str | None:
    nom = chemin.name.lower()
    if nom.startswith(".env") and "example" not in nom:
        return "fichier .env présent dans le périmètre scanné"
    if nom.startswith("config.") and nom.endswith(".json") and "example" not in nom:
        return "fichier config.json présent dans le périmètre scanné"
    if nom.endswith((".pem", ".key", ".token", ".p12", ".pfx")):
        return "fichier d'identifiants ou de clés"
    if "credential" in nom or "client_secret" in nom or "oauth_token" in nom:
        return "nom de fichier évoquant des identifiants"
    if "token" in nom:
        return "nom de fichier à vérifier (contient « token »)"
    return None


def est_binaire(chemin: Path) -> bool:
    try:
        with chemin.open("rb") as f:
            return b"\x00" in f.read(1024)
    except OSError:
        return True


def scanner(racine: Path) -> tuple[list[dict], int]:
    """Parcourt le périmètre et renvoie (alertes, nombre de fichiers texte lus)."""
    alertes: list[dict] = []
    fichiers_scannes = 0
    for dossier, sous_dossiers, fichiers in os.walk(racine):
        sous_dossiers[:] = [d for d in sous_dossiers if d not in DOSSIERS_IGNORES]
        for nom in fichiers:
            chemin = Path(dossier) / nom
            motif_nom = nom_fichier_suspect(chemin)
            if motif_nom:
                alertes.append(
                    {"type": "fichier", "motif": motif_nom,
                     "fichier": str(chemin), "ligne": "", "extrait": ""}
                )
            try:
                if chemin.stat().st_size > TAILLE_MAX_OCTETS or est_binaire(chemin):
                    continue
                texte = chemin.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            fichiers_scannes += 1
            for numero, ligne in enumerate(texte.splitlines(), start=1):
                if MARQUEUR_AUTORISE in ligne:
                    continue
                for etiquette, motif in MOTIFS:
                    correspondance = motif.search(ligne)
                    if correspondance:
                        alertes.append(
                            {
                                "type": "contenu",
                                "motif": etiquette,
                                "fichier": str(chemin),
                                "ligne": str(numero),
                                "extrait": masque(correspondance.group(0)),
                            }
                        )
    return alertes, fichiers_scannes


def main() -> int:
    parseur = argparse.ArgumentParser(
        description="Scanner d'hygiène de publication — Protocole Triade"
    )
    parseur.add_argument(
        "chemin", nargs="?", default=".",
        help="répertoire à scanner (défaut : répertoire courant)",
    )
    parseur.add_argument(
        "--json", action="store_true", help="sortie JSON (pour agent ou CI)"
    )
    arguments = parseur.parse_args()

    racine = Path(arguments.chemin).resolve()
    if not racine.is_dir():
        print(f"Erreur : {racine} n'est pas un répertoire.", file=sys.stderr)
        return 2

    alertes, fichiers_scannes = scanner(racine)

    if arguments.json:
        print(json.dumps(
            {
                "racine": str(racine),
                "date": datetime.now().isoformat(timespec="seconds"),
                "fichiers_texte_scannes": fichiers_scannes,
                "alertes": alertes,
                "statut": "ROUGE" if alertes else "VERT",
            },
            ensure_ascii=False, indent=2,
        ))
    else:
        print(f"Scanner d'hygiène Triade — périmètre : {racine}")
        print(f"Fichiers texte scannés : {fichiers_scannes}")
        print()
        if not alertes:
            print("VERT — aucune alerte détectée.")
            print("Rappel : la relecture humaine reste obligatoire (C4, étape 4).")
        else:
            print(f"ROUGE — {len(alertes)} alerte(s) :")
            for alerte in alertes:
                localisation = alerte["fichier"]
                if alerte["ligne"]:
                    localisation += f":{alerte['ligne']}"
                extrait = ""
                if alerte.get("extrait"):
                    extrait = f" — extrait masqué : {alerte['extrait']}"
                print(f"  [{alerte['motif']}] {localisation}{extrait}")
            print()
            print("Actions : localiser l'alerte, retirer le secret, puis faire une")
            print("rotation de jetons (cérémonie C1) si le secret a pu être exposé.")
    return 1 if alertes else 0


if __name__ == "__main__":
    sys.exit(main())
