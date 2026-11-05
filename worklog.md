
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

## Task ID 33 — D106 : v0.6.0 axe 2, l'interrupteur d'homme mort (2026-10-29)

- CONTEXTE : axe 3 livré (D105/Task 32) → l'axe 2 (CF2-Shamir, D86)
  mené spec d'abord ; coffre réel et clés JAMAIS touchés (discipline D105)
- SPEC écrite-avant-code : v06/I/CF2/README.md (13 sections — Shamir
  GF(2^8)/0x11B, conteneur TRIADE-CF2 (miroir CF1, HKDF coffre=v2, champ
  verif qui nomme la clé fausse), fragment papier lié au SEL du coffre,
  gardes, sentinelle double seuil, destruction + PV, restauration
  atomique, migration CF1→CF2, bornes honnêtes, moteur Windows consigné)
- ARBRE V06/I étendu aux axes 2-3 (balise v0.6.0-axes2-3, ARBRES
  sceau_I.py mis à jour, re-signé en phase test — 10 arbres VERTS)
- IMPLÉMENTATION : v06/coffre_cf2.py (Shamir + conteneur + gardes + CLI
  complète init/migrer/statut/etat-fragments/lister/obtenir/ajouter/
  retirer/verifier/restaurer/bruler/autotest 13 contrôles) ;
  v06/sentinelle_cf2.py (inotify ctypes IN_OPEN|IN_ACCESS fichiers,
  IN_ISDIR ignoré, balayage /proc immédiat + périodique, attribution
  exe+cmdline, anti-bruit, heart-beat, PV via la routine bruler — source
  unique ; fanotify EPERM utilisateur non root : CONSIGNÉ)
- TROIS FAUTES DÉNONCÉES PAR LES PREUVES : (1) tables GF sur 0x02 NON
  PRIMITIF mod 0x11B (ordre 51, 204 éléments muets — tests de coin
  complices) → générateur 0x03 + preuve EXHAUSTIVE (65536 distributivités,
  255 inverses) + témoin indépendant (somme de puissances, corps
  bit-à-bit, Gauss) ; (2) liaison fragment→empreinte d'en-tête (le
  parcours CLI écrire-puis-relire l'a dénoncée : nonce frais = en-tête
  changé = copies papier mortes à la première écriture) → liaison au SEL ;
  (3) relève à 2 copies impossible (autotest : 2 < seuil 3) → T copies
  hors-ligne, sémantique PROUVÉE (2 → morte, 3e → vie)
- FALSIFIABILITÉ v06/test_cf2.py : 43 PASS / 0 ÉCHEC (T1 témoin
  indépendant 1000×10 + Gauss ×50 + bornes ; T2 informationnel — deux M′
  forgés compatibles avec T−1 réels, verif nomme le mensonge ; T3
  fail-closed nommé + custodie répartie ; T4 fausses alertes NULLES —
  même binaire, seule la commande blanchit ; F1 exfiltration complète :
  PV nommé, mort, latence 0,05 s < borne 2 s, relève → vie ; F2 remise
  douteuse sans écrire ; T5 santé ; X8 coffres réels intacts)
- NON-RÉGRESSION : oracle M4 560 cas + verifier EXIT=0 (38/38, 482
  verrous, cristallisation 10/10, R8 49) ; oracle terrain 10 127 cas +
  verifier EXIT=0 (1158 verrous, R8 25) ; test_sceau_I 47/47 ; artefacts
  intacts (proxy 2b6481a1…/b9264e0b… 28 160 o ; superviseur f947b605…
  75 264 o)
- LIVRAISON : download/LISEZMOI-coffre-CF2.txt (cérémonie réelle pas à
  pas : vérifier → migrer → TROIS copies hors-ligne → liste blanche
  éditeur → sentinelle → sante ; bornes honnêtes en clair)
- Docs : DECISIONS D106, JOURNAL Entrée 92, FORMAT_CARTE § 11.4, PLAN
  (avancement v0.6.0), README, worklog (Task ID 33)
- Suite : passation PROTOCOLE_TRIADE à v0.6.0 (mûre — axes 2-3 écrits,
  axe 1 consigné ; arbitrage développeur) ; cérémonies réelles clé-I +
  coffre-CF2 ; D57 (intervalle exact en main) ; partage Éditeur /test au
  SA (refresh OAuth ~05/11)

## Task ID 34 — D107 (consignation différée) + D108 : le kit de cérémonie déposé dans /Cérémonie du Drive (2026-10-30)

- CONTEXTE : demande développeur du 30/10 — « dépose les livrables dans un
  dossier /Cérémonie du drive ». En amont : D107 (le maître de cérémonie
  graphique, réponse à « un script python auto-suffisant qui installe
  lui-même les dépendances requises et ouvre une GUI ») fut livré et
  committé (da8fd4c, 29/10 16:25) mais la session s'interrompit AVANT
  worklog/journal — la consigne de référence de D107 est le MESSAGE DE
  COMMIT ; cette dette de consignation est soldée ici (JOURNAL Entrée 93)
- LE DOSSIER POSÉ (14 fichiers, /Cérémonie créé à la racine du Drive
  « Triade », id 1JJXohy5olmngfm_hE_AW17AfjSciISSg) : profil hors-ligne
  (ceremonie_gui.py autoporteur + ceremonie_hors_ligne.py interopérable) ;
  les TROIS LISEZMOI (ceremonie-GUI, cle-I, coffre-CF2 — encarts MODE
  GRAPHIQUE inclus) ; lanceurs lancer_ceremonie.bat/.sh ; MANIFESTE.txt
  (taille + md5 + sha256 par fichier, régénéré à chaque dépôt) ; et v06/
  (le complément « profil dépôt » : __init__.py + les cinq .py du dépôt) —
  le sous-dossier fait du dossier un MINI-DÉPÔT : le GUI y relaye les CLI
  par RACINE_DEPOT/v06/*.py (import v06.coffre_cf2 opérationnel) ; la
  vérification des DIX arbres du sceau exige le dépôt complet — échec
  nommé depuis le kit seul, par conception
- CANAL : OAuth relais (refresh du 29/10, mode Testing ≈ 7 j — échéance
  ~05/11) ; le compte de service reste LECTEUR (échec nommé avec ses
  parades si l'OAuth meurt)
- PREUVES : gardes anti-divergence AVANT dépôt (download/ ↔ v06/ md5
  identiques pour le GUI et la CLI hors-ligne — un kit divergent n'est pas
  déposé) ; vérification ALLER-RETOUR 14/14 md5 MATCH ; IDEMPOTENCE prouvée
  par relance (14/14 « inchangé », aucun doublon) ; AUCUN secret déposé
  (ni clé, ni phrase D81, ni coffre — les LISEZMOI ne portent que des
  références, vérifié avant envoi)
- Outil : scripts/drive_ceremonie.py (dépôt + --sonde, gardes, manifeste,
  vérification md5 aller-retour, idempotent) ; journal d'exécution et
  copie d'audit du manifeste dans scripts/ de l'espace de travail
- Docs : JOURNAL Entrées 93 (D107, différée) + 94 (D108), DECISIONS D108,
  README (paragraphe cérémonies D107/D108), PLAN (avancement v0.6.0),
  worklog (Task ID 34)
- Suite : cérémonies réelles (cle-I + CF2) par le GUI — le kit est prêt,
  depuis le dépôt OU depuis le Drive ; D57 ; partage Éditeur /test au SA
  (refresh OAuth ~05/11)

## Task ID 35 — D111 : le maître de cérémonie s'attache au dépôt (2026-10-30)

- CONTEXTE : demande développeur du 30/10 — « le GUI de cérémonie ne se
  connecte pas au dépôt, je n'ai accès qu'à la version hors-ligne ;
  j'aimerais pouvoir tester en local, à moins que tu aies une solution
  pour le lancer à partir du repo git ». En amont, dette de consignation
  D109/D110 soldée (JOURNAL Entrées 95 — référence : commits e3eee92 /
  594f4dd, modèle Entrée 93)
- DIAGNOSTIC : D107 calculait RACINE_DEPOT depuis la SEULE position du
  fichier (<dépôt>/v06/) — le GUI téléchargé SEUL (fichier unique depuis
  /Cérémonie) n'active que le hors-ligne, par conception D108 le kit ne
  devient mini-dépôt que téléchargé ENTIÈREMENT ; aggravant : le remote
  GitHub vivait à D95, 17 commits NON POUSSÉS — un clone ne contenait
  même pas v0.6.0
- LIVRÉ (v1.3) : ordre de résolution NOMMÉ --depot CHEMIN > TRIADE_DEPOT
  (env) > position du fichier (défaut D107 inchangé) ;
  _resoudre_racine_depot() → (racine, source) ; chemin introuvable =
  ÉCHEC NOMMÉ (code 2 au point d'entrée, cause sur stderr, jamais de
  repli silencieux) ; dossier sans v06/coffre_cf2.py = profil désactivé,
  l'accueil nomme la cause ET les trois parades ; definir_racine_depot()
  rebascule le global AVANT construction — relais CLI / import
  v06.coffre_cf2 / sentinelle / config par défaut suivent (lecture à
  l'appel) ; l'accueil AFFICHE le dépôt attaché + sa source ; LA MÊME
  GARDE v06/coffre_cf2.py protège les trois voies
- PREUVES : test_ceremonie_gui.py 69 PASS / 0 ÉCHEC (X3 nouveau : 14
  contrôles — défaut inchangé, résolution, échecs nommés arg+env,
  précédence, fail-closed sans v06, v06 factice incomplet refusé,
  bascule/rétablissement, point d'entrée en sous-processus ×3) ; fumée
  D111 (Xvfb, scripts/fumee_gui_depot_d111.py au bac à sable) 10/10 —
  scénario EXACT de la demande : copie autonome → symptôme (profil dépôt
  refusé, --profil depot retombe sur l'accueil) → correctif (page dépôt
  ouverte directement, config dans le dépôt attaché, relais CLI réel
  sceau_I.py etat code 0) ; NON-RÉGRESSION : test_cf2 43/43 (coffres
  réels md5 inchangés), test_sceau_I 47/47 (dépôt réel VERT), fumée GUI
  19 contrôles VERT, selftest 7/7 ; kit download/ resynchronisé (md5 ==
  v06/, LISEZMOI v1.3 avec « SE CONNECTER AU DÉPÔT »)
- Docs : JOURNAL Entrées 95 (D109/D110 différées) + 96 (D111), DECISIONS
  D111, README (compteurs rafraîchis 69/7/19/10 + paragraphe D111),
  worklog (Task ID 35)
- POUSSÉE : les 18 commits (D95→D111) vers origin GitHub — v0.6.0
  devient clonable, c'est la voie « tester en local » recommandée :
  git pull && python v06\ceremonie_gui.py
- Suite : redépôt du kit Drive (ceremonie_gui.py + LISEZMOI + MANIFESTE)
  si l'OAuth relais vit encore (~05/11) ; cérémonies réelles (clé-I +
  coffre-CF2) ; D57 ; partage Éditeur /test au SA

---
Task ID: 29
Agent: Z.ai (agent principal)
Task: demande développeur 30/10 (suite D111) — « j'aimerais, dans le GUI,
pouvoir choisir le chemin dossier du repo local, choisir le chemin du
coffre, et choisir le chemin du fichier de clé (ou entrer la clef à la
main) » — D112 : les TROIS chemins se choisissent DANS la fenêtre.

Work Log:
- LE DÉPÔT SE CHOISIT DANS LA FENÊTRE (la suite logique de D111 — la ligne
  de commande devient un RACCOURCI, plus une obligation) : bouton
  « Choisir le dossier du dépôt… » à l'accueil ET sur la page dépôt
  indisponible ; garde Inchangée v06/coffre_cf2.py (le mauvais dossier =
  refus NOMMÉ par dialog, attachement et pages INCHANGÉS — fail-closed) ;
  le bon dossier appelle definir_racine_depot(candidat, "dossier choisi
  (GUI)") puis _rebâtir_pages() : destruction/reconstruction des trois
  pages (tout ce qui capture le dépôt à la construction suit — config CF2,
  coffre CF1, disponibilité, textes d'accueil), journal/exécuteur/barre de
  verdict vivant HORS des pages SURVIVENT (l'historique n'est jamais
  effacé) ; refus pendant qu'une cérémonie tourne (occupe)
- LE COFFRE CF1 SE DÉSIGNÉ (onglet CF2, nouvelle première section
  « Coffre CF1 — conteneur et phrase ») : champ coffre_fort.bin + Parcourir
  + état vivant (TROUVÉ·taille / ABSENT / vide) ; le champ est la VÉRITÉ —
  _coffre_cf1_exige refuse le vide avec échec nommé, AUCUN repli
  silencieux vers .keys/ ; câblé aux QUATRE actes : statut CF1
  (--chemin X statut, en-tête clair, aucune phrase), verifier CF1
  (--chemin X verifier + phrase par temporaire détruit), changer-phrase
  (--chemin X AVANT la sous-commande — argument global du parseur) et
  migrer (--depuis X) ; la phrase de contrôle DÉMÉNAGE de la section
  migration vers la section coffre : UNE frappe pour vérifier PUIS migrer
  (le préalable « coffre sain » devient un bouton) ; le dialogue de
  migration nomme le conteneur lu
- LA CLÉ I : FICHIER OU SAISIE MANUELLE (onglet Signer, le cas
  RÉCUPÉRATION PAPIER) : deux boutons radio, la ligne inactive est
  GRISEÉ ; _graine_depuis_saisie accepte 64 hex majuscules OU minuscules
  (une retape papier ne mérite pas un refus de casse — hex est hex) et
  refuse nommément longueur fausse/caractère non hex (position nommée,
  contenu jamais divulgué) ; hl_signer gagne graine_texte=None — la même
  graine produit les MÊMES signatures quelle que soit la source, l'échec
  est nommé et n'écrit rien ; l'entrée est MASQUÉE (•) avec case
  « afficher », verdict vivant (n/64 hex, position de faute, JAMAIS le
  contenu), pré-validation fail-closed AVANT lancement, champ EFFACÉ +
  « afficher » réinitialisé dès l'acte lancé, graine absente du journal ET
  du verdict (discipline « jamais à l'écran » tenue : le GUI n'affiche
  que si l'utilisateur le demande, pour vérifier sa frappe)
- DEUX DÉFAUTS ATTRAPÉS PAR LA FUMÉE AVANT LIVRAISON : (1) la saisie
  fautive partait en fil d'exécution pour mourir au journal — désormais
  _graine_depuis_saisie est appelée DANS le handler, refus nommé par
  dialog AVANT tout lancement ; (2) action() n'accepte pas de kwargs —
  statut CF2 passait au_racine= en direct, TypeError à l'exécution ;
  functools.partial comme tous les autres relais au_racine
- PREUVES : test_ceremonie_gui.py 96 PASS / 0 ÉCHEC (T9 clé à la main, 17
  contrôles : saisie signe IDENTIQUEMENT au fichier, majuscules acceptées,
  63 hex/non-hex/espace interne/trop long/vide/ni fichier ni saisie =
  refus NOMMÉS sans écriture, graine absente des textes, remise vérifiée
  verte ; T10 chemins coffre, 10 contrôles : init/ajouter/statut/verifier
  à chemin PERSONNALISÉ, --chemin AVANT la sous-commande, chemin faux =
  échec nommé, migrer --depuis (CF1 INTACT, 5 fragments chez les gardes,
  entrée témoin migrée, statut CF2 config choisie)) ; fumée D112 (Xvfb,
  scripts/fumee_gui_chemins_d112.py au bac à sable) 33/33 sur copie
  AUTONOME (le scénario exact de la demande) : mauvais dossier → refus
  nommé + rien ne bouge ; bon dossier → pages rebâties + config ET coffre
  CF1 dans le dépôt attaché + journal survit + relais sceau etat code 0 ;
  clé manuelle → mêmes signatures, champ effacé, graine nulle part,
  fautive refusée avant lancement, champs grisés ; coffre labo hors
  .keys/ → statut+verifier par relais, coffre RÉEL md5 inchangé ;
  NON-RÉGRESSION : selftest 7/7, test_cf2 43/43, test_sceau_I 47/47,
  fumées GUI 19 contrôles et D111 10 contrôles VERTES ; download/ ↔ v06/
  identiques (md5 4fe24995…)
- Docs : JOURNAL Entrée 97, DECISIONS D112, LISEZMOI-ceremonie-GUI v1.4
  (quatre façons de se connecter, sections « LE COFFRE CF1 SE CHOISIT » et
  « LA CLÉ PRIVÉE I : FICHIER OU SAISIE MANUELLE », compteurs honnêtes
  96/19/10/33), worklog (Task ID 29) ; aucune clé touchée : RIEN à
  remettre par cérémonie (phrase D81 valable, conteneur 0323029a…
  inchangé, sentinelles intactes)

Stage Summary:
- D112 ACCOMPLI : les trois chemins du développeur — dossier du dépôt,
  coffre CF1, clé I (fichier ou main) — se choisissent DANS la fenêtre,
  chacun avec sa garde fail-closed nommée, prouvés 96 PASS + 33 fumée
- Suite : redépôt du kit Drive (v1.4 + LISEZMOI + MANIFESTE) si l'OAuth
  relais vit encore ; cérémonies réelles (clé-I + coffre-CF2, le GUI est
  maintenant complet pour) ; D57 ; moteur sentinel Windows

---
Task ID: 30
Agent: Z.ai (agent principal)
Task: demande développeur 30/10 (suite de la cérémonie complète) — « tout
d'abord j'aimerais que pour la cérémonie, on puisse avant tout choisir
entre 2 scenarii qui détermineront les étapes à afficher : dossier local
et repo git. pour le cas du repos git, il faudrait un bouton qui permette
de cloner le repo voulu en local. ensuite (a) et (b) » — D117 + rattrapage
documentaire + préparation du verdict CF2.

Work Log:
- VERDICT À FROID de la re-cérémonie 59b7ddc (la promesse de la session
  précédente, tenue) : fetch → le distant avait AVANCÉ (re-cérémonie
  poussée à 01:51 par le terrain) ; clone FRAIS de GitHub (pas la copie
  de travail) → etat : clé RÉELLE 2bc97573… ; verifier : DIX arbres VERTS
  CODE 0 ; test_sceau_I 50/50 (« dépôt réel : VERT, canon LF D115 ») ;
  test_ceremonie_gui 109/111 — les 2 échecs = témoins T13 de la fenêtre
  D115, morts PAR CONSTRUCTION à la re-cérémonie (nommés comme tels,
  réparés en D117) ; hygiène clé privée : PROPRE (aucun chemin d'objet,
  inventaire sceau-I exhaustif, flux air-gap tenu)
- D117 : LE SCÉNARIO AVANT TOUT (section en tête d'accueil, deux
  boutons, choix consigné journal + boîte noire, re-choississable) qui
  DÉTERMINE LES ÉTAPES DU FIL (cinq en dossier local, SIX en repo git
  avec « Cloner le dépôt » en tête — preuve lecture seule rev-parse +
  origin, gestes décalés via hint_fil) ; LE BOUTON « Cloner en local… »
  (URL + parent Parcourir + nom PRÉ-REMPLI sans écraser la main) :
  refus NOMMÉS (URL vide, « - » = injection, destination vide/« - »/NON
  VIDE intacte, git absent 127, échec relayé), JETON masqué partout
  (masquer_jeton), preuve clone exigée après le clone (« un clone que
  l'on ne peut pas prouver n'est pas un clone »), garde D111 pour
  l'attachement (clone d'un autre dépôt : conservé, refus nommé), pages
  rebâties SUR LE FIL TKINTER (_sur_fin_action détecte _racine_pages !=
  RACINE_DEPOT) et profil dépôt OUVERT directement ; « Attacher un clone
  EXISTANT… » avec preuve git/origin exigée
- PREUVES D117 : test_ceremonie_gui.py 132 PASS / 0 ÉCHEC (T14 nouveau
  21 contrôles ; T13 rework ÈRE-COHÉRENT — le fil suit l'ère du dépôt
  réel, mentir dans un sens comme dans l'autre serait attrapé ; leçon de
  labo : dépôt nu + push main sans symbolic-ref HEAD → clone VIDE) ;
  fumée Xvfb D117 27/27 sur copie AUTONOME (clonage RÉEL labo attaché,
  fil SIX, bascule fil CINQ, jeton absent du journal/verdict/boîte
  noire) ; selftest 11 ; non-régression sceau 50/50 (aucun arbre signé
  touché), cf2 43/43, verifier CODE 0 ; VERDICT À FROID du commit 674b63e
  (clone frais) : 132 PASS, 50/50, CODE 0
- (a) RATTRAPAGE DOCUMENTAIRE : JOURNAL_TRAVAIL Entrées 98–103 (D113–D116
  consignées à retardement, référence = message de commit, modèle Entrée
  95 ; la re-cérémonie 59b7ddc avec la ROTATION 478f182d… → 2bc97573…
  CONSIGNÉE — spec § 5 ; l'ERRATUM § 12 du README CF2 consigné : « 2
  fragments » → TROIS copies, § 5 et le LISEZMOI font foi, le texte
  scellé reste INTACT — la correction entrera à la prochaine
  re-cérémonie) ; DECISIONS D113–D117 ; ce worklog
- (b) PRÉPARATION DU VERDICT CF2 À FROID : scripts/verdict_cf2_a_froid.py
  (bac à sable) — clonage froid + autotest + falsifiabilité CF2 + la
  liste de contrôle du rapport boîte noire du développeur (le coffre réel
  ne traverse JAMAIS git, le verdict lit le dépôt + le rapport) ; le
  LISEZMOI-coffre-CF2 du kit gagne la section « LA VÉRIFICATION À FROID »

Stage Summary:
- D117 ACCOMPLI ET JUGÉ À FROID : le scénario (dossier local / repo git)
  se choisit AVANT TOUT, détermine les étapes du fil, et le repo git se
  clone DANS la fenêtre (jeton masqué, preuve + garde D111, attachement
  à chaud) — 132 PASS + fumée 27/27 + clone frais 132 PASS
- (a) ACCOMPLI : la rotation de clé consignée, les entrées D113–D117 au
  journal, l'erratum § 12 consigné (texte scellé intact)
- Suite : cérémonie CF2 du développeur (le GUI est prêt : scénario repo
  git → cloner → migrer → TROIS fragments → sentinelle), puis verdict à
  froid CF2 par l'assistant ; D57 ; moteur sentinel Windows SACL/ETW

---
Task ID: 31
Agent: Z.ai (agent principal)
Task: RAPPORT DE CÉRÉMONIE du terrain v1.8 (D118, bouton « Envoyer le
rapport ») — deux échecs nommés (« générer la clé » Errno 2, « signer »
par contagie) et un crash (« CF2 — migrer » PermissionError errno 13 sur
triade\.keys\) : D119 corrige les trois, le verdict CF2 à froid repasse,
push.

Work Log:
- DIAGNOSTIC depuis le rapport (boîte noire complète, horodatée) : (1)
  « générer » écrivait la clé SANS créer le dossier de cérémonie —
  SEULE la copie de la remise D118 le créait (preuve : le re-run du
  terrain après « Préparer » a tout fait passer ; la borne D118 « le
  dossier naîtra à la première écriture » était écrite mais pas tenue) ;
  (2) « signer » échouait par contagie (clé absente) ; (3) « migrer »
  mourait sur os.open(dossier, O_RDONLY) dans _ecrire_atomique — légal
  POSIX, REFUSÉ par Windows ; crash PROPRE (conteneur = PREMIER écrit
  de migrer : aucun fragment ni config posés, reprise = re-lancement) ;
  l'« ÉCHEC : ni config ni conteneur » du statut CF2 était l'état
  NORMAL avant initialisation
- CORRECTIFS : _assurer_dossier_de_sortie (hl_generer / hl_signer /
  exporter_feuille — échec nommé « impossible de créer le dossier »,
  RIEN n'est écrit) ; _fsync_repertoire POSIX-seul dans coffre_cf2.py
  (DEUX sites : _ecrire_atomique + destruction des fragments) ;
  VERSION_GUI v1.9 (D119)
- PREUVES : selftest 18 PASS (+3 D119) ; test_ceremonie_gui.py
  155 PASS / 0 ÉCHEC (T16 neuf contrôles, témoin t15 version rendu
  ère-cohérent) ; test_cf2.py 46 PASS / 0 ÉCHEC (T6 : simulation
  Windows FIDÈLE — os.open(dossier) → PermissionError 13) ;
  test_sceau_I.py 50/50 ; sceau verifier CODE 0 (10 arbres VERTS) ;
  VERDICT CF2 À FROID D119 (scripts/verdict_cf2_d119.py au bac à
  sable) 14 PASS / 0 ÉCHEC : migrer CF1 → CF2 sous la sémantique
  Windows EXACTE du terrain + statut + verifier VERT + etat-fragments
  5/5 VIVANT + brûlage Windows → MORT + restauration TROIS copies →
  VIVANT + verifier VERT (journal/PV/heartbeat de labo re-localisés —
  discipline X8)
- KIT : download/ceremonie_gui.py re-synchronisé (md5 == v06/),
  LISEZMOI-ceremonie-GUI v1.9 (D119 consigné) ; consignation : JOURNAL
  Entrée 105, DECISIONS D119, ce worklog ; push ciblé (aucun arbre
  signé touché)
- CONSIGNES TERRAIN : git pull dans le clone → relancer (lancer_ceremonie.bat
  à la racine, ou copier v06/ceremonie_gui.py dans Cérémonie) → la clé
  générée à 04:08:45 reste VALABLE (le dossier de cérémonie existe
  désormais chez lui) → relancer « CF2 — migrer » (rien n'avait été
  posé) → export de la feuille + TROIS copies hors-ligne + sentinelle

Stage Summary:
- D119 ACCOMPLI : le rapport de cérémonie du terrain a dénoncé deux
  défauts invisibles au bac à sable Linux — corrigés et prouvés (155 +
  46 + 50 PASS, verdict CF2 à froid 14 PASS, sceau CODE 0), poussés
- Suite : cérémonie CF2 RÉELLE du développeur (migrer → TROIS copies
  hors-ligne → sentinelle), puis verdict à froid du rapport v1.9 ;
  moteur sentinel Windows SACL/ETW ; D57

---
Task ID: 32
Agent: Z.ai (agent principal)
Task: demande développeur 30/10 — « concernant la sentinelle, vu qu'elle
est une condition sine qua non du dispositif de sécurité, il faut qu'elle
soit indispensable au déverrouillage du coffre non ? parce que si le
déverrouillage est tenté et qu'elle n'est pas lancée, tous nos efforts
sont inutiles » — D120, la PORTE de sentinelle.

Work Log:
- ANALYSE : la demande est JUSTE et dénonce l'angle mort de l'ère D86 —
  spec § 6 disait « une sentinelle morte est un avertissement nominal » :
  la fenêtre la plus dangereuse (M en RAM) était la seule sans
  surveillance obligatoire, incohérent avec le fail-closed maison ; MAIS
  « indispensable » doit être dit honnêtement : la porte est une
  exigence de CÉRÉMONIE, pas une barrière cryptographique (heart-beat
  falsifiable, fragments copiables) — borne consignée D120
- D120 armé : porte_sentinelle() dans coffre_cf2.py (source unique) —
  refus NOMMÉ + parade + journal sur heart-beat absent/illisible/périmé
  (borne 5 s), AVANT toute lecture de fragment ; câblée dans
  _avec_deverrouillage (lister/obtenir/ajouter/retirer) et cmd_verifier
  → héritée par le GUI PAR RELAIS ; controle_lecture du GUI la passe
  AUSSI (c'est un déverrouillage — renommé ErreurCeremonie) ; config :
  exiger_sentinelle (défaut moteur_sentinelle_disponible() : la porte
  juge le heart-beat, pas la plateforme) + heartbeat_age_max ;
  restaurer/etat-fragments/statut/bruler HORS porte (relève possible
  coffre mort — la porte interdit l'OUBLI, pas la récupération)
- sentinelle_cf2.py : demarrer REFUSE sans moteur (pas de faux
  heart-beat — sécurité de façade interdite), import inotify gardé
  (sante court sous Windows), sante affiche la PORTE en tête ; migrer/
  init enseignent l'ordre inversé (sentinelle AVANT premier
  déverrouillage), LISEZMOI du kit réordonne (8 remplacements COMPTÉS)
- PREUVES : test_cf2.py 54 PASS / 0 ÉCHEC (T7 : 7 contrôles — refus
  nommé + journal + gardes intactes ; VERT sentinelle vivante ; « MORTE »
  nommée ; ère sans moteur avertit et passe ; heart-beat forgé PROUVÉ,
  l'aveu est le contrôle) ; autotest 17 PASS (4 porte) ;
  test_ceremonie_gui.py 157 PASS / 0 ÉCHEC (T5b : relecture gated) ;
  collatéral : _ecrire_atomique chemin NU gardé (T6) ;
  sceau_I verifier CODE 0 (10 arbres VERTS — texte scellé v06/I INTACT,
  amendement consigné D120 + kit, entrera à la re-cérémonie) ;
  test_sceau_I.py 50/50 ; kit md5 synchronisé
- CONSIGNES TERRAIN : git pull → la cérémonie CF2 suit l'ordre liste
  blanche → sentinelle → verifier (sous Windows la sentinelle REFUSE de
  démarrer honnêtement et la porte AVERTIT « SANS sentinelle » à chaque
  déverrouillage — moteur SACL/ETW reste à livrer, exigence consignée)

Stage Summary:
- D120 ACCOMPLI : la sentinelle morte ne donne plus un avertissement
  nominal — elle FERME le coffre (53 + 17 + 157 + 50 PASS, sceau CODE 0),
  poussée
- Suite : cérémonie CF2 réelle (migrer → TROIS copies → sentinelle là où
  elle peut vivre), verdict à froid du rapport v1.9 ; moteur sentinel
  Windows SACL/ETW ; D57

---
Task ID: 34
Agent: Z.ai (agent principal)
Task: demande développeur 30/10 — « sur le drive, j'ai 2 dossiers avec
les fichiers de cérémonie : un à la racine avec les .bat et sh pour
lancer la gui mais pas à jour, et un avec cf3 mais sans les .bat et sh ;
je n'en veux qu'un complet et à jour pour éviter toute confusion » +
« pour l'autotest cf3, fais une gui avec bouton d'envoi de journaux
afin que tu puisses analyser, en cas de problème éventuel. J'aimerais
que ces conditions soient systématiques lorsque tu produis un module à
tester » — D122, le kit unique + le trio systématique.

Work Log:
- DIAGNOSTIC (empreintes, avant d'écrire) : kit Drive « Cérémonie »
  D118 PÉRIMÉ — GUI v1.8 (pré-D119), coffre_cf2 pré-D119, sentinelle
  pré-D120, 6 fichiers divergents + 4 absents (dont coffre_cf3.py) ;
  le miroir git « TRIADE » (D121, complet) lu par le terrain comme « le
  dossier CF3 sans lanceurs » — la confusion était structurelle
- MISE EN ŒUVRE (1) : v06/autotest_cf3_gui.py v1.0 — relais
  sous-processus des vérités vivantes (autotest 28 + suite 90, JAMAIS
  une réimplémentation), environnement AVANT essai (pile pip par
  métadonnées importlib — argon2.__version__ DÉPRÉCIÉ — + EMPREINTES
  md5 des modules : « pas à jour » se LIT dans un rapport), boîte noire
  v06/autotest-cf3-journal.log (témoin muet si disque refusé), bouton
  « Envoyer le rapport » (trio D113 : .txt + presse-papiers + dossier,
  AUCUN réseau, aucun secret), constituer_rapport_complet au NIVEAU
  MODULE (une seule vérité prouvable headless), verdict compté DU FLUX
  et CROISÉ au code de sortie, PYTHONIOENCODING=utf-8 aux enfants
  (cp850), posture dite avant le fait (copie plate = refus nommé de la
  suite), fil ouvrier sans tkinter, tkinter protégé + AST « tk.Tk() ne
  vit que dans demarrer_gui » ; lanceurs lancer_autotest_cf3.bat/.sh à
  la racine du dépôt (conventions D118)
- MISE EN ŒUVRE (2) : kit UNIQUE — maj_kit_d122.py (idempotent) déploie
  Cérémonie/ complet (23 entrées, aller-retour md5 MATCH) + MANIFESTE
  22 empreintes + note D122 + LISEZMOI-kit.txt (« remplace les DEUX
  anciens ») + LISEZMOI-coffre-CF3.txt (protocole pupitre) ; miroir
  Drive « TRIADE » RENOMMÉ « TRIADE-sauvegarde-git » (même id,
  drive_sync.PROJECT_FOLDER mis à jour, ensure_folder le retrouve — le
  hook post-commit continue dans le MÊME dossier, prouvé) ; ZIP miroir
  kit-ceremonie-triade-D122.zip (23 fichiers, md5 MATCH)
- FALSIFIABILITÉ : test_autotest_cf3_gui.py 37 PASS / 0 ÉCHEC (X1-X8+L :
  menteux/avouant/muet croisés flux-code, troncature 3000 par boîte
  factice, kits plat et v06/ en sous-processus réels, lanceurs exécutés
  + .bat par contenu) ; selftest embarqué 18 PASS ; fumée Xvfb 19 PASS
  (boutons bloqués/reactivés, barre verte, fenêtre rapport, crash
  nommé) ; captures : les pixels VERTS n'apparaissent qu'au verdict
- PREUVE TERRAIN COMPLÈTE : kit RETÉLÉCHARGÉ du Drive → manifeste
  22/22 → lancer_autotest_cf3.sh --selftest 18 PASS, test_coffre_cf3.py
  90 PASS, ceremonie_gui.py --selftest 18 PASS
- NON-RÉGRESSION : verifier CODE 0 (10 arbres VERTS — pupitre et suite
  hors v06/I/), test_sceau_I 50/50, test_cf2 54/54, test_coffre_cf3
  90/90, test_ceremonie_gui 157/157 ; AUCUNE clé touchée
- DOCS : Entrée 108 JOURNAL_TRAVAIL + décision D122 (le trio
  systématique : GUI + boîte noire + bouton rapport, pour TOUT module
  livré au terrain) ; scripts persistés : maj_kit_d122.py,
  fumee_pupitre_cf3_d122.py, capture_pupitre_d122.py

Stage Summary:
- D122 ACCOMPLI : un seul kit complet (Drive vérifié par retéléchargement
  + ZIP), le pupitre d'autotest CF3 livré avec le trio systématique,
  tout vert (37 + 18 + 19 + 90 + 157 + 54 + 50 PASS, sceau CODE 0)
- Suite : preuve terrain CF3 par le pupitre PUIS protocole
  LISEZMOI-coffre-CF3 ; migration CF2→CF3 = cérémonie consignée
  (spec § 12) après preuve terrain

---
Task ID: 38
Agent: Z.ai (agent principal)
Task: demande terrain 30/10 — « le dossier du drive /cérémonie et
/TRIADE-sauvegarde-git/V06 ont encore des contenus différents, ça porte
à confusion » — D130, le kit ne dérive plus du miroir.

Work Log:
- DIAGNOSTIC (empreintes AVANT d'écrire, scripts/diag_drive_v06.py,
  cartes récursives des deux dossiers) : kit Drive 28 fichiers dont
  ceremonie_gui.py PÉRIMÉ (cd69cc837323… pré-D129 vs 0228d708f637…
  au miroir/au dépôt) ; v06 miroir = 42 fichiers (16 racine + I/ 3 +
  sceau-I/ 23) contre 13 au kit : TROIS tests absents + les DEUX arbres
  du sceau absents ; CAUSE RACINE = asymétrie de déclenchement : le
  miroir se synchro À CHAQUE COMMIT (hook D121), le kit n'était mis à
  jour que MANUELLEMENT (maj_kit_d122…d128.py, hors dépôt) — D129
  (commit 2ae5033) avait synchronisé le miroir 15:34 et laissé le kit
- MISE EN ŒUVRE (1) : scripts/maj_kit.py — déployeur CANONIQUE du kit,
  SUIVI PAR GIT comme drive_sync.py ; le v06/ du kit est déployé depuis
  `git ls-files v06/` (la MÊME source que le miroir, même arbre de
  travail : identité par construction, I/ et sceau-I/ inclus — preuves
  publiques, aucun secret) ; racine du kit = lanceurs + copies plates
  D87 + coffre_fort.py + LISEZMOI-*.txt (download/ labo, ignorés sans
  échec ailleurs) ; MANIFESTE.txt porte le COMMIT de référence ; gardes,
  idempotence md5, aller-retour TOUTES entrées, échecs NOMMÉS (parades
  OAuth ~05/11)
- MISE EN ŒUVRE (2) : le hook post-commit porte le kit — git-hooks/
  post-commit (modèle) + .git/hooks/post-commit (vivant) exécutent
  drive_sync.py --quiet PUIS maj_kit.py --quiet, rc journalisés
  séparément dans .gdrive/last_sync.log (échec kit ≠ blocage miroir ni
  commit) ; scripts/sync_backup.sh suit (réinstallation du hook +
  synchro explicite des deux canaux)
- MISE EN ŒUVRE (3) : docs du kit à la vérité — LISEZMOI-kit.txt (note
  D130 « kit == miroir », v06 entier listé), LISEZMOI-ceremonie-GUI.txt
  v2.1 (note D129 pilier droit, qui manquait), download/ceremonie_gui.py
  resynchronisé sur v06/ (la copie plate avait aussi vieilli)
- DÉPLOIEMENT : 29 téléversés (I/ ×3, sceau-I/ ×23, tests ×3), 5 mis à
  jour, 23 inchangés — 57/57 entrées VÉRIFIÉES aller-retour md5
- VÉRIFICATION INDÉPENDANTE (diag_drive_v06.py après déploiement) :
  divergences fichiers communs v06/ : AUCUNE ; présents d'un seul côté :
  AUCUN — /Cérémonie/v06 == /TRIADE-sauvegarde-git/v06, 42 fichiers aux
  mêmes empreintes
- FRONTIÈRES : rôles préservés (miroir = sauvegarde complète 722
  fichiers + bundle ; kit = distribution opérable 57 entrées) — D130
  unifie le CONTENU PARTAGÉ (v06/) et le DÉCLENCHEMENT, pas les rôles ;
  verifier : 9 arbres VERTS + v06 CODE 10 (fenêtre D126 INTACTE) ;
  AUCUNE clé touchée, AUCUN coffre réel, AUCUN arbre scellé

Stage Summary:
- D130 ACCOMPLI : /Cérémonie/v06 et /TRIADE-sauvegarde-git/v06
  identiques par construction, rafraîchis ensemble à chaque commit
  (57/57 vérifiés, diagnostic indépendant nul), poussée
- Suite : re-cérémonie (a) puis migration CF2→CF3 (b) — « a puis b »
  D126 ; OAuth relais à reprendre avant ~05/11

---
Task ID: 39
Agent: Z.ai (agent principal)
Task: rapport de cérémonie du terrain 30/10 17:15 (GUI v2.1) — (a) la
re-cérémonie ACCOMPLIE + « je suis prêt pour migration cf1 => cf2 =>
cf3 mais je ne trouve pas le coffre_fort.bin » — fermer la boucle au
labo et NOMMER le coffre réel.

Work Log:
- RAPPORT LU : fil du pilier droit D129 courante 0→5 (clone → préparer
  a-signer FRAIS → générer clé → signer 10 signatures vérifiées →
  déposer → git 20f40bc poussé) → verifier terrain : 10 arbres VERTS,
  cle deposee reelle ; CF1 — statut : fail-closed NOMMÉ (coffre
  introuvable dans le clone) — la question du coffre suit, à juste
  titre
- BOUCLE FERMÉE AU LABO : pull 20f40bc puis sceau_I.py verifier →
  CODE 0, 10 arbres VERTS — la fenêtre D126 est FERMÉE (spec CF3 +
  erratum § 12 CF2 sous le sceau réel du maître)
- INCIDENT BAC À SABLE (sans perte) : recyclage entre messages — disque
  restauré à ~13h15 (post-D127) ; reset --hard origin/main (WIP = bits
  de mode uniquement, diff 0/0), hook D130 réinstallé, LISEZMOI D130
  récupérés du kit Drive (md5 MATCH) — GitHub + Drive = vérités
  durables, disque labo volatil
- COFFRE RÉEL VÉRIFIÉ (scripts/verif_coffre_drive.py) : coffre_fort.bin
  à la RACINE du Drive md5 0323029a… == labo .keys/ (INTACT, livré) ;
  PHRASE-CONTROLE-COFFRE.txt + LISEZMOI-PHRASE-CONTROLE.txt présents ;
  le kit porte l'OUTIL (coffre_fort.py), jamais le COFFRE (aucun
  secret dans un kit)
- DOCS CORRIGÉS : LISEZMOI-kit.txt NOTE (b) « OÙ EST LE COFFRE RÉEL ? »
  (racine Drive, geste .keys\ du clone, chaîne CF1→CF2→CF3) ;
  LISEZMOI-coffre-CF2.txt posture clone attaché (.keys\ DU CLONE —
  CF1 — statut nomme le chemin)
- DÉPLOIEMENT : commit de consignation → hook D130 → kit + miroir
  Drive portent l'état SIGNÉ (signatures 20f40bc) et les docs corrigés

Stage Summary:
- (a) ACCOMPLIE et close des deux côtés (20f40bc, CODE 0) ; le coffre
  réel nommé dans le kit ; (b) reste : CF1 → CF2 → CF3 guidé par les
  LISEZMOI
- Suite : rapport de migration attendu (bouton Envoyer le rapport)

---
Task ID: 40
Agent: Z.ai (agent principal)
Task: rapport de cérémonie du terrain 31/10 18:18 (GUI v2.1, boîte noire
complète) — (b) EN MARCHE : CF1 trouvé + phrase changée (D110) +
migration CF1 → CF2 VERTE + feuille exportée ; DEUX questions du
terrain : « où puis-je trouver les 3 fragments sachant que le système
attend 3 fragment-*.cf2 ? » et « sur la page de choix de scénario, il y
a 2 boutons pour attacher un repo local qui font doublon ».

Work Log:
- RAPPORT LU : la chaîne réelle accomplie — CF1 statut/verifier VERT
  (coffre au dossier de cérémonie), phrase changée (nouveau sel
  1edc23db…, ancienne inopérante), premier migrer ÉCHEC nommé fail-
  closed (remise D81 pas encore remplacée — le maître l'a faite entre
  les deux tentatives), second migrer VERT (.keys\coffre_cf2.bin + 5
  gardes seuil 3 + CF1 INTACT + PORTE D120 ère sans moteur), feuille
  exportée (g3…g5)
- QUESTION FRAGMENTS RÉPONDUE PAR LE CODE LU (coffre_cf2.py,
  migration_cf3_gui.py) : 5 originaux sous .keys\gardes-cf2\g1…g5\
  fragment-N.cf2f (un par garde, dossier caché) ; la feuille =
  export PAPIER des 3 mêmes (g3-g5) ; relecture = les COPIES (une par
  champ, un fragment par fichier) ; CF3 lit les gardes du dépôt
  (champ « Racine des gardes CF2 » vide = config)
- D131 — DOUBLON TUÉ : accueil portait « Attacher le dépôt local… »
  DEUX fois (panneau de scénario + section « La cérémonie », gesture
  vu 2× dans le rapport à 6 min d'écart) → UN RENDU PAR PAGE :
  accueil = panneau de scénario SEUL (le bouton NAÎT du choix D117,
  sinon aucun bouton), cérémonie = bandeau « NON attaché » seul ;
  _sur_choisir_depot INTACT (garde D111 + preuve D118) ; VERSION v2.2
- NOTE FRAGMENTS (GUI + LISEZMOI-coffre-CF2.txt étape 3) : nomme les 5
  originaux + distingue FEUILLE (papier) vs COPIES USB (.cf2f) ;
  LISEZMOI-ceremonie-GUI.txt suit (ex-« Choisir le dossier du dépôt… »
  périmé corrigé)
- SCEAU VÉRIFIÉ AVANT CONSIGNATION : l'arbre signé v06 = v06/I/ (3
  fichiers de spec), PAS le code → verifier 10 arbres VERTS CODE 0
  APRÈS le correctif — D131 n'appelle AUCUNE re-cérémonie ; la note
  MANIFESTE kit (maj_kit.py) qui prétendait l'inverse réécrite avant
  commit
- FALSIFIABILITÉ : T18 ajouté (6 contrôles statiques) → suite
  178 PASS / 0 ÉCHEC ; selftest 19/19 ; fumée Xvfb D131 écrite
  (scripts/fumee_xvfb_d131.py, 8 contrôles fenêtre RÉELLE : zéro
  bouton sans scénario, UN en dossier local dans le panneau, UN en
  repo git + clonage distinct, jamais deux) ; fumée D129 intacte
  (21 PASS)
- DÉPLOIEMENT : commit → hook D130 (kit + miroir Drive, même geste) ;
  download/ceremonie_gui.py auto-réparé sur v06/ par les gardes du kit

Stage Summary:
- D131 livré : un bouton d'attachement par page (v2.2), note fragments
  qui nomme les originaux — tests et fumées verts, sceau INTACT
- Terrain suite (b) : copies hors-ligne des 3 fragments (g3/g4/g5,
  USB deux lieux + feuille papier) → Contrôler les trois copies →
  liste blanche → CF2 verifier VERT → lancer_migration_cf3
  (MIGRER média du piège / VÉRIFIER checksum contre la CARTE /
  DÉTRUIRE après recoupement) → rapport ; OAuth relais avant ~05/11

---
Task ID: 41
Agent: Z.ai (agent principal)
Task: demande développeur 31/10 — (1) le coffre fort devient PROJET FILS
(dossier Drive propre, repo git propre, plan milestone, instructions de
reprise ; développement différé au bouclage de TRIADE) ; (2) attaque du
jalon M5 (le chantier (a) étant déjà réalisé par D134).

Work Log:
- SITUATION RÉCUPÉRÉE : dépôt /home/z/my-project/triade, main ==
  origin/main, arbre propre ; v0.6.0 passée (D133), Entrée 121 (passation
  terminée après la mort du bac à sable), D134 (M5-a empreintes par build,
  registre 12 consignations, verifier VERT 10 PDF / 0 refus) — TOUT
  poussé ; sceau_I.py verifier : 10 arbres VERTS CODE 0 (base intacte)
- PROJET FILS — LES QUATRE DOCUMENTS (/home/z/my-project/coffre-fort/) :
  README.md (charte : les QUATRE domaines de l'analyse fondatrice CITÉS
  intégralement — journalisme/Dead Man's Switch, finance haute sécurité,
  défense/infrastructures critiques, héritage numérique ; héritage
  mobilisable comme FAITS ; frontières : rien n'est forké, aucune clé,
  nom et licence = arbitrage M0), docs/PLAN_MILESTONES.md (M0-M6 du fils :
  acte fondateur / détachement / profils / commutateur d'homme mort /
  succession post-mortem / durcissement / passation — PROPOSITION,
  l'arbitrage au développeur), REPRISE_PROJET.md (auto-suffisant :
  condition d'ouverture = UN MESSAGE du développeur), docs/JOURNAL_TRAVAIL
  (Entrée 0) + .gitignore (.gdrive/.keys/*.log) — commit initial 8f52851
- PROJET FILS — GITHUB : repo alexisfrlopez-debug/coffre-fort CRÉÉ par
  API (visibilité miroir du père : private ; jeton extrait du remote SANS
  affichage), push 8f52851 + 67757dc (main == origin/main)
- PROJET FILS — DRIVE : dossier « Coffre-Fort » CRÉÉ FRÈRE du dossier
  « Triade » (parent 1SByvY55…, id 1YP3Y8n3… via scripts/
  creer_dossier_drive_coffre.py) ; scripts/drive_sync.py du fils (adapté :
  racine propre, coffre-fort-sauvegarde-git + bundle + REPRISE) ;
  .gdrive/ copié (jeton relais, gitignoré) ; hook post-commit INSTALLÉ
  (git-hooks/ suivi + .git/hooks/) — le commit 67757dc a porté la PREMIÈRE
  synchro (hook rc=0), re-run idempotent : 8 inchangés, 0 erreur
- M5 (b) — L'AUTORITÉ DE TEST LOCALE (m5/autorite/) : fixtures générées
  au labo (regenerer_fixtures.sh, OpenSSL 3.5.7 — -not_before/-not_after
  pour l'expirée ; 4 chaînes JUGÉES à la sortie ; empreintes sha256
  consignées ; clés de TEST jetables) ; autorite_test.py (stdlib pure :
  4 modes, REFUS NOMMÉS MODE-INCONNU/FIXTURE-ABSENTE/FIXTURE-ILLISIBLE/
  JOURNAL-INDICIBLE/PORT-INDISPONIBLE, journal SUR LE DISQUE — poignée
  refusée NOMMÉE, arrêt propre arret-apres/arret-apres-secondes, la
  poignée refusée ne COMPTE PAS, page STABLE, close_notify borné 2 s)
- M5 (b) — FALSIFIABILITÉ : test_autorite.py 13 PASS / 0 ÉCHEC (C0
  fixtures+OpenSSL ; C1 valide 200+marqueur+4 lignes+journal ; C2 corps
  stable ; C3 autonome rejet+poignée nommée+SURVIE+comptes ; C4 autre-
  hôte ; C5 expirée ; C6-C9 les 4 refus VIVANTS ; C10 POST 405 ; C11
  juge croisé CURL 200/code 60 ; C12 arrêt délai 2,1 s) — deux leçons :
  s_client rc=1 sur EOF abrupte → close_notify SERVEUR + juge passé à
  CURL (le client M3 du terrain) ; l'en-tête Date fait échouer la
  comparaison naïve → le contrôle compare le CORPS (le Date RESTE : il
  est une preuve de run, modèle 17-H)
- M5 (b) — LE KIT VM ÉTAPE 1 (m5/vm/) : scenario-m5b.wsb (Windows
  Sandbox, RÉSEAU COUPÉ, kit RO C:\kit + preuves RW C:\preuves) ;
  scenario-m5b.ps1 (hosts + racine certutil + empreintes + RUN A valide
  [200+marqueur+tunnel chiffre etabli] + RUN B autonome [502 « Certificat
  rejete » 34 octets EXACTS + certificat rejete + poignée refusee] DANS
  LE MÊME SCÉNARIO + quit code 0 + TÉMOIN SUR LE DISQUE) ; client-m5b.ps1
  (héritier direct de terrain_m4.ps1) ; LISEZMOI-terrain-m5b.txt (prépa
  hôte 10 min, python EMBARQUÉ, mode dégradé nommé + nettoyage, risques
  consignés : PowerShell sans parseur au labo, révocation Schannel
  hors-ligne OUVERTE) — le proxy lancé par cmd /c à redirection NATIVE
  (la version à événements PowerShell ÉCARTÉE : portée $Preuves vide
  dans les handlers d'événements) ; .ps1 convertis en CRLF (assertif)
- M5 (b) — LE DESIGN DU FLUX NAVIGATEUR (m5/I/README.md) : le constat
  terrain.17 tient (aucun navigateur ne parle la forme absolue https:// ;
  https:// = CONNECT+chiffrement pair-à-pair, http:// = forme absolue du
  chemin M3 scellé) → ARBITRAGE : RELEVEMENT http→https AMONT RETENU
  (le proxy re-chiffre vers l'origine par le tunnel M4 TEL QUEL), MITM/
  CONNECT REJETÉ (exigerait un domaine AcceptSecurityContext entier) ;
  intentions écrites-avant-code : http-08:R3 (verdict « à relever »,
  politique armée SEULEMENT — sinon R2 octet pour octet, T2 reste vert),
  http-10:R3 (routage par LE MÊME chemin Q2' + LA LIGNE DE FLUX — zéro
  secret), http-12:R2 (--relever-https, argument inconnu = REFUS NOMMÉ
  au démarrage — graine de la CLI M5) ; question ouverte CONSIGNÉE
  (ligne de flux : bloc neuf vs console http-11)
- CONSIGNATION : DECISIONS.md +D135 (projet fils) +D136 (M5-b ouvert) ;
  JOURNAL_TRAVAIL.md +Entrées 123 (fondation du fils) et 124 (M5-b) —
  insérées AVANT le marqueur m5a (la règle du marqueur) ; PLAN_MILESTONES
  (b) → EN COURS D136 + section « projet fils » ; REPRISE_PROJET.md :
  bloc DERNIÈRES ÉVOLUTIONS 31/10 (v0.6.0, M4 franchi, M5 a/b, projet
  fils) + date ; le paragraphe État général marqué HISTORIQUE (arrêté à
  D82 — dette honnête, le journal fait foi)
- FRONTIÈRES : proxy 0.5.0 scellé INTACT (sha256 b9264e0b…, 28 160 o) ;
  AUCUNE notation touchée ; sceau non touché (m5/ + docs/ hors v06/I/) ;
  aucune clé réelle (fixtures de test jetables) ; le dépôt du fils ne
  contient AUCUN code forké
- SUIITE : build_pdf.sh (DECISIONS/PLAN sont sources du PDF formel — le
  build consignera lui-même), verifier sceau+empreintes, commit, push,
  hook D130 (kit + miroir) — TERRAIN : kit m5b (LISEZMOI-terrain-m5b),
  carte du sachet, machine froide, DÉTRUIRE CF2, git pull → modules

Stage Summary:
- D135 livré : le projet fils coffre-fort FONDÉ (repo GitHub privé poussé,
  dossier Drive frère synchronisé par son propre hook, 4 documents, Entrée
  0) — développement différé sur message du développeur
- D136 livré : M5 (b) OUVERT — autorité de test locale (4 modes, refus
  nommés, 13/13 au labo, juge croisé curl) + kit VM étape 1 (réseau coupé,
  deux runs dans le même scénario, témoin D99) + arbitrage du flux
  navigateur (relevement http→https amont, R3 écrites-avant-code) ; la
  notation R3 attend le verdict terrain de l'étape 1
Task ID: 42
Agent: Z.ai (agent principal)
Task: demande développeur 31/10 (suite) — « laisser le choix du niveau de
sécurité (cf1 - cf2 - cf3) à l'appréciation du développeur lors de la
création de son projet de développement, car imposer cf3 par défaut risque
d'être trop contraignant selon le projet » : révision de la règle D133-(7),
passation v0.6.1 + Livre du Coffre v1.1.

Work Log:
- SITUATION RÉCUPÉRÉE : dépôt /home/z/my-project/triade, HEAD 5878c99
  (D135+D136), arbre propre (47 fichiers en « bits de mode » seul — diff
  0/0, phénomène connu et consigné) ; sceau_I.py verifier AVANT toute
  action : 10 arbres VERTS CODE 0, cle deposee reelle
- LA RÈGLE REPLACÉE : « un coffre neuf naît CF3 » vivait dans
  PROTOCOLE_TRIADE.md (titre/en-tête/§ 1.7/§ 12.5/tableaux/historique),
  PLAN_MILESTONES, README, la chaîne spec_v060, le Livre du Coffre et le
  schéma de la chaîne (chaine_cf.html) — JAMAIS dans les specs scellées
  v06/I/ (constat : le sceau n'est pas en jeu)
- MARKDOWN v0.6.1 : scripts/revision_v061_md.py (miroir de
  revision_v060_md.py — huit remplacements/insertions ASSERTÉS) : titre,
  en-tête (archives + Livre v1.1), § 1.7 au passé + renvoi, § 1.8 NOUVEAU,
  § 12.5 RÉÉCRIT (trois naissances [CF1 init / CF2 init+migrer, init CF2 =
  LABORATOIRE selon la spec scellée CF2 § 12 / CF3 init], guide,
  obligations par niveau, migration disponible à tout moment, consigne au
  journal des décisions), § 19.8 NOUVEAU (correspondance + 4 rejets),
  versions + 1 ligne, clôture
- CHAÎNE spec_v061 : copie de spec_v060 + main.tex (en-tête/fancyhead/
  pdftitle), sec-a (§ 1.7/§ 1.8), sec-cf (§ 12.5 + tableau naissances +
  légende), sec-d (correspondance v0.6.1 + D137 narratif + annexe
  D75–D137 + ligne D137), cover.html v0.6.1 (sous-titre chevauchait
  .authors de 33 px — raccourci, re-sondé : +16,8 px), merge_cover.py,
  verify_spec.py (V11/V8/V9/V13/V14 mis à jour + V15 NOUVEAU : la règle
  invalidée vit en passe, D137 consignée, erratum, Livre aligné) ;
  build_pdf.sh → spec_v061/v0.6.1
- ERRATUM NOMMÉ : \begin{table}tbp] (crochet ouvrant manquant,
  spec_v060/sec-d.tex:377) — l'octet parasite « tbp] » PAGE 31 du PDF
  v0.6.0 livré (pdfplumber : ligne isolée) ; réparé [htbp] dans spec_v061 ;
  l'archive v0.6.0 reste intacte ; contrôle V15 raffiné (le parasite est
  une LIGNE isolée, la citation « tbp] » de la table de correspondance est
  légitime)
- SCHÉMA re-capturé : chaine_cf.html (note → « le niveau d'un coffre neuf
  est arbitré par le développeur (D137) »), Playwright @2× (2244×1912),
  PNG porté à spec_v061 + livre_coffre (spec_v060 archivée intacte)
- LIVRE v1.1 : main.tex/cover v1.1, avant-propos (complément de la
  v0.6.1), légende, runbook « Pour un coffre neuf » réécrit (arbitrage +
  trois naissances + chaîne disponible), table décisionnelle + D137,
  réponse FAQ alignée (question verbatim — réellement posée), build_livre.
  sh → v1.1
- DOCS : PLAN_MILESTONES (phrase de naissance révisée), README (pointeurs
  v0.6.1/v1.1, cahier V1–V15, discipline § 12/17.3), REPRISE_PROJET (bloc
  DERNIÈRES ÉVOLUTIONS : v0.6.1 en tête)
- CONSIGNATIONS : DECISIONS.md +D137 (demande citée fidèlement, règle,
  rejets, passation, erratum, frontières, vérifiabilité) ;
  JOURNAL_TRAVAIL.md +Entrée 125 (insérée AVANT le marqueur m5a — la règle
  du marqueur)
- BUILDS PRÉLIMINAIRES : spécification v0.6.1 39 pages sha256 f34b2720e3f5…
  (pdf_qa PASS — 11 advisories typographiques hérités, non bloquants,
  classe consignée depuis D133) ; Livre v1.1 26 pages sha256 25be934886d4…
  (pdf_qa PASS) ; empreintes consignées PAR LE BUILD (n°14, n°15) ; les
  deux artefacts livrés à download/
- FRONTIÈRES : AUCUN code d'outil touché (les trois init existaient — le
  droit de choisir manquait) ; coffre réel RESTE CF3 ; sceau vérifié avant
  consignation (10/10 VERTS) ; proxy 0.5.0 intact ; aucune notation
- SUITE : build final (les .md consignés sont sources du PDF — le stamp
  diverge, reconstruction et nouvelle consignation attendues), verify_spec
  V1–V15, contrôle visuel des deux PDF, commit + push (hook D130), note
  d'alignement au projet fils coffre-fort (commit propre)

Stage Summary:
- D137 livré : le niveau de naissance d'un coffre neuf (CF1/CF2/CF3) est
  l'arbitrage du développeur à la création — règle v0.6.0 invalidée
  explicitement, spécification v0.6.1 (§ 1.8, § 12.5, § 19.8) et Livre du
  Coffre v1.1 alignés, erratum « tbp] » nommé et réparé, chaîne
  diagramme re-capturée

Task ID: 43
Agent: Z.ai (agent principal)
Task: cérémonie D87 réalisée par le développeur (signatures-I.txt déposé
au coffre « test ») — dépôt sceau, build scellé 0.5.1 (jalon v7/D140-S3),
checklist guide §6, kit v7, livraison Drive.

Work Log:
- REMISE RAPATRIÉE : signatures-I.txt (1 425 o, md5 467ea252…) téléchargé
  PAR ID depuis le dossier « test » du coffre, md5 local == distant
  (intacte) ; sceau_I.py etat AVANT : m4 DIVERGE (README.md), 9 verts
- DÉPÔT : sceau_I.py deposer → 10 signatures installées, état clé =
  reelle (ceremonie hors-ligne, D87) ; verifier APRÈS : 10 arbres VERTS,
  m4 = 7e5c61fbce15d3ec… (empreinte signée attendue — RAPPORT chirurgie)
- BUILD SCELLÉ 0.5.1 (UNIQUE — anti-rollback : la carte scelle ensuite) :
  g70005 tls-05:R2 325 o round-trip 67/67 ; oracle structurel 524 + 492
  verrous PASS ; différentiel 560 cas verts ; R7 image M3 == scellé 0.4.0
  octet pour octet (bf02769f…) ; PE 28 160 o, 5 sections, kernel32 x10 +
  ws2_32 x13 + secur32 x7, entrée 0x7DC0 ; carte génération 6 (49 blocs,
  5 artefacts, Ed25519) ; verrou croisé OK ; scellé-dev sha256
  fb41697ddde265ac659bdceecc2ab3ec55f564d0998d43059090235762edf3f3
- CHECKLIST GUIDE §6 (scripts/checklist_051.py — indépendante du build,
  capstone + lecture PE directe) : TOUT PASSÉ — taille/table de sections/
  ImageBase ; delta .text3 CONFINÉ au slot tls-05 (0x65C0-0x673F) ;
  delta .rdata NOMMÉ = somme .text3 de la porte R10 (0x2818, recalculée
  car le bloc a changé) + version (0x2820, 0x00050002 → 0x00050003) ;
  .text/.text2/.data OCTET POUR OCTET (héritage R7) ; désassemblage du
  site ACH : trame 0x98 @0x14000660d, mov dword [rsp+0x48],5
  @0x140006651, lea rax,[rsp+0x48] @0x140006679, mov [rsp+0x20],rax
  @0x14000667e (pAuthData = ARG 5, erratum E1), xor r9d,r9d
  @0x140006692 (pvLogonID NULL), call [rip] → IAT 0x140002A00
  @0x140006695, ordre cohérent ; table verdicts tls-02 (0x6080-0x611B)
  octet pour octet ; R_TXT_502_CERT @0x2CA0 34 o INTACTE
  (« HTTP/1.1 502 Certificat rejete\r\n\r\n ») ; entrée 0x7DC0 ; secur32
  7 entrées IAT @0x2A00 ; kernel32 x10 + ws2_32 x13 ; sha256 == scellé-dev
  annoncé ; md5 ≠ scellé 0.5.0
- KIT v7 (scripts/assembler_kit_v7.py) : base = m5b-kit-v6.zip LIVRÉ (le
  coffre fait foi) ; proxy 0.5.0 → 0.5.1 (contrôle sha256 avant/après) ;
  scenario v7 ; LISEZMOI-KIT-M5B.md aligné v7 (7 remplacements ancrés,
  ancres assertées) ; archive 11 185 452 o, 55 entrées, intégrité OK,
  pièces critiques 4/4, marqueurs v7 4/4, racine v5 inchangée
  (86525998…)
- LIVRAISON DRIVE (scripts/drive_livraison_v7.py — idempotente) :
  5 pièces préparatoires DÉJÀ CONFORMES ; m5b-kit-v7.zip TÉLÉVERSÉ
  (id 1yCNq6PnUTt1…, 11 185 452 o, md5 1609228df344…) ; recoupement
  final nom+taille+md5 : VAGUE COMPLÈTE ET CONFORME (6/6)
- FRONTIÈRES : aucune clé réelle traversée (la remise opérateur est
  publique — signatures, pas la clé) ; le 0.5.0 scellé D104 reste INTACT
  (upload/m4/proxy-050-scelle.exe, md5 2b6481a1…) ; l'arbre m4 signé
  0.5.1 est VERROUILLÉ par la carte génération 6 (anti-rollback) ; le
  RUN v7 (opérateur, VM isolée) EST le test de validation du jalon
- SUITE : run v7 opérateur (LISEZMOI-m5b-v7.txt, Temps 3) ; retour des
  preuves au coffre preuves-m5b ; verdict sur pièces

Stage Summary:
- 0.5.1 BUILD ET LIVRÉ : la poignée ne meurt plus sur la révocation hors
  ligne (SCH_CREDENTIALS dwFlags=0) ; le chemin hérésie « certificat
  rejete » devient atteignable (UNTRUSTED_ROOT → verdict 3 → 502 34 o) ;
  kit v7 au coffre — le run v7 dira.

Task ID: 44
Agent: Z.ai (agent principal)
Task: règle permanente du développeur (03/11) — « ajoute le numéro de
version au nom du bundle, et archive les anciennes versions quand une
nouvelle est livrée » : application immédiate au coffre, consignation
D138-D141 (la dette D138-D140 du registre est soldée dans le même geste).

Work Log:
- L'ÉTAT DU REGISTRE CONSTATÉ : docs/DECISIONS.md s'arrête à D137 —
  D138/D139/D140 vivaient dans le VERDICT-run-v6-branche-S3.txt (download)
  sans consignation au registre du dépôt (dette nommée en fin de session
  v6) ; JOURNAL_TRAVAIL.md s'arrête à l'Entrée 125
- LE GESTE COFFRE (règle appliquée immédiatement) : sous-dossier
  archives-bundles créé dans TRIADE-sauvegarde-git ; triade-history-
  050-f62711b.bundle (état f62711b/D137, arbre m4 0.5.0) déposé en archive
  VERSIONNÉE — intégrité prouvée AVANT dépôt (md5 aab04f69… == coffre ==
  copie labo) ; triade-history-051.bundle demeure la version COURANTE à la
  racine ; BORNE CONSTATÉE : l'original triade-history.bundle appartient au
  compte du développeur — le jeton relais ne peut ni le renommer ni le
  déplacer (HTTP 403, lecture seule constatée) : il reste INTACT à la
  racine, son retrait éventuel est le geste du développeur (nommé au
  livrable, rien de caché)
- LA CONSIGNATION : DECISIONS.md +D138 (lecture virtualisée aveugle, 4e
  instance — le rc du producteur fait foi), +D139 (hosts ignoré — IP
  littérale tient, T6 Dnscache instrumenté), +D140 (RÉSOLU branche S3 —
  matrice T2a/T2b/T3/T5, mécanisme nommé, correction 0.5.1), +D141 (la
  règle du développeur : version au nom, archives-bundles, la racine ne
  porte que le courant ; la borne 403 consignée) ; JOURNAL_TRAVAIL.md
  +Entrée 126 insérée PAR SCRIPT AVANT le marqueur m5a (la règle du
  marqueur ; insertion assertée : marqueur unique, ordre recoupé) ;
  worklog +Task ID 44
- FRONTIÈRES : les arbres scellés ne sont pas touchés (les quatre
  décisions vivent dans docs/, hors v06/I/) ; aucune clé, aucun artefact ;
  le dossier « test » RESTE une file de livraison (la règle porte les
  bundles de TRIADE-sauvegarde-git uniquement — scoping nommé à D141)
- MÉCANIQUE POUR LES LIVRAISONS FUTURES : nom = triade-history-<jalon>.
  bundle (ex. 052 pour 0.5.2) ; à chaque vague nouvelle, les anciens vont
  dans archives-bundles (jamais supprimés) ; scripts lato :
  archiver_bundles_anciens.py (idempotent, intégrité avant dépôt) et
  miroir_maj_051.py (miroir + bundle)
- SUITE : run v7 opérateur (le test du jalon) ; retour des preuves ;
  verdict sur pièces

Stage Summary:
- D141 appliquée et consignée : archives-bundles/versionnée au coffre,
  racine = courant seul (à la réserve près de l'original du développeur,
  403 documenté) ; la dette D138-D140 est soldée au registre du dépôt —
  le journal des décisions raconte maintenant le run v6 et la règle sans
  lacune.


## Task ID 45 — Clôture du run v7 / jalon 0.5.1 + D142 (03/11)

- LE RUN v7 EST RENTRÉ : 29 pièces rapatriées par id du nouveau dossier
  coffre preuves-m5b (1_uHSH3OXtocUAJWM7CPP4DHXXHv9u0l3), 29/29
  CONFORMES par taille annoncée ; page-d2b.txt reprise par id après la
  même fausse alerte « HTML » qu'en v6 (la pièce EST la page servie,
  marqueur TRIADE-M5B-PAGE-200 présent)
- VERDICT : M5-b étape 1 — OK, 0 réserve restante ; JALON 0.5.1 CLOS.
  RUN A : 200 OK 279 o servis + « tunnel chiffre etabli » — PLUS AUCUN
  502 hérésie (v6 : 40 o, sha 4eac2836…) ; RUN B : 502 exacte 34 o
  « HTTP/1.1 502 Certificat rejete » + « certificat rejete » au journal
  proxy (LE critère g70008/g70009) ; réserve POIGNEE-B-REFUSEE LEVÉE
  sur pièce host (autorite-b.log : 2 poignées refusées, arret propre) ;
  matrice curl v6 à l'identique (rc=60/0/60/60) ; arrêts jugés sur la
  LIGNE (règle v7 tenue) ; PROXY-ARRET quit code 0 (S47/D99)
- D142 (nouveau) : l'invite du parefeu est déclenchée par la MISE EN
  ÉCOUTE, pas par un trafic — preuve par désassemblage capstone du
  binaire EXACT du run (sha256 fb41697d… vérifié dans le zip v7) :
  mov dword [rsp+0x20],0xA8610002 + mov dword [rsp+0x24],0 =
  bind(0.0.0.0:25000) INADDR_ANY ; la VM n'a AUCUNE interface
  (ipconfig-vm.txt) et l'invite apparaît quand même ; boucle locale
  EXEMPTE des règles (le mécanisme one-shot décrit par l'opérateur est
  réel au niveau connexion — signature rc=7/28, 10060/10061, absente de
  toutes les pièces) ; consignation labo + coffre
  (VERDICT-run-v7-parefeu-bind.txt)
- T6/D139 : Dnscache RUNNING, DIAG-HOSTS-IGNORE toujours ECHEC
  (« Hôte inconnu ») — D139 DEMEURE OUVERT, non bloquant, hors verdict
- CONSERVATION DES PREUVES : le dossier coffre preuves-m5b v6 (id
  1ByG_vBFFC…) est passé à la corbeille par le dépôt v7 (trashed=True
  constaté) — les 27 pièces v6 (labo, vérifiées) RÉ-ARCHIVÉES au coffre
  : /test/archives-preuves/preuves-run-v6/ + VERDICT-run-v6 ; la
  corbeille n'est pas vidée (geste possible du développeur)
- CONSIGNATION : JOURNAL_TRAVAIL.md +Entrée 127 (insertion PAR SCRIPT
  AVANT le marqueur m5a, ordre 126<127<marqueur recoupé) ;
  DECISIONS.md +D142 ; worklog +Task ID 45 (le présent) ; bundle
  nouveau nom triade-history-051-<tip>.bundle livré au miroir (D141 :
  version au nom), l'ancien 051 archivé versionné dans
  archives-bundles, la racine ne porte que le courant ; miroir
  journal/decisions/worklog recoupés md5
- FRONTIÈRES : arbres scellés intouchés ; 0.5.0 scellé D104 intact
  (md5 2b6481a1…) ; 0.5.1 fb41697d… = artefact exact du run ; aucune
  clé ; aucun artefact touché
- SUITE : étape 2 du M5 — INTERCEPTION D'UN FLUX NAVIGATEUR en VM
  isolée (relèvement amont http→https, D135 ; intentions
  http-08:R3/http-10:R3/http-12:R2 --relever-https écrites-avant-code)
  = build 0.6.0, puis run M5-b étape 2 ; D139 reste ouvert (T7
  éventuel)

Stage Summary:
- Le jalon 0.5.1 est CLOS sur pièces (run v7 OK, 0 réserve) : le proxy
  0.5.1 établit le tunnel sur certificat valide ET nomme « certificat
  rejete » face au scellé autonome — la hérésie 502 est morte ; D142
  nomme le mécanisme de l'invite parefeu (bind 0.0.0.0, pas un trafic)
  et fixe la signature d'un vrai blocage (rc=7/28) ; les preuves v6
  sont ré-archivées au coffre ; le registre (Entrée 127 + D142 +
  worklog 45) est consigné par scripts assertés et le bundle D141 est
  livré au miroir.


## Task ID 46 — Vague v8 (parefeu muet dès l'ouverture) + D143 + corbeille (03/11)

- DEMANDES DE L'OPÉRATEUR : archivage de fin de run (NOUVELLE RÈGLE),
  vérification de la corbeille, parefeu muet dès l'ouverture de la VM,
  puis enchaîner 0.6.0 (verbatim consigné à l'Entrée 128)
- VAGUE v8 (le décisif NE change pas — scénario seul) : fondement D142 ;
  scenario-m5b-v8.ps1 section 0bis AVANT tout bind (règles ALLOW nommées
  TRIADE-M5B pour proxy.exe/python.exe + inboundusernotification disable
  + parefeu-vm.txt ; diagnostics ADDITIFS) ; le service parefeu PAS
  coupé (règles + exemption boucle locale suffisent — consigné) ;
  construire_v8_scenario.py 8 remplacements ancrés ASSERTÉS (R1–R8,
  ancre CRLF nommée) ; m5b-kit-v8.zip 11 186 300 o / 55 entrées depuis
  le zip v7 LIVRÉ, proxy 0.5.1 scellé INCHANGÉ (fb41697d… vérifié
  AVANT/APRÈS, md5 dec21e75…), racine v5 86525998… intouchée,
  LISEZMOI-KIT-M5B.md aligné v8 (4 remplacements + item 12) ;
  livraison /test 3/3 CONFORME (recoupement md5+parent+nom)
- D143 (NOUVELLE) : archivage de fin de run — preuves →
  archives-preuves/preuves-run-<v>/ + verdict ; vagues consommées →
  archives-livraisons/vagues-m5b/ ; racine /test = vague courante +
  corriger-wsb + preuves-m5b vierge + 2 archives ; copie versionnée
  AVANT tout jet ; déduplication md5 ; index posés — APPLIQUÉE au run
  v7 : preuves-run-v7 (30 entrées : 29 pièces + verdict),
  preuves-m5b recréé VIERGE, vagues v6/v7 archivées (10 pièces)
- CORBEILLE VÉRIFIÉE (rétroactivité) : 46 enfants jetés de /test (les
  5 autres dossiers du coffre : zéro) — RESTAURÉS : preuves-run-v5
  (12 pièces 23:58Z), preuves-run-v4 (11 pièces 19:02Z),
  preuves-run-v2-depot1/2/3 (dépôts 18:33Z), vagues v3–v5, terrain-17
  (17e→h, superviseurs, temoin_m4a 4 contenus, terrain ×6,
  demo_journal 2 contenus), audit S11 copié ; RESTÉ à dessein :
  dossier v6 (copie archive existante), copies octet-identiques,
  2 oauth_token_relais.json (signalés, jamais imprimés) ;
  preuves-samu (hors /test) non touché ; API 403 PATCH combiné
  trashed+parents → deux PATCH (untrash puis move) — consigné
- FRONTIÈRES : arbres scellés intouchés ; 0.5.0 D104 intact (md5
  2b6481a1…) ; 0.5.1 fb41697d… revérifié dans le zip v8 ; aucune clé ;
  corbeille non vidée ; aucun artefact touché
- CONSIGNATION : JOURNAL_TRAVAIL.md +Entrée 128 (PAR SCRIPT AVANT le
  marqueur m5a, ordre 126<127<128<marqueur recoupé) ; DECISIONS.md
  +D143 (après D142) ; worklog +Task ID 46 (le présent) ; bundle
  nouveau nom triade-history-051-<tip>.bundle (D141), l'ancien 051
  archivé versionné dans archives-bundles ; miroir journal/decisions/
  worklog recoupés md5
- SUITE : 0.6.0 — étape 2 du M5 : INTERCEPTION D'UN FLUX NAVIGATEUR en
  VM isolée (relèvement amont http→https, D135 ; intentions
  http-08:R3/http-10:R3/http-12:R2 écrites-avant-code) ; le run v8
  verrouille le décor (parefeu muet) pour toutes les vagues ; D139
  reste ouvert (T7 éventuel), non bloquant

Stage Summary:
- Le décor des vagues à venir est verrouillé : le parefeu de la VM est
  rendu muet dès l'ouverture (section 0bis v8 — plus d'invite, tout
  trafic du kit autorisé avant le premier bind, état consigné à
  parefeu-vm.txt), la règle D143 met l'archivage de fin de run au
  registre et l'a appliquée au run v7 (preuves-run-v7 + vagues v6/v7
  archivées, preuves-m5b vierge), et la corbeille a été purgée de son
  passé TRIADE par RESTAURATION dans l'archive (runs v2/v4/v5, vagues
  v3–v5, terrain-17, audit S11) — rien n'est jeté sans copie versionnée.


## Task ID 47 — Run v8 : verdict OK 0 réserve, parefeu muet prouvé, D143 appliquée (03/11)

- RAPATRIEMENT : 30 pièces par id du dossier coffre preuves-m5b (id
  1OgqAnt2Pk5yXXnd-gfVyZ5SPYulNdA1b), 30/30 CONFORMES par taille
  (rapatrier_preuves_v8.py) ; run 2026-11-03T04:56–04:57Z, VM
  9687CE78-D5CF-4 — distinct de v7 (D99) ; pièce NOUVELLE parefeu-vm.txt
  (835 o) ; empreinte du scellé consignée par le run : proxy 0.5.1
  fb41697d… == le kit livré, racine v5 86525998… intouchée
- VERDICT : M5-b étape 1 — OK, 0 réserve. RUN A : 200 OK 452 o (279
  servis) + « tunnel chiffre etabli » + arret propre sur la LIGNE ; RUN
  B : page-b.txt 34 octets EXACTS vérifiés octet par octet (sha
  3355f352… == temoin) + « certificat rejete » (g70008/g70009) ; réserve
  POIGNEE-B-REFUSEE LEVÉE sur autorite-b.log (2 poignées refusées +
  arret propre) ; PROXY-ARRET quit code 0 ; matrice curl IDENTIQUE 3e
  fois (rc=60/0/60/60 — un rc=60 prouve le TCP connecté) ; T6/D139 :
  Dnscache RUNNING, HOSTS-IGNORE ECHEC — D139 demeure OUVERT non
  bloquant
- PAREFEU MUET PROUVÉ EN RUN : 4 DIAG-PAREFEU PASS aux PREMIÈRES lignes
  du journal (04:56:39Z) AVANT tout bind — règles ALLOW TRIADE-M5B ×2 +
  inboundusernotification off + parefeu-vm.txt (835 o : trois profils
  ACTIFS — le parefeu n'est PAS coupé, refus consigné) ; AUCUNE
  signature de blocage (rc=7/28, 10060/10061 absents) ; D142 passe de
  « condition de run consignée » à « condition MAÎTRISÉE, prouvée par
  pièce »
- D143 APPLIQUÉE (1re clôture PAR LA RÈGLE) : preuves-run-v8 (31
  entrées = 30 pièces + VERDICT-run-v8-parefeu-muet.txt, md5 recoupé)
  dans archives-preuves ; preuves-m5b recréé VIERGE ; index mis à jour
  EN PLACE ; le vierge préparé avant dépôt (1TAIGoTW…) resté en
  corbeille à dessein (consigné à l'index) ; racine /test = 8 entrées
  recoupées
- FRONTIÈRES : arbres scellés intouchés ; 0.5.0 D104 intact (md5
  2b6481a1…) ; 0.5.1 fb41697d… = artefact exact ; aucune clé ; corbeille
  non vidée ; aucun artefact touché
- CONSIGNATION : JOURNAL_TRAVAIL.md +Entrée 129 (PAR SCRIPT AVANT le
  marqueur m5a, ordre 126<127<128<129 recoupé) ; worklog +Task ID 47
  (le présent) ; bundle nouveau nom triade-history-051-<tip>.bundle
  (D141), l'ancien 721ace3 archivé versionné dans archives-bundles ;
  miroir journal/worklog recoupés md5
- SUITE : 0.6.0 — interception d'un flux NAVIGATEUR en VM isolée
  (relèvement amont http→https, D136/m5/I/README.md ; http-08:R3,
  http-10:R3 + ligne de flux, CLI --relever-https → R3) ; décor
  parefeu-muet verrouillé pour toutes les vagues ; D139 ouvert (T7
  éventuel), non bloquant

Stage Summary:
- Le run v8 rentre un deuxième verdict OK consécutif (0 réserve) avec
  le proxy 0.5.1 INCHANGÉ : la chaîne décisive est stable, la réserve
  POIGNEE-B-REFUSEE se lève encore sur pièce host, et le parefeu muet
  v8 est prouvé EN RUN (4/4 PASS avant tout bind, profils Actifs,
  parefeu-vm.txt aux preuves). D143 fait sa première clôture toute
  seule : preuves-run-v8 + verdict dans l'archive, preuves-m5b vierge.
  Le décor est prêt pour 0.6.0 (interception navigateur).


## Task ID 48 — Build 0.6.0-dev.1 : le flux navigateur embarqué et câblé (03/11)

- REPRISE SUR DÉPÔT (le contexte de session était perdu) : les intentions
  D136 (m5/I/README.md + les TROIS specs R3), le plan (m5/layout.py), les
  notations finales (377/2703/779 o — 2e réarrêt D8 pour http-10:R3) et
  DEUX harnais (cible, session) posés par la session interrompue ; le
  TROISIÈME harnais, l'oracle étendu et le passage du builder manquaient —
  chaque pièce relue depuis le dépôt avant d'écrire (T5 : citer, jamais
  recopier)
- HARNais_PRINCIPAL_R3.PY (NOUVEAU) : V1 round-trip R3 + les deux ancêtres
  scellés ; V2 différentiel R2/R3 sans argument (14 scénarios — traces
  identiques sauf LE CÂBLAGE 0x74C0 → 0x81C0 + GCLW normalisé ; divergence
  .text4 nommée : R2 nominal, R3 KO) ; V2bis LA CLI (19 cas dirigés, le
  modèle de parsing écrit depuis la spec — drapeau sain → armé + ligne
  « relever-https arme », tout autre argument → refus ExitProcess 3 sans
  initialisation, l'état .data compris) ; V3 fuzz des DEUX portes (400
  mutations, zéro passage silencieux) + fuzz CLI (300 lignes) ; V4 ONZE
  mutations stables en taille TOUTES ATTRAPÉES + témoin — BILAN 79 PASS
  0 ÉCHEC (graines 20261103/20261104)
- ORACLE_M5.PY (NOUVEAU — le cœur D136) : executer(blobs, graine, volume) ;
  F1 relevée à volume (200 cas, politique armée : routée Q2' port 443
  FORCÉ E2, gardes 501/411 la ligne porte le verdict nommé, 400/HTTP://
  sans ligne — le refus précède le routage ; la ligne OCTET PAR OCTET
  contre le MODÈLE DE COMPOSITION : méthode PAR TABLE, hôte tronqué à 14,
  v = le verdict tls TRANSPORTÉ, e/s les compteurs P8 — les relais
  délégués jamais comptés) + concordance avec la feuille (modele_cible,
  le 5e argument) ; F2 domaines hérités (150 cas : Q7 à volume — R2 émulé
  référence, octet pour octet, aucune ligne — puis politique 1 : les
  octets au client ceux de l'ancêtre ÉMULÉ, la ligne seule composée ;
  l'issue de la connexion amont propriété du générateur) ; F3 les TREIZE
  mutations attrapées + le modèle falsifié (ligne maquillée) NOMMÉ + témoin
  — BILAN 365 cas 0 écart (graines 20261103/424242)
- BUILD_M5.PY COMPLÉTÉ : SIX écarts de câblage nommés par l'oracle
  fail-closed un par un — (1) chemins d'import M4 ; (2) la liste RIP de
  http-10:R3 sans R_TAB_METHODES (I9) ; (3) celle de http-12:R3 visant
  ENTREE_M5 au lieu de LA SESSION 0x81C0 ; (4) la sentinelle -1 rendue
  0xffffffffffffffff par capstone (deux graphies admises) ; (5) les
  descripteurs hérités au plan M3 + NumberOfSections 6 + SizeOfCode
  vestige ; (6) la version 0x00060000 jamais écrite + la tranche .data +
  la preuve R7 excluant le delta version documenté (l'arbitrage de la
  preuve M4) ; ordre d'import des oracles consigné (build_m4 laisse
  sys.modules["layout"] = plan M4, les oracles s'y lient AVANT le plan M5)
- BUILD VERT : sceau-I 5 arbres conformes (clé réelle hors-ligne D87) ;
  héritage M3+M4 re-vérifié (524+492 verrous) ; l'image M4 == le scellé
  0.5.1 OCTET POUR OCTET (fb41697d… — prouvé par les runs v7/v8) ;
  structurel M5 312 verrous ; PE 36 352 o, 6 sections, .text4, kernel32
  x10 + GetCommandLineW, entrée 0x8C80, version 0x00060000, portes M5
  (fail-closed, la porte se garde elle-même) ET R10 (28 entrées) marchées ;
  R7 : 38 blocs octet-identiques, deltas documentés ; oracles M4 560 cas
  + M5 365 cas verts ; --verifier re-validé ; PROXY.EXE 0.6.0-DEV.1
  sha256 4b8f6af6caedb3e17811e6e25da1f1680068866bd1b417154fc54474170ec236
- FALSIFIABILITÉ CONSTATÉE (leçon D82) : l'arme creuse du V4 session
  (scénarios armés rejoués à politique 0 — échec garanti) FILTRÉE ; le
  fuzz-CLI a produit une fois le drapeau exact (casse tombée sur un trait
  d'union) — ATTRAPÉ par l'assertion d'intention, le générateur ne vise
  plus que les lettres
- FRONTIÈRES : arbres scellés intouchés ; 0.5.0 D104 intact ; 0.5.1
  fb41697d… revérifié par la preuve R7 ; 0.6.0-dev.1 NON scellé (la carte
  génération 7 attend la cérémonie D87) ; aucune clé ; aucun artefact
  scellé touché
- CONSIGNATION : JOURNAL_TRAVAIL.md +Entrée 130 (PAR SCRIPT AVANT le
  marqueur m5a, ordre 129<130<marqueur recoupé) ; worklog +Task ID 48 (le
  présent) ; bundle triade-history-060-<tip>.bundle (D141 : version au
  nom), l'ancien 051 archivé versionné, miroir recoupé md5
- SUITE : cérémonie de signature du développeur (D87 — clé hors-ligne,
  carte génération 7, conformité_profil), puis kit VM ÉTAPE 2 (navigateur
  du bac à sable, mandataire 127.0.0.1:25000, page http://autorite.test/
  sous --relever-https) et run M5-b étape 2 — le critère (b) : la page
  servie ET la 502 « Certificat rejete » PAR LE NAVIGATEUR, la ligne de
  flux aux preuves ; décor parefeu-muet v8 verrouillé ; D139 ouvert (T7
  éventuel), non bloquant

Stage Summary:
- Le jalon 0.6.0 est CONSTRUIT au laboratoire : les trois révisions R3
  (le verdict 5 sous politique, le routage Q2' + la ligne de flux, la CLI
  --relever-https + la porte M5) sont assemblées, harnaisées (cible 13
  PASS, session 34 PASS, principal 79 PASS) et jugées par l'oracle à
  scénarios étendu D136 (365 cas verts, falsification détectée) ; le
  proxy.exe 0.6.0-dev.1 (sha256 4b8f6af6…) reprend l'héritage scellé
  0.5.1 octet pour octet (38 blocs, preuve R7) avec les deltas .text4/
  .rdata/PE documentés ; six écarts de câblage du builder ont été nommés
  par l'oracle fail-closed lui-même et réparés. L'artefact attend la
  cérémonie de signature (D87) puis le terrain (run M5-b étape 2 — le
  navigateur).

## Task ID 49 — Synchro Drive+git vérifiée : le geste 3 de la passation D141 enfin effectif (03/11)

- DEMANDE DU DÉVELOPPEUR (consignée fidèlement) : « fais moi une synchro
  drive et git, je ne sais pas s'ils sont à jour » — vérification PAR PIÈCE
  avant tout geste, puis réparation de l'unique écart trouvé.
- ÉTAT CONSTATÉ : git local propre (HEAD 4faaf10) ; hook post-commit rc=0
  sur les deux derniers commits ; drive_sync.py rejoué : 815 inchangés,
  0 erreur ; kit Cérémonie OK ; canonique 060 au miroir md5 2bb725ef… ==
  locale ; archives-bundles/ : 5 bundles ; UN ÉCART : /test 9 entrées au
  lieu de 8 (D143) — la copie du bundle 060 y subsistait.
- ENQUÊTE : copie /test (id 1beZpC6I…, créée 17:38:08Z) et canonique
  miroir (id 1SRM35nG…, 17:40:19Z) = DEUX fichiers, md5 identiques ; le
  rejeu de passe_bundle_060.py a refusé sur son état 0 (l'ancien 051 déjà
  archivé) — gestes 1-2 effectifs, seul le geste 3 manquait.
- CAUSE RACINE (5e instance du piège PATCH, par preuve API) : l'en-tête
  Content-Type manquant — Drive IGNORE un corps non déclaré et répond 200
  sans effet ; la graphie ?trashed=true (leçon trop large du commit
  4faaf10) est tout aussi inopérante ; capabilities : canTrash=True (le
  droit jamais en cause) ; la graphie qui marche : corps {"trashed":
  true} AVEC Content-Type. Règle corrigée : trashed au corps DÉCLARÉ,
  parents en requête, jamais combinés (403 du run v7). Un 200 Drive ne
  prouve rien : toute mutation recoupée par relecture (D12 étendu).
- GESTE RÉPARÉ : copie /test corbeillée (trashed=true constaté PAR
  L'API) ; /test = 8 entrées D143 exactes ; canonique intacte ; corbeille
  non vidée. Re-vérification complète : 13/13 OK.
- OUTILS : scripts/retirer_bundle_test_060.py (geste 3 seul, idempotent,
  protections identiques à passe_bundle_060.py) ; JOURNAL_TRAVAIL.md
  +Entrée 131 (par script, ordre 130<131<marqueur recoupé).
- FRONTIÈRES : aucune suppression définitive, aucun bundle d'archive
  touché, arbres scellés intouchés, aucune clé, aucun artefact.
- SUITE : inchangée — cérémonie D87 (clé hors-ligne, carte génération 7,
  conformité_profil), kit VM ÉTAPE 2, run M5-b étape 2 (le navigateur).

---
## Task ID 50 — Kit de cérémonie déposé dans /Cérémonie à la demande du développeur (03/11)

- DEMANDE DU DÉVELOPPEUR (consignée fidèlement) : « fais moi un kit pour
  la cérémonie que tu mettras dans le drive /Cérémonie » — le geste est
  un rejeu VÉRIFIÉ du déploiement canonique D130 (scripts/maj_kit.py),
  pas une réinvention ; état constaté AVANT tout écrit.
- ÉTAT CONSTATÉ (recyclage du disque labo entre les sessions) : zone
  download/ AMPUTÉE — les 5 LISEZMOI de cérémonie absents (les copies
  plates ceremonie_gui/hors_ligne présentes, datées 17:37) ; git HEAD
  cdfabb6 propre à un bruit de bits de mode (7 fichiers, 0 insertion /
  0 suppression ; proxy.exe md5 72cf8fdd… == HEAD, sha256 4b8f6af6… =
  le 0.6.0-dev.1 attendu) — reset --hard (précédent Task 39) ; le hook
  post-commit avait DÉJÀ déployé le kit au commit cdfabb6
  (.gdrive/last_sync.log 18:21:39Z, rc=0 miroir + rc=0 kit).
- PIÈGE IDENTIFIÉ AVANT LE GESTE : un rejeu de maj_kit.py depuis un labo
  amputé aurait régénéré un MANIFESTE.txt SANS les 5 LISEZMOI (entrées
  optionnelles absentes localement = « conservé tel quel côté Drive ») —
  le manifeste n'aurait plus couvert le kit RÉEL : divergence
  silencieuse d'attestation, jamais d'échec nommé.
- GESTE (1) — RAPATRIEMENT : scripts/recuperer_lisezmoi_ceremonie.py
  (labo, hors dépôt, canal drive_sync) télécharge les 5 LISEZMOI du kit
  Drive → download/, md5 comparé AUX MÉTADONNÉES Drive : 5/5 MATCH
  (même geste que la récupération post-recyclage Task 39).
- GESTE (2) — DÉPÔT CANONIQUE : python3 scripts/maj_kit.py → gardes
  vertes (42 fichiers v06/ suivis par git + 9 racine requis), 57 entrées
  attendues, 0 téléversés, 1 mis à jour (MANIFESTE.txt régénéré — commit
  de référence cdfabb6, les 5 LISEZMOI de nouveau couverts), 56
  inchangés, 57/57 VÉRIFIÉS aller-retour md5 ; recoupement indépendant
  par la sonde : 15 entrées racine + v06/ (42 fichiers).
- INFRA : bundles-*/ ajouté au .gitignore — « zone de travail locale,
  jamais committée » (Entrée 131) devient une règle MÉCANIQUE, le
  git add -A de sync_backup.sh ne peut plus avaler un bundle (14,8 Mio).
- POST-SCRIPTUM (même session, 18:55) — PUSH GITHUB NOMMÉ EN ÉCHEC :
  l'échec « non bloquant » de sync_backup.sh a été ENQUÊTÉ, pas subi —
  cause : dans ce labo restauré, origin pointe vers un BUNDLE LOCAL
  (upload/triade-history.bundle, lecture seule), pas vers GitHub ;
  un bundle ne reçoit pas de push, la divergence n'est pas une panne
  réseau. Les canaux durables sont TOUS VERTS et recoupés : commit local
  c0bc66f ; miroir Drive TRIADE-sauvegarde-git 6/6 fichiers commités
  MATCH md5 (recoupement par relecture, scripts/recoupement_miroir_
  c0bc66f.py) ; bundle canonique au miroir inchangé ; le bilan « 818
  inchangés » du second drive_sync (non-quiet) est la PREUVE par
  relecture que le hook silencieux a porté les 8 fichiers. Le push
  GitHub réel exigera de reconfigurer origin vers l'URL du miroir
  GitHub privé (décision du développeur — les credentials ne traversent
  jamais le labo).
- PASSATION : JOURNAL_TRAVAIL.md +Entrée 132 (PAR SCRIPT, insertion
  ASSERTÉE, ordre 131<132<marqueur recoupé, rejeu REFUSÉ fail-closed) ;
  scripts/inserer_entree_132.py (contrat des entrées 127-132) ; worklog
  +Task ID 50 (le présent).
- FRONTIÈRES : aucun secret dans le kit (sceau-I/ = preuves publiques) ;
  aucune suppression côté Drive (maj_kit.py prudent, idempotent) ;
  /test intacte (8 entrées D143) ; arbres scellés intouchés ; aucune clé
  traversée ; aucun artefact touché.
- SUITE : inchangée — cérémonie de signature du développeur (D87 : clé
  hors-ligne, carte génération 7, conformité_profil à écrire), kit VM
  ÉTAPE 2 (le navigateur du bac à sable) et run M5-b étape 2 (critère
  (b) de D136) ; D139 demeure ouvert (T7 éventuel), non bloquant.

Stage Summary:
- Le kit de cérémonie (D130) est DÉPLOYÉ ET VÉRIFIÉ dans /Cérémonie
  (57/57 md5 aller-retour, MANIFESTE au commit cdfabb6, LISEZMOI
  reconstitués au labo) ; le geste demandé est EFFECTIF, rejouable et
  entretenu à chaque commit par le hook post-commit.
- Suite : inchangée — cérémonie D87, kit VM ÉTAPE 2, run M5-b étape 2.

---
## Task ID 51 — Paquet de cérémonie 0.6.0 livré dans /test + canal GitHub reconfiguré (04/11)

- DEMANDE DU DÉVELOPPEUR (consignée fidèlement) : « tu peux pas me faire
  comme pour la cérémonie v7 ? tu m'avais fait un zip avec le script de
  cérémonie en python, un document à signer, je mettais mon fichier de
  clé privée et ça produisais un document signé que je te donnais après »
  + « reconfigure origin pour le git push en echec ».
- PRÉCÉDENT V7 RELU (pièce à pièce) : a-signer.txt 10 lignes (1 neuve
  m4/0.5.1) + ceremonie_hors_ligne.py (autonome, autotest RFC 8032,
  signature auto-vérifiée) + LISEZMOI (signer hors ligne, rendre
  signatures-I.txt dans /test).
- ÉTAT DU SCEAU AVANT LE GESTE : 10 arbres verts, m5 HORS du sceau ;
  build_m5.py le nommait : « l'arbre m5 porte les révisions R3
  écrites-avant-code (D136) — sa signature appartient à la cérémonie
  0.6.0 ».
- LE PÉRIMÈTRE NE GRANDIT QUE SIGNÉ (modèle D126) : sceau_I.py ARBRES +
  m5 (proxy.exe relevement https, 0.6.0) ; v06/I/README.md § 1 « Onze
  arbres » + ligne m5 — la re-signature de v06 évite la contrebande X2
  (un code qui signe onze arbres sous une spec qui en nomme dix).
  preparer : remise 11 lignes ; état pré-cérémonie EXACT — 9 verts
  identiques, m5 CODE 12 (1869422e…), v06 CODE 10 (a8166442…).
  GEL : m5/I/ et v06/I/ figés jusqu'au retour de la remise.
- CHAÎNE PROUVÉE DEUX FOIS : (1) copie minimale /tmp/test-sceau —
  signer-test (clé TEST, jamais sur le dépôt réel) → verifier 11 VERTS
  code 0 ; (2) le paquet lui-même — clé JETABLE, 11/11 TOUT VERT,
  artefacts détruits (clé privée jetable comprise), zip 3 entrées
  AUCUNE clé, 9 232 o.
- LIVRAISON : paquet-ceremonie-0.6.0.zip + LISEZMOI-ceremonie-0.6.0.txt
  dans /test (point de reprise historique), md5 recoupés par relecture
  2/2 ; /test = 10 entrées (8 vague v8 + 2 nouvelles, aucune
  suppression) ; canal scripts/livrer_paquet_ceremonie_060.py.
- GITHUB RECONFIGURÉ : cause racine Task 50 (origin = bundle LOCAL en
  lecture seule) ; mécanique authentique retrouvée (check_auth.py +
  Entrée 0 : credential helper .gdrive/git-credentials 600) ; token_git
  rapatrié du dossier Drive « Tokens » (93 o, JAMAIS affiché), API /user
  200 (alexisfrlopez-debug), origin → github.com/alexisfrlopez-debug/
  triade.git ; CONSTAT : les ONZE commits du jalon (07d392e…cd85d8a)
  n'avaient JAMAIS été poussés ; poussée bundle051/v0.5.1-jalon-v7 à
  cd85d8a (recoupé ls-remote), main INTACT f62711b (la fusion du jalon
  = décision de clôture du développeur).
- PASSATION : JOURNAL_TRAVAIL.md +Entrée 133 (PAR SCRIPT, ordre
  132<133<marqueur, rejeu REFUSÉ fail-closed) ; scripts/inserer_entree_
  133.py ; scripts/assembler_paquet_ceremonie_060.py, livrer_paquet_
  ceremonie_060.py, reconfigurer_origin_github.py (labo, hors dépôt).
- FRONTIÈRES : clé réelle jamais traversée ni affichée ; 9 arbres
  signés INCHANGÉS (mêmes empreintes) ; aucun artefact scellé touché ;
  dépôt réel en état pré-cérémonie (clé déposée réelle intacte) ;
  .keys/ toujours absent du labo (scellage carte génération 7 = geste
  dédié à proposer après la remise).
- SUITE : signatures-I.txt attendu dans /test → deposer → verifier (11
  arbres verts) → ARBRES_GARDE_M5 += m5 → carte génération 7 → kit VM
  ÉTAPE 2 → run M5-b étape 2 (critère (b) de D136) ; D139 ouvert (T7
  éventuel), non bloquant.

Stage Summary:
- La cérémonie 0.6.0 est PRÊTE POUR LE DÉVELOPPEUR : paquet déposé dans
  /test (11 lignes à signer : m5 l'entrée + v06 la re-signature, 9
  inchangées), chaîne prouvée deux fois, aucune clé dans le paquet.
- GitHub rebranché : les 11 commits du jalon enfin poussés (branche
  dédiée, main intact) — sync_backup pousse de nouveau pour de vrai.
- Suite : attendre signatures-I.txt dans /test, puis deposer → verifier
  → carte génération 7 → kit étape 2 → run M5-b étape 2.
## Task ID 52 — Cérémonie 0.6.0 consommée : onze arbres verts, m5 à la garde (04/11)

- DEMANDE DU DÉVELOPPEUR (consignée fidèlement) : « c'est signé » —
  signatures-I.txt rendu par le chat (1 564 o, md5 a2b34831…, 11 lignes
  CRLF — la machine Windows du geste).
- CONTRÔLES SANS CLÉ avant tout geste : 11 lignes ; balises == a-signer.txt
  ligne à ligne (diff vide) ; 9 signatures héritées OCTET POUR OCTET
  identiques aux déposées (Ed25519 déterministe — même clé réelle) ;
  m5 sans signature déposée (attendu) ; v06 divergente (attendu).
- CANAL DURABLE : remise poussée dans /test du Drive (md5 MATCH par
  relecture, /test = 11 entrées, aucune suppression).
- CONSOMMATION : sceau_I.py deposer → 11 signatures installées (manifestes
  vivants), clé réelle INTACTE (D87, sans rotation — la même clé signe la
  nouvelle intention, spec § 5) ; verifier → ONZE arbres VERTS code 0 :
  m5 = 1869422e… (neuve attendue), v06 = a8166442… (re-signée attendue) ;
  écrits = signatures+m5.txt, manifestes/m5.txt (nouveaux), v06 (mis à
  jour), 9 paires inchangées, a-signer.txt inchangé (git status le prouve).
- GESTE POST-CÉRÉMONIE (nommé par la passation Task 51) : ARBRES_GARDE_M5
  += m5 (build_m5.py, commentaire historisé) → garde VERTE d'un coup
  (6 arbres m0-m5, clé réelle) ; re-vérification complète --verifier
  TOUTE VERTE : oracles 524 + 312 verrous, différentiels M4 560 + M5 365
  cas verts, R7 38 blocs réutilisés du scellé 0.5.1, PE proxy.exe
  0.6.0-dev.1 re-validé (4b8f6af6… inchangé) ; [carte] génération 7 :
  cérémonie requise — les secrets ne vivent pas au labo.
- HONNÊTETÉ DES ÉTIQUETTES : test_sceau_I.py T3-g + [final] comptaient
  « 10 arbres » en dur (ère v7) — contrôle juste, étiquette fausse par
  sous-état : compte dynamique len(ARBRES) → 51 PASS / 0 ÉCHEC, [final]
  « VERT (11 arbres) ». Labo recyclé : dépendances build réinstallées
  (capstone, keystone, pefile, pynacl, unicorn).
- PASSATION : JOURNAL_TRAVAIL.md +Entrée 134 PAR SCRIPT (ordre
  133<134<marqueur, rejeu REFUSÉ fail-closed) ; scripts/inserer_entree_
  134.py.
- FRONTIÈRES : clé privée jamais vue ni demandée (remise = signatures
  seules, 11 × 128 hex) ; clé publique déposée inchangée (173fae9c…) ;
  9 arbres signés inchangés ; aucun artefact scellé touché ; .keys/
  toujours absent du labo.
- SUITE : scellage carte génération 7 (geste OPÉRATEUR à proposer — les
  secrets de la carte ne vivent pas au laboratoire) → kit VM ÉTAPE 2
  (navigateur du bac à sable, mandataire 127.0.0.1:25000, page
  http://autorite.test/ sous --relever-https) → run M5-b étape 2
  (critère (b) de D136 : la page servie ET la 502 « Certificat rejete »
  PAR LE NAVIGATEUR) ; D139 ouvert (T7 éventuel), non bloquant.

Stage Summary:
- La cérémonie 0.6.0 est CONSOMMÉE : le sceau porte onze arbres verts
  (m5 entré, v06 re-signée), la même clé réelle — la chaîne d'intention
  M0-M5 est intégralement signée pour la première fois.
- La garde du build M5 est verte (6 arbres) et la re-vérification
  complète passe : la voie est libre pour le scellage carte génération 7,
  geste opérateur (les secrets ne vivent pas au labo).
- Suite : proposer le scellage carte génération 7, livrer le kit VM
  ÉTAPE 2, puis le run M5-b étape 2 (critère (b) de D136).

## Task ID 53 — « répare la 0.5.1 » : carte m4 génération 6 orpheline NOMMÉE et RE-SCELLÉE sous lignée D80 ; graine de signature DURABLE au coffre (D144) ; branche GitHub complétée (04/11)

Task: demande du développeur « répare la 0.5.1 » — diagnostic enchaîné puis
réparation de la carte du scellé 0.5.1, consignation Entrée 135 + D144.

Work Log:
- REPRISE DU TRAVAIL INTERROMPU (session précédente morte à ~21:40) : ses
  gestes relus et repris — poussée des 2 commits de cérémonie à la branche
  GitHub (21:12, ls-remote : bundle051/v0.5.1-jalon-v7 == a5035e1, main
  INTACTE f62711b) ; coffre CF1 rapatrié + importé (.keys/) + phrase
  lignee-D80 extraite (21:17-21:18, scripts/rapatrier_coffre_cf1.py).
- DIAGNOSTIC (preuves enchaînées, rien d'hypothétique) : la carte m4
  génération 6 (scellé 0.5.1, posée à da68021 le 03/11 03:29) a une
  signature Ed25519 VALIDE mais ses fragments NE se déchiffrent PAS avec
  la lignée D80 ; la MÊME phrase déchiffre m3 génération 5 ET la carte m4
  D104 (8c280d5) — la carte du jalon v7 est sous une autre clé. CAUSE
  RACINE : le labo du jalon v7 était un clone du bundle (D140), .keys/
  gitignoré n'y vivait pas ; carte_m0.charger_secrets a GÉNÉRÉ phrase +
  graine aléatoires ; _anti_rollback a passé SILENCIEUSEMENT (« pas de
  carte lisible ») ; construire() ne lit jamais l'ancienne carte → carte
  0.5.1 scellée sous secrets éphémères morts avec la sandbox ; le churn
  de pub (f40f8a20 → ad98a059) n'était pas consigné. Conséquences : verrou
  anti-rollback de la 0.5.1 MORT (passe silencieusement à tout labo),
  verrou croisé R8 inexécutable, promesse du coffre fausse pour cette
  carte. Vestige constaté : stash « etat-partiel-d140 » (07:05) —
  brouillons supersédés par da68021, CONSERVÉ.
- RÉPARATION (scripts/reparer_carte_051.py, 23 s, modèle D80 à faits
  inchangés) : 7 gardes fail-closed (artefact fb41697d… intact ; phrase
  D80 PROUVÉE par témoins croisés m3-g5 + m4-D104 ; orpheline authentique
  pub ad98a059… ; non-déchiffrable en D80 ; garde sceau-I verte ; sceau
  11 verts ; coffre Drive joignable md5 0323029a… == local) PUIS la
  machinerie EXACTE du build : verrous 524+492, image re-composée ==
  scellé OCTET POUR OCTET (proxy.exe PAS réécrit), oracle D93 re-joué
  (560 cas verts, graine 20261104, verdict 1e04996b…), fragments_clairs
  (49 blocs, version 0.5.1, compteurs 1/10), scellement sous D80 vérifié
  EN MÉMOIRE (signature, racine, déchiffrement, verrou croisé 38/38)
  avant l'unique écriture ; verrou croisé disque 49 empreintes ; tableau
  régénéré (seule change la graine de l'oracle : 20261104).
- GRAINE DURABLE (D144) : neuve (pub e9cd8c549485…) déposée AU COFFRE —
  entrée TRIADE/graine-ed25519-cartes (octets bruts 32 o, relève :
  obtenir --vers-fichier .keys/ed25519.seed) ; conteneur 1158 → 1906 o,
  md5 23a2987a9817…, racine Drive recoupée par RELECTURE, export
  download/ ; entrées lignee-D74/D80 INTACTES (listing 3 entrées) ;
  scripts/rapatrier_coffre_cf1.py suivi (attestation 23a2987a…, 1906 o).
- POST-VÉRIFICATIONS : P1 carte LISIBLE en D80 (frag-bld version=0.5.1,
  empreinte fb41697d…) ; P2 LE VERROU ANTI-ROLLBACK REFUSE (« carte
  scellée (0.5.1) : reconstruction interdite ») — le défaut même est
  mort ; P3 sceau ONZE verts après le geste ; P4 proxy.exe intact ;
  écrits : les 8 fichiers m4/carte/ et rien d'autre côté dépôt.
- PASSATION : JOURNAL_TRAVAIL.md +Entrée 135 PAR SCRIPT (ordre
  134<135<marqueur, rejeu REFUSÉ fail-closed) ; DECISIONS.md +D144 ;
  scripts/reparer_carte_051.py, inserer_entree_135.py ;
  reparation_carte_051.log (gitignoré, le vol complet).
- FRONTIÈRES : artefact 0.5.1 octet pour octet inchangé ; arbre m4/I et
  sceau intouchés (onze verts avant/après, clé réelle jamais sollicitée) ;
  orpheline conservée à l'historique git (da68021) ; coffre : aucune
  entrée perdue ; stash conservé ; aucune suppression Drive ; .keys/
  gitignoré (phrase + graine relèvables du coffre à tout labo).
- SUITE : scellage carte génération 7 (geste développeur, désormais
  exécutable : les deux secrets sont durables au coffre) ; kit VM
  ÉTAPE 2 ; run M5-b étape 2 (critère (b) de D136). D139 ouvert, non
  bloquant.

Stage Summary:
- La 0.5.1 est RÉPARÉE : sa carte génération 6 vit sous la lignée D80 du
  coffre (lisible, verrou croisé exécutable), le verrou anti-rollback
  REFUSE une reconstruction (preuve P2), l'artefact fb41697d… n'a pas
  bougé d'un octet, et la graine de signature est enfin DURABLE (entrée
  coffre, D144) — plus jamais orpheline aux recyclages.
- Suite : proposer le scellage carte génération 7 au développeur, kit VM
  ÉTAPE 2, run M5-b étape 2.
## Task ID 54 — « lance le scellage » : carte génération 7 SCELLÉE à 0.6.0-rc.1 — machinerie M5 écrite (modèle D104), cristallisation 52/52 × 10/10, artefact 4b8f6af6… inchangé, finale 0.6.0 en attente du critère (b) (04/11)

Task: demande du développeur « lance le scellage » — le geste développeur
attendu (D87/D144) : sceller la carte génération 7 du proxy 0.6.0.

Work Log:
- BALISE TRANCHÉE AVANT TOUT GESTE : 0.6.0-rc.1 (candidate), PAS la finale
  — le critère (b) de D136 (navigateur en VM) n'est pas prouvé ; table des
  versions du protocole : rc.N = candidate soumise à la validation terrain,
  X.Y.Z = validation consignée ; plan m5 : « la balise 0.6.0 est posée à la
  validation terrain » ; modèle D104 (rc.1 puis finale après 17-H).
- MACHINERIE ÉCRITE (trois écritures, modèle D104) : m5/carte_m5.py
  (génération 7, charger_secrets FAIL-CLOSED — D144 appliqué au code :
  aucune génération de secret au labo, relève au coffre nommée) ;
  m5/conformite_profil.py (§ 8.2 M5 : 58 contrôles, les DEUX portes
  constatées VIVANTES, oracle D136 jalon) ; build_m5.py porté
  (fragments_clairs 52 blocs/6 artefacts, construire_carte, verrou_croise
  R8, tableau_de_bord, _anti_rollback, --sceller-rc/--sceller-final) ;
  layout VERSION_RC1/VERSION_FINALE.
- CONSTRUCTION : chaîne entière re-vérifiée (524+492+312 verrous ; image M4
  == scellé 0.5.1 OCTET POUR OCTET ; oracles 560+365 cas verts) ; carte
  génération 7 NÉE (lignée D80, graine durable pub e9cd8c549485…, 52
  blocs, 6 artefacts, R8 52 empreintes, tableau) ; proxy.exe OCTET POUR
  OCTET == témoin pris avant le geste (4b8f6af6…).
- CRISTALLISATION : construire 1/10 puis NEUF --verifier (graines
  20261104…20261112, oracles complets à chaque passage, R8 à chaque
  passage) → 52/52 blocs à 10/10, dix runs datés consignés au frag-prf.
- SCELLAGE --sceller-rc : garde sceau 6 arbres (clé réelle) ;
  cristallisation exigée et constatée ; conformité § 8.2 VERTE exécutée
  par le scellage (58 contrôles) ; bascule dev.1→rc.1 UNE occurrence
  fail-closed ; re-chiffrement + signature graine durable ; vérification
  EN MÉMOIRE avant l'unique écriture (listes blanches, signature, racine,
  bascule re-déchiffrée) ; tableau suivi ; R8 post 52 empreintes ;
  artefact re-vérifié == 4b8f6af6….
- POST-VÉRIFICATIONS : P1 carte LISIBLE lignée D80 (frag-bld
  version=0.6.0-rc.1, empreinte 4b8f6af6…, signature valide, 52/52 à
  10/10) ; P2 anti-rollback REFUSE (« carte scellée (0.6.0-rc.1) :
  reconstruction interdite ») ; P3 sceau ONZE arbres VERTS (m5:
  1869422e… intact) ; P4 artefact == témoin.
- HONNÊTETÉ DES CONSTATS : deux erreurs de la conformité née (comparaison
  hexdigest vs préfixe sha16 ; indexes tuples BLOCS_REVISIONS_M5) et un
  seuil d'ombres ABI copié du 0.5.0 (la trame tls-05:R2 0x98 de D140 vit
  en imm32) — nommées et réparées PAR les échecs de la suite elle-même,
  AVANT le scellage.
- PASSATION : JOURNAL_TRAVAIL +Entrée 136 PAR SCRIPT (ordre
  135<136<marqueur, rejeu REFUSÉ fail-closed), scripts/inserer_entree_136.py.
- FRONTIÈRES : artefact 4b8f6af6… inchangé ; sceau et arbres signés
  intouchés (m5/I aucun changement, onze verts avant/après) ; cartes
  m0/m3/m4 intactes ; .keys/ gitignoré, aucun secret dans les écrits ;
  finale 0.6.0 NON posée (elle attend la validation terrain — la carte ne
  ment pas) ; aucune suppression.
- SUITE : kit VM ÉTAPE 2 (navigateur du bac à sable, mandataire
  127.0.0.1:25000, http://autorite.test/ sous --relever-https) ; run M5-b
  étape 2 (critère (b) de D136) ; si vert : --sceller-final pose 0.6.0
  (l'exigence est déjà écrite au code). D139 ouvert, non bloquant.

Stage Summary:
- La carte génération 7 VIT : scellée 0.6.0-rc.1 sous la lignée D80 et la
  graine durable du coffre (D144), lisible, verrouillée (anti-rollback
  vivant, R8 52 empreintes), l'artefact n'a pas bougé d'un octet — et la
  finale attend honnêtement le navigateur du critère (b).
- Suite : kit VM étape 2, run M5-b étape 2, puis --sceller-final si vert.
## Task ID 55 — « ok pour la suite » : LE KIT VM ÉTAPE 2 LIVRÉ AU COFFRE — la vague e2 (le flux NAVIGATEUR, critère (b) de D136) sur le proxy 0.6.0-rc.1 ARMÉ --relever-https ; base v8, 55 entrées, reprises assertées ; D143 appliquée (vague v8 + cérémonie 0.6.0 archivées) ; la finale 0.6.0 attend le run terrain (04/11)

Task: « ok pour la suite » — la suite consignée à l'Entrée 136 : kit VM
ÉTAPE 2 (navigateur du bac à sable, mandataire 127.0.0.1:25000, page
http://127.0.0.1/ — IP littérale D139 — sous --relever-https), puis run
M5-b étape 2 (critère (b) de D136), puis --sceller-final si vert.

Work Log:
- REPRISE SUR DÉPÔT (contexte de session perdu) : HEAD fe94417 (scellage
  carte génération 7, 0.6.0-rc.1) ; arbre propre au bruit de bits de mode
  près (12 fichiers, diff 0/0, phénomène connu et consigné) ; sceau_I.py
  verifier AVANT tout geste : ONZE arbres VERTS code 0 (m5 = 1869422e…),
  cle deposee reelle — le scénario vit dans m5/vm/, HORS de l'arbre m5/I
  signé, aucune signature ne peut bouger.
- LA VAGUE v8 RAPATRIÉE DU COFFRE (le coffre fait foi) : m5b-kit-v8.zip +
  scenario-m5b-v8.ps1 + LISEZMOI-m5b-v8.txt + corriger-wsb.* téléchargés
  PAR ID, md5 recoupés (kit 3986421f…) ; l'état /test constaté : 11
  entrées (vague v8 + cérémonie 0.6.0 consommée + remise signatures) ;
  le kit extrait et relu pièce à pièce (fixtures v5 SAN DNS+IP, racine
  86525998…, autorite_test.py, client v5, wsb, python 3.12.10) ; le
  scénario v8 relu ENTIER (614 lignes — 0bis parefeu, Attendre-Port,
  Verdict-Vue D138, matrice curl, branche S1-S4, témoin D99).
- LES ATTENDUS EXACTS tirés des sources (jamais devinés) : la ligne de
  flux du MODÈLE DE COMPOSITION (harnais_session_r3.ligne_flux : « flux
  » + méthode + hôte + «:» + port + « v= » + verdict + « e= » + « s= »)
  → aiguilles « flux GET 127.0.0.1:443 v=0 » / « v=3 » ; l'armement
  « relever-https arme » (http-12:R3 Q3/I2 : UNE fois, entre bannière et
  écoute) ; la 502 héritée 34 o SANS corps (Q3' — Edge rend SA page
  d'erreur, l'aiguille DOM est « 502 », aucun locale n'écrit le chiffre
  autrement) ; CONNECT REJETÉ 501 (http-08:R2 — si la montée https
  d'Edge se déclenchait malgré les drapeaux, le repli aboutit, trace
  v=501 additive au journal).
- LE SCÉNARIO e2 ÉCRIT (m5/vm/scenario-m5b-e2.ps1, BOM + CRLF, 805
  lignes, structure v8 + sections navigateur) : Edge localisé par sondes
  (x86, PF, App Paths, PATH — REFUS NAVIGATEUR-ABSENT) ; version au
  témoin (DIAG-EDGE-VERSION, additive) ; invocation headless --dump-dom
  (décisif) + --screenshot (additif) par run, profils NEUFS,
  --proxy-server=127.0.0.1:25000 + --proxy-bypass-list="<-loopback>"
  (retire la dérivation de boucle implicite de Chromium) +
  --disable-features=HttpsUpgrades,HttpsFirstBalancedModeAutoEnable,
  HttpsFirstModeEnabled ; proxy ARMÉ --relever-https par cmd /c (capture
  NATIVE, modèle v8) avec l'armement CONSTATÉ sous 20 s AVANT le
  navigateur (REFUS PROXY-SANS-ARMEMENT) ; autorités A/B PAR DÉLAI
  (150 s — le compte de requetes navigateur est inconnu, jamais
  --arret-apres N) ; verdicts DOM-A-MARQUEUR / DOM-B-502 +
  DOM-B-SANS-PAGE (Verdict-Vue D138 : vue vide + rc=0 = RÉSERVE) ;
  FLUX-A-V0 / FLUX-B-V3 ; décor v8 entier rejoué (0bis parefeu, hosts +
  sonde D139, empreintes, matrice curl additive — branches recalibrées :
  S4 attendue, S3 = régression à nommer —, T6 Dnscache, témoin D99 en
  dernier acte) ; équilibrage des délimiteurs vérifié PAR SCRIPT (156/156
  accolades, 88/88 crochets, 474/474 parenthèses) ; le labo n'a NI
  Windows NI PowerShell : le scénario est RELU, pas exécuté — les risques
  CONSIGNÉS au LISEZMOI (modèle v8, la lignée v2→v8 a prouvé que ce qui
  casse se nomme au premier lancement).
- L'ASSEMBLAGE (scripts/assembler_kit_e2.py, modèle assembler_kit_v7 —
  Task 43) : base = kit v8 LIVRÉ ; DEUX pièces remplacées (proxy.exe
  0.5.1 fb41697d… → 0.6.0-rc.1 4b8f6af6… 36 352 o, asserté avant/après ;
  scenario v8 → e2, BOM + CRLF assertés) + DEUX documents (LISEZMOI-KIT
  e2, LISEZMOI-preuves e2) ; 51 reprises ASSERTÉES par md5 ; intégrité du
  zip re-vérifiée à la sortie (testzip, proxy relu == 4b8f6af6…) ;
  m5b-kit-e2.zip 11 191 067 o, md5 76e7b02f8c922981dbdc64fb34c6f679 ;
  vérification par extraction de contrôle (55 entrées, wsb == v8,
  autorite_test.py == v8, racine == 86525998…).
- LA LIVRAISON D143 (scripts/livrer_vague_e2.py — chaque mutation
  RECOUPÉE PAR RELECTURE, D12 étendu) : vague v8 consommée archivée
  (LISEZMOI + scenario + kit) ; cérémonie 0.6.0 consommée archivée
  (paquet + LISEZMOI + signatures-I.txt RENOMMÉE signatures-I-0.6.0.txt —
  la remise 0.5.1 vit déjà au même nom à l'archive) ; vague e2 posée
  (kit + scenario octet-identique au kit + LISEZMOI-terrain) ;
  preuves-m5b/LISEZMOI-preuves passé à la liste e2 ; index des archives
  mis à jour (relu) ; ÉTAT FINAL : racine /test = EXACTEMENT 8 entrées
  D143 {vague e2 ×3, corriger-wsb ×2, preuves-m5b, archives-livraisons,
  archives-preuves}.
- PASSATION : JOURNAL_TRAVAIL.md +Entrée 137 PAR SCRIPT (ordre
  136<137<marqueur, rejeu REFUSÉ fail-closed) ; scripts/assembler_kit_
  e2.py, livrer_vague_e2.py, inserer_entree_137.py suivis (le dépôt
  porte le kit source — la dette des assembleurs v6-v8, jamais commis,
  est nommée ici) ; worklog +Task ID 55 (le présent).
- FRONTIÈRES : artefact 0.6.0-rc.1 4b8f6af6… inchangé (le kit l'EMBARQUE,
  l'assertion d'assemblage le prouve) ; sceau onze verts avant/après
  (m5/I signé INTACT) ; cartes m0/m3/m4/génération 7 intactes ; fixtures
  v5 inchangées ; aucune clé réelle (test jetables) ; aucune suppression
  Drive (archivage) ; finale 0.6.0 NON posée (elle attend le verdict
  terrain) ; le bruit de bits de mode préexistant n'est pas commis.
- SUITE : LE GESTE TERRAIN — télécharger m5b-kit-e2.zip depuis /test,
  extraire dans un dossier NEUF, corriger-wsb.bat, double-clic du
  scenario-m5b.wsb (~5-8 min), renvoyer TOUT preuves-m5b (liste au
  LISEZMOI-preuves et en dernière ligne du témoin) ; SI vert :
  python3 m5/build_m5.py --sceller-final pose 0.6.0 avec la validation
  consignée. D139 ouvert (T7 éventuel), non bloquant.

Stage Summary:
- La vague e2 VIT au coffre /test : le kit VM ÉTAPE 2 (proxy 0.6.0-rc.1
  ARMÉ, scénario Edge headless par le mandataire, décor v8 verrouillé)
  attend le double-clic du développeur — LE critère (b) de D136 : la
  page servie ET la 502 « Certificat rejete » RECUES PAR LE NAVIGATEUR,
  la ligne de flux aux preuves.
- Suite : le run M5-b étape 2 par le terrain ; si vert, --sceller-final
  pose la finale 0.6.0.

---
Task ID: 56
Agent: Z.ai (agent principal)
Task: run e2 — « preuves déposées dans le drive /test, mais je pense que
le run n'est pas tout vert » : rapatrier, juger sur pièces (D138),
clôturer D143, consigner le verdict et la correction.

Work Log:
- LABO RÉCUPÉRÉ AVANT TOUT : le dépôt local était PÉRIMÉ à a5035e1
  (recyclage après la Task 55 — origin portait 4580164/fe94417/9b3544d :
  réparation 0.5.1 D144, scellage carte génération 7 rc.1, kit e2 livré)
  ; fast-forward origin recoupé ; bruit de bits de mode neutralisé
  (core.fileMode=false, rien commis).
- PIÈCES RAPATRIÉES (preuves-m5b, 6/6 md5 MATCH par relecture) :
  scénario exécuté == dépôt == /test == zip (e06db6c0…) ; empreintes
  consignées PAR LE RUN : proxy 4b8f6af6… == 0.6.0-rc.1 scellé.
- VERDICT : ÉCHEC NOMMÉ REFUS PROXY-SANS-ARMEMENT (00:13:37Z, ligne
  finale du journal du scénario) — le navigateur n'a JAMAIS été lancé,
  le critère (b) de D136 n'est PAS tranché. LE SCELLÉ EST INNOCENT :
  proxy-journal.log (128 o) porte « relever-https arme » ; la sonde TCP
  (00:13:17) prouve l'écoute posée, donc l'armement DÉJÀ écrit (Q3 :
  bannière → armement → écoute) ; le quit post-REFUS a opéré (« arret »
  ×2) ; autorité A cohérente (1 poignée refusée SSLEOF = la sonde 443,
  0 requête servie, arret propre par délai 150 s à 00:15:46).
- CAUSE RACINE NOMMÉE : la garde en live lit un fichier encore ouvert —
  0 o lu à 00:13:37, les 7 lignes n'apparaissent qu'après la MORT du
  proxy (WriteFile direct par ligne, tcp-11 Q1). MÊME symptôme que les
  « vues vides » v7/v8 (D138) ; le v8 ne lisait le journal proxy qu'en
  post-mortem : la garde en live du e2 était la régression. « commande
  inconnue » = décor (présente au journal du run v8 VERT, même place).
- CLÔTURE D143 FAITE : preuves-run-e2 (6 pièces + VERDICT-run-e2-vues-
  vides.txt, md5 recoupés) aux archives-preuves ; preuves-m5b recréé
  VIERGE ; index mis à jour EN PLACE ; racine /test inchangée (8
  entrées) ; aucune suppression. Le script archiver_run_e2.py est
  REPRISE-CAPABLE (premier passage interrompu mi-chemin : upload_create
  exige un Path — corrigé, état final recoupé par relecture).
- PASSATION : JOURNAL_TRAVAIL +Entrée 138 PAR SCRIPT (ordre
  137<138<marqueur, rejeu REFUSÉ fail-closed) ; DECISIONS +D145 (après
  D144, ordre recoupé) ; scripts/rapatrier_preuves_e2.py,
  rapatrier_journal_v8.py, rapatrier_vagues_m5b.py, lister_drive.py,
  rapatrier_index_archives.py, archiver_run_e2.py, inserer_entree_138.py,
  inserer_d145.py.
- FRONTIÈRES : le scellé 0.6.0-rc.1 sans défaut constaté (armé, écouté,
  arrêté proprement) ; artefact/carte génération 7/sceau (onze verts)
  intouchés ; finale 0.6.0 NON posée (elle attend un run VERT) ;
  fixtures v5 inchangées ; aucune clé ; aucune suppression Drive.
- SUITE : sur l'aval du développeur — la vague e3 (garde d'armement
  FONCTIONNELLE : sonde « GET http://127.0.0.1/ » au mandataire, 200
  attendu de l'autorité A ; RELEVER-ARME en verdict post-mortem ; Edge
  version par VersionInfo), run rejoué, si vert --sceller-final. D139
  ouvert, non bloquant.

Stage Summary:
- Le run e2 dit un refus de décor, pas un verdict navigateur : le
  scénario a été piégé par la première garde en live d'un fichier vivant
  (« vues vides », D145 désormais) ; le scellé 0.6.0-rc.1 s'est armé et
  arrêté proprement — la carte ne ment pas.
- Suite : vague e3 (garde fonctionnelle + verdicts post-mortem) à
  construire sur l'aval du développeur, puis le run rejoué ; si vert,
  --sceller-final pose la finale 0.6.0.
## Task ID 57 — « go pour reconstruire le kit e3 » : LA VAGUE e3 CONSTRUITE ET LIVRÉE — la correction D145 appliquée au scénario (garde d'armement FONCTIONNELLE : la sonde forme-absolue reçoit la page 200 de l'autorité ; RELEVER-ARME post-mortem ; Edge par VersionInfo) ; le scellé 0.6.0-rc.1 n'a pas bougé d'un octet ; kit e3 au coffre /test, vague e2 archivée (04/11)

- DEMANDE DU DÉVELOPPEUR (consignée fidèlement) : « go pour reconstruire
  le kit e3 » — l'aval nommé par la SUITE de la Task 56 (Entrée 138).
- PRÉALABLE AU GESTE : le labo était PÉRIMÉ à a5035e1 (recyclage après la
  Task 56) — fast-forward depuis origin (142fc44, recoupé ls-remote),
  reset --hard pour le bruit de bits de mode (précédent Task 39), git
  propre ; les pièces du run e2 rapatriées À NEUF (rapatrier_preuves_e3.py,
  7/7 conformes, miroir download/preuves-run-e2/) — le verdict relu AVANT
  d'écrire la correction.
- LE SCÉNARIO e3 (m5/vm/scenario-m5b-e3.ps1) : ONZE remplacements ancrés
  ASSERTÉS (construire_scenario_e3.py, R1–R11) — tout le décor e2/v8
  repris octet pour octet (BOM+CRLF, 852 lignes) ; TROIS corrections
  (Entrée 138) : la garde d'armement FONCTIONNELLE (Sonde-Armement : « GET
  http://127.0.0.1/ » au mandataire, la page 200 de l'autorité A attendue
  — statut + marqueur TRIADE-M5B-PAGE-200 — pièce page-sonde-armement.txt
  toujours posée, REFUS PROXY-PAS-ARME sinon avec l'extrait de réponse),
  RELEVER-ARME en VERDICT POST-MORTEM (après le quit, modèle v8 — plus
  aucune lecture en live d'un fichier vivant), DIAG-EDGE-VERSION par
  (Get-Item).VersionInfo + pièce edge-version.txt ; l'honnêteté des
  étiquettes : AUTORITE-A-SERVIE / TUNNEL-A / FLUX-A-V0 nomment la sonde
  dans leurs détails (elle est servie, tunnelise et produit une ligne v=0
  — le décisif navigateur reste le DOM).
- LA RÉPONSE ATTENDUE DE LA SONDE EST PROUVÉE AVANT LE RUN : oracle D136
  F1 (200 cas, octets au client octet par octet), pièce page-a.txt du run
  v8 (le même tunnel — « HTTP/1.1 200 OK » + page), le marqueur ne vit
  que dans la page de l'autorité ; le refus d'un non-armé est prouvé par
  F2 (origine port 80 muette : 502).
- L'ASSEMBLAGE (assembler_kit_e3.py) : base kit e2 LIVRÉ (md5 76e7b02f…
  recoupé), LE PROXY N'EST PAS REMPLACÉ — égalité base == dépôt ASSERTÉE
  (4b8f6af6… : la correction touche le scénario, jamais le scellé) ;
  3 pièces remplacées (scénario + LISEZMOI-KIT + LISEZMOI-preuves e3),
  52 reprises assertées ; m5b-kit-e3.zip 11 192 711 o md5 981b1a5b… ;
  intégrité re-vérifiée à la sortie PUIS vérification disque indépendante
  (kit-e3-verif/, 16/16).
- LA LIVRAISON (livrer_vague_e3.py, mutations RECOUPÉES PAR RELECTURE) :
  vague e2 consommée ARCHIVÉE (3 fichiers → vagues-m5b/, md5 recoupés) ;
  vague e3 POSÉE (m5b-kit-e3.zip + scenario-m5b-e3.ps1 + LISEZMOI-m5b-
  e3.txt, md5 distants == locaux) ; preuves-m5b/LISEZMOI-preuves.txt →
  liste e3 (LES DEUX PIÈCES NOUVELLES y vivent — la liste « e3 == e2 » de
  l'Entrée 138 est corrigée de ce que la correction ajoute) ; index des
  archives mis à jour (bloc « vague e2 consommée ») ; racine /test =
  EXACTEMENT 8 entrées D143.
- PASSATION : JOURNAL_TRAVAIL +Entrée 139 PAR SCRIPT (ordre 138<139<
  marqueur, rejeu REFUSÉ fail-closed) ; scripts suivis :
  construire_scenario_e3.py, assembler_kit_e3.py, livrer_vague_e3.py,
  inserer_entree_139.py, rapatrier_preuves_e3.py ; m5/vm/scenario-m5b-
  e3.ps1 + LISEZMOI-terrain-m5b-e3.txt suivis.
- FRONTIÈRES : le scellé 0.6.0-rc.1 (4b8f6af6…) SANS UN OCTET BOUGÉ ;
  carte génération 7 et sceau (onze arbres verts) INTACTS ; arbres
  scellés intouchés ; fixtures v5 inchangées ; finale 0.6.0 NON POSÉE
  (elle attend un run VERT) ; aucune clé ; aucune suppression Drive ;
  corbeille non vidée.
- SUITE : LE GESTE TERRAIN — m5b-kit-e3.zip depuis /test, dossier NEUF,
  corriger-wsb.bat, double-clic scenario-m5b.wsb (~5-8 min), renvoyer
  TOUT preuves-m5b (page-sonde-armement.txt et edge-version.txt
  comprises) ; le critère (b) de D136 PAR LE NAVIGATEUR ; si vert :
  m5/build_m5.py --sceller-final pose la finale 0.6.0. D139 ouvert, non
  bloquant.

Stage Summary:
- La vague e3 est au coffre : la garde d'armement est fonctionnelle (la
  sonde reçoit la page 200 de l'autorité par le mandataire), les verdicts
  de journal sont post-mortem, la version d'Edge se lit par VersionInfo —
  et le scellé 0.6.0-rc.1 n'a pas bougé d'un octet.
- Suite : le run e3 au terrain (le critère (b) de D136 par le navigateur) ;
  si vert, --sceller-final pose la finale 0.6.0.
## Task ID 58 — Passation D141 rejouée à la livraison e3 : bundle courant 060-193b8d4 au miroir, ancien archivé, dette des six commits fermée ; GitHub à 193b8d4 (04/11)

- GESTE : la passation D141 n'avait plus été rejouée depuis 07d392e (SIX
  commits de jalon, deux recyclages — l'ère 051 tenait une passation par
  livraison) : triade-history-060-193b8d4.bundle (git bundle --all,
  15 128 008 o, md5 0eef6b2b…) construit, la branche jalon du bundle
  ASSERTÉE sur 193b8d4 (git bundle list-heads — le bundle porte la
  livraison e3 AVEC sa consignation), déposé au miroir (md5 MATCH par
  relecture) ; l'ancien 060-07d392e (md5 2bb725ef… recoupé AVANT) ARCHIVÉ
  VERSIONNÉ dans archives-bundles/ (déplacement par paramètres de requête,
  jamais supprimé) ; /test sans copie de bundle (recoupé) ; état final :
  LE courant unique à la racine du miroir, SIX archives.
- CANAUX : GitHub porté à 193b8d4 (push, recoupé ls-remote) — les trois
  canaux durables alignés (miroir de fichiers, bundle versionné, GitHub) ;
  le hook post-commit a fait son œuvre sur 193b8d4 (miroir rc=0, kit
  Cérémonie rc=0 — .gdrive/last_sync.log).
- PASSATION : JOURNAL_TRAVAIL +Entrée 140 PAR SCRIPT (ordre 139<140<
  marqueur, rejeu REFUSÉ fail-closed) ; scripts suivis :
  passe_bundle_e3.py, inserer_entree_140.py.
- FRONTIÈRES : aucune suppression (l'archivage est un déplacement) ;
  /test INTACT (8 entrées D143) ; aucune clé (le bundle --all suit le
  dépôt, .keys/ gitignoré) ; scellé 0.6.0-rc.1 et carte génération 7
  INTACTS.
- SUITE : inchangée — LE GESTE TERRAIN (m5b-kit-e3.zip, dossier NEUF,
  corriger-wsb.bat, double-clic, renvoyer TOUT preuves-m5b) ; si vert,
  --sceller-final pose la finale 0.6.0. D139 ouvert, non bloquant.

Stage Summary:
- Les trois canaux durables sont alignés sur la livraison e3 : fichiers
  au miroir, bundle versionné 060-193b8d4, branche GitHub — la dette de
  passation (six commits) est nommée et fermée.
- Suite : le run e3 au terrain ; si vert, la finale 0.6.0 est posée.
## Task ID 59 — Run e3 analysé sur pièces, reproduit au labo, cause racine nommée : LE RVA NU DE LA LIGNE DE FLUX (crash du proxy 0.6.0-rc.1 à la première requête routée) ; clôture D143, règle D146, chemin de réparation proposé (04/11)

- GESTE (l'analyse) : les preuves du run e3 rapatriées du coffre /test
  (rapatrier_run_e3.py, 8/8 md5 conformes) — le run s'arrête à la garde
  d'armement (RIEN reçu, MethodInvocationException immédiate) MAIS la
  pièce proxy-journal.log porte « relever-https arme » : l'étiquette
  REFUS PROXY-PAS-ARME est démentie, la signature (pas de fin connexion,
  quit sans effet, autorité vierge, mort instantanée) désigne la MORT du
  processus à la PREMIÈRE requête routée jamais envoyée au binaire.
- GESTE (la reproduction) : harnais full-PE unicorn (reproduire_run_e3.py,
  modèle emulation_forensique D52h — base préférée 0x140000000, IAT marchée
  par les 4 descripteurs, ligne de commande réelle, fils coopératifs,
  séquence terrain exacte) : le journal capté reproduit le journal réel
  LIGNE POUR LIGNE jusqu'à la mort, puis faute à http-10:R3+0xA46
  (movzx eax, byte [r12], r12 = 0x24A0 — RVA nu hors image).
- CAUSE RACINE : la ligne de flux (code NOUVEAU 0.6.0 — le 0.5.1 ne
  contient pas la chaîne « flux ») lit le couple (RVA, longueur) de la
  table des méthodes et passe le RVA NU à la copie — l'idiome hérité
  http-02 (dword + base d'image) a été PERDU. Toute requête routée tue
  le rc.1. Les oracles étaient verts parce que TOUTE l'émulation M5 vit
  à base 0 (le RVA nu y résout par accident) — règle D146 : contrôle
  d'exécution À LA BASE RÉELLE avant tout scellage.
- PREUVE CHIRURGICALE : le correctif simulé au crochet (rdx = base + rdx)
  fait disparaître le crash et renaître TOUTE la chaîne — ligne de flux
  « flux GET 127.0.0.1:443 v=6 e=51 s=40 » (port 443 forcé par le
  relèvement), getaddrinfo, connect 443, réponse ENVOYÉE au client.
- CLÔTURE D143 (archiver_run_e3.py, mutations recoupées par relecture) :
  7 pièces + VERDICT-run-e3-rva-nu.txt vers archives-preuves/preuves-run-e3/
  (11 entrées), preuves-m5b recréé VIERGE (liste e3 — vaut pour e4 : le
  scénario e3 est repris tel quel), index mis à jour EN PLACE, racine /test
  inchangée (8 entrées), aucune suppression.
- PASSATION : JOURNAL_TRAVAIL +Entrée 141 PAR SCRIPT (ordre 140<141<
  marqueur, rejeu REFUSÉ fail-closed), DECISIONS +D146 PAR SCRIPT (à la
  suite de D145), scripts suivis : lister_preuves_e3_run.py,
  rapatrier_run_e3.py, reproduire_run_e3.py, archiver_run_e3.py,
  inserer_entree_141.py, inserer_d146.py.
- FRONTIÈRES : le scellé 4b8f6af6… INTACT (lu en émulation, jamais
  écrit) ; carte génération 7, sceau ONZE arbres, scellé 0.5.1, fixtures
  v5, m5/I, scénario e3 et kit e3 au coffre INTACTS ; .keys/ absent ;
  la finale 0.6.0 TOUJOURS NON POSÉE ; D139 ouverte non bloquante.
- PASSATION D141 (passe_bundle_analyse_e3.py, modèle passe_bundle_e3.py) :
  le bundle courant triade-history-060-5da81b0.bundle (15 166 127 o, md5
  cc18759e…, branche jalon ASSERTÉE sur l'analyse e3) déposé au miroir,
  l'ancien 060-193b8d4 (md5 0eef6b2b…) ARCHIVÉ VERSIONNÉ dans
  archives-bundles/ (7 archives) — la cadence « une passation par geste »
  est tenue, aucune dette ; /test sans copie de bundle (recoupé) ; GitHub
  porté à la pointe (push, ls-remote recoupé).
- SUITE (proposition, décision du développeur) : (1) notation
  http-10-session-r3 corrigée (idiome dword + base restauré — l'arbre
  m5/I ne change pas, le sceau-I m5 reste VALIDE, pas de nouvelle
  cérémonie) ; (2) contrôle d'exécution à la base réelle adjoint au
  corpus (D146) ; (3) rebuild → 0.6.0-rc.2 → scellage rc ; (4) kit e4
  (scénario e3 repris) → geste terrain → critère (b) de D136 ; si vert,
  --sceller-final pose la finale.

Stage Summary:
- Le run e3 a fait exactement ce pour quoi il était construit : la garde
  fonctionnelle a attrapé la mort du rc.1 AVANT le navigateur. La cause
  est nommée, reproduite et prouvée chirurgicalement : un RVA nu passé
  comme pointeur par la ligne de flux — invisible pour toute émulation à
  base 0 (règle D146).
- Suite : la décision du développeur sur le chemin rc.2 (notation corrigée
  + contrôle à la base réelle + kit e4) ; le critère (b) de D136 attend
  toujours son run.
## Task ID 60 — « continue chemin rc.2 » : LE CHEMIN ACCOMPLI — idiome http-02:R1 restauré dans la ligne de flux, contrôle D146 né en livrable du jalon (rc.1 KO / rc.2 VERT — falsifiabilité prouvée), cristallisation 52/52 × 10/10, SCELLÉ 0.6.0-rc.2 (c1e46fb0…, contrôle D146 exécuté AU scellage), kit e4 LIVRÉ au coffre /test (scénario e3 repris tel quel, proxy remplacé) ; D147 (04/11)

Task: demande du développeur « continue chemin rc.2 » (et confirmation du
état e3 : non, tout n'était pas vert — le proxy rc.1 crashait à la première
requête routée) — les quatre pièces du chemin proposé à l'Entrée 141,
exécutées et consignées.

Work Log:
- REPRISE DU LABO : dépôt restauré du bundle 060-5da81b0 (méthode A, arbre
  propre), jetons .gdrive/ posés (OAuth Drive VERT par check_auth), coffre
  CF1 importé (.keys/, md5 23a2987a… attesté D144), secrets relevés
  (lignee-D80 + graine ed25519-cartes, chmod 600) ; NOTE nommée : le
  PHRASE-CONTROLE-COFFRE.txt de la RACINE Drive porte 3 lignes (59 o) —
  sa ligne 1 EST la phrase courante, mais l'ouverture directe par
  --phrase-fichier échoue ; la copie du DÉPÔT (33 o, phrase seule, norme
  D81) ouvre le coffre — l'écart vit au dossier Drive racine, à corriger
  à la prochaine synchro (aucune mutation de ma part).
- (1) LE CORRECTIF DE NOTATION : le brouillon
  m5/notation/brouillons/http-10-session-r3.asm corrigé (zone Q6, lignes
  ~237-246) — l'idiome hérité http-02:R1 restauré : base d'image dérivée
  de l'adresse complète de TAB_METHODES (lea) moins son RVA (sub rdx,
  0x2410, sub 64 bits OBLIGATOIRE — la base tient sur 33 bits), puis
  add sur le RVA lu avant l'appel .copier ; CINQ instructions (+16 o),
  registres morts seuls, arithmétique recoupée (0x84f3+7-0x60ea=0x2410) ;
  auteur.py régénère : g80002 2719 o, padding 49→33 o, slot 2752 o
  inchangé, .copier glisse 0x8bf3→0x8c03 ; m5/I INTACT (le contrat Q6
  « méthode (texte R_TAB_METHODES) » est respecté PAR le correctif) —
  sceau-I valide, pas de cérémonie.
- (2) LE CONTRÔLE D146 EN LIVRABLE DU JALON (m5/controle_base_reelle.py,
  modèle reproduire_run_e3.py D52h) : image ENTIERE à la base réelle
  0x140000000, IAT marchée, ligne de commande réelle, fils coopératifs,
  séquence e3 exacte ; verdict fail-closed en trois pièces (pas de faute
  mémoire/la ligne de flux avec méthode en texte/le client servi) ;
  FALSIFIABILITÉ PROUVÉE : le rc.1 ÉCHOUE à l'identique du terrain
  (faute 0x24A0, http-10:R3+0xA46, movzx eax, byte [r12] — KO a/b/c) ;
  le dev.2 est VERT : « flux GET 127.0.0.1:443 v=6 e=51 s=40 » émis, 502
  nommée servie au client (poignée shimmée défaillante, frontière D146),
  getaddrinfo + connect 443, ExitProcess propre.
- (3) LES VERSIONS + L'AMENDEMENT D147 (modèle D35) : layout.py dev.2 /
  U64 0x00060001 / rc.2 ; anti-rollback amendé (LICENSE une entrée :
  exactement rc.1 → dev.2, motif Entrée 141) ; _sceller GAGNE l'exigence
  D146 MÉCANIQUE (contrôle base réelle AVANT la bascule de balise, refus
  non vert) ; SHA_PROXY_060_RC1 conservé (mémoire du fautif),
  SHA_PROXY_060_DEV2 posé après constat (c1e46fb0…).
- (4) LA CHAÎNE rc.2 : build dev.2 VERT (R5 541/541 sur g80002 corrigé,
  structurels 524+492+312, R7 image M4 == scellé 0.5.1 octet pour octet,
  oracles 560+365 cas verts, PE 36 352 o INCHANGÉ, carte gén. 7) ;
  CRISTALLISATION REPARTIE À ZÉRO : DIX passages (build + graines
  20261104→20261112), 52/52 × 10/10, sha stable ; SCELLAGE rc.2 : sceau-I
  6 arbres, contrôle D146 VERT AU SCELLAGE même, conformité § 8.2 VERTE
  (58 contrôles), bascule assertée, verrou croisé 52, proxy INTACT ;
  gardes constatées après : re-scellage REFUSÉ, reconstruction REFUSÉE —
  anti-rollback VIVANT.
- (5) LE KIT e4 (assembler_kit_e4.py) : base kit e3 LIVRÉ rapatrié du
  coffre (md5 981b1a5b… recoupé), TROIS remplacements (proxy rc.1 FAUTIF
  → rc.2 — égalité base == scellé fautif ASSERTÉE ; LISEZMOI-KIT e4 ;
  LISEZMOI-preuves e4), LE SCÉNARIO e3 REPRIS TEL QUEL (byte-identique,
  asserté deux fois — la garde D145 demeure), 52 reprises assertées ;
  m5b-kit-e4.zip 11 193 488 o md5 0922b281352c02b3ed25cf9a778ba664,
  intégrité re-vérifiée + VÉRIFICATION DISQUE INDÉPENDANTE (kit-e4-verif/,
  11 contrôles verts) ; m5/vm/ gagne scenario-m5b-e4.ps1 (copie) +
  LISEZMOI-terrain-m5b-e4.txt.
- (6) LA LIVRAISON D143 (livrer_vague_e4.py, tout recoupé par relecture) :
  vague e3 consommée ARCHIVÉE (3 pièces → vagues-m5b/, md5 avant/après) ;
  vague e4 POSÉE (kit + scénario + LISEZMOI, md5 distants == locaux) ;
  preuves-m5b → liste e4 ; index mis à jour (bloc e3 après e2) ; racine
  /test = 8 entrées, vague courante e4.
- CONSIGNATIONS : JOURNAL_TRAVAIL +Entrée 142 PAR SCRIPT (ordre
  141<142<marqueur, rejeu REFUSÉ fail-closed), DECISIONS +D147 PAR SCRIPT
  (à la suite de D146), ce worklog +Task ID 60 ; scripts suivis :
  rapatrier_kit_e3.py, assembler_kit_e4.py, livrer_vague_e4.py,
  inserer_entree_142.py, inserer_d147.py.
- FRONTIÈRES : le scellé rc.1 FAUTIF vit à l'historique git (jamais
  reconstruit ni réécrit) ; scellé 0.5.1, cartes m0-m4, sceau ONZE
  arbres, arbre m5/I, fixtures v5, scénario e3 : INTACTS ; aucune
  suppression Drive, corbeille non vidée ; .keys/ gitignoré ; D139
  ouverte non bloquante ; la finale 0.6.0 TOUJOURS NON POSÉE (elle attend
  un run VERT).
- SUITE : LE GESTE TERRAIN — m5b-kit-e4.zip depuis /test, dossier NEUF,
  corriger-wsb.bat, double-clic scenario-m5b.wsb (~5-8 min), renvoyer
  TOUT preuves-m5b (page-sonde-armement.txt et edge-version.txt
  comprises) — le critère (b) de D136 ; si vert :
  python3 m5/build_m5.py --sceller-final pose la finale 0.6.0.

Stage Summary:
- Le chemin rc.2 est ACCOMPLI : l'idiome perdu est restauré (cinq
  instructions, slot préservé), le contrôle D146 vit au jalon ET au
  scellage (le rc.1 y crashe, le rc.2 y sert — la falsifiabilité est
  prouvée sur le scellé fautif lui-même), la cristallisation est repartie
  à zéro et le 0.6.0-rc.2 est SCELLÉ avec le contrôle exécuté au geste
  même. Le kit e4 (scénario e3 repris tel quel, proxy corrigé) est au
  coffre /test.
- Suite : le geste terrain du run e4 — le critère (b) de D136 par le
  navigateur ; si le verdict est vert, --sceller-final pose la finale
  0.6.0 avec la validation consignée.

- PASSATION D141 rejouée au geste rc.2 : le bundle courant
  triade-history-060-9fa7fb3.bundle (git bundle --all, 15 311 490 o,
  md5 a7567812…) déposé au MIROIR, ASSERTÉ avant dépôt (branche jalon
  pointe sur 9fa7fb3 — il porte le chemin rc.2 AVEC sa consignation) ;
  l'ancien 060-5da81b0 (md5 cc18759e… recoupé AVANT) ARCHIVÉ VERSIONNÉ
  dans archives-bundles/ (8 archives, jamais supprimé) ; /test sans copie
  de bundle (recoupé) ; GitHub porté à la pointe dans le même geste
  (sync_backup : push, ls-remote recoupé) ; script suivi :
  passe_bundle_e4.py.

## Task ID 61 — « Preuves déposées dans le drive /test » : LE RUN e4 ANALYSÉ SUR PIÈCES — LE CRITÈRE (b) DE D136 PRÉSENT (page rendue au DOM au marqueur + capture ; 502 « Certificat rejete » REÇUE par le navigateur, réception triplement recoupée), LE CRASH e3 GUÉRI à la base réelle, les cinq refus du scénario levés sur pièces (D138), LA FINALE 0.6.0 SCELLÉE au geste même ; clôture D143 du run, D148 née (04/11)

Task: le développeur a déposé les preuves du run e4 au coffre /test (« Preuves
déposées dans le drive /test ») — le geste analyse : rapatrier, juger sur
pièces (D138), et si le critère (b) est présent, consigner la validation
terrain et poser la finale 0.6.0 (l'exigence était écrite au code et au
LISEZMOI terrain e4).

Work Log:
- (1) RAPATRIEMENT (lister_preuves_e4_run.py + rapatrier_preuves_e4.py,
  modèle e2, D99 zéro mélange) : 37 entrées à /test/preuves-m5b →
  download/preuves-run-e4/, 37/37 CONFORMES par md5. Run
  2026-11-04T12:06:43–12:12:21Z, VM 9687CE78-D5CF-4 (même machine que
  v7/v8/e2/e3). Artefact jugé : proxy.exe sha256 c1e46fb0… == 0.6.0-rc.2
  SCELLÉ (le kit n'a pas bougé — le libellé « kit e3/rc.1 » du témoin est
  le texte hérité du scénario e3 repris tel quel, la pièce juge le
  binaire) ; fixtures v5 intactes ; Edge 156.0.4314.58 (VersionInfo,
  pièce née).
- (2) L'ANALYSE SUR PIÈCES (VERDICT-run-e4-critere-b.txt) : le verdict du
  scénario « ÉCHEC NOMMÉ (5) » est un artefact d'instrument — (a) rc Edge
  capturé VIDE (capture ExitCode aveugle, D138 complément d'arrêt v6) →
  NAVIGATEUR-A/B faux échecs ; (b) verdicts EN LIVE sur journaux vivants
  → « vues vides » (D138/D145 : handle vivant = 0 octet, le journal
  flushe pourtant par ligne) et la branche RÉSERVE prévue (« producteur
  rc=0 ») EMPOISONNÉE par le rc Edge vide → AUTORITE-A-SERVIE et
  POIGNEE-B-REFUSEE faux échecs (les pièces post-mortem portent les
  aiguilles : « requete servie » ×5, « poignee de main refusee » ×3) ;
  (c) DOM-B vide PAR CONSTRUCTION : la 502 M5 est une ligne de statut
  nue (TXT_502_CERT 34 o, sans corps) → Chromium échoue la 5xx à corps
  vide avec ERR_HTTP_RESPONSE_CODE_FAILURE et le headless n'émet NI DOM
  NI CAPTURE (risque consigné d'avance au LISEZMOI terrain e4, juge
  remis au labo sur pièces).
- (3) LE CRITÈRE (b) PRÉSENT : moitié A — dom-a.txt 282 o au marqueur
  TRIADE-M5B-PAGE-200 (navigateur a reçu ET parsé, aucun autre chemin
  que le tunnel), nav-a.png 13 081 o (attesté par Edge), autorité A
  5 requêtes servies par le tunnel, flux v=0 ×3 ; moitié B — « certificat
  rejete » + flux v=3 e=736 s=34 ×2 (la 502-cert 34 o SERVIE au
  navigateur, dump-dom 12:09:20 + capture 12:09:24), poignée refusée ×3
  côté autorité, ERR_HTTP_RESPONSE_CODE_FAILURE ×2 côté navigateur —
  réception TRIPLEMENT recroisée, rendu non démontrable en headless
  (réserve instrumentale nommée). LE BUT DU rc.2 : la première requête
  routée qui tua le rc.1 a VÉCU — « flux GET 127.0.0.1:443 v=0 e=51 »,
  page-sonde-armement.txt NÉE (452 o, en-tête 200 + page au marqueur) ;
  l'idiome restauré tient à la base réelle sur Windows authentique.
- (4) MATRICE CURL == v8 OCTET POUR OCTET (pièces comparées archive à la
  main) : T2a rc=60 CERT_TRUST_REVOCATION_STATUS_UNKNOWN, T2b rc=0,
  T3 rc=60, T5 rejet — branche S3 = L'ÉTAT STATIONNAIRE du curl de la VM
  (v6/v8/e4) ; le libellé « RÉGRESSION à nommer » est une expectation
  périmée de l'ère e2 — D140 réparait les credentials du PROXY (preuve :
  le run A tunnelé hors ligne), jamais curl. D139 inchangée, T6 consigné.
- (5) LA FINALE 0.6.0 POSÉE : relève du secret carte (coffre INTÈGRE,
  lignee-D80 → .keys/passphrase.txt), python3 m5/build_m5.py
  --sceller-final — sceau-I ONZE arbres verts, CONTRÔLE D146 VERT
  EXÉCUTÉ AU SCELLAGE, cristallisation 52/52 × 10/10, conformité 58
  contrôles, bascule rc.2 → 0.6.0 (occurrence unique assertée), verrou
  croisé R8 52 empreintes, proxy.exe INTACT (c1e46fb0…, 36 352 o — le
  scellage est un fait de carte) ; GARDES CONSTATÉES : re-scellage
  REFUSÉ, reconstruction REFUSÉE (anti-rollback VIVANT sous 0.6.0).
- (6) CONSIGNATIONS : JOURNAL_TRAVAIL +Entrée 143 PAR SCRIPT (ordre
  142<143<marqueur), DECISIONS +D148 PAR SCRIPT (à la suite de D147 —
  verdicts post-mortem et sur pièces, témoin de producteur jamais un rc
  aveugle, preuve d'erreur à la réception, S3 stationnaire), ce worklog
  +Task ID 61 ; scripts suivis : lister_preuves_e4_run.py,
  rapatrier_preuves_e4.py, archiver_run_e4.py, inserer_entree_143.py,
  inserer_d148.py.
- (7) LA CLÔTURE D143 DU RUN e4 (archiver_run_e4.py) : les 37 pièces →
  /test/archives-preuves/preuves-run-e4/ + VERDICT-run-e4-critere-b.txt ;
  preuves-m5b recréé VIERGE (liste e4) ; index mis à jour EN PLACE ;
  racine /test = 8 entrées (la vague e4 DEMEURE courante — aucune vague
  e5, le jalon est rentré).
- FRONTIÈRES : la finale est un FAIT DE CARTE (l'artefact n'a pas bougé
  d'un octet) ; scellé 0.5.1, cartes m0-m4, sceau ONZE arbres, arbre
  m5/I, fixtures v5, scénario e3-==-e4 : INTACTS ; aucune suppression
  Drive, corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non
  bloquante.
- SUITE : le jalon M5 est RENTRÉ (balise 0.6.0, validation terrain
  consignée) — les jalons M6/M7 attendent leur plan ; la passation D141
  suit au même geste.

Stage Summary:
- Le run e4 est VERT sur pièces : le navigateur a reçu et rendu la page
  de l'autorité par le tunnel, et reçu la 502 « Certificat rejete » du
  certificat auto-signé — les deux dans le même run, le crash e3 guéri à
  la base réelle. Les cinq refus du scénario étaient des artefacts
  d'instrument (D138), levés un à un ; la matrice curl est identique au
  run v8 de référence.
- LA FINALE 0.6.0 EST SCELLÉE : le contrôle D146 exécuté au scellage,
  la carte basculée, les gardes vivantes. Le jalon M5 (le flux navigateur
  intercepté de bout en bout) est RENTRÉ.

- PASSATION D141 rejouée au geste « run e4 analysé / finale 0.6.0 » : le
  bundle courant triade-history-060-f425ceb.bundle (git bundle --all,
  15 384 065 o, md5 e9568bd7…) déposé au MIROIR, ASSERTÉ avant dépôt
  (branche jalon pointe sur f425ceb — il porte le jalon M5 RENTRÉ AVEC sa
  consignation : analyse sur pièces + critère (b) + finale 0.6.0 +
  clôture D143 + Entrée 143 + D148) ; l'ancien 060-9fa7fb3 (md5
  a7567812… recoupé AVANT) ARCHIVÉ VERSIONNÉ dans archives-bundles/
  (9 archives, jamais supprimé) ; /test sans copie de bundle (recoupé) ;
  GitHub porté à la pointe dans le même geste (push f7b460c..f425ceb,
  recoupé ls-remote) ; script suivi : passe_bundle_analyse_e4.py.
## Task ID 62 — « ok, on enchaine » : LE PLAN DES JALONS M6/M7 ÉCRIT — le programme M6/M7 ouvert (D149, quatre chantiers par jalon, critères mesurables, frontières nommées), les FICHES DE PROFIL COMPLÈTES nées AVANT le premier octet (x86-64-linux-elf64 et riscv64-linux-elf64, 7+1 éléments, constats labo DATÉS : keystone sans RISC-V / capstone RV64 OK / qemu absent), le statut M5 FRANCHI consigné au plan et à la spec, le chantier M5-(c) REPORTÉ au M6-(d) (explicite), l'écart D81 racine Drive FERMÉ (59 o→33 o, ouverture VERT) ; Entrée 144, D149 (04/11)

Task: demande du développeur « ok, on enchaine » — la suite annoncée au Task 61
était « les jalons M6/M7 attendent leur plan » : le geste écrit ce plan et referme
le reste nommé (l'écart D81 « à corriger à la prochaine synchro »).

Work Log:
- (0) REPRISE RECROUPÉE : dépôt propre à dc318f2 (pointe = passation e4), auth
  Drive VERT (check_auth), coffre /test recoupé 8 entrées D143 (vague e4 courante,
  le jalon rentré), .keys/coffre_fort.bin md5 23a2987a… (D144) intègre.
- (1) LE CADRE NORMATIF RELU AVANT D'ÉCRIRE : spec § 16 (les 7+1 éléments du
  profil, « jamais d'instanciation approximative »), § 8.2 (suite de conformité
  par profil — le critère d'acceptation explicite de M6/M7), § 8.3 (parité à
  contrat constant : même spec I, oracle mutualisé, différences documentées dans
  frag-con), § 18 (critères M6 : suite verte + diff nul + parité + même oracle ;
  M7 : round-trip 100 % + patch fence.i + verrou croisé + export multi-profils),
  plan § Universalité (M6 change l'OS à ISA constante, M7 change d'ISA — l'ordre
  isole chaque variable).
- (2) LE PATRIMOINE MESURÉ : le profil x86-64-linux-elf64 N'EST PAS une page
  blanche — l'échelle d'auto-hébergement D34 y vit (hachoir m6/ échelon 1 :
  ELF64 À LA MAIN [ehdr 64 o + 2 phdr, composer_elf], exécuté NATIVEMENT au
  labo, oracle différentiel FIPS 180-4 sur le terrain natif ; sceau m7/ échelon
  2 phase 1) ; CONSTAT DU WRITÉ EXISTANT : ET_EXEC à base fixe, 2 PT_LOAD, sans
  GNU_STACK/RELRO — le jalon monte en gamme (ET_DYN/PIE base aléatoire, trois
  segments R/RX/RW, PT_GNU_STACK sans X), l'écart est NOMMÉ dans la fiche ;
  l'AUDIT DE COUPLAGE des contrats : les pré/post m0/m1 portent le paramétrage
  msx64 (hello-02 : HANDLE/WriteFile/rcx ; libc-01 R1 : « rcx contient dst ») —
  la VOIE du diff nul est la RÉVISION DE GRANULARITÉ R+1 (arguments formels
  dans I, convention d'appel vers frag-con, § 8.3-4), invariance des octets
  Windows ASSERTÉE.
- (3) LES CONSTATS LABO DATÉS (faisabilité vérifiée AVANT d'écrire le plan) :
  keystone 0.9.2 n'a PAS KS_ARCH_RISCV (l'assemblage RISC-V n'existe pas dans
  la chaîne — un LIVRABLE du jalon M7, pas une surprise) ; capstone 5.0.7
  désassemble RV64 (constaté sur octets : addi décodé) ; qemu-riscv64 ABSENT du
  bac à sable (prérepos chantier M7-(a)) ; le bac à sable EST Linux x86-64
  (l'oracle du jalon M6 s'exécutera NATIVEMENT — plus fort que l'émulation
  full-PE du primaire).
- (4) LES DEUX FICHES DE PROFIL (docs/PROFIL_x86-64-linux-elf64.md,
  docs/PROFIL_riscv64-linux-elf64.md) : les 7+1 éléments chacune, ACQUIS vs À
  PRODUIRE distingués — SysV (zone rouge 128 o LE PIÈGE INVERSE, XMM tous
  volatils, 4e argument syscall par R10), syscalls −errno fail-closed (table
  ERRNOS miroir HRESULTS), patch mprotect + cohérence I-cache matérielle (SDM
  vol. 3 § 8.1.3) ; RV64IMA+Zifencei SANS C (instructions 4 o — choix assumé),
  psABI LP64 (AUCUNE zone rouge — le piège inverse de SysV), table asm-generic
  avec garde anti-table-x86 (write=1 = refus nommé : la parité est SÉMANTIQUE,
  jamais lexicale), séquence patch scratch+fence.i en sept gestes (portée du
  fence.i = cœur courant, mono-fil au jalon — frontière nommée), NOP canonique
  0x13 / garde ebreak, l'exécuteur qemu avec la RÉSERVE INSTRUMENTALE nommée
  (le noyau et les syscalls réels, l'ISA émulée — jamais déguisée).
- (5) LE PROGRAMME M6/M7 (PLAN_MILESTONES.md, section « ouvert le 04/11/2026,
  D149 ») : M6 (a) durcissement format + ERRNOS ; (b) corpus paritaire (audit
  A/B/C, révision de granularité, diff nul MESURÉ PAR SCRIPT, oracle m1 régénéré
  VERT sur l'instance Linux, parité § 8.3 par exécution) ; (c) suite de
  conformité (modèle m5) + scellage 0.7.0-rc.1 avec contrôle D146 ADAPTÉ
  (exécution full-ELF à la base réelle — l'image PIE au noyau, un pointeur nu
  y meurt comme sur le terrain) ; (d) LE PATCH EN PRODUCTION — le chantier
  M5-(c) refermé : tcp-07 instancié (mprotect) et EMBARQUÉ, bascule du journal
  PENDANT le trafic, rollback, zéro régression, kit terrain au coffre /test,
  run WSL2/VM, verdict sur pièces (D138/D145/D148) → finale 0.7.0. M7 (différé
  derrière M6) : (a) assembleur RV64 + qemu ; (b) la TROISIÈME instanciation
  de la même couche I ; (c) patch fence.i + verrou croisé multi-profils ;
  (d) export multi-profils aux CINQ étapes → finale 0.8.0. FRONTIÈRES NOMMÉES :
  corpus nominal M6 RESTREINT (le serveur écho complet de M2 est un chantier
  OUVERT, jamais une réduction silencieuse) ; TROIS décisions développeur
  attendues (terrain M6 : WSL2 recommandé / VM ; terrain M7 : qemu + réserve ;
  aval du report M5-(c)) — aucune ne bloque M6-(a). Convention de dossiers :
  unix/ (M6) et riscv/ (M7), m6/ et m7/ demeurent l'échelle D34.
- (6) LES CONSIGNATIONS D'ÉTAT : PLAN_MILESTONES préambule (chantier M5-(b)
  RÉALISÉ le 04/11 — critère (b) de D136 VERT sur pièces, JALON M5 FRANCHI ;
  (c) REPORTÉ), vue d'ensemble (ligne M5 franchie), tableau programme M5
  ((a)/(b)/(c) à jour) ; PROTOCOLE_TRIADE préambule (M0–M5 franchis, M6/M7
  ouverts) + § 18 (M5 franchi 04/11 balise 0.6.0 ; M6/M7 ouverts, fiches
  référencées) — le PDF v0.6.1 se régénère par le mécanisme D17/D134, empreinte
  consignée PAR LE BUILD.
- (7) L'ÉCART D81 FERMÉ (scripts/corriger_phrase_racine.py, fail-closed) : le
  PHRASE-CONTROLE-COFFRE.txt racine Drive portait 59 o / 3 lignes (ligne 1 ==
  phrase du dépôt, recoupé en mémoire SANS affichage), l'ouverture ÉCHOUAIT
  (« déchiffrement impossible »), la copie du dépôt (33 o) ouvrait (rc=0) —
  MUTATION APRÈS preuves (upload_update), re-téléchargement IDENTIQUE octet
  pour octet, ouverture par le fichier RAPATRIÉ VERT (rc=0) ; coffre INTÈGRE
  (md5 23a2987a…, lecture seule) ; IDEMPOTENCE CONSTATÉE (re-exécution :
  ÉCART AU CONSTAT, AUCUNE MUTATION, rc=1).
- (8) CONSIGNATIONS : DECISIONS +D149 PAR SCRIPT (à la suite de D148),
  JOURNAL_TRAVAIL +Entrée 144 PAR SCRIPT (ordre 143<144<marqueur, rejeu REFUSÉ
  fail-closed), ce worklog +Task ID 62 ; scripts suivis : corriger_phrase_racine.py,
  inserer_d149.py, inserer_entree_144.py.
- FRONTIÈRES : AUCUNE balise posée (geste de PLAN — la 0.7.0-dev.1 viendra du
  premier build M6) ; scellé 0.6.0, cartes m0-m5, sceau ONZE arbres, arbres I,
  fixtures v5 : INTACTS ; aucune suppression Drive, corbeille non vidée ;
  .keys/ gitignoré ; D139 ouverte non bloquante ; la seule mutation Drive du
  geste est la correction D81 PRÉVUE (fichier phrase racine, avant/après
  attestés).
- SUITE : LE CHANTIER M6-(a) — le durcissement format (writer ET_DYN/PIE +
  GNU_STACK + segments R/RX/RW, table ERRNOS, unix/layout.py) ; les décisions
  développeur (terrain WSL2/VM, réserve qemu, aval du report M5-(c)) peuvent
  tomber au fil de l'eau.

Stage Summary:
- Le plan des jalons M6/M7 est ÉCRIT et ANCÉ DANS LE RÉEL : les fiches de
  profil complètes précèdent le premier octet (l'exigence du manuel honorée),
  le programme part du fait que la chaîne ELF64 vit déjà (échelle
  d'auto-hébergement D34) et nomme ce qui manque (parité, diff nul, durcissement
  format, patch en production) ; les constats labo sont datés et vérifiés
  (keystone sans RISC-V : l'assembleur RV64 est un livrable, pas une surprise).
- Le chantier M5-(c) est reporté AU M6-(d) de façon EXPLICITE — le critère
  « patch à chaud du journal en production » sera démontré sur le profil Linux,
  moteur tcp-07 embarqué. L'écart D81 racine Drive est FERMÉ (le fichier
  ouvre le coffre, la remise est la phrase seule, le coffre n'a pas bougé).

- ADDENDUM Task ID 62 (honnêteté des étiquettes, leçon D138) : le PDF formel
  v0.6.1 demeure BYTE-IDENTIQUE (sha f34b2720…, consignation n°19 PAR LE
  BUILD) — la chaîne spec_v061 construit depuis le LaTeX scripts/spec_v061/
  (balise de la révision D137, état des jalons au 31/10 : « M5 ouvert »,
  sec-d.tex), PAS depuis la source de travail docs/PROTOCOLE_TRIADE.md ; le
  rebuild déclenché par le changement des sources .md (stamp nouveau
  b5ae11d8…) a produit un PDF identique — comportement ÉTABLI (consignations
  14→18 identiques à travers trois commits). L'état courant « M0–M5 franchis,
  M6/M7 ouverts » vit à la SOURCE DE TRAVAIL .md et au plan ; il rejoindra le
  PDF formel à la prochaine RÉVISION de la spécification (le versionnement
  suit les révisions du protocole, jamais les franchissements — v0.5.1/D75,
  v0.5.2/D81, v0.6.0/D133, v0.6.1/D137). Le libellé du commit e6a0177
  « regénéré (état des jalons…) » nomme le DÉCLENCHEUR du rebuild, pas un
  changement de contenu du PDF — la présente note le fixe pour la traçabilité.

- PASSATION D141 rejouée au geste « plan M6/M7 écrit / programme ouvert » :
  le bundle courant triade-history-060-c1107d2.bundle (git bundle --all,
  15 425 266 o, md5 c2ebb26b…) déposé au MIROIR, ASSERTÉ avant dépôt (branche
  jalon pointe sur c1107d2 — il porte l'ouverture du programme M6/M7 AVEC sa
  consignation : fiches de profil + programme D149 + statut M5 franchi +
  report M5-(c) + écart D81 fermé + Entrée 144 + D149 + addendum d'honnêteté
  PDF) ; l'ancien 060-f425ceb (md5 e9568bd7… recoupé AVANT) ARCHIVÉ VERSIONNÉ
  dans archives-bundles/ (10 archives, jamais supprimé) ; /test sans copie de
  bundle (recoupé) ; GitHub porté à la pointe dans le même geste (sync_backup,
  push recoupé) ; script suivi : passe_bundle_plan_m6m7.py ; FRONTIÈRES :
  aucune suppression (l'archivage est un déplacement), les scellés et la
  carte 0.6.0 INTACTS, /test inchangé (8 entrées D143, vague e4 courante).

## Task ID 63 — « continue M6 » : LE CHANTIER M6-(a) ACCOMPLI — LE DURCISSEMENT FORMAT DÉMONTRÉ EN EXÉCUTION (la sonde unix/ : ET_DYN/PIE à base aléatoire CONSTATÉE 6 bases distinctes/6 runs + setarch -R + readelf, 3 segments R/RX/RW, PT_GNU_STACK sans X, W^X DEPUIS LES PHDR, table ERRNOS exercée sur ses deux branches, round-trip 100 %, falsification 11/11) ; LA BALISE 0.7.0-dev.1 POSÉE par le premier build M6 (comme l'annonçait D149) ; D150 née (la table motivée par bloc, l'état qui traverse vit en mémoire) ; Entrée 145, D150 (04/11)

Task: demande du développeur « continue M6 » — la suite annoncée au Task 62
était le chantier M6-(a), le durcissement format (« aucune décision développeur
ne le bloque ») : le geste l'exécute jusqu'au vert et le consigne.

Work Log:
- (0) REPRISE RECROUPÉE : dépôt propre à 2b2853e (pointe = passation du plan
  M6/M7), git status vide, .keys/ présent (passphrase + graine D27), labo
  re-vérifié : ASLR noyau actif (randomize_va_space=2), setarch présent,
  keystone/capstone opérationnels, le bac à sable EST Linux x86-64 (fiche
  § 10 — l'oracle du jalon s'exécutera NATIVEMENT).
- (1) LA LIGNÉE DU JALON NÉE (unix/, convention D149-(5) — m6/ et m7/
  demeurent l'échelle D34) : unix/layout.py (ET_DYN/PIE, 3 segments R/RX/RW,
  PT_GNU_STACK 0x6474e551 sans X, table ERRNOS {9:1} + VERDICT_FATAL 6,
  messages, tampon .bss, versions — 0.7.0-dev.1/rc.1/0.7.0, plancher
  0x00070000) ; unix/I/ (README + QUATRE specs écrites-avant-code : su-01
  écrire [miroir ah-01, ET instrument déclaré des sondes d'erreur], su-02
  hex64 [%016lx du noyau], su-03 verdict [la table ERRNOS, miroir
  tls-02:R1/HRESULTS D79], su-04 principal [_start : SA base par lea rip
  sur le témoin .rodata, les deux branches de la table exercées, arrêt
  propre code 6]) ; brouillons étiquetés + unix/outils/auteur.py (le point
  fixe du modèle, séries f6xxxx par CARTE) ; unix/carte_sonde.py (génération
  1 au TROISIÈME sel : m2, hachoir D34, jalon unix — clés projet partagées
  D27).
- (2) LE WRITER (unix/build_m6.py, modèle build_ah) : chaîne intégrale —
  couche I auditée (gabarit § 2.2), round-trip keystone/capstone PAR
  INSTRUCTION, oracle structurel ÉTENDU (appels : les blocs déclarés ∪ les
  étiquettes locales déclarées — le sous-programme .emit passe la même
  porte ; syscalls PAR BLOC {1}/{231} ; cibles RIP déclarées ; NOUVEAU :
  accès [base + RVA] déclarés — le code est indifférent à la base ; _start
  sans push + pile appariée du sous-programme), composition à la main
  (ehdr ET_DYN + 4 phdr, e_entry RELATIF 0x1140, .bss pur filesz 0),
  valider_elf RELIT l'image (W^X depuis les phdr, concordance des tables au
  layout source unique).
- (3) L'ORACLE NATIF (le critère du chantier, exécution réelle au labo) :
  6 runs, quatre lignes octet pour octet et code 6 à chaque fois — la
  sonde émet SA base (6 bases DISTINCTES, alignées 0x1000 : l'ASLR noyau
  CONSTATÉ, jamais décrété), setarch -R rend la MÊME base deux fois (la
  base vient du NOYAU, pas du programme), readelf recoupe (DYN, 3 LOAD
  R/R E/RW, GNU_STACK RW align 0x10) ; la table ERRNOS EXERCÉE en
  exécution : EBADF nommé (verdict 1, la sonde continue), EFAULT hors
  table (VERDICT_FATAL 6, ligne fatale, arrêt propre code 6) ;
  falsification 11 mutations attrapées (zéro silence).
- (4) LES DEUX LEÇONS ATTRAPÉES PAR LES GARDES (le cœur de D150) : (a) la
  leçon C1 EN DIRECT — @L_FATAL portait 36, le message réel en fait 37 (le
  «\n» oublié) : verifier_symboles a REFUSÉ le build AVANT exécution ;
  (b) le premier .emit mourrait au premier appel (r8/r9 clobber par
  su-02/su-03, r11 détruit par chaque syscall de su-01 — la sortie rendait
  deux lignes, l'adresse doublée rendait EFAULT) : l'oracle natif a REFUSÉ
  fail-closed, JAMAIS un faux vert. Correction : préfixe consommé avant le
  premier appel, verdict au tampon .bss +32 (TAMPON_NUM), brut en r10
  (registre interne que ni su-01 ni su-02 ni su-03 ne touchent) — la règle
  D150 consigne le réflexe.
- (5) LA CARTE + LE TABLEAU DE BORD : génération 1 de la lignée du jalon
  (4 fragments chiffrés, signature Ed25519 clés projet, verrou croisé R8
  4/4, frag-bld « artefact=sonde version=0.7.0-dev.1 profil=
  x86-64-linux-elf64 »), tableau-de-bord.txt (format durci, contrat
  d'erreurs, PIE/ASLR, falsification) ; re-vérification --verifier :
  cristallisation 2/10, verrou croisé re-recoupé.
- (6) CONSIGNATIONS : JOURNAL_TRAVAIL +Entrée 145 PAR SCRIPT (ordre
  144<145<marqueur, rejeu REFUSÉ fail-closed), DECISIONS +D150 PAR SCRIPT
  (à la suite de D149), fiche de profil § 3 (le durcissement passe de À
  PRODUIRE à ACQUIS PAR LE CHANTIER M6-(a), constats datés et re-vérifiés
  au chantier qui les touche — keystone/capstone re-vérifiés par le
  round-trip même, le MÊME moteur que le primaire), PLAN_MILESTONES §
  État du programme (M6-(a) RÉALISÉ le 04/11, (b)/(c)/(d) attendent), ce
  worklog +Task ID 63 ; scripts suivis : inserer_entree_145.py,
  inserer_d150.py, passe_bundle_m6a.py.
- FRONTIÈRES : la balise 0.7.0-dev.1 est POSÉE (geste de BUILD, jamais de
  scellage — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le
  contrôle D146 adapté ; la sonde est un DEV vivant, la garde
  anti-rollback n'existe pas encore) ; scellé 0.6.0, cartes m0-m5, sceau
  ONZE arbres, arbres I, fixtures v5, hachoir m6/ (ET_EXEC, VALIDE pour SA
  lignée — l'écart est NOMMÉ) : INTACTS ; aucune suppression Drive,
  corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non bloquante.
- SUITE : LE CHANTIER M6-(b) — le corpus paritaire (audit de couplage A/B/C,
  révision de granularité R+1 au niveau FORMEL, invariance des octets
  Windows ASSERTÉE, diff nul MESURÉ PAR SCRIPT, oracle m1 régénéré VERT sur
  l'instance Linux, un principal propre au jalon) ; puis (c) conformité +
  scellage 0.7.0-rc.1 (contrôle D146 adapté), (d) le patch en production ;
  les décisions développeur (terrain WSL2/VM, réserve qemu, aval du report
  M5-(c)) peuvent tomber au fil de l'eau.

Stage Summary:
- Le chantier M6-(a) est ACCOMPLI sur pièces : le durcissement format n'est
  plus une exigence de fiche, c'est un comportement CONSTATÉ en exécution —
  la sonde calcule et émet sa propre base (l'image PIE vit à la base que le
  NOYAU choisit), la table ERRNOS rend ses verdicts sur ses deux branches,
  et le build relit son image pour constater W^X depuis les phdr.
- Les deux défenses du protocole ont travaillé EN DIRECT : la leçon C1 a
  refusé l'arithmétique fausse de l'auteur (36 → 37), l'oracle natif a
  refusé le sous-programme qui mourait au premier appel — deux refus
  fail-closed, zéro faux vert, la règle D150 en est née.
- La balise 0.7.0-dev.1 est posée par le premier build M6, exactement comme
  l'annonçait D149 : la lignée du jalon vit, sa carte au troisième sel.

## Task ID 64 — « continue » : LE CHANTIER M6-(b) ACCOMPLI — LE CORPUS PARITAIRE INSTANCIÉ, LE DIFF NUL MESURÉ (39 recoupements, les CINQ scellés Windows octet-identiques à l'état zéro), L'ORACLE m1 RÉGÉNÉRÉ VERT SUR L'INSTANCE LINUX (76 631 cas verts, 20 verrous, exécution native, falsification 12/12 zéro silence — tcp-07 épuisé par SON scénario et le V7 DEP en fils) ; L'ARTEFACT unix/corpus 12 288 o ET_DYN/PIE (sha256 dd14195c…), LA BALISE 0.7.0-dev.2 POSÉE, la carte génération 1 du corpus (verrou croisé R8 13/13, cristallisation 2/10) ; D151 née (ABSENT ≠ ILLISIBLE ; la mutation nomme son geste ; la falsification exhaustive par instruction ; le hors-chemin épuisé par SON scénario ; l'entrant concurrent porte ses entrées locales) ; Entrée 146, D151 (04/11)

Task: reprise du chantier M6-(b) (la suite annoncée au Task 63) — le geste
s'était éteint à 14:40 (sources écrites, la chaîne jamais conduite jusqu'au
vert) ; une première reprise l'a exécutée jusqu'au vert puis s'est éteinte à
son tour à la consignation (inserer_entree_146.py écrit, jamais exécuté) ;
la présente passe vérifie l'état VERT SUR PIÈCES, conduit les consignations
et la passation.

Work Log:
- (0) REPRISE : dépôt à 018db94 (pointe = passation M6-(a)), l'arbre de
  travail porte le chantier M6-(b) non committé (audit + specs R+1 +
  notation + build/oracle/diff_nul + artefact + carte) ;
  vérification d'intégrité PAR BLOBS (seuls unix/I/README.md,
  unix/layout.py et unix/outils/auteur.py ont un contenu modifié — les
  scellés Windows, cartes m0-m5, scénarios e2/e3/e4 et sceau-I INTACTS en
  contenu, le reste n'est que des modes 755) ; labo re-vérifié :
  capstone/keystone RÉINSTALLÉS après recyclage du bac à sable (constat
  fiche § 6 inchangé — capstone 5.0.7, keystone OK).
- (1) L'AUDIT DE COUPLAGE (unix/I/AUDIT-COUPLAGE-CORPUS.md,
  écrit-avant-code) : le constat central — la classe A est VIDE (le
  paramétrage msx64 est partout dans le patrimoine), la voie du diff nul
  passe ENTIÈREMENT par la révision de granularité R+1 au niveau FORMEL ;
  la classe C (couplée à l'OS) est NOMMÉE, jamais réduite ; l'incident de
  l'état zéro consigné au § 6 (m1/build_m1.py échoue OUVERT sur carte
  illisible — except ErreurCarte: pass ; selftest.exe OCTET-IDENTIQUE,
  carte m1 RESTAURÉE depuis git) fonde ABSENT ≠ ILLISIBLE.
- (2) LES DOUZE RÉVISIONS R+1 + LE PRINCIPAL : les specs révisées vivent
  dans l'arbre du jalon unix/I/ (libc-01..08, hello-02/03, tcp-07, tcp-11
  + corpus-13 le domaine neuf modèle ah-09), ancêtres scellés INTACTS dans
  m0/m1/m2 — la même couche I que M7 instanciera en troisième ; frag-con
  DEUX PROFILS par bloc (§ 8.3-4) ; les DEUX journaux corrigés (tcp-11:R2
  + le staging v2 — le remplaçant vérifié AVANT embarquement).
- (3) LA CHAÎNE jusqu'au VERT (reprise de l'interruption 14:40) : build
  fail-closed, oracle natif 76 631 cas verts / 20 verrous (graines 1 et 2
  différenciées, empreintes 0e3d96c3…/09444ffb…), falsification 12/12 zéro
  silence, diff nul 39 recoupements (fichiers canoniques empreintés zéro
  copie, observables R1↔R+1 équivalents — 35 identiques + 1 écart nommé
  frag-con —, les CINQ scellés Windows octet-identiques à l'état zéro mesuré
  AVANT le geste par etat_zero_m6b.py), artefact 12 288 o sha256
  dd14195c…, LA BALISE 0.7.0-dev.2 POSÉE (geste de BUILD), carte
  génération 1 (fragments chiffrés, Ed25519, verrou croisé R8 13/13,
  cristallisation 2/10).
- (4) LES REFUS TRAVERSÉS (le cœur de D151) : le SEGFAULT MUET de
  l'autotest (img.poser sans ouverture — l'instrument de mutation NOMME
  désormais son geste) ; « libc-08 N=19 » (la fixture SC sert les DEUX
  sens — l'attendu corrigé SUR PIÈCES) ; le SEGFAULT DÉTERMINISTE du
  journal (memcpy rend dst jamais la longueur — l'add déplacé AVANT le
  call ; le staging v2 portait LE MÊME piège, corrigé AVANT embarquement) ;
  la cartouche non ré-entrante (verdicts divergents — entrées locales par
  appel, sommet attribué sous verrou court, fenêtre de sorties par appel) ;
  « libc-06 PASSÉ SILENCIEUX » (guéri par un RÉSIDU DE REGISTRE — la
  falsification devient EXHAUSTIVE par instruction) ; « tcp-07 : 78
  mutations TOUTES silencieuses » (HORS-CHEMIN du principal, fait de plan —
  épuisé par SON scénario + le V7 DEP en fils : le père observe, le fils
  meurt).
- (5) LA VÉRIFICATION SUR PIÈCES de la présente passe (l'état vert constaté
  AVANT consignation) : sha256 dd14195c… recoupé ; exécution native deux
  lignes code 0 + setarch -R ; readelf (DYN, 3 LOAD R/R-E/RW, GNU_STACK
  RW) ; diff_nul VERT 39 recoupements ; oracle rejoué aux DEUX graines
  (76 631 cas verts / 20 verrous, empreintes identiques à la carte).
- (6) CONSIGNATIONS : JOURNAL_TRAVAIL +Entrée 146 PAR SCRIPT (ordre
  145<146<marqueur, rejeu REFUSÉ fail-closed), DECISIONS +D151 PAR SCRIPT
  (à la suite de D150), fiche de profil § 7 (la granularité passe de Jalon
  à ACQUIS PAR LE CHANTIER M6-(b)) + § 3 (le corpus L'A HÉRITÉ), PLAN §
  État du programme (M6-(a) ET M6-(b) RÉALISÉS le 04/11, (c)/(d)
  attendent), ce worklog +Task ID 64 ; scripts suivis : etat_zero_m6b.py,
  inserer_entree_146.py, inserer_d151.py, passe_bundle_m6b.py.
- FRONTIÈRES : la balise 0.7.0-dev.2 est POSÉE (geste de BUILD, jamais de
  scellage — le scellage 0.7.0-rc.1 viendra du chantier (c) avec le
  contrôle D146 adapté full-ELF à la base réelle ; le corpus est un DEV
  vivant, la garde anti-rollback n'existe pas encore, le plancher demeure
  0.7.0-dev.1) ; scellé 0.6.0, cartes m0-m5, sceau ONZE arbres, arbres I,
  fixtures v5, hachoir m6/ : INTACTS (l'état zéro mesuré avant, le diff_nul
  recoupe à chaque build) ; aucune suppression Drive, corbeille non vidée ;
  .keys/ gitignoré ; D139 ouverte non bloquante.
- SUITE : LE CHANTIER M6-(c) — la suite de conformité (unix/
  conformite_profil.py, modèle m5 : les SEPT éléments constatés depuis
  l'artefact) + le scellage 0.7.0-rc.1 avec le contrôle D146 adapté
  (exécution full-ELF à la base réelle, l'émulation à base fixe interdite
  comme témoin unique) ; puis (d) le patch en production — le chantier
  M5-(c) refermé (bascule du journal PENDANT le trafic, moteur tcp-07
  EMBARQUÉ, le staging v2 corrigé attend la démonstration), kit terrain au
  coffre /test (WSL2 recommandé D149) ; les décisions développeur (terrain
  WSL2/VM, réserve qemu, aval du report M5-(c)) peuvent tomber au fil de
  l'eau.

Stage Summary:
- Le chantier M6-(b) est ACCOMPLI sur pièces : le diff nul n'est plus une
  exigence du plan, il est MESURÉ par script (39 recoupements rejouables) —
  les instances des deux profils chargent les MÊMES fichiers I, les
  scellés Windows n'ont pas bougé d'un octet.
- Les refus du geste ont chacun fondé une règle (D151) : l'instrument de
  mutation nomme son geste, la falsification est exhaustive par
  instruction, le hors-chemin est épuisé par SON scénario, l'entrant
  concurrent porte ses entrées locales — et ABSENT ≠ ILLISIBLE ferme le
  trou par lequel la garde m1 s'éteignait.
- La balise 0.7.0-dev.2 est posée par le build du corpus, l'héritage
  M6-(a) est CONSTATÉ (ET_DYN/PIE, W^X depuis les phdr) : la lignée du
  jalon vit, la carte du corpus en génération 1 au même troisième sel.

- PASSATION D141 rejouée au geste « chantier M6-(b) accompli / corpus
  paritaire instancié » : le bundle courant
  triade-history-060-34fe080.bundle (git bundle --all, 15 620 078 o, md5
  8ca07595…) déposé au MIROIR, ASSERTÉ avant dépôt (branche jalon pointe
  sur 34fe080 — il porte LE SECOND CHANTIER DU JALON M6 AVEC sa
  consignation : l'audit de couplage + les DOUZE specs R+1 + le build/
  oracle/diff_nul + l'artefact unix/corpus ET_DYN/PIE 12 288 o sha256
  dd14195c… + la carte génération 1 verrou croisé R8 13/13 + LE DIFF NUL
  mesuré 39 recoupements + l'oracle m1 régénéré VERT 76 631 cas + LA
  BALISE 0.7.0-dev.2 POSÉE par le build du corpus + Entrée 146 + D151 +
  worklog Task 64) ; l'ancien 060-51bd748 (md5 449d1fd0… recoupé AVANT)
  ARCHIVÉ VERSIONNÉ dans archives-bundles/ (12 archives, jamais supprimé) ;
  /test sans copie de bundle (recoupé) ; GitHub porté à la pointe dans le
  même geste (push 018db94..34fe080, recoupé ls-remote) ; script suivi :
  passe_bundle_m6b.py ; FRONTIÈRES : aucune suppression (l'archivage est un
  déplacement), la finale 0.6.0 et sa carte INTACTS, /test inchangé (8
  entrées D143, vague e4 courante — le kit terrain M6-(d) attendu).

## Task ID 65 — « continue » : LE CHANTIER M6-(c) ACCOMPLI — LA SUITE DE CONFORMITÉ VERTE 7/7 (unix/conformite_profil.py, modèle m5 : 37 contrôles PASS, les SEPT éléments CONSTATÉS depuis l'artefact relu, le diff nul REJOUÉ à chaque passage) ; LE CONTRÔLE D146 ADAPTÉ NÉ (unix/controle_base_reelle.py : l'image PIE EXÉCUTÉE PAR LE NOYAU, 6 bases réelles DISTINCTES constatées par témoin ptrace/maps à l'arrêt d'exec, ADDR_NO_RANDOMIZE recoupé même base deux fois, le mutant « RVA nu » mort NOMMÉ à 0x280 RIP dans libc-01:R2 — la classe exacte du crash e3, en base aléatoire ET figée) ; LA CRISTALLISATION CONDUITE À 10/10 (graines datées 20261105→20261112) À TRAVERS L'INCIDENT DE LA CARTOUCHE (le refus intermittent « tcp-11 concurrence : verdicts divergents » ~1/11 — la chasse par sonde 240 essais a NOMMÉ la cause : l'allocateur de sommets par décrément-restitution rompt la LIFO sous concurrence, deux appels vivants partageaient la fenêtre ; LE SOMMET EST DÉSORMAIS PAR FIL, tcp-11 EXONÉRÉ sur pièces, l'artefact n'a pas bougé d'un octet) ; SCELLAGE 0.7.0-rc.1 AVEC LE D146 EXÉCUTÉ AU SCELLAGE MÊME (modèle D147 : cristallisation 10/10 + conformité 7/7 + bascule dev.2→rc.1 dans frag-bld occurrence unique assertée + re-scellage vérifié EN MÉMOIRE avant l'unique écriture + verrou croisé 13 empreintes + l'artefact INTACT sha dd14195c…, le scellage est un fait de carte) ; LES TROIS GARDES VIVANTES (re-scellage REFUSÉ, reconstruction REFUSÉE, la balise scellée SURVIT à la re-vérification) ; D152 née (05/11)

Task: reprise « continue » — le résumé de reprise mélangeait des états
historiques M5 (le « chemin rc.2 » et le « kit e4 » : des affaires réglées
aux Entrées 142-143, la finale 0.6.0 est posée) ; l'état réel recoupé sur le
worklog et git (aecb538) : M6-(a) et M6-(b) accomplis, la suite annoncée au
Task 64 était LE CHANTIER M6-(c) — le geste l'exécute jusqu'aux gardes.

Work Log:
- (0) REPRISE : dépôt propre à aecb538 (passation M6-(b) déposée), le labo
  réinstallé après recyclage du bac à sable (pynacl manquant — réinstallé ;
  keystone/capstone opérationnels, ASLR noyau actif randomize_va_space=2),
  l'état VERT re-établi SUR PIÈCES (verifier graine 3 : round-trip 100 %,
  oracle 76 631 cas / 20 verrous, verrou croisé 13/13, sha dd14195c…
  recoupé, cristallisation portée à 3/10).
- (1) LE CONTRÔLE D146 ADAPTÉ (le livrable né — la règle D146 devenue OUTIL,
  modèle m5/controle_base_reelle.py) : le contrôle N'ÉMULE RIEN (le labo EST
  Linux x86-64, l'image est EXÉCUTÉE par execve au NOYAU) ; la base est
  CONSTATÉE par témoin PTRACE_TRACEME (arrêt garanti À L'EXEC, lecture
  /proc/<pid>/maps : le mapping du fichier à l'offset 0) ; les pièces
  fail-closed : (a) 6 exécutions témoignées, 6 bases DISTINCTES (6/6,
  alignées 0x1000), deux lignes exactes + code 0 à CHAQUE base ; (b)
  ADDR_NO_RANDOMIZE (personality, le mécanisme de setarch -R) : MÊME base
  deux fois (0x7ffff7ffb000) — la base vient du noyau ; (c) FALSIFIABILITÉ
  SUR LA CLASSE : le mutant « RVA nu » (le lea rip de la chaîne du journal
  @0x1C48 réécrit mov edi, 0x280 — l'adresse sans la base, le geste de la
  ligne de flux fautive du 0.6.0-rc.1) meurt NOMMÉ : SIGSEGV à 0x280, RIP
  rapporté AU BLOC par la plage EXACTE du slot du plan (f61003 libc-01:R2 —
  une première version attribuait à hello-02 par une plage à +0x200 : la
  faute est NOMMÉE ou n'est rien), en base aléatoire ET en base figée (la
  base figée du noyau n'est JAMAIS 0) ; (d) frontière nommée : le patch
  n'est pas au rituel (corpus-13:R1 I1), sa démonstration vit à l'oracle et
  au chantier (d). Le mutant vit en COPIE temporaire supprimée au retour.
- (2) LA SUITE DE CONFORMITÉ (modèle m5/D104 : chaque constat tranché
  binaire, sortie unix/conformite.txt) : éléments 1-7 constatés depuis
  l'ARTEFACT RELU (magie/ET_DYN/machine ; segment RX décodable sans reste ;
  les 23 vecteurs dorés octet pour octet ; les 65 appels directs aux
  entrées du plan ; zone rouge INUTILISÉE ; pile équilibrée PAR CONTEXTE —
  les sous-programmes locaux scannés dans leur contexte d'appel (.protger
  de tcp-07), alignement conduit ≡ 0 mod 16 aux points d'appel ; les
  phdr RELUS + readelf INDÉPENDANT ; les syscalls PAR BLOC depuis les
  octets ; écrire rend rax BRUT ; les codes 1-5 EXERCÉS en exécution ; la
  table ERRNOS de la lignée lue depuis la sonde dev.1 ; LA PORTE R10
  DÉCLINÉE ELF : table @0x540, staging 216 o, somme déclarée == RECALCULÉE
  depuis l'artefact ; 0x7/0x5 dans les octets ; le qword unique [r15] ; le
  scénario patch complet 6/6 familles ; round-trip REJOUÉ 13 blocs +
  staging ; empreintes frag-prf == fichiers 13/13 ; DIFF NUL REJOUÉ 39
  recoupements ; 13 blocs aux rva/slot de plan, padding >= 16, croissance
  int3) + contrôle de jalon (oracle m1 reduit 8 231 cas, graine datée) —
  VERTE 7/7, 37 contrôles PASS. Les cinq ECHECS du premier passage ont
  chacun fondé une correction (regex frag-con 3 lignes intermédiaires,
  coquille RDI/RSI, parse readelf R E en deux champs, seuil oracle reduit
  8000, scan de pile par contexte) — la suite refuse AVANT de constater.
- (3) L'INCIDENT DE LA CRISTALLISATION (le cœur de D152) : refus
  fail-closed « tcp-11 concurrence : verdicts divergents » à la graine
  20261109, INTERMITTENT (~1/11 — la même graine re-passait 4/4) ; la
  chasse par sonde dédiée (scripts/probe_concurrence.py, 240 essais) a
  attrapé la signature : rax = la longueur d'UNE AUTRE ligne (±1-2), pile
  équilibrée ; LA CAUSE : l'allocateur de sommets de la cartouche
  (décrément PAS_PILE à l'entrée, restitution au retour) est un bump-LIFO
  que l'ordre de restitution INTERFOLÉ rompt — un fil libère pendant que
  l'autre vit, le plafond remonte sur le sommet de l'appel VIVANT : deux
  appels partagent la fenêtre et la pile ; D151 avait rendu la FENÊTRE par
  appel, le SOMMET restait à recouvrement ; LE CORRECTIF : le sommet est
  PAR FIL (attribué une fois sous verrou, réutilisé en séquence dans SON
  fil, JAMAIS restitué) ; 240 essais verts post-correctif, l'oracle complet
  vert ; tcp-11 EXONÉRÉ sur pièces (l'instrument mentait, pas le code) ;
  la tentative refusée n'a PAS incrémenté la cristallisation (la carte
  n'est re-signée que sur le vert), l'artefact n'a pas bougé (sha constant
  à travers toute la chasse).
- (4) LES DÉFAUTS LATENTS corrigés avant qu'ils ne mangent : verifier()
  régénérait frag-bld avec version=dev.2 EN DUR — après un scellage, toute
  re-vérification aurait REVERTI la balise (le défaut était là depuis le
  Task 64) : la re-vérification lit la balise du manifeste et re-signe
  SOUS elle (le scellé ne se revertit pas — modèle m5), et verifier()
  n'appelle plus _anti_rollback (vérifier n'est pas reconstruire) ; le
  REGISTRE DES VERSIONS ACCEPTÉES (BALISES_LIGNEE, plancher 0.7.0-dev.1)
  refuse toute balise hors lignée ; verifier_listes_blanches délégué par
  carte_corpus (le premier passage du scellage a été REFUSÉ fail-closed
  AVANT toute écriture sur ce manque — la moitié du modèle).
- (5) LE SCELLAGE 0.7.0-rc.1 : la séquence EXÉCUTÉE AU SCELLAGE même — D146
  adapté VERT (re-exécuté dans le geste), cristallisation 13 blocs à 10/10
  (conduite aux graines datées 20261105→20261112), conformité 7/7 (37
  contrôles), bascule 0.7.0-dev.2 → 0.7.0-rc.1 dans frag-bld (occurrence
  unique ASSERTÉE), re-scellage VÉRIFIÉ EN MÉMOIRE avant l'unique écriture
  (listes blanches D15, signature, racine, bascule constatée), verrou
  croisé post-scellage 13 empreintes, artefact INTACT (sha256
  dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7,
  12 288 o — le scellage est un fait de carte).
- (6) LES GARDES VIVANTES constatées sur pièces : re-scellage REFUSÉ
  (« balise 0.7.0-dev.2 attendue une fois (0 occurrence) — scellage refusé
  fail-closed ») ; reconstruction REFUSÉE (« carte scellée (0.7.0-rc.1) :
  reconstruction interdite — procedure lourde R6 ou nouvelle version
  requise ») ; la re-vérification SOUS balise scellée fonctionne et
  PRÉSERVE la balise (carte sous 0.7.0-rc.1, cristallisation stable
  10/10, verrou croisé 13/13, oracle 76 631 cas verts graine 20261113).
- (7) CONSIGNATIONS : JOURNAL_TRAVAIL +Entrée 147 PAR SCRIPT (ordre
  146<147<marqueur, rejeu REFUSÉ fail-closed), DECISIONS +D152 PAR SCRIPT
  (à la suite de D151), fiche de profil § 8 (le scellage POSÉ avec D146 au
  geste même, les gardes vivantes, le registre au code) + § 9 (la suite
  LIVRÉE EXÉCUTÉE VERTE 7/7 au scellage même), PLAN_MILESTONES § État du
  programme (M6-(a)/(b)/(c) RÉALISÉS, le (d) attend), ce worklog +Task ID
  65 ; scripts suivis : probe_concurrence.py, inserer_entree_147.py,
  inserer_d152.py, passe_bundle_m6c.py.
- FRONTIÈRES : l'artefact unix/corpus n'a pas bougé d'un octet de tout le
  chantier (le scellage est un fait de carte) ; --sceller-final est
  DISPONIBLE au code (il attend rc.1 une fois) mais JAMAIS exécuté avant
  le run terrain vert du chantier (d) (l'exigence porte « validation
  terrain consignée » — la discipline m5) ; scellé 0.6.0 + cartes m0-m5 +
  sceau ONZE arbres + arbres I + fixtures v5 + hachoir m6/ + sonde dev.1
  INTACTS (le diff nul rejoué à chaque conformité) ; aucune suppression
  Drive, corbeille non vidée ; .keys/ gitignoré ; D139 ouverte non
  bloquante.
- SUITE : LE CHANTIER M6-(d) — le patch en production, le chantier M5-(c)
  refermé : bascule du journal PENDANT le trafic (le moteur tcp-07 EMBARQUÉ,
  le staging v2 corrigé attend la démonstration), rollback, zéro régression
  ; kit terrain Linux au coffre /test (artefact + scénario + LISEZMOI, WSL2
  recommandé D149), run du développeur, preuves renvoyées ; si vert :
  --sceller-final pose 0.7.0. Les décisions développeur (terrain WSL2/VM,
  réserve qemu, aval du report M5-(c)) peuvent tomber au fil de l'eau.

Stage Summary:
- Le chantier M6-(c) est ACCOMPLI sur pièces : la suite de conformité est
  VERTE 7/7 — les SEPT éléments CONSTATÉS depuis l'artefact relu, jamais
  déclarés, le diff nul rejoué à chaque passage.
- Le contrôle D146 adapté est NÉ et VERT : l'image PIE exécutée par le
  NOYAU à 6 bases réelles distinctes CONSTATÉES (jamais décrétées), et le
  mutant « RVA nu » — la classe exacte du défaut qui tua le 0.6.0-rc.1 —
  mort NOMMÉ à chaque base : la leçon e3 intégralement transposée au profil
  Linux, la falsifiabilité portant sur la CLASSE gardée.
- L'incident de la cristallisation a fondé D152 : l'instrument concurrent
  fautif (allocateur par décrément-restitution) nommé et corrigé sur
  pièces — le sommet est PAR FIL, le bloc sous test EXONÉRÉ ; deux défauts
  latents corrigés avant qu'ils ne mangent (la balise scellée aurait pu
  être revertie par une re-vérification).
- LE SCELLAGE 0.7.0-rc.1 EST POSÉ : D146 exécuté AU geste même, la
  cristallisation 10/10, la conformité 7/7, l'artefact INTACT — et les
  TROIS gardes vivantes constatées : le candidat est SOUMIS au chantier
  (d), le patch en production et le run terrain.

- PASSATION D141 rejouée au geste « chantier M6-(c) accompli / la suite de
  conformité verte + le scellage 0.7.0-rc.1 » : le bundle courant
  triade-history-060-5328156.bundle (git bundle --all, 15 681 564 o, md5
  e15e2c2f…) déposé au MIROIR, ASSERTÉ avant dépôt (branche jalon pointe
  sur 5328156 — il porte LE TROISIÈME CHANTIER DU JALON M6 AVEC sa
  consignation : la suite de conformité unix/conformite_profil.py [37
  contrôles, les SEPT éléments constatés depuis l'artefact relu, le diff
  nul rejoué] + LE CONTRÔLE D146 ADAPTÉ unix/controle_base_reelle.py [6
  bases noyau distinctes CONSTATÉES par témoin ptrace/maps, le mutant « RVA
  nu » mort nommé] + LE SCELLAGE 0.7.0-rc.1 avec le D146 EXÉCUTÉ AU SCELLAGE
  même [cristallisation 13/13 à 10/10, conformité 7/7, bascule de balise,
  gardes vivantes] + la cartouche au sommet PAR FIL + Entrée 147 + D152 +
  worklog Task 65) ; l'ancien 060-34fe080 (md5 8ca07595… recoupé AVANT)
  ARCHIVÉ VERSIONNÉ dans archives-bundles/ (13 archives, jamais supprimé) ;
  /test sans copie de bundle (recoupé) ; GitHub porté à la pointe dans le
  même geste (push aecb538..5328156, recoupé ls-remote) ; script suivi :
  passe_bundle_m6c.py ; FRONTIÈRES : aucune suppression (l'archivage est un
  déplacement), la finale 0.6.0 et sa carte INTACTS, /test inchangé (8
  entrées D143, vague e4 courante — le kit terrain M6-(d) attendu).

## Task ID 66 — « ok go M6-(d) » : LE CHANTIER M6-(d), PARTIE LABORATOIRE ACCOMPLIE — LE CHANTIER M5-(c) REFERMÉ SUR LE PROFIL LINUX : unix/demo_patch.py NÉ ET VERT (la bascule du journal PENDANT le trafic — 1 200 usages, apply entre 400/401, rollback entre 800/801, tcp-07:R4 V5 ; le journal COHÉRENT octet pour octet — 800 lignes v1, 400 v2 marquées j2:, aucune déchirée, aucun mélange ; la CONCURRENCE RÉELLE — le qword d'atomicité Q3 posé pendant qu'un fil ouvrier journalise, la preuve de vie AVANT la bascule, les DEUX formats dans le flux de l'ouvrier, 5/5 passages verts sans intermittence ; le retour à l'état image ; la zéro régression — le fichier artefact n'a pas bougé d'un octet, le rituel rejoué code 0) ; LA SUITE DE CONFORMITÉ EXÉCUTE DÉSORMAIS LA DÉMONSTRATION (l'élément 5 devenu CONTRÔLE RÉEL — VERTE 7/7, 37 contrôles, le scellage final re-prouvera M5-(c) à chaque passage) ; LE KIT TERRAIN LINUX AU COFFRE /test (la vague m6d : kit-m6d.zip + LISEZMOI-m6d.txt + preuves-m6/ né, la vague e4 consommée ARCHIVÉE D143 md5 intacts, le kit ÉPROUVÉ au labo PAR EXTRACTION VIERGE + RUN : VERT 16/16 — la première épreuve a ÉCHOUÉ NOMMÉ : la narration de l'instrument polluait le flux mesuré, D153) ; D153 née (05/11)

Task: la suite annoncée au Task 65 était le chantier M6-(d) — le patch en
production (le chantier M5-(c) reporté, D149-(4)), le kit terrain Linux au
coffre /test, puis le run du développeur. Le geste l'exécute jusqu'au dépôt
du kit ; le scellage final 0.7.0 attend le run terrain vert (l'exigence
porte « validation terrain consignée » — jamais le labo à sa place).

Work Log:
- (0) REPRISE : dépôt propre à 402508f (l'arbre ne portait que des modes
  755 — le motif connu des reprises, aucun contenu modifié), la carte du
  corpus sous 0.7.0-rc.1, l'artefact sha dd14195c… ; le labo RÉINSTALLÉ
  après recyclage du bac à sable (keystone, capstone 5.0.7, pynacl) ;
  l'état VERT ré-établi SUR PIÈCES en la session (build_corpus
  --verifier --volume reduit --graine 20261105 : round-trips 100 %, oracle
  8 231 cas verts, cristallisation 13×10/10, verrou croisé 13/13, la
  balise rc.1 PRÉSERVÉE ; conformite_profil : VERTE 7/7 — 37 contrôles,
  le diff nul rejoué VERT).
- (1) LA DÉMONSTRATION (unix/demo_patch.py, modèle controle_base_reelle :
  la règle devenue OUTIL) : sur l'ARTEFACT SCELLÉ relu (sha ASSERTÉ, le
  fichier en lecture seule — le patch vit en cartographie PRIVÉE), les
  QUATRE pièces tranchées binaires : (a) LE TRAFIC EN SESSION V5 — 1 200
  usages, l'apply ENTRE les usages 400/401 (rax 0, état 1), le rollback
  ENTRE 800/801 (rax 0, état 0), la boucle SANS INTERRUPTION (verdicts
  exacts, pile équilibrée, non volatils intacts à chaque usage), le flux
  OCTET POUR OCTET l'attendu (800 v1 + 400 v2 « j2: », aucune déchirée,
  aucune perdue, AUCUN MÉLANGE) ; (b) LA CONCURRENCE RÉELLE Q3 — la
  PREUVE DE VIE de l'ouvrier AVANT la bascule (des lignes déjà émises :
  la bascule tombe dans un trafic VIVANT), les trois fenêtres
  1→0→1→0, le conducteur sous CHAQUE version, l'ouvrier 5 224-5 478
  lignes ENTIÈRES (indices 0..n-1 chacun une fois, verdicts exacts) et
  SON flux porte les DEUX formats (~2 800 v1, ~2 520 v2) — le qword posé
  pendant qu'il journalisait, chaque ligne d'UNE seule version ;
  (c) LE RETOUR À L'ÉTAT IMAGE (entrée restaurée octet pour octet, état
  v1, verrou rendu, le remplaçant DORMANT dans la croissance) ; (d) LA
  ZÉRO RÉGRESSION (sha re-relu IDENTIQUE, le rituel rejoué : deux lignes,
  code 0). La chasse D152 : CINQ passages — 5/5 VERTS, 16 PASS chacun,
  aucune intermittence.
- (2) L'INTÉGRATION À LA SUITE : l'élément 5 de conformite_profil.py
  (frontière documentaire au (c)) est devenu un CONTRÔLE RÉEL qui
  EXÉCUTE demo_patch (bavard=False) et exige son vert — la frontière
  reste NOMMÉE (le run terrain juge le scellage final) ; le libellé de
  conformite.txt suit (« la bascule PENDANT LE TRAFIC DÉMONTRÉE … le run
  terrain juge le scellage final ») ; la suite rejouée VERTE 7/7 (37
  contrôles).
- (3) LE KIT TERRAIN (unix/terrain/ + scripts/assembler_kit_m6d.py) :
  la cartouche PRÉ-ASSEMBLÉE au labo (la MÊME source que l'instrument
  de l'oracle, assemblée à l'ADRESSE FACTICE HAUTE 0x100000000000 qui
  FORCE la forme imm64 — une base 0 produirait l'imm32 TRONQUÉE, le
  piège nommé), RECOUPÉE contre l'instrument VIVANT octet pour octet
  (gabarit assemblé à l'adresse réelle == la page ; gabarit + le FIXUP
  UNIQUE [movabs r11, imm64 @ +0x6d, reposé AVANT le mprotect RX] ==
  l'instrument) ; le scénario GÉNÉRÉ depuis le gabarit .in (python3 +
  ctypes SEULEMENT — sha256 de la cartouche ASSERTÉ au démarrage), il
  rejoue T0 (témoin + empreinte) / T1 (rituel ×3 à l'ASLR du noyau +
  base figée si setarch) / T2 (les phases a/b/c + LE NOYAU DE LA MACHINE
  PARLE : cartographie partagée lecture seule → mprotect EACCES → code
  5, aucun shim) / T3 (zéro régression) et rend son verdict POST-MORTEM
  (preuves-m6/ : temoin, journal, VERDICT) ; le kit m6-kit/ (corpus +x,
  scénario, LISEZMOI) 46 568 o, sha256 98b8c1be…, md5 67b85983….
- (4) L'ÉPREUVE (la moitié du montage) : LA PREMIÈRE A ÉCHOUÉ NOMMÉ —
  la narration du scénario vivait sur fd 1, le canal même que la capture
  détourne : 102 o de narration DANS le flux mesuré (T2a 14 992 !=
  14 890) et un fragment littéral au trafic de l'ouvrier (T2b) ; le
  défaut était DANS L'INSTRUMENT (pas l'artefact), l'assertion
  octet-pour-octet l'a nommé au premier passage ; CORRIGÉ : la
  narration est DIFFÉRÉE pendant les fenêtres de capture (elle se rend
  à la sortie) ; la seconde épreuve (extraction VIERGE + run du kit
  EXACT) : VERT 16/16, rc 0, les trois pièces nées — le kit déposé est
  le kit prouvé.
- (5) LE COFFRE /test (scripts/deposer_kit_m6d.py, D143, idempotent) :
  la vague e4 CONSOMMÉE archivée (LISEZMOI-m5b-e4.txt, m5b-kit-e4.zip,
  scenario-m5b-e4.ps1 → vagues-m5b/, md5 constatés INTACTS — un
  déplacement, jamais un jet) ; l'index LISEZMOI-archives-livraisons
  mis à jour ; preuves-m6/ NÉ (LISEZMOI-preuves.txt : les pièces
  attendues) ; la vague déposée (kit-m6d.zip md5 67b85983… RECOUPÉ +
  LISEZMOI-m6d.txt) ; la racine vérifiée : 8 entrées (la vague m6d +
  les résidents D143 + les deux salles d'archive).
- (6) CONSIGNATIONS : fiche de profil § 5 (la démonstration ACQUISE),
  § 9 (la suite exécute la démo), § 10 (le kit LIVRÉ au coffre — le
  run VERT pose la finale) ; PLAN_MILESTONES § État du programme (le
  (d) partie laboratoire ACCOMPLIE, le kit au coffre, RESTE le run du
  développeur) ; JOURNAL_TRAVAIL +Entrée 148 PAR SCRIPT (ordre
  147<148<marqueur, rejeu REFUSÉ), DECISIONS +D153 PAR SCRIPT (à la
  suite de D152) ; ce worklog +Task ID 66 ; scripts suivis :
  assembler_kit_m6d.py, deposer_kit_m6d.py, inserer_entree_148.py,
  inserer_d153.py.
- FRONTIÈRES : l'artefact unix/corpus n'a pas bougé d'un octet (sha
  dd14195c… re-relu PAR la démonstration même) ; la carte vit SOUS
  0.7.0-rc.1 (re-signée sous sa balise par la re-vérification du
  geste — préservée) ; --sceller-final DISPONIBLE mais JAMAIS exécuté
  (le run terrain juge) ; scellé 0.6.0 + cartes m0-m5 + sceau ONZE
  arbres + arbres I + fixtures v5 + hachoir m6/ + sonde dev.1 INTACTS ;
  AUCUNE suppression Drive (l'archivage e4 est un DÉPLACEMENT), corbeille
  non vidée ; .keys/ gitignoré ; D139 ouverte non bloquante.
- SUITE : LE RUN DU DÉVELOPPEUR — extraire kit-m6d.zip dans un dossier
  NEUF, python3 scenario-m6d.py (WSL2 recommandé D149), renvoyer
  preuves-m6/ au coffre /test/preuves-m6/ ; le labo recoupe (D138/D145/
  D148) et si le critère est établi : --sceller-final pose la FINALE
  0.7.0 (le jalon M6 franchi) ; puis M7 (l'ISA : l'assembleur RV64
  maison ou moteur tiers, qemu-riscv64, la TROISIÈME instanciation).

Stage Summary:
- Le chantier M5-(c) est REFERMÉ au labo : la bascule du journal PENDANT
  le trafic est démontrée SUR PIÈCES — entre deux usages (V5), sous
  concurrence réelle (Q3), le journal cohérent octet pour octet, le
  rollback en pleine session, la zéro régression — sur l'artefact scellé
  0.7.0-rc.1 relu, le fichier jamais touché.
- La suite de conformité EXÉCUTE la démonstration : le critère vit dans
  le témoin de jalon, le scellage final le re-prouvera à chaque passage.
- Le kit terrain Linux est AU COFFRE /test (vague m6d) : le scénario
  AUTONOME (python3 + ctypes, la cartouche du labo recoupée octet pour
  octet), ÉPROUVÉ par extraction vierge — la première épreuve a nommé
  la pollution du flux mesuré par la narration de l'instrument (D153 :
  le flux mesuré n'est à personne ; un livrable ne se dépose que vert à
  l'extraction vierge).
- RESTE LE RUN DU DÉVELOPPEUR : le seul juge du scellage final 0.7.0.

- PASSATION D141 rejouée au geste « chantier M6-(d), partie laboratoire
  accomplie / la démonstration M5-(c) verte + le kit terrain m6d au
  coffre » : le bundle courant triade-history-060-a581d1e.bundle (git
  bundle --all, 15 759 307 o, md5 3fc639bc…) déposé au MIROIR, ASSERTÉ
  avant dépôt (branche jalon pointe sur a581d1e — il porte LE QUATRIÈME
  GESTE DU JALON M6 AVEC sa consignation : la démonstration M5-(c)
  refermée unix/demo_patch.py [la bascule pendant le trafic V5, la
  concurrence réelle Q3, le journal cohérent octet pour octet, le
  rollback, la zéro régression — sur l'artefact scellé relu, CINQ
  passages 5/5 verts] + la suite de conformité qui EXÉCUTE désormais la
  démonstration [l'élément 5 devenu CONTRÔLE RÉEL, VERTE 7/7 — 37
  contrôles] + LE KIT TERRAIN unix/terrain/ [le scénario AUTONOME
  python3/ctypes, la cartouche pré-assemblée à l'adresse factice HAUTE
  recoupée contre l'instrument VIVANT de l'oracle OCTET POUR OCTET,
  relogée au terrain par le fixup imm64 unique ; le kit ÉPROUVÉ PAR
  EXTRACTION VIERGE : VERT 16/16 — la première épreuve a nommé la
  pollution du flux mesuré, D153] + le dépôt au coffre /test [la vague
  m6d : kit-m6d.zip md5 67b85983… + LISEZMOI-m6d.txt + preuves-m6/ né ;
  la vague e4 consommée archivée D143 md5 intacts] + Entrée 148 + D153 +
  worklog Task 66) ; l'ancien 060-5328156 (md5 e15e2c2f… recoupé AVANT)
  ARCHIVÉ VERSIONNÉ dans archives-bundles/ (14 archives, jamais
  supprimé) ; /test sans copie de bundle (recoupé) ; GitHub porté à la
  pointe dans le même geste (push 402508f..a581d1e, recoupé ls-remote) ;
  script suivi : passe_bundle_m6d.py ; FRONTIÈRES : aucune suppression
  (l'archivage est un déplacement), la carte du corpus vit SOUS 0.7.0-
  rc.1 (INTACTE — la re-vérification du geste l'a re-signée sous sa
  balise), l'artefact sha dd14195c… IMMUEABLE, le scellage final 0.7.0
  attend le run terrain vert du développeur (le kit m6d est AU COFFRE).

## Task ID 67 — « preuves déposées dans le dossier /test du drive » : LE JALON M6 FRANCHI — LE RUN TERRAIN M6-(d) VERT SUR PIÈCES (le kit m6d exécuté par la machine du développeur : WSL2, noyau 6.18.54.1-microsoft-standard-WSL2 — UN AUTRE noyau que celui du labo, ASLR complet randomize_va_space=2, le scellé relu dd14195c… avant tout geste, 16/16 constats PASS ; le premier geste du développeur, lancé sous Windows natif, était mort NOMMÉ AVANT T0 — libc.so.6 introuvable : le fail-closed tient hors terrain) ; LE RECOUP LABO VERT 22/22 SUR PIÈCES CROISÉES (scripts/recouper_preuves_m6d.py + scripts/recouper_run_m6d.py : les trois pièces md5 contrôlés contre le coffre, témoin ↔ journal ↔ verdict recoupés ENTRE EUX, l'arithmétique RECOMPTE [800+400==1200 ; 778+560==1338 ; 14 890 o émis == attendus], les constats vérifiés contre la SOURCE du scénario, le noyau CONSTATÉ distinct, l'artefact RECALCULÉ au geste même — le premier passage avait ÉCHOUÉ NOMMÉ : le défaut était dans l'INSTRUMENT du recoup, arguments inversés, corrigé et rejoué, les pièces immuables) ; LA FINALE 0.7.0 SCELLÉE au geste même (--sceller-final : D146 adapté vert + cristallisation 13×10/10 + conformité 7/7 AU geste — la suite EXÉCUTANT la démonstration M5-(c) — bascule rc.1→0.7.0 dans frag-bld occurrence unique assertée, re-scellage vérifié en mémoire avant l'unique écriture, verrou croisé 13/13, l'artefact INTACT sha dd14195c… — le scellage est un fait de carte) ; LES TROIS GARDES VIVANTES (re-scellage REFUSÉ, reconstruction REFUSÉE, la balise 0.7.0 PRÉSERVÉE par la re-vérification — oracle 76 631 cas verts) ; D154 née (05/11)

**Détail.** Les trois pièces (temoin-m6d.txt b425e831…, scenario-m6d-journal.log
87d340d7…, VERDICT-run-m6d.txt 28345bce…) rapatriées md5 contrôlés vers
download/preuves-run-m6d/ (D99) ; le recoup fail-closed rend son verdict ÉCRIT
(VERDICT-recoup-m6d.txt) ; la finale scellée, le tableau de bord suit
(jalon=M6 artefact=corpus version=0.7.0) ; consignations : Entrée 149 PAR
SCRIPT, D154 PAR SCRIPT, PLAN § État du programme + la ligne M6 du tableau
(FRANCHI 05/11 — balise finale 0.7.0) + la ligne (c) M5 refermée,
PROTOCOLE_TRIADE en-tête + § 18 (M0–M6 franchis, M7 DÉBLOQUÉ), fiche de
profil § 8 (balise SCELLÉE + ACQUIS la finale) + § 10 (ACQUIS le run venu et
vert) ; le PDF formel v0.6.1 BYTE-IDENTIQUE (l'état des jalons vit aux sources
de travail — addendum Task 62) ; le LISEZMOI-preuves.txt du réceptacle /test
(disparu au dépôt des pièces) RESTAURÉ par deposer_kit_m6d.py idempotent ; la
vague m6d DEMEURE courante au coffre (la clôture D143 des pièces — leur
déplacement vers archives-preuves/preuves-run-m6d/ avec le verdict du recoup —
attend le dépôt du kit M7, modèle e4) ; scripts suivis :
rapatrier_preuves_m6d.py, recouper_run_m6d.py, inserer_entree_149.py,
inserer_d154.py, passe_bundle_m6final.py ; livrables :
download/preuves-run-m6d/ (les trois pièces + VERDICT-recoup-m6d.txt),
unix/carte-corpus/ (la balise 0.7.0).

- SUITE : LE JALON M7 — la portabilité inter-ISA (l'assembleur RV64IMA+Zifencei
  maison ou un moteur tiers à la même porte, qemu-riscv64 à installer avec
  réserve instrumentale nommée, la TROISIÈME instanciation de la MÊME couche I
  dans riscv/, le patch scratch+fence.i, le verrou multi-profils, la finale
  0.8.0) ; la fiche docs/PROFIL_riscv64-linux-elf64.md attend son premier
  octet.

- PASSATION D141 rejouée au geste « JALON M6 FRANCHI / le run terrain VERT
  sur pièces + la finale 0.7.0 scellée » : le bundle courant
  triade-history-070-642e5b8.bundle (git bundle --all, 15 801 591 o, md5
  91c47a53…) — PREMIER DE LA SÉRIE 070 (l'ère de la balise 0.7.0) — déposé
  au MIROIR, ASSERTÉ avant dépôt (branche jalon pointe sur 642e5b8 — il
  porte LE GESTE QUI FRANCHIT LE JALON M6 AVEC sa consignation : le run
  terrain de la machine du développeur [WSL2, noyau
  6.18.54.1-microsoft-standard-WSL2 UN AUTRE que celui du labo, ASLR
  complet, VERT 16/16 — le premier geste hors terrain mort NOMMÉ avant
  T0, D154] + LE RECOUP LABO 22/22 sur pièces croisées [l'instrument du
  recoup corrigé sur pièces après son ÉCHEC NOMMÉ, les pièces immuables]
  + LA FINALE 0.7.0 SCELLÉE [D146 + cristallisation 13×10/10 + conformité
  7/7 au geste même, la bascule rc.1→0.7.0 dans frag-bld, verrou croisé
  13/13, l'artefact INTACT dd14195c…] + les gardes vivantes + Entrée 149
  + D154 + worklog Task 67) ; l'ancien 060-a581d1e (md5 3fc639bc…
  recoupé AVANT) ARCHIVÉ VERSIONNÉ dans archives-bundles/ (15 archives,
  jamais supprimé) ; /test sans copie de bundle (recoupé) ; GitHub porté
  à la pointe dans le même geste (push, recoupé ls-remote) ; script suivi
  : passe_bundle_m6final.py ; FRONTIÈRES : aucune suppression (l'archivage
  est un déplacement), la carte du corpus vit SOUS 0.7.0 (INTACTE — le
  scellage est un fait de carte), l'artefact sha dd14195c… IMMUABLE, le
  jalon M7 est DÉBLOQUÉ (la fiche riscv64 attend son premier octet).

## Task ID 68 — « continue M7 » : LE CHANTIER M7-(a) ACCOMPLI — LE MOTEUR DE NOTATION RV64 NÉ ET ÉPROUVÉ : l'ASSEMBLEUR RV64IMA+Zifencei MAISON DU DÉPÔT (riscv/outils/as_rv64.py : six formats R/I/S/B/U/J, 4 o exactement, SANS extension C, refus nommés fail-closed, le jeu EXACT des pseudos du juge) ; LA PORTE ROUND-TRIP EN DEUX DIRECTIONS (riscv/notation/porte_roundtrip.py : 783 textes du corpus du profil en AVANT + 1037 encodages légaux en INVERSE — le rendu INTÉGRAL du juge ré-assemble en ses octets, capstone 5.0.7 JUGE UNIQUE, 100 %) ; QEMU-RISCV64 OPÉRATIONNEL AU LABO (l'installation devient une PROCÉDURE du dépôt : riscv/outils/installer_qemu.sh, extraction locale SANS privilèges du paquet qemu-user statique 10.0.13 — le binaire instrument gitignoré sous riscv/.tmp/) ; LA LIGNÉE riscv/ NÉE (layout D8 en GÉOMÉTRIE MIROIR du plan unix — seul le demi-octet ISA change : e_machine 0xF3, e_flags 0, NOP canonique addi x0,x0,0, réserves ebreak ; quatre specs sr-01..04 ÉCRITES-AVANT-CODE, les miroirs de su-01..04 : l'ancrage auipc+addi remplace le lea rip, t1 remplace r10/r11, le cadre de .emit SAUVE ra) ; LA SONDE ET_DYN/PIE EM_RISCV 8 192 o sha d122bc68… À L'ORACLE QEMU VERT (6/6 runs — quatre lignes octet pour octet, code 6, table ERRNOS exercée sur ses DEUX branches, falsification 12/12 zéro silence) ; L'INDIFFÉRENCE À LA BASE DÉMONTRÉE PAR BASES FORCÉES DU CHARGEUR (-R 1G→0x2aaac000, -R 4G→0xaaaac000, -B+-R→0x55556000, TOUTES VERTES — la base par défaut CONSTANTE 0x555555556000 est un CONSTAT d'instrument nommé, l'épreuve -B a mort nommée avant d'être instruite) ; LA GARDE ANTI-TABLE-X86 VIVANTE (a7=1 write x86-64 : REFUS DE BUILD NOMMÉ) ; LA CARTE génération 1 (QUATRIÈME sel, verrou croisé 4/4) ; LA BALISE 0.8.0-dev.1 POSÉE par le premier build du jalon (geste de BUILD, jamais de scellage) ; D155 née (05/11)

**Détail.** Les constats de la fiche re-vérifiés AU GESTE MÊME (keystone
SANS RISC-V re-constaté, capstone RV64 confirmé, qemu installé par
PROCÉDURE) ; l'assembleur maison éprouvé par la porte — QUATRE leçons
attrapées au geste même (negw manquant, funct7 de SEPT bits des décalages
W, jalr deux-opérandes mémoire, fence « unknown » aux champs vides),
toutes par la direction INVERSE (D155 : la direction avant ne prouve que
les prévisions de l'auteur) ; l'oracle structurel 219 verrous (appels/
syscalls/données déclarés PAR BLOC, paires d'ancres re-vérifiées DEPUIS
LE CODE DÉSASSEMBLÉ, taille 4 par instruction — garde anti-C, pile psABI
appariée, t1 respecté par contrat, 22 symboles confrontés au layout —
leçon C1, l'auteur a aussi attrapé sa propre paire d'ancre : le LO
s'administre relativement à SON auipc, jamais isolément) ; le
déterminisme constaté au rebuild (sha d122bc68… constant) ; la
re-vérification complète rejouée (R5/R8 verts, cristallisation 2/10 par
bloc) ; consignations : Entrée 150 PAR SCRIPT, D155 PAR SCRIPT, fiche
riscv64 § statut/§ 6/§ 8/§ 10 (constats re-vérifiés + ACQUIS + le constat
d'instrument qemu), PLAN § État du programme (M7-(a) RÉALISÉ) ; le PDF
formel v0.6.1 BYTE-IDENTIQUE (l'état des jalons vit aux sources de
travail — addendum Task 62) ; le coffre /test INCHANGÉ (la vague m6d
demeure courante — la clôture D143 attend le kit M7) ; frontières : la
finale 0.7.0 et sa carte INTACTES, le corpus dd14195c… et la sonde unix/
INTACTS (la géométrie miroir est un PLAN partagé, jamais un octet
partagé), riscv/.tmp/ gitignoré, .keys/ gitignoré, D139 ouverte non
bloquante ; scripts suivis : inserer_entree_150.py, inserer_d155.py,
passe_bundle_m7a.py.

Stage Summary:
- Le jalon M7 a son moteur de notation : l'assembleur maison du dépôt,
  admis par la porte round-trip à 100 % en DEUX directions — la
  direction inverse (l'espace d'encodage légal) est la preuve, quatre
  leçons y ont été attrapées au geste même (D155).
- qemu-riscv64 est opérationnel au labo et son installation est une
  PROCÉDURE du dépôt ; la sonde EM_RISCV est VERTE sous l'exécuteur du
  jalon (réserve instrumentale D149 nommée dans chaque verdict), et
  l'indifférence à la base est démontrée par les paramètres du CHARGEUR —
  jamais en feignant un ASLR émulé.
- La balise 0.8.0-dev.1 est posée (geste de BUILD) ; le scellage
  0.8.0-rc.1 attendra le chantier (c) et son contrôle D146 adapté.

- SUITE : LE CHANTIER M7-(b) — la TROISIÈME instanciation de la même
  couche I : le corpus paritaire RISC-V (les MÊMES fichiers I que unix/,
  le diff nul mesuré par script, l'oracle régénéré vert sur l'instance
  qemu, la parité § 8.3 sur les TROIS profils) ; le point d'attention
  NOMMÉ : la portée imm12 des charges — le corpus unix accédait ses
  données par [rbx+disp32], l'instance RISC-V porte ses fenêtres par
  ANCES auipc+addi (le modèle des paires sr-04 généralisé, chaque fenêtre
  déclarée en I3) ; puis (c) le patch scratch+fence.i + le verrou
  multi-profils, (d) l'export multi-profils + le terrain → la finale
  0.8.0.

- PASSATION D141 rejouée au geste « CHANTIER M7-(a) ACCOMPLI / le moteur
  de notation RV64 né et éprouvé » : le bundle courant
  triade-history-070-f8472c6.bundle (git bundle --all, 15 878 588 o, md5
  845adafd…) déposé au MIROIR, ASSERTÉ avant dépôt (branche jalon pointe
  sur f8472c6 — il porte LE PREMIER CHANTIER DU JALON M7 AVEC sa
  consignation : l'assembleur RV64IMA+Zifencei MAISON du dépôt + la PORTE
  round-trip 783+1037 à 100 % en deux directions [capstone juge unique]
  + qemu-riscv64 OPÉRATIONNEL par PROCÉDURE du dépôt + la lignée riscv/
  née [layout géométrie miroir, quatre specs écrites-avant-code] + la
  sonde ET_DYN/PIE EM_RISCV sha d122bc68… à l'oracle qemu VERT 6/6 +
  falsification 12/12 + l'indifférence à la base DÉMONTRÉE par bases
  forcées du chargeur + la garde anti-table-x86 vivante + la balise
  0.8.0-dev.1 posée par le premier build du jalon + Entrée 150 + D155 +
  worklog Task 68) ; l'ancien 070-642e5b8 (md5 91c47a53… recoupé AVANT)
  ARCHIVÉ VERSIONNÉ dans archives-bundles/ (16 archives, jamais supprimé)
  ; la série DEMEURE 070 (l'ère de la balise 0.7.0 scellée — la série 080
  naîtra à la finale 0.8.0 du jalon) ; /test sans copie de bundle
  (recoupé) ; GitHub porté à la pointe dans le même geste (push f07d11c..
  f8472c6, recoupé ls-remote) ; le premier jet du passeur a été REFUSÉ
  NOMMÉ par SA PROPRE assertion (BUNDLE-TETES : le sha complet attendu
  avait été fabriqué au lieu d'être lu — corrigé sur pièces, la garde
  vivait) ; script suivi : passe_bundle_m7a.py ; FRONTIÈRES : aucune
  suppression (l'archivage est un déplacement), la finale 0.7.0 et sa
  carte INTACTES, le coffre /test INCHANGÉ (la vague m6d demeure
  courante — la clôture D143 attend le kit M7).


## Task ID 69 — « continue » : LA RECOUPURE POST-MORTEM DES DÉCISIONS D138/D145/D148 ACCOMPLIE — les TROIS décisions FIDÈLES à leurs pièces originales (v6 : 28 pièces ; e2 : 7 ; e4 : 37 re-contrôlées ; v8 : la matrice S3 ciblée — RAPATRIÉES des archives du coffre md5 contrôlés, LECTURE SEULE) : chaque fait fondateur RETROUVÉ SUR PIÈCE mot pour mot (page-d2b 279 o + marqueur + identique v6/e4 ; l'étiquette « ECHEC … rc=0 » ; les lectures in-VM «  » vides ; AUTORITE-B « arret propre — motif=delai » contre rc capturé vide ; AUTORITE-A jamais arrêtée ; le REFUS PROXY-SANS-ARMEMENT sur lecture 0 o ; la sonde TCP 00:13:17 ; la pièce post-mortem 128 o / 7 lignes avec « relever-https arme » en ligne 2 ; « ÉCHEC NOMMÉ (5) » et les CINQ refus aux noms exacts ; le rc d'Edge capturé VIDE ; dom-b 0 o + nav-b.png ABSENTE ; la réception triplement recoupée certificat rejete + s=34 + poignee refusee + ERR_HTTP_RESPONSE_CODE_FAILURE ; le libellé « REGRESSION a nommer » SUR PIÈCE) ; UNE PRÉCISION NOMMÉE sur la formulation D148 (la pièce T2b curl-d2b.txt porte la Date du run — pièce CRLF 946 o, trois md5 distincts, la seule ligne divergente entre v6/v8/e4 : l'identité octet pour octet vaut pour d2a/d3/d5 + hosts-lu, pour d2b elle vaut SAUF la ligne Date — la stationnarité S3 CONFIRMÉE EN SUBSTANCE, la précision consignée append-only, la règle D148 inchangée) ; l'instrument du recoup CORRIGÉ SUR PIÈCES après son ÉCHEC NOMMÉ (trois défauts d'instrument : l'extra LISEZMOI nommé, la matching sur texte APLATI, la ligne Date à l'index 24 et non 17 — pièce CRLF — le second passage VERT, les pièces immuables, D154 étendue au recoup de doctrine) (05/11)

**Détail.** La reprise a suivi l'ordre promis : l'état du labo re-vérifié au geste
même (porte 783+1037 VERT, build sha d122bc68… constant, sonde qemu 6/6 code 6,
corpus unix dd14195c… intact, coffre /test recoupé — la vague m6d demeure
courante) ; les décisions D138-D155 relues sur pièces (DECISIONS.md, jamais de
mémoire) ; puis le rapatriement (rapatrier_preuves_doctrine.py — lecture seule,
aucune écriture au coffre, le coffre fait foi) et le recoup
(recouper_doctrine_post_mortem.py — verdict écrit à côté des pièces :
download/recoup-post-mortem/VERDICT-recoup-doctrine.txt). Consignations :
Entrée 151 PAR SCRIPT ; frontières : aucune pièce modifiée (md5 contrôlés aux
deux passages), le coffre INCHANGÉ, download/ hors dépôt git (modèle
preuves-run-m6d), aucune passation (pas un geste de jalon) ; scripts suivis :
rapatrier_preuves_doctrine.py, recouper_doctrine_post_mortem.py,
inserer_entree_151.py ; livrables : download/preuves-run-{v6,e2,v8,e4}/ +
download/recoup-post-mortem/VERDICT-recoup-doctrine.txt.

- SUITE : LE CHANTIER M7-(b) — la TROISIÈME instanciation de la même couche I :
  le corpus paritaire RISC-V (les MÊMES fichiers I que unix/, le diff nul mesuré
  par script, l'oracle régénéré vert sur l'instance qemu, la parité § 8.3 sur
  les TROIS profils, la garde anti-table-x86 au corpus entier) ; le point
  d'attention NOMMÉ : la portée imm12 des charges — les fenêtres par ANCES
  auipc+addi (le modèle des paires sr-04 généralisé, chaque fenêtre déclarée
  en I3) ; puis (c) le patch scratch+fence.i + le verrou multi-profils,
  (d) l'export multi-profils + le terrain → la finale 0.8.0 (le terrain sera
  jugé POST-MORTEM ET SUR PIÈCES — D138/D145/D148, ré-établis sur originaux
  par la présente recoupure).


## Task ID 70 — « lance le » : LE CHANTIER M7-(b) ACCOMPLI — LE CORPUS PARITAIRE RV64, LA TROISIÈME INSTANCIATION DE LA MÊME COUCHE I : les DOUZE blocs du patrimoine (hello-02/03, libc-01..08, tcp-07/11) + corpus-13, LA NOTATION RV64 NATIVE de 523 instructions (round-trip 100 %, capstone juge unique, graphie canonique du juge) ; L'INSTANCE CHARGE LES MÊMES FICHIERS CANONIQUES de unix/I/ (13 specs, empreintes mesurées, AUCUNE copie — le diff nul VERT en 4 recoupements : les canoniques, les observables R1↔R+1 par la chaîne M6 REJOUÉE, 7 scellés octet-identiques à l'état zéro, la parité § 8.3) ; L'ORACLE QEMU VERT SUR PIÈCES (réserve instrumentale D149 — TCG, noyau et syscalls réels) : le RITUEL DE PARITÉ 6/6 — les DEUX lignes octet pour octet (« TRIADE M1 : minilibc 21/21 OK\n » puis « corpus : autotest 21 vecteurs\n ») code 0 — LA PARITÉ § 8.3 PAR EXÉCUTION sur les TROIS profils ; LES BASES FORCÉES du CHARGEUR (-R 1G / -R 4G / -B+-R 2G) VERTES (indifférence à la base) ; LA FALSIFICATION 13 mutations 12/12 blocs rompus (zéro silence ; tcp-07 hors-chemin du rituel, son scénario est le chantier (c)) ; 1535 VERROUS STRUCTURELS (appels/syscalls/données déclarés PAR BLOC, la GARDE ANTI-TABLE-X86 vivante — write 64, mprotect 226, exit_group 94 asm-generic, les numéros 1/10/231 REFUSÉS nommément) ; QUATRE LEÇONS DU GESTE, toutes attrapées par les gardes au PREMIER passage (D156) (05/11)

**Détail.** LA GÉOMÉTRIE MIROIR du plan unix (D8) : les MÊMES RVA (blocs
0x1000-0x1D80, croissance 0x1D80 en réserve ebreak), les MÊMES fixtures au
même plan, les MÊMES séries (f70xxxx à la sonde, f71xxxx au corpus) ;
l'artefact `riscv/corpus` 12 288 o sha256 b34a7147…, DÉTERMINISME constaté
au rebuild ; le staging (journal v2 « j2: », 248 o qword-paddé ebreak)
assemblé POUR la croissance 0x1D80, la table d'intégrité R10 le porte en
première entrée (somme 0x27ddc53f… — la porte AVANT tout effet) ; le verrou
tournant amoswap.d (l'extension A du profil — le portage du lock x86-64),
la restitution sd simple (mono-fil, fiche § 5) ; tcp-07 instancié avec LA
SÉQUENCE du profil (fiche § 5 : mprotect RW → copie → fence rw,rw → LA
BASCULE un mot jal CONSTRUITE EN REGISTRES → fence.i → RX, .protger local
en jal) ; LA LEÇON imm12 (D156) : le verrou 0x3800 vu de la base .bss
0x3000 vivait à +0x800 = 2048 — HORS imm12 DE UN, le REFUS NOMMÉ d'as_rv64
au premier geste ; la fenêtre s'est posée AU CENTRE (s2 = base+0x3400 :
curseur -0x400, arène -0x3C0, verrou +0x400) ; le PIÈGE AMO : l'ISA AMO
adresse [rs1] SANS déplacement (funct5 aux bits 31:27) — le premier jet
encodait la demande en ignorant le déplacement (un octet qui n'est pas
celui demandé, l'espèce la plus grave) : REFUS NOMMÉ posé, le déplacement
vit dans la formation addi déclarée ; le RECYCLAGE s3 : la fenêtre de
tcp-07 ET l'ardoise de tcp-11 — l'oracle a refusé (s3+4 non déclaré), les
rôles dédiés (s1/s2 fenêtres GLOBALES, s3 fenêtre PRIVÉE de tcp-07, s0/s7
ardoises sauvegardées, t1 jamais touché) ; LA PORTE A GRANDI : l'extension
A amoswap.w/d entre à la porte DU MÊME GESTE (AVANT 783→791 textes, INVERSE
1037→1045 encodages — les autres AMO et aq/rl armés vivent hors instrument,
frontière nommée) ; consignations : Entrée 152 PAR SCRIPT, D156 PAR SCRIPT
(à la suite de D155), fiche riscv64 (statut + § 6 la porte étendue + § 8 la
balise + § 10 l'oracle corpus), PLAN § État du programme (M7-(b) RÉALISÉ),
riscv/I/README.md (la section corpus — la table des 13 blocs, la leçon
imm12) ; la re-vérification complète rejouée (R5/R8 verts, cristallisation
2/10 par bloc) ; la carte génération 1 au SIXIÈME sel (m2, hachoir D34,
sonde unix, corpus unix, sonde riscv, corpus riscv — clés projet partagées
D27), frag-con TROIS PROFILS par bloc (§ 8.3-4 — la TROISIÈME colonne psABI
est née), verrou croisé 13/13 ; LA BALISE 0.8.0-dev.2 POSÉE par le build du
corpus (geste de BUILD, jamais de scellage — le scellage 0.8.0-rc.1 viendra
du chantier (c) avec le contrôle D146 adapté à l'exécuteur du jalon) ;
frontières : la sonde d122bc68… INTACTE (le corpus ne la touche pas), le
corpus unix dd14195c… INTACT (la TROISIÈME instanciation ne touche pas la
seconde), les cinq scellés Windows INTACTS, le coffre /test INCHANGÉ (la
vague m6d demeure courante — la clôture D143 attend le kit M7), riscv/.tmp/
gitignoré, .keys/ gitignoré ; scripts suivis : riscv/build_corpus.py,
riscv/diff_nul_corpus.py, riscv/carte_corpus.py, outils/auteur.py
(--corpus), notation/porte_roundtrip.py (AMO), inserer_entree_152.py,
inserer_d156.py ; livrables : riscv/corpus, riscv/carte-corpus/,
riscv/notation/ (13 blocs + staging v2).

Stage Summary:
- La TROISIÈME instanciation de la même couche I est UN FAIT MESURÉ : les
  13 specs sont LES MÊMES FICHIERS (empreintes, zéro copie), l'observable
  du patrimoine est LE MÊME EN EXÉCUTION (« TRIADE M1 : minilibc 21/21
  OK » octet pour octet sous qemu — § 8.3 PAR EXÉCUTION, jamais par
  déduction).
- QUATRE leçons du geste, toutes attrapées par les gardes au PREMIER
  passage (D156) : la fenêtre .bss se pose AU CENTRE (la portée imm12 est
  une contrainte de PLACE du plan) ; l'AMO adresse [rs1] sans déplacement
  (le refus nommé, jamais l'octet silencieux) ; les registres sont dédiés
  par rôle (s3 la fenêtre de tcp-07, jamais l'ardoise de tcp-11) ; la
  porte grandit avec l'instrument (amoswap 791+1045 aux deux directions).
- La balise 0.8.0-dev.2 est posée (geste de BUILD) ; le scellage 0.8.0-rc.1
  attendra le chantier (c) et son contrôle D146 adapté à l'exécuteur.


- PASSATION D141 rejouée au geste « CHANTIER M7-(b) ACCOMPLI / le corpus
  paritaire RV64, la TROISIÈME instanciation de la même couche I » : le
  bundle courant triade-history-070-09ddd06.bundle (git bundle --all,
  16 000 761 o, md5 9c7461a3…) déposé au MIROIR, ASSERTÉ avant dépôt
  (branche jalon pointe sur 09ddd06 — il porte LE SECOND CHANTIER DU
  JALON M7 AVEC sa consignation : le corpus paritaire RV64 [les DOUZE
  blocs du patrimoine + corpus-13, la notation native 523 instructions
  round-trip 100 % ; l'instance CHARGE les MÊMES FICHIERS CANONIQUES de
  unix/I/, zéro copie — le diff nul VERT 4 recoupements ; l'oracle qemu
  VERT SUR PIÈCES : rituel 6/6 les DEUX lignes octet pour octet code 0 —
  LA PARITÉ § 8.3 PAR EXÉCUTION sur les TROIS profils ; bases forcées
  VERTES ; falsification 12/12 zéro silence ; 1535 verrous, la garde
  anti-table-x86 vivante ; les QUATRE leçons D156 ; l'artefact sha
  b34a7147… DÉTERMINISME au rebuild ; la carte au SIXIÈME sel, frag-con
  TROIS PROFILS ; la balise 0.8.0-dev.2] + Entrée 152 + D156 + worklog
  Task 70) ; l'ancien 070-f8472c6 (md5 845adafd… recoupé AVANT) ARCHIVÉ
  VERSIONNÉ dans archives-bundles/ (17 archives, jamais supprimé) ; la
  série DEMEURE 070 (l'ère de la balise 0.7.0 scellée — la série 080
  naîtra à la finale 0.8.0 du jalon) ; /test sans copie de bundle
  (recoupé) ; GitHub porté à la pointe dans le même geste (push
  4b5d7fd..09ddd06, recoupé ls-remote) ; script suivi :
  passe_bundle_m7b.py.
- SUITE : LE CHANTIER M7-(c) — le patch scratch+fence.i EN DÉMONSTRATION
  (apply/effet/rollback sous qemu, l'intégrité R10, les refus nommés 1-5,
  le DEP falsifié) + le verrou multi-profils ; puis (d) l'export
  multi-profils + le terrain → la finale 0.8.0 (le terrain sera jugé
  POST-MORTEM ET SUR PIÈCES — D138/D145/D148, ré-établis sur originaux).


## Task ID 71 — « synchro git et drive puis continue » : LE CHANTIER M7-(c) ACCOMPLI — LE PATCH fence.i DÉMONTRÉ EN EXÉCUTION + LE VERROU MULTI-PROFILS + LE SCELLAGE 0.8.0-rc.1 : LA SYNCHRO vérifiée SUR PIÈCES (git propre, pointe 6d1b8dd == ls-remote ; Drive série versionnée [070-09ddd06], 17 archives, /test vague m6d courante — le vestige triade-history.bundle pré-D141 hors série, toléré) ; LE DÉMONSTRATEUR INVITÉ `riscv/demo` (f72001 demo-patch, 191 instructions, 764 o, à 0x2000 dans la réserve RX — LES MÊMES blocs du corpus + le démonstrateur, le modèle unix/demo_patch.py PORTÉ EN INVITÉ : sous qemu le scénario vit DANS l'invité) : LA BASCULE PENDANT LE TRAFIC — 1 200 usages de l'ENTRÉE du journal, l'apply ENTRE 399/400, le rollback ENTRE 799/800, la transcription OCTET POUR OCTET (15 425 o), 800 v1 + 400 v2 (marque j2:), L'EFFET AU GESTE MÊME (j2: verdict 12 o / verdict 8 o), le retour à l'état image (entrée == ENTREE_SAUVEE, remplaçant DORMANT, verrou rendu), LES REFUS 1/2/3/4 (l'absent et la somme par mutation IN-GUEST de la table R10 — mprotect par le démonstrateur, restaurée), LE DEP FALSIFIÉ (0x7→0x3 : SIGSEGV au premier apply, 4 290 o EXACTS), la falsification du démonstrateur (rompu essai 1), LES BASES FORCÉES (transcription identique), ZÉRO RÉGRESSION (corpus relu + rituel rejoué) ; LA CORRECTION tcp-07 (D157) : le PORT avait OUBLIÉ le marshalling du prot (.protger ne passait jamais a2 — mprotect recevait 0xB de débris, la page perdait son bit X, ACCERR) — nommé au premier apply par la démonstration, la pièce par QEMU_STRACE (PROT_SEM — un prot dans AUCUN plan), UNE ligne (`mv a2, t2` — l'équivalent du mov rdx, rdi x86-64), le corpus REBUILDÉ sha256 ec343b4e… (b34a7147… demeure le record de l'Entrée 152 — append-only) ; QUATRE leçons (D157 : le port n'est conforme que CHEMIN RÉEL exécuté ; le journal de l'exécuteur est une PIÈCE ; le sous-programme qui appelle SAUVE ra — .dire ; D150 réapprise — s10 l'attendu, t0 recalé) ; LE VERROU CROISÉ MULTI-PROFILS VIVANT (26 empreintes DEUX ISA AVANT l'édition, la géométrie miroir [spec/rva/slot identiques], la couche I partagée [13 fichiers mêmes empreintes aux deux cartes], les artefacts voisins intacts) ; LE CONTRÔLE D146 ADAPTÉ VERT (riscv/controle_base_reelle.py : la base CONSTATÉE PAR TRACE in_asm — le premier bloc - e_entry : 0x555555556000 ×6, D155 confirmé ; -R 1G/4G, -B+-R 2G distinctes, transcription identique) ; LA CONFORMITÉ § 8.2 VERTE 7/7 (riscv/conformite_profil.py — 29 contrôles PASS, les éléments constatés depuis l'artefact, la suite EXÉCUTANT le scénario à l'élément 5) ; LA CRISTALLISATION conduite à 10/10 (9 passes) ; SCELLAGE 0.8.0-rc.1 (le verrou multi-profils AVANT l'édition, D146, R6, 7/7 ; la bascule dans frag-bld vérifiée EN MÉMOIRE avant l'unique écriture ; l'ARTEFACT INTACT — le scellage est un fait de carte) ; LES TROIS GARDES VIVANTES (re-scellage REFUSÉ « 0 occurrence », reconstruction REFUSÉE « carte scellée », la re-vérification PRÉSERVE la balise) (05/11)

**Détail.** La séquence du profil (fiche § 5) aux octets ET en exécution :
mprotect RW (bit X RETENU — D39) → copie → fence rw,rw → LA BASCULE UN mot
(jal construit en registres) → fence.i → RX ; le verrou tournant amoswap.d
(mono-fil — fiche § 5 : la concurrence HORS périmètre nommée) ; FRONTIÈRES :
code 5 STRUCTUREL sous qemu (l'hôte accorde RWX sur mapping privé — la
branche fail-closed vit dans le bloc) ; le demo n'est PAS un artefact de la
lignée (pas de carte — l'instrument du chantier, modèle demo_patch.py) ;
l'incident des reproducers (trois images roulées à la main ont failli faire
nommer une réserve d'instrument qui n'existait pas — le mprotect invité
fonctionne PARFAITEMENT sous qemu : l'isolement se mène sur l'image de la
FAMILLE, D157) ; consignations : Entrée 153 PAR SCRIPT, D157 PAR SCRIPT (à
la suite de D156), fiche riscv64 (§ 8 la rc.1 scellée + § 9 l'élément 5
ACQUIS + § 10 le journal de l'exécuteur), PLAN § État (M7-(c) RÉALISÉ) + la
ligne M7 du tableau (les chantiers (a)(b)(c) réalisés, reste (d)) ; la carte
du corpus vit SOUS 0.8.0-rc.1, la cristallisation 10/10, le verrou croisé
13/13 ; livrables : riscv/demo (sha e57fc74b…), riscv/demo_patch.py,
riscv/verrou_multi_profils.py, riscv/controle_base_reelle.py,
riscv/conformite_profil.py (+ conformite.txt), le corpus REBUILDÉ (sha
ec343b4e…), la notation demo-patch (brouillon + générée) ; scripts suivis :
inserer_entree_153.py, inserer_d157.py.

Stage Summary:
- LA SÉQUENCE scratch+fence.i est DÉMONTRÉE EN EXÉCUTION sous qemu — la
  bascule pendant le trafic, 1200 usages, la transcription byte-exact : le
  patch est UN FAIT DE SESSION INVITÉE, jamais du fichier (l'artefact
  relu immuable).
- LE PORT N'EST CONFORME QUE CHEMIN RÉEL EXÉCUTÉ (D157) : tcp-07 se lisait
  parfaitement et crashait au premier appel — l'oubli du marshalling (a2)
  ne vivait dans AUCUNE lecture ; la pièce : le strace de l'exécuteur.
- LE VERROU MULTI-PROFILS VIVANT (26 empreintes DEUX ISA avant l'édition)
  et LE D146 PAR TRACE (in_asm — le témoin EXTERNE de la base réelle) ;
  la 0.8.0-rc.1 SCELLÉE, les trois gardes vivantes.


- PASSATION D141 rejouée au geste « CHANTIER M7-(c) ACCOMPLI / le patch
  fence.i démontré en exécution + le verrou multi-profils + le scellage
  0.8.0-rc.1 » : le bundle courant triade-history-070-33cde07.bundle (git
  bundle --all, 16 078 800 o, md5 ead5b48d…) déposé au MIROIR, ASSERTÉ
  avant dépôt (branche jalon pointe sur 33cde07 — il porte LE TROISIÈME
  CHANTIER DU JALON M7 AVEC sa consignation : le DÉMONSTRATEUR INVITÉ
  riscv/demo [la bascule pendant le trafic 1200 usages, transcription
  byte-exact 15 425 o, l'effet au geste même, les refus 1-4, le DEP
  SIGSEGV 4 290 o exacts, la falsification, les bases forcées, zéro
  régression] + LA CORRECTION tcp-07 [mv a2, t2 — le marshalling oublié au
  port, la pièce par QEMU_STRACE ; le corpus REBUILDÉ sha ec343b4e…] + LE
  VERROU MULTI-PROFILS [26 empreintes DEUX ISA avant l'édition] + LE D146
  PAR TRACE + LA CONFORMITÉ 7/7 + LA CRISTALLISATION 10/10 + LA BALISE
  0.8.0-rc.1 SCELLÉE + les TROIS gardes vivantes + Entrée 153 + D157 +
  worklog Task 71) ; l'ancien 070-09ddd06 (md5 9c7461a3… recoupé AVANT)
  ARCHIVÉ VERSIONNÉ dans archives-bundles/ (18 archives, jamais supprimé) ;
  la série DEMEURE 070 (l'ère de la balise 0.7.0 scellée — la série 080
  naîtra à la finale 0.8.0 du jalon) ; /test sans copie de bundle
  (recoupé) ; GitHub porté à la pointe dans le même geste (push
  6d1b8dd..33cde07, recoupé ls-remote) ; script suivi : passe_bundle_m7c.py.
- SUITE : LE CHANTIER M7-(d) — l'export multi-profils + le terrain (le kit
  qemu-riscv64 au coffre /test ; le run terrain jugé POST-MORTEM ET SUR
  PIÈCES — D138/D145/D148) → la finale 0.8.0, LE JALON M7 FRANCHI —
  l'universalité DÉMONTRÉE.


## Task ID 72 — « continue » : LE CHANTIER M7-(d), LA PART LABORATOIRE ACCOMPLIE — L'EXPORT DE CONTINUITÉ MULTI-PROFILS VERT DE BOUT EN BOUT + LE KIT TERRAIN DÉPOSÉ AU COFFRE AVEC L'INSTRUMENT EMBARQUÉ + LA CLÔTURE D143 DU RUN m6d (la suite annoncée au Task 71) : L'EXPORT (`riscv/export_continuite.py`, le premier depuis M1 — D16/FORMAT_CARTE § 8 aux TROIS profils déclarés) : le conteneur TRIADE-EXP1 729 277 o CHIFFRÉ (XChaCha20-Poly1305, AAD = l'en-tête clair ; la clé : Argon2id 64 Mio/3 it sur un sel DÉDIÉ à l'export — jamais celui d'une carte — puis HKDF à contexte propre) + SIGNÉ (Ed25519, la lignée D27) portant 126 fichiers — I : 81 spécifications (m0..m5 win, LES CANONIQUES unix/I, les miroirs riscv/I), B : CINQ artefacts (m5/proxy.exe 0.6.0 le scellé de la lignée win, unix/sonde 0.7.0-dev.1 + unix/corpus 0.7.0, riscv/sonde 0.8.0-dev.1 + riscv/corpus 0.8.0-rc.1), C : les CINQ cartes de l'ère courante (m5/carte — les 52 blocs de la pile win, les quatre M6/M7) ; L'IMPORT AUTO-PORTANT aux CINQ ÉTAPES § 8.2 : (1) déchiffrement terminal-à-l'échec ; (2) signature du conteneur + des CINQ cartes (le vérificateur PORTÉ, PROUVÉ équivalent aux modules — UNE seule lignée D27, la clé publique recoupée au dépôt) ; (3) LE VERROU CROISÉ : 34 empreintes de blocs (13+13 corpus, 4+4 sondes — les DEUX ISA) + 5 artefacts ENTIERS recalculés aux offsets du MANIFESTE et recoupés au frag-bld de CHAQUE carte ; (4) l'oracle RÉGÉNÉRÉ depuis I (81 specs, jamais importé — D1) ; (5) la REPRISE (win 0.6.0 / linux 0.7.0 / riscv 0.8.0-rc.1) ; LA PREUVE D'EXÉCUTION DE BOUT EN BOUT : les RITUELS rejoués sur les octets TRANSPORTÉS (le conteneur déchiffré en mémoire, jamais le disque) — corpus unix NATIF et corpus riscv SOUS QEMU chacun les DEUX lignes au code 0 (LA PARITÉ § 8.3 DES TROIS PROFILS DANS UN SEUL CONTENEUR), les sondes aux quatre lignes code 6 ; le scellé win : FRONTIÈRE NOMMÉE (son rituel vit au poste Windows — le verrou (3) porte ses octets) ; LES CONSTATS D'ÈRES SUR PIÈCES : HUIT cartes de l'ère courante (m3/m4/m5/terrain + les quatre M6/M7, signatures valides, UNE clé) — les cartes m0/m1/m2/demo/m6/m7 sont des ÈRES PASSÉES de la phrase (signatures valides, fragments NON déchiffrables avec la phrase courante) : l'état scellé COURANT du profil win vit dans SA DERNIÈRE carte de l'ère (m5) ; LE KIT TERRAIN (`scripts/assembler_kit_m7d.py`, modèle m6d) : le SCELLÉ riscv/corpus (ec343b4e…) + le DÉMONSTRATEUR riscv/demo (e57fc74b…) + L'INSTRUMENT EMBARQUÉ qemu-riscv64 10.0.13 STATIQUE (14 821 328 o, md5 bae5a36f…) + le SCÉNARIO PRÉ-ASSEMBLÉ (les 14 chaînes RECOUPÉES PAR AST au layout, le site DEP PAR DÉSASSEMBLAGE @0x1ad4, les 191 adresses du démonstrateur, les tailles FIGÉES 15 425/4 290) + le LISEZMOI ; L'ÉPREUVE D153 : extraction vierge + run au labo — VERT 16 PASS / 0 ÉCHEC ; LA CLÔTURE D143 DU RUN m6d (`scripts/deposer_kit_m7d.py`) : la vague m6d ARCHIVÉE (vagues-m6/), les PIÈCES DU RUN à preuves-run-m6d/ AVEC le VERDICT-DU-RECOUP labo (Entrée 149 — l'archive porte le JUGEMENT avec les pièces), preuves-m6/ DEMEURE avec son LISEZMOI, les DEUX index mis à jour, preuves-m7/ NÉ, la vague m7d DÉPOSÉE (kit-m7d.zip sha 85f7b4bf… + LISEZMOI-m7d.txt) ; L'EXPORT POUSSÉ au coffre Drive racine « Triade » ; LE SCELLAGE 0.8.0 ATTEND LE RUN TERRAIN DU DÉVELOPPEUR (modèle m6d) ; CINQ leçons D158 (l'import AUTO-PORTANT porte géométrie et dérivations publiques AU MANIFESTE ; une carte d'ère passée ne se transporte pas ; l'instrument du terrain vit dans le kit — version ET md5 au témoin ; qemu-user EXIGE le bit X de l'image invitée, rétabli geste nommé ; les lignées homonymes se chargent par chemin absolu) (05/11)

**Détail.** Le manifeste est AUTO-DESCENT au sens plein : géométrie par
artefact, paramètres publics de dérivation par carte, versions par profil,
contrôles effectués à l'export — tout vit au conteneur signé ; seuls la
phrase maîtresse (coffre) et la clé publique (dépôt — recoupement,
transportée en dernier recours avec la réserve nommée) viennent de
l'extérieur. FRONTIÈRES : le conteneur chiffré ne se committe PAS
(riscv/export/ gitignoré, modèle m1/export/) ; le demo n'est PAS un
artefact de la lignée ; code 5 STRUCTUREL sous qemu-user ; concurrence
HORS périmètre (mono-fil) ; le scénario terrain écrit UNIQUEMENT dans
preuves-m7/ (les mutants en .tmp/ effacés, les artefacts originaux jamais
touchés — les empreintes re-prouvées en T3). Livrables :
riscv/export_continuite.py (+ export/ le conteneur, poussé au Drive),
riscv/terrain/ (scenario-m7d.py.in, scenario-m7d.py généré,
LISEZMOI-KIT-M7D.md), scripts/assembler_kit_m7d.py,
scripts/deposer_kit_m7d.py ; consignations : Entrée 154 PAR SCRIPT, D158
PAR SCRIPT (à la suite de D157), fiche riscv64 (Statut + § 10), PLAN §
État (M7-(d) la part laboratoire RÉALISÉE) + la ligne M7 du tableau,
worklog +Task ID 72 ; scripts suivis : inserer_entree_154.py,
inserer_d158.py.

Stage Summary:
- L'EXPORT DE CONTINUITÉ EST DEVENU MULTI-PROFILS ET AUTO-PORTANT : les
  couches I/B/C des TROIS profils dans UN conteneur chiffré + signé, les
  cinq étapes § 8.2 vérifiées sur poste nu (géométrie et dérivations
  publiques AU MANIFESTE), les rituels rejoués sur les octets TRANSPORTÉS —
  export → import → reprise SANS écart.
- LE KIT TERRAIN M7 EST AU COFFRE avec l'INSTRUMENT DANS LE KIT (qemu
  statique, md5 au témoin) — épreuvé VERT 16/16 à l'extraction vierge ; la
  clôture D143 du run m6d est FAITE (les pièces + le verdict du recoup à
  l'archive).
- LA FINALE 0.8.0 ATTEND LE GESTE DU DÉVELOPPEUR : extraire kit-m7d.zip,
  python3 scenario-m7d.py, renvoyer preuves-m7/ — puis le recoup sur
  pièces (D138/D145/D148) et --sceller-final : le jalon M7 franchi,
  l'universalité DÉMONTRÉE.

- SUITE : LE RUN TERRAIN M7-(d) DU DÉVELOPPEUR (kit-m7d.zip au coffre
  /test, la réserve D149 nommée dans chaque verdict) ; le recoup
  post-mortem sur pièces croisées à sa réception ; si vert :
  --sceller-final pose LA FINALE 0.8.0 — LE JALON M7 FRANCHI.


- PASSATION D141 rejouée au geste « CHANTIER M7-(d), LA PART LABORATOIRE
  ACCOMPLIE / l'export de continuité multi-profils + le kit terrain + la
  clôture D143 » : le bundle courant triade-history-070-816eee7.bundle (git
  bundle --all, 16 139 756 o, md5 5bfed8e8…) déposé au MIROIR, ASSERTÉ avant
  dépôt (branche jalon pointe sur 816eee7 — il porte LE QUATRIÈME CHANTIER
  DU JALON M7 avec sa consignation : L'EXPORT MULTI-PROFILS [le conteneur
  TRIADE-EXP1 729 277 o chiffré + signé, 126 fichiers, l'import
  AUTO-PORTANT aux cinq étapes, les rituels sur les octets TRANSPORTÉS] + LE
  KIT TERRAIN DÉPOSÉ AU COFFRE /test [le scellé riscv/corpus 0.8.0-rc.1 +
  le démonstrateur + L'INSTRUMENT EMBARQUÉ qemu statique, épreuvé VERT
  16/16 à l'extraction vierge] + LA CLÔTURE D143 DU RUN m6d [la vague m6d
  archivée, les pièces du run + le verdict du recoup labo à
  preuves-run-m6d/] + Entrée 154 + D158 + worklog Task 72) ; l'ancien
  070-33cde07 (md5 ead5b48d… recoupé AVANT) ARCHIVÉ VERSIONNÉ dans
  archives-bundles/ (19 archives, jamais supprimé) ; la série DEMEURE 070
  (l'ère de la balise 0.7.0 scellée — la série 080 naîtra à la finale 0.8.0
  du jalon) ; /test sans copie de bundle (recoupé) ; GitHub porté à la
  pointe dans le même geste (push 3505ea8..816eee7, recoupé ls-remote) ;
  script suivi : passe_bundle_m7d.py.
- SUITE : LE RUN TERRAIN M7-(d) DU DÉVELOPPEUR — kit-m7d.zip au coffre
  /test (qemu-riscv64 DANS le kit, la réserve D149 nommée dans chaque
  verdict), preuves-m7/ le réceptacle ; le recoup post-mortem sur pièces
  croisées (D138/D145/D148) à sa réception ; si vert : --sceller-final pose
  LA FINALE 0.8.0 — LE JALON M7 FRANCHI, l'universalité DÉMONTRÉE : chaque
  profil déclaré supporté a franchi ses critères.

## Task ID 73 — « les preuves sont dans le dossier drive /test » : LE JALON M7 FRANCHI — LE RUN TERRAIN M7-(d) VERT SUR PIÈCES + LE RECOUP LABORATOIRE VERT 29/29 SUR PIÈCES CROISÉES + LA FINALE 0.8.0 SCELLÉE + L'ÉVÉNEMENT DE REPRISE D159 (la suite annoncée au Task 72) : LE RUN (les trois pièces au coffre /test/preuves-m7/, md5 contrôlés par pièce au rapatriement) : WSL2, noyau 6.18.54.1-microsoft-standard-WSL2 — UN AUTRE noyau que celui du labo (5.10.134…), l'INSTRUMENT EMBARQUÉ du kit (qemu-riscv64 10.0.13 statique, md5 bae5a36f…), le scellé relu AVANT tout geste (ec343b4e… == 0.8.0-rc.1), le démonstrateur e57fc74b… (f72001), la réserve D149 NOMMÉE, run du 05/11 05:20:37 +0100 — 16 PASS / 0 ÉCHEC, VERDICT : VERT (le même verdict que l'épreuve d'extraction vierge D153 : T0 témoin asserté ; T1 rituel ×3 + TROIS bases forcées ; T2 la bascule fence.i PENDANT le trafic — 1 200 usages, apply 399/400, retour 799/800, transcription 15 425 o OCTET POUR OCTET, journal cohérent 0..1199, DEP falsifié SIGSEGV 4 290 o EXACTS, falsification ROMPUE essai 1, bases forcées identiques ; T3 zéro régression + rituel rejoué) ; LE RECOUP (scripts/rapatrier_preuves_m7d.py + scripts/recouper_run_m7d.py) : VERT 29/29 SUR PIÈCES CROISÉES — les pièces md5 re-contrôlés contre le coffre, recoupées ENTRE ELLES (témoin ↔ journal ↔ verdict, les 16 constats LIGNE POUR LIGNE), LE JUGE EST LE CODE (constantes + GÉNÉRATEUR DÉTERMINISTE importés de riscv/terrain/scenario-m7d.py, l'attendu RE-GÉNÉRÉ au geste même : 15 425 / 4 290 o, 800 v1 + 400 v2 == 1 200, DEMO_ADDRS[0] essai n°1), le noyau CONSTATÉ distinct, les artefacts RECALCULÉS au geste même, le kit du coffre == le kit éprouvé (4d17f3fa…) ; le premier passage a ÉCHOUÉ NOMMÉ : TROIS défauts d'INSTRUMENT (la valeur du témoin au-delà du sha, la regex « o attendus », le séparateur « 1 200 »), corrigés et rejoués, les pièces immuables — D154 rejouée ; LA FINALE 0.8.0 SCELLÉE au geste même (riscv/build_corpus.py --sceller-final NÉ AU GESTE, modèle unix/m6d — la bascule ancienne DÉPENDANTE DE LA VERSION rc.1→0.8.0 : verrou multi-profils AVANT l'édition 26 empreintes DEUX ISA + D146 adapté vert + cristallisation 13×10/10 + conformité 7/7 AU geste (29 contrôles, la suite EXÉCUTANT la démonstration) + bascule occurrence unique ASSERTÉE + re-scellage vérifié EN MÉMOIRE avant l'unique écriture + verrou croisé 13/13 + L'ARTEFACT INTACT sha ec343b4e… — le scellage est un fait de carte) ; LES TROIS GARDES VIVANTES (re-scellage REFUSÉ « 0 occurrence », reconstruction REFUSÉE « carte scellée (0.8.0) », la re-vérification PRÉSERVE la balise — frag-bld 1× 0.8.0, 0× rc.1, 0× dev, l'oracle qemu rejoué) ; L'ÉVÉNEMENT DE REPRISE (D159 née) : le poste RESTAURÉ à l'instantané M6-(c) en ouverture du geste — TOUT le jalon M7 absent du disque — l'état VRAI aux MIROIRS (GitHub fetch cc56930 == la pointe consignée D141 ; le coffre Drive : kit + pièces), la reprise par fetch + reset à la pointe CONSIGNÉE (les seuls écarts : des bits de mode), l'instrument réinstallé par SA PROCÉDURE (installer_qemu.sh, md5 bae5a36f… IDENTIQUE au kit), les dépendances réinstallées — RIEN du jalon perdu, le pari D141 tenu ; LA CLÔTURE D143 DU RUN m7d (scripts/cloturer_run_m7d.py) : les pièces → archives-preuves/preuves-run-m7d/ AVEC le VERDICT-DU-RECOUP labo (l'archive porte le JUGEMENT avec les pièces), preuves-m7/ DEMEURE avec son LISEZMOI, l'index mis à jour, la vague m7d DEMEURE la vague courante (aucun kit M8 annoncé, rien ne se jette) ; FRONTIÈRES : l'export de continuité au coffre demeure celui du geste lab (0.8.0-rc.1 daté, les artefacts INTACTS — l'export 0.8.0 naîtra d'un geste dédié si demandé) ; le terrain natif Windows n'exécute pas l'instrument du kit (binaire Linux statique — WSL2 le terrain attendu) ; le programme M6/M7 (D149) ACCOMPLI — les chantiers d'après M7 attendent la décision du développeur ; consignations : Entrée 155 PAR SCRIPT, D159 PAR SCRIPT (à la suite de D158), fiche riscv64 (Statut — finale 0.8.0 SCELLÉE, jalon FRANCHI), PLAN § État (M7-(d) RÉALISÉ, programme ACCOMPLI) + la ligne M7 du tableau, worklog +Task ID 73 ; scripts suivis : lister_preuves_m7.py, rapatrier_preuves_m7d.py, recouper_run_m7d.py, cloturer_run_m7d.py, inserer_entree_155.py, inserer_d159.py, passe_bundle_finale_080.py (05/11)

Stage Summary:
- LE JALON M7 EST FRANCHI : l'universalité DÉMONTRÉE sur pièces — le run
  du développeur (WSL2, un autre noyau, l'instrument du kit) a rendu LE
  MÊME verdict que le labo, le recoup l'a établi sur pièces croisées avec
  le code pour juge, la finale 0.8.0 est scellée l'artefact intact — les
  TROIS profils déclarés ont franchi leurs critères (win 0.6.0 / linux
  0.7.0 / riscv 0.8.0).
- L'ÉVÉNEMENT DE REPRISE a prouvé la passation D141 en conditions réelles :
  le poste restauré à un état antérieur, l'intégralité du jalon retrouvée
  aux miroirs (GitHub + coffre), rien de perdu — D159 consigne la règle.
- LE PROGRAMME M6/M7 (D149) EST ACCOMPLI : la suite appartient aux
  décisions du développeur (chantiers d'après M7 : bloc optionnel de
  syscalls directs, TLS 1.3 pur en blocs scellés, profils additionnels).

- SUITE : LA PASSATION DE LA FINALE — la série 080 naît à la 0.8.0 (le
  bundle au miroir TRIADE-sauvegarde-git/, l'ancien 070-816eee7 archivé
  versionné, GitHub porté à la pointe, /test sans copie recoupé) ; puis
  les chantiers d'après M7 attendent la décision du développeur.

- PASSATION D141 rejouée au geste « JALON M7 FRANCHI / RUN TERRAIN VERT
  SUR PIÈCES + RECOUP LABO 29/29 + FINALE 0.8.0 SCELLÉE » : le bundle
  courant triade-history-080-a1541ce.bundle (git bundle --all, 16 272 636 o,
  md5 322ae6b0…) — LA SÉRIE 080 NAÎT À LA FINALE 0.8.0 — déposé au MIROIR,
  ASSERTÉ avant dépôt (branche jalon pointe sur a1541ce — il porte LA
  FINALE DU JALON M7 avec sa consignation : LE RUN TERRAIN [16/16 PASS sur
  la machine du développeur — WSL2, un autre noyau, l'instrument EMBARQUÉ
  du kit, la réserve D149 nommée] + LE RECOUP LABO [VERT 29/29 sur pièces
  croisées — le juge est le code, l'attendu re-généré au geste même ; trois
  défauts d'instrument nommés au premier passage, corrigés et rejoués, les
  pièces immuables] + LA FINALE 0.8.0 SCELLÉE [--sceller-final né au geste,
  modèle unix/m6d : verrou multi-profils AVANT l'édition + D146 adapté +
  cristallisation 13×10/10 + conformité 7/7 au geste même + bascule
  rc.1→0.8.0 + L'ARTEFACT INTACT ec343b4e… ; les trois gardes vivantes] +
  L'ÉVÉNEMENT DE REPRISE D159 [le poste restauré à l'instantané M6-(c), le
  jalon entier retrouvé aux MIROIRS — GitHub à la pointe consignée D141 +
  le coffre Drive ; la reprise par fetch + reset, l'instrument réinstallé
  par sa procédure md5 IDENTIQUE] + LA CLÔTURE D143 DU RUN m7d [les pièces
  + le verdict du recoup à preuves-run-m7d/] + Entrée 155 + D159 + worklog
  Task 73) ; l'ancien 070-816eee7 (md5 5bfed8e8… recoupé AVANT) ARCHIVÉ
  VERSIONNÉ dans archives-bundles/ (20 archives, jamais supprimé — la série
  070 s'achève aux archives) ; /test sans copie de bundle (recoupé) ;
  GitHub porté à la pointe dans le même geste (push cc56930..a1541ce,
  recoupé ls-remote) ; script suivi : passe_bundle_finale_080.py.
- SUITE : le programme M6/M7 (D149) est ACCOMPLI — les chantiers d'après
  M7 (bloc optionnel de syscalls directs, TLS 1.3 pur en blocs scellés,
  profils additionnels) attendent la décision du développeur.

## Task ID 74 — « continue » : L'ÈRE M6/M7 REFERMÉE PROPRE + LE PROGRAMME D'APRÈS M7 OUVERT — L'EXPORT DE CONTINUITÉ 0.8.0 + LE JALON M8 ET SON DOMAINE `sys` OUVERTS PAR LA COUCHE I ÉCRITE-AVANT-CODE (la suite annoncée au Task 73) : L'EXPORT 0.8.0 (le geste dédié, D160 règle 6) : le conteneur TRIADE-continuite-multiprofils-0.8.0-20261105T044932Z.bin (729 327 o chiffré + signé, 126 fichiers) RÉGÉNÉRÉ au geste même — les versions lues des CARTES {win 0.6.0 / linux 0.7.0 / riscv 0.8.0}, la carte du jalon porte ENFIN la finale ; l'IMPORT À SEC aux CINQ étapes § 8.2 VERT (signature du conteneur + des 5 cartes, le verrou croisé 34 empreintes + 5 artefacts recoupés aux frag-bld, l'oracle régénéré depuis les 81 specs — jamais importé D1, la reprise cohérente) ; LA PREUVE D'EXÉCUTION sur les octets TRANSPORTÉS VERT au geste même (corpus unix natif + corpus riscv sous qemu : chacun les DEUX lignes au code 0 ; les sondes aux quatre lignes code 6 ; le scellé win frontière nommée — le verrou (3) porte ses octets) ; la copie POUSSÉE au coffre Drive racine (3-2-1) ; LE PROGRAMME D'APRÈS M7 (D160 née, le modèle D149) : la demande « continue » EST la décision ; l'ordre des familles LA FONDATION D'ABORD — syscalls directs (le jalon M8) → TLS 1.3 pur → profils additionnels (chacune sur les résultats MESURÉS de la précédente ; la clause spec « hors périmètre courant » LEVÉE NOMMÉMENT pour la seule première famille) ; LE JALON M8 NAÎT : la lignée m8/ (m0-m5 les jalons win, m6/m7 réservés à l'auto-hébergement — m8 libre), le domaine `sys` CRÉÉ au registre figé (m0/I/README.md), la CHARTE à HUIT RÈGLES (m8/I/README.md : le SSN est une DONNÉE jamais un octet de code ; le motif du stub VÉRIFIÉ avant toute extraction — un stub divergent = refus nommé, la contre-mesure du hook un chantier futur jamais une contrebande ; AUCUN IAT dans le domaine — ntdll est LUE jamais APPELÉE ; l'ABI traversante un seul remappage rcx→r10, le noyau lit [rsp+0x28] de l'APPELANT ; fail-closed à SEPT verdicts nommés ; zéro état détenu ; la réserve d'ère Win10/11 x64 ; la lecture d'EAT BORNÉE par NumberOfNames, la comparaison par libc-04 l'héritage scellé) ; LA COUCHE I ÉCRITE-AVANT-CODE : sys-01 l'émetteur (g90001 — le trombone ABI `mov r10, rcx ; syscall ; ret`, SIX octets, AUCUN prologue : I3 la pile de l'appelant EST la pile du syscall), sys-02 le résolveur (g90002 — l'EAT de ntdll lue directement : e_lfanew dans sa fenêtre [0x40, 0x400], le motif PE, le répertoire export, la marche BORNÉE, l'ordinal, le stub confronté au MOTIF_STUB AVANT l'imm32 à +4 ; le bloc qui LIT n'ÉMET pas — I4 la séparation est la garde), sys-03 la twin de hello-02 par NtWriteFile (g90003 — NEUF arguments dont cinq sur la pile, l'IO_STATUS_BLOCK mort au retour, le fixture-ligne de hello-02 CITÉ jamais recopié, zéro IAT : la preuve STRUCTURELLE, l'échec de résolution = AUCUN syscall émis) ; LE PLAN D'ADRESSAGE NÉ (m8/layout.py, source unique : la .text5 préfigurée 0xA000-0xBFFF — le corps scellé 0.6.0 ne bouge pas d'un octet R7 ; les slots préfigurés D8 sys-01 @0xA000 / sys-02 @0xA400 / sys-03 @0xB000, l'arrêt définitif au chantier (b) sur les longueurs réelles ; les constantes MOTIF_STUB 4C8BD1B8 + OFF_SSN 4, les décalages PE/EAT, la table des SEPT verdicts, les versions 0.9.0-dev.1/0.9.0 — geste de BUILD jamais scellage, plancher R10 0x00040000 hérité ; l'héritage m5 CHARGÉ PAR CHEMIN ABSOLU — la leçon D158 appliquée dès la naissance, le module VÉRIFIÉ chargeant 52 blocs hérités + 3) ; FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES — la 0.9.0-dev.1 viendra du premier build M8 au chantier (c)) ; TLS 1.3 pur et les profils additionnels HORS PÉRIMÈTRE (une décision propre chacun) ; la PEB-walk (ntdll sans IAT) et la contre-mesure du hooking CHANTIERS FUTURS NOMMÉS ; l'export 0.8.0 au coffre est celui de l'ère close ; consignations : Entrée 156 PAR SCRIPT, D160 PAR SCRIPT (à la suite de D159), PLAN (la ligne M8 + la section « Programme d'après M7 » + la note d'ouverture), worklog +Task ID 74 ; scripts suivis : inserer_entree_156.py, inserer_d160.py, passe_bundle_m8a.py (05/11)

Stage Summary:
- L'ÈRE M6/M7 EST REFERMÉE PROPRE : l'export de continuité porte la carte
  0.8.0 scellée, l'import à sec et les rituels VERTS sur les octets
  transportés, la copie au coffre racine — l'état protocole qui quitte le
  poste est celui de la finale.
- LE PROGRAMME D'APRÈS M7 EST OUVERT (D160) : la fondation d'abord — le
  jalon M8 (le domaine sys, les syscalls directs sur le profil win) avant
  TLS 1.3 pur avant les profils additionnels ; chaque addition sur
  résultats mesurés.
- LE CHANTIER M8-(a) EST ACCOMPLI : la couche I écrite-avant-code (la
  charte à huit règles + les trois spécifications) + le plan d'adressage
  né (m8/layout.py) + le registre figé étendu — le contrat précède l'octet.

- SUITE : LE CHANTIER M8-(b) — les blocs notés-mesurés-prouvés : sys-01
  l'émetteur (six octets, l'oracle I3 : aucun prologue), sys-02 le
  résolveur (la marche EAT sur FIXTURES ntdll synthétiques), sys-03 la
  twin de hello-02 (le différentiel : la MÊME ligne par les DEUX chemins) ;
  puis (c) le build 0.9.0-dev.1 + la carte génération 8, (d) le kit
  terrain au coffre /test — le VRAI ntdll lu sur la machine du
  développeur.

- PASSATION D141 rejouée au geste « ÈRE M6/M7 REFERMÉE PROPRE + PROGRAMME
  D'APRÈS M7 OUVERT / le jalon M8 et sa couche I écrite-avant-code » : le
  bundle courant triade-history-080-ab41def.bundle (git bundle --all,
  16 311 627 o, md5 0682e407…) déposé au MIROIR, ASSERTÉ avant dépôt
  (branche jalon pointe sur ab41def — il porte L'OUVERTURE DE L'ÈRE avec
  sa consignation : L'EXPORT DE CONTINUITÉ 0.8.0 [le conteneur régénéré
  porte la carte 0.8.0 scellée, import à sec + rituels VERTS sur les
  octets transportés, la copie au coffre racine] + LE PROGRAMME D'APRÈS
  M7 [D160 : la fondation d'abord — syscalls directs → TLS 1.3 pur →
  profils additionnels] + LE JALON M8 ET SA COUCHE I [la charte à huit
  règles ; sys-01 l'émetteur ; sys-02 le résolveur ; sys-03 la twin de
  hello-02 ; m8/layout.py la .text5 préfigurée et les constantes en
  source unique] + le registre figé étendu + Entrée 156 + D160 + worklog
  Task 74) ; l'ancien 080-a1541ce (md5 322ae6b0… recoupé AVANT — la
  finale 0.8.0) ARCHIVÉ VERSIONNÉ dans archives-bundles/ (21 archives,
  jamais supprimé) ; la série 080 continue (la série 090 naîtra à la
  finale 0.9.0 du jalon M8) ; /test sans copie de bundle (recoupé) ;
  GitHub porté à la pointe dans le même geste (push 7d0188a..ab41def,
  recoupé ls-remote) ; script suivi : passe_bundle_m8a.py.
- SUITE : LE CHANTIER M8-(b) — les blocs notés-mesurés-prouvés ; le
  labo ne connaît pas le SSN du terrain et ne le devine jamais (les
  FIXTURES ntdll synthétiques font la preuve au harnais ; le VRAI ntdll
  se lira au terrain, chantier (d)).

## Task ID 75 — « continue » : LE CHANTIER M8-(b) ACCOMPLI — LES TROIS BLOCS DU DOMAINE `sys` NOTÉS-MESURÉS-PROUVÉS AU HARNAIS SUR FIXTURES ntdll SYNTHÉTIQUES (la suite annoncée au Task 74) : LES TROIS ERRATA DE LA COUCHE I corrigés NOMMÉMENT AVANT la notation (sur pièces : memcmp est libc-02 b20002 jamais libc-04 [le registre figé m1 fait foi] ; « NtWriteFile » mesure 11 octets jamais 10 ; le padding de slot de la lignée est NOP 0.90 jamais int3 [build_m0.py `octets + b"\x90" * pad` — int3 est la convention des zones RÉSERVÉES] — chaque erratum consigné DANS le fichier de la couche I, aucun octet n'avait encore été écrit sur les citations fausses) ; LA NOTATION à la main (m8/notation/brouillons/ → m8/outils/auteur.py, le modèle M5 : étiquettes au point fixe, symboles du plan m8/layout.py source unique, memcmp CITÉ de la table scellée BLOCS_LIBC_EMBARQUES 0x1180) : sys-01 l'émetteur SIX octets 49 89 CA 0F 05 C3 (I3 aucun prologue, I2 rax jamais écrit, I6 le ret immédiat), sys-02 le résolveur 293 o / 73 instructions (les gardes span -5, la fenêtre e_lfanew [0x40, 0x400] + motif PE -2, export -3, la marche BORNÉE — NumberOfNames lu UNE fois, la borne en REGISTRE sauvée par push/pop autour du SEUL appel memcmp libc-02, le MOTIF_STUB 0xB8D18B4C AVANT l'imm32 +4 I3, -4 le stub crocheté, -1 la marche complète ; les verdicts de VRAIS négatifs 64 bits signe-étendus, les SSN zéro-étendus — la séparation STRUCTURELLE), sys-03 la twin 164 o / 44 instructions (sys-02 PUIS sys-01 I3, le SSN traverse en rax SANS être réécrit, les NEUF arguments NtWriteFile — cinq à [rsp+0x28]+ dans le cadre, l'iosb sur la pile I2, le fixture-ligne CITÉ à 0x2ED0 I4, le fixture-nom 11 o à 0x2EC0, I5 échec de résolution = AUCUN syscall avec LA CAUSE en rdx, -6 le STATUS consigné jamais muet, la divergence iosb = -6) ; L'ARRÊT D161 des slots sur les longueurs RÉELLES (D47/D79 : la préfiguration 0xA000/0xA400/0xB000 n'était pas un droit — sys-01 @0xA000/0x40, sys-02 @0xA040/0x140, sys-03 @0xA180/0xC0, tassés depuis 0xA000, la réserve contiguë 0xA240-0xBFFF 7 488 o) ; LES FIXTURES .rdata ARRÊTÉES dans la zone VIERGE 0x2EB0-0x2FFF du scellé 0.6.0 (vérifiée sur pièces : 336 octets NULS dans proxy.exe — le corps ne bouge d'AUCUN octet R7) : nom @0x2EC0 (11 o, AUCUN NUL — un SPAN), ligne @0x2ED0 (byte-exact le MESSAGE M0), borne @0x2F00 (fail-closed, miroir D95) ; LA PREUVE AU HARNAIS (m8/harnais_sys.py — le modèle différentiel M4/M5, fixtures PE32+ synthétiques BIEN FORMÉES, l'hostilité dans les noms/stubs/bornes jamais les pointeurs) : **BILAN 61 contrôles · 61 VERTS · 0 échec** (empreinte 19e24b4884c3ee20, graine 20261105 ; re-joué 424242 et 777, chacune 61/61 au volume complet 300 modules fuzz) — V1 round-trip 100 % + CONCORDANCE AU PLAN (12/12 et 4/4 immédiats re-contrôlés contre layout.py, les DEUX [rip] de sys-03 résolvent à 0x2EC0/0x2ED0, l'ordre résoudre-puis-émettre constaté I3) ; V2a LE TROMBONE AU NOYAU SIMULÉ (hook UC_X86_INS_SYSCALL : le remappage rcx→r10, le SSN transmis TEL QUEL, les CINQ arguments de pile lus à [rsp+0x28] AU MOMENT du syscall — la pile de l'APPELANT, le site UNIQUE, le NTSTATUS traversant y compris l'échec, rcx/r11 détruits, les non-volatils sentinelles, l'appelant ET la zone morte aux canaris intacts) ; V2b LE RÉSOLVEUR (rax = LE SSN au succès JAMAIS 0 — Q1, rdx = l'adresse du stub Q2 ; les SIX verdicts nommés sur fixtures hostiles ; I1 la borne lue UNE fois au traceur, I4 AUCUN syscall au compteur, I7 non-volatils, I8 AUCUNE écriture au module — empreinte avant/après ; le SSN à bit 31 zéro-étendu POSITIF) ; V2c LA TWIN AU DIFFÉRENTIEL (LE CHEMIN A : hello-02 le scellé M0 par l'IAT au trampoline M2/M3 ; LE CHEMIN B : sys-03 par NtWriteFile au noyau simulé — LA MÊME LIGNE octet pour octet le fixture M0 ; les NEUF arguments vérifiés au noyau, l'iosb dans le cadre, le SSN résolu AU GESTE MÊME — deux fixtures à SSN distincts en suite, I5 AUCUN syscall sur échec, -6 le STATUS 0xC0000022, -6 la divergence iosb 0xC0000094) ; V3 LE FUZZING (300 modules par graine : noms, SSN, préfixes pièges, stubs crochetés, e_lfanew hostiles, doublons, EAT vide — le MODÈLE dérivé de la couche I et du plan JAMAIS des octets, 0 écart, l'intégrité et les gardes re-contrôlées à CHAQUE cas) ; V4 LA FALSIFICATION (QUINZE mutations D'UN SEUL point stables en taille — leçon D82 — TOUTES ATTRAPÉES : sys-01 muté trahit la twin [r10←rdx, r10←r8, syscall→nop, ret→int3] ; sys-02 mutée trahie sur la batterie [motif+1, OFF_SSN+4→8, fenêtre 0x401, verdict mensonger, marche non bornée jae→jb, motif ignoré jne→je] ; sys-03 mutée trahit [longueur 32, handle depuis rbp, LE SPAN-NOM 10 — le préfixe piège « NtWriteFil » attrape « NtWriteFilter » AVANT la cible, divergence iosb ignorée, ordre inverse] ; les TROIS témoins intacts VERTS) ; LES TROIS DÉFAUTS D'INSTRUMENT du premier passage NOMMÉS et corrigés (les pièces immuables — D154 rejouée : unicorn rend les registres NON SIGNÉS → conversion s64 ; unicorn NE RE-TRADUIT pas un bloc déjà exécuté après mem_write → ctl_remove_cache à chaque re-pose [probe sur pièces : la mutante s'exécutait, la cache servait le témoin] ; le répertoire export du forgeur à RVA FIXE 0x200 écrasait l'entrée DataDirectory pour e_lfanew ∈ [0x178, 0x1A0] — la graine 424242 l'a nommé, les zones dérivent désormais de e_lfanew) ; les ancres de falsification ASSEMBLÉES au geste par keystone (jamais un octet gravé de tête) ; FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES — la 0.9.0-dev.1 viendra du build (c), geste de BUILD jamais scellage), le corps 0.6.0 intact R7, le labo ne connaît pas le SSN du terrain et ne le devine JAMAIS, TLS 1.3 pur et profils additionnels HORS PÉRIMÈTRE (D160), PEB-walk et contre-mesure du hooking CHANTIERS FUTURS NOMMÉS ; consignations : JOURNAL_TRAVAIL +Entrée 157 PAR SCRIPT (ordre 156<157<marqueur, rejeu REFUSÉ), DECISIONS +D161 PAR SCRIPT (à la suite de D160), PLAN (la ligne M8 + le chantier (b) RÉALISÉ), worklog +Task ID 75 ; scripts suivis : inserer_entree_157.py, inserer_d161.py ; SUITE : LE CHANTIER M8-(c) — le build 0.9.0-dev.1 : la composition .text5 sur le corps 0.6.0 INTACT (deltas PE documentés, modèle D94/D136), l'oracle structurel AVEC la règle du domaine (AUCUN IAT PAR BLOC sys), la carte génération 8, la balise 0.9.0-dev.1 (geste de BUILD, jamais scellage) ; puis (d) le kit terrain au coffre /test — le VRAI ntdll lu sur la machine du développeur (05/11)

Stage Summary:
- LE CHANTIER M8-(b) EST ACCOMPLI : les trois blocs du domaine sys
  notés (6/293/164 o) à la main via auteur.py, mesurés (l'arrêt D161
  des slots sur les longueurs réelles — la préfiguration s'incline),
  prouvés au harnais sur fixtures ntdll synthétiques (61 contrôles ·
  61 VERTS sur trois graines).
- LA TWIN EST VERT AU DIFFÉRENTIEL : hello-02 par l'IAT (le scellé M0)
  et sys-03 par NtWriteFile en syscall direct émettent LA MÊME LIGNE
  octet pour octet — la preuve d'observable du domaine entier.
- LES TROIS ERRATA de la couche I corrigés nommément avant la notation
  (libc-02/11 octets/NOP) — sur pièces, jamais sur mémoire.
- Les pièces : m8/notation/ (brouillons + trois notations explicites),
  m8/outils/auteur.py, m8/harnais_sys.py, m8/layout.py arrêté, m8/I/
  errata consignés, Entrée 157, D161, PLAN, worklog Task 75.

- SUITE : LE CHANTIER M8-(c) — le build 0.9.0-dev.1 + la carte
  génération 8 + l'oracle structurel (AUCUN IAT PAR BLOC sys) ; puis
  (d) le kit terrain au coffre /test — le VRAI ntdll lu sur la machine
  du développeur, la finale 0.9.0 attend le vert.

- PASSATION D141 rejouée au geste « CHANTIER M8-(b) : les trois blocs du
  domaine sys notés-mesurés-prouvés au harnais sur fixtures ntdll
  synthétiques » : le bundle courant triade-history-080-99f96b1.bundle
  (git bundle --all, 16 366 513 o, md5 3e8b77fb…) déposé au MIROIR,
  ASSERTÉ avant dépôt (branche jalon pointe sur 99f96b1 — il porte LE
  CHANTIER M8-(b) avec sa consignation : LES TROIS ERRATA de la couche I
  corrigés nommément avant la notation [memcmp est libc-02 jamais
  libc-04 ; « NtWriteFile » mesure 11 octets jamais 10 ; le padding de
  slot est NOP 0x90 jamais int3] + LA NOTATION à la main [sys-01 l'émetteur
  SIX octets ; sys-02 le résolveur 293 o — la marche EAT bornée, le motif
  AVANT l'imm32 ; sys-03 la twin 164 o — les neuf arguments, le
  fixture-ligne CITÉ, I5 aucun syscall sur échec] + L'ARRÊT D161 des slots
  sur les longueurs réelles [0xA000/0x40, 0xA040/0x140, 0xA180/0xC0] + LES
  FIXTURES .rdata dans la zone VIERGE du scellé [nom @0x2EC0, ligne
  @0x2ED0, borne @0x2F00] + LA PREUVE AU HARNAIS [61 contrôles · 61 VERTS
  sur TROIS graines 20261105/424242/777 — la twin au différentiel, la
  MÊME ligne par les DEUX chemins ; les QUINZE mutations de falsification
  attrapées, les témoins intacts verts] + Entrée 157 + D161 + worklog
  Task 75) ; l'ancien 080-ab41def (l'ouverture de l'ère : l'export de
  continuité 0.8.0 + D160 + la couche I du jalon M8, md5 0682e407…
  recoupé AVANT) ARCHIVÉ VERSIONNÉ dans archives-bundles/ (22 archives,
  jamais supprimé) ; la série 080 continue (la série 090 naîtra à la
  finale 0.9.0 du jalon M8) ; /test sans copie de bundle (recoupé) ;
  GitHub porté à la pointe dans le même geste (push 407343c..99f96b1,
  recoupé ls-remote) ; script suivi : passe_bundle_m8b.py.
- SUITE : LE CHANTIER M8-(c) — le build 0.9.0-dev.1 + la carte génération 8
  + l'oracle structurel (AUCUN IAT PAR BLOC sys) ; puis (d) le kit terrain
  au coffre /test — le VRAI ntdll lu sur la machine du développeur.

## Task ID 76 — « ok continue » : LE CHANTIER M8-(c) OUVERT SUR UNE DÉCOUVERTE — LE GARDE-SCEAU D87 NOMME LA DETTE DE CÉRÉMONIE DE L'ÈRE (la suite annoncée au Task 75 : le build 0.9.0-dev.1) : LA DÉCOUVERTE (le premier geste du build, sur pièces) : le garde REFUSE — l'arbre m0 a divergé, fichier modifié README.md (code 10, diff d'intention non signé : la clé hors-ligne du développeur est requise) — LA MESURE : le M8-(a) (ab41def, D160 règle 6) a étendu le REGISTRE FIGÉ m0/I/README.md (le domaine sys créé) SANS cérémonie de re-signature ; les TROIS specs hello-01/02/03 INTACTES (seul le registre diverge du manifeste signé à la cérémonie 0.6.0 du 04/11) ; l'arbre m8 ABSENT de la table du sceau (la couche I du domaine jamais signée — l'arbre m5 lui-même ne le fut qu'à SA cérémonie de scellage) — LE SCEAU FAIT SON TRAVAIL, la dette est née au M8-(a), elle est ÉCHUE au premier build ; LA CÉRÉMONIE DE L'ÈRE M8 EXIGÉE (le geste du développeur, D87) : la table du sceau ÉTENDUE (v06/sceau_I.py : m8 = proxy.exe domaine sys, sys.1 — sceau_I.py n'est PAS couvert par l'arbre v06 : aucune cascade), sceau_I.py preparer JOUÉ (a-signer.txt écrit : 12 arbres, les empreintes vivantes), LA REMISE MINIMALE : m0 (le registre étendu) + m8 (le domaine) signés hors-ligne avec SA clé Ed25519, puis sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt (l'atomicité de cérémonie — la remise du 04/11 fut de 11 lignes, celle-ci en demande 2) ; le labo NE SIGNERA JAMAIS à sa place (la clé de TEST déclasserait l'état « réelle » : une régression de preuve, refusée) ; LE BUILD ÉCRIT (m8/build_m8.py — le modèle build_m5) : LE GARDE ARMÉ EN TÊTE (ARBRES_GARDE_M8 = m0-m5+m8, le refus CONSTATÉ au geste avec la notice de cérémonie), l'héritage re-vérifié de bout en bout (B4.assembler_tout_m4 + B3 + B5.assembler_tout_m5 : round-trip 100 % par bloc, oracles structurels M3 524 + M4 492 + M5 312 verrous, L'IMAGE M5 COMPOSÉE confrontée OCTET PAR OCTET au scellé 0.6.0 sha c1e46fb0… MATCH — la carte génération 7 scellée version=0.6.0 prouve CES octets, le fait de carte D104), L'ORACLE STRUCTUREL M8 (54 verrous — LA RÈGLE AUCUN IAT PAR BLOC sys [charte § 3], le site syscall UNIQUE Q1, les SIX octets exacts du trombone, rax jamais écrit avant le site I2, AUCUN prologue I3, le ret immédiat I6, AUCUN syscall dans sys-02/sys-03 I4, le MOTIF_STUB AVANT l'imm32 I3 de sys-02, memcmp libc-02 @0x1180 le SEUL appel I2, la borne lue UNE fois I1, l'ordre résoudre-puis-émettre I3 de sys-03, l'échec court-circuité js I5, les fixtures CITÉES I4), LA COMPOSITION (.text5 NOUVELLE : la réserve int3 0xA240+, les TROIS slots D161 code+NOP ; .rdata : l'héritage M5 octet/octet + les fixtures dans la zone VIERGE vérifiée [le span-nom 11 o @0x2EC0 SANS NUL, la ligne byte-exact le fixture M0 @0x2ED0] + LA VERSION 0x00090001 @0x2820 [LE delta R10 : geste de BUILD jamais scellage — la 0.9.0 attend le terrain vert (d)]), L'ÉDITEUR PE32+ À SEPT SECTIONS (NumberOfSections 7, .text5 RX @0xA000 raw 0x8E00, SizeOfImage 0xC000, taille 0xAE00, l'entrée PE 0x8C80 INCHANGÉE [le principal pas recâblé R7], les 7 en-têtes 608 o TIENNENT dans la marge 0x400 : LE DÉCALAGE D94 N'EST PAS REJOUÉ), LA VALIDATION PE (les imports INCHANGÉS — le domaine ne déclare RIEN ; les portes R10 28 + M5 ; la réserve .rdata vierge ; R_POLITIQUE 0), LA PREUVE R7 (les sections .text/.text2/.data/.text3/.text4 == scellé octet/octet ; .rdata identique SAUF version+fixtures, les trouées VIERGES des deux côtés ; 41 blocs hérités octet-identiques) ; LES COMPOSANTS VÉRIFIÉS SUR PIÈCES DÉTACHÉES (le garde n'est PAS appelé — ce n'est pas construire, c'est le test du code ; AUCUN artefact écrit, AUCUNE carte déposée) : l'exe composé 44 544 o (0xAE00), sha256 1492b0bc0792e1ab…, RE-CONSTATÉ IDENTIQUE (le déterminisme) ; les TROIS oracles appelés depuis le build sur les blobs (M4 héritage 30 cas + M5 héritage 29 cas + LE HARNAIS M8 le domaine 61 cas, volume reduit — le code d'appel validé) ; LA CARTE GÉNÉRATION 8 (m8/carte_m8.py — le sel Argon2id propre, le sel HKDF M8, CARTE_DIR m8/carte/) : les primitives testées À BLANC dans un répertoire temporaire (JAMAIS dans m8/carte/) — la clé publique e9cd8c549485… : LE TÉMOIN NE BOUGE PAS (la graine durable D144) ; LE HARNAIS ÉTENDU (executer(blobs, graine, volume) — le point d'entrée du build, modèle oracle_m5 ; l'Emulateur re-constate byte-égal les octets du build avec les notations : JAMAIS deux sources de vérité ; les modules déjà chargés RÉUTILISÉS — la leçon D158 appliquée au mode build ; 61/61 en mode autonome ET en mode blobs) ; L'ARRÊT D162 DES OFFSETS FICHIER (m8/layout.py, la source unique) : .text5 raw 0x8E00 (les six premières raw inchangées), taille 0xAE00 ; FRONTIÈRES : AUCUN artefact écrit (m8/proxy.exe N'EXISTE PAS — il naîtra de construire() après la cérémonie), AUCUNE carte déposée, AUCUNE balise posée (la 0.9.0-dev.1 viendra du build), le scellé 0.6.0 INTACT (l'ancre R7 de l'ère), l'état de clé du sceau « réelle » INTACT, le labo ne connaît toujours pas le SSN du terrain ; consignations : JOURNAL_TRAVAIL +Entrée 158 PAR SCRIPT (ordre 157<158<marqueur, rejeu REFUSÉ), DECISIONS +D162 PAR SCRIPT (à la suite de D161), PLAN (le chantier (c) OUVERT — la cérémonie attend), worklog +Task ID 76 ; scripts suivis : inserer_entree_158.py, inserer_d162.py ; SUITE : LA CÉRÉMONIE DE L'ÈRE M8 (la remise du développeur : m0 + m8 signés hors-ligne, v06/sceau-I/a-signer.txt) → LE DÉPÔT (sceau_I.py deposer) → LE GARDE REPASSÉ → LE BUILD EXÉCUTÉ (construire : l'artefact 0.9.0-dev.1 + la carte génération 8 + le verrou croisé + la cristallisation) ; puis le chantier (d) — le kit terrain au coffre /test, le VRAI ntdll lu sur la machine du développeur (05/11)

Stage Summary:
- LE CHANTIER (c) EST OUVERT SUR UNE DÉCOUVERTE : le garde-sceau D87
  refuse le registre m0 étendu au M8-(a) sans re-signature — la dette
  de cérémonie de l'ère est nommée, LA CLÉ DU DÉVELOPPEUR est requise
  (a-signer.txt préparé, remise minimale m0 + m8).
- LE BUILD 0.9.0-dev.1 EST ÉCRIT ET VÉRIFIÉ PAR PIÈCES DÉTACHÉES :
  l'héritage complet re-vérifié (l'image M5 == scellé 0.6.0 octet par
  octet), l'oracle structurel M8 54 verrous (AUCUN IAT PAR BLOC sys),
  l'exe composé 44 544 o sha256 1492b0bc… DÉTERMINISTE, les trois
  oracles appelés, la carte génération 8 prête (le témoin ne bouge pas).
- AUCUN ARTEFACT N'EST NÉ : le garde est armé en tête de construire() —
  l'artefact et la carte suivront le dépôt de la remise du développeur.

- SUITE : la cérémonie (m0 + m8 signés hors-ligne) → le dépôt → le
  garde repassé → construire() : l'artefact m8/proxy.exe 0.9.0-dev.1 +
  la carte génération 8 + le verrou croisé ; puis le chantier (d) — le
  kit terrain au coffre /test, le VRAI ntdll sur la machine du
  développeur, la finale 0.9.0 attend le vert.

- PASSATION D141 rejouée au geste « CHANTIER M8-(c) OUVERT SUR UNE
  DÉCOUVERTE : le garde-sceau D87 nomme la dette de cérémonie de l'ère » :
  le bundle courant triade-history-080-d999103.bundle (git bundle --all,
  16 415 924 o, md5 46a74722…) déposé au MIROIR, ASSERTÉ avant dépôt
  (branche jalon pointe sur d999103 — il porte LE CHANTIER M8-(c) OUVERT
  avec sa consignation : LA DÉCOUVERTE [le garde refuse le registre m0
  étendu au M8-(a) sans re-signature — les specs hello intactes, seul le
  registre diverge ; l'arbre m8 absent de la table] + LA CÉRÉMONIE DE
  L'ÈRE M8 EXIGÉE [la table étendue à m8 sys.1, a-signer.txt préparé —
  la remise du développeur : m0 + m8 signés hors-ligne, sa clé] + LE
  BUILD ÉCRIT [build_m8.py construire+verifier, le garde armé en tête],
  ses composants VÉRIFIÉS SUR PIÈCES DÉTACHÉES [l'héritage complet :
  l'image M5 composée == scellé 0.6.0 octet/octet, M3 524 + M4 492 +
  M5 312 verrous ; l'oracle structurel M8 54 verrous — AUCUN IAT PAR
  BLOC sys ; l'exe composé 44 544 o sha256 1492b0bc… re-constaté
  identique ; les TROIS oracles appelés ; la carte génération 8 prête —
  le témoin e9cd8c549485… ne bouge pas ; l'arrêt D162 des offsets :
  .text5 raw 0x8E00, taille 0xAE00] + Entrée 158 + D162 + worklog Task
  76) ; l'ancien 080-99f96b1 (le chantier M8-(b) : les trois blocs
  notés-mesurés-prouvés, md5 3e8b77fb… recoupé AVANT) ARCHIVÉ VERSIONNÉ
  dans archives-bundles/ (23 archives, jamais supprimé) ; la série 080
  continue (la série 090 naîtra à la finale 0.9.0 du jalon M8) ; /test
  sans copie de bundle (recoupé) ; GitHub porté à la pointe dans le même
  geste (push 897e9b7..d999103, recoupé ls-remote) ; script suivi :
  passe_bundle_m8c.py.
- SUITE : LA CÉRÉMONIE DE L'ÈRE M8 (la remise du développeur : m0 + m8
  signés hors-ligne, v06/sceau-I/a-signer.txt) → LE DÉPÔT → LE GARDE
  REPASSÉ → LE BUILD EXÉCUTÉ (construire : l'artefact 0.9.0-dev.1 + la
  carte génération 8) ; puis le chantier (d) — le kit terrain au coffre
  /test, le VRAI ntdll lu sur la machine du développeur.

## Task ID 77 — « fais une synchro git et drive, et fais moi un kit pour la cérémonie comme tu as fait pour les précédentes » : LA SYNCHRO SUR PIÈCES + LE KIT DE CÉRÉMONIE DE L'ÈRE M8 DÉPOSÉ

- LA SYNCHRO (la doctrine d'abord — sur pièces, jamais sur mémoire) :
  git PROPRE à f3d72e9, la branche jalon == origin RECROUPÉE ls-remote
  (f3d72e9829a8…, 0 avance / 0 retard — GitHub à la pointe, rien à
  pousser) ; le miroir Drive re-synchronisé (drive_sync.py rc=0 : 1 126
  fichiers inchangés, triade-history.bundle mis à jour — le hook
  post-commit avait déjà tourné à chaque commit, le rejeu manuel le
  constate).
- L'ÉTAT CONSTATÉ AVANT LE KIT : la zone download/ AMPUTÉE des 5
  LISEZMOI de cérémonie (le disque labo encore recyclé — le PIÈGE de
  l'Entrée 132 guettait : un rejeu de maj_kit.py depuis un labo amputé
  aurait régénéré un MANIFESTE sans les LISEZMOI, divergence
  silencieuse d'attestation).
- PAS 1 — RAPATRIEMENT + RECOUP DE L'ÈRE
  (scripts/rapatrier_lisezmoi_ceremonie.py, labo hors dépôt, aucun
  secret) : les 5 LISEZMOI du kit Drive /Cérémonie → download/, md5
  vérifiés CONTRE LES MÉTADONNÉES Drive après écriture : 5/5 MATCH
  (25 136 + 5 391 + 14 246 + 9 171 + 10 264 o — les mêmes tailles qu'à
  l'Entrée 132) ; PUIS le recoup propre à l'ère (sur métadonnées) : le
  kit porte DÉJÀ la remise fraîche v06/sceau-I/a-signer.txt md5 MATCH
  (12 arbres, déposé au kit par le hook du commit d999103 — la charge
  du développeur est EN PLACE), cle-publique-I.txt MATCH (173fae9c…,
  l'ancre de rotation) et etat-cle.txt MATCH (« reelle ») — le kit et
  le dépôt décrivent le MÊME état de cérémonie.
- LA PIÈCE NOUVELLE — LISEZMOI-ceremonie-ere-M8.txt ÉCRIT ET RECOUPÉ :
  le mode d'emploi de la cérémonie de l'ère (celui qui manquait — le
  LISEZMOI-cle-I.txt couvre la PREMIÈRE fois [generer + signer +
  déposer --cle], celui-ci couvre la RE-SIGNATURE) : POURQUOI (le garde
  D87 refuse le registre m0 étendu au M8-(a) — README.md modifié, code
  10 — et l'arbre m8 jamais signé : la dette est échue au premier
  build, D162) ; CE QUI A CHANGÉ (12 arbres, DEUX empreintes bougées :
  m0 0.1.0 d94154840c9de80a… le registre étendu [les specs hello
  INTACTES], m8 sys.1 621daf173debcc4c… le domaine sys [README +
  sys-01/02/03] ; les DIX autres aux MÊMES empreintes qu'au 04/11 —
  Ed25519 déterministe : les re-signer redonne les signatures déposées)
  ; LA RÈGLE D'OR : JAMAIS « generer » (la clé du 04/11 réutilisée, sa
  moitié publique 173fae9c75229b15… écrite noir sur blanc — une clé
  neuve romprait la continuité de l'état « réelle » ; si
  cle-publique-I.txt diverge : ARRÊT) ; LE PAS-À-PAS (emporter
  ceremonie_hors_ligne.py + a-signer.txt + cle-publique-I.txt + SA
  cle-I-privee.txt ; signer → signatures-I.txt 12 lignes
  auto-vérifiées ; verifier → TOUT VERT + la clé commence par
  173fae9c… ; ramener signatures-I.txt ET cle-publique-I.txt) ; LE
  DÉPÔT (sceau_I.py deposer signatures-I.txt --cle
  cle-publique-I.txt — l'atomicité de cérémonie) ; CE QUE CELA
  DÉBLOQUE (le garde repassé → construire() : l'artefact 0.9.0-dev.1 +
  la carte génération 8 → le chantier (d), le VRAI ntdll). LE RECOUP
  PAR SCRIPT AVANT DÉPÔT : les empreintes m0/m8 et la clé citées ==
  les pièces (a-signer.txt, cle-publique-I.txt — aucun chiffre
  inventé), les empreintes vivantes des DIX arbres inchangés == leurs
  manifestes déposés (la phrase « mêmes empreintes qu'au 04/11 »
  PROUVÉE sur pièces), aucun marqueur de substitution.
- PAS 2 — LE DÉPÔT CANONIQUE (maj_kit.py ÉTENDU puis rejoué) :
  RACINE_KIT reçoit l'entrée LISEZMOI-ceremonie-ere-M8.txt
  (optionnelle comme ses cinq aînées — le contrat D130 inchangé),
  NOTE_D130 (qui alimente MANIFESTE.txt) porte la mention de la
  cérémonie de l'ère (le développeur qui ouvre le dossier est ORIENTÉ
  vers le bon LISEZMOI) ; le rejeu : gardes vertes (44 fichiers v06/
  suivis par git + 9 racine requis), 60 entrées attendues, 1 téléversé
  (LISEZMOI-ceremonie-ere-M8.txt), 1 mis à jour (MANIFESTE.txt), 58
  inchangés, 60/60 VÉRIFIÉS ALLER-RETOUR md5.
- FRONTIÈRES : AUCUN artefact m8 écrit (m8/proxy.exe n'existe pas — il
  naîtra de construire() après la cérémonie), AUCUNE balise ne bouge
  (win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), la remise
  a-signer.txt INCHANGÉE (12 arbres), le scellé 0.6.0 INTACT (l'ancre
  R7), l'état de clé « réelle » INTACT, AUCUN secret déposé (le kit ne
  porte que des preuves publiques — D130), le labo ne signe rien (la
  cérémonie appartient au développeur, D87/D162) ; consignations :
  JOURNAL_TRAVAIL +Entrée 159 PAR SCRIPT (ordre 158<159<marqueur,
  rejeu REFUSÉ), PLAN (la ligne M8-(c) : le kit déposé), worklog
  +Task ID 77 ; scripts suivis : inserer_entree_159.py (dépôt),
  rapatrier_lisezmoi_ceremonie.py (labo, hors dépôt).
- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer
  a-signer.txt avec la clé du 04/11, ramener signatures-I.txt +
  cle-publique-I.txt — le kit /Cérémonie du Drive porte tout) → LE
  DÉPÔT (sceau_I.py deposer) → LE GARDE REPASSÉ → LE BUILD EXÉCUTÉ
  (construire : l'artefact 0.9.0-dev.1 + la carte génération 8) ; puis
  le chantier (d) — le kit terrain au coffre /test, le VRAI ntdll lu
  sur la machine du développeur.

Stage Summary:
- LE KIT DE CÉRÉMONIE DE L'ÈRE M8 EST DÉPOSÉ au dossier /Cérémonie du
  Drive : la remise fraîche (a-signer.txt, 12 arbres — les DEUX
  signatures nouvelles m0 d9415484… + m8 621daf17…), les outils
  (ceremonie_hors_ligne.py, GUI, lanceurs), les cinq LISEZMOI
  historiques RAPATRIÉS (5/5 md5 MATCH) et LA PIÈCE NOUVELLE :
  LISEZMOI-ceremonie-ere-M8.txt — le mode d'emploi de la
  RE-SIGNATURE, avec LA RÈGLE D'OR « JAMAIS generer » (la clé du
  04/11 173fae9c… est réutilisée).
- LA SYNCHRO EST VERTE SUR PIÈCES : git f3d72e9 == GitHub (recoupé
  ls-remote, 0/0), le miroir Drive re-synchronisé (rc=0), le recoup
  de l'ère 3/3 (le kit porte exactement l'état de cérémonie du
  dépôt : remise + ancre de clé + état « reelle »).
- AUCUN ARTEFACT N'EST NÉ : m8/proxy.exe n'existe toujours pas — la
  cérémonie du développeur précède construire() (le garde est armé,
  D87/D162).

- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer
  a-signer.txt avec la clé du 04/11, ramener signatures-I.txt +
  cle-publique-I.txt — le kit /Cérémonie du Drive porte tout) → LE
  DÉPÔT (sceau_I.py deposer) → LE GARDE REPASSÉ → LE BUILD EXÉCUTÉ
  (construire : l'artefact 0.9.0-dev.1 + la carte génération 8 + le
  verrou croisé) ; puis le chantier (d) — le kit terrain au coffre
  /test, le VRAI ntdll sur la machine du développeur, la finale 0.9.0
  attend le vert.

- PASSATION D141 rejouée au geste « LE KIT DE CÉRÉMONIE DE L'ÈRE M8
  DÉPOSÉ » : le bundle courant triade-history-080-b7b6e01.bundle
  (git bundle --all, 16 428 940 o, md5 39393eaa…) DÉPOSÉ AU MIROIR
  ASSERTÉ (il porte LE KIT DE L'ÈRE avec sa consignation : la synchro
  sur pièces [git == GitHub recoupé, miroir rc=0] + les 5 LISEZMOI
  rapatriés [5/5 md5 MATCH] + le recoup de l'ère [3/3 : a-signer.txt
  12 arbres + cle-publique 173fae9c… + état « reelle »] +
  LISEZMOI-ceremonie-ere-M8.txt écrit et recoupé [la règle d'or
  « JAMAIS generer », les empreintes m0/m8 citées == les pièces] +
  maj_kit.py étendu [RACINE_KIT + NOTE_D130] + le kit déployé 60/60
  aller-retour + Entrée 159 + worklog Task 77), l'ancien
  080-d999103 (le chantier M8-(c) ouvert, md5 46a74722… recoupé
  AVANT) ARCHIVÉ VERSIONNÉ dans archives-bundles/ (24 archives,
  jamais supprimé), la série 080 continue, /test sans copie
  (recoupé), GitHub porté à la pointe dans le même geste (push
  f3d72e9..b7b6e01, recoupé ls-remote) ; script suivi :
  passe_bundle_ere.py ; FRONTIÈRES : aucune balise ne bouge (win
  0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN artefact m8
  écrit (le garde est armé — l'artefact naîtra après la cérémonie),
  le scellé 0.6.0 INTACT (l'ancre R7), l'état de clé du sceau
  « réelle » INTACT ; SUITE : LA CÉRÉMONIE (le geste du développeur —
  le kit /Cérémonie porte tout) → le dépôt → le garde repassé →
  construire() : l'artefact 0.9.0-dev.1 + la carte génération 8.

## Task ID 78 — « signatures déposées dans le drive /test » : LA CÉRÉMONIE DE L'ÈRE M8 PASSÉE SUR PIÈCES — LA DETTE D162 SOLDÉE, LE GARDE VERT 12/12, L'ARTEFACT 0.9.0-dev.1 NÉ DU BUILD (déterministe : 1492b0bc… == la pièce du Task 76) ; le disque labo encore recyclé (troisième fois), la reprise D159 rejouée, le relais compte de service portant le geste (le jeton OAuth encore mort) (05/11)

- L'OUVERTURE (sur pièces, jamais sur mémoire) : le message du
  développeur annonce la remise ; l'état constaté : (1) le disque
  labo RECYCLÉ ENCORE — HEAD 402508f, worklog Task 65, Entrée 147,
  D152 : TOUT le jalon M7 et l'ère M8 absents du disque (troisième
  recyclage : Entrée 132, m7d/D159, aujourd'hui) ; (2) le jeton OAuth
  du relais MORT (invalid_grant — la deuxième fois, le même symptôme
  que le 29/10).
- LA REPRISE D159 REJOUÉE : ls-remote → origin à 7079df1 (EXACTEMENT
  la pointe consignée par la passation Task 77, bundle 080-b7b6e01) ;
  fetch + fast-forward PROPRE (les seuls écarts : 9 fichiers en bits
  de mode, ZÉRO contenu) ; les 24 gestes revenus : M6-(d) run terrain
  vert + LA FINALE 0.7.0, M7 ENTIER jusqu'à LA FINALE 0.8.0 (jalon
  franchi, D159 née de la reprise précédente), l'ère M8 (a/b/c :
  D160/D161/D162) et le kit de cérémonie Task 77 ; les instruments
  réinstallés PAR LA PROCÉDURE consignée à la reprise m7d (pip :
  keystone-engine 0.9.2, capstone 5.0.9, pefile, pynacl 1.6.2,
  unicorn 2.1.4) — RIEN ne s'est perdu (troisième recyclage, zéro
  perte).
- LE RELAIS COMPTE DE SERVICE PORTE LE GESTE (scripts/sonder_coffre_
  sa.py, LECTURE SEULE — le mécanisme du 29/10 étendu au sondage du
  coffre entier) : racine 14 entrées (l'export de continuité 0.8.0
  posé, le miroir à la pointe 080-b7b6e01), /Cérémonie 17 (le
  LISEZMOI de l'ère en place), /test 10 — LA PIÈCE : signatures-I.txt
  (md5 annoncé ab22512a6864…).
- LE RAPATRIEMENT + LE RECOUP (scripts/rapatrier_ceremonie_m8.py,
  lecture seule sur le dépôt) : md5 MATCH après écriture (1 703 o) ;
  L'ANCRE DE CLÉ tenue (cle-publique-I.txt == 173fae9c75229b15…) ;
  12/12 lignes valides ; LE RECOUP DE L'ÈRE : les DIX arbres inchangés
  (m1-m7, demo, terrain, v06) portent les MÊMES signatures que les
  déposées du 04/11 — Ed25519 déterministe : la réutilisation de la
  clé du 04/11 PROUVÉE par la comparaison bit à bit, sans jamais voir
  la clé privée ; m0 RE-SIGNÉ (d941548… le registre étendu), m8 ARBRE
  NEUF (621daf17…) ; les empreintes vivantes == a-signer.txt 12/12 ;
  chaque signature VÉRIFIÉE Ed25519 contre 173fae9c… — RECOUPE
  INTÉGRAL VERT 12/12.
- LE DÉPÔT CANONIQUE : le garde AVANT nommait la dette EXACTEMENT
  (m0 CODE 10 « fichier modifie : README.md », m8 CODE 12 « manifeste
  depose absent », les DIX verts) ; sceau_I.py deposer --cle : les 12
  signatures VÉRIFIÉES INTÉGRALEMENT avant toute écriture, PUIS
  installées (manifestes vivants), l'état « reelle » INTACT ; LE
  GARDE REPASSÉ : 12/12 arbres VERTS code 0 — LA DETTE D162 SOLDÉE.
- LE BUILD EXÉCUTÉ (m8/build_m8.py construire(), graine 20261105,
  volume complet) : le garde en tête PASSE ; l'héritage re-vérifié
  (oracle M4 560 + M5 365 cas verts, structurels M3 524 + M4 492 +
  M5 312 verrous, l'image M5 == scellé 0.6.0 octet/octet) ; la preuve
  R7 : 44 blocs octet-identiques au scellé 0.6.0 ; le harnais M8
  61/61 VERTS (empreinte 628ff4de…, graine 20261105) ; L'ARTEFACT
  m8/proxy.exe NÉ : 44 544 o, sha256 1492b0bc0792e1ab162338b414fb2057
  3134e84d752b9d0657292421f8eb0cd4 — IDENTIQUE à la pièce de
  vérification du Task 76 (le déterminisme d'un poste à l'autre) ;
  LA CARTE GÉNÉRATION 8 vivante (4 fragments chiffrés, signature
  Ed25519, 55 blocs sur 7 artefacts, le témoin e9cd8c549485… ne
  bouge pas — graine durable D144) ; verrou croisé 55 empreintes
  (signature OK, racine OK) ; tableau de bord écrit (0 défaut ouvert,
  0 changement hors journal).
- FRONTIÈRES : AUCUNE balise ne bouge (win 0.6.0 / linux 0.7.0 /
  riscv 0.8.0 INTACTES — la 0.9.0-dev.1 est un GESTE DE BUILD, jamais
  un scellage : la finale 0.9.0 attend le run terrain vert du (d)) ;
  le scellé 0.6.0 INTACT (l'ancre R7) ; l'état de clé « réelle »
  INTACT (le labo n'a RIEN signé — la cérémonie appartient au
  développeur, D87/D162) ; le SSN du terrain INCONNU du labo (les
  fixtures synthétiques font la preuve au harnais) ; download/ la
  zone labo (la pièce rapatriée y demeure, non suivie).
- Consignations : JOURNAL_TRAVAIL +Entrée 160 PAR SCRIPT (ordre
  159<160<marqueur, rejeu REFUSÉ), DECISIONS +D163 PAR SCRIPT (à la
  suite de D162), PLAN (le chantier M8-(c) RÉALISÉ —
  scripts/maj_plan_m8c.py), ce worklog +Task ID 78 ; scripts suivis :
  inserer_entree_160.py, inserer_d163.py, maj_plan_m8c.py,
  sonder_coffre_sa.py, rapatrier_ceremonie_m8.py.
- SUITE : LA PASSATION (le bundle de la série 080 au miroir, l'ancien
  archivé versionné, GitHub porté à la pointe) ; puis LE CHANTIER
  M8-(d) — le kit terrain au coffre /test (le VRAI ntdll lu sur la
  machine du développeur, le motif confronté, la ligne comparée par
  les DEUX chemins, tout stub divergent = refus nommé), la finale
  0.9.0 attend le vert.

Stage Summary:
- LA CÉRÉMONIE DE L'ÈRE M8 EST PASSÉE SUR PIÈCES : la remise du
  développeur (signatures-I.txt, 1 703 o, md5 ab22512a… MATCH)
  rapatriée du coffre /test par le RELAIS COMPTE DE SERVICE (le
  jeton OAuth encore mort), recoupée INTÉGRALEMENT avant dépôt —
  l'ancre de clé 173fae9c… tenue, les DIX signatures des arbres
  inchangés IDENTIQUES aux déposées du 04/11 (la clé réutilisée
  PROUVÉE par le déterminisme Ed25519), m0 re-signé, m8 neuf,
  empreintes == a-signer.txt 12/12, Ed25519 12/12.
- LA DETTE D162 EST SOLDÉE : le dépôt canonique a installé les 12
  signatures (l'atomicité vérifiée AVANT écriture), le garde REPASSÉ
  est VERT 12/12 (code 0).
- L'ARTEFACT 0.9.0-dev.1 EST NÉ DU BUILD : 44 544 o, sha256
  1492b0bc… IDENTIQUE à la pièce de vérification du Task 76 (le
  déterminisme d'un poste à l'autre, à travers un recyclage de disque
  et une reprise D159) ; la carte génération 8 vivante (le témoin ne
  bouge pas), le verrou croisé 55 empreintes, la preuve R7 (44 blocs
  octet-identiques au scellé 0.6.0), le harnais 61/61.
- LE POSTE A ENCORE ÉTÉ RECYCLÉ (troisième fois) : la reprise D159
  rejouée au geste même — fetch + pointe consignée 7079df1, les
  instruments par leur procédure ; RIEN ne s'est perdu.

## Task ID 79 — « on reprend ce projet : signatures déposées dans le drive /test, et j'ai mis à jour le jeton relais du drive /tokens » (la suite, côté infrastructure) : LA REPRISE SUR LES TROIS MIROIRS + LA PASSATION REJOUÉE

- LA DÉCOUVERTE (le recoup GitHub AVANT de travailler) : origin à
  9193019, UN COMMIT EN AVANCE du bundle 080-b7b6e01 — le Task 78
  d'une session précédente (cérémonie installée + garde 12/12 + build
  0.9.0-dev.1 + Entrée 160 + D163) POUSSÉ mais la session morte
  AVANT la passation : le bundle ne portait pas la pointe.
- L'ALIGNEMENT (D159 rejouée) : le geste parallèle refait au labo
  constaté DOUBLON AVANT consignation (aucune entrée doublée), reset
  à la pointe consignée 9193019 ; l'état vérifié : garde 12 VERTS
  (état « reelle »), carte génération 8, artefact régénéré 44 544 o
  sha256 1492b0bc… == la pièce de D163 (le déterminisme s'accumule :
  trois postes, le même sha).
- LE JETON RELAIS ROUVRE LE CANAL D'ÉCRITURE (la mise à jour du
  développeur au /Tokens) : check_auth 200, drive_sync.py rc=0 (16
  téléversés, 7 mis à jour, 1 122 inchangés, 0 erreur — le miroir à
  la pointe, triade-history.bundle mis à jour).
- LE KIT D130 : le premier rejeu depuis le labo amputé a RE-DÉCLENCHÉ
  LE PIÈGE des Entrées 132/159 (MANIFESTE 56 entrées pour un kit
  réel de 62 — les 6 LISEZMOI ignorés) ; LE RAPATRIEMENT CANONIQUE
  d'abord (6/6 md5 MATCH contre les métadonnées Drive après
  écriture), le rejeu ensuite : 62/62 vérifiés aller-retour — le
  manifeste couvre le kit réel.
- LA PASSATION VERSIONNÉE : triade-history-080-9193019.bundle (16
  565 966 o, md5 a8cd69f8…, branche jalon == 9193019) DÉPOSÉ au
  miroir (relu MATCH), l'ancien 080-b7b6e01 ARCHIVÉ VERSIONNÉ
  (md5 39393eaa… recoupé avant le déplacement PATCH — 25 archives,
  rien supprimé), /test recoupé SANS copie de bundle ; script :
  scripts/passe_bundle_m8c_execution.py.
- FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 /
  riscv 0.8.0 INTACTES), l'artefact 0.9.0-dev.1 INTACT (régénéré
  identique), le garde VERT 12/12, le scellé 0.6.0 INTACT, aucun
  secret exposé ; consignations : Entrée 161 PAR SCRIPT, D164 PAR
  SCRIPT, worklog +Task ID 79 ; scripts suivis :
  inserer_entree_161.py, inserer_d164.py,
  passe_bundle_m8c_execution.py (dépôt),
  rapatrier_lisezmoi_ceremonie.py (labo, hors dépôt).
- SUITE : LE CHANTIER M8-(d) — le kit terrain au coffre /test (le
  VRAI ntdll lu sur la machine du développeur, le motif confronté,
  la ligne comparée par les DEUX chemins), la finale 0.9.0 attend le
  vert ; la cristallisation R6 progresse par les --verifier.

Stage Summary:
- LES TROIS MIROIRS SONT À LA POINTE : GitHub 9193019 == le bundle
  080-9193019 == le miroir (16/7/1122, 0 erreur) == le kit (62/62) —
  la dette de passation de la session morte est SOLDÉE, la reprise
  D164 est la doctrine consignée (fetch GitHub d'abord, alignement à
  la pointe, passation rejouée, rapatriement avant maj_kit).
- L'artefact 0.9.0-dev.1 RÉGÉNÉRÉ IDENTIQUE (1492b0bc…, troisième
  poste) — la preuve de déterminisme s'accumule, le garde est VERT à
  12/12, l'état « réelle » intact.
- SUITE : le chantier M8-(d) — le kit terrain au coffre /test (le
  VRAI ntdll sur la machine du développeur).

## Task ID 80 — (la suite annoncée au Task 79) : LE CHANTIER M8-(d) OUVERT ET SERVI — LE KIT TERRAIN DÉPOSÉ AU COFFRE /test

- LE SCÉNARIO (m8/terrain/scenario-m8d.py — python SEUL, stdlib) :
  QUATRE temps — T0 LE TÉMOIN (l'empreinte de l'artefact assertée,
  l'environnement consigné [la version Windows], le VRAI ntdll localisé
  et haché, l'artefact cartographié DONT_RESOLVE [le scénario est le
  CHARGEUR : aucune entrée résolue, aucun point d'entrée appelé], les
  octets attendus constatés UN PAR UN, le slot kernel32!WriteFile
  résolu PAR LE SCÉNARIO — le geste du chargeur pour le chemin A) ;
  T1 LA LECTURE (le VRAI ntdll par DEUX lecteurs indépendants : la
  marche EAT en PYTHON et le BLOC sys-02 à son adresse scellée — LE
  MÊME SSN ; le MOTIF confronté [4C 8B D1 B8 avant l'imm32, les octets
  du stub consignés] ; un second nom [NtReadFile — jamais un numéro en
  cache] ; LA FALSIFICATION INVITÉE [un module forgé au stub crocheté :
  -4 NOMMÉ sur la machine réelle]) ; T2 LA TWIN (la même ligne par les
  DEUX chemins : hello-02 l'IAT kernel32 VS sys-03 le syscall direct —
  les DEUX fichiers comparés OCTET PAR OCTET au fixture 33 o) ; T3 LES
  GARDES (la base invalide → -1 NOMMÉ, AUCUN syscall [le
  fichier-témoin VIDE — la garde I5 sur la machine réelle] ; proxy.exe
  relu inchangé ; le ntdll relu inchangé [I8] ; FreeLibrary).
- L'ÉPREUVE DE LABO (assembler_kit_m8d.py) : le labo NE PEUT PAS
  exécuter le scénario (Windows + VRAI ntdll — le cœur du chantier) ;
  LE RECOUP PAR AST : 13 constantes du scénario == l'artefact/le plan
  (AUCUN chiffre gravé de tête) ; py_compile ; L'EXTRACTION VIERGE
  VERT — kit-m8d.zip 20 286 o, md5 117eb10a…, sha256 cc21cd85….
- LE DÉPÔT (deposer_kit_m8d.py, règle D143 : par DÉPLACEMENT, jamais
  un jet) : la vague m7d CONSOMMÉE archivée (vagues-m7/ : kit-m7d.zip
  md5 4d17f3fa… + LISEZMOI-m7d.txt, md5 constatés après) ; preuves-m8d/
  NÉ avec son LISEZMOI-preuves.txt (les six pièces attendues) ; LA
  VAGUE m8d POSÉE (kit-m8d.zip MATCH par relecture + LISEZMOI-m8d.txt) ;
  l'index mis à jour ; la vérification : 11 entrées à la racine, rien
  jeté (corriger-wsb.* et signatures-I.txt [la remise consommée]
  demeurent).
- FRONTIÈRES : aucune balise ne bouge (win 0.6.0 / linux 0.7.0 / riscv
  0.8.0 INTACTES — la finale 0.9.0 attend le run terrain vert),
  l'artefact INTACT (lecture seule), le labo ne connaît toujours PAS le
  SSN du terrain (le scénario le résout sur la machine du développeur,
  le témoin le consigne), la carte ne voyage pas avec l'artefact (R1) ;
  consignations : Entrée 162 PAR SCRIPT, PLAN (la ligne (d) : le kit
  déposé), worklog +Task ID 80 ; scripts suivis : inserer_entree_162.py,
  assembler_kit_m8d.py, deposer_kit_m8d.py.
- SUITE : LE GESTE DU DÉVELOPPEUR (python scenario-m8d.py sur la
  machine Windows — les pièces au coffre /test/preuves-m8d/) → LE
  RECOUP LABORATOIRE (D138/D145/D148) → SI VERT : LA FINALE 0.9.0
  SCELLÉE (le jalon M8 franchi).

Stage Summary:
- LE KIT TERRAIN M8-(d) EST DÉPOSÉ au coffre /test : le scénario du
  VRAI ntdll en QUATRE temps (le témoin, la lecture par deux lecteurs,
  LA TWIN par les deux chemins, les gardes), recoupé au labo PAR AST
  (13 constantes == l'artefact), la vague m8d posée, la vague m7d
  archivée, preuves-m8d/ né.
- LA FINALE 0.9.0 ATTEND LE VERT DU TERRAIN : le run du développeur
  (python scenario-m8d.py sur sa machine Windows) — le second chemin
  preuve, la même observable SANS un seul import.

- PASSATION D141 (la clôture du geste M8-(d)) : le bundle courant
  triade-history-080-b5d5018.bundle (16 677 811 o, md5 356315b0…,
  branche jalon == b5d5018 [le geste 1e3aaf6 + sa consignation]) DÉPOSÉ
  au miroir ASSERTÉ (relu MATCH), l'ancien 080-9193019 (la cérémonie +
  le build 0.9.0-dev.1) ARCHIVÉ VERSIONNÉ (md5 a8cd69f8… recoupé — 26
  archives, rien supprimé), /test sans copie (recoupé) ; script suivi :
  passe_bundle_m8d.py ; la série 080 continue (la série 090 naîtra à
  la finale 0.9.0).

## Task ID 81 — (la suite annoncée au Task 80) : LE PREMIER RUN DÉVELOPPEUR A CRASHÉ NOMMÉ — le kit terrain M8-(d) CORRIGÉ et REDÉPOSÉ

- LE RUN (Windows 10.0 build 26300, Python 3.13.9 AMD64) : T0 et T1
  verts jusqu'à la falsification (empreinte MATCH, le VRAI ntdll lu par
  les DEUX lecteurs d'accord, le motif confronté, NtReadFile résolu,
  les DEUX SSN distincts) — puis CRASH Python à la préparation du
  module forgé : ligne 207, « ValueError: memoryview assignment:
  lvalue and rvalue have different structures ». Le run meurt AVANT
  T2 : aucun syscall émis, l'artefact intact.
- LA CAUSE NOMMÉE : v[0x2A0:0x2B0] (16 octets) face à
  b"NtWriteFile\x00" (12 octets) — l'assignation memoryview exige la
  structure identique ET LA LONGUEUR EST LA STRUCTURE (jamais de
  remplissage tacite). La vue était saine ('B', 1-D) : le défaut est
  la FORME, pas le format. Reproduit au labo à l'identique (la MÊME
  ValueError, la même ligne).
- LA CORRECTION : UNE ligne — v[0x2A0:0x2AC] = b"NtWriteFile\x00"
  (la tranche == la valeur, 12 octets : le nom + son NUL — le motif
  déjà suivi par les voisins MZ/PE/stub) ; la règle portée en
  commentaire DANS la source.
- L'ÉPREUVÉ : assembler_kit_m8d.py REJOUÉ (recoup AST 13 constantes
  == l'artefact/le plan, py_compile, extraction vierge VERT) ; le
  contrat du forgé vérifié SUR LE FICHIER LIVRÉ (verifier_m8d.py :
  la marche EAT trouve « NtWriteFile » au RVA 0x300, le motif ABSENT
  du stub crocheté b8 44 33 22 11 → le refus -4 NOMMÉ attendu de
  sys-02) ; vérifié AUSSI sur le script extrait du zip (zip == zone
  == dépôt).
- LE DÉPÔT CORRIGÉ (corriger_kit_m8d.py) : kit-m8d.zip du coffre
  /test MIS À JOUR EN PLACE (upload_update — le contenu remplacé, le
  fichier conservé, rien jeté) : md5 117eb10a… (défectueux) →
  ad6cbffe… MATCH par relecture ; les résidents intacts (11 entrées).
- FRONTIÈRES : aucune balise ne bouge (la finale 0.9.0 attend le
  vert du run rejoué), l'artefact INTACT, le labo ne connaît toujours
  pas le SSN du terrain (la sortie collée en conversation n'est pas
  une pièce — le témoin temoin-m8d.txt reste la référence) ;
  consignations : Entrée 163 PAR SCRIPT, worklog +Task ID 81 ;
  scripts suivis : inserer_entree_163.py, corriger_kit_m8d.py.
- SUITE : LE GESTE DU DÉVELOPPEUR REJOUE (kit-m8d.zip retéléchargé du
  coffre /test OU le seul scenario-m8d.py remplacé, puis python
  scenario-m8d.py) → les pièces au coffre /test/preuves-m8d/ → LE
  RECOUP LABO (D138/D145/D148) → SI VERT : LA FINALE 0.9.0 SCELLÉE.

Stage Summary:
- LE CRASH DU PREMIER RUN EST NOMMÉ ET RÉPARÉ : une tranche memoryview
  de 16 octets face à une valeur de 12 — la longueur fait partie de la
  « structure », le refus était la RÈGLE de Python, pas la panne du
  terrain.
- LE KIT CORRIGÉ EST AU COFFRE /test (md5 ad6cbffe… MATCH par
  relecture) : le geste du développeur peut reprendre — la finale
  0.9.0 attend toujours le vert.

## Task ID 82 — « preuves m8d déposées dans le drive /test » : LE RUN TERRAIN M8-(d) VERT SUR PIÈCES + LE RECOUP LABO VERT 30/30 SUR PIÈCES CROISÉES + LA FINALE 0.9.0 SCELLÉE — LE JALON M8 FRANCHI (05/11)

- LE RUN REJOUÉ (le kit corrigé ad6cbffe…, la ligne 207 n'est plus) :
  temoin-m8d.txt (2026-11-05 12:10:03, Windows 10.0 build 26300, Python
  3.13.9 AMD64) — T0-T3 ENTIERS, 35 verts / 0 échecs, VERDICT VERT ; le
  SSN(NtWriteFile) rendu DEUX fois le MÊME (Python + sys-02), NtReadFile
  DISTINCT, le stub confronté, le forgé crocheté REFUSÉ (-4), LA TWIN
  (l'IAT kernel32 == le syscall direct == le fixture 33 octets), le refus
  -1 sur pièce VIDE, proxy.exe relu inchangé.
- LE RECOUP (scripts/recouper_run_m8d.py — le juge est le code : les
  constantes importées de la source, le fixture et le sha RECALCULÉS au
  geste même) : 30 contrôles, RECOUP VERT 30/30 — l'imm32 du stub
  consigné == LE SSN (RE-LU, jamais cru), la twin re-contrôlée octet par
  octet au labo (md5 c64ab06b…, sha du fixture == le constat T2.TWIN),
  le kit du coffre == le corrigé, le zip == le dépôt (scenario + proxy).
  DEUX défauts d'INSTRUMENT nommés par le fail-closed (le « $ » sans
  re.M ; la tranche de sortie amputant la première attestation —
  attrapée par LE SCELLAGE), corrigés et rejoués, les pièces immuables
  (D154).
- LA CRISTALLISATION R6 : dix passes --verifier (M4 560 + M5 365 +
  harnais M8 61 verts par passe, verrou 55/55) — 55 blocs à 10/10.
- LE SCELLAGE (m8/build_m8.py --sceller-final né au geste, modèle
  D147/corpus) : garde sceau I (7 arbres, clé réelle) + recoup terrain
  EXIGÉ SUR PIÈCES + cristallisation 10/10 + verrou croisé avant/après
  + bascule unique version=0.9.0-dev.1 → 0.9.0 dans frag-bld (EN MÉMOIRE
  avant l'unique écriture), entête portant la balise, signature à la
  graine durable (pub e9cd8c549485… ne bouge pas), tableau CONSCIENT de
  la balise ; proxy.exe INTACT (1492b0bc…, 44 544 o — FAIT DE CARTE) ;
  l'anti-rollback REFUSE désormais la reconstruction (constaté), la
  re-vérification sous 0.9.0 VERTE.
- FRONTIÈRES : win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES ; le
  scellé 0.6.0 ancre R7 ; le SSN du terrain INCONNU du labo (donnée du
  témoin) ; consignations : Entrée 164 PAR SCRIPT (ordre 163<164<
  marqueur, rejeu REFUSÉ), D165 PAR SCRIPT (à la suite de D164), PLAN
  (jalon M8 FRANCHI — ligne du jalon, ligne (d), État du programme),
  worklog +Task ID 82 ; scripts suivis : inserer_entree_164.py,
  rapatrier_preuves_m8d.py, recouper_run_m8d.py [labo].
- SUITE : LA PASSATION D141 (la série 090 NAÎT à la finale 0.9.0 — le
  bundle à la pointe, l'ancien 080 archivé versionné) + LA CLÔTURE D143
  du run m8d (les pièces + VERDICT-recoup-labo-m8d.txt →
  archives-preuves/preuves-run-m8d/, le réceptacle demeure) + le push
  GitHub à la pointe.

- PASSATION + CLÔTURE (le même geste, Task ID 82) : LA SÉRIE 090 NÉE —
  triade-history-090-4edf0c3.bundle (16 757 330 o, md5 63c6bfb3…, branche
  jalon == 4edf0c3 LA FINALE 0.9.0) DÉPOSÉ AU MIROIR ASSERTÉ (relu MATCH),
  l'ancien 080-b5d5018 ARCHIVÉ VERSIONNÉ (md5 356315b0… recoupé — 27
  archives, rien supprimé), /test sans copie (recoupé), le push GitHub à
  la pointe (431666c..4edf0c3) ; LA CLÔTURE D143 du run m8d : les SIX
  pièces DÉPLACÉES vers archives-preuves/preuves-run-m8d/ (md5 constatés
  APRÈS le geste — jamais un jet), VERDICT-recoup-labo-m8d.txt DÉPOSÉ AVEC
  elles (le jugement AVEC les pièces), les DEUX index mis à jour,
  preuves-m8d/ ne porte plus que son LISEZMOI (le réceptacle demeure), la
  racine recoupée (kit-m8d.zip md5 ad6cbffe…) ; scripts suivis :
  passe_bundle_finale_090.py, cloturer_run_m8d.py.

Stage Summary:
- LE JALON M8 EST FRANCHI : le terrain a établi le critère (le VRAI
  ntdll lu, la même ligne par les DEUX chemins), le labo a recoupé sur
  pièces croisées, la carte a scellé — l'artefact n'a pas bougé d'un
  octet.
- LA FINALE 0.9.0 EST SCELLÉE (le fait de carte, la chrystal 10/10, le
  recoup 30/30 exigé comme pièce — le fail-closed a refusé deux fois
  avant de sceller, et il avait raison les deux fois).

## Task ID 83 — « on ouvre la suite » : LA SECONDE FAMILLE OUVERTE — LE JALON M9 TLS 1.3 PUR (domaine `tls13`, ère 1.0.0) ; l'ère M8 refermée propre (export 0.9.0 au coffre racine), la couche I fondée, la dette de cérémonie nommée (05/11)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == 8ced0bb la
  pointe ; le bundle 090-4edf0c3 au geste — le schéma normal), les canaux
  200 ; qemu-riscv64 réinstallé PAR SA PROCÉDURE (10.0.13, la réserve
  D149 re-vérifiée avant usage).
- L'ÈRE M8 REFERMÉE PROPRE : riscv/export_continuite.py étendu au scellé
  win COURANT (m8/proxy.exe 0.9.0 + carte génération 8 + m8/I) ; le
  conteneur 0.9.0 (779 272 o, md5 3de022b7…) régénéré, import à sec CINQ
  étapes VERT, preuve d'exécution VERT sur les octets transportés, copie
  au coffre racine relu MATCH ; les anciens 0.8.0 demeurent.
- LA COUCHE I FONDÉE : le domaine `tls13` (l'identifiant `tls` appartient
  à M4 — jamais réutilisé) ; la charte à HUIT règles ; le tableau des 28
  blocs (h10xxxx, SIX familles) ; la famille `sha` spécifiée (les 4
  miroirs win des contrats ah-04..07, le contexte en ARGUMENT) ;
  tls13/layout.py préfiguré (.text6, versions 1.0.0, SEPT verdicts — la
  préfiguration n'est pas un droit, D161).
- LA DETTE DE CÉRÉMONIE NOMMÉE : le garde constate m0 CODE 10 + tls13
  CODE 12 (les 11 autres verts) ; a-signer.txt préparé (13 arbres, remise
  minimale m0 + tls13) ; AUCUN build avant la remise du développeur.
- FRONTIÈRES : aucune balise ne bouge (0.9.0/0.7.0/0.8.0 INTACTES), le
  1.0.0-dev.1 naîtra du premier BUILD M9 ; m8/proxy.exe INTACT
  (1492b0bc…) ; consignations : Entrée 165 PAR SCRIPT, D166 PAR SCRIPT,
  PLAN (famille (2) OUVERTE + table M9 + État), worklog +Task ID 83 ;
  scripts suivis : inserer_entree_165.py.
- SUITE : les 24 spécifications restantes du chantier M9-(a) (hkdf,
  x25519, aead, enregistrement, poignée, principal — R2) ; le kit de
  cérémonie de l'ère M9 au /Cérémonie du Drive (modèle Entrée 159).

Stage Summary:
- LA SECONDE FAMILLE EST OUVERTE sur la demande « on ouvre la suite »
  (D166, le modèle D149/D160) : TLS 1.3 pur en blocs scellés — le jalon
  M9, la grande œuvre, l'ère 1.0.0.
- L'ÈRE M8 S'EST REFERMÉE PROPRE (l'export de continuité 0.9.0 au coffre
  racine) ET LA DÉTTE DE CÉRÉMONIE EST NÉE NOMMÉE : le garde refuse
  jusqu'à la remise du développeur — c'est son travail, exactement comme
  en D162.

- PASSATION (le même geste, Task ID 83) : le bundle courant
  triade-history-090-ab48be1.bundle (16 788 985 o, md5 3663dc5a…, branche
  jalon == ab48be1 [le geste + sa consignation]) DÉPOSÉ AU MIROIR ASSERTÉ
  (relu MATCH : il porte l'export 0.9.0 + D166/Entrée 165 + la couche I
  tls13 + la dette de cérémonie + le plan M9 + Task 83), l'ancien
  090-4edf0c3 (LA FINALE 0.9.0) ARCHIVÉ VERSIONNÉ (md5 63c6bfb3… recoupé
  avant le déplacement PATCH — 28 archives, rien supprimé), /test sans
  copie (recoupé), le push GitHub à la pointe ; scripts suivis :
  passe_bundle_m9a.py.

## Task ID 84 — LE CHANTIER M9-(a) COMPLET : LES 28 SPÉCIFICATIONS POSÉES — les 24 du geste (hkdf, x25519, aead, enregistrement, poignée, principal), le plan étendu aux SIX familles, l'erratum av-10 consigné, l'instrument 117 VERTS (05/11 au soir)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == 45c8970 la
  pointe, le bundle 090-ab48be1 au geste), les canaux 200 ; un défaut
  d'instrument nommé au geste même (le recyclage du disque avait posé le bit
  exécutable sur 179 fichiers suivis — ZÉRO octet de contenu : réparé par git
  restore, l'arbre propre re-constaté).
- LES 24 SPÉCIFICATIONS : hkdf (HMAC RFC 2104/4231, Extract/Expand RFC
  5869, Expand-Label RFC 8446 § 7.1) ; x25519 (les miroirs av-05..11, la
  passe propagation+gel FUSIONNÉE, l'échelle SANS branche de données, l'état
  EN PILE — la divergence nommée sur av-11) ; aead (l'arrêt AES-NI, GHASH
  sans table par donnée, le tag VÉRIFIÉ avant restitution, AUCUNE brique
  d'inversion) ; enregistrement (le nonce IV ⊕ séquence, l'AAD = l'en-tête,
  l'opaque 23, la borne 2^14) ; poignée (le ClientHello FIXE 114 o, le
  ServerHello aux refus nommés [HRR -5, suite -5], le calendrier à trois
  étages, le Finished, l'épinglage -6) ; principal (la machine d'états
  17 520 o, quatre événements, OUVRIR tient la poignée entière par la
  rotule ; le socle d'appel à deux rappels en argument).
- LE PLAN ÉTENDU : les constantes des SIX familles DÉRIVÉES PAR ARITHMÉTIQUE
  (les membres de p, p − 2, la valeur magique HRR, R, les libellés, les
  dispositions 200/17 520 o) ; l'ERRATUM av-10 consigné AVANT la notation
  (quatorze chiffres hex pour un membre de 51 bits — l'écriture fautive,
  jamais la notation prouvée ; le miroir re-dérive, il ne copie pas).
- L'INSTRUMENT : verifier_specs_m9a.py — 117 contrôles VERTS (28/28 specs,
  la table h100001..h100028, les constantes re-dérivées, les constructions
  re-jouées 114/90/17 520, les verdicts dans la table des SEPT) ; TROIS
  défauts nommés par le fail-closed avant le vert (les identifiants lus en
  hex au lieu du DÉCIMAL — les neuf premiers passaient par coïncidence ;
  l'ordre de tri de la table ; la formule structurelle absente de tls13-27)
  : corrigés, rejoués.
- FRONTIÈRES : aucune balise ne bouge (0.9.0/0.7.0/0.8.0 INTACTES), AUCUN
  octet de notation (R2), AUCUN build avant la remise (la dette de
  cérémonie demeure) ; consignations : Entrée 166 PAR SCRIPT, D167 PAR
  SCRIPT, PLAN (chantier (a) RÉALISÉ + État), worklog +Task ID 84 ;
  scripts suivis : inserer_entree_166.py, verifier_specs_m9a.py [labo].
- SUITE : le kit de cérémonie de l'ère M9 au /Cérémonie du Drive (modèle
  Entrée 159) ; puis le chantier (b) — la notation et les vecteurs
  officiels — APRÈS la remise du développeur.

Stage Summary:
- LE CHANTIER M9-(a) EST RÉALISÉ : les 28 spécifications posées avant tout
  octet de notation, la charte instanciée bloc par bloc, les constantes
  re-dérivées par arithmétique — l'erratum av-10 consigné en fait la règle.
- LA COÏNCIDENCE N'EST PAS UNE PREUVE (les neuf premiers identifiants
  passaient en hex par hasard) : le fail-closed a nommé, l'instrument s'est
  instruit, le vert final est gagné.

- PASSATION (le même geste, Task ID 84) : le bundle courant
  triade-history-090-64eae8e.bundle (16 847 529 o, md5 90c7168e…, branche
  jalon == 64eae8e [le geste + sa consignation]) DÉPOSÉ AU MIROIR ASSERTÉ
  (relu MATCH : il porte les 24 spécifications + le plan étendu aux SIX
  familles + l'erratum av-10 + l'instrument 117 VERTS + Entrée 166/D167 +
  le PLAN [chantier (a) RÉALISÉ] + Task 84), l'ancien 090-ab48be1
  (L'OUVERTURE M9) ARCHIVÉ VERSIONNÉ (md5 3663dc5a… recoupé avant le
  déplacement PATCH — 29 archives, rien supprimé), /test sans copie
  (recoupé), le push GitHub à la pointe ; scripts suivis :
  passe_bundle_m9a2.py.

## Task ID 85 — LE KIT DE CÉRÉMONIE DE L'ÈRE M9 DÉPOSÉ au /Cérémonie (la remise RÉGÉNÉRÉE sur l'arbre complet — la charge de l'ouverture était périmée par les 24 specs ; le LISEZMOI pas à pas ; l'erratum de la ligne SUITE de l'Entrée 166) (05/11 au soir)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == e83a27e la
  pointe, le bundle 090-64eae8e au geste), les canaux 200 ; l'état du sceau
  LU au geste même (clé « reelle » 173fae9c…, m0 DIVERGE + tls13 DEPOT
  INCOHERENT + 11 verts — la dette constatée sur pièces).
- LA CHARGE RÉGÉNÉRÉE : la découverte du geste — a-signer.txt de
  l'ouverture portait tls13 0ef882d6… (l'arbre alors naissant) ; les 24
  specs ont bougé l'arbre ; preparer rejoué : UNE ligne sur treize
  (tls13 → 9ff91874… = L'ARBRE COMPLET : le registre + les 28 specs), les
  douze autres octet-identiques. SANS ce geste, la remise signée aurait
  laissé tls13 CODE 10 APRÈS installation.
- LE LISEZMOI + LE DÉPÔT : LISEZMOI-ceremonie-ere-M9.txt (modèle Entrée
  159 : les deux empreintes m0 4ebe6a2c… / tls13 9ff91874…, la règle d'or
  « JAMAIS generer », les pas à pas console + graphique, le contrat D87) ;
  déposé au /Cérémonie md5 par relecture ; la remise du kit recoupée ==
  celle du dépôt (D130).
- L'ERRATUM : la ligne SUITE de l'Entrée 166 (« le chantier (b) … APRÈS la
  remise ») — IMPRÉCIS : le garde exige la remise pour LE BUILD (chantier
  (e)), pas pour la notation (le miroir M8 : Entrée 157 précéda 158) ;
  consigné en tête du geste suivant, le journal ne se réécrit pas.
- FRONTIÈRES : aucune balise ne bouge, AUCUN build avant la remise (le
  garde fait son travail), AUCUN octet de notation ; consignations :
  Entrée 167 PAR SCRIPT, D168 PAR SCRIPT, worklog +Task ID 85 ; scripts
  suivis : inserer_entree_167.py, deposer_lisezmoi_ere_m9.py.
- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer la
  remise 13 arbres à la clé du 04/11, ramener signatures-I.txt +
  cle-publique-I.txt) → le labo installe et recroise (le garde 13/13) ;
  EN PARALLÈLE LICITE : le chantier (b) — la notation des 28 blocs + les
  vecteurs officiels.

Stage Summary:
- LA MAIN DU DÉVELOPPEUR EST SERVIE : la remise est FRAÎCHE (l'arbre
  complet des 28 spécifications), le LISEZMOI la sert pas à pas, la règle
  d'or est réitérée — la cérémonie peut avoir lieu.
- LA CHARGE PÉRIMÉE DE L'OUVERTURE EST LA PREUVE DE LA RÈGLE : la charge
  se prépare au geste de la cérémonie — l'ouverture annonce, la cérémonie
  exige.

- PASSATION (le même geste, Task ID 85) : le bundle courant
  triade-history-090-094a15f.bundle (16 863 824 o, md5 a20150c1…, branche
  jalon == 094a15f [le geste + sa consignation]) DÉPOSÉ AU MIROIR ASSERTÉ
  (relu MATCH : il porte la remise régénérée [tls13 9ff91874… = l'arbre
  complet des 28 specs] + Entrée 167/D168 + l'erratum de la ligne SUITE +
  Task 85), l'ancien 090-64eae8e (M9-(a) COMPLET) ARCHIVÉ VERSIONNÉ (md5
  90c7168e… recoupé — 30 archives, rien supprimé), /test sans copie
  (recoupé), le push GitHub à la pointe ; scripts suivis :
  passe_bundle_ere_m9.py.
