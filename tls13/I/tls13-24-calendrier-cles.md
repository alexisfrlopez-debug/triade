tls13-24 · la poignée : le calendrier de clés · révision 1
Intention : la machine à dériver de la RFC 8446 § 7.1 — le calendrier à
TROIS étages (early → handshake → application), chaque étage AVANCÉ PAR
UN APPEL : le contexte porte le secret courant et L'ÉTAPE (une machine
dérivée, charte § 6 : l'état est un ARGUMENT pointé, jamais une adresse
fixe). Chaque étage produit LES CONTEXTES ENREGISTREMENT prêts à
l'emploi (clés de tour par tls13-15, IV, séquence zéro) et les clés
Finished — les sorties de la poignée.
Contrat :
  pre  : P1 rcx = le contexte calendrier (48 o : secret courant 32 o @
             +0, étape u32 @ +32, réserve @ +36 — la disposition
             DÉCLARÉE par la présente spec, l'adresse choisie par
             l'appelant) ;
         P2 rdx = l'ENTRÉE de l'étage (l'étage 1 : RIEN, rdx ignoré ;
             l'étage 2 : le secret partagé x25519 [32 o] suivi du hash
             du transcript CH..SH [32 o] — 64 o ; l'étage 3 : le hash
             du transcript CH..Finished serveur [32 o]) ;
         P3 r8 = la SORTIE (l'étage 1 : RIEN ; l'étage 2 : les DEUX
             contextes enregistrement de POIGNÉE [2 × 200 o : émission
             client, réception serveur] suivis des DEUX clés Finished
             [64 o] — 464 o ; l'étage 3 : les DEUX contextes
             d'APPLICATION [2 × 200 o] — 400 o) ;
         P4 la pile alignée 16.
  post : Q1 L'ÉTAPE 1 (le contexte doit être à l'étape 0 — verdict -3
             NOMMÉ sinon : la machine refuse de sauter) : early_secret
             = Extract(zéros32, zéros32) ; derived_1 = Expand-Label(
             early, « derived », vide, 32) ; le contexte porte
             (derived_1, étape 1). La PSK est HORS PÉRIMÈTRE : pas de
             reprise de session au jalon, l'IKM du premier extrait est
             LES ZÉROS (la voie « 0 » du diagramme § 7.1 — chantier
             futur nommé) ;
         Q2 L'ÉTAPE 2 (l'étape doit être 1, -3 sinon) :
             handshake_secret = Extract(derived_1, secret partagé) ;
             c_hs = Expand-Label(handshake, « c hs traffic », hash,
             32) ; s_hs = Expand-Label(handshake, « s hs traffic »,
             hash, 32) ; par direction : la clé write =
             Expand-Label(secret, « key », vide, 16), le IV =
             Expand-Label(secret, « iv », vide, 12), la clé Finished =
             Expand-Label(secret, « finished », vide, 32) ; derived_2 =
             Expand-Label(handshake, « derived », vide, 32) — les
             contextes enregistrement POSÉS (clés de tour par tls13-15,
             IV, séquence 0), le contexte porte (derived_2, étape 2) ;
         Q3 L'ÉTAPE 3 (l'étape doit être 2, -3) : master =
             Extract(derived_2, zéros32) ; c_ap / s_ap =
             Expand-Label(master, « c ap traffic » / « s ap traffic »,
             hash, 32) ; les contextes d'application POSÉS ; le
             contexte porte (master, étape 3 — CLOS : l'étape 4
             n'existe pas, -3) ;
         Q4 LA PREUVE : le TRANSFERT RFC 8448 — le transcript enregistré
             DOCUMENTE les secrets par étage (client_handshake_traffic_
             secret, server_handshake_traffic_secret, les clés write) :
             chaque étage rejoué sur les octets du fixture rend LES
             clés consignées, octet pour octet (le juge est le code :
             les libellés sont des données du plan d'adressage, les
             longueurs vérifiées par construction).
  inv  : I1 les compositions DÉCLARÉES : tls13-06 (l'extrait — un par
             étage), tls13-08 (l'étiquette — TOUTES les clés), tls13-15
             (le déploiement des clés de tour) ; le calendrier ne
             hache RIEN : le hash du transcript est un ARGUMENT (le
             principal tient le contexte SHA — tls13-27 I3) ;
         I2 l'ordre : les étages se suivent STRICTEMENT (-3 sur tout
             saut) ; les contextes sortis sont COMPLETS (aucun champ
             non posé — le récepteur n'initialise rien) ;
         I3 le temps constant : les secrets sont des DONNÉES SECRÈTES
             (charte § 3) — la propriété hérite de tls13-05..08, le
             calendrier n'ajoute AUCUNE branche sur le contenu (l'étape
             est une donnée publique de contrôle) ;
         I4 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ; aucun
             état détenu hors du contexte pointé (charte § 6) ; aucun
             registre non volatil détruit ; NOP, 0x90 (charte § 8).
