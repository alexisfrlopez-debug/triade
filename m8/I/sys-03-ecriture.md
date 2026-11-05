sys-03 · l'écriture directe — la twin de hello-02 par NtWriteFile · révision 1
Intention : LE premier usage réel du domaine — émettre LA MÊME LIGNE que
hello-02 (WriteFile par l'IAT kernel32, le scellé M0) par NtWriteFile EN
SYSCALL DIRECT : zéro entrée IAT, le SSN résolu au geste même sur la machine
qui exécute. La ligne est le FIXTURE PARTAGÉ de la lignée (celle de
hello-02, citée par déplacement — jamais une seconde copie) ; l'observable
est IDENTIQUE, le chemin est STRUCTURELLEMENT distinct : la preuve du
domaine entier tient dans cette twin (le harnais au labo sur FIXTURES
ntdll, le terrain du développeur sur le VRAI — README, « ce que le domaine
promet »).
Contrat :
  pre  : P1 rcx = la base du module ntdll (l'appelant l'obtient et la
             fournit — sys-03 ne touche AUCUN IAT, pas même
             GetModuleHandleA ; le chantier (c) câblera le principal) ;
         P2 rdx = le handle d'écriture (le même que hello-02 recevrait —
             fourni par l'appelant ; le bloc ne l'ouvre pas, ne le ferme
             pas, ne le possède pas) ;
         P3 les fixtures du domaine vivent en .rdata, cités par
             déplacement : le nom « NtWriteFile » (ASCII, 11 octets — la
             CLEF de la résolution ; erratum M8-(b) : la couche I naissante
             disait « 10 octets », la mesure sur pièces fait foi —
             N-t-W-r-i-t-e-F-i-l-e) et la LIGNE de hello-02 (le fixture
             M0, R7 : la twin n'invente pas sa ligne, elle la CITE —
             33 octets utiles + NUL, « TRIADE M0 : Hello, Windows 11 !
             CRLF », byte-exact le fixture posé par build_m0.py) ;
  post : Q1 succès : rax = 0, la ligne est ÉMISE (octet pour octet le
             fixture de hello-02 — la comparaison est la preuve
             d'observable, elle se joue au harnais ET au terrain) ;
         Q2 le SSN a été résolu AU GESTE MÊME (sys-02 appelé depuis le
             bloc, P1 et le span du fixture-nom — jamais un numéro en
             cache d'un appel précédent : charte § 6, le bloc ne détient
             rien, chaque appel résout) ;
         Q3 l'appel est émis par sys-01 avec les NEUF arguments de
             NtWriteFile dans l'ordre NT : handle (P2), Event = NULL,
             ApcRoutine = NULL, ApcContext = NULL (l'écriture est
             SYNCHRONE — aucun événement, jamais d'attente), l'IO_STATUS_
             BLOCK (sur la PILE du bloc — zone morte au retour, I2), le
             tampon (le fixture-ligne), la longueur (celle du fixture),
             ByteOffset = NULL (position courante — le handle synchrone
             écrit où il en est), Key = 0 ; les quatre premiers en
             registres, les CINQ derniers à [rsp+0x28]+ au moment du
             syscall (charte § 4 — sys-03 appelle sys-01 comme toute
             fonction msx64 : l'ombre et la pile d'appel sont AUSSI celles
             du noyau, c'est le charme du trombone) ;
         Q4 échecs nommés (la table, charte § 5) : -1 la résolution a
             échoué (le verdict de sys-02 négatif — rdx consigne LA CAUSE :
             le verdict du résolveur, nommé, jamais muet) et AUCUN syscall
             n'est émis (I5) ; -6 le syscall a rendu un STATUS non nul
             (rdx = le NTSTATUS brut consigné — nommé, jamais muet) ; une
             divergence entre le rax rendu et le statut de l'IO_STATUS_
             BLOCK est -6 (le noyau ne parle pas deux fois — un désaccord
             est une anomalie, jamais un succès décrété).
  inv  : I1 AUCUN IAT (charte § 3 — la twin se preuve à l'oracle
             structurel : hello-02 DÉCLARE WriteFile, sys-03 ne déclare
             RIEN ; c'est la preuve STRUCTURELLE du domaine) ;
         I2 l'IO_STATUS_BLOCK vit sur la pile du bloc (zone morte au
             retour — aucun état, charte § 6 ; le bloc ne le conserve
             jamais) ;
         I3 les seuls appels directs déclarés : sys-02 puis sys-01 —
             L'ORDRE EST LE CONTRAT (résoudre AVANT d'émettre, jamais
             l'inverse ; un émetteur sans résolution serait un numéro
             gravé déguisé) ;
         I4 le fixture-ligne est celui de hello-02, CITÉ par déplacement
             (R7 — le scellé M0 ne bouge pas, la twin n'écrit pas sa
             propre ligne : une seconde copie serait une divergence
             d'observable en sursis) ;
         I5 échec de résolution = AUCUN syscall émis (jamais un appel au
             numéro deviné — la garde la plus importante du bloc) ;
         I6 les registres non volatils sont intacts (les deux appels
             respectent l'ABI, le bloc sauvegarde ce qu'il utilise) ;
         I7 le NTSTATUS rendu n'est JAMAIS muet : succès = 0 nommé, échec
             = -6 avec le STATUS consigné en rdx (charte § 5 — le miroir
             de tls-02 : le code brut accompagne, il ne remplace pas) ;
         I8 la croissance du slot est NOP, 0x90 (la convention de la
             lignée win depuis M0 — erratum M8-(b) : la couche I naissante
             disait « int3 », sur pièces le padding de slot est NOP).
