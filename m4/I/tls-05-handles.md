tls-05 · cycle de vie des handles · révision 2
Intention : envelopper acquisition et libérations SSPI — LE seul
propriétaire du cycle de vie des handles (AcquireCredentialsHandleW,
DeleteSecurityContext, FreeCredentialsHandle) : charte § 4, compensation
exacte — chaque handle acquis est libéré sur TOUT chemin ; personne
d'autre n'appelle ces trois entrées.
Révision 2 (D140, branche S3 du run v6 du 03/11) : l'acquisition passe
une SCH_CREDENTIALS EXPLICITE au lieu de pAuthData NULL — les credentials
par défaut de Schannel consultent la RÉVOCATION, qui exige le réseau ;
dans la VM isolée (Networking=Disable) la consultation meurt sur
CERT_TRUST_REVOCATION_STATUS_UNKNOWN (T2a/T3, rc=60) et la poignée
n'a jamais pu naître : c'est la cause nommée de l'ÉCHEC NOMMÉ (7).
Contrat :
  pre  : P1 rcx = opération :
             0 acquérir les credentials clientes ;
             1 détruire le contexte de sécurité ;
             2 libérer les credentials ;
         P2 rdx pointe le cadre de session TLS (les handles y vivent à
             leurs offsets documentés : credentials, contexte — deux mots
             de 64 bits chacun, petits-boutistes) ;
         P3 pour l'opération 0 : pAuthData (argument 5, [rsp+0x20] en
             msx64 — pvLogonID reste l'argument 4, NULL) pointe une
             SCH_CREDENTIALS construite SUR LA PILE du bloc, de 0x48
             octets : dwVersion = SCH_CREDENTIALS_VERSION (5,
             schannel.h) et TOUS les autres champs NULS — dwCredFormat,
             cCreds/paCred (aucun certificat client), hRootStore = NULL
             (le magasin MACHINE par défaut, celui où la racine certutil
             est déposée — prouvé par T2b rc=0), cMappers/aphMappers,
             dwSessionLifespan, dwFlags = 0, cTlsParameters/pTlsParameters ;
             dwFlags = 0 : AUCUN bit de révocation (l'équivalent
             --ssl-no-revoke de curl — la révocation exige le réseau,
             impossible dans la VM isolée) ; la validation de la CHAÎNE
             reste AUTOMATIQUE et par défaut (le contrat cryptographique
             M4 ne désactive JAMAIS la validation : un certificat dont la
             racine n'est pas approuvée est TOUJOURS rejeté — prouvé par
             T5, CERT_TRUST_IS_UNTRUSTED_ROOT, le juge discriminate ;
             seul le contrôle de RÉVOCATION est retiré).
  post : Q1 acquisition : rax = verdict tls-02 du retour (0 : handle
             écrit dans le cadre ; sinon : verdict nommé, cadre intact —
             rien d'acquis ne reste à compenser) ;
         Q2 destruction de contexte : rax = verdict tls-02 (0 : le
             contexte est détruit — le cadre est remis à zéro APRÈS un
             succès constaté, jamAIS avant l'appel) ;
         Q3 libération des credentials : rax = verdict tls-02 (idem) ;
         Q4 tout verdict non nul est retourné tel quel à tls-08 — la
             compensation d'une libération échouée appartient à la
             session (journal du verdict, ressaisie unique), pas à ce
             bloc.
  inv  : I1 aucune fermeture de socket, aucun autre appel système que
             l'opération demandée ; I2 le bloc ne détient AUCUN état
             entre les appels (les handles vivent dans le cadre de
             session, jamais en données propres) ; I3 l'ordre
             zéro-puis-propriété : un handle remis à zéro n'est plus
             détruit une seconde fois — la remise à zéro suit le succès
             constaté (Q2/Q3), la détection de double libération
             appartient à tls-08 (état de session) ; I4 aucun registre
             non volatil modifié hors cadre ; I5 aucun octet du cadre
             n'est journalisé (charte § 3) ; I6 la structure
             SCH_CREDENTIALS ne vit QUE dans la trame de l'appel (zone
             morte au retour — aucun état, cohérent avec I2).
Échecs :
  E1 : acquisition refusée (verdict 5/6 de tls-02) — la session n'a
       aucune compensation à faire : rien n'a été acquis (Q1). Sous R2,
       la famille CERTIFICAT REJETÉ (0x80090325 UNTRUSTED_ROOT…) devient
       ATTEIGNABLE et nommée (le chemin 502 « Certificat rejete » 34 o
       existe et est câblé — D92) ; l'erreur de révocation hors ligne
       (0x80092012/0x80092013) ne peut plus tuer l'acquisition : elle
       n'est plus consultée (D140).
  E2 : libération en échec (Q4) — consignée par la session (verdict
       nommé, une ressaisie), le processus ne s'arrête pas pour ça :
       l'échec de libération est un ÉTAT nommé, pas un crash.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à shims : acquisition/déstruction/libération en succès ;
       acquisition en échec ; libération en échec — états du cadre
       exactement prédits avant/après chaque appel (octet par octet) ;
       LA STRUCTURE SCH_CREDENTIALS relue PAR LE SHIM à l'adresse
       pAuthData et confrontée OCTET PAR OCTET au contrat P3 (dwVersion
       = 5, tous les autres octets nuls) — pAuthData NULL (la
       régression 0.5.0) est REFUSÉE ;
       double libération détectée par tls-08 (scénario dédié).
  V3 : fuzzing à propriétés : verdicts tls-02 aléatoires en retour des
       shims — le cadre ne change QUE sur succès constaté.
  V4 : test de rejet : toute notation appelant une autre entrée IAT que
       l'opération demandée, ou détenant un état, est refusée ;
       mutations nommées incluant la régression pAuthData NULL et une
       dwVersion divergente.
Fixtures    : cadre de session TLS, shims SSPI de l'oracle.
Provenance  : écrite-avant-code (révision 2 consignée AVANT le build
             0.5.1 — l'octet suit l'intention, jamais l'inverse).
Décisions   : D27 (indirecte — l'antisurvie des secrets), D45, D77,
              D140 (révocation hors ligne — branche S3, correctif 0.5.1),
              charte M4 § 4 (compensation exacte).
