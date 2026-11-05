tls13-23 · la poignée : traiter le ServerHello · révision 1
Intention : le verdict sur la réponse — la marche BORNÉE du message (le
type de poignée 2, la longueur u24, le corps) : chaque champ CONFRONTÉ à
l'attendu du jalon, chaque divergence un REFUS NOMMÉ (le domaine ne
s'adapte JAMAIS en silence) ; l'issue EST le secret partagé : la
key_share x25519 du serveur croisée avec la clé privée du client par
tls13-13.
Contrat :
  pre  : P1 rcx = le message ServerHello (le message de poignée
             COMPLET : l'en-tête type + u24 + le corps — 90 octets
             MINIMUM : le message minimal attendu, la longueur exacte
             déclarée par l'u24) ;
         P2 rdx = la longueur disponible (≥ 94, verdict -2 : 4 + 90) ;
         P3 r8 = la clé privée x25519 du client (32 o — BRUTE : le
             clamp est l'affaire de tls13-13) ;
         P4 r9 = la sortie : le secret partagé (32 o) ; la pile
             alignée 16.
  post : Q1 les confrontations DANS L'ORDRE DU CORPS, CHACUNE NOMMÉE :
             le type de poignée == 2 (verdict -1) ; la version héritage
             == 0x0303 (-1) ; l'aléa != LA VALEUR MAGIQUE
             HelloRetryRequest (SHA-256 de « HelloRetryRequest », la
             constante du plan d'adressage — l'ÉGALER est le verdict
             -5 NOMMÉ « HelloRetryRequest : le chantier futur nommé »,
             RFC 8446 § 4.1.3 : la demande de nouvelle offre est un
             refus propre, jamais une seconde offre silencieuse) ;
             session_id_echo VIDE (le nôtre était vide, -1) ; la suite
             == 0x1301 (-5 : LA NÉGOCIATION REFUSÉE — le serveur a
             choisi autre chose, charte § 1) ; la compression nulle
             (-1) ; supported_versions PRÉSENTE == 0x0304 (-5) ;
             key_share PRÉSENTE, groupe x25519, 32 octets (-5) ; les
             extensions INCONNUES IGNORÉES (RFC 8446 § 4.1.3 : la
             règle DU PROTOCOLE, pas une tolérance du domaine) ; la
             longueur consommée == la longueur disponible (-1 : le
             message doit s'épuiser exactement) ;
         Q2 l'issue : tls13-13(clé privée, clé publique du serveur) →
             le secret partagé à r9 — les vecteurs RFC 7748 § 6.1 (la
             paire Alice/Bob : chaque côté rend LE MÊME secret) et le
             TRANSFERT RFC 8448 (le secret du transcript, via le
             calendrier du chantier (b)) ;
         Q3 le message et la clé privée INTACTS ; rax = 0 (ou le
             verdict NOMMÉ de Q1 — la clé privée n'est JAMAIS touchée
             sur un message refusé : tls13-13 n'est appelé qu'après le
             dernier refus possible).
  inv  : I1 la marche est BORNÉE : chaque lecture précédée du contrôle
             de reste (le message ne déborde JAMAIS de P2 — les rejets
             -1/-2 se prononcent AVANT toute lecture hors borne) ;
         I2 le temps constant : la comparaison à la valeur magique HRR
             est par OU cumulatif (charte § 3 : la discipline demeure —
             même sur un refus nommé) ;
         I3 le message ne TOUCHE PAS au transcript (le principal
             absorbe — la même séparation que tls13-22) ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu (charte § 6) ; aucun registre non volatil
             détruit ; NOP, 0x90 (charte § 8).
