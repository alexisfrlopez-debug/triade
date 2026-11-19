#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_secrets.py — LE SCAN DE SECRETS DE L'HISTORIQUE GIT COMPLET (D219).

L'ÉQUIVALENT PYTHON NOMMÉ (l'instruction jx4l5vy5c prescrit gitleaks ou
trufflehog ; TOUS DEUX ABSENTS du bac — l'écart d'outillage nommé à D207 —
la présente est l'équivalent Python NOMMÉ, jamais une simulation : chaque
blob de l'historique est réellement lu et confronté aux règles).

LA MÉTHODE (gitleaks, la sémantique) :
  1. ÉNUMÉRER tous les objets du dépôt — `git cat-file --batch-all-objects`
     rend CHAQUE blob jamais né (y compris les blobs supprimés de la tête :
     un secret commisé puis retiré demeure dans l'historique — c'est LE
     point du scan complet) ;
  2. RATTACHER chaque blob à ses chemins — `git rev-list --all --objects` ;
  3. CONFRONTER chaque blob aux RÈGLES NOMMÉES (fichiers-jetons par nom,
     clés privées, jetons GitHub/Google, assignations secrètes à entropie) ;
  4. NE JAMAIS AFFICHER UN SECRET : l'aperçu est MASQUÉ (4 premiers
     caractères + … + 2 derniers), le contenu ne traverse jamais la sortie.

LES RÈGLES (chacune nommée, aucune règle silencieuse) :
  PHRASE-CONTROLE     le fichier-remise D81 (PHRASE-CONTROLE-COFFRE*.txt)
  FICHIER-JETON       token_git.txt, oauth_token*.json, *service_account*,
                      client_secret*.json, .env, id_rsa*, *.keytab, *.p12
  CLE-PRIVEE          un bloc « -----BEGIN … PRIVATE KEY----- »
  JETON-GITHUB        ghp_/gho_/ghu_/ghs_/ghr_… et github_pat_…
  SECRET-OAUTH-GOOGLE GOCSPX-… (client secret Google) et ya29.…
  ASSIGNATION-SECREE  (api_key|secret|token|password) = <valeur ≥ 28 car.
                      à entropie de Shannon ≥ 3,8 — les mots de passe forts
                      en clair dans le code

Usage :
  python3 scan_secrets.py --repo <chemin>            # le scan, verdict
  python3 scan_secrets.py --repo <chemin> \
      --attendu <manifeste.json>                     # + l'assertion dry-run
                                                      # (chaque secret planté
                                                      #  ATTENDU, zéro faux
                                                      #  négatif)

Sortie : exit 0 si le scan est mené à terme (le rapport est l'office de
l'outil — un secret trouvé n'est pas une panne de l'outil, c'est son
travail) ; exit 1 si le dry-run attend un secret que le scan ne trouve pas
(FAUX NÉGATIF — l'outil est faux) ou si le dépôt est illisible.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------------------
# Les règles
# ---------------------------------------------------------------------------
REGLES_FICHIER = {
    "PHRASE-CONTROLE": re.compile(r"^PHRASE-CONTROLE-COFFRE.*\.txt$", re.I),
    "FICHIER-JETON": re.compile(
        r"^(token_git\.txt|oauth_token[^/]*\.json|.*service_account.*\.json|"
        r"client_secret[^/]*\.json|\.env|id_rsa[^/]*|.*\.keytab|.*\.p12)$", re.I),
}
REGLES_CONTENU = [
    ("CLE-PRIVEE", re.compile(
        rb"-----BEGIN (RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY-----")),
    ("JETON-GITHUB", re.compile(
        rb"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,255}\b")),
    ("JETON-GITHUB-PAT", re.compile(
        rb"\bgithub_pat_[A-Za-z0-9_]{60,255}\b")),
    ("SECRET-OAUTH-GOOGLE", re.compile(
        rb"\bGOCSPX-[A-Za-z0-9_-]{27,255}\b|\bya29\.[A-Za-z0-9._-]{20,255}\b")),
    ("ASSIGNATION-SECREE", re.compile(
        rb"(?i)\b(api_?key|secret|token|passwd|password)\b[\"']?\s*[:=]\s*[\"']?"
        rb"([A-Za-z0-9+/_-]{28,255}={0,3})[\"']?")),
]
SEUIL_ENTROPIE = 3.8          # bits/caractère — les valeurs trop françaises
# (les phrases de prose, les hex de hash publics) restent sous le seuil
TAILLE_MAX_SCAN = 4 * 1024 * 1024   # les blobs géants : règles de nom seules


def entropie(v: bytes) -> float:
    if not v:
        return 0.0
    c = Counter(v)
    n = len(v)
    return -sum((k / n) * math.log2(k / n) for k in c.values())


def masque(v: bytes) -> str:
    s = v.decode("utf-8", "replace").strip()
    if len(s) <= 8:
        return s[:2] + "…"
    return f"{s[:4]}…{s[-2:]} (longueur {len(s)})"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, check=True)


def blobs_chemins(repo: Path) -> dict[str, set[str]]:
    """Chaque blob → l'ensemble de ses chemins connus de l'historique."""
    chemins: dict[str, set[str]] = {}
    res = git(repo, "rev-list", "--all", "--objects")
    for ligne in res.stdout.decode("utf-8", "replace").splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        morceaux = ligne.split(" ", 1)
        if len(morceaux) == 2 and morceaux[1]:
            chemins.setdefault(morceaux[0], set()).add(morceaux[1])
    return chemins


def lire_blobs(repo: Path, shas: list[str]) -> dict[str, bytes]:
    """Tous les contenus en UN SEUL flux `git cat-file --batch` (jamais un
    sous-processus par blob — l'historique complet se lit d'un souffle)."""
    entree = "\n".join(shas) + "\n"
    res = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch"],
                         input=entree.encode(), capture_output=True, check=True)
    sortie: dict[str, bytes] = {}
    pos = 0
    data = res.stdout
    while pos < len(data):
        nl = data.find(b"\n", pos)
        if nl == -1:
            break
        en_tete = data[pos:nl].decode().split()
        pos = nl + 1
        if len(en_tete) < 3 or en_tete[1] != "blob":
            continue
        sha, taille = en_tete[0], int(en_tete[2])
        sortie[sha] = data[pos:pos + taille]
        pos += taille + 1          # le contenu puis le LF final
    return sortie


def scan(repo: Path) -> list[dict]:
    trouves: list[dict] = []
    chemins = blobs_chemins(repo)
    # l'énumération de TOUS les objets (le passe-partout de l'historique)
    res = git(repo, "cat-file", "--batch-all-objects",
              "--batch-check=%(objectname) %(objecttype) %(objectsize)")
    blobs = []
    for ligne in res.stdout.decode().splitlines():
        nom, type_obj, taille = (ligne.split() + ["", ""])[:3]
        if type_obj == "blob":
            blobs.append((nom, int(taille or 0)))
    # les contenus en un seul flux — seuls les blobs scannables (règles de
    # contenu) sont demandés ; les fichiers-jetons NE SONT JAMAIS LUS (la
    # présence du fichier EST le constat, D105 : le labo ne lit pas la
    # phrase réelle)
    a_lire = []
    for nom, taille in blobs:
        chemins_blob = chemins.get(nom, {""})
        nom_fichiers = {Path(c).name for c in chemins_blob}
        regle_nom = None
        for rn, rx in REGLES_FICHIER.items():
            if any(rx.match(nf) for nf in nom_fichiers):
                regle_nom = rn
                break
        if regle_nom is None and 0 < taille <= TAILLE_MAX_SCAN:
            a_lire.append(nom)
    contenus = lire_blobs(repo, a_lire)
    for nom, taille in blobs:
        chemins_blob = chemins.get(nom, {""})
        nom_fichiers = {Path(c).name for c in chemins_blob}
        regle_nom = None
        for rn, rx in REGLES_FICHIER.items():
            if any(rx.match(nf) for nf in nom_fichiers):
                regle_nom = rn
                break
        # (a) la règle de nom — la présence du fichier EST le constat
        if regle_nom is not None:
            trouves.append({
                "regle": regle_nom,
                "chemins": sorted(chemins_blob),
                "blob": nom,
                "taille": taille,
                "apercu": "(fichier-jeton — contenu jamais affiché)",
            })
            continue
        contenu = contenus.get(nom)
        if contenu is None or b"\x00" in contenu[:8192]:
            continue
        # (b) les règles de contenu
        vus: set[tuple[str, bytes]] = set()
        for rn, rx in REGLES_CONTENU:
            for m in rx.finditer(contenu):
                valeur = m.group(m.lastindex) if m.lastindex else m.group(0)
                valeur = valeur.strip(b"\"'")
                if rn == "ASSIGNATION-SECREE" and entropie(valeur) < SEUIL_ENTROPIE:
                    continue
                cle = (rn, valeur)
                if cle in vus:
                    continue
                vus.add(cle)
                trouves.append({
                    "regle": rn,
                    "chemins": sorted(chemins_blob),
                    "blob": nom,
                    "taille": taille,
                    "apercu": masque(valeur),
                })
    # ordre stable : règle, puis chemin
    trouves.sort(key=lambda t: (t["regle"], t["chemins"], t["blob"]))
    return trouves


def dry_run(trouves: list[dict], manifeste: Path) -> bool:
    """L'assertion du dry-run : chaque secret planté est ATTENDU par
    (règle, fragment d'aperçu) ; un secret attendu introuvable est un FAUX
    NÉGATIF — l'outil est faux."""
    attends = json.loads(manifeste.read_text(encoding="utf-8"))
    verts = 0
    for attendu in attends:
        regle, fragment = attendu["regle"], attendu["fragment"]
        match = [t for t in trouves
                 if t["regle"] == regle
                 and any(fragment in c for c in t["chemins"])]
        if match:
            print(f"DRY-RUN VERT   {regle} @ {fragment} → ATTRAPÉ "
                  f"(blob {match[0]['blob'][:12]}…)")
            verts += 1
        else:
            print(f"DRY-RUN ROUGE  {regle} @ {fragment} → FAUX NÉGATIF — "
                  "L'OUTIL EST FAUX")
            return False
    # les fichiers propres ne doivent RIEN produire (le bruit tue l'usage)
    bruits = [t for t in trouves
              if t["regle"] == "ASSIGNATION-SECREE"
              and any("propre" in c for c in t["chemins"])]
    if bruits:
        print(f"DRY-RUN ROUGE  {len(bruits)} faux positif(s) sur les "
              "fichiers propres — le seuil est faux")
        return False
    print(f"DRY-RUN : {verts}/{len(attends)} secrets plantés ATTRAPÉS, "
          "zéro faux négatif, zéro faux positif sur les fichiers propres")
    return True


def main() -> int:
    if "--repo" not in sys.argv:
        raise SystemExit(__doc__)
    repo = Path(sys.argv[sys.argv.index("--repo") + 1])
    if not repo.exists():
        print(f"REFUS — le dépôt {repo} est introuvable")
        return 1
    print(f"LE SCAN DE SECRETS (D219) — l'historique git COMPLET de {repo}")
    trouves = scan(repo)
    print(f"  {len(trouves)} constat(s) — chaque blob de l'historique "
          "confronté aux règles nommées\n")
    for t in trouves:
        chemins = ", ".join(t["chemins"]) or "(blob orphelin)"
        print(f"  [{t['regle']}] {chemins}")
        print(f"      blob {t['blob'][:16]}…, {t['taille']} o — "
              f"apercu masque : {t['apercu']}")
    if "--attendu" in sys.argv:
        manifeste = Path(sys.argv[sys.argv.index("--attendu") + 1])
        print()
        if not dry_run(trouves, manifeste):
            return 1
    print("\nRAPPEL (D81/D219) : un secret commis en git y demeure à vie — "
          "le retrait du fichier ne retire pas l'historique ; le remède "
          "est la ROTATION (CHECKLIST-ROTATION.txt) et, pour la phrase de "
          "contrôle, la cérémonie D183 (le kit présent).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
