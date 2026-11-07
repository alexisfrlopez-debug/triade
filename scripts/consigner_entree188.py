#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree188.py — LA CONSIGNATION DU GESTE « LA SECONDE
SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE (« j'ai refait les signatures
et elles sont re-déposées dans le drive /test »), RECROPÉE 13/13 ET
INSTALLÉE — LE GARDE 13/13 VERTS ; LE REBUILD 1.0.0-dev.3 NÉ SUR
L'INSTRUMENT RÉVISÉ (LE DIFF CONTRÔLÉ : TROIS octets — la version R10 +
LES DEUX POSES DU WSABUF 0x64 → 0x68), LA CARTE GÉNÉRATION 11 ; LE KIT
M9F RÉPARÉ ASSEMBLÉ (md5 79d44284…) ET LIVRÉ AU COFFRE /test » : la
rangée (f) du plan reçoit le constat, l'État du programme reçoit la
phrase du geste, le worklog reçoit l'Entrée 188 + la Task ID 106.
Rejeu REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

# --- la rangée (f) : le constat du geste remplace l'attente -------------------------

ANCIEN_RANGEE = (
    "— LA SECOND SIGNATURE ATTENDUE : la remise étendue au /test → deposer → "
    "le garde 13/13 → LE REBUILD 1.0.0-dev.3 [les blocs sys-05 ET sys-06 "
    "réparés, les portes de l'assemblage re-passées sur l'instrument "
    "révisé] → LE KIT M9F RÉPARÉ au /test → le run — ET SI LE VERT "
    "TIENT : LA FINALE 1.0.0, LE JALON M9]**")

NOUVELLE_RANGEE = (
    "— **LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE, RECROPÉE 13/13 "
    "ET INSTALLÉE le 07/11/2026 au soir (Entrée 188, Task 106), PUIS LE "
    "REBUILD 1.0.0-dev.3 NÉ ET LE KIT M9F RÉPARÉ LIVRÉ** : le terrain "
    "vérifié AVANT le geste [le /test porte les DEUX pièces — "
    "signatures-I.txt md5 503f3822… NOUVEAU ≠ la première remise "
    "af382476… ≠ la build 62c43222…, cle-publique-I.txt == 188a7d42… "
    "l'ancre], la remise RAPATRIÉE [rapatrier_ceremonie_rev2_etendue.py : "
    "la remise PÉRIMÉE af382476… REFUSÉE NOMMÉE — re-déposer l'ancienne "
    "n'est pas re-signer] PUIS RECROPÉE SUR PIÈCES 13/13 [l'ancre de clé "
    "== 173fae9c… ; le format 13/13 ; LE RECOUP D163 REJOINT UNE "
    "QUATRIÈME FOIS : les DOUZE arbres inchangés == les signatures "
    "DÉPOSÉES == build 1.0.0 (Ed25519 déterministe) ; m8 RE-SIGNÉ ENCORE : "
    "la signature diverge de la déposée a7a787a0… (la première signature "
    "de la révision 2, contre 3e778fa0…) et vérifie Ed25519 contre "
    "l'empreinte vivante c444d730… ; LE DIFF CONTRÔLÉ vs la première "
    "remise : UNE ligne changée, LA m8, les DOUZE autres byte-identiques "
    "— le précédent M9-(d) tenu sur les signatures ; les empreintes "
    "vivantes == a-signer.txt 13/13], DEPOSER JOUÉ [l'atomicité de "
    "cérémonie : TOUT vérifié avant TOUTE écriture] ET LE GARDE "
    "REPASSÉ : **13/13 arbres VERTS** — m8 vert (c444d730…) : la dette de "
    "cérémonie de la révision 2 ÉTENDUE (sys-05 ET sys-06) EST SOLDÉE ; "
    "LE REBUILD 1.0.0-dev.3 [les portes de l'assemblage re-passées : "
    "BLOCS_SOCLE porte sys-05:R2 + sys-06:R2, la version R10 0x01000003, "
    "GENERATION 11 ; la chaîne rejouée : le garde 13/13 AVANT construire, "
    "l'héritage M3+M4+M5+M8 re-vérifié de bout en bout — le scellé 0.9.0 "
    "recomposé OCTET PAR OCTET (R7), le socle socket re-assemblé des "
    "notations réparées, l'oracle structurel, les 28 blocs tls13, le PE "
    "validé (AUCUN import nouveau, l'entrée 0x8C80 inchangée), les "
    "oracles différentiels M4+M5+LE HARNAIS RÉVISÉ 131 VERTS, la carte "
    "génération 11, le verrou croisé 86/86] : **l'artefact de23e577…** "
    "(65 024 o) ; LE DIFF CONTRÔLÉ dev.2 ↔ dev.3 : **TROIS octets sur "
    "65 024** — la version R10 @0x2820 (0x01000002 → 0x01000003) + LA "
    "POSE DU WSABUF dans sys-05 (@0xa58e) ET sys-06 (@0xa70e) : le disp8 "
    "0x64 → 0x68 — RIEN d'autre ne bouge, la pose canonique relue dans "
    "l'image (89 74 24 60 48 89 7c 24 68) aux DEUX blocs ; LE KIT M9F "
    "RÉPARÉ [scenario-m9f.py re-épinglé (SHA_PROXY de23e577…, le T0 "
    "porte LE CONTRÔLE erratum n° 9 : la pose relue dans l'image aux "
    "DEUX blocs), LISEZMOI-KIT-M9F.md réécrit (l'erratum n° 9 + la "
    "révision 2 étendue, LE CINQUIÈME RUN), l'assembleur re-passé : 28 "
    "constantes PAR AST + LE CONTRÔLE PERMANENT erratum n° 9 + les "
    "portes 6/7 + py_compile + extraction vierge — kit-m9f.zip md5 "
    "79d44284…] ET LIVRÉ AU COFFRE /test [corriger_kit_m9f_e9.py : le "
    "zip MIS À JOUR EN PLACE (l'ancien vit dans l'histoire git), le "
    "LISEZMOI + le réceptacle à jour, l'index des livraisons, la racine "
    "16 entrées, les PIÈCES DE CÉRÉMONIE demeurées (la seconde remise "
    "503f3822… + l'ancre 188a7d42…)] — LE CINQUIÈME RUN DU DÉVELOPPEUR "
    "EST ATTENDU (le premier du build réparé) — ET SI LE VERT TIENT : "
    "LA FINALE 1.0.0, LE JALON M9]**")

# --- l'État du programme : la phrase du geste remplace l'attente --------------------

ANCIEN_ETAT = (
    "LA SECONDE SIGNATURE ATTENDUE : la remise étendue (signatures-I.txt + "
    "cle-publique-I.txt au /test) ; puis le dépôt : deposer → le garde "
    "13/13 → LE REBUILD 1.0.0-dev.3 [les blocs sys-05 ET sys-06 réparés, "
    "les portes de l'assemblage re-passées sur l'instrument révisé] → LE "
    "KIT M9F RÉPARÉ au /test → le run du développeur — ET SI LE VERT "
    "TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

NOUVEL_ETAT = (
    "**LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE, RECROPÉE 13/13 "
    "ET INSTALLÉE le 07/11/2026 au soir (Entrée 188, Task 106) : le garde "
    "13/13 VERTS [l'ancre 173fae9c… tenue, les DOUZE arbres inchangés == "
    "les signatures déposées — la preuve de D163 rejointe une QUATRIÈME "
    "fois, m8 re-signé contre c444d730…, le diff vs la première remise : "
    "la ligne m8 seule] ; LE REBUILD 1.0.0-dev.3 NÉ SUR L'INSTRUMENT "
    "RÉVISÉ [les portes re-passées (sys-05:R2 + sys-06:R2), le scellé "
    "0.9.0 recomposé octet par octet (R7), le harnais révisé 131 VERTS, "
    "la carte génération 11, le verrou croisé 86/86 — l'artefact "
    "de23e577…, LE DIFF CONTRÔLÉ : TROIS octets sur 65 024 (la version "
    "R10 + LES DEUX POSES DU WSABUF 0x64 → 0x68), RIEN d'autre ne "
    "bouge] ; LE KIT M9F RÉPARÉ LIVRÉ AU /test [kit-m9f.zip md5 "
    "79d44284… mis à jour en place, le LISEZMOI et le réceptacle à jour "
    "(l'artefact dev.3, LE CINQUIÈME RUN), l'index des livraisons, les "
    "pièces de cérémonie demeurées]** — LE CINQUIÈME RUN DU DÉVELOPPEUR "
    "EST ATTENDU (le premier du build réparé : dézipper kit-m9f.zip dans "
    "un dossier NEUF D99, python scenario-m9f.py, renvoyer preuves-m9f/ "
    "ENTIER au coffre) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON "
    "M9 — LA GRANDE ŒUVRE**")

# --- le journal : l'Entrée 188, AVANT le marqueur m5a -------------------------------

ENTREE_188 = """## Entrée 188 — LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.3 NÉ SUR L'INSTRUMENT RÉVISÉ (LE DIFF CONTRÔLÉ : TROIS octets), LA CARTE GÉNÉRATION 11 ; LE KIT M9F RÉPARÉ LIVRÉ AU COFFRE (07/11 au soir)

**Le terrain a été vérifié avant de recevoir.** Le sondage du /test (lecture seule) : signatures-I.txt porte le md5 **503f3822…** — NOUVEAU, ≠ la première remise de la révision 2 (af382476…, contre 3e778fa0…, installée au geste précédent) et ≠ la remise du build (62c43222…) : la re-signature est CONSTATÉE ; cle-publique-I.txt == **188a7d42…** (l'ancre, inchangée). La racine demeure en ordre (16 entrées, les réceptacles armés, les archives en place).

**La remise recoupée sur pièces AVANT tout dépôt.** rapatrier_ceremonie_rev2_etendue.py (modèle D166 r.8, LECTURE SEULE sur v06/) : rapatriement des DEUX pièces vers download/ceremonie-revision2-etendue/ avec contrôle md5 APRÈS écriture (MATCH les métadonnées Drive) — et la remise PÉRIMÉE REFUSÉE NOMMÉE par avance (si le /test porte encore af382476… : re-déposer l'ancienne n'est pas re-signer) ; l'ANCRE DE CLÉ : la clé déposée == **173fae9c…** l'ancre des ères (la règle d'or tenue : JAMAIS « generer ») == l'ancre locale ; le format : 13/13 lignes valides ; **LE RECOUP D163 REJOINT UNE QUATRIÈME FOIS** : les DOUZE arbres inchangés portent les signatures BYTE-IDENTIQUES à celles DÉPOSÉES (== les signatures du build 1.0.0 : Ed25519 déterministe, la clé du 04/11 réutilisée) ; **m8 RE-SIGNÉ ENCORE** : la signature nouvelle DIVERGE de la déposée a7a787a0… (la première signature de la révision 2 — l'empreinte a bougé : 3e778fa0… → c444d730…) et VÉRIFIE Ed25519 contre l'empreinte vivante c444d73059af33ce… de la révision 2 étendue ; **LE DIFF CONTRÔLÉ vs la première remise** : UNE ligne changée, LA m8, les DOUZE autres byte-identiques — le précédent M9-(d) tenu sur les signatures comme sur la remise ; les empreintes vivantes des TREIZE arbres == a-signer.txt 13/13. **RECOUPE INTÉGRAL VERT — 13/13.**

**Le dépôt canonique et la garde.** sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt JOUÉ (l'atomicité de cérémonie : la remise entière vérifiée AVANT toute écriture — 13 signatures installées, les manifestes vivants, la clé réelle). Puis **verifier : 13/13 arbres VERTS** — m8 vert (c444d730…) : la dette de cérémonie de la révision 2 ÉTENDUE (sys-05 R2 + sys-06 R2) EST SOLDÉE. Le rebuild est DÉBLOQUÉ pour l'état signé.

**Le rebuild 1.0.0-dev.3, les portes re-passées.** La table BLOCS_SOCLE de la chaîne d'assemblage porte désormais les contrats révisés (sys-05:R2 + sys-06:R2 — la révision étendue à la SOURCE du build), la version R10 incrémentée (layout.py VERSION_DEV 0x01000003, carte_m9.py VERSION_DEV1 « 1.0.0-dev.3 », GENERATION 11) ; puis LA CHAÎNE REJOUÉE DE BOUT EN BOUT : le garde 13/13 AVANT construire() (le fail-closed D87), l'héritage M3+M4+M5+M8 re-vérifié (le scellé 0.9.0 recomposé OCTET PAR OCTET — R7, l'ancre 1492b0bc…), le socle socket re-assemblé DES NOTATIONS RÉPARÉES (la pose canonique 0x68), l'oracle structurel socle (la séquence fermée create→bind→connect, les fixtures .text6, la convention multiple-de-64), les 28 blocs tls13 + l'oracle (AUCUN IAT, LES SLOTS DISJOINTS), l'image composée, le PE validé (8 sections, AUCUN import nouveau, l'entrée 0x8C80 inchangée), la preuve R7, les oracles différentiels M4 + M5 + **LE HARNAIS RÉVISÉ (le noyau simulé lit buf à +8 : 131 contrôles · 131 VERTS)**, la carte GÉNÉRATION 11, le verrou croisé 86/86, le tableau de bord. **L'ARTEFACT : proxy.exe 1.0.0-dev.3, 65 024 o, sha256 de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be66b29226f.**

**Le diff contrôlé — l'évidence nommée.** diff_dev2_dev3.py (le dev.2 extrait du kit ACQUITTÉ 90a1d022… — la pièce des runs 3-4) : **TROIS octets divergents sur 65 024** — la version R10 @.rdata VA 0x2820 (0x02 → 0x03 : geste de BUILD, jamais scellage), LA POSE DU WSABUF dans sys-05 (@VA 0xa58e, le disp8 0x64 → 0x68) ET sys-06 (@VA 0xa70e, 0x64 → 0x68) ; TOUT le reste byte-identique — l'héritage R7 prouvé PAR L'ÉVIDENCE, la réparation NOMMÉE à l'octet. La pose canonique relue dans l'image aux DEUX blocs : `89 74 24 60 48 89 7c 24 68` @+0x46 (len à [rsp+0x60], buf à [rsp+0x68] — le WSABUF canonique SEIZE o).

**Le kit m9f réparé.** scenario-m9f.py re-épinglé (SHA_PROXY de23e577…, le docstring dev.3, la carte génération 11) et **LE T0 PORTE LA PREUVE** : la vérification `T0.erratum-9 : LA POSE DU WSABUF canonique relu` aux DEUX blocs — le kit embarque la preuve que CES octets sont les réparés (le miroir de l'octet 0x72 de l'erratum n° 5). LISEZMOI-KIT-M9F.md RÉÉCRIT : l'artefact dev.3 + LA SECTION « L'ERRATUM n° 9 + LA RÉVISION 2 ÉTENDUE » (les runs 3-4 morts à l'émission, LA MESURE de la sonde : 0xC0000005 × 3, LE COUPABLE NOMMÉ À L'INSTRUCTION — le WSABUF « packé », le noyau lit buf à +8 ; sys-06 LE MÊME défaut — la symétrie send/recv ; LA RÉPARATION selon la charte ; LA CÉRÉMONIE — l'ancre tenue, les douze inchangés ; LE REBUILD et le diff contrôlé TROIS octets) + les frontières à jour (le harnais révisé, la mesure SUR LE VRAI NOYAU) — **LE CINQUIÈME RUN est attendu, le premier du build réparé**. L'ASSEMBLEUR RE-PASSÉ : 28 constantes PAR AST (les deux constantes de pose comprises) + **LE CONTRÔLE PERMANENT ERRATUM n° 9** (la pose canonique relue DANS L'IMAGE aux DEUX blocs à l'assemblage — le STATUS_ACCESS_VIOLATION ne peut plus dormir) + les portes 6/7 + py_compile + l'épreuve d'extraction vierge — **kit-m9f.zip : 39 142 o, md5 79d44284…, sha256 1ced6ca0…**

**La livraison au coffre.** corriger_kit_m9f_e9.py (modèle e7 — D143 : jamais un jet) : kit-m9f.zip MIS À JOUR EN PLACE au /test (md5 79d44284… MATCH par relecture — le contenu remplacé, le fichier même conservé, l'ancien kit vit dans l'histoire git et demeure la pièce des archives des runs 3-4) ; LISEZMOI-m9f.txt mis à jour (l'erratum n° 9 consigné) ; preuves-m9f/LISEZMOI-preuves.txt mis à jour (l'artefact dev.3, la carte génération 11, LE CINQUIÈME RUN) — le réceptacle RÉ-ARMÉ (il ne porte que son LISEZMOI) ; l'index des livraisons porte la note de la révision 2 ; la vérification finale : la racine 16 entrées, le kit réparé recoupé, **LES PIÈCES DE CÉRÉMONIE DEMEURÉES** (signatures-I.txt 503f3822… la seconde remise installée + cle-publique-I.txt 188a7d42… l'ancre des ères).

**Frontières.** Le scellé 0.9.0 INTACT (recomposé octet par octet au build même — R7) ; l'artefact dev.2 (d8928934…) remplacé PAR LE DIFF CONTRÔLÉ (trois octets nommés — il demeure dans l'histoire git et dans les archives du coffre, la pièce des runs 3-4) ; AUCUNE balise posée (D104 : la finale 1.0.0 attend le vert du CINQUIÈME run — le scellage est un fait de carte) ; la clé privée jamais traversée (D87) — la seconde cérémonie est le geste du développeur, REÇU ET INSTALLÉ, jamais signé par le labo. Consignations : la présente Entrée 188 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 106. SUITE : LE CINQUIÈME RUN DU DÉVELOPPEUR — le premier du build réparé (dézipper kit-m9f.zip dans un dossier NEUF D99, python scenario-m9f.py ~10 s réseau vivant, renvoyer preuves-m9f/ ENTIER au coffre /test) ; le labo recoupe sur pièces (D138/D145/D148) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.

"""

# --- le worklog racine : la Task ID 106, À LA SUITE (append) ------------------------

TASK_106 = """
## Task ID 106 — LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE ET INSTALLÉE (LE GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.3 NÉ (LE DIFF CONTRÔLÉ : TROIS octets — la version R10 + LES DEUX POSES DU WSABUF), LA CARTE GÉNÉRATION 11 ; LE KIT M9F RÉPARÉ LIVRÉ AU /test — LE CINQUIÈME RUN ATTENDU (07/11 au soir)

Work Log:
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR (lecture seule) : signatures-I.txt
  md5 503f3822… NOUVEAU (≠ la première remise af382476… ≠ la build
  62c43222…), cle-publique-I.txt == 188a7d42… l'ancre ; la racine 16
  entrées.
- LA REMISE RECROPÉE SUR PIÈCES AVANT TOUT DÉPÔT
  (rapatrier_ceremonie_rev2_etendue.py — la remise PÉRIMÉE af382476…
  REFUSÉE NOMMÉE par avance) : rapatriement md5 MATCH ; l'ancre de clé
  == 173fae9c… ; le format 13/13 ; LE RECOUP D163 REJOINT UNE
  QUATRIÈME FOIS : les DOUZE arbres inchangés == les signatures
  DÉPOSÉES == build 1.0.0 (Ed25519 déterministe) ; m8 RE-SIGNÉ ENCORE :
  diverge de la déposée a7a787a0… (la première signature rév. 2),
  vérifie Ed25519 contre l'empreinte vivante c444d730… ; LE DIFF
  CONTRÔLÉ vs la première remise : UNE ligne changée, LA m8, les DOUZE
  autres byte-identiques ; les empreintes vivantes == a-signer.txt
  13/13 — RECOUPE INTÉGRAL VERT.
- LE DÉPÔT CANONIQUE (sceau_I.py deposer --cle : l'atomicité — tout
  vérifié avant toute écriture) ET LA GARDE REPASSÉE : **13/13 arbres
  VERTS** — m8 vert (c444d730…) : la dette de cérémonie de la
  révision 2 ÉTENDUE (sys-05 R2 + sys-06 R2) SOLDÉE.
- LE REBUILD 1.0.0-dev.3, LES PORTES RE-PASSÉES : BLOCS_SOCLE porte
  sys-05:R2 + sys-06:R2 (la révision à la source du build), la version
  R10 0x01000003, GENERATION 11 ; la chaîne rejouée : le garde 13/13
  AVANT construire, l'héritage M3+M4+M5+M8 re-vérifié (le scellé 0.9.0
  recomposé OCTET PAR OCTET — R7), le socle socket re-assemblé des
  notations réparées, l'oracle structurel, les 28 blocs tls13, le PE
  validé (AUCUN import nouveau, l'entrée 0x8C80 inchangée), les
  oracles M4+M5+LE HARNAIS RÉVISÉ 131 VERTS, la carte génération 11,
  le verrou croisé 86/86 — L'ARTEFACT : de23e577… (65 024 o).
- LE DIFF CONTRÔLÉ dev.2 ↔ dev.3 (diff_dev2_dev3.py, le dev.2 extrait
  du kit ACQUITTÉ) : **TROIS octets sur 65 024** — la version R10
  @0x2820 + LA POSE DU WSABUF dans sys-05 (@0xa58e) ET sys-06
  (@0xa70e) : 0x64 → 0x68 ; RIEN d'autre ne bouge ; la pose canonique
  relue dans l'image (89 74 24 60 48 89 7c 24 68) aux DEUX blocs
  @+0x46.
- LE KIT M9F RÉPARÉ : scenario-m9f.py re-épinglé (SHA_PROXY
  de23e577… ; LE T0 PORTE LA PREUVE : « T0.erratum-9 : LA POSE DU
  WSABUF canonique relu » aux DEUX blocs) ; LISEZMOI-KIT-M9F.md
  RÉÉCRIT (l'erratum n° 9 + la révision 2 étendue, LE CINQUIÈME RUN) ;
  l'assembleur re-passé : 28 constantes PAR AST + LE CONTRÔLE
  PERMANENT erratum n° 9 + les portes 6/7 + py_compile + extraction
  vierge — kit-m9f.zip md5 79d44284…, sha256 1ced6ca0…
- LA LIVRAISON AU COFFRE (corriger_kit_m9f_e9.py, modèle e7) :
  kit-m9f.zip MIS À JOUR EN PLACE (md5 79d44284… MATCH par relecture,
  l'ancien vit dans l'histoire git) ; LISEZMOI-m9f.txt à jour ;
  preuves-m9f/LISEZMOI-preuves.txt à jour (dev.3, génération 11, LE
  CINQUIÈME RUN), le réceptacle RÉ-ARMÉ ; l'index des livraisons ; la
  vérification finale (16 entrées, LES PIÈCES DE CÉRÉMONIE demeurées :
  la seconde remise 503f3822… + l'ancre 188a7d42…).
- FRONTIÈRES : le scellé 0.9.0 INTACT (R7 recomposé au build même),
  l'artefact dev.2 remplacé PAR LE DIFF CONTRÔLÉ (il demeure la pièce
  des archives des runs 3-4), aucune balise (D104), la clé privée
  jamais traversée (D87). SUITE : LE CINQUIÈME RUN DU DÉVELOPPEUR (le
  premier du build réparé : kit-m9f.zip → dossier NEUF D99, python
  scenario-m9f.py, preuves-m9f/ ENTIER au coffre) — ET SI LE VERT
  TIENT : LA FINALE 1.0.0, le jalon M9 — LA GRANDE ŒUVRE.
"""


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE" in plan:
        print("PLAN : la rangée (f) + l'État déjà consignés — constaté")
    else:
        if plan.count(ANCIEN_RANGEE) != 1:
            sys.exit(f"ÉCHEC : ancrage rangée (f) trouvé "
                     f"{plan.count(ANCIEN_RANGEE)} fois (attendu : 1)")
        if plan.count(ANCIEN_ETAT) != 1:
            sys.exit(f"ÉCHEC : ancrage État trouvé "
                     f"{plan.count(ANCIEN_ETAT)} fois (attendu : 1)")
        plan = plan.replace(ANCIEN_RANGEE, NOUVELLE_RANGEE, 1)
        plan = plan.replace(ANCIEN_ETAT, NOUVEL_ETAT, 1)
        if "LE REBUILD 1.0.0-dev.3 NÉ" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                     "après remplacement")
        if "LE CINQUIÈME RUN DU DÉVELOPPEUR" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 188 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 188 —" in journal:
        print("JOURNAL : l'Entrée 188 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_188 + marqueur, 1)
        if "## Entrée 188 — LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE" not in journal:
            sys.exit("ÉCHEC : l'Entrée 188 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 188 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 106 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 106 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 106 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 105 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 105 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = "ET SI LE VERT TIENT : LA FINALE 1.0.0, le jalon M9 —\n  LA GRANDE ŒUVRE."
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 105 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_106
    if "## Task ID 106 — LA SECONDE SIGNATURE DE LA RÉVISION 2 ÉTENDUE REÇUE" not in worklog:
        sys.exit("ÉCHEC : la Task ID 106 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 106 consignée À LA SUITE de la Task 105")


if __name__ == "__main__":
    main()
