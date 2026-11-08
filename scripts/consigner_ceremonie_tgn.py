#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_ceremonie_tgn.py — LA CONSIGNATION DE LA CÉRÉMONIE D'ÈRE DU TGN
(« go pour la cérémonie ») : le registre figé de m0 ÉTENDU au domaine
`loupe`, l'arbre `loupe` ENTRÉ à la table canonique (le quatorzième), LA
REMISE FRAÎCHE des QUATORZE arbres RÉGÉNÉRÉE AU GESTE (D168 rejouée) et
SERVIE au /Cérémonie du Drive avec le LISEZMOI pas à pas — la dette
D166/D171 ÉCHUE AU BUILD, le geste hors-ligne du développeur attendu.

Le journal reçoit l'Entrée 200, DECISIONS reçoit la D177, le PLAN reçoit
l'État de la cérémonie (la phrase du M10-(d) remplacée) + la rangée (d) +
la phrase de la dette au programme TGN, le worklog reçoit la Task ID 118.

GARDES AVANT ÉCRITURE (l'état de dette nommé, le miroir de l'ère M9) :
  - sceau I : m0 CODE 10 (fichier modifié : README.md — le registre
    étendu), loupe CODE 12 (manifeste déposé absent — l'arbre neuf), les
    DOUZE autres VERTS ;
  - la remise v06/sceau-I/a-signer.txt : QUATORZE lignes, m0 à
    667fb5ae… et loupe à 59e4871a… (les empreintes du geste) ;
  - le LISEZMOI download/LISEZMOI-ceremonie-ere-TGN.txt présent.
Tout écart = ÉCHEC NOMMÉ, rien n'est écrit. Rejeu REFUSÉ."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"
ASIGNER = REPO / "v06" / "sceau-I" / "a-signer.txt"
LISEZMOI = pathlib.Path("/home/z/my-project/download/LISEZMOI-ceremonie-ere-TGN.txt")
MARQUEUR = "<!-- m5a:journal-des-builds v1"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_m10d as _c198  # noqa: E402  # la chaîne des gestes

sys.path.insert(0, str(REPO / "v06"))
import sceau_I  # noqa: E402

# --- l'empreinte de l'état du geste (les valeurs constatées au geste) ---------------

EMP_M0 = "667fb5ae36e4ab3c5dcfd4899fc680fd5b2393d2cdc6ad32241be14b89d9f920"
EMP_LOUPE = "59e4871ab5b47623be8aad0d6633abf7a1f8b64acd6f87f4f87e2003aa5d8520"

# --- l'État du programme : la phrase de la cérémonie remplace celle du (d) ----------

ANCIEN_ETAT = _c198.NOUVEL_ETAT   # l'État 198 (M10-(d) première moitié, la suite)

NOUVEL_ETAT = (
    "**LA CÉRÉMONIE D'ÈRE DU TGN ARMÉE le 08/11/2026 au soir (Entrée 200, D177, "
    "Task 118) : LA DETTE D166/D171 ÉCHUE AU BUILD, LE KIT SERVI AU /CÉRÉMONIE** "
    "— LE REGISTRE FIGÉ DE m0 ÉTENDU au domaine `loupe` (M10 : l'extension "
    "promise à la cérémonie par loupe/I/README.md — m0 DIVERGÉ nommément CODE "
    "10, fichier modifié : README.md, les trois spécifications hello-01..03 "
    "inchangées octet pour octet) et L'ARBRE `loupe` ENTRÉ À LA TABLE "
    "CANONIQUE du sceau I (LE QUATORZIÈME, loupe.1, à sa place d'ère après "
    "tls13.1 — CODE 12, manifeste déposé absent : l'arbre neuf des 19 fichiers "
    "[le README + les 18 spécifications] attend sa première signature) ; LA "
    "REMISE RÉGÉNÉRÉE AU GESTE (D168 rejouée : sceau_I.py preparer — QUATORZE "
    "arbres, DEUX empreintes nouvelles [m0 667fb5ae… le registre étendu ; "
    "loupe 59e4871a… l'arbre complet], les DOUZE autres inchangées — "
    "re-signées à l'identique par le déterminisme Ed25519, la preuve D163) ; "
    "LE LISEZMOI-ceremonie-ere-TGN.txt ÉCRIT ET DÉPOSÉ au /Cérémonie du Drive "
    "(le pas à pas du geste hors-ligne, la règle d'or « JAMAIS generer » — la "
    "clé du 04/11 173fae9c… réutilisée) ; le garde CONSTATE la dette nommée "
    "(m0 CODE 10 + loupe CODE 12, les DOUZE autres VERTS — LE SIGNAL, pas la "
    "panne ; le miroir exact de l'ère M9, Entrée 165). SUITE : LE GESTE "
    "HORS-LIGNE DU DÉVELOPPEUR (signer la remise des QUATORZE arbres à la clé "
    "du 04/11, ramener signatures-I.txt + cle-publique-I.txt au coffre /test) "
    "; le labo rapatrie, recoupe, installe canoniquement — LE GARDE PASSE À "
    "QUATORZE arbres VERTS PUIS le build loupe 0.1.0-dev.1 + le kit terrain "
    "(M10-(d) seconde moitié) et le run (M10-(e))**"
)

# --- le plan : la rangée (d) — la cérémonie armée -----------------------------------

RANGEE_D_ANCIENNE = (
    "l'oracle 45 VERTS × 3 graines (le disque saisissable, la mort complète, "
    "LE RÉSEAU de la garde, la falsification) ; LE KIT ATTEND LA CÉRÉMONIE "
    "D'ÈRE (le 14e arbre, AVANT tout build)"
)
RANGEE_D_NOUVELLE = (
    "l'oracle 45 VERTS × 3 graines (le disque saisissable, la mort complète, "
    "LE RÉSEAU de la garde, la falsification) ; LA CÉRÉMONIE D'ÈRE ARMÉE "
    "(Entrée 200, D177) : le registre de m0 ÉTENDU, l'arbre `loupe` NEUF à la "
    "table canonique, LA REMISE FRAÎCHE des QUATORZE arbres (m0 667fb5ae… + "
    "loupe 59e4871a…) servie au /Cérémonie du Drive avec le LISEZMOI pas à "
    "pas — LE GESTE HORS-LIGNE DU DÉVELOPPEUR ATTENDU (signer à la clé du "
    "04/11, déposer signatures-I.txt + cle-publique-I.txt au /test)"
)

# --- le plan : la phrase de la dette au programme TGN -------------------------------

DETTE_ANCIENNE = (
    "la dette de cérémonie est nommée à la naissance (le 14e arbre + "
    "l'extension du registre figé m0/I § 2.1 attendent la cérémonie d'ère — "
    "le modèle D166/D168 : le garde demeure à 13 arbres VERTS jusqu'alors, "
    "aucun arbre signé n'est touché)."
)
DETTE_NOUVELLE = (
    "la dette de cérémonie est nommée à la naissance (le modèle D166/D168) — "
    "LA CÉRÉMONIE D'ÈRE ARMÉE le 08/11 au soir (Entrée 200, D177) : le "
    "registre figé m0/I § 2.1 ÉTENDU au domaine `loupe`, l'arbre `loupe` "
    "entré à la table canonique (le 14e), la remise fraîche des QUATORZE "
    "arbres servie au /Cérémonie du Drive avec le LISEZMOI pas à pas — le "
    "garde CONSTATE la dette nommée (m0 CODE 10, loupe CODE 12, les douze "
    "autres VERTS), le geste hors-ligne du développeur est attendu ; le "
    "garde passera à QUATORZE arbres VERTS à l'installation — AUCUN build "
    "avant, aucun arbre signé touché hors le registre annoncé."
)

# --- le journal : l'Entrée 200 -------------------------------------------------------

ENTREE = """## Entrée 200 — « go pour la cérémonie » : LA CÉRÉMONIE D'ÈRE DU TGN ARMÉE — le registre figé de m0 étendu au domaine `loupe` (l'extension promise, D171/D168), l'arbre `loupe` entré à la table canonique (LE QUATORZIÈME), la remise fraîche des QUATORZE arbres régénérée au geste et servie au /Cérémonie du Drive avec le LISEZMOI pas à pas — la dette D166/D171 échue au build, le geste hors-ligne du développeur attendu (08/11 au soir)

**La demande et son moment.** Le message du développeur « go pour la cérémonie » arme le geste que la ligne SUITE de l'Entrée 199 annonçait : la cérémonie d'ère du TGN au geste qui suit la spécification v0.8.0, les quatre chantiers de notation accomplis (Entrées 195–198 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS, la couche I FINALE). La dette D166/D171 est ÉCHUE AU BUILD — le garde suit le calendrier de la cérémonie, jamais l'inverse (§ 13.5). L'état constaté AVANT toute écriture : le garde sceau I à TREIZE arbres VERTS, clé « reelle » 173fae9c… (D87) ; les canaux OAuth Drive + GitHub 200 (check_auth.py) ; l'outil hors-ligne ceremonie_hors_ligne.py AGNOSTIQUE de la table des arbres (il valide le format des lignes de la remise — le quatorzième arbre ne réclame AUCUNE pièce nouvelle du kit).

**Le geste source (les DEUX écrits qui font la dette visible).** (1) LE REGISTRE FIGÉ DE m0 ÉTENDU : la ligne du registre des domaines (m0/I/README.md, § 2.1) porte désormais `loupe` (M10) entre `tls13` (M9) et `notation` — l'extension que la couche I de Loupe attendait depuis D171 (loupe/I/README.md l'avait promise : « l'extension du registre VIT À LA CÉRÉMONIE D'ÈRE du TGN — m0 est un arbre SIGNÉ, le geste d'ouverture n'y touche pas ») ; les trois spécifications hello-01..03 demeurent inchangées, octet pour octet. (2) LA TABLE CANONIQUE ÉTENDUE : v06/sceau_I.py ARBRES reçoit le quatorzième arbre — `loupe` : loupe.exe (domaine loupe, l'éditeur hexadécimal au panneau d'empreintes), balise `loupe.1` — à sa place d'ère (après tls13.1, l'ordre M8 → M9 → M10, l'ordre canonique qui nomme le premier arbre fautif). La spec v06/I/README.md DEMEURE INCHANGÉE : sa table normative vit figée à l'ère 0.6.0 (les entrées m8 et tls13 n'y figurent pas non plus — le sceau ne se re-spécifie pas à chaque ère, la table vivante est celle de l'outil).

**La remise régénérée AU GESTE (D168 rejouée).** `sceau_I.py preparer` rejoué au geste de la cérémonie : QUATORZE arbres, DEUX empreintes nouvelles — m0 667fb5ae36e4ab3c… (LE REGISTRE ÉTENDU) et loupe 59e4871ab5b47623… (L'ARBRE NEUF : le manifeste compte 19 fichiers — le README [la charte + le tableau des 18 blocs + les conventions] et les 18 spécifications loupe-01..18 en cinq familles, jamais signé avant cette cérémonie) ; les DOUZE autres arbres aux empreintes inchangées (m1–m8, tls13, demo, terrain, v06 — re-signés à l'identique par le déterminisme Ed25519, la preuve D163 rejouée à chaque cérémonie). LE CONSTAT DE LA DETTE SUR PIÈCES (verifier rejoué AVANT consignation) : m0 CODE 10 (fichier modifié : README.md), loupe CODE 12 (manifeste déposé absent), les DOUZE autres VERTS — LE SIGNAL, pas la panne ; le miroir exact de l'ouverture de l'ère M9 (Entrée 165 : « le garde m0 CODE 10 + tls13 CODE 12 »).

**Le LISEZMOI et le kit.** LISEZMOI-ceremonie-ere-TGN.txt (le modèle des ères M8/M9 — Entrées 159/167 — et du build 1.0.0) : le POURQUOI (la dette échue au build, les DEUX états qui exigent la clé hors-ligne : le registre étendu, l'arbre neuf), les DEUX empreintes citées noir sur blanc, la règle d'or (« JAMAIS generer » — la clé du 04/11 173fae9c… réutilisée, l'état « reelle » ne se régresse pas), la cérémonie PAS À PAS (console + mode graphique, l'atomicité du dépôt, le retour au /test), ce que cela DÉBLOQUE (le garde QUATORZE arbres verts → le build loupe 0.1.0-dev.1 [geste de BUILD jamais scellage] → le kit terrain [M10-(d) seconde moitié] → le run [M10-(e)] → la balise `loupe 0.1.0` scellée sur run recoupé), et le contrat D87 (la clé privée ne traverse jamais le bac à sable). maj_kit.py ÉTENDU : RACINE_KIT reçoit l'entrée LISEZMOI-ceremonie-ere-TGN.txt (optionnelle comme ses aînées — le contrat D130 inchangé) et NOTE_D130 RÉORIENTÉE (la mention de la re-cérémonie de la révision 3 était PÉRIMÉE — soldée à l'Entrée 192 ; celle de la cérémonie d'ère du TGN l'a remplacée : le développeur qui ouvre le dossier est orienté vers LE LISEZMOI courant). Le kit DÉPOSÉ au geste du commit (le hook post-commit : drive_sync.py PUIS maj_kit.py — D130, le v06/ du kit suit le miroir par construction, la remise fraîche voyagée dans le geste même), le recoup indépendant par scripts/deposer_lisezmoi_ere_tgn.py (md5 par relecture, la remise du kit == celle du dépôt).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 INTACTES), AUCUN build (la dette demeure JUSQU'À la remise du développeur — c'est le travail du garde), AUCUN octet de notation (R2 — les 18 spécifications et les notations INTACTES, la cérémonie signe les écrits, elle ne les touche pas), le proxy 1.0.0 et la carte tls13 INTACTS ; l'outil de cérémonie hors-ligne INCHANGÉ (agnostique de la table). Livrables : m0/I/README.md (le registre étendu), v06/sceau_I.py (la table à quatorze), v06/sceau-I/a-signer.txt (la charge, 14 arbres), download/LISEZMOI-ceremonie-ere-TGN.txt (+ le dépôt au /Cérémonie), scripts/maj_kit.py (étendu), scripts/consigner_ceremonie_tgn.py, scripts/deposer_lisezmoi_ere_tgn.py ; consignations : la présente Entrée PAR SCRIPT, D177 PAR SCRIPT, le PLAN (l'État + la rangée (d) + la phrase de la dette au programme TGN), worklog +Task ID 118.

- SUITE : LE GESTE HORS-LIGNE DU DÉVELOPPEUR (signer la remise des QUATORZE arbres à la clé du 04/11 — la règle d'or « JAMAIS generer », ramener signatures-I.txt et cle-publique-I.txt au coffre /test) ; le labo rapatrie, recoupe (l'ancre de clé, les arbres inchangés rendant les MÊMES signatures par le déterminisme Ed25519, m0 re-signé au registre étendu, l'arbre `loupe` neuf), installe canoniquement — le garde passe à QUATORZE arbres VERTS : LE BUILD DE LOUPE PEUT NAÎTRE ; puis le build loupe 0.1.0-dev.1 + le kit terrain (M10-(d) seconde moitié, modèle m9f) et le run (M10-(e)) ; le projet fils attend son premier geste à son message propre.
"""

# --- les décisions : la D177 --------------------------------------------------------

D177 = """

## D177 — LA CÉRÉMONIE D'ÈRE DU TGN ARMÉE : le registre figé de m0 ÉTENDU au domaine `loupe` (M10) et l'arbre `loupe` ENTRÉ à la table canonique du sceau I (le quatorzième — `loupe.1`, l'arbre complet des 19 fichiers : le README + les 18 spécifications) ; la remise FRAÎCHE des QUATORZE arbres RÉGÉNÉRÉE AU GESTE (D168 rejouée : DEUX empreintes nouvelles [m0 667fb5ae… le registre étendu ; loupe 59e4871a… l'arbre neuf], les douze autres inchangées) et SERVIE au dossier /Cérémonie du Drive avec le LISEZMOI pas à pas ; la dette D166/D171 ÉCHUE AU BUILD — le geste hors-ligne du développeur (la clé du 04/11, « JAMAIS generer ») demeure LE seul chemin vers le build de Loupe

**Le contexte qui fonde la décision (08/11 au soir, la demande du développeur).** « go pour la cérémonie » : le message arme la cérémonie d'ère que le programme annonçait (la ligne SUITE de l'Entrée 199). Les quatre chantiers de notation sont accomplis (D172–D175 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS), la couche I est FINALE, la spécification v0.8.0 livrée — la dette de cérémonie D166/D171 est ÉCHUE AU BUILD : aucun octet de build ne naîtra avant la remise du développeur installée (le garde suit le calendrier de la cérémonie, jamais l'inverse — § 13.5).

**Les règles.** (1) **L'extension du registre figé vit AU GESTE de la cérémonie** (D168 : la charge se prépare au geste — l'ouverture ANNONCE, la cérémonie EXIGE) : m0/I/README.md § 2.1 porte désormais `loupe` (M10), m0 est DIVERGÉ nommément (CODE 10, fichier modifié : README.md) — l'extension promise par la couche I de Loupe à sa naissance (D171, règle 8). (2) **Le quatorzième arbre entre à la table canonique** : `loupe` (loupe.exe, l'éditeur hexadécimal au panneau d'empreintes), balise `loupe.1`, à sa place d'ère après `tls13.1` — l'arbre est NEUF (CODE 12 : manifeste déposé absent), sa première signature naîtra de cette cérémonie ; la spec v06/I DEMEURE figée à l'ère 0.6.0 (la table vivante est celle de l'outil, le sceau ne se re-spécifie pas à chaque ère). (3) **La remise est COMPLÈTE et FRAÎCHE** : quatorze lignes (une rotation couvre TOUS les arbres — spec § 5), régénérée au geste (D168) ; les douze arbres inchangés seront re-signés à l'identique par le déterminisme Ed25519 (la preuve D163, rejouée à chaque cérémonie). (4) **AUCUN build ne précède la remise installée** : le garde à QUATORZE arbres VERTS est la condition du build de Loupe — le kit terrain (M10-(d) seconde moitié) suit le build, le run (M10-(e)) suit le kit, la balise `loupe 0.1.0` se scellera sur le run terrain vert recoupé.

**Alternatives rejetées.** Signer à la clé de test pour débloquer le build (rejeté : déclasserait l'état « reelle » — une régression de preuve, D87 : le labo ne signe jamais à la place du développeur) ; attendre la clôture de M10 pour tout signer d'un coup (rejeté : la dette est ÉCHUE AU BUILD — chaque étape a sa cérémonie au moment où le garde l'exige, le miroir des ères M8/M9) ; étendre le registre sans re-signer m0 (rejeté : un diff d'intention non signé — le garde le nommerait CODE 10 indéfiniment, le build naîtrait sur une dette cachée) ; poser le domaine `loupe` sous un arbre existant (rejeté : un identifiant n'est jamais réutilisé, chaque ère son arbre — § 2.1) ; mettre à jour la table normative v06/I (rejeté : la spec du sceau est figée à son ère, la table vivante vit dans l'outil — la preuve D75/D105 : ce qui est signé ne se ré-écrit pas, ce qui vit se met à jour).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 — la cérémonie ne scelle rien) ; les 18 spécifications et les notations INTACTES (R2 — la cérémonie signe les écrits, elle ne les touche pas) ; le proxy 1.0.0 et la carte tls13 INTACTS ; l'outil hors-ligne INCHANGÉ (agnostique de la table des arbres) ; la clé privée JAMAIS au bac à sable (D87). Les pièces : m0/I/README.md (le registre étendu), v06/sceau_I.py (la table à quatorze), v06/sceau-I/a-signer.txt (la remise, 14 arbres), download/LISEZMOI-ceremonie-ere-TGN.txt (le pas à pas, déposé au /Cérémonie du Drive), scripts/maj_kit.py (RACINE_KIT + NOTE_D130 réorientées), scripts/consigner_ceremonie_tgn.py, scripts/deposer_lisezmoi_ere_tgn.py (le recoup indépendant).
"""

# --- le worklog : la Task ID 118 ----------------------------------------------------

TASK = """

## Task ID 118 — LA CÉRÉMONIE D'ÈRE DU TGN ARMÉE : le kit servi au /Cérémonie, la remise fraîche des quatorze arbres, le geste hors-ligne du développeur attendu (08/11 au soir)

- LA DEMANDE : « go pour la cérémonie » — armer la cérémonie d'ère du TGN
  (le 14e arbre, la dette D166/D171 échue au build — la ligne SUITE de
  l'Entrée 199 l'annonçait).
- LE GESTE SOURCE : le registre figé de m0 ÉTENDU (`loupe` M10 —
  l'extension promise par loupe/I/README.md à la cérémonie, D171/D168) ;
  la table canonique de sceau_I.py à QUATORZE arbres (loupe.1 après
  tls13.1, l'ordre des ères) ; l'outil hors-ligne AGNOSTIQUE de la table —
  aucune pièce du kit à changer pour lui.
- LA REMISE : preparer AU GESTE (D168 rejouée) — 14 arbres, DEUX
  empreintes nouvelles (m0 667fb5ae… le registre étendu ; loupe
  59e4871a… l'arbre neuf, 19 fichiers), les douze autres inchangées ; le
  constat sur pièces : m0 CODE 10 + loupe CODE 12, les douze autres
  VERTS — le miroir exact de l'ère M9 (Entrée 165).
- LE KIT : LISEZMOI-ceremonie-ere-TGN.txt écrit (le pourquoi, les deux
  empreintes, la règle d'or « JAMAIS generer », le pas à pas console +
  graphique, ce que cela débloque, le contrat D87) ; maj_kit.py étendu
  (RACINE_KIT + NOTE_D130 réorientée vers la cérémonie courante) ; le kit
  déposé au geste du commit (hook D130), le recoup indépendant par
  scripts/deposer_lisezmoi_ere_tgn.py (md5 par relecture, la remise du
  kit == celle du dépôt).
- FRONTIÈRES : aucune balise ne bouge, AUCUN build, aucun octet de
  notation (R2 — les écrits intacts, la cérémonie les signe) ; la dette
  demeure jusqu'à la remise du développeur (le garde constate m0 CODE 10
  + loupe CODE 12, les douze autres VERTS).
- SUITE : le geste hors-ligne du développeur (la clé du 04/11,
  signatures-I.txt + cle-publique-I.txt au /test) ; le labo recoupe et
  installe — le garde à QUATORZE VERTS ; puis le build loupe 0.1.0-dev.1,
  le kit terrain (M10-(d) seconde moitié) et le run (M10-(e)).
"""


# ------------------------------------------------------------------ gardes

def gardes():
    """L'état de dette nommé, le miroir de l'ère M9 — sinon ÉCHEC, rien n'est écrit."""
    if not LISEZMOI.is_file():
        sys.exit("ÉCHEC : LISEZMOI-ceremonie-ere-TGN.txt absent du download/ labo.")
    attendus = {"m0": sceau_I.CODE_DIVERGE, "loupe": sceau_I.CODE_DEPOT}
    for arbre in sceau_I.ARBRES:
        try:
            code, empreinte, detail = sceau_I._etat_arbre(arbre)
        except sceau_I.EchecSceauI as exc:
            sys.exit(f"ÉCHEC : arbre {arbre} illisible — {exc}")
        if arbre in attendus:
            if code != attendus[arbre]:
                sys.exit(f"ÉCHEC : {arbre} attendu CODE {attendus[arbre]} (la dette "
                         f"nommée), lu CODE {code} — {detail}")
        elif code != sceau_I.OK:
            sys.exit(f"ÉCHEC : {arbre} attendu VERT, lu CODE {code} — {detail}")
    if len(sceau_I.ARBRES) != 14:
        sys.exit(f"ÉCHEC : la table canonique porte {len(sceau_I.ARBRES)} arbres "
                 "(attendu : 14 — le quatorzième `loupe`).")
    lignes = [l.strip() for l in ASIGNER.read_text(encoding="utf-8").splitlines()
              if l.strip()]
    if len(lignes) != 14:
        sys.exit(f"ÉCHEC : la remise porte {len(lignes)} lignes (attendu : 14).")
    par_arbre = {l.split()[0]: l for l in lignes}
    if not par_arbre["m0"].endswith(EMP_M0):
        sys.exit("ÉCHEC : l'empreinte m0 de la remise n'est pas celle du geste "
                 f"(attendu …{EMP_M0[-16:]}).")
    if not par_arbre["loupe"].endswith(EMP_LOUPE):
        sys.exit("ÉCHEC : l'empreinte loupe de la remise n'est pas celle du geste "
                 f"(attendu …{EMP_LOUPE[-16:]}).")
    texte_lisezmoi = LISEZMOI.read_text(encoding="utf-8")
    for emp in (EMP_M0, EMP_LOUPE):
        if emp not in texte_lisezmoi:
            sys.exit("ÉCHEC : le LISEZMOI ne cite pas l'empreinte "
                     f"{emp[:16]}… noir sur blanc.")
    print("[consigner-ceremonie-tgn] gardes vertes : la dette nommée constatée "
          "(m0 CODE 10, loupe CODE 12, les douze autres VERTS) ; la remise à "
          "14 arbres aux empreintes du geste ; le LISEZMOI présent.")


# ------------------------------------------------------------------ le geste

def main() -> int:
    gardes()

    # ---- 1) le journal : l'Entrée 200 AVANT le marqueur (ordre 199 < 200) ----
    t = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 200 —" in t:
        print("[consigner-ceremonie-tgn] REJEU REFUSÉ : l'Entrée 200 existe déjà.")
        return 1
    if "## Entrée 199 —" not in t:
        print("[consigner-ceremonie-tgn] ÉCHEC : l'Entrée 199 absente (ordre rompu).")
        return 1
    n = t.count(MARQUEUR)
    if n != 1:
        print(f"[consigner-ceremonie-tgn] ÉCHEC : marqueur m5a {n} fois.")
        return 1
    t = t.replace(MARQUEUR, ENTREE.strip("\n") + "\n\n" + MARQUEUR, 1)
    JOURNAL.write_text(t, encoding="utf-8")
    print("[consigner-ceremonie-tgn] journal : Entrée 200 insérée avant le marqueur.")

    # ---- 2) les décisions : la D177 à la suite de la D176 ----
    d = DECISIONS.read_text(encoding="utf-8")
    if "## D177 —" in d:
        print("[consigner-ceremonie-tgn] REJEU REFUSÉ : D177 existe déjà.")
        return 1
    if "## D176 —" not in d:
        print("[consigner-ceremonie-tgn] ÉCHEC : D176 absente (ordre rompu).")
        return 1
    d = d.rstrip("\n") + "\n" + D177.strip("\n") + "\n"
    DECISIONS.write_text(d, encoding="utf-8")
    print("[consigner-ceremonie-tgn] décisions : D177 consignée à la suite de D176.")

    # ---- 3) le plan : l'État + la rangée (d) + la phrase de la dette ----
    p = PLAN.read_text(encoding="utf-8")
    if p.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État trouvé {p.count(ANCIEN_ETAT)} fois "
                 "(attendu : 1).")
    if p.count(RANGEE_D_ANCIENNE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (d) trouvé {p.count(RANGEE_D_ANCIENNE)} "
                 "fois (attendu : 1).")
    if p.count(DETTE_ANCIENNE) != 1:
        sys.exit(f"ÉCHEC : ancrage dette TGN trouvé {p.count(DETTE_ANCIENNE)} "
                 "fois (attendu : 1).")
    p = p.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
    p = p.replace(RANGEE_D_ANCIENNE, RANGEE_D_NOUVELLE, 1)
    p = p.replace(DETTE_ANCIENNE, DETTE_NOUVELLE, 1)
    if EMP_M0[:8] not in p or EMP_LOUPE[:8] not in p:
        sys.exit("ÉCHEC : les empreintes du geste (préfixes 8, la convention du "
                 "plan) absentes du plan après remplacement.")
    PLAN.write_text(p, encoding="utf-8")
    print("[consigner-ceremonie-tgn] plan : l'État de la cérémonie + la rangée "
          "(d) + la phrase de la dette remplacées (3 ancres, 1/1 chacune).")

    # ---- 4) le worklog : la Task ID 118 en append ----
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 118 —" in w:
        print("[consigner-ceremonie-tgn] REJEU REFUSÉ : Task ID 118 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK.rstrip("\n") + "\n"
    WORKLOG.write_text(w, encoding="utf-8")
    print("[consigner-ceremonie-tgn] worklog : Task ID 118 ajoutée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
