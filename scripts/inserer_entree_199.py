#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inserer_entree_199.py — LA CONSIGNATION DU GESTE « LA SPÉCIFICATION
v0.8.0 » : JOURNAL_TRAVAIL +Entrée 199 (ordre 198<199<marqueur, rejeu
REFUSÉ), worklog +Task ID 117. Tout ancrage absent = ÉCHEC NOMMÉ, rien
n'est écrit."""

import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds v1"

ENTREE = """## Entrée 199 — LA SPÉCIFICATION v0.8.0 : LA CONSOLIDATION DU PROGRAMME D'APRÈS M9 livrée sur la demande du développeur (la mise à jour du document PDF Protocole TRIADE) — M9 FRANCHI (finale 1.0.0, la session réelle), LE TEST GRANDEUR NATURE OUVERT (M10 « Loupe », la notation 18/18), LA DETTE DU QUATORZIÈME ARBRE NOMMÉE (la cérémonie d'ère du TGN précède tout build), le projet fils COFFRE-FORT dégelé en parallèle (08/11)

**La demande et son moment.** La demande du développeur porte la mise à jour du document PDF Protocole TRIADE au geste qui suit les quatre chantiers de notation du TGN (Entrées 195–198). Le constat du geste : la spécification vivante v0.7.0 est EN RETARD SUR LE PROGRAMME sur quatre points nommés — le § 18 titre « jalons M0 à M9 » et tient M9 « ouvert » alors que M9 est FRANCHI (finale 1.0.0 scellée le 07/11, Entrée 193/D170 : LA SESSION RÉELLE — la ligne applicative chiffrée échangée avec un serveur réel, le témoin « HTTP/1.1 200 OK » déchiffré par la machine, l'épinglage -6 nommé, proxy.exe byte-identique 446279f3…) ; le TGN ouvert à D171 (l'application « Loupe », le domaine `loupe`) et ses QUATRE chantiers de notation accomplis (D172–D175 : les 18 blocs NOTÉS-MESURÉS-PROUVÉS) ne vivent nulle part au document ; le § 13.5 s'arrête aux cérémonies des ères M8/M9 alors que l'ère du TGN porte sa dette nommée (le 14e arbre, D166/D171) ; le projet fils COFFRE-FORT demeure « développement différé » alors que D171 l'a dégelé. Le versionnement suit les RÉVISIONS, jamais les franchissements — mais un programme entré en exécution EST une révision en attente de sa passation : la v0.8.0 est la passation du programme d'après M9, le miroir exact de ce que D169 fit pour le programme d'après M7.

**La révision du maître markdown (PAR SCRIPT, remplacements ASSERTÉS).** scripts/revision_v080_md.py (miroir de revision_v070_md.py) : ONZE remplacements/insertions assertés — le titre et le bloc d'en-tête (l'archive v0.7.0 ajoutée à la liste, la phrase de consolidation du programme d'après M9), la puce Version (M0–M9 franchis, le TGN M10 ouvert, la notation 18/18 posée, le 14e arbre attendu), la puce Date (8 novembre 2026), le § 1.2 porté à M0–M10, le NOUVEAU § 1.10 « Ce que change la v0.8.0 », le § 12.4 (treize arbres + LA DETTE DU QUATORZIÈME), le § 13.5 (le paragraphe de l'ère TGN — la cérémonie attend son geste), le § 18 (le titre M0 à M10, Onze jalons, la rangée M9 FRANCHIE finale 1.0.0, la rangée M10 NOUVELLE, la clôture étendue), le NOUVEAU § 19.10 « Correspondance v0.7.0 → v0.8.0 » avec QUATRE rejets explicites, la ligne v0.8.0 au journal des versions, la clôture du § 21 RÉCRITE.

**La chaîne formelle (spec_v070 → spec_v080 par COPIE, l'archive v070 DEMEURE).** scripts/revision_v080_tex.py : VINGT-TROIS remplacements LaTeX ASSERTÉS — main.tex (l'en-tête de chaîne étendu à D176, fancyhead, pdftitle — v0.8.0) ; sec-a.tex (+ le § 1.10 « Ce que change la v0.8.0 ») ; sec-c.tex (les domaines du profil primaire : sys + tls13 + loupe, le TGN) ; sec-cf.tex (le § 12.4 : la dette du quatorzième arbre ; le § 13.5 : l'ère du TGN — la cérémonie attend son geste, le garde à QUATORZE après) ; sec-d.tex (le titre et l'intro des jalons M0 à M10, M9 PORTÉ franchi finale 1.0.0, la rangée M10 au tableau, la clôture étendue à l'épreuve de la méthode entière, le paragraphe « Le test grandeur nature (D171) », la NOUVELLE correspondance v0.7.0 → v0.8.0 avec ses QUATRE rejets, la synthèse du journal étendue à D176, l'annexe décisionnelle ÉTENDUE de D170 à D176 — SEPT lignes nouvelles) ; cover.html (v0.8.0, la consolidation du programme d'après M9 en sous-titre — VALIDÉE par le contrôleur de chevauchements SANS raccourcissement) ; merge_cover.py (métadonnées v0.8.0) ; build_pdf.sh → spec_v080/v0.8.0.

**Le build et ses preuves.** build_pdf.sh --force : couverture validée (poster_validate + cover_validate PASS — AUCUN chevauchement, la leçon v0.6.1/v0.7.0 tenue), corps Tectonic, fusion, pdf_qa WARN (12 advisories : la classe des tirets cadratins en début de ligne, consignée depuis D133, non bloquants ; le « content overflow » page 31 est le faux positif des filets du tableau des jalons — le miroir exact de la v0.7.0 page 30) ; L'ARTEFACT : docs/Protocole_TRIADE_v0.8.0_Specification.pdf — 45 pages, 1 016 024 o, sha256 95226c2b24dd…, md5 9c5a47b3fdf4198e894918886f959b9a, EMPOINTE CONSIGNÉE PAR LE BUILD (n°26 au TABLEAU_DE_BORD, stamp c40efb955b1e…) ; empreintes_build.py verifier : 14 PDF livrés, 26 consignations, 0 refus — VERT. LE CAHIER scripts/spec_v080/verify_spec.py (V1–V16, miroir du cahier v0.7.0) : 104 CONTRÔLES TOUT PASSÉ — hiérarchie intacte, règles intactes, aucune couche d'exécution, l'héritage v0.5.0–v0.7.0 intact (D75/D81/D133/D137 + les cérémonies d'ère M8/M9), le § 12.4 à TREIZE arbres avec la dette du QUATORZIÈME, le § 13.5 étendu (l'ère du TGN, la remise FRAÎCHE, le garde à QUATORZE), les jalons M0–M10 (M9 franchi, M10 ouvert), la correspondance v0.7.0 → v0.8.0 au PDF, l'annexe étendue à D176, aucune référence non résolue, aucun placeholder, aucune ligne parasite. CONTRÔLE VISUEL PAR CODE (scripts/controle_visuel_v080.py) : 45 pages rendues à 60 dpi, AUCUNE quasi blanche (l'encre minimale p.45 : 0.039 — la fin de l'annexe, normale), la couverture PLEINE PAGE sombre (0.956 de pixels sombres — le bleu nuit de la série), le sommaire écrit ; les pages clés constatées par extraction : la couverture « VERSION 0.8.0 · Consolidation du programme d'après M9 », le § 1.10 page 7, le § 12.4 avec la dette du quatorzième, le § 13.5 pages 25–26 (l'ère du TGN, QUATORZE arbres VERTS : le build de Loupe peut naître), le tableau des jalons pages 29–31 (M0–M9 franchis, M10 ouvert), la correspondance v0.7.0 → v0.8.0 page 37, l'annexe close sur D176 page 45.

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 — la révision documente, elle ne scelle rien), AUCUNE règle modifiée, AUCUNE couche d'exécution ajoutée, la hiérarchie inchangée ; l'archive v0.7.0 DEMEURE (sha dd36eb41… — rien ne se jette) ; le *Livre du Coffre* v1.1 INCHANGÉ ; AUCUN octet de notation (R2) ; le garde sceau I vérifié AVANT consignation : 13 arbres VERTS, cle deposee reelle (D87) — la dette de cérémonie D166/D171 DEMEURE (la spécification documente la cérémonie à venir, elle ne la passe pas). Livrables : docs/PROTOCOLE_TRIADE.md (v0.8.0), docs/Protocole_TRIADE_v0.8.0_Specification.pdf (45 pages, empreinte n°26), scripts/spec_v080/ (la chaîne + le cahier), scripts/revision_v080_md.py + scripts/revision_v080_tex.py + scripts/inserer_d176.py + scripts/controle_visuel_v080.py ; consignations : la présente Entrée PAR SCRIPT, D176 PAR SCRIPT, worklog +Task ID 117.

- SUITE : LA CÉRÉMONIE D'ÈRE DU TGN (le geste hors-ligne du développeur : le kit de cérémonie au /Cérémonie — la remise FRAÎCHE des QUATORZE arbres régénérée AU GESTE [D168 : les empreintes ont bougé avec les quatre chantiers de notation], le LISEZMOI pas à pas, la règle d'or « JAMAIS generer » ; le développeur signe hors ligne à la clé du 04/11 [l'ancre de toutes les ères], ramène signatures-I.txt et cle-publique-I.txt au coffre /test) PUIS le build loupe 0.1.0-dev.1 + le kit terrain (M10-(d) seconde moitié, modèle m9f) et le run terrain (M10-(e)) ; le projet fils attend son premier geste à son message propre.

"""

TASK = """

## Task ID 117 — LA SPÉCIFICATION v0.8.0 LIVRÉE : la consolidation du programme d'après M9 (la demande du développeur : la mise à jour du document PDF Protocole TRIADE) (08/11)

- LA DEMANDE : la mise à jour du document PDF Protocole TRIADE, au geste qui
  suit les quatre chantiers de notation du TGN ; le constat : la v0.7.0 était
  en retard sur le programme (M9 « ouvert » au § 18 alors que FRANCHI, le TGN
  et ses 18 blocs absents du document, le § 13.5 arrêté aux ères M8/M9, le
  fils COFFRE-FORT encore « différé »).
- LA RÉVISION : revision_v080_md.py — 11 remplacements ASSERTÉS (titre,
  en-tête, § 1.10 NOUVEAU, § 12.4 la dette du 14e, § 13.5 l'ère TGN,
  § 18 M0-M10 + M9 franchi + rangée M10, § 19.10 NOUVEAU + 4 rejets,
  journal des versions, clôture réécrite).
- LA CHAÎNE : spec_v070 → spec_v080 par COPIE (l'archive v070 demeure) ;
  revision_v080_tex.py — 23 remplacements LaTeX ASSERTÉS (main 4, sec-a 1,
  sec-c 1, sec-cf 2, sec-d 8, cover 4, merge 3) ; l'annexe décisionnelle
  étendue D170–D176 (SEPT lignes).
- LES PREUVES : le PDF 45 pages, 1 016 024 o, sha256 95226c2b24dd…, md5
  9c5a47b3fdf4…, empreinte CONSIGNÉE PAR LE BUILD (n°26, stamp c40efb95…) ;
  empreintes verifier VERT (14 PDF, 26 consignations, 0 refus) ; LE CAHIER
  V1–V16 : 104 CONTRÔLES TOUT PASSÉ ; contrôle visuel par code : 45 pages
  rendues, AUCUNE quasi blanche, la couverture pleine page sombre validée
  SANS chevauchement ; les pages clés constatées (couverture 0.8.0, § 1.10
  p.7, § 13.5 p.25-26 l'ère du TGN, jalons p.29-31 M10 ouvert, la
  correspondance p.37, l'annexe close sur D176 p.45).
- FRONTIÈRES : aucune balise ne bouge, AUCUNE règle modifiée, AUCUNE couche
  d'exécution ajoutée, hiérarchie inchangée ; l'archive v0.7.0 DEMEURE
  (dd36eb41…), le Livre du Coffre v1.1 INCHANGÉ ; le garde sceau I vérifié
  AVANT consignation : 13 arbres VERTS (la dette D166/D171 demeure — la
  cérémonie d'ère du TGN précède tout build).
- SUITE : LA CÉRÉMONIE D'ÈRE DU TGN (le kit au /Cérémonie, la remise FRAÎCHE
  des 14 arbres régénérée au geste, le geste hors-ligne du développeur à la
  clé du 04/11, les pièces au /test) PUIS le build loupe 0.1.0-dev.1 + le
  kit terrain (M10-(d) seconde moitié) et le run (M10-(e)).
"""


def main() -> int:
    # ---- 1) le journal : l'Entrée 199 AVANT le marqueur (ordre 198 < 199) ----
    t = JOURNAL.read_text(encoding="utf-8")
    if "## Entrée 199 —" in t:
        print("[inserer-entree-199] REJEU REFUSÉ : l'Entrée 199 existe déjà.")
        return 1
    if "## Entrée 198 —" not in t:
        print("[inserer-entree-199] ÉCHEC : l'Entrée 198 absente (ordre rompu).")
        return 1
    n = t.count(MARQUEUR)
    if n != 1:
        print(f"[inserer-entree-199] ÉCHEC : marqueur m5a {n} fois.")
        return 1
    t = t.replace(MARQUEUR, ENTREE.strip("\n") + "\n\n" + MARQUEUR, 1)
    JOURNAL.write_text(t, encoding="utf-8")
    print("[inserer-entree-199] journal : Entrée 199 insérée avant le marqueur.")

    # ---- 2) le worklog : la Task ID 117 en append ----
    w = WORKLOG.read_text(encoding="utf-8")
    if "## Task ID 117 —" in w:
        print("[inserer-entree-199] worklog : Task ID 117 existe déjà.")
        return 1
    w = w.rstrip("\n") + "\n" + TASK.rstrip("\n") + "\n"
    WORKLOG.write_text(w, encoding="utf-8")
    print("[inserer-entree-199] worklog : Task ID 117 ajoutée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
