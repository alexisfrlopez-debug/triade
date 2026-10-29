tls-07 · réception déchiffrée · révision 2
Intention : déchiffrer le flux TLS reçu vers des spans clairs — LE seul
appelant de DecryptMessageW du projet : l'incomplet est un état nommé (pas
un échec), le résidu Extra vit en tête de zone (propriétaire unique), la
fin de contexte est une fin PROPRE, chaque octet reçu finit déchiffré ou
nommé. R2 (D102) : le clair et le résidu sont CHERCHÉS PAR TYPE, jamais
par position — Schannel réelle RECLASSE les tampons en sortie.
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
  post : Q1 enregistrement déchiffré : rax = 0 — Schannel réécrit les
             QUATRE tampons en sortie de son SEC_E_OK : [0] devient
             STREAM_HEADER (l'en-tête du record — 13 octets en GCM :
             5 en-tête + 8 nonce explicite, la preuve byte-level du
             témoin terrain 17-C/17-F), [1] devient DATA (LE clair, pv
             = zone + en-tête), [2] devient STREAM_TRAILER (le tag),
             [3] devient EXTRA (le résidu) ou EMPTY — et msdn
             (« Extra Buffers Returned by Schannel ») nomme l'EXTRA
             rendu « seul, à une position quelconque » ; le span de
             sortie EST le premier tampon de type SECBUFFER_DATA
             (l'exemple canonique msdn « Decrypting a Message » scanne
             i < 4 par BufferType — le PREMIER gagne) ; le span pointe
             DANS la zone de réception (déchiffrement sur place : le
             clair remplace le brut à l'offset de l'en-tête) ;
             l'appelant pompe ce clair AVANT tout nouvel appel (il sera
             écrasé) ; le résidu = le premier tampon de type
             SECBUFFER_EXTRA (consigné : longueur utile @+0x3A :=
             résidu, offset @+0x3C := lot − résidu) ; la région vivante
             [offset, offset+longueur) est exactement le résidu ; le
             DÉPLACEMENT en tête (libc-01) appartient au PROCHAIN
             appel (I1 : personne d'autre ne touche la zone entre deux
             appels) ;
         Q2 message incomplet : rax = 2 (SEC_E_INCOMPLETE_MESSAGE, tls-02)
             — aucun octet consommé, la zone est laissée EN L'ÉTAT
             (normalisée ce tour : (0, lot)), la bibliothèque a
             reclassé le tampon porteur en SECBUFFER_MISSING (octets
             manquants — IGNORÉ : la quantité n'est jamais une
             dépendance) ; l'appelant réceptionne davantage et rappelle
             avec la nouvelle longueur totale ; le descripteur reçoit
             la zone ENTIÈRE à chaque appel (sémantique SSPI) ;
         Q3 fin de contexte : rax = 4 (SEC_I_CONTEXT_EXPIRED — close_notify)
             — fin PROPRE : le résidu éventuel est PURGÉ (le premier
             tampon de type SECBUFFER_EXTRA lu, curiosité « fin propre
             avec résidu » consignée @+0x3A si longueur > 0 — le
             serveur a parlé après sa fermeture, pas
             d'interprétation), offset := 0 ;
         Q4 échec nommé : rax = verdict tls-02 non nul autre (5 altération,
             6 fatal…) — le cadre porte verdict + HRESULT d'origine ;
         Q5 la zone ne contient JAMAIS d'octet clair en fin d'appel hors
             span livré (Q1) — le résidu est du BRUT non déchiffré.
  inv  : I1 le résidu Extra n'appartient qu'à tls-07 (normalisation libc-01
             en tête — personne d'autre ne touche la zone entre deux
             appels) ; I2 aucune fermeture de socket (tls-08 seul
             propriétaire — ici : AUCUNE socket, AUCUN ws2_32) ; I3
             aucune journalisation de brut ni de clair (charte § 3 —
             aucun WRITE, aucun IAT kernel32) ; I4 aucune écriture hors
             zone de réception, cadre et span de sortie (le
             descripteur vit dans la PILE de travail) ; I5 volatils
             seuls modifiés — cadre, zone, longueurs et span
             sauvegardés dans la pile ; I6 la POSITION d'un tampon
             n'est JAMAIS une hypothèse — seuls les TYPES parlent
             (STREAM_HEADER en [0] est un fait de Schannel, pas un
             contrat : le scan par type reste correct si la
             bibliothèque ordonne autrement, y compris l'EXTRA « seul,
             à une position quelconque » de msdn).
Échecs :
  E1 : verdict tls-02 non nul de DecryptMessageW → Q4 (altération : le
       tunnel est mort — session fermée proprement, réponse tronquée
       propre au client si des octets ont déjà été relayés).
  E2 : longueur utile > capacité de zone (2 × MAX_JETON — résidu + reçus)
       → verdict 5 « zone de réception dépassée » AVANT tout appel SSPI et
       AVANT tout déplacement, la zone et les champs sont laissés INTACTS
       (fail-closed : le flux est anormalement dense, la session refuse).
  E3 : fin de contexte avec résidu (Q3) — état nommé, pas un échec : le
       verdict reste 4.
  E4 : SEC_E_OK SANS aucun tampon reclassé SECBUFFER_DATA (bibliothèque
       dégénérée, descripteur altéré en vol) → verdict 6 AVANT toute
       écriture au span (le span de sortie reste INTACT — jamais un mot
       forgé) ; la région est consignée normalisée (0, lot) — miroir de
       Q4, la géométrie de la région vivante reste VRAIE (la
       normalisation a déjà joué) ; cadre verdict 6, HRESULT d'origine
       @+0x34 déjà posé.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios (shim au reclassement RÉEL : [0]=STREAM_HEADER,
       [1]=DATA, [2]=TRAILER, [3]=EXTRA-ou-EMPTY) : enregistrement exact ;
       incomplet par un octet (Q2 puis Q1 après un octet de plus) ; deux
       enregistrements + Extra dans un même lot (Q1 puis Q1, résidu
       déplacé — le span du premier appel reste INTACT en zone : la
       preuve géométrique de la normalisation à l'appel SUIVANT) ;
       close_notify pur (Q3) ; close_notify avec résidu (E3, curiosité
       consignée) ; altération (E1) ; densité hostile par le lot ET par
       l'offset (E2 — zone et champs INTACTS, la garde étendue D89) ;
       verdicts 3 et 6 (table TOTALE) ; normalisation depuis un état
       offset non nul ; lot vide ; fin de contexte après un
       enregistrement — CHAQUE appel finit par l'état du cadre ET de la
       zone de réception EXACTEMENT PRÉDITS (image 0xD000 octet par
       octet : verdict, HRESULT d'origine, champs +0x3A/+0x3C, clair
       déchiffré, résidu brut — Q5 : zéro clair hors span livré) + le
       contrat d'appels complet ; NOUVEAUTÉS R2 : l'EXTRA à une position
       INHABITUELLE (le cas « extra seul » de msdn : [1]=EMPTY, EXTRA
       en [2]) doit être trouvé ; aucun DATA après SEC_E_OK → E4
       verdict 6, span intact.
  V3 : fuzzing à propriétés : lots de longueurs hostiles, verdicts shim
       aléatoires — survie, terminaison, zones jamais débordées.
  V4 : test de rejet : toute notation fermant une socket, journalisant un
       octet ou écrivant hors zone est refusée ; R2 : toute notation
       lisant le clair ou le résidu à une POSITION FIXE (tampon 0 /
       tampon 1) est refusée — le scan par type est le contrat (I6).
Fixtures    : cadre de session TLS, zone de réception, shims SSPI (reclassement réel D102).
Provenance  : écrite-avant-code ; R2 le 29/10/2026 après la preuve
             byte-level du témoin terrain 17-F (13 octets = 17 03 03
             03 B3 + nonce GCM 00…01 = le STREAM_HEADER du premier
             record : l'ancienne notation pompait le tampon [0]
             reclassé STREAM_HEADER — le client recevait l'EN-TÊTE
             CHIFFRÉ, jamais le clair ; modèle et émulation d'accord
             entre eux, tous deux faux contre l'API réelle — msdn
             « Decrypting a Message » / « Extra Buffers Returned by
             Schannel »).
Décisions   : D45, D77, D102, charte M4 § 1, § 3, § 7.
