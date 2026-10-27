win-08 · serveur d'acceptation (thread) · révision 2
Intention : la moitié serveur de la démonstration — initialiser l'écoute par
le bloc scellé tcp-01 (WSAStartup, socket, bind 25000, listen), publier la
socket d'écoute en .data (R_LISTEN, même slot que tcp-12), puis boucler sur
accept (tcp-02) en confiant chaque connexion au thread scellé tcp-09 via
tcp-06 (spawn) — le miroir exact de l'orchestration de tcp-12, sans bannière
ni console : le journal graphique (win-05) remplace la sortie standard.
Contrat :
  pre  : P1 appelé une fois, dans un thread dédié (arg ignoré) ; P2 pile
         alignée ; P3 aucun serveur concurrent sur 25000 (sinon tcp-01
         échoue — le défaut est PRÉVU : DRAPEAU_SRV le publiera) ; P4 la
         section critique R_CS est initialisée AVANT le premier spawn (le
         fil tcp-09 journalise via tcp-11 qui l'exige, P5 de tcp-11 — devoir
         assuré par win-09:R3, D42).
  post : Q1 tcp-01 = 0 (échec) : DRAPEAU_SRV (0x3880) = 2, ligne d'échec au
         journal graphique, thread terminé — la démonstration continue et
         affichera l'impossibilité réseau ; Q2 succès : R_LISTEN (0x3810) =
         socket d'écoute, DRAPEAU_SRV = 1, boucle : accept → client ≥ 0 :
         SONDE S1 (acceptation constatée), spawn(tcp-09, client), handle
         sauvé en registre préservé (r13), SONDE S2 (fil lancé), handle
         fermé dès retour, boucle suivante ; accept < 0 (R_QUIT armé par le
         scénario, socket d'écoute fermée) : thread terminé proprement ;
         Q3 aucun ExitProcess ici (un thread de service ne tue jamais la
         fenêtre — leçon contrastée de tcp-12).
  inv  : I1 appels directs limités aux blocs scellés tcp-01/02/06 et à
         l'entrée trace de win-05 (sondes S1/S2, D42) ; CloseHandle seul
         appel IAT kernel32 direct ; I2 l'état partagé passe par les slots
         .data hérités de M2 (R_LISTEN, R_QUIT, DRAPEAU_SRV nouveau) —
         aucune nouvelle donnée de synchronisation ; I3 arrêt PROPRE exigé :
         le scénario arme R_QUIT et ferme l'écoute, accept échoue, le thread
         sort (miroir tcp-12, Q3) ; I4 les sondes ne journalisent que des
         FAITS (retours d'accept/spawn vérifiés avant écriture), jamais un
         succès non prouvé ; I5 le handle de thread vit en r13 (préservé)
         autour de la sonde S2 — les volatils meurent à tout appel (D38).
Échecs :
  E1 : port 25000 occupé (echo.exe encore lancé) — Q1 : défaillance PUBLIÉE
       (drapeau 2), pas de crash, l'utilisateur est invité à fermer echo.exe.
  E2 : spawn échoue — arrêt du thread serveur (défense minimale), drapeau
       laissé à 1 : le scénario constatera l'échec d'échange.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims tcp-01 (via ws2 shims) OK → R_LISTEN + drapeau 1 +
       accept scriptés (client, puis -1 après R_QUIT armé) → spawns tcp-09
       observés + sondes S1/S2 au journal fichier (écran sauté, HWND nul
       dans le cas direct) ; tcp-01 = 0 → drapeau 2 + ligne d'échec
       (couvre Q1-Q3, I4).
Fixtures    : néant (chaînes de sondes S1/S2 en .rdata, zone libre M2
              0x266E-0x26D8 — jamais lue par le chargeur, D42).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33, D35 ; réutilisation intégrale tcp-01/02/06/09 ;
              D42 (instrumentation bilatérale de l'échange — TEMPORAIRE,
              retirée en R3 après constat vert terrain).

RÉVISION 2 (D42 — instrumentation serveur, TEMPORAIRE) : le journal terrain
demo.7 s'arrête à « client : connecté » sans ligne d'échec E5 — mort violente
du processus dans le premier échange réseau. Le diagnostic statique a nommé
le coupable (section critique R_CS jamais initialisée dans l'hôte démo —
correctif win-09:R3) ; les sondes S1/S2 encadrent désormais accept et spawn
dans le fil serveur pour VALIDER le correctif au terrain et localiser toute
mortalité résiduelle côté serveur. RISQUE CONNU ET ACCEPTÉ : ce fil
journalise via win-05 CONCURREMMENT au fil scénario — les tampons .data
(BUF_MIROIR, BUF_CONV) ne sont pas réentrants ; au pire une ligne de sonde
mélangée (jamais un crash : bornes par longueurs), et l'ordre S1/S2 autour
de « client : connecté » n'est pas garanti (course bénigne des deux fils —
toutes les combinaisons sont interprétables au terrain). Les sondes seront
retirées (R3) après le constat vert.
