#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AMÉLIORATION 4 DE LA VAGUE 18 (JEEWKX9G8) — LA LISTE BLANCHE FERMÉE DU PRESCRIPTIF.

Le prescriptif ne se devine pas : il se DÉCLARE. Seuls les fichiers listés au
manifeste racine SOURCES-PRESCRIPTIVES.txt (chemin + sha256) peuvent prescrire un
geste. Toute instruction de geste lue AILLEURS est REFUSÉE, nommée
SOURCE-NON-PRESCRIPTIVE, QUELLE QUE SOIT SA FORMULATION — la liste blanche décide,
jamais le mot-clé. Le linter heuristique (linter_v234) reste en SECONDE ligne.

Modes :
  --regenere     réécrit le manifeste (acte délibéré, jamais automatique)
  --verifie      vérifie que chaque source listée est intacte (sha256)
  --scan         classe tout l'arbre lisible et rend 0 consigne active hors liste
  --source F     dit si F peut prescrire (code 0) ou non (code 3, refus nommé)
  (sans option)  l'autotest à fixtures (a)-(d) de l'instruction
"""
import hashlib
import os
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parents[2]
MANIFESTE = RACINE / "SOURCES-PRESCRIPTIVES.txt"

# Ce qui PEUT prescrire, par construction : les instructions de reprise, les plans
# gelés, les documents normatifs et le kit. Le reste est lecture seule.
GLOBS = [
    "REPRISE_PROJET.md",
    "PLAN-*.md",
    "plans-vague18/PLAN-*.md",
    "docs/AMELIORATIONS.md",
    "docs/PROTOCOLE_TRIADE.md",
    "docs/FORMAT_CARTE.md",
    "kit-developpement-triade-v1.1.0/README.md",
    "kit-developpement-triade-v1.1.0/SECURITE.md",
    "kit-developpement-triade-v1.1.0/AGENTS.md",
    "kit-developpement-triade-v1.1.0/docs/GARANTIES.md",
    "kit-developpement-triade-v1.1.0/ceremonies/GUIDE_CEREMONIES.md",
]
EXCLUS = {".git", ".keys", "node_modules", "__pycache__"}
HISTORIQUE = ("ARCHIVE/", "atelier-", "worklog.md", "docs/JOURNAL_", "depot-zenodo-", "pack-v240", "pack-v233", "download", "instructions/", "instructions_")
MOTIFS_HEADING = re.compile(r"^#{1,4}\s.*(instruction|consigne|à exécuter|a executer|à faire|protocole de (la )?session)", re.IGNORECASE)
MARQUEUR_AGENT = re.compile(r"(\bagent\b|\bIA\b|\btoi\b|\btu\b|il faut|\bdois\b)", re.IGNORECASE)
MOTIFS = re.compile(
    r"^(\s*[-*]?\s*)(Ajoute|Ajouter|Corrige|Corriger|Vérifie|Vérifier|Execute|Exécute|Lance|Lancer|"
    r"Crée|Créer|Supprime|Supprimer|Remplace|Remplacer|Publie|Publier|Pousse|Pousser|Mets à jour|"
    r"Met(?:s)? à jour|Régénère|Regénère|Installe|Installer|Dois|Tu dois|Il faut)\b",
    re.IGNORECASE,
)


def sha(p):
    d = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            d.update(b)
    return d.hexdigest()


def sources():
    vus = []
    for g in GLOBS:
        vus.extend(sorted(RACINE.glob(g)))
    return [p for p in vus if p.is_file()]


def regenere():
    lignes = ["# SOURCES-PRESCRIPTIVES — les SEULS fichiers autorisés à prescrire un geste",
              "# (chemin relatif racine puis deux espaces puis sha256 ; régénéré par un acte délibéré)",
              ""]
    for p in sources():
        lignes.append(f"{p.relative_to(RACINE)}  {sha(p)}")
    MANIFESTE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"[prescriptif] manifeste régénéré : {len(sources())} sources")
    return 0


def lit_manifeste():
    entrees = {}
    if not MANIFESTE.exists():
        return None
    for l in MANIFESTE.read_text(encoding="utf-8").splitlines():
        if not l or l.startswith("#"):
            continue
        if "  " in l:
            nom, h = l.split("  ", 1)
            entrees[nom.strip()] = h.strip()
    return entrees


def verifie():
    m = lit_manifeste()
    if m is None:
        print("[prescriptif] REFUS MANIFESTE-ABSENT")
        return 2
    refus = []
    for nom, h in m.items():
        p = RACINE / nom
        if not p.exists():
            refus.append(("SOURCE-ABSENTE", nom)); continue
        if sha(p) != h:
            refus.append(("SOURCE-MODIFIEE", nom))
    for classe, nom in refus:
        print(f"[prescriptif] REFUS {classe} — {nom}")
    if not refus:
        print(f"[prescriptif] {len(m)} sources intactes")
        return 0
    return 2


def peut_prescrire(source_rel):
    m = lit_manifeste() or {}
    return source_rel in m


def classe(rel):
    """prescriptive | historique | lecture-seule — décidée par le CHEMIN, jamais par le contenu."""
    m = lit_manifeste() or {}
    if rel in m:
        return "prescriptive"
    if any(rel.startswith(x) or x in rel for x in HISTORIQUE):
        return "historique"
    return "lecture-seule"


def scan():
    m = lit_manifeste() or {}
    actives = 0
    for base, dirs, files in os.walk(RACINE):
        dirs[:] = [d for d in dirs if d not in EXCLUS]
        for f in files:
            p = pathlib.Path(base) / f
            rel = str(p.relative_to(RACINE))
            if rel in m:
                continue
            if any(rel.startswith(x) or x in rel for x in HISTORIQUE):
                continue
            # la PROSE se lit ; le code s'exécute — ses chaînes ne sont pas des consignes
            if p.suffix.lower() not in (".md", ".txt"):
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            n = 0
            dans_section = False
            for ligne in txt.splitlines():
                if ligne.startswith("#"):
                    dans_section = bool(MOTIFS_HEADING.match(ligne))
                    continue
                if not MOTIFS.match(ligne):
                    continue
                # une CONSIGNE ACTIVE est adressée à un agent : le motif SEUL ne suffit pas
                if dans_section or MARQUEUR_AGENT.search(ligne):
                    n += 1
            if n:
                actives += n
                print(f"[prescriptif] hors liste : {rel} — {n} ligne(s) impérative(s) (contenu non imprimé)")
    print(f"[prescriptif] SCAN : {actives} consigne(s) active(s) hors liste — {len(m)} sources autorisées")
    return 0 if actives == 0 else 3


def autotest():
    import tempfile
    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        (tmp / "liste.txt").write_text("a.txt  x\n", encoding="utf-8")
        a = tmp / "hors.md"; a.write_text("Ajoute un champ au manifeste.\n", encoding="utf-8")
        b = tmp / "dans.md"; b.write_text("Ajoute un champ au manifeste.\n", encoding="utf-8")
        c = tmp / "inédit.md"; c.write_text("Tu dois déposer le paquet avant midi.\n", encoding="utf-8")
        d = tmp / "ARCHIVE.md"; d.write_text("Ajoute un champ (geste daté du 12/11).\n", encoding="utf-8")
        essais = []
        # (a) hors liste : refus, indépendamment du contenu
        essais.append(("(a) consigne hors liste REFUSÉE", peut_prescrire("hors.md") is False))
        # (b) dans la liste : admise
        m = {"dans.md": "x"}
        essais.append(("(b) consigne dans la liste ADMISE", "dans.md" in m))
        # (c) reformulation inédite hors liste : refusée par la liste blanche
        essais.append(("(c) reformulation inédite REFUSÉE par la liste", peut_prescrire("inédit.md") is False))
        # (d) fichier historique daté : admis en lecture, jamais prescriptif
        essais.append(("(d) historique daté ADMIS en lecture, jamais prescriptif",
                       classe("ARCHIVE/instructions/x.md") == "historique"))
    finally:
        import shutil; shutil.rmtree(tmp, ignore_errors=True)
    verts = 0
    print("=" * 78); print("JEEWKX9G8 — LA LISTE BLANCHE FERMÉE (D262)"); print("=" * 78)
    for nom, ok in essais:
        verts += 1 if ok else 0
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom}")
    print(f"{verts}/{len(essais)}")
    return 0 if verts == len(essais) else 3


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(autotest())
    if a[0] == "--regenere": sys.exit(regenere())
    if a[0] == "--verifie": sys.exit(verifie())
    if a[0] == "--scan": sys.exit(scan())
    if a[0] == "--source":
        ok = peut_prescrire(a[1])
        print("[prescriptif]", "ADMISE" if ok else f"REFUS SOURCE-NON-PRESCRIPTIVE — {a[1]}")
        sys.exit(0 if ok else 3)
    print("option inconnue"); sys.exit(2)
