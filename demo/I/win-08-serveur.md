win-08 · serveur d'acceptation (thread) · révision 1
Intention : la moitié serveur de la démonstration — initialiser l'écoute par
le bloc scellé tcp-01 (WSAStartup, socket, bind 25000, listen), publier la
socket d'écoute en .data (R_LISTEN, même slot que tcp-12), puis boucler sur
accept (tcp-02) en confiant chaque connexion au thread scellé tcp-09 via
tcp-06 (spawn) — le miroir exact de l'orchestration de tcp-12, sans bannière
ni console : le journal graphique (win-05) remplace la sortie standard.
Contrat :
  pre  : P1 appelé une fois, dans un thread dédié (arg ignoré) ; P2 pile
         alignée ; P3 aucun serveur concurrent sur 25000 (sinon tcp-01
         échoue — le défaut est PRÉVU : DRAPEAU_SRV le publiera).
  post : Q1 tcp-01 = 0 (échec) : DRAPEAU_SRV (0x3880) = 2, ligne d'échec au
         journal graphique, thread terminé — la démonstration continue et
         affichera l'impossibilité réseau ; Q2 succès : R_LISTEN (0x3810) =
         socket d'écoute, DRAPEAU_SRV = 1, boucle : accept → client ≥ 0 :
         spawn(tcp-09, client), handle fermé dès retour, boucle suivante ;
         accept < 0 (R_QUIT armé par le scénario, socket d'écoute fermée) :
         thread terminé proprement ; Q3 aucun ExitProcess ici (un thread de
         service ne tue jamais la fenêtre — leçon contrastée de tcp-12).
  inv  : I1 appels directs limités aux blocs scellés tcp-01/02/06 ; CloseHandle
         seul appel IAT kernel32 direct ; I2 l'état partagé passe par les
         slots .data hérités de M2 (R_LISTEN, R_QUIT, DRAPEAU_SRV nouveau) —
         aucune nouvelle donnée de synchronisation ; I3 arrêt PROPRE exigé :
         le scénarme arme R_QUIT et ferme l'écoute, accept échoue, le thread
         sort (miroir tcp-12, Q3).
Échecs :
  E1 : port 25000 occupé (echo.exe encore lancé) — Q1 : défaillance PUBLIÉE
       (drapeau 2), pas de crash, l'utilisateur est invité à fermer echo.exe.
  E2 : spawn échoue — arrêt du thread serveur (défense minimale), drapeau
       laissé à 1 : le scénario constatera l'échec d'échange.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims tcp-01 (via ws2 shims) OK → R_LISTEN + drapeau 1 +
       accept scriptés (client, puis -1 après R_QUIT armé) → spawns tcp-09
       observés ; tcp-01 = 0 → drapeau 2 + ligne d'échec (couvre Q1-Q3).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33, D35 ; réutilisation intégrale tcp-01/02/06/09.
