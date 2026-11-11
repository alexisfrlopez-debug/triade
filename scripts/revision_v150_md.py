#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v150_md.py — le md PROTOCOLE_TRIADE.md porté en v0.15.0 (les
ancres refusent si elles manquent) : les preuves non bornées, le
raffinement, les kits, la réplication, les statuts systématiques, la
gouvernance D197 + l'empreinte du PDF formel au registre D134."""
import hashlib
import pathlib
import subprocess

REPO = pathlib.Path("/home/z/my-project/triade")
MD = REPO / "docs" / "PROTOCOLE_TRIADE.md"
s = MD.read_text(encoding="utf-8")
FAITS = []


def remplace(ancien, nouveau, nom):
    global s
    if ancien not in s:
        raise SystemExit(f"[md v0.15.0] ANCRE INTROUVABLE — {nom}")
    s = s.replace(ancien, nouveau, 1)
    FAITS.append(nom)


# 1. le titre et le préambule
remplace("# PROTOCOLE TRIADE v0.14.0 — Spécification technique",
         "# PROTOCOLE TRIADE v0.15.0 — Spécification technique",
         "le titre")
remplace("> Source de travail faisant autorité pour la v0.14.0. Les archives formelles des versions",
         "> Source de travail faisant autorité pour la v0.15.0. Les archives formelles des versions",
         "le préambule")
remplace("> précédentes demeurent : `docs/Protocole_TRIADE_v0.13.0_Specification.pdf` (v0.13.0 —",
         "> précédentes demeurent : `docs/Protocole_TRIADE_v0.14.0_Specification.pdf` (v0.14.0 —\n"
         "> le programme empirique), `docs/Protocole_TRIADE_v0.13.0_Specification.pdf` (v0.13.0 —",
         "la liste des archives")

# 2. la ligne de version (§ 1, la version courante)
remplace("- Version : v0.14.0 — la révision du PROGRAMME EMPIRIQUE (D193/D194/D195 : le bras de référence pré-enregistré [zéro divergence, sha-256 paritaire, H4 tenue], la re-mesure RQ2 en distributions avec la baseline naive, l'indépendance par instance isolée, le re-jeu des 832 mutants aux composition-killers [93,3 %]).",
         "- Version : v0.15.0 — la révision des PREUVES NON BORNÉES ET DU RAFFINEMENT (D197/D198 : le croisement d'attribution des instructions recoupé et corrigé, la règle du contenu cité, la règle d'archivage des versions ; l'invariant inductif [P1-P4 PROUVÉES NON BORNÉES, la fidélité D187 reproduite 154/1 152, les bornes étendues zéro hors I], le raffinement modèle↔implémentation [34 pas, zéro écart, les chemins d'échec inclus], les trois kits de mesure matérielle EN ATTENTE, la réplication outillée [grille finalisée, κ autotesté], les statuts systématiques). Sous la v0.14.0, la révision du programme empirique (D193/D194/D195 : le bras de référence pré-enregistré [zéro divergence, sha-256 paritaire, H4 tenue], la re-mesure RQ2 en distributions avec la baseline naive, l'indépendance par instance isolée, le re-jeu des 832 mutants aux composition-killers [93,3 %]).",
         "la ligne de version")

# 3. le § 1.16 (avant la couche I)
SEC116 = """### 1.16 Ce que change la v0.15.0

LES PREUVES NON BORNÉES ET LE RAFFINEMENT (le sixième fichier
d'instructions, ic09ydeli sous son vrai nom — le croisement
d'attribution d'hier RECROUPÉ et CORRIGÉ, D197). AUCUNE règle du cœur
modifiée, AUCUNE couche d'exécution ajoutée, AUCUN artefact scellé
touché.

**La déviation constatée** : Tamarin ET ProVerif demeurent ABSENTS du
laboratoire (constat re-vérifié au geste) — la route consignée à D196
est suivie : la preuve par INVARIANT INDUCTIF dans l'explorateur.

**L'invariant inductif** (`scripts/preuves_v150/modele_invariant_v150.py`) :
le plafond d'époque de l'explorateur v0.12.0 (un artefact d'exploration,
jamais du design — l'implémentation fait e ← e+1 sans borne) est RETIRÉ ;
l'invariant I (I1 secret ⟹ seuil = 3 ; I2 aucune destruction injuste ;
I3 média du piège et fragments CF2 intacts ; I4 époque ≥ 1) est
initialisé, PRÉSERVÉ par chacune des 13 règles sur l'ensemble FINI des
formes d'état (288 formes, les deux classes d'époque {1} et {≥ 2}),
l'uniformité témoignée par translations δ ∈ {7, 50, 1000} aux verdicts
IDENTIQUES ; la monotonie vérifiée INCONDITIONNELLEMENT (4 096 formes,
zéro décroissance) ; le rejeu retourne l'état inchangé. **P1-P4 SONT
PROUVÉES NON BORNÉES** (toute époque, toute profondeur, sous A1-A4 ;
A5 hors modèle nommé). La FIDÉLITÉ : D187 reproduit EXACTEMENT (154
états / 1 152 transitions) ; les bornes étendues (époques ≤ 5 prof 8 :
228/1 902 ; époques ≤ 7 prof 12 : 372/3 342) trouvent ZÉRO état hors
de I — la preuve bornée CONFIRME la preuve non bornée.

**Le raffinement** (`scripts/preuves_v150/raffinement_v150.py`) :
chaque règle abstraite REJOUÉE contre l'implémentation Python (coffre
de TEST à phrase publique marquée, D192) : le cycle honnête sur CINQ
époques VÉCUES aux deux niveaux, la phrase erronée aux deux actes
(quinze essais, zéro destruction), la falsification du conteneur (une
destruction LOCALE, un PV, le média intact), la falsification du piège
(refus nommé, rien détruit), le rejeu d'époque passée en TROIS
variantes, le piège absent (IMPOSSIBLE, pas refusé), le piège d'un
autre coffre, l'adversaire sous le seuil (32 moitiés forgées, zéro
passage) : **34 pas, ZÉRO ÉCART** — les chemins d'échec inclus ; trois
gestes hors modèle consignés comme tels.

**Les trois kits de mesure matérielle** (`scripts/kits_mesure_v150/`) :
le dudect temps réel (quatre cibles extraites de la pièce scellée,
l'appel natif VALIDÉ au vecteur FIPS « abc », le mesureur C double
backend dont l'autotest POSIX n'éprouve que le mécanisme), le fence.i
sur silicium (le scénario M7, la cible changée), le terrain tiers Loupe
(T0→T7+S0 intégral) — TOUS **EN ATTENTE DE RUN MATÉRIEL** : aucun
chiffre n'existe, aucun n'est fabriqué.

**La réplication** (`scripts/replication_v150/`) : la grille T/X
FINALISÉE (définitions opérationnelles, exemples vécus), le
calculateur κ de Cohen AUTOTESTÉ (trois cas synthétiques au κ
calculable à la main), les critères pré-enregistrés D189 INCHANGÉS ;
le second annotateur À RECRUTER, le second domaine EN ATTENTE d'une
vraie commande — les statuts consignés.

**Les statuts systématiques** (la commande, point 4) : chaque
affiliation de preuve porte son statut — *prouvé non borné* / *prouvé
borné* / *en attente de run matériel* — la table générée depuis les
pièces (`scripts/statuts_preuves_v150.py`), AUCUNE revendication
matérielle tant que le run n'est pas recoupé.

**La dette documentaire guérie** : la table des preuves du manuscrit
(29 lignes en v0.13.0/v0.14.0) n'était JAMAIS RENDUE — le flot
dépassait la page et LaTeX le rejetait silencieusement : la table
devient LONGTABLE, les 34 lignes sont rendues.

**La gouvernance** (D197) : le croisement d'attribution des
instructions n°5/n°6 recoupé aux métadonnées Drive et corrigé aux
gestes (ysddxpk0o archivé, ic09ydeli rappelé vers /instructions) ; LA
RÈGLE DU CONTENU CITÉ (à l'ouverture de toute instruction : lecture
intégrale, empreinte confrontée, le contenu cité à l'entrée
d'ouverture) ; LA RÈGLE DU DÉVELOPPEUR (12/11) : à chaque livraison
d'une nouvelle version d'un document, les anciennes versions sont
archivées (racine → /ARCHIVE, déplacement vérifié).

"""
remplace("## 2. La couche I : format normalisé des spécifications",
         SEC116 + "## 2. La couche I : format normalisé des spécifications",
         "le § 1.16")

# 4. le § 19.17 (après le § 19.16)
SEC1917 = """### 19.17 Correspondance v0.14.0 → v0.15.0

| Évolution | En v0.14.0 | En v0.15.0 | Statut |
|---|---|---|---|
| Le modèle formel | prouvé BORNÉ (époques ≤ 3, le plafond de l'explorateur) | PROUVÉ NON BORNÉ (l'invariant inductif I, la préservation par les 13 règles, la translation δ) | livré (D198) |
| La fidélité du portage | — | D187 reproduit EXACTEMENT (154/1 152), bornes étendues zéro hors I | livré (D198) |
| Le raffinement | — | 34 pas rejoués contre l'implémentation, ZÉRO ÉCART, les chemins d'échec inclus | livré (D198) |
| Les statuts de preuve | « prouvé dans le modèle » (borné, la nuance dans le texte) | SYSTÉMATIQUES : prouvé non borné / prouvé borné / en attente de run matériel | livré (D198) |
| La table des preuves du manuscrit | générée mais JAMAIS RENDUE (le flot rejeté silencieusement) | LONGTABLE : les 34 lignes rendues | guéri (D198) |
| Les kits matériels | le kit terrain du bras C (en attente) | TROIS kits (dudect temps réel [l'appel natif validé FIPS], fence.i sur silicium, terrain tiers) — EN ATTENTE | préparés (D198) |
| La réplication | la grille T/X proposée (D189) | la grille FINALISÉE (définitions opérationnelles, exemples vécus), le κ AUTOTESTÉ, les critères INCHANGÉS, les statuts consignés | outillé (D198) |
| La gouvernance | — | le croisement d'attribution RECOUPÉ et CORRIGÉ (D197), la règle du contenu cité, la règle d'archivage des versions | consigné (D197) |

Modifications explicitement rejetées (v0.15.0) : relâcher la moindre
hypothèse A1-A5 au bénéfice de la preuve non bornée — rejeté (la
généralisation porte sur l'ÉPOQUE, jamais sur le modèle symbolique) ;
consigner un résultat matériel d'après l'autotest POSIX du kit dudect —
rejeté (l'autotest éprouve le MÉCANISME, le run appartient au
développeur) ; réécrire les entrées d'hier au sujet du croisement —
rejeté (append-only : la correction vit dans l'Entrée 230 et D197).

"""
remplace("## 20. Glossaire", SEC1917 + "## 20. Glossaire", "le § 19.17")

# 5. le journal des versions (l'entrée v0.15.0 en tête)
remplace("| v0.14.0 | 11 nov. 2026 | Révision du PROGRAMME EMPIRIQUE",
         "| v0.15.0 | 12 nov. 2026 | Révision des PREUVES NON BORNÉES ET DU RAFFINEMENT (D197/D198) : le croisement d'attribution des instructions n°5/n°6 recoupé aux métadonnées Drive et corrigé aux gestes (la règle du contenu cité, la règle d'archivage des versions) ; l'invariant inductif (P1-P4 PROUVÉES NON BORNÉES : le plafond d'époque retiré, la préservation par les 13 règles sur 288 formes, la translation δ∈{7,50,1000}, la monotonie inconditionnelle, la fidélité D187 reproduite 154/1 152, les bornes étendues zéro hors I) ; le raffinement modèle↔implémentation (34 pas, zéro écart, les chemins d'échec inclus, cinq époques vécues aux deux niveaux) ; les trois kits de mesure matérielle EN ATTENTE (dudect temps réel à l'appel natif validé FIPS, fence.i sur silicium, terrain tiers Loupe) ; la réplication outillée (grille T/X finalisée, κ autotesté, critères inchangés, statuts consignés) ; les statuts de preuve systématiques ; la dette de la table des preuves du manuscrit guérie (longtable). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n| v0.14.0 | 11 nov. 2026 | Révision du PROGRAMME EMPIRIQUE",
         "le journal des versions")

MD.write_text(s, encoding="utf-8")

# 6. le PDF formel v0.15.0 au dépôt + l'empreinte au registre D134
pdf_src = REPO / "scripts" / "spec_v150" / "final.pdf"
pdf_dst = REPO / "docs" / "Protocole_TRIADE_v0.15.0_Specification.pdf"
pdf_dst.write_bytes(pdf_src.read_bytes())
emp = hashlib.sha256(pdf_dst.read_bytes()).hexdigest()
print(f"[pdf] {pdf_dst.name} : {len(pdf_dst.read_bytes())} octets, "
      f"sha256 {emp[:16]}…")
r = subprocess.run(["python3", "scripts/empreintes_build.py", "consigner",
                    "--artefact",
                    "docs/Protocole_TRIADE_v0.15.0_Specification.pdf",
                    "--build",
                    "chaîne spec_v150 (les preuves non bornées et le "
                    "raffinement v0.15.0 — D197/D198)"],
                   cwd=REPO, capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[:300])
print(f"[md v0.15.0] {len(FAITS)} remplacements ancrés")
for f in FAITS:
    print(f"  - {f}")
