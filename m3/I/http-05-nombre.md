http-05 · nombre décimal borné · révision 1
Intention : convertir un span de chiffres ASCII en u32 SANS jamais
déborder — chaque chiffre est accumulé après test de borne (aucun
enroulement silencieux u64→u32), et la forme elle-même est validée : vide,
trop long, non-chiffre et zéros de tête sont des verdicts nommés (le
durcissement Content-Length anti-contrebande de la RFC 7230 §5.5).
Contrat :
  pre  : P1 rcx pointe le span (octets quelconques reçus) ;
         P2 rdx contient la longueur du span (u64) ;
         P3 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 succès (rax = 0) : edx contient la valeur u32 (de 0 à
             0xFFFFFFFF) ;
         Q2 span vide (longueur 0) → rax = 1 ;
         Q3 longueur > 10 chiffres → rax = 2 (dépassement garanti de la
             plage u32) ;
         Q4 caractère hors '0'-'9' n'importe où → rax = 3 (les espaces, le
             signe, le point et l'hexadécimal sont refusés — aucun
             tolérancement de format) ;
         Q5 valeur à 10 chiffres > 0xFFFFFFFF → rax = 4 (débordement
             arithmétique nommé) ;
         Q6 zéros de tête (longueur > 1, premier octet '0') → rax = 5 —
             sauf la valeur exacte « 0 » (longueur 1) : durcissement
             anti-contrebande, la RFC 7230 §5.5.1 EXIGE le rejet des
             zéros de tête sur Content-Length ;
         Q7 sur tout verdict non nul, edx est inchangé (aucune valeur
             partielle n'est jamais publiée).
  inv  : I1 feuille pure : aucun appel, aucun IAT, aucun état, aucune
             écriture mémoire ; I2 l'accumulation est testée À CHAQUE
             chiffre : valeur_courante > (0xFFFFFFFF - chiffre) / 10 avant
             toute multiplication — l'invariant est qu'aucune opération
             arithmétique non bornée n'existe dans le bloc ; I3 aucune
             hypothèse de terminaison NUL ; I4 non-volatils préservés.
Échecs :
  E1 : verdicts 1-6 (Q2-Q6) — l'appelant (http-10) répond 400 pour toute
       longueur de corps mal formée : une longueur ambiguë n'est jamais
       devinée.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 20 000 spans (frontières 0/1/9/
       10/11 chiffres, 4294967295 et 4294967296, « 0 », « 00 », « 007 »,
       « 1a », « 1 2 », « +1 », « -1 », vide, NUL binaires) — verdict et
       valeur exacts contre modèle, edx intact sur échec (couvre P1-P3,
       Q1-Q7, I1-I4).
  V3 : fuzz P1-P5 sur spans non fiables (D45) : survie, terminaison,
       verdict conforme, aucune écriture mémoire (couvre I1).
  V4 : test de rejet : toute notation accumulant sans test de borne par
       chiffre (multiplication puis troncature) est refusée (couvre I2).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D8, D19, D45, D46.
