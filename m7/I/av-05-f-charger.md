av-05 · désérialisation 32 octets vers membres f25519 · révision 1
Intention : charger un scalaire sérialisé little-endian de 32 octets (clé
publique A, composante R' de signature) dans la représentation « membres »
du corps (radix 2^51, 5 u64) : cinq chargements non alignés (l'architecture
x86-64 les permet nativement), décalages et masques — la transposition du
« fexpand » classique, écrite à la main.
Contrat :
  pre  : P1 rdi pointe vers 32 octets lisibles (source, SÉRIALISÉE
             little-endian) ; P2 rsi pointe vers 40 octets inscriptibles
             (membres destination) ; P3 pile alignée.
  post : Q1 les cinq membres contiennent exactement les bits [51i,
             51(i+1)) de la valeur des 255 bits de poids faible de la
             source (membre i = (x >> 51i) & (2^51 − 1)) ;
         Q2 le bit 255 de la source (octet 31, bit 7 — le drapeau de
             signe Ed25519) est IGNORÉ : il appartient à l'appelant
             (av-14 le lit séparément, avant ou après l'appel) ;
         Q3 rax = rsi (chaînage libre).
  inv  : I1 la source est lue par exactement cinq chargements qword aux
             décalages 0, 6, 12, 19, 24 — le dernier couvre les octets
             24..31 : AUCUNE lecture au-delà du 32e octet (garantie
             frontière) ;
         I2 feuille : aucun appel, aucun syscall, 0 octet de pile, aucun
             non-volatil ;
         I3 masques et décalages en immédiats (0x7ffffffffffff, 3, 6, 1,
             12) — aucune donnée RIP.
Échecs :
  E1 : aucun (cinq chargements et cinq écritures).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, appel direct sous harnais) :
       32 octets aléatoires → les membres reconstitués (Σ m[i]·2^51i)
       égaux aux 255 bits bas de la source — mille vecteurs, plus les
       cas zéro, tous-uns, p−1, p, 2^255−1.
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Les décalages 0/6/12/19/24 viennent de la décomposition
              51·k : 51 = 6·8+3, 102 = 12·8+6, 153 = 19·8+1, 204 = 25·8+4
              (chargé à 24, décalé de 12 : 24·8+12 = 204) — l'arithmétique
              de l'auteur est dans LA SPEC, vérifiable, et les symboles de
              la notation seront confrontés aux longueurs réelles (leçon
              C1 : jamais crue, toujours mesurée).
