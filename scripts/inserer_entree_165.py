#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_165.py — LA CONSIGNATION DU GESTE « ON OUVRE LA SUITE » :
JOURNAL_TRAVAIL +Entrée 165 (ordre 164<165<marqueur, rejeu REFUSÉ), worklog
+Task ID 83. D166 et le PLAN sont DÉJÀ consignés (vérifiés par ancres — tout
ancrage absent = ÉCHEC NOMMÉ, rien n'est écrit)."""

import pathlib

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 165 — « on ouvre la suite » : LA SECONDE FAMILLE OUVERTE — TLS 1.3 PUR EN BLOCS SCELLÉS (le jalon M9, le domaine `tls13`, l'ère 1.0.0) ; l'ère M8 refermée propre par l'export de continuité 0.9.0, la couche I fondée, la dette de cérémonie nommée à la naissance (05/11)

**La reprise (D164 rejouée).** Les trois miroirs confrontés : le dépôt local INTACT à 8ced0bb (la pointe consignée du Task 82), GitHub à l'IDENTIQUE sur la branche jalon (la branche main demeure l'ancienne par défaut, figée depuis le 31/10 — un constat, pas une divergence), le bundle miroir 090-4edf0c3 AU GESTE + sa consignation (le schéma normal de fin de session — le worklog du Task 82 fait foi) ; les canaux OAuth Drive + GitHub 200 (check_auth.py). qemu-riscv64 avait disparu avec le recyclage du disque — RÉINSTALLÉ PAR SA PROCÉDURE (riscv/outils/installer_qemu.sh : qemu-user 10.0.13, extraction locale sans privilèges — la réserve instrumentale D149 re-vérifiée avant usage, exactement le scénario qu'elle consigne).

**L'ère M8 refermée propre (le modèle Entrée 156 rejoué à la pointe 0.9.0).** L'instrument étendu au scellé win COURANT : riscv/export_continuite.py porte désormais m8/proxy.exe 0.9.0 + la carte génération 8 (les couches I m0..m5 + m8/I ; le nom du conteneur porte LA POINTE des balises — max des versions par profil). Le conteneur régénéré TRIADE-continuite-multiprofils-0.9.0-20261105T115943Z.bin (779 272 o, md5 3de022b7…) : verrou croisé 34 empreintes de blocs + 5 artefacts entiers conformes aux frag-bld (les DEUX ISA), rituels VERTS au geste même (corpus unix natif + corpus riscv sous qemu — le scellé win se rejoue au poste Windows, frontière nommée), l'import à sec CINQ étapes VERT (85 spécifications I transportées : les 4 de m8/I comprises, versions win 0.9.0 / linux 0.7.0 / riscv 0.8.0), la preuve d'exécution VERT sur les octets TRANSPORTÉS ; la copie au coffre racine relu MATCH ; les anciens conteneurs 0.8.0 et 0.8.0-rc.1 DEMEURENT (rien ne se jette).

**La couche I fondée (écrit-avant-code, R2).** Le domaine `tls13` créé — l'identifiant `tls` est PRIS par M4 (la poignée Schannel) et « un identifiant n'est jamais réutilisé ». La charte à HUIT règles (la suite constante TLS_AES_128_GCM_SHA256 + x25519, les vecteurs officiels AVANT usage, le temps constant NOMMÉ par bloc, le transcript source de vérité, l'échec propre et nommé, le bloc ne détient rien, aucun import aucun syscall, le padding NOP) ; le tableau des 28 blocs en SIX familles (sha, hkdf, x25519, aead, enregistrement, poignée + principal), les identifiants machine h10xxxx (la famille `h` est libre : la carte génération 8 porte a/b/c/e/g) ; la famille `sha` SPÉCIFIÉE (tls13-01..04, les miroirs win des contrats ah-04..07 de M6 — le contexte en ARGUMENT : TLS exige des hachages MULTIPLES simultanés, le modèle ah à contexte d'adresse fixe ne survivrait pas) ; le plan d'adressage PRÉFIGURÉ (tls13/layout.py : .text6 raw 0xAE00 / RVA 0xC000, les versions 1.0.0-dev.1 / 1.0.0, la table des SEPT verdicts, les H0 FIPS — **la préfiguration n'est pas un droit**, D161 rejoué : les slots s'arrêtent à la notation sur les longueurs réelles).

**La dette de cérémonie nommée à la naissance (D162 rejouée volontairement).** Le registre figé m0/I/README.md étendu (`tls13`, M9) et l'arbre tls13/I neuf : le garde CONSTATE au geste même m0 CODE 10 (fichier modifié : README.md — un diff d'intention) + tls13 CODE 12 (manifeste déposé absent), les ONZE autres arbres verts ; la charge a-signer.txt PRÉPARÉE (13 arbres, remise minimale m0 + tls13 — les arbres inchangés rendront les MÊMES signatures par déterminisme Ed25519, la preuve de D163). AUCUN build M9 avant la remise du développeur (sa clé hors-ligne, D87) — le refus nommé est le résultat, pas la panne.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES — la 1.0.0-dev.1 naîtra du premier BUILD M9, geste de BUILD après la cérémonie) ; l'artefact m8/proxy.exe INTACT (1492b0bc…, 44 544 o — le fait de carte D165) ; l'anti-rollback 0.9.0 ARMÉ ; les 24 spécifications restantes précèdent toute notation (R2). Livrables : riscv/export_continuite.py (l'instrument étendu), riscv/export/TRIADE-continuite-multiprofils-0.9.0-20261105T115943Z.bin (au coffre racine relu MATCH), tls13/I/ (README la charte + tls13-01..04 la famille sha), tls13/layout.py (la préfiguration), m0/I/README.md (le registre figé étendu), v06/sceau_I.py (la table à 13 arbres), v06/sceau-I/a-signer.txt (la charge du développeur) ; consignations : la présente Entrée PAR SCRIPT, D166 PAR SCRIPT (docs/DECISIONS.md), PLAN (la famille (2) OUVERTE, la table des chantiers M9, l'État du programme), worklog +Task ID 83 ; scripts suivis : inserer_entree_165.py.

- SUITE : LE CHANTIER M9-(a) CONTINUE (les 24 spécifications restantes : hkdf, x25519, aead, enregistrement, poignée, principal — AVANT toute notation, R2) ; le kit de cérémonie de l'ère M9 à préparer au dossier /Cérémonie du Drive (la remise du développeur précède tout build, modèle Entrée 159).

"""

TASK = """
## Task ID 83 — « on ouvre la suite » : LA SECONDE FAMILLE OUVERTE — LE JALON M9 TLS 1.3 PUR (domaine `tls13`, ère 1.0.0) ; l'ère M8 refermée propre (export 0.9.0 au coffre racine), la couche I fondée, la dette de cérémonie nommée (05/11)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == 8ced0bb la
  pointe ; le bundle 090-4edf0c3 au geste — le schéma normal), les canaux
  200 ; qemu-riscv64 réinstallé PAR SA PROCÉDURE (10.0.13, la réserve
  D149 re-vérifiée avant usage).
- L'ÈRE M8 REFERMÉE PROPRE : riscv/export_continuite.py étendu au scellé
  win COURANT (m8/proxy.exe 0.9.0 + carte génération 8 + m8/I) ; le
  conteneur 0.9.0 (779 272 o, md5 3de022b7…) régénéré, import à sec CINQ
  étapes VERT, preuve d'exécution VERT sur les octets transportés, copie
  au coffre racine relu MATCH ; les anciens 0.8.0 demeurent.
- LA COUCHE I FONDÉE : le domaine `tls13` (l'identifiant `tls` appartient
  à M4 — jamais réutilisé) ; la charte à HUIT règles ; le tableau des 28
  blocs (h10xxxx, SIX familles) ; la famille `sha` spécifiée (les 4
  miroirs win des contrats ah-04..07, le contexte en ARGUMENT) ;
  tls13/layout.py préfiguré (.text6, versions 1.0.0, SEPT verdicts — la
  préfiguration n'est pas un droit, D161).
- LA DETTE DE CÉRÉMONIE NOMMÉE : le garde constate m0 CODE 10 + tls13
  CODE 12 (les 11 autres verts) ; a-signer.txt préparé (13 arbres, remise
  minimale m0 + tls13) ; AUCUN build avant la remise du développeur.
- FRONTIÈRES : aucune balise ne bouge (0.9.0/0.7.0/0.8.0 INTACTES), le
  1.0.0-dev.1 naîtra du premier BUILD M9 ; m8/proxy.exe INTACT
  (1492b0bc…) ; consignations : Entrée 165 PAR SCRIPT, D166 PAR SCRIPT,
  PLAN (famille (2) OUVERTE + table M9 + État), worklog +Task ID 83 ;
  scripts suivis : inserer_entree_165.py.
- SUITE : les 24 spécifications restantes du chantier M9-(a) (hkdf,
  x25519, aead, enregistrement, poignée, principal — R2) ; le kit de
  cérémonie de l'ère M9 au /Cérémonie du Drive (modèle Entrée 159).

Stage Summary:
- LA SECONDE FAMILLE EST OUVERTE sur la demande « on ouvre la suite »
  (D166, le modèle D149/D160) : TLS 1.3 pur en blocs scellés — le jalon
  M9, la grande œuvre, l'ère 1.0.0.
- L'ÈRE M8 S'EST REFERMÉE PROPRE (l'export de continuité 0.9.0 au coffre
  racine) ET LA DÉTTE DE CÉRÉMONIE EST NÉE NOMMÉE : le garde refuse
  jusqu'à la remise du développeur — c'est son travail, exactement comme
  en D162.
"""


def main() -> int:
    journal = JOURNAL.read_text(encoding="utf-8")
    worklog = WORKLOG.read_text(encoding="utf-8")
    decisions = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    plan = (REPO / "docs" / "PLAN_MILESTONES.md").read_text(encoding="utf-8")

    ancres = {
        "l'Entrée 164 (l'ordre)": "## Entrée 164 —" in journal,
        "l'Entrée 165 absente (rejeu refusé)": "## Entrée 165 —" not in journal,
        "le marqueur du journal": MARQUEUR in journal,
        "le Task 82 au worklog": "## Task ID 82 —" in worklog,
        "le Task 83 absent (rejeu refusé)": "## Task ID 83 —" not in worklog,
        "D166 déjà consignée": "## D166 —" in decisions,
        "le PLAN porte la table M9": "Chantier M9 (win, l'ère 1.0.0" in plan,
        "le PLAN porte la famille ouverte": "le domaine `tls13` créé au registre figé" in plan,
    }
    manquantes = [n for n, ok in ancres.items() if not ok]
    if manquantes:
        print(f"[inserer-165] ÉCHEC NOMMÉ — ancres absentes : {manquantes}")
        return 2

    journal = journal.replace(
        MARQUEUR, ENTREE + MARQUEUR, 1)
    JOURNAL.write_text(journal, encoding="utf-8")
    with WORKLOG.open("a", encoding="utf-8") as f:
        f.write(TASK)
    print("[inserer-165] Entrée 165 insérée avant le marqueur ; Task 83 ajouté ; "
          "D166 et le PLAN constatés déjà en place")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
