http-08 · cible : forme absolue et relèvement · révision 3
Ancêtre : http-08:R2 (D77, embarquée 0.5.1 @0x7340 — la spécification R2 vit
dans m4/I/ et ne change pas : la balise est immuable § 9). La révision vit en
M5 (.text4 0x8000) et ne modifie que CE que le relèvement exige : SOUS
politique armée, la forme absolue « http:// » reçoit un verdict PROPRE « cible
à relever ». Tout le reste de R2 (forme origine, forme autorité CONNECT,
https:// byte-exact, chemin, casse, bornes, ordre des tests) est REPRIS TEL
QUEL — cité, non recopié (T5).
Intention : la composition D136 — le navigateur parle « http://hôte/… » au
mandataire explicite ; sous la politique --relever-https, la cible est
RELEVÉE vers l'HTTPS de l'hôte demandé : le parseur nomme la décision, le
routage appartient à http-10:R3 (l'unique propriétaire de l'appel de tls-08).
Aucun relèvement implicite : la politique vient de http-12:R3 (.data
R_POLITIQUE, écrite UNE fois au démarrage) et atteint cette feuille pure en
CINQUIÈME argument — jamais une lecture .data (I1).
Contrat :
  pre  : P1-P4 de http-08:R2 repris tels quels (span cible, longueur,
             sorties méthode/chemin/autorité, zone d'accueil 40 o) ;
         P5 NOUVEAU : la politique (u64 à la loge d'argument 5 — [rsp+0x30]
             du callee, miroir de la convention msx64) vaut 0 ou 1 ; toute
             autre valeur suit la branche « politique absente » (le test
             est un test de ZÉRO — l'appelant n'écrit jamais autre chose).
  post : Q1-Q3 et Q5 de http-08:R2 repris tels quels (formes ABSOLUE=1 /
             ORIGINE=2 / AUTORITÉ=3, refus de schéma, autorité vide) ;
         Q4 de http-08:R2 repris tel quel (« https:// » byte-exact 8 octets
             minuscules → rax 4, port implicite 443) ;
         Q6 NOUVEAU — forme absolue « http:// » (les 7 octets exacts,
             minuscules — R1 inchangé) ET P5 != 0 : rax = 5, verdict
             « cible à relever » (valeur propre à la révision, distincte du
             succès générique 0 et du verdict TLS 4) ; la zone est remplie
             aux règles R1 (forme ABSOLUE=1 — la STRUCTURE est absolue ;
             autorité et chemin découpés à l'identique de R2 ; le port
             implicite 443 au relèvement est déductible du verdict —
             consigné DANS la sortie, la décision d'appeler tls-08
             appartient à http-10:R3) ;
         SANS politique (P5 == 0) : R2 OCTET POUR OCTET sur tout chemin —
             « http:// » reprend le succès générique (rax 0, forme 1),
             le chemin M3 scellé T2 reste vert (anti-régression R7).
  inv  : I1-I5 de http-08:R2 repris (feuille pure, aucune écriture hors la
             zone d'accueil, aucun NUL supposé, non-volatils, comparaisons
             byte-exactes) ; I6 NOUVEAU : l'ordre des tests est documenté —
             « http:// » D'ABORD (le verdict 5 naît À LA PLACE du succès
             générique, jamais après), « https:// » ENSUITE (inchangé) —
             un schéma préfixe ne peut jamais produire le verdict 5
             (structurellement : le début d'autorité du verdict 5 est
             rcx+7, distinct du seuil rcx+8 du verdict 4) ; I7 : la
             politique est LUE UNE fois ([rsp+0x30]), jamais écrite.
Échecs :
  E1 : schéma malformé → refus R1/Q5 hérité — inchangé.
  E2 : politique absente → AUCUN verdict nouveau possible (Q6 inexistant) :
       la surface de contrebande n'augmente que du verdict, jamais d'une
       tolérance (D136).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : différentiel hérité + 5 000 cibles « http:// » sous DEUX politiques
       (armée : verdicts 5 et découpages exacts, port 443 déductible ;
       absente : verdicts R2 identiques octet pour octet — l'oracle compare
       R3-sans-politique à R2 émulée) — casse mixte, préfixes piégeux
       (« http://s://x »), autorités dégénérées, ports explicites (l'explicite
       du navigateur est PERDU au relèvement : l'origine est l'HTTPS standard
       de l'hôte — consigné au contrat de http-10:R3, E3).
  V3 : fuzzing à propriétés hérité (feuille pure : survie, terminaison,
       aucune écriture hors zone, non-volatils).
  V4 : test de rejet hérité (feuille pure) + toute notation lisant .data
       directement est refusée (I1).
Fixtures    : néant (la fixture SLASH de l'ancêtre R1 est réutilisée, R7).
Provenance  : écrite-avant-code (révision inter-jalon, modèle http-08:R2).
Décisions   : D77 (ancêtre), D136, D140 (0.5.1 embarqué), charte m5/I § 5.
