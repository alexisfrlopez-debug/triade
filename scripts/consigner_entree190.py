#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree190.py — LA CONSIGNATION DU GESTE « LE SIXIÈME RUN REÇU
ET ANALYSÉ SUR PIÈCES : LE JUMEAU — le -7 REPRODUIT IDENTIQUE (l'émission
VERT ×2, la réception immédiate -7 ×2, le run en SA seconde ×2, le bord
DNS changé) — LA CONDITION NOMMÉE D'AVANCE EST REMPLIE : LE PASSAGER
ÉLIMINÉ SUR PIÈCES ; LA SONDE SYS-06 LIVRÉE au /test par le même geste » :
la rangée (f) du plan reçoit le constat, l'État du programme reçoit la
phrase du geste, le worklog reçoit l'Entrée 190 + la Task ID 108. Rejeu
REFUSÉ ; tout ancrage absent ou compté autrement qu'UNE fois = ÉCHEC
NOMMÉ, rien n'est écrit."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

# --- la rangée (f) : le constat du geste remplace l'attente -------------------------

ANCIEN_RANGEE = (
    " ; LE SIXIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le MÊME kit, réseau "
    "vivant — UN AUTRE réseau si possible : le discriminant du passager) — "
    "SI LE VERT VIENT : LA FINALE 1.0.0, LE JALON M9 ; SI LE -7 SE "
    "REPRODUIT IDENTIQUE : LA SONDE sys-06 (nommée d'avance, le miroir de "
    "l'Entrée 185)**")

NOUVELLE_RANGEE = (
    " ; **LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES le 07/11/2026 (Entrée "
    "190, Task 108) : LE JUMEAU — LE -7 REPRODUIT IDENTIQUE, LE PASSAGER "
    "ÉLIMINÉ SUR PIÈCES** [le terrain tenu : Windows 11 build 26300, "
    "ntdll b072efae… — LE MÊME que les runs 4/5, l'interpréteur seul "
    "change (Python 3.14.3) ; l'artefact RÉPARÉ de23e577… — LE MÊME que "
    "le run 5, le kit ACQUITTÉ INCHANGÉ 79d44284… ; le recoup labo 33/33 "
    "sur pièces croisées : l'échelle REJOUÉE sur la clé privée DU RUN "
    "rend la clé du témoin, le CH 119 o recoupé octet pour octet — LA "
    "SECONDE ÉMISSION RÉELLE DU PROJET (sys-05 rend 0 ENCORE : "
    "l'émission réparée du run 5 N'ÉTAIT PAS UN PASSAGER, elle TIENT) ; "
    "LE JUMEAU CONSTATÉ PAR CODE : le journal du run 6 == le journal du "
    "run 5 LIGNE À LIGNE (horodatements exceptés), les témoins divergent "
    "sur les invariants seuls — l'interpréteur, l'ASLR, le handle, LE "
    "BORD DNS CHANGÉ (104.16.124.96 → 104.16.123.96 : une AUTRE arête "
    "Cloudflare a répondu, le même verdict est revenu), l'aléa et les "
    "clés ; LE -7 REPRODUIT IDENTIQUE — l'émission VERT ×2, la réception "
    "immédiate -7 ×2, le run en SA seconde ×2 : LA CONDITION NOMMÉE "
    "D'AVANCE EST REMPLIE — LE PASSAGER ÉLIMINÉ SUR PIÈCES ; restent le "
    "contrat de réception sys-06 [réparé PAR SYMÉTRIE, jamais mesuré par "
    "sonde] et LA DEMI-FIN [le pair a refermé proprement à l'offre sans "
    "SNI] ; le run archivé → archives-preuves/preuves-run-m9f-6/ AVEC le "
    "verdict du recoup, le réceptacle m9f CLOS ; LA FINALE 1.0.0 REFUSÉE "
    "pour CE run (fail-closed — le critère exige le vert)]** ; LA SONDE "
    "SYS-06 LIVRÉE au /test par LE MÊME GESTE (kit-sonde-sys06.zip md5 "
    "67e2014d… + LISEZMOI-sonde-sys06.txt + le réceptacle "
    "preuves-sonde-sys06/ — le miroir de l'Entrée 185 : LE GESTE M9F "
    "DÉCOMPOSÉ, l'offre du CH par sys-05 direct PUIS LA PREMIÈRE LECTURE "
    "par le trampoline de capture, le compas étalonné avant la mesure, "
    "la contre-épreuve standard S4 embarquée) — LE GESTE AU DÉVELOPPEUR : "
    "python scenario-sonde-sys06.py (dossier NEUF D99, Python 64 bits, "
    "réseau vivant), renvoyer preuves-sonde-sys06/ ENTIER au coffre "
    "/test/preuves-sonde-sys06/ — SI LA LECTURE REND DES OCTETS : LA "
    "PERCÉE, LA FINALE 1.0.0 EN VUE, LE JALON M9 — LA GRANDE ŒUVRE ; SI "
    "LE ZÉRO (-7) : LA DEMI-FIN NOMMÉE SUR PIÈCES ; SI LE -6 : LE "
    "NTSTATUS NOMME LE COUPABLE (PENDING le bug du contrat, "
    "INVALID_PARAMETER le contrat d'appel, RESET/DISCONNECT le pair)**")

# --- l'État du programme : la phrase du geste remplace l'attente --------------------

ANCIEN_ETAT = (
    " — LE SIXIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le MÊME kit, un dossier "
    "NEUF D99, réseau vivant — UN AUTRE réseau si possible : le "
    "discriminant du passager ; renvoyer preuves-m9f/ ENTIER au coffre) — "
    "SI LE VERT VIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ; "
    "SI LE -7 SE REPRODUIT IDENTIQUE (l'émission VERT, la réception "
    "immédiate -7, le run en SA seconde) : LA SONDE sys-06 S'OUVRE (nommée "
    "d'avance — lire le NTSTATUS brut ou LE ZÉRO de LA RÉCEPTION, le "
    "miroir de l'Entrée 185)**")

NOUVEL_ETAT = (
    "**LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES le 07/11/2026 (Entrée "
    "190, Task 108) : LE JUMEAU — le journal du run 6 == le journal du "
    "run 5 LIGNE À LIGNE (les horodatements exceptés), sur LE MÊME noyau "
    "(Win11 26300, ntdll b072efae…), LE MÊME artefact réparé "
    "(de23e577…), le kit ACQUITTÉ INCHANGÉ (79d44284…) ; LA SECONDE "
    "ÉMISSION RÉELLE DU PROJET (sys-05 rend 0 encore : le CH 119 o émis "
    "et recoupé — l'émission réparée N'ÉTAIT PAS UN PASSAGER, elle "
    "TIENT) ; le bord DNS changé (104.16.124.96 → 104.16.123.96 : une "
    "autre arête Cloudflare a répondu, le même verdict est revenu) ; LE "
    "-7 REPRODUIT IDENTIQUE (l'émission VERT ×2, la réception immédiate "
    "-7 ×2, le run en SA seconde ×2) : LA CONDITION NOMMÉE D'AVANCE EST "
    "REMPLIE — LE PASSAGER ÉLIMINÉ SUR PIÈCES ; restent le contrat de "
    "réception sys-06 et LA DEMI-FIN ; le recoup labo 33/33, le run "
    "archivé (preuves-run-m9f-6/ avec le jugement), le réceptacle m9f "
    "CLOS, le push GitHub tenu à l'ouverture (origin == 9db461b, la "
    "passation 107 partie — le flux ré-aligné)** — LA SONDE SYS-06 EST "
    "LIVRÉE au coffre /test par le même geste (kit-sonde-sys06.zip "
    "67e2014d… : le miroir de l'Entrée 185 — le geste m9f DÉCOMPOSÉ, "
    "l'offre par sys-05 direct puis LA PREMIÈRE LECTURE par le "
    "trampoline de capture : n ≥ 1 le ServerHello arrivé, -7 LE ZÉRO de "
    "la demi-fin, ou -6 + LE NTSTATUS BRUT de rdx ; le compas étalonné "
    "avant la mesure, la contre-épreuve standard S4 embarquée) — LE "
    "GESTE AU DÉVELOPPEUR : dézipper kit-sonde-sys06.zip dans un dossier "
    "NEUF D99, python scenario-sonde-sys06.py (Python 64 bits, réseau "
    "vivant — la cible www.cloudflare.com:443), renvoyer "
    "preuves-sonde-sys06/ ENTIER au coffre /test/preuves-sonde-sys06/ — "
    "SI LA LECTURE REND DES OCTETS : LA PERCÉE — la finale 1.0.0 en "
    "vue, LE JALON M9 — LA GRANDE ŒUVRE ; SI LE ZÉRO : LA DEMI-FIN "
    "nommée sur pièces ; SI LE -6 : le NTSTATUS nomme le coupable "
    "(PENDING le bug du contrat, INVALID_PARAMETER le contrat d'appel, "
    "RESET/DISCONNECT le pair)**")

# --- le journal : l'Entrée 190, AVANT le marqueur m5a -------------------------------

ENTREE_190 = """## Entrée 190 — LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES : LE JUMEAU — LE -7 REPRODUIT IDENTIQUE (L'ÉMISSION VERT ×2, LA RÉCEPTION IMMÉDIATE -7 ×2, LE RUN EN SA SECONDE ×2, LE BORD DNS CHANGÉ) — LA CONDITION NOMMÉE D'AVANCE EST REMPLIE : LE PASSAGER ÉLIMINÉ SUR PIÈCES ; LA SONDE SYS-06 LIVRÉE AU /TEST PAR LE MÊME GESTE (LE MIROIR DE L'ENTRÉE 185) (07/11)

**Le terrain a été vérifié avant de recevoir.** Le sondage du /test (lecture seule) : preuves-m9f/ porte le trio DU RUN (temoin-m9f.txt 9351b2bf…, scenario-m9f-journal.log acdc0fe8…, VERDICT-run-m9f.txt f432bc45…) auprès du LISEZMOI du réceptacle, AUCUNE pièce conditionnelle née ; la racine demeure en ordre (16 entrées, les archives en place) ; le kit RÉPARÉ INCHANGÉ (kit-m9f.zip md5 79d44284…) ; les pièces de cérémonie demeurées (signatures-I.txt 503f3822… + cle-publique-I.txt 188a7d42…). **Le push GitHub tenu à l'ouverture du geste** : le commit de passation Task 107 (9db461b) parti EN AVANCE du flux — origin ré-aligné (17fb911..9db461b, un fast-forward propre — les trois miroirs à la pointe).

**Le run rapatrié et recoupé sur pièces.** ramasse_run6_m9f.py (dossier NEUF download/preuves-run-m9f-6/, D99) : les TROIS pièces téléchargées, md5 aller-retour MATCH les métadonnées Drive, toutes inédites. Puis **recouper_run6_m9f.py : 33/33 sur pièces croisées (D138/D145/D148, D154)** — A : les md5 re-contrôlés contre Drive, les pièces T4/T6 absentes du coffre (le run est mort à T3, cohérence avec le run 5) ; B : **LES DIX-HUIT contrôles T0 [ok]** (dont LES DEUX T0.erratum-9), l'artefact INTACT == de23e577… (**LE MÊME rebuild dev.3 que le run 5 : le jumeau court le MÊME binaire**), LE TERRAIN TENU (Windows 11 build 26300, ntdll b072efae… — LE MÊME que les runs 4/5 ; l'interpréteur seul change : Python 3.14.3 — le run 4 le portait aussi), T1 (SSN 85/7/15, motif sain) + T2 VERT (sys-04 : rax 0, handle 0x338), la clé publique attendue NON-NULLE (000a6be0…), L'ÉCHEC NOMMÉ T3.ouvrir (rax -7, état 5 — LE MÊME NOM que le run 5), le recoup du jalon VERT (le CH == la construction re-jouée, 119 o), **AUCUN rappel émission → sys-05 rend 0 ENCORE : LA SECONDE ÉMISSION RÉELLE DU PROJET** ; C : le journal — SIX lignes toutes à 08:31:42 (le run entier dans SA seconde), l'échec journalé == l'échec nommé, la ligne -7 au texte exact de la source, le journal mort là ; D : le témoin embarqué dans le verdict == la pièce, LIGNE POUR LIGNE (34 lignes) ; E : l'échelle REJOUÉE sur LA CLÉ PRIVÉE DU RUN (0824c1e4… → 000a6be0… == le témoin), la construction CH re-jouée (114 o, l'aléa @ +6, la clé @ +82), la chaîne reconstituée depuis les contrats, le kit ACQUITTÉ (le /test INCHANGÉ 79d44284…), LA FRONTIÈRE NOMMÉE D'AVANCE (le LISEZMOI § 4 + la spec sys-06 R2) ; F : **LE JUMEAU CONSTATÉ PAR CODE** — le journal du run 6 == le journal du run 5 LIGNE À LIGNE (les horodatements exceptés — 07:23:36 ↔ 08:31:42 : soixante-huit minutes d'écart, PAS UNE LETTRE de différence), les témoins divergent sur les invariants seuls (l'interpréteur, l'ASLR, le handle, **LE BORD DNS CHANGÉ 104.16.124.96 → 104.16.123.96 : une AUTRE arête Cloudflare a répondu au run, le même verdict est revenu**, l'aléa et les clés ; le noyau et l'artefact TENUS), **LE -7 REPRODUIT IDENTIQUE — LA CONDITION NOMMÉE D'AVANCE EST REMPLIE : LE PASSAGER ÉLIMINÉ SUR PIÈCES** (un état transitoire du chemin ne revient pas deux fois à l'identique, sur des poignées synchrones vivantes, vers deux arêtes du bord), LA MORT À LA MÊME PLACE (la première lecture, sys-06 — le code exact vit dans rdx), LE TEMPS ENCORE (le verdict de réception SEC), LA COHÉRENCE UNANIME (aucune pièce conditionnelle née aux DEUX runs).

**Le run archivé.** archiver_run6_m9f.py (modèle archiver_run5, D143 : par DÉPLACEMENT, jamais un jet) : le trio DU RUN + LE VERDICT DU RECOUP (33/33) → **archives-preuves/preuves-run-m9f-6/** ; preuves-m9f/ ré-armé puis CLOS (son LISEZMOI seul — le geste au développeur n'est plus un run m9f : c'est LA SONDE) ; les DEUX index mis à jour (la section preuves-run-m9f-6 + la note du sixième run) ; la vérification finale : la racine 16 entrées, le kit ACQUITTÉ INCHANGÉ (79d44284…), les pièces de cérémonie demeurées.

**LA SONDE SYS-06 — le miroir de l'Entrée 185, le chantier promis.** scenario-sonde-sys06.py (LE MÊME triptyque T0/T1/T2 que m9f — dont LES DEUX contrôles T0.erratum-9 : la sonde de l'Entrée 185 a mesuré 0xC0000005 sur la pose « packée », le kit EMPORTE LA PREUVE que ces octets sont LES RÉPARÉS) ; **LE GESTE M9F DÉCOMPOSÉ** : (c) le ClientHello DE RÉFÉRENCE émis par **sys-05 DIRECT** (le chemin réparé, vert aux runs 5/6 : la reproduction) PUIS **LA PREMIÈRE LECTURE PAR LE TRAMPOLINE DE CAPTURE** — le même bloc sys-06 à son adresse scellée, 33 o posés au run (l'artefact INTACT, relu inchangé à la fin), le code ET le NTSTATUS empaquetés ; **LE COMPAS ÉTALONNÉ AVANT LA MESURE** (un handle invalide → -6 + STATUS_INVALID_HANDLE 0xC0000008 : la preuve que la capture lit VRAIMENT rdx — un compas muet arrête la sonde) ; LA VARIATION TAILLE (capacité 1, session sacrifiée) et LA VARIATION DÉLAI (après 2 s) ; **LA CONTRE-ÉPREUVE S4** (la poignée par LE RAPPEL STANDARD sur une session NEUVE — si la lecture rend des octets, la ligne applicative suit DANS LE MÊME RUN : LA PERCÉE). assembler_kit_sondesys06.py : **le recoup PAR AST de 31 constantes == l'artefact/le plan** (dont LA POSE DU WSABUF relue DANS L'IMAGE aux DEUX blocs @0xA586 ET @0xA706) ; LES PORTES passées (l'erratum n° 7 hérité : aucune écriture .raw, LE site OUVRIR au POINTEUR, l'échelle contre les vecteurs officiels RFC 7748/8448 + 16 clés semées ; S1 le squelette du trampoline EXACT vers sys-06 ; S2 la table NTSTATUS == la référence canonique ntstatus.h — 23 valeurs au bit près ; S3 le compas AVANT la mesure ; S4 le témoin vivant ; **S5 LE GESTE DÉCOMPOSÉ : l'offre sys-05 direct AVANT la lecture — l'ordre du geste m9f**) ; py_compile ; l'extraction vierge VERT. deposer_kit_sondesys06.py : **kit-sonde-sys06.zip (md5 67e2014d…) + LISEZMOI-sonde-sys06.txt + le réceptacle preuves-sonde-sys06/ NÉ** au coffre /test (la racine 19 entrées), la vague m9f INTACTE constatée avant le geste (kit-m9f.zip 79d44284… + la sonde sys-05 215c2caa… demeurée), l'index des livraisons mis à jour.

**Frontières.** LA FINALE 1.0.0 REFUSÉE pour CE run (fail-closed — le critère de la rangée (f) exige le vert : la session réelle ÉTABLIE ; D104 : aucune balise) ; le kit m9f INCHANGÉ (le terrain lavé, l'offre parfaite ET ÉMISE DEUX FOIS) ; le scellé 0.9.0 INTACT ; la clé privée jamais traversée (D87). Consignations : la présente Entrée 190 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 108. SUITE : **LE RUN DE LA SONDE SYS-06 AU DÉVELOPPEUR** — dézipper kit-sonde-sys06.zip dans un dossier NEUF D99, python scenario-sonde-sys06.py (Python 64 bits, réseau vivant — la cible www.cloudflare.com:443), renvoyer preuves-sonde-sys06/ ENTIER au coffre /test/preuves-sonde-sys06/ — **SI LA LECTURE REND DES OCTETS (n ≥ 1) : LA PERCÉE — le ServerHello ARRIVÉ, la finale 1.0.0 en vue, LE JALON M9 — LA GRANDE ŒUVRE ; SI LE ZÉRO (-7, rdx 0) : LA DEMI-FIN nommée sur pièces (le pair a refermé proprement à l'offre sans SNI — le geste sera la cible ou le SNI) ; SI LE -6 : LE NTSTATUS NOMME LE COUPABLE (PENDING le bug du contrat du bloc — l'erratum de la notation + la révision de la spec sys-06 ; INVALID_PARAMETER le contrat d'appel ; RESET/DISCONNECT le pair)**.

"""

# --- le worklog racine : la Task ID 108, À LA SUITE (append) ------------------------

TASK_108 = """
## Task ID 108 — LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES : LE JUMEAU (LE JUMELA CONSTATÉ PAR CODE — LE -7 REPRODUIT IDENTIQUE, LE PASSAGER ÉLIMINÉ SUR PIÈCES) ; LE RUN ARCHIVÉ ; LA SONDE SYS-06 LIVRÉE AU /TEST PAR LE MÊME GESTE (LE MIROIR DE L'ENTRÉE 185) (07/11)

Work Log:
- LE PUSH GITHUB TENU À L'OUVERTURE DU GESTE : le commit de passation
  Task 107 (9db461b) parti EN AVANCE du flux — origin ré-aligné
  (17fb911..9db461b, un fast-forward propre ; les trois miroirs à la
  pointe).
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR (lecture seule,
  sonder_run6_m9f.py) : preuves-m9f/ porte le trio DU RUN + le LISEZMOI
  du réceptacle, AUCUNE pièce conditionnelle née ; la racine 16
  entrées ; le kit RÉPARÉ INCHANGÉ (79d44284…) ; les pièces de
  cérémonie demeurées (503f3822… + 188a7d42…).
- LE RUN RAPATRIÉ (ramasse_run6_m9f.py, dossier NEUF
  download/preuves-run-m9f-6/, D99) : les TROIS pièces, md5
  aller-retour MATCH (temoin 9351b2bf…, journal acdc0fe8…, verdict
  f432bc45…), toutes inédites.
- LE RECOUP 33/33 SUR PIÈCES CROISÉES (recouper_run6_m9f.py,
  D138/D145/D148) : les DIX-HUIT T0 [ok] (dont LES DEUX T0.erratum-9) ;
  l'artefact INTACT == de23e577… (LE MÊME rebuild dev.3 que le run 5 —
  le jumeau court le MÊME binaire) ; LE TERRAIN TENU (Win11 build
  26300, ntdll b072efae… — LE MÊME que les runs 4/5 ; Python 3.14.3) ;
  T1 + T2 VERT (handle 0x338) ; la clé attendue NON-NULLE (000a6be0…) ;
  l'échec NOMMÉ T3.ouvrir (rax -7, état 5 — LE MÊME NOM que le run 5) ;
  le recoup du jalon VERT (le CH == la construction re-jouée, 119 o) ;
  LA SECONDE ÉMISSION RÉELLE DU PROJET (AUCUN rappel émission → sys-05
  rend 0 ENCORE : l'émission réparée N'ÉTAIT PAS UN PASSAGER, elle
  TIENT) ; l'échelle REJOUÉE sur la clé privée DU RUN (0824c1e4… →
  000a6be0…) ; le témoin == le verdict LIGNE POUR LIGNE (34) ; le kit
  du coffre ACQUITTÉ INCHANGÉ.
- LE JUMEAU CONSTATÉ PAR CODE (F1/F2) : le journal du run 6 == le
  journal DU RUN 5 LIGNE À LIGNE, les horodatements exceptés (07:23:36
  ↔ 08:31:42 : soixante-huit minutes d'écart, PAS UNE LETTRE de
  différence) ; les témoins divergent sur les invariants seuls —
  l'interpréteur (3.13.9 → 3.14.3), l'ASLR, le handle (0x284 →
  0x338), LE BORD DNS CHANGÉ (104.16.124.96 → 104.16.123.96 : une
  AUTRE arête Cloudflare a répondu au run — le DNS résolu AU RUN), les
  clés ; LE NOYAU ET L'ARTEFACT TENUS.
- LE -7 REPRODUIT IDENTIQUE (F3) — LA CONDITION NOMMÉE D'AVANCE PAR LE
  RECOUP-5 ET LA PASSATION 107 EST REMPLIE : l'émission VERT ×2, la
  réception immédiate -7 ×2, le run en SA seconde ×2 → LE PASSAGER
  ÉLIMINÉ SUR PIÈCES (un état transitoire du chemin ne revient pas
  deux fois à l'identique, sur des poignées synchrones vivantes, vers
  deux arêtes du bord) ; restent DEUX candidats : le contrat de
  réception sys-06 [la spec R2 : « La réception n'a JAMAIS couru sur
  le terrain réel » — réparée PAR SYMÉTRIE, jamais mesurée par sonde]
  et LA DEMI-FIN [le zéro de sys-06 Q2 : le pair a refermé proprement
  à l'offre sans SNI].
- LE TEMPS ENCORE (F5) : le run entier dans SA seconde (08:31:42), T2
  venant de réussir le three-way handshake synchrone : le verdict de
  réception fut SEC, ENCORE ; LA COHÉRENCE UNANIME (F6) : aucune pièce
  conditionnelle née aux DEUX runs — la lecture n'a JAMAIS rendu un
  octet.
- L'ARCHIVAGE (archiver_run6_m9f.py, modèle archiver_run5, D143 : par
  DÉPLACEMENT) : le trio + LE VERDICT DU RECOUP (33/33) →
  archives-preuves/preuves-run-m9f-6/ ; preuves-m9f/ ré-armé puis CLOS
  (son LISEZMOI seul) ; les DEUX index mis à jour ; la racine 16
  entrées ; le kit ACQUITTÉ INCHANGÉ (79d44284… — AUCUN dépôt).
- LA SONDE SYS-06 OUVERTE (scenario-sonde-sys06.py, le miroir de
  l'Entrée 185) : LE GESTE M9F DÉCOMPOSÉ — l'offre du CH de référence
  par sys-05 DIRECT (le chemin réparé, vert aux runs 5/6) PUIS LA
  PREMIÈRE LECTURE PAR LE TRAMPOLINE DE CAPTURE (33 o posés au run,
  l'artefact INTACT : le code ET le NTSTATUS de rdx empaquetés) ; LE
  COMPAS ÉTALONNÉ AVANT LA MESURE (handle invalide → -6 +
  STATUS_INVALID_HANDLE) ; LA TABLE NTSTATUS canonique (23 valeurs,
  Wine ET ReactOS au bit près) ; LES VARIATIONS (taille : capacité 1
  sur session sacrifiée ; délai : après 2 s) ; LA CONTRE-ÉPREUVE S4
  (la poignée par LE RAPPEL STANDARD, session NEUVE — si la lecture
  rend des octets : LA PERCÉE, la ligne applicative suit DANS LE MÊME
  RUN).
- L'ASSEMBLAGE ÉPROUVÉ (assembler_kit_sondesys06.py) : le recoup PAR
  AST de 31 constantes == l'artefact/le plan (dont LA POSE DU WSABUF
  relue DANS L'IMAGE aux DEUX blocs @0xA586/@0xA706) ; LES PORTES
  passées (erratum n° 7 hérité ; S1 le squelette EXACT vers sys-06 ;
  S2 la table canonique ; S3 le compas avant la mesure ; S4 le témoin
  vivant ; S5 LE GESTE DÉCOMPOSÉ : l'offre AVANT la lecture) ;
  py_compile ; l'extraction vierge VERT — kit-sonde-sys06.zip md5
  67e2014d… (39 262 o).
- LA LIVRAISON (deposer_kit_sondesys06.py) : kit-sonde-sys06.zip +
  LISEZMOI-sonde-sys06.txt + le réceptacle preuves-sonde-sys06/ NÉ au
  coffre /test (la racine 19 entrées) ; la vague m9f INTACTE constatée
  AVANT le geste (kit-m9f.zip 79d44284… + la sonde sys-05 215c2caa…
  demeurée) ; l'index des livraisons mis à jour (la note de la sonde).
- FRONTIÈRES : LA FINALE 1.0.0 REFUSÉE pour CE run (fail-closed — le
  critère exige le vert ; D104 : aucune balise) ; le kit m9f INCHANGÉ
  (l'offre parfaite ET ÉMISE DEUX FOIS) ; le scellé 0.9.0 INTACT ; la
  clé privée jamais traversée (D87). SUITE : LE RUN DE LA SONDE SYS-06
  AU DÉVELOPPEUR — dézipper kit-sonde-sys06.zip dans un dossier NEUF
  D99, python scenario-sonde-sys06.py (Python 64 bits, réseau vivant),
  renvoyer preuves-sonde-sys06/ ENTIER au coffre /test/preuves-sonde-
  sys06/ — SI LA LECTURE REND DES OCTETS : LA PERCÉE, LA FINALE 1.0.0
  EN VUE, LE JALON M9 — LA GRANDE ŒUVRE ; SI LE ZÉRO (-7) : LA
  DEMI-FIN NOMMÉE SUR PIÈCES ; SI LE -6 : LE NTSTATUS NOMME LE
  COUPABLE (PENDING le bug du contrat, INVALID_PARAMETER le contrat
  d'appel, RESET/DISCONNECT le pair).
"""


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" in plan:
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
        if "LE PASSAGER ÉLIMINÉ SUR PIÈCES" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                     "après remplacement")
        if "LA SONDE SYS-06 EST LIVRÉE" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 190 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 190 —" in journal:
        print("JOURNAL : l'Entrée 190 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_190 + marqueur, 1)
        if "## Entrée 190 — LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" not in journal:
            sys.exit("ÉCHEC : l'Entrée 190 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 190 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 108 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 108 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 108 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 107 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 107 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = ("ET LA SONDE sys-06 S'OUVRE (lire le NTSTATUS brut ou LE "
                 "ZÉRO de la\n  réception, le miroir de l'Entrée 185).")
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 107 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_108
    if "## Task ID 108 — LE SIXIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" not in worklog:
        sys.exit("ÉCHEC : la Task ID 108 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 108 consignée À LA SUITE de la Task 107")


if __name__ == "__main__":
    main()
