ah-06 · absorption tamponnée · révision 1
Intention : absorber n octets dans le contexte, par morceaux quelconques,
en ne comprimant que des blocs complets — le bloc qui rend le hachage
insensible au découpage : un million d'octets en un appel ou un à la
fois, même digest. C'est la propriété qui fait de hachoir un outil
général et pas une démonstration : l'invariance de découpage est le
contrat central (Q4).
Contrat :
  pre  : P1 rdi pointe vers le contexte (initialisé ah-04) ;
         P2 rsi pointe vers la source (n octets lisibles ; si n = 0 le
             pointeur peut être quelconque) ;
         P3 rdx contient n (u64) ;
         P4 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 succès : les n octets de la source sont absorbés — le
             contenu combiné (ancien tampon valide + source) est
             traité comme flux continu : exactement floor((remplissage
             + n) / 64) compressions ah-05 ont été exécutées ;
         Q2 remplissage' = (remplissage + n) mod 64, les octets
             résiduels sont en tête du tampon ;
         Q3 total' = total + n (compteur d'octets cumulés) ;
         Q4 invariance de découpage : pour toute partition de la
             source en appels successifs, l'état final (H, remplissage,
             total) est identique à l'absorption en un seul appel ;
         Q5 rax = total' (le compteur se rend en retour — chaînage).
  inv  : I1 appel direct : ah-05 @ 0x1200 exclusivement (uniquement
             avec remplissage == 64, contrat de coopération P2 ah-05) ;
         I2 appels système : AUCUN ; lecture : [rsi, rsi+n) et le
             contexte ; écriture : le contexte (tampon, remplissage,
             total, H via ah-05) exclusivement — la source n'est jamais
             modifiée ;
         I3 cadre : 5 non-volatils poussés (rbx, r12, r13, r14, r15),
             pile alignée aux points d'appel ((8 + 40) ≡ 0 mod 16) ;
             la copie utilise rep movsb (rdi/rsi/rcx volatils — ils ne
             traversent pas le call) ;
         I4 la zone rouge n'est jamais touchée.
Échecs :
  E1 : aucun — l'absorption ne peut pas échouer (P2 garantit la
       lisibilité ; n = 0 est un no-op conforme : Q1..Q3 triviaux, Q4
       par identité).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, granularité bloc, en émulation
       contrôlée OU via artefact entier) : pour chaque témoin, les
       découpages {1 octet, 7, 63, 64, 65, 100, tout} produisent le
       même digest final que la référence FIPS dérivée de I (couvre
       Q1-Q4 — 4 096 séquences aléatoires contraintes par exécution).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. L'invariance de découpage (Q4) est l'exigence qui a
              dicté la conception : le tampon de 64 o appartient au
              CONTEXTE, pas à la pile de absorber — sinon deux appels
              successifs perdraient les résiduels. Même décision que
              les implémentations EVP : l'état vit avec le calcul.
