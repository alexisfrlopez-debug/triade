sys-01 · l'émetteur syscall direct · révision 1
Intention : LE mécanisme du domaine — l'instruction `syscall` et RIEN
d'autre. Le bloc reçoit les arguments du syscall DANS L'ORDRE EXACT de
l'API NT (déjà placés par l'appelant — charte § 4) et le numéro de service
dans rax ; il exécute le seul remappage que le noyau exige (rcx→r10) puis
l'instruction ; le NTSTATUS rendu traverse tel quel. Six octets, aucune
entrée IAT, aucun autre appel : le trombone ABI du domaine.
Contrat :
  pre  : P1 rax = le SSN (le numéro de service, une DONNÉE chargée par
             l'appelant — charte § 1 : jamais un octet de code, jamais une
             constante du plan d'adressage) ;
         P2 rcx, rdx, r8, r9 et la pile à [rsp+0x28] et au-delà portent les
             arguments du syscall DANS L'ORDRE DE L'API NT (l'appelant a
             fait le travail msx64 — ombre 0x20 comprise : ce que le noyau
             voit à [rsp+0x28] est le 5e argument, exactement comme dans
             un stub ntdll natif) ;
         P3 la pile est alignée 16 à l'entrée (convention msx64 ordinaire —
             l'appelant a traité sys-01 comme toute fonction).
  post : Q1 l'instruction syscall exécutée UNE fois, au site unique du
             bloc (site déclaré — l'oracle du jalon le comptera : exactement
             un, jamais deux) ;
         Q2 rax = le NTSTATUS rendu par le noyau, TEL QUEL (la table des
             verdicts appartient à l'APPELANT — charte § 5 : ce bloc ne
             nomme rien, il émet et rend) ;
         Q3 rcx et r11 sont DÉTRUITS (le coup du noyau : rcx reçoit
             l'adresse de retour utilisateur, r11 les drapeaux — l'appelant
             ne compte JAMAIS sur eux après l'appel) ;
         Q4 la pile est inchangée à l'entrée près (le `ret` rend la main —
             aucun mot poussé, aucun ajustement : charte § 4).
  inv  : I1 le bloc ne déclare AUCUNE entrée IAT, AUCUN appel direct
             (charte § 3 — le site syscall est l'unique interaction
             système) ;
         I2 rax n'est JAMAIS écrit avant l'instruction syscall (le SSN de
             l'appelant traverse — écrire rax avant serait détourner le
             numéro, le défaut le plus grave du domaine) ;
         I3 AUCUN prologue de pile : aucun push, aucun sub rsp, aucune
             écriture à [rsp-…] (charte § 4 — la pile de l'appelant EST la
             pile du syscall : le noyau lit [rsp+0x28] AU MOMENT de
             l'instruction, un mot de décalage décalerait TOUS les
             arguments de pile) ;
         I4 aucun registre non volatil touché (rbx, rbp, rdi, rsi, r12-r15
             traversent intacts — le bloc n'a rien à garder) ;
         I5 le bloc ne détient AUCUN état (charte § 6 — rien en .data,
             rien en .bss, aucune écriture mémoire du tout) ;
         I6 le `ret` suit IMMÉDIATEMENT le site syscall (aucune
             instruction entre les deux — après le verdict du noyau, la
             main rendue est la suivante) ;
         I7 la croissance du slot est NOP, 0x90 (la convention de la lignée
             win depuis M0 — build_m0.py pose `octets + b"\x90" * pad` ; les
             zones RÉSERVÉES inter-blocs seules sont int3 ; erratum M8-(b) :
             la couche I naissante disait « int3, le reste du slot en
             0xCC » — sur pièces, le padding de slot de toute la lignée
             est NOP) ;
