
---
Task ID: 25
Agent: Z.ai (agent principal)
Task: rapport machine réelle terrain.17-B — « la fenêtre principale se
ferme, proxy.exe reste ouvert » + journal déposé dans /test du Drive.
Diagnostic (ombre ABI x64 perdue par la régénération D96), correctif
taille-neutre, verrou neuf anti-récurrence, livraison terrain.17-C.

Work Log:
- FAITS RAPATRIÉS (drive /test) : terrain_20261029_014640.txt (journal du
  run 17-B — coupé NET après « TRIADE M3 : proxy demarre (port 25000) » :
  AUCUN S22, aucun verdict) + terrain_page_http.txt (3 961 o — la VRAIE
  page neverssl.com : le proxy M4 a relayé la requête réelle, curl a tout
  reçu) + demo_journal.txt (T1 D57 connu). A/B avec terrain16 : T2 complet
  (S22..S28 + T3) — le 17-B meurt DANS .curl, entre la bannière et S22.
- DIAGNOSTIC BINAIRE BLOC PAR BLOC (diag_bloc_16_17b.py) : sup-31
  identique ; sup-34 : 6 octets dont UNE paire sémantique — .curl
  sub/add rsp, 0x28 (terrain16) → 8 (régénération D96). MÉCANISME :
  l'ombre ABI x64 (0x20 de maisons d'arguments) absente — la maison rdx
  de WaitForSingleObject/GetExitCodeProcess [rsp+0x10] recouvre
  L'ADRESSE DE RETOUR de .curl → le callee kernel32 y déverse → ret vers
  la nature → mort du superviseur → fenêtre fermée → proxy mode 1 orphelin
  (port 25000 occupé). Même faute .ps (sup-38) : T4 serait mort au
  premier powershell. Audit complet (audit_ombre_abi.py) : 2 violations,
  aucune ailleurs (m0-m4/démo/terrain).
- POURQUOI VERT PARTOUT : shims sans déversement (l'ombre invisible à
  l'émulation) + _prologue_aligne vérifie le mod 16, pas l'ombre. Trois
  noms de la dérive de dépôt : D54, D68, D98 — terrain16 portait 0x28 en
  local, jamais committé.
- CORRECTIF (brouillons sup-34/sup-38, source unique) : sub/add rsp, 8 →
  0x28 dans .curl/.ps — imm8 → imm8 TAILLE-NEUTRE (compteurs, slots,
  padding inchangés) ; auteur.py régénère (1418 o/315, 1505 o/331 —
  identiques) ; VERROU NEUF _ombre_abi() dans build_terrain.py (fenêtre
  < 0x28 + appel IAT = ÉCHEC ; appels internes tolérés, convention
  prouvée machine terrain16) : oracle structurel 1 090 → 1 114.
- REBUILD (graine 20261029) : R5 round-trip 100 %, croisement T4 10/10,
  oracle 10 111 cas verts + 28/28 R10 + 7 mutations, carte génération 5
  re-scellée (24 + Ed25519 + R8 OK), PE 75 264 o, sha256
  c381d088c19e6941907850fcc0eed7c03bd3e39263787f44596a2394b856cb9a.
- VÉRIFICATION BINAIRE (verif_terrain17c.py) : cadres 0x28 dans .curl
  (0x5D1E) et .ps (0x7775) ; motif loader D54 INTACT (IAT 0x2300 9/9
  pré-remplies, OFT #4/#5 → 0x2B40/0x2B90, INT/hints .rdata présents) ;
  différentiel 17-B → 17-C : 8 octets (0x5D21/0x5D63/0x7778/0x77BA
  08→28 ; 4 sommes R10 0x2599/0x259B/0x25C8/0x25CA) — RIEN d'autre.
- LIVRAISON : download/superviseur-terrain17c.exe + LISEZMOI-terrain17c.txt
  (ÉTAPE 0 : taskkill /IM proxy.exe /F — l'orphelin tient le port 25000 ;
  S23 octets=N avec N≠640 légitime — le M4 relaie la VRAIE page, T2 juge
  la présence pas le contenu) ; le 17-B retiré du download
  (mono-génération) ; la sentinelle superviseur du dépôt = le rebuild
  (c381d088…).
- Docs : Entrée 84 du journal, DECISIONS D98, worklog (Task ID 25) ;
  aucune clé touchée : RIEN à remettre par cérémonie (phrase de contrôle
  D81 valable, conteneur 0323029a… inchangé, sentinelles intactes —
  proxy 0.4.0 dd12b649…, demo 73c064fb…, hello, selftest, echo).

Stage Summary:
- TERRAIN.17-C ACCOMPLI : le superviseur ne meurt plus au premier curl —
  l'ombre ABI perdue par la régénération D96 est restaurée (.curl T2 +
  .ps T4) ET verrouillée (24 verrous neufs, un par bloc) ; le proxy
  orphelin du run 17-B est expliqué (mort avant la séquence d'arrêt) et
  soldé (ÉTAPE 0 du protocole) ; la preuve machine du relais M4 réel est
  consignée (page 3 961 o)
- LEÇON SYSTÉMIQUE : alignement n'est pas ombre — l'ABI de la machine
  cible fait partie de la surface de test terrain ; la dérive de dépôt a
  trois noms (D54, D68, D98)
- Suite M4 : LE JOURNAL DU DÉVELOPPEUR (run terrain.17-C) → scellage
  0.5.0 ; puis v0.6.0 axes 2-3 (CF2-Shamir, sceau I) selon le
  positionnement D86/D87 ; terrain : D57 (WER) seul point ouvert

---
Task ID: 26
Agent: Z.ai (agent principal)
Task: journaux du drive /test — le run 17-C ANALYSÉ (critère M4 PROUVÉ,
anomalie page A nommée), diagnostic armé : terrain.17-D (sup-38:R2 —
témoin de page + ligne S47), rebuild complet, différentiel, livraison.

Work Log:
- FAITS RAPATRIÉS (drive /test) : terrain_20261029_055906.txt (1 570 o) —
  le journal du run 17-C ; demo_journal.txt déjà analysé (md5 identique,
  T1/D57). LE JOURNAL EST MAJEUR : S22-S28 T2 VERDICT OK (le superviseur
  SURVIT — D98 tient), « tunnel chiffre etabli » + « certificat rejete »
  (PREMIÈRES FOIS), « S46 octets=34 » (502 étiquetée OCTET POUR OCTET —
  LE CRITÈRE M4 « HTTPS en transit ; échec propre sur certificat
  invalide » PROUVÉ sur machine réelle), S07 nettoyage (plus d'orphelin).
  UNE ligne KO : S49 + « S44 page exemple octets=13 » (page A ~1 300 o
  attendues, tronquée à son premier enregistrement, fermeture propre).
- ÉLIMINATION (neuf bits, notation sup-38 ligne à ligne) : bits 1-8
  prouvés posés par les lignes (chaque ligne suit son memcmp gagné) ;
  tout chemin propre du relais mène à S49A — le bit manquant = contenu
  des 13 octets (bit 3) ou code de sortie du proxy (bit 9 — E6). Le
  journal ne pouvait pas départager : page supprimée au nettoyage, exit
  jamais journalisé. Analyse statique tls-07/tls-08 (4 tampons ✓,
  résidu/consumé cohérent, send partiel géré, sockets bloquantes) : la
  cause racine réelle-vs-shim (DecryptMessageW) exige les FAITS —
  discipline D54/D68/D98 : évidence avant correctif.
- SUP-38:R2 écrite-avant-code : Q5' TÉMOIN (LU octets → TAMPON_COMPO →
  temoin_m4a.txt, SURVIT au nettoyage Q11, miroir terrain_page_http.txt,
  charte § 3 entière — jamais une ligne de journal) ; Q9' LIGNE S47
  (« S47 T4 exit proxy=N » après GetExitCodeProcess, tout chemin, avant
  le verdict).
- PIÈGES NOMMÉS PAR L'ORACLE AVANT LA MACHINE : (a) l'écriture du témoin
  compose SON chemin dans TAMPON_CMD (le tampon de la page !) → .temoin
  devient SAUVER→ÉCRIRE→RESTAURER (double memcpy, transparent) ; (b) le
  motif M8 devait compter 15 (nom+NUL) et être discriminé de FIX_PS1 par
  le mov r9d,[rip+LU] qui suit (44 8b 0d vs 41 b9).
- GÉOMÉTRIE : table R10 PLEINE (28 entrées) — AUCUN bloc neuf :
  .temoin/.exitline dans sup-38 (motif .ligne/.ps), slot 0x600→0x800
  (0x7800-0x7FFF libre), l'entrée R10 T4 seule étendue. Code 1 645 o /
  357 ins / 403 padding. Version terrain.5 (u64 0x00050105).
- CHAÎNE VERTE : R5 100 % (357/357), croisement T4 10/10, structurel
  1 130 verrous, scénario 10 114 cas verts + falsification 28/28 + 9
  mutations (M8/M9 neuves), carte génération 5 re-scellée (24 +
  Ed25519 + R8 OK), PE 75 264 o TAILLE INCHANGÉE, cristallisation 3/10
  en trois runs byte-stables (sha e82924dd… inchangé).
- DIFFÉRENTIEL 17-C → 17-D (verif_terrain17d.py) : 1 652 o en 12 plages
  TOUTES NOMMÉES ; kit INTACT (demo 73c064fb…, proxy 33c91815…), motif
  loader D54 INTACT, monotonie version ✓. RIEN d'autre ne bouge.
- LIVRAISON : download/superviseur-terrain17d.exe (md5 18aa0a66…, sha256
  e82924dd…) + LISEZMOI-terrain17d.txt (ÉTAPE 0 inchangée ; déposer dans
  /test : journal + temoin_m4a.txt + pages T2 si présentes ; lecture du
  verdict quadrichotomique) ; le 17-C retiré (mono-génération) ; les exes
  16/17/17b obsolètes retirés du download ; sentinelle dépôt = e82924dd…
- Docs : Entrée 85 du journal, DECISIONS D99, worklog (Task ID 26) ;
  aucune clé touchée : RIEN à remettre par cérémonie (phrase de contrôle
  D81 valable, conteneur 0323029a… inchangé, sentinelles intactes —
  proxy 0.4.0 dd12b649…, demo 73c064fb…, hello, selftest, echo).

Stage Summary:
- TERRAIN.17-D ACCOMPLI : le critère M4 est PROUVÉ par le journal 17-C
  (tunnel + certificat + 502 exacte) ; l'anomalie page A (13 o) est
  nommée et le prochain run la fera PARLER (témoin sur le disque, S47
  dans le journal) — le diagnostic précède le correctif
- LEÇON SYSTÉMIQUE : un verdict KO sans ses faits est un échec muet —
  chaque run terrain doit rapporter ses propres preuves
- Suite M4 : LE JOURNAL + LE TÉMOIN du run 17-D → scellage 0.5.0 (si
  S47=0 et S49 OK, ou correctif ciblé sinon) ; puis v0.6.0 axes 2-3
  (CF2-Shamir, sceau I) selon le positionnement D86/D87 ; terrain : D57
  (WER) seul point ouvert

---
Task ID: 27
Agent: Z.ai (agent principal)
Task: journaux + témoin du drive /test — le run 17-D ANALYSÉ (S47=0 :
compensation PROUVÉE ; témoin = la 502 du PROXY — tcp-13 en échec,
réseau intermittent, proxy INNOCENT ; badssl 34 o exact ENCORE), la
fuite I2 du journal nommée (.evt_a_ko journalisait TAMPON/LU périmés =
la page après un timeout qui n'a rien lu) + le piège latent (LU=640 :
memcpy sauvage — le superviseur serait MORT en plein T4), correctif
taille-neutre sup-38:R3 (les deux timeouts silencieux, miroir sup-34),
verrou d'oracle (k) « proxy M4 muet », rebuild, différentiel, livraison
terrain.17-E.

Work Log:
- FAITS RAPATRIÉS (drive /test) : terrain_20261029_071458.txt (1 534 o,
  le journal 17-D) + temoin_m4a.txt (40 o — LE TÉMOIN). TROIS PREUVES :
  « S47 T4 exit proxy=0 » PREMIÈRE FOIS (la compensation intégrale tient
  sur machine réelle — E6 MORT) ; le témoin = « HTTP/1.1 502 Passerelle
  inaccessible\r\n\r\n » (40 o exacts — la 502 DU PROXY : tcp-13 n'a pas
  joint example.com, tls-08 E1 conforme : 502 propre, service continu,
  badssl OK juste après, sortie propre — LE PROXY EST INNOCENT, la panne
  était le réseau : neverssl ET example.com injoignables en amont à
  07:14, pendant que CONNECT/badssl répondaient) ; « S46 octets=34 » —
  la 502 Certificat rejete OCTET POUR OCTET, ENCORE.
- LA FUITE I2 (hexdump du journal) : les 40 o de la page A recopiés
  DANS le journal après S44 (charte § 3 violée). Mécanisme (notation
  sup-38 + sup-34 ligne à ligne, adresses par table des déplacements) :
  .evt_a_ko journalise (TAMPON, LU) ; après un timeout le sondage n'a
  rien lu — TAMPON/LU portent ENCORE la page. Reconstruction COMPLÈTE
  du journal 17-D octet par octet : S23 octets=40 VRAI (le jne 0x592d
  saute VERS le bloc de lecture — la page est lue même sur code=28) ;
  « tun » = la lecture fixe de 43 o coupe « tunnel » (le « connexion
  entrante » http non consommé par le timeout SILENT de sup-34 décale
  tout) ; S26 lignes=2 = bannière + l'unique .flux de 43 o ; le
  « connexion entrante\r » de T4 = la lecture de 54 o (35 résidus de A +
  19 de B).
- LE PIÈGE LATENT (sonde par crochet memcpy, émulation) : à LU=640 (une
  VRAIE page), la ligne de fuite compose au-delà du tampon journal
  0x3890, ÉCRASE l'état .data (LU relu comme count : memcpy au count
  0x45004500450045 — les octets de page devenus longueur) et emporte
  l'émulation (UC_ERR_WRITE_PROT, rip memcpy+0xE, 178 memcpy tracés).
  Sur machine réelle : PLANTAGE du superviseur en plein T4. Le run 17-D
  a eu de la chance (sa page ne faisait que 40 o).
- SUP-38:R3 écrite-avant-code (I/sup-38-tunnel.md révision 3) : les
  DEUX branchements de timeout deviennent SILENCIEUX (branchement
  direct je .req_b / je .arret — miroir sup-34 : rien lu, rien
  journalisé) ; la divergence memcmp seule journalise — les OCTETS LUS.
  Correctif TAILLE-NEUTRE : 74 48 → 74 56 aux rva 0x73F5/0x74EA ; code
  1 645 o / 357 ins / 403 o padding INCHANGÉS.
- VERROU D'ORACLE NEUF — cas (k) « proxy M4 muet » (famille échecs) :
  les DEUX sondages expirent ; assertions S49B + S47 exit=0 + arret
  journalisé + voix A/B absentes + « HTTP/1.1 200 OK » JAMAIS dans le
  journal ; le crash éventuel converti en EchecOracle NOMMÉ. PREUVE
  DANS LES DEUX SENS : le 17-D REJETÉ nommément, le 17-E VERT.
- CHAÎNE VERTE (graines 20261029/20261030, cristallisation 2/2
  byte-stables) : R5 100 % (357/357), croisement T4 10/10, structurel
  1 130 verrous, scénario 10 117 cas verts (+3) + falsification 28/28 +
  9 mutations, carte génération 5 re-scellée (24 + Ed25519 + R8 OK,
  artefact 0.5.0-terrain.6), PE 75 264 o TAILLE INCHANGÉE, sha256
  234b99d6590a5aeee44a9830b685fbf99e4ea6408516a2a5ed07949e1e470b80,
  md5 739cbd42bf37…, version terrain.6 (u64 0x00050106).
- DIFFÉRENTIEL 17-D → 17-E (scripts/verif_terrain17e.py) : DIX octets
  en HUIT plages TOUTES NOMMÉES (les deux 74 48→74 56 vérifiés
  explicitement ; somme R10 T4 ; u64 de version ; champs .rsrc) — kit
  INTACT (demo 73c064fb…, proxy 33c91815…), loader D54 INTACT,
  géométrie R10 T4 inchangée, monotonie ✓. RIEN d'autre ne bouge.
- LIVRAISON : download/superviseur-terrain17e.exe + LISEZMOI-
  terrain17e.txt, poussés dans /test du Drive (md5 MATCH vérifié) ; le
  17-D mis à la corbeille du Drive (mono-génération D69 ; référence
  locale scripts/superviseur-terrain17d_ref.exe — le différentiel reste
  rejouable) ; le test s'appelle TOUJOURS terrain17 (S00/L00
  inchangés) ; ÉTAPE 0 BIS NEUVE du protocole : vérifier l'amont avant
  le run (curl -s -o NUL https://example.com/). Lecture du verdict
  mise à jour : S49 OK + témoin « 200 » → scellage 0.5.0 ; S49 KO +
  S47=0 + témoin 502 Passerelle → réseau (réessayer) ; S49 KO + S47=0 +
  témoin « 200 » tronqué → correctif tls-08 (l'anomalie 13 o du 17-C,
  toujours ouverte).
- Docs : Entrée 86 du journal, DECISIONS D100, worklog (Task ID 27),
  README (état M4) ; aucune clé touchée : RIEN à remettre par cérémonie
  (phrase de contrôle D81 valable, conteneur 0323029a… inchangé,
  sentinelles intactes — proxy 0.4.0 dd12b649…, demo 73c064fb…, hello,
  selftest, echo ; le superviseur du dépôt est la balise COURANTE
  terrain.17-E 234b99d6…).

Stage Summary:
- TERRAIN.17-E ACCOMPLI : le journal du run 17-D est PROPREMENT soldé —
  les preuves (S47=0, témoin 502, badssl 34 o) sont consignées, la fuite
  I2 est nommée, corrigée (deux octets) et verrouillée (l'oracle rejette
  le 17-D nommément) ; le piège latent (memcpy sauvage à grande page)
  est désamorcé avant d'avoir tué
- LEÇON SYSTÉMIQUE : un tampon non lu n'est pas une preuve — journaliser
  un état qu'on n'a pas lu, c'est forger ; la charte § 3 protège le
  journal d'enregistrement, et une ligne de fuite à grande page était
  une bombe
- Suite M4 : LE JOURNAL + LE TÉMOIN du run 17-E (réseau stable
  souhaité) → scellage 0.5.0 si S49 OK + témoin « 200 » complet ;
  sinon correctif ciblé (tls-08 si tronqué) ; puis v0.6.0 axes 2-3
  (CF2-Shamir, sceau I) selon le positionnement D86/D87 ; terrain :
  D57 (WER) seul point ouvert

---
Task ID: 28
Agent: Z.ai (agent principal)
Task: demande développeur 29/10 (« journaux envoyés » — trois runs du jour
rapatriés : 01:46 tronqué au démarrage T2, 05:59 le run 17-C complet
[anomalie 13 o], 07:14 le 17-D déjà soldé par D100 ; question : « quand je
lance le superviseur puis TOUT DÉMARRER, une 2e fenêtre s'ouvre avec aussi
un bouton TOUT DÉMARRER, puis se referme au cours du test » ; demande :
« peux-tu intégrer la commande taskkill et la verif curl dans le
superviseur ? ») — réponse : terrain.18 / superviseur-terrain17f.exe, LE
PRÉVOL f60039 (les ÉTAPES 0/0 BIS du protocole deviennent automatiques).

Work Log:
- LA 2e FENÊTRE, EXPLIQUÉE (aucun mystère) : c'est la fenêtre de demo.exe,
  le test T1 — le superviseur est construit sur la COQUILLE DÉMO (héritage
  R7, « coquille démo éprouvée ») : deux fenêtres jumelles, deux fois le
  même bouton TOUT DÉMARRER. Elle se referme « au cours du test » parce que
  le superviseur ne retrouve PAS la fenêtre démo en 10 s (S11 ABSENTE —
  panne D57, connue et documentée) et TERMINE alors le processus démo
  (.tuer_ko de sup-33) pendant que T2/T4 continuent (~4 min). Compagnon
  nouveau du LISEZMOI 17-F : réponse en tête de document.
- LE PRÉVOL sup-39:R1, ÉCRITE-AVANT-CODE (I/sup-39-prevol.md révision 1) :
  après porte+libc, AVANT l'extraction (un proxy.exe orphelin VERROUILLE le
  fichier à re-poser et tient le port 25000 ; une démo orpheline ferait
  mentir FindWindowW), DEUX sondes MODE 0 bornées 30 s : taskkill.exe /f
  /IM proxy.exe /IM demo.exe puis curl.exe -s --max-time 20 -o NUL
  https://example.com/ (amont DIRECT, sans proxy — la panne du 17-D).
  Codes BRUTS au journal (S08/S09, mode numérique win-05 miroir S13/S22/
  S47), JAMAIS au verdict : une évidence, pas un juge (miroir du témoin
  D99). Lancement impossible = ligne sautée, jamais un crash.
- GÉOMÉTRIE (la contrainte maîtresse) : la table R10 est PLEINE depuis
  terrain.17 (28 entrées, 464 o touchant l'ancre — « tout futur bloc
  exige une autre surface ») → le prévol est ZONE-RÉSIDENT : slot
  0x4B40-0x4BFF (0xC0) dans la queue de la zone données sup 1 (FIN_SUP_1
  0x4B17 + marge 41 o), couvert par l'ENTRÉE DE ZONE R10 — aucune case
  neuve, la falsification passe par la somme de zone (la porte reste
  juge) ; chaînes S08/S09 + cmdlines en queue de zone sup 3 (0x70FA-
  0x71A0, marge 95 o). Code 169 o / 36 ins / padding 23 o ; sup-09:R4
  (I/sup-09-scenario.md révision 4) gagne les 5 octets de `call PREVOL`
  @0x4CE6 (432 o, padding 80).
- STRUCTURE INTERNE DU PRÉVOL (économie de place) : .ligne (relais
  terminal jmp vers win-05 : mov r8d,1 + code → 18 o) et .attendre
  (mort bornée HPROC + GetExitCodeProcess + CloseHandle, cadre 0x28 —
  ombre ABI D98) factorisent les DEUX sondes : 149 o de code utile.
- CHAÎNE VERTE (graines 20261029/20261030/20261029, cristallisation 3/3
  byte-stables) : R5 100 % (25 blocs, f60039 36/36), oracle structurel
  1 158 verrous (+28), scénario 10 124 cas verts (+7 : verdict f60039,
  échec (l) prévol dégradé, mutation M10, cible porte f60039), falsifi-
  cation 29/29 cibles + 10 mutations, carte génération 5 re-scellée
  (25 empreintes + Ed25519 + R8), PE 75 264 o TAILLE INCHANGÉE (le prévol
  vit dans le 0xCC de queue de zone), sha256 81f7ef3feab8ff29f4dd7334ca
  c1ff5128f8a06cfd3f95f9e6b4e992f7261a76, md5 2d2bc168…, version
  terrain.7 (u64 0x00050107, FileVersion 0.5.0.7).
- VERROUS D'ORACLE NEUFS : (l) prévol dégradé (taskkill absent + amont
  curl 28 → S08 sautée SANS crash, S09 code=28 BRUTE au journal, verdict
  = 1 : les sondes ne comptent JAMAIS) ; M10 (ligne S08 amputée 41 → 40 :
  le journal d'or refuse — miroir M9/S47) ; la porte détecte f60039 via
  la somme de zone (cible 29e, octets 11/23). Journal d'or : S08
  code=128 (rien à tuer — FS vierge, l'état PROPRE) + S09 code=0, AVANT
  S04 ; lancements 9 (publique) / 12 (livraison).
- DIFFÉRENTIEL 17-E → 17-F (scripts/verif_terrain17f.py) : 579 octets en
  ONZE plages TOUTES NOMMÉES (sommes R10 #16/#25/#27 ; version u64 ; le
  prévol 0x4B40-0x4BFF de 0xCC vers code ; call PREVOL + 2 disp32
  jmp .fin +5 + code décalé ; chaînes zone 3 ; champs .rsrc) — kit INTACT
  (demo 73c064fb…, proxy 33c91815…), loader D54 INTACT, table R10
  28 entrées CONSERVÉES, entrée zone sup 1 géométrie inchangée (0x4340/
  0x8C0), monotonie ✓. Cosmétique : le tableau de bord affichait l'u64
  terrain.4 (bug d'affichage préexistant) — corrigé vers TERRAIN7.
- LIVRAISON : download/superviseur-terrain17f.exe + LISEZMOI-
  terrain17f.txt (md5 MATCH vérifié) ; le 17-E retiré du download
  (mono-génération ; référence locale scripts/superviseur-terrain17e_
  ref.exe — le différentiel reste rejouable). POUSSÉE DRIVE BLOQUÉE :
  le refresh OAuth du relais est MORT (HTTP 400 invalid_grant, 29/10
  08:11 — jeton révoqué/expiré) ; le compte de service .gdrive/
  physichong (z-ai-811@physichong.iam.gserviceaccount.com) s'authentifie
  (JWT RS256, scripts/relais_service_account.py neuf) et LISTE tout le
  Drive Triade mais n'a que le rôle LECTEUR (403 « Insufficient
  permissions » à la création, racine comprise) → le canal /test attend
  un partage Éditeur du dossier test au compte de service (ou une
  reprise OAuth interactive côté développeur) ; livrable disponible dans
  download/ de l'espace de travail.
- Docs : Entrée 87 du journal, DECISIONS D101, worklog (Task ID 28),
  I/README + I/sup-09 rév 4 + I/sup-39 neuf, LISEZMOI-terrain17f.txt ;
  aucune clé touchée : RIEN à remettre par cérémonie (phrase de contrôle
  D81 valable, conteneur 0323029a… inchangé, sentinelles intactes —
  proxy 0.4.0 dd12b649…, demo 73c064fb…, hello, selftest, echo ; le
  superviseur du dépôt est la balise COURANTE terrain.17-F 81f7ef3f… —
  artefact vivant re-scellé par version).

Stage Summary:
- TERRAIN.18 ACCOMPLI : la demande développeur du 29/10 est INTÉGRÉE —
  taskkill et la vérif curl vivent DANS le superviseur (prévol f60039),
  les ÉTAPES 0/0 BIS du protocole sont SUPPRIMÉES du LISEZMOI ; la 2e
  fenêtre est expliquée (la coquille démo de T1 — normale, refermée par
  la panne connue D57)
- LEÇON SYSTÉMIQUE : une table d'intégrité PLEINE n'interdit pas
  d'ajouter du code — elle impose de vivre SOUS une couverture
  existante (le prévol zone-résident : la porte reste juge par la somme
  de zone, aucune case neuve)
- Canal Drive : OAuth relais mort + compte de service lecteur — le
  partage Éditeur du dossier test au compte de service rouvre la voie
  (action développeur, une seule fois)
- Suite M4 : LE JOURNAL + LE TÉMOIN du run 17-F (S09 dira l'amont AVANT
  les tests) → scellage 0.5.0 si S49 OK + témoin « 200 » complet ; sinon
  correctif ciblé (tls-08 si tronqué) ; puis v0.6.0 axes 2-3 (CF2-
  Shamir, sceau I) selon D86/D87 ; terrain : D57 (WER) seul point ouvert

## Task ID 29 — D102 : tls-07:R2, l'anomalie des 13 octets éteinte (2026-10-29)

- TÉMOIN 17-F ANALYSÉ byte-level : 13 o = en-tête TLS brut + nonce GCM —
  Schannel reclasse les tampons PAR TYPE ([0]=STREAM_HEADER, [1]=DATA,
  [2]=TRAILER, [3]=EXTRA) ; l'ancienne tls-07 lisait des positions fixes
- CORRECTIF tls-07:R2 (scan PAR TYPE, E4 fail-closed) + shims au
  reclassement réel + dispositions aléatoires au fuzz ; 40 + 53 PASS,
  oracle M4 560 verts ; proxy.exe 28 160 o TAILLE INCHANGÉE (carte
  génération 6, cristallisation 2/2, sha b9264e0b…)
- TERRAIN.17-G : kit D102 (md5 proxy 2b6481a1…), terrain.8, 75 264 o
  TAILLE INCHANGÉE (sept générations), sha ee23cc80…, différentiel
  295 o / 10 plages nommées ; livraison download/ + /test Drive (md5
  MATCH) ; 17-F archivé en référence locale
- Canal Drive : OAuth relais RESSUSCITÉ (refresh_token neuf + copie
  Tokens) — meurt dans 7 jours (mode Testing) ; parade définitive :
  partage Éditeur du dossier test au compte de service
- Suite : LE JOURNAL + LE TÉMOIN du run 17-G (S05C md5 2b6481a1…) →
  scellage 0.5.0 si S49 OK + témoin « HTTP/1.1 200 » ; puis v0.6.0 axes
  2-3 (CF2-Shamir, sceau I) selon D86/D87 ; terrain : D57 (WER) seul
  point ouvert

## Task ID 30 — D103 : terrain.19 / 17-H, le doublon est mort (2026-10-29)

- JOURNAUX 17-G RAPATRIÉS (SA, md5 MATCH) : S05C 2b6481a1 ✓ (kit D102) ;
  TÉMOIN « HTTP/1.1 502 Passerelle inaccessible » = HTTP CLAIR chez le
  client — D102 PROUVÉ sur machine réelle (le 502 = amont coupé PENDANT
  le run, S47 exit=0, S49 KO honnête) ; S11 « fenetre demo ABSENTE » x2
  pendant que demo_journal.txt (5 lignes vivantes) prouvait la fenêtre
- DIAGNOSE DOUBLON (constat développeur prioritaire, juste) :
  FindWindowW(NULL, « TRIADE_demo ») = recherche par TITRE (notation
  ligne 31-32, binaire 0x424f) — le bug terrain.5 ressuscité par la
  reconstruction terrain.17 (le patch BINAIRE terrain.6 n'a jamais vécu
  dans la source) ; terrain.14 détectait, 17-C→17-G mentaient (7 runs) ;
  oracle complice (shim rendait toujours un handle — leçon D102 au
  niveau user32)
- CORRECTIF sup-33:R2 : classe en rcx / NULL en rdx (9 octets échangés,
  même adresse 0x544f, même cible 0x2a92) ; spec Q2 réécrite, notation
  régénérée 940 o INTACTE, layout terrain.19 + VERSION_TERRAIN9
  (0x00050109, .rsrc 0.5.0.9), auteur.py + README à jour
- ORACLE : contrat Win32 RÉEL (handle ssi classe « TRIADE_demo »),
  verrou D103 (3 appels exacts par variante), mutation M11 (le bug 17-G
  rejoué octet par octet) ATTRAPÉE ; M10 restauré (compteur avalé par
  la première insertion — audit par exécution isolée : 40 = 29 + 11)
- CHAÎNE : 10 127 cas verts (+3), 29/29 + 11 mutations, 1 158 verrous,
  round-trip 100 %, carte re-scellée (R8 OK), 75 264 o (HUIT
  générations), sha256 f947b605…, md5 ab8afc77… ; kit INTACT (demo
  73c064fb… + proxy 2b6481a1…) ; diff 17-G → 17-H : 23 o / 8 plages
  nommées, .blob intouché
- LIVRAISON : download/superviseur-terrain17h.exe + LISEZMOI-terrain17h
  (preuve comportementale : S11 « detectee » + S12 « clic envoyé »,
  impossibles en 17-G) + Drive ; dépôt demandé EN PLUS : demo_journal.txt
  (la donnée D57) ; 17-G archivé (scripts/superviseur-terrain17g_ref.exe)
- Suite : run 17-H → T1 atteint ENFIN la panne D57 (S13 0xC0000005
  attendu, honnête) ; S49 OK + témoin « HTTP/1.1 200 » → scellage 0.5.0
  (sinon 502 = amont, réessayer — D102 déjà prouvé) ; puis v0.6.0 axes
  2-3 (CF2-Shamir, sceau I) selon D86/D87 ; D57 avec le journal démo
  complet

## Task ID 31 — D104 : M4 scellé 0.5.0 — le run 17-H a livré le jugement et le témoin (2026-10-29)

- JOURNAUX 17-H RAPATRIÉS (SA, md5 MATCH) avec le dépôt du superviseur
  lui-même : md5 ab8afc77… == livraison D103 (identité du run prouvée) ;
  S05C 2b6481a1 ✓ (kit D102 octet pour octet)
- VERDICT : doublon MORT sur machine réelle (S11 detectee + S12 clic
  envoyé + demo_journal 14 lignes — impossible pour 17-G) ; T1 KO honnête
  D57 PRÉVU (échange réseau échec + 0xC0000005 — l'intervalle exact en
  main) ; T2 OK ; **T4 S49 OK + témoin HTTP/1.1 200** (640 o example.com
  en clair par le tunnel, badssl 34 o exacts, S47=0) — juges M4 verts
  ENSEMBLE, première fois avec témoin 200
- CONFORMITÉ § 8.2 écrite pour M4 (m4/conformite_profil.py, 44 contrôles
  + sentinelle oracle ; trois leçons de constat : empan de section, hints
  sans padding, padding compté depuis la queue)
- CRISTALLISATION 10/10 (verifier × graines 20261029-37 ; 49 blocs) ;
  _sceller porté (rc/final, modèle D74) ; cérémonie : 0.5.0-rc.1 →
  **0.5.0 FINALE** (frag-bld une occurrence, fragments re-chiffrés,
  carte re-signée Ed25519) — proxy.exe INTACT (2b6481a1…, 28 160 o : le
  scellage est un fait de carte, la preuve terrain reste la preuve du
  binaire scellé) ; anti-rollback ARMÉ (testé), R8 indépendant 49
  empreintes artefact 0.5.0
- M4 CLOS (§ 16) : balise 0.5.0 immuable, défaut → 0.5.1 (R4)
- Suite : v0.6.0 axes 2-3 (CF2-Shamir, sceau I) D86/D87 ; D57 avec
  l'intervalle exact (M2 scellé, 0.3.x à contrat stable si ouvert) ;
  partage Éditeur /test au SA toujours attendu (refresh OAuth ~05/11)

## Task ID 32 — D105 : v0.6.0 axe 3, le sceau de l'Intention (2026-10-29)

- CONTEXTE : M4 scellé 0.5.0 (D104) → suite déclarée = v0.6.0 axes 2-3 ;
  axe 3 ouvert le premier (additif, zéro contact coffre/clés existantes)
- SPEC écrite-avant-code : v06/I/README.md (220 lignes) — 10 arbres
  (9 lignées + v06/I : le sceau se scelle lui-même), manifeste canonique
  POSIX, empreinte = SHA-256 du texte entier, signature Ed25519 sur 32 o
  (charge utile PAPIER), codes 0/10/11/12, périmètre des trois gardes
- CÉRÉMONIE v06/ceremonie_hors_ligne.py (427 l.) : stdlib SEULE, autotest
  RFC 8032 fail-closed ; VECTEURS VÉRIFIÉS À LA SOURCE (mémoire fautive
  sur TEST 2 — rattrapée multi-sources + témoin cryptography : la leçon
  D102 retournée en méthode de preuve)
- OUTIL v06/sceau_I.py (470 l.) : preparer / deposer (atomicité INTÉGRALE
  — faute propre corrigée : clé installée seulement en phase d'écriture) /
  signer-test / verifier / etat ; 10 arbres signés (clé TEST = constante
  PUBLIQUE, état « test » visible — X8 tenu) ; a-signer.txt prêt
- FALSIFIABILITÉ v06/test_sceau_I.py : 47 PASS / 0 ÉCHEC (T1 RFC + T2
  interop ×20 bidirectionnelle + T3 déterminisme + F1 cérémonie complète
  en sous-processus jusqu'à « reelle » sur réplique + F2 un octet/arbre
  10/10 nommé + F3 manifeste réécrit dénoncé (11) + garde de build + F4
  remise douteuse sans écrire) ; 2 fautes du HARNAIS nommées, zéro dans
  le sceau
- GARDES : build_m4.py [m0..m4] ×3 chemins + build_terrain.py
  [m0,m1,m2,demo,terrain] ×2 chemins ; PREUVE END-TO-END : octet muté
  dans m4/I/tls-02-verdicts.md → build refuse EN TÊTE (exit 1, fichier
  nommé), restauration → vert
- NON-RÉGRESSION : M4 verifier EXIT=0 (38/38, 524+482 verrous,
  cristallisation 10/10, R8 49) ; terrain verifier EXIT=0 (10 127 cas,
  1 158 verrous, R8 25) ; ARTEFACTS INTACTS (proxy b9264e0b… 28 160 o,
  superviseur f947b605… 75 264 o)
- NOTA : dépendances build réinstallées (bac à sable reconstruit :
  capstone, keystone-engine, pefile, pynacl, unicorn)
- LIVRAISON : download/LISEZMOI-cle-I.txt + copie du script de cérémonie
  (flux air-gap pas à pas — la souveraineté s'arme à la cérémonie réelle)
- Suite : v0.6.0 axe 2 (CF2-Shamir D86) ; cérémonie réelle développeur ;
  D57 (intervalle exact en main) ; partage Éditeur /test au SA
  (refresh OAuth ~05/11)
