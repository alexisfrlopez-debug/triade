win-11 · journal fichier (trace terrain) · révision 1
Intention : donner une voix au terrain — chaque étape de la démonstration
s'écrit dans un fichier de trace posé À CÔTÉ de l'exécutable
(demo_journal.txt), avec les codes GetLastError des échecs : quand l'écran
ne parle pas (fenêtre invisible, crash précoce, réseau muet), le fichier,
lui, raconte la dernière étape franchie. C'est la réponse directe au constat
D36 : « ça ne fonctionne pas » sans logs est indiagnosticable.
Contrat :
  pre  : P1 rcx pointe le texte : ASCII (modes 0/1) ou UTF-16LE (mode 2),
         longueur portée par rdx (octets en 0/1, CHARS en 2) ; P2 r8d = mode :
         0 = ligne ASCII telle quelle, 1 = préfixe ASCII + valeur r9d en
         décimal, 2 = conversion UTF-16 → octet (Latin-1 : 0x2192 → '>',
         tout point ≥ 0x100 → '-', sinon octet bas) ; P3 r9d = valeur u32
         (mode 1 uniquement, ignoré sinon) ; P4 bornes dures : len ≤ 100 en
         modes 0/1, nchars ≤ 60 en mode 2 (BUF_CONV = 128 o, CRLF inclus) ;
         P5 pile alignée (rsp ≡ 8 mod 16) ; P6 appelable de tout thread.
  post : Q1 la ligne + "\r\n" est écrite AU BOUT du fichier (CRLF ajouté
         seulement si absent — mode 2 idempotent : une ligne déjà terminée
         n'est pas doublée) (CreateFileA en
         FILE_APPEND_DATA : chaque WriteFile est atomique, multi-threads
         sûrs) puis FlushFileBuffers forcé (trace survivant à un crash) ;
         Q2 rax = 1 si écrit ; Q3 première invocation (ou après échec) :
         chemin construit = répertoire de l'exécutable (GetModuleFileNameA,
         scan arrière du dernier séparateur) + "demo_journal.txt",
         CreateFileA CREATE_ALWAYS (chaque lancement repart d'un fichier
         neuf) ; Q4 échec d'ouverture : handle marqué -1, rax = 0, aucune
         écriture — la tentative est rejouée à l'appel suivant (état
         transitoire récupérable) ; Q5 échec d'écriture : handle marqué -1,
         rax = 0, re-ouverture tentée au prochain appel.
  inv  : I1 ouvertures paresseuses : aucune API fichier appelée avant la
         première ligne ; I2 la composition passe par les blocs scellés
         libc-01 (memcpy préfixe), libc-04 (itoa décimal), libc-03 (strlen)
         — réutilisation M1, aucun reformateur local ; I3 imports
         kernel32#2 exclusivement (GetModuleFileNameA, CreateFileA,
         WriteFile FT commune, FlushFileBuffers, GetLastError) — descripteur
         d'import distinct, l'IAT kernel32 historique (0x20B0) reste
         intouchée (R7) ; I4 les seuls états touchés : JOURNAL_HANDLE
         (0x3888), BUF_CONV (0x3890), BUF_CHEMIN (0x3910), SCRATCH_ECRIT
         (0x3A40) — tous en zone .data non scellée ; I5 la conversion
         mode 2 ne dépend d'aucune table externe (map inline, 3 cas).
Échecs :
  E1 : GetModuleFileNameA échoue (rax = 0) — impossible en pratique
       (l'exécutable existe) — handle -1, retour 0, pas de crash.
  E2 : CreateFileA échoue (répertoire en lecture seule, fichier verrouillé
       par un éditeur) — handle -1, retour 0 : la démonstration continue
       (le fichier est un confort de diagnostic, pas une dépendance).
  E3 : WriteFile échoue (disque plein) — handle -1, retour 0, re-essayé
       à la ligne suivante.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : mode 0 « abc » → fichier "abc\r\n" ; mode 1 préfixe
       "gle=" valeur 1400 → "gle=1400\r\n" ; mode 2 UTF-16 « écho → — » →
       octets E9 'c' 'h' 'o' 20 3E 20 2D (Latin-1 + maps) ; V3 chemin :
       GetModuleFileNameA simulé "C:\demo\demo.exe" → CreateFileA appelé
       sur "C:\demo\demo_journal.txt" (scan du séparateur prouvé) ; V4
       paresse : aucune ouverture avant la première ligne ; V5 échec
       CreateFileA → retour 0, pas d'écriture, re-tentative à l'appel
       suivant (Q4) ; V6 multi-lignes : ordre et contenu exacts de N
       invocations.
Fixtures    : chaînes ASCII .rdata (NOM_FICHIER "demo_journal.txt" + les
              préfixes L00/L01/L02/L03/LKO_* de win-02/04).
Provenance  : écrite-avant-code.
Décisions   : D36 (trace terrain), D7 (imports kernel32#2), D8 ; miroir
              fichier de tcp-11/win-05 ; FILE_APPEND_DATA pour l'atomicité
              inter-threads ; CREATE_ALWAYS pour un fichier neuf à chaque
              lancement.
