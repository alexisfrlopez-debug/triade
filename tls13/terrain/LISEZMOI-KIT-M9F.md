# KIT TERRAIN M9-(f) — LA SESSION RÉELLE, LA GRANDE ŒUVRE (win)

> Préparé au laboratoire le 06/11/2026, **RÉPARÉ le 07/11/2026 au soir**
> (le chantier (f) : le dernier du jalon — la finale `1.0.0` attend le vert
> de CE run, D104 : le scellage est un fait de carte).
>
> **Deux pièces** : `proxy.exe` est L'ARTEFACT **1.0.0-dev.3** du jalon M9 —
> 65 024 o, sha256
> `de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be66b29226f` —
> le CLIENT TLS 1.3 ENTIER en blocs scellés sur le corps 0.9.0 INTACT
> (la carte génération 11 le prouve, le verrou croisé 86/86 est vert) ;
> `scenario-m9f.py` est LE SCÉNARIO (python SEUL — aucun paquet à
> installer, aucun droit particulier ; le réseau vers
> www.cloudflare.com:443 EST requis, c'est le but même du run).
>
> **L'erratum n° 5 est la raison d'être du build dev.2** : la sonde
> terrain du laboratoire (le 06/11, avant le kit) a prouvé sur pièces
> que le build dev.1 ne pouvait PAS franchir un serveur réel —
> (1) l'octet de longueur du record ClientHello revendiquait 118 octets
> pour un vol de 119 = 5 + 114 : les serveurs réels attendaient 4 octets
> jamais émis (le SILENCE prouvé contre google/github/cloudflare/debian) ;
> (2) les serveurs réels émettent l'enregistrement CCS de compatibilité
> (`14 03 03 00 01 01`) ENTRE leur ServerHello et leur vol protégé — la
> RFC 8446 § 4.1.3 ordonne de l'ignorer, la machine dev.1 en mourrait ;
> (3) les verdicts internes de la machine s'écrivent désormais en 64
> bits (la frontière du kit). La spécification scellée disait déjà TOUT
> CELA (P1 : « 114 ») — la notation a été réparée à la source, le harnais
> 54/54 × 3 graines re-joué VERT, le kit embarque le build réparé.
>
> **L'ERRATUM n° 6 (le kit corrigé le 06/11 au soir, après le premier
> run)** : le premier run (le 06/11 à 16:17, Windows 10.0 build 19045,
> Python 3.14.6) a rendu un verdict ROUGE HONNÊTE, nommé
> `T1.la-résolution` : « le miroir Python refuse “NtCreateFile” :
> répertoire export absent ». LA FAUTE ÉTAIT AU KIT, jamais au terrain :
> T1 passait la base de L'ARTEFACT (`base` = proxy.exe, qui n'a PAS de
> répertoire export) aux lecteurs de SSN, au lieu de la base du VRAI
> ntdll (`ntdll_base`) — le refus était INÉVITABLE sur toute machine. Le
> terrain est LAVÉ par le recoup sur pièces (le VRAI ntdll localisé et
> haché, l'artefact relu INTACT, le scénario exécuté fidèlement : octet
> pour octet celui du labo) ; la réparation est À LA SOURCE (les trois
> sites de résolution reçoivent `ntdll_base`) avec un CONTRÔLE PERMANENT
> à l'assemblage (l'AST exige `ntdll_base` aux trois lecteurs — la faute
> ne peut plus dormir). L'ARTEFACT n'a pas bougé d'un octet : proxy.exe
> demeure le build 1.0.0-dev.2 (sha256 d8928934…). NOTE d'environnement :
> le kit vise Windows 11 (les mesures AFD WinDbg) mais ne l'exige pas —
> le premier run a eu lieu sur Windows 10 22H2 : si votre afd.sys
> diverge, le refus sera NOMMÉ (-6, l'étape en cause) — un échec honnête
> vaut plus qu'un vert muet.

> **L'ERRATUM n° 7 (le kit corrigé le 07/11, après le second run)** : le
> second run (le 06/11 à 16:56, Windows 10.0 build 19045, Python 3.14.6)
> avait traversé T0/T1/T2 VERT — la réparation de l'erratum n° 6 PROUVÉE
> sur la machine réelle, le VRAI afd.sys franchi pour la première fois —
> puis est MORT d'un crash PYTHON nommé sur la console du développeur :
> `TypeError: 'bytes' object does not support item assignment` à la
> ligne 593 (`kit96.raw[:32] = alea`). LA FAUTE ÉTAIT AU KIT, jamais au
> terrain : l'analyse du journal seul (l'Entrée 181) avait acquitté le
> kit « par élimination » (console gelée ? mort du processus ?) — la
> pièce console RENVERSE l'acquittement : `.raw` est une copie bytes
> IMMUABLE, l'écriture par tranches échoue sur TOUTE machine — un crash
> DÉTERMINISTE, jamais une console gelée. TROIS fautes vivaient dans le
> même segment Python pur (aucune machine en vol) : (1) LA POSE DU KIT
> par tranches sur `.raw` — le crash nommé, ligne 593 ; (2) L'ÉCHELLE
> RFC 7748 du recoup : x_3 né à 0 (le point à l'infini — la « clé
> publique attendue » imprimée NULLE, 000…0, le symptôme lisible sur la
> console) ET a24 = (p+1)//4 au lieu de 121665 (la fausse courbe) — le
> recoup T3 aurait été IMPOSSIBLE même sans le crash ; (3) LES SITES
> OUVRIR passaient la TAILLE (96) en r9 là où tls13-27 É1 exige LE
> POINTEUR des 96 o — la machine aurait lu à l'adresse 0x60, la mort au
> premier geste si le crash (1) ne l'avait pas devancée de quatre
> lignes. La réparation est À LA SOURCE (les 96 o posés EN UN GESTE par
> `create_string_buffer` ; `r9 = ctypes.addressof(kit96)` aux DEUX
> sites OUVRIR ; l'échelle == le pseudocode officiel RFC 7748 § 5, LA
> RÉFÉRENCE DU DÉPÔT, éprouvée contre les vecteurs officiels § 6.1 et
> le couple RFC 8448 § 3) avec le CONTRÔLE PERMANENT à l'assemblage
> (l'assembleur porte TROIS portes : AUCUNE écriture `.raw[...]`, LE
> POINTEUR aux DEUX sites OUVRIR, l'échelle re-jouée contre les
> vecteurs officiels — la preuve négative sur la pointe pré-réparation
> 35706ef : les TROIS refus nommés). Le terrain demeure LAVÉ et
> L'ARTEFACT n'a pas bougé d'un octet : proxy.exe demeure le build
> 1.0.0-dev.2 (sha256 d8928934… — relu VERT au T0 du run mort lui-même).

> **L'ERRATUM n° 9 + LA RÉVISION 2 ÉTENDUE (le kit RÉPARÉ le 07/11 au
> soir, après les runs 3-4 et la sonde)** : les troisième et quatrième
> runs (le 07/11) ont traversé T0/T1/T2 VERT — puis sont morts À
> L'ÉMISSION du ClientHello : **-6 NOMMÉ**, chaîne -6 → -7, déterministe
> sur DEUX générations de Windows (10 ET 11 — le suspect
> afd.sys-divergent ÉLIMINÉ SUR PIÈCES). La sonde sys-05 (l'instrument
> livré au quatrième geste) a MESURÉ le NTSTATUS brut :
> **0xC0000005 STATUS_ACCESS_VIOLATION, trois fois, déterministe**.
> LE COUPABLE NOMMÉ À L'INSTRUCTION PRÈS : **LA POSE DU WSABUF** — la
> spec disait « 12 o » (un WSABUF « packé » : len à +0, buf posé à +4)
> alors que le WSABUF CANONIQUE x64 fait **SEIZE octets** (len à +0,
> PADDING d'alignement 4 o, **buf à +8**) : le noyau lit buf à +8, les
> quatre octets hauts du vrai pointeur collés aux immondices de pile →
> l'adresse folle → ACCESS_VIOLATION. Lu dans l'artefact scellé à
> sys-05+0x46 (`89 74 24 60 48 89 7c 24 64`). **La réception sys-06
> portait LE MÊME défaut** (l'erratum n° 9 : le contrat AFD est
> SYMÉTRIQUE, le C_ASSERT send/recv — à la réception le noyau
> ÉCRIRAIT la réponse chez l'adresse folle, la mort à T3 un cran plus
> loin). LA RÉPARATION SELON LA CHARTE : la RÉVISION 2 des DEUX specs
> (sys-05 ET sys-06 — le WSABUF canonique 16 o NOMMÉ, la structure
> totale 40 o), les DEUX notations corrigées (`mov qword ptr
> [rsp+0x68], rdi` — le MÊME encode 5 o, le slot intact), le harnais
> RÉVISÉ (le noyau simulé lit buf à +8 comme le vrai — 131 contrôles ·
> 131 VERTS × 3 graines), l'erratum n° 8 (le jmp rel32 du T6) réparé
> à la source. PUIS LA CÉRÉMONIE : l'arbre m8 a évolué — le garde-sceau
> REFUSAIT tout build (LE SIGNAL, jamais la panne) — la remise étendue
> (m8 sys.1 `c444d730…`) re-signée hors-ligne par la clé du développeur
> (l'ancre des ères `173fae9c…` tenue, les DOUZE arbres inchangés
> byte-identiques — Ed25519 déterministe), la garde **13/13 VERTS**.
> **LE REBUILD 1.0.0-dev.3** : l'héritage 0.9.0 recomposé octet par
> octet (R7), et LE DIFF CONTRÔLÉ — **TROIS octets sur 65 024** : la
> version R10 (0x01000002 → 0x01000003) et LA POSE DU WSABUF dans
> sys-05 ET sys-06 (le disp8 `0x64` → `0x68`) — RIEN d'autre ne bouge.
> Le T0 de CE kit RELIT LA POSE dans l'image aux DEUX blocs (`89 74
> 24 60 48 89 7c 24 68`) : la preuve que le kit embarque le build
> réparé. **LE CINQUIÈME RUN est attendu — le premier du build réparé.**

## 1. Ce que ce kit contient

```
m9-kit/
├── proxy.exe         l'ARTEFACT 1.0.0-dev.3 (65 024 o, sha256
│                     de23e577… — lecture seule pour le run ; la carte
│                     privée ne voyage JAMAIS avec l'artefact, R1) ;
├── scenario-m9f.py   LE SCÉNARIO (python SEUL : ctypes, hashlib, os,
│                     platform, socket, struct, sys, threading, time —
│                     les constantes FIGÉES au laboratoire depuis le
│                     plan du dépôt, recoupées PAR AST contre l'artefact
│                     à l'assemblage — un kit corrompu est un refus
│                     nommé AVANT tout geste) ;
└── LISEZMOI-KIT-M9F.md  le présent document.
```

## 2. Le geste (trois temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99). Sur votre Windows 11 : `m9-kit/`.
2. **Lancer** : `python scenario-m9f.py` (ou `py`/`python3` selon votre
   installation — **un Python 64 bits est requis**). Aucun paquet à
   installer, aucun droit particulier ; le réseau doit être vivant (la
   cible : www.cloudflare.com:443). Le run dure ~10 secondes et dit
   tout à l'écran ; chaque constat est tranché binaire, le verdict se
   rend POST-MORTEM. Si rien ne bouge au-delà de 300 secondes, la
   garde-chien du scénario vous le dira et rendra la main — un
   transport muet est une information, jamais une attente.
3. **Renvoyer** le dossier `preuves-m9f/` ENTIER au coffre
   `/test/preuves-m9f/` (dossier Drive « Triade » → « test ») : les
   pièces naissent toutes seules —
   - `temoin-m9f.txt` — l'environnement (Windows, Python, le VRAI ntdll
     localisé et haché), les SSN des TROIS noms lus par les DEUX
     lecteurs, l'empreinte épinglée, chaque contrôle tranché ;
   - `scenario-m9f-journal.log` — le journal horodaté du run ;
   - `VERDICT-run-m9f.txt` — le verdict post-mortem ;
   - `ligne-recue.txt` — la ligne applicative DÉCHIFFRÉE PAR LA MACHINE
     (la réponse HTTP reçue chiffrée, restituée en clair) ;
   - `journal-emissions.txt` — TOUT ce que la machine a émis (le CH
     recoupé octet par octet, le Finished client, la ligne scellée, le
     close_notify).

## 3. Ce que le scénario démontre (les temps du run)

- **T0 LE TÉMOIN** : l'empreinte de l'artefact ASSERTÉE avant tout geste ;
  le VRAI ntdll localisé et haché ; l'artefact cartographié
  (LoadLibraryEx DONT_RESOLVE — le scénario est le CHARGEUR, jamais
  l'exécutant de l'artefact entier) ; les octets attendus constatés UN
  PAR UN — dont **l'octet de l'erratum n° 5 relu dans l'image**
  (`41 C7 02 16 03 03 00 41 C6 42 04 72` @0x10082 : la preuve que le
  kit embarque le build réparé) ; la cible résolue par DNS.
- **T1 LA RÉSOLUTION** : le VRAI ntdll lu par DEUX lecteurs indépendants —
  la marche EAT refaite en PYTHON et le BLOC sys-02 appelé à son adresse
  scellée — LE MÊME SSN pour NtCreateFile, NtDeviceIoControlFile et
  NtClose ; le MOTIF du stub confronté (`4C 8B D1 B8` avant l'imm32 :
  un stub crocheté — un hook — est un REFUS NOMMÉ, jamais un numéro
  extrait).
- **T2 L'ÉTABLISSEMENT** : le socket TCP par le **VRAI afd.sys** — sys-04
  à son adresse scellée : NtCreateFile sur `\Device\Afd\Endpoint`, bind
  implicite WILDCARD, connect SYNCHRONE — TROIS appels NT, chaque SSN
  résolu AU GESTE MÊME, **zéro ws2_32** (la surface de hook que M8 a
  nommée — le socket natif SANS une seule entrée d'import réseau).
- **T3 LA SESSION** : LA POIGNÉE ENTIÈRE par LE CLIENT TLS 1.3 DE
  L'ARTEFACT — tls13-27 (la machine d'états) appelé à son adresse
  scellée, le socle tls13-28 câblé aux rappels DU KIT (émettre/recevoir
  → sys-05/sys-06 → les SYSCALLS DIRECTS). Le kit fournit TOUT : l'aléa,
  le couple x25519, L'EMPREINTE ÉPINGLÉE (96 o, le contrat P1 de la
  machine). **LE RECOUP** : le ClientHello émis par la machine ==
  `16 03 03 00 72` + la construction re-jouée en Python pur (114 o,
  l'aléa du kit à +6, la clé publique à +82 == l'échelle RFC 7748
  refaite en Python — les DEUX lecteurs, encore). L'état 3 (CONNECTÉ).
- **T4 LA LIGNE** : la ligne applicative CHIFFRÉE ÉCHANGÉE — É2 ÉMETTRE
  (le GET scellé par LA MACHINE sous SES clés), É3 RECEVOIR (la
  réponse DÉCHIFFRÉE PAR LA MACHINE) ; le témoin « HTTP/1.1 200 OK »
  cherché dans le flux EN CLAIR restitué ; les éventuels tickets de
  session traversent comme données et sont ignorés.
- **T5 L'ÉPINGLAGE** : LA FALSIFICATION CONTRE LE VRAI SERVEUR — une
  seconde session, l'empreinte MUTÉE d'un bit → le certificat réel
  offert n'est pas celui qu'on attend → **-6 NOMMÉ** (l'épinglage
  divergent), l'état 5 (MORT), le journal == l'offre seule. La
  confiance est une COMPARAISON, jamais une croyance — la garde est
  constatée sur le monde réel.
- **T6 LA CLÔTURE** : É4 FERMER (le close_notify composé, scellé et
  émis PAR LA MACHINE — 24 o) ; puis la fermeture des handles — LE
  GESTE DU KIT (I8 de sys-04) : NtClose résolu par sys-02, ÉMIS PAR
  SYS-01, le trombone ABI, via un trampoline à deux instructions
  (ctypes ne peut pas charger rax — le trampoline le fait) ; proxy.exe
  relu inchangé, la cartographie libérée.

## 4. Les frontières nommées (l'honnêteté du terrain)

- **Le certificat épinglé est servi SANS SNI** : le ClientHello du jalon
  ne porte pas l'extension nom-de-serveur (I3 de tls13-22 : « le kit
  cible le serveur par son adresse, l'épinglage fait la confiance »).
  www.cloudflare.com répond alors avec le certificat de son vhost par
  défaut — **CN=www.cloudflare.com, émis par Let's Encrypt (YR2),
  RSA-2048, valide 2026-11-01 → 2027-01-30** — l'empreinte épinglée
  (sha256 du DER) :
  `045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af3259b106f72f`.
  **Un renouvellement côté serveur** (Let's Encrypt renouvelle tous
  les ~60-90 jours) fera échouer T3 par -6 NOMMÉ : c'est la NATURE de
  l'épinglage — renvoyez les pièces, le labo re-gèle l'empreinte.
  L'analyse X.509 complète reste le CHANTIER FUTUR NOMMÉ (tls13-26) :
  le jalon COMPARE, il ne fait pas confiance en silence.
- **Le socle socket (sys-04/05/06)** fut prouvé au labo sur le MODÈLE
  STRICT du noyau — **le harnais RÉVISÉ de la révision 2** (le noyau
  simulé lit buf à +8 comme le VRAI) re-passe 131 contrôles · 131 VERTS
  × 3 graines ; la séquence create/bind/connect vient des mesures
  WinDbg de Windows 11 (« Under the Hood of AFD.sys », leftarcode 2025).
  LA POSE DU WSABUF fut MESURÉE SUR LE VRAI NOYAU par la sonde sys-05
  (le STATUS_ACCESS_VIOLATION déterministe, trois fois) : la réparation
  est NOMMÉE à l'instruction, jamais une devinette. Si votre afd.sys
  diverge, le verdict sera -6 NOMMÉ avec l'étape
  nommée — un échec honnête vaut plus qu'un vert muet.
- **Les causes NTSTATUS vivent dans rdx** au moment des verdicts -6 de
  sys-04/05/06 (le contrat) : ctypes ne restitue que rax — le kit NOMME
  l'étape en échec, l'information exacte existe dans les octets, la
  limite de l'instrument est nommée ici.
- **Sous Python, le scénario utilise ctypes** pour charger l'artefact
  et appeler les blocs à leurs adresses scellées, et pour câbler ses
  propres rappels de transport au socle de la machine — c'est le moyen
  standard d'invoquer du code natif depuis un script. Le CODE appelé
  est celui de l'ARTEFACT (vérifié par empreinte avant tout appel) ;
  le scénario n'embarque AUCUN octet de code exécuté — seulement les
  attendus, les rappels de transport et les pièces. Le réseau, lui,
  n'est JAMAIS touché par Python : chaque octet émis ou reçu passe par
  les SYSCALLS DIRECTS de l'artefact (sys-05/sys-06).

## 5. Après le run

- Si le verdict est **VERT** : renvoyer `preuves-m9f/` au coffre
  `/test/preuves-m9f/` — le laboratoire recoupe sur pièces
  (D138/D145/D148 : témoin ↔ journal ↔ verdict ↔ émissions recoupés
  ENTRE EUX) et, si elles établissent le critère, la **finale 1.0.0**
  est posée (fait de carte) : **le jalon M9 franchi — LA GRANDE
  ŒUVRE : le client TLS 1.3 entier en blocs scellés, zéro délégation
  cryptographique, la souveraineté complète.**
- Si un constat dit **ÉCHEC NOMMÉ** : renvoyer `preuves-m9f/` TEL QUEL —
  la ligne nomme le défaut ; un échec honnête vaut plus qu'un vert
  muet (l'ordre lexicographique de la maison : la vérité d'abord).

*Le laboratoire ne peut PAS rejouer ce kit (Windows + le VRAI ntdll + le
VRAI afd.sys exigés — le cœur même du chantier). Le labo a fait ce qu'il
peut : le client de RÉFÉRENCE en Python (la sonde du 06/11) a rejoué le
protocole EXACT du kit contre la MÊME cible — le calendrier recoupé sur
les pièces RFC 8448, la poignée entière, le certificat épinglé, la ligne
reçue — et le kit est éprouvé par l'assemblage : chaque constante du
scénario recoupée contre l'artefact, la compilation vérifiée,
l'extraction vierge constatée.*
