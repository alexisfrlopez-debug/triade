# PLAN GELÉ — H66O54PJD (la vague 13)
> Le recensement exhaustif des gestes prescriptifs de remise de phrase au Livre
> v1.6 et à la spec v0.15.7, les phrases cassées réparées, les métadonnées v1.7 /
> v0.15.8, le linter étendu, la garde pre-commit/pre-push.
> Gelé AVANT toute modification ; append-only ; les pièces historiques demeurent.

## Le mandat
La garde active est le séquestre Shamir 5/3 (D183/D223) : reconstitution à froid de
TROIS parts, la phrase en AUCUN dépôt. Cinq gestes :

1. **Le recensement EXHAUSTIF** des gestes prescriptifs de remise de phrase au Livre
   v1.6 et à la spec v0.15.7, TOUTE formulation : « fichier-remise », « garde
   durable », « posez la phrase… commit, push », « vérifiez le fichier-remise »,
   glossaire « relève », Table 16 git, §12.5 CF1 « garde durable », §14.3
   « Contrepartie consignée » au présent. Chaque occurrence corrigée vers LA GARDE
   ACTIVE (reconstitution à froid de trois parts, refus nommé D223) ou bornée en
   histoire datée explicitement étiquetée. Les cibles nommées au recensement préalable :
   spec tex sec-cf.tex:373-374 (Tableau 14 CF1), sec-cf.tex:403-406 (§12.5), sec-d.tex:82-84
   (§14.3, le splice), sec-a.tex:328-340 (énoncé périmé « DEMEURE à la garde D81 ») ;
   docs/PROTOCOLE_TRIADE.md l.1355, 1374, 1398, 1710-1723 (§17.3), 2113 (glossaire) ;
   docs/FORMAT_CARTE.md l.310-315, 355-366.

2. **Les phrases cassées réparées par réécriture complète des paragraphes** (jamais
   par remplacement de sous-chaînes) : Livre §7.5 (sec-4.tex:181-187, le splice
   « tant que… depuis que… tant qu'elle ne l'est pas… ») et §8.2 item 7
   (sec-4.tex:283-286, « tant qu'elle est VÉCUE »). Le §2.3 vérifié refermé (D245).

3. **Les métadonnées alignées** : Livre v1.7 / spec v0.15.8 partout (couverture
   cover.html, avant-propos sec-1.tex:8, §10.1 et Table 12 sec-5.tex:139-146 —
   l'annexe A de la spécification v0.15.8, sommaire des décisions sec-5.tex:253
   étendu à la plage réelle D75–D25x, fancyhead/pdftitle/merge) ; la plage
   décisionnelle réelle incluant D183/D219/D220/D223/D236 ; **D236 PORTÉ à l'annexe B
   de la spec** (sec-d.tex:1551, plage étendue).

4. **Le linter documentaire étendu** : la règle « aucun verbe d'écriture de dépôt à
   proximité d'un référent de phrase, hors table historique datée » au vocabulaire
   ÉLARGI (fichier-remise, garde durable, phrase de contrôle, remise) ; le lint des
   CHAÎNES DE VERSION (couvertures/avant-propos/tables : Livre == v1.7, spec ==
   v0.15.8, les constantes attendues) ; le contrôle négatif vécu (réinjection d'une
   instruction D81 synthétique → refus nommé).

5. **La garde pre-commit/pre-push ÉTENDUE** : détection par EMPREINTES sha256 des
   secrets connus (la liste dressée : jetons GitHub ghp_…, secrets OAuth GOCSPX-…,
   clés privées PEM, la phrase-marqueur D105) + ENTROPIE (les règles de
   scan_secrets.py : assignations ≥ 28 car. à entropie Shannon ≥ 3,8), PAS seulement
   le nom de fichier ; les hooks committés au dépôt (git-hooks/pre-commit,
   git-hooks/pre-push), installés au .git/hooks, l'amendement consigné append-only.

## Les gestes
1. Ce plan gelé AVANT toute modification.
2. Atelier atelier-purge-v13-h66o54pjd/ : le recensement par code (grep multi-motifs
   sur les sources, chaque occurrence classée PRESCRIPTIF/HISTORIQUE-DATÉ), les
   patchers ancrés (REFUS si une ancre manque), les paragraphes réécrits, les
   contrôles négatifs, les rapports.
3. Les PDF reconstruits (tectonic + weasyprint) : Livre v1.7, spec v0.15.8 — les
   empreintes consignées ; le grep multi-motifs sur les PDF régénérés : zéro
   occurrence prescriptive, chaque occurrence restante classée HISTORIQUE-DATÉE.

## La vérification après modifications
- relecture intégrale des paragraphes réparés (pas de grep seul) : zéro phrase
  tronquée, zéro splice ancien/nouveau ;
- la simulation du runbook sur clone à phrase publique D105 : les huit étapes sans
  écriture de dépôt, le geste-piège refusé au premier nom pour CHAQUE variante de
  formulation ;
- le linter étendu vert sur les cinq pièces v0.23.0 + les deux PDF (Livre, spec) ;
  la version au PDF == v1.7/v0.15.8 partout ;
- la garde pre-commit : le secret connu réinjecté à la copie → REFUS nommé au
  commit ; le faux positif vérifié nul sur l'état courant ;
- sceau 14/14 avant et après ; append-only.

## Les refus
Aucun coffre réel ni phrase réelle ; les récits historiques annotés, jamais effacés ;
le patcher ancré refuse si une ancre manque ; aucun secret réel dans les tests.
