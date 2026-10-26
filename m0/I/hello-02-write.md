hello-02 · bloc d'écriture stdout · révision 1
Intention : écrire un tampon mémoire sur un flux Windows en un seul appel WriteFile,
en honorant intégralement le contrat msx64 à cinq arguments.
Contrat :
  pre  : P1 rcx contient un HANDLE de flux (valeur retournée par GetStdHandle) ;
         P2 rdx contient l'adresse du tampon à écrire ;
         P3 r8d contient la longueur en octets du tampon (len > 0) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16).
  post : Q1 eax contient le verdict BOOL de WriteFile, sans masquage ;
         Q2 la pile est restaurée à l'identique (frame équilibré, ret) ;
         Q3 le 4e et le 5e argument de WriteFile sont NULL (pas d'octets écrits
             rapportés, pas d'opération avec chevauchement).
  inv  : I1 le shadow space de 32 octets est alloué avant l'appel ;
         I2 aucun registre non volatil n'est modifié ;
         I3 la longueur passée à WriteFile est exactement celle reçue (P3).
Échecs :
  E1 : WriteFile retourne FALSE → propagation du verdict (eax = 0) à l'appelant,
       aucune transformation, aucun re-essai (repli : silence documenté côté hello-01).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale, donc P1-P4, Q1-Q3,
       I1-I3).
  V2 : propriété structurelle (oracle) : r9d et [rsp+0x20] annulés avant l'appel IAT
       unique, `add rsp` symétrique au `sub rsp`, `ret` terminal (couvre Q2, Q3, I1).
  V3 : test de rejet : toute notation sans allocation du shadow space, avec écriture
       sous RSP, ou avec un appel système direct est refusée par l'oracle (couvre I1,
       et la discipline I2 de hello-01 pour la partie appel).
  V4 : exécution sur Windows 11 — le message complet s'affiche (couvre Q1, I3 ;
       critère de sortie M0, validation terrain).
Fixtures    : néant (le tampon provient de hello-01, donnée embarquée du profil).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D8 (granularité/padding), D26 (M0).
