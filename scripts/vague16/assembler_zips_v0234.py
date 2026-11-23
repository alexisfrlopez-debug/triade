#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0234.py — LA RELEASE CORRECTIVE v0.23.4 (la vague 16, la
commande du maître « fais une mise à jour des kits soumission/présentation et
complet sur les dépôts git/drive et zenodo si besoin »).

LE CONSTAT : les CINQ PIÈCES n'ont PAS bougé depuis v0.23.3 (leurs cinq sha256
== les empreintes consignées, byte-byte). La SOUMISSION et la PRÉSENTATION sont
donc RECONDUITES OCTET POUR OCTET (le précédent v0.23.1 : la release corrective
porte le complet régénéré, les deux autres byte-byte sous leur nom d'origine).

CE QUI EST RÉGÉNÉRÉ : LE COMPLET — les entrées du complet v0.23.3 RECONDUITES
octet pour octet (README excepté) PLUS tout ce que le dépôt a gagné depuis :
les HUIT ateliers de la vague 15 continuée et de la vague 16, les SIX plans
gelés de la vague 16 et sa table d'empreintes, les scripts de la vague 16
(le linter des résidus, le publisher), les rapports de la vague 16, le worklog
et le REPRISE courants.

LES DEUX PORTES :
  (A) LES PIÈCES BYTE-BYTE — les cinq sha256 confrontés aux empreintes
      consignées de v0.23.3 ; un écart REFUSE l'assemblage ;
  (B) LE LINTER D'ÉDITION v233 RE-JOUÉ — 222 VERT et UN ROUGE NOMMÉ : la
      dérive de l'extracteur (pdftotext 26.09 rend 3 tokens numériques de plus
      que l'extraction de l'édition, 1991 contrôlés). La porte (A) prouve les
      pièces identiques — le verdict d'édition (223 VERT) demeure ; le rouge
      est NOMMÉ au README, jamais dissimulé, et REFUSE l'assemblage s'il
      sort de la classe d'extraction.
"""

import hashlib
import pathlib
import re
import subprocess
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[2]
V15 = REPO / "scripts" / "vague15"
V16 = REPO / "scripts" / "vague16"
DEPOT = REPO / "depot-zenodo-v0233"
OUT = REPO / "depot-zenodo-v0234"
OUT.mkdir(exist_ok=True)

EMPREINTES_V233 = {
    "a2835461edb30f15a212dbe06eb2420c4452f6054110363c287af63c5a020c08":
        "manuscrit", "06171f7ff2fb462abe8bffea9584cfe343d9631ef5d08c56b19b9f84be7b9c95":
        "specification", "5930539839b2e49469b5af7797e1cd2e1a7102c1622fbe4b7fdaac570afb1c82":
        "livre", "69a0b4c30acdd579306ae38b82a634b2f55f172ebe72cf8f8f5af3ea83337bf0":
        "preuves", "0b5e843b94598dca0c79d5cb886ff090c58486eea4a3ef9c29103c947cccc674":
        "presentation",
}
PIECES = {
    "manuscrit": REPO / "edition-v0230" / "main.pdf",
    "specification": REPO / "scripts" / "spec_v158" / "main.pdf",
    "livre": REPO / "scripts" / "livre_v17" / "final.pdf",
    "preuves": V15 / "TRIADE_preuves_et_calculs_v0.23.3.pdf",
    "presentation": V15 / "TRIADE_presentation_v233.pdf",
}

ATELIERS_V16 = (
    "atelier-ajouter-v7-81eruqtl6",        # la vague 15 continuée (Entrée 392)
    "atelier-corpusv2-avmwtf5w",           # la vague 15 continuée (Entrée 393)
    "atelier-campagne-v6-0j7ywza2h",
    "atelier-ancrage-sentinelle-ru2rfjl2g",
    "atelier-couloirs-scelles-io3uh37cj",
    "atelier-cloture-tamarin-0pljbn96b",
    "atelier-audit-splits-am9d6o2th",
    "atelier-residus-86d3ushrr",
)
RAPPORTS_V16 = (
    "rapport-corpus-v2-20261123.txt",
    "rapport-depots-zenodo-20261123.txt",
    "rapport-instrument-20261123.txt",
    "rapport-vague16-20261123.txt",
    "rapport-vague16-suite-20261123.txt",
    "rapport-vague16-cloture-20261123.txt",
)


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


# ---- (A) LES PIÈCES BYTE-BYTE ---------------------------------------------
print("[A] les cinq pièces confrontées aux empreintes consignées v0.23.3…")
for nom, chemin in PIECES.items():
    if not chemin.is_file():
        raise SystemExit(f"PIÈCE ABSENTE : {nom} ({chemin})")
    h = sha256(chemin)
    if h not in EMPREINTES_V233:
        raise SystemExit(f"ÉCART D'EMPREINTE : {nom} — les pièces ne sont pas "
                         f"celles de v0.23.3, l'assemblage est REFUSÉ")
    print(f"    {nom:14s} {h[:16]}… ✓ (l'empreinte consignée)")
print("    LES CINQ PIÈCES SONT BYTE-BYTE CELLES DE v0.23.3")

# ---- (B) LE LINTER D'ÉDITION RE-JOUÉ --------------------------------------
print("[B] le linter d'édition v233 re-joué (la dérive de l'extracteur NOMMÉE)…")
r = subprocess.run([sys.executable, str(V15 / "linter_v233.py")],
                   capture_output=True, text=True, cwd=str(REPO))
sortie = r.stdout + r.stderr
m = re.search(r"LE LINTER v233 : (\d+) VERT, (\d+) ROUGE", sortie)
if not m:
    print(sortie[-1500:])
    raise SystemExit("LE LINTER v233 : sortie illisible — l'assemblage REFUSÉ")
verts, rouges = int(m.group(1)), int(m.group(2))
print(f"    le linter : {verts} VERT, {rouges} ROUGE")
if rouges:
    lignes_rouges = [l.strip() for l in sortie.splitlines() if l.strip().startswith("ROUGE")]
    hors_extraction = [l for l in lignes_rouges if "EXTRACTION" not in l]
    if rouges > 1 or hors_extraction:
        for l in lignes_rouges:
            print("    " + l[:160])
        raise SystemExit("ROUGE HORS DE LA CLASSE D'EXTRACTION — l'assemblage REFUSÉ")
    print("    LE ROUGE UNIQUE EST LA CLASSE D'EXTRACTION (la dérive de "
          "pdftotext — les pièces byte-byte, le verdict d'édition demeure) : "
          "NOMMÉ au README, l'assemblage poursuit")

# ---- LA SOUMISSION ET LA PRÉSENTATION : RECONDUITES OCTET POUR OCTET ------
for nom in ("TRIADE_soumission_v0.23.3.zip", "TRIADE_presentation_v0.23.3.zip"):
    # la soumission et le complet vivent au dossier de dépôt ; LA PRÉSENTATION À LA RACINE
    src = DEPOT / nom
    if not src.is_file():
        src = REPO / nom
    dst = OUT / nom
    if not src.is_file():
        raise SystemExit(f"ARCHIVE v0.23.3 ABSENTE : {nom} (ni {DEPOT} ni {REPO})")
    if not dst.exists() or sha256(dst) != sha256(src):
        dst.write_bytes(src.read_bytes())
    print(f"[reconduit byte-byte] {nom} : {dst.stat().st_size} o, "
          f"sha256 {sha256(dst)[:16]}…")

# ---- LE COMPLET v0.23.4 --------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.23.4.zip"
if CMP.exists():
    CMP.unlink()

README = (
    "TRIADE — l'archive complète de l'édition v0.23.4 (LA RELEASE CORRECTIVE de la "
    "vague 16).\n\n"
    "CE QUI CHANGE : les CINQ PIÈCES N'ONT PAS BOUGÉ — leurs cinq sha256 sont "
    "byte-byte ceux de v0.23.3 (prouvé par empreintes_livrables_v0.23.3.txt). La "
    "SOUMISSION et la PRÉSENTATION sont donc RECONDUITES OCTET POUR OCTET sous "
    "leur nom d'origine (le précédent de la release corrective v0.23.1). LE "
    "COMPLET, lui, porte tout ce que le dépôt a gagné depuis v0.23.3 : les HUIT "
    "ateliers de la vague 15 continuée et de la vague 16, les SIX PLANS GELÉS de "
    "la vague 16 et leur table d'empreintes, les SCRIPTS de la vague 16 (le "
    "linter des résidus v233, le publisher du corpus), les RAPPORTS de la vague "
    "16, le WORKLOG et le REPRISE à l'état de la clôture.\n\n"
    "LA VAGUE 16 (six instructions du 23/11/2026) : (1) am9d6o2th — L'AUDIT "
    "D'ÉTANCHÉITÉ DES SPLITS : la fuite par contrat du corpus v2 constatée (dix "
    "contrats partagés entre TRAIN et DEV/TEST — le TEST contaminé par "
    "construction) et réparée par GROUPE-DE-CONTRAT à la graine 20261126 (TRAIN "
    "14, DEV 2, TEST 2), le TEST nu, le canari unique au TRAIN, l'audit rejoué "
    "ÉTANCHE et les dix rebuilds bit-identiques ; (2) 86d3ushrr — LES SIX "
    "RÉSIDUS : le linter v2 étendu aux trois classes nouvelles (le ratio "
    "recalculé depuis ses opérandes à la précision affichée, la plage contre la "
    "table locale, la cohérence cible-périmètre) et TROIS RÉSIDUS TRANCHÉS PAR LA "
    "MACHINE : le ratio publié 3,23 ne se recompute pas (63,39/19,66 = 3,22), la "
    "plage D1–D251 porte 43 trous, la cible ≥ 15/18 re-scopée au TEST corrigé ; "
    "(3) ru2rfjl2g — le témoin d'époque et son vérificateur OFFLINE fail-closed "
    "(6/6 contrôles), la garde RAM native (5/5, le contrôle négatif sans verrou), "
    "les deux écarts nommés (RtlSecureZeroMemory intrinsèque non exporté, le "
    "drapeau dumpable POSIX) ; (4) io3uh37cj — LES COULOIRS SCELLÉS : la chaîne "
    "reproduite à l'octet (l'aller-retour keystone → capstone → keystone "
    "IDENTIQUE, la différentielle contre la chaîne scellée ZÉRO ÉCART — le sha256 "
    "ddedc26c… reconstruit à la source, 10/10 rebuilds), le kit métal nu à "
    "l'agrégateur qui REFUSE, le dispatch CPUID 32/32, LE SURCOÛT TOKEN DE "
    "GOUVERNANCE MESURÉ (34 663 tokens par changement contre les budgets "
    "627/674/2 200 — 732 une fois compressée) ; (5) 0pljbn96b — LE KIT DE "
    "CLÔTURE TAMARIN/PROVERIF : les commandes exactes aux budgets nommés, le "
    "négatif d'abord, l'autotest 6/6 (--executer REFUSÉ au bac) ; (6) 0j7ywza2h "
    "— L'INSTRUMENT CONTRAINT rendu exécutable (GBNF + validateur, 8/8) et "
    "L'ÉCART DE RÈGLE NOMMÉ : 21 des 24 complétions VERT du corpus violent la "
    "grammaire canonique que le contrat énonce (17 définissent « LBL-xxx : » "
    "interdit) — un décodeur contraint CHANGERAIT l'ensemble d'acceptation ; les "
    "48 PAIRES DPO au verdict du juge et les recettes SFT/DPO/RLVR au budget "
    "consigné.\n\n"
    "LE CORPUS : la version v2.1 est DÉPOSÉE au concept 10.5281/zenodo.24457524 "
    "(DOI de version 10.5281/zenodo.24479882) — les splits étanches par contrat, "
    "les 48 paires DPO, les recettes ; le record v2 demeure immuable.\n\n"
    "LE DÉFAUT DE REPRODUCTIBILITÉ NOMMÉ (à corriger à la prochaine génération) : "
    "(a) le linter d'édition v233 dépend de campagne-v5.log, GITIGNORÉ — la porte "
    "n'est pas re-jouable depuis le dépôt public ; la reconstruction depuis les "
    "JSONL committés reproduit EXACTEMENT ses constantes (60 appels, 18 tâches, "
    "5 VERT, médiane 4 604), le log est REDONDANT ; (b) le verdict du linter "
    "dépend de la version de pdftotext : re-joué avec pdftotext 26.09.0 sur les "
    "pièces BYTE-BYTE identiques, il rend 222 VERT et 1 ROUGE (3 tokens "
    "numériques de plus à l'extraction du manuscrit, 1991 contrôlés) — la dérive "
    "est de l'EXTRACTEUR, jamais des pièces ; le linter devrait épingler "
    "l'extracteur ou porter l'extraction.\n\n"
    "LES GESTES AU POSTE RÉEL demeurent nommés : la campagne v6 à l'instrument de "
    "serving, la mesure des cycles au métal nu (≥ 2 machines), la RÉGÉNÉRATION "
    "des cinq pièces (tectonic + weasyprint — le linter v233 des résidus est prêt "
    "à la contrôler), les runs Tamarin/ProVerif (le poste Linux à 16 Go), la "
    "sentinelle SACL/4663 et le FIDO2, la cérémonie d'ère (la clé du maître).\n"
)

with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    # (1) les entrées du complet v0.23.3 RECONDUITES octet pour octet
    v233 = DEPOT / "TRIADE_complet_v0.23.3.zip"
    with zipfile.ZipFile(v233) as zsrc:
        for info in zsrc.infolist():
            if info.filename == "README.txt":
                continue
            z.writestr(info, zsrc.read(info.filename))
    # (2) le nouveau README
    z.writestr("README.txt", README)
    # (3) les ateliers de la vague 15 continuée et de la vague 16
    for d in ATELIERS_V16:
        racine = REPO / d
        if not racine.is_dir():
            print(f"    (absent : {d})")
            continue
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "moteur_oracles/" not in str(src) \
                    and "garde-prompts" not in str(src):
                z.write(src, f"ateliers-vague16/{d}/{src.relative_to(racine).as_posix()}")
    # (4) les plans gelés, la table, les rapports, le worklog, REPRISE
    for nom in ("PLAN-0J7YWZA2H.md", "PLAN-0PLJBN96B.md", "PLAN-86D3USHRR.md",
                "PLAN-AM9D6O2TH.md", "PLAN-IO3UH37CJ.md", "PLAN-RU2RFJL2G.md",
                "PLAN-81ERUQTL6.md", "PLAN-AVMWTF5W.md",
                "EMPREINTES-PLANS-VAGUE16.txt"):
        z.write(REPO / nom, f"vague16/{nom}")
    for nom in RAPPORTS_V16:
        p = REPO / nom
        if p.is_file():
            z.write(p, f"vague16/rapports/{nom}")
    z.write(REPO / "worklog.md", "vague16/worklog.md")
    z.write(REPO / "REPRISE_PROJET.md", "vague16/REPRISE_PROJET.md")
    # (5) les scripts de la vague 16
    for src in sorted(V16.glob("*.py")):
        z.write(src, f"scripts/vague16/{src.name}")

with zipfile.ZipFile(CMP) as z:
    mauvais = z.testzip()
    if mauvais is not None:
        raise SystemExit(f"ZIP CORROMPU : {mauvais}")
    n = len(z.namelist())

print(f"[archive] {CMP.name} : {CMP.stat().st_size} o, {n} entrées, "
      f"sha256 {sha256(CMP)}")
for nom in ("TRIADE_soumission_v0.23.3.zip", "TRIADE_presentation_v0.23.3.zip"):
    p = OUT / nom
    print(f"[archive] {nom} : {p.stat().st_size} o, sha256 {sha256(p)}")
