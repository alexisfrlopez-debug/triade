# PLAN GELÉ — W28TERRAIN (la vague terrain groupée pré-enregistrée : les dix attentes d'un seul geste — sécurité)

> Vague 28, prompt 5 (dépôt du 26/11/2026). UN SEUL plan pré-enregistré (sha256 consigné
> avant tout run), l'agrégateur fail-closed : un run manquant REFUSE le verdict de la vague.
> Les statuts se dérivent des runs (PREUVES-STATUTS.json), jamais de la frappe ; INCOMPLETE
> demeure INCOMPLETE tant que la preuve n'est pas close. Aucun chiffre fabriqué.

## Geste
1. LE PLAN GELÉ (le présent fichier, sha256 consigné au commit d'abord) : l'ordre des runs,
   les machines (empreintes CPU, état de fréquence — goupillé ou caveat nommé), les budgets,
   l'attendu par kit, les critères de verdict, ET la randomisation stratifiée pour H7 (la
   campagne aux 28 unités — l'effet d'ordre, le tirage T-premier 4/4 et l'événement 1/16
   consignés) ; l'investigation des pics dudect N=200 (12,39/5,19) pré-enregistrée : les
   causes candidates nommées AVANT les données, aucune élue d'avance.
2. L'ORDRE DES RUNS (ProVerif d'abord, la grande RAM) : (P1) ProVerif CF3-v3.pv (le port
   livré, sha256 98d8e6d1…) — la grande RAM, les six requêtes actives ; (P2) Tamarin — L1a
   par sous-lemmes de connaissance, L2b reformulé au fait persistant (!) ou à l'événement
   de naissance explicite (la sémantique d'occurrence nommée — le modèle-témoin test_occ
   .spthy demeure la référence), lemmes [reuse] ; (P3) dudect n ≥ 10 × {60, 200, 400} sur
   ≥ 2 machines goupillées ; (P4) fence.i sur silicium RV64 ; (P5) la 3ᵉ machine Loupe ;
   (P6) VAES goupillé (le kit W27VAES : source + notation + porte + commande) ; (P7) le
   compteur NV TPM matériel ; (P8) la bascule métal nu (le banc 16/16 prêt) ; (P9) la
   sentinelle Windows SACL/4663 ; (P10) FIDO2 hmac-secret. LE SERVING CONFORME (la dixième
   attente) vit à W28RLVR (le gate d'endpoint).
3. LES AUTOTESTS AVANT CHAQUE RUN (le mécanisme prouvé, jamais la machine) : chaque kit
   livré à empreinte consignée, l'autotest exécuté au bac AVANT le run du poste réel ; un
   autotest rouge suspend le kit (jamais la machine accusée).
4. L'AGRÉGATEUR FAIL-CLOSED : un run manquant refuse le verdict de la vague ; chaque témoin
   signé et daté consigné au journal append-only ; les refus nommés éprouvés par kit
   (ANCRE-PERDUE, RETOUR-EN-ARRIERE, APPEL-MANQUANT selon le kit).
5. LA PUBLICATION : chaque verdict TEL QUEL, les pics dudect N=200 compris s'ils persistent
   (l'investigation pré-enregistrée : les causes candidates au plan, la donnée ensuite) ;
   INCOMPLETE demeure INCOMPLETE tant que la preuve n'est pas close.

## Critères d'acceptation
- Le plan gelé AVANT tout run (le commit d'abord, sha256 à EMPREINTES-PLANS-VAGUE28.txt).
- Les autotests des kits vécus au bac (les empreintes recoupées avant/après).
- Aucun artefact scellé touché ; sceau-I 14/14 ; la recomposition C16 du compte d'attentes
  et C26 des statuts aux cinq pièces ; aucun chiffre fabriqué.
