ah-07 · finalisation bourrage-longueur-extraction · révision 1
Intention : clore le hachage — bourrage FIPS § 5.1.1 (0x80, zéros, longueur
en bits sur 64 bits gros-boutistes), compression des un ou deux derniers
blocs, extraction du digest : H[8] réordonnés gros-boutiste vers 32 octets
de sortie. Le bloc qui transforme un état interne en valeur publique.
Contrat :
  pre  : P1 rdi pointe vers le contexte (initialisé ah-04, alimenté
             ah-06) ;
         P2 rsi pointe vers la sortie (32 octets inscriptibles) ;
         P3 pile alignée (rsp ≡ 8 mod 16).
  post : Q1 la sortie contient exactement le digest SHA-256 du flux
             absorbé : sortie[4i..4i+3] = H[i] en gros-boutiste, pour
             i de 0 à 7 ;
         Q2 le bourrage est conforme : si remplissage < 56, un bloc
             (0x80 à l'offset remplissage, zéros, longueur aux octets
             56..63) ; sinon deux blocs (remplissage jusqu'à 64,
             compression, puis bloc de zéros avec longueur en 56..63) ;
             la longueur est total × 8 (bits) en u64 gros-boutiste ;
         Q3 le contexte reste cohérent après finalisation (remplissage
             = 64, H dans l'état final — le contexte n'est PAS
             réutilisable sans réinitialisation ah-04) ;
         Q4 rax = rsi (la sortie se rend en retour).
  inv  : I1 appel direct : ah-05 @ 0x1200 exclusivement (contrat de
             coopération : uniquement avec remplissage == 64) ;
         I2 appels système : aucun ; lecture : contexte ; écriture :
             contexte (tampon, remplissage, H via ah-05) et la sortie
             [rsi, rsi+32) exclusivement — les octets de sortie au-delà
             de 32 ne sont jamais touchés ;
         I3 cadre : 2 non-volatils poussés (rbx, r12) + sous-cadre
             d'alignement de 8 octets — pile alignée aux points d'appel
             ((8 + 16 - 8) ≡ 0 mod 16) ;
         I4 la zone rouge n'est jamais touchée.
Échecs :
  E1 : aucun — la finalisation ne peut pas échouer (P1/P2 garantissent
       la mémoire ; les deux chemins de bourrage sont couverts par V2).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : les vecteurs dorés FIPS
       180-4 — vide → e3b0c442…b855 ; « abc » → ba7816bf…15ad ; « abcdbcde
       …nopq » (448 bits) → 248d6a61…06c1 ; un million de 'a' →
       cdc76e5c…2cd0 — couvrent Q1/Q2 sur les deux chemins de bourrage
       (le vecteur 448 bits exerce remplissage = 56 exactement, cas
       limite du deux-blocs).
Fixtures    : néant.
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. Le cas limite remplissage == 56 (0x80 à l'offset 56
              déborde sur la longueur) est le piège classique : couvert
              nommément par V2 (vecteur 448 bits : 56 octets + 0x80 =
              exactly 57 → chemin deux-blocs).
