#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""construire_batterie_5ey7gmjra.py — construit les modules de contrôles
étendus, la chaîne plafond/fidélité étendue et les configs de run (le motif
89488hblm, la garde de la règle 4 portant l'extension)."""
import pathlib

AT = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path("/home/z/my-project/depot/atelier-cf3-89488hblm")
V150 = pathlib.Path("/home/z/my-project/depot/scripts/tla_v150")

REGLES = ["VoleKUser", "VoleSSerrure", "VoleSPiege", "FalsifieConteneur",
          "FalsifiePiege", "RejoueEpoquePassee", "OuvrirCorrect",
          "OuvrirPhraseErronee", "OuvrirAncienCouple", "Verifier",
          "CrashPendantSession", "CloturerCorrecte", "CloturerPhraseErronee"]


def transformer(src_nom, dst_nom, substitutions, src_dir=SRC):
    texte = (pathlib.Path(src_dir) / src_nom).read_text(encoding="utf-8")
    for ancien, nouveau, cause in substitutions:
        if ancien not in texte:
            raise SystemExit(f"[ROUGE] substitution introuvable ({cause}) "
                             f"dans {src_nom}")
        texte = texte.replace(ancien, nouveau, 1)
    (AT / dst_nom).write_text(texte, encoding="utf-8")
    print(f"[VERT] {dst_nom} gravé ({len(substitutions)} substitutions)")


# (1) les contrôles Python étendus — L'INVERSION : la mutation de 89488hblm
#     (trap_ok seul) fut adoptée par 5ey7gmjra comme la VÉRITÉ ; l'ancienne
#     vérité (canonique seul) devient LA MUTATION de la présente.
transformer("CF3PythonControles.tla", "CF3PythonControlesEtendu.tla", [
    ("------------------------ MODULE CF3PythonControles -----------------------",
     "--------------------- MODULE CF3PythonControlesEtendu --------------------",
     "le nom du module"),
    (" * CF3PythonControles — LES 26 MUTATIONS DU POINT (a) : les fautes de",
     " * CF3PythonControlesEtendu — LES 26 MUTATIONS SUR LE MODÈLE ÉTENDU : les\n * fautes de",
     "l'en-tête"),
    ("EXTENDS CF3Python\n", "EXTENDS CF3PythonEtendu\n", "la base étendue"),
    ("\\* 4 : la falsification du conteneur SANS l'exigence canonique — LA\n\\*     simplification fausse que la campagne PBT a croisée (l'écart de\n\\*     couverture v0.15.0 : la sentinelle court sur le canonique)\nGPw_FalsifieConteneur == trap_ok",
     "\\* 4 : L'EXTENSION ANNULÉE — la garde v0.15.0 restaurée (canonique\n\\*     seul) : la mutation de 89488hblm (trap_ok) fut ADOPTÉE par\n\\*     5ey7gmjra comme la VÉRITÉ (la sentinelle concrète) ; l'ancienne\n\\*     vérité devient LA MUTATION — à phase = \"brouillon\" le mutant\n\\*     refuse ce que la règle étendue tire : l'écart des 660 traces\n\\*     renaîtrait\nGPw_FalsifieConteneur == trap_ok /\\ phase = \"canonique\"",
     "L'INVERSION (le contrôle de l'extension)"),
])

# (2) les contrôles d'équivalence étendus
transformer("CF3EquivControles.tla", "CF3EquivControlesEtendu.tla", [
    ("------------------------ MODULE CF3EquivControles -----------------------",
     "--------------------- MODULE CF3EquivControlesEtendu --------------------",
     "le nom du module"),
    (" * CF3EquivControles — LES 26 CONTRÔLES NÉGATIFS DU POINT (a), UN PAR",
     " * CF3EquivControlesEtendu — LES 26 CONTRÔLES NÉGATIFS SUR LE MODÈLE\n * ÉTENDU, UN PAR",
     "l'en-tête"),
    ("EXTENDS CF3Equiv, CF3PythonControles\n",
     "EXTENDS CF3EquivEtendu, CF3PythonControlesEtendu\n",
     "les bases étendues"),
    ("CFPw == INSTANCE CF3PythonControles WITH",
     "CFPw == INSTANCE CF3PythonControlesEtendu WITH",
     "l'instance mutée étendue"),
    (" * Le contrôle de l'épinglage TLC : la garde mutée de la falsification\n * du conteneur (LA simplification fausse croisée par la campagne PBT)\n * — le TLC DOIT tomber (le tir réel impossible où la garde mutée\n * prétend : deadlock rapporté).",
     " * Le contrôle de l'épinglage TLC : la garde mutée de la falsification\n * du conteneur (L'EXTENSION ANNULÉE — la garde v0.15.0 canonique-seule\n * restaurée comme mutation, PLUS RESTRICTIVE que la règle étendue)\n * — le TLC DOIT tomber : à phase = \"brouillon\" la règle RÉELLE étendue\n * tire (marque posée) tandis que la garde mutée REFUSE — l'INVARIANT\n * InvPinCtl tombe (la violation rapportée — le sens inverse du contrôle\n * 89488hblm, la même discipline).",
     "le commentaire du contrôle d'épinglage"),
])

# (3) la chaîne plafond/fidélité étendue (les comptes étendus consignés)
transformer("CF3Plafond.tla", "CF3PlafondEtendu.tla", [
    ("------------------------- MODULE CF3Plafond -------------------------",
     "----------------------- MODULE CF3PlafondEtendu ----------------------",
     "le nom du module"),
    ("EXTENDS CF3, Naturals\n", "EXTENDS CF3Etendu, Naturals\n",
     "la base étendue"),
], src_dir=V150)
transformer("CF3Fidelite.tla", "CF3FideliteEtendu.tla", [
    ("------------------------ MODULE CF3Fidelite ------------------------",
     "---------------------- MODULE CF3FideliteEtendu ---------------------",
     "le nom du module"),
    ("EXTENDS CF3Plafond, Naturals\n", "EXTENDS CF3PlafondEtendu, Naturals\n",
     "la base étendue"),
], src_dir=V150)

# (4) la config de fidélité étendue (les noms d'opérateurs inchangés)
(AT / "CF3FideliteEtendu.cfg").write_text(
    (V150 / "CF3Fidelite.cfg").read_text(encoding="utf-8"),
    encoding="utf-8")
print("[VERT] CF3FideliteEtendu.cfg gravé (le motif scellé)")

# (5) toutes les configs de run (le motif 89488hblm, préfixe ME- pour
#     l'étendu : MEE/MET/MCC/MTLP)
CTE = ('CONSTANTS\nKUser = "K_user"\nSSerrure = "S_serrure"\n'
       'SPiege = "S_piege"\n')


def cfg(nom, init, nxt, inv):
    (AT / nom).write_text(
        f"{CTE}INIT\n{init}\nNEXT\n{nxt}\nINVARIANT\n{inv}\n",
        encoding="utf-8")


cfg("MEE_base.cfg", "Init", "Next", "Inv")
cfg("MEE_ind.cfg", "Inv", "Next", "Inv")
for r in REGLES:
    cfg(f"MEEg_{r}.cfg", "InitCopies", "RecopieTout", f"OblGarde_{r}")
    cfg(f"MEEi_{r}.cfg", "InitCopies", f"NextImage_{r}", "InvImage")
    cfg(f"MEEa_{r}.cfg", "InitCopies", f"NextAct_{r}", f"InvAct_{r}")
    cfg(f"MCCg_{r}.cfg", "InitCopies", "RecopieTout", f"OblFaibleGarde_{r}")
    cfg(f"MCCi_{r}.cfg", "InitCopies", f"NextImageCtl_{r}", "InvImage")
    cfg(f"MTLP_{r}.cfg", "InitPin", f"NextPin_{r}", f"InvPin_{r}")
cfg("MET_lt1.cfg", "InitLT", "NextLTScelle", "LT1")
cfg("MET_lt2.cfg", "InitLT", "NextLTScelle", "Couplage")
cfg("MET_cc1.cfg", "InitLTfaible", "NextLTScelle", "LT1")
cfg("MET_cc2.cfg", "InitLT", "NextLTplafond", "Couplage")
cfg("MTLP_ctl.cfg", "InitPin", "NextPinCtl_FalsifieConteneur",
    "InvPinCtl_FalsifieConteneur")
print(f"[VERT] {13 * 6 + 8} configs de run gravées "
      "(MEE_*/MET_*/MCC_*/MTLP_*)")
