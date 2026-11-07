loupe-06 · md5 d'une gamme : l'empreinte du quotidien, notée neuve · révision 1
Intention : le condensé MD5 d'une gamme du fichier ouvert — LA NOUVELLE
NOTATION du domaine (aucun héritage : MD5 n'existe pas au projet, le
quotidien le réclame — toutes les pièces vivent par leur md5 au journal
des builds). Le cœur est pur (les tables publiques .rdata, dérivées par
arithmétique), la lecture par fenêtres glissantes de 64 Kio le joint au
fichier. MD5 N'EST PAS UNE PREUVE DE SÉCURITÉ — c'est l'empreinte de
cohérence du quotidien, la spec le nomme et le domaine s'en tient là.
Contrat :
  pre  : P1 la session est ouverte ; P2 rcx = le décalage (≥ 0), rdx =
             la longueur (≥ 0) ; P3 décalage + longueur ≤ taille ;
         P4 r8 = la sortie, 16 o accessibles en écriture.
  post : Q1 la sortie = MD5(F[décalage .. décalage + longueur)) —
             RFC 1321 : le contexte 88 o (A,B,C,D u32 @ +0 · longueur
             u64 @ +16 · tampon[64] @ +24) tenu SUR LA PILE ; le petit-
             boutisme DE MD5 (le condensé sérialisé little-endian, RFC
             1321 § 3.2 — le miroir exact du grand-boutisme SHA : les
             deux empreintes du panneau, les deux boutismes) ;
         Q2 LE CŒUR : l'initialisation aux QUATRE abscisses (0x67452301,
             0xEFCDAB89, 0x98BADCFE, 0x10325476), les SOIXANTE-QUATRE
             tours par blocs de 64 (les décalages MD5_S, les
             constantes MD5_T — les tables PUBLIQUES du plan
             d'adressage, DÉRIVÉES PAR ARITHMÉTIQUE au geste (a) : T[i]
             = floor(2^32 · |sin(i+1)|), le vérificateur les
             re-dérive), le bourrage 0x80 puis les zéros, la longueur
             sur 64 bits, l'extraction des QUATRE mots ;
         Q3 les fenêtres : SetFilePointerEx + ReadFile dans TAMPON_CUMUL
             (au plus 64 Kio), le cœur nourri fenêtre à fenêtre — un
             fichier de 2 Gio se condense, jamais tout en mémoire ;
         Q4 la gamme vide rend d41d8cd98f00b204e9800998ecf8427e (le
             vecteur RFC 1321) ; Q5 rax = 0.
  inv  : I1 le cœur ne déclare AUCUNE entrée IAT (le calcul pur — la
             lecture seule porte l'IAT : SetFilePointerEx, ReadFile,
             GetLastError, la liste fermée du bloc) ;
         I2 les tables MD5_S/MD5_T sont des DONNÉES PUBLIQUES en
             lecture seule (.rdata) — la source unique vit au plan
             d'adressage, jamais re-déclarée ;
         I3 la lecture passe par TAMPON_CUMUL (l'exclusion de famille —
             jamais deux flux), le tampon de vue INTACT ;
         I4 le contexte ne survit pas au retour (la pile le rend) ;
             registres non volatils rendus ; NOP, 0x90 ;
         I5 MD5 N'EST PAS UNE PREUVE : aucune décision de sécurité du
             projet ne repose sur ce bloc — l'empreinte de cohérence
             du quotidien, RIEN DE PLUS.
Échecs :
  E1 : sans session (P1) → verdict -4 SESSION, rax = -4.
  E2 : la gamme hors fichier (P3) → verdict -3 HORS-BORNES, rax = -3.
  E3 : la sortie inutilisable (P4) → verdict -5 ENTRÉE, rax = -5.
  E4 : ReadFile ou SetFilePointerEx en échec → verdict -6 SYSTÈME, le
       code GetLastError consigné, la sortie INTACTE (jamais un
       condensé partiel).
Vecteurs :
  V1 : doré — LES SEPT VECTEURS OFFICIELS RFC 1321 (le vide, « a »,
       « abc », « message digest », l'alphabet minuscule, l'alphabet
       mixte, « 1234567890 » ×8) : les condensés exacts, octet pour
       octet, AU FICHIER (les gammes d'un témoin composé pour eux)
       (couvre Q1, Q2, Q4, Q5).
  V2 : différentiel — 1 000 gammes aléatoires des témoins + proxy.exe
       scellé, comparées à hashlib.md5 : l'égalité exacte (couvre Q1,
       Q3).
  V3 : rejet — sans session, hors bornes, sortie nulle : les TROIS
       verdicts nommés (couvre E1, E2, E3).
  V4 : rejet — le shim ReadFile en échec : verdict -6, la sortie
       intacte, le code consigné (couvre E4).
  V5 : falsification — une constante MD5_T mutée d'un ulp à la table
       .rdata : les sept vecteurs dorés échouent — la falsification
       ATTRAPÉE PAR LES VECTEURS OFFICIELS.
Fixtures    : les SEPT vecteurs RFC 1321 (le témoin du kit les porte) +
              proxy.exe scellé (md5 recoupé par hashlib au labo —
              l'empreinte que le projet consigne à chaque build).
Provenance  : écrite-avant-code.
Décisions   : D171, D161 (les tables dérivées avant la notation), D7/D35
              (l'IAT), D134 (le journal des builds vit de ces
              empreintes).
