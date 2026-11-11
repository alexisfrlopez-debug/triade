#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v130_md.py — LE MD PROTOCOLE_TRIADE.md PORTÉ EN v0.13.0 (le
modèle des révisions précédentes : remplacements ANCRÉS, le script REFUSE
si une ancre manque). Les corrections de la commande (f3q3x9i7n) portées au
document de travail : le préambule corrigé (jamais un chiffre faux), le
§ 1.14 NOUVEAU, le § 19.15 NOUVEAU, la ligne du journal des versions."""
import pathlib

MD = pathlib.Path("/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md")
s = MD.read_text(encoding="utf-8")
FAITS = []


def remplace(ancien, nouveau, nom):
    global s
    if ancien not in s:
        raise SystemExit(f"[md v0.13.0] ANCRE INTROUVABLE — {nom}")
    s = s.replace(ancien, nouveau, 1)
    FAITS.append(nom)


# 1. le titre
remplace("# PROTOCOLE TRIADE v0.12.0 — Spécification technique",
         "# PROTOCOLE TRIADE v0.13.0 — Spécification technique",
         "titre v0.13.0")

# 2. la source de travail + l'archive v0.12.0 ajoutée à la liste
remplace(
    "> Source de travail faisant autorité pour la v0.12.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.8.4_Specification.pdf` (v0.8.4 — dernière révision de terrain du TGN),",
    "> Source de travail faisant autorité pour la v0.13.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.12.0_Specification.pdf` (v0.12.0 — le\n"
    "> modèle formel et la gouvernance assainie), `docs/Protocole_TRIADE_v0.11.0_Specification.pdf`\n"
    "> (v0.11.0), `docs/Protocole_TRIADE_v0.10.0_Specification.pdf` (v0.10.0),\n"
    "> `docs/Protocole_TRIADE_v0.9.0_Specification.pdf` (v0.9.0 — consolidation d'après M10),\n"
    "> `docs/Protocole_TRIADE_v0.8.4_Specification.pdf` (v0.8.4 — dernière révision de terrain du TGN),",
    "source + archives")

# 3. le préambule v0.13.0 NOUVEAU (avant le paragraphe v0.12.0)
remplace(
    "> La v0.12.0 consigne LE MODÈLE FORMEL ET LA GOUVERNANCE ASSAINIE",
    """> La v0.13.0 consigne LES CORRECTIONS DE L'ÉDITION (D190/D191/D192, le
> quatrième fichier d'instructions) : la liste exhaustive d'incohérences
> VÉRIFIÉE UNE À UNE (quatorze arbres signés, comptes exacts du journal en
> macros générées, « Fig. 5 » → « Table 5 », la Table 6 des preuves
> RÉGÉNÉRÉE intégralement en anglais par le générateur ANTI-TRONCATURE, la
> note TOTAL/brouillons du tableau des budgets, le paragraphe de
> consolidation aligné sur D181 [douze runs, loupe 0.1.1 scellée], la
> phrase du tableau de menaces, les renvois recalés) ; LES STATISTIQUES
> REFORMULÉES (P(sceller|q) = (1−q)ⁿ — les « α » de D189 étaient des
> rapports de vraisemblance mal étiquetés ; quantiles unilatéraux exacts
> 1,87σ/3,10σ ; l'IC95 % exact de 11/12 [0,615 ; 0,998] avec la réserve
> de non-indépendance ; la règle de comptage opérationnelle des défauts
> échappés) ; LE BENCHMARK AUDITÉ (le facteur « 15,3 » RETIRÉ comme
> ARTEFACT DE PÉRIMÈTRE : l'instrument lisait le compteur de la
> finalisation SEULE après le pipeline, comparé à l'opération complète de
> la référence — 4,16 instructions/ronde était le signe ; les chiffres
> corrigés : 75 983 instructions/op complète contre 69 132 [gcc -O2] et
> 77 505 [-Os], condensé vérifié avant comptage, 17 compressions
> confirmées — la notation est COMPÉTITIVE [−9 %/+2 %], jamais
> spectaculaire) ; LA NEUTRALITÉ DOCUMENTAIRE (l'anti-debug léger
> documenté honnêtement dans les deux documents — la dissuasion, jamais la
> résistance ; la conséquence D81 au modèle de menace : la phrase au dépôt
> + S_serrure en en-tête clair = deux éléments trivialement disponibles,
> la confidentialité effective repose sur le seul média piège ; la
> frontière D105/D81 du clone du laboratoire ; le terrain M7 requalifié :
> qemu-riscv64 TCG au noyau réel, la sémantique matérielle I-cache de
> fence.i NON prouvée sur silicium) ; LE KIT DE LA CÉRÉMONIE D183 PRÉPARÉ
> SANS L'APPLIQUER (`scripts/kit_ceremonie_d183/` : l'outil au partage
> CF2 D120 tel quel, l'autotest VERT sur phrase de test publique, le
> LISEZMOI pas à pas — le geste appartient au développeur) ; L'ÉTAT DE
> L'ART ÉTENDU (huit références vérifiées DOI/arXiv : LLM Compiler,
> CompCert, Kitsune, POLUS, SWE-agent, Jakobi, Peng, Bacic ; la
> revendication « first quantified account » scopée ; RQ3 recadrée en
> GARANTIES SILENCIEUSES DU COMPILATEUR). Aucune règle modifiée, aucune
> couche d'exécution ajoutée, hiérarchie inchangée.

> La v0.12.0 consigne LE MODÈLE FORMEL ET LA GOUVERNANCE ASSAINIE""",
    "préambule v0.13.0")

# 4. le SPRT du préambule v0.12.0 CORRIGÉ (jamais un chiffre faux qui traîne)
remplace(
    "> l'analyse chiffrée ; la cristallisation ÉVALUÉE (le seuil 10 justifié\n"
    "> par le SPRT : α = 1,08 × 10⁻³, 46× plus strict que le canonique — le\n"
    "> seuil demeure, la politique jamais changée en silence) et le protocole",
    "> l'analyse chiffrée ; la cristallisation ÉVALUÉE (le seuil 10 justifié —\n"
    "> l'étiquetage « α » des rapports de vraisemblance de D189 est CORRIGÉ\n"
    "> par D190 : voir les caractéristiques opérationnelles ci-dessus ; le\n"
    "> seuil demeure, la politique jamais changée en silence) et le protocole",
    "SPRT préambule corrigé")

# 5. le facteur 15,3 du préambule v0.11.0 CORRIGÉ
remplace(
    "les benchmarks comparatifs (sha256 : 4 524\n"
    "> instructions/op contre 69 132 à la référence gcc -O2, facteur 15,3, au\n"
    "> MÊME émulateur ; md5/aes écartés par l'auto-vérification de\n"
    "> l'instrument)",
    "les benchmarks comparatifs (sha256 : l'opération complète 75 983\n"
    "> instructions/op contre 69 132 à la référence gcc -O2 et 77 505 à -Os,\n"
    "> au MÊME émulateur — le « facteur 15,3 » publié par la v0.11.0 était\n"
    "> un ARTEFACT DE PÉRIMÈTRE retiré par l'audit D191 ; md5/aes écartés\n"
    "> par l'auto-vérification de l'instrument)",
    "benchmark préambule corrigé")

# 6. le § 1.14 NOUVEAU (avant « ## 2. La couche I »)
remplace(
    "## 2. La couche I : format normalisé des spécifications",
    """### 1.14 Ce que change la v0.13.0

La révision des **corrections de l'édition** (D190/D191/D192, le quatrième
fichier d'instructions). Aucune règle modifiée, aucune couche d'exécution
ajoutée, aucun artefact scellé touché — l'édition CORRIGE les documents,
elle ne légifère pas (le modèle D180/D182).

**Les incohérences corrigées** (la liste de la commande, vérifiée une à une,
le rapport de conformité joint aux livrables) : les quatorze arbres signés
(cohérence avec le garde 14/14) ; la référence au manuscrit accompagnant
portée v0.13.0 ; le compte de lignes du journal UNIFIÉ en valeur exacte
extraite (macros générées — jamais un arrondi) ; « Fig. 5 » devient
« Table 5 » ; la Data Availability portée aux archives v0.13.0 ; la Table 6
des preuves RÉGÉNÉRÉE intégralement en anglais par le générateur
**anti-troncature** (aucune cellule jamais coupée, chaque ligne PARSÉE
depuis les sorties brutes) ; la note TOTAL/brouillons au tableau des
budgets (8 774 + 5 099 = 13 873, les brouillons exclus) ; le paragraphe de
consolidation du § 1.10 aligné sur D181 (douze runs, la balise
`loupe 0.1.1` scellée) ; le tableau de menaces (« le code volé est
inexploitable » devient « l'évolution du code volé est bloquée, son
exécution ne l'est pas ») ; les renvois au manuscrit recalés (§ 3.5 les
preuves renforcées, § 4.1 le modèle formel).

**Les statistiques reformulées** (D190) : la cristallisation — les
caractéristiques opérationnelles P(sceller|q) = (1−q)ⁿ (à q = 50 % :
3,1 % à n=5, 0,098 % à n=10, soit 32× plus strict ; les quantiles
unilatéraux exacts 1,87σ/3,10σ) remplacent les « α = 3,29·10⁻² /
1,08·10⁻³ » de D189 (des rapports de vraisemblance (0,5/0,99)ⁿ mal
étiquetés) ; l'IC95 % EXACT de 11/12 (Clopper-Pearson [0,615 ; 0,998],
la réserve de non-indépendance des itérations séquentielles) ; la règle
de comptage opérationnelle des défauts échappés DÉFINIE en méthodes du
manuscrit (les runs 6/7 à deux défauts comptés une fois chacun ; le
résidu [T0-PÉRIMÉ] du run 12 divulgué, non compté — et pourquoi).

**La neutralité documentaire** (D190) : l'anti-debug léger par mesure de
temps documenté honnêtement dans les deux documents (la portée : la
dissuasion, jamais la résistance) ; la conséquence D81 ajoutée au modèle
de menace (deux éléments trivialement disponibles, le média piège seul
rempart de confidentialité) ; la frontière D105/D81 du clone du
laboratoire (clones temporaires à phrases de test) ; le kit de la
cérémonie D183 préparé sans l'appliquer.

**Le benchmark audité** (D191) : le facteur 15,3 retiré — l'artefact de
périmètre nommé et rejoué sur pièces ; les chiffres corrigés (75 983
contre 69 132 / 77 505), la parité d'extensions ISA au baseline constatée,
le terrain M7 requalifié (qemu TCG, fence.i non prouvé sur silicium).

**L'état de l'art étendu** (D192) : huit références vérifiées DOI/arXiv ;
la revendication « first quantified account » scopée ; RQ3 recadrée en
garanties silencieuses du compilateur.

## 2. La couche I : format normalisé des spécifications""",
    "§ 1.14")

# 7. le § 19.15 NOUVEAU (avant « ## 20. Glossaire »)
remplace(
    "## 20. Glossaire",
    """### 19.15 Correspondance v0.12.0 → v0.13.0

| Évolution | En v0.12.0 | En v0.13.0 | Statut |
|---|---|---|---|
| Incohérences documentaires | onze runs au § 1.10, « Fig. 5 », comptes arrondis, Table 6 tronquée à la main | douze runs (D181), « Table 5 », comptes exacts en macros, Table 6 RÉGÉNÉRÉE anti-troncature | corrigé (D190) |
| Cristallisation | « α = 1,08 × 10⁻³, 46× plus strict » (des rapports de vraisemblance mal étiquetés) | P(sceller\\|q) = (1−q)ⁿ : 3,1 %/0,098 % à q = 50 %, 32× ; quantiles 1,87σ/3,10σ ; l'IC95 exact de 11/12 ; la règle de comptage opérationnelle | reformulé (D190) |
| Benchmark | « facteur 15,3 » (4 524 contre 69 132) | l'opération complète : 75 983 contre 69 132 (-O2) et 77 505 (-Os) — le facteur RETIRÉ, la parité ISA au baseline constatée | audité (D191) |
| Neutralité | « no anti-analysis » (manuscrit) contre l'anti-debug léger (spec) non réconciliés | l'arbitrage D190 : documenté honnêtement dans les DEUX documents ; la conséquence D81 au modèle de menace ; le M7 requalifié (qemu TCG, fence.i non prouvé sur silicium) | arbitré (D190) |
| Séquestre D183 | la proposition documentée (D183), la conséquence D81 absente du modèle de menace | la conséquence D81 consignée (deux éléments trivialement disponibles) ; le kit de cérémonie PRÉPARÉ sans l'appliquer (l'outil CF2 D120, l'autotest VERT, le LISEZMOI, les listes de contrôle) ; la frontière D105/D81 du clone | préparé (D192) |
| État de l'art | design by contract, N-version, DO-178C, supply-chain, live patching, repo-maps | + LLM Compiler, CompCert, Kitsune/POLUS, SWE-agent, sim-to-real (Jakobi/Peng), hardware-in-the-loop (Bacic) — la revendication scopée, RQ3 recadrée | étendu (D192) |

Modifications explicitement rejetées (v0.13.0) : retirer l'anti-debug de la
spécification — rejeté (le mécanisme existe dans l'œuvre scellée, le retirer
du document le falsifierait) ; corriger les décisions historiques en place —
rejeté (le journal est append-only, les corrections vivent en décisions
nouvelles D190-D192) ; masquer le retrait du facteur 15,3 — rejeté (la
correction est publiée avec son mécanisme).

## 20. Glossaire""",
    "§ 19.15")

# 8. la ligne du journal des versions
remplace(
    "| v0.12.0 | 11 nov. 2026 | Révision du MODÈLE FORMEL ET DE LA GOUVERNANCE ASSAINIE",
    """| v0.13.0 | 11 nov. 2026 | Révision des CORRECTIONS DE L'ÉDITION (D190/D191/D192) : les incohérences vérifiées une à une (quatorze arbres, douze runs au § 1.10, comptes exacts en macros, Table 6 régénérée anti-troncature, la note TOTAL/brouillons, les renvois recalés) ; les statistiques reformulées (P(sceller\\|q) = (1−q)ⁿ, quantiles 1,87σ/3,10σ, l'IC95 exact de 11/12 [0,615 ; 0,998], la règle de comptage opérationnelle) ; le benchmark AUDITÉ — le facteur 15,3 retiré comme artefact de périmètre, les chiffres corrigés (75 983 contre 69 132/-Os 77 505), le M7 requalifié (qemu TCG, fence.i non prouvé sur silicium) ; la neutralité documentaire (l'anti-debug arbitré, la conséquence D81 au modèle de menace, la frontière D105/D81, le kit D183 préparé sans l'appliquer) ; l'état de l'art étendu (huit références vérifiées, la revendication scopée, RQ3 recadrée en garanties silencieuses du compilateur). Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |
| v0.12.0 | 11 nov. 2026 | Révision du MODÈLE FORMEL ET DE LA GOUVERNANCE ASSAINIE""",
    "journal des versions")

MD.write_text(s, encoding="utf-8")
print(f"[md v0.13.0] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print("  -", f)
