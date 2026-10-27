http-02 · ligne de requête · révision 1
Intention : découper UNE ligne de requête isolée (par http-01) en champs
typés — méthode, cible, version — chaque champ étant un span (ptr, longueur)
dans le tampon d'origine, jamais une copie : la table des huit méthodes est
LA validation (un jeton hors table est rejeté nommément — rien d'inconnu
n'est jamais transmis).
Contrat :
  pre  : P1 rcx pointe la ligne (sans CRLF — garantie par http-01:Q1) ;
         P2 rdx contient la longueur de la ligne (u64, peut être 0) ;
         P3 r8 pointe la zone d'accueil « champs requête » de 56 octets
             fournie par l'appelant (pile) : méthode enum u32 @0, version
             enum u32 @4, méthode ptr u64 @8, méthode longueur u64 @16,
             cible ptr u64 @24, cible longueur u64 @32, version ptr u64
             @40, version longueur u64 @48 ;
         P4 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès (rax = 0) : la zone est remplie — méthode enum
             (GET=1, HEAD=2, POST=3, PUT=4, DELETE=5, OPTIONS=6, TRACE=7,
             CONNECT=8), version enum (HTTP/1.0=1, HTTP/1.1=2), et les
             trois spans pointent DANS la ligne d'origine ;
         Q2 structure exigée : MÉTHODE SP CIBLE SP VERSION — exactement un
             seul espace (0x20) entre chaque champ, trois champs non vides,
             rien après la version ; tout écart → rax = 2 (structure), la
             zone d'accueil est intacte (aucune écriture partielle) ;
         Q3 méthode : le jeton doit correspondre EXACTEMENT (sensible à la
             casse — RFC 7230 §5.1.1) à une entrée de la table .rdata des
             huit méthodes ; sinon rax = 1 (méthode inconnue) ;
         Q4 version : le span version doit être exactement « HTTP/1.0 » ou
             « HTTP/1.1 » (sensible à la casse) ; sinon rax = 3 (version
             non supportée — couvre HTTP/0.9, HTTP/2.0, minuscules,
             troisièmes champs) ;
         Q5 cible : longueur dans [1, 2048] (MAX_CIBLE, constante nommée de
             ce bloc — limite d'usage des URI légitimes, repère navigateurs
             ~2048) ; sinon rax = 4 (cible vide ou excessive).
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture hors la zone d'accueil (56 octets) ; I2 la comparaison
             de méthode est une lecture de table .rdata (huit entrées
             ptr/longueur) — la table est la propriété de ce bloc, la
             réécriture de requête (http-10) réutilise le SPAN, jamais la
             table (aucune connaissance dupliquée) ; I3 aucune hypothèse de
             terminaison NUL (spans seulement) ; I4 non-volatils préservés.
Échecs :
  E1 : méthode hors table → rax = 1 : l'appelant (http-10) répond 501 et
       clôt (aucune méthode inconnue n'est relayée en aveugle) ;
  E2 : structure non conforme (espaces multiples, champ manquant, ligne
       vide en tête de requête) → rax = 2 : réponse 400 (le tolérancement
       des CRLF initiaux et des espaces multiples, permis en MAY par la
       RFC, est refusé — durcissement anti-contrebande) ;
  E3 : version non supportée → rax = 3 : réponse 505 ;
  E4 : cible vide ou > 2048 octets → rax = 4 : réponse 400.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 lignes générées (les huit
       méthodes, casse mélangée, espaces 0/1/2/3, versions valides et
       proches — HTTP/1.1, HTTP/1.0, HTTP/0.9, HTTP/2.0, http/1.1 —,
       cibles 0/1/2048/2049 octets, fin de ligne après le 2e champ,
       traînées) — verdict et champs exacts contre modèle ; zone intacte
       sur tout verdict non nul (couvre P1-P4, Q1-Q5, I1-I4).
  V3 : fuzz P1-P5 sur lignes non fiables (D45) : survie, terminaison,
       verdict conforme, aucune écriture hors zone (couvre I1).
  V4 : test de rejet : toute notation écrivant la zone avant le verdict
       final, ou lisant hors [ligne, ligne+longueur), est refusée (couvre
       I1, Q2).
Fixtures    : table des méthodes .rdata (GET, HEAD, POST, PUT, DELETE,
              OPTIONS, TRACE, CONNECT — huit entrées ptr/longueur, la
              longueur fait partie de la fixture) ; fixtures partagées de
              requêtes dorées (http-10).
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
