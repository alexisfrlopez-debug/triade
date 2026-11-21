#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# LA REPRISE 0UUG27TEO — simuler_runbook.py REJOUE au dépôt courant
# (le simulateur de la vague 11 INTACT, le chemin du dépôt patché ;
# huit étapes sans écriture, le geste piège refusé au premier nom)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""simuler_runbook.py — LA VÉRIFICATION (2) DE L'INSTRUCTION ou6wn6wlv :
LE RUNBOOK §8 DÉROULÉ EN SIMULATION sur clone de test à phrase publique
marquée (D105) — AUCUN chemin ne commit de phrase.

La méthode (le plan gelé) : le runbook re-écrit en étapes mécaniques,
chaque étape exécutée sur le clone, CHAQUE écriture inspectée — le
surveilleur git (post-commit du clone de test) et le scan du contenu
committé (la phrase-marqueur ne doit JAMAIS apparaître dans un objet git
ni dans un fichier suivi).

LA PHRASE DE TEST PUBLIQUE (D105 — jamais une phrase réelle) :
« PHRASE-TEST-PUBLIQUE-D105-vague11-simulation »."""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
ICI = REPO / "atelier-purge-0uug27teo"
CLONE = ICI / "clone-runbook-reprise"
PHRASE_TEST = "PHRASE-TEST-PUBLIQUE-D105-vague12-simulation"
FICHIER_PHRASE = "PHRASE-CONTROLE-COFFRE.txt"

ETAPES = []


def etaape(nom, cmd, cwd):
    """Une étape mécanique du runbook — exécutée, le dépôt inspecté APRÈS."""
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120,
                       shell=isinstance(cmd, str))
    ecrit = False
    # 1. le fichier-phrase existe-t-il dans l'arbre suivi ?
    suivi = subprocess.run(["git", "ls-files"], cwd=cwd, capture_output=True,
                           text=True).stdout
    if FICHIER_PHRASE in suivi:
        ecrit = True
    # 2. la phrase-marqueur vit-elle dans un objet git (contenu committé) ?
    p = subprocess.run(["git", "grep", "-I", PHRASE_TEST, "HEAD"],
                       cwd=cwd, capture_output=True, text=True)
    if p.returncode == 0:
        ecrit = True
    # 3. la phrase-marqueur vit-elle dans un fichier NON-IGNORÉ du plan de travail ?
    st = subprocess.run(["git", "status", "--porcelain"], cwd=cwd,
                        capture_output=True, text=True).stdout
    for ligne in st.splitlines():
        chemin = ligne[3:].strip().strip('"')
        if chemin == FICHIER_PHRASE and not ligne.startswith("??"):
            ecrit = True
    ETAPES.append({"etape": nom, "commande": cmd if isinstance(cmd, str) else " ".join(cmd),
                   "code": r.returncode, "phrase_au_depot": ecrit,
                   "sortie": (r.stdout + r.stderr)[-200:]})
    print(f"  [{'ROUGE' if ecrit else 'VERT '}] {nom} (code {r.returncode})")
    return r.returncode, ecrit


def main() -> int:
    # ---- le clone de test (jamais le dépôt réel) ----------------------------
    if CLONE.exists():
        shutil.rmtree(CLONE)
    subprocess.run(["git", "clone", "-q", str(REPO), str(CLONE)], check=True,
                   timeout=300)
    # le marquage public : la phrase de test POSÉE au plan de travail du clone
    # (l'état initial délibéré — la simulation doit prouver qu'AUCUNE étape du
    # runbook ne la commite ; le fichier est posé NON SUIVI, comme un brouillon)
    (CLONE / FICHIER_PHRASE).write_text(PHRASE_TEST + "\n", encoding="utf-8")

    print("LE RUNBOOK §8 DÉROULÉ EN SIMULATION (clone de test, phrase publique D105)")
    print(f"  la phrase-marqueur : {PHRASE_TEST[:40]}…")

    rouge = 0
    # ---- §8.1 trouver la maison ----------------------------------------------
    code, e = etaape("§8.1 git pull (la maison à jour)",
                     ["git", "pull", "-q"], CLONE)
    rouge += e
    code, e = etaape("§8.1 MANIFESTE lu (le kit)",
                     "cat MANIFESTE.txt 2>/dev/null || cat LISEZMOI-ARCHIVE.txt >/dev/null",
                     CLONE)
    rouge += e
    # ---- §8.2 l'ordre des gestes ----------------------------------------------
    # étape 3 (la phrase à vous) : la cérémonie sous séquestre — les parts
    # assemblées à froid HORS dépôt ; la simulation exécute les gestes locaux
    # (le dossier de travail), JAMAIS d'écriture suivie
    code, e = etaape("§8.2-3 la cérémonie de changement sous séquestre (les parts "
                     "hors-ligne assemblées — AUCUN fichier au dépôt)",
                     "mkdir -p .keys && echo parts > .keys/sequestre-simulation.txt",
                     CLONE)
    rouge += e
    code, e = etaape("§8.2-4 CF1 -> CF2 (le conteneur au .keys/, gitignoré)",
                     "echo conteneur > .keys/coffre_fort.bin", CLONE)
    rouge += e
    code, e = etaape("§8.2-5 CF2 -> CF3 (l'époque au .keys/, le média hors dépôt)",
                     "echo epoque > .keys/cf3-epoque.txt", CLONE)
    rouge += e
    code, e = etaape("§8.2-6 détruire CF2 (le PV au .keys/)",
                     "echo pv > .keys/pv-cf3/destruction.txt 2>/dev/null || "
                     "mkdir -p .keys/pv-cf3 && echo pv > .keys/pv-cf3/destruction.txt",
                     CLONE)
    rouge += e
    # ---- le geste PIÈGE : un commit volontaire du fichier-phrase -------------
    # (le chemin interdit — le refus nommé doit s'exercer : la garde active)
    # La simulation exécute le geste PUIS constate que le pipeline refuserait :
    # le hook pre-commit du modèle D223 (le refus nommé) — installé au clone.
    hook = CLONE / ".git" / "hooks" / "pre-commit"
    hook.write_text(
        "#!/bin/sh\n"
        "# LA GARDE ACTIVE D223 — le refus nommé : la phrase (ou son fichier)\n"
        "# ne vit JAMAIS au dépôt (public, D220)\n"
        "if git diff --cached --name-only | grep -qx '" + FICHIER_PHRASE + "'; then\n"
        "  echo \"REFUS-NOMMÉ : la phrase de contrôle ne se commite pas au dépôt " \
        "(D223 — le séquestre 5/3 est la garde, le dépôt est PUBLIC D220)\"\n"
        "  exit 1\n"
        "fi\n"
        "exit 0\n", encoding="utf-8")
    hook.chmod(0o755)
    code, e = etaape("LE GESTE PIÈGE : git add du fichier-phrase (le chemin interdit)",
                     ["git", "add", FICHIER_PHRASE], CLONE)
    # l'étape add NE COMMITE PAS : l'inspection vérifie le commit lui-même
    r = subprocess.run(["git", "commit", "-m", "le geste piège — la phrase"],
                       cwd=CLONE, capture_output=True, text=True)
    refuse = r.returncode != 0 and "REFUS-NOMMÉ" in (r.stdout + r.stderr)
    ETAPES.append({"etape": "LE GESTE PIÈGE : git commit du fichier-phrase",
                   "commande": "git commit -m …",
                   "code": r.returncode, "phrase_au_depot": not refuse,
                   "sortie": (r.stdout + r.stderr)[-300:]})
    print(f"  [{'ROUGE' if not refuse else 'VERT '}] le commit du fichier-phrase "
          f"{'REFUSÉ au nom (D223)' if refuse else 'ACCEPTÉ — ROUGE'}")
    rouge += 0 if refuse else 1
    # le staging nettoyé (la simulation s'arrête là — le refus prouvé)
    subprocess.run(["git", "reset", "-q"], cwd=CLONE, capture_output=True)

    # ---- l'état final : la phrase n'a JAMAIS atteint un objet git ------------
    p = subprocess.run(["git", "log", "--all", "--oneline"], cwd=CLONE,
                       capture_output=True, text=True)
    n_commits = len(p.stdout.splitlines())
    # le scan du contenu de TOUS les objets blob du dépôt (le juge intégral)
    scan = subprocess.run(
        f"git rev-list --objects --all | awk '{{print $1}}' | "
        f"git cat-file --batch-check='%(objectname) %(objecttype)' | "
        f"grep blob | awk '{{print $1}}' | "
        f"xargs -r -n1 git cat-file blob | grep -c '{PHRASE_TEST}' || true",
        cwd=CLONE, capture_output=True, text=True, shell=True)
    n_fuites = int(scan.stdout.strip() or 0)
    verdict = (rouge == 0 and n_fuites == 0)

    print()
    print(f"LE VERDICT : {'VERT' if verdict else 'ROUGE'} — "
          f"{len(ETAPES)} étapes mécaniques ; {rouge} chemin(s) rouges ; "
          f"{n_fuites} objet(s) git portant la phrase-marqueur sur "
          f"{n_commits} commits")
    print("LA PREUVE : le geste piège REFUSÉ au nom ; le scan intégral des blobs "
          "de l'historique — la phrase publique D105 n'y vit nulle part")

    (ICI / "simulation-runbook.json").write_text(
        json.dumps({"verdict": "VERT" if verdict else "ROUGE",
                    "phrase_test": PHRASE_TEST,
                    "etapes": ETAPES, "chemins_rouges": rouge,
                    "fuites_blob": n_fuites, "commits_scannes": n_commits},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
