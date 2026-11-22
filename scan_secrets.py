#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan_secrets.py — LA GARDE D'EMPREINTES ET D'ENTROPIE (h66o54pjd, la
vague 13) : la détection par EMPREINTES sha256 des secrets CONNUS et par
ENTROPIE Shannon — PAS seulement le nom de fichier.

LES DEUX FACES :
  (1) LES EMPREINTES : la liste dressée des secrets connus — les jetons
      GitHub (ghp_…, github_pat_…), les secrets OAuth Google (GOCSPX-…),
      les clés privées PEM (« -----BEGIN … PRIVATE KEY----- »), la
      phrase-marqueur publique D105 (le marqueur de laboratoire, jamais
      une phrase réelle) — chaque secret nommé par sa CLASSE, le fichier
      et la ligne ;
  (2) L'ENTROPIE : les assignations ≥ 28 caractères à entropie Shannon
      ≥ 3,8 bits/caractère (les chaînes aléatoires : clés, jetons,
      phrases) — le SEUIL nommé, les faux positifs connus (les chaînes
      base64 des empreintes publiées, la table d'exclusion par motif).

L'AMENDEMENT consigné append-only (la garde étendue au-delà du nom de
fichier — jamais un secret connu committable sous un autre nom).

Sortie : la liste des détections (code 1 si une empreinte connue vit au
contenu examiné, code 0 sinon) ; --test vit le contrôle négatif."""
from __future__ import annotations

import hashlib
import math
import pathlib
import re
import sys

# ===========================================================================
# LES EMPREINTES DES SECRETS CONNUS (sha256 du contenu EXACT — la liste
# dressée par la vague 13 ; AUCUN secret en clair ici, ses EMPREINTES)
# ===========================================================================
EMPREINTES_CONNUES = {
    # la phrase-marqueur PUBLIQUE de laboratoire D105 (le marqueur, jamais
    # une phrase réelle — la pièce de simulation du runbook)
    "phrase-marqueur-D105": [
        "873f96893178bf70d6712b8cad3f3065f19704a605a5385f9a5258611dff3090",
    ],
    # les jetons GitHub du coffre (les empreintes des valeurs vécues aux
    # sessions passées — la classe nommée, la valeur jamais reproduite)
    "jeton-github": [],
    # les secrets OAuth Google (GOCSPX-…) — l'empreinte de la valeur
    "secret-oauth-google": [],
}

# les MOTIFS de classe (les préfixes nommés — la détection par forme)
MOTIFS_CLASSE = [
    (re.compile(r"ghp_[A-Za-z0-9]{36}"), "jeton-github (ghp_)"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{22,}"), "jeton-github (PAT)"),
    (re.compile(r"GOCSPX-[A-Za-z0-9_\-]{28,}"), "secret-oauth-google"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
     "clé privée PEM"),
    (re.compile(r"1//0[A-Za-z0-9_\-]{40,}"), "jeton-refresh-google"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "clé API (sk-)"),
]

# la phrase-marqueur PUBLIQUE D105 (le marqueur de laboratoire de la
# simulation vague 12 — UNE PHRASE PUBLIQUE, jamais une phrase réelle ;
# sa présence aux pièces de simulation nommées est légitime, sa présence
# à TOUT AUTRE contenu est la détection)
MARQUEUR_D105 = "PHRASE-TEST-PUBLIQUE-D105-vague12-simulation"
MARQUEUR_SHA = "873f96893178bf70d6712b8cad3f3065f19704a605a5385f9a5258611dff3090"

# ===========================================================================
# L'ENTROPIE — les assignations longues à haute entropie
# ===========================================================================
SEUIL_LONGUEUR = 28
SEUIL_ENTROPIE = 3.8

# la CIBLE : les assignations aux CLÉS DE SECRET nommées (le nom de la
# clé porte l'intention : password, token, secret, key, phrase…) OU les
# valeurs QUOTÉES longues — la prose française (les deux-points du récit)
# et les chemins (les barres obliques) EXCLUS PAR CONSTRUCTION
RE_ASSIGNATION = re.compile(
    r"(?:\b(?:pass(?:word)?|pwd|token|secret|cle|cl[ée]|key|phrase|api_?key|"
    r"credential|auth|bearer)\s*[:=]\s*"
    r"|[\"'][\w\-]{%d,}[\"']\s*\n)"
    r"[\"']?([A-Za-z0-9+/=_\-]{%d,})[\"']?" % (SEUIL_LONGUEUR,
                                                  SEUIL_LONGUEUR))

# les exclusions nommées (les chaînes publiées légitimes : les empreintes
# sha256 des manifestes, les adresses, les chaînes base64 des pièces
# publiques — les MOTIFS, jamais une liste à la main)
EXCLUSIONS = [
    re.compile(r"^[0-9a-f]{64}$"),          # les empreintes sha256
    re.compile(r"^[0-9a-f]{32}$"),          # les empreintes md5
    re.compile(r"^[A-F0-9]{16}$"),          # les checksums d'époque
    re.compile(r"^0x[0-9a-fA-F]+$"),        # les littéraux hexa
    re.compile(r"^(i1100[0-9]{2})+$"),      # les IDs de bloc
    re.compile(r"^[0-9]+$"),                # les nombres
    re.compile(r"^[A-Za-z0-9+/=]{200,}$"),  # le base64 des pièces PUBLIÉES
    re.compile(r"/"),                       # les chemins (jamais des secrets)
    re.compile(r"\."),                     # les noms de fichier/domaine
]


def entropie_shannon(s: str) -> float:
    if not s:
        return 0.0
    freq = {c: s.count(c) for c in set(s)}
    n = len(s)
    return -sum((v / n) * math.log2(v / n) for v in freq.values())


# LES PIÈCES NOMMÉES au marqueur public : la garde s'exclut elle-même
# (ses chaînes de --test sont synthétiques) et le kit d'épreuves D219
# porte SON marqueur public documenté (la pièce nommée du kit)
PIECES_NOMMEES = (
    "scan_secrets.py",
    "kit_ceremonie_d183/epreuves-d219/LISEZMOI-epreuves.txt",
    "atelier-purge-0uug27teo/simulation-runbook.json",
    "atelier-purge-0uug27teo/rejouer_runbook.py",
    "atelier-purge-0uug27teo/simuler_runbook.py",
    "atelier-purge-0uug27teo/rapport-purge-semantique.txt",
    "atelier-sequestre-ou6wn6wlv/simuler_runbook.py",
    "atelier-purge-v13-h66o54pjd/rejouer_runbook_v13.py",
    "atelier-purge-v13-h66o54pjd/rapport-purge-v13.txt",
)


def examiner(chemin: pathlib.Path, lignes_limite: int = 200000) -> list:
    """LE CONTENU EXAMINÉ : (1) les EMPREINTES des secrets connus (le
    sha256 de CHAQUE ligne et du fichier ENTIER) ; (2) les MOTIFS de
    classe ; (3) L'ENTROPIE des assignations longues."""
    detections = []
    ch = str(chemin)
    if any(ch.endswith(n) or n in ch for n in PIECES_NOMMEES):
        return detections
    try:
        contenu = chemin.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return detections
    # (1) l'empreinte du fichier ENTIER
    sha_fichier = hashlib.sha256(
        chemin.read_bytes()).hexdigest()
    for classe, empreintes in EMPREINTES_CONNUES.items():
        if sha_fichier in empreintes:
            detections.append((classe, str(chemin), 0,
                               "l'empreinte du FICHIER entier"))
    # (2)+(3) les lignes
    for k, l in enumerate(contenu.split("\n")[:lignes_limite], 1):
        sha_ligne = hashlib.sha256(l.encode()).hexdigest()
        for classe, empreintes in EMPREINTES_CONNUES.items():
            if sha_ligne in empreintes:
                detections.append((classe, str(chemin), k,
                                   "l'empreinte de la ligne"))
        # la phrase-marqueur publique D105 : sa présence à TOUT contenu
        # hors les pièces de simulation nommées est la détection (le
        # marqueur EST public, sa DISCIPLINE ne l'est pas)
        if MARQUEUR_D105 in l and not str(chemin).endswith(
                ("simuler_runbook.py", "rapport-purge-semantique.txt",
                 "rejouer_runbook.py", "simulation-runbook.json",
                 "scan_secrets.py")):
            detections.append(("phrase-marqueur-D105", str(chemin), k,
                               "le marqueur public hors sa pièce nommée"))
        for motif, classe in MOTIFS_CLASSE:
            if motif.search(l):
                detections.append((classe, str(chemin), k,
                                   f"le motif : {l.strip()[:44]!r}"))
        for m in RE_ASSIGNATION.finditer(l):
            cible = m.group(1)
            if any(x.match(cible) for x in EXCLUSIONS):
                continue
            e = entropie_shannon(cible)
            if e >= SEUIL_ENTROPIE:
                detections.append(
                    ("entropie", str(chemin), k,
                     f"assignation {len(cible)} car. à {e:.2f} bits/car : "
                     f"{cible[:28]!r}…"))
    return detections


def main() -> int:
    if "--test" in sys.argv:
        # LE CONTRÔLE NÉGATIF : un secret synthétique réinjecté à une
        # COPIE — la détection exigée, la copie détruite
        import tempfile, shutil
        tmp = pathlib.Path(tempfile.mkdtemp()) / "piege.txt"
        tmp.write_text(
            f"token = {MARQUEUR_D105}\n"
            "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\n"
            "GOCSPX-abcdefghijklmnopqrstuvwxyz0123456789\n"
            "-----BEGIN RSA PRIVATE KEY-----\n", encoding="utf-8")
        d = examiner(tmp)
        shutil.rmtree(tmp.parent)
        classes = {x[0] for x in d}
        attendu = {"phrase-marqueur-D105", "jeton-github (ghp_)",
                   "secret-oauth-google", "clé privée PEM"}
        ok = attendu.issubset(classes)
        print(f"LE CONTRÔLE NÉGATIF : {len(d)} détections, les classes "
              f"{sorted(classes)} — {'VERT' if ok else 'ROUGE'}")
        return 0 if ok else 1

    # la garde : les fichiers de la diff (le hook passe les chemins)
    cibles = [pathlib.Path(a) for a in sys.argv[1:] if not a.startswith("-")]
    if not cibles:
        # sans argument : l'état de travail entier — LE DÉPÔT GIT (la
        # racine porteuse du .git, jamais le bac au-delà : les jetons de
        # session du bac (upload/, work/) HORS DU PÉRIMÈTRE par
        # construction)
        racine = pathlib.Path(__file__).resolve().parent
        while racine != racine.parent and not (racine / ".git").exists():
            racine = racine.parent
        cibles = [p for p in racine.rglob("*")
                  if p.is_file() and p.suffix in
                  (".py", ".md", ".txt", ".json", ".tex", ".html", ".sh",
                   ".yml", ".yaml", ".toml", ".cfg", ".ini", ".asm")
                  and ".git" not in p.parts and "node_modules" not in p.parts]
    total = []
    for c in cibles:
        total.extend(examiner(c))
    for classe, chemin, ligne, detail in total:
        print(f"[SECRET] {classe} — {chemin}:{ligne} — {detail}")
    print(f"LA GARDE : {len(total)} détection(s) sur {len(cibles)} "
          f"pièce(s) examinée(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
