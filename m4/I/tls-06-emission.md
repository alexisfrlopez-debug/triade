tls-06 · émission chiffrée · révision 1
Intention : chiffrer et émettre un span clair vers le serveur TLS — LE
seul appelant d'EncryptMessageW et de QueryContextAttributesW (tailles de
flux) du projet : le clair de l'appelant n'est jamais modifié, les
enregistrements sont bornés par la valeur NÉGOCIÉE (jamais une constante
inventée — charte § 8), chaque émission est intégrale.
Contrat :
  pre  : P1 rcx pointe le cadre de session TLS (contexte établi par
             tls-04 ; zone d'émission : capacité en-tête + message
             maximal + queue) ;
         P2 rdx pointe le span clair à émettre (octets de la requête
             réécrite — propriété de http-10:R2, jamais modifiés) ;
         P3 r8 contient la longueur du span clair (u64, peut être 0 :
             émission d'un enregistrement vide — légal, aucun cas
             spécial) ;
         P4 les tailles de flux (en-tête, queue, message maximal) sont
             acquises UNE fois par session au PREMIER appel (QueryContext-
             AttributesW, verdict tls-02 — échec : verdict nommé, aucun
             écrasement partiel) puis consignées dans le cadre : les
             appels suivants ne les redemandent pas (charte § 6).
  post : Q1 succès : rax = 0 — le span clair a été émis INTÉGRALEMENT en
             enregistrements chiffrés : chaque morceau de longueur au
             plus message maximal (découpe de tls-03:Q2 en amont), chaque
             enregistrement = copie libc-01 du morceau vers la zone
             d'émission, descripteur tls-03 type 1, EncryptMessageW
             (verdict tls-02 — 0 seul continue), puis émission tcp-04 en
             boucle d'achèvement bornée (modèle http-09 hérité :
             jamais fermer, toujours finir) ;
         Q2 échec nommé : rax = verdict tls-02 non nul, ou verdict
             « émission rompue » si tcp-04 échoue en système — le cadre
             porte le verdict ; AUCUN octet clair ne subsiste dans la
             zone d'émission après l'appel (fin d'appel : zone
             réutilisée à l'appel suivant — le chiffré ne survit pas
             à l'appel qui le suit) ;
         Q3 le clair de l'appelant est OCTET POUR OCTET inchangé (la
             copie seule est chiffrée : chiffrement sur place DANS la
             zone d'émission, jamais dans le tampon de l'appelant).
  inv  : I1 aucune fermeture de socket ; I2 aucune journalisation du
             clair ni du chiffré (charte § 3) ; I3 QueryContextAttributesW
             est appelé au plus UNE fois par session (P4 — constaté par
             l'oracle : deux appels = défaut) ; I4 aucune écriture hors
             zone d'émission et cadre ; I5 aucun registre non volatil
             modifié hors cadre.
Échecs :
  E1 : verdict tls-02 non nul d'EncryptMessageW → Q2 (tunnel rompu :
       verdict 5 — la session ferme proprement, compensation tls-05).
  E2 : échec système de tcp-04 (socket serveur morte en cours d'émission)
       → verdict « émission rompue » — la boucle d'achèvement est bornée
       (elle ne tourne jamais sur une socket morte).
  E3 : échec de l'acquisition des tailles (P4) → verdict nommé, AUCUN
       enregistrement entamé.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle à scénarios : span de 1 octet, de message maximal exact,
       de 2 × message maximal + 1 (chaîne de découpe) ; tailles
       négociées exotiques (en-tête 5, queue 16, message 512) ;
       EncryptMessage en verdict 5 au milieu d'une chaîne ; tcp-04 en
       émission partielle exigeant l'achèvement — chaque scénario
       vérifie : clair de l'appelant intact (Q3), zéro octet clair
       résiduel en zone (Q2), compte d'appels QueryContext (I3).
  V3 : fuzzing à propriétés : longueurs hostiles, verdicts shim
       aléatoires — survie, terminaison, bornes respectées.
  V4 : test de rejet : toute notation modifiant le tampon de l'appelant,
       fermant une socket ou journalisant un octet est refusée.
Fixtures    : cadre de session TLS, zone d'émission, shims SSPI.
Provenance  : écrite-avant-code.
Décisions   : D45, D77, charte M4 § 3, § 6, § 8.
