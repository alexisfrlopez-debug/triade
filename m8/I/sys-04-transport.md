sys-04 · le transport établi — le socket natif par AFD, sans ws2_32 · révision 1
Intention : LA FONDATION I/O que M8 a nommée — ouvrir le second chemin du
réseau : l'endpoint TCP IPv4 par le périphérique AFD DIRECTEMENT
(NtCreateFile sur \Device\Afd\Endpoint), JAMAIS l'IAT ws2_32 (la surface de
hook que le jalon M8 a nommée — le plan M9-(d) le réclame tel quel). Le bloc
est L'ORCHESTRATEUR de la séquence MESURÉE mswsock au connect d'un client
Windows 11 : le handle SYNCHRONE d'abord (NtCreateFile, le EA
AfdOpenPacketXX), le bind IMPLICITE WILDCARD ensuite (IOCTL_AFD_BIND —
le noyau déduit l'adresse source, le domaine n'en choisit JAMAIS), le
connect ENFIN (IOCTL_AFD_CONNECT, le sockaddr distant du kit, boutisme
réseau) — TROIS appels NT, chaque SSN résolu AU GESTE MÊME par sys-02
(charte § 6 : le bloc ne détient rien, chaque appel résout). Provenance :
phnt/ntafd.h (diversenok, Hunt & Hackett, avril 2025) pour les définitions
canoniques ; les mesures WinDbg Windows 11 x64 (« Under the Hood of
AFD.sys », parties 1-2, leftarcode.com, juillet 2025) pour les dumps
octet par octet — recopiés en VECTEURS DORÉS à l'instrument
verifier_specs_m9d.py ; le terrain M9-(f) confrontera le VRAI afd.sys de la
machine du développeur (le témoin consignera la version Windows, charte
§ 2 — la réserve d'ère s'étend au transport).
Contrat :
  pre  : P1 rcx = la base du module ntdll (l'appelant l'obtient et la
             fournit — miroir sys-02:R1 P3 ; la PEB-walk demeure le
             chantier futur nommé) ;
         P2 rdx = le pointeur du sockaddr_in distant (16 octets — le KIT
             construit : family u16 = AF_INET en boutisme machine, port
             u16 et adresse u32 en BOUTISME RÉSEAU, zero[8] ; le domaine
             ne convertit JAMAIS en silence — le format est celui de la
             structure Windows, le kit répond de son boutisme) ;
         P3 r8 = le pointeur u64 de sortie du handle (chez l'appelant —
             l'état vit chez le kit, charte § 6 : le bloc ne le garde
             pas, ne le ferme pas, ne le possède pas) ;
         P4 les fixtures du domaine vivent en .text6 (la réserve .rdata
             M8 est ÉPUIISÉE par K[64], Entrée 172) : le nom
             UTF-16LE du périphérique (42 o avec NUL), le EA complet
             DÉTERMINISTE (54 o : l'en-tête FILE_FULL_EA_INFORMATION, le
             nom AfdOpenPacketXX, la valeur aux SIX DWORD utiles +
             six NULS — la mesure ws2_32 y laisse du bruit de pile
             qu'afd.sys ne lit pas : les notres sont NULS, le transport
             est reproductible), le bind implicite WILDCARD (20 o) et
             les noms de résolution « NtCreateFile »,
             « NtDeviceIoControlFile » — cités par déplacement (T5),
             jamais reconstruits en code.
  post : Q1 succès : rax = 0, le handle SYNCHRONE posé à [P3] —
             l'endpoint AFD TCP IPv4 créé (AF_INET 2, SOCK_STREAM 1,
             IPPROTO_TCP 6 : les paramètres du jalon, portés par le EA
             fixture, jamais des octets de code), bindé WILDCARD (le
             port et l'adresse locale DÉDUITS par le noyau), connecté
             au sockaddr distant : la poignée TCP est ÉTABLIE au retour
             (le connect est SYNCHRONE sur le handle synchrone — le
             syscall attend la fin du three-way handshake, miroir du
             recv bloquant) ;
         Q2 la séquence est LE CONTRAT (la marche mesurée mswsock,
             jamais une invention) : NtCreateFile PUIS
             NtDeviceIoControlFile(BIND) PUIS NtDeviceIoControlFile
             (CONNECT) — les ONZE arguments de NtCreateFile dans
             l'ordre NT (DesiredAccess 0xC0140000, ObjectAttributes —
             construit sur la pile : Length 0x30, RootDirectory 0,
             ObjectName pointant l'UNICODE_STRING du fixture-device
             [Length 40, MaximumLength 42 — ERRATUM DE L'INSTRUMENT : la
             couche I naissante disait « 42/44 », le nom fait 20
             caractères UTF-16LE = 40 octets SANS le NUL, 42 AVEC :
             l'écriture seule était fautive, corrigée sur pièces AVANT
             la notation, le juge est le code], Attributes
             OBJ_CASE_INSENSITIVE 0x40, ni descripteur ni QoS —,
             le IOSB de pile, ShareAccess 3, Disposition FILE_OPEN 1,
             CreateOptions 0x20 FILE_SYNCHRONOUS_IO_NONALERT, le EA
             fixture, sa taille 54) ; les DIX arguments de
             NtDeviceIoControlFile dans l'ordre NT (le handle, Event
             NULL, ApcRoutine NULL, ApcContext NULL, le IOSB de pile,
             l'IOCTL du plan, le buffer d'entrée, sa taille, le buffer
             de sortie [16 o de pile pour le BIND, NULL pour le
             CONNECT], sa taille) ;
         Q3 chaque SSN est résolu AU GESTE MÊME par sys-02 (TROIS
             résolutions : « NtCreateFile », « NtDeviceIoControlFile »,
             « NtDeviceIoControlFile » — jamais un numéro en cache d'un
             appel précédent, miroir Q2 de sys-03 ; le nom
             « NtDeviceIoControlFile » résolu DEUX FOIS : chaque geste
             résout, charte § 6) ;
         Q4 échecs nommés (la table des HUIT — charte § 5 étendue) :
             -1 une résolution a échoué (rdx consigne LA CAUSE : le
                verdict du résolveur, nommé, jamais muet — miroir I7 de
                sys-03) et AUCUN syscall n'est émis pour ce geste : la
                marche s'arrête NOMMÉMENT (un échec de résolution du
                connect n'émet JAMAIS le connect — I5) ;
             -6 un syscall a rendu un STATUS non nul (rdx = le
                NTSTATUS brut consigné — nommé, jamais muet ; le PREMIER
                STATUS non nul arrête la marche : create, bind puis
                connect, l'ordre est le contrat) ; une divergence
                entre le rax rendu et l'IOSB.Status du syscall est -6
                (le noyau ne parle pas deux fois — miroir Q4 de
                sys-03) ; au -6 le handle n'est PAS posé à [P3] (le
                kit ne reçoit JAMAIS un handle d'un établissement
                échoué : aucune possession partielle).
  inv  : I1 AUCUN IAT (charte § 3 : ws2_32 n'est JAMAIS importé — la
             règle structurelle du domaine tient pour le transport ;
             l'oracle structurel du build (e) le constatera : le
             socket natif SANS une seule entrée d'import réseau) ;
         I2 les structures transitoires vivent sur la PILE du bloc
             (l'UNICODE_STRING, l'OBJECT_ATTRIBUTES, les IOSB, le
             AFD_CONNECT_JOIN_INFO_TL de 40 o [SanActive 0 + 7 NUL,
             RootEndpoint 0, ConnectEndpoint 0 — la mesure : les zéros
             SONT acceptés par afd.sys —, le sockaddr du kit COPIÉ à
             +24], la sortie de bind 16 o) : zones mortes au retour —
             aucun état, charte § 6 ;
         I3 le fixture-EA, le nom-device et le fixture-bind sont CITÉS
             par déplacement .text6 (T5 — les constantes du plan
             d'adressage, jamais des octets de code) ; le bind est le
             WILDCARD implicite MESURÉ (flags 2 : le noyau DÉDUIT —
             jamais une adresse choisie par le domaine, jamais un
             port choisi : le domaine ne décide RIEN de la source) ;
         I4 le sockaddr est LU depuis le kit (16 o copiés dans le
             AFD_CONNECT de pile, AUCUNE interprétation des champs —
             le domaine ne valide ni le port ni l'adresse : ce sont les
             données de l'appelant, la validation est l'affaire du
             noyau qui connecte) ;
         I5 échec de résolution = AUCUN syscall émis pour ce geste (la
             garde la plus importante du domaine, miroir I5 de
             sys-03) ;
         I6 l'ordre est LE CONTRAT : jamais connect sans bind, jamais
             bind sans handle — la séquence mesurée mswsock est la
             règle (un connect sans bind serait une invention, un
             bind explicite serait une décision que le domaine n'a
             pas) ;
         I7 les registres non volatils sont intacts (les TROIS appels
             respectent l'ABI, le bloc sauvegarde ce qu'il utilise) ;
         I8 le handle rendu est la DONNÉE du kit (le bloc ne le ferme
             pas au retour — échec ou succès : la fermeture est le
             geste du kit par « NtClose » résolu par sys-02, émis par
             sys-01 ; la fermeture n'est PAS un bloc, le kit
             orchestre) ;
         I9 le verdict -7 n'est PAS celui de l'établissement (le -7
             nomme l'échec D'ÉCHANGE — sys-05/06 ; l'établissement
             échoue par -1/-6 : la table des HUIT est le plan, chaque
             bloc prend ses noms et pas les autres) ;
         I10 la croissance du slot est NOP, 0x90 (la convention de la
             lignée win depuis M0).
