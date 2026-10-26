tcp-11 · ligne de journal console · révision 1
Intention : écrire UNE ligne de journal complète sur stdout — préfixe, champ
numérique décimal optionnel, suffixe — sous section critique : la ligne est
composée dans le cadre privé du thread appelant puis émise par une seule
écriture WriteFile ; deux threads qui journalisent simultanément produisent
deux lignes entières, jamais un entrelacement.
Contrat :
  pre  : P1 rcx pointe le préfixe (rdx = sa longueur, éventuellement 0) ;
         P2 r8d contient la valeur du champ numérique, ou le sentinelle
             0xFFFFFFFF signifiant « pas de champ numérique » (la valeur
             0xFFFFFFFF elle-même n'est pas journalisable : les compteurs
             du serveur sont petits) ;
         P3 r9 pointe le suffixe ([rsp+arg5] = sa longueur, éventuellement
             0) ;
         P4 préfixe + 12 + suffixe <= 64 octets (discipline de l'appelant —
             les lignes du serveur sont courtes) ;
         P5 la section critique .data (R_CS) est initialisée et le handle
             stdout est caché en .data (R_STDOUT) par tcp-12 ;
         P6 la pile est alignée à l'entrée (rsp ≡ 8 mod 16).
  post : Q1 une seule écriture WriteFile est effectuée, du tampon composé,
             pour la longueur totale préfixe + décimale (si champ) + suffixe
             — les octets sont exactement la composition attendue, la
             décimale étant produite par libc-04 (auto-hébergement) ;
         Q2 rax = BOOL brut de WriteFile (1 réussi, 0 échec) ;
         Q3 EnterCriticalSection est pris AVANT la première écriture du
             tampon et LeaveCriticalSection rendu APRÈS l'écriture, sur
             tout chemin — l'échec de WriteFile ne laisse jamais la
             section critique verrouillée.
  inv  : I1 appels système : IAT kernel32 EnterCriticalSection,
             LeaveCriticalSection ; appels directs : libc-01 (copie du
             préfixe puis du suffixe), libc-04 (décimale), libc-03
             (longueur du champ), hello-02 a10002 (écriture) ;
         I2 le tampon (64 octets) vit dans le cadre du bloc ([rsp+0x40]) —
             pile privée : AUCUNE allocation d'arène (discipline M2, voir
             libc-09) ;
         I3 le prologue alloue 0x80 octets et sauvegarde rbx, r12-r15 ;
             l'épilogue restaure symétriquement ;
         I4 le 5e argument (longueur du suffixe) est lu depuis la loge
             d'argument pile [rsp+0x50] après les cinq push — jamais au-delà ;
         I5 aucune écriture hors du cadre du bloc ; les seules lectures
             .data sont le handle stdout et l'adresse de la section
             critique.
Échecs :
  E1 : WriteFile échoue → rax = 0 (Q2), section critique rendue (Q3) :
       la ligne est perdue, le serveur continue (le journal n'est pas un
       chemin critique — propagation documentée, même discipline que
       hello-01).
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : propriété différentielle (oracle, shims) : 4 000 lignes aléatoires
       (préfixes/suffixes 0-20 octets, valeurs 0-4 milliards, sentinelle) —
       octets exacts, longueur exacte, BOOL propagé, Enter/Leave appariés
       un-pour-un sur tous les chemins (couvre Q1-Q3, I1, I4).
  V3 : concurrence sérialisée : deux suites de journal entrelacées par
       l'oracle (verrous alternés) — aucune ligne fragmentée (couvre Q1,
       Q3).
  V4 : test de rejet : toute notation composant hors du cadre, appelant un
       IAT hors I1, ou quittant sans Leave après Enter, est refusée
       (couvre I1, I2, I5).
Fixtures    : néant (les chaînes viennent de l'appelant ; fixtures .rdata
              des autres blocs).
Provenance  : écrite-avant-code.
Décisions   : D7, D8, D20, D33.
