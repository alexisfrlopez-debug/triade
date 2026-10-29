tls-07 · réception déchiffrée · révision 1
Intention : déchiffrer le flux TLS reçu vers des spans clairs — LE seul
appelant de DecryptMessageW du projet : l'incomplet est un état nommé (pas
un échec), le résidu Extra vit en tête de zone (propriétaire unique), la
fin de contexte est une fin PROPRE, chaque octet reçu finit déchiffré ou
nommé.
Contrat :
  pre  : P1 rcx pointe le cadre de session TLS (contexte établi ; zone de
             réception : capacité 2 × MAX_JETON — le résidu Extra suivi
             des octets bruts récents) ;
         P2 rdx pointe la zone de réception ; r8 contient la longueur
             utile TOTALE de la zone (résidu Extra PRÉCÉDENT + octets
             bruts reçus depuis le dernier appel — l'appelant (tls-08)
             réceptionne PAR-DESSUS le résidu, jamais ailleurs) ;
         P3 r9 pointe le span de sortie (deux mots : ptr, longueur) —
             propriété de l'appelant, rempli uniquement sur succès.
  post : Q1 enregistrement déchiffré : rax = 0 — le span de sortie pointe
             DANS la zone de réception (déchiffrement sur place : le clair
             remplace le brut à l'offset de l'en-tête d'enregistrement) ;
             l'appelant pompe ce clair AVANT tout nouvel appel (il sera
             écrasé) ; le résidu Extra éventuel est déplacé en tête de
             zone par libc-01, longueur utile mise à jour ;
         Q2 message incomplet : rax = 2 (SEC_E_INCOMPLETE_MESSAGE, tls-02)
             — aucun octet consommé : l'appelant réceptionne davantage et
             rappelle avec la nouvelle longueur totale ; le descripteur
             reçoit la zone ENTIÈRE à chaque appel (sémantique SSPI) ;
         Q3 fin de contexte : rax = 4 (SEC_I_CONTEXT_EXPIRED — close_notify)
             — fin PROPRE : le résidu éventuel est purgé (nommé « fin
             propre avec résidu » dans le cadre si longueur > 0 : le
             serveur a parlé après sa fermeture, curiosité consignée, pas
             d'interprétation) ;
         Q4 échec nommé : rax = verdict tls-02 non nul autre (5 altération,
             6 fatal…) — le cadre porte verdict + HRESULT d'origine ;
         Q5 la zone ne contient JAMAIS d'octet clair en fin d'appel hors
             span livré (Q1) — le résidu est du BRUT non déchiffré.
  inv  : I1 le résidu Extra n'appartient qu'à tls-07 (déplacement libc-01
             en tête — personne d'autre ne touche la zone entre deux
             appels) ; I2 aucune fermeture de socket ; I3 aucune
             journalisation de brut ni de clair (charte § 3) ; I4 aucune
             écriture hors zone de réception, cadre et span de sortie ;
             I5 aucun registre non volatil modifié hors cadre.
Échecs :
  E1 : verdict tls-02 non nul de DecryptMessageW → Q4 (altération : le
       tunnel est mort — session fermée proprement, réponse tronquée
       propre au client si des octets ont déjà été relayés).
  E2 : longueur utile > capacité de zone (2 × MAX_JETON — résidu + reçus)
       → verdict 5 « zone de réception dépassée » AVANT tout appel SSPI
       (fail-closed : le flux est anormalement dense, la session refuse).
  E3 : fin de contexte avec résidu (Q3) — état nommé, pas un échec : le
       verdict reste 4.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios : enregistrement exact ; incomplet par un octet
       (Q2 puis Q1 après un octet de plus) ; deux enregistrements + Extra
       dans un même lot (Q1 puis Q1, résidu déplacé) ; close_notify pur
       (Q3) ; close_notify avec résidu (E3) ; altération (E1) ; densité
       hostile (E2) — chaque scénario vérifie le contenu de la zone
       octet par octet (résidu exact, zéro clair résiduel Q5).
  V3 : fuzzing à propriétés : lots de longueurs hostiles, verdicts shim
       aléatoires — survie, terminaison, zones jamais débordées.
  V4 : test de rejet : toute notation fermant une socket, journalisant un
       octet ou écrivant hors zone est refusée.
Fixtures    : cadre de session TLS, zone de réception, shims SSPI.
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 1, § 3, § 7.
