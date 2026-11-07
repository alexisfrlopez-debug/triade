#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree187.py — LA CONSIGNATION DU GESTE « LA PREMIÈRE
SIGNATURE DE LA RÉVISION 2 REÇUE (« la signature est dans le drive
/test »), RECROPÉE 13/13 ET INSTALLÉE — LE GARDE 13/13 VERTS ; PUIS
L'ERRATUM n° 9 NOMMÉ AVANT LE KIT : SYS-06 PORTE LE MÊME WSABUF
« PACKÉ » (le C_ASSERT send/recv, le même patron à l'instruction
près) — LA RÉVISION 2 S'ÉTEND À LA RÉCEPTION, LE HARNAIS RÉVISÉ
(131 · 131 VERTS × 3 graines), LA REMISE RÉGÉNÉRÉE (m8 c444d730…) » :
la rangée (f) du plan reçoit le constat, l'État du programme reçoit la
phrase du geste, le worklog reçoit l'Entrée 187 + la Task ID 105.
Rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

# --- la rangée (f) : le constat du geste, avant la colonne du critère -------------

ANCIEN_RANGEE = ("LE GESTE ATTENDU : la signature hors-ligne de la remise → "
                 "signatures-I.txt + cle-publique-I.txt au /test — puis "
                 "deposer, le garde 13/13, LE REBUILD 1.0.0-dev.3, LE KIT "
                 "M9F RÉPARÉ, le run — ET SI LE VERT TIENT : LA FINALE "
                 "1.0.0, LE JALON M9]** | run terrain VERT sur pièces")

NOUVELLE_RANGEE = (
    "LE GESTE ATTENDU : la signature hors-ligne de la remise → "
    "signatures-I.txt + cle-publique-I.txt au /test — puis deposer, le "
    "garde 13/13, LE REBUILD 1.0.0-dev.3, LE KIT M9F RÉPARÉ, le run — ET "
    "SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9]** ; **LA PREMIÈRE "
    "SIGNATURE DE LA RÉVISION 2 REÇUE ET INSTALLÉE le 07/11/2026 au soir "
    "(Entrée 187, Task 105) : le terrain vérifié AVANT le geste [le /test "
    "porte les DEUX pièces — signatures-I.txt md5 af382476… NOUVEAU ≠ "
    "l'ancienne 62c43222…, cle-publique-I.txt == 188a7d42… LA clé du kit ; "
    "les DEUX kits INTACTS, les réceptacles ré-armés], la remise "
    "RAPATRIÉE AVEC contrôle md5 [rapatrier_ceremonie_rev2.py, lecture "
    "seule sur v06/] PUIS RECROPÉE SUR PIÈCES 13/13 [l'ancre de clé == "
    "173fae9c… l'ancre des ères ; le format : 13 lignes ; les DOUZE "
    "arbres inchangés == les signatures du build 1.0.0 BYTE-IDENTIQUES "
    "(la preuve de D163 REJOINTE UNE TROISIÈME FOIS — Ed25519 "
    "déterministe, la clé du 04/11 réutilisée) ; m8 RE-SIGNÉ : la "
    "signature NOUVELLE vérifie Ed25519 contre l'empreinte vivante "
    "3e778fa0… de la révision 2 ; les empreintes vivantes == a-signer.txt "
    "13/13], DEPOSER JOUÉ [l'atomicité de cérémonie : TOUT vérifié avant "
    "TOUTE écriture — 13 signatures installées, manifestes vivants, la "
    "clé réelle] ET LE GARDE REPASSÉ : **13/13 arbres VERTS** — la dette "
    "de cérémonie de la révision 2 (sys-05 seul) EST SOLDÉE ; PUIS À LA "
    "PRÉPARATION DES PORTES DE L'ASSEMBLAGE : **L'ERRATUM n° 9 NOMMÉ "
    "AVANT LE KIT — SYS-06 PORTE LE MÊME WSABUF « PACKÉ »** [la porte V1 "
    "du harnais attend encore la pose 0x64 là où la notation réparée de "
    "sys-05 pose 0x68 : L'INSTRUMENT DOIT SUIVRE LA RÉVISION 2 — et le "
    "noyau AFD simulé lisant buf à +8 condamne MÉCANIQUEMENT la notation "
    "sys-06 non réparée (la même pose 0x64, la spec R1 « 12 o + 24 o ») ; "
    "la symétrie est CONSIGNÉE : le C_ASSERT send/recv (AFD_SENDRECV_"
    "TAILLE 0x18), le MÊME patron d'instruction — à la réception le "
    "noyau ÉCRIRAIT la réponse chez l'adresse folle : la mort à T3 du "
    "run, un cran après la réparation de l'émission ; la faute est nommée "
    "PAR LA MESURE DE LA MÊME STRUCTURE (la sonde, Entrée 185 : le noyau "
    "lit buf à +8), jamais une devinette] ; LA RÉPARATION SELON LA CHARTE "
    "[la RÉVISION 2 DE LA SPEC SYS-06 : Q3 réécrit — le WSABUF canonique "
    "16 o, le padding NOMMÉ, buf à +8, la structure totale 40 o, non 36 ; "
    "la note de révision consigne la symétrie ; l'erratum de lecture "
    "AfdFlags/TdiFlags demeure intact] + la notation et le brouillon "
    "corrigés [mov qword ptr [rsp+0x68], rdi — le MÊME encode 5 o, le "
    "slot ne bouge pas d'un octet, la carte demeure] + LE HARNAIS RÉVISÉ "
    "[_wsabuf lit buf à +8 — le noyau simulé suit le noyau réel mesuré ; "
    "les attendus V1 de sys-05 ET sys-06 à 0x68 ; la mutante V4b "
    "wsabuf-buf-pour-capacite ré-encodée à 0x68] ET LA PREUVE RE-PASSÉE : "
    "**131 contrôles · 131 VERTS × 3 graines** (20261105, 424242, 777777 "
    "— empreintes distinctes par graine, zéro échec, les CINQ mutantes de "
    "sys-06 trahies, les témoins intacts) ; LA REMISE RÉGÉNÉRÉE "
    "[preparer : m8 sys.1 c444d730… — sys-06-reception.md SEUL diverge du "
    "manifeste signé (942907fd… → caa17ed6…), les DOUZE autres arbres "
    "inchangés ; la balise demeure sys.1] ; LA MAIN DU DÉVELOPPEUR "
    "RE-SERViE [LISEZMOI-ceremonie-revision2-sys05.txt RÉÉCRIT : la "
    "révision 2 ÉTENDUE, l'empreinte à attendre c444d730…, la remise "
    "3e778fa0… PÉRIMÉE par l'erratum n° 9 ; le NOTE_D130 réécrit] — LA "
    "SECOND SIGNATURE ATTENDUE : la remise étendue au /test → deposer → "
    "le garde 13/13 → LE REBUILD 1.0.0-dev.3 [les blocs sys-05 ET sys-06 "
    "réparés, les portes de l'assemblage re-passées sur l'instrument "
    "révisé] → LE KIT M9F RÉPARÉ au /test → le run — ET SI LE VERT "
    "TIENT : LA FINALE 1.0.0, LE JALON M9]** | run terrain VERT sur "
    "pièces")

# --- l'État du programme : la phrase du geste remplace l'attente ------------------

ANCIEN_ETAT = ("— LE GESTE DU DÉVELOPPEUR ATTENDU : la signature hors-ligne "
               "de la remise → signatures-I.txt + cle-publique-I.txt au "
               "/test ; puis le dépôt : deposer → le garde 13/13 → LE "
               "REBUILD 1.0.0-dev.3 [le bloc sys-05 réparé, les portes de "
               "l'assemblage re-passées] → LE KIT M9F RÉPARÉ au /test → le "
               "run du développeur — ET SI LE VERT TIENT : LA FINALE 1.0.0, "
               "LE JALON M9 — LA GRANDE ŒUVRE**")

NOUVEL_ETAT = (
    "— **LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE, RECROPÉE 13/13 ET "
    "INSTALLÉE le 07/11/2026 au soir (Entrée 187, Task 105) : le garde "
    "13/13 VERTS [la remise recoupée sur pièces : l'ancre de clé "
    "173fae9c… tenue, les DOUZE arbres inchangés == les signatures du "
    "build 1.0.0 — la preuve de D163 rejointe une TROISIÈME fois, m8 "
    "re-signé contre 3e778fa0…] ; PUIS L'ERRATUM n° 9 NOMMÉ AVANT LE "
    "KIT : sys-06 porte le MÊME WSABUF « packé » que la sonde a condamné "
    "à l'émission [le C_ASSERT send/recv, le même patron d'instruction, "
    "le harnais lui-même modélisait le « packé » — l'instrument suit la "
    "révision 2 : le noyau simulé lit buf à +8] ; LA RÉPARATION SELON LA "
    "CHARTE : la spec sys-06 en R2 + la notation corrigée [0x64 → 0x68, "
    "le même encode, le slot intact] + le harnais révisé — LA PREUVE "
    "RE-PASSÉE : 131 contrôles · 131 VERTS × 3 graines ; LA REMISE "
    "RÉGÉNÉRÉE [m8 c444d730… — sys-06-reception.md seul diverge], LA "
    "MAIN DU DÉVELOPPEUR RE-SERVIE [le LISEZMOI de cérémonie réécrit : "
    "la révision 2 ÉTENDUE, l'empreinte à attendre c444d730…] — LA "
    "SECONDE SIGNATURE ATTENDUE : la remise étendue (signatures-I.txt + "
    "cle-publique-I.txt au /test) ; puis le dépôt : deposer → le garde "
    "13/13 → LE REBUILD 1.0.0-dev.3 [les blocs sys-05 ET sys-06 réparés, "
    "les portes de l'assemblage re-passées sur l'instrument révisé] → LE "
    "KIT M9F RÉPARÉ au /test → le run du développeur — ET SI LE VERT "
    "TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

# --- le journal : l'Entrée 187, AVANT le marqueur m5a -----------------------------

ENTREE_187 = """## Entrée 187 — LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE, RECROPÉE 13/13 ET INSTALLÉE — LE GARDE 13/13 VERTS ; PUIS L'ERRATUM n° 9 NOMMÉ AVANT LE KIT : SYS-06 PORTE LE MÊME WSABUF « PACKÉ » — LA RÉVISION 2 S'ÉTEND À LA RÉCEPTION, LE HARNAIS RÉVISÉ (131 · 131 VERTS × 3 graines), LA REMISE RÉGÉNÉRÉE (m8 c444d730…) (07/11 au soir)

**Le terrain a été vérifié avant de recevoir.** lister_drive.py (lecture seule) : le /test porte les DEUX pièces du geste — signatures-I.txt md5 **af382476…** (NOUVELLE, ≠ l'ancienne 62c43222… de la cérémonie du build : la remise déposée est bien la remise RÉGÉNÉRÉE de l'Entrée 186) et cle-publique-I.txt == **188a7d42…** (LA clé publique du kit, inchangée). Les DEUX kits INTACTS (kit-m9f.zip == l'ACQUITTÉ 90a1d022…, kit-sonde-sys05.zip == le livré 215c2caa…), les réceptacles ré-armés, le run de la sonde archivé, la racine 16 entrées.

**La remise recoupée sur pièces AVANT tout dépôt.** rapatrier_ceremonie_rev2.py (D166 règle 8 rejouée, LECTURE SEULE sur v06/) : rapatriement des DEUX pièces vers download/ceremonie-revision2/ avec contrôle md5 APRÈS écriture (MATCH les métadonnées Drive) ; l'ANCRE DE CLÉ : la clé déposée == **173fae9c…** l'ancre des ères (« si cle-publique-I.txt diverge : ARRÊT », la règle d'or tenue : JAMAIS « generer ») == l'ancre locale du dépôt ; le format : 13/13 lignes valides (arbre balise signature-128hex, balises == la table canonique) ; **LE RECOUP D163 REJOINT UNE TROISIÈME FOIS** : les DOUZE arbres inchangés (m0..m7, tls13, demo, terrain, v06) portent les signatures BYTE-IDENTIQUES à celles déposées au build 1.0.0 (Ed25519 déterministe : la clé du 04/11 réutilisée redonne exactement les signatures déposées) ; **m8 RE-SIGNÉ** : la signature nouvelle DIVERGE de la déposée (l'empreinte a bougé : 72aadd38… → 3e778fa0…) et VÉRIFIE Ed25519 contre l'empreinte vivante 3e778fa0e7ff4a7e… de la révision 2 ; les empreintes vivantes des TREIZE arbres == a-signer.txt (la remise fraîche de l'Entrée 186) 13/13. **RECOUPE INTÉGRAL VERT — 13/13.**

**Le dépôt canonique et la garde.** sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt JOUÉ (l'atomicité de cérémonie : la remise entière vérifiée AVANT toute écriture — 13 signatures installées, les manifestes vivants, la clé réelle : etat « reelle (ceremonie hors-ligne, D87) »). Puis **verifier : 13/13 arbres VERTS** — m8 vert (3e778fa0…), les DOUZE autres verts : la dette de cérémonie de la révision 2 (sys-05 seul) EST SOLDÉE. Le rebuild 1.0.0-dev.3 est DÉBLOQUÉ pour l'état signé.

**Mais les portes de l'assemblage ont nommé la suite.** À la préparation du rebuild, la PORTE V1 DU HARNAIS est restée sur l'ancien monde : elle attend la concordance `mov qword ptr [rsp + 0x64], rdi` (la pose « packée ») là où la notation réparée de sys-05 (Entrée 185) pose désormais `mov qword ptr [rsp + 0x68], rdi` (le canonique) — l'INSTRIMENT DOIT SUIVRE LA RÉVISION 2. Et l'instrument une fois révisé (le noyau AFD simulé lisant buf à +8, comme le noyau réel MESURÉ PAR LA SONDE), la notation de **sys-06 EST CONDAMNÉE MÉCANIQUEMENT** : elle pose le MÊME WSABUF « packé » (la même instruction à l'offset près, relu dans la notation : `mov qword ptr [rsp + 0x64], rdi`), sa spec R1 décrète le même « 12 o + 24 o ». **L'ERRATUM n° 9 : sys-06 porte le même défaut que la sonde a nommé à l'émission — la symétrie est CONSIGNÉE PARTOUT** : le C_ASSERT send/recv (AFD_SENDRECV_TAILLE 0x18 — « la taille de l'un EST celle de l'autre », la spec sys-06 le dit elle-même), le MÊME contrat d'appel AFD, le MÊME WSABUF, le même +8. À la réception, le noyau ÉCRIRAIT la réponse du serveur chez l'adresse folle : STATUS_ACCESS_VIOLATION à T3 du run — la mort un cran après la réparation de l'émission. La réception n'a JAMAIS couru sur le terrain réel (les cinq runs mouraient à l'émission) : la faute est nommée PAR LA MESURE DE LA MÊME STRUCTURE (la sonde, Entrée 185 : le noyau lit buf à +8), pas une devinette — et NOMMÉE AVANT LE KIT (la charte : jamais livrer un défaut connu, jamais une dérive silencieuse).

**La réparation selon la charte.** LA RÉVISION 2 DE LA SPEC SYS-06 (m8/I/sys-06-reception.md) : Q3 réécrit — le WSABUF et l'AFD_RECV_INFO sur la pile « (16 o + 24 o…) : le WSABUF CANONIQUE x64 — len à +0 (4 o), le PADDING d'alignement 4 o, buf à +8 (8 o) : JAMAIS un « packé » de 12 o, le noyau lit buf à +8 » ; la note de révision en tête consigne la symétrie (la mesure de la sonde, le C_ASSERT, le même patron d'instruction, la structure totale 40 o non 36 — l'erratum de lecture AfdFlags/TdiFlags de la R1 demeure, lui, intact). LA NOTATION corrigée (m8/notation/sys-06-reception.asm + le brouillon) : `mov qword ptr [rsp + 0x68], rdi` — le MÊME encode (48 89 7c 24 68, 5 o), le slot ne bouge pas d'un octet, la carte demeure. LE HARNAIS RÉVISÉ (m8/harnais_sys.py) : _wsabuf lit buf à +8 (le noyau simulé suit le noyau réel), les attendus V1 de sys-05 ET sys-06 portent la pose canonique 0x68, la mutante V4b « wsabuf-buf-pour-capacite » ré-encodée à 0x68. **LA PREUVE RE-PASSÉE : 131 contrôles · 131 VERTS × 3 graines** (20261105, 424242, 777777 — empreintes distinctes par graine, ZÉRO échec : les batteries des SIX blobs verts, les mutantes TOUTES trahies dont les CINQ de sys-06, les témoins intacts).

**La remise régénérée, la main du développeur re-servie.** sceau_I.py preparer JOUÉ : a-signer.txt porte m8 sys.1 **c444d73059af33ce0d61bf48ce8ac976d1e86a566574dcb4ef63a771f7b1875a** — sys-06-reception.md SEUL diverge du manifeste signé (sha256 942907fd… → caa17ed6…, diff contrôlé : un fichier, un seul) ; les DOUZE autres arbres INCHANGÉS (leurs empreintes == les signatures déjà déposées — la seconde signature ne sera qu'une re-signature de m8, les douze autres rendront encore les mêmes). La balise demeure sys.1. Le garde relit : m8 CODE 10 — fichier modifié : sys-06-reception.md. LE SIGNAL, pas la panne. LISEZMOI-ceremonie-revision2-sys05.txt RÉÉCRIT : OÙ NOUS EN SOMMES (la première signature reçue, recoupée 13/13, installée — puis l'erratum n° 9) ; POURQUOI la révision s'étend ; CE QUI A CHANGÉ (m8 c444d730… — DEUX fichiers de l'arbre m8 désormais, les CINQ autres inchangés ; l'empreinte 3e778fa0… du geste précédent PÉRIMÉE par l'erratum n° 9, 72aadd38… celle du build) ; LA RÈGLE D'OR INCHANGÉE (JAMAIS « generer », la clé du 04/11 — 173fae9c…) ; LES CINQ PAS (le pas 3 exige c444d730… sur la ligne m8) ; CE QUE CELA DÉBLOQUE. Le NOTE_D130 (le manifeste du kit) RÉÉCRIT en conséquence — déployés au commit même (hook post-commit : le miroir PUIS le kit, D130).

**Frontières.** L'artefact INTACT (tls13/proxy.exe d8928934… — le build 1.0.0-dev.2 : le rebuild dev.3 attend la seconde signature, jamais une reconstruction tacite), le scellé 0.9.0 INTACT, les signatures DÉPOSÉES de la première cérémonie de la révision 2 DEMEURENT le dossier honnête de l'état signé (elles couvrent sys-05 R2 + sys-06 R1 : valides pour cet état — la nouvelle remise remplacera la ligne m8 à la seconde cérémonie), AUCUNE balise posée (D104), la clé privée jamais traversée (D87) — le labo ne signera JAMAIS à la place du développeur. Consignations : la présente Entrée 187 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 105. SUITE : LA SECONDE SIGNATURE DU DÉVELOPPEUR — la remise étendue (signatures-I.txt + cle-publique-I.txt au /test) ; puis le dépôt : deposer, le garde 13/13, LE REBUILD 1.0.0-dev.3 (les blocs sys-05 ET sys-06 réparés, les portes de l'assemblage re-passées sur l'instrument révisé), LE KIT M9F RÉPARÉ livré au /test, le run du développeur — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.

"""

# --- le worklog racine : la Task ID 105, À LA SUITE (append) ----------------------

TASK_105 = """
## Task ID 105 — LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE GARDE 13/13 VERTS) ; PUIS L'ERRATUM n° 9 NOMMÉ AVANT LE KIT : SYS-06 LE MÊME WSABUF « PACKÉ » — LA RÉVISION 2 ÉTENDUE (SPEC R2 + NOTATION + HARNAIS RÉVISÉ, 131 · 131 VERTS × 3 graines), LA REMISE RÉGÉNÉRÉE m8 c444d730… — LA SECONDE SIGNATURE ATTENDUE (07/11 au soir)

Work Log:
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR (lister_drive.py, lecture seule) :
  le /test porte les DEUX pièces — signatures-I.txt md5 af382476…
  (NOUVELLE ≠ l'ancienne 62c43222… : la remise déposée est bien la
  remise régénérée de l'Entrée 186) et cle-publique-I.txt == 188a7d42…
  (LA clé du kit) ; les DEUX kits INTACTS (90a1d022… + 215c2caa…), les
  réceptacles ré-armés, la racine 16 entrées.
- LA REMISE RECROPÉE SUR PIÈCES AVANT TOUT DÉPÔT
  (rapatrier_ceremonie_rev2.py — D166 règle 8 rejouée, lecture seule
  sur v06/) : rapatriement avec contrôle md5 MATCH ; l'ancre de clé ==
  173fae9c… l'ancre des ères (la règle d'or tenue) ; le format 13/13 ;
  LE RECOUP D163 REJOINT UNE TROISIÈME FOIS : les DOUZE arbres
  inchangés == les signatures du build 1.0.0 BYTE-IDENTIQUES (Ed25519
  déterministe, la clé du 04/11 réutilisée) ; m8 RE-SIGNÉ : la
  signature nouvelle vérifie Ed25519 contre l'empreinte vivante
  3e778fa0e7ff4a7e… ; les empreintes vivantes == a-signer.txt 13/13 —
  RECOUPE INTÉGRAL VERT.
- LE DÉPÔT CANONIQUE (sceau_I.py deposer --cle : l'atomicité — tout
  vérifié avant toute écriture, 13 signatures installées, les manifestes
  vivants, la clé réelle) ET LA GARDE REPASSÉE : **13/13 arbres
  VERTS** — la dette de cérémonie de la révision 2 (sys-05 seul)
  SOLDÉE pour l'état signé.
- L'ERRATUM n° 9 NOMMÉ AVANT LE KIT, à la préparation des portes de
  l'assemblage : la porte V1 du harnais attendait encore la pose
  « packée » (0x64) que la notation réparée de sys-05 ne pose plus
  (0x68) — L'INSTRUMENT DOIT SUIVRE LA RÉVISION 2 ; et le noyau AFD
  simulé lisant buf à +8 (comme le noyau réel MESURÉ PAR LA SONDE)
  condamne MÉCANIQUEMENT la notation sys-06 : la MÊME pose 0x64, la
  spec R1 « 12 o + 24 o », la symétrie CONSIGNÉE (le C_ASSERT
  send/recv — AFD_SENDRECV_TAILLE 0x18, la spec sys-06 le dit
  elle-même) : à la réception le noyau ÉCRIRAIT chez l'adresse folle —
  la mort à T3 du run, un cran après la réparation de l'émission ; la
  faute nommée PAR LA MESURE DE LA MÊME STRUCTURE, jamais une
  devinette, AVANT le kit (la charte).
- LA RÉPARATION SELON LA CHARTE : LA RÉVISION 2 DE LA SPEC SYS-06
  (Q3 réécrit — le WSABUF canonique 16 o, le padding NOMMÉ, buf à
  +8, la structure totale 40 o non 36, la note de révision consignant
  la symétrie ; l'erratum de lecture AfdFlags/TdiFlags intact) + la
  notation et le brouillon corrigés (0x64 → 0x68, le MÊME encode 5 o,
  le slot intact, la carte demeure) + LE HARNAIS RÉVISÉ (_wsabuf lit
  buf à +8, les attendus V1 de sys-05 ET sys-06 à 0x68, la mutante
  V4b ré-encodée).
- LA PREUVE RE-PASSÉE : **131 contrôles · 131 VERTS × 3 graines**
  (20261105, 424242, 777777 — zéro échec, les mutantes toutes
  trahies, les témoins intacts).
- LA REMISE RÉGÉNÉRÉE (preparer) : m8 sys.1 c444d73059af33ce…
  (sys-06-reception.md SEUL diverge du manifeste signé :
  942907fd… → caa17ed6…, diff contrôlé) ; les DOUZE autres arbres
  inchangés ; la balise demeure sys.1 ; le garde relit m8 CODE 10 —
  LE SIGNAL, pas la panne.
- LA MAIN DU DÉVELOPPEUR RE-SERVIE : LISEZMOI-ceremonie-revision2-
  sys05.txt RÉÉCRIT (OÙ NOUS EN SOMMES ; POURQUOI la révision
  s'étend ; CE QUI A CHANGÉ : m8 c444d730…, DEUX fichiers de l'arbre
  m8, l'empreinte 3e778fa0… PÉRIMÉE ; LA RÈGLE D'OR inchangée ;
  LES CINQ PAS — le pas 3 exige c444d730…) ; le NOTE_D130 réécrit —
  déployés au commit même (hook post-commit : le miroir PUIS le kit).
- FRONTIÈRES : l'artefact INTACT (d8928934…), le scellé 0.9.0
  INTACT, les signatures déposées de la première cérémonie demeurent
  le dossier honnête de l'état signé (sys-05 R2 + sys-06 R1), aucune
  balise (D104), la clé privée jamais traversée (D87). SUITE : LA
  SECONDE SIGNATURE DU DÉVELOPPEUR (la remise étendue →
  signatures-I.txt + cle-publique-I.txt au /test) — puis deposer, le
  garde 13/13, LE REBUILD 1.0.0-dev.3 [sys-05 ET sys-06 réparés], LE
  KIT M9F RÉPARÉ au /test, le run — ET SI LE VERT TIENT : LA FINALE
  1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.
"""


def main():
    # 1. le plan : la rangée (f) + l'État
    plan = PLAN.read_text(encoding="utf-8")
    if "LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE ET INSTALLÉE le 07/11" in plan:
        sys.exit("ÉCHEC : la rangée (f) est déjà à jour (rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                 f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
    if "L'ERRATUM n° 9 NOMMÉ AVANT LE KIT" not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                 "après remplacement")
    if "LA SECONDE SIGNATURE ATTENDUE" not in plan:
        sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
    PLAN.write_text(plan, encoding="utf-8")
    print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 187 avant le marqueur m5a
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 187 —" in journal:
        sys.exit("ÉCHEC : l'Entrée 187 existe déjà (rejeu REFUSÉ)")
    marqueur = "<!-- m5a:journal-des-builds v1"
    if journal.count(marqueur) != 1:
        sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                 f"{journal.count(marqueur)} fois (attendu : 1)")
    journal = journal.replace(marqueur, ENTREE_187 + marqueur, 1)
    if "## Entrée 187 — LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE" not in journal:
        sys.exit("ÉCHEC : l'Entrée 187 absente après remplacement")
    JOURNAL.write_text(journal, encoding="utf-8")
    print("JOURNAL : l'Entrée 187 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 105 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 105 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 105 existe déjà (rejeu REFUSÉ)")
    ancre_fin = "— ET SI LE VERT TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE\n  ŒUVRE."
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la passation "
                 "Task 104 attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_105
    if "## Task ID 105 — LA PREMIÈRE SIGNATURE DE LA RÉVISION 2 REÇUE" not in worklog:
        sys.exit("ÉCHEC : la Task ID 105 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 105 consignée À LA SUITE de la Task 104")


if __name__ == "__main__":
    main()
