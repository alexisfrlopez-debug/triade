#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_184.py — LA CONSIGNATION DU GESTE « LE QUATRIÈME RUN
TERRAIN (f) REÇU (« preuves déposées dans le drive /test ») : LE GESTE (ii)
DU RECOUP-3 ACCOMPLI — LA MACHINE WINDOWS 11 (build 26300) ENFIN ESSAYÉE —
ET LE -6 SE RÉPÈTE À L'IDENTIQUE (le journal du run 4 == celui du run 3,
LIGNE À LIGNE) : LE SUSPECT (a) (la divergence afd.sys Win10 ↔ Win11) EST
ÉLIMINÉ SUR PIÈCES ; LE RECOUP 30/30, LE RUN ARCHIVÉ ; LA SONDE SYS-05
(m9-(g)) — LE CHANTIER PROMIS — EST OUVERTE ET LIVRÉE AU COFFRE (le
trampoline de capture, l'artefact INTACT) » :
JOURNAL_TRAVAIL +Entrée 184 (ordre 183<184<marqueur, rejeu REFUSÉ), worklog
+Task ID 102. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 07/11 (le run : 2026-11-06 19:20:57,
l'heure de la machine du développeur)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 184 — LE QUATRIÈME RUN TERRAIN (f) REÇU (« preuves déposées dans le drive /test ») : LE GESTE (ii) DU RECOUP-3 ACCOMPLI — LA MACHINE WINDOWS 11 (build 26300) ENFIN ESSAYÉE — ET LE -6 SE RÉPÈTE À L'IDENTIQUE (LE JOURNAL DU RUN 4 == CELUI DU RUN 3, LIGNE À LIGNE, LES HORODATEMENTS EXCEPTÉS) : LE SUSPECT (a) — LA DIVERGENCE afd.sys Win10 ↔ Win11 — EST ÉLIMINÉ SUR PIÈCES ; LE RECOUP 30/30, LE RUN ARCHIVÉ ; ET LA SONDE SYS-05 (m9-(g)), LE CHANTIER PROMIS, EST OUVERTE ET LIVRÉE AU COFFRE — LE TRAMPOLINE DE CAPTURE, L'ARTEFACT INTACT (07/11)

**Le geste (ii) du recoup-3 accompli à la lettre — et la réponse du réel est sans appel.** LE RAPATRIEMENT (scripts/ramasse_run4_m9f.py) : le trio INÉDIT au réceptacle (temoin-m9f.txt 2 350 o md5 79c83775…, scenario-m9f-journal.log 605 o md5 2b819ae4…, VERDICT-run-m9f.txt md5 c95fb66e…), md5 aller-retour OK, les pièces T4/T6 JAMAIS NÉES (mort à T3 : cohérence) ; le run : **2026-11-06 19:20:57** — **LA MACHINE A CHANGÉ : Windows 10.0 build 26300 (Windows 11 — Python 3.14.3, ntdll b072efae…) contre Windows 10 build 19045 (Python 3.14.6, ntdll 36b1a62e…) au run 3** ; l'artefact INTACT (d8928934… — LE MÊME), le kit ACQUITTÉ INCHANGÉ (90a1d022…) : SEULE LA MACHINE A CHANGÉ, exactement le geste demandé.

**La répétition à l'identique, CONSTATÉE PAR CODE.** T0 VERT (les SEIZE contrôles [ok]), T1 VERT (SSN 85/7/15, motif 4c8bd1b8 — les MÊMES numéros sur l'AUTRE ntdll), T2 VERT (rax 0, handle 0x280 : sys-04 create+bind+connect traverse VIVANT sur Win11 AUSSI), la clé publique attendue NON-NULLE f650affb… (l'erratum n° 7 toujours réparé), T3.recoup [ok] (le CH == la construction re-jouée, 119 o) — PUIS LA MORT, LA MÊME : sys-05 rend -6 à L'ÉMISSION DU CH à SON PREMIER APPEL RÉEL SUR WINDOWS 11 AUSSI, la machine propage -7, l'état 5. **LA PREUVE PAR CODE (le recoup F1)** : le journal du run 4 est IDENTIQUE au journal DU RUN 3, LIGNE À LIGNE, les horodatements exceptés (le run 3 rapatrié au geste même depuis archives-preuves/preuves-run-m9f-3/) — les SEPT lignes, le même rappel « sys-05 rend -6 » (UN CONSTAT, PAS UN RAPPEL FIXE : relu dans la source, la ligne 578 ne journalise QUE SI r != 0), le même échec nommé, la même branche -7. **LE SUSPECT (a) EST ÉLIMINÉ** : un refus qui ne distingue PAS les générations de noyau n'est PAS une divergence de génération — le refus est INTER-GÉNÉRATIONS, STRUCTUREL au contrat d'appel de sys-05 ou à l'état de l'endpoint.

**Le recoup labo 30/30 (scripts/recouper_run4_m9f.py) — quatre contrôles NEUFS (la série F).** F1 LA RÉPÉTITION PAR CODE ; F2 LES TÉMOINS DIVERGENT SUR L'ENVIRONNEMENT SEULEMENT (Win10 19045 ↔ Win11 26300 : la preuve que la machine a changé) ; F3 LE SUSPECT (a) ÉLIMINÉ ; F4 LA CONNEXION ÉTAIT ÉTABLIE AUX DEUX RUNS (T2 VERT, handle posé : sys-04 Q1 — le connect SYNCHRONE attend le three-way handshake ; l'hypothèse « socket jamais connectée » s'affaiblit). LES CANDIDATS RE-ÉVALUÉS : (b) **LE CONTRAT D'APPEL de sys-05** (l'IOCTL_AFD_SEND 0x1201F / l'AFD_SEND_INFO de 24 o tel que le bloc le pose : un paramètre invalide rend le même refus PARTOUT — le profil correspond) ; (c) **L'ÉTAT DE L'ENDPOINT au moment du send** (un PENDING ou un état de dispositif invalide : le profil correspond aussi) ; (d) **LE PASSAGER réseau INVRAISEMBLABLE** (un serveur muet ferait échouer le CONNECT SYNCHRONE, pas le SEND ; et le refus est identique sur deux machines, deux générations, deux réseaux). **→ LE NTSTATUS BRUT (que l'instrument NE REMONTE PAS : il vit dans rdx, sys-05 Q5) DÉPARTAGE (b) de (c) : UNE SEULE INFORMation MANQUE — LA SONDE LA LIT.**

**LA SONDE SYS-05 (m9-(g)) — le chantier promis, OUVERT ET LIVRÉ dans le même geste.** tls13/terrain/scenario-sonde-sys05.py + LISEZMOI-KIT-SONDE-SYS05.md : la mission est LIRE LE NTSTATUS BRUT DE L'ÉMISSION, la limite NOMMÉE de l'instrument, **franchie par UN TRAMPOLINE DE CAPTURE — l'artefact INTACT, JAMAIS reconstruit** : 33 octets posés au run (VirtualAlloc, le MÊME geste que le trampoline NtClose du kit m9f T6 : « ctypes ne peut pas charger rax, le trampoline le fait » — ici : ctypes ne peut pas LIRE rdx, le trampoline le rend) qui APPELLE LE MÊME BLOC sys-05 à son adresse scellée et rend (le code de rax) EMPAQUETÉ avec (le NTSTATUS de rdx) — `sub rsp,0x28 ; mov rax,sys-05 ; call rax ; shl rdx,32 ; mov ecx,eax ; or rcx,rdx ; mov rax,rcx ; add rsp,0x28 ; ret` (l'ABI msx64 démontrée : shadow space + pile alignée au call ; le dépaquetage éprouvé au labo sur les QUATRE cas — le signe 32 bits, PENDING, le compte partiel, le succès). **LE COMPAS AVANT LA MESURE** (un handle invalide 0xDEAD0000 → -6 + STATUS_INVALID_HANDLE 0xC0000008 attendu : la preuve que la capture lit VRAIMENT rdx — un compas muet arrête la sonde, fail-closed) ; **LA MESURE** (le CH DE RÉFÉRENCE du jalon, 119 o, par le trampoline : LE NTSTATUS ENFIN LU ET NOMMÉ) ; **LES VARIATIONS** (la TAILLE : un octet sur session sacrifiée ; le DÉLAI : le CH re-tenté après 2 s) ; **LA CONTRE-ÉPREUVE S4** (la poignée par LE RAPPEL STANDARD sur une session NEUVE — si le refus disparaît : LA PERCÉE, la ligne suit DANS LE MÊME RUN) ; **LA TABLE NTSTATUS** (23 noms recoupés aux sources canoniques ntstatus.h — Wine ET ReactOS s'accordent au bit près, vérifiés au labo le 07/11 : les valeurs qui corrigent les fausses mémoires, INVALID_DEVICE_STATE = 0xC0000184, CONNECTION_RESET = 0xC000020D — la CLASSE de sévérité tranche : un PENDING ou un AVERTISSEMENT traité en -6 serait LE BUG DU CONTRAT, pas un refus du noyau).

**L'assemblage et la livraison.** assembler_kit_sondesys05.py : le recoup PAR AST de 29 constantes == l'artefact/le plan/la sonde, **LES PORTES passées** (l'erratum n° 7 hérité : aucune écriture `.raw[...]`, LE site OUVRIR au POINTEUR, l'échelle contre les vecteurs officiels RFC 7748 § 6.1 Alice/Bob + le couple RFC 8448 § 3 + 16 clés semées contre ref_x25519 ; PLUS LES QUATRE PORTES DE LA SONDE : S1 le squelette du trampoline EXACT + la pose par découpe, S2 la table NTSTATUS == la référence canonique, S3 LE COMPAS AVANT LA MESURE, S4 le témoin écrit au fil du run), py_compile, l'extraction vierge VERT — kit-sonde-sys05.zip (37 012 o, md5 215c2caa…, sha256 cc917600…). deposer_kit_sondesys05.py : **LA VAGUE M9F DEMEURE** (kit-m9f.zip 90a1d022… recoupé INTACT — la finale 1.0.0 attend toujours LE RUN m9f), kit-sonde-sys05.zip + LISEZMOI-sonde-sys05.txt à la racine, preuves-sonde-sys05/ NÉ avec son LISEZMOI-preuves.txt, l'index des livraisons mis à jour, la racine 16 entrées vérifiée.

**Le geste au développeur — un seul envoi.** Dézipper kit-sonde-sys05.zip dans un dossier NEUF, `python scenario-sonde-sys05.py` (Python 64 bits, réseau vivant ; Windows 11 OU Windows 10 — le refus constaté est inter-générations), ~15 s (le délai de 2 s volontaire : la variation DÉLAI), puis renvoyer preuves-sonde-sys05/ ENTIER au coffre /test/preuves-sonde-sys05/ — VERT-MESURE, PERCÉE ou ROUGE nommé : le labo recoupe (D138/D145/D148), NOMME le coupable (le contrat du bloc sys-05, l'état de l'endpoint, ou le réseau) et répare selon la charte : **l'erratum de la notation + la révision 2 de la spec sys-05 le cas échéant, jamais une dérive silencieuse** — puis le run m9f réparé suivra, et avec lui la finale 1.0.0.

**Détail.** LE RUN ARCHIVÉ (scripts/archiver_run4_m9f.py) : preuves-run-m9f-4/ créé dans archives-preuves/ (D99), le trio DU RUN DÉPLACÉ (D143 : un déplacement, jamais un jet), le VERDICT-recoup-labo-m9f-4.txt déposé AVEC les pièces (l'archive porte le jugement : 30/30), preuves-m9f/ ré-armé (son LISEZMOI seul), les DEUX INDEX mis à jour, la racine vérifiée (13 entrées puis 16 après la livraison de la sonde). FRONTIÈRES : le kit m9f du /test INCHANGÉ (90a1d022…), l'artefact INTACT (d8928934… re-haché au geste même — la sonde ne reconstruit RIEN), le scellé 0.9.0 INTACT, AUCUNE balise posée (la finale 1.0.0 attend le VERT — D104), la clé privée jamais traversée (D87), les archives des runs 1/2/3 INTACTES. Livrables : download/preuves-run-m9f-4/ (le trio + le verdict du recoup), download/kit-sonde-sys05.zip (le kit sonde). Consignations : la présente Entrée 184 PAR SCRIPT, PLAN (maj_plan_m9q.py : la rangée (f) + l'État du programme), worklog +Task ID 102. SUITE : LE GESTE DU DÉVELOPPEUR SUR LA SONDE — puis le recoup, le coupable NOMMÉ, la réparation selon la charte — et si la percée tient : le run m9f réparé, LA FINALE 1.0.0, le jalon M9 franchi — LA GRANDE ŒUVRE."""

TASK = """## Task ID 102 — LE QUATRIÈME RUN TERRAIN (f) REÇU (« preuves déposées dans le drive /test ») : LE GESTE (ii) ACCOMPLI (Windows 11 build 26300) ET LE -6 SE RÉPÈTE À L'IDENTIQUE — LE SUSPECT (a) ÉLIMINÉ SUR PIÈCES (le refus est INTER-GÉNÉRATIONS) ; LE RECOUP 30/30, LE RUN ARCHIVÉ ; LA SONDE SYS-05 (m9-(g)) OUVERTE ET LIVRÉE AU COFFRE — LE TRAMPOLINE DE CAPTURE, L'ARTEFACT INTACT (07/11)

Work Log:
- LE RAPATRIEMENT : le trio INÉDIT (temoin 79c83775… 2 350 o, journal
  2b819ae4… 605 o SEPT lignes, verdict c95fb66e…), md5 aller-retour OK ;
  le run : 2026-11-06 19:20:57 — LA MACHINE CHANGÉE : Windows 11 build
  26300 (Python 3.14.3, ntdll b072efae…) contre Win10 19045 au run 3 ;
  l'artefact INTACT (d8928934…), le kit ACQUITTÉ INCHANGÉ (90a1d022…).
- LA RÉPÉTITION CONSTATÉE PAR CODE (F1) : le journal du run 4 == celui
  du run 3, LIGNE À LIGNE, horodatements exceptés (le run 3 rapatrié du
  coffre au geste même) ; les témoins ne divergent QUE sur
  l'environnement (F2) — le rappel « sys-05 rend -6 » est UN CONSTAT
  (relu dans la source : la ligne 578 ne journalise QUE SI r != 0), pas
  un rappel fixe.
- LE SUSPECT (a) ÉLIMINÉ (F3) : le même -6 à l'émission du CH sur les
  DEUX GÉNÉRATIONS — un refus qui ne distingue pas les générations
  n'est pas une divergence de génération : STRUCTUREL au contrat
  d'appel de sys-05 ou à l'état de l'endpoint ; F4 : la connexion était
  ÉTABLIE aux deux runs (T2 VERT, handle posé, le connect SYNCHRONE de
  sys-04 Q1).
- LE RECOUP LABO 30/30 (recouper_run4_m9f.py) : l'échelle REJOUÉE sur
  la clé privée DU RUN (c3184909… → f650affb… == le témoin), la
  construction CH re-jouée (114 o, le vol 119 o), la chaîne -6 → -7
  reconstituée, la frontière nommée d'avance réalisée DEUX FOIS ; LES
  CANDIDATS RE-ÉVALUÉS : (b) le contrat d'appel, (c) l'état de
  l'endpoint, (d) le passager INVRAISEMBLABLE — LE NTSTATUS BRUT qui
  vit dans rdx DÉPARTAGE : la sonde le lit.
- LA SONDE SYS-05 (m9-(g)) OUVERTE : scenario-sonde-sys05.py — LE
  TRAMPOLINE DE CAPTURE (33 o, l'ABI msx64 démontrée, le dépaquetage
  éprouvé sur QUATRE cas) appelle LE MÊME BLOC sys-05 et rend le code
  ET le NTSTATUS ; LE COMPAS AVANT LA MESURE (handle invalide → -6 +
  0xC0000008 attendu : fail-closed) ; LA MESURE (le CH de référence,
  119 o) ; LES VARIATIONS (taille : un octet sur session sacrifiée ;
  délai : 2 s) ; LA CONTRE-ÉPREUVE S4 (la poignée par LE RAPPEL
  STANDARD sur session NEUVE — si le refus disparaît : LA PERCÉE, la
  ligne suit DANS LE MÊME RUN) ; LA TABLE NTSTATUS recoupée aux sources
  canoniques (Wine ET ReactOS au bit près — la classe de sévérité
  tranche : un PENDING traité en -6 serait LE BUG DU CONTRAT).
- L'ASSEMBLAGE (assembler_kit_sondesys05.py) : 29 constantes recoupées
  PAR AST, LES PORTES passées (l'erratum n° 7 hérité + S1 le squelette
  EXACT + S2 la table canonique + S3 le compas avant la mesure + S4 le
  témoin vivant), l'extraction vierge VERT — kit-sonde-sys05.zip
  (37 012 o, md5 215c2caa…, sha256 cc917600…).
- LA LIVRAISON (deposer_kit_sondesys05.py) : LA VAGUE M9F DEMEURE
  (kit-m9f.zip 90a1d022… recoupé INTACT — la finale attend LE RUN
  m9f), kit-sonde-sys05.zip + LISEZMOI-sonde-sys05.txt à la racine,
  preuves-sonde-sys05/ NÉ avec son LISEZMOI, l'index mis à jour, la
  racine 16 entrées.
- LE RUN ARCHIVÉ (archiver_run4_m9f.py) : preuves-run-m9f-4/ (le trio
  DÉPLACÉ + le verdict 30/30 AVEC), preuves-m9f/ ré-armé, les DEUX
  index, le kit recoupé INCHANGÉ.
- LE GESTE AU DÉVELOPPEUR : python scenario-sonde-sys05.py (Python 64
  bits, réseau vivant, Win11 OU Win10), puis preuves-sonde-sys05/
  ENTIER au coffre — le labo recoupe, NOMME le coupable (le contrat du
  bloc, l'état de l'endpoint, ou le réseau) et répare selon la charte
  (l'erratum de la notation + la révision 2 de la spec sys-05 le cas
  échéant — jamais une dérive silencieuse).
- FRONTIÈRES : l'artefact INTACT (la sonde ne reconstruit RIEN — relu
  d8928934…), le scellé 0.9.0 INTACT, AUCUNE balise (la finale attend
  le VERT), les archives des runs 1/2/3 intactes ; livrables :
  download/preuves-run-m9f-4/ + download/kit-sonde-sys05.zip ;
  consignations : Entrée 184 PAR SCRIPT, PLAN (maj_plan_m9q.py :
  rangée (f) + État), worklog +Task ID 102.
- SUITE : LE GESTE DU DÉVELOPPEUR SUR LA SONDE — puis le recoup, le
  coupable NOMMÉ, la réparation — et si la percée tient : le run m9f
  réparé, LA FINALE 1.0.0 — LA GRANDE ŒUVRE.

Stage Summary:
- LE GESTE (ii) DU RECOUP-3 EST ACCOMPLI ET LE RÉEL A RÉPONDU : le
  même kit, la même offre PARFAITE, sur Windows 11 — le même refus -6
  à l'émission du CH, à l'identique, journal pour journal : la
  divergence afd.sys Win10 ↔ Win11 est ÉLIMINÉE, le refus est
  INTER-GÉNÉRATIONS.
- IL NE RESTE QU'UNE INFORMATION MANQUANTE — LE NTSTATUS BRUT qui vit
  dans rdx (la limite NOMMÉE de l'instrument, sys-05 Q5) — ET LA SONDE
  SYS-05 EST LIVRÉE POUR LA LIRE : le trampoline de capture (l'artefact
  INTACT), le compas étalonné, la table canonique, les variations, et
  la contre-épreuve qui enchaîne la poignée si le refus disparaît.
- LE KIT M9F DEMEURE ACQUITTÉ ET EN PLACE : la finale 1.0.0 attend
  toujours LE RUN m9f — la sonde est l'instrument du diagnostic, la
  réparation suivra la charte (l'erratum de la notation + la
  révision 2 de la spec le cas échéant), jamais une dérive
  silencieuse."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 184" in journal:
        sys.exit("ÉCHEC : Entrée 184 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 183" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 183 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i183 = journal.index("## Entrée 183")
    im = journal.index(MARQUEUR)
    if not (i183 < im):
        sys.exit("ÉCHEC : l'ordre 183<marqueur est rompu")
    if "## Entrée 184" in journal[i183:im]:
        sys.exit("ÉCHEC : état inattendu entre 183 et le marqueur")
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 102" in worklog:
        sys.exit("ÉCHEC : Task ID 102 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 101" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 101 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 184 déposée au journal "
          "(ordre 183<184<marqueur)")
    print("[consignation] Task ID 102 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 183") < j.index("## Entrée 184") < j.index(MARQUEUR)
    assert "## Entrée 184" in j and "build 26300" in j and "f650affb" in j
    assert "ÉLIMINÉ" in j and "INTER-GÉNÉRATIONS" in j
    assert "30/30" in j and "preuves-run-m9f-4" in j
    assert "SONDE SYS-05" in j and "215c2caa" in j
    assert "## Task ID 102" in w and w.index("## Task ID 101") < w.index("## Task ID 102")
    assert "TRAMPOLINE" in w and "COMPAS" in w
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
