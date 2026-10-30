#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Passation v0.6.0 de docs/PROTOCOLE_TRIADE.md (source de travail).

Convention maison (miroir de revision_v050_md.py) : chaque remplacement est
vérifié (assert) — échec bruyant plutôt que silence. Deux temps :
(1) renumérotation 12→14 … 19→21 (en-têtes, sous-sections, références « § N »,
    en ordre DÉCROISSANT pour éviter les double-décalages) ;
(2) insertion du contenu neuf (§ 1.7, § 12 souveraineté, § 13 cérémonies,
    menaces, jalons, correspondance 19.7, journal des versions, glossaire).
"""

import re
from pathlib import Path

P = Path("/home/z/my-project/triade/docs/PROTOCOLE_TRIADE.md")
s = P.read_text(encoding="utf-8")


def remplace(ancien, nouveau, occurrence=None):
    global s
    n = s.count(ancien)
    if n == 0:
        marqueur = nouveau.strip().splitlines()[0][:60]
        assert marqueur in s, f"introuvable : {ancien[:80]!r} / {marqueur!r}"
        return
    if occurrence is None:
        s = s.replace(ancien, nouveau)
    else:
        assert n >= occurrence, f"occurrences insuffisantes ({n}) : {ancien[:60]!r}"
        s = s.replace(ancien, nouveau, occurrence)


def renum_regex(motif, cible, attendu):
    """Renumérote par regex, en vérifiant le compte EXACT des touches."""
    global s
    trouve = len(re.findall(motif, s, flags=re.M))
    assert trouve == attendu, f"{motif!r}: {trouve} touches, {attendu} attendues"
    s = re.sub(motif, cible, s, flags=re.M)


# ================================================================ 1. RENUMÉROTATION
# ordre décroissant : 19→21, 18→20, 17→19 (x avant x), 16→18, 15→17,
# 14→16, 13→15, 12→14.
renum_regex(r"^## 19\. Journal des versions", "## 21. Journal des versions", 1)
renum_regex(r"§ 19\b", "§ 21", 4)
renum_regex(r"^## 18\. Glossaire", "## 20. Glossaire", 1)
for chiffres, attendu in [("17.6", 1), ("17.5", 1), ("17.3", 1), ("17.2", 1)]:
    renum_regex("§ " + chiffres.replace(".", "\\."),
                "§ " + chiffres.replace("17", "19"), attendu)
renum_regex(r"§ 17\b", "§ 19", 1)
for sub in ["17.6", "17.5", "17.4", "17.3", "17.2", "17.1"]:
    renum_regex(rf"^### {sub} ", f"### {sub.replace('17', '19')} ", 1)
renum_regex(r"^## 17\. Correspondance des versions", "## 19. Correspondance des versions", 1)
renum_regex(r"§ 16\b", "§ 18", 3)
renum_regex(r"^## 16\. Critères d'acceptation des jalons M0 à M7",
            "## 18. Critères d'acceptation des jalons M0 à M7", 1)
for chiffres, attendu in [("15.3", 8), ("15.2", 9), ("15.1", 1)]:
    renum_regex("§ " + chiffres.replace(".", "\\."),
                "§ " + chiffres.replace("15", "17"), attendu)
renum_regex("§ 15\\b", "§ 17", 1)
for sub in ["15.3", "15.2", "15.1"]:
    renum_regex(rf"^### {sub} ", f"### {sub.replace('15', '17')} ", 1)
renum_regex(r"^## 15\. Gouvernance", "## 17. Gouvernance", 1)
for sub in ["14.2", "14.1"]:
    renum_regex(rf"^### {sub} ", f"### {sub.replace('14', '16')} ", 1)
renum_regex(r"^## 14\. Profils de cible — universalité",
            "## 16. Profils de cible — universalité", 1)
renum_regex("§ 13\\.1", "§ 15.1", 6)
renum_regex(r"§ 13\b", "§ 15", 1)
for sub in ["13.2", "13.1"]:
    renum_regex(rf"^### {sub} ", f"### {sub.replace('13', '15')} ", 1)
renum_regex(r"^## 13\. Sécurité : modèle de menace et limites",
            "## 15. Sécurité : modèle de menace et limites", 1)
renum_regex(r"§ 12\b", "§ 14", 7)
renum_regex(r"^## 12\. Coût en tokens : fragmentation, localisation, budgets",
            "## 14. Coût en tokens : fragmentation, localisation, budgets", 1)

# ================================================================ 2. TITRE + EN-TÊTE
remplace(
    "# PROTOCOLE TRIADE v0.5.2 — Spécification technique",
    "# PROTOCOLE TRIADE v0.6.0 — Spécification technique",
)
remplace(
    "> Source de travail faisant autorité pour la v0.5.2. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (v0.5.0),",
    "> Source de travail faisant autorité pour la v0.6.0. Les archives formelles des versions\n"
    "> précédentes demeurent : `docs/Protocole_TRIADE_v0.5.2_Specification.pdf` (v0.5.2),\n"
    "> `docs/Protocole_TRIADE_v0.5.0_Specification.pdf` (v0.5.0),",
)
remplace(
    "> et l'édition académique v0.4 (`docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf`, D18 —\n"
    "> présentation IMRAD du noyau v0.3, sans valeur normative). Depuis la décision D17,",
    "> et l'édition académique v0.4 (`docs/Protocole_TRIADE_v0.4_Article_Recherche.pdf`, D18 —\n"
    "> présentation IMRAD du noyau v0.3, sans valeur normative) ; depuis la v0.6.0, le\n"
    "> **Livre du Coffre** l'accompagne (`docs/Livre_du_Coffre_TRIADE_CF1-CF3_v1.0.pdf`,\n"
    "> D133 — complément opératoire : cérémonies, runbook, mode dégradé). Depuis la décision D17,",
)
remplace(
    "> La v0.5.2 consigne la garde durable de la phrase de contrôle du coffre-fort (D81) ;\n"
    "> la v0.5.1 avait ajouté le coffre-fort des phrases maîtresses (D75) et consigné M3 franchi\n"
    "> (balise finale 0.4.0) ; la v0.5.0 demeure la révision du retour du terrain (validation\n"
    "> normée, taxonomie X1–X8, jalons M0–M2).",
    "> La v0.6.0 consigne la passation du programme de souveraineté cryptographique (D133) :\n"
    "> axes 2-3-4 accomplis et prouvés sur terrain — la chaîne réelle du coffre a migré\n"
    "> CF1 → CF2 → CF3 les 30–31 octobre 2026 ; la v0.5.2 avait consigné la garde durable de\n"
    "> la phrase de contrôle (D81) ; la v0.5.1 avait ajouté le coffre-fort (D75) et consigné\n"
    "> M3 franchi ; la v0.5.0 demeure la révision du retour du terrain (validation normée,\n"
    "> taxonomie X1–X8, jalons M0–M2).",
)
remplace(
    "- Version : v0.5.2 — phrase de contrôle du coffre-fort sous garde durable dépôt + coffre Drive (D81) ; état des jalons constaté : M0–M3 franchis (balises 0.2.0, 0.3.0, 0.4.0), M4 ouvert (D77)\n"
    "- Date : 28 octobre 2026",
    "- Version : v0.6.0 — souveraineté cryptographique accomplie (D133) : axes 2-3-4 prouvés terrain, chaîne réelle du coffre migrée CF1 → CF2 → CF3, un coffre neuf naît CF3 ; état des jalons constaté : M0–M4 franchis (balises 0.2.0 à 0.5.0), M5 ouvert (D133)\n"
    "- Date : 31 octobre 2026",
)

# ================================================================ 3. § 1.7
ancre_s2 = "## 2. La couche I : format normalisé des spécifications"
assert s.count(ancre_s2) == 1
s17 = """### 1.7 Ce que change la v0.6.0

La révision de génération attendue par le plan : le **programme de souveraineté
cryptographique est accompli et prouvé sur terrain** — décision de passation D133,
arbitrage du développeur. Trois axes livrés (§ 12) : l'**axe 2** (D86) — le coffre CF2 à
clé maîtresse répartie par Shamir, cinq gardes seuil trois, sentinelle à double seuil
puis PORTE D120 ; l'**axe 3** (D87) — le sceau de l'Intention : dix arbres de couche I
signés par la clé Ed25519 hors-ligne du développeur, gardes de build et de patch ;
l'**axe 4** (D121, né du terrain) — le coffre CF3 : la serrure à triple scellement, le
piège sur média séparé, la sentinelle instantanée *par invocation* et le cycle en deux
actes. L'**axe 1** (D85, attestation TEE) demeure une exigence consignée :
l'infrastructure sans racine de confiance matérielle ne peut pas la satisfaire et le
dit. La **chaîne réelle du coffre** a migré sur le terrain du développeur les 30–31
octobre 2026 — CF1 vérifié INTÈGRE, phrase de contrôle changée (D110), CF2 migré (cinq
gardes, seuil 3, trois copies hors-ligne), CF3 migré (époque 1, checksum `0cc89a96`),
verdict à froid VERT deux fois — les cérémonies étant conduites par le maître de
cérémonie graphique (D107–D118) avec le kit Drive tenu identique au miroir par
construction (D130) : le détail vit au § 13. Un **coffre neuf naît désormais CF3** :
`init` direct à l'époque 1 — la chaîne de migration est l'histoire du coffre réel, pas
un rite obligé. Un document complémentaire, le *Livre du Coffre* (même date, même
dépôt), porte la posture opératoire du maître : cérémonies pas à pas, runbook, mode
dégradé. Aucune règle du cœur n'est modifiée ; aucune couche n'est ajoutée à
l'exécution ; la hiérarchie de la fonction objectif est inchangée.

"""
s = s.replace(ancre_s2, s17 + ancre_s2)

# ================================================================ 4. § 12 et § 13 neufs
ancre_s14 = "## 14. Coût en tokens : fragmentation, localisation, budgets"
assert s.count(ancre_s14) == 1
nouveaux = """## 12. Souveraineté cryptographique — le programme v0.6.0

La menace fondatrice est nommée depuis D84 : *l'expropriation* — un tiers (typ.
l'employeur) qui s'empare du binaire, du dépôt, voire des clés du poste. La barrière
juridique (licence BSL 1.1) répond aux tribunaux ; la barrière cryptographique répond à
la machine. Sources normatives de ce chapitre : les spécifications scellées sous le
sceau de l'Intention — `v06/I/README.md` (axe 3), `v06/I/CF2/README.md` (axe 2),
`v06/I/CF3/README.md` (axe 4). En cas de divergence, l'arbre signé fait foi.

| Axe | Décision | Mécanisme livré | État à la passation |
|---|---|---|---|
| 1 · Attestation de non-exfiltration | D85 | quote vérifiable TPM 2.0/SGX du code manipulant le coffre ; refus de déverrouillage sans quote | **exigence consignée** — infrastructure sans TEE |
| 2 · Interrupteur d'homme mort | D86 | clé maîtresse CF2 jamais stockée entière (Shamir, 5 gardes seuil 3) ; sentinelle à double seuil ; destruction des fragments ; PORTE D120 | **livré, prouvé terrain** — chaîne réelle migrée CF1 → CF2 le 31/10/2026 |
| 3 · Filigrane de l'Intention | D87 | chaque arbre de couche I condensé puis signé par la clé Ed25519 *hors-ligne* ; build et chemin de patch refusent une couche I non signée | **livré, prouvé terrain** — dix arbres signés, re-cérémonie réelle D126 |
| 4 · Serrure piégée | D121 | coffre CF3 : clé utilisateur invariable, moitiés serrure/piège fraîches à chaque époque, piège sur média séparé, cycle en deux actes, sentinelle instantanée par invocation | **livré, prouvé terrain** — chaîne réelle migrée CF2 → CF3 le 30–31/10/2026 |

### 12.1 La hiérarchie des gardes — quatre secrets, quatre menaces

| Garde | Menace couverte | Où elle vit |
|---|---|---|
| Phrase de lignée | chiffre les enveloppes de carte — vol du dépôt au repos | en tête du développeur, secours au coffre Drive (D81 : le fichier est la remise) |
| Graine Ed25519 en ligne | signe les cartes — atteste les FAITS (les octets scellés) | dépôt du développeur (jamais confiée au bac à sable, D30) |
| Clé I hors-ligne | signe l'intention — atteste la VOLONTÉ (le droit de faire évoluer) | support physique hors machine ; le dépôt ne voit que la clé publique |
| Clave du coffre (CF2/CF3) | le secret maître — expropriation du poste vivant | CF2 : répartie par Shamir ; CF3 : moitié piège sur média séparé |

### 12.2 CF2 — la clé maîtresse répartie (D86)

Le secret maître **M** (32 octets CSPRNG) n'est *jamais* écrit entier — nulle part,
jamais. Découpage Shamir sur GF(2^8) (polynôme générateur **0x11B**) : pour chacun des
32 octets, un polynôme distinct de degré T−1 à coefficients frais du CSPRNG ; le
fragment j porte les évaluations. Bornes : 2 ≤ T ≤ N ≤ 255, **T = 1 refusé**.
Reconstruction par Lagrange sur T fragments valides, vérifiée contre `verif` (16 o)
avant toute interprétation. **Sous le seuil, la sécurité est informationnelle** : tout
M′ reste compatible — la destruction des fragments est une mort, pas une révocation.
Valeurs terrain : **N = 5, T = 3** ; la relève exige T copies hors-ligne (erratum D121 :
TROIS, pas deux). Format fragment ASCII (transportable sur papier) :

```
TRIADE-CF2-FRAG v1
coffre: <sel HKDF du conteneur, 64 hex - identite STABLE du coffre>
x: <indice, decimal>
seuil: t=3/n=5
fragment: <64 hex - 32 o>
tag: <16 hex - sha256("TRIADE-CF2-frag" || x || fragment) tronque>
```

La sentinelle CF2 surveille la couche C à **double seuil** (processus hors liste
blanche ET lecture de contenu) ; moteur laboratoire inotify + `/proc`, moteur Windows
SACL/4663/ETW exigence consignée. La **PORTE D120** exige une sentinelle vivante pour
déverrouiller ; sans moteur, la porte *avertit nommément* à chaque déverrouillage —
l'ère intermédiaire est dite, pas cachée. Destruction `bruler` : trois passes + PV
nommant le déclencheur ; restauration atomique (toute anomalie et rien n'est écrit).

### 12.3 CF3 — la serrure à triple scellement (D121)

Trois éléments : **K_user** (`Argon2id(phrase, sel_argon)`, 65536 Kio / 3 it / p=1 —
**invariable à travers les époques**) ; **S_serrure** (32 o frais par époque, dans
l'en-tête clair) ; **S_piège** (32 o frais par époque, *exclusivement sur le média
séparé*). L'**époque** (u64, incrémentée à chaque clôture) est l'horloge de la
métamorphose et le témoin anti-retour ; **H_projet** lie la clé de clôture au contenu.
Dérivation : `KEK = HKDF-SHA256(ikm = K_user ‖ S_serrure ‖ S_piège ; salt = sel_hkdf ;
info = "triade-CF3/v1|" ‖ époque ‖ H_projet)` ; le champ **verif** rend l'essai
hors-ligne impossible au voleur de la machine seule (il manque V_piège, publique,
portée par le piège). Conteneur :

```
"TRIADE-CF3" 10 o | version u16 (=1) | époque u64 | H_projet 32 o |
sel_argon 16 o | params (t,m,p : u32×3) | sel_hkdf 32 o | S_serrure 32 o |
nonce 24 o |                       <- fin de l'AAD (168 o)
empreinte 32 o = sha256(chiffretexte) | verif 16 o |
chiffretexte = AEAD(clair, aad, nonce, KEK)
```

Le fichier **piège** (un ASCII par époque, sur le média du sachet) : une clôture
AJOUTE le piège N+1 et ne ronge jamais les pièges passés ; un piège entièrement forgé
se présente comme une phrase erronée — bénin, jamais de destruction. La **sentinelle
instantanée** réalise l'exigence D120 *par invocation au lieu de résidence* : cinq
vérifications ordonnées à tout acte (piège présent → tag → cohérence époques/H_projet
→ phrase → AEAD + étiquette) — le démon résident, usurpable par faux heart-beat, est
mort ; *le piège est le témoin, et il est hors machine*. Le **cycle en deux actes**
borne la session : ouverture → brouillon sous K_session (média débranché, canonique
jamais réécrit) ; clôture → phrase retapée, moitiés fraîches, époque N+1, piège
additif, staging relu à froid, remplacement atomique — une panne auto-nettoie. La
**réponse à la falsification prouvée** (AEAD + étiquette après quatre verts) détruit
côté machine (trois passes + PV) — jamais le média ni les fragments. L'**anti-retour**
repose sur trois témoins d'époque : journal local (effaçable par un admin), **carte
papier du sachet** (checksum à la main, indécevable par logiciel), journal Git
(poussé, hors machine).

### 12.4 Le sceau de l'Intention (D87)

Dix arbres de couche I vivent sous le sceau (les neuf lignées plus `v06/I` — la
spécification du sceau est la première couche qu'il garde). Manifeste canonique (UTF-8,
LF, tri lexicographique déterministe) ; chaque ligne porte le SHA-256 du contenu
**canonique LF** (D115 — la représentation du checkout n'est pas l'intention) ;
l'empreinte d'arbre est le SHA-256 du manifeste entier ; la signature **Ed25519**
(RFC 8032) couvre l'empreinte — 32 octets, imprimables : la cérémonie hors-ligne
manipule quelques lignes hexadécimales, jamais le dépôt. Cérémonie autoportée (stdlib
seule) : `generer`, `signer` (chaque signature vérifiée avant écriture), `verifier`.
Gardes dans la source des chaînes : `build_m4.py` et `build_terrain.py` refusent le
build sur arbre divergé ; tout script qui modifie une couche I appelle la garde en
sortie. `sceau_I.py verifier` : codes nommés 0/10/11/12.

### 12.5 Le coffre neuf naît CF3

La chaîne CF1 → CF2 → CF3 est le chemin *historique* du coffre réel. Un coffre neuf
n'a rien à migrer : `coffre_cf3.py init` le crée sous CF3, époque 1, média du piège
dès le premier jour. La question du terrain — *puisqu'on impose CF3 dès la création,
la sentinelle ne devient-elle pas inutile ?* — reçoit sa réponse normative : la
sentinelle de CF3 n'est pas un composant qu'on peut oublier de lancer, c'est la
serrure elle-même ; l'exigence D120 est réalisée *par construction*. Ce qui demeure
obligatoire : le média du piège (sans S_piège, le déverrouillage est *impossible*) et
la discipline du sachet (§ 13).

### 12.6 Bornes honnêtes consolidées

Attaquant admin pendant un acte (le rayon est borné à UNE époque) ; zéroïsation au
mieux de Python (garantie native au déploiement Windows) ; sentinelle CF2 tuable (le
heart-beat rend la mort visible — CF3 supprime la classe du risque) ; lecture non
attribuée < ~10 ms (journalée, non brûlée) ; CoW/instantanés (l'écrasement logique ne
tue pas les copies physiques) ; carte papier regardée (le verdict à froid est le
filet) ; axe 1 TEE non satisfait (exigence consignée, pas promesse).

## 13. Les cérémonies et le kit du terrain

Les cérémonies de la souveraineté sont des *actes du maître* : le bac à sable ne
touche jamais le conteneur ni les phrases réels (discipline D105). L'outillage les
guide sans les réimplémenter.

### 13.1 La chaîne des cérémonies

| Cérémonie | Gestes | Preuve attendue |
|---|---|---|
| Sceau de l'Intention (D87/D126) | `preparer` ; cérémonie hors-ligne `signer` (clé physique) ; `deposer` (vérifié avant écriture) ; `verifier` | dix arbres VERTS, code 0 ; commit poussé |
| CF1 → CF2 (D106) | phrase (remise D81 AVANT tout) ; `migrer` ; 5 gardes ; T = 3 copies hors-ligne (feuille g3–g5 ou USB) ; relecture ; liste blanche | CF2 `verifier` VERT ; CF1 laissé intact |
| CF2 → CF3 (D121/D127) | MIGRER (conteneur CF2, gardes, *média du piège requis*, phrase deux fois) ; VÉRIFIER (checksum contre la carte) ; DÉTRUIRE (case explicite) | époque 1, checksum 8 hex noté ; verdict à froid VERT (machine froide recommandé) |
| Clôture CF3 (usage courant) | acte I (média débranché) ; session sur le brouillon ; acte II (phrase retapée, époque N+1) | checksum affiché, ligne sur la carte ; journal Git consigné |
| Destruction locale (`bruler`) | commande explicite `--oui-je-comprends` ; trois passes + PV | PV nommé ; fragments et médias jamais touchés |

### 13.2 Le maître de cérémonie graphique et le trio D122

Les cérémonies sont conduites par le maître de cérémonie graphique
(`v06/ceremonie_gui.py` pour le sceau et CF2 ; `v06/migration_cf3_gui.py` pour CF2 →
CF3) : zéro ligne de commande, un fichier, deux profils. Le GUI est un *relais* : il
lance les vérités vivantes et croise code de sortie ET marque de verdict. La phrase
passe par STDIN, jamais affichée, jamais dans un rapport. Chaque module porte le trio
D122 : une GUI, une boîte noire locale horodatée, un bouton « Envoyer le rapport ».
L'habit a appris du terrain : cahier numéroté (D128), pilier droit permanent (D129),
un bouton d'attachement par page (D131), grille — chaque bouton « Parcourir » sur la
ligne de son champ (D132).

### 13.3 Le kit Drive — identité par construction (D130)

Les cérémonies s'arment depuis le dépôt *ou* depuis le kit du dossier `/Cérémonie` du
Drive. Depuis D130, le `v06/` du kit est déployé depuis `git ls-files v06/` — la même
source que le miroir, lue dans le même arbre : **identité octet pour octet par
construction**, `I/` et `sceau-I/` inclus. Le hook post-commit porte le miroir PUIS le
kit dans le même geste. Le `MANIFESTE.txt` du kit porte le commit de référence : un
kit périmé se *lit*, ne se devine pas.

### 13.4 La preuve terrain de la chaîne réelle (30–31 octobre 2026)

CF1 statut VERT ; CF1 verifier INTÈGRE ; phrase changée (D110) ; un premier `migrer`
CF2 refusé nommément (« phrase de contrôle divergente » — la remise D81 n'était pas
encore remplacée : le fail-closed a travaillé, la cérémonie rejouée) ; CF2 né (cinq
gardes, seuil 3, CF1 intact, porte D120 posée en ère sans moteur) ; feuille exportée ;
puis CF2 → CF3 : MIGRER VERT (base re-scellée, schéma identique — rien à traduire ;
piège posé sur le média ; re-lecture à froide verte ; époque 1, checksum
`0cc89a96`, CF2 laissé intact) et VÉRIFIER VERT deux fois, checksum identique. La
destruction du conteneur CF2 (acte 4) est un geste *explicite* du maître, après
recoupement sur machine froide : jamais l'ancien avant le vert du neuf. Observation
honnête consignée : l'empreinte du `coffre_fort.py` mesurée au clone terrain
(`299fd124…`) diverge de celle du dépôt (`8c79263b…`) — à recouper au prochain
`git pull`.

"""
s = s.replace(ancre_s14, nouveaux + ancre_s14)

# ================================================================ 5. MENACES (§ 15.1)
remplace(
    "| **Vol du coffre-fort des phrases** | Voleur, stockage cloud compromis | Conteneur du coffre-fort (D75) ; depuis D81 la phrase de contrôle elle-même vit au coffre Drive et dans le dépôt (arbitrage PERTE > EXPOSITION) | Chiffrement intégral (Argon2id, contexte HKDF dédié, AEAD) ; écriture atomique 0600 ; mitigation première : restreindre le partage par lien du dossier (§ 17.3) | Confidentialité ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — on ne compte plus sur sa confidentialité, la rotation reste le remède |",
    "| **Vol du coffre-fort des phrases** | Voleur, stockage cloud compromis | Conteneur du coffre-fort (D75) ; depuis D81 la phrase de contrôle elle-même vit au coffre Drive et dans le dépôt (arbitrage PERTE > EXPOSITION) | Chiffrement intégral (Argon2id, contexte HKDF dédié, AEAD) ; écriture atomique 0600 ; mitigation première : restreindre le partage par lien du dossier (§ 17.3) | Confidentialité ramenée au contrôle d'accès du dossier ; une phrase commise en git y demeure à vie — on ne compte plus sur sa confidentialité, la rotation reste le remède |\n"
    "| **Expropriation (employeur, tiers)** | D84 | Barrière juridique BSL 1.1 ; barrière cryptographique : clé maîtresse jamais entière (Shamir, axe 2), intention signée par la clé hors-ligne (sceau I, axe 3), serrure piégée à média séparé (axe 4) | Le code volé est inexploitable et ne peut pas évoluer ; l'axe 1 (TEE) reste une exigence consignée |\n"
    "| **Evil maid sur le conteneur ou le média du piège** | D121 | Tag du piège, époques croisées conteneur/piège, AEAD + étiquette, champ `verif` indérivable | Détecté — refus nommé ; la falsification prouvée détruit côté machine, jamais le média |\n"
    "| **Roll-back du couple conteneur + piège** | D121 | Trois témoins d'époque : journal local, carte papier du sachet (à la main), journal Git poussé | Détecté — « RETOUR EN ARRIÈRE » nommé ; recoupement humain à froid |",
)

# ================================================================ 6. JALONS (§ 18)
# M4 : le markdown v0.5.2 le consigne déjà FRANCHI (D104, run 17-H) — inchangé.
remplace(
    "| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives | à venir |",
    "| M5 | Outil complet | interception d'un flux navigateur en VM isolée ; patch à chaud du journal en production ; empreintes par build actives ; programme d'étapes et critères dans `PLAN_MILESTONES.md` | **ouvert** 31/10/2026 (D133 — empreintes par build, interception VM, patch du journal en production) |",
)

# ================================================================ 7. CORRESPONDANCE 19.7
ancre_glossaire = "## 20. Glossaire"
assert s.count(ancre_glossaire) == 1
corr = """### 19.7 Correspondance v0.5.2 → v0.6.0

| Évolution | En v0.5.2 | En v0.6.0 | Statut |
|---|---|---|---|
| Coffre-fort | conteneur TRIADE-CF1 à phrase (D75), garde durable de la phrase (D81) | chaîne complète : CF2 (clé maîtresse Shamir, cinq gardes seuil 3, sentinelle/porte D120) puis CF3 (serrure à triple scellement, piège sur média, cycle en deux actes, sentinelle instantanée par invocation) — le coffre réel a migré par cérémonies (30–31/10/2026) ; un coffre neuf naît CF3 | ajouté (D86, D106, D121, D127, D133) |
| Souveraineté de l'intention | exigence consignée (D87) | le sceau de l'Intention vit : dix arbres signés par la clé Ed25519 hors-ligne, cérémonie autoportée, gardes de build et de patch, re-cérémonie réelle (D126) | ajouté (D87, D105, D126) |
| Cérémonies et kit | non couverts | maître de cérémonie graphique, trio D122, kit Drive identique au miroir par construction (D130), lanceurs Windows/POSIX | ajouté (D107–D132) |
| Attestation TEE (axe 1) | exigence consignée (D85) | inchangée — l'infrastructure sans racine de confiance ne peut pas la satisfaire et le dit | constaté (D133) |
| Menaces | vol du coffre, rollback binaire | lignes nouvelles : expropriation, evil maid, roll-back du couple conteneur + piège | étendu (D133) |
| Jalons | M4 ouvert (D77) | M4 franchi (0.5.0 scellée, terrain.17-D) ; M5 ouvert (D133) | constaté |

Modifications explicitement rejetées (v0.6.0) : supprimer la sentinelle en guise de
simplification — rejeté : l'exigence D120 est réalisée *par invocation* (la sentinelle
instantanée est la serrure) ; ce qui meurt est le démon résident, usurpable. N'imposer
la chaîne de migration aux coffres neufs — rejeté : un coffre neuf naît CF3. Signer la
présente spécification avant passation — reporté : les sources `docs/` sont hors
périmètre du sceau courant (modèle par-version, `v06/I/README.md` § 1). Passer à
v0.6.0 en attendant l'axe 1 — arbitrée par le développeur : la passation se fait avec
l'axe 1 consigné (D133).

"""
s = s.replace(ancre_glossaire, corr + ancre_glossaire)

# ================================================================ 8. JOURNAL DES VERSIONS (§ 21)
ancre_jv = "## 21. Journal des versions"
assert s.count(ancre_jv) == 1
ancre_v040 = "| v0.4.0 | 26 oct. 2026 |"
assert s.count(ancre_v040) == 1
ligne_v060 = "| v0.6.0 | 31 oct. 2026 | Passation du programme de souveraineté cryptographique (D133) : axes 2-3-4 accomplis et prouvés terrain — la chaîne réelle du coffre a migré CF1 → CF2 → CF3 les 30–31/10 (CF2 : Shamir 5/3, sentinelle/porte D120 ; CF3 : serrure piégée, époque 1, checksum `0cc89a96`, verdict à froid VERT ×2) —, axe 1 TEE consigné ; nouveau chapitre 12 (souveraineté : hiérarchie des gardes, CF2, CF3, sceau de l'Intention, coffre neuf né CF3, bornes) et chapitre 13 (cérémonies et kit du terrain) ; menaces étendues (expropriation, evil maid, roll-back du couple conteneur+piège) ; M5 ouvert ; correspondance § 19.7 ; le PDF formel porte annexe empreintes et tableau décisionnel ; le *Livre du Coffre* accompagne (complément opératoire). Aucune règle modifiée, aucune couche ajoutée à l'exécution, hiérarchie inchangée |\n"
s = s.replace(ancre_v040, ligne_v060 + ancre_v040, 1)

# ================================================================ 9. PERSPECTIVE (état de relais)
remplace(
    "La présente version consigne l'état au passage de relais : jalons M0 à M3 franchis sur\n"
    "validations terrain (balises finales 0.2.0, 0.3.0, 0.4.0), coffre-fort des phrases\n"
    "maîtresses opérationnel (D75) et sa phrase de contrôle sous garde durable (D81), jalon\n"
    "M4 (tunnel chiffré) ouvert — couche I écrite-avant-code (D77), étape (b) en cours.",
    "La présente version consigne l'état au passage de relais : jalons M0 à M4 franchis sur\n"
    "validations terrain (balises finales 0.2.0 à 0.5.0), le programme de souveraineté\n"
    "cryptographique accompli (axes 2-3-4, D133) — le coffre réel a migré CF1 → CF2 → CF3\n"
    "les 30–31 octobre 2026 —, jalon M5 (outil complet) ouvert (D133) : empreintes par\n"
    "build, interception en VM isolée, patch à chaud du journal en production.",
)

# ================================================================ 10. GLOSSAIRE (§ 20)
ancre_fin_glossaire = "## 21. Journal des versions"
entrees = """- **Époque** — compteur u64 du coffre CF3, incrémenté à chaque clôture : l'horloge de la métamorphose et le témoin anti-retour.
- **Piège** — la moitié S_piège de la clé CF3, vivant exclusivement sur le média séparé ; sans elle, le déverrouillage est impossible.
- **Sentinelle instantanée** — les cinq vérifications ordonnées qui courent à chaque acte CF3, par invocation : la serrure est le témoin.
- **Sachet** — la pochette physique individuelle : pièges d'époque, copies hors-ligne des fragments, carte papier.
- **Carte du sachet** — fiche où le maître consigne à la main le checksum de chaque clôture : témoin indécevable par logiciel.
- **PORTE D120** — l'exigence de sentinelle vivante au déverrouillage CF2 ; sans moteur de plateforme, avertissement nommé à chaque acte.

"""
s = s.replace(ancre_fin_glossaire, entrees + ancre_fin_glossaire)

P.write_text(s, encoding="utf-8")
print("PROTOCOLE_TRIADE.md passé en v0.6.0 —", len(s.splitlines()), "lignes")
