#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_kit_tgn.py — LA CONSIGNATION DE LA LIVRAISON DU KIT TERRAIN
LOUPE (M10-(d) seconde moitié ACCOMPLIE : le kit déployé au coffre /test,
le réceptacle armé — la rangée (e) LE RUN attend le geste du développeur).

Le journal reçoit l'Entrée 203, le PLAN reçoit la rangée (d) accomplie
(le kit livré), le worklog reçoit la Task ID 121.

GARDES AVANT ÉCRITURE :
  - le kit au coffre : kit-loupe.zip (md5 ee43c991…) + LISEZMOI-loupe.txt
    lus au /test, les empreintes recoupées ;
  - le réceptacle preuves-loupe/ armé (son LISEZMOI) ;
  - LES PIÈCES DE L'ÈRE DEMEURÉES (signatures-I.txt f33c803a… +
    cle-publique-I.txt 188a7d42…) ;
  - l'artefact : loupe.exe 50 688 o, sha256 f07dd2cf… (inchangé).
Tout écart = ÉCHEC NOMMÉ, rien n'est écrit. Rejeu REFUSÉ."""

import hashlib
import importlib.util
import os
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
SHA_EXE = ("f07dd2cfc6cab97598657a8488a33ba0"
           "f7de2d1509a84d6b008ad4c1c1965499")
KIT_MD5 = "ee43c991455720fb162e3aedb43c3a6d"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds"


def _garde() -> None:
    racine = ds.list_folder(TEST_ID)
    kit = racine.get("kit-loupe.zip")
    assert kit and kit.get("md5Checksum") == KIT_MD5, "kit-loupe.zip absent/divergent au /test"
    assert "LISEZMOI-loupe.txt" in racine, "LISEZMOI-loupe.txt absent du /test"
    receptacle = racine.get("preuves-loupe")
    assert receptacle, "preuves-loupe/ absent du /test"
    assert "LISEZMOI-preuves.txt" in ds.list_folder(receptacle["id"]), \
        "le réceptacle n'est pas armé"
    for piece, md5_attendu in (("signatures-I.txt",
                                "f33c803aad80711995c6ea61ce30aa7b"),
                               ("cle-publique-I.txt",
                                "188a7d42df2d03f68bfb50fada3a84a1")):
        p = racine.get(piece)
        assert p and p.get("md5Checksum") == md5_attendu, \
            f"la pièce d'ère {piece} a divergé"
    donnees = (REPO / "loupe" / "loupe.exe").read_bytes()
    assert len(donnees) == 50688 and hashlib.sha256(donnees).hexdigest() == SHA_EXE
    print("[garde] le coffre : kit-loupe.zip + LISEZMOI-loupe.txt + "
          "preuves-loupe/ armé ; LES PIÈCES DE L'ÈRE DEMEURENT ; "
          "l'artefact inchangé f07dd2cf…")


ENTREE_203 = """## Entrée 203 — LE KIT TERRAIN LOUPE LIVRÉ AU COFFRE /test : la rangée M10-(d) ACCOMPLIE (l'artefact 0.1.0-dev.1 + le scénario + le LISEZMOI, le réceptacle armé) — LA RANGÉE (e) LE RUN attend le geste du développeur (09/11)

**L'instrument : loupe/terrain/scenario-loupe.py + scripts/assembler_kit_loupe.py + scripts/deposer_kit_loupe.py (les modèles m9f — D143/D153).** LE SCÉNARIO (python seul : ctypes, hashlib, os, platform, struct, sys) : LE SCÉNARIO EST LE CHARGEUR (LoadLibraryEx DONT_RESOLVE, aucun point d'entrée exécuté — la vitrine se vit à côté, au double-clic), l'IAT RÉSOLUE par le kit (34 feuilles + la double entrée démo posées aux slots du plan, VirtualProtect le temps de la pose), puis LES BLOCS APPELÉS À LEURS ADRESSES SCELLÉES : T1 la session (loupe-01 sur le VRAI fichier, le cadre relu champ à champ) · T2 LA DOUBLE LECTURE (loupe-02 le tampon == Python ; loupe-07 le panneau md5+sha256 == hashlib — ET LA PIÈCE DE L'ÈRE JUGÉE PAR SA PROPRE APPLICATION : loupe-07 sur loupe.exe rend son sha256 asserté f07dd2cf…) · T3 les lignes (loupe-08 == le format composé en Python, la ligne finale incomplète garde l'alignement) · T4 la recherche (loupe-13 le memcmp SCELLÉ M1 == bytes.find) · T5 L'ÉDITION LA BOUCLE ENTIÈRE (ouvrir, la saisie « 4d », Ctrl+S l'écriture À L'OCTET — le fichier revérifié : EXACTEMENT l'octet changé, la taille constante, la marque levée) · T6 les rejets NOMMÉS (-1 FIN, -2 ABSENT, -5 la session double, -3 hors bornes) · T7 la clôture (le cadre re-vierge, l'artefact relu INCHANGÉ).

**L'ÉPREUVE DE LABO (le labo ne peut pas exécuter — Windows exigé)** : l'assemblage loupe-kit/ = loupe.exe (sha256 f07dd2cf… ASSERTÉ) + scenario-loupe.py + LISEZMOI-KIT-LOUPE.md ; LE RECOUP DES CONSTANTES PAR AST : chaque constante du scénario relue DANS L'ARTEFACT ou DANS LE PLAN — les 25 adresses scellées == loupe/layout.py, les listes IAT == l'ordre FIGÉ, la table K == tls13/layout.py (FIPS 180-4), les champs du cadre == la chaîne des tailles, ET LES TÊTES SCELLÉES À DOUBLE ANCRE (les prologues de libc-01/02/07, win-03 et tls13-01 — dont le mov de H0[0] 0x6A09E667 posé par le scellé M9 — relus DANS l'artefact ET DANS les scellés d'origine : jamais gravés de tête ; la correction du premier jet : les têtes supposées ont été RÉFUTÉES par le recoup même — la source unique est le dépôt) ; py_compile VERT ; L'ÉPREUVE D'EXTRACTION VIERGE (le zip extrait dans un répertoire NEUF, les empreintes re-constatées, le recoup REJOUÉ) — **kit-loupe.zip : 21 095 o, md5 ee43c991…, sha256 1689fc20…**.

**La livraison au coffre (règle D143 : archivage par DÉPLACEMENT, jamais un jet)** : la vague m9f CONSOMMÉE archivée → /test/archives-livraisons/vagues-m9/ (kit-m9f.zip + LISEZMOI-m9f.txt, md5 recoupés après déplacement — le jalon M9 franchi, la pièce des sept runs demeure aux archives) ; preuves-loupe/ NÉ avec son LISEZMOI-preuves.txt (le témoin attendu + LES CAPTURES DE LA VITRINE bienvenues — la vie de l'application chez l'utilisateur, le cœur du grandeur nature) ; LA VAGUE DÉPOSÉE à la racine : kit-loupe.zip (md5 MATCH par relecture) + LISEZMOI-loupe.txt (le document du kit, lisible AU coffre sans extraire — les quatre temps du geste : extraire, lancer le scénario, VIVRE LA VITRINE [double-clic, F5 l'aller, F3 la recherche, la saisie hexa, Ctrl+S, le double Alt+F4], renvoyer preuves-loupe/ ENTIER) ; l'index des livraisons mis à jour ; **LES PIÈCES DE L'ÈRE DEMEURENT** (signatures-I.txt f33c803a… la remise INSTALLÉE + cle-publique-I.txt 188a7d42… l'ancre — la vague ne les touche jamais, vérifié après livraison).

**Détail.** FRONTIÈRES : l'artefact inchangé (sha256 re-asserté à la garde), la carte privée ne voyage JAMAIS avec l'artefact (R1), le scénario n'écrit JAMAIS loupe.exe (relu à la clôture du run), aucune balise ne bouge (la 0.1.0 se scellera sur le run terrain vert recoupé — fait de carte, D104). LA RANGÉE M10-(d) EST ACCOMPLIE : la notation (Entrée 198) + la cérémonie (Entrée 201) + le build (Entrée 202) + LE KIT DÉPLOYÉ au coffre, LISEZMOI à jour, le réceptacle armé, l'artefact empreinté par le build. Livrables : loupe/terrain/scenario-loupe.py, loupe/terrain/LISEZMOI-KIT-LOUPE.md, scripts/assembler_kit_loupe.py, scripts/deposer_kit_loupe.py, kit-loupe.zip au /test.

- SUITE : LE RUN TERRAIN M10-(e) — LE GESTE DU DÉVELOPPEUR (dézipper kit-loupe.zip dans un dossier NEUF D99, python scenario-loupe.py ~quelques secondes, VIVRE LA VITRINE au double-clic, renvoyer preuves-loupe/ ENTIER au coffre /test) ; le labo recoupe sur pièces (D138/D145/D148) — ET SI LE VERT TIENT : la balise `loupe 0.1.0` scellée sur run recoupé, LE JALON M10, la méthode entière prouvée par la CRÉATION ; le projet fils attend son premier geste à son message propre.

"""


TASK_121 = """## Task ID 121 — LE KIT TERRAIN LOUPE LIVRÉ AU COFFRE /test : la rangée M10-(d) accomplie (le scénario-chargeur, le recoup AST à double ancre, le réceptacle armé) — la rangée (e) LE RUN attend le développeur (09/11)

- LA DEMANDE : la SUITE de l'Entrée 202 (LE KIT TERRAIN, le geste
  suivant du programme M10).
- LE SCÉNARIO (loupe/terrain/scenario-loupe.py — python seul) : LE
  SCÉNARIO EST LE CHARGEUR (DONT_RESOLVE, l'IAT résolue par le kit aux
  slots du plan), LES BLOCS APPELÉS À LEURS ADRESSES SCELLÉES : la
  session, LA DOUBLE LECTURE (le panneau == hashlib ET loupe-07 sur
  loupe.exe rend son sha256 asserté — la pièce jugée par sa propre
  application), les lignes, la recherche (le memcmp scellé), L'ÉDITION
  LA BOUCLE ENTIÈRE à l'octet, les rejets nommés, la clôture.
- L'ÉPREUVE DE LABO : le recoup des constantes PAR AST (25 adresses ==
  le plan, les listes IAT == l'ordre figé, la table K == FIPS, LES
  TÊTES SCELLÉES À DOUBLE ANCRE == l'artefact ET les scellés d'origine
  — les têtes supposées du premier jet RÉFUTÉES par le recoup même),
  py_compile, l'extraction vierge — kit-loupe.zip 21 095 o, md5
  ee43c991…, sha256 1689fc20….
- LA LIVRAISON (D143 : archivage par déplacement) : la vague m9f
  archivée → vagues-m9/ ; preuves-loupe/ NÉ armé (le témoin + les
  captures de la vitrine bienvenues) ; kit-loupe.zip + LISEZMOI-
  loupe.txt à la racine (md5 MATCH par relecture) ; l'index mis à
  jour ; LES PIÈCES DE L'ÈRE DEMEURENT (signatures-I.txt f33c803a… +
  cle-publique-I.txt 188a7d42…, vérifié).
- LA RANGÉE M10-(d) ACCOMPLIE : la notation + la cérémonie + le build
  + LE KIT DÉPLOYÉ, le réceptacle armé, l'artefact empreinté.
- SUITE : LE RUN M10-(e) — LE GESTE DU DÉVELOPPEUR (le scénario +
  VIVRE LA VITRINE ; preuves-loupe/ ENTIER au coffre) ; le labo
  recoupe (D138/D145/D148) ; si le vert tient : la balise
  `loupe 0.1.0` scellée — LE JALON M10.
"""


def main() -> int:
    _garde()

    texte = JOURNAL.read_text(encoding="utf-8")
    assert "## Entrée 203" not in texte, "l'Entrée 203 existe déjà — rejeu refusé"
    idx = texte.index(MARQUEUR)
    texte = texte[:idx] + ENTREE_203 + texte[idx:]
    JOURNAL.write_text(texte, encoding="utf-8")
    print("[journal] l'Entrée 203 insérée")

    plan = PLAN.read_text(encoding="utf-8")
    ancien = ("LE KIT TERRAIN est "
              "le geste suivant")
    nouveau = ("LE KIT TERRAIN LIVRÉ (Entrée 203, Task 121 : kit-loupe.zip au "
               "coffre /test — le scénario-chargeur, le recoup AST à double "
               "ancre, le réceptacle preuves-loupe/ armé, LES PIÈCES DE L'ÈRE "
               "demeurées) — LA RANGÉE (d) ACCOMPLIE, la rangée (e) LE RUN "
               "attend le geste du développeur")
    assert ancien in plan, "la phrase de la rangée (d) introuvable (le PLAN a bougé ?)"
    plan = plan.replace(ancien, nouveau, 1)
    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] la rangée (d) : LE KIT LIVRÉ, la rangée ACCOMPLIE")

    wl = WORKLOG.read_text(encoding="utf-8")
    assert "## Task ID 121" not in wl, "la Task 121 existe déjà — rejeu refusé"
    wl = wl.rstrip("\n") + "\n\n" + TASK_121
    WORKLOG.write_text(wl, encoding="utf-8")
    print("[worklog] la Task ID 121 ajoutée")

    print("[consigner] LA CONSIGNATION ÉCRITE : Entrée 203 + PLAN (la rangée "
          "(d) accomplie) + worklog Task 121")
    return 0


if __name__ == "__main__":
    sys.exit(main())
