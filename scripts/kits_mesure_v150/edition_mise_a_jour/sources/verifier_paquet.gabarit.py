#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_paquet.py — LE VÉRIFICATEUR D'INTÉGRITÉ DE L'EXTRACTION (l'édition
MISE À JOUR du paquet multimachines, __EDITION__).

Le manifeste gravé ci-dessous fut calculé au LABORATOIRE sur le montage
même du paquet (chaque pièce telle qu'elle vit dans le zip livré — les .bat
en CRLF, leur forme canonique). Le vérificateur recoupe chaque pièce de
VOTRE extraction : l'extraction incomplète, l'exe retiré par l'antivirus
(l'événement du 12/11 : test_appel.exe refusé par le coffre Drive même,
HTTP 403 « malware or spam » — un faux positif des exe de mesure de
timing), la pièce bougée — TOUT écart est NOMMÉ, jamais maquillé (D189).

L'HONNÊTETÉ DU MANIFESTE : il couvre les 45 pièces du paquet, TOUTES
sauf le vérificateur lui-même — un fichier ne peut pas sceller sa propre
empreinte sans cercle ; l'empreinte du vérificateur et celle du présent
fichier EMPREINTES-PAQUET.txt sont rendues par le sha256 du zip ENTIER,
consigné à l'Entrée 249 du journal de travail et au coffre /test.

Le rapport naît dans verification-paquet.txt. Code de sortie : 0 si
TOUT est vert, 1 s'il y a des écarts (chaque écart est un résultat),
2 si le vérificateur lui-même fautait.
"""

import hashlib
import pathlib
import sys

SORTIE = "verification-paquet.txt"

# LE MANIFESTE GRAVÉ (calculé au laboratoire, 45 pièces — tout sauf ce
# fichier même : voyez l'HONNÊTETÉ ci-dessus).
MANIFESTE = __MANIFESTE__

LIGNES = []


def dit(texte=""):
    print(texte)
    LIGNES.append(texte)


def main():
    ici = pathlib.Path(__file__).resolve().parent
    dit("=" * 66)
    dit(" LE VÉRIFICATEUR DU PAQUET — l'intégrité de VOTRE extraction")
    dit(" %d pièces recoupées contre le manifeste du laboratoire."
        % len(MANIFESTE))
    dit(" Un écart nommé est un RÉSULTAT (D189), jamais un échec à"
        " maquiller.")
    dit("=" * 66)
    vertes = 0
    ecarts = 0
    for chemin in sorted(MANIFESTE):
        attendu = MANIFESTE[chemin]
        piece = ici / chemin
        if not piece.is_file():
            dit("[ÉCART : ABSENTE]      %s  (extraction incomplète ?"
                " l'antivirus ?)" % chemin)
            ecarts += 1
            continue
        lu = hashlib.sha256(piece.read_bytes()).hexdigest()
        if lu != attendu:
            dit("[ÉCART : DIVERGENTE]   %s" % chemin)
            dit("    attendu : %s" % attendu)
            dit("    lu      : %s" % lu)
            ecarts += 1
        else:
            dit("[VERT] %s" % chemin)
            vertes += 1
    dit()
    dit("=" * 66)
    if ecarts == 0:
        dit(" LE BILAN : %d/%d pièces VERTES — l'extraction est la pièce"
            % (vertes, len(MANIFESTE)))
        dit(" du laboratoire. Vivez les kits (COMMENCER-ICI.bat), la"
            " feuille de route est CE-QUI-RESTE-A-FAIRE.txt.")
    else:
        dit(" LE BILAN : %d/%d pièces vertes, %d ÉCART(S) NOMMÉ(S) —"
            % (vertes, len(MANIFESTE), ecarts))
        dit(" renvoyez verification-paquet.txt TEL QUEL (D122) : le labo")
        dit(" recoupe sur pièces. Si un EXE manque : c'est l'ANTIVIRUS"
            " (un faux positif des exe de mesure), pas le paquet —")
        dit(" voyez CE-QUI-RESTE-A-FAIRE.txt, section LES DEUX TESTS NEUFS.")
    dit("=" * 66)
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(LIGNES) + "\n")
    print()
    print("[rapport] écrit : %s" % SORTIE)
    return 0 if ecarts == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:                          # noqa: BLE001 — nommé
        print("[ERREUR NOMMÉE] le vérificateur a fauté : %r" % e)
        sys.exit(2)
