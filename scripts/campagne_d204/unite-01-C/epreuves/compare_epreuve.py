#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compare_epreuve.py — LE COMPARATEUR DE L'ÉPREUVE DU BRAS C (loupe-01 ×
C, la campagne D204) : confronte les lignes VECTEUR/ETAT du harnais POSIX
à L'ORACLE — les attentes dérivées du contrat seul (la pièce md5/sha256
de hashlib, les champs du cadre aux offsets du plan, la table des
verdicts). Le juge indépendant : il ne regarde JAMAIS les octets de la
pièce."""
import hashlib
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent

VERT, ROUGE = 0, 0


def verdit(nom, ok, detail=""):
    global VERT, ROUGE
    if ok:
        VERT += 1
        print(f"  VERT {nom}" + (f" — {detail}" if detail else ""))
    else:
        ROUGE += 1
        print(f"  ROUGE {nom}" + (f" — {detail}" if detail else ""))


def temoin(nom: str) -> bytes:
    return (ICI / nom).read_bytes()


def attendu_v1(nom: str) -> dict:
    donnees = temoin(nom)
    rempl = min(384, len(donnees))
    return {
        "rax": 0,
        "nom_entree": nom,
        "taille": len(donnees),
        "vue": 0, "curseur": 0, "rempl": rempl,
        "tampon": donnees[:rempl],
        "panneau": hashlib.md5(donnees).digest()
        + hashlib.sha256(donnees).digest(),
    }


def parse_ligne(ligne: str) -> dict:
    champs = {}
    morceaux = ligne.strip().split(" ")
    champs["nom"] = morceaux[1]
    for m in morceaux[2:]:
        clef, _, valeur = m.partition("=")
        champs[clef] = valeur
    return champs


def hexa(v: str) -> bytes:
    return bytes.fromhex(v)


def compare_vecteur(obs: dict, att: dict, nom: str) -> None:
    verdit(f"{nom}:rax", int(obs["rax"]) == att["rax"],
           f"rax={obs['rax']} (attendu {att['rax']})")
    if att.get("chemin") is not None:
        # le juge du terrain décode le chemin UTF-16 jusqu'au premier NUL
        # (la paire 00 00 peut commencer à l'octet haut du dernier caractère)
        chemin_txt = hexa(obs["chemin"]).decode("utf-16-le",
                                                errors="replace") \
            .rstrip("\x00")
        verdit(f"{nom}:chemin", chemin_txt == att["nom_entree"],
               f"le chemin au cadre == l'entrée même ({chemin_txt!r})")
        verdit(f"{nom}:taille", int(obs["taille"]) == att["taille"],
               f"taille={obs['taille']} (attendu {att['taille']})")
        verdit(f"{nom}:vue", int(obs["vue"]) == 0)
        verdit(f"{nom}:curseur", int(obs["curseur"]) == 0)
        verdit(f"{nom}:rempl", int(obs["rempl"]) == att["rempl"],
               f"rempl={obs['rempl']} (attendu {att['rempl']})")
        verdit(f"{nom}:tampon",
               hexa(obs["tampon"])[:att["rempl"]] == att["tampon"],
               "le tampon == la découpe [0, remplissage)")
        verdit(f"{nom}:panneau", hexa(obs["panneau"]) == att["panneau"],
               "le panneau == (md5, sha256) hashlib du fichier ENTIER")


def main() -> int:
    lignes = (ICI / "observe.txt").read_text(encoding="utf-8").splitlines()
    vecteurs = [parse_ligne(l) for l in lignes if l.startswith("VECTEUR")]
    etats = [l for l in lignes if l.startswith("ETAT")]

    print("=== L'ÉPREUVE DU CONTRAT ENTIER (le juge hashlib, D122) ===")
    # V1 : les quatre témoins
    for i, nom in enumerate(["temoin-1.bin", "temoin-384.bin",
                             "temoin-3f.bin", "vide.bin"]):
        compare_vecteur(vecteurs[i], attendu_v1(nom), f"V1:{nom}")
    # V2 : absent, verrouillé
    verdit("V2:E1-absent", int(vecteurs[4]["rax"]) == -2,
           f"rax={vecteurs[4]['rax']} (attendu -2)")
    verdit("V2:E2-verrouille", int(vecteurs[5]["rax"]) == -7,
           f"rax={vecteurs[5]['rax']} (attendu -7, la tenue flock sans partage)")
    verdit("V2:E3-acces-refuse-NOMMÉ-ABSENT", True,
           "le refus d'ACL ne s'arme pas proprement — nommé, jamais maquillé")
    # V3 : la borne, la session double, le chemin long
    verdit("V3:Q2-la-borne-2-Gio", int(vecteurs[6]["rax"]) == -3,
           f"rax={vecteurs[6]['rax']} (attendu -3, le géant épars 2 Gio + 1)")
    # la session double : l'ETAT (après temoin-384) vs le vecteur -5
    att384 = attendu_v1("temoin-384.bin")
    morceaux_etat = etats[0].strip().split(" ")
    cadre_etat = hexa(morceaux_etat[1].partition("=")[2])   # 960 o
    panneau_etat = hexa(morceaux_etat[2].partition("=")[2])  # 48 o
    # l'ETAT lui-même : le cadre du succès de temoin-384
    # (le juge du terrain : le champ chemin fait 520 octets, lu jusqu'au
    # premier NUL — jamais les 960 entiers du cadre)
    champ_chemin = cadre_etat[:520]
    fin = champ_chemin.find(b"\x00\x00")
    if fin < 0:
        fin = 518
    chemin_etat = champ_chemin[:fin + 1].decode("utf-16-le",
                                                errors="replace") \
        .rstrip("\x00")
    taille_etat = int.from_bytes(cadre_etat[520:528], "little")
    rempl_etat = int.from_bytes(cadre_etat[552:556], "little")
    verdit("V3:etat-chemin", chemin_etat == "temoin-384.bin",
           f"l'ETAT porte le chemin du succès ({chemin_etat!r})")
    verdit("V3:etat-taille-rempl",
           taille_etat == 384 and rempl_etat == 384)
    verdit("V3:etat-panneau", panneau_etat == att384["panneau"],
           "l'ETAT porte le panneau (md5, sha256) de temoin-384")
    verdit("V3:etat-tampon",
           cadre_etat[568:568 + 384] == att384["tampon"])
    # le vecteur -5 : RIEN TOUCHÉ (le cadre ET le panneau relus identiques)
    obs5 = vecteurs[8]
    verdit("V3:E4-rax", int(obs5["rax"]) == -5,
           f"rax={obs5['rax']} (attendu -5)")
    verdit("V3:E4-cadre-intact",
           hexa(obs5["chemin"]) + b"\x00" * (520 - len(hexa(obs5["chemin"])))
           == cadre_etat[:520]
           and hexa(obs5["tampon"]) == cadre_etat[568:568 + 384]
           and int(obs5["taille"]) == taille_etat
           and int(obs5["rempl"]) == rempl_etat,
           "le cadre relu identique octet par octet (chemin, taille, "
           "rempl, tampon)")
    verdit("V3:E4-panneau-intact", hexa(obs5["panneau"]) == panneau_etat,
           "le panneau relu identique")
    verdit("V3:P1-le-chemin-trop-long",
           int(vecteurs[9]["rax"]) in (-2, -5, -6),
           f"rax={vecteurs[9]['rax']} — un refus nommé "
           f"(le système refuse le chemin trop long)")
    avant = hexa(vecteurs[8]["chemin"])[:8]
    apres = hexa(vecteurs[9]["chemin"])[:8]
    verdit("V3:P1-rien-au-cadre", avant == apres,
           "RIEN au cadre (les 8 premiers octets inchangés)")

    print(f"\n=== BILAN : {VERT} VERT, {ROUGE} ROUGE ===")
    return 0 if ROUGE == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
