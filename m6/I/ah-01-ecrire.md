ah-01 · écriture par appel système · révision 1
Intention : écrire des octets sur un descripteur de fichiers — le bloc
d'entrée/sortie élémentaire du profil Linux, miroir exact de hello-02:R1
du profil Windows (WriteFile) : l'agent parle directement au noyau, sans
bibliothèque, sans tampon intermédiaire. Interface noyau x86-64 Linux
spécifiée intégralement (I1) : le numéro d'appel voyage dans rax, le
quatrième argument éventuel d'un appel voyage en r10 (pas rcx — le piège
miroir de l'ABI fonction), rcx et r11 sont détruits par l'instruction.
Contrat :
  pre  : P1 edi contient le descripteur de fichiers (u32, ex. 1 = stdout,
             2 = stderr) ;
         P2 rsi pointe vers le tampon à écrire (mémoire lisible) ;
         P3 edx contient le nombre d'octets à écrire (u32 ; n ≤ 2^32-1) ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16 — l'appelant
             vient d'exécuter call).
  post : Q1 succès : rax contient le nombre d'octets écrits (≥ 0) ;
         Q2 échec noyau : rax contient -errno (valeur négative).
  inv  : I1 appel système : instruction syscall avec rax = 1 (sys_write)
             exclusivement — aucun autre numéro, aucune autre interface ;
         I2 feuille : 0 octet de pile consommé, aucun stockage sous rsp,
             aucun registre non volatil touché, aucun accès mémoire hors
             la lecture de [rsi, rsi+rdx) par le noyau ;
         I3 le bloc ne tamponne pas : un appel, un verdict — l'appelant
             gère les écritures partielles (aucune observée sur pipes et
             fichiers réguliers pour n < 2^31, mais le contrat ne le
             promet pas).
Échecs :
  E1 : descripteur invalide ou fermé → rax = -EBADF (-9) ; E2 : n > ce
       que le descripteur accepte → écriture partielle (Q1) ; E3 : tampon
       illisible → rax = -EFAULT (-14).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, artefact entier) : chaque octet
       transmis par hachoir transite exactement une fois par ce bloc —
       la sortie constatée sur stdout est octet-identique à la ligne
       attendue (couvre Q1) ; l'écriture sur un descripteur fermé est
       couverte par la falsification ( divergence garantie).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Premier bloc du domaine ah — l'interface noyau remplace
              l'IAT du profil Windows : l'adresse cible n'est plus un slot
              résolu par le chargeur mais un numéro dans rax, détruisant
              rcx/r11 au passage (documenté I1 : l'auteur ne le réapprend
              pas à chaque bloc, chaque spec sys le répète).
