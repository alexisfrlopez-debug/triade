tls-04 · poignée de main cliente · révision 1
Intention : conduire la boucle InitializeSecurityContext jusqu'à
l'établissement du contexte TLS — LE seul appelant d'InitializeSecurity-
ContextW du projet : chaque aller-retour est borné, chaque HRESULT passe
par tls-02, aucun jeton ne dépasse MAX_JETON, la boucle se termine
TOUJOURS (critère M4 : poignée de main TLS).
Contrat :
  pre  : P1 rcx pointe le cadre de session TLS (contient : handles de
             tls-05 [credentials acquis, contexte à zéro], socket serveur
             connectée par tcp-13, nom cible UTF-16 de tls-01, deux zones
             jetons de MAX_JETON — émission et réception) ;
         P2 le cadre et ses zones appartiennent à tls-08 (le présent bloc
             ne possède RIEN : il emprunte et rend) ;
         P3 la socket serveur est connectée et vierge de tout octet échangé.
  post : Q1 succès : rax = 0 — le contexte est établi (handle de contexte
             valide dans le cadre, prêt pour tls-06/tls-07) ; le nombre
             d'allers-retours est consigné dans le cadre (u16) ;
         Q2 échec nommé : rax = verdict tls-02 non nul (3 certificat
             invalide, 5 négociation rompue, 6 fatal inconnu…) — le cadre
             porte le verdict ET l'HRESULT d'origine (tls-02:Q2) pour la
             réponse propre de http-10:R2 ; le contexte reste dans l'état
             où la bibliothèque l'a laissé — la compensation des handles
             appartient à tls-05/tls-08, JAMAIS ici ;
         Q3 chaque itération : jeton client produit → émission intégrale
             par tcp-04 (boucle d'achèvement bornée) ; réception par
             tcp-03 dans la zone jeton réception (accumulation si
             réception partielle) ; l'appel suivant reçoit ce jeton en
             entrée — les rôles entrée/sortie suivent la sémantique SSPI,
             tls-03 construit les descripteurs ;
         Q4 le premier appel se fait SANS jeton d'entrée (le client
             initie) et PRODUIT le premier jeton client.
  inv  : I1 le nombre d'itérations est borné : MAX_ALLERS = 16 (un
             échange TLS réel n'en demande pas plus de ~ 10) — au-delà :
             verdict 5 « poignée interminable » (fail-closed, la boucle
             se termine TOUJOURS) ; I2 aucun octet de jeton n'est JAMAIS
             journalisé (charte § 3 — zéro divulgation) ; I3 aucune
             fermeture de socket, aucune libération de handle ici
             (propriétaires uniques : http-10:R2 côté client, tls-08 côté
             serveur, tls-05 pour les handles) ; I4 le nom cible est lu
             tel quel (traduction déjà faite par tls-01, jamais refaite) ;
             I5 aucun registre non volatil modifié hors cadre.
Échecs :
  E1 : verdict tls-02 non nul au premier ou dernier appel → Q2 (échec
       nommé — le certificat invalide arrive ICI : verdict 3).
  E2 : jeton serveur > MAX_JETON (la réception de tcp-03 déborlerait la
       zone) → verdict 5 « jeton hors borne » AVANT tout appel SSPI
       (échec avant l'entrée système, charte héritée M3 § 9).
  E3 : émission tcp-04 en échec système → verdict 5 « émission rompue ».
  E4 : réception tcp-03 en échec système → verdict 5 « réception rompue ».
  E5 : 16 allers-retours sans établissement → verdict 5 (I1).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios (shims SSPI scriptés) : poignée complète en 2,
       3 puis 9 allers-retours ; certificat invalide (verdict 3 simulé) ;
       jeton trucidé (verdict 5) ; HRESULT exotique (verdict 6) ; boucle
       sans fin (E5) — chaque scénario finit par un état du cadre
       exactement prédit (compensation constatée par tls-08).
  V3 : fuzzing à propriétés sur les shims : HRESULT aléatoires à chaque
       retour, jetons de longueurs hostiles — survie, terminaison
       (I1 garantit la borne), verdict conforme au modèle.
  V4 : test de rejet : toute notation fermant la socket, libérant un
       handle ou journalisant un octet de jeton est refusée.
Fixtures    : cadre de session TLS (zone de travail, shim SSPI de l'oracle).
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 1, § 3, § 4.
