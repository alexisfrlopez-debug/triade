
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
