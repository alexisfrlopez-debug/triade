sup-31 · lanceur de processus (CreateProcessA) · révision 1
Intention : l'unique frontière process du superviseur — TOUT lancement
(demo.exe, proxy.exe, curl.exe x4) passe par elle. Deux modes : sans tuyaux
(les processus console muets — curl écrit dans des fichiers par -o) et
avec tuyaux (proxy.exe : stdin alimenté par nous pour "quit", stdout
capturé ligne à ligne). Le répertoire de travail de l'enfant est FORCÉ au
répertoire de l'exécutable du superviseur (construit sur pile à chaque
appel) : demo.exe écrit demo_journal.txt À CÔTÉ des exécutables même si
le superviseur est lancé depuis un autre répertoire courant.
Contrat :
  pre  : P1 rcx = ligne de commande ASCII NUL-terminée (l'exécutable est
         le premier jeton — CreateProcessA résout par répertoire de
         l'application puis System32 puis PATH ; curl.exe est un composant
         système Windows 10/11) ; P2 rdx = mode tuyaux : 0 = aucun
         (STARTUPINFO sans USESTDHANDLES, handles non hérités), 1 = tuyaux
         proxy (stdin/stdout/stderr de l'enfant branchés sur deux tuyaux
         anonymes créés ici) ; P3 ETAT_SUP prêt (.data) ; P4 pile alignée.
  post : Q1 mode 1 : CreatePipe x2 (SECURITY_ATTRIBUTES héritables) ->
         TUYAU_IN_RD/WR et TUYAU_OUT_RD/WR posés ; Q2 STARTUPINFOA sur
         pile (cb 0x68, STARTF_USESTDHANDLES si mode 1, hStdInput =
         TUYAU_IN_RD, hStdOutput = hStdError = TUYAU_OUT_WR) ; Q3
         lpCurrentDirectory = répertoire de l'exécutable (GetModuleFileNameA
         sur pile, tronqué au dernier séparateur, NUL posé) ; Q4
         CreateProcessA(NULL, cmdline, 0, 0, hérite = mode 1, 0, 0, 0, si,
         pi) : faux -> rax = 0, GetLastError tracé par l'APPELANT (ce bloc
         ne journalise pas — il est sous le journal) ; Q5 succès :
         HPROC = pi.hProcess, PID = pi.dwProcessId, hThread fermé
         immédiatement (CloseHandle scellé par IAT), extrémités ENFANT des
         tuyaux fermées (TUYAU_IN_RD, TUYAU_OUT_WR — le parent garde
         l'écriture stdin et la lecture stdout), rax = 1 ; Q6 en mode 0,
         TUYAU_* intacts (jamais touchés).
  inv  : I1 un seul CreateProcessA par appel — aucune retry, aucune
         fantaisie ; I2 la STARTUPINFO et le chemin courant vivent sur
         pile (aucun état .data au-delà d'ETAT_SUP) ; I3 les handles
         fuits sont interdits : tout handle créé ici est soit posé dans
         ETAT_SUP, soit fermé avant le retour ; I4 l'héritage n'est
         demandé QU'en mode 1 (mode 0 : bInheritHandles = 0 — les enfants
         muets n'héritent de rien).
Échecs :
  E1 : CreatePipe échoue -> rax = 0 (aucun tuyau posé, l'appelant
       journalise l'absence).
  E2 : CreateProcessA échoue (exe absent, chemin invalide) -> rax = 0,
       ETAT_SUP inchangé, tuyaux éventuels laissés à l'appelant (il les
       ferme par le chemin d'échec) — hmm, NON : fermeture IMMÉDIATE des
       quatre extrémités ici-même avant rax = 0 (I3 : zéro fuite même en
       échec).
  E3 : GetModuleFileNameA échoue (impossible en pratique) -> répertoire
       courant NULL passé (héritage du parent) — dégradation documentée,
       le lancement continue.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation — mode 0 : CreateProcessA appelé avec cmdline exacte,
       héritage 0, SI sans USESTDHANDLES, cwd = "C:\sup" ; mode 1 :
       tuyaux créés, SI branché, héritage 1, extrémités enfant fermées
       après le lancement (ordres observés).
  V3 : échec piloté CreateProcessA = 0 -> rax = 0, quatre extrémités
       fermées (zéro fuite prouvé par la liste des CloseHandle).
  V4 : falsification — inverser le flag d'héritage fait échouer V2
       (tuyaux non hérités -> l'enfant ne peut pas écrire).
Fixtures    : aucune (cmdlines composées par les appelants).
Provenance  : écrite-avant-code.
Décisions   : D48 ; délégation OS assumée : le superviseur ne implémente
              NI TLS NI HTTP — il appelle curl.exe (composant système,
              schannel) exactement comme il appelle ws2_32 pour TCP : la
              frontière mécanique vit dans l'IAT/le process, pas dans le
              code écrit à la main ; cwd forcé (constat terrain D36 : les
              chemins relatifs sont le piège numéro un).
