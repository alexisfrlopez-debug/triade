loupe-04 · le cadre : la structure unique de session, posée vierge · révision 1
Intention : LA STRUCTURE UNIQUE que les dix-sept autres blocs partagent —
la disposition déclarée UNE FOIS ici (chaque champ à son offset, la
source unique : les autres blocs y RENVOIENT, aucune connaissance
dupliquée), et le geste de la poser VIERGE : tout à zéro, la poignée à
INVALIDE. Le cadre naît à l'ouverture (loupe-01 l'appelle) et re-naît à
la fermeture (loupe-03 l'appelle) — entre les deux, il est LA vérité de
la session.
Contrat :
  pre  : P1 AUCUNE précondition — le geste de naissance/mort ne dépend
             de rien (la zone est À L'IMAGE, déclarée au plan
             d'adressage : 960 o, alignée 16).
  post : Q1 le cadre VIERGE : chemin (520 o UTF-16) à zéro, taille = 0,
             poignée = INVALIDE (0xFFFF…FFFF), vue = 0, curseur = 0,
             remplissage = 0, sale = 0, refus_quitter = 0, réservé = 0,
             le tampon (384 o) à zéro ;
         Q2 la mise à zéro par libc-07 (memset) HÉRITÉ PAR LA CARTE —
             le bloc scellé M1, byte-identique, JAMAIS une boucle
             réécrite ; puis la poignée posée à INVALIDE ;
         Q3 rax = 0.
  inv  : I1 LA DISPOSITION (la source unique, D161 — les offsets du
             plan d'adressage) : chemin UTF-16[260] @ +0 (520 o) ·
             taille u64 @ +520 · poignée u64 @ +528 · vue u64 @ +536
             (multiple de 16, INVARIANT) · curseur u64 @ +544 (borné
             [0, taille−1], INVARIANT) · remplissage u32 @ +552 ·
             sale u32 @ +556 · refus_quitter u32 @ +560 · réservé u32
             @ +564 · tampon[384] @ +568 — total 952, la zone 960
             (alignée 16) ;
         I2 AUCUNE entrée IAT, AUCUN site syscall (le memset passe PAR
             LA CARTE — le miroir exact des feuilles pures tls13,
             charte § 9) ;
         I3 le bloc ne détient AUCUN autre état : rien hors la zone
             pointée, rien en pile qui survive au retour ;
         I4 aucun registre non volatil détruit ; la croissance du slot
             est NOP, 0x90 (charte § 9).
Échecs :
  E1 : AUCUN — la zone est à l'image (D161 : déclarée avant la
       notation), le geste ne peut pas échouer ; l'oracle le constate
       par le cadre vierge (justification au champ Intention : le
       gabarit l'exige, le domaine la nomme).
Vecteurs :
  V1 : différentiel — après le geste : les 960 octets comparés au
       modèle (zéros partout sauf la poignée INVALIDE aux octets
       +528..+535) (couvre Q1, Q2, Q3).
  V2 : scénario — la chaîne complète : loupe-01 (le cadre rempli) PUIS
       loupe-04 direct : le cadre revient VIERGE — l'ouverture
       re-démarre propre (couvre Q1).
  V3 : falsification — un octet hors zéro au modèle : le
       différentiel échoue (l'état neuf est une exigence, pas un
       espoir).
Fixtures    : néant (le cadre est l'état, pas un contrat externe).
Provenance  : écrite-avant-code.
Décisions   : D171, D161 (la disposition arrêtée avant la notation),
              D7 (l'héritage minilibc PAR LA CARTE).
