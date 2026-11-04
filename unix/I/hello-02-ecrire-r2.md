hello-02 · écrire (bloc d'écriture du flux de sortie) · révision 2
Intention : écrire un tampon mémoire sur le flux de sortie du profil en un
seul appel au service d'écriture, en honorant intégralement la convention
d'appel du profil pour les arguments au-delà des registres (aucun chez
l'instance SysV, quatre registres puis la pile chez l'instance Windows).
Contrat :
  pre  : P1 flux (argument 1) : le descripteur du flux de sortie du profil
             (frag-con : Windows — HANDLE retourné par GetStdHandle, passé
             par l'appelant ; Linux — fd entier, la sortie standard est 1) ;
         P2 tampon (argument 2) : l'adresse du tampon à écrire ;
         P3 longueur (argument 3, 32 bits significatifs) : le nombre d'octets
             du tampon (longueur > 0) ;
         P4 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 la valeur de retour contient le verdict BRUT du service
             d'écriture, sans masquage (frag-con : Windows — BOOL de
             WriteFile ; Linux — rax du noyau : nombre d'octets écrits ou
             -errno) ;
         Q2 la pile est restaurée à l'identique (frame équilibré, ret) ;
         Q3 les arguments supplémentaires du service, quand le profil en
             exige, sont neutres (Windows : le 4e et le 5e argument de
             WriteFile sont NULL — pas d'octets écrits rapportés, pas
             d'opération avec chevauchement ; Linux : write n'en a pas).
  inv  : I1 la zone d'accueil du profil est honorée avant l'appel au service
             (frag-con : Windows — shadow space de 32 octets alloué ; Linux —
             aucune, l'ABI n'en exige pas) ;
         I2 aucun registre non volatil du profil n'est modifié (frag-con) ;
         I3 la longueur passée au service est exactement celle reçue (P3) ;
         I4 l'appel au service est UNIQUE (une écriture, un verdict).
Échecs :
  E1 : le service rend un verdict d'échec → propagation du verdict brut à
       l'appelant (Q1), aucune transformation, aucun re-essai (repli :
       silence documentée chez l'appelant — même discipline que hello-01).
Vecteurs :
  V1 : round-trip de notation 100 % (couvre P1-P4, Q1-Q3, I1-I4).
  V2 : propriété structurelle (oracle) : l'appel au service est unique et
       dérivé du flux reçu, les arguments neutres du profil sont posés avant
       l'appel, `add rsp` symétrique au `sub rsp` le cas échéant, `ret`
       terminal (couvre Q2, Q3, I1, I4).
  V3 : test de rejet : toute notation sans la zone d'accueil exigée par le
       profil, avec écriture sous RSP, ou avec un chemin d'émission dédoublé
       est refusée par l'oracle (couvre I1, I4).
  V4 : exécution réelle sur le profil — le message complet s'affiche (couvre
       Q1, I3 ; validation terrain M0 côté Windows, exécution native au labo
       côté Linux — parité par exécution § 8.3).
Fixtures    : néant (le tampon provient de l'appelant).
Provenance  : écrite-avant-code.
Décisions   : D7 (l'interface du profil), D8 (granularité/padding), D26 (M0),
              D149 (révision de granularité — le contrat d'interface écrire
              du corpus).
Historique  : R1 (m0/I, instance Windows scellée 0.1.0, réutilisée octet pour
              octet dans selftest.exe et echo.exe — R7) révisée en R2 au
              chantier M6-(b) : la révision de granularité (D149-(3)) — le
              service WriteFile devient « le service d'écriture du profil »,
              le HANDLE devient « le flux », le shadow space devient « la
              zone d'accueil du profil », la convention d'appel vit en
              frag-con ; l'OBSERVABLE (un appel unique, le verdict brut
              propagé, la longueur exacte) est INVARIANT — l'instance Windows
              scellée (hello-02:R1 à l'identique dans trois artefacts) demeure
              conforme, l'instance SysV naît de la même spécification (write,
              fd 1, aucune zone d'accueil).
