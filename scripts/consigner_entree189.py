#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree189.py — LA CONSIGNATION DU GESTE « LE CINQUIÈME RUN
REÇU ET ANALYSÉ SUR PIÈCES : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET —
L'ERRATUM n° 9 VALIDÉ SUR LE VRAI NOYAU — MAIS LE ROUGE TIENT (T3.ouvrir
: la première lecture, rax -7) ; LA MORT A RECULÉ D'UN CRAN, À LA
FRONTIÈRE NOMMÉE PAR L'ENTRÉE 187 ; LE PUSH GITHUB RÉPARÉ À L'OUVERTURE
DU GESTE (origin == 5dcd1f9) ; LE SIXIÈME RUN EST LE GESTE AU
DÉVELOPPEUR — SI LE -7 SE REPRODUIT IDENTIQUE : LA SONDE sys-06 » : la
rangée (f) du plan reçoit le constat, l'État du programme reçoit la
phrase du geste, le worklog reçoit l'Entrée 189 + la Task ID 107.
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
    "— LE CINQUIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le premier du build "
    "réparé) — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9]**")

NOUVELLE_RANGEE = (
    "— **LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES le 07/11/2026 "
    "(Entrée 189, Task 107) : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET** "
    "[le terrain tenu : Windows 11 build 26300, ntdll b072efae… — LE "
    "MÊME que le run 4, l'interpréteur seul change (Python 3.13.9) ; "
    "l'artefact RÉPARÉ de23e577… — LA POSE canonique relue DANS L'IMAGE "
    "aux DEUX blocs (les DEUX contrôles T0.erratum-9 [ok]), le kit "
    "ACQUITTÉ INCHANGÉ 79d44284… ; le recoup labo 33/33 sur pièces "
    "croisées : l'échelle REJOUÉE sur la clé privée DU RUN rend la clé "
    "du témoin, le CH 119 o recoupé octet pour octet, LA DIFFÉRENCE "
    "D'UNE LIGNE constatée par code — le journal du run 5 == le journal "
    "du run 4 MOINS la ligne « le rappel émission : sys-05 rend -6 », "
    "sur LE MÊME noyau : L'A/B CONCLUT — LA RÉPARATION (la pose 0x68, "
    "buf à +8) EST LA CAUSE DE LA GUÉRISON, le refus -6 "
    "ACCESS_VIOLATION de la sonde (Entrée 185) EST MORT — **L'ERRATUM "
    "n° 9 VALIDÉ SUR LE VRAI NOYAU** ; le CH PARTI SUR LE RÉSEAU par le "
    "VRAI afd.sys, zéro ws2_32] ; **MAIS LE ROUGE TIENT : T3.ouvrir "
    "rax -7, état 5 — LA MORT A RECULÉ D'UN CRAN**, de l'émission "
    "(sys-05) à LA PREMIÈRE LECTURE (sys-06, le ServerHello attendu : "
    "le rappel réception, jamais journalé, rend non-nul → « la coupure "
    "du socle → -7 », tls13-27 Q3, l'état 5) — EXACTEMENT LA FRONTIÈRE "
    "QUE L'ENTRÉE 187 NOMMAIT D'AVANCE ; LE TEMPS ÉLIMINE LE SILENCE "
    "[le run entier dans SA seconde : le verdict de réception fut SEC — "
    "un refus du noyau ou une fermeture vive du pair, PAS une attente "
    "muette] ; les candidats : le passager réseau [AFFAIBLI, PAS "
    "ÉLIMINÉ], le contrat de réception sys-06 [la spec R2 le nomme "
    "elle-même : « La réception n'a JAMAIS couru sur le terrain réel » "
    "— réparée PAR SYMÉTRIE, jamais mesurée par sonde], LA DEMI-FIN [le "
    "pair a refermé proprement à l'offre sans SNI] — le code exact vit "
    "dans rdx : UN SEUL MOT D'INFORMATION MANQUE, LA SONDE sys-06 LE "
    "LIRAIT ; le run archivé → archives-preuves/preuves-run-m9f-5/ AVEC "
    "le verdict du recoup, le réceptacle ré-armé, la racine 16 entrées ; "
    "LA FINALE 1.0.0 REFUSÉE pour CE run (fail-closed — le critère "
    "exige le vert)]** ; LE SIXIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le "
    "MÊME kit, réseau vivant — UN AUTRE réseau si possible : le "
    "discriminant du passager) — SI LE VERT VIENT : LA FINALE 1.0.0, LE "
    "JALON M9 ; SI LE -7 SE REPRODUIT IDENTIQUE : LA SONDE sys-06 "
    "(nommée d'avance, le miroir de l'Entrée 185)**")

# --- l'État du programme : la phrase du geste remplace l'attente --------------------

ANCIEN_ETAT = (
    "— LE CINQUIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le premier du build "
    "réparé : dézipper kit-m9f.zip dans un dossier NEUF D99, python "
    "scenario-m9f.py, renvoyer preuves-m9f/ ENTIER au coffre) — ET SI LE "
    "VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

NOUVEL_ETAT = (
    "**LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES le 07/11/2026 (Entrée "
    "189, Task 107) : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET — le CH 119 "
    "o PARTI SUR LE RÉSEAU par le VRAI afd.sys (sys-05 rend 0 : la "
    "ligne « le rappel émission : sys-05 rend -6 » des runs 1/3/4 a "
    "DISPARU — L'ERRATUM n° 9 VALIDÉ SUR LE VRAI NOYAU, l'A/B concluant "
    "sur le MÊME noyau Win11 26300/ntdll b072efae…) ; MAIS LE ROUGE "
    "TIENT : T3.ouvrir rax -7, état 5 — LA MORT A RECULÉ D'UN CRAN, à "
    "LA PREMIÈRE LECTURE (sys-06 rend non-nul → « la coupure du socle "
    "») : la frontière nommée d'avance par l'Entrée 187 ; le recoup labo "
    "33/33, le run archivé (preuves-run-m9f-5/ avec le jugement), le kit "
    "ACQUITTÉ INCHANGÉ (79d44284…), le réceptacle ré-armé ; le push "
    "GitHub RÉPARÉ à l'ouverture du geste (origin == 5dcd1f9, la "
    "passation 106 partie en avance du flux : un fast-forward propre)** "
    "— LE SIXIÈME RUN DU DÉVELOPPEUR EST ATTENDU (le MÊME kit, un "
    "dossier NEUF D99, réseau vivant — UN AUTRE réseau si possible : le "
    "discriminant du passager ; renvoyer preuves-m9f/ ENTIER au coffre) "
    "— SI LE VERT VIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE "
    "ŒUVRE ; SI LE -7 SE REPRODUIT IDENTIQUE (l'émission VERT, la "
    "réception immédiate -7, le run en SA seconde) : LA SONDE sys-06 "
    "S'OUVRE (nommée d'avance — lire le NTSTATUS brut ou LE ZÉRO de LA "
    "RÉCEPTION, le miroir de l'Entrée 185)**")

# --- le journal : l'Entrée 189, AVANT le marqueur m5a -------------------------------

ENTREE_189 = """## Entrée 189 — LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET — L'ERRATUM n° 9 VALIDÉ SUR LE VRAI NOYAU — MAIS LE ROUGE TIENT (T3.ouvrir : LA PREMIÈRE LECTURE, rax -7) ; LA MORT A RECULÉ D'UN CRAN, À LA FRONTIÈRE NOMMÉE PAR L'ENTRÉE 187 ; LE PUSH GITHUB RÉPARÉ À L'OUVERTURE DU GESTE ; LE SIXIÈME RUN EST LE GESTE AU DÉVELOPPEUR — SI LE -7 SE REPRODUIT IDENTIQUE : LA SONDE sys-06 (07/11)

**Le terrain a été vérifié avant de recevoir.** Le sondage du /test (lecture seule) : preuves-m9f/ porte le trio DU RUN (temoin-m9f.txt, scenario-m9f-journal.log, VERDICT-run-m9f.txt) auprès du LISEZMOI du réceptacle ; la racine demeure en ordre (16 entrées, les archives en place) ; le kit RÉPARÉ INCHANGÉ (kit-m9f.zip md5 79d44284…) ; les pièces de cérémonie demeurées (signatures-I.txt 503f3822… la seconde remise installée + cle-publique-I.txt 188a7d42… l'ancre). **Le push GitHub RÉPARÉ à l'ouverture du geste** (la demande du développeur : « répare le push git ») : le push re-tenté — **origin == 5dcd1f9** (la passation 106 partie EN AVANCE du flux : un fast-forward propre, rien défait — la passation du présent geste ré-aligne les trois miroirs à sa pointe).

**Le run rapatrié et recoupé sur pièces.** ramasse_run5_m9f.py (dossier NEUF download/preuves-run-m9f-5/, D99) : les QUATRE pièces téléchargées, md5 aller-retour MATCH les métadonnées Drive, toutes inédites (aucune collision avec les runs 1-4). Puis **recouper_run5_m9f.py : 33/33 sur pièces croisées (D138/D145/D148, D154)** — A : les md5 re-contrôlés contre Drive, les pièces T4/T6 absentes du coffre (nées à T4/T6 : le run est mort à T3, cohérence) ; B : **LES DIX-HUIT contrôles T0 [ok]** (les seize du run 4 + LES DEUX T0.erratum-9 NOUVEAUX : la pose du WSABUF canonique relue DANS L'IMAGE aux DEUX blocs, 89 74 24 60 48 89 7c 24 68 @0xa586 ET @0xa706), l'artefact INTACT == de23e577… (le rebuild dev.3 — le premier run du build réparé), LE TERRAIN TENU (Windows 11 build 26300, ntdll b072efae… — LE MÊME que le run 4 ; l'interpréteur seul change : Python 3.13.9, sans effet sur le natif), T1 (SSN 85/7/15, motif sain) + T2 VERT (sys-04 : rax 0, handle 0x284), la clé publique attendue NON-NULLE (ca6cf4ba…), L'ÉCHEC NOMMÉ T3.ouvrir (rax -7, état 5), le recoup du jalon VERT (le CH == la construction re-jouée, 119 o) ; C : le journal — SIX lignes toutes à 07:23:36 (le run entier dans SA seconde), **AUCUNE ligne « le rappel émission »** (la source ne journalise QUE si r != 0 → sys-05 a rendu 0), l'échec journalé == l'échec nommé, la ligne -7 au texte exact de la source, le journal mort là ; D : le témoin embarqué dans le verdict == la pièce, LIGNE POUR LIGNE (34 lignes) ; E : l'échelle REJOUÉE sur LA CLÉ PRIVÉE DU RUN (c757a3b5… → ca6cf4ba… == le témoin), la construction CH re-jouée (114 o, l'aléa @ +6, la clé @ +82), **LA CHAÎNE RECONSTITUÉE DEPUIS LES CONTRATS** (sys-05 rend 0 → le CH PARTI ; LA PREMIÈRE LECTURE : le rappel réception — sys-06, jamais journalé — rend NON-NUL → « la coupure du socle → -7 », tls13-27 Q3, l'état 5), le kit ACQUITTÉ (le /test INCHANGÉ 79d44284…, la source : SHA_PROXY de23e577… + T0.erratum-9 + le pointeur aux deux sites OUVRIR), LA FRONTIÈRE NOMMÉE D'AVANCE (le LISEZMOI § 4 : « Les causes NTSTATUS vivent dans rdx » — la limite NOMMÉE de l'instrument ; la spec sys-06 R2 : « La réception n'a JAMAIS couru sur le terrain réel ») ; F : **LA DIFFÉRENCE D'UNE LIGNE** (le journal du run 5 == le journal du run 4 MOINS la ligne « le rappel émission : sys-05 rend -6 », les horodatements exceptés — le run 4 rapatrié au geste même du coffre), LES TÉMOINS DIVERGENT SUR L'ARTEFACT SEUL (d8928934… → de23e577…, 16 → 18 contrôles T0), **L'A/B CONCLUT** (le même noyau, l'autre pose : la réparation est la cause de la guérison), **LA PRÉDICTION DE L'ENTRÉE 187 TENUE À LA LETTRE** (la mort a reculé d'EXACTEMENT UN CRAN), **LE -7 A CHANGÉ DE CHAÎNE** (run 4 : l'émission refusée, le CH jamais parti ; run 5 : le CH PARTI, la réception en échec), **LE TEMPS ÉLIMINE LE SILENCE** (le retour immédiat : un serveur muet aurait tenu la lecture jusqu'à la garde-chien, 300 s).

**LA PREMIÈRE ÉMISSION RÉELLE DU PROJET.** Les runs 1/3/4 mouraient à l'émission (sys-05 rend -6, la mesure de la sonde : 0xC0000005 ACCESS_VIOLATION × 3, le WSABUF « packé » — l'Entrée 185). LE RUN 5 A PASSÉ LA PORTE : **sys-05 rend 0 à son premier appel réel** — le ClientHello (119 o : 5 + 114), composé PARFAIT (recoupé octet pour octet contre la construction re-jouée : l'aléa du kit @ +6, la clé publique @ +82 == l'échelle RFC 7748), EST PARTI SUR LE RÉSEAU par le VRAI afd.sys (zéro ws2_32). L'A/B des runs 4 ↔ 5 (LE MÊME noyau Win11 build 26300, LE MÊME ntdll b072efae…, l'artefact seul ayant changé : les TROIS octets du diff contrôlé) CONCLUT : **la pose canonique (0x68, buf à +8) est la cause de la guérison — l'erratum n° 9 VALIDÉ SUR LE TERRAIN RÉEL.**

**La mort un cran plus loin — la frontière de l'Entrée 187 atteinte.** La machine d'états a franchi l'émission, composé l'attente du ServerHello — et LA PREMIÈRE LECTURE a échoué : le rappel réception (sys-06 — jamais journalé par le scénario) rend NON-NUL, le socle est coupé, la machine rend -7, l'état 5 (MORT). C'est EXACTEMENT ce que l'analyse de l'erratum n° 9 nommait d'avance (« la mort à T3 un cran après la réparation de l'émission ») — et la spec sys-06 R2 le reconnaît : « La réception n'a JAMAIS couru sur le terrain réel » — réparée PAR SYMÉTRIE avec l'émission (le C_ASSERT send/recv), jamais mesurée par sonde. **LE TEMPS ÉLIMINE LE SILENCE** : le run entier a vécu SA seconde (07:23:36) — T2 venait de réussir le three-way handshake synchrone (le chemin était vivant) et la lecture BLOQUANTE est revenue IMMÉDIATEMENT : un serveur muet aurait TENU la lecture (la garde-chien tire à 300 s) — le verdict de réception fut SEC. Restent TROIS candidats (évidence avant correctif — D54/D68/D98) : **(a) le passager réseau** (un middlebox peut refermer VITE l'offre sans SNI — le scénario le suggère : « réessayez réseau vivant ») ; **(b) le contrat de réception sys-06 refusé structurellement** (IOCTL_AFD_RECEIVE tel que le bloc le pose : l'AFD_RECV_INFO 24 o, AfdFlags 0x20 — la mesure leftarcode, TdiFlags 0) ; **(c) LA DEMI-FIN** (le pair a fermé proprement à l'offre : le zéro de sys-06 Q2). **LE CODE EXACT (-6 le STATUS / -7 le zéro ; le NTSTATUS brut vit dans rdx — sys-06 Q5) N'EST PAS SURFACÉ PAR L'INSTRUMENT** (la limite NOMMÉE au LISEZMOI § 4) : UN SEUL MOT D'INFORMATION MANQUE — LA SONDE sys-06 LE LIRAIT (le miroir exact de l'Entrée 185).

**L'archivage et le kit.** archiver_run5_m9f.py (modèle archiver_run4, D143 : par DÉPLACEMENT, jamais un jet) : le trio DU RUN + LE VERDICT DU RECOUP (33/33) → **archives-preuves/preuves-run-m9f-5/** ; preuves-m9f/ RÉ-ARMÉ (son LISEZMOI seul — le réceptacle du SIXIÈME run) ; les DEUX index mis à jour (la section preuves-run-m9f-5 + la note du cinquième run) ; la vérification finale : la racine 16 entrées, **le kit ACQUITTÉ INCHANGÉ (79d44284… — AUCUN dépôt : le kit du run 5 est celui du run 6)**, les pièces de cérémonie demeurées.

**Frontières.** LA FINALE 1.0.0 REFUSÉE pour CE run (fail-closed — le critère de la rangée (f) exige le vert : la session réelle ÉTABLIE ; D104 : aucune balise posée, le scellage est un fait de carte) ; le kit INCHANGÉ (le MÊME binaire dev.3, le MÊME scénario — le terrain est lavé, l'offre est parfaite ET ÉMISE) ; le scellé 0.9.0 INTACT ; la clé privée jamais traversée (D87). Consignations : la présente Entrée 189 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 107. SUITE : **LE SIXIÈME RUN DU DÉVELOPPEUR** — le MÊME kit (kit-m9f.zip 79d44284…, AUCUNE réparation à faire), un dossier NEUF D99, réseau vivant (**UN AUTRE réseau si possible** : le discriminant du passager au meilleur coût — et la chance du vert), renvoyer preuves-m9f/ ENTIER au coffre /test/preuves-m9f/ — **SI LE VERT VIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE ; SI LE -7 SE REPRODUIT IDENTIQUE (l'émission VERT, la réception immédiate -7, le run en SA seconde) : LE PASSAGER ÉLIMINÉ SUR PIÈCES ET LA SONDE sys-06 S'OUVRE** (nommée d'avance : mesurer IOCTL_AFD_RECEIVE sur le vrai noyau, lire le NTSTATUS brut ou LE ZÉRO qui vit dans rdx).

"""

# --- le worklog racine : la Task ID 107, À LA SUITE (append) ------------------------

TASK_107 = """
## Task ID 107 — LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES : LA PREMIÈRE ÉMISSION RÉELLE DU PROJET (L'ERRATUM n° 9 VALIDÉ SUR LE VRAI NOYAU) — MAIS LE ROUGE TIENT : T3.ouvrir, LA PREMIÈRE LECTURE (rax -7, état 5), LA MORT A RECULÉ D'UN CRAN ; LE PUSH GITHUB RÉPARÉ À L'OUVERTURE ; LE RUN ARCHIVÉ — LE SIXIÈME RUN ATTENDU (07/11)

Work Log:
- LE PUSH GITHUB RÉPARÉ À L'OUVERTURE DU GESTE (la demande du
  développeur : « répare le push git ») : le push re-tenté —
  origin == 5dcd1f9 (la passation 106 partie EN AVANCE du flux : un
  fast-forward propre, rien défait ; la passation du présent geste
  ré-aligne les trois miroirs à sa pointe).
- LE TERRAIN VÉRIFIÉ AVANT DE RECEVOIR (lecture seule) : preuves-m9f/
  porte le trio DU RUN + le LISEZMOI du réceptacle ; la racine 16
  entrées ; le kit RÉPARÉ INCHANGÉ (79d44284…) ; les pièces de
  cérémonie demeurées (503f3822… + 188a7d42…).
- LE RUN RAPATRIÉ (ramasse_run5_m9f.py, dossier NEUF
  download/preuves-run-m9f-5/) : les QUATRE pièces, md5 aller-retour
  MATCH, toutes inédites.
- LE RECOUP 33/33 SUR PIÈCES CROISÉES (recouper_run5_m9f.py,
  D138/D145/D148) : les DIX-HUIT T0 [ok] (dont LES DEUX T0.erratum-9 :
  la pose relue DANS L'IMAGE aux DEUX blocs) ; l'artefact INTACT ==
  de23e577… (le premier run du build réparé) ; LE TERRAIN TENU (Win11
  build 26300, ntdll b072efae… — LE MÊME que le run 4 ; Python 3.13.9) ;
  T1 + T2 VERT (handle 0x284) ; la clé attendue NON-NULLE (ca6cf4ba…) ;
  l'échec NOMMÉ T3.ouvrir (rax -7, état 5) ; le recoup du jalon VERT
  (le CH == la construction re-jouée, 119 o) ; l'échelle REJOUÉE sur la
  clé privée DU RUN (c757a3b5… → ca6cf4ba…) ; le témoin == le verdict
  LIGNE POUR LIGNE (34) ; le kit du coffre ACQUITTÉ INCHANGÉ.
- LA PREMIÈRE ÉMISSION RÉELLE DU PROJET : la ligne « le rappel
  émission : sys-05 rend -6 » des runs 1/3/4 a DISPARU (la source ne
  journalise QUE si r != 0 → sys-05 a rendu 0) — le CH 119 o, composé
  PARFAIT, EST PARTI SUR LE RÉSEAU par le VRAI afd.sys, zéro ws2_32.
- L'A/B CONCLUT (F1/F2/F3) : le journal du run 5 == le journal du run
  4 MOINS la ligne « sys-05 rend -6 », les horodatements exceptés, sur
  LE MÊME noyau (Win11 26300, ntdll b072efae…), l'artefact seul ayant
  changé (d8928934… → de23e577… : les TROIS octets du diff contrôlé) :
  LA RÉPARATION (la pose canonique 0x68, buf à +8) EST LA CAUSE DE LA
  GUÉRISON — L'ERRATUM n° 9 VALIDÉ SUR LE TERRAIN RÉEL ; le refus -6
  ACCESS_VIOLATION (la sonde Entrée 185) EST MORT.
- LA MORT A RECULÉ D'UN CRAN (F4/F5) : de l'émission (sys-05) à LA
  PREMIÈRE LECTURE (sys-06, le ServerHello attendu : le rappel
  réception, jamais journalé, rend non-nul → « la coupure du socle →
  -7 », tls13-27 Q3, l'état 5) — EXACTEMENT la frontière que l'Entrée
  187 nommait d'avance ; LE -7 A CHANGÉ DE CHAÎNE (run 4 : le CH
  jamais parti ; run 5 : le CH PARTI, la réception en échec).
- LE TEMPS ÉLIMINE LE SILENCE (F6) : le run entier dans SA seconde
  (07:23:36), T2 venant de réussir le three-way handshake synchrone :
  la lecture BLOQUANTE est revenue IMMÉDIATEMENT — un serveur muet
  aurait TENU la lecture (la garde-chien tire à 300 s) : le verdict de
  réception fut SEC (un refus du noyau ou une fermeture vive du pair).
- LES CANDIDATS (évidence avant correctif — D54/D68/D98) : (a) le
  passager réseau [AFFAIBLI PAR LE TEMPS, PAS ÉLIMINÉ — un middlebox
  peut refermer VITE l'offre sans SNI ; le scénario le suggère :
  « réessayez réseau vivant »] ; (b) le contrat de réception sys-06
  refusé STRUCTURELLEMENT [la spec R2 le nomme : « La réception n'a
  JAMAIS couru sur le terrain réel » — réparée PAR SYMÉTRIE, jamais
  mesurée par sonde] ; (c) LA DEMI-FIN [le pair a refermé proprement à
  l'offre : le zéro de sys-06 Q2]. LE CODE EXACT vit dans rdx (sys-06
  Q5) : UN SEUL MOT D'INFORMATION MANQUE — LA SONDE sys-06 LE LIRAIT
  (le miroir de l'Entrée 185).
- L'ARCHIVAGE (archiver_run5_m9f.py, modèle archiver_run4, D143 : par
  DÉPLACEMENT) : le trio + LE VERDICT DU RECOUP (33/33) →
  archives-preuves/preuves-run-m9f-5/ ; preuves-m9f/ RÉ-ARMÉ (son
  LISEZMOI seul) ; les DEUX index mis à jour ; la racine 16 entrées ;
  le kit ACQUITTÉ INCHANGÉ (79d44284… — AUCUN dépôt : le kit du run 5
  est celui du run 6).
- FRONTIÈRES : LA FINALE 1.0.0 REFUSÉE pour CE run (fail-closed — le
  critère exige le vert ; D104 : aucune balise) ; le kit INCHANGÉ (le
  terrain lavé, l'offre parfaite ET ÉMISE) ; le scellé 0.9.0 INTACT ;
  la clé privée jamais traversée (D87). SUITE : LE SIXIÈME RUN DU
  DÉVELOPPEUR — le MÊME kit, un dossier NEUF D99, réseau vivant (UN
  AUTRE réseau si possible : le discriminant du passager), preuves-m9f/
  ENTIER au coffre — SI LE VERT VIENT : LA FINALE 1.0.0, le jalon M9 —
  LA GRANDE ŒUVRE ; SI LE -7 SE REPRODUIT IDENTIQUE : LA SONDE sys-06
  (nommée d'avance).
"""


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" in plan:
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
        if "LA PREMIÈRE ÉMISSION RÉELLE DU PROJET" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                     "après remplacement")
        if "LE SIXIÈME RUN DU DÉVELOPPEUR EST ATTENDU" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 189 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 189 —" in journal:
        print("JOURNAL : l'Entrée 189 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_189 + marqueur, 1)
        if "## Entrée 189 — LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" not in journal:
            sys.exit("ÉCHEC : l'Entrée 189 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 189 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 107 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 107 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 107 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 106 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 106 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = ("ET SI LE\n  VERT TIENT : LA FINALE 1.0.0, le jalon M9 — "
                 "LA GRANDE ŒUVRE.")
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 106 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_107
    if "## Task ID 107 — LE CINQUIÈME RUN REÇU ET ANALYSÉ SUR PIÈCES" not in worklog:
        sys.exit("ÉCHEC : la Task ID 107 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 107 consignée À LA SUITE de la Task 106")


if __name__ == "__main__":
    main()
