sup-22 · balayeur d'extrait (étiquette -> valeur) · révision 1
Intention : l'unique parseur du superviseur — un chercheur d'étiquette
borné, dans la lignée de http-04-chercher (recherche d'en-tête, M3) : dans
un tampon d'octets NON FIABLES (réponses HTTP de l'API Drive servies par
curl.exe), trouver la première occurrence d'une étiquette littérale, puis
copier les octets qui la suivent jusqu'à un octet d'arrêt. Trois usages :
"access_token": " ... " dans la réponse OAuth (format INDENTÉ réel de
Google — D69 : un espace après les deux-points), "Location: " ... CR dans les
en-têtes de session resumable (HTTP/1.1 forcée — D69), "\"id\"" ... presence
test. Rien n'est
interprété : ce qui n'est pas extrait ne peut pas être mal parsé (leçon
M3 appliquée au canal Drive).
Contrat :
  pre  : P1 rcx = tampon (octets bruts, aucune terminaison supposée) ;
         P2 rdx = longueur utile du tampon (u64, > 0) ; P3 r8 = étiquette
         (octets littéraux), r9 = longueur d'étiquette (1..32) ; P4 5e
         arg [rsp+0x20] = octet d'arrêt (ex. '"' ou 0x0D) ; P5 6e arg
         [rsp+0x28] = destination (tampon appelant, assez grand) ; P6 7e
         arg [rsp+0x30] = capacité max de destination (u64, > 0) ; P7
         pile alignée.
  post : Q1 première occurrence de l'étiquette cherchée par memcmp
         glissant (libc-02 scellée) ; Q2 si absente -> rax = 0, destination
         intacte ; Q3 si trouvée : les octets après l'étiquette sont
         copiés (libc-01) jusqu'au PREMIER octet d'arrêt (non compris) ou
         la fin du tampon (non comprise) ; Q4 rax = nombre d'octets copiés
         (0 si vide : étiquette en fin de tampon) ; Q5 si la copie
         atteindrait la capacité max -> copie tronquée à max - 1 + NUL
         posé + rax = 0 (défaillance visible, pas de débordement) ; Q6 en
         cas de copie non vide, un NUL terminal est posé après les octets
         (destination[max_copie] = 0) — la destination est une chaîne C
         utilisable par memcpy/strlen.
  inv  : I1 bornes : jamais lu avant tampon[0] ni après tampon[len-1],
         jamais écrit après destination[cap-1] ; I2 memcmp/memcpy scellées
         uniquement (aucune boucle de comparaison locale — miroir http-04) ;
         I3 aucun état .data : bloc pur, réentravant, appelable de tout
         thread ; I4 l'étiquette elle-même n'est jamais copiée (seule la
         valeur suit).
Échecs :
  E1 : étiquette absente -> rax = 0 (chemin nominal d'échec, pas une
       exception — le scénario journalise et continue).
  E2 : valeur tronquée par la capacité -> rax = 0 (défaillance explicite ;
       un jeton OAuth raccourci ne doit jamais circuler).
  E3 : tampon contenant l'étiquette SANS valeur suivante (fin de tampon
       immédiate) -> rax = 0, aucun octet copié.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : différentiel — 10 000 cas aléatoires contraints (tampons <= 600 o,
       étiquettes 1..16 o, octet d'arrêt présent/absent, étiquette
       présente zéro/une/plieurs fois, valeur vide, valeur collée à la
       fin) comparés à la référence Python (find + split).
  V3 : cas nominaux — access_token dans une réponse OAuth réaliste ;
       "Location: https://..." arrêté au CR ; "\"id\"" dans un manifeste.
  V4 : falsification — décrémenter la longueur d'étiquette d'un octet fait
       échouer V2 (occurrences parasites acceptées à tort).
Fixtures    : génération par graine (harnais, miroir M3 P1-P5).
Provenance  : écrite-avant-code.
Décisions   : D48 ; discipline http-04-chercher (unique comparaison, bornes
              testées à chaque pas) ; bloc pur par contrat (testable au
              différentiel, miroir fuzzing M3).
