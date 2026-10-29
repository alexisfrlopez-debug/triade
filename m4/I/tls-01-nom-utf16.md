tls-01 · hôte span → UTF-16 · révision 1
Intention : traduire le nom d'hôte (octets réseau) vers UTF-16 bas pour
pTargetName de la poignée de main — LE seul propriétaire de la traduction
span → UTF-16 du projet (verrou T5), miroir exact de tcp-13:Q2 (span →
chaîne C) : l'exigence de terminaison NUL de SSPI vit ici et nulle part
ailleurs.
Contrat :
  pre  : P1 rcx pointe l'hôte (octets réseau, jamais supposés terminés) ;
         P2 rdx contient la longueur de l'hôte (u64, > 0) ;
         P3 r8 pointe la destination (cadre de l'appelant, capacité au
             moins 2 × (HOTE_MAX + 1) octets = 512) ;
         P4 l'hôte et la destination sont disjoints (l'appelant garantit
             des zones non recouvrantes).
  post : Q1 succès : rax = 0, la destination contient la séquence UTF-16
             petit-boutiste des octets source, terminée par un mot NUL
             (exigence SSPI) ; rdx = longueur en octets écrite
             (2 × (longueur source + 1)) ;
         Q2 refus de longueur : rax = 1 — l'hôte dépasse HOTE_MAX (255,
             limite DNS héritée tcp-13) : rien n'est écrit ;
         Q3 refus d'encodage : rax = 2 — un octet source ≥ 0x80 : les noms
             internationalisés (IDNA/punycode) sont hors périmètre M4, un
             octet étendu est une contrebande d'encodage : rien n'est écrit.
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état ; I2 écrit
             SEULEMENT dans [destination, destination + 2 × (longueur + 1))
             (Q1) — aucun octet sinon (Q2/Q3) ; I3 la traduction est
             injective : chaque octet source devient exactement un mot
             16 bits égal à sa valeur ; I4 aucun registre non volatil
             modifié.
Échecs :
  E1 : hôte vide (longueur 0) → refus 1 de Q2 (l'autorité http-07 exclut
       déjà l'hôte vide : double barrière, une par couche).
  E2 : octet ≥ 0x80 → verdict 2 de Q3 — nommé « cible non traduisible »
       côté session, réponse 502 propre (http-10:R2), JAMAIS une tentative
       de conversion partielle.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 hôtes aléatoires (ASCII
       imprimable, longueurs 0 à 300, octets ≥ 0x80 injectés en positions
       limites) contre un modèle de référence — verdict, contenu, longueur
       écrite ; non-volatils inchangés (couvre P1-P4, Q1-Q3, I1-I4).
  V3 : fuzzing à propriétés (V3 hérité D45) : survie, terminaison, aucun
       octet écrit hors destination (couvre I1-I4 sur entrées non fiables).
  V4 : test de rejet : toute notation écrivant hors destination, appelant
       un autre bloc ou modifiant un non-volatil est refusée.
Fixtures    : néant (l'hôte appartient à l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 5 (spans, traduction unique).
