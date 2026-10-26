av-04 · finalisation bourrage-longueur-extraction SHA-512 · révision 1
Intention : clôturer le hachage : octet 0x80, zéros jusqu'à 112 (mod 128),
longueur du message en BITS sur 128 bits gros-boutistes dans les 16
derniers octets du bloc, compression finale, extraction des 64 octets du
digest en gros-boutiste — miroir exact de ah-07:R1 avec la longueur 128
bits (le champ haut de 8 octets est zéro : total < 2^61 octets, limite
documentée miroir hachoir).
Contrat :
  pre  : P1 rdi pointe vers le contexte (256 o) après absorptions ;
         P2 rsi pointe vers la sortie (64 octets inscriptibles) ;
         P3 pile alignée.
  post : Q1 la séquence de compression produit exactement le digest
             FIPS du message absorbé — octet pour octet égale à
             sha512sum (la preuve est l'oracle différentiel natif) ;
         Q2 la sortie contient H[0..7] sérialisés gros-boutistes (8
             qwords bswappés, 64 octets) ;
         Q3 rax = rsi (la sortie se rend en retour) ;
         Q4 le contexte reste lisible (remplissage = 128 après la
             dernière compression — l'état est cohérent, une seconde
             finalisation n'est PAS prévue par contrat).
  inv  : I1 appels directs : av-02 (compression, deux fois au plus —
             chemin court un bloc, chemin long deux) ;
         I2 deux chemins : remplissage < 112 (0x70) : bourrage + longueur
             dans LE bloc courant ; sinon : bourrage du bloc courant,
             compression, second bloc de zéros + longueur — miroir
             ah-07 ; le champ longueur s'écrit en deux qwords : mot haut
             zéro @ tampon+112, mot bas bswappé @ tampon+120 ;
         I3 aucune donnée RIP, aucun syscall ; aucune écriture hors
             contexte/sortie ;
         I4 prologue : 2 pushes + sub 8 — pile 16-alignée aux appels
             (miroir ah-07).
Échecs :
  E1 : aucun (les deux chemins sont bornés).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle différentiel natif : les tailles de transition 111, 112,
       127, 128, 129 (frontières du double bloc) et le million de 'a'
       produisent les digests sha512sum exacts (couvre Q1/Q2 : la
       longueur 128 bits et le second bloc sont les deux nouveautés
       à casser).
  V3 : falsification intégrale — zéro silence.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La longueur 128 bits impose le mot haut nul explicite :
              rep stosb ne couvre que 0..111, le qword @ +176 est posé
              par mov — la spec l'exige (I2), le bogue silencieux
              (longueur décalée de 8 octets) ne peut pas naître.
