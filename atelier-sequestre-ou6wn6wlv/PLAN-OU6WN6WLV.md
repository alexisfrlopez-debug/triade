# PLAN PRÉ-ENREGISTRÉ — LA VAGUE 11, L'INSTRUCTION ou6wn6wlv : LA PURGE DES INSTRUCTIONS DE REMISE D81 — LE SÉQUESTRE 5/3 EST LA GARDE ACTIVE

> Pré-enregistré AVANT toute modification des pièces (l'empreinte sha256
> consignée à EMPREINTES-PLANS-VAGUE11.txt, commitée AVANT le premier geste).

## 1. L'ÉTAT DE FAIT (le fondement)

Le séquestre D183 est VÉCU (cérémonie du 19/11 11:17 — la phrase retirée du
dépôt ET de la racine, commit e433d3e, les parts Shamir 5/3 réparties, la
reconstitution prouvée à froid DEUX fois, la rotation vécue et l'ancienne
refusée). Le dépôt est PUBLIC (D220, 19/11 14:05 UTC). D223 acta : D183
ACTIVE, D81 AMENDÉE. Les pièces opératoires (le Livre v1.5, la spec v0.15.6)
contiennent ENCORE des instructions opératoires de remise D81 (« commit,
push » de PHRASE-CONTROLE-COFFRE.txt) — leur exécution aujourd'hui POUSSERAIT
la phrase de contrôle au dépôt public : la purge exigée est une correction de
SÉCURITÉ au rang supérieur de l'ordre lexicographique.

## 2. LES EMPLACEMENTS PURGÉS (la liste de l'instruction, vérifiée ligne à ligne)

- LIVRE v1.5 → v1.6 : §1.4 règle 2 (sec-1.tex, « La remise précède l'usage ») ;
  §8.2 étape 3 (le runbook de rotation, sec-4.tex) ; §8.3 item 2 (la
  restauration post-panne, sec-4.tex) ; le remède « phrase de contrôle
  divergente » §9.2 (sec-5.tex) ; LES TABLES 5 ET 6 (les tables du runbook et
  du mode dégradé portant la colonne « commit + push »).
- SPEC v0.15.6 → v0.15.7 : §14.3 (la clause de garde durable de la phrase) ;
  LA TABLE 16 (le tableau décisionnel de la phrase).
- CHAQUE emplacement remplacé par : LA GARDE ACTIVE — le séquestre Shamir 5/3
  (D183/D223 : cinq parts, seuil trois, les parts inerte sous le seuil, la
  phrase EN AUCUN dépôt) ET LA CÉRÉMONIE DE RECONSTITUTION À FROID (trois
  parts assemblées hors-ligne, la phrase reconstituée JAMAIS écrite au dépôt,
  l'usage transient détruit après le geste) ; LE REFUS NOMMÉ : tout geste qui
  tenterait de réécrire la phrase (ou son fichier) au dépôt est REFUSÉ avec
  son nom — le dépôt est PUBLIC depuis D220, la phrase n'y vit plus.
- Les mentions HISTORIQUES datées (D81, la chronique de la garde) demeurent :
  l'histoire n'est pas réécrite (append-only) — SEULES les instructions
  OPÉRATOIRES actives sont purgées.

## 3. LE LINTER (la garde mécanique)

Ajout au linter v220 : « AUCUNE instruction de remise D81 ACTIVE dans les
pièces opératoires » — le motif (le nom du fichier-remise À PROXIMITÉ d'un
verbe d'écriture de dépôt : commit/push/sauvegarder au dépôt) INTERDIT au
Livre et à la spec ; les mentions historiques datées ADMISES à la table
nommée des contextes historiques. Fail-closed : le motif actif = ROUGE.

## 4. LA VÉRIFICATION APRÈS MODIFICATION (la lettre de l'instruction)

(1) LE GREP EXHAUSTIF « PHRASE-CONTROLE » sur les cinq pièces régénérées :
ZÉRO occurrence prescriptive restante (chaque occurrence restante classée :
historique-datée / séquestre / refus-nommé) ; (2) LE RUNBOOK §8 DÉROULÉ EN
SIMULATION sur clone de test à phrase publique marquée (D105 — la phrase de
test publique, jamais la phrase réelle) : AUCUN chemin ne commit de phrase —
la simulation exécutée par code (le runbook re-écrit en étapes mécaniques,
chaque étape inspectée pour l'écriture de dépôt) ; (3) LE LINTER DE STATUT
D81/D183/D220 re-roulé (l'état : D183 actif, D81 amendée, le dépôt public) ;
(4) la décision d'amendement consignée append-only.
