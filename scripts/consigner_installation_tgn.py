#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_installation_tgn.py — LA CONSIGNATION DE L'INSTALLATION DE LA
CÉRÉMONIE D'ÈRE DU TGN (« signatures déposées dans le dossier /test du
drive ») : la remise des QUATORZE arbres du développeur RECROPÉE 14/14 SUR
PIÈCES et INSTALLÉE canoniquement — LE GARDE QUATORZE arbres VERTS, LA
DETTE D166/D171 SOLDÉE, l'ère du TGN OUVERTE AU BUILD (le miroir exact de
l'Entrée 168, la cérémonie de l'ère M9).

Le journal reçoit l'Entrée 201, le PLAN reçoit l'État de l'installation
(la phrase de l'armement remplacée) + la rangée (d) + la phrase de la
dette au programme TGN, le worklog reçoit la Task ID 119. AUCUNE nouvelle
décision (le miroir de l'Entrée 168 : l'installation est l'exécution de
la D177, elle ne décide rien de nouveau).

GARDES AVANT ÉCRITURE (l'état de dette SOLDÉE, le miroir de l'ère M9) :
  - sceau I : LES QUATORZE arbres VERTS (m0 à 667fb5ae… le registre
    étendu, loupe à 59e4871a… l'arbre neuf), l'état « reelle » ;
  - les pièces rapatriées : download/ceremonie-tgn/signatures-I.txt (md5
    f33c803a…) + cle-publique-I.txt (md5 188a7d42…) ;
  - les signatures INSTALLÉES : m0.txt == 9090752d… (la re-signature du
    registre étendu, ≠ c71bf747… l'ère close) et loupe.txt == 08caf05f…
    (LA PREMIÈRE signature de l'arbre) ;
  - la remise v06/sceau-I/a-signer.txt : QUATORZE lignes aux empreintes
    du geste.
Tout écart = ÉCHEC NOMMÉ, rien n'est écrit. Rejeu REFUSÉ."""

import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
ASIGNER = REPO / "v06" / "sceau-I" / "a-signer.txt"
ETAT_CLE = REPO / "v06" / "sceau-I" / "etat-cle.txt"
PIECES = REPO / "download" / "ceremonie-tgn"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_ceremonie_tgn as _c200  # noqa: E402  # la chaîne des gestes

sys.path.insert(0, str(REPO / "v06"))
import sceau_I  # noqa: E402

# --- l'empreinte de l'état du geste (les valeurs constatées au geste) ---------------

EMP_M0 = "667fb5ae36e4ab3c5dcfd4899fc680fd5b2393d2cdc6ad32241be14b89d9f920"
EMP_LOUPE = "59e4871ab5b47623be8aad0d6633abf7a1f8b64acd6f87f4f87e2003aa5d8520"
SIG_M0_NOUVELLE = ("9090752d7eda43cd2edf64c548558a8294013d9199821bbafdba9f8be0"
                   "69c0b3dac81fbcd83a3b4c4e67c2e712b24286084f21707b68bc5ffda2c"
                   "1dbd654af02")
SIG_LOUPE_PREMIERE = ("08caf05f6174e1fa18b2183408416f143b6594dfea292934e1e8206"
                      "5ff0c246f0b289d10529adb163d6a847e21d6fb4dbe3bf029fb694d7"
                      "11b5ff38133006a0d")
MD5_REMISE = "f33c803aad80711995c6ea61ce30aa7b"
MD5_CLE = "188a7d42df2d03f68bfb50fada3a84a1"

# --- le plan : l'État du programme (la phrase de l'armement remplacée) --------------

ANCIEN_ETAT = _c200.NOUVEL_ETAT   # l'État 200 (la cérémonie armée, la suite)

NOUVEL_ETAT = (
    "**LA CÉRÉMONIE D'ÈRE DU TGN PASSÉE SUR PIÈCES le 09/11/2026 (Entrée 201, "
    "Task 119) : LA DETTE D166/D171 SOLDÉE — LE GARDE QUATORZE arbres VERTS, "
    "L'ÉTAT « reelle » TENANT (le geste hors-ligne du développeur, l'annonce "
    "« signatures déposées dans le dossier /test du drive »)** — la remise "
    "RECROPÉE 14/14 SUR PIÈCES AVANT tout dépôt (rapatrier_ceremonie_tgn.py, "
    "modèle D166 r.8 : l'ANCRE DE CLÉ tenue [la clé déposée == 173fae9c… "
    "l'ancre des ères == l'ancre locale — la règle d'or « JAMAIS generer »] ; "
    "le format 14/14 lignes, balises == la table canonique à QUATORZE arbres ; "
    "LE RECOUP D163 REJOINT UNE SIXIÈME FOIS [les DOUZE arbres inchangés aux "
    "signatures BYTE-IDENTIQUES aux déposées — Ed25519 déterministe, la clé du "
    "04/11 réutilisée, sans jamais voir la clé privée] ; m0 RE-SIGNÉ "
    "[9090752d… contre 667fb5ae… LE REGISTRE FIGÉ ÉTENDU — la signature diverge "
    "de la déposée c71bf747… de l'ère close, vérifiée Ed25519] ; LOUPE L'ARBRE "
    "NEUF SIGNÉ [08caf05f… contre 59e4871a… — LA PREMIÈRE signature de l'arbre "
    "des 19 fichiers, le quatorzième entre au monde signé] ; LE DIFF CONTRÔLÉ "
    "vs l'ère close [la ligne m0 changée + la ligne loupe ajoutée, les DOUZE "
    "autres byte-identiques] ; les empreintes vivantes == a-signer.txt 14/14 ; "
    "chaque signature VÉRIFIÉE Ed25519 14/14 VERT) ; le dépôt canonique JOUÉ "
    "(l'atomicité de cérémonie : QUATORZE signatures vérifiées AVANT toute "
    "écriture, installées avec les manifestes vivants, l'état « reelle "
    "(ceremonie hors-ligne, D87) » INTACT) ; verifier : QUATORZE arbres VERTS, "
    "code 0. L'ÈRE DU TGN EST OUVERTE AU BUILD. SUITE : LE BUILD DE LOUPE "
    "loupe 0.1.0-dev.1 (le geste de BUILD jamais scellage : construire() "
    "compose l'artefact — les 18 blocs notés aux slots ARRÊTÉS, les héritages "
    "PAR LA CARTE aux adresses scellées [R7 : libc-01/02/07, la famille sha "
    "tls13-01..04, la boucle win-03], le cadre, la vitrine, l'éditeur ; "
    "l'oracle structurel y lira l'application ENTIÈRE née des seuls blocs "
    "scellés), puis la carte génération + le verrou croisé + la "
    "cristallisation, le kit terrain (M10-(d) seconde moitié, modèle m9f) et "
    "le run (M10-(e))**"
)

# --- le plan : la rangée (d) — la cérémonie passée sur pièces -----------------------

RANGEE_D_ANCIENNE = _c200.RANGEE_D_NOUVELLE
RANGEE_D_NOUVELLE = (
    "l'oracle 45 VERTS × 3 graines (le disque saisissable, la mort complète, "
    "LE RÉSEAU de la garde, la falsification) ; LA CÉRÉMONIE D'ÈRE PASSÉE SUR "
    "PIÈCES (Entrée 201, Task 119) : la remise du développeur RECROPÉE 14/14 "
    "ET INSTALLÉE (l'ancre de clé 173fae9c… tenue, LE RECOUP D163 la sixième "
    "fois — les douze inchangés aux signatures déposées, m0 re-signé "
    "9090752d… au registre étendu, loupe l'arbre neuf signé 08caf05f… — sa "
    "première signature) — LE GARDE QUATORZE arbres VERTS, la dette D166/D171 "
    "SOLDÉE ; le build loupe 0.1.0-dev.1 DÉBLOQUÉ, le kit attend le build"
)

# --- le plan : la phrase de la dette au programme TGN -------------------------------

DETTE_ANCIENNE = _c200.DETTE_NOUVELLE
DETTE_NOUVELLE = (
    "la dette de cérémonie est nommée à la naissance (le modèle D166/D168) — "
    "LA CÉRÉMONIE D'ÈRE PASSÉE SUR PIÈCES le 09/11 (Entrée 201, Task 119) : "
    "le geste hors-ligne du développeur reçu, recoupé 14/14 et installé "
    "canoniquement, le garde à QUATORZE arbres VERTS, la dette D166/D171 "
    "SOLDÉE — l'ère du TGN est OUVERTE AU BUILD (loupe 0.1.0-dev.1, le geste "
    "de BUILD jamais scellage) ; aucun arbre signé n'a été touché hors le "
    "registre annoncé, la clé privée n'a jamais traversé le bac à sable (D87)."
)

# --- le journal : l'Entrée 201 -------------------------------------------------------

ENTREE = """## Entrée 201 — LA CÉRÉMONIE D'ÈRE DU TGN PASSÉE SUR PIÈCES : LA DETTE D166/D171 SOLDÉE (LE GARDE VERT QUATORZE arbres, L'ÉTAT « reelle » TENANT) — le geste du développeur venu et annoncé (« signatures déposées dans le dossier /test du drive »), le labo rapatrie, recoupe, installe — l'ère du TGN OUVERTE AU BUILD, le build de Loupe attendu (09/11)

**Le geste du développeur (l'annonce).** Le SUITE du Task 118 nommait LA CÉRÉMONIE HORS-LIGNE : signer la remise des QUATORZE arbres à la clé du 04/11 (la règle d'or « JAMAIS generer »), ramener signatures-I.txt + cle-publique-I.txt au coffre /test. Le développeur l'a conduite — l'annonce est venue : « signatures déposées dans le dossier /test du drive ». Les DEUX pièces sont au coffre /test (constaté au sondage).

**Le terrain a été vérifié avant de recevoir.** Le sondage du /test (lecture seule) : signatures-I.txt porte le md5 **f33c803a…** — NOUVEAU, ≠ les remises de l'ère close (62c43222… la remise du build 1.0.0 ; af382476… la seconde remise de la révision 2 étendue) : la signature de l'ère est CONSTATÉE ; cle-publique-I.txt == **188a7d42…** (l'ancre, inchangée — la clé du 04/11, la continuité « reelle »).

**Le rapatriement (LECTURE SEULE, md5 contrôlés).** scripts/rapatrier_ceremonie_tgn.py (modèle D166 r.8, le miroir de rapatrier_ceremonie_revision3.py — LECTURE SEULE sur v06/) : signatures-I.txt (1 991 o, md5 f33c803a…) et cle-publique-I.txt (65 o, md5 188a7d42…) téléchargés par le canal OAuth du relais vers download/ceremonie-tgn/, md5 re-contrôlés APRÈS écriture contre les métadonnées Drive — MATCH ; les remises PÉRIMÉES de l'ère close REFUSÉES NOMMÉES par avance (toute remise sans loupe = l'ère close, re-déposer l'ancienne n'est pas re-signer).

**Le recoup intégral AVANT tout dépôt (le verdict, pas la croyance).** (a) L'ANCRE DE CLÉ : la clé DÉPOSÉE PAR LE DÉVELOPPEUR == 173fae9c75229b15… (l'ancre de toutes les ères — la règle d'or « JAMAIS generer » respectée, la continuité de l'état « reelle » tenue) ; l'ancre locale du dépôt identique. (b) LE FORMAT : 14/14 lignes valides « arbre balise signature-128hex », balises == la table canonique à QUATORZE arbres (la rotation couvre TOUS les arbres, spec § 5). (c) LE RECOUP DE L'ÈRE (D163 REJOINT UNE SIXIÈME FOIS) : les DOUZE arbres inchangés (m1–m8, tls13, demo, terrain, v06) rendent les MÊMES signatures que celles déposées à l'ère close — la preuve de la réutilisation de la clé du 04/11 PAR LE DÉTERMINISME Ed25519, sans jamais voir la clé privée. (d) m0 RE-SIGNÉ : la signature nouvelle **9090752d…** DIVERGE de la déposée de l'ère close (c71bf747… — l'ancien registre) et VÉRIFIE Ed25519 contre l'empreinte vivante **667fb5ae36e4ab3c…** du REGISTRE FIGÉ ÉTENDU (le domaine `loupe` (M10) au registre des domaines — l'extension promise à cette cérémonie, D171/D168). (e) LOUPE, L'ARBRE NEUF : AUCUNE signature déposée n'existait (l'arbre n'a JAMAIS été signé), l'empreinte vivante == **59e4871ab5b47623…** (l'arbre complet des 19 fichiers : le README + les 18 spécifications loupe-01..18 en cinq familles), la signature **08caf05f…** VÉRIFIÉE Ed25519 — LA PREMIÈRE SIGNATURE DE L'ARBRE, le quatorzième entre au monde signé. (f) LE DIFF CONTRÔLÉ vs l'ère close : UNE ligne changée, LA m0, UNE ligne AJOUTÉE, LOUPE, les DOUZE autres byte-identiques (le précédent M9-(d) tenu sur les signatures). (g) LES EMPREINTES VIVANTES == a-signer.txt 14/14 (la remise fraîche régénérée au geste de l'Entrée 200 — la charge de l'ARBRE COURANT). (h) CHAQUE SIGNATURE VÉRIFIÉE Ed25519 contre la clé de l'ère sur l'empreinte du manifeste VIVANT : 14/14 VERT. **RECOUPE INTÉGRAL VERT — 14/14.**

**Le dépôt canonique (l'atomicité).** sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt JOUÉ : les QUATORZE signatures vérifiées INTÉGRALEMENT avant toute écriture, puis installées avec les manifestes vivants — l'état « reelle (ceremonie hors-ligne, D87) » INTACT. Puis LES CONTRÔLES : verifier → **QUATORZE arbres VERTS**, code 0 (m0 vert [667fb5ae…] + loupe vert [59e4871a…] — la dette NOMMÉE à l'Entrée 200 est la dette SOLDÉE) ; etat → clé « reelle », la table des quatorze arbres tous SIGNE (vert). **LA DETTE D166/D171 EST SOLDÉE — L'ÈRE DU TGN EST OUVERTE AU BUILD.**

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 INTACTES), AUCUN build exécuté (le build loupe 0.1.0-dev.1 est LE geste suivant — construire() suit le garde VERT, le miroir des ères M8/M9 : la remise installée, le build PEUT naître), AUCUN octet de notation (R2 — les 18 spécifications et les notations INTACTES, la cérémonie les a signées, elle ne les touche pas), le proxy 1.0.0 et la carte tls13 INTACTS, la clé privée n'a JAMAIS traversé le bac à sable (le contrat D87 tenu — le labo n'a rien signé). Livrables : download/ceremonie-tgn/ (les deux pièces rapatriées), scripts/rapatrier_ceremonie_tgn.py, scripts/consigner_installation_tgn.py ; consignations : la présente Entrée PAR SCRIPT, PLAN (l'État + la rangée (d) + la phrase de la dette au programme TGN), worklog +Task ID 119. Ce que cela DÉBLOQUE : **LE BUILD DE LOUPE** (le même geste, côté dépôt : construire() compose l'artefact loupe 0.1.0-dev.1 — geste de BUILD jamais scellage [miroir M6/M7/M8] ; les 18 blocs notés aux slots ARRÊTÉS [D161/D173–D175], les héritages PAR LA CARTE aux adresses scellées [R7 : libc-01/02/07, la famille sha tls13-01..04, la boucle win-03], le cadre, la vitrine, l'éditeur — et l'oracle structurel y lira l'application ENTIÈRE née des seuls blocs scellés) ; puis la carte génération, le verrou croisé, la cristallisation ; puis le kit terrain (M10-(d) seconde moitié, modèle m9f : le coffre /test recevra la vague Loupe) et le run (M10-(e)) : le VRAI Windows 11, l'application réelle ouverte, éditée, sauvegardée — et si le vert tient, la balise `loupe 0.1.0` scellée sur run terrain recoupé : LE JALON M10, la méthode entière prouvée par la CRÉATION.

- SUITE : LE BUILD DE LOUPE loupe 0.1.0-dev.1 (le geste de BUILD, le garde est VERT — construire() compose l'artefact des 18 blocs notés + les héritages scellés, puis la carte génération + le verrou croisé + la cristallisation) ; puis le kit terrain (M10-(d) seconde moitié, modèle m9f) et le run (M10-(e)) ; le projet fils attend son premier geste à son message propre.
"""

# --- le worklog : la Task ID 119 ----------------------------------------------------

TASK = """

## Task ID 119 — LA CÉRÉMONIE D'ÈRE DU TGN PASSÉE SUR PIÈCES : la remise du développeur recoupée 14/14 et installée, le garde QUATORZE arbres VERTS, la dette D166/D171 soldée — l'ère ouverte au build (09/11)

- LA DEMANDE : « signatures déposées dans le dossier /test du drive » — le
  geste hors-ligne du développeur annoncé (la ligne SUITE du Task 118
  l'attendait : signer la remise des 14 arbres à la clé du 04/11).
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR : le sondage /test —
  signatures-I.txt md5 f33c803a… NOUVEAU (≠ les remises de l'ère close :
  62c43222… le build 1.0.0, af382476… la révision 2 étendue),
  cle-publique-I.txt 188a7d42… (l'ancre, inchangée).
- LE RAPATRIEMENT : rapatrier_ceremonie_tgn.py (modèle D166 r.8, LECTURE
  SEULE sur v06/) — les DEUX pièces vers download/ceremonie-tgn/, md5
  contrôlés APRÈS écriture (MATCH les métadonnées Drive), les remises
  PÉRIMÉES refusées nommées par avance.
- LE RECOUP INTÉGRAL AVANT DÉPÔT : l'ancre de clé 173fae9c… tenue (==
  l'ancre locale) ; le format 14/14 ; LE RECOUP D163 LA SIXIÈME FOIS (les
  DOUZE inchangés == les déposées — Ed25519 déterministe, la clé du
  04/11 réutilisée) ; m0 re-signé 9090752d… contre 667fb5ae… (le registre
  étendu — la signature diverge de c71bf747… l'ère close) ; LOUPE l'arbre
  neuf signé 08caf05f… contre 59e4871a… (SA PREMIÈRE signature) ; le diff
  contrôlé (m0 changée + loupe ajoutée, les douze autres
  byte-identiques) ; les empreintes vivantes == a-signer.txt 14/14 ;
  14/14 VERT Ed25519.
- LE DÉPÔT CANONIQUE : sceau_I.py deposer --cle (l'atomicité — tout
  vérifié AVANT toute écriture) ; verifier : QUATORZE arbres VERTS code
  0 ; etat : « reelle » — LA DETTE D166/D171 SOLDÉE, l'ère du TGN
  OUVERTE AU BUILD.
- FRONTIÈRES : aucune balise ne bouge, AUCUN build à ce geste (le build
  loupe 0.1.0-dev.1 est le geste suivant), aucun octet de notation (R2),
  la clé privée jamais traversée (D87 — le labo n'a rien signé).
- SUITE : LE BUILD DE LOUPE (loupe 0.1.0-dev.1 — construire(), la carte
  génération, le verrou croisé, la cristallisation) ; puis le kit terrain
  (M10-(d) seconde moitié, modèle m9f) et le run (M10-(e)).
"""


# ------------------------------------------------------------------ gardes

def _md5(chemin):
    return hashlib.md5(chemin.read_bytes()).hexdigest()


def gardes():
    """L'état de dette SOLDÉE, le miroir de l'ère M9 — sinon ÉCHEC, rien n'est écrit."""
    remise = PIECES / "signatures-I.txt"
    cle = PIECES / "cle-publique-I.txt"
    if not remise.is_file() or not cle.is_file():
        sys.exit("ÉCHEC : les pièces rapatriées absentes de download/ceremonie-tgn/.")
    if _md5(remise) != MD5_REMISE:
        sys.exit(f"ÉCHEC : md5 remise {_md5(remise)} != {MD5_REMISE} (la pièce du geste).")
    if _md5(cle) != MD5_CLE:
        sys.exit(f"ÉCHEC : md5 clé {_md5(cle)} != {MD5_CLE} (l'ancre).")
    if ETAT_CLE.read_text(encoding="utf-8").strip() != \
            "reelle (ceremonie hors-ligne, D87)":
        sys.exit("ÉCHEC : l'état de clé n'est pas « reelle (ceremonie hors-ligne, "
                 "D87) ».")
    if len(sceau_I.ARBRES) != 14:
        sys.exit(f"ÉCHEC : la table canonique porte {len(sceau_I.ARBRES)} arbres "
                 "(attendu : 14).")
    for arbre in sceau_I.ARBRES:
        try:
            code, empreinte, detail = sceau_I._etat_arbre(arbre)
        except sceau_I.EchecSceauI as exc:
            sys.exit(f"ÉCHEC : arbre {arbre} illisible — {exc}")
        if code != sceau_I.OK:
            sys.exit(f"ÉCHEC : {arbre} attendu VERT (la dette soldée), lu CODE "
                     f"{code} — {detail}")
    # les empreintes du geste, relues à la table verte
    _, emp_m0 = sceau_I.manifeste("m0")
    _, emp_loupe = sceau_I.manifeste("loupe")
    if emp_m0 != EMP_M0:
        sys.exit("ÉCHEC : l'empreinte m0 vivante n'est pas celle du geste "
                 f"(attendu {EMP_M0[:16]}…).")
    if emp_loupe != EMP_LOUPE:
        sys.exit("ÉCHEC : l'empreinte loupe vivante n'est pas celle du geste "
                 f"(attendu {EMP_LOUPE[:16]}…).")
    # les signatures INSTALLÉES : la re-signature de m0 + la première de loupe
    sig_m0 = (REPO / "v06" / "sceau-I" / "signatures" / "m0.txt").read_text(
        encoding="utf-8").strip()
    sig_loupe = (REPO / "v06" / "sceau-I" / "signatures" / "loupe.txt").read_text(
        encoding="utf-8").strip()
    if sig_m0 != SIG_M0_NOUVELLE:
        sys.exit("ÉCHEC : la signature m0 installée n'est pas la re-signature du "
                 "registre étendu (attendu 9090752d…).")
    if sig_loupe != SIG_LOUPE_PREMIERE:
        sys.exit("ÉCHEC : la signature loupe installée n'est pas la première "
                 "signature de l'arbre (attendu 08caf05f…).")
    # la remise fraîche du dépôt : quatorze lignes aux empreintes du geste
    lignes = [l.strip() for l in ASIGNER.read_text(encoding="utf-8").splitlines()
              if l.strip()]
    if len(lignes) != 14:
        sys.exit(f"ÉCHEC : a-signer.txt porte {len(lignes)} lignes (attendu : 14).")
    par_arbre = {l.split()[0]: l for l in lignes}
    if not par_arbre["m0"].endswith(EMP_M0):
        sys.exit("ÉCHEC : l'empreinte m0 de la remise du dépôt n'est pas celle "
                 f"du geste (attendu …{EMP_M0[-16:]}).")
    if not par_arbre["loupe"].endswith(EMP_LOUPE):
        sys.exit("ÉCHEC : l'empreinte loupe de la remise du dépôt n'est pas celle "
                 f"du geste (attendu …{EMP_LOUPE[-16:]}).")
    print("[consigner-installation-tgn] gardes vertes : le garde QUATORZE arbres "
          "VERTS (m0 à 667fb5ae…, loupe à 59e4871a…), l'état « reelle » ; les "
          "pièces rapatriées md5-contrôlées ; m0 installé à la re-signature "
          "9090752d…, loupe à sa première signature 08caf05f… ; la remise du "
          "dépôt à 14 arbres aux empreintes du geste.")


# ------------------------------------------------------------------ le geste

def main() -> int:
    gardes()

    # ---- 1) le journal : l'Entrée 201 AVANT le marqueur (ordre 200 < 201) ----
    t = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 201 —" in t:
        print("[consigner-installation-tgn] REJEU REFUSÉ : l'Entrée 201 existe déjà.")
        return 1
    if "## Entrée 200 —" not in t:
        print("[consigner-installation-tgn] ÉCHEC : l'Entrée 200 absente (ordre rompu).")
        return 1
    n = t.count(MARQUEUR)
    if n != 1:
        print(f"[consigner-installation-tgn] ÉCHEC : marqueur m5a {n} fois.")
        return 1
    t = t.replace(MARQUEUR, ENTREE.strip("\n") + "\n\n" + MARQUEUR, 1)
    JOURNAL.write_text(t, encoding="utf-8")
    print("[consigner-installation-tgn] journal : Entrée 201 insérée avant le marqueur.")

    # ---- 2) le plan : l'État + la rangée (d) + la phrase de la dette ----
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
    for attendu in ("9090752d", "08caf05f"):
        if attendu not in p:
            sys.exit(f"ÉCHEC : le préfixe {attendu}… absent du plan après "
                     "remplacement (la convention du plan : préfixes 8).")
    PLAN.write_text(p, encoding="utf-8")
    print("[consigner-installation-tgn] plan : l'État de l'installation + la rangée "
          "(d) + la phrase de la dette remplacées (3 ancres, 1/1 chacune).")

    # ---- 3) le worklog : la Task ID 119 en append ----
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 119 —" in w:
        print("[consigner-installation-tgn] REJEU REFUSÉ : Task ID 119 existe déjà.")
        return 1
    if "## Task ID 118 —" not in w:
        print("[consigner-installation-tgn] ÉCHEC : Task ID 118 absente (ordre rompu).")
        return 1
    w = w.rstrip("\n") + "\n" + TASK.rstrip("\n") + "\n"
    WORKLOG.write_text(w, encoding="utf-8")
    print("[consigner-installation-tgn] worklog : Task ID 119 ajoutée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
