# PLAN GELÉ — W17R3R10 (racine de confiance au chargement et anti-rollback)

> Instruction source : `/instructions/03_R10_CONFIANCE.md`. Dépend du gel (W17R0GEL).
> Objet : préciser ce que R10 garantit contre chaque classe d'attaquant, sans
> transformer une vérification locale en garantie universelle.

## Périmètre
1. Cartographier ce qui est vérifié au chargement, par profil : binaire, code du
   vérificateur, manifeste, données embarquées, clé publique, plancher de version R10,
   stockage de l'état.
2. Identifier, par profil, l'**ancre d'authenticité réelle** et son propriétaire :
   signature de code / OS, clé publique protégée, secure boot, matériel, ou autre
   mécanisme déjà spécifié. Si l'ancre est modifiable avec l'artefact, l'écrire.
3. Distinguer systématiquement **intégrité** (octets inchangés), **authenticité**
   (signataire autorisé) et **fraîcheur** (version non révoquée, non ancienne).
   Documenter rotation et révocation des clés, remplacement d'une clé perdue, erreurs
   fail-closed.
4. Analyser le rollback face à : restauration d'un ancien couple binaire+état,
   administrateur local, snapshots, panne hors ligne. Séparer le plancher R10, l'époque
   CF3 et les témoins d'époque du coffre — trois propriétés distinctes.
5. Mettre à jour les hypothèses A1… du modèle formel et les lemmes **uniquement** si les
   outils disponibles les rejouent ; sinon statut inchangé et nommé.
6. Rendre la matrice menace → mécanisme → ancre → preuve → limite, par profil supporté.

## Fichiers touchés
- `docs/FORMAT_CARTE.md` (structure de la carte, plancher, stockage d'état).
- `docs/PROTOCOLE_TRIADE.md` (section chargement / vérification).
- `docs/DECISIONS.md` : nouvelle décision (D25x) — la garantie R10 bornée, ancre par
  profil, alternatives rejetées.
- Le modèle formel (CF3, hypothèses A1…) : annotations de statut seulement si rejouées.
- `atelier-w17-r10-confiance/` : matrice, rapport, contrôles fail-closed au banc.

## Hypothèses
- H1 : les témoins d'époque et le plancher R10 ne protègent pas la même chose ; les
  traiter comme une seule propriété serait une erreur de raisonnement à nommer.
- H2 : aucune exécution matérielle (TEE, FIDO2, secure boot) n'est disponible ici →
  statut « en attente », aucun mécanisme activé sur le coffre réel.
- H3 : `tamarin-prover` / `proverif` / `z3` sont absents du bac → aucune preuve nouvelle
  n'est revendiquée ; seules les preuves déjà consignées sont citées avec leur statut.

## Critères d'acceptation
- Matrice complète, une ligne par menace × profil, chaque ligne nommant l'ancre et sa
  LIMITE.
- « Prouvé sous hypothèses » maintenu partout où les outils n'ont pas rejoué ; aucune
  exécution matérielle annoncée.
- Rotation/révocation et erreurs fail-closed documentées, y compris la perte de clé.
- Sceau-I avant/après ; un commit seul ; verbatim historique conservé.

## Risques
- R1 : présenter une vérification locale comme une garantie universelle.
- R2 : activer TEE/FIDO2 (interdit sans geste explicite du maître).
- R3 : confondre intégrité, authenticité et fraîcheur.
- R4 : annoter un lemme comme prouvé alors que l'outil n'a pas tourné.

## Tests et preuves requis
- Revue croisée des passages (chargement, carte, Livre) : une seule règle énoncée.
- Contrôles fail-closed au banc : carte absente, signature invalide, version sous le
  plancher, état restauré ancien → refus attendus, tous consignés.
- `python3 v06/sceau_I.py verifier`.

## Dépendances
Gel (W17R0GEL). W17R2PAT pour la cohérence de la publication atomique (la carte et le
patch à chaud se rencontrent sur les permissions de page et l'ordre mémoire).
