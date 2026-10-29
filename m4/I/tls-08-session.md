tls-08 · session TLS cliente · révision 1
Intention : orchestrer une session TLS cliente complète de bout en bout —
connexion, poignée de main, émission chiffrée de la requête, relais du
flux déchiffré vers le client, arrêt — L'unique propriétaire de la socket
serveur TLS et de la compensation intégrale (charte § 4) : tout chemin
termine avec exactement les mêmes libérations, dans le même ordre.
Contrat :
  pre  : P1 rcx pointe le cadre de session TLS (zone de travail complète :
             handles, zones jetons/émission/réception, nom traduit,
             compteurs) — le cadre est fourni VIERGE par http-10:R2, qui
             en est le propriétaire mémoire ;
         P2 rdx pointe le paquet de session (spans : autorité cible
             [hôte, port], requête claire réécrite en forme origine
             [préparée par http-10:R2 — la réécriture absolu → origine
             reste propriété http-10], socket cliente, contexte de
             réponse) ;
         P3 le thread appelant est le thread session de http-10 (aucun
             thread créé ici — les threads appartiennent à tcp-06 via
             http-10, inchangé depuis M2).
  post : Q1 succès complet : rax = 0 — connexion tcp-13, nom tls-01,
             handles tls-05, poignée tls-04 (console tcp-11 : « tunnel
             chiffre etabli » — état nommé, AUCUN secret), requête émise
             tls-06, puis boucle de relais : tcp-03 (réception brute dans
             la zone, PAR-DESSUS le résidu tls-07) → tls-07 → tcp-04 vers
             le client (le clair livré est pompé TEL QUEL — jamais parsé,
             charte § 7) ; jusqu'à fin de contexte (tls-07:Q3) ou
             fermeture système ;
         Q2 échec nommé : rax = verdict de l'échec (tls-02/tls-04:Q2/
             tls-06:Q2/tls-07:Q4, « cible injoignable » si tcp-13 échoue,
             « certificat invalide » si verdict 3) — http-10:R2 mappe à
             la réponse client (502 + libellé nommé) ;
         Q3 compensation INTÉGRALE sur tout chemin (succès, Q2, arrêt
             brutal d'un appel système) : contexte détruit (tls-05:1) SI
             établi, credentials libérés (tls-05:2) SI acquis, socket
             serveur fermée (tcp-05) SI ouverte — exactement une fois
             chacun, dans cet ordre (contexte avant credentials : le
             contexte référence les credentials) ; l'oracle constate la
             compensation par comptage d'appels des shims ;
         Q4 le cadre est rendu VIERGE de secrets (zones réécrites à
             l'usage suivant — aucun effacement explicite requis : les
             zones vivent dans le cadre mémoire du thread, jamais dans
             une donnée statique, jamais journalisées).
  inv  : I1 tls-08 est le SEUL propriétaire de fermeture de la socket
             serveur (http-10:R2 garde la socket cliente — héritage
             http-10:Q5 inchangé) ; I2 aucun thread créé ; I3 aucune
             journalisation hors états nommés (charte § 3) ; I4 le
             verdict 3 (certificat) produit la ligne console « certificat
             rejete » ET la réponse 502 — le critère M4 est cet endroit
             précis ; I5 aucun registre non volatil modifié hors cadre.
Échecs :
  E1 : tcp-13 en échec (résolution/connexion) → « cible injoignable »,
       compensation triviale (rien n'était acquis — ordre de Q3 respecté).
  E2 : verdict 3 de tls-04 → « certificat invalide » (I4) : réponse 502
       PROPRE, connexion cliente fermée proprement — jamais un octet de
       la session vers le client, jamais un crash.
  E3 : verdict non nul de tls-06/07 en cours de relais → réponse
       tronquée PROPRE : le client reçoit ce qui a déjà été déchiffré et
       relayé, puis fermeture — l'échec est consigné, le relais ne
       « continue au mieux » jamais.
  E4 : échec d'une libération (tls-05:Q4) → consigné (une ressaisie),
       la compensation continue — l'ordre de Q3 n'est jamais interrompu
       par l'échec d'une libération.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios (compensation par comptage) : succès complet ;
       certificat invalide ; échec tcp-13 ; verdict 5 à la poignée ;
       altération en plein relais ; close_notify avec résidu ; échec de
       libération simulé — CHAQUE scénario finit par exactement la
       séquence de compensation attendue (comptes d'appels des shims :
       Acquire 1 / Delete 0-1 / Free 1, tcp-05 socket serveur 1).
  V3 : le fuzzing à propriétés ne s'applique PAS directement (aucune
       entrée non fiable directe : tout traverse tls-01..07 d'abord) —
       héritage de la règle M3 pour les orchestrateurs.
  V4 : test de rejet : toute notation créant un thread, fermant la
       socket cliente ou journalisant un octet de zone est refusée.
Fixtures    : cadre + paquet de session, shims SSPI réseau complets.
Provenance  : écrite-avant-code.
Décisions   : D45, D48 (héritage console tcp-11), D77, charte M4 entière.
