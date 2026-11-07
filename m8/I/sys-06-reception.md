sys-06 · la réception du transport — le recv AFD bloquant par syscall direct · révision 2
Révision 2 (07/11/2026, l'erratum n° 9 — consigné AVANT le kit, la faute
nommée PAR LA MESURE DE LA MÊME STRUCTURE) : le recoup du premier run
de la sonde sys-05 (Entrée 185) a nommé le coupable à l'instruction
près — le noyau lit buf à +8. Q3 portait « 12 o » pour le WSABUF — UN
WSABUF « PACKÉ » (len 4 + buf 8, SANS le padding d'alignement). Le
WSABUF canonique x64 fait SEIZE octets (len à +0, PADDING d'alignement
4 o, buf à +8) : la pose de la révision 1 (buf à +4) tend au noyau
l'adresse folle — à la réception il ÉCRIRAIT la réponse chez une
adresse folle, STATUS_ACCESS_VIOLATION (0xC0000005), le miroir exact
de la mesure de la sonde à l'émission. La réception n'a JAMAIS couru
sur le terrain réel (les cinq runs mouraient à l'émission, sys-05) :
la faute est nommée AVANT le kit — le C_ASSERT send/recv (la taille de
l'un EST celle de l'autre, 24 o) et le MÊME patron d'instruction (la
pose à +4, relu dans l'artefact scellé) scellent la symétrie du
contrat : le même WSABUF, le même +8. Q3 suit : 16 o + 24 o — la
structure totale fait 40 octets, non 36. Révision 1 : la pose
initiale (l'erratum de lecture AfdFlags/TdiFlags demeure, lui, intact).
Intention : LE GESTE DE RÉCEPTION du socle socket — lire les octets de
l'endpoint établi par NtDeviceIoControlFile(IOCTL_AFD_RECEIVE), le
WSABUF unique pointant LE TAMPON DU KIT (le noyau écrit chez l'appelant :
le bloc ne copie rien, ne touche rien — le tampon est à l'appelant, le
noyau y écrit, le bloc rend le compte), la lecture BLOQUANTE sur le
handle SYNCHRONE (FILE_SYNCHRONOUS_IO_NONALERT posé par sys-04 : le
syscall ATTEND les données — Q2 du socle tls13-28 : « la LECTURE
BLOQUANTE à la réception »), et LE ZÉRO EST LA DEMI-FIN : une lecture
qui rend zéro octet est LE REFUS -7 NOMMÉ (Q2 du socle tls13-28 : « le
zéro de réception [la demi-fin] est le refus -7 du KIT, jamais une
lecture vide silencieuse » — le pair a fermé, le kit tranche).
Provenance : phnt/ntafd.h (AFD_RECV_INFO — le C_ASSERT : la taille du
send EST celle du recv, 24 o) et la mesure WinDbg Windows 11
(leftarcode, partie 4, août 2025). ERRATUM DE LECTURE consigné sur
pièces AVANT la notation (le modèle M8-(b) libc-02, jamais une écriture
faussière laissée debout) : la littérature courante (unknowncheats,
« Native TCP Client Socket ») pose TDI_RECEIVE_NORMAL (0x20) dans le
champ TdiFlags ; LA MESURE WinDbg le pose dans le champ AfdFlags (« I
have experimentally checked and our version is the one that works » —
le dump : BufferArray, BufferCount 1, puis 0x20 en TROISIÈME champ) ;
l'instrument recoupe le dump octet par octet, la notation suivra la
MESURE, le terrain recoupera sur le VRAI — le juge est le code.
Contrat :
  pre  : P1 rcx = la base du module ntdll (l'appelant fournit) ;
         P2 rdx = le handle de l'endpoint (posé par sys-04 — le bloc
             ne l'ouvre pas, ne le ferme pas, ne le possède pas) ;
         P3 r8 = le pointeur du tampon (CHEZ LE KIT : le noyau y
             écrira les octets reçus — le bloc ne fait que pointer) ;
         P4 r9 = la capacité du tampon (1 ≤ r9 ≤ 0xFFFF : un
             enregistrement TLS reçu [5 + L, L ≤ 2^14] + l'étiquette
             AEAD tient dans la borne avec marge ; pointeur nul ou
             capacité nulle : le verdict -5 — aucun syscall émis) ;
         P5 le nom « NtDeviceIoControlFile » vit au fixture .text6
             (SPAN de 21 octets — T5, jamais une seconde copie).
  post : Q1 succès : rax = n ≥ 1, les octets reçus (n = le
             IOSB.Information : le compte du noyau, n ≤ la capacité) —
             le tampon du kit contient les n octets, la lecture est
             BLOQUANTE : le syscall a attendu s'il le fallait (le
             handle synchrone, Event NULL — jamais un compte nul
             silencieux : le zéro est Q2) ;
         Q2 LE ZÉRO EST LA DEMI-FIN : une lecture qui rend zéro octet
             (le pair a fermé proprement) est LE REFUS -7 NOMMÉ (rdx =
             0, le compte consigné — la demi-fin n'est NI un succès NI
             une erreur du noyau : c'est l'ÉVÉNEMENT TRANSPORT que le
             kit doit trancher ; le bloc ne le masque JAMAIS en
             succès) ;
         Q3 le WSABUF et l'AFD_RECV_INFO sont construits sur la PILE
             du bloc (16 o + 24 o, zones mortes au retour) : le WSABUF
             CANONIQUE x64 — len à +0 (4 o), le PADDING d'alignement
             4 o, buf à +8 (8 o) : JAMAIS un « packé » de 12 o, le
             noyau lit buf à +8 ; le BufferArray pointe le WSABUF de
             pile, le WSABUF porte la capacité et LE TAMPON DU KIT
             (P3), BufferCount = 1,
             AfdFlags = TDI_RECEIVE_NORMAL (0x20 — LA MESURE, l'erratum
             ci-dessus : la réception NORMALE qui purge la file du
             noyau), TdiFlags = 0 ;
         Q4 l'appel porte les DIX arguments NT dans l'ordre (handle,
             Event NULL, ApcRoutine NULL, ApcContext NULL, l'IOSB de
             pile, l'IOCTL_AFD_RECEIVE du plan, l'AFD_RECV_INFO de
             pile, sa taille 24, NULL, 0) ;
         Q5 échecs nommés (la table des HUIT) : -5 le span invalide
             (aucun syscall émis) ; -1 la résolution a échoué (rdx = la
             cause, AUCUN syscall émis — I5) ; -6 le syscall a rendu
             un STATUS non nul (rdx = le NTSTATUS brut consigné —
             p. ex. STATUS_CONNECTION_RESET : le pair a coupé BRUTA-
             LEMENT, le STATUS le NOMME, jamais muet ; la divergence
             rax/IOSB.Status est -6) ; -7 la demi-fin (Q2 — le zéro
             propre du pair).
  inv  : I1 AUCUN IAT (charte § 3 — le recv SANS ws2_32.recv) ;
         I2 AUCUNE COPIE : le noyau écrit DIRECTEMENT chez l'appelant
             (le bloc ne touche pas au tampon : il pointe — miroir
             I2 de sys-05, l'adaptateur du socle) ;
         I3 le SSN est résolu AU GESTE MÊME par sys-02 (charte § 6) ;
         I4 l'IOCTL_AFD_RECEIVE (0x12017) et TDI_RECEIVE_NORMAL
             (0x20) sont les constantes du plan d'adressage (T5 —
             dérivées/citées, jamais des littéraux de notation hors
             plan) ;
         I5 échec de résolution = AUCUN syscall émis ;
         I6 les registres non volatils sont intacts ; la pile rendue
             propre ;
         I7 le bloc ne détient AUCUN état (charte § 6 — aucune
             mémoire de transport, aucun reste de lecture : ce que le
             noyau n'a pas livré appartient à la file du NOYAU, le
             bloc ne met jamais de côté — le KIT reçoit exactement n
             octets et rien de caché) ;
         I8 le reçu est INTEGRE (le bloc ne modifie JAMAIS les octets
             écrits par le noyau — la preuve du kit se joue sur SES
             octets : les canaris du harnais le constateront) ;
         I9 la croissance du slot est NOP, 0x90.
