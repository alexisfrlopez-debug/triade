#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree191.py — LA CONSIGNATION DU GESTE « LE RUN DE LA SONDE
SYS-06 REÇU ET ANALYSÉ SUR PIÈCES : LE MOT D'INFORMATION EST VENU — le
code exact de la première lecture réelle LU ET NOMMÉ (-6,
STATUS_INVALID_PARAMETER, DÉTERMINISTE) ; L'A/B DES NOTATIONS NOMME LE
CHAMP : AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU ; L'ERRATUM n° 10 ET LA
RÉVISION 3 DE LA SPEC SYS-06 — LA REMISE RÉGÉNÉRÉE m8 e36141f7…, LA
TROISIÈME SIGNATURE ATTENDUE » : la rangée (f) du plan reçoit le
constat, l'État du programme reçoit la phrase du geste, le worklog
reçoit l'Entrée 191 + la Task ID 109. Rejeu REFUSÉ ; tout ancrage
absent ou compté autrement qu'UNE fois = ÉCHEC NOMMÉ, rien n'est
écrit. Les ancres RANGEE/ÉTAT sont importées de consigner_entree190
(les constats du geste précédent — la chaîne des remplacements tient
sans retranscription)."""
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"

sys.path.insert(0, str(REPO / "scripts"))
import consigner_entree190 as _c190  # noqa: E402  # la chaîne des gestes

# --- la rangée (f) : le constat du geste remplace l'attente -------------------------

ANCIEN_RANGEE = _c190.NOUVELLE_RANGEE   # le constat 190 (le jumeau + la sonde livrée)

NOUVELLE_RANGEE = (
    " ; **LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES le "
    "07/11/2026 (Entrée 191, Task 109) : LE MOT D'INFORMATION EST VENU** "
    "[le QUATUOR rapatrié md5 MATCH (temoin 69122e4d…, journal 05b499b7…, "
    "VERDICT a4f68279…, émissions 1bd8f538… — la pièce conditionnelle "
    "émissions NÉE : le CH de S4 recoupé 119 o ; ligne-recue.txt ABSENTE : "
    "la mesure, pas la percée) ; le recoup labo 17/17 sur pièces croisées "
    ": le compas étalonné (STATUS_INVALID_HANDLE : la capture lit "
    "VRAIMENT rdx), l'offre sys-05 VERT au même geste (rax 0 — le chemin "
    "lavé), LA MESURE : LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE = "
    "-6, NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D), CLASSE ERREUR, "
    "TROIS fois (la mesure + la variation taille capacité 1 + la "
    "variation délai 2 s : DÉTERMINISTE), S4 : le chemin standard meurt "
    "AU MÊME GESTE (-7, état 5 — la mesure du trampoline parle pour les "
    "DEUX) ; LA TABLE DE LA PASSATION 108 TRANCHE : INVALID_PARAMETER "
    "NOMME LE CONTRAT D'APPEL ; L'A/B DES NOTATIONS NOMME LE CHAMP : "
    "sys-05 (AfdFlags 0) PASSE sur LE MÊME montage, sys-06 (AfdFlags "
    "0x20) REFUSÉ — LE VRAI afd.sys (Win11 build 26300) REFUSE le bit "
    "0x20 dans AfdFlags : l'erratum de lecture de l'Entrée 187 RÉFUTÉ "
    "PAR LE TERRAIN, TDI_RECEIVE_NORMAL (0x20) RETOURNE au champ "
    "TdiFlags (le placement de la littérature) ; le -7 des SIX runs "
    "DÉSORMAIS LU : la machine -7/état 5 == sys-06 -6 == le noyau "
    "INVALID_PARAMETER — les SIX runs mouraient DU CONTRAT D'APPEL]** ; "
    "**LA RÉPARATION SELON LA CHARTE : L'ERRATUM n° 10 + LA RÉVISION 3 "
    "DE LA SPEC SYS-06 (AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL "
    "0x20 — le même encode 8 o, le slot intact) + la notation corrigée "
    "+ le harnais suivi (le noyau strict refuse le 0x20 en AfdFlags : "
    "131 contrôles · 131 VERTS × 3 graines) + LA REMISE RÉGÉNÉRÉE m8 "
    "sys.1 e36141f7… (README.md + sys-06-reception.md seuls divergent, "
    "les DOUZE autres arbres inchangés) ; le run archivé → "
    "archives-preuves/preuves-sonde-sys06-1/ AVEC le verdict du recoup "
    "(D143), le réceptacle ré-armé ; LA FINALE 1.0.0 REFUSÉE pour ce "
    "geste (fail-closed — le critère exige le vert)** ; LA TROISIÈME "
    "SIGNATURE DU DÉVELOPPEUR ATTENDUE (la remise e36141f7… → "
    "signatures-I.txt + cle-publique-I.txt au /test, la règle d'or : la "
    "clé du 04/11 réutilisée — 173fae9c…) — puis deposer, le garde "
    "13/13, LE REBUILD 1.0.0-dev.4 (le bloc sys-06 réparé SUR LE "
    "TERRAIN), LE KIT M9F RÉPARÉ au /test, le run — SI LE VERT TIENT : "
    "LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**")

# --- l'État du programme : la phrase du geste remplace l'attente --------------------

ANCIEN_ETAT = _c190.NOUVEL_ETAT        # l'État 190 (le jumeau + la sonde livrée)

NOUVEL_ETAT = (
    "**LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES le "
    "07/11/2026 (Entrée 191, Task 109) : LE MOT D'INFORMATION EST VENU "
    "— LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU ET NOMMÉ par le "
    "trampoline de capture (l'artefact INTACT, relu inchangé) : -6, "
    "NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D), CLASSE ERREUR, "
    "DÉTERMINISTE (trois mesures identiques — dont la capacité 1 et le "
    "délai 2 s ; le compas étalonné AVANT la mesure, l'offre sys-05 "
    "VERT au même geste, S4 : le chemin standard meurt AU MÊME GESTE — "
    "rax -7, état 5)** ; LA TABLE DE LA PASSATION 108 TRANCHE : "
    "INVALID_PARAMETER NOMME LE CONTRAT D'APPEL ; **L'A/B DES NOTATIONS "
    "NOMME LE CHAMP** : sys-05 (AfdFlags 0) passe sur LE MÊME montage, "
    "sys-06 (AfdFlags 0x20) est refusé — LE VRAI afd.sys (Win11 build "
    "26300) REFUSE le bit 0x20 dans AfdFlags : l'erratum de lecture de "
    "l'Entrée 187 (la mesure WinDbg citée : 0x20 en TROISIÈME champ) "
    "EST RÉFUTÉ PAR LE TERRAIN — TDI_RECEIVE_NORMAL (0x20) RETOURNE au "
    "champ TdiFlags, le placement de la littérature ; **le -7 des SIX "
    "runs m9f EST DÉSORMAIS LU : la machine -7/état 5 == sys-06 -6 == "
    "le noyau INVALID_PARAMETER — les SIX runs mouraient DU CONTRAT "
    "D'APPEL** ; LA RÉPARATION SELON LA CHARTE : **L'ERRATUM n° 10 + "
    "LA RÉVISION 3 DE LA SPEC SYS-06** (AfdFlags = 0, TdiFlags = "
    "TDI_RECEIVE_NORMAL 0x20) + la notation corrigée (le même encode 8 "
    "o, le slot intact) + le harnais suivi (131 contrôles · 131 VERTS "
    "× 3 graines) + **LA REMISE RÉGÉNÉRÉE m8 sys.1 e36141f7…** "
    "(README.md + sys-06-reception.md seuls divergent, les DOUZE autres "
    "arbres inchangés) ; le run archivé (preuves-sonde-sys06-1/ AVEC le "
    "verdict 17/17, le réceptacle ré-armé — D143) ; LA FINALE 1.0.0 "
    "REFUSÉE pour ce geste (fail-closed)** — **LA TROISIÈME SIGNATURE "
    "DU DÉVELOPPEUR ATTENDUE** (la remise e36141f7… → signatures-I.txt "
    "+ cle-publique-I.txt au /test ; la règle d'or : JAMAIS « generer "
    "», la clé du 04/11 réutilisée — 173fae9c…) — puis deposer, le "
    "garde 13/13, **LE REBUILD 1.0.0-dev.4** (le bloc sys-06 réparé "
    "SUR LE TERRAIN), LE KIT M9F RÉPARÉ au /test, le run du "
    "développeur — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 "
    "— LA GRANDE ŒUVRE**")

# --- le journal : l'Entrée 191, AVANT le marqueur m5a -------------------------------

ENTREE_191 = """## Entrée 191 — LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES : LE MOT D'INFORMATION EST VENU — LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU ET NOMMÉ (-6, STATUS_INVALID_PARAMETER, DÉTERMINISTE) — L'A/B DES NOTATIONS NOMME LE CHAMP : AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU ; L'ERRATUM n° 10 ET LA RÉVISION 3 DE LA SPEC SYS-06 — LA REMISE RÉGÉNÉRÉE m8 e36141f7…, LA TROISIÈME SIGNATURE ATTENDUE (07/11)

**La porte unique du geste jouée.** verifier_coherence_git_drive.py (lecture seule) : **g1/g2/g4 + d1..d10 + m1/m2 VERTS — LES TROIS MIROIRS ALIGNÉS** (HEAD == 43f942d == origin/bundle051/v0.5.1-jalon-v7 : la demande du développeur « répare le push git » SOLDÉE, le commit de passation Task 108 parti au flux ; le coffre /test 19 entrées — la vague INTACTE : kit-m9f.zip 79d44284… + kit-sonde-sys05.zip 215c2caa… + kit-sonde-sys06.zip 67e2014d…, les pièces de cérémonie demeurées 503f3822… + 188a7d42…, le réceptacle de la sonde ARMÉ, le réceptacle m9f CLOS, le run 6 archivé ; le miroir bundle 090-eb1479e 1e9f2e68… + 53 archives, rien supprimé). La seule porte ROUGE : g3 — l'arbre SALE, la réparation en vol (constatée, nommée : les CINQ fichiers m8 du geste même).

**Le run rapatrié et recoupé sur pièces.** ramasse_sondesys06.py (dossier dédié download/preuves-sonde-sys06/, D99, lecture seule) : le QUATUOR téléchargé, md5 aller-retour MATCH les métadonnées Drive (temoin-sonde-sys06.txt 69122e4d…, sonde-sys06-journal.log 05b499b7…, VERDICT-sonde-sys06.txt a4f68279…, journal-emissions.txt 1bd8f538… — la pièce conditionnelle émissions NÉE : le CH de la contre-épreuve S4, UN enregistrement 119 o, recoupé octet pour octet == le CH de référence ; ligne-recue.txt ABSENTE : la mesure, pas la percée — l'absence CONSTATÉE et nommée). Puis **recouper_sondesys06.py : 17/17 sur pièces croisées (D138/D145/D148, D154)** — r1..r5 l'intégrité : l'artefact IDENTIQUE de23e577… (la carte génération 11, l'erratum n° 9 relu aux DEUX blocs @0xA586/@0xA706), LE VRAI ntdll b072efae… (le même noyau que les runs 5/6, Win11 build 26300, l'interpréteur Python 3.13.9), le trampoline 33 o == LE SQUELETTE de la source, le compas étalonné (-6 + STATUS_INVALID_HANDLE 0xC0000008 sur le handle invalide : la capture lit VRAIMENT rdx) ; r6..r9 LA MESURE : l'offre VERT (rax 0 — sys-05 direct, la reproduction des runs 5/6), **LA MESURE : code -6, NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D), CLASSE ERREUR — un vrai refus du noyau**, les DEUX variations IDENTIQUES (taille capacité 1 sur session sacrifiée, délai 2 s : le refus est DÉTERMINISTE, pas transitoire) ; r10..r12 LA CONTRE-ÉPREUVE S4 : le chemin standard meurt AU MÊME GESTE (rax -7, état 5 — la coupure du socle : le -7 de la machine EST le -6 de sys-06, la mesure du trampoline parle pour les DEUX), l'émission 119 o == le CH de référence (16 03 03 00 72 || 114 o), T6 PROPRE (l'artefact relu inchangé) ; r13..r17 LE COUPABLE NOMMÉ SUR PIÈCES : **L'A/B DES NOTATIONS** — les notations sys-05 (l'émission, RÉUSSIE au geste même : rax 0) et sys-06 (la réception, REFUSÉE) LUES octet par octet sont IDENTIQUES au montage près (les DIX arguments NT, le WSABUF canonique buf à +8, l'info 24 o, l'IOSB, le handle, le tampon, la capacité) : UNE SEULE écriture diffère — **AfdFlags 0x20 (sys-06) contre AfdFlags 0 (sys-05, TdiFlags 0 aux DEUX)**.

**Le verdict du kit tenu : VERT-MESURE.** LE VERDICT DU RUN (a4f68279…) : le compas étalonné, LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU ET NOMMÉ (la limite nommée de l'instrument, franchie par le trampoline), les variations consignées, la contre-épreuve standard : la non-régression constatée. LA MISSION DE LA SONDE EST LA MESURE, PAS LA FINALE : un verdict VERT-MESURE n'est PAS le vert du critère M9-(f) — la finale 1.0.0 attend le run m9f complet (la falsification T5 y vit).

**La table tranche, le champ est nommé.** LA TABLE DE LA PASSATION 108 : ni la percée (n ≥ 1), ni la demi-fin (-7 / rdx 0), ni le bug du bloc (PENDING), ni le pair (RESET/DISCONNECT) — **INVALID_PARAMETER NOMME LE CONTRAT D'APPEL** ; l'A/B des notations le resserre au CHAMP : **AfdFlags = 0x20 est LE paramètre invalide** (sys-05, l'émission, passe AfdFlags = 0 sur LE MÊME montage ; le VRAI noyau refuse le bit 0x20 dans AfdFlags). **L'erratum de lecture de l'Entrée 187 EST RÉFUTÉ PAR LE TERRAIN** : TDI_RECEIVE_NORMAL (0x20) appartient au champ TdiFlags — la « littérature courante » écartée par l'erratum avait raison du placement ; la mesure WinDbg citée avait raison de la VALEUR mais tort du CHAMP. LE JUGE EST LE CODE : le noyau réel a le dernier mot sur le dump interprété. **La limite de l'instrument est FRANCHIE : le -7 des runs 1..6 est DÉSORMAIS LU** (la machine -7/état 5 == sys-06 -6 == le noyau INVALID_PARAMETER — les SIX runs mouraient DU CONTRAT D'APPEL, pas du pair, pas du passager, pas du silence).

**La réparation selon la charte (jamais une dérive silencieuse).** **LA RÉVISION 3 DE LA SPEC SYS-06** (m8/I/sys-06-reception.md : la note de révision 3 en tête — LE TERRAIN A JUGÉ LA MESURE ; Q3 réécrit : AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20 ; l'erratum de lecture n° 1 nommé avec son jugement par le terrain ; la structure totale 40 o inchangée, le WSABUF canonique 16 o inchangé) + **l'inventaire README de l'arbre m8 suivi** (la rangée sys-06 : l'erratum n° 10 tenu, le placement de la littérature rétabli) + **la notation corrigée** (m8/notation/sys-06-reception.asm + le brouillon : le QUATRIÈME champ porte le 0x20, le TROISIÈME porte 0 — le MÊME encode mov dword, 8 o, le slot ne bouge pas d'un octet, la carte demeure ; auteur.py rejoué : 287 o, 71 instructions, 97 o de padding — le round-trip tenu) + **le harnais suivi** (m8/harnais_sys.py : le noyau simulé AFD STRICT refuse désormais ce que le VRAI noyau refuse — le 0x20 en AfdFlags est REFUSÉ, la notation suit LE TERRAIN ; la mutante V4b ré-encodée DANS LES DEUX SENS) ; **LA PREUVE RE-PASSÉE : 131 contrôles · 131 VERTS × 3 graines** (20261105 empreinte 103da725…, 424242 e3281042…, 777777 283b938c… — zéro échec, les mutantes toutes trahies, les témoins intacts).

**La remise régénérée, la main du développeur re-servie.** sceau_I.py preparer JOUÉ : a-signer.txt porte **m8 sys.1 e36141f75ebd8e615c53ff1bd59a4f4cee45b9397eefa66773ffbf54580b3536** — README.md ET sys-06-reception.md seuls divergent du manifeste signé (DEUX fichiers, diff contrôlé) ; les DOUZE autres arbres INCHANGÉS (leurs empreintes == les signatures déjà déposées — la troisième signature ne sera qu'une re-signature de m8, les douze autres rendront encore les mêmes). La balise demeure sys.1 ; le garde relit : m8 CODE 10 — LE SIGNAL, pas la panne. **LISEZMOI-ceremonie-revision3-sys06.txt ÉCRIT** (OÙ NOUS EN SOMMES ; POURQUOI la révision 3 — LE TERRAIN A JUGÉ LA MESURE ; CE QUI A CHANGÉ : m8 e36141f7…, DEUX fichiers de l'arbre m8, l'empreinte c444d730… PÉRIMÉE par l'erratum n° 10 ; LA RÈGLE D'OR inchangée — JAMAIS « generer », la clé du 04/11 173fae9c… ; LES CINQ PAS — le pas 3 exige e36141f7… ; CE QUE CELA DÉBLOQUE) ; le NOTE_D130 réécrit (maj_kit.py : la rangée RACINE_KIT + le manifeste du kit) — déployés au commit même (hook post-commit : le miroir PUIS le kit).

**Le run archivé.** archiver_sondesys06.py (modèle archiver_sonde1, D143 : par DÉPLACEMENT, jamais un jet) : le QUATUOR DU RUN + LE VERDICT DU RECOUP (17/17) → **archives-preuves/preuves-sonde-sys06-1/** (le QUATUOR md5-contrôlé avant le geste, le verdict du recoup déposé AVEC les pièces — l'archive porte le jugement) ; preuves-sonde-sys06/ ré-armé (son LISEZMOI seul — le réceptacle du prochain run) ; les DEUX index mis à jour (la section preuves-sonde-sys06-1 + la note du run de la sonde) ; la vérification finale : la racine 19 entrées, les TROIS kits INCHANGÉS (79d44284… + 215c2caa… + 67e2014d… — recoupés).

**Frontières.** LA FINALE 1.0.0 REFUSÉE pour ce geste (fail-closed — le critère de la rangée (f) exige le vert : la session réelle ÉTABLIE ; D104 : aucune balise) ; les kits INCHANGÉS (le geste est l'analyse et la réparation de la couche I, AUCUN dépôt de kit) ; le scellé 0.9.0 INTACT ; la clé privée jamais traversée (D87). Consignations : la présente Entrée 191 PAR SCRIPT, PLAN (la rangée (f) + l'État du programme), worklog +Task ID 109. SUITE : **LA TROISIÈME SIGNATURE DU DÉVELOPPEUR** — la remise e36141f7… (v06/sceau-I/a-signer.txt, TREIZE arbres, UNE seule empreinte nouvelle) à signer HORS LIGNE avec la clé du 04/11, ramener signatures-I.txt + cle-publique-I.txt au /test — puis deposer, le garde 13/13, **LE REBUILD 1.0.0-dev.4** (le bloc sys-06 réparé SUR LE TERRAIN : AfdFlags 0, TdiFlags 0x20 — le même encode, le slot intact), LE KIT M9F RÉPARÉ au /test, le run du développeur — **ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE**.

"""

# --- le worklog racine : la Task ID 109, À LA SUITE (append) ------------------------

TASK_109 = """
## Task ID 109 — LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES : LE MOT D'INFORMATION EST VENU (LE CODE EXACT DE LA PREMIÈRE LECTURE RÉELLE LU : -6, STATUS_INVALID_PARAMETER — L'A/B NOMME LE CHAMP : AfdFlags 0x20 REFUSÉ PAR LE VRAI NOYAU) ; L'ERRATUM n° 10 + LA RÉVISION 3 + LA REMISE RÉGÉNÉRÉE m8 e36141f7… — LA TROISIÈME SIGNATURE ATTENDUE ; LE RUN ARCHIVÉ (07/11)

Work Log:
- LA PORTE UNIQUE DU GESTE JOUÉE (verifier_coherence_git_drive.py,
  lecture seule) : g1/g2/g4 + d1..d10 + m1/m2 VERTS — LES TROIS
  MIROIRS ALIGNÉS (HEAD == 43f942d == origin : LE PUSH RÉPARÉ tenu,
  le flux à la pointe ; le /test 19 entrées, les TROIS kits
  acquittés, le miroir bundle + 53 archives) ; la seule ROUGE g3 :
  l'arbre SALE — la réparation en vol, constatée et nommée.
- LE RUN RAPATRIÉ (ramasse_sondesys06.py, dossier dédiété D99) : le
  QUATUOR md5 aller-retour MATCH (temoin 69122e4d…, journal
  05b499b7…, VERDICT a4f68279…, émissions 1bd8f538… — la pièce
  conditionnelle émissions NÉE : le CH de S4, 119 o, UN
  enregistrement ; ligne-recue.txt ABSENTE : la mesure, pas la
  percée).
- LE RECOUP 17/17 SUR PIÈCES CROISÉES (recouper_sondesys06.py) :
  l'artefact IDENTIQUE de23e577…, le VRAI ntdll b072efae… (le même
  noyau que les runs 5/6 — Win11 build 26300, Python 3.13.9), le
  trampoline 33 o == le squelette de la source, le compas étalonné
  (STATUS_INVALID_HANDLE : la capture lit VRAIMENT rdx) ; l'offre
  sys-05 VERT (rax 0 au même geste — le chemin lavé) ; LA MESURE :
  code -6, NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D), CLASSE
  ERREUR, TROIS fois (la mesure + la variation taille + la variation
  délai : DÉTERMINISTE) ; S4 : le chemin standard meurt AU MÊME
  GESTE (rax -7, état 5 — le -7 de la machine EST le -6 de sys-06) ;
  l'émission 119 o == le CH de référence ; T6 PROPRE.
- LE COUPABLE NOMMÉ SUR PIÈCES (r13..r17, L'A/B) : les notations
  sys-05 (l'émission RÉUSSIE : rax 0) et sys-06 (la réception
  REFUSÉE) LUES octet par octet — IDENTIQUES au montage près ; UNE
  SEULE écriture diffère : AfdFlags 0x20 (sys-06) contre AfdFlags 0
  (sys-05). LA TABLE DE LA PASSATION 108 TRANCHE :
  INVALID_PARAMETER NOMME LE CONTRAT D'APPEL ; L'A/B NOMME LE CHAMP :
  LE VRAI afd.sys REFUSE le bit 0x20 dans AfdFlags — l'erratum de
  lecture de l'Entrée 187 (la mesure WinDbg citée : 0x20 en
  TROISIÈME champ) EST RÉFUTÉ PAR LE TERRAIN ; TDI_RECEIVE_NORMAL
  (0x20) RETOURNE au champ TdiFlags (le placement de la littérature)
  ; LE -7 DES SIX RUNS DÉSORMAIS LU : la machine -7/état 5 == sys-06
  -6 == le noyau INVALID_PARAMETER — les SIX runs mouraient DU
  CONTRAT D'APPEL.
- LA RÉPARATION SELON LA CHARTE : LA RÉVISION 3 DE LA SPEC SYS-06
  (Q3 : AfdFlags = 0, TdiFlags = TDI_RECEIVE_NORMAL 0x20 ; l'erratum
  de lecture n° 1 nommé avec son jugement par le terrain) + le
  README de l'arbre m8 suivi (l'erratum n° 10 tenu) + la notation et
  le brouillon corrigés (le QUATRIÈME champ porte le 0x20, le
  TROISIÈME porte 0 — le même encode 8 o, le slot intact ; auteur.py
  rejoué : 287 o, 71 instructions, 97 o de padding) + LE HARNAIS
  SUIVI (le noyau simulé AFD STRICT refuse le 0x20 en AfdFlags, la
  mutante V4b ré-encodée DANS LES DEUX SENS).
- LA PREUVE RE-PASSÉE : 131 contrôles · 131 VERTS × 3 graines
  (20261105 empreinte 103da725…, 424242 e3281042…, 777777
  283b938c… — zéro échec, les mutantes toutes trahies).
- LA REMISE RÉGÉNÉRÉE (sceau_I.py preparer) : a-signer.txt porte m8
  sys.1 e36141f75ebd8e615c53ff1bd59a4f4cee45b9397eefa66773ffbf54580b
  3536 — README.md ET sys-06-reception.md seuls divergent (DEUX
  fichiers, diff contrôlé) ; les DOUZE autres arbres INCHANGÉS ; la
  balise demeure sys.1 ; le garde relit : m8 CODE 10 — LE SIGNAL,
  pas la panne.
- LA MAIN DU DÉVELOPPEUR RE-SERVIE :
  LISEZMOI-ceremonie-revision3-sys06.txt ÉCRIT (OÙ NOUS EN SOMMES ;
  POURQUOI la révision 3 — LE TERRAIN A JUGÉ LA MESURE ; CE QUI A
  CHANGÉ : m8 e36141f7…, l'empreinte c444d730… PÉRIMÉE ; LA RÈGLE
  D'OR inchangée ; LES CINQ PAS — le pas 3 exige e36141f7… ; CE QUE
  CELA DÉBLOQUE) ; le NOTE_D130 réécrit (maj_kit.py : RACINE_KIT +
  manifeste) — déployés au commit même (hook post-commit).
- L'ARCHIVAGE (archiver_sondesys06.py, modèle archiver_sonde1,
  D143 : par DÉPLACEMENT) : le QUATUOR + LE VERDICT DU RECOUP
  (17/17) → archives-preuves/preuves-sonde-sys06-1/ ; le réceptacle
  ré-armé (son LISEZMOI seul) ; les DEUX index mis à jour ; la
  racine 19 entrées ; les TROIS kits INCHANGÉS (79d44284… +
  215c2caa… + 67e2014d… — AUCUN dépôt).
- FRONTIÈRES : LA FINALE 1.0.0 REFUSÉE pour ce geste (fail-closed —
  le critère exige le vert ; D104 : aucune balise) ; les kits
  INCHANGÉS ; le scellé 0.9.0 INTACT ; la clé privée jamais traversée
  (D87). SUITE : LA TROISIÈME SIGNATURE DU DÉVELOPPEUR (la remise
  e36141f7… à signer HORS LIGNE avec la clé du 04/11 →
  signatures-I.txt + cle-publique-I.txt au /test) — puis deposer, le
  garde 13/13, LE REBUILD 1.0.0-dev.4 (le bloc sys-06 réparé SUR LE
  TERRAIN), LE KIT M9F RÉPARÉ au /test, le run — ET SI LE VERT
  TIENT : LA FINALE 1.0.0, LE JALON M9 — LA GRANDE ŒUVRE.
"""


def main():
    # 1. le plan : la rangée (f) + l'État (idempotent : déjà-fait = constaté)
    plan = PLAN.read_text(encoding="utf-8")
    if "LE RUN DE LA SONDE SYS-06 REÇU ET ANALYSÉ SUR PIÈCES" in plan:
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
        if "LE MOT D'INFORMATION EST VENU" not in plan:
            sys.exit("ÉCHEC : la rangée (f) ne porte pas le constat du geste "
                     "après remplacement")
        if "LA TROISIÈME SIGNATURE DU DÉVELOPPEUR ATTENDUE" not in plan:
            sys.exit("ÉCHEC : l'État ne porte pas la phrase du geste")
        PLAN.write_text(plan, encoding="utf-8")
        print("PLAN : la rangée (f) + l'État du programme — consignés")

    # 2. le journal : l'Entrée 191 avant le marqueur m5a (idempotent)
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 191 —" in journal:
        print("JOURNAL : l'Entrée 191 déjà consignée — constaté")
    else:
        marqueur = "<!-- m5a:journal-des-builds v1"
        if journal.count(marqueur) != 1:
            sys.exit(f"ÉCHEC : le marqueur m5a trouvé "
                     f"{journal.count(marqueur)} fois (attendu : 1)")
        journal = journal.replace(marqueur, ENTREE_191 + marqueur, 1)
        if "## Entrée 191 — LE RUN DE LA SONDE SYS-06 REÇU" not in journal:
            sys.exit("ÉCHEC : l'Entrée 191 absente après remplacement")
        JOURNAL.write_text(journal, encoding="utf-8")
        print("JOURNAL : l'Entrée 191 consignée AVANT le marqueur m5a")

    # 3. le worklog racine : la Task ID 109 à la suite
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 109 —" in worklog:
        sys.exit("ÉCHEC : la Task ID 109 existe déjà (rejeu REFUSÉ)")
    if "## Task ID 108 —" not in worklog:
        sys.exit("ÉCHEC : l'entrée Task ID 108 absente (le geste précédent "
                 "n'est pas consigné)")
    ancre_fin = ("RESET/DISCONNECT le pair).")
    if not worklog.rstrip().endswith(ancre_fin):
        sys.exit("ÉCHEC : le worklog ne se termine pas sur la Task 108 "
                 "attendue (ancre de suite absente)")
    worklog = worklog.rstrip("\n") + "\n" + TASK_109
    if "## Task ID 109 — LE RUN DE LA SONDE SYS-06 REÇU" not in worklog:
        sys.exit("ÉCHEC : la Task ID 109 absente après append")
    WORKLOG.write_text(worklog, encoding="utf-8")
    print("WORKLOG : la Task ID 109 consignée À LA SUITE de la Task 108")


if __name__ == "__main__":
    main()
