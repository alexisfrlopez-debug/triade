http-10 · session proxy : routage du relèvement et ligne de flux · révision 3
Ancêtre : http-10:R2 (D92, embarquée 0.5.1 @0x74C0 — la spécification R2 vit
dans m4/I/ et ne change pas : la balise est immuable § 9). La révision vit en
M5 (.text4 0x81C0) et modifie CE que le relèvement exige : le routage du
verdict « cible à relever » (http-08:R3 rax = 5) vers tls-08 AVEC la politique
passée au parseur, et la LIGNE DE FLUX. Tout le reste de R2 (accumulation
bornée, tri-entrée, pompe détachée, une requête par connexion, propriété de
la socket cliente, anti-interblocage, table des réponses Q3') est REPRIS TEL
QUEL — cité, non recopié (T5).
Intention : le critère (b) de D136 — un flux NAVIGATEUR intercepté de bout en
bout — tient en deux pièces : la requête claire du navigateur est RELEVÉE
(elle traverse le tunnel M4 tel quel) et la session NOMME ce qu'elle a vu.
La ligne de flux est une PIÈCE D'INTERCEPTION : elle naît avec la politique
(sans elle, R2 octet pour octet — l'oracle differentiel R1/R3-sans-politique
exige le silence total, anti-régression R7).
Contrat :
  pre  : P1-P5 de http-10:R2 repris tels quels (thread session, paquet
             client, socket cliente, cadres) ;
         P6 de http-10:R2 repris tel quel (verdict « cible TLS » → paquet
             tls-08, port 443) ;
         P7 NOUVEAU : la politique est lue UNE fois dans .data (R_POLITIQUE,
             layout — l'état que http-12:R3 a écrit au démarrage) et passée
             en CINQUIÈME argument à http-08:R3 (la feuille pure ne lit
             jamais .data — I1 de sa spec) ; le verdict 5 est routé comme
             le verdict 4 : LE MÊME chemin Q2' — paquet de session tls-08
             (autorité découpée, requête réécrite en forme origine, port
             443 AUSSI pour la cible relevée), cadre TLS vierge, verdicts
             transportés tels quels, table des réponses Q3' INCHANGÉE ;
         P8 NOUVEAU : les compteurs de flux — rsi (octets clairs ENTRÉS :
             l'accumulation + le corps pompé) et rdi (octets clairs SORTIS :
             les émissions .emettre) — sont des non-volatils SAUVEGARDÉS au
             prologue (7 pushes) et restitués à l'épilogue (ABI msx64) ;
             les octets des relais délégués (HTTP_POMPE R1, tls-08) ne sont
             PAS comptés par la session — chaque octet est compté par son
             propriétaire exact, jamais deux fois (la ligne ne ment pas).
  post : Q1-Q5 et Q2'/Q3'/Q4' de http-10:R2 repris tels quels ;
         Q6 NOUVEAU (la ligne de flux, politique ARMÉE seulement) : une
             ligne par session cliente ABOUTIE — dont la requête a été
             parsée (http-02 succès) — émise via tcp-11 UNE fois avant la
             compensation de fermeture R1 :
             « flux » + méthode (texte R_TAB_METHODES) + « » + hôte
             (span autorité effective, TRONQUÉ à 14 octets — la borne est
             nommée : préfixe + 12 + suffixe <= 64, P4 de tcp-11 ; un hôte
             plus long est porté coupé, la ligne ne ment jamais) + «:» +
             port (le champ numérique de tcp-11) + « v= » + verdict de
             session + « e= » + octets entrés + « s= » + octets sortis
             + CRLF — les trois nombres du suffixe formés par libc-04
             (héritage, R7) dans la zone de flux du cadre (convention
             layout : FLUX_VERDICT @+0x7028, ZONE_FLUX_* @+0x7030..+0x70EF) ;
             le verdict de session suit le domaine TOTAL de layout
             (0 aboutie / 2..7 verdicts tls-08 transportés / 400..505 la
             réponse d'erreur nommée) ; PAS de ligne quand la requête
             n'a pas été identifiable (http-02 en échec, accumulation
             morte — la sentinelle -1 : rien à nommer, la ligne ne
             porterait que du vide) ;
         Q7 : sans politique (R_POLITIQUE == 0) : R2 OCTET POUR OCTET —
             aucune ligne de flux, aucun verdict 5 possible, le chemin M3
             scellé T2 reste vert (anti-régression R7).
  inv  : I1-I6 de http-10:R2 repris (premier push, terminale ret, aucun
             pop sans push, sondes en lecture sous RSP interdites au
             stockage, tri-entrée, JAMAIS d'entrée SSPI directe) ;
         I7 NOUVEAU : les appels IAT de la session restent EXACTEMENT
             {CloseHandle} (la ligne de flux vit via tcp-11 et libc-04,
             appels DIRECTS hérités — aucun IAT nouveau) ; I8 : le
             verdict de session est écrit aux DEUX dispatches (succès
             TLS, réponses nommées) AVANT l'émission ; I9 : la ligne de
             flux est composée dans le cadre du thread (ZONES FLUX),
             jamais en donnée statique (charte § 6), EN DEUX TEMPS : le
             PRÉFIXE (« flux » + méthode PAR TABLE + hôte tronqué) au
             ROUTAGE — AVANT tout relais, le tampon de requête
             [rsp..rsp+0x4000) étant prêté aux relais (http-09 y reçoit
             la réponse, le corps pompé l'écrase ; la méthode vient de
             R_TAB_METHODES, .rdata STABLE — jamais le span du tampon),
             sa longueur consignée en cadre (FLUX_PREF_LEN, layout) —
             le SUFFIXE (v/e/s) seul à .fin.
Échecs :
  E1 : verdict nommé de tls-08 → Q3' (502 propre) — hérité, inchangé ;
       le verdict de flux est le verdict tls-08 (3 = certificat rejeté),
       pas la réponse 502 (la LIGNE nomme la CAUSE, la réponse nomme
       l'effet).
  E2 : port explicite du navigateur (http://hote:8080/…) : l'origine du
       relèvement est l'HTTPS STANDARD de l'hôte (port 443) — le port
       explicite du schéma http est PERDU au relèvement, consigné ICI
       (la ligne de flux porte le port EFFECTIF — 443 — jamais le port
       perdu) ; un relèvement vers :8080 serait une invention.
  E3 : hôte > 14 octets → la ligne porte l'hôte tronqué (Q6) — la borne
       est un état de la ligne, jamais une perte silencieuse de verdict.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios étendu (D136) : cible relevée saine (verdict 0,
       page relayée, ligne de flux exacte) ; certificat invalide relevé
       (verdict 3, 502 étiquetée, ligne verdict=3) ; politique absente →
       R1/R2 émulés contre R3 : ZÉRO écart (octets, lignes console,
       compensation — le différentiel d'ancêtre rejoué sur la R3) ;
       chaque scénario vérifie la ligne de flux OCTET PAR OCTET (modèle
       de composition D136), la réponse exacte au client, la compensation
       croisée, le paquet P6/P7 au passage de tls-08.
  V3 : hérité (accumulation P1-P5) — la session reste hors fuzz direct.
  V4 : falsification — mutations d'un point stables en taille (leçon D82)
       attrapées : le verdict 5 non routé, le SECOND dispatch amnésique
       (post-réécriture — la relevée tomberait dans l'émission claire),
       la politique non passée (P7), la ligne émise sans politique (Q7),
       l'hôte non tronqué (E3), le verdict de flux remappé (E1), la
       méthode hors table (I9 — le span du tampon recyclé) ; témoin vert.
Fixtures    : pièces de la ligne de flux (R_FLUX_*, layout) + paquet de
             session + cadre TLS, shims complets.
Provenance  : écrite-avant-code (révision inter-jalon, modèle http-10:R2).
Décisions   : D77, D92 (ancêtre), D136, charte m5/I § 6 (l'arbitrage T5 :
             la ligne de flux appartient au JOURNAL tcp-11 — émise par la
             session, modèle tcp-11 ; http-11 est la console interactive,
             elle ne porte rien de la session).
