#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_zips_v0233.py — LES DEUX ARCHIVES DE DÉPÔT de l'édition
v0.23.3 : LA SOUMISSION (README, le manuscrit, le manifeste des
empreintes, le rapport de vérification, la note des tables générées) et
LE COMPLET (les sources des cinq pièces, les ateliers des vagues 12-15,
les chaînes de génération et LES TROIS LINTERS v230/v232/v233 + le
linter v2 de l'atelier, le pack des cinq documents). Le linter v233
EXIGÉ vert avant l'assemblage (le refus ferme) ; chaque archive testée
au dézippage."""
import hashlib
import pathlib
import subprocess
import sys
import zipfile

REPO = pathlib.Path("/home/z/my-project/depot")
V15 = REPO / "scripts" / "vague15"
OUT = REPO / "depot-zenodo-v0233"
OUT.mkdir(exist_ok=True)


def ajouter(z, chemin, arcname=None):
    z.write(chemin, arcname or chemin.name)


# (0) LE LINTER EXIGÉ VERT AVANT L'ASSEMBLAGE (le refus ferme)
print("[0] le linter v233 exigé vert avant l'assemblage…")
r = subprocess.run([sys.executable, str(V15 / "linter_v233.py")],
                   capture_output=True, text=True)
if r.returncode != 0:
    print(r.stdout[-2000:])
    raise SystemExit("LE LINTER v233 ROUGE — les archives REFUSÉES")
print("    le linter : VERT")

# ---- LA SOUMISSION -------------------------------------------------------
SUB = OUT / "TRIADE_soumission_v0.23.3.zip"
if SUB.exists():
    SUB.unlink()
with zipfile.ZipFile(SUB, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — la soumission de l'édition v0.23.3 (la vague 15, "
               "la RELEASE — la commande du maître « ok pour la suite "
               "(release de la vague etc…) » : les CINQ PIÈCES "
               "RÉGÉNÉRÉES sous le linter v2 à cinq classes de vxf37231r "
               "(les phrases sémantiques retirées — le compilateur N'EST "
               "JAMAIS LIVRÉ, la notation scellée l'est —, les plages "
               "décisionnelles, les faisabilités n/18 datées avec la "
               "campagne v5 (nov. 2026) à 5/18 la cible manquée "
               "consignée, le claim de version à la v0.23.2 courante, "
               "les gallicismes EN guéris) ; la vague 15 portée au corps : "
               "la composition 0.7271 c/octet@4096 (la cible pré-enregistrée "
               "≤ 2.0 tenue au 36 %, OpenSSL EVP 0.5757 à 1.26×, la "
               "chaîne scellée 68.7× derrière, aucun contrôle retiré), le "
               "TCB réduit 58→34→11 (le corridor des onze à 0xFC00, le "
               "harnais 36/36, le coût du dispatch nommé), le moteur "
               "d'oracles natif (5189× aux opérandes non arrondies), "
               "TPL-ADD-v5 à 5/18 (la cible ≥ 15/18 manquée, la lecture "
               "défavorable consignée — la variance du sujet au CLI "
               "nommée, les juges intacts), H7 servie aux 28 unités (le "
               "sha canonique 2de7d488 re-exécuté bit-identique, le "
               "second annotateur re-autotesté, le confound 1.5B nommé "
               "0/64), CF3-v3 au verdict machine (L3 vérifié à 1 122 "
               "pas, les cinq autres au mur de mémoire 4 Go — la cause "
               "nommée, la voie du poste réel, le port ProVerif livré), "
               "et l'écosystème d'adoption (le corpus aux 109 triples "
               "aux splits étanches, le gym à la récompense typée, la "
               "ladder re-jouable, le guide d'agent, la doc EN au noyau, "
               "le kit aux 156 pièces sans aucune ancre). Le concept DOI "
               "10.5281/zenodo.24367343 résout sur la version courante.\n")
    ajouter(z, REPO / "edition-v0230" / "main.pdf",
            "TRIADE_manuscrit_v0.23.3.pdf")
    ajouter(z, V15 / "empreintes_livrables_v0.23.3.txt")
    ajouter(z, REPO / "rapport_verification_v0.23.3.txt")
    z.writestr("tables_generees.txt",
               "Les tableaux du manuscrit sont GÉNÉRÉS des registres bruts "
               "(edition-v0230/donnees/ — les macros régénérées des "
               "journaux vivants et des JSON bruts) ; le linter v233 "
               "(LES CINQ CLASSES v2 INTÉGRÉES : les phrases sémantiques, "
               "les plages décisionnelles, les faisabilités datées, les "
               "claims de version, les gallicismes — la clause verbatim : "
               "la trace historique exemptée au marqueur, comme la règle "
               "T/X admettait ses marqueurs d'époque) extrait TOUT token "
               "numérique de la prose des cinq pièces, le recalcule des "
               "CSV/JSONL bruts et refuse toute divergence (223 VERT "
               "0 ROUGE, le contrôle négatif vécu : les violations "
               "injectées REFUSÉES aux onze noms, une par classe et par "
               "règle).\n")

# ---- LE COMPLET ----------------------------------------------------------
CMP = OUT / "TRIADE_complet_v0.23.3.zip"
if CMP.exists():
    CMP.unlink()
with zipfile.ZipFile(CMP, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("README.txt",
               "TRIADE — l'archive complète de l'édition v0.23.3 (la vague "
               "15, la release) : les sources des cinq documents (le "
               "manuscrit, la spécification v0.15.8, le Livre v1.7, les "
               "preuves, la présentation), les ateliers des vagues 12-15 "
               "(la vague 15 : les DIX-SEPT ateliers — CF3-vers-le-"
               "verdict, la composition, le feedback, le triage, le TCB, "
               "le moteur d'oracles, TPL-ADD-v5, la validité, le dataset, "
               "le corpus, le gym, l'eval, le guide, la doc EN, le kit, "
               "les matériels, la cohérence/linter v2), les chaînes de "
               "génération (vague13 + vague14 + vague15) et LES QUATRE "
               "LINTERS (le v230 : 71 VERT — le socle ; le v232 : 153 "
               "VERT — les quatre règles ; le v233 : 223 VERT — LES CINQ "
               "CLASSES v2 INTÉGRÉES avec la clause verbatim ; le linter "
               "v2 de l'atelier vxf37231r : le contrôle négatif 5/5) et "
               "LE PACK des cinq documents.\n")
    for src in sorted((REPO / "edition-v0230").rglob("*")):
        if src.is_file() and "main.pdf" not in src.name:
            ajouter(z, src, f"edition-v0230/{src.relative_to(REPO / 'edition-v0230')}")
    for d in ("spec_v158", "livre_v17"):
        for src in sorted((REPO / "scripts" / d).rglob("*")):
            if src.is_file() and src.suffix in (".tex", ".py", ".html",
                                                ".png"):
                ajouter(z, src, f"scripts/{d}/{src.name}")
    ajouter(z, REPO / "scripts" / "vague12" / "linter_v230.py",
            "scripts/vague12/linter_v230.py")
    for src in sorted((REPO / "scripts" / "vague13").glob("*.py")):
        ajouter(z, src, f"scripts/vague13/{src.name}")
    for src in sorted((REPO / "scripts" / "vague14").glob("*.py")):
        ajouter(z, src, f"scripts/vague14/{src.name}")
    for src in sorted(V15.glob("*.py")):
        ajouter(z, src, f"scripts/vague15/{src.name}")
    ajouter(z, REPO / "atelier-coherence-vxf37231r" / "linter_v2.py",
            "atelier-coherence-vxf37231r/linter_v2.py")
    ajouter(z, REPO / "rapport_verification_v0.23.3.txt",
            "rapport_verification_v0.23.3.txt")
    ajouter(z, V15 / "empreintes_livrables_v0.23.3.txt",
            "scripts/vague15/empreintes_livrables_v0.23.3.txt")
    # — LES ATELIERS DES VAGUES 12-14 (le périmètre des éditions "
    #   antérieures, reconduit) —
    for d in ("atelier-recomposabilite-6kbfrpn7k",
              "atelier-purge-0uug27teo",
              "atelier-double-moteur-14n3k8gd7",
              "atelier-conformite-alhmpl35u",
              "atelier-ajouter-v2-pgodgk35l",
              "atelier-marge-vierge-x705m50vl",
              "atelier-ghash-0g3400vql",
              "atelier-requalification-q8kugkpdu",
              "atelier-hcgp3-ay6zuzm8o",
              "atelier-ajouter-v3-5nwnwoceo",
              "atelier-purge-v13-h66o54pjd",
              "atelier-generation-v0230-ylrzmlbn8",
              "atelier-fermeture-f3uznui3l",
              "atelier-ghash-agrege-h1mz2sr8s",
              "atelier-hcgp4-s2p9bm3zd",
              "atelier-ajouter-v4-842vqyy1k",
              "atelier-validite-tcb7tpf9q"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "gardes_smt" not in str(src) \
                    and "clone-test/" not in str(src) \
                    and "rig_garde" not in str(src):
                ajouter(z, src,
                        f"ateliers-v1234/{d}/{src.relative_to(racine)}")
    # — LES DIX-SEPT ATELIERS DE LA VAGUE 15 (le périmètre de la release) —
    for d in ("atelier-cf3-verdict-qa3k5putf",
              "atelier-entrelacement-2sown2h3z",
              "atelier-feedback-witgt6qta",
              "atelier-triage-e1lr9i8ts",
              "atelier-gardes-tcb-k69mvt43j",
              "atelier-oracles-8hguph5ee",
              "atelier-ajouter-v5-yfkpml1j2",
              "atelier-validite-ab2vh5c2m",
              "atelier-dataset-0i4pkzbyr",
              "atelier-corpus-2i7iy3xmg",
              "atelier-gym-3x9cf4e5d",
              "atelier-eval-vpcr7mh3t",
              "atelier-guide-zd316de39",
              "atelier-doc-m8qc10sxg",
              "atelier-kit-v2n6v8rao",
              "atelier-materiel-gzxvze3py",
              "atelier-coherence-vxf37231r"):
        racine = REPO / d
        for src in sorted(racine.rglob("*")):
            if src.is_file() and src.stat().st_size < 3_000_000 \
                    and "native/" not in str(src) \
                    and "moteur_oracles/" not in str(src) \
                    and "garde-prompts" not in str(src):
                ajouter(z, src,
                        f"ateliers-vague15/{d}/{src.relative_to(racine)}")
    # — les plans gelés + les journaux de la vague 15 —
    for src in sorted(REPO.glob("PLAN-*.md")):
        ajouter(z, src, f"vague15/{src.name}")
    ajouter(z, REPO / "EMPREINTES-PLANS-VAGUE15.txt",
            "vague15/EMPREINTES-PLANS-VAGUE15.txt")
    ajouter(z, REPO / "REPRISE_PROJET.md", "vague15/REPRISE_PROJET.md")
    ajouter(z, REPO / "worklog.md", "vague15/worklog.md")
    # — LE PACK des cinq documents —
    for src in sorted((V15 / "pack-v233").rglob("*")):
        if src.is_file():
            ajouter(z, src,
                    f"pack-v233/{src.relative_to(V15 / 'pack-v233')}")

for f in (SUB, CMP):
    with zipfile.ZipFile(f) as z:
        mauvais = z.testzip()
        if mauvais is not None:
            raise SystemExit(f"ZIP CORROMPU : {mauvais} ({f.name})")
    h = hashlib.sha256(f.read_bytes()).hexdigest()
    print(f"[archive] {f.name} : {f.stat().st_size} o, "
          f"{len(zipfile.ZipFile(f).namelist())} entrées, sha256 {h}")
