av-02 · compression d'un bloc de 128 octets SHA-512 · révision 2
Intention : exécuter les 80 rondes de compression FIPS 180-4 § 4.1.3 sur un
bloc complet du tampon du contexte : extension du message W[16]→W[80] en
mots 64 bits, puis boucle de compression a..h avec les rotations DROITES
(Σ0 : 28/34/39 ; Σ1 : 14/18/41 ; σ0 : 1, 8 et décalage 7 ; σ1 : 19, 61 et
décalage 6 — les rotations de la leçon hachoir sont À DROITE, miroir exact
de ah-05:R1 en mots 64 bits) et la table K[80] u64 de .rodata. Le cœur de
SHA-512 : c'est lui que h = SHA-512(R'||A||M) exécute pour la vérification
de signatures — le bloc le plus chaud de l'échelon 2.
Contrat :
  pre  : P1 rdi pointe vers le contexte (256 o) — le tampon @ +64
             contient 128 octets valides (l'appelant garantit la
             validité ; le bloc n'examine pas remplissage) ;
         P2 pile alignée ; six non-volatils autorisés (I3).
  post : Q1 H[0..7] sont incrémentés par les huit variables de travail
             finales (a..h additionnés membre à membre, mod 2^64 — FIPS
             § 6.4.2 pas 4) ;
         Q2 le tampon et les champs remplissage/total ne sont NI lus NI
             écrits (seul H évolue — la compression est pure sur l'état) ;
         Q3 rax = rdi (chaînage libre).
  inv  : I1 lecture des données : le tampon (via rdi+64), la table K[80]
             @ R_K512 (un seul lea RIP, cible déclarée) — RIEN d'autre :
             aucune autre donnée RIP, aucun appel, aucun syscall (feuille
             de calcul) ;
         I2 les 80 mots W vivent sur la pile (640 o, sous-cadre 0x2a8) ;
             les 16 chargements initiaux passent par bswap (gros-boutiste
             FIPS, miroir ah-05) ; l'extension et la compression sont deux
             boucles bornées (r15 : 16→80 puis 0→80) dont les sauts
             internes restent aux frontières d'instruction du bloc ;
         I3 prologue : 6 pushes + sub rsp, 0x2a8 — pile 16-alignée à
             l'intérieur (aucun appel : l'alignement d'appel ne s'applique
             pas, la symétrie prologue/épilogue est vérifiée par
             l'oracle structurel) ;
         I4 aucune écriture sous rsp ; aucun stockage hors (pile locale,
             H du contexte).
Échecs :
  E1 : aucun (le bloc est un calcul pur borné : 80 rondes, retour).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle natif) : les quatre vecteurs
       dorés FIPS 180-4 (vide, « abc », 448 bits, un million de 'a')
       passent PAR CE BLOC — tout défaut de rotation, de table K ou
       d'ordre produit un digest divergent de sha512sum (couvre Q1).
  V3 : falsification : chaque octet de code du bloc corrompu diverge
       (digest faux, crash ou non-retour) — zéro silence.
Fixtures    : K[80] u64 @ R_K512 (le builder écrit la table et vérifie
              l'octet-identité à chaque run — FIPS 180-4 § 4.2.3).
Provenance  : écrite-avant-code.
Décisions   : D34.
Historique  : R1. La révision 1 de la spec vivait en chantier (couche I
              posée avant la première session de notation) ; R2 consigne
              la spec EXÉCUTÉE : ronde en mots 64 bits, W sur pile, K en
              .rodata — la transposition complète de ah-05 avec quatre
              membres de plus par ronde (80 mots au lieu de 64, u64 au
              lieu de u32, rotations distinctes).
