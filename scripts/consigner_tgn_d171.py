#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_tgn_d171.py — LA CONSIGNATION DU GESTE D'OUVERTURE DU TEST
GRANDEUR NATURE « L'APPLICATION "LOUPE" ARBITRÉE, LE DOMAINE loupe FONDÉ
(LA CHARTE + LE TABLEAU DES 18 BLOCS, LA DETTE DE CÉRÉMONIE NOMMÉE) ; LE
PROJET COFFRE-FORT DÉGELÉ EN PARALLÈLE » : le plan reçoit le programme
TGN (une section neuve AVANT le projet fils) + la phrase de l'État du
programme + le dégel au fils, le journal reçoit l'Entrée 194, DECISIONS
reçoit la D171, le worklog reçoit la Task ID 112. Rejeu REFUSÉ ; tout
ancrage absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien
n'est écrit. Les ancres État sont importées de consigner_entree193 (la
chaîne des gestes tient sans retranscription)."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_entree193 as _c193  # noqa: E402  # la chaîne des gestes

# --- l'État du programme : la phrase du TGN remplace celle du jalon M9 --------------

ANCIEN_ETAT = _c193.NOUVEL_ETAT   # l'État 193 (le septième run + le jalon M9 franchi)

NOUVEL_ETAT = (
    "**LE TEST GRANDEUR NATURE OUVERT le 07/11/2026 (Entrée 194, D171, "
    "Task 112) : l'ère 1.0.0 refermée propre (la passation D141 passée, "
    "LES TROIS MIROIRS ALIGNÉS — la cohérence re-vérifiée à la pointe "
    "R4 17/17 : git 5/5 [HEAD == origin relu EN DIRECT], le coffre /test "
    "10/10, le miroir 2/2), la demande du développeur ouvre DEUX "
    "chantiers en parallèle — l'application « LOUPE » (l'éditeur "
    "hexadécimal natif au panneau d'empreintes, le jalon M10 : 18 blocs "
    "en CINQ familles [fichier · empreintes · rendu · navigation · "
    "édition], la charte posée à loupe/I/README.md, la dette de "
    "cérémonie nommée — le 14e arbre et l'extension du registre figé "
    "attendent la cérémonie d'ère) ET LE PROJET FILS COFFRE-FORT DÉGELÉ "
    "(D135 amendée : le développement différé cesse, le fils vit en "
    "parallèle sans dépendance vivante — aucun code TRIADE forké)**"
)

# --- la section du programme TGN (insérée AVANT le projet fils) ----------------------

SECTION_TGN = """## Programme TGN — le test grandeur nature (ouvert le 07/11/2026, D171)

La demande du développeur « on peut commencer le test grandeur nature : coder une appli entièrement avec Triade » EST la décision d'ouverture (D171, le modèle D149/D160 : le message du développeur ouvre). Le TGN est l'épreuve de la MÉTHODE ENTIÈRE : le protocole a prouvé chaque capacité, M0 à M9 — l'outil de validation l'a fait naître et le septième run l'a scellé (1.0.0, la session réelle) ; il reste à prouver qu'il DÉVELOPPE une application réelle NEUVE, de l'intention à l'octet livré. Le modèle RoomEq (v0.3) s'arrêtait au recodage d'une application existante — le TGN exige la CRÉATION. L'application — non nommée par le message, ARBITRÉE à D171, CONTREDISIBLE au message suivant (la couche I seule vit, rien n'est scellé) — est **« Loupe » : l'éditeur hexadécimal natif au panneau d'empreintes** (voir les octets, leurs lignes, leurs empreintes md5/sha-256, leur place — l'outil du quotidien du projet), sur le profil primaire `x86-64-win11-pe`, artefact `loupe.exe`, lignée de balises propre (`loupe 0.1.0-dev.1` au premier build — un projet de développement au sens du coffre, D137). Le domaine `loupe` est fondé (loupe/I/README.md : la charte + le tableau des 18 blocs en cinq familles + les conventions transverses) ; la dette de cérémonie est nommée à la naissance (le 14e arbre + l'extension du registre figé m0/I § 2.1 attendent la cérémonie d'ère — le modèle D166/D168 : le garde demeure à 13 arbres VERTS jusqu'alors, aucun arbre signé n'est touché).

| Chantier M10 (win, le TGN « Loupe ») | Contenu | Critère de sortie mesurable |
|---|---|---|
| (a) La couche I complète — **OUVERT (D171)** | les 18 spécifications loupe-01..18 posées (les cinq familles), les budgets et plans d'adressage déclarés avant toute notation | R2 tenue : chaque bloc porté par une spécification AVANT le premier octet de notation ; les vecteurs du harnais nommés (FIPS 180-4, les fixtures du dépôt) |
| (b) Le noyau — fichier + empreintes | ouvrir/lire/fermer + sha-256/md5 d'une gamme + le cumul du fichier entier par fenêtres glissantes | le harnais différentiel VERT sur vecteurs officiels + fichiers réels du dépôt (empreintes recoupées contre l'outil du labo) ; l'héritage sha PAR LA CARTE constaté byte-identique (R7) |
| (c) Le rendu + la navigation | la ligne hexa, l'écran, la peinture, le défilement, l'aller-à, la recherche d'octets | l'oracle à scénarios VERT (l'écran attendu octet par octet pour des états donnés) ; la falsification attrapée (une mutation = un refus nommé) |
| (d) L'édition + le kit terrain | curseur, saisie, sauver, quitter ; le kit livré au /test (modèle m9f : double-clic, témoin, réceptacle) | le kit déployé au coffre, LISEZMOI à jour, le réceptacle armé ; l'artefact empreinté par le build (D134) |
| (e) Le run terrain + le scellage | le développeur court LOUPE sur SA machine ; le recoup labo sur pièces ; la balise `loupe 0.1.0` scellée | le run VERT sur pièces + recoup N/N sur pièces croisées + la 0.1.0 SCELLÉE (fait de carte, l'artefact INTACT) + la clôture D143 des pièces |

"""

# --- le dégel du projet fils (append à la section Coffre-Fort, la fin du plan) -------

FIN_FILS = "la fondation est consignée D135 / Entrée 123 du présent dépôt."

DEGEL = """
**LE DÉGEL (07/11/2026, D171).** Le message du développeur qui ouvre le test grandeur nature porte aussi le dégel : « ça n'empêchera pas de continuer le projet Coffre Fort en parallèle ». Le développement différé CESSE — le fils vit EN PARALLÈLE du TGN (le père), chacun son rythme, AUCUN ne bloque l'autre. La frontière fondatrice demeure INTACTE : aucun code TRIADE forké, aucune dépendance vivante entre les dépôts (toute dépendance serait un défaut à consigner — D135 tenue). Le premier geste du fils viendra à son message propre."""

# --- la D171 (append à la suite de D170) ----------------------------------------------

D171 = """
## D171 — LE TEST GRANDEUR NATURE OUVERT : L'APPLICATION « LOUPE » ARBITRÉE (l'éditeur hexadécimal natif au panneau d'empreintes — coder une appli ENTIÈREMENT avec Triade, la demande du développeur) ; LE PROJET COFFRE-FORT DÉGELÉ EN PARALLÈLE (D135 amendée par le même message) ; LE DOMAINE `loupe` FONDÉ (la charte + le tableau des 18 blocs, la couche I écrite-avant-code — la dette de cérémonie nommée à la naissance)

**Le contexte qui fonde la décision (07/11).** Le message du développeur : « on peut commencer le test grandeur nature : coder une appli entièrement avec Triade. ça n'empêchera pas de continuer le projet Coffre Fort en parallèle ». L'ère 1.0.0 est refermée propre (D170 : la finale scellée sur le recoup terrain exigé comme pièce ; la passation D141 passée ; les trois miroirs alignés — la cohérence re-vérifiée à la pointe au geste d'ouverture de session, R4 17/17). Le programme D160 est accompli (les deux premières familles : M8 0.9.0, M9 1.0.0). Le TGN est la suite NATURELLE : le protocole a prouvé chaque capacité, il reste à prouver la MÉTHODE ENTIÈRE sur une application réelle neuve — le modèle RoomEq (v0.3, 44 spécifications) s'arrêtait au RECODAGE d'une application existante ; le TGN exige la CRÉATION. Le même message DÉGÈLE le projet fils Coffre-Fort (D135 : le développement en était différé au bouclage de TRIADE).

**Les règles.** (1) **L'application est codée ENTIÈREMENT par la méthode** : couche I écrite-avant-code (R2), notations à la main (keystone, l'outil du labo — jamais un compilateur), plan d'adressage arrêté avant la notation (D161), carte scellée, oracle à scénarios + harnais différentiel, kit terrain, recoup sur pièces — AUCUN octet d'application ne naît hors contrat. (2) **Le choix de l'application (délégué par le message qui ne la nommait pas) est ARBITRÉ** : « Loupe », l'éditeur hexadécimal au panneau d'empreintes — l'outil du quotidien du projet (toutes ses pièces vivent par leurs md5/sha-256), l'épreuve complète (GUI + fichiers + hachage + libc + recherche + édition : cinq familles en un artefact utile dès le premier run), le périmètre tenable (18 blocs, un jalon, un kit). Le choix est CONTREDISIBLE au message suivant : la couche I seule vit, rien n'est scellé. (3) **Le TGN vit dans SON domaine** (loupe/) avec SA lignée de balises (`loupe 0.1.0-dev.1` au premier build) : le proxy 1.0.0, la carte tls13 et les arbres scellés DEMEURENT INTACTS (l'anti-rollback armé). (4) **La dette de cérémonie est NOMMÉE À LA NAISSANCE** (le modèle D166) : le 14e arbre (loupe) et l'extension du registre figé (m0/I/README.md § 2.1) attendent la cérémonie d'ère du TGN — le geste hors-ligne du développeur, la re-signature de m0 au registre étendu (le modèle de l'ère M8) ; le garde demeure à 13 arbres VERTS jusqu'alors. (5) **COFFRE-FORT DÉGELÉ** : le message amende D135 — le fils vit EN PARALLÈLE, chacun son rythme, aucun ne bloque l'autre ; la frontière fondatrice demeure (aucun code forké, aucune dépendance vivante — toute dépendance serait un défaut à consigner). (6) **Les frontières du geste** : AUCUNE clé, AUCUN coffre réel, AUCUN fragment, AUCUN arbre signé touchés ; le sceau I vérifié AVANT consignation (13 arbres VERTS, cle deposee reelle).

**Alternatives rejetées.** Un navigateur web (rejeté : périmètre déraisonnable pour un premier TGN — un moteur de rendu est un projet par lui-même) ; un client Drive (rejeté : utile mais protocolairement lourd — OAuth 2.0 et JSON résolus à la main, différé à un TGN ultérieur) ; recoder une application existante (rejeté : c'est le modèle RoomEq DÉJÀ démontré — le TGN exige la création, la méthode doit prouver le NEUF) ; attendre le bouclage de Coffre-Fort pour ouvrir le TGN (rejeté : le message ouvre les DEUX en parallèle) ; éditer le registre figé m0/I au geste d'ouverture (rejeté : m0 est un arbre SIGNÉ — l'extension vit à la cérémonie d'ère, la dette est nommée, modèle D166/D168) ; demander à la machine de choisir l'application sans consigner l'arbitrage (rejeté : un arbitrage muet serait un contrat non écrit — D137 le tient pour les niveaux du coffre, le TGN le tient pour ses choix).
"""

# --- l'Entrée 194 (avant le marqueur m5a) ---------------------------------------------

ENTREE_194 = """## Entrée 194 — « on peut commencer le test grandeur nature : coder une appli entièrement avec Triade. ça n'empêchera pas de continuer le projet Coffre Fort en parallèle » : LE TEST GRANDEUR NATURE OUVERT — L'APPLICATION « LOUPE » ARBITRÉE, LE DOMAINE `loupe` FONDÉ (LA CHARTE + LE TABLEAU DES 18 BLOCS, LA DETTE DE CÉRÉMONIE NOMMÉE) ; LE PROJET COFFRE-FORT DÉGELÉ EN PARALLÈLE (07/11)

**La reprise (le geste qui ouvre la session : la cohérence re-vérifiée à la pointe — R4, 17/17).** Le labo relit l'état après la passation : `verifier_coherence_git_drive_r4.py` [labo] — le miroir du vérificateur recalé sur la pointe 011ba3c : GIT 5/5 (HEAD == origin == 011ba3c, relu EN DIRECT par ls-remote — la preuve hors cache local ; l'arbre propre ; le fetch joignable), LE COFFRE /test 10/10 (la racine 19 entrées, le kit RÉPARÉ 92098687…, les DEUX sondes 215c2caa… + 67e2014d…, LA TROISIÈME remise 0978c117… + l'ancre des ères 188a7d42…, SANS copie de bundle, le réceptacle m9f ré-armé, le réceptacle sonde ré-armé, l'index des livraisons), LE MIROIR 2/2 (le bundle courant 090-db00005 == 1f6b98ac… distant ET local, l'ancien 090-96d2b8d == 09ee7a1d… archivé versionné — 56 archives, rien supprimé). VERDICT : 17/17 PORTES VERTES — LES TROIS MIROIRS ALIGNÉS. L'état du programme lu au plan : le D160 accompli, le père au sommet de la grande œuvre — la suite appartient au développeur.

**Le geste du développeur (l'ouverture double).** Le message ouvre DEUX chantiers d'un seul geste : LE TEST GRANDEUR NATURE (coder une application ENTIÈREMENT avec Triade — la méthode à l'épreuve du réel, au-delà de l'outil de validation qui l'a fait naître) ET LE PROJET COFFRE-FORT EN PARALLÈLE (« ça n'empêchera pas de continuer le projet Coffre Fort en parallèle » — D135 amendée : le dégel). L'application n'est PAS nommée par le message : le choix est ARBITRÉ au geste (D171, les raisons et les rejets y vivent) et CONTREDISIBLE au message suivant — la couche I seule vit, rien n'est scellé, un contre-ordre rouvrirait le choix sans rien défaire.

**L'arbitrage : « Loupe », l'éditeur hexadécimal au panneau d'empreintes.** QUATRE raisons : (1) L'OUTIL DU QUOTIDIEN — toutes les pièces du projet vivent par leurs empreintes (md5/sha-256 consignées à chaque geste) ; l'application les rend À L'ŒIL ; (2) L'ÉPREUVE COMPLÈTE — cinq familles d'exigences en un artefact : l'interface (l'héritage démo win-*), les fichiers (lire et écrire AUX octets), le hachage (l'héritage de la famille sha tls13, PAR LA CARTE — R7), la libc (M1), la recherche et l'édition — aucune capacité ne reste à l'état de démonstration ; (3) LE PÉRIMÈTRE TENABLE — 18 blocs, un jalon (M10), livrable en kit terrain au développeur (modèle m9f) ; un fichier de 2 Gio s'ouvre (jamais tout en mémoire, les empreintes par fenêtres glissantes) ; (4) LE NEUF — pas un recodage : une application qui n'existe nulle part ailleurs, née de sa couche I.

**La fondation du domaine `loupe`.** loupe/I/README.md — la charte écrite-avant-code (R2) : la promesse MESURABLE et TRIPLE (structurelle : chaque bloc porté par sa spécification AVANT ses octets, les adresses déclarées AVANT la notation, les héritages byte-identiques — R7 ; observable au labo : les vecteurs officiels octet pour octet [FIPS 180-4], l'écran attendu octet par octet, la falsification attrapée ; observable chez le développeur : le kit s'ouvre d'un double-clic sur SA machine, charge SES fichiers, rend leurs empreintes recoupées, et rend son témoin au réceptacle du coffre /test). LE TABLEAU DES 18 BLOCS EN CINQ FAMILLES : fichier (loupe-01..04 : ouvrir, lire, fermer, le cadre de session), empreintes (loupe-05..07 : sha-256, md5, le cumul du fichier entier par fenêtres), rendu (loupe-08..11 : la ligne, l'écran, la peinture, le défilement), navigation (loupe-12..14 : l'aller-à, la recherche, le suivant), édition (loupe-15..18 : le curseur, la saisie, la sauvegarde, la sortie propre). Les conventions transverses : l'oracle à scénarios + le harnais différentiel, les budgets déclarés avant la notation (D161), le kit terrain modèle m9f, la balise `loupe 0.1.0-dev.1` au premier build (UN PROJET DE DÉVELOPPEMENT au sens du coffre — D137), les frontières. LA DETTE DE CÉRÉMONIE NOMMÉE À LA NAISSANCE (le modèle D166) : le 14e arbre (loupe) et l'extension du registre figé (m0/I/README.md § 2.1) attendent LA CÉRÉMONIE D'ÈRE du TGN — le geste hors-ligne du développeur, la re-signature de m0 au registre étendu (le modèle de l'ère M8) ; le garde demeure à 13 arbres VERTS jusqu'alors, AUCUN arbre signé n'est touché au geste.

**Le dégel du projet fils COFFRE-FORT (D135 amendée).** Le message du développeur cesse le développement différé : le fils vit EN PARALLÈLE du TGN (le père), chacun son rythme, AUCUN ne bloque l'autre. La frontière fondatrice demeure INTACTE : aucun code TRIADE forké, aucune dépendance vivante entre les dépôts (toute dépendance serait un défaut à consigner). Le premier geste du fils viendra à son message propre — le plan détaillé vit au FILS (docs/PLAN_MILESTONES.md du dépôt coffre-fort), la fondation demeure D135 / Entrée 123.

**Détail.** FRONTIÈRES : le proxy 1.0.0 INTACT (l'ère refermée D170 — le TGN n'y touche pas : le domaine loupe vit sa vie) ; la carte tls13 1.0.0 demeurée (l'anti-rollback armé : reconstruction interdite) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment, AUCUN arbre scellé touchés ; le sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87). Livrables : loupe/I/README.md (la charte + le tableau des 18 blocs + les conventions), scripts/consigner_tgn_d171.py, scripts/verifier_coherence_git_drive_r4.py [labo, le geste de reprise] ; consignations : la présente Entrée PAR SCRIPT, D171 PAR SCRIPT (docs/DECISIONS.md), PLAN (la section Programme TGN + la phrase de l'État du programme + le dégel au projet fils), worklog +Task ID 112. SUITE : M10-(a) LES DIX-HUIT SPÉCIFICATIONS POSÉES (loupe-01..18, la couche I complète — R2 : la cérémonie de l'ère précède tout build) ; la cérémonie d'ère du TGN attend son geste (le 14e arbre) ; le projet fils attend son premier geste à son message propre.

"""

# --- la Task ID 112 (append au worklog) ----------------------------------------------

TASK_112 = """
## Task ID 112 — LE TEST GRANDEUR NATURE OUVERT : L'APPLICATION « LOUPE » ARBITRÉE (l'éditeur hexadécimal natif au panneau d'empreintes), LE DOMAINE loupe FONDÉ ; LE PROJET COFFRE-FORT DÉGELÉ EN PARALLÈLE ; LA COHÉRENCE RE-VÉRIFIÉE À LA POINTE (R4 17/17) (07/11)

- La reprise (l'ouverture de session) : la cohérence git ↔ Drive re-vérifiée
  à la pointe 011ba3c — verifier_coherence_git_drive_r4.py [labo] : GIT 5/5
  (HEAD == origin relu EN DIRECT par ls-remote), LE COFFRE /test 10/10 (la
  racine 19 entrées, le kit RÉPARÉ, les DEUX sondes, LA TROISIÈME remise +
  l'ancre, le run 7 archivé AVEC ses SIX pièces + LE VERDICT, SANS copie de
  bundle), LE MIROIR 2/2 (090-db00005 == 1f6b98ac… distant ET local ;
  56 archives, rien supprimé) — 17/17 PORTES VERTES, LES TROIS MIROIRS
  ALIGNÉS.
- Le message du développeur ouvre DEUX chantiers d'un seul geste : LE TEST
  GRANDEUR NATURE (coder une application ENTIÈREMENT avec Triade) ET LE
  PROJET COFFRE-FORT EN PARALLÈLE (« ça n'empêchera pas de continuer le
  projet Coffre Fort en parallèle » — D135 amendée : le dégel).
- L'ARBITRAGE (D171) : « Loupe » — l'éditeur hexadécimal natif au panneau
  d'empreintes. L'outil du quotidien du projet (toutes ses pièces vivent
  par leurs empreintes), l'épreuve complète de la méthode (GUI + fichiers +
  hachage + libc + recherche + édition), le périmètre tenable (18 blocs, un
  jalon, un kit terrain), LE NEUF (le modèle RoomEq s'arrêtait au recodage
  — le TGN exige la création). CONTREDISIBLE au message suivant (la couche
  I seule vit, rien n'est scellé).
- LA FONDATION du domaine `loupe` : loupe/I/README.md — la charte (R2) +
  LE TABLEAU DES 18 BLOCS EN CINQ FAMILLES (fichier 01-04 · empreintes
  05-07 · rendu 08-11 · navigation 12-14 · édition 15-18) + les
  conventions transverses (l'oracle à scénarios + le harnais
  différentiel, les budgets déclarés avant la notation — D161, le kit
  terrain modèle m9f, la balise loupe 0.1.0-dev.1 au premier build, les
  frontières).
- LA DETTE DE CÉRÉMONIE NOMMÉE À LA NAISSANCE (le modèle D166) : le 14e
  arbre (loupe) + l'extension du registre figé (m0/I § 2.1) attendent LA
  CÉRÉMONIE D'ÈRE du TGN (le geste hors-ligne du développeur, la
  re-signature de m0 au registre étendu — le modèle de l'ère M8) ; le
  garde demeure à 13 arbres VERTS, AUCUN arbre signé touché.
- LE DÉGEL DU FILS : Coffre-Fort vit en parallèle du TGN, chacun son
  rythme, sans dépendance vivante (D135 tenue : aucun code forké) ; le
  premier geste du fils viendra à son message propre.
- FRONTIÈRES : le proxy 1.0.0 INTACT ; la carte tls13 1.0.0 demeurée
  (l'anti-rollback armé) ; AUCUNE clé, AUCUN coffre réel, AUCUN fragment
  touchés ; le sceau I : 13 arbres VERTS (cle deposee reelle) vérifié
  AVANT consignation. Livrables : loupe/I/README.md,
  scripts/consigner_tgn_d171.py, scripts/verifier_coherence_git_drive_r4.py
  [labo]. Consignations : l'Entrée 194 PAR SCRIPT, la D171 PAR SCRIPT, le
  PLAN (la section TGN + l'État + le dégel), la présente Task ID 112.
- SUITE : M10-(a) LES DIX-HUIT SPÉCIFICATIONS POSÉES (la couche I complète,
  R2) ; la cérémonie d'ère du TGN (le 14e arbre) attend son geste ; le
  projet fils attend son premier geste à son message propre.
"""


def main():
    # 0. le garde AVANT consignation (la discipline du projet)
    import subprocess
    r = subprocess.run(["python3", str(REPO / "v06" / "sceau_I.py"),
                        "verifier"], capture_output=True, text=True)
    if "13 arbres VERTS" not in r.stdout:
        sys.exit("ÉCHEC : le garde sceau I ne constate pas 13 arbres VERTS "
                 f"— consignation REFUSÉE\n{r.stdout[-400:]}")
    print("GARDE : 13 arbres VERTS (cle deposee reelle) — la consignation peut suivre")

    # 1. le plan : la section TGN + l'État + le dégel (idempotent)
    plan = PLAN.read_text(encoding="utf-8")
    if "## Programme TGN — le test grandeur nature" in plan:
        print("PLAN : le programme TGN déjà consigné — constaté")
    else:
        if plan.count("## Le projet fils COFFRE-FORT") != 1:
            sys.exit(f"ÉCHEC : l'ancre du projet fils trouvée "
                     f"{plan.count('## Le projet fils COFFRE-FORT')} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        if plan.count(FIN_FILS) != 1:
            sys.exit(f"ÉCHEC : l'ancre fin du fils trouvée "
                     f"{plan.count(FIN_FILS)} fois (attendu : 1)")
        plan = plan.replace("## Le projet fils COFFRE-FORT",
                            SECTION_TGN + "## Le projet fils COFFRE-FORT", 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        plan = plan.replace(FIN_FILS, FIN_FILS + DEGEL, 1)
        if "## Programme TGN — le test grandeur nature (ouvert le 07/11/2026, D171)" not in plan:
            sys.exit("ÉCHEC : la section TGN absente après remplacement")
        if "LE TEST GRANDEUR NATURE OUVERT le 07/11/2026" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du TGN")
        if "**LE DÉGEL (07/11/2026, D171).**" not in plan:
            sys.exit("ÉCHEC : le dégel absent du projet fils")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la section TGN + l'État du programme + le dégel — consignés")

    # 2. le journal : l'Entrée 194 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 194 —" in journal:
        print("JOURNAL : l'Entrée 194 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_194 + marqueur, 1)
        if "## Entrée 194 — « on peut commencer le test grandeur nature" not in journal:
            sys.exit("ÉCHEC : l'Entrée 194 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 194 consignée AVANT le marqueur m5a")

    # 3. le registre des décisions : la D171 à la suite de D170
    decisions = DECISIONS.read_text(encoding="utf-8")
    if "## D171 —" in decisions:
        print("DECISIONS : la D171 déjà consignée — constaté")
    else:
        if decisions.count("## D170 —") != 1:
            sys.exit("ÉCHEC : la D170 absente ou multiple (le geste précédent "
                     "n'est pas consigné)")
        decisions = decisions.rstrip("\n") + "\n" + D171.strip("\n") + "\n"
        if "## D171 — LE TEST GRANDEUR NATURE OUVERT" not in decisions:
            sys.exit("ÉCHEC : la D171 absente après append")
        DECISIONS.write_text(decisions, encoding="utf-8")
        print("DECISIONS : la D171 consignée À LA SUITE de la D170")

    # 4. le worklog racine : la Task ID 112 à la suite de la 111
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 112 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 112 existe déjà (rejeu REFUSÉ)")
    if worklog.count("## Task ID 111 —") != 1:
        sys.exit("ÉCHEC : l'entrée Task ID 111 absente ou multiple (le geste "
                 "précédent n'est pas consigné)")
    if not worklog.rstrip().endswith("(D160) ACCOMPLI."):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 111 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_112
    if "## Task ID 112 — LE TEST GRANDEUR NATURE OUVERT" not in worklog:
        sys.exit("ÉCHEC : la Task ID 112 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 112 consignée À LA SUITE de la Task 111")


if __name__ == "__main__":
    main()
