#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_juge_u02.py — LE JUGE DE L'ORACLE ÉQUIVALENT u02 (3lmyfb2xa) : le
modèle indépendant Python. DEUX rôles :
  --prepare : PRÉ-GÉNÈRE les décalages (le MÊME Random(GRAINE 20261114)
              consommé dans le MÊME ordre de fichiers que l'oracle du bras
              T — la fonction decales_valides portée À L'IDENTIQUE) et les
              écrit à cgp-decales-u02.txt ;
  --juge    : confronte la sortie du harnais : chaque OUVRIR (la fenêtre
              née à l'ouverture) et CHAQUE décalage (rax, remplissage, le
              tampon == la découpe, la vue et le curseur INTACTS) — le
              volume EXIGÉ : 2032 décalages (2 + 24 + 1003 + 1003, le
              volume du bras T), fail-closed sinon ; la liste observée
              confrontée à la liste attendue (nom, déc) PAR PAIRE.

Le juge ne regarde JAMAIS les octets de la pièce."""
from __future__ import annotations

import hashlib
import pathlib
import random
import sys

ICI = pathlib.Path.cwd()          # le corpus (les témoins + proxy.exe)
GRAINE = 20261114
TAILLE_TAMPON = 384
FICHIERS = ("temoin-1.bin", "temoin-384.bin", "temoin-3f.bin",
            "proxy.exe")
VERT, ROUGE = 0, 0


def decales_valides(taille: int, rng: random.Random) -> list[int]:
    """Portée À L'IDENTIQUE de oracle_unite02_v180.decales_valides (la
    même graine, la même consommation du rng, le même ordre)."""
    out = []
    if taille > 0:
        out.append(0)
        dernier = (taille - 1) // 16 * 16
        out.append(dernier)
        pleine = taille - TAILLE_TAMPON
        if pleine >= 0 and pleine % 16 == 0 and pleine not in out:
            out.append(pleine)
        elif pleine >= 0:
            pleine -= pleine % 16
            if pleine >= 0 and pleine not in out:
                out.append(pleine)
        if taille % 16 == 0 and taille - 16 not in out and taille >= 16:
            out.append(taille - 16)
        pool = list(range(0, (taille + 15) // 16 * 16, 16))
        k = min(1000, len(pool))
        out += [d for d in rng.sample(pool, k) if d not in set(out)]
    return out


def listes_attendues() -> dict[str, list[int]]:
    rng = random.Random(GRAINE)
    return {nom: decales_valides((ICI / nom).stat().st_size, rng)
            for nom in FICHIERS}


def modele_fenetre(contenu: bytes, decalage: int):
    taille = len(contenu)
    if decalage % 16 != 0:
        return (-5, None, None)
    if decalage >= taille:
        return (-3, None, None)
    remplissage = min(TAILLE_TAMPON, taille - decalage)
    tampon = contenu[decalage:decalage + remplissage]
    return (0, remplissage, tampon)


def preparer() -> int:
    attendu = listes_attendues()
    total = sum(len(v) for v in attendu.values())
    with open("cgp-decales-u02.txt", "w", encoding="ascii") as f:
        for nom in FICHIERS:
            f.write(nom + " " + ",".join(str(d) for d in attendu[nom])
                    + "\n")
    print("[prepare] les décalages pré-générés (la graine "
          f"{GRAINE}, le même ordre que l'oracle T) : "
          + " ; ".join(f"{nom}={len(attendu[nom])}" for nom in FICHIERS)
          + f" — TOTAL {total}")
    return 0


def juger() -> int:
    global VERT, ROUGE
    attendu = listes_attendues()
    total_attendu = sum(len(v) for v in attendu.values())
    lignes = pathlib.Path(sys.argv[2] if len(sys.argv) > 2
                          else "cgp-sortie-u02.txt"
                          ).read_text(encoding="utf-8").splitlines()

    print("=== L'ORACLE ÉQUIVALENT u02 (C+G+) — le différentiel au volume "
          "du bras T, le juge = le modèle indépendant ===")
    integrations, epreuves, epreuves_rouges = 0, 0, 0
    observes: list[tuple[str, int]] = []
    for l in lignes:
        if l.startswith("OUVRIR"):
            m = l.split()
            nom = m[1]
            rax = int(m[2].partition("=")[2])
            rempl = int(m[3].partition("=")[2])
            donnees = (ICI / nom).read_bytes()
            ok = (rax == 0
                  and rempl == min(TAILLE_TAMPON, len(donnees)))
            print(f"[{'VERT' if ok else 'ROUGE'}] "
                  f"V1:{nom}-la-fenetre-nee-a-l-ouverture")
            VERT += ok
            ROUGE += not ok
            integrations += 1
        elif l.startswith("EPREUVE"):
            champs = {}
            for m in l.split()[2:]:
                c, _, v = m.partition("=")
                champs[c] = v
            nom = l.split()[1]
            dec = int(champs["dec"])
            observes.append((nom, dec))
            donnees = (ICI / nom).read_bytes()
            v_att, rempl_att, tamp_att = modele_fenetre(donnees, dec)
            ok = (int(champs["rax"]) == v_att
                  and int(champs["rempl"]) == rempl_att
                  and bytes.fromhex(champs["tampon"])[:rempl_att]
                  == tamp_att
                  and int(champs["vue"]) == 0
                  and int(champs["curseur"]) == 0)
            epreuves += 1
            if not ok:
                print(f"[ROUGE] {nom} dec={dec} : rax={champs['rax']} "
                      f"(attendu {v_att}), rempl={champs['rempl']} "
                      f"(attendu {rempl_att}), le tampon != la découpe "
                      "ou la vue/curseur déplacés")
                epreuves_rouges += 1
    ROUGE += epreuves_rouges
    VERT += epreuves - epreuves_rouges
    # la liste observée == la liste attendue (les paires, l'ordre compris)
    attendues_paires = [(nom, d) for nom in FICHIERS for d in attendu[nom]]
    liste_ok = observes == attendues_paires

    print(f"\n=== L'ORACLE ÉQUIVALENT u02 : {epreuves} épreuves-"
          f"décalages ({integrations} intégrations), "
          f"{ROUGE} ROUGE — "
          f"{'VERT' if ROUGE == 0 else 'ROUGE'} ===")
    if epreuves != total_attendu or not liste_ok or ROUGE or \
            integrations != 4:
        print(f"[juge-u02] REFUS VOLUME : {epreuves} décalages observés "
              f"(attendu {total_attendu} = le volume du bras T), "
              f"la liste {'conforme' if liste_ok else 'NON CONFORME'}, "
              f"{ROUGE} ROUGE", file=sys.stderr)
        return 2
    return 0


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--prepare":
        return preparer()
    if len(sys.argv) > 1 and sys.argv[1] == "--juge":
        return juger()
    print("usage: cgp_juge_u02.py --prepare | --juge [sortie]",
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
