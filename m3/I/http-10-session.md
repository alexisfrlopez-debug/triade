http-10 · session proxy · révision 3
Intention : servir UNE connexion cliente de bout en bout dans son thread —
accumuler la tête, la PARSER par les blocs http-01..08 (chaque octet non
fiable a un comportement défini), trancher (requête ordinaire ou tunnel
CONNECT), router vers l'amont (tcp-13), réécrire la ligne de requête,
pomper dans les deux sens, et clôturer — chaque socket fermée exactement
une fois, par CE thread, jamais ailleurs (miroir de tcp-09:Q2).
Contrat :
  pre  : P1 rcx contient la socket cliente connectée (argument transmis
             par tcp-06 depuis http-12) ;
         P2 la section critique du journal et le handle stdout sont
             initialisés par http-12 AVANT le premier accept (leçon D42 :
             le devoir d'initialisation de l'hôte est ici UN CONTRAT, pas
             une supposition) ;
         P3 la pile du thread (réserve ~1 Mio, dont UNE SEULE PAGE est
             committée à la naissance du thread, guard page dessous —
             terrain 21:38/D63 : le commit PE initial est 0x1000) — le
             cadre de session (tampon d'accumulation 16 Kio ≥ MAX_TETE+1
             de http-06, tampon de réécriture 12 Kio, zones d'accueil des
             champs) vit entièrement dans le cadre ET doit être étendu
             page par page par le probing de Q0 avant toute écriture ;
         P4 WSA est actif (tcp-01 a réussi dans http-12) ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q0 prologue : AVANT le sub rsp, 0x7100, une boucle de probing
             touche une adresse de chaque page du cadre en DESCENDANT
             (rsp-0x1000, rsp-0x2000, …, rsp-0x7000, puis rsp-0x7100 :
             la page du bas exact) — chaque touche étend la pile par la
             guard page AU PLUS UNE page sous la zone déjà garantie ;
             registres de travail volatils (r10 compteur, rax touche),
             rsp INCHANGÉ (l'alignement ABI de la R2 est préservé),
             rcx (socket) intact ; SANS ce probing, la première écriture
             au bas du cadre saute la guard page et lève c00000fd —
             mort DU PROCESSUS ENTIER (leçon terrain 21:38/D63 : la
             bannière était sortie, puis silence total du tuyau, RST au
             client, jamais d'« arret ») ;
         Q1 accumulation : boucle tcp-03 (réception, capacité restante du
             tampon) jusqu'au verdict http-06 : complet → parsing ;
             incomplet → continuer ; limite (2) → réponse 431, fin ;
             LF isolé (3) → réponse 400, fin ; réception 0 ou -1 pendant
             l'accumulation → fin SANS réponse (le pair est parti ou
             muet — rien à répondre) ;
         Q2 parsing (tout verdict non nul → la réponse nommée de la table
             E1-E8, émise au client, puis fin de session) : http-01
             isole la ligne de requête (ligne vide en tête → 400) ;
             http-02 (champs requête) ; http-04 cherche « Host »,
             « Content-Length », « Transfer-Encoding » ; http-08 (forme) ;
             http-07 sur l'autorité (span de la cible absolue/autorité,
             ou valeur Host en forme origine — défaut de port 80, sauf
             forme autorité où le port est exigé : défaut 0) ;
             Transfer-Encoding présent (valeur non vide) → 501 (le
             relais en flux n'est pas dans le périmètre M3 — refus
             honnête, jamais de tentative) ; Content-Length présent mais
             invalide (http-05 non nul) → 400 ; méthode POST/PUT sans
             Content-Length et sans Transfer-Encoding → 411 ; forme
             origine sans Host → 400 (RFC 7230 §5.4) ;
         Q3 tunnel (méthode CONNECT) : tcp-13 (hôte, port) ; échec →
             502, fin ; succès → émission de « HTTP/1.1 200 Tunnel
             etabli » au client, lancement (tcp-06) d'une pompe http-09
             amont→cliente dans un thread détaché (argument compacté
             (amont<<32)|cliente — handles Win32 significatifs sur 32
             bits, documenté ; le handle est fermé immédiatement après
             restitution, miroir tcp-12:I4), puis pompe http-09
             cliente→amont DANS CE thread ; à la fin de cette pompe :
             fermeture de la socket amont PUIS de la socket cliente
             (l'ordre réveille la pompe sœur en échec nommé — http-09:Q2
             — qui rend la main ; AUCUNE double fermeture n'est
             possible : la fermeture n'appartient qu'ici) ;
         Q4 requête ordinaire : réécriture de la tête dans le tampon de
             réécriture — span méthode (http-02:Q1, octets d'origine) +
             SP + span chemin (http-08 — origine ou absolue, « / » par
             défaut inclus) + SP + span version (http-02, octets
             d'origine — la version du client est relayée telle quelle) +
             CRLF + les en-têtes RECOPIÉS VERBATIM (du début des en-têtes
             à la fin de tête incluse) — émission intégrale vers l'amont
             (tcp-04 en boucle) ; corps : les octets déjà au-delà de la
             longueur de tête sont émis (au plus Content-Length), puis
             relais BORNÉ Content-Length par des boucles tcp-03/tcp-04
             INLINE de la session (R2 : même discipline d'émission
             intégrale octet exact que http-09, mais bornée — http-09,
             à fermeture délimitée, s'arrêterait à l'EOF du client qui
             attend la réponse sur la même connexion) jusqu'à total
             Content-Length (sans Content-Length : aucun corps — les
             octets excédentaires reçus pendant l'accumulation sont
             ignorés : M3 = UNE requête par connexion, documenté) ; puis
             relais réponse : http-09 amont→cliente jusqu'à fermeture
             amont (le cadrage de la réponse appartient au serveur amont
             et au client — M3 ne parse AUCUNE réponse : ce qui n'est
             pas parsé ne peut pas être mal parsé) ;
         Q5 fermetures : sur TOUT chemin de fin, la socket amont (si
             ouverte) puis la socket cliente sont fermées (tcp-05),
             chacune EXACTEMENT une fois, par ce thread, avant tout
             journal final ; la ligne « fin » est journalisée (tcp-11)
             puis le thread rend la main par ret — jamais ExitThread
             (miroir tcp-09:I2) ;
         Q6 journal : « connexion entrante » à l'entrée (ligne déléguée
             par http-12:Q3), « tunnel » à l'établissement d'un CONNECT,
             « fin » au départ — lignes courtes, discipline tcp-11:P4.
  inv  : I1 appels directs : tcp-03, tcp-04, tcp-05, tcp-06, tcp-11,
             tcp-13, http-01, http-02, http-04, http-05, http-06,
             http-07, http-08, http-09 ; IAT kernel32 : CloseHandle
             (handle de la pompe détachée du tunnel, fermé immédiatement
             après restitution — miroir tcp-12:I4 ; unique entrée IAT de
             la session, la surface système est intégralement déléguée
             aux blocs scellés) ;
         I2 le cadre de pile (~0x7100) est alloué au prologue et rendu à
             l'épilogue : tampons, zones d'accueil, sauvegarde rbx,
             r12-r15 ; aucun stockage sous rsp ; les sockets vives dans
             les non-volatils ;
         I3 tout verdict des blocs appelés est testé AVANT usage du
             résultat (fail-closed — aucun champ d'une zone d'accueil
             n'est lu après un verdict non nul) ;
         I4 les chaînes de méthode/version/chemin réémises sont les SPANS
             d'origine ou les fixtures de leurs blocs propriétaires —
             aucune table de méthode n'est recopiée ici (T5) ;
         I5 la table des réponses (7 lignes d'état statiques) est la
             fixture de ce bloc — unique propriété des textes de
             réponse ; les assistants locaux (.emettre émission
             intégrale, .copier copie d'octets, .pompe_amont proc de
             thread) sont des étiquettes internes du bloc, pile
             équilibrée, miroir .protger de tcp-07.
Échecs :
  E1 : défaut de format (http-01/02/03-via-04/05/07/08 non nuls, LF
       isolé, ligne vide en tête, Host requis absent) → réponse 400 ;
  E2 : tunnel sans port (http-07 avec défaut 0) ou cible mal formée →
       400 ; E3 : tête > 8192 (http-06:2) → 431 ; E4 : méthode hors
       table (http-02:1) ou Transfer-Encoding (Q2) ou schéma non http
       (http-08:3) → 501 ; E5 : POST/PUT sans longueur → 411 ;
  E6 : version non supportée (http-02:3) → 505 ; E7 : amont injoignable
       (tcp-13 = 0) → 502 ; E8 : émission vers le client en échec à un
       moment quelconque → fin sans insister (le client est parti) ;
       chaque réponse est émise par tcp-04 en boucle avec le même
       contrat d'émission intégrale.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V6 (R3, D63) : contrôle statique du probing — le prologue contient la
      boucle (mouvements [rsp+r10] par pas de 0x1000, bornes -0x1000 à
      -0x7000, touche finale [rsp-0x7100]) AVANT le sub rsp, 0x7100, et
      l'émulation rejoue les sessions V2 SANS changement de comportement
      (la pile émulée est mappée d'avance : le probing y est inoffensif —
      c'est exactement pourquoi ce défaut était invisible à l'oracle de
      R1/R2) ; en émulation à guard simulée (une page committée, le
      reste marqué indisponible), SANS probing le prologue lève — AVEC,
      il passe.
  V2 : sessions scriptées (oracle, shims réseau) : GET/POST/CONNECT
       complets, CHAQUE verdict E1-E8 injecté (réponse exacte attendue,
       octet près), corps de 0/1/2048 octets, émissions partielles,
       fermeture du pair en accumulation, réécriture exacte (octets
       attendus construits par le modèle), fermetures comptées : chaque
       socket exactement une fois, ordre amont puis cliente (couvre
       P1-P5, Q1-Q6, I1-I5, E1-E8).
  V3 : falsification : détourner UNE fermeture (ne pas fermer, fermer
       deux fois, fermer dans la pompe) DOIT faire échouer l'oracle
       (couvre Q3, Q5).
  V4 : harnais de fuzzing P1-P5 (D45) sur la chaîne complète
       accumulation→parsing (générateurs de têtes hostiles : têtes
       coupées, LF nus, en-têtes dégénérés, corps tronqués) : survie,
       terminaison, réponse conforme au modèle de référence ou
       fin-sans-réponse documentée, aucune écriture hors cadre, aucune
       double fermeture (couvre Q1, Q5, I2, I3) ;
  V5 : test de rejet : toute notation appelant un IAT hors CloseHandle,
       un bloc hors I1, ou lisant une zone d'accueil après verdict non
       nul est refusée (couvre I1, I3).
Fixtures    : table des réponses .rdata (7 lignes statiques : « HTTP/1.1
              400 Requete mal formee », « HTTP/1.1 431 Tete trop grande »,
              « HTTP/1.1 501 Non implemente », « HTTP/1.1 411 Longueur
              requise », « HTTP/1.1 505 Version non supportee », « HTTP/1.1
              502 Passerelle inaccessible », « HTTP/1.1 200 Tunnel etabli »
              — chacune terminée par CRLF CRLF, copie unique) ; noms
              chercheurs « Host », « Content-Length », « Transfer-Encoding »
              (consommateur) ; requêtes dorées partagées (GET/POST/CONNECT
              tels qu'émis par curl — propriété de la suite, référencées par
              l'oracle et le harnais).
Provenance  : écrite-avant-code.
Historique  : R1 (D46) — version initiale écrite-avant-code ; la Q4 décrivait
              le relais du corps comme « http-09 cliente→amont jusqu'à total
              Content-Length » : MÉCANIQUEMENT IMPOSSIBLE (http-09 s'arrête à
              l'EOF du client, qui attend la réponse sur la même connexion —
              la pompe bloquerait). R2 (journal 36, D47) — le corps est
              relayé BORNÉ Content-Length par des boucles tcp-03/tcp-04
              inline de la session (autorisées par I1, même discipline
              d'émission intégrale) ; http-09 reste réservé aux pompes du
              tunnel et au relais de réponse ; I1 gagne l'IAT CloseHandle
              (handle de la pompe détachée — fermé immédiatement, sans
              fuite, miroir tcp-12:I4) ; la Q3 précise le compactage
              d'argument du thread détaché. Contrat stable au sens R4 : les
              verdicts, les réponses et les fermetures de R1 sont inchangés.
Décisions   : D7, D8, D19, D42 (pre P2), D45, D46, D47, D63 (R3).
Historique R3 (D63, terrain 21:38) : la P3 de R2 supposait la pile du
  thread « vierge ~1 Mio » — FAUX sous Windows : CreateThread (pile 0,
  tcp-06:Q2) ne commet qu'UNE page (commit PE 0x1000), le reste est
  réservé derrière une guard page. Le prologue R2 faisait sub rsp,
  0x7100 puis écrivait directement au bas du cadre : première session
  = c00000fd avant TOUTE journalisation, mort du processus entier
  (RST au client → curl code 56 ; port libéré → curl suivant code 7 ;
  tuyau muet après la bannière). L'émulation unicorn mappe la pile en
  entier (pas de guard) : le défaut était invisible à l'oracle — le
  proxy n'avait JAMAIS été exécuté en réel (étape c prévue « sur le
  terrain », journal 37/38). Correctif : Q0 (boucle de probing, miroir
  du __chkstk des compilateurs), P3 réécrite, V6 ajouté. Aucun autre
  bloc n'a de cadre > 0x1000 (balayage D63 : http-09 0x28, http-11
  0x80, tcp-13 0x170…). Contrat stable au sens R4 pour Q1-Q6 : les
  verdicts, réponses et fermetures de R2 sont inchangés.
