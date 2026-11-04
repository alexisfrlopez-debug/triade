su-02 · formatage hexadécimal u64 · révision 1
Intention : formater une valeur 64 bits en 16 caractères hexadécimaux
minuscules, à l'identique de la graphie des outils du noyau (%016lx) — le
bloc d'affichage de la sonde : la base de chargement (ligne 1), les rax
bruts et les verdicts (lignes des sondes). Miroir assumé de ah-08:R1 (32
octets → 64 caractères), réduit à la largeur native du mot : la valeur est
un u64, la sortie fait exactement 16 octets, chiffre de poids fort en tête.
Contrat :
  pre  : P1 rdi contient la valeur à formater (u64 — la convention est la
             valeur BRUTE : un rax négatif de syscall se formate en son
             complément à deux, 0xfffffffffffffff7 pour -9) ;
         P2 rsi pointe vers 16 octets inscriptibles (le tampon .bss —
             le principal passe toujours le même) ;
         P3 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 les 16 caractères "0123456789abcdef" dérivés de la valeur sont
             écrits dans [rsi, rsi+16) ; le reste du tampon n'est pas
             touché ; rax n'est pas garanti (registre de travail).
  inv  : I1 données : lecture de la table HEXCHARS @ 0x180 exclusivement
             (16 octets, .rodata segment R) — l'accès est rip-relatif ;
         I2 feuille pure : aucun appel, aucun push, aucun registre non
             volatil touché, 0 octet de pile ;
         I3 l'arithmétique : 16 itérations, décalage 60, 56, …, 0 — le
             caractère i porte le nibble (v >> (60 - 4*i)) & 0xF.
Échecs :
  E1 : aucun (bloc arithmétique pur — pas de chemin d'échec ; un tampon
       non inscriptible est une violation de P2, hors contrat).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : oracle natif (artefact entier) : les lignes de la sonde portent les
       hex exacts — base aléatoire en ligne 1 (16 chiffres, alignée à la
       page), 0xfffffffffffffff7 et 0xfffffffffffffff2 en rax des sondes,
       0x0000000000000001 et 0x0000000000000006 en verdicts.
Fixtures    : HEXCHARS ("0123456789abcdef", 16 o — .rodata).
Provenance  : écrite-avant-code.
Décisions   : D149, D34 (modèle ah-08 de l'échelle).
Historique  : R1. Premier bloc de formatage du jalon. Le choix minuscule =
              %016lx du noyau ; le choix 16-caractères-fixes = pas de
              compression (les zéros de tête sont de l'information : ils
              distinguent 6 (verdict) de 0x6000000000000000).
