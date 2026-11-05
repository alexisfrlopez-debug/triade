#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_d169.py — LA CONSIGNATION DE LA DÉCISION D169 (la consolidation
v0.7.0) au journal des décisions. Append-only : l'entrée suit D168. Tout
ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
DECISIONS = REPO / "docs" / "DECISIONS.md"

D169 = """

## D169 — LA SPÉCIFICATION v0.7.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M7 (le jalon M8 — le domaine `sys`, les syscalls directs — franchi, finale 0.9.0 scellée sur run terrain vert recoupé 30/30 ; le jalon M9 — le domaine `tls13`, TLS 1.3 pur — ouvert, sa couche I complète, SA CÉRÉMONIE D'ÈRE PASSÉE le 05/11 [13 arbres, garde 13/13, la dette D166 soldée] ; le sceau de l'Intention portant TREIZE arbres et ses cérémonies d'ère entrant au protocole) ; LA CLAUSE « HORS PÉRIMÈTRE COURANT » EST LEVÉE NOMMÉMENT POUR LES DEUX PREMIÈRES FAMILLES (D160), les profils additionnels demeurant hors périmètre

**Le contexte qui fonde la décision (05/11 au soir, la demande du développeur).** « Je voudrais que tu produises la dernière version complète du document pdf Protocole TRIADE. » La demande arrive au moment nommé : la cérémonie de l'ère M9 vient d'être installée (le garde 13/13) et la spécification vivante est EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 12.4 dit « Dix arbres » alors que le sceau en porte treize ; le § 18 titre « jalons M0 à M7 » alors que M7 est franchi (0.8.0, Entrée 155) et que M8/M9 n'y figurent pas ; la clôture du § 21 tient les syscalls directs et TLS 1.3 pur « hors périmètre courant » alors que D160/D166 les ont ouverts et que M8 est FRANCHI ; l'état des jalons de l'en-tête s'arrête à M6. Le versionnement suit les RÉVISIONS, jamais les franchissements (addendum Task 62) — mais un PROGRAMME entré en exécution EST une révision en attente de sa passation : la v0.7.0 est la passation du programme d'après M7 dans la spécification, le miroir exact de ce que D133 fit pour la souveraineté cryptographique.

**Les règles.** (1) **Le programme d'après M7 entre en spécification** : la clause « hors périmètre courant » de la clôture v0.6.1 est LEVÉE NOMMÉMENT pour les deux premières familles (syscalls directs — accompli ; TLS 1.3 pur — en cours), les profils additionnels demeurent hors périmètre (chacun répétera M6/M7 sur résultats mesurés). (2) **Le sceau est consigné à son état réel** : TREIZE arbres (m0–m8, tls13, demo, terrain, v06) et les cérémonies d'ère entrent au protocole (§ 12.4, § 13.5) — la dette se nomme à la naissance (D166 règle 8), la charge se prépare au geste qui sert la main (D168), la continuité de clé se prouve par le déterminisme Ed25519 (D163). (3) **L'état des jalons est constaté** : M0–M8 franchis (balises 0.2.0 à 0.9.0), M9 ouvert — la cérémonie de son ère passée sur pièces. (4) **Aucune règle du cœur n'est modifiée, aucune couche n'est ajoutée à l'exécution, la hiérarchie est inchangée** — la révision consolide, elle ne légifère pas.

**Alternatives rejetées.** Régénérer la seule v0.6.1 sur les sources courantes (rejeté : le document aurait continué de dire « dix arbres » et de tenir M8/M9 hors spécification — la demande porte sur la DERNIÈRE version COMPLÈTE, pas sur la plus récente impression de l'ancienne) ; attendre la finale 1.0.0 pour réviser (rejeté : la consolidation suit le PROGRAMME, pas la finale — la cérémonie d'ère passée est le moment nommé, le précédent D133 fut la passation du programme accompli) ; signer les sources `docs/` sous le sceau courant (rejeté : le modèle par-version demeure, `v06/I/README.md` § 1) ; ouvrir les profils additionnels dans la même révision (rejeté : hors périmètre, sur résultats mesurés) ; réviser à chaque franchissement (rejeté : le versionnement suit les RÉVISIONS — la présente est la passation d'un programme, pas un constat de plus).

**Frontières.** Les balises INTACTES (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 — la révision documente, elle ne scelle rien) ; l'archive v0.6.1 DEMEURE (docs/Protocole_TRIADE_v0.6.1_Specification.pdf, dernier build consigné sha256 4aac10f1…, 984 555 o — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ (la révision ne touche pas le coffre) ; la chaîne spec_v061 devient spec_v070 par RENOMMAGE git (le modèle des révisions précédentes — l'ancienne chaîne reste dans l'histoire). Les pièces : docs/PROTOCOLE_TRIADE.md (v0.7.0), scripts/revision_v070_md.py + scripts/revision_v070_tex.py (les remplacements ASSERTÉS), scripts/spec_v070/ (la chaîne), scripts/spec_v070/verify_spec.py (le cahier V1–V16), docs/Protocole_TRIADE_v0.7.0_Specification.pdf (l'artefact, empreinte consignée PAR LE BUILD).
"""

def main() -> int:
    t = DECISIONS.read_text(encoding="utf-8")
    if "## D169 —" in t:
        print("[inserer-d169] REJEU REFUSÉ : D169 existe déjà.")
        return 1
    ancre = "l'état du sceau au geste (check_auth.py : m0 DIVERGE + tls13 DEPOT INCOHERENT + 11 verts)."
    n = t.count(ancre)
    if n != 1:
        print(f"[inserer-d169] ÉCHEC : ancre de fin D168 {n} fois.")
        return 1
    t = t.rstrip("\n") + "\n" + D169.strip("\n") + "\n"
    DECISIONS.write_text(t, encoding="utf-8")
    print("[inserer-d169] PASSÉ : D169 consignée à la suite de D168.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
