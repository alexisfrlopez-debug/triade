## PROMPT 05 — Clôture, versionnement, release et synchronisation des trois bords

Cette consigne autorise la préparation et la publication d’une release uniquement si les ateliers ont produit des changements pertinents, si leurs plans et commits sont présents et si les contrôles passent. Elle autorise le PUBLISH Zenodo de la version nouvelle après vérification complète. Elle n’autorise ni la divulgation de secrets ni la modification/destruction d’anciens records.

## A. Pré-vol et versionnement

- Repars de l’état vivant des dépôts Git, du coffre Drive et des records Zenodo. Résous d’abord les divergences : la reprise consultée indique une release corrective v0.23.4 et un corpus v2.1, tandis que ses paragraphes permanents citent encore v0.23.3, v2 et l’ancienne règle D81. Vérifie les DOI/records et les octets avant d’établir la version de départ.

- Décide si les changements justifient une nouvelle édition, une release corrective ou aucune publication. Ne réécris jamais une balise/record immuable ; ne mint pas de version vide ou simplement renommée.

- Utilise le patron de génération, linter, assemblage, livraison et vérification le plus récent présent dans le dépôt. Ne suppose pas que v232/v233 ou un numéro de script est encore le patron courant.

- Vérifie le sceau-I avant génération et après ; utilise les arbres et attentes du manifeste vivant. Vérifie les cinq pièces et les empreintes enregistrées. Archive le rapport, le manifeste et les résultats des contrôles.

## B. Zenodo

- Garde séparés le concept du protocole, le kit développeur et le corpus. Ne mets à jour un concept que si son contenu a changé.

- Pour une nouvelle version, suis le patron existant : new version, bucket, dépôt, métadonnées, comparaison byte-byte des empreintes, puis PUBLISH. Ne remplace pas une version publiée et ne réutilise pas un DOI de version.

- Avant PUBLISH, confirme que les fichiers et métadonnées correspondent exactement à la release, que les sommes sont recoupées par re-téléchargement et que le DOI du nouveau record résout. Si un contrôle échoue, laisse la version en brouillon et explique le blocage.

- Les archives du kit v1 et du corpus v1 restent immuables si leur contenu n’a pas changé. Ne mint pas de version pour ces œuvres par simple synchronisation.

## C. Drive et GitHub

- Livre au coffre Drive les fichiers demandés aux emplacements racine, /test, /livrables et ARCHIVE selon les patrons courants. Re-télécharge chaque fichier et compare les octets/empreintes.

- Fais les gestes d’archivage Drive en deux étapes séparées : retirer une instruction exécutée de /instructions, puis l’ajouter au lot ARCHIVE. Ne déplace pas une instruction non exécutée ; ne déclare pas /instructions vide si des tâches restent pendantes.

- Synchronise le miroir Drive et le bundle d’historique, pousse GitHub, puis vérifie les trois bords. Les têtes/références et l’univers d’objets doivent correspondre au commit consigné. Si GitHub pousse avant Drive, recale le miroir sur la tête réellement poussée.

- Respecte les secrets : ne les lis pas dans un rapport, ne les committe pas, ne les copie pas dans les packs, manifests ou sorties de commandes.

## D. Clôture

Mets à jour worklog.md, OU-TROUVER-LES-LIVRABLES.md et REPRISE_PROJET.md avec un état unique, daté et recoupé. Les mentions d’anciennes versions doivent être étiquetées historiques ; aucune consigne active ne doit contredire D223. Ajoute les rapports de release, les empreintes et l’état de chaque bord. Archive les instructions exécutées selon la règle deux-étapes. Fais le commit final, pousse GitHub et synchronise le miroir Drive.

Rends un rapport final factuel : commits, version, DOI de concept et de version, records, fichiers et empreintes, état des trois bords, contrôles réalisés, instructions restantes, blocages matériels ou du maître. N’annonce pas « complet » si une étape autorisée demeure en attente.

