http-06 · détection de fin de tête · révision 2
Intention : dire si les octets accumulés contiennent une tête de requête
COMPLÈTE — la paire CRLF CRLF terminatrice — et être LE propriétaire de la
limite de tête MAX_TETE (8192 octets, repère RFC 7230 §3.1.1 « au moins
8000 ») et du rejet du LF isolé : une tête non terminée est un état, une
tête excessive ou sale est un verdict nommé, jamais une boucle infinie
d'accumulation.
Contrat :
  pre  : P1 rcx pointe le tampon d'accumulation (octets réseau quelconques,
             la tête éventuelle puis des octets de corps éventuels) ;
         P2 rdx contient le remplissage utile (u64, peut être 0 — rien
             reçu) ;
         P3 le tampon a une capacité ≥ MAX_TETE + 1 (8193 octets —
             garantie de l'appelant http-10 : la limite est testable sans
             dépassement) ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 tête complète (rax = 0) : longueur de la tête, CRLF CRLF
             inclus, INFERIEURE OU ÉGALE à MAX_TETE (R2 — une tête
             complète mais excessive est le verdict Q3, jamais un succès) ;
             rdx porte la longueur (le corps commence exactement à cet
             offset — borne rendue à l'appelant) ; le terminateur reconnu
             est la paire 0x0D 0x0A 0x0D 0x0A ;
         Q2 tête incomplète (rax = 1) : pas de terminateur dans le
             remplissage, remplissage ≤ MAX_TETE — l'appelant accumule
             davantage (état nominal, pas un défaut) ;
         Q3 limite dépassée (rax = 2) : la tête excède MAX_TETE —
             remplissage > MAX_TETE sans terminateur (R1), OU terminateur
             trouvé au-delà de MAX_TETE (R2 : le trou de R1 laissait
             passer une tête complète de 8232 octets comme un succès —
             surface de contrebande ET débordement du tampon de
             réécriture de http-10) ; aucune tête partielle n'est jamais
             parsée au-delà ;
         Q4 LF isolé (rax = 3) : un octet 0x0A non précédé de 0x0D dans le
             remplissage balayé — rejet strict CRLF (la RFC 7230 §3.5
             PERMET d'accepter le LF nu ; nous le refusons : durcissement
             anti-contrebande, chaque tolérance de format est une surface
             d'attaque) ;
         Q5 sur tout verdict, le tampon n'est jamais lu au-delà du
             remplissage ni écrit (le bloc ne connaît pas la capacité
             au-delà de P3).
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture mémoire ; I2 un seul balayage linéaire — la paire
             CRLF CRLF peut être trouvée par le LF du premier CRLF déjà
             rencontré, mais tout LF isolé tranché (rax = 3) au premier ;
         I3 la constante MAX_TETE (8192) vit dans CE contrat (unique
             propriétaire — T1) : http-10, qui alloue le tampon, et la
             réponse 431, y renvoient ; I4 non-volatils préservés.
Échecs :
  E1 : tête > 8192 octets → rax = 2 : l'appelant (http-10) répond 431 et
       clôture la connexion (jamais de ré-allocation ni de tampon
       dynamique — la limite est un contrat, pas un accident) ;
  E2 : LF isolé → rax = 3 : réponse 400.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 tampons (remplissages
       0/1/8192/8193/8194, terminateur aux positions limites
       8188-8192, LF isolés en tête/milieu/fin, CR finaux sans LF,
       tampons binaires purs, terminateur suivi d'un corps quelconque) —
       verdict et longueur exacts contre modèle (couvre P1-P4, Q1-Q5,
       I1-I4).
  V3 : fuzz P1-P5 sur accumulations non fiables (D45) : survie,
       terminaison, verdict conforme, aucune écriture mémoire — c'est le
       point d'entrée du différentiel de campagne million sur la chaîne
       d'accumulation (couvre I1, I2).
  V4 : test de rejet : toute notation lisant au-delà du remplissage,
       écrivant le tampon, ou portant une seconde copie de la constante de
       limite est refusée (couvre Q5, I1, I3).
Fixtures    : néant (le tampon d'accumulation appartient à http-10).
Provenance  : écrite-avant-code.
Historique  : R1 (D46) — version initiale. R2 (journal 36, D47) — le trou
              du succès excessif : une tête AVEC terminateur au-delà de
              8192 rendait verdict 0 (Q1 ne bornait pas la longueur),
              ouvrant deux défauts réels : (a) contournement de la réponse
              431 (une tête de 12 Kio était parsée puis réécrite), (b)
              débordement du tampon de réécriture de http-10 (11,75 Kio
              utiles) pour les têtes entre ~11,75 et 16 Kio — corruption
              de la pile session. R2 borne Q1 (longueur <= MAX_TETE) et
              étend Q3 au terminateur au-delà de la limite. Contrat stable
              au sens R4 pour tout verdict déjà rendu à R1 (les têtes
              conformes et les remplissages incomplets sont inchangés).
Décisions   : D8, D19, D45, D46, D47.
