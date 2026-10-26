win-06 · autotest (porte R10 + vecteurs libc) · révision 1
Intention : le gardien au démarrage de la démonstration — ré-exécuter la porte
R10 (sommes de blocs + version, algorithme fidèle de tcp-12) puis quatre
vecteurs dorés contre les blocs libc scellés M1 embarqués (memcpy, memcmp,
strlen, itoa) ; le verdict distingue la porte (fatal) des vecteurs (comptés).
Contrat :
  pre  : P1 l'image est chargée, .data vierge, table R10 (.rdata 0x2450,
         entrée 0 = staging — lue par tcp-07) et version (0x2600) cohérentes
         avec l'image ; P2 pile alignée (rsp ≡ 8 mod 16) ; P3 les blocs
         b20001-b20004 et les fixtures .rdata sont présents à leurs adresses
         de plan.
  post : Q1 porte KO (une somme diverge OU version < plancher 0x00030000) :
         eax = -1 (0xFFFFFFFF), AUCUN vecteur libc exécuté, aucun autre
         effet — le scénario affichera l'arrêt ; Q2 porte OK : eax = nombre
         de vecteurs verts (0..4) : memcpy 16 o ("TRIADE-M2-DEMO!!" copié
         puis comparé), memcmp triple ("aaa"/"abc" 3 o = 0, "aaa"/"aab" 3 o
         = -1), strlen 13 ("porte-libc-ok"), itoa 25000 ("25000") ;
         Q3 tampons dans le cadre de pile, aucun octet .data écrit.
  inv  : I1 la porte précède TOUT appel (miroir tcp-12 : fail-closed au
         chargement) ; I2 lecture seule de .rdata (table, version, fixtures) ;
         I3 appels directs limités à b20001-b20004 ; I4 la somme parcourt la
         région en qwords, taille multiple de 8 (convention table D33).
Échecs :
  E1 : somme d'une entrée divergente — détection immédiate, eax = -1 (la
       corruption d'UN octet d'UN bloc suffit — l'oracle le prouve par
       falsification de chaque bloc embarqué).
  E2 : version sous le plancher (anti-rollback R10) — eax = -1.
  E3 : vecteur libc en échec (bloc corrompu alors que la table serait
       restée cohérente — incohérence construite par l'oracle) — eax < 4,
       le scénario affiche la défaillance sans arrêter la machine.
Vecteurs :
  V1 : round-trip de notation 100 %.
  V2 : émulation : image saine → eax = 4 ; version < plancher → eax = -1 ;
       chaque octet de chaque entrée de table corrompu → eax = -1
       (falsification exhaustive, zéro silence attendu).
Fixtures    : .rdata — "TRIADE-M2-DEMO!!" (16 o), "aaa\0abc\0aab\0",
              "porte-libc-ok\0", "25000\0" (zone fixtures 0x2620).
Provenance  : écrite-avant-code.
Décisions   : D5 (verrou croisé), D29, D33 (table), R10 (fail-closed), D35.
