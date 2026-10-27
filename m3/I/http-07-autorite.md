http-07 · autorité · révision 1
Intention : résoudre une autorité « hôte[:port] » — extraire le span hôte
(y compris la forme IPv6 entre crochets, crochets exclus de la valeur
rendue) et le port — LA seule implémentation du découpage d'autorité du
projet (verrou T5) : la cible absolue de http-08 et la valeur de l'en-tête
Host de http-10 passent par ici, jamais par deux codes frères.
Contrat :
  pre  : P1 rcx pointe le span autorité (octets quelconques) ;
         P2 rdx contient la longueur du span (u64, peut être 0) ;
         P3 r8d contient le port par défaut (u16) : la valeur 0 signifie
             « port EXIGÉ » (le connecteur de tunnel n'a pas de base pour
             deviner — tout autre valeur est le défaut de l'appelant : 80
             pour un schéma http) ;
         P4 r9 pointe la zone d'accueil « autorité résolue » de 24 octets
             (pile de l'appelant) : hôte ptr u64 @0, hôte longueur u64 @8,
             port u32 @16 ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès (rax = 0) : la zone contient le span hôte (crochets
             IPv6 ouvrant/fermant EXCLUS — le littéral nu est rendu, prêt
             pour le résolveur) et le port effectif (explicite, ou le
             défaut de P3) ;
         Q2 hôte vide (span vide, « :8080 », « []:8080 », crochets vides)
             → rax = 1 (hôte absent) ;
         Q3 port invalide → rax = 2 : vide (« hôte: »), non-chiffres,
             plus de 5 chiffres, ou valeur > 65535 ; ET port absent alors
             qu'exigé (défaut P3 = 0 et aucun « : » dans le span) — le
             tunnel sans port nommé est rejeté, pas deviné ;
         Q4 crochet IPv6 non fermé (« [::1 », « [::1:80 ») ou « : » après
             le crochet fermant mal placé → rax = 3 (crochet invalide) ;
         Q5 sur tout verdict non nul, la zone d'accueil est intacte.
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture hors la zone d'accueil, aucune écriture partielle ;
         I2 le découpage repère le DERNIER « : » hors crochets (le port
             suit le dernier deux-points — un hôte IPv6 nu sans crochets
             est ambigu par nature et tombe dans Q3 : les formes valides
             exigent les crochets, les formes ambiguës sont rejetées
             nommément) ;
         I3 les chiffres du port sont validés un à un (refus immédiat du
             premier non-chiffre) et la valeur est testée ≤ 65535 avant
             publication ; I4 aucune hypothèse de terminaison NUL ;
         I5 non-volatils préservés.
Échecs :
  E1 : verdicts 1-3 (Q2-Q4) — l'appelant (http-10) répond 400 : aucune
       autorité mal formée n'atteint jamais le résolveur (tcp-13) — le
       rejet avant l'entrée système est la règle du jalon.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 15 000 autorités générées
       (hôtes courts/longs, ports 0/1/80/443/65535/65536/123456,
       absents/exigés/défauts, IPv6 « [::1]:443 », « [2001:db8::1] »,
       crochets ouverts, deux-points multiples, « a:b:c » — dernier
       deux-points, vides) — verdict, span hôte (crochets exclus), port
       effectif contre modèle ; zone intacte sur échec (couvre P1-P5,
       Q1-Q5, I1-I5).
  V3 : fuzz P1-P5 sur autorités non fiables (D45) : survie, terminaison,
       verdict conforme, aucune écriture hors zone (couvre I1).
  V4 : test de rejet : toute notation publiant une valeur de port avant
       validation complète, ou recopiant l'autorité, est refusée (couvre
       I1, I3).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
