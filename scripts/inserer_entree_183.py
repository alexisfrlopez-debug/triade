#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_183.py — LA CONSIGNATION DU GESTE « LE TROISIÈME RUN TERRAIN
(f) REÇU : ROUGE T3.ouvrir NOMMÉ — MAIS LE RECOUP DU JALON VERT (le
ClientHello de LA MACHINE == la référence octet pour octet, 119 o) ET LA
RÉPARATION DE L'ERRATUM n° 7 PROUVÉE SUR LA MACHINE RÉELLE ; la mort nommée à
sys-05 (son PREMIER appel réel) ; le kit ACQUITTÉ, le run archivé AVEC le
verdict du recoup 26/26 ; LA RELANCE EST LE GESTE SUIVANT » :
JOURNAL_TRAVAIL +Entrée 183 (ordre 182<183<marqueur, rejeu REFUSÉ), worklog
+Task ID 101. Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit.

La datation : la présente porte le 06/11 au soir, deuxième geste de la soirée
(le run : 2026-11-06 18:49:34, l'heure de la machine du développeur — SIX
MINUTES après le dépôt du kit corrigé 18:43 Paris)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 183 — LE TROISIÈME RUN TERRAIN (f) REÇU (« preuves deposees dans le drive /test ») : ROUGE T3.ouvrir NOMMÉ — MAIS LE RECOUP DU JALON VERT (LE ClientHello DE LA MACHINE == LA RÉFÉRENCE OCTET POUR OCTET, 119 o — LA PREUVE CRYPTOGRAPHIQUE DU JALON SUR LA MACHINE RÉELLE) ET LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE ; LA MORT NOMMÉE À sys-05 (SON PREMIER APPEL RÉEL) ; LE KIT ACQUITTÉ, LE RUN ARCHIVÉ AVEC LE VERDICT DU RECOUP 26/26 — LA RELANCE EST LE GESTE SUIVANT (06/11 au soir, deuxième geste)

**Le kit corrigé exécuté SIX MINUTES après son dépôt — et le programme n'a jamais été aussi loin.** LE RAPATRIEMENT (scripts/rapatrier_preuves_m9f.py) : le TRIO complet au réceptacle (temoin-m9f.txt 2 349 o md5 f8491dc2…, scenario-m9f-journal.log 605 o md5 03e555c8…, VERDICT-run-m9f.txt 2 740 o md5 b9d79a0c…), les pièces T4/T6 JAMAIS NÉES (nées à T4/T6 : cohérentes avec une mort à T3 — l'absence est CONSTATÉE, jamais un mystère) ; le run : **2026-11-06 18:49:34** (l'heure de la machine du développeur — la correction poussée à 18:43 Paris, le kit corrigé md5 90a1d022… exécuté TEL QUEL).

**La réparation de l'erratum n° 7 PROUVÉE sur la machine réelle — et le recoup du jalon, VERT.** T0 VERT (les SEIZE contrôles [ok] : l'artefact d8928934… ASSERTÉ avant tout geste, l'octet de l'erratum n° 5 relu, le VRAI ntdll haché 36b1a62e…), T1 VERT (SSN 85/7/15, motif 4c8bd1b8), T2 VERT (rax 0, handle 0x328 : le VRAI afd.sys franchi) — PUIS T3, le segment qui tua le run 2, TRAVERSÉ VIVANT : l'aléa (8b049cad…), la clé privée (927f6ec8…), **la clé publique attendue NON-NULLE 89d50a86…** (le run 2 imprimait 000…0 : l'échelle réparée est la bonne — l'échelle REJOUÉE au labo sur la clé privée DU RUN rend EXACTEMENT la clé du témoin), la machine appelée AU POINTEUR — ET **T3.recoup [ok] : le CH émis == 16 03 03 00 72 || la construction re-jouée (119 o)** — LE ClientHello COMPOSÉ PAR LA MACHINE (tls13-22 + tls13-14 + la famille f25519, LES BLOCS SCELLÉS) == LA RÉFÉRENCE DU DÉPÔT OCTET POUR OCTET : les DEUX lecteurs d'accord, la preuve cryptographique du jalon SUR LA MACHINE RÉELLE.

**La mort nommée — la preuve en une ligne.** Le journal (SEPT lignes, toutes à 18:49:34 — le run entier dans SA seconde) : « le rappel émission : sys-05 rend -6 (l'émission TOTALE ou refusée — jamais un demi-envoi déguisé) » AU TEXTE EXACT DE LA SOURCE, puis « T3 : -7 LE TRANSPORT EN ÉCHEC — le serveur n'a rien servi après l'offre (réseau coupé ?) : réessayez réseau vivant » AU TEXTE EXACT — l'état 5 (MORT), le verdict ROUGE un échec nommé : T3.ouvrir. **LA PREUVE EN UNE LIGNE (le recoup B8/C4)** : l'append du rappel d'émission PRÉCÈDE l'envoi (relu dans la source au geste même) et la ligne « [T3] la dernière émission : 58 o » est ABSENTE du témoin → **UNE SEULE émission fut tentée, CELLE DU CH** : l'offre est PARFAITE en composition, son ENVOI fut REFUSÉ par le transport — le CH n'a pas quitté la machine (l'émission TOTALE ou refusée). LA CHAÎNE : sys-05 rend -6 (un NTSTATUS non nul — **l'information exacte vit dans rdx**, la limite NOMMÉE de l'instrument : ctypes ne restitue que rax) → la machine propage -7 (tls13-27 Q2), l'état 5. **L'ÉTAPE NOMMÉE : sys-05, L'ÉMISSION — à SON PREMIER APPEL RÉEL** (les runs 1/2 morts avant ; le labo n'a que le MODÈLE STRICT du noyau, 131 contrôles — les mesures du socle viennent de Windows 11, leftarcode 2025).

**Le recoup labo 26/26 (scripts/recouper_run3_m9f.py) — ROUGE CONSTATÉ COHÉRENT, LE KIT ACQUITTÉ.** Les candidats NOMMÉS (évidence avant correctif — D54/D68/D98) : (a) **LA DIVERGENCE afd.sys Windows 10 ↔ Windows 11** — les TROIS runs ont lieu sur Windows 10 22H2 build 19045, sys-04 (create/bind/connect) PASSE sur Win10 mais sys-05 (SEND) est refusé à son premier appel : le suspect que le LISEZMOI § les frontières avait nommé AU MOT PRÈS (« si votre afd.sys diverge, le refus sera NOMMÉ (-6, l'étape en cause) — un échec honnête vaut plus qu'un vert muet ») ; (b) **LA CONNEXION REFERMÉE côté serveur** (un RST entre le connect et l'envoi — le serveur, un intermédiaire, une garde locale) ; (c) **LE PASSAGER réseau**. L'HORLOGE ne départage pas (le run entier dans SA seconde) et le NTSTATUS vit dans rdx : **UNE RELANCE tranche (c)** ; **la répétition à l'identique du -6 à l'émission du CH INSTALLE (a) en suspect principal**. LE KIT EST ACQUITTÉ cette fois POUR DE BON : le scénario exécuté fidèlement (la source réparée == le kit du coffre 90a1d022…, relu à la passation), l'offre de la machine PARFAITE sur pièces — RIEN ne condamne le kit ; la frontière est L'ARTEFACT contre le VRAI afd.sys, nommée d'avance.

**Le geste rendu au développeur — trois temps, un seul envoi.** (i) **RELANCER le kit TEL QUEL**, réseau vivant (`python scenario-m9f.py`, ~10 s — un réseau passager se distingue d'un refus structurel par UNE relance) ; (ii) **SI LE -6 SE RÉPÈTE À L'IDENTIQUE** (même étape, même seconde, l'émission du CH) : la divergence afd.sys Windows 10 ↔ Windows 11 devient le suspect principal — essayer une machine **Windows 11** (la cible du kit : les mesures AFD WinDbg en proviennent) si disponible, OU renvoyer les pièces : **le labo ouvre la sonde sys-05** (mesurer IOCTL_AFD_SEND sur le vrai noyau — le chantier futur nommé) ; (iii) DANS TOUS LES CAS : renvoyer preuves-m9f/ ENTIER au coffre — le VERT comme le ROUGE nommé : le labo recoupe (D138/D145/D148) et, si les pièces établissent le critère, **LA FINALE 1.0.0 est posée (fait de carte, D104) : le jalon M9 franchi — LA GRANDE ŒUVRE**.

**Détail.** LE RUN ARCHIVÉ (scripts/archiver_run3_m9f.py) : preuves-run-m9f-3/ créé dans archives-preuves/ (D99 : jamais mélanger les runs), le trio DU RUN DÉPLACÉ (D143 : un déplacement, jamais un jet), le VERDICT-recoup-labo-m9f-3.txt déposé AVEC les pièces (md5 9941d303… — l'archive porte le jugement : ROUGE CONSTATÉ COHÉRENT 26/26), preuves-m9f/ ré-armé (son LISEZMOI seul), les DEUX INDEX mis à jour, la racine vérifiée (13 entrées). FRONTIÈRES : le kit du /test INCHANGÉ (md5 90a1d022… — ACQUITTÉ, relu après le geste), l'artefact INTACT (d8928934… re-haché au geste même), le scellé 0.9.0 INTACT, les arbres I inchangés, AUCUNE balise posée (la finale 1.0.0 attend le VERT — D104), la clé privée jamais traversée (D87), les archives des runs 1/2 INTACTES. Livrables : download/preuves-run-m9f/ (le trio rapatrié) + download/preuves-run-m9f-3/ (le miroir local de l'archive avec le verdict du recoup). Consignations : la présente Entrée 183 PAR SCRIPT, PLAN (maj_plan_m9p.py : la rangée (f) + l'État du programme), worklog +Task ID 101. SUITE : LA RELANCE DU DÉVELOPPEUR — preuves-m9f/ ENTIER au coffre → le recoup → si vert : LA FINALE 1.0.0 (fait de carte — D104) : le jalon M9 franchi — LA GRANDE ŒUVRE."""

TASK = """## Task ID 101 — LE TROISIÈME RUN TERRAIN (f) REÇU (« preuves deposees dans le drive /test ») : ROUGE T3.ouvrir NOMMÉ (sys-05 rend -6 à SON PREMIER APPEL RÉEL — l'émission du CH refusée par le transport) — MAIS LE RECOUP DU JALON VERT (le ClientHello de LA MACHINE == la référence octet pour octet, 119 o) ET LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE ; LE KIT ACQUITTÉ, LE RUN ARCHIVÉ AVEC LE VERDICT DU RECOUP 26/26 — LA RELANCE EST LE GESTE SUIVANT (06/11 au soir, deuxième geste)

Work Log:
- LE RAPATRIEMENT : le TRIO complet au réceptacle (temoin f8491dc2…,
  journal 03e555c8… 605 o SEPT lignes, verdict b9d79a0c…), les pièces
  T4/T6 jamais nées (mort à T3 : cohérence constatée) ; le run :
  2026-11-06 18:49:34, l'heure de la machine du développeur — SIX
  MINUTES après le dépôt du kit corrigé (18:43 Paris).
- LA RÉPARATION PROUVÉE : T0/T1/T2 VERT (les SEIZE T0, SSN 85/7/15,
  handle 0x328), la clé publique attendue NON-NULLE 89d50a86… (le run 2
  imprimait 000…0), le segment qui tua le run 2 TRAVERSÉ VIVANT, la
  machine appelée AU POINTEUR.
- LE RECOUP DU JALON, VERT : T3.recoup [ok] — le CH COMPOSÉ PAR LA
  MACHINE (les blocs scellés tls13-22 + tls13-14 + f25519) == la
  construction re-jouée OCTET POUR OCTET (119 o) : les DEUX lecteurs
  d'accord — LA PREUVE CRYPTOGRAPHIQUE DU JALON SUR LA MACHINE RÉELLE.
- LA MORT NOMMÉE : sys-05 rend -6 (un NTSTATUS non nul — l'information
  vit dans rdx, la limite NOMMÉE de l'instrument) à L'ÉMISSION, SON
  PREMIER APPEL RÉEL → la machine propage -7 LE TRANSPORT EN ÉCHEC,
  état 5 ; LA PREUVE EN UNE LIGNE : la ligne « [T3] la dernière
  émission » ABSENTE du témoin et l'append du rappel PRÉCÈDE l'envoi →
  UNE SEULE émission tentée, CELLE DU CH : l'offre PARFAITE en
  composition, son envoi REFUSÉ.
- LE RECOUP LABO 26/26 (recouper_run3_m9f.py) : l'échelle REJOUÉE sur
  la clé privée DU RUN rend la clé du témoin ; la construction CH
  re-jouée (114 o, le vol 119 o) ; la chaîne -6 → -7 reconstituée
  depuis les contrats ; le LISEZMOI avait nommé la frontière AU MOT
  PRÈS ; LE KIT ACQUITTÉ (exécuté fidèlement, l'offre parfaite — le
  kit du /test INCHANGÉ 90a1d022…).
- LES CANDIDATS NOMMÉS : (a) la divergence afd.sys Windows 10 ↔
  Windows 11 (les mesures du socle viennent de Win11 ; sys-04 passe
  sur Win10, sys-05 refusé à son premier appel) ; (b) la connexion
  refermée côté serveur (RST) ; (c) le passager réseau — l'horloge ne
  départage pas (le run entier dans SA seconde), le NTSTATUS vit dans
  rdx : UNE RELANCE tranche (c), la répétition à l'identique installe
  (a).
- LE RUN ARCHIVÉ (archiver_run3_m9f.py) : preuves-run-m9f-3/ (le trio
  DÉPLACÉ + le verdict 26/26 déposé AVEC), preuves-m9f/ ré-armé, les
  DEUX index, la racine 13 entrées, le kit ACQUITTÉ recoupé INCHANGÉ.
- LE GESTE RENDU : (i) RELANCER le kit TEL QUEL, réseau vivant ; (ii)
  si le -6 se répète À L'IDENTIQUE à l'émission du CH : Windows 11 si
  disponible (la cible du kit), ou renvoyer les pièces — le labo
  ouvre LA SONDE sys-05 (le chantier futur nommé) ; (iii) preuves-m9f/
  ENTIER au coffre → si vert : LA FINALE 1.0.0, le jalon M9 franchi —
  LA GRANDE ŒUVRE.
- FRONTIÈRES : l'artefact INTACT (d8928934… re-haché au geste), le
  scellé 0.9.0 INTACT, AUCUNE balise (la finale attend le VERT), les
  archives des runs 1/2 intactes ; livrables :
  download/preuves-run-m9f-3/ (l'archive locale avec le verdict du
  recoup) ; consignations : Entrée 183 PAR SCRIPT, PLAN
  (maj_plan_m9p.py : rangée (f) + État), worklog +Task ID 101.
- SUITE : LA RELANCE DU DÉVELOPPEUR — puis le recoup, et si vert : LA
  FINALE 1.0.0 — LA GRANDE ŒUVRE.

Stage Summary:
- LE TROISIÈME RUN EST LE PLUS LOIN DU PROGRAMME : la réparation de
  l'erratum n° 7 PROUVÉE sur la machine réelle, ET le recoup du jalon
  VERT — le ClientHello composé PAR LA MACHINE (les blocs scellés)
  égale la référence octet pour octet : la preuve cryptographique du
  jalon tient SUR LE TERRAIN.
- LA MORT EST NOMMÉE À LA FRONTIÈRE QUI L'ÉTAIT D'AVANCE : sys-05
  (l'émission) rend -6 à son PREMIER appel réel — le NTSTATUS vit
  dans rdx (la limite nommée de l'instrument) ; le kit est ACQUITTÉ,
  l'artefact INTACT : la frontière est l'artefact contre le VRAI
  afd.sys (les mesures viennent de Windows 11, les runs ont lieu sur
  Windows 10).
- LE GESTE SUIVANT EST UNE RELANCE (un réseau vivant distingue le
  passager du structurel) ; si le -6 se répète à l'identique : la
  divergence afd.sys devient le suspect principal — Windows 11, ou la
  sonde sys-05 au labo ; et si le vert tient : LA FINALE 1.0.0, le
  jalon M9 franchi — LA GRANDE ŒUVRE."""


def main():
    if not JOURNAL.exists():
        sys.exit("ÉCHEC : journal introuvable")
    journal = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 183" in journal:
        sys.exit("ÉCHEC : Entrée 183 déjà consignée (rejeu REFUSÉ)")
    if "## Entrée 182" not in journal:
        sys.exit("ÉCHEC : ancrage Entrée 182 introuvable")
    if MARQUEUR not in journal:
        sys.exit("ÉCHEC : marqueur introuvable")
    i182 = journal.index("## Entrée 182")
    im = journal.index(MARQUEUR)
    if not (i182 < im):
        sys.exit("ÉCHEC : l'ordre 182<marqueur est rompu")
    if "## Entrée 183" in journal[i182:im]:
        sys.exit("ÉCHEC : état inattendu entre 182 et le marqueur")
    journal = journal[:im] + ENTREE + "\n\n" + journal[im:]
    JOURNAL.write_text(journal, encoding="utf-8")

    if not WORKLOG.exists():
        sys.exit("ÉCHEC : worklog introuvable")
    worklog = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 101" in worklog:
        sys.exit("ÉCHEC : Task ID 101 déjà consigné (rejeu REFUSÉ)")
    if "## Task ID 100" not in worklog:
        sys.exit("ÉCHEC : ancrage Task ID 100 introuvable")
    worklog = worklog.rstrip("\n") + "\n\n" + TASK + "\n"
    WORKLOG.write_text(worklog, encoding="utf-8")

    print("[consignation] Entrée 183 déposée au journal "
          "(ordre 182<183<marqueur)")
    print("[consignation] Task ID 101 déposé au worklog")
    print("[consignation] la relecture fait foi :")
    j = JOURNAL.read_text(encoding="utf-8")
    w = WORKLOG.read_text(encoding="utf-8")
    assert j.index("## Entrée 182") < j.index("## Entrée 183") < j.index(MARQUEUR)
    assert "## Entrée 183" in j and "89d50a86" in j and "T3.recoup" in j
    assert "sys-05" in j and "UNE SEULE émission" in j
    assert "26/26" in j and "preuves-run-m9f-3" in j
    assert "## Task ID 101" in w and w.index("## Task ID 100") < w.index("## Task ID 101")
    assert "LA RELANCE" in w and "PREUVE EN UNE LIGNE" in w
    print("[consignation] ORDRE et ANCRAGES constatés — rien d'autre n'a bougé")
    return 0


if __name__ == "__main__":
    sys.exit(main())
