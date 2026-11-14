#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_unite01C.py — L'OUTIL AUTEUR du bras C (l'unité 1, loupe-01 × C,
la campagne D204) : applique les PATCHS du modèle à la pièce source, dans
l'ordre de leur livraison (l'arithmétique d'assemblage est à l'outil, la
LOGIQUE est à l'auteur — le même partage que la notation à étiquettes du
bras T). Chaque remplacement vérifié AU CARACTÈRE : une ligne AVANT
introuvable, le montage REFUSE (fail-closed)."""
import pathlib
import sys

UNITE = pathlib.Path(__file__).resolve().parent
SOURCE = UNITE / "source"


def _remplace_flexible(texte: str, avant: str, apres: str) -> str:
    """Le remplacement : exact d'abord, puis au contenu (l'indentation du
    fichier conservée — les étiquettes de l'auteur résolues par l'outil)."""
    if avant in texte:
        return texte.replace(avant, apres, 1)
    lignes = texte.splitlines(keepends=True)
    cible = avant.strip()
    trouves = [k for k, l in enumerate(lignes) if l.strip() == cible]
    if len(trouves) != 1:
        raise SystemExit(f"[REFUS] le montage refuse : l'AVANT "
                         f"({len(trouves)} correspondance(s) au contenu) :\n{avant}")
    k = trouves[0]
    indent = lignes[k][:len(lignes[k]) - len(lignes[k].lstrip())]
    nouvelles = []
    for l in apres.splitlines():
        if l.strip():
            nouvelles.append(indent + l.strip() + "\n")
        else:
            nouvelles.append("\n")
    lignes[k:k + 1] = nouvelles
    return "".join(lignes)


def applique_patch(texte: str, reponse: str) -> str:
    """Applique les sections ###REMPLACEMENTS et ###SUITE d'une réponse."""
    lignes = reponse.splitlines()
    # --- les remplacements (UNE ou PLUSIEURS sections) ---
    paires = []
    k = 0
    while k < len(lignes):
        if lignes[k].strip() == "###REMPLACEMENTS":
            k += 1
            while k < len(lignes) and lignes[k].strip() != "###FIN REMPLACEMENTS":
                if lignes[k].startswith("AVANT="):
                    avant = [lignes[k][len("AVANT="):]]
                    k += 1
                    while k < len(lignes) and not lignes[k].startswith(
                            ("AVANT=", "APRÈS=")) \
                            and lignes[k].strip() != "###FIN REMPLACEMENTS":
                        avant.append(lignes[k])
                        k += 1
                    if k < len(lignes) and lignes[k].startswith("APRÈS="):
                        apres = lignes[k][len("APRÈS="):]
                        k += 1
                        while k < len(lignes) and not lignes[k].startswith(
                                ("AVANT=", "APRÈS=")) \
                                and lignes[k].strip() not in (
                                "###FIN REMPLACEMENTS",):
                            apres += "\n" + lignes[k]
                            k += 1
                    else:
                        apres = None
                    paires.append(("\n".join(avant), apres))
                else:
                    k += 1
        else:
            k += 1
    for avant, apres in paires:
        if apres is None or apres.startswith("(supprimée"):
            # la suppression : la ligne (ou le bloc) disparaît
            lignes_f = texte.splitlines(keepends=True)
            cible = avant.strip().splitlines()
            trouves = [i for i, l in enumerate(lignes_f)
                       if all(lignes_f[i + j].strip() == cible[j].strip()
                              for j in range(len(cible))
                              if i + j < len(lignes_f))]
            if len(trouves) != 1:
                raise SystemExit(f"[REFUS] la suppression : l'AVANT "
                                 f"({len(trouves)} correspondance(s)) :\n{avant}")
            i = trouves[0]
            del lignes_f[i:i + len(cible)]
            texte = "".join(lignes_f)
        else:
            texte = _remplace_flexible(texte, avant, apres)
        print(f"[remplacement] {avant.splitlines()[0].strip()[:72]}…")
    # --- la suite (optionnelle — un correctif peut ne porter que des
    #     remplacements) ---
    if "###SUITE" in [l.strip() for l in lignes]:
        j0 = next(k for k, l in enumerate(lignes)
                  if l.strip() == "###SUITE")
        j1 = next(k for k, l in enumerate(lignes)
                  if l.strip() == "###FIN SUITE")
        suite = "\n".join(lignes[j0 + 1:j1]).strip("\n")
        # la suite s'assemble après la DERNIÈRE ligne livrée du fichier
        # (la coupure : la ligne ReadFile de la boucle)
        ancre = ("        if (!ReadFile(h, morceau, a_lire, &lus, NULL) "
                 "|| lus == 0) break;")
        if ancre not in texte:
            raise SystemExit("[REFUS] l'ancre de la suite (le ReadFile) "
                             "introuvable — le montage refuse")
        texte = texte.replace(ancre, ancre + "\n" + suite, 1)
        print("[suite] assemblée après la ligne coupée (le ReadFile)")
    return texte


def main() -> int:
    if len(sys.argv) != 3:
        print("usage : build_unite01C.py <édition-actuelle> <réponse-patch>")
        return 2
    actuelle = pathlib.Path(sys.argv[1])
    reponse = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    texte = actuelle.read_text(encoding="utf-8")
    texte = applique_patch(texte, reponse)
    actuelle.write_text(texte, encoding="utf-8", newline="")
    print(f"[monté] {actuelle} : {len(texte.encode())} o, "
          f"{len(texte.splitlines())} lignes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
