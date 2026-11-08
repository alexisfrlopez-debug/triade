#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_retouche_loupe.py — LA CONSIGNATION DE LA RETOUCHE dev.2
(Entrée 204 : le run terrain M10-(e) a REFUSÉ dev.1 — 0xc000007b, le
VRAI chargeur Windows ne peut pas reloger une image ASLR sans table de
relocalisation ; LA RETOUCHE BASERELOC née et livrée, la vague refusée
archivée, le run rejoué attend le développeur).

Le journal reçoit l'Entrée 204, le PLAN reçoit la note de la rangée (e)
(le premier run a nommé le défaut, la retouche livrée), le worklog
reçoit la Task ID 122.

GARDES AVANT ÉCRITURE :
  - le coffre : kit-loupe.zip dev.2 (md5 d50288d8…) + LISEZMOI-loupe.txt
    à la racine, la vague dev.1 archivée à vagues-m10/, LES PIÈCES DE
    L'ÈRE DEMEURÉES ;
  - l'artefact local : loupe.exe 50 688 o, sha256 a8a65ed4… (dev.2 —
    le BASERELOC dirs[5] déclaré, les douze octets de la lignée).
Tout écart = ÉCHEC NOMMÉ, rien n'est écrit. Rejeu REFUSÉ."""

import hashlib
import importlib.util
import os
import pathlib
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
SHA_EXE = ("a8a65ed4cc3778c691dffbd104ef8385"
           "85bcb5df206b0c5c79a0283f1f74c71d")
KIT_MD5 = "d50288d82147959cba679f9320810b61"
ANCIEN_KIT_MD5 = "ee43c991455720fb162e3aedb43c3a6d"
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds"


def _garde() -> None:
    # le coffre
    racine = ds.list_folder(TEST_ID)
    kit = racine.get("kit-loupe.zip")
    assert kit and kit.get("md5Checksum") == KIT_MD5, \
        "kit-loupe.zip dev.2 absent/divergent au /test"
    assert "LISEZMOI-loupe.txt" in racine, "LISEZMOI-loupe.txt absent du /test"
    arch = racine.get("archives-livraisons")
    assert arch, "archives-livraisons/ introuvable"
    vagues = ds.list_folder(arch["id"]).get("vagues-m10")
    assert vagues, "vagues-m10/ introuvable aux archives"
    arch_kit = ds.list_folder(vagues["id"]).get("kit-loupe.zip")
    assert arch_kit and arch_kit.get("md5Checksum") == ANCIEN_KIT_MD5, \
        "la vague dev.1 archivée est absente/divergente"
    for piece, md5_attendu in (("signatures-I.txt",
                                "f33c803aad80711995c6ea61ce30aa7b"),
                               ("cle-publique-I.txt",
                                "188a7d42df2d03f68bfb50fada3a84a1")):
        p = racine.get(piece)
        assert p and p.get("md5Checksum") == md5_attendu, \
            f"la pièce d'ère {piece} a divergé"
    # l'artefact local
    donnees = (REPO / "loupe" / "loupe.exe").read_bytes()
    assert len(donnees) == 50688 and hashlib.sha256(donnees).hexdigest() == SHA_EXE
    e = struct.unpack_from("<I", donnees, 0x3C)[0]
    rva, taille = struct.unpack_from("<II", donnees, e + 24 + 112 + 40)
    assert (rva, taille) == (0x2E90, 12), "dirs[5] != le BASERELOC du plan"
    assert donnees[0x2090:0x209C] == bytes.fromhex("001000000c00000000000000"), \
        "le bloc BASERELOC != les douze octets de la lignée"
    print("[garde] le coffre : kit dev.2 à la racine + la vague dev.1 "
          "archivée + LES PIÈCES DE L'ÈRE ; l'artefact a8a65ed4… porte "
          "le BASERELOC dirs[5] (0x2E90, 12 o)")


ENTREE_204 = """## Entrée 204 — LE RUN TERRAIN M10-(e) A REFUSÉ dev.1 : LE DÉFAUT NOMMÉ PAR LE VRAI CHARGEUR (0xc000007b — l'image ASLR sans table de relocalisation, l'oubli du premier build) — LA RETOUCHE dev.2 NÉE ET LIVRÉE (le BASERELOC minimal rendu au plan, le miroir M1..M9) ; LE RUN REJOUÉ ATTEND LE DÉVELOPPEUR (09/11 au soir)

**Le fait du terrain (la capture du développeur).** Le run M10-(e) sur LE VRAI Windows 11 : le bandeau, l'environnement consigné (Python 64 bits, AMD64), [T0] l'empreinte ASSERTÉE (50 688 o, sha256 f07dd2cf… — l'artefact authentique, la carte génération 13 prouve CES octets) — puis AU GESTE DE CARTOGRAPHIE la boîte dure du chargeur : « python.exe — Image incorrecte : C:\\Users\\Alek\\Downloads\\loupe-kit\\loupe.exe n'est pas conçu pour s'exécuter sous Windows ou il contient une erreur. État de l'erreur : 0xc000007b » — STATUS_INVALID_IMAGE_FORMAT, le scénario-chargeur refusé AVANT tout constat, son refus nommé CARTOGRAPHIE armé. **UN ÉCHEC NOMMÉ VAUT PLUS QU'UN VERT MUET : le grandeur nature a fait EXACTEMENT ce pour quoi il existe — l'application vit chez son utilisateur, et SEUL le VRAI chargeur Windows pouvait nommer ce défaut (le labo est Linux : le harnais PARSE l'image, il ne la charge jamais).**

**Le diagnostic (l'autopsie de l'image, la preuve par la lignée).** L'en-tête sain champ après champ (PE32+ AMD64, les quatre sections, les alignements, les imports, l'IAT — tout conforme) MAIS LE RÉPERTOIRE dirs[5] ABSENT : l'image déclare DllCharacteristics 0x0160 (DYNAMIC_BASE + HIGH_ENTROPY_VA — l'invitation au relogement) sans AUCUNE table de relocalisation ; la base de prédilection 0x140000000 est occupée dans le processus python.exe du développeur (l'EXE MSVC vit LÀ) — le chargeur DOIT reloger l'image, il ne le PEUT pas : refus. LA PREUVE PAR LA LIGNÉE : LES HUIT artefacts précédents — hello.exe M0, selftest.exe M1, echo.exe M2, proxy.exe M3/M4/M5/M8, proxy.exe M9 — portent TOUS le BASERELOC minimal (12 o : la page .text, BlockSize 12, deux entrées ABSOLUTE type 0 sans effet — l'image PI que le chargeur PEUT reloger, m2/layout.py:183 « image sans [fixups réels] ») ; TOUS ont passé la cartographie chez l'utilisateur ; loupe.exe dev.1 était LE SEUL sans table — l'éditeur PE du build dev.1 avait omis la pose et dirs[5], personne au labo ne pouvait le voir.

**La retouche (la révision nommée dev.1 → dev.2).** loupe/layout.py : R_RELOC = 0x2E90 (la marge machinerie APRÈS l'ancre @0x2E88, AVANT K[64] @0x2F00 — AUCUNE adresse scellée ne bouge) + VERSION_DEV 0x00010002 ; loupe/build_loupe.py : LA POSE des douze octets de la lignée (le miroir m1/m2/m3 : struct page .text, 12, deux ABSOLUTE) + dirs[5] = (R_RELOC, 12) + LA VALIDATION NEUVE (le répertoire déclaré au plan, les octets relus — le refus ne reviendra plus, il est TRANCHÉ au build) + la balise libellé portée à « Loupe 0.1.0-dev.2 » ; loupe/carte_m10.py : VERSION_DEV « 0.1.0-dev.2 » (la génération 13 inchangée — le miroir M8 : une génération par domaine, les builds la réécrivent). **LE BUILD REJOUÉ : le garde 14/14 VERT, l'oracle 43 verrous, R7 la double preuve, LES TROIS HARNAIS rejoués VERTS AU GESTE (noyau 59/59 · rendu 53/53 · édition 45/45 — 157 contrôles ; EN CONCURRENCE : des instruments indépendants, aucun chemin partagé, chacun son sous-processus, les empreintes et l'ordre de consignation CEUX DE LA LIGNÉE — la fenêtre du labo est bornée, l'édition 5 min 20 ne tient plus en série en une seule vie), loupe.exe 0.1.0-dev.2 NÉ : 50 688 o, sha256 a8a65ed4cc3778c6…, la carte génération 13 réécrite, le verrou croisé 26/26, le tableau de bord écrit.** LE DIFF CHIRURGICAL (dev.1 → dev.2, l'octet près) : SEPT octets en SIX plages — dirs[5] @0xF0 (90 2E 00 00 0C 00), la balise @0x1520 (« 1 »→« 2 »), le qword version @0x2080 (0x00010001→0x00010002), le bloc BASERELOC @0x2090 (00 10 00 00 0C 00 00 00 00 00 00 00) — la taille CONSTANTE, AUCUNE adresse scellée touchée, R2 tenuu (aucun octet de notation).

**Le kit rejoué (M10-(d) seconde moitié, la vague dev.2).** scenario-loupe.py : l'empreinte dev.2 figée, VERSION_R10 0x00010002, ET LE CONSTAT NEUF AU T0 — LE BASERELOC MINIMAL DÉCLARÉ tranché binaire (dirs[5] de l'image MAPPÉE == (0x2E90, 12), sinon le refus nommé BASERELOC : la leçon de l'Entrée 204 garde la porte pour toujours) ; LISEZMOI-KIT-LOUPE.md : la retouche racontée noir sur blanc, le geste D99 RENFORCÉ (le dossier du run dev.1 ne se réutilise JAMAIS — un dossier neuf, l'artefact refusé ne se mélange à rien) ; l'assembleur : LE RECOUP PORTÉ À 35 CONSTANTES (R_RELOC entre elles, la source unique le plan), py_compile, L'ÉPREUVE D'EXTRACTION VIERGE rejouée — **kit-loupe.zip : 21 949 o, md5 d50288d8…, sha256 62b1a080…**.

**Le coffre (D143 : archivage par DÉPLACEMENT, jamais un jet — scripts/deposer_kit_loupe_r2.py).** La vague dev.1 REFUSÉE archivée → /test/archives-livraisons/vagues-m10/ (kit-loupe.zip md5 ee43c991… + LISEZMOI-loupe.txt, les md5 recoupés APRÈS déplacement — LE REFUS DU TERRAIN EST UN FAIT, la pièce demeure) ; LA VAGUE dev.2 DÉPOSÉE à la racine (kit-loupe.zip md5 MATCH par relecture + LISEZMOI-loupe.txt — le document du kit dev.2) ; preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact attendu : 0.1.0-dev.2, a8a65ed4…, la leçon de l'Entrée 204 nommée au réceptacle) ; l'index LISEZMOI-archives-livraisons.txt mis à jour (la vague refusée archivée + la vague courante dev.2) ; **LES PIÈCES DE L'ÈRE DEMEURENT** (signatures-I.txt f33c803a… + cle-publique-I.txt 188a7d42…, vérifié après livraison).

**Détail.** FRONTIÈRES : AUCUN arbre signé touché (le garde 14/14 AVANT construire()), AUCUN octet de notation (R2 — la retouche vit dans la machinerie .rdata et l'en-tête, jamais dans les blocs), AUCUNE adresse scellée déplacée (le BASERELOC dans la marge vierge 0x2E90-0x2EFF), aucune balise scellée ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 INTACTES — la `loupe 0.1.0` se scellera sur le run terrain vert recoupé, fait de carte D104), la clé privée jamais traversée (D87). Livrables : loupe/layout.py, loupe/build_loupe.py, loupe/carte_m10.py, loupe/loupe.exe (0.1.0-dev.2, a8a65ed4…), loupe/carte/ (génération 13 réécrite), loupe/terrain/scenario-loupe.py, loupe/terrain/LISEZMOI-KIT-LOUPE.md, scripts/assembler_kit_loupe.py, scripts/deposer_kit_loupe_r2.py, kit-loupe.zip dev.2 au /test (la vague dev.1 à vagues-m10/).

- SUITE : LE RUN TERRAIN M10-(e) REJOUÉ — LE GESTE DU DÉVELOPPEUR (récupérer kit-loupe.zip NEUF au coffre /test, dézipper dans un dossier NEUF D99 — le dossier du run dev.1 est abandonné, python scenario-loupe.py, VIVRE LA VITRINE au double-clic, renvoyer preuves-loupe/ ENTIER au coffre /test) ; le labo recoupe sur pièces (D138/D145/D148) — ET SI LE VERT TIENT : la balise `loupe 0.1.0` scellée sur run recoupé, LE JALON M10, la méthode entière prouvée par la CRÉATION ; le projet fils attend son premier geste à son message propre.

"""


TASK_122 = """## Task ID 122 — LA RETOUCHE dev.2 APRÈS LE REFUS TERRAIN DE dev.1 : le défaut nommé par le VRAI chargeur (0xc000007b), le BASERELOC minimal rendu au plan, le kit dev.2 livré au coffre (09/11 au soir)

- LE FAIT : le run M10-(e) chez le développeur — [T0] l'empreinte
  ASSERTÉE puis la boîte dure « python.exe — Image incorrecte …
  0xc000007b » AU GESTE DE CARTOGRAPHIE (LoadLibraryEx DONT_RESOLVE).
- LE DIAGNOSTIC : l'image déclare DYNAMIC_BASE|HIGH_ENTROPY_VA SANS
  table de relocalisation ; la base 0x140000000 occupée par python.exe
  chez l'utilisateur → le chargeur DOIT reloger, il ne PEUT pas →
  STATUS_INVALID_IMAGE_FORMAT. LA PREUVE PAR LA LIGNÉE : les HUIT
  artefacts M0..M9 portent TOUS le BASERELOC minimal (12 o, entrées
  ABSOLUTE — image PI) ; dev.1 était LE SEUL sans table (l'éditeur PE
  avait omis la pose + dirs[5] — invisible au labo Linux : le harnais
  PARSE, il ne charge jamais).
- LA RETOUCHE : R_RELOC 0x2E90 (la marge machinerie, AUCUNE adresse
  scellée touchée) + VERSION_DEV 0x00010002 + la pose des douze octets
  de la lignée + dirs[5] + LA VALIDATION NEUVE au build ; LE BUILD
  REJOUÉ : garde 14/14, 43 verrous, LES TROIS HARNAIS 157 VERTS (en
  concurrence — la fenêtre du labo bornée : instruments indépendants,
  empreintes et ordre de la lignée), loupe.exe 0.1.0-dev.2 NÉ
  (50 688 o, sha256 a8a65ed4…, carte génération 13 réécrite, verrou
  croisé 26/26) ; LE DIFF CHIRURGICAL : 7 octets en 6 plages (dirs[5],
  la balise, le qword version, le bloc BASERELOC) — la taille
  CONSTANTE.
- LE KIT REJOUÉ : le scénario à l'empreinte dev.2 + LE CONSTAT NEUF
  T0 (dirs[5] == (0x2E90, 12), refus nommé BASERELOC sinon — la
  leçon garde la porte), le LISEZMOI raconté + D99 renforcé, le recoup
  PORTÉ À 35 constantes, l'extraction vierge — kit-loupe.zip 21 949 o,
  md5 d50288d8…, sha256 62b1a080….
- LE COFFRE (D143) : la vague dev.1 REFUSÉE archivée → vagues-m10/
  (md5 recoupés après déplacement — le refus est un FAIT, la pièce
  demeure) ; la vague dev.2 à la racine (md5 MATCH) ; le réceptacle et
  l'index mis à jour ; LES PIÈCES DE L'ÈRE DEMEURENT.
- SUITE : LE RUN REJOUÉ — kit NEUF, dossier NEUF D99, scénario +
  VITRINE, preuves-loupe/ ENTIER au coffre ; si le vert tient : la
  balise `loupe 0.1.0` scellée — LE JALON M10.
"""


def main() -> int:
    _garde()

    texte = JOURNAL.read_text(encoding="utf-8")
    assert "## Entrée 204" not in texte, "l'Entrée 204 existe déjà — rejeu refusé"
    idx = texte.index(MARQUEUR)
    texte = texte[:idx] + ENTREE_204 + texte[idx:]
    JOURNAL.write_text(texte, encoding="utf-8")
    print("[journal] l'Entrée 204 insérée")

    plan = PLAN.read_text(encoding="utf-8")
    ancien = ("| (e) Le run terrain + le scellage | le développeur court "
              "LOUPE sur SA machine ; le recoup labo sur pièces ; la "
              "balise `loupe 0.1.0` scellée |")
    nouveau = ("| (e) Le run terrain + le scellage | le développeur court "
               "LOUPE sur SA machine ; le recoup labo sur pièces ; la "
               "balise `loupe 0.1.0` scellée — LE PREMIER RUN A NOMMÉ LE "
               "DÉFAUT (09/11 : 0xc000007b, l'image ASLR sans table de "
               "relocalisation — l'oubli du build dev.1, invisible au labo "
               "Linux ; LA RETOUCHE dev.2 NÉE ET LIVRÉE, Entrée 204, Task "
               "122 : le BASERELOC minimal rendu au plan, loupe.exe "
               "0.1.0-dev.2 a8a65ed4…, kit dev.2 au coffre /test, la vague "
               "refusée archivée vagues-m10/) ; le run REJOUÉ attend le "
               "geste du développeur |")
    assert ancien in plan, "la rangée (e) introuvable (le PLAN a bougé ?)"
    plan = plan.replace(ancien, nouveau, 1)
    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] la rangée (e) : le refus nommé + la retouche dev.2 livrée")

    wl = WORKLOG.read_text(encoding="utf-8")
    assert "## Task ID 122" not in wl, "la Task 122 existe déjà — rejeu refusé"
    wl = wl.rstrip("\n") + "\n\n" + TASK_122
    WORKLOG.write_text(wl, encoding="utf-8")
    print("[worklog] la Task ID 122 ajoutée")

    print("[consigner] LA CONSIGNATION ÉCRITE : Entrée 204 + PLAN (la "
          "rangée (e) : refus nommé + retouche) + worklog Task 122")
    return 0


if __name__ == "__main__":
    sys.exit(main())
