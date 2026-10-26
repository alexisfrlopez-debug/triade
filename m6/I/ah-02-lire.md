ah-02 · lecture par appel système · révision 1
Intention : lire des octets depuis un descripteur de fichiers — le pendant
d'ah-01 : l'agent tire ses données du noyau, un morceau à la fois, sans
bibliothèque. La boucle de lecture (appel répété jusqu'à EOF) appartient à
l'orchestration (ah-09) : ce bloc est UNE lecture, au contrat le plus fin.
Contrat :
  pre  : P1 edi contient le descripteur de fichiers (u32) ;
         P2 rsi pointe vers le tampon de réception (mémoire inscriptible
             d'au moins edx octets) ;
         P3 edx contient la capacité demandée (u32) ;
         P4 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 succès : rax contient le nombre d'octets lus (0 = fin de
             fichier, > 0 = octets disponibles, ≤ edx) ;
         Q2 échec noyau : rax contient -errno (négatif).
  inv  : I1 appel système : instruction syscall avec rax = 0 (sys_read)
             exclusivement ;
         I2 feuille : 0 octet de pile, aucun non-volatil, aucun stockage
             sous rsp ; le noyau écrit au plus edx octets en [rsi, rsi+edx) ;
         I3 le bloc ne boucle pas : un appel, un verdict — EOF (rax = 0)
             est un verdict, pas un échec.
Échecs :
  E1 : descripteur invalide → -EBADF (-9) ; E2 : répertoire ouvert en
       lecture → -EISDIR (-21) au premier read ; E3 : tampon non
       inscriptible → -EFAULT (-14).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, artefact entier) : la
       concaténation de tous les morceaux lus par hachoir sur un fichier
       témoin est octet-identique au contenu du témoin (couvre Q1 sur
       toutes les tailles de transitions 65535/65536/65537) ; un
       répertoire passé en argument produit le message d'erreur de
       lecture et le code de sortie 1 (couvre E2, ah-09).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La granularité un-appel-un-verdict est délibérée : elle
              rend la limite de capacité observable par l'oracle (chaque
              lecture de 64 Kio est un cas différentiel autonome).
