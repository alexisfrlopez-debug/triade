#!/usr/bin/env python3
"""diff_nul.py — LE DIFF NUL MESURÉ PAR SCRIPT (le critère de sortie du chantier
M6-(b) : « les instances des deux profils chargent les MÊMES fichiers I,
empreintes identiques », D149-(3)).

Trois recoupements, rejouables :

  1. LES FICHIERS CANONIQUES — l'instance Linux (build_corpus.py) charge
     EXACTEMENT les fichiers de unix/I/ (les révisions R+1) : empreintes
     sha256 mesurées, aucune copie du corpus nulle part ailleurs dans le
     dépôt (une copie tuerait le diff nul — c'est la preuve que «
     l'intention vit dans I et pas dans les octets »). M7 chargera les
     MÊMES fichiers (la troisième instanciation, D149-(7)).

  2. L'ÉQUIVALENCE DES OBSERVABLES R1 ↔ R+1 — pour chaque contrat révisé,
     les sections OBSERVABLES du contrat (post Q, échecs E, vecteurs V)
     sont extraites de l'ancêtre scellé (m0/I, m1/I, m2/I — INTACTS) et de
     la révision, puis comparées : le diff est NUL sur les observables
     (aux paramétrisations de profil près, nommées : le terminateur de
     ligne de libc-08:R2, l'émission de tcp-11:R1 — chaque écart restant
     est NOMMÉ et motivé, jamais silencieux). Les pré-conditions seules
     bougent : c'est la granularité.

  3. L'INVARIANCE DES SCELLÉS — les empreintes sha256 des artefacts
     Windows (hello.exe 0.1.0, selftest.exe 0.2.0, echo.exe 0.3.0,
     proxy.exe 0.4.0, proxy.exe 0.6.0) sont identiques à l'état zéro
     mesuré avant le geste (scripts/etat_zero_m6b.json) : les scellés ne
     bougent pas.

Usage : python3 diff_nul.py [--etat-zero scripts/etat_zero_m6b.json]
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
UNIX = ICI
RACINE = os.path.dirname(UNIX)

# Le corpus : (révision unix/I, ancêtre scellé) — l'audit de couplage
CORPUS = [
    ("libc-01-memcpy-r2.md",       "../m1/I/libc-01-memcpy.md"),
    ("libc-02-memcmp-r2.md",       "../m1/I/libc-02-memcmp.md"),
    ("libc-03-strlen-r2.md",       "../m1/I/libc-03-strlen.md"),
    ("libc-04-itoa-r3.md",         "../m1/I/libc-04-itoa.md"),
    ("libc-05-zone-alloc-r2.md",   "../m1/I/libc-05-zone-alloc.md"),
    ("libc-06-zone-reset-r2.md",   "../m1/I/libc-06-zone-reset.md"),
    ("libc-07-memset-r2.md",       "../m1/I/libc-07-memset.md"),
    ("libc-08-autotest-r3.md",     "../m1/I/libc-08-autotest.md"),
    ("hello-02-ecrire-r2.md",      "../m0/I/hello-02-write.md"),
    ("hello-03-sortir-r2.md",      "../m0/I/hello-03-exit.md"),
    ("tcp-07-patch-r4.md",         "../m2/I/tcp-07-patch.md"),
    ("tcp-11-journal-r2.md",       "../m2/I/tcp-11-journal.md"),
]

SCELLES = [
    ("m0/hello.exe", "hello.exe — scellé 0.1.0 (M0)"),
    ("m1/selftest.exe", "selftest.exe — scellé 0.2.0 (M1)"),
    ("m2/echo.exe", "echo.exe — scellé 0.3.0 (M2)"),
    ("m3/proxy.exe", "proxy.exe — scellé 0.4.0 (M3)"),
    ("m5/proxy.exe", "proxy.exe — scellé 0.6.0 (M5, finale)"),
]

# Les écarts d'observables NOMMÉS (la granularité elle-même — chaque ligne
# est un couple (ancêtre, révision) dont la différence est la
# PARAMÉTRISATION du profil, jamais un changement sémantique)
ECARTS_MOTIVES = {
    ("libc-08-autotest-r3.md", "vecteurs"):
        "V2 : « OK\\r\\n » (Windows) -> la ligne du profil (terminateur \\n, "
        "frag-con) — le préfixe et le verdict sont invariants",
    ("libc-08-autotest-r3.md", "post"):
        "Q2/Q3 : le service d'écriture/sortie du profil (WriteFile/ExitProcess "
        "-> écrire/sortir, N rendu au principal — frag-con, l'observable la "
        "ligne exacte et le code 0/1 est invariant)",
    ("tcp-11-journal-r2.md", "post"):
        "Q2 : le verdict BRUT du service (BOOL Windows / rax Linux) — le verdict "
        "propagé sans transformation est l'observable invariante",
    ("hello-02-ecrire-r2.md", "post"):
        "Q1 : le verdict brut du service d'écriture du profil (frag-con)",
    ("hello-03-sortir-r2.md", "post"):
        "Q1 : le service de sortie du profil (ExitProcess -> exit_group, frag-con)",
    ("tcp-07-patch-r4.md", "post"):
        "Q4/Q5 : le service de protection du profil et ses constantes (0x40/0x20 "
        "-> 0x7/0x5, frag-con — les codes 1-5 et la bascule atomique invariants)",
}


def sha(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def extraire_section(texte: str, marque_debut: str, marque_fin: str) -> str:
    lignes = texte.splitlines()
    indices = [i for i, l in enumerate(lignes) if re.match(marque_debut, l.strip())]
    if not indices:
        return ""
    debut = indices[0]
    fin = len(lignes)
    for i in range(debut + 1, len(lignes)):
        if re.match(marque_fin, lignes[i].strip()):
            fin = i
            break
    return "\n".join(lignes[debut:fin])


def _jetons(texte: str) -> tuple[set, set, set]:
    """Extrait les JETONS OBSERVABLES d'un texte de contrat :
    (chaînes citées, codes d'échec « code N », volumes de vecteurs).
    Les noms de services et constantes de plateforme (WriteFile, PAGE_*, 0x40,
    0x28…) NE SONT PAS des observables : ils vivent en frag-con — ils sont
    exclus par construction. La comparaison porte la SÉMANTIQUE : les
    verdicts, les codes, les messages exacts, les volumes."""
    chaines = set(re.findall(r"[«\"]([^»\"]+)[»\"]", texte))
    codes = set(re.findall(r"code (\d+)", texte))
    # les VOLUMES de test : les grands nombres (groupés à la française ou
    # nus) — « 12 000 cas », « 4 000 lignes », « 3 000 séquences ». Les
    # petits nombres (versions, tailles, indices) ne sont pas des volumes :
    # ils vivent dans les chaînes citées et les codes quand ils sont
    # sémantiques.
    volumes = set(re.findall(r"\b\d{1,3}(?: \d{3})+\b", texte)) \
        | set(re.findall(r"\b\d{4,}\b", texte))
    return chaines, codes, volumes


def comparer_observables(ancetre: str, revision: str, nom: str) -> list[str]:
    """Compare les jetons observables ancêtre ↔ révision, section par section.
    Tout écart de chaîne citée est REFUSÉ sauf s'il est NOMMÉ (la table des
    écarts motivés — la paramétrisation de profil, jamais un changement
    sémantique). Les codes et les volumes ne tolèrent AUCUN écart."""
    rapports = []
    sections = (("post", r"^post\s*:"), ("échecs", r"^Échecs\s*:"),
                ("vecteurs", r"^Vecteurs\s*:"))
    for section, debut in sections:
        def couper(texte):
            lignes = texte.splitlines()
            idx = [i for i, l in enumerate(lignes) if re.match(debut, l.strip())]
            if not idx:
                return ""
            d = idx[0] + 1
            f = len(lignes)
            for i in range(d, len(lignes)):
                if re.match(r"^(inv|Échecs|Vecteurs|Fixtures|Provenance|Décisions|Historique)\s*:",
                            lignes[i].strip()):
                    f = i
                    break
            return "\n".join(lignes[d:f])
        ca, ka, va = _jetons(couper(ancetre))
        cr, kr, vr = _jetons(couper(revision))
        if ka != kr:
            raise SystemExit(f"DIFF NON NUL : {nom} § {section} — les codes d'échec "
                             f"{sorted(ka)} -> {sorted(kr)} : un observable a bougé !")
        if va != vr:
            manquent = va - vr
            nouveaux = vr - va
            raise SystemExit(f"DIFF NON NUL : {nom} § {section} — les volumes "
                             f"{sorted(manquent)} disparus, {sorted(nouveaux)} apparus")
        if ca == cr:
            rapports.append(f"{nom} § {section} : jetons identiques "
                            f"({len(ca)} chaînes, {len(ka)} codes)")
        else:
            mot = ECARTS_MOTIVES.get((nom, section))
            if not mot:
                raise SystemExit(f"DIFF NON NUL : {nom} § {section} — chaînes citées "
                                 f"{sorted(ca - cr)} disparues, {sorted(cr - ca)} apparues, "
                                 f"écart NON MOTIVÉ")
            rapports.append(f"{nom} § {section} : chaînes écartées NOMMÉES — {mot}")
    return rapports


def main() -> int:
    print("=== LE DIFF NUL (mesuré par script — D149-(3), chantier M6-(b)) ===")
    rapports = []

    # 1 — les fichiers canoniques : empreintes, aucune copie
    print("\n[1] Les fichiers canoniques de la couche I (unix/I/)")
    total = 0
    for revision, _ in CORPUS + [("corpus-13-principal.md", "")]:
        chemin = os.path.join(UNIX, "I", revision)
        if not os.path.exists(chemin):
            raise SystemExit(f"fichier canonique absent : {chemin}")
        print(f"  {revision:32s} sha256:{sha(chemin)[:24]}…")
        total += 1
    # aucune copie du corpus hors unix/I (le diff nul exige l'unicité)
    for racine_dir, dirs, fichiers in os.walk(RACINE):
        dirs[:] = [d for d in dirs if d not in
                   (".git", ".keys", "__pycache__", "carte", "carte-corpus",
                    "archives-bundles", "bundles-060", "node_modules")]
        if os.path.relpath(racine_dir, RACINE) == "unix/I":
            continue
        for f in fichiers:
            for revision, _ in CORPUS:
                if f == revision:
                    raise SystemExit(
                        f"COPIE INTERDITE : {os.path.join(racine_dir, f)} — le corpus "
                        f"vit à unix/I/ et NULLE PART ailleurs (le diff nul)")
    rapports.append(f"fichiers canoniques : {total} contrats, empreintes mesurées, "
                    f"zéro copie hors unix/I/")
    print(f"  aucune copie hors unix/I/ — l'instance Linux charge LES fichiers "
          f"canoniques (M7 les chargera aussi)")

    # 2 — l'équivalence des observables R1 ↔ R+1
    print("\n[2] L'équivalence des observables (ancêtres scellés ↔ révisions)")
    for revision, ancetre_relp in CORPUS:
        ancetre = os.path.normpath(os.path.join(UNIX, ancetre_relp))
        with open(ancetre, encoding="utf-8") as f:
            texte_a = f.read()
        with open(os.path.join(UNIX, "I", revision), encoding="utf-8") as f:
            texte_r = f.read()
        rapports.extend(comparer_observables(texte_a, texte_r, revision))
    n_identiques = sum(1 for r in rapports if "jetons identiques" in r)
    n_motives = sum(1 for r in rapports if "NOMMÉES" in r or "NOMMÉ" in r)
    print(f"  {n_identiques} sections identiques (normalisées), "
          f"{n_motives} écarts NOMMÉS et motivés (la paramétrisation frag-con)")
    rapports.append(f"équivalence : {n_identiques} identiques + {n_motives} écarts "
                    f"motivés — les observables sont invariants, la granularité seule bouge")

    # 3 — l'invariance des scellés
    print("\n[3] L'invariance des scellés Windows (l'état zéro ↔ maintenant)")
    etat_zero = os.path.join(RACINE, "scripts", "etat_zero_m6b.json")
    if "--etat-zero" in sys.argv:
        etat_zero = sys.argv[sys.argv.index("--etat-zero") + 1]
    with open(etat_zero, encoding="utf-8") as f:
        z = json.load(f)
    for rel, role in SCELLES:
        chemin = os.path.join(RACINE, rel)
        actuel = sha(chemin) if os.path.exists(chemin) else None
        attendu = (z.get("scelles", {}).get(rel) or {}).get("sha256")
        if actuel != attendu:
            raise SystemExit(f"SCELLÉ MUTÉ : {rel} sha256 {actuel} != état zéro "
                             f"{attendu} — les scellés ne bougent pas (D149-(3))")
        print(f"  {rel:18s} INTACT — sha256:{actuel[:24]}… ({role})")
    rapports.append(f"invariance : {len(SCELLES)} scellés octet-identiques à l'état "
                    f"zéro (mesuré avant le geste)")

    empreinte = hashlib.sha256("\n".join(rapports).encode()).hexdigest()
    print(f"\n[diff-nul] VERT — {len(rapports)} recoupements, empreinte {empreinte[:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
