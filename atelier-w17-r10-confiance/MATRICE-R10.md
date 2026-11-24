# MATRICE R10 — RACINE DE CONFIANCE AU CHARGEMENT ET ANTI-ROLLBACK

> Atelier W17R3R10 de la vague 17 (24/11/2026) — exécution du plan gelé au commit
> `8853bcf` (empreinte `aad901fed767776d3ee2a6d88a3fac8f8a2acdffc43362160523b06aa9222813`).
> Chaque ligne a été établie sur les pièces du dépôt et les manuels primaires ; les
> lignes qui dépendent d'un mécanisme absent du bac portent le statut **EN ATTENTE**,
> jamais un vert de complaisance. Aucun mécanisme n'est activé sur le coffre réel.

## 1. Ce que R10 énonce, et ce qu'il ne dit pas

R10 (spec § 6, renforcée par D20) exige qu'au lancement — **avant toute entrée dans
le chemin d'exécution** — l'artefact vérifie : (a) les checksums de ses blocs scellés,
(b) la signature du manifeste de build couvrant le code et les données embarquées,
(c) la monotonie de version contre le plancher accepté, (d) la conformité minimale de
l'environnement au profil ; tout écart est un arrêt propre, sans chemin dégradé.

R10 est une règle **locale et hors ligne**. Il n'énonce ni qui détient la clé de
signature, ni où vit le plancher, ni ce qui empêche un administrateur de remplacer
l'ensemble binaire + clé + état. Ces trois questions sont l'objet de la présente
matrice : **la garantie de R10 vaut exactement ce que vaut son ancre**, et par profil
cette ancre n'est pas la même.

## 2. Les trois propriétés, jamais confondues

| Propriété | Question à laquelle elle répond | Mécanisme R10 | Ce qu'elle ne dit pas |
|---|---|---|---|
| **Intégrité** | Les octets sont-ils ceux qui ont été scellés ? | checksums des blocs + empreinte du manifeste recomposée | rien sur l'identité du signataire |
| **Authenticité** | Le manifeste a-t-il été signé par la clé autorisée ? | signature Ed25519 vérifiée sous la clé épinglée | rien sur la fraîcheur de la version |
| **Fraîcheur** | Cette version est-elle la plus récente admise, non révoquée ? | plancher de version + époque de l'état local | rien sur l'intégrité des octets |

Une carte dont la signature est valide peut porter une version ancienne ; une version
récente peut être altérée ; un état restauré peut être parfaitement intègre et
authentique. **Traiter ces trois propriétés comme une seule serait l'erreur de
raisonnement que ce document ferme** (hypothèse H1 du plan).

## 3. Ce qui est vérifié au chargement, par profil

| Élément vérifié | `x86-64-win11-pe` | `x86-64-linux-elf64` | `riscv64-linux-elf64` |
|---|---|---|---|
| Binaire livré | checksums des blocs scellés (porte R10 du modèle m5/m4) | idem (image ELF64) | idem (image ELF64) |
| Code du vérificateur | couvert par la signature du manifeste ; son **exécution** est ancrée par Authenticode/OS **si** la politique l'exige | couvert par le manifeste ; ancrage par IMA appraisal **si** configuré | couvert par le manifeste ; ancrage par la chaîne de boot signée **si** présente |
| Manifeste de build | Ed25519, clé épinglée locale | idem | idem |
| Données embarquées | empreintes dans le manifeste (R10 b) | idem | idem |
| Clé publique | fichier local root-owned / magasin protégé ; **jamais dans l'artefact modifiable** | idem (0644 root:root, hors arborescence inscriptible) | idem |
| Plancher de version | champ `plancher` signé + état local | idem | idem |
| Stockage de l'état | fichier local (époque, version) ; journal local effaçable | idem | idem |
| Réseau | **aucun** appel au chargement — l'absence réseau est l'état normal | idem | idem |

## 4. La matrice menace → mécanisme → ancre → preuve → limite

| # | Menace | Mécanisme | Ancre d'authenticité réelle, et son propriétaire | Preuve au banc | Limite nommée |
|---|---|---|---|---|---|
| M1 | Corruption accidentelle (bit rot, panne) | checksums + AEAD + manifeste | la clé publique épinglée (développeur) | `controles_fail_closed.py` : corps muté → SIGNATURE INVALIDE (11/11) | une corruption qui touche aussi la clé et l'état local n'est pas détectée |
| M2 | Falsification locale opportuniste | signature du manifeste | clé privée hors ligne, clé publique root-owned | signature d'une autre clé → SIGNATURE INVALIDE | un attaquant **administrateur** remplace binaire, clé et état ensemble : R10 seul ne le voit pas |
| M3 | Artefact empoisonné en amont (supply chain) | signature du manifeste | clé de publication ; sur Windows Authenticode, sur Linux IMA (clé noyau) **si** déployés | manifeste divergent → MANIFESTE DIVERGENT | la compromission de la clé de publication elle-même exige rotation + révocation (§ 6) |
| M4 | Rejeu d'une version ancienne vulnérable (artefact seul) | plancher signé + monotonie | plancher publié par le développeur | version 0.6.0 sous plancher 0.7.0 → VERSION SOUS LE PLANCHER | le plancher vit dans un état local : un admin peut l'abaisser — voir M5 |
| M5 | Restauration d'un couple binaire + état ancien (snapshot, VM) | détection locale de l'époque | **aucune ancre locale ne suffit** : l'état recule avec le binaire | état 12 / carte époque 9 → RETOUR EN ARRIERE | la restauration **cohérente** du couple échappe à R10 ; seule une ancre externe la voit (§ 5) |
| M6 | Attaquant administrateur local pendant un acte | R10 ne le couvre pas | hors périmètre R10 ; relève de la sentinelle et du coffre (D120/D242) | non revendiqué | le modèle de menace borne le rayon à une époque (§ 12.6) |
| M7 | Machine hors ligne | ancres locales uniquement ; `--reseau` refusé | clé publique locale | tentative réseau → RESEAU AU CHARGEMENT | aucune révocation consultable hors ligne : elle voyage avec la version suivante |
| M8 | Environnement non conforme au profil | conformité minimale (R10 d) | le système d'exploitation | non couvert par le banc (matériel) | **EN ATTENTE** : exécution au métal nu requise |
| M9 | Élévation par TEE / secure boot | non activé | aucune | non revendiqué | **EN ATTENTE** : exigence consignée, jamais simulée (D242, axe 1) |

## 5. Le rollback face aux quatre scénarios

| Scénario | Ce que voit R10 | Ce qui reste nécessaire |
|---|---|---|
| Binaire ancien seul, état courant | refus (plancher et/ou époque) | rien |
| **Binaire + état restaurés ensemble** | rien — le couple est cohérent | un témoin **hors machine** : carte papier du sachet (à la main), journal Git poussé, ancre de transparence publique du témoin d'époque (D242) |
| Administrateur local baissant le plancher | rien si la modification est cohérente | les mêmes témoins externes + la sentinelle (SACL/4663 ou ETW) sur le poste réel — **EN ATTENTE** |
| Panne hors ligne au milieu d'une clôture | l'état doit être atomique (tmp + rename) | le cycle en deux actes du coffre, qui borne la session |

**Les trois propriétés distinctes que le plan exige de séparer :**
1. **le plancher R10** protège l'**artefact** (version minimale acceptée) ;
2. **l'époque CF3** protège la **clé du coffre** (métamorphose de KEK, anti-retour du conteneur) ;
3. **les témoins d'époque du coffre** (journal local, carte papier, journal Git, ancre publique)
   protègent la **fraîcheur de l'état**.
Aucune ne remplace l'autre : un plancher R10 élevé ne dit rien de la fraîcheur du coffre,
et une époque CF3 à jour ne dit rien de la version du binaire.

## 6. Rotation, révocation, perte de clé

- **Rotation** : la nouvelle clé publique est distribuée hors bande (poste du développeur,
  jamais dans l'artefact qu'elle authentifie) ; le manifeste porte un identifiant de clé
  (`kid`) et l'époque de publication. Le vérificateur refuse toute clé inconnue ou retirée
  — `CLE D'ANCRE ABSENTE` au banc.
- **Révocation** : un plancher d'époque de clé est publié avec la version qui révoque ;
  une clé révoquée est refusée même si sa signature est valide. La liste de révocation
  voyage avec la version (hors ligne oblige) ; aucune consultation réseau au chargement.
- **Perte de la clé** : la clé de succession signe la nouvelle clé (chaîne de confiance
  locale) ; à défaut, la réémission exige un acte explicite du maître et une nouvelle
  distribution hors bande. **Aucune récupération automatique** : une clé absente est un
  refus nommé, jamais un repli silencieux.
- **Erreurs fail-closed** : carte absente, clé absente, signature invalide, manifeste
  divergent, version sous plancher, état absent non déclaré, retour en arrière, tentative
  réseau — huit refus nommés, tous rendus au banc (§ 7).

## 7. Preuves au banc (ce qui est réellement exécuté)

`atelier-w17-r10-confiance/controles_fail_closed.py` — **11/11 contrôles rendus** :
nominal OUVERT ; carte absente ; signature d'une autre clé ; corps muté après signature ;
manifeste divergent signé ; version sous le plancher ; état restauré (époque) ; état absent
sans déclaration ; première ouverture déclarée admise ; clé d'ancre absente ; tentative
réseau au chargement. Le banc modélise la **logique** de la porte, pas l'ancre
d'exploitation : il ne remplace ni Authenticode, ni IMA, ni secure boot, ni le métal.

## 8. Statut, par profil effectivement supporté

| Profil | Statut R10 | Ce qui manque |
|---|---|---|
| `x86-64-win11-pe` | spécifié et éprouvé au banc | Authenticode + sentinelle SACL/4663 sur le poste réel — **EN ATTENTE** |
| `x86-64-linux-elf64` | spécifié et éprouvé au banc | IMA appraisal ou signature de paquet sur le poste réel — **EN ATTENTE** |
| `riscv64-linux-elf64` | spécifié ; exécution QEMU seulement | chaîne de boot signée et exécution silicium — **EN ATTENTE** |

**Conclusion bornée** : R10 garantit l'intégrité et l'authenticité d'un artefact local
contre un adversaire non-administrateur, et la fraîcheur contre le rejeu du seul artefact.
Il **ne garantit pas** la fraîcheur d'un couple binaire + état restauré ensemble, ni la
résistance à un administrateur local, ni l'absence d'un binaire signé par une clé
compromise. Ces trois limites sont nommées, non contournées.
