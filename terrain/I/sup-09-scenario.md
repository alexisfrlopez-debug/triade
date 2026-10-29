sup-09 · scénario (orchestrateur des tests) · révision 4
Intention : le fil ouvrier du superviseur — lancé par UN clic (win-04
scellé, tcp-06 scellé), il enchaîne porte R10, libc, EXTRACTION du kit
embarqué (sup-37, D49), T1 (démo M2), T2 (proxy M3), T4 (tunnel TLS
M4, terrain.17), T3 (envoi Drive), NETTOYAGE du kit, et rend le verdict
final : « SUPERVISEUR : TOUT OK » ou « SUPERVISEUR : ECHEC ». Chaque test
est indépendant : un KO n'arrête pas les suivants (le constat veut TOUT
le tableau, pas la première ligne). Le journal produit est le constat
§ 8.4 complet — prêt à partir dans le Drive par T3 (qui vient APRÈS T4 :
l'envoi embarque la voix du tunnel). Révision 2 (D49) : l'extraction
précède les tests (T1/T2 lancent des fichiers qui sortent de CE
superviseur), le nettoyage suit T3 (le journal seul reste posé), et le
verdict de T3 ne compte QUE si la variante declare l'annexe (variante
publique du dépôt : T3 non applicable, pas échoué — la variante de
livraison, elle, reste intégralement comptée, sémantique terrain.1
préservée). Révision 3 (D96, terrain.17) : T4 (sup-38) s'insère entre
T2 et T3 — le port 25000 est partagé par T2 ET T4 (l'ordre est un
invariant : le proxy de T2 est MORT avant celui de T4), et T3 reste le
dernier (le journal téléversé contient les lignes du tunnel). Révision 4
(D101, terrain.18) : le PRÉVOL (sup-39) s'insère entre le verdict libc et
l'extraction — les ÉTAPES 0/0 BIS du protocole (taskkill des orphelins,
sonde curl de l'amont) deviennent automatiques : un proxy.exe orphelin
verrouillerait le fichier à re-poser et tiendrait le port 25000, et le
réseau amont est désormais un FAIT journalisé (S08/S09) avant tout test.
Contrat :
  pre  : P1 lancé une fois par win-04 (drapeau DRAPEAU_WORKER) ; P2
         TAMPON_NOM/TAMPON_AFF posés (sup-01) ; P3 journal opérationnel ;
         P4 pile alignée.
  post : Q1 en-tête : S00 (bannière terrain.2), S01 (date, TAMPON_AFF
         mode 0, longueur = retour de sup-21 conservée) ; Q2 autotest
         win-06 scellé : -1 -> S02 KO + S91 + rax = 0 (arrêt immédiat —
         la porte invalide TOUT le reste, fail-closed R10 ; elle couvre
         AUSSI la zone .blob depuis D49) ; 4 -> S02 VERTE + S03 4/4 ;
         autre -> S03 KO + arrêt ; Q2' NOUVEAU (R4) : prévol (sup-39)
         — taskkill orphelins + sonde amont, lignes S08/S09 journalisées
         par sup-39 lui-même, rax ignoré (une évidence, jamais un bit) ;
         Q3 extraction (sup-37 .extraire) ->
         drapeaux bit 0 demo / bit 1 proxy / bit 2 T3 applicable, lignes
         S04*/S05*/S06* journalisées par sup-37 lui-même ; Q4 T1 (sup-33)
         si bit 0, sinon SAUTÉ (S04B/S04D déjà dit pourquoi) ; Q5 T2
         (sup-34) si bit 1, sinon SAUTÉ ; Q5' NOUVEAU (R3) : T4 (sup-38)
         si bit 1 (LE MÊME bit — le tunnel M4 vit dans le MÊME proxy.exe
         0.5.0-dev.2 que T2 teste : un seul artefact, deux facettes),
         sinon SAUTÉ ; Q6 T3 (sup-35) si bit 2, sinon SAUTÉ (S06B a dit
         pourquoi — variante publique) ; Q7 nettoyage
         (sup-37 .nettoyage) TOUJOURS appelé après T3 — sur les chemins
         de succès COMME d'échec, tant que l'extraction a été tentée ;
         ligne S07 ; Q8 verdict final : les verdicts COMPTÉS tous == 1 ->
         S90 « SUPERVISEUR : TOUT OK », rax = 1 ; sinon S91 « SUPERVISEUR :
         ECHEC (voir lignes KO) », rax = 0 ; un test sauté pour extraction
         impossible (bits 0/1 = 0) COMPTE COMME ÉCHEC (jamais de TOUT OK
         sur un test non prouvé) ; un T3 non applicable (bit 2 = 0,
         variante publique) n'est PAS compté du tout ; Q9 le fil se
         termine TOUJOURS (retour) — la fenêtre reste ouverte, le journal
         est complet, l'envoi a déjà été tenté, le kit est retiré.
  inv  : I1 ordre strict porte -> libc -> prévol -> extraction -> T1 ->
         T2 -> T4 -> T3 -> nettoyage -> verdict (le prévol AVANT
         l'extraction : un orphelin tué après re-pose verrouillerait le
         fichier ; l'envoi se fait APRÈS que le journal
         contient tout le reste — les lignes du tunnel comprises ; le
         nettoyage se fait APRÈS T3 — l'annexe posée doit vivre le temps
         de l'envoi) ; I2 aucune dépendance entre tests (T2 et T4
         lancent CHACUN leur proxy : le port 25000 partagé impose la
         séquence — verrou d'ordre dans l'oracle : le proxy de T4 ne
         naît qu'après la MORT de celui de T2) ; I3 le verdict final
         agrège les retours comptés — jamais une impression ; I4 la
         porte R10 précède tout test (héritage win-09, R10) ; I5 le
         nettoyage n'efface JAMAIS le journal du run (c'est le constat —
         seul le kit est retiré).
Échecs :
  E1 : porte KO (image corrompue, zone .blob comprise) -> S02 KO + S91,
       rax = 0, AUCUN test lancé, AUCUN fichier posé — exactement le
       comportement démo éprouvé.
  E2 : tout test KO -> sa ligne KO, les suivants quand même, nettoyage
       quand même, S91 final.
  E3 : extraction impossible pour un artefact -> test correspondant sauté
       et COMPTÉ ÉCHEC au verdict (pas de TOUT OK usurpé).
Vecteurs :
  V1 : round-trip 100 %.
  V2 : émulation nominale COMPLÈTE livraison (extraction 3 fichiers
       conformes, T1/T2/T4/T3 verts, nettoyage) — journal ÉCRAN + FICHIER
       comparés exactement à la séquence d'or (l'ordre des appels
       observé : porte, extraction, T1, T2, T4, T3, nettoyage, verdict),
       rax = 1.
  V3 : émulation nominale publique (slot annexe vide) -> S06B, T3 SAUTÉ
       non compté, T1/T2/T4 verts + extraction conforme -> S90, rax = 1
       (la variante du dépôt prouve T1/T2/T4, pas l'envoi).
  V4 : T2 KO seul -> S91 final, rax = 0, T3 quand même, nettoyage quand
       même.
  V5 : extraction demo.exe en échec (bit 0 = 0) -> T1 sauté, compté
       échec -> S91 même si T2/T3 verts.
  V6 : porte KO (octet de la zone .blob corrompu — falsification) ->
       arrêt immédiat après S02, aucun spawn, aucun fichier posé.
  V7 : falsification — réordonner T3 avant T2 fait échouer le verrou
       d'ordre ; appeler le nettoyage avant T3 fait échouer le verrou
       (l'annexe serait retirée avant l'envoi).
Fixtures    : lignes S00..S03, S90, S91 (.rdata zone données sup), lignes
              S04..S07 (sup-37, zone données sup 3).
Provenance  : écrite-avant-code ; révision 2 née de D49 (kit embarqué —
              l'exigence développeur « 1 seul exe qui contient tout ») ;
              révision 3 née de D96 (terrain.17 — T4 : le critère M4
              exige son run terrain) ; révision 4 née de D101 (terrain.18 —
              le prévol : les ÉTAPES 0/0 BIS du protocole deviennent
              automatiques, l'exigence développeur du 29/10).
Décisions   : D48 (v1), D49 (R2), D96 (R3), D101 (R4) ; squelette win-09:R4 (porte -> libc ->
              séquence) ; l'indépendance des tests est le cœur du
              superviseur (un constat partiel vaut mieux qu'un arrêt au
              premier échec) ; la règle du T3 non compté en variante
              publique est la seule entorse à « tout compte » — sans
              elle, le binaire du dépôt finirait TOUJOURS ÉCHEC (il n'a
              pas d'annexe par construction), ce qui tuerait sa
              lisibilité de preuve.
