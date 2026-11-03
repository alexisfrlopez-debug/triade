#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Révision v0.6.1 de docs/PROTOCOLE_TRIADE.md (source de travail).

D137 — le niveau de sécurité d'un coffre neuf (CF1/CF2/CF3) devient
l'arbitrage du développeur lors de la création de son projet de
développement : imposer CF3 par défaut (règle v0.6.0, D133) risque d'être
trop contraignant selon le projet.

Convention maison (miroir de revision_v060_md.py / revision_v050_md.py) :
chaque remplacement est VÉRIFIÉ (assert) — échec bruyant plutôt que silence.
Aucune renumérotation : les ajouts sont des sous-sections qui s'insèrent
dans la numérotation existante (§ 1.8, § 19.8).

Touches :
(1) titre + bloc d'en-tête + puce version ;
(2) § 1.7 : la phrase de naissance passe au passé, renvoi ajouté ;
(3) § 1.8 « Ce que change la v0.6.1 » (nouveau) ;
(4) § 12.5 réécrit — l'arbitrage, les trois naissances, le guide,
    les obligations par niveau ;
(5) § 19.8 « Correspondance v0.6.0 → v0.6.1 » + rejets (nouveau) ;
(6) journal des versions : ligne v0.6.1 ;
(7) paragraphe de clôture : l'arbitrage consigné.
"""

from pathlib import Path

P = Path("/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md")
s = P.read_text(encoding="utf-8")


def remplace(ancien, nouveau):
    """Remplacement ASSERTÉ — échec bruyant, jamais silencieux."""
    global s
    n = s.count(ancien)
    assert n == 1, f"attendu 1 occurrence, trouvée {n} : {ancien[:90]!r}"
    s = s.replace(ancien, nouveau)


def insere_avant(ancre, bloc):
    """Insertion ASSERTÉE d'un bloc juste avant l'ancre."""
    global s
    n = s.count(ancre)
    assert n == 1, f"ancre attendue 1 fois, trouvée {n} : {ancre[:70]!r}"
    s = s.replace(ancre, bloc + ancre)


# ================================================================ 1. TITRE
remplace("# PROTOCOLE TRIADE v0.6.0 — Spécification technique",
         "# PROTOCOLE TRIADE v0.6.1 — Spécification technique")

# ================================================================ 2. EN-TÊTE
remplace("""> Source de travail faisant autorité pour la v0.6.0. Les archives formelles des versions
> précédentes demeurent : `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (v0.5.2),""",
         """> Source de travail faisant autorité pour la v0.6.1. Les archives formelles des versions
> précédentes demeurent : `docs/Protocole_TRIADE_v0.6.0_Specification.pdf` (v0.6.0),
> `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (v0.5.2),""")

remplace("""présentation IMRAD du noyau v0.3, sans valeur normative) ; depuis la v0.6.0, le
> **Livre du Coffre** l'accompagne (`docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.0.pdf`,
> D133 — complément opératoire : cérémonies, runbook, mode dégradé). Depuis la décision D17,""",
         """présentation IMRAD du noyau v0.3, sans valeur normative) ; depuis la v0.6.0, le
> **Livre du Coffre** l'accompagne (`docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.1.pdf`,
> D133 — complément opératoire : cérémonies, runbook, mode dégradé ; v1.1 : l'arbitrage
> D137 du niveau de naissance y est aligné). Depuis la décision D17,""")

remplace("""> La v0.6.0 consigne la passation du programme de souveraineté cryptographique (D133) :
> axes 2-3-4 accomplis et prouvés sur terrain — la chaîne réelle du coffre a migré
> CF1 → CF2 → CF3 les 30–31 octobre 2026 ; la v0.5.2 avait consigné la garde durable de""",
         """> La v0.6.1 consigne l'arbitrage du niveau de naissance d'un coffre neuf (D137) ; la
> v0.6.0 avait consigné la passation du programme de souveraineté cryptographique (D133) :
> axes 2-3-4 accomplis et prouvés sur terrain — la chaîne réelle du coffre a migré
> CF1 → CF2 → CF3 les 30–31 octobre 2026 ; la v0.5.2 avait consigné la garde durable de""")

remplace("- Version : v0.6.0 — souveraineté cryptographique accomplie (D133) : axes 2-3-4 prouvés terrain, chaîne réelle du coffre migrée CF1 → CF2 → CF3, un coffre neuf naît CF3 ; état des jalons constaté : M0–M4 franchis (balises 0.2.0 à 0.5.0), M5 ouvert (D133)",
         "- Version : v0.6.1 — le niveau du coffre neuf (CF1/CF2/CF3) devient l'arbitrage du développeur à la création (D137) ; la v0.6.0 avait accompli la souveraineté cryptographique (D133) : axes 2-3-4 prouvés terrain, chaîne réelle du coffre migrée CF1 → CF2 → CF3 ; état des jalons constaté : M0–M4 franchis (balises 0.2.0 à 0.5.0), M5 ouvert (D133)")

# ============================================================ 3. § 1.7 (passé)
remplace("""construction (D130) : le détail vit au § 13. Un **coffre neuf naît désormais CF3** :
`init` direct à l'époque 1 — la chaîne de migration est l'histoire du coffre réel, pas
un rite obligé.""",
         """construction (D130) : le détail vit au § 13. Un **coffre neuf naissait CF3** :
`init` direct à l'époque 1 — la chaîne de migration est l'histoire du coffre réel, pas
un rite obligé (la v0.6.1 remet ce choix au développeur — § 1.8, § 12.5).""")

# ============================================================ 4. § 1.8 (nouveau)
SECTION_18 = """### 1.8 Ce que change la v0.6.1

Une seule règle, explicitement invalidée et remplacée (§ 19.8) : le niveau de
sécurité d'un coffre neuf. La v0.6.0 (D133) l'avait fixé — un coffre neuf naît CF3,
`init` direct à l'époque 1 ; la v0.6.1 (D137) en fait **l'arbitrage du développeur au
moment de créer son projet de développement** : CF1, CF2 ou CF3, chacun avec son acte
de naissance, ses obligations et son guide (§ 12.5) — imposer CF3 par défaut risque
d'être trop contraignant selon le projet : média du piège à produire dès le premier
jour, cycle en deux actes à chaque session, sachet physique à tenir — la contrainte se
justifie quand le secret la mérite. La chaîne de migration CF1 → CF2 → CF3 demeure
disponible à tout moment pour un coffre dont les besoins grandissent ; le coffre réel
de TRIADE reste CF3 (époque 1, checksum `0cc89a96`). Aucune autre règle n'est
modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la fonction
objectif est inchangée.

"""
insere_avant("## 2. La couche I : format normalisé des spécifications", SECTION_18)

# ============================================================ 5. § 12.5 (réécrit)
remplace("""### 12.5 Le coffre neuf naît CF3

La chaîne CF1 → CF2 → CF3 est le chemin *historique* du coffre réel. Un coffre neuf
n'a rien à migrer : `coffre_cf3.py init` le crée sous CF3, époque 1, média du piège
dès le premier jour. La question du terrain — *puisqu'on impose CF3 dès la création,
la sentinelle ne devient-elle pas inutile ?* — reçoit sa réponse normative : la
sentinelle de CF3 n'est pas un composant qu'on peut oublier de lancer, c'est la
serrure elle-même ; l'exigence D120 est réalisée *par construction*. Ce qui demeure
obligatoire : le média du piège (sans S_piège, le déverrouillage est *impossible*) et
la discipline du sachet (§ 13).""",
         """### 12.5 Le niveau du coffre neuf — un arbitrage du développeur (D137)

La chaîne CF1 → CF2 → CF3 est le chemin *historique* du coffre réel ; elle n'est plus
un rang de naissance. La v0.6.0 fixait la règle « un coffre neuf naît CF3 » (`init`
direct, époque 1, média du piège dès le premier jour) ; la v0.6.1 revient sur cet
arbitrage : **le niveau de sécurité d'un coffre neuf — CF1, CF2 ou CF3 — est choisi
par le développeur lors de la création de son projet de développement** (D137).
Imposer CF3 par défaut risque d'être trop contraignant selon le projet : le niveau le
plus fort exige un média de piège dès le premier jour, le cycle en deux actes à chaque
session, le sachet physique et sa carte — la contrainte se justifie quand le secret la
mérite, pas pour tout projet.

**Les trois naissances** — l'acte de création détermine le niveau et ses obligations :

| Niveau | Acte de création | Ce qui vient avec |
|---|---|---|
| CF1 | `coffre_fort.py init` | conteneur chiffré à phrase (D75) ; garde durable de la phrase (D81) ; relève simple |
| CF2 | `coffre_fort.py init` puis cérémonie `coffre_cf2.py migrer` — l'`init` direct de CF2 demeure un outil de LABORATOIRE, la spécification scellée CF2 (§ 12 — phase laboratoire / cérémonie réelle) fait foi | clé maîtresse répartie Shamir (N gardes, seuil T), T copies hors-ligne, liste blanche, sentinelle/porte D120 |
| CF3 | `coffre_cf3.py init` | époque 1, média du piège dès le premier jour, cycle en deux actes, sentinelle par invocation, sachet + carte papier (§ 13) |

**Le guide de l'arbitrage** (recommandation, pas contrainte) : CF1 suffit quand la
menace est le vol au repos du poste seul et que la simplicité de relève prime —
prototype, projet jetable, secrets reproductibles ; CF2 quand la garde doit être
partagée ou survivre au maître — quorum, relève à plusieurs ; CF3 pour les secrets
maîtresses d'un projet vivant sous menace d'expropriation — la référence demeure le
coffre réel de TRIADE, né CF1 et monté à CF3 par cérémonies. La montée n'est jamais
bloquée : **la chaîne de migration CF1 → CF2 → CF3 reste disponible à tout moment** —
les besoins grandissent, le coffre suit ; la descente de niveau n'existe pas (`bruler`
demeure l'acte de fin de vie). Le niveau choisi se consigne au journal des décisions
du projet avec sa raison — un arbitrage muet serait un contrat non écrit (§ 3).

La question du terrain — *puisqu'un coffre né CF3 porte sa sentinelle dès la
création, celle-ci ne devient-elle pas inutile ?* — garde sa réponse normative au
niveau CF3 : la sentinelle de CF3 n'est pas un composant qu'on peut oublier de
lancer, c'est la serrure elle-même ; l'exigence D120 est réalisée *par construction*.
Ce qui demeure obligatoire, niveau par niveau : CF1 — la garde durable de la phrase ;
CF2 — les T copies hors-ligne et la liste blanche ; CF3 — le média du piège (sans
S_piège, le déverrouillage est *impossible*) et la discipline du sachet (§ 13).""")

# ============================================================ 6. § 19.8 (nouveau)
SECTION_198 = """### 19.8 Correspondance v0.6.0 → v0.6.1

| Évolution | En v0.6.0 | En v0.6.1 | Statut |
|---|---|---|---|
| Niveau de naissance d'un coffre neuf | un coffre neuf naît CF3 — `init` direct à l'époque 1 (D133) | le niveau (CF1/CF2/CF3) est arbitré par le développeur à la création de son projet : les trois naissances, le guide et les obligations par niveau (§ 12.5) ; la chaîne de migration demeure disponible à tout moment | révisé (D137) |
| Le coffre réel | CF3 (époque 1, checksum `0cc89a96`) | inchangé — la révision est un droit de création, pas un geste sur le coffre vivant | constaté |
| Chaîne PDF et Livre du Coffre | spécification v0.6.0 (37 p.) ; Livre v1.0 | chaîne spec_v061 (l'erratum typographique « tbp] » page 31 réparé au passage) ; Livre v1.1 — runbook « coffre neuf » et FAQ terrain alignés sur D137 | révisé (D137) |
| Le reste de la spécification | — | inchangé : aucune autre règle, aucune couche d'exécution ajoutée, hiérarchie inchangée | constaté |

Modifications explicitement rejetées (v0.6.1) : imposer CF1 par défaut en guise de
souplesse — rejeté : remplacer une imposition par une autre ne rend pas la décision au
développeur. Rendre le niveau mutable sans cérémonie — rejeté : le niveau change par
MIGRATION uniquement, acte explicite et fail-closed (l'anti-retour d'époque et le
verrou croisé demeurent). Promouvoir l'`init` de CF2 (laboratoire) en cérémonie réelle
dans cette révision — rejeté : la spécification scellée CF2 fait foi ; la naissance
CF2 passe par `init` CF1 puis `migrer`, tout est prouvé ; l'arbitrage est consigné si
le besoin naît. Toucher au code des trois outils — rejeté : les trois actes de
création existent et sont prouvés ; c'est le droit de choisir qui manquait, pas la
mécanique.

"""
insere_avant("## 20. Glossaire", SECTION_198)

# ============================================================ 7. Journal des versions
remplace("""| v0.6.0 | 31 oct. 2026 | Passation du programme de souveraineté cryptographique (D133) :""",
         """| v0.6.1 | 31 oct. 2026 | Révision de l'arbitrage de naissance du coffre (D137) : le niveau de sécurité d'un coffre neuf — CF1, CF2 ou CF3 — est choisi par le développeur lors de la création de son projet de développement ; la règle v0.6.0 « un coffre neuf naît CF3 » (D133) est explicitement invalidée et remplacée — imposer CF3 par défaut risque d'être trop contraignant selon le projet. § 12.5 réécrit (les trois naissances, guide de l'arbitrage, obligations par niveau) ; § 1.8 ajouté ; correspondance v0.6.0 → v0.6.1 (§ 19.8) ; la chaîne de migration CF1 → CF2 → CF3 demeure disponible à tout moment ; le coffre réel reste CF3 ; le *Livre du Coffre* passe à v1.1 (runbook et FAQ alignés) ; erratum typographique « tbp] » (page 31 du PDF v0.6.0) réparé dans la chaîne spec_v061. Une règle modifiée et nommée ; aucune couche d'exécution ajoutée ; hiérarchie inchangée |
| v0.6.0 | 31 oct. 2026 | Passation du programme de souveraineté cryptographique (D133) :""")

# ============================================================ 8. Paragraphe de clôture
remplace("""La présente version consigne l'état au passage de relais : jalons M0 à M4 franchis sur""",
         """La présente version consigne l'arbitrage du niveau de naissance d'un coffre neuf
(D137, § 12.5) et l'état au passage de relais : jalons M0 à M4 franchis sur""")

# ============================================================ ÉCRITURE
P.write_text(s, encoding="utf-8")
print(f"[revision_v061_md] PROTOCOLE_TRIADE.md → v0.6.1 ({len(s)} caractères)")
print("[revision_v061_md] touches : titre, en-tête, § 1.7 passé, § 1.8 nouveau,")
print("[revision_v061_md]          § 12.5 réécrit, § 19.8 nouveau, versions +1, clôture")
