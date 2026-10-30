
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
