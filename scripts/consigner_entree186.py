#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree186.py — LA CONSIGNATION DU GESTE « LA RE-CÉRÉMONIE DE
LA RÉVISION 2 ARMÉE : LA REMISE RÉGÉNÉRÉE (m8 3e778fa0…, UNE seule
empreinte nouvelle), LA MAIN DU DÉVELOPPEUR SERVIE (LISEZMOI-ceremonie-
revision2-sys05.txt au kit), LA SYNCHRO GIT ↔ DRIVE RE-VÉRIFIÉE AU POINT
M9F AVANT LE GESTE (43/43 VERTS) » : la rangée (f) du plan reçoit le
constat de l'armement, l'État du programme reçoit la phrase du geste, le
worklog reçoit l'Entrée 186 + la Task ID 104. Rejeu REFUSÉ ; tout ancrage
absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est écrit."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

# --- la rangée (f) : le constat de L'ARMEMENT, avant la colonne du
# critère -----------------------------------------------------------------------

ANCIEN_RANGEE = ("le run du développeur, LA FINALE 1.0.0]** | run terrain "
                 "VERT sur pièces")

NOUVELLE_RANGEE = (
    "le run du développeur, LA FINALE 1.0.0]** ; **LA RE-CÉRÉMONIE ARMÉE "
    "le 07/11 au soir (Entrée 186, Task 104) : LA REMISE RÉGÉNÉRÉE pour "
    "la révision 2 [sceau_I.py preparer : a-signer.txt porte les TREIZE "
    "arbres à l'état vivant, UNE seule empreinte nouvelle — m8 sys.1 "
    "3e778fa0…, l'ancienne 72aadd38… remplacée ; les DOUZE autres lignes "
    "byte-identiques ; la balise demeure sys.1 — le précédent M9-(d) "
    "tenu : l'empreinte porte le changement, la balise nomme la lignée], "
    "le garde relit m8 CODE 10 « signature requise » [LE SIGNAL, pas la "
    "panne — construire() suit le garde VERT], LA MAIN DU DÉVELOPPEUR "
    "SERVIE [LISEZMOI-ceremonie-revision2-sys05.txt au kit + le NOTE_D130 "
    "du manifeste réécrit ; la règle d'or : JAMAIS « generer », la clé "
    "du 04/11 réutilisée 173fae9c…] ; la synchro git ↔ Drive re-vérifiée "
    "au point m9f AVANT le geste [verify_sync_m9f.py : 43/43 VERTS — les "
    "TROIS MIROIRS alignés au 15b7de7, le kit « Cérémonie » 58/58 == "
    "MANIFESTE == l'arbre local, les DEUX kits du /test INTACTS] ; LE "
    "GESTE ATTENDU : la signature hors-ligne de la remise → "
    "signatures-I.txt + cle-publique-I.txt au /test — puis deposer, le "
    "garde 13/13, LE REBUILD 1.0.0-dev.3, LE KIT M9F RÉPARÉ, le run — "
    "ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9]** | run terrain "
    "VERT sur pièces")

# --- l'État du programme : la phrase du geste remplace l'attente ----------------

ANCIEN_ETAT = ("— LE GESTE SUIVANT : LE REBUILD 1.0.0-dev.3 [le bloc "
               "sys-05 réparé, les portes de l'assemblage re-passées], LE "
               "KIT M9F RÉPARÉ livré au /test — puis le run du "
               "développeur, ET SI LE VERT TIENT : LA FINALE 1.0.0, LE "
               "JALON M9 — LA GRANDE ŒUVRE**")

NOUVEL_ETAT = (
    "— **LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE le 07/11 au soir (Entrée "
    "186, Task 104)** : la synchro git ↔ Drive re-vérifiée au point m9f "
    "d'abord [verify_sync_m9f.py : 43/43 VERTS — les TROIS MIROIRS "
    "alignés au 15b7de7, le kit « Cérémonie » 58/58 == MANIFESTE == "
    "l'arbre local, les DEUX kits du /test INTACTS, origin == 9413fd2 la "
    "pointe du geste sonde] ; le garde relit : m8 CODE 10 « signature "
    "requise » [LE SIGNAL — la révision 2 a fait évoluer l'arbre m8, les "
    "DOUZE autres arbres verts] ; LA REMISE RÉGÉNÉRÉE [preparer : les "
    "TREIZE arbres à l'état vivant, UNE seule empreinte nouvelle — m8 "
    "sys.1 3e778fa0…, l'ancienne 72aadd38… remplacée ; les DOUZE autres "
    "lignes byte-identiques ; la balise demeure sys.1] ; LA MAIN DU "
    "DÉVELOPPEUR SERVIE [LISEZMOI-ceremonie-revision2-sys05.txt au kit + "
    "le NOTE_D130 du manifeste réécrit ; la règle d'or : JAMAIS "
    "« generer », la clé du 04/11 réutilisée 173fae9c…] — LE GESTE DU "
    "DÉVELOPPEUR ATTENDU : la signature hors-ligne de la remise → "
    "signatures-I.txt + cle-publique-I.txt au /test ; puis le dépôt : "
    "deposer → le garde 13/13 → LE REBUILD 1.0.0-dev.3 [le bloc sys-05 "
    "réparé, les portes de l'assemblage re-passées] → LE KIT M9F RÉPARÉ "
    "au /test → le run du développeur — ET SI LE VERT TIENT : LA FINALE "
    "1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

# --- le worklog : l'Entrée 186, AVANT la ligne m5a -------------------------------

ENTREE_186 = """## Entrée 186 — LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE : LA REMISE RÉGÉNÉRÉE (m8 3e778fa0…, UNE SEULE EMPREINTE NOUVELLE), LA MAIN DU DÉVELOPPEUR SERVIE ; LA SYNCHRO GIT ↔ DRIVE RE-VÉRIFIÉE AU POINT M9F AVANT LE GESTE (43/43 VERTS) — LE REBUILD 1.0.0-dev.3 ATTEND LA SIGNATURE HORS LIGNE (07/11 au soir)

**La reprise a vérifié le terrain avant d'armer.** verify_sync_m9f.py (LECTURE SEULE — D164 rejouée) : **43/43 VERTS**. Local : HEAD == 15b7de7 (la passation Task 103), l'arbre PROPRE, le worklog porte la dernière consignation Task 103 (aucune Task 104). Miroir Drive : le bundle courant triade-history-090-9413fd2 UNIQUE, archives-bundles/ 48 archives (l'ancien 090-46d3eee versionné, rien supprimé), /test sans copie de bundle. Les QUATORZE fichiers du geste sonde + de la passation au miroir : md5 MATCH (les DEUX scénarios réparés de l'erratum n° 8, la RÉVISION 2 de la spec sys-05, la notation corrigée, les cinq scripts du geste, worklog, JOURNAL, PLAN). /test : les DEUX kits INTACTS (kit-m9f.zip == l'ACQUITTÉ 90a1d022…, kit-sonde-sys05.zip == le livré 215c2caa…, == les copies locales), cle-publique-I.txt == 188a7d42… LA clé publique du kit, signatures-I.txt présent, les réceptacles ré-armés, le run de la sonde archivé (le trio + le VERDICT 31/31 == les copies locales), la racine 16 entrées. Kit « Cérémonie » (D130) : 58/58 empreintes du MANIFESTE == le dossier Drive == l'arbre local, octet pour octet — le kit au niveau du commit 15b7de7. GitHub : origin == 9413fd2 (la pointe du geste sonde — le commit de passation 15b7de7 EMBARQUÉ au geste présent, le flux établi). Le jeton OAuth relais vivant. **LES TROIS MIROIRS ALIGNÉS.**

**Le garde a dit le signal.** sceau_I.py verifier : m8 CODE 10 — fichier modifié : sys-05-emission.md (empreinte vivante 3e778fa0e7ff4a7e…), les DOUZE autres arbres VERTS. C'est LE SIGNAL attendu — la révision 2 (Entrée 185) a fait évolué l'arbre d'intention m8 — PAS une panne : construire() suit le garde VERT, le rebuild 1.0.0-dev.3 (le bloc sys-05 réparé) ne peut pas naître tant que la re-signature n'est pas déposée. La remise du kit portait encore l'empreinte ancienne (72aadd38…, signée à la cérémonie du build 1.0.0 du 06/11) : si le développeur l'avait signée, le garde serait DEMEURÉ rouge — la régénération précède la cérémonie, toujours.

**La remise régénérée.** sceau_I.py preparer JOUÉ : a-signer.txt porte les TREIZE arbres à l'état vivant — UNE SEULE empreinte nouvelle : m8 sys.1 3e778fa0e7ff4a7ef7557820933cb3a2b66dca0dcba31e26c45bccddf51c83ab (l'ancienne 72aadd38… remplacée) ; les DOUZE autres lignes BYTE-IDENTIQUES (diff contrôlé : une ligne, une seule). La balise demeure sys.1 — le précédent tenu : la révision M9-(d) avait déjà fait évoluer l'arbre m8 (README révisé + TROIS specs nouvelles sys-04..06) sans bouger la balise ; l'empreinte porte le changement, la balise nomme la lignée de l'artefact. Comme Ed25519 est déterministe, re-signer les douze arbres inchangés rendra exactement les signatures déjà déposées — la preuve de D163 rejointe une troisième fois.

**La main du développeur servie.** LISEZMOI-ceremonie-revision2-sys05.txt ÉCRIT au kit : POURQUOI (la mesure de la sonde — 0xC0000005, la pose du WSABUF lue dans l'artefact scellé à sys-05+0x46 — et la révision 2 qui s'ensuit) ; CE QUI A CHANGÉ (UN fichier de l'arbre m8, sys-05-emission.md seul — Q3 le WSABUF canonique 16 o, I2 : 40 o, la note de révision ; l'empreinte à attendre sur la ligne m8 : 3e778fa0…) ; LA RÈGLE D'OR (JAMAIS « generer », la clé du 04/11 réutilisée — 173fae9c…) ; LES CINQ PAS (signer hors ligne → vérifier → ramener signatures-I.txt + cle-publique-I.txt au /test) ; CE QUE CELA DÉBLOQUE (deposer → le garde 13/13 → LE REBUILD 1.0.0-dev.3 → LE KIT M9F RÉPARÉ au /test → le run → ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9). Le LISEZMOI AJOUTÉ à RACINE_KIT (maj_kit.py) : déployé et listé au MANIFESTE au commit même. Le NOTE_D130 (le manifeste du kit) RÉÉCRIT : il nommait encore la cérémonie du build Task 95 (soldée le 06/11) — il nomme désormais la re-cérémonie de la révision 2, la remise à signer et la chaîne que la signature débloque.

**Frontières.** L'artefact INTACT (d8928934… — le rebuild attend la signature, jamais une reconstruction tacite), le scellé 0.9.0 INTACT, les manifestes et signatures DÉPOSÉS INCHANGÉS (le dépôt ne bouge qu'à deposer — l'atomicité de cérémonie : tout est vérifié AVANT toute écriture), AUCUNE balise posée (D104), la clé privée jamais traversée (D87) — le labo ne signera JAMAIS à la place du développeur (la clé de TEST déclasserait l'état « réelle » : une régression de preuve, refusée). Consignations : la présente Entrée 186 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 104. SUITE : LE GESTE DU DÉVELOPPEUR — la signature hors-ligne de la remise (signatures-I.txt + cle-publique-I.txt au /test) ; puis le dépôt : deposer, le garde 13/13, LE REBUILD 1.0.0-dev.3 (le bloc sys-05 réparé, les portes de l'assemblage re-passées), LE KIT M9F RÉPARÉ livré au /test, le run du développeur — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.

"""

# --- le worklog racine : la Task ID 104, À LA SUITE (append) ---------------------

TASK_104 = """
## Task ID 104 — LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE : LA REMISE RÉGÉNÉRÉE (m8 3e778fa0…, UNE SEULE EMPREINTE NOUVELLE — LES DOUZE AUTRES LIGNES BYTE-IDENTIQUES), LA MAIN DU DÉVELOPPEUR SERVIE (LISEZMOI-ceremonie-revision2-sys05.txt AU KIT + LE NOTE_D130 RÉÉCRIT) ; LA SYNCHRO GIT ↔ DRIVE RE-VÉRIFIÉE AU POINT M9F AVANT LE GESTE (verify_sync_m9f.py : 43/43 VERTS) — LE REBUILD 1.0.0-dev.3 ATTEND LA SIGNATURE HORS LIGNE (07/11 au soir)

Work Log:
- LA REPRISE A VÉRIFIÉ LE TERRAIN AVANT D'ARMER (verify_sync_m9f.py,
  lecture seule — D164 rejouée) : 43/43 VERTS — HEAD == 15b7de7 (la
  passation Task 103), l'arbre propre, la dernière consignation == Task
  103 ; le bundle courant 090-9413fd2 UNIQUE au miroir, 48 archives
  (rien supprimé), /test sans copie de bundle ; les QUATORZE fichiers
  du geste sonde + de la passation au miroir (md5 MATCH) ; les DEUX
  kits du /test INTACTS (90a1d022… + 215c2caa… == les copies locales),
  les matériaux de signature (cle-publique-I == 188a7d42… LA clé
  publique du kit, signatures-I présent), les réceptacles ré-armés, le
  run de la sonde archivé (le trio + le VERDICT 31/31 == les copies
  locales), la racine 16 entrées ; le kit « Cérémonie » re-vérifié
  (58/58 == MANIFESTE == l'arbre local, octet pour octet) ; origin
  GitHub == 9413fd2 (la pointe du geste sonde — le commit de passation
  15b7de7 EMBARQUÉ au geste présent, flux établi) ; le jeton OAuth
  vivant — LES TROIS MIROIRS ALIGNÉS.
- LE GARDE A DIT LE SIGNAL : sceau_I.py verifier — m8 CODE 10,
  fichier modifié : sys-05-emission.md (empreinte vivante
  3e778fa0e7ff4a7e…), les DOUZE autres arbres VERTS. LE SIGNAL attendu
  (la révision 2 a fait évoluer l'arbre m8), PAS la panne :
  construire() suit le garde VERT — le rebuild 1.0.0-dev.3 attend la
  re-signature ; la remise du kit portait ENCORE l'empreinte ancienne
  (72aadd38…, signée à la cérémonie du build du 06/11) : la
  régénération précède la cérémonie.
- LA REMISE RÉGÉNÉRÉE (sceau_I.py preparer) : a-signer.txt porte les
  TREIZE arbres à l'état vivant — UNE SEULE empreinte nouvelle : m8
  sys.1 3e778fa0e7ff4a7ef7557820933cb3a2b66dca0dcba31e26c45bccddf51c83ab
  (l'ancienne 72aadd38… remplacée) ; les DOUZE autres lignes
  BYTE-IDENTIQUES (diff contrôlé : une ligne, une seule) ; la balise
  demeure sys.1 (le précédent M9-(d) tenu : l'empreinte porte le
  changement, la balise nomme la lignée de l'artefact) ; Ed25519
  déterministe — les douze re-signatures rendront les signatures
  déposées (la preuve de D163 rejointe).
- LA MAIN DU DÉVELOPPEUR SERVIE : LISEZMOI-ceremonie-revision2-sys05
  .txt ÉCRIT au kit (POURQUOI : la mesure 0xC0000005 + la révision 2 ;
  CE QUI A CHANGÉ : sys-05-emission.md SEUL, l'empreinte à attendre
  3e778fa0… ; LA RÈGLE D'OR : JAMAIS « generer », la clé du 04/11
  réutilisée 173fae9c… ; LES CINQ PAS ; ce que cela débloque) ; le
  LISEZMOI AJOUTÉ à RACINE_KIT (maj_kit.py : déployé + listé au
  MANIFESTE au commit même) ; le NOTE_D130 RÉÉCRIT (il nommait encore
  la cérémonie du build Task 95, soldée le 06/11 — il nomme désormais
  la re-cérémonie de la révision 2).
- FRONTIÈRES : l'artefact INTACT (d8928934…), le scellé 0.9.0 INTACT,
  les manifestes et signatures DÉPOSÉS INCHANGÉS (le dépôt ne bouge
  qu'à deposer — l'atomicité de cérémonie), la clé privée jamais
  traversée (D87), le labo ne signera JAMAIS à la place du développeur.
  SUITE : LE GESTE DU DÉVELOPPEUR (la signature hors-ligne →
  signatures-I.txt + cle-publique-I.txt au /test) — puis deposer, le
  garde 13/13, LE REBUILD 1.0.0-dev.3, LE KIT M9F RÉPARÉ au /test, le
  run — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE
  ŒUVRE.
"""


def main():
    # 1. le plan : la rangée (f) + l'État
    plan = PLAN.read_text(encoding="utf-8")
    if "LA RE-CÉRÉMONIE ARMÉE le 07/11 au soir (Entrée 186" in plan:
        sys.exit("ÉCHEC : la rangée (f) est déjà à jour (rejeu REFUSÉ)")
    if plan.count(ANCIEN_RANGEE) != 1:
        sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                 f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
    if plan.count(ANCIEN_ETAT) != 1:
        sys.exit(f"ÉCHEC : ancrage État trouvé "
                 f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
    plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
    plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
    if "LA RE-CÉRÉMONIE ARMÉE le 07/11 au soir (Entrée 186, Task 104)" not in plan:
        sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat de "
                 "l'armement après remplacement")
    if "LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE le 07/11 au soir" not in plan:
        sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
    PLAN.write_text(plan, encoding="utf-8")
    print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 186 avant le marqueur m5a
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 186 —" in journal:
        sys.exit("ÉCHEC : l'Entrée 186 existe déjà (rejeu REFUSÉ)")
    marqueur = "<!-- m5a:journal-des-builds v1"
    if journal.count(marqueur) != 1:
        sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                 f"{journal.count(marqueur)} fois (attendu : 1)")
    journal = journal.replace(marqueur, ENTREE_186 + marqueur, 1)
    if "## Entrée 186 — LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE" not in journal:
        sys.exit("ÉCHEC : l'Entrée 186 absente après remplacement")
    JOURNAL.write_text(journal, encoding="utf-8")
    print("JOURNAL : l'Entrée 186 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 104 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 104 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 104 existe déjà (rejeu REFUSÉ)")
    if not worklog.rstrip().endswith("LE REBUILD\n  1.0.0-dev.3 EST LE GESTE SUIVANT."):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la passation "
                 "Task 103 attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_104
    if "## Task ID 104 — LA RE-CÉRÉMONIE DE LA RÉVISION 2 ARMÉE" not in worklog:
        sys.exit("ÉCHEC : la Task ID 104 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 104 consignée À LA SUITE de la Task 103")


if __name__ == "__main__":
    main()
