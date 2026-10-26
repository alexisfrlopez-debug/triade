libc-01 · copie mémoire · révision 1
Intention : copier exactement n octets de src vers dst en direction avant, sans
interpréter les octets ni dépendre d'aucun service extérieur — la brique de
déplacement de mémoire de la mini-libc.
Contrat :
  pre  : P1 rcx contient dst, région d'au moins n octets accessible en écriture ;
         P2 rdx contient src, région d'au moins n octets accessible en lecture ;
         P3 r8 contient n, nombre d'octets à copier (u64) ;
         P4 les régions dst et src ne se chevauchent pas ;
         P5 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 les n octets de dst sont égaux aux n octets de src ;
         Q2 rax contient dst (valeur de retour canonique) ;
         Q3 les n octets de src sont inchangés.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (rsp identique à l'entrée, ret) ;
         I3 aucun registre non volatil (RBX, RBP, RDI, RSI, R12-R15) n'est modifié ;
         I4 n = 0 : aucun octet n'est écrit.
Échecs :
  E1 : chevauchement dst/src (P4 violée) → comportement hors contrat, jamais
       généré par l'oracle (la sanction appartient à l'appelant, comme la libc C).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale, donc P1-P5,
       Q1-Q3, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à entrées aléatoires
       contraintes par P1-P5, n ∈ [0, 1024], contenus aléatoires — dst comparé
       à la référence, src recontrôlé, rax, non volatils, rsp (couvre Q1-Q3,
       I2-I4).
  V3 : vecteurs dorés embarqués (autotest b20008) : motif 16 octets, copie de
       longueur nulle sur sentinelle, motif 33 octets (couvre Q1, I4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors de dst est refusée par l'oracle structurel (couvre I1).
Fixtures    : motifs .rdata MOTIF16/SENT16/MOTIF33 (référencés par libc-08).
Provenance  : écrite-avant-code.
Décisions   : D7 (aucun appel système), D8 (granularité/padding), D26 (chaîne
              artefact), D28 (zones d'adressage), D29 (substrat d'émulation).
