http-01 · itérateur de ligne · révision 1
Intention : isoler la prochaine ligne CRLF dans un tampon borné — LE seul
propriétaire du balayage de ligne du projet (verrou T5) : tout bloc qui a
besoin de « la ligne suivante » passe par ici ; les octets réseau ne sont
jamais supposés terminés par un NUL.
Contrat :
  pre  : P1 rcx pointe le tampon (octets réseau reçus, quelconques) ;
         P2 rdx contient la longueur utile du tampon (u64, rempli par les
             réceptions — peut couvrir des octets binaires quelconques) ;
         P3 r8 contient le curseur de balayage (offset u64, dans
             [0, longueur utile]) — position où commence la recherche ;
         P4 le tampon est stable pendant l'appel (il vit dans le cadre de
             l'appelant).
  post : Q1 ligne trouvée : rax = 0, rdx = longueur de la ligne SANS le
             CRLF (peut être 0 — la ligne vide est le terminateur de tête,
             cas légitime), r8 = curseur avancé APRÈS le CRLF (position de
             la ligne suivante) ;
         Q2 ligne incomplète (aucun CRLF dans [curseur, fin utile)) :
             rax = 1, rdx et r8 inchangés — l'appelant accumule et rappelle
             avec un curseur identique sur un tampon plus rempli ;
         Q3 aucun autre octet que la paire CRLF terminatrice n'est consommé
             (le curseur avance d'exactement longueur + 2 en cas de
             succès).
  inv  : I1 le bloc est une feuille pure : aucun appel, aucun IAT, aucun
             état ; I2 aucune écriture mémoire (lecture seule sur le
             tampon) ; I3 la recherche reconnaît exactement la paire 0x0D
             0x0A (CR puis LF) — un LF non précédé de CR n'est PAS un
             terminateur pour ce bloc (sa détection comme défaut appartient
             à http-06, propriétaire de la validité de tête) ; I4 aucun
             registre non volatil modifié.
Échecs :
  E1 : pas de CRLF jusqu'à la fin utile → verdict 1 (Q2) : ce n'est pas un
       échec de contrat mais un état nommé — l'appelant (http-10, http-04)
       décide : accumuler davantage ou constater la malformation.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 tampons aléatoires
       (binaires hostiles : NUL, CR isolés, LF isolés, CRLF en positions
       limites, curseur à la fin exacte) — verdict, longueur et curseur
       contre un modèle de référence ; non-volatils inchangés (couvre
       P1-P4, Q1-Q3, I1-I4).
  V3 : harnais de fuzzing à propriétés P1-P5 (D45) étendu à la surface
       http : survie, terminaison, verdict conforme au modèle, aucune
       écriture mémoire (couvre I1-I4 sur entrées non fiables).
  V4 : test de rejet : toute notation du bloc écrivant en mémoire, appelant
       un autre bloc ou modifiant un non-volatil est refusée (couvre I1,
       I2, I4).
Fixtures    : néant (le tampon appartient à l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
