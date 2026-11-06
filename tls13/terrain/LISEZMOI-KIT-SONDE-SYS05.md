# KIT SONDE SYS-05 — LE NTSTATUS BRUT DE L'ÉMISSION (win)

> Préparé au laboratoire le 07/11/2026 (le chantier (g), promis par le recoup
> du quatrième run : le geste (ii) du recoup-3 accompli — Windows 11 essayé,
> le -6 À L'IDENTIQUE, le suspect « divergence afd.sys Win10 ↔ Win11 »
> ÉLIMINÉ sur pièces ; le refus est INTER-GÉNÉRATIONS, il ne reste qu'UNE
> information manquante : LE NTSTATUS BRUT que l'instrument ne remonte pas).
>
> **Deux pièces** : `proxy.exe` est L'ARTEFACT **1.0.0-dev.2** — LE MÊME que
> le kit m9f, **INTACT** (65 024 o, sha256
> `d892893469608fd69e381b92b8e18623107bd2bc694f43a512bc5900773dc314` —
> relu au T0 du run, il n'a pas bougé d'un octet : la sonde NE RECONSTRUIT
> RIEN) ; `scenario-sonde-sys05.py` est LE SCÉNARIO (python SEUL — aucun
> paquet à installer ; le réseau vers www.cloudflare.com:443 est requis,
> c'est le geste même de la mesure).
>
> **LA MISSION** : le bloc sys-05 rend -6 quand le noyau rend un STATUS non
> nul — et la spec (m8/I/sys-05-emission.md, Q5) dit : « rdx = le NTSTATUS
> brut consigné ». Le scénario m9f ne lit que rax : LE NTSTATUS EST LA
> LIMITE NOMMÉE DE L'INSTRUMENT. La sonde la franchit par UN TRAMPOLINE DE
> CAPTURE — 33 octets posés au run (VirtualAlloc, le MÊME geste que le
> trampoline NtClose du kit m9f T6 : « ctypes ne peut pas charger rax, le
> trampoline le fait » — ici : ctypes ne peut pas LIRE rdx, le trampoline
> le rend), qui appelle LE MÊME BLOC sys-05 à son adresse scellée et rend
> le code ET le NTSTATUS empaquetés. **L'artefact reste INTACT : la sonde
> n'écrit JAMAIS dans son image** (relue inchangée à la fin du run).

## 1. Ce que ce kit contient

```
sonde-sys05-kit/
├── proxy.exe                l'ARTEFACT 1.0.0-dev.2 (65 024 o, sha256
│                            d8928934… — LE MÊME que le kit m9f, lecture
│                            seule pour le run) ;
├── scenario-sonde-sys05.py  LA SONDE (python SEUL : ctypes, hashlib, os,
│                            platform, socket, struct, sys, threading,
│                            time — les constantes FIGÉES au laboratoire,
│                            recoupées PAR AST contre l'artefact à
│                            l'assemblage ; la table NTSTATUS recoupée
│                            aux sources canoniques ntstatus.h — Wine ET
│                            ReactOS s'accordent au bit près) ;
└── LISEZMOI-KIT-SONDE-SYS05.md  le présent document.
```

## 2. Le geste (trois temps)

1. **Extraire** le zip COMPLET dans un NOUVEAU dossier (ne jamais mélanger
   les runs — D99). Windows 11 ou Windows 10 — le refus constaté est
   INTER-GÉNÉRATIONS, la machine importe peu.
2. **Lancer** : `python scenario-sonde-sys05.py` (**un Python 64 bits est
   requis**). Aucun paquet, aucun droit ; le réseau doit être vivant (la
   cible : www.cloudflare.com:443). Le run dure ~15 secondes (il porte un
   délai de 2 s volontaire : la variation DÉLAI) ; au-delà de 300 s la
   garde-chien rend la main.
3. **Renvoyer** le dossier `preuves-sonde-sys05/` ENTIER au coffre
   `/test/preuves-sonde-sys05/` (dossier Drive « Triade » → « test ») :
   - `temoin-sonde-sys05.txt` — l'environnement, les T0, **LES OCTETS DU
     TRAMPOLINE consignés** (la preuve lisible de ce qui est exécuté), et
     CHAQUE lecture : code + NTSTATUS NOMMÉ + classe de sévérité ;
   - `sonde-sys05-journal.log` — le journal horodaté ;
   - `VERDICT-sonde-sys05.txt` — le verdict post-mortem ;
   - (`ligne-recue.txt`, `journal-emissions.txt` ne naissent QUE si la
     contre-épreuve S4 a tenu — la percée).

## 3. Ce que la sonde mesure (les temps du run)

- **T0/T1/T2 — LE MÊME TRIPTYQUE QUE M9F** : l'artefact relu (sha + taille
  + les têtes des SIX slots + les fixtures + l'octet 0x72 de l'erratum
  n° 5), le VRAI ntdll lu par les DEUX lecteurs (SSN 85/7/15 attendus),
  l'endpoint AFD établi par le VRAI afd.sys (sys-04 : create + bind +
  connect, TROIS appels NT, zéro ws2_32).
- **S3 LA MESURE — LE CŒUR** :
  - **(a) le trampoline posé**, ses 33 octets consignés au témoin :
    `sub rsp,0x28 ; mov rax,sys-05 ; call rax ; shl rdx,32 ; mov ecx,eax ;
    or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret` — l'ABI msx64
    respectée (shadow space + pile alignée) ;
  - **(b) LE COMPAS ÉTALONNÉ** : un handle invalide (0xDEAD0000) doit
    rendre -6 + STATUS_INVALID_HANDLE (0xC0000008) — la preuve que la
    capture lit VRAIMENT rdx. **Un compas muet arrête la sonde**
    (fail-closed : un instrument non étalonné ne mesure pas) ;
  - **(c) LA MESURE** : LE ClientHello DE RÉFÉRENCE du jalon (16 03 03 00
    72 || 114 o — la MÊME construction que le recoup m9f, composée en
    Python : l'aléa et la clé de la sonde) émis par LE TRAMPOLINE sur
    l'endpoint frais : **LE NTSTATUS BRUT DU GESTE M9F, LU ET NOMMÉ** ;
  - **(d) LA VARIATION TAILLE** : un octet seul sur une session FRAÎCHE
    sacrifiée (jamais réutilisée : un octet parti pollue le flux) ;
  - **(e) LA VARIATION DÉLAI** : le CH re-tenté APRÈS 2 s (le refus
    est-il transitoire ? un PENDING qui n'a pas mûri ?).
- **S4 LA CONTRE-ÉPREUVE** : LA POIGNÉE par LE RAPPEL STANDARD (le chemin
  du kit m9f, SANS le trampoline) sur une session NEUVE — tls13-27 OUVRIR
  (le CH composé PAR LA MACHINE, émis par sys-05 direct), et si la session
  tient : LA LIGNE applicative (É2/É3 : le GET scellé, la réponse
  DÉCHIFFRÉE PAR LA MACHINE, le témoin « HTTP/1.1 200 OK ») — **si la
  poignée tient, LA PERCÉE est consignée : le jalon en vue** ; si elle
  meurt au même geste, la NON-RÉGRESSION est constatée (le chemin standard
  et le trampoline meurent ENSEMBLE : la mesure du trampoline parle pour
  les DEUX).
- **T6 LA CLÔTURE** : le close_notify de la machine si une session vit ;
  les handles fermés (NtClose par le trombone sys-01 — le trampoline à
  deux instructions du kit m9f) ; le trampoline de capture LIBÉRÉ ;
  proxy.exe relu INCHANGÉ ; la cartographie libérée.

## 4. La table des NTSTATUS (ce que chaque lecture veut dire)

La sonde NOMME ce qu'elle lit, et la CLASSE de sévérité tranche les
candidats nommés par le recoup du quatrième run :

| Si la lecture dit… | classe | le coupable |
|---|---|---|
| `STATUS_PENDING` (0x00000103) | SUCCÈS | **LE BUG DU CONTRAT** : le noyau n'a pas REFUSÉ, il n'a pas FINI — le bloc rend -6 sur tout status non nul, y compris les statuses de classe SUCCÈS/AVERTISSEMENT. La réparation : l'erratum de la notation + la révision 2 de la spec sys-05. |
| `STATUS_INVALID_PARAMETER` (0xC000000D) | ERREUR | **LE CONTRAT D'APPEL** (le candidat (b)) : l'IOCTL_AFD_SEND 0x1201F ou l'AFD_SEND_INFO de 24 o tel que le bloc le pose. |
| `STATUS_INVALID_DEVICE_REQUEST` (0xC0000010) | ERREUR | l'IOCTL inconnu du périphérique : le contrat, encore. |
| `STATUS_INVALID_DEVICE_STATE` (0xC0000184) | ERREUR | **L'ÉTAT DE L'ENDPOINT** (le candidat (c)) : la socket pas dans l'état attendu pour un SEND au moment de l'appel. |
| `STATUS_CONNECTION_RESET` / `REFUSED` / `GRACEFUL_DISCONNECT` / `REMOTE_DISCONNECT` | ERREUR | **LE PAIR OU LE RÉSEAU** (le candidat (d)) : le serveur ou un intermédiaire a fermé. |

*(la table complète — 23 noms — vit dans le scénario, recoupée aux
sources canoniques ntstatus.h : Wine et ReactOS, au bit près).*

## 5. Les frontières nommées (l'honnêteté du terrain)

- **LA MISSION EST LA MESURE, PAS LA FINALE** : un verdict « VERT — LA
  MESURE RENDUE » n'est PAS le vert du critère M9-(f) — la finale 1.0.0
  attend le run m9f complet (la falsification T5 y vit : la confiance est
  une comparaison). Si la lecture condamne LE CONTRAT DU BLOC : la
  réparation sera UN ERRATUM DE LA NOTATION + LA RÉVISION 2 DE LA SPEC
  sys-05, jamais une dérive silencieuse ; si elle nomme LE RÉSEAU : la
  cible ou le chemin en cause, le kit m9f demeure acquitté.
- **Le trampoline de capture est UN GESTE D'INSTRUMENT**, pas une
  modification de l'artefact : 33 octets dans SA PROPRE page VirtualAlloc,
  jamais dans l'image de proxy.exe (relue inchangée à la fin du run) ; les
  octets sont CONSIGNÉS AU TÉMOIN — ce qui est exécuté est LISIBLE. Le
  réseau n'est touché QUE par les blocs de l'artefact (sys-05 via le
  trampoline appelle LE MÊME bloc — le geste mesuré est LE GESTE du run
  m9f, pas une réécriture).
- **Les variations (d)/(e) sont des gestes EXPÉRIMENTAUX nommés** : la
  session sacrifiée de la variation TAILLE n'est JAMAIS réutilisée (un
  octet parti polluerait le flux d'une poignée éventuelle) ; la
  contre-épreuve S4 court TOUJOURS sur une session NEUVE ET VIERGE.
- **Sous Python, la sonde utilise ctypes** pour charger l'artefact et
  appeler les blocs à leurs adresses scellées — le MÊME moyen standard que
  le kit m9f ; le CODE appelé est celui de L'ARTEFACT (vérifié par
  empreinte avant tout appel).

## 6. Après le run

- **Quel que soit le verdict** (VERT-MESURE, PERCÉE, ou ROUGE nommé) :
  renvoyer `preuves-sonde-sys05/` TEL QUEL au coffre
  `/test/preuves-sonde-sys05/` — le laboratoire recoupe sur pièces
  (D138/D145/D148), NOMME le coupable (le contrat du bloc, l'état de
  l'endpoint, ou le réseau) et répare selon la charte : l'erratum de la
  notation le cas échéant, la révision 2 de la spec sys-05 — puis LE RUN
  M9F réparé suivra, et avec lui la finale 1.0.0 : le jalon M9 — LA
  GRANDE ŒUVRE.

*Le laboratoire ne peut PAS rejouer ce kit (Windows + le VRAI ntdll + le
VRAI afd.sys exigés). Le labo a fait ce qu'il peut : le squelette du
trampoline vérifié octet par octet à l'assemblage, le dépaquetage éprouvé
sur les quatre cas (le signe 32 bits, PENDING, le compte partiel, le
succès), l'alignement de pile msx64 démontré, la table NTSTATUS recoupée
aux DEUX sources canoniques, chaque constante du scénario recoupée contre
l'artefact — et la contre-épreuve S4 embarquée : si le refus disparaît,
la poignée suit DANS LE MÊME RUN.*
