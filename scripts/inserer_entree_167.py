#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_167.py — LA CONSIGNATION DU GESTE « LE KIT DE CÉRÉMONIE DE
L'ÈRE M9 DÉPOSÉ » : JOURNAL_TRAVAIL +Entrée 167 (ordre 166<167<marqueur,
rejeu REFUSÉ), DECISIONS +D168, worklog +Task ID 85. Tout ancrage absent =
ÉCHEC NOMMÉ, rien n'est écrit."""

import pathlib

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 167 — LE KIT DE CÉRÉMONIE DE L'ÈRE M9 DÉPOSÉ au dossier /Cérémonie du Drive (modèle Entrée 159) : LA REMISE RÉGÉNÉRÉE SUR L'ARBRE COMPLET (UNE ligne bougée sur treize — tls13 : la charge de l'ouverture était PÉRIMÉE par le geste des 24 specs), le LISEZMOI-ceremonie-ere-M9.txt écrit et déposé (la re-signature m0 + tls13 pas à pas, la règle d'or « JAMAIS generer »), l'erratum de la ligne SUITE de l'Entrée 166 consigné (le garde exige la remise pour LE BUILD, pas pour la notation) (05/11 au soir)

**La reprise (D164 rejouée).** Les trois miroirs confrontés : le dépôt local == GitHub == e83a27e (la pointe consignée du Task 84 — la passation commitée), le bundle miroir 090-64eae8e AU GESTE (M9-(a) complet, + sa consignation — le schéma normal : le bundle porte le geste, la passation le suit) ; les canaux OAuth Drive + GitHub 200 (check_auth.py : l'état du sceau lu au geste même — clé « reelle » 173fae9c…, m0 DIVERGE [fichier modifié : README.md], tls13 DEPOT INCOHERENT [manifeste déposé absent], les ONZE autres verts — la dette de cérémonie CONSTATÉE sur pièces avant le geste).

**La charge régénérée (la découverte du geste).** La remise préparée à l'OUVERTURE (Task 83) portait tls13 0ef882d6… — l'empreinte de l'arbre ALORS naissant (le README + les 4 specs sha). Le geste des 24 spécifications (Task 84) a fait bouger l'arbre : la charge était PÉRIMÉE. `sceau_I.py preparer` rejoué au geste de la cérémonie : UNE ligne bougée sur treize (tls13 → 9ff91874d7ef2e364930b704aa0146d3474c10a858c6b725a0bba75ddc081c9c — l'empreinte de l'ARBRE COMPLET : le registre + les 28 spécifications), les DOUZE autres octet-identiques (le déterminisme). SANS la régénération, la remise signée par le développeur aurait laissé tls13 CODE 10 APRÈS installation (l'arbre ≠ le manifeste) : la cérémonie aurait échoué son objet, le geste du développeur gaspillé. LA RÈGLE QUI EN DÉCOULE : la charge se prépare AU GESTE DE LA CÉRÉMONIE — l'ouverture ANNONCE (une charge provisoire constate l'état), la cérémonie EXIGE (la charge de l'arbre courant, préparée dans le geste qui sert la main).

**Le LISEZMOI et le dépôt.** LISEZMOI-ceremonie-ere-M9.txt (le modèle de l'ère M8, Entrée 159) : le POURQUOI (le garde refuse — m0 divergé [le registre figé étendu au tls13], tls13 jamais signé), les DEUX empreintes qui exigent la signature (m0 4ebe6a2c… — le registre étendu ; tls13 9ff91874… — le domaine complet), les ONZE autres inchangées (re-signées à l'identique par le déterminisme Ed25519 — la preuve D163), LA RÈGLE D'OR (« JAMAIS generer » — la clé du 04/11 173fae9c… réutilisée, l'état « reelle » ne se régresse pas), la cérémonie PAS À PAS (le mode console et le mode graphique, l'atomicité du dépôt), ce que cela DÉBLOQUE (le garde TREIZE arbres verts → construire() → 1.0.0-dev.1, le geste de BUILD jamais scellage — le miroir D162/D165), et le contrat D87 (la clé privée ne traverse JAMAIS le bac à sable). Déposé au /Cérémonie par scripts/deposer_lisezmoi_ere_m9.py : md5 CONTRÔLÉ PAR RELECTURE, la remise du kit recoupée == celle du dépôt (la synchro D130 porta la charge régénérée dans le geste du commit).

**L'erratum de la ligne SUITE de l'Entrée 166 (consigné avant usage).** La ligne disait : « PUIS le chantier (b) — la notation et les vecteurs officiels — APRÈS la remise (le garde le requiert) ». IMPRÉCIS : le garde exige la remise pour LE BUILD (construire(), le chantier (e) au plan M9), PAS pour la notation — le miroir de l'ère M8 : la notation fut réalisée AVANT la cérémonie (Entrée 157 [le chantier (b) M8 réalisé] précéda Entrée 158 [la cérémonie D162]). La correction est consignée ICI, en tête du geste qui suit, AVANT qu'un chantier ne s'ouvre sur la ligne fausse — le journal est append-only : l'erratum se consigne, il ne réécrit jamais.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES), AUCUN build (la dette demeure JUSQU'À la remise du développeur — c'est le travail du garde), AUCUN octet de notation (R2), m8/proxy.exe INTACT (1492b0bc…) ; la charge préparée à l'ouverture DEMEURE dans l'histoire (le diff du geste la cite — rien ne se jette, D143). Livrables : v06/sceau-I/a-signer.txt (la charge régénérée, 13 arbres), LISEZMOI-ceremonie-ere-M9.txt (au /Cérémonie + la copie labo download/), scripts/deposer_lisezmoi_ere_m9.py ; consignations : la présente Entrée PAR SCRIPT, D168 PAR SCRIPT, worklog +Task ID 85 ; scripts suivis : inserer_entree_167.py, deposer_lisezmoi_ere_m9.py.

- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer la remise 13 arbres avec la clé du 04/11, ramener signatures-I.txt + cle-publique-I.txt au coffre) → LE LABO INSTALLE ET RECROISE (sceau_I.py deposer, le garde 13/13) ; EN PARALLÈLE LICITE : le chantier (b) — la notation des 28 blocs aux adresses préfigurées + les vecteurs officiels (FIPS 180-4, RFC 4231, RFC 5869, RFC 7748 § 6.1, SP 800-38D, CAVP) — la falsification, zéro silence.

"""

DECISION = """
## D168 — LA CHARGE DE CÉRÉMONIE SE PRÉPARE AU GESTE DE LA CÉRÉMONIE (la charge de l'ouverture était PÉRIMÉE par le geste des 24 specs : une empreinte sur treize avait bougé — tls13 0ef882d6… → 9ff91874… ; preparer rejoué, UNE ligne, les douze autres octet-identiques — une remise signée sur la charge périmée aurait laissé tls13 CODE 10 APRÈS installation : la cérémonie aurait échoué son objet) ; LE KIT DE L'ÈRE M9 DÉPOSÉ AU /Cérémonie (modèle Entrée 159 : le LISEZMOI pas à pas + la remise FRAÎCHE + les outils — la main du développeur SERVIE, md5 contrôlés par relecture) ; L'ERRATUM DE LA LIGNE SUITE DE L'ENTRÉE 166 (le garde exige la remise pour LE BUILD — construire(), chantier (e) — jamais pour la notation : le miroir M8, Entrées 157/158 ; la correction consignée en tête du geste suivant, le journal n'étant jamais réécrit)

**Le contexte qui fonde la décision (05/11 au soir, le geste du kit).** Le SUITE du Task 84 nommait le kit de cérémonie au /Cérémonie (modèle Entrée 159). Au geste de le servir, la confrontation a nommé une PÉREMPTION : la charge a-signer.txt préparée à l'OUVERTURE du M9 portait l'empreinte de l'arbre tls13 ALORS naissant (README + 4 specs sha) — le geste des 24 spécifications avait fait bouger l'arbre, la charge ne correspondait plus. Le garde constatait au geste même : m0 DIVERGE (le registre étendu), tls13 DEPOT INCOHERENT (jamais signé) — la dette de cérémonie exactement telle que D166 l'avait nommée à la naissance.

**Les règles.** (1) **La charge se prépare AU GESTE DE LA CÉRÉMONIE** : l'ouverture ANNONCE (sa charge est un constat provisoire de l'état), la cérémonie EXIGE la charge DE L'ARBRE COURANT — préparée dans le geste qui sert la main du développeur. La preuve par le geste : tls13 0ef882d6… (l'ouverture) ≠ 9ff91874… (l'arbre complet des 28 specs) ; une remise signée sur la charge périmée aurait installé un manifeste divergent de l'arbre — tls13 serait DEMEURÉ CODE 10, le geste du développeur gaspillé. (2) **Le kit sert la main** : le LISEZMOI porte les DEUX empreintes qui exigent la signature (m0 4ebe6a2c…, tls13 9ff91874…), les onze autres inchangées (le déterminisme Ed25519 les rendra identiques — la preuve D163), LA RÈGLE D'OR (« JAMAIS generer » : la clé du 04/11 réutilisée, l'état « reelle » ne se régresse pas), les pas à pas console ET graphique, l'atomicité du dépôt, et le contrat D87 (la clé privée ne traverse jamais le bac à sable — le labo ne signera jamais à la place du développeur). (3) **Le dépôt se recoupe** : le LISEZMOI téléversé md5 par relecture ; la remise du kit == celle du dépôt (la synchro D130 porte la charge régénérée dans le geste du commit — le kit ne peut pas prendre un coup de retard). (4) **L'erratum se consigne, il ne réécrit pas** : la ligne SUITE de l'Entrée 166 disait le chantier (b) « APRÈS la remise (le garde le requiert) » — le garde exige la remise pour LE BUILD (construire(), le chantier (e)), pas pour la notation (le miroir M8 : Entrée 157 précéda Entrée 158) ; la correction vit EN TÊTE du geste suivant, le journal append-only ne se réécrit jamais.

**Alternatives rejetées.** Déposer le kit avec la charge de l'ouverture (rejeté : périmée — la cérémonie aurait échoué son objet APRÈS le geste du développeur : le pire des gaspillages) ; régénérer la charge à CHAQUE geste (rejeté : la charge n'a d'objet qu'au geste de la cérémonie — la régénérer au chantier (a) l'aurait périmée au chantier (b) : la règle est le geste qui sert la main, pas un rythme) ; corriger l'Entrée 166 en place (rejeté : append-only — l'erratum en tête du geste suivant, jamais la réécriture) ; laisser la ligne SUITE imprécise (rejeté : le prochain chantier s'ouvrirait sur une fausse dépendance — la notation n'attend pas la remise, le build oui) ; signer au labo pour épargner le développeur (rejeté : D87 — la clé de TEST déclasserait l'état « reelle », une régression de preuve).

**Frontières.** AUCUNE balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 INTACTES) ; AUCUN build avant la remise (le garde m0 CODE 10 + tls13 CODE 12 — la dette EST le verrou, il fait son travail) ; AUCUN octet de notation (R2) ; la charge périmée de l'ouverture DEMEURE dans l'histoire (le diff du geste la cite — rien ne se jette). Les pièces de l'arrêt : v06/sceau-I/a-signer.txt (13 arbres, tls13 9ff91874…), LISEZMOI-ceremonie-ere-M9.txt (au /Cérémonie, md5 recoupé), scripts/deposer_lisezmoi_ere_m9.py, l'état du sceau au geste (check_auth.py : m0 DIVERGE + tls13 DEPOT INCOHERENT + 11 verts).
"""

TASK = """
## Task ID 85 — LE KIT DE CÉRÉMONIE DE L'ÈRE M9 DÉPOSÉ au /Cérémonie (la remise RÉGÉNÉRÉE sur l'arbre complet — la charge de l'ouverture était périmée par les 24 specs ; le LISEZMOI pas à pas ; l'erratum de la ligne SUITE de l'Entrée 166) (05/11 au soir)

- LA REPRISE : les trois miroirs confrontés (local == GitHub == e83a27e la
  pointe, le bundle 090-64eae8e au geste), les canaux 200 ; l'état du sceau
  LU au geste même (clé « reelle » 173fae9c…, m0 DIVERGE + tls13 DEPOT
  INCOHERENT + 11 verts — la dette constatée sur pièces).
- LA CHARGE RÉGÉNÉRÉE : la découverte du geste — a-signer.txt de
  l'ouverture portait tls13 0ef882d6… (l'arbre alors naissant) ; les 24
  specs ont bougé l'arbre ; preparer rejoué : UNE ligne sur treize
  (tls13 → 9ff91874… = L'ARBRE COMPLET : le registre + les 28 specs), les
  douze autres octet-identiques. SANS ce geste, la remise signée aurait
  laissé tls13 CODE 10 APRÈS installation.
- LE LISEZMOI + LE DÉPÔT : LISEZMOI-ceremonie-ere-M9.txt (modèle Entrée
  159 : les deux empreintes m0 4ebe6a2c… / tls13 9ff91874…, la règle d'or
  « JAMAIS generer », les pas à pas console + graphique, le contrat D87) ;
  déposé au /Cérémonie md5 par relecture ; la remise du kit recoupée ==
  celle du dépôt (D130).
- L'ERRATUM : la ligne SUITE de l'Entrée 166 (« le chantier (b) … APRÈS la
  remise ») — IMPRÉCIS : le garde exige la remise pour LE BUILD (chantier
  (e)), pas pour la notation (le miroir M8 : Entrée 157 précéda 158) ;
  consigné en tête du geste suivant, le journal ne se réécrit pas.
- FRONTIÈRES : aucune balise ne bouge, AUCUN build avant la remise (le
  garde fait son travail), AUCUN octet de notation ; consignations :
  Entrée 167 PAR SCRIPT, D168 PAR SCRIPT, worklog +Task ID 85 ; scripts
  suivis : inserer_entree_167.py, deposer_lisezmoi_ere_m9.py.
- SUITE : LE GESTE DU DÉVELOPPEUR (la cérémonie hors-ligne : signer la
  remise 13 arbres à la clé du 04/11, ramener signatures-I.txt +
  cle-publique-I.txt) → le labo installe et recroise (le garde 13/13) ;
  EN PARALLÈLE LICITE : le chantier (b) — la notation des 28 blocs + les
  vecteurs officiels.

Stage Summary:
- LA MAIN DU DÉVELOPPEUR EST SERVIE : la remise est FRAÎCHE (l'arbre
  complet des 28 spécifications), le LISEZMOI la sert pas à pas, la règle
  d'or est réitérée — la cérémonie peut avoir lieu.
- LA CHARGE PÉRIMÉE DE L'OUVERTURE EST LA PREUVE DE LA RÈGLE : la charge
  se prépare au geste de la cérémonie — l'ouverture annonce, la cérémonie
  exige.
"""


def main() -> int:
    journal = JOURNAL.read_text(encoding="utf-8")
    worklog = WORKLOG.read_text(encoding="utf-8")
    decisions = DECISIONS.read_text(encoding="utf-8")

    ancres = {
        "l'Entrée 166 (l'ordre)": "## Entrée 166 —" in journal,
        "l'Entrée 167 absente (rejeu refusé)": "## Entrée 167 —" not in journal,
        "le marqueur du journal": MARQUEUR in journal,
        "le Task 84 au worklog": "## Task ID 84 —" in worklog,
        "le Task 85 absent (rejeu refusé)": "## Task ID 85 —" not in worklog,
        "D167 déjà consignée": "## D167 —" in decisions,
        "D168 absente (rejeu refusé)": "## D168 —" not in decisions,
        "la charge régénérée en place": "9ff91874d7ef2e364930b704aa0146d3474c10a858c6b725a0bba75ddc081c9c"
        in (REPO / "v06" / "sceau-I" / "a-signer.txt").read_text(encoding="utf-8"),
    }
    manquantes = [n for n, ok in ancres.items() if not ok]
    if manquantes:
        print(f"[inserer-167] ÉCHEC NOMMÉ — ancres absentes : {manquantes}")
        return 2

    journal = journal.replace(MARQUEUR, ENTREE + MARQUEUR, 1)
    JOURNAL.write_text(journal, encoding="utf-8")
    with DECISIONS.open("a", encoding="utf-8") as f:
        f.write(DECISION)
    with WORKLOG.open("a", encoding="utf-8") as f:
        f.write(TASK)
    print("[inserer-167] Entrée 167 insérée avant le marqueur ; D168 "
          "consignée ; Task 85 ajouté ; la charge régénérée constatée en place")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
