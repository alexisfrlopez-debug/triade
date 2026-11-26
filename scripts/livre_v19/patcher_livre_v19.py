#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v19.py — le Livre du Coffre v1.16 (né de v1.15 par copie) :
LA RÉCONCILIATION SÉMANTIQUE INTER-PIÈCES (W27RECON, la vague 27, prompt 1 —
priorité 1). Le paragraphe D267 disait « le déploiement n'est pas fait … EN
ATTENTE » alors que le journal d'ancrage append-only détient des entrées
vérifiées v0.27.0 → v0.31.0 et que la spec §7.11, la présentation §4 et les
preuves §5 portent le statut DÉRIVÉ : DÉPLOYÉ. Le statut se dérive du journal
(scripts/vague24/statut_ancrage.py) ; le paragraphe est réécrit au statut
dérivé, les deux ères nommées (la règle adoptée à la vague 20, le déploiement
appliqué depuis). Chaque remplacement EST ANCRÉ (échec si une ancre manque)."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "livre_v18"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "cover.html",
          SRC / "merge_cover.py", SRC / "chaine_cf.html", SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
S1 = (ICI / "sec-1.tex").read_text(encoding="utf-8")
S5 = (ICI / "sec-5.tex").read_text(encoding="utf-8")
COUV = (ICI / "cover.html").read_text(encoding="utf-8")
FUSION = (ICI / "merge_cover.py").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v1.16] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v1.16] ANCRE NON UNIQUE ({txt.count(ancien)}×) — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête (v1.16) ------------------------------------------------------
M = remplace(M, "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.15, h66o54pjd)",
             "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.16, W27RECON)",
             "l'en-tête (v1.16)")
M = remplace(M, "%  v1.15 : la chaîne D261–D267 (compteur NV, ancrage de transparence)",
             "%  v1.16 : l'ancrage de transparence à son statut DÉRIVÉ du journal\n"
             "%  (le déploiement appliqué depuis la vague 20 — témoin RFC 3161\n"
             "%  vérifié, entrées v0.27.0 → v0.31.0 ; la divergence du présent\n"
             "%  paragraphe avec la spec §7.11 soldée, W27RECON)\n"
             "%  v1.15 : la chaîne D261–D267 (compteur NV, ancrage de transparence)",
             "la ligne de version (v1.16)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.15)}",
             r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.16)}",
             "le running header (v1.16)")
M = remplace(M, "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.15)},",
             "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.16)},",
             "le pdftitle (v1.16)")

# ---- l'avant-propos : l'édition courante ------------------------------------
S1 = remplace(S1, "spécification (v1.15 : l'édition courante est la v0.15.16) : il ne crée aucune règle,",
              "spécification (v1.16 : l'édition courante est la v0.15.17) : il ne crée aucune règle,",
              "l'avant-propos (édition courante v0.15.17)")

# ---- LE PARAGRAPHE D267 : le statut dérivé du journal ------------------------
S5 = remplace(
    S5,
    "\\paragraph{L'ancrage de transparence, à son statut appliqué (D267, v1.15).} Un témoin\n"
    "d'époque (édition, empreinte de l'artefact, empreinte de l'état, date) peut être ancré hors\n"
    "de la machine : une entrée de journal de transparence (Rekor) ou un horodatage qualifié\n"
    "(RFC 3161). La règle est adoptée et outillée, le déploiement n'est pas fait : aucun témoin\n"
    "ancré n'existe à cette révision, et la porte de release le dit EN ATTENTE. Les refus sont\n"
    "nommés (\\code{ANCRE-INDISPONIBLE}, \\code{TEMOIN-SANS-ANCHE}, \\code{ANCRE-INCOHERENTE}).",
    "\\paragraph{L'ancrage de transparence, à son statut dérivé (D267, v1.16).} Un témoin\n"
    "d'époque (édition, empreinte de l'artefact, empreinte de l'état, date) peut être ancré hors\n"
    "de la machine : une entrée de journal de transparence (Rekor) ou un horodatage qualifié\n"
    "(RFC 3161). La règle est adoptée depuis la vague 20, et le déploiement est APPLIQUÉ : le\n"
    "témoin d'époque de chaque édition est ancré à l'autorité RFC 3161, le jeton vérifié hors\n"
    "ligne, chaque ancrage consigné au journal append-only — de v0.27.0 à v0.31.0, les entrées\n"
    "vérifiées recouvrent les pièces. Le statut ne se tape pas : il se DÉRIVE du journal (une\n"
    "entrée vérifiée recouvrant les pièces de l'édition courante : DÉPLOYÉ ; sinon EN ATTENTE),\n"
    "et la porte de release le recompose à chaque passe. Les refus sont\n"
    "nommés (\\code{ANCRE-INDISPONIBLE}, \\code{TEMOIN-SANS-ANCHE}, \\code{ANCRE-INCOHERENTE}).",
    "le paragraphe D267 au statut dérivé (W27RECON)")

# ---- la couverture -----------------------------------------------------------
COUV = remplace(COUV, '<div class="label">Document compl&eacute;mentaire &middot; Version 1.15</div>',
                '<div class="label">Document compl&eacute;mentaire &middot; Version 1.16</div>',
                "la couverture (Version 1.16)")
COUV = remplace(COUV, "(l'&eacute;dition courante v0.15.16)&nbsp;:",
                "(l'&eacute;dition courante v0.15.17)&nbsp;:",
                "la couverture (édition courante)")
COUV = remplace(COUV, "R&eacute;vision v1.15 (h66o54pjd)&nbsp;: la chaîne D261&ndash;D267 (le compteur NV, l'ancrage de transparence) ;",
                "R&eacute;vision v1.16 (W27RECON)&nbsp;: l'ancrage de transparence à son statut d&eacute;riv&eacute; du journal (le d&eacute;ploiement appliqu&eacute; depuis la vague 20) ;",
                "la couverture (révision v1.16)")
COUV = remplace(COUV, "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.15</span>",
                "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.16</span>",
                "la couverture (pied v1.16)")

# ---- la fusion : les métadonnées ---------------------------------------------
FUSION = remplace(FUSION, '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.15)",',
                  '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.16)",',
                  "les métadonnées de fusion (v1.16)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
(ICI / "sec-1.tex").write_text(S1, encoding="utf-8")
(ICI / "sec-5.tex").write_text(S5, encoding="utf-8")
(ICI / "cover.html").write_text(COUV, encoding="utf-8")
(ICI / "merge_cover.py").write_text(FUSION, encoding="utf-8")
print(f"[v1.16] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print(f"  - {f}")
