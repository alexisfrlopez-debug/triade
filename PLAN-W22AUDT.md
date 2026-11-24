# PLAN GELÉ — W22AUDT (quatre améliorations issues de l'audit + règle permanente)

> Commande du maître du 24/11/2026 : « go pour tes nouvelles propositions » + règle permanente
> (audit après chaque vague, améliorations vers sécurité/optimisation/performance/tokens).
> Append-only ; aucune valeur mesurée modifiée ; aucun artefact scellé touché.

## Périmètre
(a) COULOIR RECHERCHE — cible RELATIVE : la cible absolue ≤ 561 cycles est déjà tenue par
    glibc, elle ne discrimine plus. La cible devient ≤ 0,9 × memchr ; memchr est la
    référence ; si le balayage écrit est dominé, il est REFUSÉ NOM MÉ (COULOIR-DOMINE) et
    aucun gain n'est revendiqué.
(b) CONTEXTES D'EXÉCUTION DES 50 BLOCS : fournir un contexte standard (IAT bouchonnée,
    fenêtre de registres, pile gardée) et rejouer les 320 vecteurs ; compter OK/FAULT par
    bloc et consigner le delta. Aucun résultat inventé : un bloc qui faute reste FAULT.
(c) C17 FAULT-COUNT : le compte des vecteurs et des FAULT est publié dans une pièce et
    RECOMPOSÉ depuis les fichiers de vecteurs ; tout écart = refus.
(d) PÉREMPTION DU REGISTRE : chaque entrée porte « inchangée depuis N vagues » ; une entrée
    gelée > 2 vagues sans justification est REFUSÉE par C16 (ou justifiée par écrit).

## Contraintes
- Aucune valeur mesurée modifiée ; les nouveaux chiffres sont des mesures du bac, nommées.
- Les plans sont gelés et committés avant toute donnée.

## Critères d'acceptation
- (a) mesure relative consignée ; refus nommé si dominé ; pré-enregistrement avant mesure.
- (b) delta OK/FAULT publié par bloc, recomposable depuis les fichiers.
- (c) C17 verte, une mutation refusée nommément.
- (d) C16 refuse une entrée gelée non justifiée (mutation) ; le registre est à jour.
- Porte V1..V7 + L1..L17 : zéro rouge ; témoin ré-ancré automatiquement.
