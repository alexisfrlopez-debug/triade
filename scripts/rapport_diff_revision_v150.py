#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapport_diff_revision_v150.py — LE RAPPORT DIFF COMPLET de la révision
manuscrit+spécification (paquet 4/6, sollwnmae, D203).

Chaque fichier révisé, son diff unifié contre l'état AVANT (git HEAD —
la session n'a touché AUCUN de ces fichiers avant la révision), ses
empreintes sha256 avant/après, et le contexte de la vérification."""

import hashlib
import pathlib
import subprocess

REPO = pathlib.Path("/home/z/my-project/triade")
SORTIE = REPO / "scripts" / "preuves_v150" / "revision_manuscrit"
SORTIE.mkdir(parents=True, exist_ok=True)

# Les fichiers révisés par le paquet 4 (les sources ; jamais les livrés)
REVISES = [
    "scripts/manuscrit_v150/main.tex",
    "scripts/spec_v150/sec-a.tex",
    "scripts/spec_v150/sec-d.tex",
    "scripts/statuts_preuves_v150.py",
    "scripts/manuscrit_v150/donnees/statuts_v150.tex",
    "scripts/replication_v150/grille_tx.csv",
    "scripts/replication_v150/LISEZMOI-replication.txt",
    "scripts/replication_v150/kohen_kappa_v150.py",
]

# Les fichiers générés (régénérés par les scripts, pas édités à la main)
REGENERES = [
    "scripts/manuscrit_v150/donnees/macros_v150.tex",
    "scripts/manuscrit_v150/donnees/tables_generees.tex",
    "scripts/manuscrit_v150/donnees/jalons.csv",
    "scripts/manuscrit_v150/donnees/budgets.csv",
    "scripts/manuscrit_v150/donnees/oracles.csv",
    "scripts/manuscrit_v150/donnees/runs_loupe.csv",
    "scripts/manuscrit_v150/donnees/empreintes.csv",
    "scripts/manuscrit_v150/donnees/extraits_journal.txt",
]


def sha256_disque(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def sha256_git(chemin: str) -> str:
    """L'empreinte de l'état AVANT (git HEAD) — None si non suivi."""
    p = subprocess.run(["git", "show", f"HEAD:{chemin}"],
                       capture_output=True, cwd=str(REPO))
    if p.returncode != 0:
        return "(nouveau)"
    return hashlib.sha256(p.stdout).hexdigest()


def main() -> None:
    lignes = []
    lignes.append("=" * 74)
    lignes.append("RAPPORT DIFF COMPLET — LA RÉVISION MANUSCRIT+SPÉCIFICATION")
    lignes.append("Paquet 4/6 de la vague 3 (instruction sollwnmae) — D203, "
                  "Entrée 238")
    lignes.append("=" * 74)
    lignes.append("")
    lignes.append("LES LIVRÉS DE L'ÉDITION v0.15.0 DEMEURENT INTACTS :")
    lignes.append("  les deux zips, les deux PDF de docs/, les main.pdf/"
                  "final.pdf des chaînes —")
    lignes.append("  la révision vit aux SOURCES ; la prochaine édition "
                  "l'embarquera")
    lignes.append("  (compilations témoins au bac à sable /tmp : manuscrit "
                  "22 pages,")
    lignes.append("   spécification 64 pages avec couverture — zéro chaîne "
                  "périmée au texte extrait,")
    lignes.append("   zéro parasite « tbp] »)")
    lignes.append("")
    lignes.append("-" * 74)
    lignes.append("A. LES FICHIERS RÉVISÉS (le diff unifié complet)")
    lignes.append("-" * 74)
    for c in REVISES:
        avant, apres = sha256_git(c), sha256_disque(REPO / c)
        diff = subprocess.run(["git", "diff", "HEAD", "--", c],
                              capture_output=True, text=True, cwd=str(REPO))
        n_ajouts = sum(1 for l in diff.stdout.splitlines()
                       if l.startswith("+") and not l.startswith("+++"))
        n_retraits = sum(1 for l in diff.stdout.splitlines()
                         if l.startswith("-") and not l.startswith("---"))
        lignes.append("")
        lignes.append(f"### {c}")
        lignes.append(f"    avant (git HEAD) : {avant[:16]}…")
        lignes.append(f"    après            : {apres[:16]}…")
        lignes.append(f"    diff : +{n_ajouts} / -{n_retraits} lignes")
        lignes.append("")
        lignes.extend("    " + l if l else "" for l in
                      diff.stdout.splitlines())
    lignes.append("")
    lignes.append("-" * 74)
    lignes.append("B. LES FICHIERS RÉGÉNÉRÉS (par les scripts, jamais à la "
                  "main)")
    lignes.append("-" * 74)
    for c in REGENERES:
        avant, apres = sha256_git(c), sha256_disque(REPO / c)
        etat = ("RÉGÉNÉRÉ" if avant != apres else "identique")
        if avant == "(nouveau)":
            etat = "NOUVEAU"
        lignes.append(f"  {c}")
        lignes.append(f"      {etat} — avant {avant[:16]}… / après "
                      f"{apres[:16]}…")
    lignes.append("  le générateur : extraire_donnees_v150.py (la plage de")
    lignes.append("  décisions \\plageDecisions porte D1--D203, la dernière "
                  "décision réelle ;")
    lignes.append("  les autres comptes exacts du journal suivent)")
    lignes.append("")
    lignes.append("-" * 74)
    lignes.append("C. LA VÉRIFICATION (le détail vit au "
                  "rapport_verification_revision.txt)")
    lignes.append("-" * 74)
    lignes.append("  SIX contrôles VERT : les pourcentages du benchmark "
                  "(recalculés")
    lignes.append("    depuis audit_benchmark.csv), les ratios RQ2 "
                  "(recalculés depuis")
    lignes.append("    remesure_rq2.csv contre budgets.csv), le quantile "
                  "(1,8627 par")
    lignes.append("    bisection maison), les résidus d'édition (chaque "
                  "occurrence")
    lignes.append("    restante classée historique), la grille F/L "
                  "(zéro T/X courant),")
    lignes.append("    les empreintes (scellés == consignées, livrés "
                  "intacts, garde 14/14).")
    lignes.append("")

    texte = "\n".join(lignes) + "\n"
    sortie = SORTIE / "rapport_diff_revision.txt"
    sortie.write_text(texte, encoding="utf-8")
    print(f"[diff] {len(texte.splitlines())} lignes -> {sortie}")


if __name__ == "__main__":
    main()
