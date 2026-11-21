# PLAN GELÉ — 0UUG27TEO (la vague 12)
> La purge des résidus prescriptifs de la garde D81 que le grep « PHRASE-CONTROLE » ne couvre pas — Livre du Coffre v1.6 et Protocole TRIADE v0.15.7.
> Gelé AVANT toute modification. Toute correction suit ce plan ; tout écart est nommé au rapport.

## Le mandat
Les pièces Livre_du_Coffre v1.6 et Protocole_TRIADE v0.15.7 contiennent des résidus
prescriptifs de la garde D81 que le grep « PHRASE-CONTROLE » ne couvre pas. Localisation
exacte des résidus :
- Livre Annexe C, dernière FAQ : « posez la phrase courante dans le fichier-remise, commit,
  push — puis rejouez » ;
- Livre §7.3 étape 1 : « Le fichier-remise D81 est à jour … le fichier AVANT tout » ;
- Livre §9.2 ligne « phrase ERRONÉE » : « vérifiez le fichier-remise » ;
- Livre Tableau 1 colonne CF1 « garde vivante » et glossaire B entrée « relève » ;
- Spec Tableau 16 (§13.6) ligne « Dépôt git » : « et la phrase de contrôle (D81 : le
  fichier est la remise…) » ;
- Spec Tableau 13 (§12.3) ligne « Relève si la machine brûle » colonne CF1 ;
- Spec §14.3 paragraphe « Contrepartie consignée » (la phrase vit sur le Drive partagé
  par lien).

## Les gestes (l'ordre)
1. Geler ce plan (empreinte consignée à EMPREINTES-PLANS-VAGUE12.txt) AVANT toute modification.
2. Remplacer chaque résidu par la garde active D223 (séquestre 5/3, reconstitution à froid
   de TROIS parts, phrase en AUCUN dépôt, refus nommé de la réécriture), par remplacements
   ancrés échouant si une ancre manque.
3. Les contextes historiques datés (récit D81 borné, table d'évolutions v0.5.2, chronologie
   du terrain) DEMEURENT intacts et annotés « amendé D223 ».
4. Corriger au passage : couverture du Livre « VERSION 1.3 » → v1.6, avant-propos
   « v0.15.2 » → v0.15.7, phrase tronquée du §2.3, ordre chronologique du Tableau 13.
5. Étendre le linter : motif sémantique élargi (fichier-remise, remise D81, phrase de
   contrôle à proximité d'un verbe d'écriture de dépôt ou d'un impératif prescriptif),
   whitelist explicite des contextes historiques datés, contrôle négatif planté (une phrase
   prescriptive synthétique réintroduite dans une copie doit être REFUSÉE au premier nom).
6. Consigner l'erratum de la purge en décision append-only D2xx : la revendication « zéro
   prescriptive » de ou6wn6wlv était exacte au périmètre du grep, inexacte au périmètre
   sémantique ; la cause est nommée (le motif du linter dérivait du nom de fichier, pas de
   l'intention de la garde).
7. Reconstruire les deux PDF (tectonic), consigner les nouvelles empreintes.

## La vérification après modifications
1. grep sémantique élargi sur les deux pièces régénérées → zéro occurrence prescriptive,
   chaque occurrence restante classée HISTORIQUE-DATÉE à la table nommée ;
2. rejouer simuler_runbook.py sur clone à phrase publique D105 → huit étapes sans écriture,
   geste piège refusé au premier nom ;
3. re-scan intégral des blobs git (rev-list --all | cat-file --batch) → zéro fuite ;
4. linter re-roulé sur les cinq pièces avec son contrôle négatif planté → REFUS nommé ;
5. sceau_I verifier → 14/14 arbres VERTS avant et après, empreintes identiques ;
6. diff des PDF contre l'édition précédente : seules les zones ancrées ont bougé.

Tout écart = refus nommé, jamais de correction silencieuse.
