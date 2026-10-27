sup-11 · journal fichier horodaté · révision 1
Intention : le jumeau fichier de win-11 démo, au contrat identique (modes
0/1/2, ouverture paresseuse, append atomique, flush forcé), UNE différence
structurelle : le nom du fichier vient de .data (TAMPON_NOM, posé par
sup-21) et non d'une chaîne .rdata figée — chaque run écrit SON
terrain_YYYYMMDD_HHMMSS.txt à côté de l'exécutable. Le relais queue de
win-05 scellé (jmp 0x1E00) appelle CE bloc : mêmes registres, mêmes
modes, zéro changement pour les appelants (R4 — le remplacement honore le
contrat publié de win-11:R1).
Contrat :
  pre  : P1-P6 de win-11:R1 inchangées (rcx texte, rdx longueur, r8d mode
         0/1/2, r9d valeur, bornes len <= 100 / nchars <= 60, pile
         alignée, appelable de tout thread) ; P2 TAMPON_NOM posé par
         sup-21 AVANT la première ligne (sinon chemin vide -> échec
         d'ouverture, handle -1, retour 0 : dégradation propre).
  post : Q1-Q5 de win-11:R1 (append + CRLF idempotent, FILE_APPEND_DATA +
         CREATE_ALWAYS, rax 1/0, re-tentative après échec) ; Q3 adaptée :
         chemin = répertoire de l'exécutable (GetModuleFileNameA, scan
         arrière du séparateur) + TAMPON_NOM (28 o recopiés — le NUL
         compris) ; Q6 conversion mode 2 identique (0x2192 -> '>', >=
         0x100 -> '-', sinon octet bas).
  inv  : I1-I5 de win-11:R1 (libc scellées memcpy/itoa/strlen, imports
         kernel32#2 exclusivement, états .data bornés, conversion inline) ;
         I4 adapté : JOURNAL_HANDLE (0x3888), BUF_CONV (0x3890, 128 o),
         BUF_CHEMIN (0x3910, 304 o), SCRATCH_ECRIT (0x3A40) — mêmes
         adresses que la démo (win-05 scellé ne touche que BUF_MIROIR et
         HWND_JOURNAL, inchangés) ; I6 BUF_CHEMIN reste VALIDE après
         ouverture (jamais réécrit par ce bloc) — sup-35 le relit pour
         téléverser le journal (le chemin complet du journal est la
         propriété de ce tampon, unique propriétaire : ce bloc).
Échecs :
  E1-E3 de win-11:R1 (GetModuleFileNameA, CreateFileA, WriteFile) —
       handle -1, rax = 0, re-tentative au prochain appel.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : modes — "abc" -> "abc\r\n" ; "gle=" + 1400 -> "gle=1400\r\n" ;
       UTF-16 « écho → — » -> octets E9 'c' 'h' 'o' 20 3E 20 2D.
  V3 : chemin — GetModuleFileNameA simulé "C:\sup\superviseur.exe" ->
       CreateFileA appelé sur "C:\sup\terrain_20261027_093012.txt"
       (TAMPON_NOM recopié au séparateur, NUL compris).
  V4 : paresse — aucune API fichier avant la première ligne.
  V5 : échec CreateFileA -> 0, pas d'écriture, re-tentative suivante.
  V6 : multi-lignes — ordre et contenu exacts de N invocations.
  V7 : DIFFÉRENCIATION — le chemin ouvert finit par ".txt" du run, JAMAIS
       par "demo_journal.txt" (le journal du superviseur ne peut pas
       écraser celui de la démo testée : collision impossible par nom).
Fixtures    : TAMPON_NOM (.data, posé par sup-21 — fixture vivante, pas
              .rdata : le nom change à chaque run).
Provenance  : écrite-avant-code.
Décisions   : D48 ; contrat calqué win-11:R1 (R4 — les appelants scellés
              win-05/ne changent pas) ; nom dynamique = la seule différence.
