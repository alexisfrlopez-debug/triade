shani-03 · SHA-256 : l'absorption tamponnée À DISPATCH SHA-NI/SCALAIRE · révision 1
Intention : LE MÊME CŒUR que tls13-03 — l'invariance de découpage, absorber
N octets quelconques dans le tampon du contexte, comprimer chaque fois que
64 octets sont complets, garder le reste — avec LA SEULE DIFFÉRENCE : la
compression est SÉLECTIONNÉE au geste par dispatch CPUID (l'instruction
lfh49a1xf : « sélectionnée par dispatch CPUID avec repli scalaire sur les
blocs scellés existants »). LA SONDE shani-01 est RAPPELÉE UNE FOIS PAR
APPEL d'absorption (jamais par bloc de 64 o — le sondage par bloc mangerait
le gain : R11, le hot path est la compression) ; le verdict tenu en
registre non volatil, les DEUX sites d'appel DIRECTS et STATIQUES —
shani-02 la variante, tls13-02 LE SCELLÉ à son adresse d'origine (R7).
Contrat :
  pre  : P1 rcx = le pointeur du contexte (initialisé) ;
         P2 rdx = le pointeur des données (N octets lisibles, aucun
             alignement exigé) ;
         P3 r8 = N, la longueur en octets (0 ≤ N ≤ 2^61 — N = 0 est LÉGAL :
             le bloc ne fait rien, rend 0) ;
         P4 la pile alignée 16, l'ombre 0x20 fournie.
  post : Q1 les N octets absorbés : le tampon reçoit le couplage au
             remplissage courant, CHAQUE bloc complet de 64 o est comprimé
             PAR LA VARIANTE shani-02 SI le verdict de la sonde est 1, PAR
             LE SCELLÉ tls13-02 SINON (les DEUX appels DIRECTS aux
             adresses du plan — I1), le remplissage et le total sont mis
             à jour (total += N) ;
         Q2 l'INVARIANCE (le miroir exact de tls13-03 Q2) : l'état final
             du contexte est IDENTIQUE quel que soit le découpage des
             mêmes octets en appels successifs — ET QUEL QUE SOIT LE
             CHEMIN du dispatch : le condensé d'une gamme est LE MÊME sur
             la machine SHA-NI (chemin matériel) et sur le processeur
             sans SHA (chemin scellé) — l'égalité scalaire/SHA-NI est la
             propriété fondatrice, prouvée au corpus aléatoire ;
         Q3 les données d'entrée INTACTES (aucune écriture à rdx) ;
         Q4 rax = 0.
  inv  : I1 LES DEUX APPELS DIRECTS DÉCLARÉS (la liste fermée) : call
             shani-02 @0xD080 (la variante — le chemin matériel) et call
             tls13-02 @0xC080 (LE SCELLÉ, à son adresse d'origine R7 — le
             repli) ; la sonde shani-01 @0xD000 appelée UNE FOIS à
             l'entrée (jamais dans la boucle) ; le verdict lu du
             processeur, tenu en r15 SAUVÉ (non volatil), la branche du
             dispatch PRÉVISIBLE (le même chemin pour toute la durée de
             l'appel) ;
         I2 AUCUNE entrée IAT, AUCUN site syscall (charte § 7) ;
         I3 aucun état détenu hors du contexte pointé ; les transitoires
             vivent sur la pile et les registres SAUVÉS (charte § 6) ;
         I4 le temps constant PAR CONSTRUCTION SUR LE CONTENU (miroir de
             tls13-03 I4) : la longueur N est PUBLIQUE — le nombre de
             compressions en dépend, le contenu JAMAIS ; le verdict du
             dispatch dépend du PROCESSEUR, pas des données ;
         I5 aucun registre non volatil détruit (rbx, rbp, rdi, rsi,
             r12-r15 sauvés/restaurés — le miroir de tls13-03) ; la
             croissance du slot est NOP, 0x90.
Échecs :
  E1 : aucun échec NOMMÉ propre au bloc — le miroir de tls13-03 (les
       refus d'arguments vivent à loupe-05, l'appelant du domaine
       déployé) ; l'absence d'instructions SHA sur le processeur N'EST
       PAS un échec : c'est le repli scalaire, le scellé — le chemin
       ordinaire.
Vecteurs :
  V1 : le doré au pipeline complet — la composition tls13-01 (scellé) →
       shani-03 (variante) → tls13-04 (scellé) sur les QUATRE vecteurs
       FIPS 180-4 § 6.3.1, aux DEUX chemins (dispatch réel sur machine
       SHA-NI, dispatch FORCÉ scalaire par sonde neutralisée en copie de
       laboratoire) : chaque condensé == hashlib — les opérations
       COMPLÈTES init+absorb+final, jamais un périmètre partiel ;
  V2 : l'égalité scalaire/SHA-NI sur corpus aléatoire (l'exigence de
       l'instruction) — 1 000 tampons aléatoires aux longueurs aux
       bords (0, 1, 55, 56, 63, 64, 65, …, 4 096) : le condensé de la
       composition scellée (tls13-03) == le condensé de la variante
       (shani-03) aux DEUX chemins == hashlib ;
  V3 : l'invariance de découpage aux TROIS découpages (1, 3, 63/64/65)
       sur le chemin SHA-NI — le miroir de la preuve du harnais M9 ;
  V4 : la falsification — un octet muté entre deux appels : le condensé
       diverge (le dispatch ne change PAS la sémantique, seulement le
       chemin).
Fixtures    : celles de shani-02 (le masque, la table K du scellé —
              citées par son intermédiaire, jamais re-déclarées ici).
Provenance  : écrite-avant-code ; la structure d'absorption est le MIROIR
              DE tls13-03 (le brouillon scellé relu avant l'écriture —
              le chemin PLEIN sur l'ÉGALITÉ STRICTE, journal 20 de la
              lignée : jbe laissait remplissage=64 sans compression) ;
              la différence UNIQUE : la sonde à l'entrée + les deux
              sites d'appel.
Décisions   : D205, R4 (le contrat de tls13-03 à la lettre), R7 (le
              repli à l'adresse scellée 0xC080), R11 (la sonde UNE FOIS
              par appel — le sondage par bloc interdit : le hot path est
              la compression), D161 (l'ARRÊT du slot sur la longueur
              réelle).
