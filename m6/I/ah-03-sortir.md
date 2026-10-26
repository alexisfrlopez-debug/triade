ah-03 · terminaison par appel système · révision 1
Intention : terminer le processus avec un code de sortie — le miroir de
hello-03:R1 (ExitProcess) : le bloc ne revient jamais, le noyau détruit
l'image. Dernier octet exécuté de l'artefact en tout état de cause
réussi ou échoué : son contrat inclut l'obligation d'être atteint.
Contrat :
  pre  : P1 edi contient le code de sortie (u32 ; convention : 0 = succès,
             1 = erreur d'usage ou d'exécution) ;
         P2 pile alignée (rsp ≡ 8 mod 16 — jamais violée : le bloc
             n'exécute aucun call).
  post : Q1 le processus est terminé au retour de l'appel système : le
             code de sortie est propagé au parent (constaté par le lanceur,
             exit ≠ 0 sur les chemins d'échec, 0 sur le chemin nominal) ;
         Q2 le bloc ne retourne jamais (pas de post-condition d'état).
  inv  : I1 appel système : instruction syscall avec rax = 60 (sys_exit)
             exclusivement ;
         I2 feuille terminale : 0 octet de pile, aucun non-volatil ; la
             notation ne contient aucune instruction après syscall (le
             contrat exclut le retour, l'oracle structurel le vérifie) ;
         I3 aucun vidage de tampon : stdout du profil est le pipe/terminal
             du lanceur (write-through par ah-01, pas de tampon utilisateur).
Échecs :
  E1 : aucun — sys_exit ne échoue pas (le noyau ne peut refuser de tuer).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, artefact entier) : hachoir
       rend exactement 0 sur le chemin nominal, 1 sur les chemins
       d'usage et d'erreur (constatés par le lanceur sur chaque vecteur
       doré, couvre Q1).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le code de sortie est la SEULE sortie latérale de
              l'artefact : le profil Linux n'a pas de boîte de dialogue
              d'erreur — tout échec se lit dans le code ou stderr.
