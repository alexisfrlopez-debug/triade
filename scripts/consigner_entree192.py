#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree192.py — LA CONSIGNATION DU GESTE « LA TROISIÈME
SIGNATURE DE LA RÉVISION 3 REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE
GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.4 NÉ SUR LE TERRAIN (LE
DIFF CONTRÔLÉ : TROIS octets — la version R10 + LES DEUX IMMÉDIATES
DU CONTRAT D'APPEL dans sys-06), LA CARTE GÉNÉRATION 12 ; LE KIT M9F
RÉPARÉ LIVRÉ AU COFFRE /test — LE SEPTIÈME RUN ATTENDU » : la rangée
(f) du plan reçoit le constat, l'État du programme reçoit la phrase
du geste, le worklog reçoit l'Entrée 192 + la Task ID 110. Rejeu
REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois =
ÉCHEC NOMMÉ, rien n'est écrit. Les ancres RANGEE/ÉTAT sont importées
de consigner_entree191 (les constats du geste précédent — la chaîne
des remplacements tient sans retranscription)."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_entree191 as _c191  # noqa: E402  # la chaîne des gestes

# --- la rangée (f) : le constat du geste remplace l'attente -------------------------

ANCIEN_RANGEE = _c191.NOUVELLE_RANGEE   # le constat 191 (le mot d'information + la remise régénérée)

NOUVELLE_RANGEE = (
    " ; **LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE, RECROPÉE 13/13 "
    "ET INSTALLÉE le 07/11/2026 (Entrée 192, Task 110) : LE GARDE 13/13 "
    "VERTS** [rapatrier_ceremonie_revision3.py : la remise 0978c117… "
    "NOUVELLE (≠ la seconde 503f3822… REFUSÉE NOMMÉE par avance — "
    "re-déposer l'ancienne n'est pas re-signer), l'ancre de clé == "
    "173fae9c… l'ancre des ères (JAMAIS « generer »), le format 13/13, "
    "LE RECOUP D163 REJOINT UNE CINQUIÈME FOIS — les DOUZE arbres "
    "inchangés == les signatures déposées == build 1.0.0 (Ed25519 "
    "déterministe, la clé du 04/11 réutilisée), m8 RE-SIGNÉ : la "
    "signature diverge de la déposée et VÉRIFIE Ed25519 contre "
    "l'empreinte vivante e36141f7… ; LE DIFF CONTRÔLÉ vs la seconde "
    "remise : UNE ligne changée, LA m8, les DOUZE autres "
    "byte-identiques ; les empreintes vivantes == a-signer.txt 13/13 — "
    "RECOUPE INTÉGRAL VERT ; deposer : l'atomicité de cérémonie — tout "
    "vérifié avant toute écriture] ; **LE REBUILD 1.0.0-dev.4 NÉ SUR LE "
    "TERRAIN** [les portes re-passées : BLOCS_SOCLE porte sys-06:R3, la "
    "version R10 0x01000004, GENERATION 12 ; la chaîne rejouée : le "
    "garde 13/13 AVANT construire(), l'héritage M3+M4+M5+M8 re-vérifié "
    "(le scellé 0.9.0 recomposé OCTET PAR OCTET — R7), le socle socket "
    "re-assemblé de la notation réparée (AfdFlags = 0, TdiFlags = "
    "TDI_RECEIVE_NORMAL 0x20 — le QUATRIÈME champ porte le 0x20), les "
    "oracles M4+M5+LE HARNAIS SUIVI 131 VERTS (les DEUX mutantes du "
    "terrain — AfdFlags 0→0x20 rétablie, TdiFlags 0x20→0 vidée — "
    "TOUTES DEUX TRAHIES), la carte génération 12, le verrou croisé "
    "86/86 — L'ARTEFACT 446279f3… (65 024 o) ; LE DIFF CONTRÔLÉ "
    "dev.3 ↔ dev.4 : TROIS octets sur 65 024 — la version R10 @RVA "
    "0x2820 (0x03 → 0x04) + LES DEUX IMMÉDIATES du contrat d'appel "
    "dans sys-06 (@RVA 0xa725 : AfdFlags 0x20 → 0 ; @RVA 0xa730 : "
    "TdiFlags 0 → 0x20 — le disp32 nommé : 0x80 dépasse la portée "
    "disp8), RIEN d'autre ne bouge] ; **LE KIT M9F RÉPARÉ LIVRÉ AU "
    "COFFRE /test** [scenario-m9f.py re-épinglé (SHA_PROXY 446279f3…, "
    "génération 12) + LE T0 PORTE LA PREUVE (T0.erratum-10 : le "
    "contrat d'appel relu dans l'image au bloc sys-06 — les DEUX "
    "encodes), LISEZMOI-KIT-M9F.md réécrit (l'erratum n° 10 + la "
    "révision 3), l'assembleur re-passé : 32 constantes PAR AST + LE "
    "CONTRÔLE PERMANENT erratum n° 10 + les portes 6/7 + py_compile + "
    "extraction vierge — kit-m9f.zip md5 92098687… MIS À JOUR EN PLACE "
    "au /test (l'ancien vit dans l'histoire git), le LISEZMOI + le "
    "réceptacle preuves-m9f/ RÉ-ARMÉ + l'index des livraisons, la "
    "racine 19 entrées, LES PIÈCES DE CÉRÉMONIE demeurées (la "
    "TROISIÈME remise 0978c117… + l'ancre 188a7d42…)]** ; **LE "
    "SEPTIÈME RUN DU DÉVELOPPEUR ATTENDU (le premier du contrat "
    "réparé) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — "
    "LA GRANDE ŒUVRE**")

# --- l'État du programme : la phrase du geste remplace l'attente --------------------

ANCIEN_ETAT = _c191.NOUVEL_ETAT        # l'État 191 (le mot d'information + la remise régénérée)

NOUVEL_ETAT = (
    "**LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE (« signatures "
    "déposées dans le dossier /test du drive »), RECROPÉE 13/13 ET "
    "INSTALLÉE le 07/11/2026 (Entrée 192, Task 110) : LA DETTE DE "
    "CÉRÉMONIE DE LA RÉVISION 3 EST SOLDÉE — LE GARDE 13/13 VERTS** "
    "(l'ancre de clé 173fae9c… tenue — JAMAIS « generer » ; les DOUZE "
    "arbres inchangés byte-identiques aux déposées == build 1.0.0 — "
    "Ed25519 déterministe, le recoup D163 REJOINT UNE CINQUIÈME fois ; "
    "m8 RE-SIGNÉ contre l'empreinte vivante e36141f7… ; le diff "
    "contrôlé : la ligne m8 seule ; deposer : l'atomicité de "
    "cérémonie) ; **LE REBUILD 1.0.0-dev.4 NÉ SUR LE TERRAIN** : "
    "BLOCS_SOCLE porte sys-06:R3 (AfdFlags = 0, TdiFlags = "
    "TDI_RECEIVE_NORMAL 0x20), la version R10 0x01000004, GENERATION "
    "12 ; la chaîne entière rejouée (le garde 13/13 AVANT construire, "
    "le scellé 0.9.0 recomposé OCTET PAR OCTET — R7, le harnais suivi "
    "131 VERTS — les DEUX mutantes du terrain trahies, la carte "
    "génération 12, le verrou croisé 86/86) — **L'ARTEFACT 446279f3… "
    "(65 024 o)** ; LE DIFF CONTRÔLÉ dev.3 ↔ dev.4 : TROIS octets sur "
    "65 024 (la version R10 + LES DEUX IMMÉDIATES du contrat d'appel "
    "dans sys-06 : @RVA 0xa725 AfdFlags 0x20 → 0, @RVA 0xa730 "
    "TdiFlags 0 → 0x20 — le disp32 Nommé) ; **LE KIT M9F RÉPARÉ LIVRÉ "
    "AU COFFRE /test** (kit-m9f.zip md5 92098687… MIS À JOUR EN PLACE "
    "— l'assembleur re-passé : 32 constantes PAR AST + LE CONTRÔLE "
    "PERMANENT erratum n° 10 + extraction vierge ; le T0 du kit "
    "EMBARQUE LA PREUVE : le contrat d'appel relu dans l'image ; le "
    "LISEZMOI + le réceptacle preuves-m9f/ RÉ-ARMÉ + l'index, la "
    "racine 19 entrées, les pièces de cérémonie demeurées : la "
    "TROISIÈME remise 0978c117… + l'ancre 188a7d42…) ; le scellé 0.9.0 "
    "INTACT (R7), aucune balise (D104), la clé privée jamais traversée "
    "(D87) — **LE SEPTIÈME RUN DU DÉVELOPPEUR ATTENDU (le premier du "
    "contrat réparé : kit-m9f.zip au /test, un dossier NEUF D99, "
    "python scenario-m9f.py — réseau vivant — renvoyer preuves-m9f/ "
    "ENTIER au coffre) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE "
    "JALON M9 — LA GRANDE ŒUVRE**")

# --- le journal : l'Entrée 192, AVANT le marqueur m5a -------------------------------

ENTREE_192 = """## Entrée 192 — LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE, RECROPÉE 13/13 ET INSTALLÉE (LE GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.4 NÉ SUR LE TERRAIN (LE DIFF CONTRÔLÉ : TROIS octets — la version R10 + LES DEUX IMMÉDIATES DU CONTRAT D'APPEL dans sys-06), LA CARTE GÉNÉRATION 12 ; LE KIT M9F RÉPARÉ LIVRÉ AU COFFRE — LE SEPTIÈME RUN ATTENDU (07/11)

**Le terrain a été vérifié avant de recevoir.** Le sondage du /test (lecture seule) : signatures-I.txt porte le md5 **0978c117…** — NOUVEAU, ≠ la seconde remise de la révision 2 étendue (503f3822…, contre c444d730…, installée au geste 3dc3d3e) : la re-signature est CONSTATÉE ; cle-publique-I.txt == **188a7d42…** (l'ancre, inchangée). La racine demeure en ordre (19 entrées, les TROIS kits recoupés : 79d44284… + 215c2caa… + 67e2014d…, les réceptacles en place, les archives en place).

**La remise recoupée sur pièces AVANT tout dépôt.** rapatrier_ceremonie_revision3.py (modèle D166 r.8, LECTURE SEULE sur v06/) : rapatriement des DEUX pièces vers download/ceremonie-revision3/ avec contrôle md5 APRÈS écriture (MATCH les métadonnées Drive) — et la remise PÉRIMÉE REFUSÉE NOMMÉE par avance (si le /test porte encore 503f3822… : re-déposer l'ancienne n'est pas re-signer) ; l'ANCRE DE CLÉ : la clé déposée == **173fae9c…** l'ancre des ères (la règle d'or tenue : JAMAIS « generer ») == l'ancre locale ; le format : 13/13 lignes valides ; **LE RECOUP D163 REJOINT UNE CINQUIÈME FOIS** : les DOUZE arbres inchangés portent les signatures BYTE-IDENTIQUES à celles DÉPOSÉES (== les signatures du build 1.0.0 : Ed25519 déterministe, la clé du 04/11 réutilisée) ; **m8 RE-SIGNÉ ENCORE** : la signature nouvelle DIVERGE de la déposée (celle de la seconde remise, contre c444d730…) et VÉRIFIE Ed25519 contre l'empreinte vivante **e36141f75ebd8e615c53ff1bd59a4f4cee45b9397eefa66773ffbf54580b3536** de la révision 3 ; **LE DIFF CONTRÔLÉ vs la seconde remise** : UNE ligne changée, LA m8, les DOUZE autres byte-identiques ; les empreintes vivantes des TREIZE arbres == a-signer.txt 13/13. **RECOUPE INTÉGRAL VERT — 13/13.**

**Le dépôt canonique et la garde.** sceau_I.py deposer signatures-I.txt --cle cle-publique-I.txt JOUÉ (l'atomicité de cérémonie : la remise entière vérifiée AVANT toute écriture — 13 signatures installées, les manifestes vivants, la clé réelle : etat « reelle (ceremonie hors-ligne, D87) »). Puis **verifier : 13/13 arbres VERTS** — m8 vert (e36141f7…) : la dette de cérémonie de la révision 3 EST SOLDÉE. Le rebuild est DÉBLOQUÉ pour l'état signé.

**Le rebuild 1.0.0-dev.4, les portes re-passées.** La table BLOCS_SOCLE de la chaîne d'assemblage porte désormais le contrat révisé (sys-06:R3 seul — la révision 3 à la SOURCE du build : AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20, sys-05:R2 inchangé), la version R10 incrémentée (layout.py VERSION_DEV 0x01000004, carte_m9.py VERSION_DEV1 « 1.0.0-dev.4 », GENERATION 12) ; puis LA CHAÎNE REJOUÉE DE BOUT EN BOUT : le garde 13/13 AVANT construire() (le fail-closed D87), l'héritage M3+M4+M5+M8 re-vérifié (le scellé 0.9.0 recomposé OCTET PAR OCTET — R7, l'ancre 1492b0bc…), le socle socket re-assemblé DE LA NOTATION RÉPARÉE (le QUATRIÈME champ porte le 0x20, le TROISIÈME porte 0), l'oracle structurel socle, les 28 blocs tls13 + l'oracle, l'image composée, le PE validé, la preuve R7, les oracles différentiels M4 + M5 + **LE HARNAIS SUIVI (le noyau simulé AFD STRICT refuse le 0x20 en AfdFlags : 131 contrôles · 131 VERTS, empreinte b8373757… — dont LES DEUX NOUVELLES MUTANTES DU TERRAIN : « LE-TERRAIN-falsifié » [AfdFlags 0 → 0x20 : la mesure WinDbg rétablie] et « LE-TERRAIN-VIDÉ » [TdiFlags 0x20 → 0 : le placement perdu], TOUTES DEUX TRAHIES)**, la carte GÉNÉRATION 12, le verrou croisé 86/86, le tableau de bord. **L'ARTEFACT : proxy.exe 1.0.0-dev.4, 65 024 o, sha256 446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d.**

**Le diff contrôlé — l'évidence nommée.** diff_dev3_dev4.py (le dev.3 extrait du kit ACQUITTÉ 79d44284… — la pièce des runs 5-6 et de la sonde sys-06) : **TROIS octets divergents sur 65 024** — la version R10 @RVA 0x2820 (0x03 → 0x04 : geste de BUILD, jamais scellage), **LES DEUX IMMÉDIATES DU CONTRAT D'APPEL dans sys-06** : @RVA 0xa725 **AfdFlags 0x20 → 0** et @RVA 0xa730 **TdiFlags 0 → 0x20** ; TOUT le reste byte-identique — l'héritage R7 prouvé PAR L'ÉVIDENCE, la réparation NOMMÉE à l'octet. Le contrat réparé relu dans l'image aux DEUX sites : `c7 44 24 7c 00 00 00 00` (AfdFlags = 0, le TROISIÈME champ — encode disp8, 8 o) et `c7 84 24 80 00 00 00 20 00 00 00` (TdiFlags = TDI_RECEIVE_NORMAL 0x20, le QUATRIÈME champ — encode disp32, 11 o : **0x80 DÉPASSE la portée disp8, l'encode canonique nommé**).

**Le kit m9f réparé.** scenario-m9f.py re-épinglé (SHA_PROXY 446279f3…, le docstring dev.4, la carte génération 12) et **LE T0 PORTE LA PREUVE** : la vérification `T0.erratum-10 : LE CONTRAT D'APPEL relu dans sys-06` aux DEUX sites (AfdFlags = 0 en encode disp8 ; TdiFlags = 0x20 en encode disp32) — le kit embarque la preuve que CES octets sont les réparés (le miroir de l'octet 0x72 de l'erratum n° 5 et de la pose 0x68 de l'erratum n° 9). LISEZMOI-KIT-M9F.md RÉÉCRIT : l'artefact dev.4 + LA SECTION « L'ERRATUM n° 10 + LA RÉVISION 3 » (les runs 5-6 morts à la première lecture, LA MESURE de la sonde sys-06 : -6 STATUS_INVALID_PARAMETER ×3 DÉTERMINISTE, LE CHAMP NOMMÉ par l'A/B des notations — le VRAI afd.sys REFUSE le bit 0x20 dans AfdFlags ; l'erratum de lecture de la révision 2 RÉFUTÉ PAR LE TERRAIN ; LA RÉPARATION selon la charte ; LA CÉRÉMONIE — l'ancre tenue, les douze inchangés ; LE REBUILD et le diff contrôlé TROIS octets) + les frontières à jour (le harnais suivi : le noyau simulé REFUSE ce que le VRAI refuse). L'ASSEMBLEUR RE-PASSÉ : **32 constantes PAR AST** (les QUATRE nouvelles constantes du contrat d'appel comprises) + **LE CONTRÔLE PERMANENT ERRATUM n° 10** (le contrat relu DANS L'IMAGE au bloc sys-06 à l'assemblage — le INVALID_PARAMETER ne peut plus dormir) + les portes 6/7 + py_compile + l'épreuve d'extraction vierge — **kit-m9f.zip : 40 885 o, md5 92098687…, sha256 c0883c87…**

**La livraison au coffre.** corriger_kit_m9f_e10.py (modèle e9 — D143 : jamais un jet) : kit-m9f.zip MIS À JOUR EN PLACE au /test (md5 92098687… MATCH par relecture — le contenu remplacé, le fichier même conservé, l'ancien kit vit dans l'histoire git et demeure la pièce des archives des runs 5-6 et de la sonde sys-06) ; LISEZMOI-m9f.txt mis à jour (l'erratum n° 10 consigné, md5 41add303…) ; preuves-m9f/LISEZMOI-preuves.txt mis à jour (l'artefact dev.4, la carte génération 12, LE SEPTIÈME RUN attendu) — le réceptacle RÉ-ARMÉ (il ne porte que son LISEZMOI) ; l'index des livraisons porte la note de la révision 3 ; la vérification finale : la racine 19 entrées, le kit réparé recoupé, **LES PIÈCES DE CÉRÉMONIE DEMEURÉES** (signatures-I.txt 0978c117… la troisième remise INSTALLÉE + cle-publique-I.txt 188a7d42… l'ancre des ères).

**Frontières.** Le scellé 0.9.0 INTACT (recomposé octet par octet au build même — R7) ; l'artefact dev.3 (de23e577…) remplacé PAR LE DIFF CONTRÔLÉ (trois octets nommés — il demeure dans l'histoire git et dans les archives du coffre, la pièce des runs 5-6 et de la sonde sys-06) ; AUCUNE balise posée (D104 : la finale 1.0.0 attend le vert du SEPTIÈME run — le scellage est un fait de carte) ; la clé privée jamais traversée (D87) — la troisième cérémonie est le geste du développeur, REÇU ET INSTALLÉ, jamais signé par le labo. Consignations : la présente Entrée 192 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 110. SUITE : **LE SEPTIÈME RUN DU DÉVELOPPEUR — le premier du contrat réparé** (dézipper kit-m9f.zip dans un dossier NEUF D99, python scenario-m9f.py ~10 s réseau vivant, renvoyer preuves-m9f/ ENTIER au coffre /test) ; le labo recoupe sur pièces (D138/D145/D148) — **ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**.

"""

# --- le worklog racine : la Task ID 110, À LA SUITE (append) ------------------------

TASK_110 = """
## Task ID 110 — LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE ET INSTALLÉE (LE GARDE 13/13 VERTS) ; LE REBUILD 1.0.0-dev.4 NÉ (LE DIFF CONTRÔLÉ : TROIS octets — la version R10 + LES DEUX IMMÉDIATES DU CONTRAT D'APPEL dans sys-06), LA CARTE GÉNÉRATION 12 ; LE KIT M9F RÉPARÉ LIVRÉ AU /test — LE SEPTIÈME RUN ATTENDU (07/11)

Work Log:
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR (lecture seule) : signatures-I.txt
  md5 0978c117… NOUVEAU (≠ la seconde remise 503f3822… ≠ la build
  62c43222…), cle-publique-I.txt == 188a7d42… l'ancre ; la racine 19
  entrées, les TROIS kits recoupés.
- LA REMISE RECROPÉE SUR PIÈCES AVANT TOUT DÉPÔT
  (rapatrier_ceremonie_revision3.py — la remise PÉRIMÉE 503f3822…
  REFUSÉE NOMMÉE par avance) : rapatriement md5 MATCH ; l'ancre de clé
  == 173fae9c… ; le format 13/13 ; LE RECOUP D163 REJOINT UNE
  CINQUIÈME FOIS : les DOUZE arbres inchangés == les signatures
  DÉPOSÉES == build 1.0.0 (Ed25519 déterministe) ; m8 RE-SIGNÉ :
  diverge de la déposée (la seconde remise, contre c444d730…),
  vérifie Ed25519 contre l'empreinte vivante e36141f7… ; LE DIFF
  CONTRÔLÉ vs la seconde remise : UNE ligne changée, LA m8, les DOUZE
  autres byte-identiques ; les empreintes vivantes == a-signer.txt
  13/13 — RECOUPE INTÉGRAL VERT.
- LE DÉPÔT CANONIQUE (sceau_I.py deposer --cle : l'atomicité — tout
  vérifié avant toute écriture) ET LA GARDE REPASSÉE : **13/13 arbres
  VERTS** — m8 vert (e36141f7…) : la dette de cérémonie de la
  révision 3 SOLDÉE.
- LE REBUILD 1.0.0-dev.4, LES PORTES RE-PASSÉES : BLOCS_SOCLE porte
  sys-06:R3 (la révision 3 à la source du build — AfdFlags = 0,
  TdiFlags = TDI_RECEIVE_NORMAL 0x20, sys-05:R2 inchangé), la version
  R10 0x01000004, GENERATION 12 ; la chaîne rejouée : le garde 13/13
  AVANT construire, l'héritage M3+M4+M5+M8 re-vérifié (le scellé
  0.9.0 recomposé OCTET PAR OCTET — R7), le socle re-assemblé de la
  notation réparée, l'oracle structurel, les 28 blocs tls13, le PE
  validé, les oracles M4+M5+LE HARNAIS SUIVI 131 VERTS (empreinte
  b8373757… — dont LES DEUX NOUVELLES MUTANTES DU TERRAIN : AfdFlags
  0→0x20 rétablie ET TdiFlags 0x20→0 vidée, TOUTES DEUX TRAHIES), la
  carte génération 12, le verrou croisé 86/86 — L'ARTEFACT :
  446279f3… (65 024 o).
- LE DIFF CONTRÔLÉ dev.3 ↔ dev.4 (diff_dev3_dev4.py, le dev.3 extrait
  du kit ACQUITTÉ 79d44284…) : **TROIS octets sur 65 024** — la
  version R10 @RVA 0x2820 (0x03 → 0x04) + LES DEUX IMMÉDIATES du
  contrat d'appel dans sys-06 (@RVA 0xa725 : AfdFlags 0x20 → 0, en
  encode disp8 ; @RVA 0xa730 : TdiFlags 0 → 0x20, en encode disp32 —
  0x80 DÉPASSE la portée disp8, l'encode canonique nommé) ; RIEN
  d'autre ne bouge ; le contrat réparé relu dans l'image aux DEUX
  sites (c7 44 24 7c 00 00 00 00 / c7 84 24 80 00 00 00 20 00 00 00).
- LE KIT M9F RÉPARÉ : scenario-m9f.py re-épinglé (SHA_PROXY
  446279f3…, génération 12) + LE T0 PORTE LA PREUVE
  (T0.erratum-10 : le contrat d'appel relu dans l'image au bloc
  sys-06, aux DEUX sites) ; LISEZMOI-KIT-M9F.md RÉÉCRIT (l'erratum
  n° 10 + la révision 3, LE SEPTIÈME RUN) ; l'assembleur re-passé :
  32 constantes PAR AST + LE CONTRÔLE PERMANENT erratum n° 10 + les
  portes 6/7 + py_compile + extraction vierge — kit-m9f.zip md5
  92098687…, sha256 c0883c87…
- LA LIVRAISON AU COFFRE (corriger_kit_m9f_e10.py, modèle e9) :
  kit-m9f.zip MIS À JOUR EN PLACE (md5 92098687… MATCH par relecture,
  l'ancien vit dans l'histoire git) ; LISEZMOI-m9f.txt à jour
  (41add303…) ; preuves-m9f/LISEZMOI-preuves.txt à jour (dev.4,
  génération 12, LE SEPTIÈME RUN), le réceptacle RÉ-ARMÉ ; l'index
  des livraisons porte la note de la révision 3 ; la vérification
  finale (19 entrées, LES PIÈCES DE CÉRÉMONIE demeurées : la
  TROISIÈME remise 0978c117… + la clé ancre 188a7d42…).
- FRONTIÈRES : le scellé 0.9.0 INTACT (R7 recomposé au build même),
  l'artefact dev.3 remplacé PAR LE DIFF CONTRÔLÉ (il demeure la pièce
  des archives des runs 5-6 et de la sonde sys-06), aucune balise
  (D104), la clé privée jamais traversée (D87). SUITE : LE SEPTIÈME
  RUN DU DÉVELOPPEUR (le premier du contrat réparé : kit-m9f.zip →
  dossier NEUF D99, python scenario-m9f.py, preuves-m9f/ ENTIER au
  coffre) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA
  GRANDE ŒUVRE.
"""


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" in plan:
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
        if "LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                     "après remplacement")
        if "LE SEPTIÈME RUN DU DÉVELOPPEUR ATTENDU" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 192 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 192 —" in journal:
        print("JOURNAL : l'Entrée 192 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_192 + marqueur, 1)
        if "## Entrée 192 — LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in journal:
            sys.exit("ÉCHEC : l'Entrée 192 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 192 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 110 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 110 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 110 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 109 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 109 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = ("TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.")
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 109 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_110
    if "## Task ID 110 — LA TROISIÈME SIGNATURE DE LA RÉVISION 3 REÇUE" not in worklog:
        sys.exit("ÉCHEC : la Task ID 110 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 110 consignée À LA SUITE de la Task 109")


if __name__ == "__main__":
    main()
