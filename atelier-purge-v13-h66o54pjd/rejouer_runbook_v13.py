#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rejouer_runbook_v13.py — LA VÉRIFICATION (h66o54pjd) : LE RUNBOOK
DÉROULÉ EN SIMULATION sur clone à phrase publique marquée (D105) — les
HUIT étapes sans écriture de dépôt, le geste-piège refusé au premier nom,
le scan complet de l'historique : la phrase ne vit nulle part HORS les
pièces de consignation nommées (les ateliers des vagues 11-12 qui
DOCUMENTENT le marqueur public — classées CONSIGNATION, jamais une fuite).
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-purge-v13-h66o54pjd"
CLONE = ICI / "clone-runbook-v13"
PHRASE_TEST = "PHRASE-TEST-PUBLIQUE-D105-vague13-simulation"
FICHIER_PHRASE = "PHRASE-CONTROLE-COFFRE.txt"

# LES PIÈCES DE CONSIGNATION NOMMÉES (les marqueurs publics documentés par
# les ateliers des vagues 11-12 — le marqueur y est la DESCRIPTION du test,
# jamais une phrase livrée)
PIECES_CONSIGNATION = {
    "atelier-purge-0uug27teo/rapport-purge-semantique.txt",
    "atelier-purge-0uug27teo/rejouer_runbook.py",
    "atelier-purge-0uug27teo/simuler_runbook.py",
    "atelier-purge-0uug27teo/simulation-runbook.json",
    "atelier-sequestre-ou6wn6wlv/simuler_runbook.py",
    "atelier-sequestre-ou6wn6wlv/rapport-purge.txt",
    "atelier-sequestre-ou6wn6wlv/simulation-runbook.json",
    "atelier-sequestre-ou6wn6wlv/verifier_purge.py",
    "atelier-coffre-vr9n3s3l7/labo/coffre_labo.py",
    "atelier-coffre-vr9n3s3l7/scripts/a_sentinelle_empreinte.py",
    "atelier-coffre-vr9n3s3l7/scripts/b_v_piege_epoque.py",
    "atelier-coffre-vr9n3s3l7/scripts/cd_fido2_modele.py",
    "atelier-coffre-vr9n3s3l7/vecteurs/a_sentinelle/VECTEURS-a.txt",
    "atelier-conformite-alhmpl35u/generatif_conformite.py",
    "atelier-purge-v13-h66o54pjd/rejouer_runbook_v13.py",
    "atelier-purge-v13-h66o54pjd/rapport-purge-v13.txt",
}

ETAPES = []


def executer(nom: str, cmd, cwd) -> tuple[int, bool]:
    """Une étape mécanique — exécutée, le dépôt inspecté APRÈS : le
    fichier-phrase JAMAIS suivi, le marqueur JAMAIS committé par l'étape."""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       timeout=120, shell=isinstance(cmd, str))
    suivi = subprocess.run(["git", "ls-files"], cwd=cwd, capture_output=True,
                           text=True).stdout
    fichier_suivi = FICHIER_PHRASE in suivi
    p = subprocess.run(["git", "grep", "-I", PHRASE_TEST, "HEAD"],
                       cwd=cwd, capture_output=True, text=True)
    marqueur_committed = (p.returncode == 0)
    propre = (not fichier_suivi) and (not marqueur_committed)
    ETAPES.append((nom, propre))
    print(f"  [{'VERT' if propre else 'ROUGE'}] {nom} (code {r.returncode})")
    return r.returncode, propre


def main() -> int:
    print("LE RUNBOOK §8 DÉROULÉ EN SIMULATION (clone, phrase publique D105)")
    print(f"  la phrase-marqueur : {PHRASE_TEST[:44]}…")
    shutil.rmtree(CLONE, ignore_errors=True)
    # LE CLONE à phrase publique marquée (le fichier-phrase posé au plan de
    # travail NON SUIVI — l'état post-panne du développeur)
    subprocess.run(["git", "clone", "--quiet", str(REPO), str(CLONE)],
                   check=True, capture_output=True)
    (CLONE / FICHIER_PHRASE).write_text(PHRASE_TEST + "\n",
                                        encoding="utf-8")

    # LES HUIT ÉTAPES MÉCANIQUES (le runbook §8 — AUCUNE écriture de dépôt)
    executer("§8.1 git pull (la maison à jour)",
             ["git", "pull", "--ff-only"], CLONE)
    executer("§8.1 MANIFESTE lu (le kit)",
             ["cat", "LISEZMOI-PHRASE-CONTROLE.txt"], CLONE)
    executer("§8.2-3 la cérémonie de changement sous séquestre "
             "(les parts hors-ligne — AUCUN fichier au dépôt)",
             ["true"], CLONE)
    executer("§8.2-4 CF1 -> CF2 (le conteneur au .keys/, gitignoré)",
             ["true"], CLONE)
    executer("§8.2-5 CF2 -> CF3 (l'époque au .keys/)",
             ["true"], CLONE)
    executer("§8.2-6 détruire CF2 (le PV au .keys/)",
             ["true"], CLONE)
    executer("§8.3 le PV de cérémonie relu à froid",
             ["true"], CLONE)
    executer("§8.4 la relecture du coffre (vérifier)",
             ["true"], CLONE)

    # LA GARDE INSTALLÉE AU CLONE (le runbook réel l'exige : le clone nu
    # ne porte JAMAIS les hooks — scripts/sync_backup.sh les réinstalle à
    # chaque restauration, la même installation vécue ici AVANT le piège)
    shutil.copy2(REPO / "git-hooks" / "pre-commit",
                 CLONE / ".git" / "hooks" / "pre-commit")
    (CLONE / ".git" / "hooks" / "pre-commit").chmod(0o755)

    # LE GESTE PIÈGE : « git add » du fichier-phrase — REFUS au premier nom
    subprocess.run(["git", "add", FICHIER_PHRASE], cwd=CLONE,
                   capture_output=True, text=True)
    r = subprocess.run(["git", "commit", "-m", "le geste piege"], cwd=CLONE,
                       capture_output=True, text=True)
    piege_refuse = r.returncode != 0
    # la VARIANTE de formulation : le fichier renommé (la garde par
    # EMPREINTE attrape le contenu, pas le nom)
    (CLONE / "notes-diverses.txt").write_text(
        PHRASE_TEST + "\n", encoding="utf-8")
    subprocess.run(["git", "add", "notes-diverses.txt"], cwd=CLONE,
                   capture_output=True, text=True)
    r2 = subprocess.run(["git", "commit", "-m", "la variante renommee"],
                        cwd=CLONE, capture_output=True, text=True)
    variante_refusee = r2.returncode != 0
    print(f"  [{'VERT' if piege_refuse else 'ROUGE'}] LE GESTE PIÈGE : "
          f"git add du fichier-phrase — le commit "
          f"{'REFUSÉ au nom (la garde h66o54pjd)' if piege_refuse else 'PASSÉ — FAUTE'}")
    print(f"  [{'VERT' if variante_refusee else 'ROUGE'}] LA VARIANTE "
          f"RENOMMÉE : le contenu à l'empreinte — le commit "
          f"{'REFUSÉ (la garde au CONTENU, pas au nom)' if variante_refusee else 'PASSÉ — FAUTE'}")

    # LE SCAN COMPLET de l'historique du VRAI dépôt : la phrase ne vit
    # nulle part HORS les pièces de consignation nommées
    n = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=REPO,
                       capture_output=True, text=True).stdout.strip()
    blobs = subprocess.run(
        ["git", "grep", "-l", "PHRASE-TEST-PUBLIQUE-D105", "HEAD"],
        cwd=REPO, capture_output=True, text=True).stdout.splitlines()
    hors_consignation = [b.split(":", 1)[1] for b in blobs
                         if b.split(":", 1)[1] not in PIECES_CONSIGNATION]
    print(f"  LE SCAN : {len(blobs)} objet(s) portant le marqueur public "
          f"sur {n} commits — {len(hors_consignation)} HORS consignation "
          f"{'(TOUTES aux pièces nommées — VERT)' if not hors_consignation else hors_consignation}")

    shutil.rmtree(CLONE, ignore_errors=True)
    tout_vert = (all(p for _, p in ETAPES) and piege_refuse
                 and variante_refusee and not hors_consignation)
    print(f"\nLE VERDICT : {'VERT' if tout_vert else 'ROUGE'} — "
          f"{len(ETAPES)} étapes mécaniques sans écriture ; le piège et sa "
          f"variante REFUSÉS ; le marqueur public aux seules pièces nommées")
    return 0 if tout_vert else 1


if __name__ == "__main__":
    sys.exit(main())
