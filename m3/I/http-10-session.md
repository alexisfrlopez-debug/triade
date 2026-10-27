http-10 · session proxy · révision 1
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
         P3 la pile du thread (défaut système ~1 Mio) est vierge — le
             cadre de session (tampon d'accumulation 16 Kio ≥ MAX_TETE+1
             de http-06, tampon de réécriture 12 Kio, zones d'accueil des
             champs) vit entièrement dans le cadre ;
         P4 WSA est actif (tcp-01 a réussi dans http-12) ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 accumulation : boucle tcp-03 (réception, capacité restante du
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
             amont→cliente dans un thread détaché, puis pompe
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
             http-09 cliente→amont jusqu'à total Content-Length (sans
             Content-Length : aucun corps — les octets excédentaires
             reçus pendant l'accumulation sont ignorés : M3 = UNE
             requête par connexion, documenté) ; puis relais réponse :
             http-09 amont→cliente jusqu'à fermeture amont (le cadrage
             de la réponse appartient au serveur amont et au client —
             M3 ne parse AUCUNE réponse : ce qui n'est pas parsé ne peut
             pas être mal parsé) ;
         Q5 fermetures : sur TOUT chemin de fin, la socket amont (si
             ouverte) puis la socket cliente sont fermées (tcp-05),
             chacune EXACTEMENT une fois, par ce thread, avant tout
             journal final ; la ligne « fin » est journalisée (tcp-11)
             puis le thread rend la main par ret — jamais ExitThread
             (miroir tcp-09:I2) ;
         Q6 journal : « connexion » à l'entrée, « tunnel » à
             l'établissement d'un CONNECT, « fin » au départ — lignes
             courtes, discipline tcp-11:P4.
  inv  : I1 appels directs : tcp-03, tcp-04, tcp-05, tcp-06, tcp-11,
             tcp-13, http-01, http-02, http-04, http-05, http-06,
             http-07, http-08, http-09 — AUCUN IAT direct (la surface
             système est intégralement déléguée aux blocs scellés) ;
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
             réponse.
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
  V5 : test de rejet : toute notation appelant un IAT direct, un bloc
       hors I1, ou lisant une zone d'accueil après verdict non nul est
       refusée (couvre I1, I3).
Fixtures    : table des réponses .rdata (7 lignes statiques : « HTTP/1.1
              400 Requete mal formee », « HTTP/1.1 431 Tete trop grande »,
              « HTTP/1.1 501 Non implemente », « HTTP/1.1 411 Longueur
              requise », « HTTP/1.1 505 Version non supportee », « HTTP/1.1
              502 Passerelle inaccessible », « HTTP/1.1 200 Tunnel etabli »
              — chacune terminée par CRLF CRLF, copie unique) ; requêtes
              dorées partagées (GET/POST/CONNECT tels qu'émis par curl —
              propriété de la suite, référencées par l'oracle et le
              harnais).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D19, D42 (pre P2), D45, D46.
