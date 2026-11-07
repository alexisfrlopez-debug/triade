loupe-13 · recherche : l'algorithme pur, la fenêtre et le motif · révision 1
Intention : L'ALGORITHME PUR — la première occurrence d'une suite
d'octets (le motif, 1 à 32 o) dans un tampon, à partir d'un départ
donné — PROUVÉ AU LABO AVANT TOUT EMBARQUEMENT (la feuille pure du
domaine : les arguments seuls, aucune IAT, aucun état). La comparaison
par libc-02 (memcmp) HÉRITÉ PAR LA CARTE : chaque candidat testé par le
bloc scellé M1, le premier match gagne. Loupe-14 l'appelle fenêtre par
fenêtre sur le fichier — la pureté ici est la condition de la preuve
là-bas.
Contrat :
  pre  : P1 rcx = la fenêtre, au moins rdx octets lisibles ; P2 rdx =
             la taille de fenêtre (≥ 0) ; P3 r8 = le motif, au moins
             r9 octets lisibles ; P4 r9 = la taille du motif, 1 à
             32 (MOTIF_MAX) ; P5 le départ à l'adresse [rsp+0x28],
             0 à rdx inclus.
  post : Q1 rax = la position DE LA PREMIÈRE occurrence du motif dans
             fenêtre[départ .. rdx) — position ABSOLUE dans la
             fenêtre (départ compté), la première, jamais la
             seconde ;
         Q2 l'absence → rax = -1 : LA FIN NOMMÉE de la table (le
             verdict -1 — la plage est épuisée) ; le motif plus
             long que la plage restante → -1 IMMÉDIAT (le constat
             trivial, jamais une boucle : la fenêtre ne peut pas le
             contenir) ;
         Q3 le départ = rdx (la plage vide) → -1 (le miroir de Q2) ;
         Q4 rax ≥ 0 → fenêtre[rax .. rax + r9) == le motif octet par
             octet (l'occurrence est VRAIE — memcmp l'a juré) et
             AUCUNE occurrence n'existe dans fenêtre[départ .. rax)
             (la première, la vraie première).
  inv  : I1 AUCUNE entrée IAT, AUCUN site syscall, AUCUN état détenu
             (les arguments seuls — le miroir exact des feuilles
             pures tls13, charte § 9) ;
         I2 LA COMPARAISON PAR LA CARTE : chaque candidat testé par
             libc-02 (le bloc scellé M1, byte-identique) — JAMAIS
             une boucle de comparaison réécrite (R7) ; la liste
             d'appels est FERMÉE (libc-02 seul) ;
         I3 la fenêtre et le motif LUS SEULS (jamais modifiés — la
             pureté) ; la complexité est HONNÊTE (la recherche directe
             O(n·m), m ≤ 32 : la borne du quotidien la rend tenable —
             aucune table, aucune allocation, l'algorithme tient dans
             la tête) ;
         I4 aucun registre non volatil détruit ; NOP, 0x90.
Échecs :
  E1 : le motif vide (P4 = 0) → verdict -5 ENTRÉE — chercher rien
       n'est pas chercher.
  E2 : le motif > 32 (P4) → verdict -5 ENTRÉE — la borne du quotidien
       (MOTIF_MAX), la barre la nomme chez loupe-14.
  E3 : le départ hors fenêtre (P5 > rdx) → verdict -5 ENTRÉE — le
       départ est une position, pas un vœu.
Vecteurs :
  V1 : différentiel — 10 000 cas aléatoires (fenêtres 0 à 4 096 o,
       motifs 1 à 32, départs aléatoires, alphabet plein 0x00-0xFF
       ET alphabet pauvre pour forcer les occurrences multiples) :
       rax == bytes.find du modèle Python À L'IDENTIQUE, y compris
       les -1 (couvre Q1, Q2, Q3, Q4).
  V2 : doré — le motif au premier octet, au dernier, à cheval sur le
       départ, l'occurrence double (la PREMIÈRE exigée), le motif
       répétitif « AAAA » dans « AAAAB » (les cas de l'école, tenus
       pour toujours) (couvre Q1, Q4).
  V3 : rejet — motif vide, motif de 33 o, départ au-delà : les TROIS
       verdicts -5 (couvre E1, E2, E3).
  V4 : falsification — une position rendue mutée d'un (le second
       match au lieu du premier) : la différentielle échoue — la
       falsification DEMANDÉE (la pureté du bloc est la preuve du
       fichier chez loupe-14).
Fixtures    : les cas de l'école (le corpus V2, consigné au harnais)
              + les fenêtres de proxy.exe scellé (les motifs « MZ »,
              « PEMax », « This program » — les marques de la pièce
              de l'ère).
Provenance  : écrite-avant-code.
Décisions   : D171, D161, D7 (l'héritage libc-02 PAR LA CARTE).
