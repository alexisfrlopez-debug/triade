#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exécuteur de cérémonies — Protocole Triade.

Guide le déroulé d'une cérémonie étape par étape et écrit la fiche dans
journal/ à la fin (règle R6). Aucune dépendance externe.

Usage :
    python3 scripts/triade_ceremonie.py              # menu interactif
    python3 scripts/triade_ceremonie.py --liste      # catalogue des cérémonies
    python3 scripts/triade_ceremonie.py --c 3        # lance directement C3
    python3 scripts/triade_ceremonie.py --c 3 --oui  # tout confirmer (agent / CI)
    python3 scripts/triade_ceremonie.py --resume     # squelette de résumé de session
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

CEREMONIES: dict[str, dict] = {
    "0": {
        "nom": "Fondation",
        "objectif": "Instancier une triade complète et opérationnelle.",
        "declencheur": "Démarrage du projet.",
        "etapes": [
            "Créer le dépôt Git (privé) et committer le kit complet.",
            "Activer .gitignore.triade (.env, config.json, journal/, clés).",
            "Créer l'arborescence Drive : documents/, packs/, coffre-jetons/.",
            "Créer le dépôt Zenodo (réservé, privé).",
            "Générer les jetons initiaux (privilège minimum) vers coffre-jetons/rotation-AAAA-MM-JJ/.",
            "Remplir .env (valeurs) et config.json (identifiants non sensibles).",
            "Définir la phrase de contrôle dans CONTROLE.md.",
            "Lancer scripts/triade_hygiene.py : aucune alerte attendue.",
            "Initialiser ETAT_PROJET.md et écrire la fiche C0 dans journal/.",
        ],
    },
    "1": {
        "nom": "Rotation des jetons",
        "objectif": "Remplacer les jetons et propager le changement aux trois plateformes.",
        "declencheur": "Échéance (≈ 90 jours), fuite, mouvement d'équipe.",
        "etapes": [
            "Ouvrir la fiche C1 : annoncer date et périmètre de la rotation.",
            "Créer les nouveaux jetons SANS révoquer les anciens (sauf fuite : révoquer d'abord).",
            "Déposer les nouveaux jetons dans coffre-jetons/rotation-AAAA-MM-JJ/.",
            "Mettre à jour le .env local.",
            "Propager et vérifier par une opération réelle : Git, puis Drive, puis Zenodo.",
            "Révoquer les anciens jetons.",
            "Lancer scripts/triade_hygiene.py sur tout le projet.",
            "Écrire la fiche C1 et mettre à jour ETAT_PROJET.md (échéances).",
        ],
    },
    "2": {
        "nom": "Synchronisation",
        "objectif": "Ramener les trois plateformes à un état cohérent.",
        "declencheur": "Fin de séquence de travail ; obligatoire avant C3.",
        "etapes": [
            "Git : relecture du diff, commits atomiques, push.",
            "Drive : téléverser ou mettre à jour les documents vivants modifiés.",
            "Contrôle de cohérence des versions et des noms.",
            "Fiche C2 dans journal/.",
        ],
    },
    "3": {
        "nom": "Gel & Pack",
        "objectif": "Figer un état cohérent et régénérer le pack versionné.",
        "declencheur": "Jalon de contenu (C2 préalable obligatoire).",
        "etapes": [
            "Choisir le numéro de version (MAJEUR/MINEUR/PATCH).",
            "Geler l'état : créer le tag Git du même numéro.",
            "Régénérer complètement les documents du pack (config.json → pack.documents).",
            "Calculer les SHA-256 et remplir templates/PACK_MANIFEST.md.",
            "Téléverser le pack dans Drive packs/vX.Y.Z/.",
            "Mettre à jour CHANGELOG.md.",
            "Écrire la fiche C3 et mettre à jour ETAT_PROJET.md.",
        ],
    },
    "4": {
        "nom": "Revue & Réception",
        "objectif": "Valider qualité, exactitude et salubrité avant publication.",
        "declencheur": "Intention de passage public, ou jalon majeur.",
        "etapes": [
            "Revue du manifeste : chaque document, chaque empreinte vérifiée.",
            "Revue de contenu : faits, mentions, licences, autorisations.",
            "Scanner d'hygiène sur le pack exact, puis sur tout le projet.",
            "Relecture humaine anti-fuite (captures, PDF, métadonnées, noms).",
            "Produire le résumé de session normalisé.",
            "Décision humaine GO / NO-GO consignée.",
            "Mettre à jour ETAT_PROJET.md.",
        ],
    },
    "5": {
        "nom": "Passage public",
        "objectif": "Publier la version validée sur Zenodo et obtenir le DOI.",
        "declencheur": "GO de la cérémonie C4, et elle seule.",
        "etapes": [
            "Re-vérifier le GO de C4 et son horodatage.",
            "Dernier scan d'hygiène sur le pack exact à publier.",
            "Téléverser sur Zenodo avec métadonnées complètes (titre, auteurs, version, licence).",
            "Passer le dépôt en public et récupérer le DOI.",
            "Consigner le DOI dans ETAT_PROJET.md et le manifeste.",
            "Créer la release Git mentionnant le DOI.",
            "Écrire la fiche C5 et le résumé de session.",
        ],
    },
}

RACINE = Path.cwd()
JOURNAL = RACINE / "journal"


def lire_rotation_config() -> tuple[str, int] | None:
    """Lit config.json pour rappeler l'échéance de rotation (facultatif)."""
    chemin = RACINE / "config.json"
    if not chemin.is_file():
        return None
    try:
        donnees = json.loads(chemin.read_text(encoding="utf-8"))
        rotation = donnees.get("rotation_jetons", {})
        derniere = rotation.get("derniere_rotation", "")
        cadence = int(rotation.get("cadence_jours", 90))
        if derniere:
            return str(derniere), cadence
    except (json.JSONDecodeError, ValueError, OSError):
        return None
    return None


def rappel_rotation() -> str:
    info = lire_rotation_config()
    if not info:
        return ""
    derniere, cadence = info
    try:
        date_rotation = date.fromisoformat(derniere)
    except ValueError:
        return f"Rotation de jetons : dernière consignée le {derniere} (date illisible)."
    echeance = date_rotation + timedelta(days=cadence)
    aujourdhui = date.today()
    if aujourdhui >= echeance:
        return f"ROTATION DUE : dernière rotation le {derniere}, échéance {echeance.isoformat()} (cérémonie C1)."
    return f"Rotation de jetons : dernière le {derniere}, prochaine échéance {echeance.isoformat()} (cérémonie C1)."


def afficher_liste() -> None:
    print("Cérémonies du protocole Triade")
    print("=" * 60)
    for code, c in CEREMONIES.items():
        print(f"  C{code} — {c['nom']}")
        print(f"      Objectif    : {c['objectif']}")
        print(f"      Déclencheur : {c['declencheur']}")
        print(f"      Étapes      : {len(c['etapes'])}")
    print()
    print("Guide complet : ceremonies/GUIDE_CEREMONIES.md")


def ecrire_fiche(code: str, etats: list[tuple[str, str]]) -> Path:
    JOURNAL.mkdir(parents=True, exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d")
    heure = datetime.now().strftime("%H:%M")
    chemin = JOURNAL / f"C{code}_{horodatage}.md"
    lignes = [
        f"# Fiche de cérémonie — C{code} {CEREMONIES[code]['nom']}",
        "",
        f"- **Date et heure** : {horodatage} {heure}",
        f"- **Objectif** : {CEREMONIES[code]['objectif']}",
        "- **Participants** : humain (décideur) ; agent (exécutant)",
        "",
        "## Étapes vérifiées",
        "",
    ]
    for index, (etape, etat) in enumerate(etats, start=1):
        lignes.append(f"{index}. [{'x' if etat == 'o' else ' '}] {etape}"
                      + ("" if etat == "o" else f" — {etat.upper()}"))
    lignes += [
        "",
        "## Anomalies et décisions",
        "",
        "- (à compléter)",
        "",
        "## Échéances générées",
        "",
        f"- {rappel_rotation() or '(à compléter)'}",
    ]
    chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    return chemin


def derouler(code: str, auto_oui: bool) -> None:
    ceremonie = CEREMONIES[code]
    print(f"Cérémonie C{code} — {ceremonie['nom']}")
    print("=" * 60)
    print(f"Objectif    : {ceremonie['objectif']}")
    print(f"Déclencheur : {ceremonie['declencheur']}")
    print()
    etats: list[tuple[str, str]] = []
    for index, etape in enumerate(ceremonie["etapes"], start=1):
        print(f"  {index}/{len(ceremonie['etapes'])} — {etape}")
        if auto_oui:
            print("      → confirmé (--oui)")
            etats.append((etape, "o"))
            continue
        while True:
            reponse = input("      Confirmer ? [o]ui / [n]on / [s]auter / [q]uitter : ").strip().lower()
            if reponse in ("o", "n", "s", "q"):
                break
            print("      Réponse non comprise : o, n, s ou q.")
        if reponse == "q":
            print("Cérémonie interrompue — aucune fiche écrite (règle R6 : fiche obligatoire pour clôturer).")
            return
        etats.append((etape, reponse))
        print()
    chemin = ecrire_fiche(code, etats)
    print("=" * 60)
    print(f"Fiche écrite : {chemin}")
    message = rappel_rotation()
    if message:
        print(f"Rappel : {message}")
    print("Cérémonie enregistrée. Mettre à jour ETAT_PROJET.md si nécessaire.")


def generer_resume() -> None:
    JOURNAL.mkdir(parents=True, exist_ok=True)
    horodatage = datetime.now().strftime("%Y-%m-%d")
    chemin = JOURNAL / f"RESUME_{horodatage}.md"
    squelette = f"""# Résumé de session — {horodatage}

> Mémoire du projet entre deux sessions. Factuel, daté, sans interprétation
> libre. Produit en fin de session (règle R5 de AGENTS.md).

## 1. Demande principale et intention

-

## 2. Concepts et décisions techniques clés

-

## 3. Fichiers et artefacts touchés

-

## 4. Erreurs rencontrées et corrections

-

## 5. Problèmes résolus / en cours

-

## 6. Messages clés de l'humain (chronologie)

-

## 7. Tâches restantes

-

## 8. Travail en cours au moment du résumé

-

## 9. Prochaines étapes suggérées

-
"""
    chemin.write_text(squelette, encoding="utf-8")
    print(f"Squelette de résumé écrit : {chemin}")


def main() -> int:
    parseur = argparse.ArgumentParser(description="Exécuteur de cérémonies — Protocole Triade")
    parseur.add_argument("--liste", action="store_true", help="afficher le catalogue des cérémonies")
    parseur.add_argument("--c", choices=sorted(CEREMONIES.keys()), help="code de la cérémonie à dérouler (0-5)")
    parseur.add_argument("--oui", action="store_true", help="confirmer toutes les étapes (mode agent/CI)")
    parseur.add_argument("--resume", action="store_true", help="générer un squelette de résumé de session")
    arguments = parseur.parse_args()

    if arguments.liste:
        afficher_liste()
        return 0
    if arguments.resume:
        generer_resume()
        return 0
    if arguments.c:
        derouler(arguments.c, arguments.oui)
        return 0

    print("Exécuteur de cérémonies — Protocole Triade")
    message = rappel_rotation()
    if message:
        print(message)
    print()
    for code, c in CEREMONIES.items():
        print(f"  C{code} — {c['nom']}")
    print("   r — générer un squelette de résumé de session")
    print("   q — quitter")
    choix = input("Cérémonie à dérouler : ").strip().lower()
    if choix == "q":
        return 0
    if choix == "r":
        generer_resume()
        return 0
    if choix in CEREMONIES:
        derouler(choix, False)
        return 0
    print("Code inconnu. Utiliser --liste pour le catalogue.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
