#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_233.py — LE MANUSCRIT v0.15.0 INTROUVABLE AU COFFRE :
le constat du développeur (« je ne trouve pas le manuscrit v0.15 dans le
drive »), le diagnostic (le PDF INTÈGRE mais INVISIBLE — la convention
docs/TRIADE_manuscrit_vX.pdf des cinq versions précédentes rompue par la
chaîne v0.15.0 ; au coffre il n'existait qu'à l'intérieur des zips), la
réparation double (la convention RÉTABLIE à docs/ + le dépôt EN CLAIR à la
racine du coffre) — Entrée 233 + worklog Task 139. Append-only : les fins
sont VÉRIFIÉES avant chaque écriture (Entrée 232 / Task 138 attendues)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    occurrences = texte.count(fin_attendue)
    if occurrences != 1:
        sys.exit(f"[consigner] {nom} : la fin attendue apparaît "
                 f"{occurrences} fois (attendu : 1) — append refusé")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    if "Entrée 233" in texte:
        sys.exit(f"[consigner] {nom} : Entrée 233 déjà présente — "
                 f"append refusé (doublon)")
    with chemin.open("a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} caractères)")


ENTREE_233 = """

## Entrée 233 — LE MANUSCRIT v0.15.0 INTROUVABLE AU COFFRE : le constat du développeur reçu (« je ne trouve pas le manuscrit v0.15 dans le drive »), le diagnostic porté aux pièces (le PDF INTÈGRE mais INVISIBLE), la réparation double vécue (la convention docs/ RÉTABLIE et le dépôt EN CLAIR à la racine du coffre) (12/11, la session du manuscrit introuvable)

**Le constat et le diagnostic.** Le développeur ne trouve pas le manuscrit v0.15.0 au Drive — et il a RAISON de ne pas le trouver : le PDF est INTÈGRE partout (sha256 e8e075df81fafd06ce0ab1799bceb83a014484507fc4e4a00edbc6b7dd986ec6, identique à trois endroits recoupés : scripts/manuscrit_v150/main.pdf, le PDF dans TRIADE_soumission_v0.15.0.zip, le PDF dans TRIADE_complet_v0.15.0.zip — l'empreinte consignée à empreintes_livrables_v0.15.0.txt) mais INVISIBLE : (a) la chaîne d'édition v0.15.0 fit vivre le PDF sous le nom GÉNÉRIQUE scripts/manuscrit_v150/main.pdf — la convention des cinq versions précédentes (docs/TRIADE_manuscrit_v0.10.0.pdf … v0.14.0.pdf, chacune TROUVABLE au miroir TRIADE-sauvegarde-git/docs/) fut ROMPUE ; (b) à la racine du coffre, le manuscrit n'existait qu'À L'INTÉRIEUR des zips (soumission et complet) — lisible seulement après extraction.

**La réparation double.** (1) LA CONVENTION RÉTABLIE : docs/TRIADE_manuscrit_v0.15.0.pdf — la copie VÉRIFIÉE de scripts/manuscrit_v150/main.pdf (sha256 recoupé à l'empreinte consignée AVANT le geste : e8e075df… EXACT) ; au miroir Drive, le manuscrit redevient TROUVABLE par son nom à côté de ses cinq aînés. (2) LE DÉPÔT EN CLAIR À LA RACINE DU COFFRE : TRIADE_manuscrit_v0.15.0.pdf (181 335 o) déposé par scripts/deposer_manuscrit_v150.py — l'empreinte recoupée AVANT (== la consignée), le dépôt refusé si un doublon divergent existait (aucun écrasement silencieux), le md5 recoupé APRÈS (6dd1d74c… local == 6dd1d74c… Drive) ; la PREMIÈRE fois qu'un manuscrit vit en clair à la racine — le développeur le LIT sans dézipper.

**La règle qui en découle (D197 étendue aux documents en clair).** La racine du coffre ne porte que les versions COURANTES : à la prochaine édition du manuscrit, l'ancien PDF en clair passera racine → /ARCHIVE par déplacement vérifié — le miroir exact de la règle des livrables zips. Et la leçon de découvrabilité : un livrable de lecture porte SON NOM (le nom de version, jamais un nom de chaîne interne) — le manuscrit vit à docs/TRIADE_manuscrit_vX.pdf, la spécification à docs/Protocole_TRIADE_vX_Specification.pdf (la v0.15.0, 64 pages, y demeure TROUVABLE : la convention ne fut rompue que pour le manuscrit).

**Frontières.** Aucun zip touché (les livrables consignés à l'Entrée 231 demeurent INTACTS — le dépôt en clair est un geste d'ACCÈS, pas une nouvelle livraison) ; aucun octet du PDF modifié (la copie est une copie, l'empreinte le prouve) ; aucune pièce scellée touchée ; les consignations antérieures non réécrites (append-only).
"""

TASK_139 = """

Task ID: 139
Agent: Z.ai (agent principal)
Task: LE MANUSCRIT v0.15.0 INTROUVABLE AU COFFRE — le constat du
développeur, le diagnostic (le PDF intègre mais invisible : la convention
docs/ rompue par la chaîne v0.15.0, le coffre ne portait que les zips), la
réparation double (docs/ rétablie + le dépôt en clair à la racine).

Work Log:
- LE DIAGNOSTIC : le PDF INTÈGRE aux trois endroits (sha256 e8e075df… ==
  l'empreinte consignée : scripts/manuscrit_v150/main.pdf, le zip
  soumission, le zip complet) mais INVISIBLE (le nom générique main.pdf de
  la chaîne v0.15.0 ; au miroir /docs les manuscrits s'arrêtaient à
  v0.14.0 ; à la racine du coffre le manuscrit n'existait que dans les
  zips).
- LA CONVENTION RÉTABLIE : docs/TRIADE_manuscrit_v0.15.0.pdf (copie
  VÉRIFIÉE, sha256 == consigné avant le geste) — le manuscrit TROUVABLE
  au miroir à côté de ses cinq aînés.
- LE DÉPÔT EN CLAIR : TRIADE_manuscrit_v0.15.0.pdf (181 335 o) à la
  racine du coffre (scripts/deposer_manuscrit_v150.py : empreinte
  recoupée avant, doublon divergent refusé, md5 6dd1d74c… recoupé après).
- LA RÈGLE (D197 étendue) : à la prochaine édition, l'ancien manuscrit en
  clair sera archivé racine → /ARCHIVE (la racine ne porte que les
  versions courantes) ; un livrable de lecture porte SON NOM de version,
  jamais un nom de chaîne interne.
- Frontières : aucun zip touché, aucun octet du PDF modifié, aucune pièce
  scellée touchée.
- SUITE : au développeur — les trois runs matériels, la cérémonie du
  séquestre D183, la cérémonie d'ère, la réplication (l'annotateur, le
  second domaine).
"""


def main() -> int:
    append_verifie(JOURNAL,
                   "CONSIGNE — et rend la main au développeur.",
                   ENTREE_233, "JOURNAL_TRAVAIL.md")
    append_verifie(WORKLOG,
                   "annotateur R2, le second domaine à la vraie commande.",
                   TASK_139, "worklog.md")
    print("[consigner] Entrée 233 + Task 139 : CONSIGNÉES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
