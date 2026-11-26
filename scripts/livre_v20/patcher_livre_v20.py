#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""patcher_livre_v20.py — le Livre du Coffre v1.17 (né de v1.16 par copie) :
LA VAGUE 28 (W28IMRAD). L'en-tête, le running header, le pdftitle, la ligne
de version, la couverture et les métadonnées portés à v1.17 (l'édition
courante v0.15.18) ; le §1 porte la note de la vague 28 (la restructuration
IMRAD, les résultats vécus). Chaque remplacement EST ANCRÉ."""
import pathlib
import shutil

ICI = pathlib.Path(__file__).resolve().parent
SRC = ICI.parent / "livre_v19"
for f in [SRC / "main.tex", *SRC.glob("sec-*.tex"), SRC / "cover.html",
          SRC / "merge_cover.py", SRC / "chaine_cf.html", SRC / "chaine_cf.png"]:
    if f.exists():
        shutil.copy2(f, ICI / f.name)

M = (ICI / "main.tex").read_text(encoding="utf-8")
S1 = (ICI / "sec-1.tex").read_text(encoding="utf-8")
COUV = (ICI / "cover.html").read_text(encoding="utf-8")
FUSION = (ICI / "merge_cover.py").read_text(encoding="utf-8")
FAITS = []


def remplace(txt, ancien, nouveau, nom):
    if ancien not in txt:
        raise SystemExit(f"[v1.17] ANCRE INTROUVABLE — {nom}")
    if txt.count(ancien) != 1:
        raise SystemExit(f"[v1.17] ANCRE NON UNIQUE ({txt.count(ancien)}×) — {nom}")
    FAITS.append(nom)
    return txt.replace(ancien, nouveau)


# ---- l'en-tête (v1.17) ------------------------------------------------------
M = remplace(M, "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.16, W27RECON)",
             "%  LE LIVRE DU COFFRE — TRIADE CF1 -> CF2 -> CF3 (v1.17, W28IMRAD)",
             "l'en-tête (v1.17)")
M = remplace(M, "%  v1.16 : l'ancrage de transparence à son statut DÉRIVÉ du journal",
             "%  v1.17 : la vague 28 portée (le cœur IMRAD, le harnais à carte dérivée,\n"
             "%  le moteur généralisé, OPT-16, les classes C30/C31, le budget OPT-20)",
             "la ligne de version (v1.17)")
M = remplace(M, r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.16)}",
             r"\fancyhead[L]{\small\itshape Le Livre du Coffre — TRIADE CF1 → CF3 (v1.17)}",
             "le running header (v1.17)")
M = remplace(M, "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.16)},",
             "pdftitle={Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.17)},",
             "le pdftitle (v1.17)")

# ---- le §1 : la note de la vague 28 ------------------------------------------
S1 = remplace(S1, "spécification (v1.16 : l'édition courante est la v0.15.17)",
              "spécification (v1.17 : l'édition courante est la v0.15.18)",
              "le §1 (v1.17, l'édition courante)")

# ---- la couverture -----------------------------------------------------------
COUV = remplace(COUV, '<div class="label">Document compl&eacute;mentaire &middot; Version 1.16</div>',
                '<div class="label">Document compl&eacute;mentaire &middot; Version 1.17</div>',
                "la couverture (Version 1.17)")
COUV = remplace(COUV, "(l'&eacute;dition courante v0.15.17)&nbsp;:",
                "(l'&eacute;dition courante v0.15.18)&nbsp;:",
                "la couverture (édition courante)")
COUV = remplace(COUV, "R&eacute;vision v1.16 (W27RECON)&nbsp;: l'ancrage de transparence à son statut d&eacute;riv&eacute; du journal (le d&eacute;ploiement appliqu&eacute; depuis la vague 20) ; le s&eacute;questre 5/3 la garde active, la phrase hors d&eacute;p&ocirc;t (D223)",
                "R&eacute;vision v1.17 (W28IMRAD)&nbsp;: la vague 28 (le c&oelig;ur IMRAD du manuscrit, le harnais &agrave; carte d&eacute;riv&eacute;e 229/235, le moteur g&eacute;n&eacute;ralis&eacute; &agrave; 4,56 × C, OPT-16 &agrave; 79,5 tokens, les classes C30/C31) ; le s&eacute;questre 5/3 la garde active, la phrase hors d&eacute;p&ocirc;t (D223)",
                "la couverture (révision v1.17)")
COUV = remplace(COUV, "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.16</span>",
                "<span>S&eacute;rie TRIADE &middot; r&eacute;vision v1.17</span>",
                "la couverture (pied v1.17)")

# ---- la fusion : les métadonnées ---------------------------------------------
FUSION = remplace(FUSION, '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.16)",',
                  '"/Title": "Le Livre du Coffre — TRIADE CF1 → CF2 → CF3 (v1.17)",',
                  "les métadonnées de fusion (v1.17)")

(ICI / "main.tex").write_text(M, encoding="utf-8")
(ICI / "sec-1.tex").write_text(S1, encoding="utf-8")
(ICI / "cover.html").write_text(COUV, encoding="utf-8")
(ICI / "merge_cover.py").write_text(FUSION, encoding="utf-8")
print(f"[v1.17] {len(FAITS)} remplacements ancrés :")
for f in FAITS:
    print(f"  - {f}")
