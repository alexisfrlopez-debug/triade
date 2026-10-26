ah-08 · encodage hexadécimal · révision 1
Intention : encoder 32 octets binaires en 64 caractères hexadécimaux
minuscules — le pont entre le digest machine et l'humain : sans lui, la
sortie de hachoir serait illisible ; avec lui, elle est diffable contre
sha256sum caractère par caractère. L'encodage est autoporteur : la table
de 16 caractères vit en .rodata, adressée une fois par déplacement RIP.
Contrat :
  pre  : P1 rdi pointe vers la source (32 octets lisibles) ;
         P2 rsi pointe vers la destination (64 octets inscriptibles) ;
         P3 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 pour chaque octet i : destination[2i] = hexdigit(source[i]
             >> 4) et destination[2i+1] = hexdigit(source[i] & 0xF),
             hexdigit = « 0123456789abcdef » (minuscules — même alphabet
             que sha256sum) ;
         Q2 les octets de destination au-delà de 64 ne sont jamais
             touchés ;
         Q3 rax = rsi (la destination se rend en retour).
  inv  : I1 lectures : la source (32 o) et la table hexdigit @ 0x2100
             (16 o, .rodata — donnée pure) exclusivement ; écriture :
             destination (64 o) exclusivement — la source n'est jamais
             modifiée (l'encodage sur place source == destination est
            hors contrat, hachoir ne le fait jamais : digests et ligne
             vivent à des adresses distinctes) ;
         I2 feuille : 0 octet de pile, aucun non-volatil, aucun
             stockage sous rsp ; r8 (volatile) sert de base de table ;
         I3 la zone rouge n'est jamais touchée.
Échecs :
  E1 : aucun — l'encodage ne peut pas échouer (P1/P2 garantissent la
       mémoire, la boucle est bornée par contrat à 32 itérations).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, via artefact entier) : la
       ligne de sortie de hachoir commence exactement par l'hexadécimal
       minuscule du digest de référence sur chaque vecteur doré FIPS
       (couvre Q1 — les 64 caractères sont comparés au sha256sum du
       terrain, diff caractère par caractère).
Fixtures    : la table hexdigit @ 0x2100 (16 o — donnée pure du profil).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Minuscules par contrat : la compatibilité diff avec
              sha256sum est un critère de sortie de l'artefact (D34) —
              l'alphabet est spécifié, pas laissé à la table.
