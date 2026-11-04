libc-01 · copie mémoire · révision 2
Intention : copier exactement n octets de src vers dst en direction avant, sans
interpréter les octets ni dépendre d'aucun service extérieur — la brique de
déplacement de mémoire de la mini-libc.
Contrat :
  pre  : P1 dst (argument 1) : région d'au moins n octets accessible en
             écriture ;
         P2 src (argument 2) : région d'au moins n octets accessible en
             lecture ;
         P3 n (argument 3) : nombre d'octets à copier (u64) ;
         P4 les régions dst et src ne se chevauchent pas ;
         P5 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 — la
             discipline d'alignement, identique aux profils du corpus, vit
             en frag-con, § 8.3-4).
  post : Q1 les n octets de dst sont égaux aux n octets de src ;
         Q2 la valeur de retour (rax aux deux profils) contient dst ;
         Q3 les n octets de src sont inchangés.
  inv  : I1 le bloc est une feuille : aucun appel, aucun accès système ;
         I2 la pile est équilibrée à la sortie (rsp identique à l'entrée, ret) ;
         I3 aucun registre non volatil du profil n'est modifié (l'ensemble
             vit en frag-con : msx64 — RBX/RBP/RDI/RSI/R12-R15 ; SysV —
             RBX/RBP/R12-R15) ;
         I4 n = 0 : aucun octet n'est écrit.
Échecs :
  E1 : chevauchement dst/src (P4 violée) → comportement hors contrat, jamais
       généré par l'oracle (la sanction appartient à l'appelant, comme la libc C).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre la fidélité générale, donc P1-P5,
       Q1-Q3, I1-I4).
  V2 : propriété différentielle (oracle) : 12 000 cas à entrées aléatoires
       contraintes par P1-P5, n ∈ [0, 1024], contenus aléatoires — dst comparé
       à la référence, src recontrôlé, retour, non volatils, rsp (couvre Q1-Q3,
       I2-I4).
  V3 : vecteurs dorés embarqués (autotest) : motif 16 octets, copie de
       longueur nulle sur sentinelle, motif 33 octets (couvre Q1, I4).
  V4 : test de rejet : toute notation du bloc contenant un appel, un syscall ou
       une écriture hors de dst est refusée par l'oracle structurel (couvre I1).
Fixtures    : motifs MOTIF16/SENT16/MOTIF33 (référencés par libc-08, au plan
              d'adressage de l'image).
Provenance  : écrite-avant-code.
Décisions   : D7 (aucun appel système), D8 (granularité/padding), D26 (chaîne
              artefact), D28 (zones d'adressage), D29 (substrat d'exécution),
              D149 (révision de granularité, chantier M6-(b)).
Historique  : R1 (m1/I, instance Windows scellée 0.2.0) révisée en R2 au
              chantier M6-(b) : la révision de granularité (D149-(3)) — les
              arguments quittent les registres physiques (R1 : « rcx contient
              dst ») pour leurs NOMS (dst/src/n), la convention d'appel et
              l'ensemble non volatil vivent en frag-con (§ 8.3-4). Les
              observables Q1-Q3, E1 et les vecteurs sont INVARIANTS —
              l'instance Windows scellée demeure conforme (elle passe dst/src/n
              en rcx/rdx/r8, l'instance SysV en rdi/rsi/rdx : les deux
              satisfont la même spécification).
