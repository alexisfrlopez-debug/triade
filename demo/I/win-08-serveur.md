win-08 · serveur d'acceptation (thread) · révision 3
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
         assuré par le scénario win-09 en tête, I0, D42).
  post : Q1 tcp-01 = 0 (échec) : DRAPEAU_SRV (0x3880) = 2, ligne d'échec au
         journal graphique, thread terminé — la démonstration continue et
         affichera l'impossibilité réseau ; Q2 succès : R_LISTEN (0x3810) =
         socket d'écoute, DRAPEAU_SRV = 1, boucle : accept → client ≥ 0 :
         spawn(tcp-09, client), handle sauvé en registre préservé (r13),
         handle fermé dès retour, boucle suivante ; accept < 0 (R_QUIT armé
         par le scénario, socket d'écoute fermée) : thread terminé
         proprement ; Q3 aucun ExitProcess ici (un thread de service ne tue
         jamais la fenêtre — leçon contrastée de tcp-12).
  inv  : I1 appels directs limités aux blocs scellés tcp-01/02/06 et à
         l'entrée scénario de win-05 (ligne d'échec seule) ; CloseHandle
         seul appel IAT kernel32 direct ; I2 l'état partagé passe par les
         slots .data hérités de M2 (R_LISTEN, R_QUIT, DRAPEAU_SRV nouveau)
         — aucune nouvelle donnée de synchronisation ; I3 arrêt PROPRE
         exigé : le scénario arme R_QUIT et ferme l'écoute, accept échoue,
         le thread sort (miroir tcp-12, Q3) ; I4 (D43) la socket cliente
         vit en r12 et le handle de thread en r13 (registres préservés) —
         ce bloc ne s'appuie JAMAIS sur un volatile à travers un appel
         (leçon D38) ; en chemin nominal le bloc n'écrit AUCUNE ligne de
         journal : la preuve de vie du serveur vit dans le scénario
         (J_SRV_OK/J_CLI_OK après vérification), pas dans des traces.
Échecs :
  E1 : port 25000 occupé (echo.exe encore lancé) — Q1 : défaillance PUBLIÉE
       (drapeau 2), pas de crash, l'utilisateur est invité à fermer echo.exe.
  E2 : spawn échoue — arrêt du thread serveur (défense minimale), drapeau
       laissé à 1 : le scénario constatera l'échec d'échange.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : shims tcp-01 (via ws2 shims) OK → R_LISTEN + drapeau 1 +
       accept scriptés (client, puis -1 après R_QUIT armé) → spawns tcp-09
       observés et journal FICHIER VIDE en chemin nominal (R3 : toute ligne
       parasite — sonde oubliée — fait échouer l'oracle) ; tcp-01 = 0 →
       drapeau 2 + ligne d'échec (couvre Q1-Q3, I4).
Fixtures    : néant (les chaînes de sondes S1/S2 de R2 sont retirées avec
              l'instrumentation — D43 : les zones libres qui les portaient
              reviennent à zéro).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D33, D35 ; réutilisation intégrale tcp-01/02/06/09 ;
              D42 (instrumentation bilatérale de l'échange — TEMPORAIRE) ;
              D43 (constat vert terrain demo.8 : « boucle § 5 complète —
              DÉMO OK » 28/28 lignes, S1/S2 lues — retrait de TOUTES les
              sondes, R3 final ; le correctif D42 reste vivant et gardé).

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

RÉVISION 3 (D43 — retrait de l'instrumentation, FINALE de lignée) : le
journal terrain demo.8 (28/28 lignes, « boucle § 5 complète — DÉMO OK »)
a tout validé des deux côtés de la socket : « S1 accept ok » puis « S2 fil
echo lance » lus APRÈS « client : connecté » (la course documentée de R2,
résolue sans incident — aucune ligne mélangée), et la boucle § 5 entière
fermée par memcmp. Le devoir d'instrumentation est ACQUITTÉ : R3 retire
les 8 instructions des sondes S1/S2 et rend au bloc son orchestration nue
(accept → spawn → CloseHandle). La discipline r12/r13 est conservée (I4) :
ce code ne reprend jamais l'habitude morte des volatiles à travers un appel
(D38). Le journal fichier VIDE en chemin nominal devient un verrou (V2) :
une sonde réintroduite en silence ferait échouer l'oracle.
