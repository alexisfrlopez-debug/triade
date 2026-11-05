tls13-26 · la poignée : l'épinglage du certificat · révision 1
Intention : LA décision de confiance du jalon — une COMPARAISON, jamais
une croyance : le SHA-256 des octets DER du certificat de l'entité,
confronté à L'EMPREINTE ÉPINGLÉE fournie par l'appelant (la donnée du
kit). L'analyse X.509 complète (la chaîne, les extensions, la révocation,
la vérification de signature du CertificateVerify) est un CHANTIER FUTUR
NOMMÉ — le jalon compare et NOMME la frontière : il ne fait pas
confiance en silence.
Contrat :
  pre  : P1 rcx = le certificat (les octets DER de l'entité — N o ; le
             DÉTROIT est nommé : l'extraction de la PREMIÈRE entrée de
             la certificate_list du message Certificate — la lecture du
             u24 de longueur — est le geste du principal tls13-27,
             jamais de la brique) ;
         P2 rdx = N (1 ≤ N ≤ 2^61) ; P3 r8 = l'empreinte attendue (32
             o — la donnée de confiance du kit) ; la pile alignée 16.
  post : Q1 le SHA-256 des N octets (par tls13-01/03/04 — un contexte
             de PILE local, charte § 6) CONFRONTÉ à l'empreinte par OU
             cumulatif : conforme → rax = 0 ; divergent → rax = -6
             NOMMÉ (épinglage divergent — la session MEURT sans
             autres formes, charte § 5 : le certificat offert n'est
             pas celui qu'on attendait) ;
         Q2 le certificat et l'empreinte INTACTS ;
         Q3 la preuve : le certificat du TRANSFERT RFC 8448 (le DER du
             transcript : l'empreinte RECALCULÉE au chantier (b), le
             verdict vert) et LA FALSIFICATION INVITÉE (un octet du
             DER muté → -6 ; l'empreinte mutée → -6 — la garde
             constatée dans les DEUX sens).
  inv  : I1 la comparaison est TEMPS CONSTANT (charte § 3 : le OU
             cumulatif des 32 différences — l'empreinte est une donnée
             de confiance, la discipline demeure) ;
         I2 compositions : tls13-01, tls13-03, tls13-04 (le hachage) —
             la brique ne calcule RIEN d'autre que le condensé et le
             verdict ;
         I3 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8).
