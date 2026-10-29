http-10 · session proxy : routage TLS · révision 2
Ancêtre : http-10:R1 (D46, scellée 0.4.0 — la spécification R1 vit dans
m3/I/ et ne change pas : la balise est immuable § 9). La révision vit en
M4 et modifie CE que le tunnel exige : le routage d'une cible TLS vers
tls-08 et la table des réponses d'échec du tunnel. Tout le reste de R1
(accumulation bornée, tri-entrée, pompe détachée, une requête par
connexion, propriété de la socket cliente, anti-interblocage) est REPRIS
TEL QUEL — cité, non recopié (T5).
Intention : router la requête https vers la session TLS et traduire ses
verdicts nommés en réponses HTTP propres — L'unique propriétaire de la
table des réponses du projet (héritage R1 : une table, un propriétaire) :
le critère M4 « échec propre sur certificat invalide » ATERRIT ICI.
Contrat :
  pre  : P1-P5 de http-10:R1 repris tels quels (thread session, paquet
             client, socket cliente, cadres) ;
         P6 NOUVEAU : quand http-08:R2:Q4 rend son verdict « cible TLS »,
             la session prépare le paquet de session tls-08 (autorité
             découpée R1, requête réécrite en forme origine — la
             réécriture absolu → origine reste propriété R1 inchangée,
             port implicite 443) et fournit le cadre TLS vierge.
  post : Q1-Q5 de http-10:R1 repris tels quels (chemin http non TLS,
             relais à fermeture délimitée, fermeture socket cliente
             exactement une fois par le thread session, réponse jamais
             parsée — le tunnel ne change RIEN au chemin M3 scellé) ;
         Q2' NOUVEAU (routage) : verdict « cible TLS » → appel de tls-08
             avec le paquet préparé ; succès : le relais du flux déchiffré
             a déjà été fait PAR tls-08 (la session n'achève rien
             elle-même : socket serveur et boucle de relais appartiennent
             à tls-08) ; la réponse du serveur relayée n'est TOUJOURS pas
             parsée (charte § 7) ;
         Q3' NOUVEAU (table des réponses, extension de la table R1 —
             table unique, entrées nouvelles) :
             « cible injoignable »  (tls-08:E1) → 502 ;
             « certificat invalide » (tls-08:E2) → 502 « certificat
               rejete » + ligne console tcp-11 (état nommé, aucun octet
               de secret) ;
             « tunnel rompu »        (verdicts 5/6 tls-02) → 502 ;
             « zone dépassée », « poignée interminable », « émission/
               réception rompue » (tls-04/06/07 nommés) → 502 ;
             — chaque entrée NOUVELLE est nommée ICI une seule fois ;
             les entrées R1 (400, 431, 502 de connexion) sont inchangées ;
         Q4' la compensation TLS appartient à tls-08 (Q3 de tls-08) — la
             session R1 ne libère JAMAIS un handle SSPI : sa compensation
             propre (socket cliente, thread) est inchangée R1.
  inv  : I1-I5 de http-10:R1 repris (premier push, terminale ret, aucun
             pop sans push, sondes en lecture sous RSP interdites au
             stockage, tri-entrée) ; I6' NOUVEAU : la session n'appelle
             JAMAIS directement une entrée SSPI (Acquire/ISC/Encrypt/
             Decrypt/Query/Delete/Free vivent dans tls-04..07 via tls-08
             — un appel direct est un défaut T5).
Échecs :
  E1 : verdict nommé de tls-08 → Q3' (502 propre) — puis fermeture
       cliente R1 : l'échec du tunnel est un ÉTAT de la session, pas un
       crash, pas un silence.
  E2 : entrée de table manquante (verdict de tls-08 sans entrée) —
       IMPOSSIBLE par contrat (Q3' énumère les verdicts de tls-08:Q2 un à
       un) ; toute divergence est un défaut de spécification croisée,
       détecté par V2 (oracle vérifie l'exhaustivité croisée).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios hérité V2 de R1 + scénarios TLS : cible https
       saine (poignée 2 allers, réponse relayée) ; certificat invalide ;
       cible injoignable ; altération en relais — chaque scénario
       vérifie : réponse exacte au client (octets de la table Q3'),
       compensation croisée tls-08:Q3 (comptage des shims), chemin M3
       http non TLS inchangé octet pour octet (anti-régression R7).
  V3 : hérité (accumulation P1-P5) — la session reste hors fuzz direct,
       ses entrées non fiables traversent les blocs fuzzés.
  V4 : test de rejet : toute notation appelant SSPI directement ou
       fermant la socket serveur est refusée (I6', I1 de tls-08).
Fixtures    : paquet de session + cadre TLS, shims complets.
Provenance  : écrite-avant-code (révision inter-jalon, modèle tcp-07:R3).
Décisions   : D46 (ancêtre), D64 (T2 hérité), D77, charte M4 entière.
