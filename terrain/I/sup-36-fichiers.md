sup-36 · fichiers du terrain (lire/écrire/supprimer, préfixe répertoire) · révision 1
Intention : le facteur commun des trois tests — TOUT fichier du superviseur
(demo_journal.txt lu, terrain_req.txt écrit, terrain_jeton.json lu,
terrain_page_http.txt lu puis supprimé…) vit À CÔTÉ DE L'EXÉCUTABLE, pas
dans le répertoire courant de lancement (le piège numéro un du terrain,
D36). Ce bloc compose chemin = répertoire de l'exécutable + nom, une seule
fois pour toutes : la longueur du préfixe (DIR_LONG) est calculée au
premier appel puis cachée en .data — un seul propriétaire du calcul, les
lectures/écritures/suppressions des tests n'ont plus qu'à nommer le
fichier. Sans lui, chaque test porterait sa propre copie du balayage
arrière de BUF_CHEMIN.
Contrat :
  pre  : P1 rcx = nom de fichier ASCII NUL-terminé (lu dans les zones
         données sup, ex. "demo_journal.txt") ; P2 edx = opération :
         0 = lire, 1 = écrire, 2 = supprimer ; P3 r8d = longueur du nom
         (NUL compris) ; P4 [écriture] r9d = longueur du contenu, posé à
         TAMPON_CMD+ZONE_COMPO par l'appelant ; P5 BUF_CHEMIN valide
         (journal ouvert au moins une fois — sup-09 trace S00/S01 avant
         tout test) ; P6 pile alignée.
  post : Q1 premier appel : balayage arrière de BUF_CHEMIN (strlen scellé
         + marche jusqu'au séparateur 0x5C) -> DIR_LONG posé (préfixe,
         séparateur compris) ; appels suivants : cache lu, zéro rescan ;
         Q2 TAMPON_CMD = BUF_CHEMIN[0..DIR_LONG) + nom (memcpy scellées
         x2) ; Q3 lire : CreateFileA(GENERIC_READ, OPEN_EXISTING) ->
         INVALID_VALUE = rax 0 (absent/erreur, honnête) ; sinon ReadFile
         (MAX_LECTURE 640 o, LU posé en .data), CloseHandle, rax = LU ;
         le contenu écrase TAMPON_CMD depuis +0 (jamais au-delà de
         MAX_LECTURE) ; Q4 écrire : CreateFileA(GENERIC_WRITE,
         CREATE_ALWAYS) -> WriteFile(TAMPON_CMD+ZONE_COMPO, r9d),
         CloseHandle, rax = 1/0 ; Q5 supprimer : DeleteFileA(TAMPON_CMD),
         rax = son retour ; Q6 op inconnue -> rax = 0 (fail-closed).
  inv  : I1 zéro fuite : tout handle ouvert est fermé sur TOUT chemin,
         y compris échec d'écriture ; I2 le chemin composé ne dépasse
         jamais TAMPON_CMD (DIR_LONG ≤ 304, nom ≤ 20) ; I3 DIR_LONG est
         la propriété EXCLUSIVE de ce bloc (poseur unique) — les tests ne
         le lisent jamais directement, ils passent par les opérations ;
         I4 aucune interprétation du contenu lu (octets bruts, la
         sémantique appartient à l'appelant) ; I5 libc scellées
         (memcpy/strlen) et IAT kernel32 exclusivement.
Échecs :
  E1 : fichier absent (lecture) -> rax = 0 — chemin nominal d'échec, pas
       une exception (le sondage du journal démo vit dessus).
  E2 : CreateFileA en écriture échoue (disque plein, droits) -> rax = 0,
       handle INVALID non posé.
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation — lire "terrain_jetons.bin" servi (4 champs) -> rax = 4
       champs lisibles dans TAMPON_CMD, LU exact ; écrire "terrain_req.txt"
       (contenu 280 o à +ZONE_COMPO) -> CreateFileA(CREATE_ALWAYS) +
       WriteFile exact observés ; supprimer -> DeleteFileA sur le chemin
       préfixé exact.
  V3 : DIR_LONG — premier appel le calcule (balayage arrière observé :
       un seul appel strlen), second appel zéro rescan (compteur strlen).
  V4 : absent -> rax = 0, aucun ReadFile.
  V5 : falsification — corrompre le décalage ZONE_COMPO d'un octet fait
       échouer le verrou d'écriture (contenu décalé).
Fixtures    : noms de fichiers (zone données sup 2), DIR_LONG/ZONE_COMPO
              (plan), MAX_LECTURE (64 o de marge sous TAMPON_CMD+688).
Provenance  : écrite-avant-code (né du dimensionnement D48 : sans
              facteur commun, les trois blocs de test débordaient leurs
              slots de cent cinquante octets chacun).
Décisions   : D48 ; le répertoire de travail forcé de sup-31 (côté
              enfant) et le préfixe DIR_LONG de sup-36 (côté parent) sont
              les deux faces du correctif D36 (les chemins relatifs ne
             existent pas) ; cache .data plutôt que registre persistant
              (les tests s'appellent entre appels, aucun registre ne
              survit).
