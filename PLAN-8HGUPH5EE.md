# PLAN GELÉ — 8HGUPH5EE (la vague 15)
> L'atelier du moteur d'oracles : livrer le moteur natif d'exécution des oracles
> (le gap nommé DEUX fois), les oracles portant 81 % du chemin critique —
> jumeau Unicorn de référence, mémo content-addressed, audit vivant 1-sur-10 chaîné.
> Gelé AVANT toute exécution ; l'empreinte du moteur précède le premier run.

## Le mandat
(1) **LE MOTEUR NATIF** : compiler l'oracle en natif avec JUMEAU UNICORN de
référence — la console du moteur natif ligne-identique à celle du jumeau pour
tout vecteur (divergence zéro exigée).
(2) **LA MÉMO CONTENT-ADDRESSED** : clé = sha256 de TOUT ce qui détermine le
résultat (oracle, vecteurs, configuration moteur, graine) — un octet changé =
MISS (le rebuild court vivant), jamais une miss maquillée en exécution.
(3) **L'AUDIT VIVANT 1-SUR-10 CHAÎNÉ** : la re-exécution complète sous Unicorn,
le relevé confronté CHAMP PAR CHAMP au produit caché — tout écart = refus nommé.
(4) **LA COMPOSITION** avec la mémo de régime (−89,4 % H-CGP4) et la
cristallisation incrémentale (−54 %) ; la mesure avant/après n=5, horloge
monotone, liste de commandes fixe.
(5) **LE GATE** : un shim délibérément muté du moteur natif ATTRAPÉ à la
première ligne — la porte divise les moteurs honnêtes des faux.

## Les gestes
1. Le plan gelé ; le moteur compilé (versions consignées) ; le jumeau Unicorn.
2. La différentielle natif/jumeau sur les vecteurs du régime (consoles
   ligne-identiques, hors horodatages nommés).
3. La mémo content-addressed + le contrôle négatif (un octet changé = miss).
4. L'audit 1-sur-10 chaîné (le compteur signé déclenche, la confrontation champ
   par champ).
5. La mesure avant/après n=5 composée avec H-CGP4 et la cristallisation.
6. Le shim muté (le contrôle négatif vécu).

## La vérification après modifications
Les consoles d'oracle capturées ligne-identiques aux originales ; divergence
zéro sur l'échantillon d'audit ; le shim muté attrapé à la première ligne ;
empreintes scellées intactes avant/après ; AUCUN vecteur réduit ni graine
retirée ; sceau 14/14 ; entrée append-only.

## Les refus
Jamais une miss maquillée en exécution ; jamais l'audit contourné ; jamais un
vecteur réduit ; jamais le jumeau retiré (il est la référence).
