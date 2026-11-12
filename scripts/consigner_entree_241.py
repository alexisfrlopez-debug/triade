#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_entree_241.py — LE POINT DE REPRISE APRÈS LA VAGUE 3 : le
rapatriement du bac à sable local (resté à 24a04d6 — les six paquets de la
vague vécurent dans d'autres instances, le dépôt git fit foi), les TROIS
MIROIRS recoupés (HEAD == origin/main == ac42880 ; le bundle Drive VERT par
l'instrument réparé D199), le garde 14/14, la re-exécution du vérificateur
TLA+ clone-frais 13/13 VERT (les pièces consignées restaurées intactes), les
QUATRE scellés recoupés, l'archivage des SIX instructions de la vague
(/instructions VIDE) — Entrée 241 + worklog Task 148. Append-only : les fins
sont VÉRIFIÉES avant chaque écriture (Entrée 240 / Task 147 attendues)."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"


def append_verifie(chemin: pathlib.Path, fin_attendue: str, bloc: str,
                   nom: str, marqueur: str) -> None:
    texte = chemin.read_text(encoding="utf-8")
    occurrences = texte.count(fin_attendue)
    if occurrences != 1:
        sys.exit(f"[consigner] {nom} : la fin attendue apparaît "
                 f"{occurrences} fois (attendu : 1) — append refusé")
    if not texte.rstrip("\n").endswith(fin_attendue.rstrip("\n")):
        sys.exit(f"[consigner] {nom} : la fin attendue n'est pas la "
                 f"dernière section — append refusé")
    if marqueur in texte:
        sys.exit(f"[consigner] {nom} : {marqueur} déjà présent — "
                 f"append refusé (doublon)")
    with chemin.open("a", encoding="utf-8") as f:
        f.write(bloc)
    print(f"[consigner] {nom} : appendé ({len(bloc)} caractères)")


ENTREE_241 = """

## Entrée 241 — LE POINT DE REPRISE APRÈS LA VAGUE 3 : le bac à sable local RAPATRIÉ depuis le dépôt (resté à 24a04d6 — les six paquets vécurent dans d'autres instances, le dépôt git FIT FOI), les TROIS MIROIRS recoupés (HEAD == origin/main == ac42880, le bundle Drive VERT par l'instrument D199), la re-exécution du vérificateur TLA+ clone-frais 13/13 VERT (les pièces consignées restaurées intactes), les QUATRE scellés recoupés INTACTS, les SIX instructions de la vague ARCHIVÉES (/instructions VIDE) (12/11, la session du point de reprise)

**Le constat d'ouverture.** Le bac à sable local portaient l'état de l'Entrée 233 (24a04d6, 11/11 18:38) — les SIX paquets de la vague 3 (Entrées 234-240, D200-D205, Tasks 140-147, commités 21:03-00:18) vécurent dans d'AUTRES instances du laboratoire : la preuve vit au dépôt. LE RAPATRIEMENT : git fetch (origin/main == ac42880), les changements locaux de mode de fichiers ignorés (core.fileMode=false — artefact du montage, zéro octet de contenu), fast-forward PULLED — le journal local porte désormais les 200 entrées, la dernière 240 ; l'arbre de travail PROPRE. LES TROIS MIROIRS : (a) HEAD == ac42880 == origin/main (le fetch relu) ; (b) le bundle triade-history.bundle du miroir Drive : git bundle verify VALIDE, refs/heads/main == ac42880 — l'instrument RÉPARÉ (D199) rend son verdict VERT sur la branche canonique ; (c) le garde sceau-I : 14 arbres VERTS, la clé demeurée « reelle (ceremonie hors-ligne, D87) ». La leçon d'exploitation : UN POINT DE REPRISE COMMENCE PAR LES MIROIRS — l'instance locale d'un bac à sable n'est jamais qu'une copie, le dépôt est la source de vérité (l'ordre des gestes de la présente session : recoupement AVANT toute lecture d'état).

**La re-exécution au point de reprise (le modèle de l'Entrée 232 — l'instrument de la vague re-éprouvé depuis l'état committé).** LE VÉRIFICATEUR TLA+ CLONE-FRAIS (scripts/tla_v150/verifier_clone_frais.py) re-exécuté avec les OUTILS REPROVISIONNÉS aux empreintes CONSIGNÉES (tla2tools.jar sha256 e1f11b75c4b5bc44… EXACT ; apalache-0.63.0.tgz a756e96af249bf33… EXACT — téléchargés amont v0.63.0/v1.8.0, recoupés AVANT usage, l'environnement est re-téléchargeable par conception [.gitignore : « outils TLA+/Apalache : ENVIRONNEMENT, pas artefacts »]) : **13/13 VERT** — le clone neuf porte la fidélité D187 (154 états / 1 152 transitions REPRODUITS EXACTEMENT), les espaces 154/216/360, le déchargement Apalache (base + pas inductif, entiers non bornés) et ses DEUX contrôles négatifs ATTRAPÉS, la campagne PBT 200/200 condensats IDENTIQUES au CSV committé. LA COMPARAISON À LA PIÈCE CONSIGNÉE : les VERDICTS identiques ; l'unique divergence du rapport NOMMÉE — la ligne HEAD (cb3968f à la consignment du paquet 1, ac42880 au rejeu : l' horodatage du clone, jamais un verdict) et les journaux d'outils (chemins temporaires, graines, pids) ; LA PIÈCE CONSIGNÉE RESTAURÉE INTACTE après le geste (le modèle D192 tenu : verification_clone_frais_rapport.txt sha256 7bab89e4267dcff0… recoupé == le committé, les logs_clone_frais/ restaurés par git checkout, l'arbre PROPRE) — le rejeu vit dans la présente entrée, la pièce consignée demeure. LES QUATRE SCELLÉS recoupés INTACTS : loupe.exe c111510535767a40…, proxy.exe [tls13/] 446279f3ab356900…, demo.exe df8f2e50949b14c0…, selftest.exe [m1/] 8038585b7af83c9f… — chacun == les empreintes des frontières de l'Entrée 240.

**L'archivage des six instructions (la règle D197 appliquée à la vague).** Les SIX programmes sont EXÉCUTÉS et consignés (Entrées 235-240) : 6zqo2h60n (TLA+/Apalache), n4kwcs3wa (mutation 10 400), xboh1kljq (reclassement), sollwnmae (révision), 54wni4hzh (plan comparaison), lfh49a1xf (SHA-NI) — l'instruction s'archive APRÈS exécution. scripts/archiver_instructions_vague3.py : pour CHACUN des six — le md5 recoupé AVANT à /instructions, le déplacement /instructions → /ARCHIVE (aucun contenu modifié, aucune suppression), le md5 recoupé APRÈS à /ARCHIVE, l'absence constatée au source ; **6/6 OK — /instructions VIDE** (le dossier ne porte plus RIEN ; l'archive porte les DOUZE instructions des trois vagues, empreintes inchangées). Le geste manquait à la clôture de la vague : la session interrompue commita le paquet 6 (00:18) sans l'archivage — la présente session le SOLD.

**L'état.** La vague 3 est EXÉCUTÉE en ses six paquets, consignée (D200-D205), vérifiée au point de reprise (13/13 + les miroirs + les scellés). Le programme du laboratoire demeure ÉPUISÉ pour ce qui est outillable ; les attentes du développeur, nommées à l'Entrée 240 : (a) LE TÉMOIN DU KIT SHA-NI (temoin-shani.txt — la mesure terrain avant/après, le LISEZMOI en cinq minutes) ; (b) LA CÉRÉMONIE D'ÈRE si la variante s'embarque (aucun bloc shani dans la carte — les ids g210001..003 préfigurés) ; (c) LA CAMPAGNE DE COMPARAISON des workflows (le plan verrouillé D204, les bras T/C, AUCUNE mesure exécutée) ; (d) les suites nommées de l'Entrée 232 demeurent (le séquestre D183, la cérémonie d'ère, la réplication). Aucun programme inventé pour soi-même : la session de reprise VÉRIFIE, RAPATRIE, ARCHIVE, CONSIGNE — et rend la main au développeur.

**Frontières.** Aucun artefact scellé touché (les QUATRE recoupés INTACTS) ; le garde sceau-I 14/14 VERT avant et après ; aucune pièce consignée modifiée (le rapport clone-frais et les journaux RESTAURÉS à l'identique après le rejeu, l'arbre PROPRE) ; l'archivage par DÉPLACEMENT uniquement (aucune suppression, empreintes recoupées avant/après) ; le coffre réel jamais ouvert ; les consignations antérieures non réécrites (append-only).
"""

TASK_148 = """

Task ID: 148
Agent: Z.ai (agent principal)
Task: LE POINT DE REPRISE APRÈS LA VAGUE 3 — le rapatriement du bac à
sable local depuis le dépôt (source de vérité), les trois miroirs
recoupés, la re-exécution du vérificateur TLA+ clone-frais 13/13 VERT,
l'archivage des six instructions de la vague, la main rendue au
développeur.

Work Log:
- LE CONSTAT : le bac à sable local était resté à 24a04d6 (Entrée 233) —
  les six paquets de la vague 3 (Entrées 234-240, D200-D205) vécurent
  dans d'autres instances ; le dépôt git fit foi (origin/main ac42880).
- LE RAPATRIEMENT : fast-forward pulled, l'arbre PROPRE, le journal
  local porte les 200 entrées ; core.fileMode=false (les changements de
  mode étaient des artefacts du montage, zéro octet de contenu).
- LES TROIS MIROIRS : HEAD == origin/main == ac42880 ; le bundle Drive
  verify VALIDE, refs/heads/main == ac42880 (l'instrument D199 VERT) ;
  le garde sceau-I 14/14 VERT (clé reelle).
- LA RE-EXÉCUTION : verifier_clone_frais.py 13/13 VERT — les outils
  reprovisionnés aux empreintes consignées (tla2tools e1f11b75…,
  apalache.tgz a756e96a… EXACTS), la fidélité D187 154/1 152 REPRODUITE,
  le déchargement Apalache + les contrôles négatifs, la PBT 200/200
  IDENTIQUE ; la pièce consignée RESTAURÉE intacte (7bab89e4…) après le
  geste (modèle D192) ; les QUATRE scellés recoupés INTACTS
  (loupe.exe c1115105…, proxy.exe 446279f3…, demo.exe df8f2e50…,
  selftest.exe 8038585b…).
- L'ARCHIVAGE : les SIX instructions de la vague 3 déplacées
  /instructions → /ARCHIVE, md5 recoupés avant/après, 6/6 OK —
  /instructions VIDE (le geste manquant de la clôture, soldé).
- L'ÉTAT : la vague 3 exécutée en ses six paquets ; au développeur —
  le témoin du kit SHA-NI, la cérémonie d'ère si embarquement, la
  campagne de comparaison (plan D204), et les suites nommées (séquestre
  D183, réplication).
- Frontières : aucun scellé touché, aucune pièce consignée modifiée,
  append-only, aucun chiffre fabriqué.
"""


def main() -> int:
    # NB : la formule de clôture « append-only » revient à plusieurs
    # entrées — le marqueur de fin retenu est la phrase UNIQUE de la
    # frontière de l'Entrée 240 (temoin-shani.txt attendu), puis la fin
    # réelle du fichier est confrontée séparément.
    texte = JOURNAL.read_text(encoding="utf-8")
    if texte.count("le kit livré, temoin-shani.txt attendu") != 1:
        sys.exit("[consigner] JOURNAL : le marqueur de l'Entrée 240 "
                 "n'apparaît pas exactement une fois — append refusé")
    if not texte.rstrip("\n").endswith(
            "les consignations antérieures non réécrites (append-only)."):
        sys.exit("[consigner] JOURNAL : la fin du fichier n'est pas la "
                 "frontière attendue de l'Entrée 240 — append refusé")
    if "Entrée 241" in texte:
        sys.exit("[consigner] JOURNAL : Entrée 241 déjà présente — "
                 "append refusé (doublon)")
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(ENTREE_241)
    print(f"[consigner] JOURNAL_TRAVAIL.md : appendé "
          f"({len(ENTREE_241)} caractères)")
    append_verifie(WORKLOG,
                   "les bras T/C, le plan verrouillé D204).",
                   TASK_148, "worklog.md", "Task ID: 148")
    print("[consigner] Entrée 241 + Task 148 : CONSIGNÉES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
