http-08 · cible · révision 1
Intention : classer la cible d'une requête par sa forme et la découper —
forme absolue (schéma http, autorité, chemin), forme origine (chemin seul,
l'autorité viendra de l'en-tête Host), forme autorité (CONNECT) — sans
JAMAIS interpréter l'autorité (http-07) ni recopier un octet : ce bloc
découpe, les autres décident.
Contrat :
  pre  : P1 rcx pointe le span cible (issu de http-02, octets quelconques) ;
         P2 rdx contient sa longueur (u64 > 0 — garantie http-02:Q5) ;
         P3 r8d contient l'enum méthode de http-02 (CONNECT=8 est la seule
             méthode admettant la forme autorité) ;
         P4 r9 pointe la zone d'accueil « cible résolue » de 40 octets
             (pile de l'appelant) : forme enum u32 @0, autorité ptr u64
             @8, autorité longueur u64 @16, chemin ptr u64 @24, chemin
             longueur u64 @32 ;
         P5 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès (rax = 0), la zone est remplie selon la forme :
             ABSOLUE=1 — schéma « http:// » exact (MINUSCULES,
             sensible à la casse : durcissement, tous les émetteurs
             réels émettent minuscules et le schéma est le seul point de
             tolérance que nous refusons), puis span autorité (jusqu'au
             premier « / », « ? » ou fin — NON interprétée, renvoi à
             http-07), puis span chemin (du « / » jusqu'à la fin,
             éventuellement reconstruit : une forme absolue sans chemin
             (« http://hôte ») rend le chemin « / » PAR DÉFAUT DÉFINI —
             un pointeur sur la chaîne « / » .rdata de ce bloc, longueur
             1) ; l'autorité peut être vide → verdict Q3 ;
             ORIGINE=2 — la cible entière est le chemin ; l'autorité est
             rendue vide (ptr = 0, longueur = 0) : l'autorité EFFECTIVE
             est la valeur de l'en-tête Host, affaire de http-10 ;
             AUTORITÉ=3 — méthode CONNECT : la cible entière est le span
             autorité ; le chemin est rendu vide (ptr = 0, longueur = 0) ;
         Q2 forme origine invalide (premier octet différent de « / » —
             couvre la forme astérisque « * » et toute autorité nue hors
             CONNECT) → rax = 1 (forme refusée) ;
         Q3 autorité vide en forme absolue → rax = 2 (« http:// » seul,
             « http:///chemin ») ;
         Q4 schéma non supporté → rax = 3 : tout préfixe de schéma suivi
             de « :// » qui n'est pas exactement « http » (y compris
             « https », « ftp », « HTTP », « Http ») — le tunnel TLS est
             l'affaire de CONNECT (M4 fera son lit), jamais d'un schéma
             https en requête directe ; une cible sans « :// » et sans
             « / » initial est une forme origine invalide (Q2) ou une
             autorité hors CONNECT (Q2) — tout octet d'entrée a un
             comportement défini ;
         Q5 sur tout verdict non nul, la zone est intacte.
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture hors la zone d'accueil, aucune écriture partielle ;
         I2 aucun octet de la cible n'est recopié (spans dans le tampon
             d'origine, sauf le chemin par défaut « / » .rdata — chaîne
             fixture de ce bloc) ; I3 le découpage absolu s'arrête au
             PREMIER « / » ou « ? » après l'autorité (la requête « ?q=1 »
             sans chemin rend le chemin « / » — défini, pas déduit) ;
         I4 non-volatils préservés ; I5 aucune hypothèse de terminaison
             NUL.
Échecs :
  E1 : verdicts 1-3 (Q2-Q4) — l'appelant (http-10) répond : forme refusée
       ou autorité vide → 400 ; schéma non supporté → 501.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 15 000 cibles générées
       (absolues avec/sans chemin, avec « ? », ports dans l'autorité,
       origines avec requêtes longues, astérisque, autorités nues,
       schémas http/https/HTTP/ftp/vides, cibles « / » seul, CONNECT avec
       cible origine, GET avec cible autorité) — verdict, forme, bornes
       des spans contre modèle ; zone intacte sur échec (couvre P1-P5,
       Q1-Q5, I1-I5).
  V3 : fuzz P1-P5 sur cibles non fiables (D45) : survie, terminaison,
       verdict conforme, aucune écriture hors zone (couvre I1).
  V4 : test de rejet : toute notation interprétant l'autorité (découpe
       hôte/port ici) ou recopiant la cible est refusée (couvre I2 — la
       connaissance d'autorité appartient à http-07).
Fixtures    : chaîne « / » .rdata (chemin par défaut, 1 octet — fixture de
              ce bloc, propriété unique).
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
