#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Falsifiabilité des empreintes par build (M5-a, D134).

Chaque contrôle de la présente suite attaQUe le mécanisme : l'état sain doit
rendre VERT, chaque faute (octet modifié hors build, artefact supprimé, PDF
livré non consigné, rebuild non déterministe, copie de livraison divergente,
registre corrompu, module divergent d'ANNEXE A) doit produire son REFUS NOMMÉ
— un contrôle muet est un contrôle mort. Tout se joue dans un bac à sable
temporaire (TRIADE_EMPREINTES_ROOT) : le dépôt réel n'est JAMAIS touché, et
la suite le vérifie elle-même (contrôle 0).

Contrôles :
   0 bac-à-sable — le dépôt réel n'est ni lu ni écrit
   1 consigner-calcule — md5/sha256/taille mesurés indépendamment (hashlib)
   2 consigner-écrit-tableau — ligne exacte au registre généré
   3 consigner-écrit-journal — ligne sous le marqueur, la plus récente en tête
   4 consigner-idempotent — même octet + même stamp + même build → rien
   5 journal-sans-marqueur — la section « builds » s'auto-crée en fin de journal
   6 verifier-vert — état sain : 0 refus, code 0
   7 refus-EMPREINTE-DIVERGENTE — octet modifié après consignation
   8 refus-ARTEFACT-ABSENT — artefact consigné supprimé du disque
   9 refus-ARTEFACT-DELIVRÉ-NON-CONSIGNÉ — PDF livré hors registre
  10 refus-BUILD-NON-DÉTERMINISTE — même stamp, deux sha256 différents
  11 refus-COPIE-DIVERGENTE — copie de livraison (download/) ≠ dépôt
  12 refus-REGISTRE-ILLISIBLE — ligne de registre corrompue
  13 refus-MODULE-DIVERGENT — module du dépôt ≠ ANNEXE A (bac git initialisé)
  14 refus-MODULE-ABSENT — module d'ANNEXE A absent du dépôt git
  15 chemin-hors-projet — consigner refuse un chemin extérieur

Usage : python3 scripts/test_empreintes_build.py
Code de sortie : 0 = tout PASS, 1 = au moins un ÉCHEC.
"""

import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "empreintes_build.py"
VRAI_TDB = REPO / "docs" / "TABLEAU_BORD.md"
VRAI_JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"

RESULTATS = []


def executer(racine, *args):
    """Appelle empreintes_build.py dans le bac à sable `racine`."""
    env = dict(os.environ)
    env["TRIADE_EMPREINTES_ROOT"] = str(racine)
    r = subprocess.run([sys.executable, str(SCRIPT), *args],
                       capture_output=True, text=True, env=env, timeout=120)
    return r.returncode, r.stdout + r.stderr


def nouveau_bac():
    """Bac neuf : <tmp>/repo (dépôt) + <tmp>/download (livraison)."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="empreintes_m5a_"))
    repo = tmp / "repo"
    (repo / "docs").mkdir(parents=True)
    (tmp / "download").mkdir()
    return tmp, repo


def artefact(repo, nom, contenu=b"%PDF-1.7 faux artefact\n"):
    p = repo / "docs" / nom
    p.write_bytes(contenu)
    return p


def consigner(repo, nom, build="test-build", stamp=None, stamp_file=None):
    args = ["consigner", "--artefact", f"docs/{nom}", "--build", build]
    if stamp_file is not None:
        args += ["--stamp-file", stamp_file]
    elif stamp is not None:
        args += ["--stamp", stamp]
    return executer(repo, *args)


def controle(numero, titre, condition, detail=""):
    ok = bool(condition)
    RESULTATS.append((numero, titre, ok))
    print(f"[test] {'PASS' if ok else 'ÉCHEC'} — {numero} {titre}"
          + (f" ({detail})" if detail and not ok else ""))


def main():
    # 0 — bac à sable : le dépôt réel n'est jamais touché
    avant_tdb = VRAI_TDB.read_bytes() if VRAI_TDB.exists() else None
    avant_journal = VRAI_JOURNAL.read_bytes() if VRAI_JOURNAL.exists() else None

    tmp, repo = nouveau_bac()
    try:
        # 1 — consigner calcule (mesure indépendante par hashlib)
        a = artefact(repo, "a.pdf", b"octets du premier artefact\n")
        md5v = hashlib.md5(a.read_bytes()).hexdigest()
        sha = hashlib.sha256(a.read_bytes()).hexdigest()
        rc, out = consigner(repo, "a.pdf", stamp="aa11" * 16)
        controle("1", "consigner-calcule",
                 rc == 0 and md5v in out and sha[:12] in out,
                 f"rc={rc} out={out.strip()[:120]}")

        # 2 — la ligne du registre générée est exacte
        tdb = (repo / "docs" / "TABLEAU_BORD.md").read_text(encoding="utf-8")
        taille_a = pathlib.Path(a).stat().st_size
        ligne_ok = any(
            f"| docs/a.pdf |" in l and sha in l and md5v in l
            and f"| {taille_a} |" in l and ("aa11" * 16) in l
            and "| test-build |" in l
            for l in tdb.splitlines())
        controle("2", "consigner-écrit-tableau", ligne_ok,
                 tdb[:400] if not ligne_ok else "")

        # 3 — journal : ligne sous le marqueur, la plus récente EN TÊTE
        journal = repo / "docs" / "JOURNAL_TRAVAIL.md"
        journal.write_text("# Journal du bac\n\nEntrée 1 — texte.\n",
                           encoding="utf-8")
        consigner(repo, "a.pdf", build="premier")            # (déjà consigné → skip)
        b = artefact(repo, "b.pdf", b"deuxieme artefact\n")
        consigner(repo, "b.pdf", build="second")
        texte = journal.read_text(encoding="utf-8")
        lignes = texte.split("\n")
        marqueur = [i for i, l in enumerate(lignes)
                    if l.startswith("<!-- m5a:journal-des-builds")]
        sous_marqueur = lignes[marqueur[0] + 1] if marqueur else ""
        ok3 = (len(marqueur) == 1
               and sous_marqueur.startswith("- ")
               and "docs/b.pdf" in sous_marqueur
               and "second" in sous_marqueur
               and any("Entrée 1" in l for l in lignes))
        controle("3", "consigner-écrit-journal", ok3,
                 texte[:300] if not ok3 else "")

        # 4 — idempotence : même octet, même stamp, même build → aucune entrée
        n_avant = sum(1 for l in (repo / "docs" / "TABLEAU_BORD.md")
                      .read_text(encoding="utf-8").splitlines()
                      if l.startswith("| 2 |"))
        rc4, out4 = consigner(repo, "b.pdf", build="second")
        n_apres = sum(1 for l in (repo / "docs" / "TABLEAU_BORD.md")
                      .read_text(encoding="utf-8").splitlines()
                      if l.startswith("| 2 |"))
        controle("4", "consigner-idempotent",
                 rc4 == 0 and "inchangé" in out4 and n_avant == n_apres == 1,
                 f"rc={rc4} n={n_avant}->{n_apres} out={out4.strip()[:80]}")

        # 5 — journal sans marqueur : la section s'auto-crée en fin de fichier
        tmp5, repo5 = nouveau_bac()
        artefact(repo5, "c.pdf", b"artefact cinq\n")
        j5 = repo5 / "docs" / "JOURNAL_TRAVAIL.md"
        j5.write_text("Dernière entrée du journal.\n", encoding="utf-8")
        consigner(repo5, "c.pdf", build="cinquieme")
        t5 = j5.read_text(encoding="utf-8")
        l5 = t5.split("\n")
        ok5 = ("Dernière entrée du journal." in t5
               and any(l.startswith("<!-- m5a:journal-des-builds") for l in l5)
               and "docs/c.pdf" in l5[l5.index(
                   [x for x in l5 if x.startswith("<!-- m5a:journal-des-builds")][0]) + 1])
        controle("5", "journal-sans-marqueur", ok5, t5[:200] if not ok5 else "")
        shutil.rmtree(tmp5, ignore_errors=True)

        # 6 — verifier vert sur état sain
        rc6, out6 = executer(repo, "verifier")
        controle("6", "verifier-vert",
                 rc6 == 0 and "VERDICT : VERT" in out6 and "0 refus" in out6,
                 f"rc={rc6} out={out6.strip()[:160]}")

        # 7 — EMPREINTE-DIVERGENTE : octet modifié après consignation
        tmp7, repo7 = nouveau_bac()
        artefact(repo7, "a.pdf", b"original\n")
        consigner(repo7, "a.pdf", build="sain")
        artefact(repo7, "a.pdf", b"original TAMPRE\n")
        rc7, out7 = executer(repo7, "verifier")
        controle("7", "refus-EMPREINTE-DIVERGENTE",
                 rc7 == 1 and "EMPREINTE-DIVERGENTE" in out7
                 and "REFUS" in out7, f"rc={rc7} out={out7.strip()[:160]}")
        shutil.rmtree(tmp7, ignore_errors=True)

        # 8 — ARTEFACT-ABSENT : consigné puis supprimé
        tmp8, repo8 = nouveau_bac()
        artefact(repo8, "a.pdf", b"original\n")
        consigner(repo8, "a.pdf", build="sain")
        (repo8 / "docs" / "a.pdf").unlink()
        rc8, out8 = executer(repo8, "verifier")
        controle("8", "refus-ARTEFACT-ABSENT",
                 rc8 == 1 and "ARTEFACT-ABSENT" in out8,
                 f"rc={rc8} out={out8.strip()[:160]}")
        shutil.rmtree(tmp8, ignore_errors=True)

        # 9 — ARTEFACT-DELIVRÉ-NON-CONSIGNÉ : PDF livré hors registre
        tmp9, repo9 = nouveau_bac()
        artefact(repo9, "a.pdf", b"consigne\n")
        consigner(repo9, "a.pdf", build="sain")
        artefact(repo9, "fantome.pdf", b"livre en silence\n")
        rc9, out9 = executer(repo9, "verifier")
        controle("9", "refus-ARTEFACT-DELIVRÉ-NON-CONSIGNÉ",
                 rc9 == 1 and "ARTEFACT-DELIVRÉ-NON-CONSIGNÉ" in out9
                 and "fantome.pdf" in out9,
                 f"rc={rc9} out={out9.strip()[:160]}")
        shutil.rmtree(tmp9, ignore_errors=True)

        # 10 — BUILD-NON-DÉTERMINISTE : même stamp, deux sha256
        tmp10, repo10 = nouveau_bac()
        artefact(repo10, "a.pdf", b"version un\n")
        consigner(repo10, "a.pdf", build="force", stamp="bb22" * 16)
        artefact(repo10, "a.pdf", b"version un REBUILDEE\n")
        consigner(repo10, "a.pdf", build="force", stamp="bb22" * 16)
        rc10, out10 = executer(repo10, "verifier")
        controle("10", "refus-BUILD-NON-DÉTERMINISTE",
                 rc10 == 1 and "BUILD-NON-DÉTERMINISTE" in out10,
                 f"rc={rc10} out={out10.strip()[:160]}")
        shutil.rmtree(tmp10, ignore_errors=True)

        # 11 — COPIE-DIVERGENTE : la livraison download/ ne suit plus le dépôt
        tmp11, repo11 = nouveau_bac()
        artefact(repo11, "a.pdf", b"version depot\n")
        consigner(repo11, "a.pdf", build="sain")
        (tmp11 / "download" / "a.pdf").write_bytes(b"version depot ALTEREE\n")
        rc11, out11 = executer(repo11, "verifier")
        controle("11", "refus-COPIE-DIVERGENTE",
                 rc11 == 1 and "COPIE-DIVERGENTE" in out11,
                 f"rc={rc11} out={out11.strip()[:160]}")
        shutil.rmtree(tmp11, ignore_errors=True)

        # 12 — REGISTRE-ILLISIBLE : ligne de registre corrompue
        tmp12, repo12 = nouveau_bac()
        artefact(repo12, "a.pdf", b"consigne\n")
        consigner(repo12, "a.pdf", build="sain")
        tdb12 = repo12 / "docs" / "TABLEAU_BORD.md"
        tdb12.write_text(tdb12.read_text(encoding="utf-8").replace(
            hashlib.sha256(b"consigne\n").hexdigest(), "pas-un-sha-valide"),
            encoding="utf-8")
        rc12, out12 = executer(repo12, "verifier")
        controle("12", "refus-REGISTRE-ILLISIBLE",
                 rc12 == 1 and "REGISTRE-ILLISIBLE" in out12,
                 f"rc={rc12} out={out12.strip()[:160]}")
        shutil.rmtree(tmp12, ignore_errors=True)

        # 13 — MODULE-DIVERGENT : dépôt git du bac ≠ ANNEXE A
        tmp13, repo13 = nouveau_bac()
        (repo13 / "coffre_fort.py").write_text("# bac : PAS le coffre du dépôt\n",
                                               encoding="utf-8")
        for cmd in (["init", "-q"], ["config", "user.email", "bac@exemple"],
                    ["config", "user.name", "bac"],
                    ["add", "-A"], ["commit", "-qm", "bac"]):
            subprocess.run(["git", "-C", str(repo13), *cmd],
                           capture_output=True)
        rc13, out13 = executer(repo13, "modules")
        controle("13", "refus-MODULE-DIVERGENT",
                 rc13 == 1 and "MODULE-DIVERGENT" in out13
                 and "coffre_fort.py" in out13,
                 f"rc={rc13} out={out13.strip()[:200]}")
        shutil.rmtree(tmp13, ignore_errors=True)

        # 14 — MODULE-ABSENT : ANNEXE A référence un fichier absent du dépôt
        tmp14, repo14 = nouveau_bac()
        (repo14 / "autre.txt").write_text("rien à voir\n", encoding="utf-8")
        for cmd in (["init", "-q"], ["config", "user.email", "bac@exemple"],
                    ["config", "user.name", "bac"],
                    ["add", "-A"], ["commit", "-qm", "bac"]):
            subprocess.run(["git", "-C", str(repo14), *cmd],
                           capture_output=True)
        rc14, out14 = executer(repo14, "modules")
        controle("14", "refus-MODULE-ABSENT",
                 rc14 == 1 and out14.count("MODULE-DIVERGENT") >= 15,
                 f"rc={rc14} refus={out14.count('MODULE-DIVERGENT')}")
        shutil.rmtree(tmp14, ignore_errors=True)

        # 15 — chemin hors projet refusé
        rc15, out15 = executer(
            repo, "consigner", "--artefact", "/etc/hostname", "--build", "x")
        controle("15", "chemin-hors-projet", rc15 == 2 and "hors projet" in out15,
                 f"rc={rc15} out={out15.strip()[:100]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # 0 — le dépôt réel n'a pas bougé d'un octet
    apres_tdb = VRAI_TDB.read_bytes() if VRAI_TDB.exists() else None
    apres_journal = VRAI_JOURNAL.read_bytes() if VRAI_JOURNAL.exists() else None
    controle("0", "bac-à-sable (dépôt réel intact)",
             avant_tdb == apres_tdb and avant_journal == apres_journal)

    passes = sum(1 for _, _, ok in RESULTATS if ok)
    echecs = len(RESULTATS) - passes
    print(f"[test] empreintes M5-a : {passes} PASS / {echecs} ÉCHEC "
          f"({len(RESULTATS)} contrôles)")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
