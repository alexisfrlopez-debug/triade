# KIT SONDE SYS-06 — LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE (win)

> Préparé au laboratoire le 07/11/2026 (la sonde NOMMÉE D'AVANCE par le
> recoup du cinquième run et la passation 107 — le miroir de l'Entrée
> 185 ; OUVERTE par le recoup du sixième run : LE JUMEAU CONSTATÉ PAR
> CODE — le journal du run 6 == le journal du run 5 ligne à ligne,
> l'émission VERT deux fois, la réception immédiate -7 deux fois, le
> run en SA seconde deux fois, le bord DNS changé — **LE PASSAGER
> ÉLIMINÉ SUR PIÈCES** ; restent le contrat de réception sys-06 et LA
> DEMI-FIN : il ne manque qu'UNE information — LE CODE EXACT de la
> première lecture réelle que l'instrument ne remonte pas).
>
> **Deux pièces** : `proxy.exe` est L'ARTEFACT **1.0.0-dev.3 RÉPARÉ** —
> LE MÊME que le kit m9f actuel, **INTACT** (65 024 o, sha256
> `de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be66b29226f` —
> relu au T0 du run, il n'a pas bougé d'un octet : la sonde NE
> RECONSTRUIT RIEN) ; `scenario-sonde-sys06.py` est LE SCÉNARIO (python
> SEUL — aucun paquet à installer ; le réseau vers
> www.cloudflare.com:443 est requis, c'est le geste même de la mesure).
>
> **LA MISSION** : le bloc sys-06 (spec m8/I/sys-06-reception.md,
> RÉVISION 2) rend n ≥ 1 à la lecture réussie, **-6 quand le noyau a
> rendu un STATUS non nul — et CONSIGNE LE NTSTATUS BRUT DANS RDX**
> (Q5) ; LE ZÉRO EST LA DEMI-FIN (Q2 : le pair a fermé proprement →
> **-7**, rdx = 0)**. Le scénario m9f ne lit que rax : LE CODE EXACT
> EST LA LIMITE NOMMÉE DE L'INSTRUMENT — les runs 5/6 y sont morts. La
> sonde la franchit par UN TRAMPOLINE DE CAPTURE — 33 octets posés au
> run (VirtualAlloc, le MÊME geste que le trampoline NtClose du kit m9f
> T6), qui appelle LE MÊME BLOC sys-06 à son adresse scellée et rend le
> code ET le NTSTATUS empaquetés. **L'artefact reste INTACT : la sonde
> n'écrit JAMAIS dans son image** (relue inchangée à la fin du run).
>
> **LE GESTE M9F DÉCOMPOSÉ** : la sonde ne réinvente rien — elle rejoue
> LE GESTE EXACT des runs 5/6 en deux temps mesurés : (1) le
> ClientHello DE RÉFÉRENCE du jalon (16 03 03 00 72 || 114 o — la MÊME
> construction que le recoup m9f, composée en Python : l'aléa et la clé
> de la sonde) émis par **sys-05 DIRECT** — le chemin RÉPARÉ du kit,
> vert aux runs 5/6 : la reproduction ; (2) **LA PREMIÈRE LECTURE par
> LE TRAMPOLINE** — là où les deux runs sont morts. Le compas
> étalonné AVANT la mesure (un handle invalide → -6 +
> STATUS_INVALID_HANDLE) : la preuve que la capture lit VRAIMENT rdx.

## 1. Ce que ce kit contient

```
sonde-sys06-kit/
├── proxy.exe                l'ARTEFACT 1.0.0-dev.3 RÉPARÉ (65 024 o,
│                            sha256 de23e577… — LE MÊME que le kit m9f,
│                            lecture seule pour le run) ;
├── scenario-sonde-sys06.py  LA SONDE (python SEUL : ctypes, hashlib, os,
│                            platform, socket, struct, sys, threading,
│                            time — les constantes FIGÉES au laboratoire,
│                            recoupées PAR AST contre l'artefact à
│                            l'assemblage ; la table NTSTATUS recoupée
│                            aux sources canoniques ntstatus.h — Wine ET
│                            ReactOS s'accordent au bit près) ;
└── LISEZMOI-KIT-SONDE-SYS06.md  le présent document.
```

## 2. Le geste (trois temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais
   mélanger les runs — D99). Windows 11 ou Windows 10 — le -7 constaté
   est INTER-GÉNÉRATIONS, la machine importe peu.
2. **Lancer** : `python scenario-sonde-sys06.py` (**un Python 64 bits
   est requis**). Aucun paquet, aucun droit ; le réseau doit être
   vivant (la cible : www.cloudflare.com:443). Le run dure ~15 secondes
   (il porte un délai de 2 s volontaire : la variation DÉLAI) ; au-delà
   de 300 s la garde-chien rend la main.
3. **Renvoyer** le dossier `preuves-sonde-sys06/` ENTIER au coffre
   `/test/preuves-sonde-sys06/` (dossier Drive « Triade » → « test ») :
   - `temoin-sonde-sys06.txt` — l'environnement, les T0 (dont LES DEUX
     contrôles erratum-9 : la pose du WSABUF canonique relue DANS
     L'IMAGE aux DEUX blocs), **LES OCTETS DU TRAMPOLINE consignés**
     (la preuve lisible de ce qui est exécuté), l'offre (sys-05 direct)
     et CHAQUE lecture : code + NTSTATUS NOMMÉ + classe de sévérité ;
   - `sonde-sys06-journal.log` — le journal horodaté ;
   - `VERDICT-sonde-sys06.txt` — le verdict post-mortem ;
   - (`ligne-recue.txt`, `journal-emissions.txt` ne naissent QUE si la
     contre-épreuve S4 a tenu — la percée).

## 3. Ce que la sonde mesure (les temps du run)

- **T0/T1/T2 — LE MÊME TRIPTYQUE QUE M9F** : l'artefact relu (sha +
  taille + LES DEUX contrôles T0.erratum-9 [la pose du WSABUF
  canonique, 89 74 24 60 48 89 7c 24 68, relue DANS L'IMAGE à sys-05
  @+0x46 ET sys-06 @+0x46] + les têtes des SIX slots + les fixtures +
  l'octet 0x72 de l'erratum n° 5), le VRAI ntdll lu par les DEUX
  lecteurs (SSN 85/7/15 attendus), l'endpoint AFD établi par le VRAI
  afd.sys (sys-04 : create + bind + connect, TROIS appels NT, zéro
  ws2_32).
- **S3 LA MESURE — LE CŒUR, LE GESTE M9F DÉCOMPOSÉ** :
  - **(a) le trampoline posé**, ses 33 octets consignés au témoin :
    `sub rsp,0x28 ; mov rax,sys-06 ; call rax ; shl rdx,32 ; mov ecx,eax ;
    or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret` — l'ABI msx64
    respectée (shadow space + pile alignée) ;
  - **(b) LE COMPAS ÉTALONNÉ** : un handle invalide (0xDEAD0000) doit
    rendre -6 + STATUS_INVALID_HANDLE (0xC0000008) — la preuve que la
    capture lit VRAIMENT rdx. **Un compas muet arrête la sonde**
    (fail-closed : un instrument non étalonné ne mesure pas) ;
  - **(c) LA MESURE** : le ClientHello DE RÉFÉRENCE émis par **sys-05
    DIRECT** sur l'endpoint frais (le chemin réparé — la reproduction
    des runs 5/6), PUIS **LA PREMIÈRE LECTURE PAR LE TRAMPOLINE** :
    le code exact ENFIN LU — n ≥ 1 (LE SERVERHELLO ARRIVÉ : la tête du
    flux consignée), -7 + rdx 0 (LE ZÉRO : LA DEMI-FIN), ou -6 + le
    NTSTATUS brut NOMMÉ ;
  - **(d) LA VARIATION TAILLE** : une capacité d'UN octet (la borne
    minimale du contrat P4) sur une session FRAÎCHE sacrifiée (jamais
    réutilisée) ;
  - **(e) LA VARIATION DÉLAI** : la lecture re-tentée APRÈS 2 s (le
    refus est-il transitoire ? un PENDING qui n'a pas mûri ?).
- **S4 LA CONTRE-ÉPREUVE** : LA POIGNÉE par LE RAPPEL STANDARD (le
  chemin du kit m9f, SANS le trampoline) sur une session NEUVE —
  tls13-27 OUVRIR (le CH composé PAR LA MACHINE, émis par sys-05
  direct, lu par sys-06 direct), et si la session tient : LA LIGNE
  applicative (É2/É3 : le GET scellé, la réponse DÉCHIFFRÉE PAR LA
  MACHINE, le témoin « HTTP/1.1 200 OK ») — **si la poignée tient, LA
  PERCÉE est consignée : le jalon en vue** ; si elle meurt au même
  geste, la NON-RÉGRESSION est constatée (le chemin standard et le
  trampoline meurent ENSEMBLE : la mesure du trampoline parle pour les
  DEUX).
- **T6 LA CLÔTURE** : le close_notify de la machine si une session
  vit ; les handles fermés (NtClose par le trombone sys-01) ; le
  trampoline de capture LIBÉRÉ ; proxy.exe relu INCHANGÉ ; la
  cartographie libérée.

## 4. La table des NTSTATUS (ce que chaque lecture veut dire)

La sonde NOMME ce qu'elle lit, et la CLASSE de sévérité tranche les
candidats restants du recoup du sixième run (le passager est MORT sur
pièces — restent le contrat de réception et la demi-fin) :

| Si la lecture dit… | classe | le coupable |
|---|---|---|
| `rax = n ≥ 1` | — | **LE SERVERHELLO ARRIVÉ — LA PERCÉE** : la lecture vit sur le vrai noyau ; la contre-épreuve S4 dira si la machine d'états passe aussi (si oui : la finale 1.0.0 en vue — LE JALON M9). |
| `rax = -7`, rdx = 0 | — | **LA DEMI-FIN (sys-06 Q2)** : le pair a refermé PROPREMENT à l'offre — l'offre SANS SNI refermée par le bord : le geste sera la cible ou le SNI, le kit m9f demeure acquitté. |
| `STATUS_PENDING` (0x00000103) | SUCCÈS | **LE BUG DU CONTRAT** : le noyau n'a pas REFUSÉ, il n'a pas FINI — le bloc rend -6 sur tout status non nul, y compris les statuses de classe SUCCÈS. La réparation : l'erratum de la notation + la révision de la spec sys-06. |
| `STATUS_INVALID_PARAMETER` (0xC000000D) | ERREUR | **LE CONTRAT D'APPEL** (le candidat restant) : l'IOCTL_AFD_RECEIVE 0x12017 ou l'AFD_RECV_INFO de 24 o tel que le bloc la pose. |
| `STATUS_INVALID_DEVICE_REQUEST` (0xC0000010) | ERREUR | l'IOCTL inconnu du périphérique : le contrat, encore. |
| `STATUS_INVALID_DEVICE_STATE` (0xC0000184) | ERREUR | **L'ÉTAT DE L'ENDPOINT** : la socket pas dans l'état attendu pour un RECEIVE au moment de l'appel. |
| `STATUS_CONNECTION_RESET` / `REFUSED` / `GRACEFUL_DISCONNECT` / `REMOTE_DISCONNECT` | ERREUR | **LE PAIR OU LE RÉSEAU** : le serveur ou un intermédiaire a fermé (la demi-fin brutale — à distinguer du zéro propre par le STATUS lui-même). |

*(la table complète — 23 noms — vit dans le scénario, recoupée aux
sources canoniques ntstatus.h : Wine et ReactOS, au bit près).*

## 5. Les frontières nommées (l'honnêteté du terrain)

- **LA MISSION EST LA MESURE, PAS LA FINALE** : un verdict « VERT — LA
  MESURE RENDUE » n'est PAS le vert du critère M9-(f) — la finale 1.0.0
  attend le run m9f complet (la falsification T5 y vit : la confiance
  est une comparaison). Si la lecture condamne LE CONTRAT DU BLOC : la
  réparation sera UN ERRATUM DE LA NOTATION + LA RÉVISION DE LA SPEC
  sys-06, jamais une dérive silencieuse ; si elle nomme LE ZÉRO (la
  demi-fin propre) : le kit m9f demeure acquitté, le geste sera la
  cible ou le SNI ; si LA LECTURE REND DES OCTETS : LA PERCÉE — la
  poignée suit DANS LE MÊME RUN.
- **Le trampoline de capture est UN GESTE D'INSTRUMENT**, pas une
  modification de l'artefact : 33 octets dans SA PROPRE page
  VirtualAlloc, jamais dans l'image de proxy.exe (relue inchangée à la
  fin du run) ; les octets sont CONSIGNÉS AU TÉMOIN — ce qui est
  exécuté est LISIBLE. Le réseau n'est touché QUE par les blocs de
  l'artefact (sys-06 via le trampoline appelle LE MÊME bloc — le geste
  mesuré est LE GESTE du run m9f, pas une réécriture ; l'offre passe
  par sys-05 DIRECT, le chemin réparé vert deux fois).
- **Les variations (d)/(e) sont des gestes EXPÉRIMENTAUX nommés** : la
  session sacrifiée de la variation TAILLE n'est JAMAIS réutilisée ; la
  contre-épreuve S4 court TOUJOURS sur une session NEUVE ET VIERGE.
- **Sous Python, la sonde utilise ctypes** pour charger l'artefact et
  appeler les blocs à leurs adresses scellées — le MÊME moyen standard
  que le kit m9f ; le CODE appelé est celui de L'ARTEFACT (vérifié par
  empreinte avant tout appel).

## 6. Après le run

- **Quel que soit le verdict** (VERT-MESURE, PERCÉE, ou ROUGE nommé) :
  renvoyer `preuves-sonde-sys06/` TEL QUEL au coffre
  `/test/preuves-sonde-sys06/` — le laboratoire recoupe sur pièces
  (D138/D145/D148), NOMME le coupable (le contrat du bloc sys-06, ou
  la demi-fin du pair) et répare selon la charte : l'erratum de la
  notation le cas échéant, la révision de la spec sys-06 — puis LE RUN
  M9F réparé suivra, et avec lui la finale 1.0.0 : le jalon M9 — LA
  GRANDE ŒUVRE.

*Le laboratoire ne peut PAS rejouer ce kit (Windows + le VRAI ntdll +
le VRAI afd.sys exigés). Le labo a fait ce qu'il peut : le squelette du
trampoline vérifié octet par octet à l'assemblage, le dépaquetage
éprouvé sur les quatre cas (le signe 32 bits, PENDING, le compte
reçu, le succès), l'alignement de pile msx64 démontré, la table
NTSTATUS recoupée aux DEUX sources canoniques, chaque constante du
scénario recoupée contre l'artefact — et la contre-épreuve S4
embarquée : si la lecture rend des octets, la poignée suit DANS LE
MÊME RUN.*
