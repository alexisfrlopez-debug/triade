#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""porte_la_mention_lanceur.py — LES SIX RETOUCHES DE LISEZMOI de l'édition
AUTOMATISÉE : chaque LISEZMOI de kit porte désormais la mention de SON
lanceur (insérée dans la section protocole, l'histoire demeure). Les
insertions sont UNIQUES (refus si déjà présentes) et VÉRIFIÉES par la
présence de l'ancre exacte."""

import pathlib
import sys

BASE = pathlib.Path("/home/z/my-project/triade/scripts/kits_mesure_v150")
BRUT = pathlib.Path("/home/z/my-project/triade/download/multimachines-brut")

RETOUCHES = [
    # (fichier, ancre exacte, insertion AVANT l'ancre)
    (BASE / "kit_shani/LISEZMOI-shani.txt",
     "COMMENT L'EXÉCUTER (votre machine Windows)\n  1. Ouvrez une invite",
     "COMMENT L'EXÉCUTER (votre machine Windows)\n"
     "  L'ÉDITION AUTOMATISÉE : DOUBLE-CLIQUEZ LANCER-KIT-1-SHANI.bat —\n"
     "  il fait les gestes 1 et 2 pour vous (les pièces vérifiées, Python\n"
     "  trouvé, le scénario lancé) et vous dit où sont les preuves. Rien à\n"
     "  compiler : le moteur-shani.bin est livré et asserté. Les étapes\n"
     "  ci-dessous demeurent la référence manuelle.\n"),

    (BASE / "kit_dudect/LISEZMOI-dudect.txt",
     "LE PROTOCOLE (le run, sur la machine Windows du développeur) :\n"
     "  1. Copiez le dossier kit_dudect/",
     "LE PROTOCOLE (le run, sur la machine Windows du développeur) :\n"
     "  L'ÉDITION AUTOMATISÉE : DOUBLE-CLIQUEZ LANCER-KIT-2-DUDECT.bat —\n"
     "  il fait TOUT : la compilation (SI un compilateur vit — cl, gcc,\n"
     "  clang — il recompile depuis LA SOURCE, la vérité ; SINON les exe\n"
     "  précompilés livrés courent), l'épreuve d'appel, LE RUN (N = 200 par\n"
     "  défaut ; passez votre N en argument, minimum 60) et il écrit\n"
     "  temoin-dudect-BROUILLON.txt (machine, CPU, binaire, empreintes —\n"
     "  l'état EFFECTIF du turbo et la signature restent à votre main).\n"
     "  Aucun Python requis. Le protocole ci-dessous demeure la référence.\n"),

    (BASE / "kit_terrain_tiers/LISEZMOI-terrain-tiers.txt",
     "LE PROTOCOLE (le run, sur la machine tierce) :\n"
     "  1. La machine :",
     "LE PROTOCOLE (le run, sur la machine tierce) :\n"
     "  L'ÉDITION AUTOMATISÉE : DOUBLE-CLIQUEZ LANCER-KIT-3-LOUPE.bat —\n"
     "  il recoupe le sha256 de loupe.exe contre le scellé AVANT tout\n"
     "  lancement (le geste 2 ci-dessous), vérifie que Python est 64 bits\n"
     "  et vit le scénario intégral T0→T7 + S0. Le témoin vitrine\n"
     "  (facultatif) demeure un double-clic à part : temoin-vitrine.bat.\n"),

    (BASE / "kit_constat_arm/LISEZMOI-constat-arm.txt",
     "LE PROTOCOLE (le run, sur le téléphone) :\n"
     "  1. Installez Termux",
     "LE PROTOCOLE (le run, sur le téléphone) :\n"
     "  L'ÉDITION AUTOMATISÉE : sur le téléphone, tapez\n"
     "  « bash lancer-kit-constat-arm.sh » — le lanceur INSTALLE PYTHON\n"
     "  TOUT SEUL s'il manque (pkg), puis vit le run et vous dit où sont\n"
     "  les preuves. Les étapes ci-dessous demeurent la référence.\n"),

    (BASE / "qemu_emulation/LISEZMOI-qemu.txt",
     "  LE GESTE : extraire le dossier, puis sous WSL2 (Ubuntu par exemple) :\n"
     "      cd kit-m7d && python3 scenario-m7d.py",
     "  LE GESTE : extraire le dossier, puis sous WSL2 (Ubuntu par exemple) :\n"
     "      cd kit-m7d && python3 scenario-m7d.py\n"
     "  L'ÉDITION AUTOMATISÉE : tapez « bash qemu-wsl2/lancer-voie1-m7d.sh »\n"
     "  — le lanceur trouve python3 (voire l'installe si sudo vit sans mot\n"
     "  de passe) et vit le run : le qemu-riscv64 embarqué ne demande RIEN."),

    (BRUT / "LISEZMOI-KIT-LOUPE.md",
     "2. **Lancer le scénario** : `python scenario-loupe.py` (ou",
     "2. **Lancer le scénario** : `python scenario-loupe.py` (ou\n"
     "   l'édition automatisée du paquet multimachines :\n"
     "   DOUBLE-CLIQUEZ `LANCER-KIT-3-LOUPE.bat` du dossier parent —\n"
     "   il recoupe le scellé, vérifie le Python 64 bits, lance) ; ou"),
]


def main() -> int:
    ok = True
    for chemin, ancre, remplacement in RETOUCHES:
        t = chemin.read_text(encoding="utf-8")
        if remplacement in t:
            print(f"[déjà tenu] {chemin.name}")
            continue
        if ancre not in t:
            print(f"[ANCRE INTROUVABLE] {chemin} — ancre : {ancre[:60]!r}")
            ok = False
            continue
        t = t.replace(ancre, remplacement, 1)
        chemin.write_text(t, encoding="utf-8")
        print(f"[retouché] {chemin}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
