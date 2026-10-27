http-04 · recherche d'en-tête · révision 1
Intention : retrouver la PREMIÈRE valeur d'un en-tête par son nom dans un
bloc d'en-têtes isolé (la région après la ligne de requête) — la
comparaison de noms insensible à la casse (obligatoire, RFC 7230 §3.2)
appartient à ce bloc seul : c'est l'unique comparaison non sensible du
domaine http, ici et nulle part ailleurs.
Contrat :
  pre  : P1 rcx pointe le début du bloc d'en-têtes (première ligne
             d'en-tête, après la ligne de requête — l'appelant fournit la
             région, ce bloc ne saute jamais la première ligne) ;
         P2 rdx contient la longueur du bloc (u64, jusqu'à la fin de la
             tête incluse) ;
         P3 r8 pointe le nom cherché (span, jamais modifié), r9 contient
             sa longueur (u64 > 0) ;
         P4 le 5e argument ([rsp+0x20] à l'entrée, loge conventionnelle)
             pointe la zone d'accueil « champs en-tête » de http-03
             (32 octets, pile de l'appelant) ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 trouvé (rax = 0) : la zone contient les champs de la PREMIÈRE
             occurrence (les doublons suivants sont ignorés — comportement
             défini) ; la recherche s'arrête au premier nom égal ;
         Q2 absent (rax = 1) : aucune occurrence — la zone est intacte ;
             la ligne vide (fin des en-têtes, longueur 0 par http-01)
             termine la recherche proprement ;
         Q3 tête invalide (rax = 2) : une ligne du bloc échoue au parsing
             http-03 (verdict non nul) — la recherche s'arrête
             immédiatement, la zone est intacte : la malformation est
             propagée, jamais contournée.
  inv  : I1 appels directs : http-01 (itération de ligne — propriété T5 du
             balayage CRLF), http-03 (parsing de chaque ligne) ; I2 aucun
             IAT, aucun état, aucune écriture hors la zone d'accueil ;
         I3 la comparaison de noms est insensible à la casse ASCII (A-Z
             versus a-z uniquement, 0x20 d'écart) — boucle locale de ce
             bloc, seul propriétaire (toute autre comparaison du domaine
             http est sensible : méthodes, versions, schémas) ;
         I4 le nom cherché n'est jamais recopié ni modifié ; I5
             non-volatils préservés ; I6 le bloc rend la main au premier
             verdict tranchant (trouvé, absent-fin-de-tête, invalide) —
             aucun balayage au-delà.
Échecs :
  E1 : bloc d'en-têtes mal formé → rax = 2 : l'appelant (http-10) répond
       400 — un proxy qui parcourt une tête invalide ne fait aucune
       supposition sur la suite.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 15 000 blocs générés (noms
       présents en 1/N occurrences, casses mélangées Host/hOsT/HOST,
       chercheurs de longueurs 0/1/N, blocs se terminant par la ligne vide,
       blocs contenant une ligne invalide en position k, noms préfixes les
       uns des autres — « Host » versus « Hostx ») — verdict, première
       occurrence exacte, zone intacte sur non-trouvé (couvre P1-P5, Q1-Q3,
       I1-I6).
  V3 : fuzz P1-P5 sur blocs non fiables (D45) : survie, terminaison
       bornée, verdict conforme au modèle (couvre I1, I6).
  V4 : test de rejet : toute notation comparant par libc-02 (sensible) ou
       recopiant le nom cherché est refusée (couvre I3, I4).
Fixtures    : néant (les blocs viennent du tampon de l'appelant ; les noms
              signifiants — Host, Content-Length, Transfer-Encoding —
              appartiennent aux fixtures de http-10, consommateur).
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
