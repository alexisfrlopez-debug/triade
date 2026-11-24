# PROMPT 03 — Clarifier la racine de confiance et l’anti-rollback R10

Exécute le plan gelé sur la confiance au chargement et la fraîcheur des versions. Le résultat doit préciser ce que R10 garantit contre chaque classe d’attaquant, sans transformer une vérification locale en garantie universelle.

1. Cartographie les éléments vérifiés au chargement : binaire, code du vérificateur, manifeste, données embarquées, clé publique, plancher de version et stockage de l’état.
2. Pour chaque profil, identifie l’ancre d’authenticité réelle et son propriétaire : signature de code/OS, clé publique protégée, secure boot, matériel, ou autre mécanisme déjà spécifié. Si l’ancre est modifiable avec l’artefact, indique cette limite explicitement.
3. Distingue intégrité (octets inchangés), authenticité (signataire autorisé) et fraîcheur (version non révoquée/non ancienne). Documente la rotation et révocation des clés, le remplacement d’une clé perdue et les erreurs fail-closed.
4. Analyse le rollback face à la restauration d’un ancien couple binaire+état, à un administrateur local, aux snapshots et à une panne hors ligne. Sépare le plancher R10 de l’époque CF3 et des témoins d’époque du coffre ; ne les traite pas comme une seule propriété.
5. Mets à jour les hypothèses A1… du modèle formel et les preuves/lemmas uniquement si les outils disponibles les permettent. Les preuves de modèle restent étiquetées « prouvées sous hypothèses » ; les exécutions matérielles absentes restent « en attente ».
6. Donne une matrice menace → mécanisme → ancre → preuve → limite, avec les profils effectivement supportés.

Mets à jour la spécification, le modèle et les contrôles selon le plan, en conservant le verbatim historique. N’active pas de TEE/FIDO2 ni de nouveau mécanisme sur le coffre réel sans geste explicite du maître. Vérifie le sceau-I avant/après et committe cet atelier seul. Pas de release dans ce prompt.
