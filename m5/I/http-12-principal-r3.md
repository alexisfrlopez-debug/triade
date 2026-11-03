http-12 · orchestration du proxy · révision 3 — la CLI et la porte M5
Intention : la pièce exigée par la composition D136 avant le critère (b) —
l'orchestrateur scellé lance encore http-10:R2 @0x74C0 (la session 0.5.1,
qui ne connaît pas le relèvement) et ne sait ni lire une ligne de commande ni
garder la couche M5. La révision câble la boucle d'acceptation sur
http-10:R3 @0x81C0 (la session révisée : routage du verdict 5 + ligne de
flux), ARME la politique --relever-https à partir des arguments, porte avec
elle la porte R10 .text4 (marche aux bornes, miroir D95) et nomme la
politique au journal (« relever-https arme ») quand elle est armée — le
processus ne démarre JAMAIS en silence avec un drapeau mal orthographié.
Ancêtre : http-12:R2 (D95, embarquée 0.5.1 @0x7DC0 — spécification m4/I/,
citée non recopiée T5 ; balise immuable § 9). La révision câble, arme et
ferme — elle ne touche à RIEN d'autre : l'initialisation est l'héritage
instruction pour instruction (à la géométrie du plan près).
RENUMÉROTATION : l'intention écrite-avant-code (m5/I/README.md, D136) disait
« http-12:R2 » ; le nom est PRIS par le câblage D95 — la révision CLI est
http-12:R3, ancêtre http-12:R2 (verdict v8).
Contrat :
  pre  : P1 le bloc est le point d'entrée PE de proxy.exe — DÉSORMAIS
             0x8C80 (.text4, delta PE documenté — 2e réarrêt D8 sur la
             mesure réelle : http-10:R3 a grandi du ROUTAGE du verdict 5
             aux trois dispatches et du FORÇAGE E2 du port effectif 443,
             le pas 0x81C0+0xAC0 pousse l'entrée de 0x8C40 à 0x8C80 ;
             les ancêtres @0x7DC0 et
             @0x1800 restent embarqués octet pour octet, R7, indexés par la
             carte — morts au lancement, vivants à la preuve d'héritage) ;
         P2 la pile est alignée à l'entrée (rsp ≡ 8 mod 16, convention
             chargeur) ;
         P3 l'état .data est à l'état image (handles nuls, drapeaux nuls,
             R_POLITIQUE = 0, section critique NON initialisée) — repris
             de R1/R2.
  post : Q1 [porte R10 héritée] avant tout effet : la table .rdata M3/M4
             est parcourue de R_TAB_SUM (0x2660) à la BORNE — l'adresse de
             R_VERSION (0x2820), JAMAIS son contenu — 28 entrées, fail-
             closed sur entrée trouée (rva nul / taille nul = KO), somme
             additive 64 bits des qwords du bloc visé == somme attendue ;
         Q1bis NOUVEAU [porte M5] : la table .rdata M5 est parcourue de
             R_TAB_SUM_M5 (0x2EA0) à SA BORNE (R_BORNE_M5 = 0x2EB0) — UNE
             entrée (0x8000, 0x2000, somme .text4) : fail-closed sur
             entrée trouée, même contrat que la porte héritée (miroir
             D95 — la porte se garde elle-même, le bloc 0x8C80 est DANS
             la plage gardée) ;
         Q1ter : version >= 0x00040000 (plancher M3 inchangé, monotonie
             anti-rollback) ; tout écart des trois contrôles : ligne
             unique « TRIADE M3 : integrite KO, arret » par hello-02,
             ExitProcess(1), AUCUN appel réseau ;
         Q2 NOUVEAU [la CLI naît] : GetCommandLineW (IAT M5, I1) — l'argument
             0 (chemin du programme, entre guillemets ou non) est SAUTÉ ;
             chaque argument suivant est comparé BYTE-EXACT (UTF-16, casse
             sensible) à L"--relever-https" (fixture R_CMD_RELEVER, 15
             caractères larges) : égal → R_POLITIQUE (.data) = 1 ; TOUT
             autre argument non vide → REFUS NOMMÉ : ligne « TRIADE M5 :
             argument inconnu, arret » par hello-02 (GSH propre, miroir
             .integrite_ko), ExitProcess(3), AUCUN appel réseau, AUCUNE
             initialisation (E4) ; la comparaison est CASE-SENSITIVE
             (un drapeau mal cassé est un argument inconnu, pas un
             synonyme) ; la politique est écrite AVANT toute
             initialisation (l'ordonnanceur n'a pas commencé : aucun
             fil, aucune socket) ;
         Q3 initialisation dans l'ordre — l'héritage R1/R2 TEL QUEL :
             GetStdHandle(-11) puis (-10) cachés en .data,
             InitializeCriticalSection(R_CS) AVANT toute émission (D42),
             bannière, [NOUVEAU : SI R_POLITIQUE == 1, la ligne console
             tcp-11 « relever-https arme » — l'état nommé de la
             politique, UNE fois, avant toute écoute], tcp-01 (écoute),
             thread console (tcp-06 sur http-11 @0x5D80), échecs →
             ExitProcess(2) avec journal ;
         Q4 boucle : tcp-02 (acceptation) ; socket valide → tcp-06 sur
             http-10:R3 (0x81C0) avec la socket en argument — LE
             CÂBLAGE 0.6.0, l'unique différence fonctionnelle de
             routage avec R2 —, handle fermé, boucle ; acceptation en
             échec : R_QUIT posé → journal « arret », WSACleanup,
             ExitProcess(0) ; sinon → journal « erreur reseau, arret »,
             ExitProcess(2) ;
         Q5 le processus se termine TOUJOURS par ExitProcess (0 arrêt
             demandé, 1 intégrité, 2 erreur structurale, 3 refus CLI)
             — repris et étendu.
  inv  : I1 appels système : IAT kernel32 GetStdHandle,
             InitializeCriticalSection, ExitProcess, CloseHandle,
             GetCommandLineW (LA seule entrée nouvelle — IAT M5 propre,
             les slots scellés M3/M4 ne bougent pas, R7) ; IAT ws2_32
             WSACleanup ; appels directs : hello-02, tcp-01, tcp-02,
             tcp-06, tcp-11 ; cibles de CODE par lea (pointeurs de
             fonctions passés à tcp-06) : http-11 @0x5D80, http-10:R3
             @0x81C0 — JAMAIS http-10:R2 (0x74C0) ni http-10:R1 (0x5580)
             (le contre-câblage est la falsification nominale de V4) ;
         I2 l'ordre d'initialisation de Q3 est un invariant (leçon D42)
             — la ligne de politique s'insère entre la bannière et
             l'écoute, tous les ordres hérités restent relatifs ;
         I3 la porte précède TOUT autre effet — les DEUX marches aux
             bornes et la version avant la CLI, la CLI avant toute
             initialisation ; I4 handles de threads fermés
             immédiatement ; I5 la couche .text4 est gardée par SA
             PROPRE entrée dans la table M5 (0x8000, 0x2000 — le bloc
             0x8C80 est DANS la plage : la porte se garde elle-même,
             miroir D95) ; aucun stockage sous rsp ; I6 la CLI est
             lue UNE fois — aucun re-scan, aucun état caché.
Échecs :
  E1 : intégrité KO (somme divergente, entrée trouée, version sous
       plancher — table héritée OU porte M5) → ExitProcess(1) avant
       tout effet ;
  E2 : échec d'écoute ou de lancement de console → ExitProcess(2) ;
  E3 : acceptation en échec sans arrêt demandé → ExitProcess(2) ;
  E4 : argument inconnu → ligne nommée + ExitProcess(3) avant toute
       initialisation — le refus est un ÉTAT consigné, jamais un
       silence ni un démarrage au mieux.
Vecteurs :
  V1 : round-trip de notation 100 % (R3 ET les deux ancêtres R1/R2
       assemblés à leurs RVA — le préalable du différentiel).
  V2 : différentiel d'ancêtre — R2 émulé contre R3 émulé sur les mêmes
       scénarios (sans argument : ordre exact Q3, démarrage nominal ;
       corruption .text4 squelette ; accepts successifs ; quit ; échecs
       E2/E3) : traces IDENTIQUES sauf la cible du spawn session
       (0x74C0 → 0x81C0 — la divergence LÉGITIME unique) ; la CLI (avec
       argument, argument inconnu, casse mixte, guillemets, arguments
       multiples) est un domaine NOUVEAU sans ancêtre — le modèle de
       marche + de parsing (écrit depuis la SPÉCIFICATION) juge
       l'émulation (les OCTETS).
  V3 : fuzz de la porte M5 — toute mutation d'un champ d'entrée (rva,
       taille, somme) ou tout octet retourné dans [0x8000, 0xA000) →
       KO, jamais de passage silencieux (propriété calculée par le
       modèle de marche, jamais par la notation) ; fuzz CLI — toute
       casse, toute troncature, tout suffixe de --relever-https est un
       refus nommé (E4), jamais un armement.
  V4 : falsification — mutations d'un point stables en taille (leçon
       D82) attrapées : le contre-câblage (lea → 0x74C0 ou 0x5580), la
       borne M5 décalée (±0x10), le plancher abaissé, l'ordre
       d'initialisation, la politique armée sans argument, l'argument
       inconnu accepté en silence, le code de sortie E4 ; témoin vert.
Fixtures    : héritage R7 intégral (bannière 40 o, « erreur reseau, arret »
              22 o, « arret » 7 o, ligne KO 33 o) ; NOUVELLES fixtures M5
              (layout, zone .rdata M5) : « TRIADE M5 : argument inconnu,
              arret » 37 o, « relever-https arme » 20 o,
              L"--relever-https" 32 o ; l'entrée porte M5 est propriété du
              build (somme recalculée du binaire final, table générée).
Provenance  : écrite-avant-code (révision inter-jalon, modèle http-12:R2).
Décisions   : D8, D42, D45, D63, D77, D94, D95 (ancêtre), D136, D140,
              D141/D142/D143 (le décor), verdict v8 (renumérotation R3) ;
              arrêt .text4 réarrêté sur la mesure (0x8C80, layout D8 —
              2e réarrêt : 0x8C40 → 0x8C80, http-10:R3 mesurée 0xAC0).
