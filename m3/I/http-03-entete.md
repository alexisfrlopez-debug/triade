http-03 · ligne d'en-tête · révision 1
Intention : découper UNE ligne d'en-tête isolée (par http-01) en nom et
valeur — deux spans dans le tampon d'origine, la valeur débarrassée des
blancs facultatifs (OWS : SP/HTAB) aux deux extrémités ; le rejet des
défauts de forme (RFC 7230 §3.2.4) est nominal et nommé, jamais une
tolérance silencieuse.
Contrat :
  pre  : P1 rcx pointe la ligne (sans CRLF — garantie par http-01:Q1) ;
         P2 rdx contient la longueur de la ligne (u64, peut être 0) ;
         P3 r8 pointe la zone d'accueil « champs en-tête » de 32 octets
             fournie par l'appelant (pile) : nom ptr u64 @0, nom longueur
             u64 @8, valeur ptr u64 @16, valeur longueur u64 @24 ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès (rax = 0) : la zone est remplie — le nom est le span
             jusqu'au premier deux-points (non inclus), la valeur est le
             span après le deux-points, rogné des OWS (0x20 et 0x09)
             extrêmes ; la valeur peut être vide (longueur 0) ;
         Q2 aucun deux-points dans la ligne → rax = 1 (pas de séparateur),
             zone intacte ;
         Q3 nom vide, ou nom contenant un blanc (SP/HTAB) avant le
             deux-points → rax = 2 (nom invalide — RFC 7230 §3.2.4 : le
             rejet est OBLIGATOIRE, la tolérance est la faille
             anti-contrebande historique), zone intacte ;
         Q4 les caractères au-delà des OWS de la valeur (y compris
             binaires hors contrôle de ce bloc — la ligne est déjà isolée
             du CRLF par http-01) ne sont ni filtrés ni interprétés :
             la valeur est un span opaque.
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état ; I2 aucune
             écriture hors la zone d'accueil (32 octets), aucune écriture
             partielle avant le verdict final ; I3 aucune hypothèse de
             terminaison NUL ; I4 non-volatils préservés ; I5 le rognage
             OWS ne déplace aucun octet (ajustement de bornes du span
             uniquement — le tampon n'est jamais réécrit).
Échecs :
  E1 : pas de deux-points → rax = 1 : l'appelant (http-10) répond 400 ;
  E2 : nom vide ou blanc avant le deux-points → rax = 2 : réponse 400
       (durcissement délibéré, E2 de la classe « smuggling »).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 lignes (noms valides,
       noms avec blancs interdits en tête/milieu, valeurs avec OWS
       asymétriques SP/HTAB, valeurs vides, deux-points en position 0,
       plusieurs deux-points — le premier sépare) — verdict et bornes
       exacts contre modèle ; zone intacte sur verdict non nul (couvre
       P1-P4, Q1-Q4, I1-I5).
  V3 : fuzz P1-P5 sur lignes non fiables (D45) : survie, terminaison,
       verdict conforme, aucune écriture hors zone (couvre I1, I2).
  V4 : test de rejet : toute notation copiant la valeur, écrivant la zone
       avant verdict, ou modifiant le tampon est refusée (couvre I2, I5).
Fixtures    : néant (les lignes viennent du tampon de l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
