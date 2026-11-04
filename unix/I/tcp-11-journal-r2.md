tcp-11 · ligne de journal console · révision 2
Intention : écrire UNE ligne de journal complète sur le flux de sortie —
préfixe, champ numérique décimal optionnel, suffixe — sous verrou
d'exclusion : la ligne est composée dans le cadre privé du thread appelant
puis émise par une seule écriture ; deux threads qui journalisent
simultanément produisent deux lignes entières, jamais un entrelacement.
Contrat :
  pre  : P1 préfixe (argument 1) : l'adresse du préfixe (argument 2 = sa
             longueur, éventuellement 0) ;
         P2 valeur (argument 3, 32 bits significatifs) : la valeur du champ
             numérique, ou le sentinelle 0xFFFFFFFF signifiant « pas de champ
             numérique » (la valeur 0xFFFFFFFF elle-même n'est pas
             journalisable : les compteurs du serveur sont petits) ;
         P3 suffixe (argument 4) : l'adresse du suffixe (argument 5 = sa
             longueur, éventuellement 0) ;
         P4 préfixe + 12 + suffixe <= 64 octets (discipline de l'appelant —
             les lignes du serveur sont courtes) ;
         P5 le verrou d'exclusion du profil est en état initialisé et le
             service d'écriture est joignable (frag-con : Windows — la
             section critique .data est initialisée et le handle stdout est
             caché en .data par tcp-12 ; Linux — le qword verrou du plan de
             l'image naît déverrouillé au chargement, AUCUNE initialisation
             requise, et le flux de sortie est l'entier 1 passé par
             l'appelant) ;
         P6 la pile est alignée à l'entrée du bloc (rsp ≡ 8 mod 16 —
             discipline partagée, frag-con, § 8.3-4).
  post : Q1 une seule écriture est effectuée, du tampon composé, pour la
             longueur totale préfixe + décimale (si champ) + suffixe — les
             octets sont exactement la composition attendue, la décimale
             étant produite par libc-04 (auto-hébergement) ;
         Q2 la valeur de retour contient le verdict BRUT du service
             d'écriture, sans transformation (frag-con : Windows — BOOL de
             WriteFile ; Linux — rax du noyau) ;
         Q3 le verrou est pris AVANT la première écriture du tampon et rendu
             APRÈS l'écriture, sur tout chemin — l'échec d'écriture ne laisse
             jamais le verrou pris.
  inv  : I1 appels : le verrou d'exclusion du profil (frag-con : Windows —
             EnterCriticalSection/LeaveCriticalSection par IAT ; Linux — le
             verrou tournant du plan de l'image, atomique lock xchg sur le
             qword .bss, attente passive pause, jamais de service système)
             et le service d'écriture du profil ; appels directs : libc-01
             (copie du préfixe puis du suffixe), libc-04 (décimale), libc-03
             (longueur du champ), écrire (l'émission) ;
         I2 le tampon (64 octets) vit dans le cadre du bloc — pile privée :
             AUCUNE allocation d'arène (discipline M2, voir libc-09) ;
         I3 le prologue réserve le cadre exigé par la convention du profil
             (frag-con) et sauvegarde les non volatils de travail ;
             l'épilogue restaure symétriquement ;
         I4 le cinquième argument (longueur du suffixe) est reçu selon la
             convention du profil (frag-con : Windows — loge d'argument pile
             au-delà des quatre registres ; Linux — registre, l'ABI porte
             cinq arguments sans pile) et consommé avant tout appel ;
         I5 aucune écriture hors du cadre du bloc ; les seules lectures
             d'état sont le verrou et le flux au plan de l'image.
Échecs :
  E1 : le service d'écriture rend un verdict d'échec → la valeur de retour
       porte le verdict brut (Q2), le verrou est rendu (Q3) : la ligne est
       perdue, le serveur continue (le journal n'est pas un chemin critique —
       propagation documentée, même discipline que hello-01).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle) : 4 000 lignes aléatoires (préfixes/
       suffixes 0-20 octets, valeurs 0-4 milliards, sentinelle) — octets
       exacts, longueur exacte, verdict brut propagé, verrou pris puis rendu
       un-pour-un sur tous les chemins (couvre Q1-Q3, I1, I4).
  V3 : concurrence sérialisée : deux suites de journal simultanées (deux
       threads réels au labo Linux, verrous alternés en émulation côté
       Windows) — aucune ligne fragmentée (couvre Q1, Q3).
  V4 : test de rejet : toute notation composant hors du cadre, appelant un
       service hors I1, ou quittant le verrou pris, est refusée (couvre I1,
       I2, I5).
Fixtures    : néant (les chaînes viennent de l'appelant ; fixtures au plan
              de l'image des autres blocs).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D20, D33, D149 (révision de granularité), D150 (l'état
              qui traverse vit en mémoire — le verrou est un qword du plan,
              jamais un registre).
Historique  : R1 (m2/I, instance Windows scellée 0.3.0 dans echo.exe) révisée
              en R2 au chantier M6-(b) : la révision de granularité
              (D149-(3)) — les cinq arguments quittent rcx/rdx/r8/r9 + pile
              pour leurs NOMS (préfixe/longueur/valeur/suffixe/longueur),
              la section critique devient « le verrou d'exclusion du profil »
              (l'instance Linux : le qword tournant lock xchg, né déverrouillé
              — l'initialisation de tcp-12 devient une paramétrisation
              Windows), WriteFile devient le service d'écriture ; les
              OBSERVABLES — une seule écriture de la composition exacte
              (Q1), le verdict brut propagé (Q2), le verrou pris puis rendu
              sur tout chemin (Q3) — sont INVARIANTS.
