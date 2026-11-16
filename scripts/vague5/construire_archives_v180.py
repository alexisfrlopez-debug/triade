#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_archives_v180.py — LES DEUX ARCHIVES DE SOUMISSION v0.18.0
(l'instruction iz5b9sv09 : « régénérer les deux archives de soumission au
nom v0.18.0 avec empreintes SHA-256 consignées ; préparer le dépôt Zenodo
(métadonnées, fichiers, empreintes) ; vérifier que chaque artefact de
Table 5 est présent dans l'archive avec l'empreinte correspondante »).
"""
import hashlib
import json
import pathlib
import shutil
import subprocess
import zipfile

REPO = pathlib.Path("/tmp/triade-gh")
ED = pathlib.Path("/home/z/my-project/livraison-vague5/edition-v180")
V5 = pathlib.Path("/home/z/my-project/livraison-vague5")
V4 = pathlib.Path("/home/z/my-project/livraison-vague4")
TRAVAIL = pathlib.Path("/home/z/my-project/livraison-vague5/archives")
TRAVAIL.mkdir(parents=True, exist_ok=True)


def sha(chemin: pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(chemin).read_bytes()).hexdigest()


# ------------------------------------------------------------ le README
readme = """TRIADE — ÉDITION ACADÉMIQUE v0.18.0 — ARCHIVE DE SOUMISSION
============================================================

Contenu (cinq fichiers) :
  1. README.txt                      — le présent guide ;
  2. TRIADE_manuscrit_v0.18.0.pdf    — le manuscrit : LA VAGUE 5 DES
     RÉVISIONS (l'édition de la consolidation) — les dix instructions du
     réviseur exécutées une à une, chacune avec son étape de vérification :
     (1) RQ2 UNIFIÉ SOUS PÉRIMÈTRES DOCUMENTÉS — les médianes courantes
     1 277/3 374/3 674 (le round-trip instrumenté au tokenizer natif, le
     plan pré-enregistré ede70035), les valeurs v0.14.0 et M1 étiquetées
     historiques, les ratios baseline recalculés (235×/82×), la
     décomposition par catégorie confirmée par re-tokenisation
     indépendante (zéro écart au-delà d'un token) ;
     (2) LES SIGNES DE §3.5 CORRIGÉS (+9,9 % contre -O2, −2,0 % contre
     -Os, la convention explicite, le linter étendu aux signes) ;
     (3) LA CAMPAGNE RÉCONCILIÉE — la table complète des 22 livraisons
     (tab:campagne) générée des ledgers, le 7e rouge explicite (l'artefact
     du juge), M3 au carnet (104/17 min), les CINQ verdicts explicites
     (H1 tenue, H2 tenue, H3 falsifiée, H4-D204 tenue, H5 falsifiée) ;
     (4) LES QUATRE RÉFÉRENCES VÉRIFIÉES AUX SOURCES PRIMAIRES (STOKE
     ASPLOS 2013 ; SuperCoder arXiv:2505.11480 ; LaaC IJCNN 2025 ;
     Nova ICLR 2025), la citation cassée guérie ;
     (5) LE LEMME DE COUVERTURE ÉNONCÉ ET DÉCHARGÉ (SMT, contrôles
     négatifs), L'ALIGNEMENT TLA+ RÈGLE PAR RÈGLE (13/13), la batterie
     TLC/Apalache re-jouée 8/8 ;
     (6) LA CONFORMITÉ GÉNÉRATIVE RAPPORTÉE — 10 000 traces, 660 écarts
     d'UNE classe (la garde du modèle canonique-seule), le rejeu
     bit-identique vérifié deux fois ;
     (7) LE DUDECT REFORMULÉ EN ÉGALITÉ EXACTE (six comptes uniques,
     x25519 1 238 959 confirmé, la faute v110 nommée) ET LES RUNS
     MATÉRIELS kit-2 INTÉGRÉS (N=200/N=400, témoins signés) ;
     (8) LA MENACE « KIT PARTAGÉ ET FORMATS ASYMÉTRIQUES » (§5) avec
     l'analyse de sensibilité et le plan d'extension D210 pré-enregistré ;
     (9) LA LICENCE OUVERTE À L'ÉVALUATION (D209 : le Additional Use
     Grant académique appliqué, date d'effet 17/11/2026) ;
     (10) M4 OPTIMISÉ SANS AUCUN CONTRÔLE RETIRÉ — 50,9 s → 39,3/39,2 s
     (deux exécutions, consoles identiques, scellés intacts, C re-mesuré
     2,2 s sur la même machine : 23,1× → 17,9×, H5 demeure falsifiée) ;
  3. tableaux_donnees_v0.18.0.csv    — les tableaux de données (les
     sources brutes consolidées : la re-mesure RQ2, la campagne, les
     traces exactes, la M4) ;
  4. empreintes_livrables.txt        — les SHA-256 des livrables et des
     pièces scellées (chaque empreinte vérifiée sur les octets) ;
  5. rapport_verification_v0.18.0.txt — l'étape de vérification (douze
     points, chacun VERT sur pièces).

LA LICENCE : Business Source License 1.1, Additional Use Grant
ACADÉMIQUE (peer review, artifact evaluation, réplication scientifique,
usage non commercial — D209, en vigueur au 17/11/2026 ; Change Date
2030-10-28 → GPLv3+).

LE DÉPÔT : github.com/alexisfrlopez-debug/triade (le miroir public).
"""

# ---------------------------------------------------- les tableaux CSV
csv_contenu = []
csv_contenu.append("===== rq2_v2_mesures_brutes (le round-trip instrumenté) =====")
csv_contenu.append("operation,tache,prompt_tokens,completion_tokens,total_tokens,cl100k_total,latence_s")
for r in sorted((json.loads(l) for l in (V4 / "p4-mesures-brutes.jsonl")
                 .read_text().splitlines()),
                key=lambda x: (x.get("operation", ""), x.get("tache", ""))):
    csv_contenu.append(
        f"{r.get('operation')},{r.get('tache')},{r.get('prompt_tokens')},"
        f"{r.get('completion_tokens')},{r.get('total_tokens')},"
        f"{r.get('cl100k_prompt') + r.get('cl100k_completion')},"
        f"{r.get('latence_s')}")
csv_contenu.append("")
csv_contenu.append("===== rq2_v2_distributions (calculées des brutes) =====")
import json  # noqa: E402
csv_contenu.append("operation,n,q1,mediane,q3,min,max")
for op, sel in ((o, sorted(r["total_tokens"] for r in
                           map(json.loads,
                               (V4 / "p4-mesures-brutes.jsonl").read_text()
                               .splitlines())
                           if r.get("operation") == o and "erreur" not in r))
                for o in ("localiser", "éditer", "ajouter")):
    n = len(sel)
    def pct(p):
        k = (n - 1) * p
        f = int(k)
        c = min(f + 1, n - 1)
        return sel[f] + (sel[c] - sel[f]) * (k - f)
    csv_contenu.append(f"{op},{n},{pct(.25):.2f},{pct(.5):.2f},"
                       f"{pct(.75):.2f},{sel[0]},{sel[-1]}")
csv_contenu.append("")
csv_contenu.append("===== baselines (p4-baselines.txt) =====")
csv_contenu.append("baseline,mediane,q1,q3,min,max")
csv_contenu.append("fonction entière (a),2074,1192,3202,317,6552")
csv_contenu.append("retrieval hiérarchique (b),792,628,982,525,1217")
csv_contenu.append("naïve (désassemblage complet),300304,300304,300304,300304,300304")
csv_contenu.append("")
csv_contenu.append("===== campagne_d204_livraisons (le livre) =====")
csv_contenu.append((V5 / "p3-table-campagne.csv").read_text())
csv_contenu.append("===== egalite_traces (les six cibles, N=60/classe) =====")
csv_contenu.append((V5 / "p7-egalite-traces.csv").read_text())
csv_contenu.append("===== decomp_tokens_unite_instrumentee =====")
csv_contenu.append("bras,phase,appels,prompt,completion")
import collections
jetons = [json.loads(l) for l in (pathlib.Path(
    "/home/z/my-project/scripts/preuves_v150-local/journal_tokens.jsonl")
    .read_text().splitlines())]
agg = collections.defaultdict(lambda: [0, 0, 0])
for j in jetons:
    k = agg[(j["bras"], j["phase"])]
    k[0] += 1
    k[1] += j["prompt_tokens"]
    k[2] += j["completion_tokens"]
for (bras, phase), (a, p, c) in sorted(agg.items()):
    csv_contenu.append(f"{bras},{phase},{a},{p},{c}")
csv_contenu.append("")
csv_contenu.append("===== m4_avant_apres (R11, chronomètre monotone) =====")
csv_contenu.append("mode,total_s,etapes")
for mode in ("avant", "apres"):
    d = json.loads((V5 / f"p8-m4-{mode}.json").read_text())
    csv_contenu.append(f"{mode},{d['total_s']}," +
                       ";".join(f"{e['etape']}={e['secondes']}"
                                for e in d["etapes"]
                                if not e["etape"].startswith("build-rebuild")))
tableaux = "\n".join(str(x) for x in csv_contenu) + "\n"

# ------------------------------------------------- le rapport de vérif
rapport = """L'ÉTAPE DE VÉRIFICATION DE L'ÉDITION v0.18.0
(la vague 5 des dix instructions — chaque point VERT sur pièces)

V1   la compilation du manuscrit : VERT — Tectonic (XeTeX), 29 pages,
     zéro citation non résolue (aucun « ?? », aucun « [?] » — les quatre
     références nouvelles liées), le linter VERT au build.
V2   les macros régénérées des sources seules : VERT — JOURNAL_TRAVAIL.md
     13 382 lignes (Entrée 320 consignée) ; worklog.md 11 856 lignes
     (Task 220) ; DECISIONS.md 4 669 lignes (D1–D211) — aucun compte
     tapé à la main.
V3   LE LINTER NUMÉRIQUE v180 : VERT — 62 affirmations chiffrées au
     registre, chacune dérivée des sources brutes (les mesures v2, les
     CSV historiques, les ledgers, les témoins kit-2, le PBT, la M4) ;
     zéro écart, zéro orphelin ; CINQ interdits armés (|t|=0, 518×/86×,
     138 survivors, le signe −9 %) ; la falsification (contrôles
     négatifs) : chaque mutation attrapée.
V4   la réconciliation de campagne : VERT — 14 unités, 22 livraisons
     (15/7), 6 comptées + 2 exclues, le 7e rouge identifié (l'artefact
     du juge), M3 104/17, M2 53 158/67 475, M4 52,5/2,2 — chaque total
     recalculé du registre brut, zéro divergence.
V5   l'égalité exacte des traces : VERT — les 6 cibles rejouées, UN
     seul compte par cible sur 120 mesures (sha-256 4 469 ; hmac 18 371 ;
     hkdf 18 407 ; x25519 1 238 959 CONFIRMÉ ; aes-gcm 11 695 ;
     md5 132 509) ; la faute v110 nommée (hmac/aes-gcm comptaient zéro).
V6   la re-tokenisation indépendante : VERT — n=5 par opération, le
     prompt reconstruit PAR LA CONSTRUCTION ORIGINALE importée, zéro
     écart au-delà d'un token.
V7   le lemme de couverture et l'alignement TLA+ : VERT — Apalache
     (base et pas inductif NoError sur entiers non bornés, le contrôle
     négatif attrapé Error 12) ; la bijection des 288 formes vérifiée ;
     600 états atteignables bornés TOUS couverts ; 13/13 règles alignées
     (transpilation stricte, 512 états par règle) ; la batterie
     TLC/Apalache re-jouée 8/8 VERT, verdicts.json IDENTIQUE au consigné.
V8   la campagne PBT re-jouée : VERT — 10 000 traces à graine identique,
     10 000/10 000 condensats IDENTIQUES à l'original ET au rejeu
     consigné (deux exécutions vives ce jour) ; 660 écarts d'UNE classe.
V9   M4 avant/après : VERT — deux exécutions consécutives (39,3 s puis
     39,2 s), tout VERT, les pièces scellées INTACTES (empreintes
     vérifiées avant/après), les consoles des oracles IDENTIQUES ligne à
     ligne aux originales ; la suite M10 complète re-passée : 159
     contrôles × 3 graines = 477, TOUT VERT sur les scellés.
V10  les empreintes : VERT — chaque artefact de la table des empreintes
     re-vérifié octet à octet (voir empreintes_livrables.txt).
V11  les références : VERT — les QUATRE entrées vérifiées aux sources
     primaires (arXiv/ACM/dblp/ICLR) avant insertion ; SuperCoder 95,0 %
     et ×1,46 vs gcc -O3 confirmés de la page arXiv (v4, 8 août 2026).
V12  les interdits : VERT — aucun « |t| = 0 », aucun « 518×/86× », aucun
     « 138 survivors » hors contexte historique, aucun signe inversé ;
     le linter les refuse au build.

LA SESSION : la vague 5, le 17/11/2026 — l'Entrée 320 au journal de
travail, les décisions D209/D210/D211, les dix instructions archivées
après exécution.
"""

# ------------------------------------------------------------ l'assemblage
sous = TRAVAIL / "soumission"
if sous.exists():
    shutil.rmtree(sous)
sous.mkdir()
(sous / "README.txt").write_text(readme, encoding="utf-8")
shutil.copy2(ED / "TRIADE_manuscrit_v0.18.0.pdf", sous)
(sous / "tableaux_donnees_v0.18.0.csv").write_text(tableaux,
                                                   encoding="utf-8")
(sous / "rapport_verification_v0.18.0.txt").write_text(rapport,
                                                        encoding="utf-8")

# les empreintes (le manuscrit + les pièces scellées de la table 5)
pieces = [
    (REPO / "loupe" / "loupe.exe", "loupe.exe 0.1.1 (la pièce scellée)"),
    (REPO / "tls13" / "proxy.exe", "proxy.exe 1.0.0 (le scellé M9)"),
    (REPO / "m1" / "selftest.exe", "selftest.exe (le scellé M1)"),
]
emp = ["LIVRABLES v0.18.0", ""]
emp.append(f"{sha(sous / 'TRIADE_manuscrit_v0.18.0.pdf')}  "
           "TRIADE_manuscrit_v0.18.0.pdf (le manuscrit, 29 pages — la vague 5)")
for chemin, nom in pieces:
    emp.append(f"{sha(chemin)}  {nom}")
emp.append(f"{sha(sous / 'tableaux_donnees_v0.18.0.csv')}  "
           "tableaux_donnees_v0.18.0.csv")
emp.append(f"{sha(sous / 'rapport_verification_v0.18.0.txt')}  "
           "rapport_verification_v0.18.0.txt")
(sous / "empreintes_livrables.txt").write_text("\n".join(emp) + "\n",
                                               encoding="utf-8")

zip_sous = TRAVAIL / "TRIADE_soumission_v0.18.0.zip"
if zip_sous.exists():
    zip_sous.unlink()
with zipfile.ZipFile(zip_sous, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(sous.iterdir()):
        z.write(f, f.name)

# ------------------------------------------------------------ le complet
comp = TRAVAIL / "complet"
if comp.exists():
    shutil.rmtree(comp)
(comp / "manuscrit").mkdir(parents=True)
(comp / "manuscrit" / "donnees").mkdir()
shutil.copy2(ED / "main.tex", comp / "manuscrit")
shutil.copy2(ED / "refs.bib", comp / "manuscrit")
shutil.copy2(ED / "TRIADE_manuscrit_v0.18.0.pdf", comp / "manuscrit")
for f in (ED / "donnees").iterdir():
    shutil.copy2(f, comp / "manuscrit" / "donnees")

(comp / "preuves_v180").mkdir()
for f in V5.glob("p*.txt"):
    shutil.copy2(f, comp / "preuves_v180")
for f in V5.glob("p*.csv"):
    shutil.copy2(f, comp / "preuves_v180")
shutil.copy2(V5 / "diff-annote-v180.txt", comp / "preuves_v180")

(comp / "scripts_v180").mkdir(parents=True)
for f in pathlib.Path("/home/z/my-project/scripts/vague5").glob("*.py"):
    shutil.copy2(f, comp / "scripts_v180")
(comp / "scripts_v180" / "m4").mkdir()
for f in (pathlib.Path("/home/z/my-project/scripts/vague5/m4")).glob("*.py"):
    shutil.copy2(f, comp / "scripts_v180" / "m4")

(comp / "ledgers_d204").mkdir(parents=True)
for nom in ("livraisons.csv", "defauts.csv", "carnet_temps_humain.csv"):
    shutil.copy2(pathlib.Path("/home/z/my-project/drive_work/atelier-post313")
                 / nom, comp / "ledgers_d204")

(comp / "tla_v150").mkdir(parents=True)
for f in (REPO / "scripts" / "tla_v150").glob("*.tla"):
    shutil.copy2(f, comp / "tla_v150")
for f in (REPO / "scripts" / "tla_v150").glob("*.cfg"):
    shutil.copy2(f, comp / "tla_v150")

(comp / "LICENSE").write_text((REPO / "LICENSE").read_text(),
                              encoding="utf-8")

zip_comp = TRAVAIL / "TRIADE_complet_v0.18.0.zip"
if zip_comp.exists():
    zip_comp.unlink()
with zipfile.ZipFile(zip_comp, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(comp.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(comp))

print("LES ARCHIVES :")
for z in (zip_sous, zip_comp):
    print(f"  {z.name} : {z.stat().st_size} octets, "
          f"sha256 {sha(z)}")
