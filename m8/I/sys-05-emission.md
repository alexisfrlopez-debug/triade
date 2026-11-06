sys-05 · l'émission du transport — le send AFD par syscall direct · révision 2
Révision 2 (07/11/2026, le recoup du premier run de la sonde sys-05 —
Entrée 185) : Q3 portait « 12 o » pour le WSABUF — UN WSABUF « PACKÉ »
(len 4 + buf 8, SANS le padding d'alignement). Le WSABUF canonique x64
fait SEIZE octets (len à +0, PADDING d'alignement 4 o, buf à +8) : le
noyau lit buf à +8, quatre octets TROP TÔT — l'adresse lue est folle et
le noyau rend STATUS_ACCESS_VIOLATION (0xC0000005), la mesure même de la
sonde (le -6 des cinq runs, nommé à l'instruction près). I2 suit :
40 octets de structure, non 36. Révision 1 : la pose initiale.
Intention : LE GESTE D'ÉMISSION du socle socket — émettre une charge sur
l'endpoint établi par sys-04 par NtDeviceIoControlFile(IOCTL_AFD_SEND),
le WSABUF unique pointant la charge DU KIT (aucune copie : les octets
appartiennent à l'appelant, miroir Q4 du socle tls13-28), le SSN résolu
au geste même. LA RÈGLE DU KIT : l'émission est TOTALE ou refusée — le
compteur du IOSB (Information) doit couvrir la longueur demandée, un
envoi partiel est LE REFUS -7 NOMMÉ (Q3 du socle tls13-28 : « un envoi
partiel est le refus du kit » — jamais une boucle silencieuse, jamais un
succès décrété sur une moitié). Provenance : phnt/ntafd.h (AFD_SEND_INFO)
et la mesure WinDbg Windows 11 (leftarcode, partie 3, juillet 2025 :
l'AFD_SEND_INFO de 24 o [BufferArray ptr, BufferCount 1, AfdFlags 0,
TdiFlags 0] — le dump octet par octet recopié à l'instrument) ; le noyau
accepte les grandes charges d'un coup (la mesure : 10 Mio testés) — la
réception TOTALE par le pair est l'affaire du TCP de la machine, le
compteur du IOSB tranche au retour.
Contrat :
  pre  : P1 rcx = la base du module ntdll (l'appelant fournit, miroir
             sys-02:R1 P3) ;
         P2 rdx = le handle de l'endpoint (celui que sys-04 a posé —
             le bloc ne l'ouvre pas, ne le ferme pas, ne le possède
             pas) ;
         P3 r8 = le pointeur de la charge (les octets de l'appelant —
             AUCUNE copie : le WSABUF pointe CE pointeur) ;
         P4 r9 = la longueur de la charge (1 ≤ r9 ≤ 0xFFFF : la charge
             d'un enregistrement TLS [5 + 2^14 + 17 = 16406] tient
             dans la borne avec marge ; r9 nul ou pointeur nul : le
             verdict -5, le span invalide — charte § 5 ; la borne ne
             devine jamais ce que le kit voudra demain : le WSABUF
             porte un u32, la marge est celle du jalon) ;
         P5 le nom « NtDeviceIoControlFile » vit au fixture .text6
             (SPAN de 21 octets, cité par déplacement — T5).
  post : Q1 succès : rax = 0 — TOUT est émis (le IOSB.Information ==
             la longueur demandée : la charge est partie AU COMPLET,
             le noyau l'a acceptée d'un geste) ;
         Q2 l'émission PARTIELLE est LE REFUS -7 NOMMÉ (rdx = le
             compte Information du IOSB — les octets reconnus partis,
             consignés, jamais muets) : le kit décide de la suite
             (réessayer, fermer, renoncer) — le bloc ne boucle JAMAIS
             en silence (une boucle d'envoi serait une décision de
             transport que le domaine n'a pas : le refus nommé est la
             règle, miroir de l'échec propre — charte § 5) ;
         Q3 le WSABUF et l'AFD_SEND_INFO sont construits sur la PILE
             du bloc (16 o + 24 o, zones mortes au retour) : le WSABUF
             CANONIQUE x64 — len à +0 (4 o), le PADDING d'alignement
             4 o, buf à +8 (8 o) : JAMAIS un « packé » de 12 o, le
             noyau lit buf à +8 ; le BufferArray pointe le WSABUF de
             pile, le WSABUF pointe la charge du kit (P3),
             BufferCount = 1, AfdFlags = 0,
             TdiFlags = 0 (la MESURE du send — leftarcode p.3 : aucun
             drapeau, le Fast I/O du noyau) ;
         Q4 l'appel porte les DIX arguments NT dans l'ordre (handle,
             Event NULL, ApcRoutine NULL, ApcContext NULL, l'IOSB de
             pile, l'IOCTL_AFD_SEND du plan, l'AFD_SEND_INFO de pile,
             sa taille 24, NULL, 0 — aucune sortie attendue : la
             réponse est le IOSB) ;
         Q5 échecs nommés (la table des HUIT) : -5 le span invalide
             (pointeur nul ou longueur nulle — aucun syscall émis) ;
             -1 la résolution a échoué (rdx = la cause du résolveur,
             AUCUN syscall émis — I5) ; -6 le syscall a rendu un STATUS
             non nul (rdx = le NTSTATUS brut consigné ; la divergence
             rax/IOSB.Status est -6 — le noyau ne parle pas deux fois,
             miroir sys-03) ; -7 l'émission partielle (Q2).
  inv  : I1 AUCUN IAT (charte § 3 — le send SANS ws2_32.send, la
             règle structurelle TENUE) ;
         I2 AUCUNE COPIE de la charge (les octets appartiennent à
             l'appelant — le bloc ne touche que les 40 octets de
             structure de sa pile : miroir tls13-28 Q4, l'adaptateur) ;
         I3 le SSN de « NtDeviceIoControlFile » est résolu AU GESTE
             MÊME par sys-02 (jamais un numéro en cache — charte § 6) ;
         I4 l'IOCTL_AFD_SEND (0x1201F) est la constante du plan
             d'adressage, DÉRIVÉE par la macro canonique (jamais un
             littéral de notation hors plan, T5) ;
         I5 échec de résolution = AUCUN syscall émis (la garde du
             domaine) ;
         I6 les registres non volatils sont intacts ; la pile rendue
             propre (cadre détrait au retour) ;
         I7 le bloc ne détient AUCUN état (charte § 6 — ni séquence,
             ni compte cumulé : le transport est SANS ÉTAT, chaque
             émission est un geste neuf) ;
         I8 la croissance du slot est NOP, 0x90.
