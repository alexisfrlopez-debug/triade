# LE PLAN PRÉ-ENREGISTRÉ DU CHANTIER fkkqc7v8t — LE TEMPS CONSTANT STRUCTUREL
# PASSÉ DE L'ÉGALITÉ DE TRACES À LA VÉRIFICATION STATIQUE NON BORNÉE, ET LA
# CAUSE RACINE DU RENVERSEMENT DUDECT N=200→N=400

L'instruction exécutée (Qwen__20261116_fkkqc7v8t.txt, la vague 6, le chantier 4
du listing — déposée au /instructions du coffre, md5 recoupé au rapatriement) :

  « Fais passer le temps constant structurel des six cibles crypto (sha-256,
  hmac, hkdf, x25519, aes-gcm, md5) du statut "borné par égalité de traces" à
  une vérification statique non bornée : analyse de flux d'information prouvant
  que ni les branchements ni les adresses mémoire ne dépendent du secret
  (système de types constant-time ou décharge SMT sur les chemins), intégrée
  comme audit au build à côté de l'audit ABI msx64. En parallèle, investigue
  la cause racine du renversement dudect N=200 (|t|=12,39 et 5,19) → N=400
  (tous sous le seuil) : warm-up, turbo/fréquence CPU, outliers, ordre des
  classes ; rejoue avec warm-up contrôlé, affinity et fréquence fixées, ordre
  randomisé, plusieurs runs indépendants par N, et consigne distributions et
  tests robustes en plus des statistiques de Welch. Ne revendique jamais
  "constant time proven" au-delà de ce que les runs signés consignent. ÉTAPE
  DE VÉRIFICATION : après modifications, vérifie l'audit statique par
  contrôles négatifs (des mutants volontairement dépendants du secret doivent
  être attrapés), rejoue l'égalité exacte des traces d'instructions exécutées
  (graine consignée, compte unique par cible sur 120 mesures), et confirme
  que les empreintes des pièces scellées sont inchangées ; consigne chaque
  écart restant comme gap nommé. »

LE PLAN EST GELÉ AVANT TOUTE MESURE (la règle D204/D211 reconduite — le
commit qui porte ce fichier précède la première exécution ; sha256 consigné
au message du commit). AUCUNE donnée de mesure n'existe encore : les six
modules d'obligations ci-dessous sont les CONTRATS, les verdicts attendus
sont des PRÉDICTIONS inscrites avant les runs — un verdict contraire sera
consigné TEL QUEL, jamais plié au prédit.

## L'ÉTAT DE DÉPART (constaté, non mesuré ce chantier)

- Le statut courant des six cibles : « borné par égalité de traces » —
  l'Entrée 320 (vague 5, l'instruction gfylb610p) : l'égalité EXACTE des
  comptages d'instructions entre classes secret-fixe et secret-aléatoire
  (N=60/classe, graine 20261111, UN SEUL compte distinct sur les 120 mesures
  par cible, x25519 = 1 238 959) — un contrôle STRUCTUREL EXACT mais
  DYNAMIQUE : il n'échantillonne pas les secrets, il les fixe par la graine ;
  il couvre les chemins EXÉCUTÉS, pas tous les chemins atteignables.
- Le renversement dudect : le run kit-2 N=200 (journal-dudect-1794557691.csv,
  13/11, le terrain du développeur) a consigné tls13-02 |t|=12,39 et
  tls13-13 |t|=5,19 (> seuil 5), GHASH 3,11 ; le run N=400
  (journal-dudect-1794566245.csv, ~2 h 23 plus tard) : les QUATRE sous le
  seuil (0,84 / 1,55 / −0,30 / 2,02). Les deux journaux BRUTS (1 600 et
  3 200 lignes de mesures, cycles RDTSC + secondes QPC, ordre d'exécution
  conservé) sont consignés au dépôt — la forensie est possible SUR PIÈCES.
- Les pièces scellées au seuil (sha256 constatés, à re-vérifier en V3) :
  m8/proxy.exe 1492b0bc… (l'ancre R7), tls13/proxy.exe 446279f3…,
  loupe/loupe.exe c1115105…, m1/selftest.exe 8038585b….

## LA PARTIE A — L'AUDIT STATIQUE NON BORNÉ (le flux d'information)

### A0 · LE MOTEUR (audit_temps_constant.py, à la racine du dépôt)

Un interpréteur abstrait SYMBOLO-TAINT sur les notations explicites (keystone
assemble → capstone désassemble, le round-trip R5 du dépôt) :

- L'ÉTAT : par point de programme, chaque registre porte (i) une EXPRESSION
  symbolique Z3 BitVec 64 ancrée sur les SYMBOLES DU SECRET (les octets
  d'entrée déclarés secrets par le protocole) et les symboles PUBLICS, et
  (ii) un bit de TAINT (dérivé du secret ou non). Les DRAPEAUX (CF/ZF/SF/
  OF/PF) portent le même couple par drapeau écrit.
- LA MÉMOIRE : cellules (racine, décalage) où la racine est un POINTEUR
  SYMBOLIQUE (SP de la frame courante, P0..P3 les pointeurs d'arguments,
  GLOBAL les données RIP-relatives — les fixtures PUBLIQUES du domaine,
  OS le tampon du système) ; les accès INDICÉS [base + idx*s + d] avec idx
  public lisent le SEAU de la base (l'union des cellules écrites via indice
  — la sur-approximation est SÈCHE : elle ne crée des faux POSITIFS que
  sur des VALEURS taaintées, jamais sur des adresses ou branchements que
  le code ne brancherait pas sinon) ; un idx ou une base TAINTÉE dans une
  ADRESSE = l'obligation ADRESSE (A3) AVANT toute lecture.
- LE FLOW : worklist en fixpoint sur le CFG par fonction (le taaint ne
  croît que — monotonie, terminaison) ; l'INTERPROCEDURAL suit les appels
  DIRECTS aux adresses scellées (les feuilles 09/10/11/12, libc-01/07, le
  sous-programme interne .comprimer de loupe-06) avec mémoïsation par
  signature de taaint d'entrée ; les appels IAT (kernel32/user32) suivent
  des MODÈLES NOMMÉS (ReadFile = LA SOURCE du secret — le tampon rdx
  devient taaint sur r8 octets ; les autres = publics, eax public).
- LE JEU D'INSTRUCTIONS : l'inventaire exact des 45 mnémoniques des blocs
  audités (mov/movzx/movabs/lea, add/sub/adc/sbb/xor/and/or/not, shl/shr/
  sar/ror/rol/shld/shrd, imul/mul, cmp/test/inc/dec, bswap, setcc, xchg,
  push/pop/call/ret/jcc/jmp, rep movsb/stosb, les SSE movdqa/movdqu/pxor/
  pslldq/pshufd et la famille AES-NI aesenc/aesenclast/aeskeygenassist —
  propagation OPAQUE taaint→taaint pour les SIMD, l'AES-NI est constant par
  construction matérielle).

### A1 · LES OBLIGATIONS (les protocoles = les entrées MESURÉES, fidèles)

Les protocoles reprennent EXACTEMENT les classes mesurées (v110 + kit-2) :
ce qui varie entre classes fixe/aléatoire est le SECRET, les longueurs et
les non-variés sont PUBLICS. Les adresses d'entrée sont celles du plan
(tls13/layout.py, loupe/layout.py — source unique).

  O1  sha-256 — tls13-01 (aucun secret, le contrôle trivial) ;
      tls13-02 SOUS DEUX protocoles : (a) bloc 64 o secret (rdx), état
      public ; (b) bloc secret ET état ctx secret (les compressions
      amont) ; tls13-03 : tampon secret (rdx, r8 public), ctx état+
      tampon secrets, longueurs (96, 104) publiques ; tls13-04 : ctx
      état+tampon secrets, longueurs publiques.
      → PRÉDICTION : VERT (les seuls jcc sont sur compteurs et longueurs).
  O2  hmac (tls13-05) — clé 32 o SECRÈTE (rcx, rdx=32 public), message
      public (r8/r9), sortie pile publique.
      → PRÉDICTION : VERT (branch sur test rbx (sortie non-nulle) et
      cmp r13, 64 (longueur de clé) — publics).
  O3  hkdf — tls13-06 : IKM 22 o SECRET (r8, r9 public), sel PUBLIC ;
      LA FAMILLE COMPLÉTÉE : tls13-07/08 (expand/expand-label) sous
      PRK secret (la dérivation aval) — l'instruction nomme la cible
      « hkdf », la famille entière est auditée.
      → PRÉDICTION : VERT.
  O4  x25519 — tls13-14 (rcx sortie, rdx SCALAIRE SECRET) → tls13-13
      (rdx secret, r8 = u PUBLIC — le point de base 9, le kit-2 tient
      aux constant entre classes) → les feuilles 09/10/11/12.
      → PRÉDICTION : VERT (le cswap XOR-masqué : le bit secret atteint
      r10/rbp comme MASQUE, jamais un jcc ni une adresse ; le jz de
      l'inversion teste l'exposant PUBLIC p−2 du fixture).
  O5  aes-gcm — tls13-18 (rcx = clé 16 o SECRÈTE — la round key 0 EST
      la clé, rdx nonce public, r8 texte public, r9/pile publics) →
      15/16/17 ; la famille COMPLÉTÉE : tls13-19 (ouvrir) même protocole.
      → PRÉDICTION : VERT pour 18 ; pour 19 : UN ÉCART NOMMÉ ATTENDU —
      la branche du verdict `test r10, r10 / jnz .divergente` où r10 =
      le OU des 16 différences d'étiquette (secret-dérivé) : l'API
      rend ce bit public (rax = −4 ou la restitution), l'écart sera
      consigné COMME GAP NOMMÉ (classe BRANCHE, public par contrat),
      JAMAIS masqué.
  O6  md5 (loupe-06) — le CONTENU DU FICHIER secret (la source : le
      modèle ReadFile taaint le tampon OS), rcx/rdx/r8 publics, les
      feuilles libc-01 (memcpy) / libc-07 (memset) suivies, le
      sous-programme .comprimer interne audité comme fonction.
      → PRÉDICTION : VERT (les jcc sont sur poignées, longueurs,
      compteurs de rounds, retours IAT publics).

### A2 · LES DEUX CLASSES DE VIOLATION (le critère, la formulation CT)

  CLASSE BRANCHE — un jcc dont les drapeaux testés sont taaintés, un
    jmp/call INDIRECT dont la cible est taaintée, un rep movsb/stosb
    dont le COMPTE (rcx) est taaint (le facteur de travail dépend du
    secret — une dépendance de CONTRÔLE).
  CLASSE ADRESSE — un accès mémoire (lecture/écriture, y compris
    rep movsb/stosb sur [rdi]/[rsi]) dont l'EXPRESSION d'adresse
    (base ou index) est taaintée.

### A3 · LA DÉCHARGE SMT SUR LES CHEMINS (non bornée)

Chaque occurrence des classes ci-dessus n'est PAS un verdict immédiat :
elle devient une OBLIGATION SMT — « pour TOUTES les valeurs du secret
(non borné : les symboles sont libres sur 256^k), la condition de
branchement (resp. l'expression d'adresse) est-elle INVARIANTE ? » :
  - Z3 : la condition sous deux jeux de secrets frais s1 ≠ s2 —
    cond(s1) ≠ cond(s2) SATISFIABLE → CONTRE-EXEMPLE TÉMOIN (les deux
    secrets exhibés, les deux issues) = VIOLATION NOMMÉE ;
  - INSATISFIABLE → DÉCHARGÉE (la dépendance syntaxique était
    sémantiquement nulle — p.ex. un masque forcé à zéro) : l'obligation
    est close SANS faille.
Fail-closed : un UNKNOWN du solveur = VIOLATION (jamais une décharge
par l'ignorance). Les cibles doivent passer À VIDE de toute obligation
— une décharge ne devrait être exercée que par le mutant M7 (le contrôle
positif de la voie SMT).

### A4 · L'INTÉGRATION AU BUILD (à côté de l'audit ABI msx64)

  - tls13/build_m9.py : construire() ET verifier() — après l'oracle
    structurel tls13, l'appel `audit_temps_constant.auditer_tls13(
    code_tls13)` — mêmes conventions que audit_msx64 : les verrous
    comptés, la ligne [audit temps constant] au tableau, EchecBuild sur
    violation ;
  - loupe/build_loupe.py : construire() ET verifier() — `audit_temps_
    constant.auditer_loupe(insns_par_bloc)` à côté de audit_msx64 ;
  - LA PREUVE : les DEUX builds tournent VERTS avec l'audit intégré
    (la sortie consignée aux preuves) — l'audit échoue le build sur
    violation (le mutant M1 le démontre sur le chemin d'intégration).

### A5 · LES CONTRÔLES NÉGATIFS (les mutants — l'instruction l'exige)

Sept mutants générés AUX ATELIERS (les notations scellées JAMAIS
touchées — des COPIES modifiées, assemblées à part) :

  M1  sha-02 · l'échappée précoce — `test edx, edx / jz` sur le mot du
      planning W (secret-dérivé) inséré dans la boucle d'extension.
      → ATTENDU : classe BRANCHE, contre-exemple SMT (un mot W nul /
      non nul — deux secrets, deux issues).
  M2  sha-02 · la table indexée par le secret — le chargement K[64]
      `[rbp + r15*4]` réécrit `[rbp + rax]` où rax = le mot W.
      → ATTENDU : classe ADRESSE.
  M3  x25519-13 · le cswap branché — le masque XOR remplacé par
      `test ebp, 1 / jnz .swap` (la faute de transcription classique).
      → ATTENDU : classe BRANCHE.
  M4  ghash-17 · le repli branché — le masque `sbb rdx, rdx` remplacé
      par `jc .replie` (la retenue du secret).
      → ATTENDU : classe BRANCHE (drapeau CF secret-dérivé).
  M5  loupe-06 · la table md5 indexée par l'octet du message — le
      chargement T[r12] réécrit indexé par le premier octet du bloc.
      → ATTENDU : classe ADRESSE.
  M6  hmac-05 · la clé branchée — `cmp byte ptr [r12], 0 / je .refus`
      sur le premier octet de clé.
      → ATTENDU : classe BRANCHE.
  M7  sha-02 · LE CONTRÔLE POSITIF DE LA DÉCHARGE — `mov eax, W ;
      and eax, 0 ; test eax, eax / jz` : la dépendance est
      syntaxique mais SÉMANTIQUEMENT NULLE.
      → ATTENDU : DÉCHARGÉE par SMT (and eax, 0 ≡ 0 ∀ secret) — la
      voie de décharge REFUSE de sur-signaler (le garde-fou contre
      l'audit qui crierait au loup sur tout ce qui touche le secret).

Un huitième (M8) si le besoin apparaît aux runs — nommé avant exécution.

## LA PARTIE B — LA CAUSE RACINE DU RENVERSEMENT DUDECT N=200→N=400

### B1 · LA FORENSIE SUR LES DEUX JOURNAUX CONSIGNÉS (sur pièces)

Les données : journal-dudect-1794557691.csv (N=200) et
journal-dudect-1794566245.csv (N=400) — cycles RDTSC ET secondes QPC
PAR MESURE, ordre d'exécution conservé (8 blocs : fixe PUIS aléatoire
par cible — l'ordre BLOQUÉ constaté au plan).

  B1a  LE RECOUP : recalculer le t de Welch consigné (12,39 / 5,19 /
       3,11 / 0,94 pour N=200 ; 0,84 / 1,55 / −0,30 / 2,02 pour N=400)
       — cycles ET secondes ; toute divergence = constat premier.
  B1b  L'ARITHMÉTIQUE DU POUVOIR : un effet de classe RÉEL et constant
       donne |t| ≈ δ/σ·√(n/2) — CROISSANT en √n ; le renversement
       12,39→0,84 à n doublé est ARITHMÉTIQUEMENT INCOMPATIBLE avec un
       effet constant — la forensie doit dire QUELLE classe d'artefact.
  B1c  LES QUATRE HYPOTHÈSES (l'instruction les nomme) :
       - WARM-UP : régression des cycles sur le RANG d'itération DANS
         chaque bloc (pente, Spearman) — une dérive monotone intra-
         bloc est la signature d'un échauffement/engourdissement ;
       - TURBO/FRÉQUENCE : la DÉRIVE INTER-BLOCS — le palier fixe→
         aléatoire (les 50 dernières fixe contre les 50 premières
         aléatoire), la pente globale sur TOUT le run, le recoup
         cycles↔secondes (une dérive d'horloge frappe les DEUX
         métriques proportionnellement — un artefact RDTSC non) ;
       - OUTLIERS : quantiles (p50/p90/p99/max), l'effet du TRIMMING
         (5 %, 10 %, 20 %) et de la Winsorisation sur |t| — si le
         |t|=12,39 s'effondre sous trimming, l'excursion était
         portée par la QUEUE ;
       - ORDRE DES CLASSES : l'ANCOVA cycles ~ classe + rang global —
         si le coefficient de classe devient non significatif quand
         le rang est dans le modèle, la « dépendance » était la
         DÉRIVE TEMPORELLE collée à l'ordre bloqué.
  B1d  LES TESTS ROBUSTES (l'instruction l'exige, EN PLUS de Welch) :
       Mann-Whitney U (+ p exact approché), KS deux échantillons,
       médiane et différence de médianes (bootstrap BCa 10 000,
       IC 95 %), le t de Yuen (trimming apparié), le τ de Kendall
       cycles↔rang. Consignés par cible × run × métrique.
  B1e  LE VERDICT FORENSIQUE : la classe d'artefact dominante nommée
       avec ses chiffres, par cible ; ce que le N=200 a vu que le
       N=400 n'a pas vu (ou réciproquement), et POURQUOI le protocole
       v150 l'a permis (l'échauffement 100 appels AVANT la classe fixe
       seulement ; l'ordre bloqué ; __rdtsc non sérialisé — trois
       constats de source, lignes 396-419 de dudect_v150.c).

### B2 · LE REJEU CONTRÔLÉ (dudect_v160 — la démonstration du labo)

Le mesureur v160 (la source à l'atelier, LES DEUX BACKENDS du v150
conservés — POSIX au labo, Windows au terrain) :

  - WARM-UP CONTRÔLÉ : W=200 appels AVANT CHAQUE classe, les DEUX
    classes échauffées (le v150 n'échauffait que la fixe — la faille) ;
  - AFFINITÉ : cœur fixé (SetThreadAffinityMask / sched_setaffinity),
    l'échec NOMMÉ dans le journal (jamais silencieux) ;
  - FRÉQUENCE : au labo la lecture de /sys/devices/system/cpu/*/cpufreq
    (le bac de virtualisation peut ne rien exposer — le GAP SERA NOMMÉ
    si le contrôle est impossible ; au terrain : les consignes powercfg
   高性能 au LISEZMOI — l'état EFFECTIF consigné par le témoin) ;
  - ORDRE RANDOMISÉ : à CHAQUE itération, la classe est tirée par PRNG
    À GRAINE CONSIGNÉE (l'entrelacement canonique dudect — l'ordre
    bloqué du v150 éliminé) ;
  - RUNS MULTIPLES : R=5 runs indépendants par N ∈ {200, 400}, chaque
    run sa graine (consignée), le journal porte run/graine/classe ;
  - LE CHRONOMÈTRE SÉRIALISÉ : lfence ; rdtsc ; lfence (la lecture
    hors-ordre du v150 — l'artefact de mesure nommé) ;
  - LA SORTIE : le journal CSV complet + LE MÊME PIPELINE D'ANALYSE
    que B1 (Welch + robustes + régressions de dérive — le script
    d'analyse UNIQUE, appliqué aux journaux v150 ET v160).

  LA DÉMONSTRATION DU LABO (POSIX, le matériel du labo — étiquette
  « démonstration laboratoire, AUCUN statut terrain », la discipline
  du v150 conservée) :
  - le bras CONTRÔLÉ : les 4 cibles du kit-2 (l'image scellée proxy-
    image.bin recoupée sha256, l'extracteur v150 réutilisé tel quel)
    × N=200/400 × R=5 → PRÉDICTION : tous |t| sous le seuil, les
    tests robustes d'accord, aucune dérive de rang ;
  - le bras TÉMOIN NON CONTRÔLÉ (le v150 tel quel, une seule variante :
    l'ordre bloqué et l'échauffement asymétrique rejoués) →
    PRÉDICTION : la CLASSE de l'artefact N=200 se REPRODUIT au labo
    (des excursions |t|>5 sporadiques portées par la dérive/les
    queues, se dissipant sous trimming) — la démonstration que la
    cause est le PROTOCOLE, pas le code.

### B3 · LA FORMULATION HONNÊTE (l'instruction l'exige)

Jamais « constant time proven » au-delà des runs signés : l'audit A
prouve la propriété STRUCTURELLE (∀ valeurs du secret, non borné :
aucune branche, aucune adresse ne dépend du secret — les cibles
VÉRDIQUO-vertes) ; le temps RÉEL du terrain demeure CE QUE LES RUNS
SIGNÉS CONSIGNENT : le N=200 (deux dépendances au seuil) et le N=400
(les quatre sous le seuil) restent TOUS DEUX des faits — le rapport
les rend côte à côte avec la forensie B1 qui les réconcilie, et le
rejeu v160 du TERRAIN (le geste du développeur, le kit source livré)
tranchera sur SA machine.

## L'ÉTAPE DE VÉRIFICATION (prescrite — après les modifications)

  V1  LES MUTANTS ATTRAPÉS — les 7 contrôles négatifs de A5 : chacun
      NOMMÉ par l'audit (classe + contre-exemple SMT quand la classe
      est BRANCHE), M7 DÉCHARGÉ — le compte exact consigné.
  V2  L'ÉGALITÉ DES TRACES REJOUÉE — la vague 5 (egalite_traces_v180)
      rejouée SUR CLONE FRAIS du dépôt poussé (graine 20261111,
      N=60/classe, UN compte unique par cible sur les 120 mesures,
      x25519 = 1 238 959) — l'audit n'a RIEN changé aux pièces : les
      comptages demeurent BIT-IDENTIQUES.
  V3  LES SCELLES INTACTS — sha256 des pièces scellées re-calculés :
      m8/proxy.exe == 1492b0bc… (l'ancre R7), tls13/proxy.exe ==
      446279f3…, loupe/loupe.exe == c1115105…, m1/selftest.exe ==
      8038585b… (les valeurs constatées au seuil, aucune ne doit
      bouger — l'audit est une LECTURE, il ne retouche RIEN).
  V4  LES BUILDS VERTS — m9 construire + verifier, loupe construire +
      verifier, avec l'audit intégré (A4), sorties consignées.
  V5  LES GAPS NOMMÉS — au minimum attendus : (a) la branche du
      verdict tls13-19 (l'étiquette GCM — public par contrat d'API) ;
      (b) l'exe terrain v160 non compilable au labo cette session
      (la chaîne mingw absente du bac — la source + les consignes
      livrées, le geste au développeur) ; (c) le contrôle de
      fréquence du labo si /sys ne l'expose pas ; tout autre écart
      découvert aux runs sera nommé AVANT toute conclusion.

## LA CONSIGNATION

L'Entrée 330 au worklog, la décision D216 au journal des décisions,
l'atelier entier au dépôt (le plan gelé, le moteur, les mutants, les
journaux d'outils, les preuves, le rapport), les livrables à download/,
la synchro Drive + le push GitHub au commandement du développeur,
l'instruction fkkqc7v8t archivée au /ARCHIVE après exécution — p39uklsca
demeure (le chantier 5, le plan d'extension D210 — les gestes du terrain).

(17/11/2026, la session du flux — gelé avant toute mesure)
