#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_164.py — LA CONSIGNATION DU GESTE « FINALE 0.9.0 SCELLÉE » :
JOURNAL_TRAVAIL +Entrée 164 (ordre 163<164<marqueur, rejeu REFUSÉ),
DECISIONS +D165 (à la suite de D164), worklog +Task ID 82, PLAN (le jalon M8
FRANCHI — la ligne du jalon, la ligne du chantier (d), l'État du programme).
Tout ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit (atomicité du script)."""

import sys

# ---------------------------------------------------------------- Entrée 164 --
ENTREE = """## Entrée 164 — « preuves m8d déposées dans le drive /test » : LE RUN TERRAIN M8-(d) VERT SUR PIÈCES, LE RECOUP LABO VERT 30/30 SUR PIÈCES CROISÉES, LA FINALE 0.9.0 SCELLÉE — LE JALON M8 FRANCHI (05/11)

**Le run rejoué du développeur (kit corrigé ad6cbffe… — la ligne 207 n'est plus).** Le témoin temoin-m8d.txt (run du 2026-11-05 12:10:03, heure locale) : Windows 10.0 build 26300 · Python 3.13.9 · AMD64 ; le VRAI ntdll (base, chemin System32, sha256 b072efae… du fichier) consigné ; l'artefact ASSERTÉ (1492b0bc…, 44 544 o) ; T0-T3 ENTIERS — 30 constats [ok] aux noms de la source, 4 [env], 1 [pièce], ZÉRO [ÉCHEC], « Contrôles : 35 verts · 0 échecs », VERDICT : VERT. Le SSN(NtWriteFile) rendu par les DEUX lecteurs indépendants (la marche EAT Python et le bloc sys-02 : parité bloc == python), le second nom NtReadFile DISTINCT (jamais un numéro en cache), le stub confronté (4C 8B D1 B8 avant l'imm32), le module forgé crocheté REFUSÉ (-4), le ntdll relu inchangé (I8), LA TWIN (chemin-a par l'IAT kernel32 == chemin-b par NtWriteFile en syscall direct == le fixture 33 octets), le refus nommé -1 sur pièce VIDE (I5 : aucun syscall émis), proxy.exe relu inchangé.

**Le recoup labo (scripts/recouper_run_m8d.py — le juge est le code).** Les SIX pièces + le kit rapatriés du coffre /test/preuves-m8d/ (md5 contrôlés par le rapatriement, RE-contrôlés au recoup). TRENTE contrôles tranchés : A les pièces md5 ; B le témoin (titre, date POSTÉRIEURE au correctif, machine/ère, artefact == scellé, ntdll, LE SSN croisé tête/[pièce]/parité/verdict, LE STUB consigné — le motif == MOTIF_STUB de la source et l'imm32 == LE SSN : le numéro RE-LU du stub, jamais cru ; le second nom distinct, la falsification -4, les 30 [ok] aux noms de la source dans l'ordre, le compte 35/0) ; C le journal (2 o — MINCE PAR CONSTRUCTION : journal() n'est jamais appelé par la source, le témoin porte le run entier ; un contenu autre serait l'anomalie) ; D le verdict croisé ; E les fichiers du geste RE-CONTRÔLÉS octet par octet au labo (a == b == le fixture RE-IMPORTÉ, md5 c64ab06b…, le sha du fixture RECALCULÉ == le constat T2.TWIN dd307b39… ; la pièce du refus VIDE) ; F le labo parle (l'artefact du dépôt INTACT re-calculé, le kit du coffre == le corrigé éprouvé, le zip porte scenario-m8d.py et proxy.exe OCTET POUR OCTET le dépôt — la chaîne du scellé). **DEUX DÉFAUTS D'INSTRUMENT NOMMÉS PAR LE FAIL-CLOSED, corrigés et rejoués, les pièces immuables (md5 de part et d'autre — D154 appliqué au recoup lui-même)** : (1) le « $ » sans re.M ne matchait pas la ligne [pièce] en plein milieu du témoin (B6 ÉCHEC au premier passage) ; (2) la tranche de sortie r.lignes[4:] AMPUTAIT le premier PASS « A : temoin-m8d.txt » du verdict écrit — c'est LE SCELLAGE qui l'a attrapé (l'attestation des six pièces). VERDICT : RECOUP VERT 30/30 — la finale 0.9.0 DÉBLOQUÉE.

**La cristallisation R6 (exigée au scellage).** Dix passes --verifier (graine 20261105, volume complet : M4 560 + M5 365 + harnais M8 61 cas verts à chaque passe, verrou croisé 55/55) : 55 blocs à 10/10.

**Le scellage (m8/build_m8.py --sceller-final — né au geste, modèle D147/corpus).** LES PORTES tranchées AVANT l'unique écriture : le garde sceau I (7 arbres m0-m5+m8, clé « réelle ») ; LE RECOUP TERRAIN EXIGÉ SUR PIÈCES (le verdict VERT 30/30 + les six attestations A — absent ou rouge : REFUS NOMMÉ) ; la cristallisation 55×10/10 ; le verrou croisé R8 et la balise encore dev.1 ; la bascule version=0.9.0-dev.1 → version=0.9.0 dans frag-bld (occurrence UNIQUE, vérifiée EN MÉMOIRE, l'ancienne absente après) ; les fragments re-chiffrés, la racine re-dérivée, L'ENTÊTE PORTE LA BALISE (construire_entete paramétré — m8/carte_m8.py), la signature Ed25519 re-signée (graine durable D144, pub e9cd8c549485… : LE TÉMOIN NE BOUGE PAS) ; le tableau de bord suit (la ligne preversions CONSCIENTE de la balise : « 0.9.0 SCELLÉE sur le recoup terrain M8-(d) VERT 30/30 sur pièces croisées ») ; post-scellage : verrou croisé 55/55, **proxy.exe INTACT (1492b0bc…, 44 544 o — LE SCELLAGE EST UN FAIT DE CARTE, l'artefact ne bouge jamais)**, la reconstruction désormais REFUSÉE par l'anti-rollback (constaté : « carte scellée (0.9.0) : reconstruction interdite »), la re-vérification sous 0.9.0 VERTE (la balise préservée, cristallisation maintenue).

**Détail.** FRONTIÈRES : les balises win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES ; le scellé 0.6.0 (c1e46fb0…) demeure L'ANCRE R7 ; le SSN du terrain demeure INCONNU du labo (une DONNÉE du témoin : RE-LUE de l'imm32 consigné, prouvée par le geste de la twin — jamais une connaissance du labo) ; les pièces demeurent au coffre /test/preuves-m8d/ (la clôture D143 suit). Livrables : scripts/rapatrier_preuves_m8d.py, scripts/recouper_run_m8d.py, m8/build_m8.py (--sceller-final), m8/carte_m8.py (entête paramétré), m8/carte/ (la balise 0.9.0), download/preuves-run-m8d/ (les pièces + VERDICT-recoup-m8d.txt) ; consignations : la présente Entrée PAR SCRIPT, D165 PAR SCRIPT, PLAN (jalon M8 FRANCHI), worklog +Task ID 82 ; scripts suivis : inserer_entree_164.py.

- SUITE : la passation D141 (LA SÉRIE 090 NAÎT à la finale 0.9.0 — le bundle à la pointe, l'ancien 080 archivé versionné) + la clôture D143 du run m8d (les pièces + VERDICT-recoup-labo-m8d.txt → archives-preuves/preuves-run-m8d/, le réceptacle demeure) + le push GitHub à la pointe.

"""

# ------------------------------------------------------------------ D165 -----
DECISION = """
## D165 — LA FINALE D'UNE ÈRE SE SCELLE SUR LE RECOUP TERRAIN EXIGÉ COMME PIÈCE (le scellage REFUSE en l'absence du verdict du recoup vert : la porte est de PROCESSUS, jamais de console — D138/D145/D148/D154 étendues au geste final) ; LE SCELLAGE EST UN FAIT DE CARTE, L'ARTEFACT NE BOUGE JAMAIS (la balise vit dans frag-bld, l'entête la porte, proxy.exe demeure byte-identique 1492b0bc…) ; LE SSN DU TERRAIN DEMEURE INCONNU DU LABO (RE-LU de l'imm32 du stub consigné, rendu par les DEUX lecteurs, PROUVÉ par le geste de la twin — le numéro n'est jamais cru, jamais su) ; L'INSTRUMENT DU RECOUP S'INSTRUIT AVANT LES PIÈCES (DEUX défauts nommés par le fail-closed en un geste, corrigés et rejoués, les pièces immuables — D154 re-vivante)

**Le contexte qui fonde la décision (05/11, le geste final M8-(d)).** Le développeur a rejoué le run sur le kit corrigé et déposé les pièces au coffre /test/preuves-m8d/. Le labo a rapatrié (md5 contrôlés), recoupé (30 contrôles : pièces, témoin, journal, verdict, fichiers du geste re-contrôlés octet par octet, chaîne du scellé) — VERT 30/30. Deux défauts d'INSTRUMENT ont été nommés par le fail-closed pendant le geste (un « $ » sans re.M ; une tranche de sortie amputant la première attestation du verdict écrit — attrapée par LE SCELLAGE lui-même, qui exige les six attestations de pièces) : corrigés, rejoués, les pièces n'ont pas bougé d'un octet. Puis la cristallisation (10 passes, 55 blocs à 10/10) et le scellage : la balise 0.9.0-dev.1 → 0.9.0 basculée DANS LA CARTE (frag-bld, occurrence unique vérifiée en mémoire avant l'unique écriture), l'entête porte la balise, la signature re-signée à la graine durable, le tableau suit — et proxy.exe INTACT.

**Les règles.** (1) **La finale d'une ère exige le verdict du recoup terrain COMME PIÈCE** : --sceller-final refuse nommément si VERDICT-recoup-m8d.txt est absent, non « VERT 30/30 », ou sans les six attestations de pièces — la validation terrain n'est jamais une parole, toujours une pièce croisée. (2) **Le scellage est un fait de carte** : l'artefact ne bouge jamais (sha constaté avant et après), la balise vit dans frag-bld, l'entête de carte la porte (construire_entete paramétré — la cohérence entête/frag-bld est vérifiée à chaque re-signature), le tableau de bord est CONSCIENT de la balise (la ligne preversions nomme le geste qui a scellé). (3) **Le SSN du terrain demeure une donnée du témoin, jamais du labo** : le labo ne le devine pas, il RE-LIT l'imm32 du stub consigné, constate la parité des DEUX lecteurs et la distinctivité du second nom, et tient la preuve du geste (la twin == le fixture octet par octet — un SSN faux n'aurait pas écrit la ligne). (4) **L'anti-rollback est vivant après le scellage** : la reconstruction REFUSÉE nommément, la re-vérification demeure licite sous la balise scellée (cristallisation continue, verrou croisé re-constaté).

**Alternatives rejetées.** Sceller sur la console du développeur (rejeté : D138/D145/D148 — sur pièces, jamais sur console) ; sceller sans la 10/10 (rejeté : R6 — la cristallisation est exigée au scellage, dix passes la constituent) ; re-générer l'artefact « en 0.9.0 » (rejeté : le scellage est un fait de carte — l'octet ne bouge pas, un artefact régénéré serait un AUTRE artefact) ; traiter le SSN 8 comme une connaissance du labo (rejeté : c'est une donnée du témoin de la machine du développeur — le labo ne la connaît pas, il la recoupe) ; laisser le verdict amputé passer (rejeté : le scellage a REFUSÉ — le fail-closed a fait son travail, l'instrument corrigé et rejoué).

**Frontières.** Les balises win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES ; l'artefact 0.9.0 == l'artefact 0.9.0-dev.1 (1492b0bc…, 44 544 o — le même octet, une autre balise de CARTE) ; le scellé 0.6.0 demeure l'ancre R7 ; l'état de clé du sceau « réelle » intact ; les pièces au coffre /test/preuves-m8d/ jusqu'à la clôture D143. Les pièces de l'arrêt : download/preuves-run-m8d/ (les six pièces + VERDICT-recoup-m8d.txt), m8/carte/ (la balise 0.9.0, entête + frag-bld + signature), m8/build_m8.py (--sceller-final), scripts/rapatrier_preuves_m8d.py, scripts/recouper_run_m8d.py.
"""

# ------------------------------------------------------------------ worklog --
WORKLOG = """
## Task ID 82 — « preuves m8d déposées dans le drive /test » : LE RUN TERRAIN M8-(d) VERT SUR PIÈCES + LE RECOUP LABO VERT 30/30 SUR PIÈCES CROISÉES + LA FINALE 0.9.0 SCELLÉE — LE JALON M8 FRANCHI (05/11)

- LE RUN REJOUÉ (le kit corrigé ad6cbffe…, la ligne 207 n'est plus) :
  temoin-m8d.txt (2026-11-05 12:10:03, Windows 10.0 build 26300, Python
  3.13.9 AMD64) — T0-T3 ENTIERS, 35 verts / 0 échecs, VERDICT VERT ; le
  SSN(NtWriteFile) rendu DEUX fois le MÊME (Python + sys-02), NtReadFile
  DISTINCT, le stub confronté, le forgé crocheté REFUSÉ (-4), LA TWIN
  (l'IAT kernel32 == le syscall direct == le fixture 33 octets), le refus
  -1 sur pièce VIDE, proxy.exe relu inchangé.
- LE RECOUP (scripts/recouper_run_m8d.py — le juge est le code : les
  constantes importées de la source, le fixture et le sha RECALCULÉS au
  geste même) : 30 contrôles, RECOUP VERT 30/30 — l'imm32 du stub
  consigné == LE SSN (RE-LU, jamais cru), la twin re-contrôlée octet par
  octet au labo (md5 c64ab06b…, sha du fixture == le constat T2.TWIN),
  le kit du coffre == le corrigé, le zip == le dépôt (scenario + proxy).
  DEUX défauts d'INSTRUMENT nommés par le fail-closed (le « $ » sans
  re.M ; la tranche de sortie amputant la première attestation —
  attrapée par LE SCELLAGE), corrigés et rejoués, les pièces immuables
  (D154).
- LA CRISTALLISATION R6 : dix passes --verifier (M4 560 + M5 365 +
  harnais M8 61 verts par passe, verrou 55/55) — 55 blocs à 10/10.
- LE SCELLAGE (m8/build_m8.py --sceller-final né au geste, modèle
  D147/corpus) : garde sceau I (7 arbres, clé réelle) + recoup terrain
  EXIGÉ SUR PIÈCES + cristallisation 10/10 + verrou croisé avant/après
  + bascule unique version=0.9.0-dev.1 → 0.9.0 dans frag-bld (EN MÉMOIRE
  avant l'unique écriture), entête portant la balise, signature à la
  graine durable (pub e9cd8c549485… ne bouge pas), tableau CONSCIENT de
  la balise ; proxy.exe INTACT (1492b0bc…, 44 544 o — FAIT DE CARTE) ;
  l'anti-rollback REFUSE désormais la reconstruction (constaté), la
  re-vérification sous 0.9.0 VERTE.
- FRONTIÈRES : win 0.6.0 / linux 0.7.0 / riscv 0.8.0 INTACTES ; le
  scellé 0.6.0 ancre R7 ; le SSN du terrain INCONNU du labo (donnée du
  témoin) ; consignations : Entrée 164 PAR SCRIPT (ordre 163<164<
  marqueur, rejeu REFUSÉ), D165 PAR SCRIPT (à la suite de D164), PLAN
  (jalon M8 FRANCHI — ligne du jalon, ligne (d), État du programme),
  worklog +Task ID 82 ; scripts suivis : inserer_entree_164.py,
  rapatrier_preuves_m8d.py, recouper_run_m8d.py [labo].
- SUITE : LA PASSATION D141 (la série 090 NAÎT à la finale 0.9.0 — le
  bundle à la pointe, l'ancien 080 archivé versionné) + LA CLÔTURE D143
  du run m8d (les pièces + VERDICT-recoup-labo-m8d.txt →
  archives-preuves/preuves-run-m8d/, le réceptacle demeure) + le push
  GitHub à la pointe.

Stage Summary:
- LE JALON M8 EST FRANCHI : le terrain a établi le critère (le VRAI
  ntdll lu, la même ligne par les DEUX chemins), le labo a recoupé sur
  pièces croisées, la carte a scellé — l'artefact n'a pas bougé d'un
  octet.
- LA FINALE 0.9.0 EST SCELLÉE (le fait de carte, la chrystal 10/10, le
  recoup 30/30 exigé comme pièce — le fail-closed a refusé deux fois
  avant de sceller, et il avait raison les deux fois).
"""

# ------------------------------------------------------------------- PLAN ----
PLAN_ETAT_ANCIEN = "**État du programme.** **Chantiers M6-(a), M6-(b) et M6-(c) RÉALISÉS"
PLAN_ETAT_NOUVEAU = ("**État du programme.** **LE JALON M8 FRANCHI le 05/11/2026 "
                     "(Entrée 164, D165) : le run terrain M8-(d) VERT sur pièces + le "
                     "recoup labo 30/30 sur pièces croisées + LA FINALE 0.9.0 SCELLÉE "
                     "(fait de carte — l'artefact 1492b0bc… INTACT) ; les chantiers "
                     "M6/M7 accomplis, le programme du jalon M8 EST ACCOMPLI.** Les "
                     "chantiers M6-(a), M6-(b) et M6-(c) RÉALISÉS")
PLAN_JALON_ANCIEN = ("LE CHANTIER (d) ATTEND (le kit terrain au coffre /test, le VRAI "
                     "ntdll lu sur la machine du développeur — la finale 0.9.0 attend "
                     "le run terrain vert)** |")
PLAN_JALON_NOUVEAU = ("LE CHANTIER (d) RÉALISÉ le 05/11 (Entrée 164, D165) : LE RUN "
                      "TERRAIN VERT SUR PIÈCES (35 verts / 0 échecs — le VRAI ntdll "
                      "lu par les DEUX lecteurs indépendants, LA MÊME ligne de 33 "
                      "octets par les DEUX chemins, le refus nommé sur pièce vide) + "
                      "LE RECOUP LABO VERT 30/30 SUR PIÈCES CROISÉES + LA FINALE "
                      "0.9.0 SCELLÉE (le fait de carte — proxy.exe INTACT "
                      "1492b0bc…) — **LE JALON M8 FRANCHI, le programme M8 ACCOMPLI**"
                      "** |")
PLAN_D_ANCIEN = ("LE RUN ATTEND LE GESTE DU DÉVELOPPEUR (python scenario-m8d.py sur "
                 "Windows)** |")
PLAN_D_NOUVEAU = ("LE RUN EST VENU ET IL EST VERT (le 05/11, sur le kit corrigé : 35 "
                  "verts / 0 échecs — le VRAI ntdll lu, la twin octet pour octet, le "
                  "refus nommé sur pièce vide) ; LE RECOUP LABO VERT 30/30 SUR PIÈCES "
                  "CROISÉES (le juge est le code) ; LA FINALE 0.9.0 SCELLÉE le 05/11 "
                  "(Entrée 164, D165 : cristallisation 55×10/10, bascule de balise "
                  "dans frag-bld, l'artefact INTACT — le fait de carte) — LE CHANTIER "
                  "EST RÉALISÉ, LE JALON M8 FRANCHI** |")


def faire(chemin, transformations):
    with open(chemin, encoding="utf-8") as f:
        texte = f.read()
    for etiquette, ancien, nouveau, unique in transformations:
        if ancien not in texte:
            sys.exit(f"ECHEC : ancrage absent ({etiquette}) dans {chemin} — "
                     "rien n'est écrit")
        if unique and texte.count(ancien) != 1:
            sys.exit(f"ECHEC : ancrage non unique ({etiquette}, "
                     f"{texte.count(ancien)} occurrences) — rien n'est écrit")
        texte = texte.replace(ancien, nouveau, 1)
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(texte)
    print(f"[consigne] {chemin} : {len(transformations)} transformation(s)")


# --- 1. JOURNAL_TRAVAIL : l'Entrée 164 (ordre 163<164<marqueur) ----------------
with open("docs/JOURNAL_TRAVAIL.md", encoding="utf-8") as f:
    jt = f.read()
if "## Entrée 164" in jt:
    sys.exit("ECHEC : l'Entrée 164 existe déjà")
MARQUEUR = "<!-- m5a:journal-des-builds"
if MARQUEUR not in jt:
    sys.exit("ECHEC : marqueur journal introuvable")
if jt.find("## Entrée 163") < 0:
    sys.exit("ECHEC : l'Entrée 163 introuvable (l'ordre 163<164)")
nouveau_jt = jt.replace(MARQUEUR, ENTREE + MARQUEUR, 1)
if not (0 <= nouveau_jt.find("## Entrée 163") < nouveau_jt.find("## Entrée 164")
        < nouveau_jt.find(MARQUEUR)):
    sys.exit("ECHEC : l'ordre 163<164<marqueur n'est pas tenu")
with open("docs/JOURNAL_TRAVAIL.md", "w", encoding="utf-8") as f:
    f.write(nouveau_jt)
print("[consigne] docs/JOURNAL_TRAVAIL.md : Entrée 164 insérée "
      "(l'ordre 163<164<marqueur constaté)")

# --- 2. DECISIONS : D165 à la suite de D164 -------------------------------------
with open("docs/DECISIONS.md", encoding="utf-8") as f:
    dec = f.read()
if "## D165" in dec:
    sys.exit("ECHEC : D165 existe déjà")
if not dec.rstrip().endswith("passe_bundle_m8c_execution.py (la passation rejouée, dépôt)."):
    sys.exit("ECHEC : D164 n'est pas la dernière décision (la fin du fichier a "
             "divergé) — D165 s'inscrit à la suite, jamais au milieu")
with open("docs/DECISIONS.md", "w", encoding="utf-8") as f:
    f.write(dec.rstrip("\n") + "\n" + DECISION)
print("[consigne] docs/DECISIONS.md : D165 consignée à la suite de D164")

# --- 3. worklog : +Task ID 82 ----------------------------------------------------
with open("worklog.md", encoding="utf-8") as f:
    wl = f.read()
if "## Task ID 82" in wl:
    sys.exit("ECHEC : le Task ID 82 existe déjà")
if "## Task ID 81" not in wl:
    sys.exit("ECHEC : le Task ID 81 introuvable (l'ordre 81<82)")
with open("worklog.md", "w", encoding="utf-8") as f:
    f.write(wl.rstrip("\n") + "\n" + WORKLOG)
print("[consigne] worklog.md : Task ID 82 consigné à la suite du 81")

# --- 4. PLAN : le jalon M8 FRANCHI ------------------------------------------------
faire("docs/PLAN_MILESTONES.md", [
    ("État du programme", PLAN_ETAT_ANCIEN, PLAN_ETAT_NOUVEAU, True),
    ("la ligne du jalon M8", PLAN_JALON_ANCIEN, PLAN_JALON_NOUVEAU, True),
    ("la ligne du chantier (d)", PLAN_D_ANCIEN, PLAN_D_NOUVEAU, True),
])
print("[consigne] LES QUATRE CONSIGNATIONS SONT PORTÉES — le geste est consigné")
