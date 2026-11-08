#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""revision_v080_md.py — LA RÉVISION v0.8.0 DU PROTOCOLE TRIADE (miroir de
revision_v070_md.py, modèle D133/D137/D169) : la consolidation du programme
d'après M9 (D170/D171). Chaque remplacement est ASSERTÉ (ancrage trouvé UNE
fois exactement) — un ancrage absent ou ambigu = ÉCHEC NOMMÉ, rien n'est
écrit.

Onze remplacements/insertions :
  (1)  titre → v0.8.0 ;
  (2)  bloc d'en-tête : autorité v0.8.0, l'archive v0.7.0 ajoutée, la phrase
       de consolidation du programme d'après M9 ;
  (3)  puce Version (l'état consolidé : M0–M9 franchis, le TGN M10 ouvert,
       la notation 18/18 posée, le 14e arbre attendu) ;
  (4)  puce Date → 8 novembre 2026 ;
  (5)  § 1.2 : la charge de validation du cœur natif porte M0 à M10 ;
  (6)  § 1.10 « Ce que change la v0.8.0 » NOUVEAU ;
  (7)  § 12.4 : treize arbres + LA DETTE DU QUATORZIÈME (l'ère du TGN) ;
  (8)  § 13.5 : le paragraphe de l'ère TGN (la cérémonie attend son geste) ;
  (9)  § 18 : le titre M0 à M10, la rangée M9 FRANCHIE (finale 1.0.0), la
       rangée M10 LE TGN NOUVELLE, la phrase de clôture étendue ;
  (10) § 19.10 « Correspondance v0.7.0 → v0.8.0 » NOUVEAU + rejets ;
  (11) § 21 : la ligne v0.8.0 au journal des versions + la clôture réécrite.
"""

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DOC = REPO / "docs" / "PROTOCOLE_TRIADE.md"

REMP = []


def remplace(ancrage, nouveau):
    REMP.append((ancrage, nouveau))


# ---------------------------------------------------------------- (1) titre
remplace(
    "# PROTOCOLE TRIADE v0.7.0 — Spécification technique",
    "# PROTOCOLE TRIADE v0.8.0 — Spécification technique",
)

# ------------------------------------------------- (2) bloc d'en-tête
remplace(
    "> Source de travail faisant autorité pour la v0.7.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.6.1_Specification.pdf` (v0.6.1),",
    "> Source de travail faisant autorité pour la v0.8.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.7.0_Specification.pdf` (v0.7.0),\n"
    "> `docs/Protocole_TRIADE_v0.6.1_Specification.pdf` (v0.6.1),",
)
remplace(
    "> La v0.7.0 consolide le programme d'après M7 (D160) : le jalon M8 — le domaine `sys`,\n"
    "> les syscalls directs — est franchi (finale 0.9.0 scellée sur run terrain vert recoupé\n"
    "> 30/30), le jalon M9 — le domaine `tls13`, TLS 1.3 pur — est ouvert (couche I complète,\n"
    "> 28 spécifications), et le sceau de l'Intention porte treize arbres, ses cérémonies\n"
    "> d'ère (M8 puis M9) passées sur pièces (garde 13/13) ; la",
    "> La v0.8.0 consolide le programme d'après M9 (D170/D171) : le jalon M9 — TLS 1.3 pur\n"
    "> en blocs scellés, le domaine `tls13` — est FRANCHI (finale `1.0.0` scellée sur le\n"
    "> run terrain vert recoupé et LA SESSION RÉELLE — la ligne applicative chiffrée\n"
    "> échangée avec un serveur réel, D170), et LE TEST GRANDEUR NATURE est ouvert (D171) :\n"
    "> le jalon M10 — coder une application réelle NEUVE entièrement avec TRIADE — porte\n"
    "> l'application « Loupe » (l'éditeur hexadécimal au panneau d'empreintes, le domaine\n"
    "> `loupe`), sa couche I de 18 spécifications et ses QUATRE chantiers de notation\n"
    "> accomplis (le noyau, le rendu + la navigation, l'édition + la table de routage\n"
    "> étendue — les 18 blocs NOTÉS-MESURÉS-PROUVÉS) ; le kit terrain attend LA CÉRÉMONIE\n"
    "> D'ÈRE du TGN (le quatorzième arbre, la dette D166/D171) ; la",
)

# ------------------------------------------------- (3)(4) les puces
remplace(
    "- Version : v0.7.0 — la consolidation du programme d'après M7 (D160) : le jalon M8 (syscalls directs — le domaine `sys`) est franchi, finale `0.9.0` scellée le 05/11/2026 sur run terrain vert recoupé 30/30 sur pièces croisées (Entrée 164, D165) ; le jalon M9 (TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère 1.0.0) est ouvert (D166) : couche I complète — 28 spécifications en six familles, l'instrument 117 contrôles verts (D167) — et cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13, la dette D166 soldée) ; le sceau de l'Intention porte TREIZE arbres (cérémonies d'ère M8 : 12 arbres, D162/D163 ; M9 : 13 arbres, D168) ; la v0.6.1 avait consigné l'arbitrage du niveau du coffre neuf (D137) ; la v0.6.0 avait accompli la souveraineté cryptographique (D133) : axes 2-3-4 prouvés terrain, chaîne réelle du coffre migrée CF1 → CF2 → CF3 ; état des jalons constaté : M0–M6 franchis (balises 0.2.0 à 0.7.0 — M5 rentré le 04/11/2026, Entrée 143/D148 ; M6 franchi le 05/11/2026 sur run terrain WSL2 vert recoupé sur pièces, Entrée 149/D154 — le chantier M5-(c) refermé sur le profil Linux), M7 ouvert (D149 — fiche `docs/PROFIL_riscv64-linux-elf64.md`)",
    "- Version : v0.8.0 — la consolidation du programme d'après M9 (D170/D171) : le jalon M9 (TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère 1.0.0) est FRANCHI le 07/11/2026 — les 28 blocs notés-mesurés-prouvés aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, 5869, 7748, SP 800-38D, la poignée rejouée sur le transcript RFC 8448), le socle socket par syscalls directs, la finale `1.0.0` SCELLÉE sur le run terrain vert recoupé exigé comme pièce, LA SESSION RÉELLE la ligne applicative chiffrée échangée avec un serveur réel (D170) ; LE TEST GRANDEUR NATURE ouvert le 07/11 (D171) : le jalon M10 — coder une application réelle NEUVE entièrement avec TRIADE — porte « Loupe », l'éditeur hexadécimal au panneau d'empreintes (le domaine `loupe`, la lignée i11xxxx) : couche I de 18 spécifications posée écrite-avant-code (D172), les QUATRE chantiers de notation accomplis — le noyau (D173), le rendu + la navigation (D174), l'édition + la table de routage étendue de loupe-09 r2 (D175) — les 18 blocs NOTÉS-MESURÉS-PROUVÉS, la 0.9.0 de l'ère M8 et la 1.0.0 de l'ère M9 refermées propres ; le sceau de l'Intention porte treize arbres et LA DETTE DU QUATORZIÈME est nommée (l'arbre `loupe` et l'extension du registre figé attendent la cérémonie d'ère du TGN, AVANT tout build) ; le projet fils COFFRE-FORT est dégelé en parallèle (D135 amendée par D171)",
)
remplace(
    "- Date : 5 novembre 2026",
    "- Date : 8 novembre 2026",
)

# ------------------------------------------------- (5) § 1.2
remplace(
    "jalons M0 à M9 demeurent la charge de validation du cœur natif.",
    "jalons M0 à M10 demeurent la charge de validation du cœur natif — le TGN\n"
    "l'exige tout entier : de l'intention (la couche I) à l'octet livré (le kit terrain),\n"
    "chaque geste d'une application réelle NEUVE est prouvé sur pièces.",
)

# ------------------------------------------------- (6) § 1.10 NOUVEAU
remplace(
    "## 2. La couche I : format normalisé des spécifications",
    """### 1.10 Ce que change la v0.8.0

La révision de consolidation du programme d'après M9 (D170/D171). Le **jalon M9**
(TLS 1.3 pur en blocs scellés — le domaine `tls13`, l'ère 1.0.0) est **franchi** :
les 28 blocs notés-mesurés-prouvés — les primitives aux vecteurs officiels octet
pour octet (FIPS 180-4, RFC 2104/4231, 5869, 7748, SP 800-38D), la poignée
rejouée sur le transcript RFC 8448, les héritages PAR LA CARTE (R7) —, le socle
socket par syscalls directs, le septième run terrain vert sur pièces et recoupé,
LA SESSION RÉELLE (la ligne applicative chiffrée ÉCHANGÉE avec un serveur réel,
le témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ PAR LA MACHINE, l'épinglage -6 NOMMÉ
contre le vrai serveur, la fermeture propre), la finale `1.0.0` scellée sur le
recoup exigé comme pièce (D170 : le scellage est un fait de carte, l'artefact ne
bouge jamais) — et l'ère M8 refermée propre par l'export de continuité. **LE TEST
GRANDEUR NATURE est ouvert (D171)** : le protocole avait prouvé chaque capacité,
M0 à M9 — il reste à prouver qu'il DÉVELOPPE une application réelle NEUVE, de
l'intention à l'octet livré (le modèle RoomEq s'arrêtait au recodage ; le TGN
exige la CRÉATION). L'application — arbitrée à D171, contredisible — est
« Loupe », l'éditeur hexadécimal au panneau d'empreintes sur le profil primaire
(l'outil du quotidien du projet : voir les octets, leurs lignes, leurs empreintes
md5/sha-256, leur place) : le domaine `loupe` fondé (la charte + le tableau des
18 blocs en cinq familles), la couche I posée écrite-avant-code (D172 : les 18
spécifications, le plan d'adressage arrêté avant toute notation, la table des
sept verdicts), et les QUATRE chantiers de notation accomplis — le noyau
fichier + empreintes (D173 : les héritages vivent à leurs adresses scellées, le
mini-OS virtuel du harnais), le rendu + la navigation (D174 : l'oracle à
scénarios — l'écran attendu octet par octet —, le mini-GUI virtuel, le plancher
qui ne recule jamais), l'édition + la table de routage étendue de loupe-09 r2
(D175 : le disque saisissable et la mort du harnais, le réseau de la garde
16↔17↔18, l'écriture à l'octet prouvée différentielle) — les 18 blocs
NOTÉS-MESURÉS-PROUVÉS, 45 + 53 + 59 contrôles verts aux trois graines sur les
trois harnais. Le **kit terrain attend LA CÉRÉMONIE D'ÈRE du TGN** : la dette
D166/D171 est nommée à la naissance — le quatorzième arbre (`loupe`) et
l'extension du registre figé exigent la clé hors-ligne du développeur AVANT
tout build (§ 13.5) ; le garde demeure à treize arbres. Le projet fils
COFFRE-FORT est dégelé en parallèle (D135 amendée par D171) : le père continue
sans ralentir, la frontière fondatrice demeure INTACTE. Aucune règle du cœur
n'est modifiée ; aucune couche n'est ajoutée à l'exécution ; la hiérarchie de la
fonction objectif est inchangée.

## 2. La couche I : format normalisé des spécifications""",
)

# ------------------------------------------------- (7) § 12.4
remplace(
    "Treize arbres de couche I vivent sous le sceau — les lignées m0 à m8 (le domaine\n"
    "`sys` depuis l'ère M8), l'arbre `tls13` (le domaine TLS 1.3 pur depuis l'ère M9),\n"
    "`demo`, `terrain`, et `v06/I` : la spécification du sceau est la première couche\n"
    "qu'il garde.",
    "Treize arbres de couche I vivent sous le sceau — les lignées m0 à m8 (le domaine\n"
    "`sys` depuis l'ère M8), l'arbre `tls13` (le domaine TLS 1.3 pur depuis l'ère M9),\n"
    "`demo`, `terrain`, et `v06/I` : la spécification du sceau est la première couche\n"
    "qu'il garde. **Le quatorzième arbre est nommé** : l'ère du TGN (le domaine\n"
    "`loupe`, D171) porte sa dette de cérémonie à la naissance — l'arbre `loupe` et\n"
    "l'extension du registre figé m0 attendent la re-signature hors-ligne du\n"
    "développeur AVANT tout build de l'application ; le garde demeure à treize arbres\n"
    "jusque-là, AUCUN arbre signé n'est touché.",
)

# ------------------------------------------------- (8) § 13.5
remplace(
    "La règle qui en découle : la cérémonie d'ère\n"
    "n'est pas une formalité de documentation — c'est le geste qui rend le build de\n"
    "l'ère possible, et il suit le calendrier du garde, jamais l'inverse.",
    "La règle qui en découle : la cérémonie d'ère\n"
    "n'est pas une formalité de documentation — c'est le geste qui rend le build de\n"
    "l'ère possible, et il suit le calendrier du garde, jamais l'inverse. **L'ère du\n"
    "TGN (le domaine `loupe`, D171/D175)** suit la même discipline : la dette fut\n"
    "nommée à la naissance de la couche I (D171, règle 8) et la notation des 18 blocs\n"
    "s'accomplit sous elle — quatre chantiers, la table de routage de loupe-09 étendue\n"
    "en révision nommée sans cascade — AUCUN build : la cérémonie précède (le miroir\n"
    "des ères M8/M9). Le kit de cérémonie vit au dossier `/Cérémonie` du Drive (la\n"
    "remise FRAÎCHE des quatorze arbres — la charge se prépare AU GESTE de la\n"
    "cérémonie, D168 : les empreintes bougent avec chaque révision de spécification —\n"
    "le LISEZMOI pas à pas, la règle d'or « JAMAIS generer ») : le développeur signe\n"
    "hors ligne à la clé du 04/11 (l'ancre de toutes les ères), ramène\n"
    "signatures-I.txt et cle-publique-I.txt au coffre `/test` ; le laboratoire\n"
    "rapatrie, recoupe (l'ancre de clé, les arbres inchangés rendant les MÊMES\n"
    "signatures par le déterminisme Ed25519, m0 re-signé au registre étendu, l'arbre\n"
    "`loupe` neuf), installe canoniquement — et le garde passe à QUATORZE arbres\n"
    "VERTS : le build de Loupe peut naître.",
)

# ------------------------------------------------- (9) § 18
remplace(
    "## 18. Critères d'acceptation des jalons M0 à M9\n"
    "\n"
    "Dix jalons, chacun couvrant une capacité nouvelle et se terminant par des critères de\n"
    "sortie mesurables — détail dans `docs/PLAN_MILESTONES.md`, mis à jour avec la présente\n"
    "révision.",
    "## 18. Critères d'acceptation des jalons M0 à M10\n"
    "\n"
    "Onze jalons, chacun couvrant une capacité nouvelle et se terminant par des critères de\n"
    "sortie mesurables — détail dans `docs/PLAN_MILESTONES.md`, mis à jour avec la présente\n"
    "révision.",
)
remplace(
    "| M9 | TLS 1.3 pur (domaine `tls13`) | la charte à huit règles et les 28 spécifications en six familles écrites-avant-code ; les primitives aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, RFC 5869, RFC 7748, SP 800-38D) ; la poignée rejouée sur le transcript RFC 8448 ; le socle socket par syscalls directs (sys-04+) ; la cérémonie de l'ère avant construire() ; la session réelle avec un serveur réel — la ligne applicative chiffrée | **ouvert** 05/11/2026 (D166) — couche I complète (28 spécifications, l'instrument 117 verts, D167) ; cérémonie de l'ère passée le 05/11 (13 arbres, garde 13/13 — la dette soldée) ; chantiers (b) notation, (c) harnais RFC 8448, (d) socle socket, (e) build 1.0.0-dev.1, (f) terrain → finale `1.0.0` |",
    "| M9 | TLS 1.3 pur (domaine `tls13`) | la charte à huit règles et les 28 spécifications en six familles écrites-avant-code ; les primitives aux vecteurs officiels (FIPS 180-4, RFC 2104/4231, RFC 5869, RFC 7748, SP 800-38D) ; la poignée rejouée sur le transcript RFC 8448 ; le socle socket par syscalls directs (sys-04+) ; la cérémonie de l'ère avant construire() ; la session réelle avec un serveur réel — la ligne applicative chiffrée | **franchi** 07/11/2026 — finale `1.0.0` (Entrées 170–194, D166–D170 : les 28 blocs notés-mesurés-prouvés, le run terrain vert recoupé EXIGÉ COMME PIÈCE du scellage, LA SESSION RÉELLE — la ligne applicative chiffrée échangée avec un serveur réel, le témoin déchiffré par la machine, l'épinglage -6 nommé ; le scellage un fait de carte, proxy.exe byte-identique `446279f3…`) |\n"
    "| M10 | Le test grandeur nature — « Loupe » (domaine `loupe`) | coder une application réelle NEUVE entièrement avec TRIADE, de l'intention (la couche I) à l'octet livré (le kit terrain) ; les 18 spécifications écrites-avant-code avant tout octet de notation (R2) ; les héritages PAR LA CARTE byte-identiques aux adresses scellées (R7) ; l'oracle à scénarios vert — l'écran attendu octet par octet ; le kit déployé au coffre `/test` (modèle m9f) ; la balise `loupe 0.1.0` scellée sur run terrain recoupé | **ouvert** 07/11/2026 (D171) — la couche I complète (18 spécifications, D172) et les QUATRE chantiers de notation accomplis : le noyau (D173), le rendu + la navigation (D174), l'édition + la table de routage étendue de loupe-09 r2 (D175) — les 18 blocs NOTÉS-MESURÉS-PROUVÉS (59 + 53 + 45 contrôles verts aux trois graines) ; LA CÉRÉMONIE D'ÈRE du TGN précède le build (le 14e arbre, la dette D166/D171) puis le kit terrain (M10-(d) seconde moitié) et le run (M10-(e)) |",
)
remplace(
    "M8 et M9 sont les additions mesurées du\n"
    "programme d'après M7 (D160) : la fondation d'abord — le domaine `sys` est la\n"
    "condition d'une pile TLS 1.3 qui n'émettrait plus par l'IAT userland ; chaque\n"
    "famille s'appuie sur les résultats mesurés de la précédente.",
    "M8 et M9 sont les additions mesurées du\n"
    "programme d'après M7 (D160) : la fondation d'abord — le domaine `sys` est la\n"
    "condition d'une pile TLS 1.3 qui n'émettrait plus par l'IAT userland ; chaque\n"
    "famille s'appuie sur les résultats mesurés de la précédente. M10 est l'épreuve de\n"
    "la MÉTHODE ENTIÈRE (D171) : non plus une capacité, mais une application réelle\n"
    "neuve — l'outil du quotidien du projet — développée de l'intention à l'octet\n"
    "livré, chaque geste prouvé ; la notation entière (18 blocs) est déjà\n"
    "notée-mesurée-prouvée, le build attend la cérémonie d'ère du TGN.",
)

# ------------------------------------------------- (10) § 19.10 NOUVEAU
remplace(
    "## 20. Glossaire",
    """### 19.10 Correspondance v0.7.0 → v0.8.0

| Évolution | En v0.7.0 | En v0.8.0 | Statut |
|---|---|---|---|
| Programme d'après M9 | M9 ouvert : couche I complète, la cérémonie passée, les chantiers (b) à (f) attendent | M9 FRANCHI : les 28 blocs notés-mesurés-prouvés, le septième run terrain vert recoupé, LA SESSION RÉELLE (la ligne applicative chiffrée avec un serveur réel), la finale `1.0.0` scellée sur recoup exigé comme pièce (D170) | révisé (D170) |
| Le test grandeur nature | — | LE TGN ouvert (D171) : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — coder une application réelle NEUVE entièrement avec TRIADE ; le domaine `loupe` fondé, la couche I de 18 spécifications posée (D172) et les QUATRE chantiers de notation accomplis (D173/D174/D175 : les 18 blocs notés-mesurés-prouvés, la table de routage de loupe-09 étendue en révision nommée) | nouveau (D171–D175) |
| Sceau de l'Intention | treize arbres, les cérémonies d'ère M8/M9 passées | treize arbres + LA DETTE DU QUATORZIÈME nommée (l'ère du TGN : l'arbre `loupe` et le registre figé étendu attendent la clé hors-ligne AVANT tout build — § 13.5) ; le garde demeure à 13/13 jusque-là | étendu (D166/D171/D175) |
| Projet fils COFFRE-FORT | développement différé (D135) | DÉGELÉ en parallèle du TGN (D171) : le fils vit son rythme, la frontière fondatrice intacte — aucun code TRIADE forké, aucune dépendance vivante | révisé (D171) |
| Chaîne PDF | spec_v070 | chaîne spec_v080 ; l'archive v0.7.0 demeure | révisé (D176) |

Modifications explicitement rejetées (v0.8.0) : réviser la spécification à chaque
franchissement — rejeté : le versionnement suit les RÉVISIONS (la v0.8.0 consolide
le PROGRAMME d'après M9 : M9 franchi ET le TGN ouvert, deux moteurs d'une même
passation). Mettre l'application « Loupe » sous le sceau AVANT la cérémonie —
rejeté : le garde suit le calendrier de la cérémonie, jamais l'inverse (§ 13.5).
Ajouter un profil de cible pour le TGN — rejeté : le profil primaire
`x86-64-win11-pe` est l'épreuve ; l'universalité est déjà prouvée (M6/M7).
Sceller la 0.1.0 de Loupe au build — rejeté : la balise de développement naît au
build (geste de BUILD jamais scellage, miroir M6/M7/M8) ; la 0.1.0 se scellera sur
le run terrain vert recoupé.

## 20. Glossaire""",
)

# ------------------------------------------------- (11) § 21
remplace(
    "| Version | Date | Contenu |\n|---|---|---|\n",
    "| Version | Date | Contenu |\n|---|---|---|\n"
    "| v0.8.0 | 8 nov. 2026 | Révision de consolidation du programme d'après M9 (D170/D171) : le jalon M9 — TLS 1.3 pur en blocs scellés — est FRANCHI (les 28 blocs notés-mesurés-prouvés, la finale `1.0.0` scellée sur recoup exigé comme pièce, LA SESSION RÉELLE la ligne applicative chiffrée avec un serveur réel — D170) ; LE TEST GRANDEUR NATURE ouvert (D171) : le jalon M10 porte « Loupe », l'éditeur hexadécimal au panneau d'empreintes — la couche I de 18 spécifications (D172) et les QUATRE chantiers de notation accomplis (D173–D175 : les 18 blocs notés-mesurés-prouvés, la table de routage de loupe-09 étendue) ; la dette du quatorzième arbre nommée (la cérémonie d'ère du TGN précède le build) ; le projet fils COFFRE-FORT dégelé en parallèle. Aucune règle modifiée, aucune couche d'exécution ajoutée, hiérarchie inchangée |\n",
)
remplace(
    "La présente version consolide le programme d'après M7 (D160, § 1.9) et l'état au\n"
    "passage de relais : jalons M0 à M8 franchis sur validations terrain (balises\n"
    "finales 0.2.0 à 0.9.0), le programme de souveraineté cryptographique accompli\n"
    "(axes 2-3-4, D133) — le coffre réel a migré CF1 → CF2 → CF3 les 30–31 octobre\n"
    "2026 —, le sceau de l'Intention portant treize arbres signés, ses cérémonies d'ère\n"
    "passées sur pièces (garde 13/13) ; jalon M9 (TLS 1.3 pur) ouvert : sa couche I est\n"
    "complète et sa cérémonie d'ère passée — les chantiers de notation, de harnais, de\n"
    "socle socket et de build attendent. La clause « hors périmètre courant » est levée\n"
    "nommément pour les deux premières familles du programme D160 ; les profils\n"
    "additionnels après M7 restent volontairement hors du périmètre courant afin que\n"
    "chaque addition s'appuie sur des résultats mesurés.",
    "La présente version consolide le programme d'après M9 (D170/D171, § 1.10) et\n"
    "l'état au passage de relais : jalons M0 à M9 franchis sur validations terrain\n"
    "(balises finales 0.2.0, 0.9.0 et `1.0.0` — la session réelle la ligne applicative\n"
    "chiffrée), le programme de souveraineté cryptographique accompli (axes 2-3-4,\n"
    "D133), le sceau de l'Intention portant treize arbres signés ; LE TEST GRANDEUR\n"
    "NATURE est ouvert (M10, D171) : « Loupe » — l'éditeur hexadécimal au panneau\n"
    "d'empreintes — porte sa couche I entière et ses 18 blocs notés-mesurés-prouvés ;\n"
    "le kit terrain attend LA CÉRÉMONIE D'ÈRE du TGN (le quatorzième arbre, la dette\n"
    "D166/D171 — le garde à 13/13 jusque-là), puis le build `loupe 0.1.0-dev.1` et le\n"
    "run terrain. Les profils additionnels après M7 restent volontairement hors du\n"
    "périmètre courant afin que chaque addition s'appuie sur des résultats mesurés.",
)


def main():
    texte = DOC.read_text(encoding="utf-8")
    echecs = []
    for anc, nouv in REMP:
        n = texte.count(anc)
        if n != 1:
            echecs.append(f"ancrage {n} fois : {anc[:70]!r}…")
            continue
        texte = texte.replace(anc, nouv)
    if echecs:
        print("ÉCHEC — la révision v0.8.0 n'est PAS écrite :")
        for e in echecs:
            print(f"  [!] {e}")
        return 1
    if "PROTOCOLE TRIADE v0.7.0" in texte:
        print("ÉCHEC — il reste une mention v0.7.0 hors archive")
        return 1
    DOC.write_text(texte, encoding="utf-8")
    print("La révision v0.8.0 du PROTOCOLE_TRIADE.md est écrite :",
          len(REMP), "remplacements assertés")
    return 0


if __name__ == "__main__":
    sys.exit(main())
