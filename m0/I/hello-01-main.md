hello-01 · bloc principal (point d'entrée) · révision 1
Intention : orchestrer l'artefact M0 — obtenir la sortie standard, déléguer l'écriture
du message puis la sortie du processus, sans porter aucune logique propre.
Contrat :
  pre  : P1 le bloc est le point d'entrée PE (AddressOfEntryPoint) ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention loader Windows) ;
         P3 aucun registre n'est préchargé par le chargeur au-delà de la norme PEB.
  post : Q1 le message de hello-02 a été soumis à WriteFile sur la sortie standard ;
         Q2 le processus se termine par ExitProcess(0), quel que soit le verdict d'écriture.
  inv  : I1 aucun stockage sous RSP (zone shadow space incluse) ;
         I2 tout appel système passe par l'IAT, jamais en direct ;
         I3 aucun registre non volatil (RBX, RBP, RDI, RSI, R12-R15) n'est modifié ;
         I4 l'écart de pile est nul à la sortie du bloc (frame strictement équilibré).
Échecs :
  E1 : GetStdHandle retourne INVALID_HANDLE_VALUE → repli documenté : l'écriture
       suivante échoue silencieusement et le processus termine ExitProcess(0) ;
       accepté pour M0 (chaîne artefact), durcissement du contrat d'erreur à M1.
Vecteurs :
  V1 : round-trip de notation 100 % — keystone → capstone → keystone, octets
       identiques (couvre la fidélité générale du bloc, donc P1-P3, Q1-Q2, I1-I4).
  V2 : propriété structurelle (oracle) : premier `sub rsp, 0x28` à l'adresse du bloc,
       appels inter-blocs vers a10002 et a10003 uniquement, aucun `syscall`/`int`
       (couvre P2, I1, I2, I4).
  V3 : test de rejet : toute notation alternative du bloc contenant un appel non-IAT
       au système, un déséquilibre de pile ou l'écriture sous RSP est refusée par
       l'oracle structurel (couvre I1, I2, I4).
  V4 : exécution sur Windows 11 — le message s'affiche et le code de sortie est 0
       (couvre Q1, Q2 ; critère de sortie M0, validation terrain).
Fixtures    : néant (aucune entrée externe parsée).
Provenance  : écrite-avant-code.
Décisions   : D7 (IAT), D8 (granularité/padding), D10 (profil primaire), D26 (M0).
