#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cgp_juge_u01.py — LE JUGE DE L'ORACLE ÉQUIVALENT u01 (3lmyfb2xa) : le
modèle indépendant Python qui confronte les DOUZE épreuves du harnais
cgp_oracle_u01.c — les MÊMES épreuves que l'oracle du bras T
(oracle_unite01_v180), les QUATORZE contrôles reconduits :
  V1 : les trois témoins (la session née entière + le panneau né) et le vide ;
  V2 : E1 absent, E2 verrouillé, E3 accès refusé (ARMÉ — l'écart de
       campagne nommé comblé : chmod 000 → -6 SYSTÈME) ;
  V3 : Q2 la borne 2 Gio + 1 (la poignée refermée AVANT le retour,
       comptée), E4 la session double (le cadre ET le panneau relus
       identiques), P1 le chemin trop long ;
  V4 : la falsification demandée (la taille mutée — l'écran attendu
       diverge : le juge lit l'état, jamais le modèle).

L'ÉCART NOMMÉ (P1) : la pièce T répond -5 ; la pièce C au POSIX répond -2
(ENAMETOOLONG → ABSENT — la sémantique du shim, l'état de campagne) — le
juge épingle -2, la divergence consignée au rapport.

Usage : python3 cgp_juge_u01.py [sortie]   (défaut : cgp-sortie-u01.txt)
Sortie : 0 = 12 épreuves / 14 contrôles / 0 ROUGE ; 2 = refus nommé."""
from __future__ import annotations

import hashlib
import pathlib
import sys

ICI = pathlib.Path.cwd()          # le corpus (les témoins + la sortie)
VERT, ROUGE = 0, 0
EPREUVES = 0


def verdit(nom: str, ok: bool, detail: str = "") -> None:
    global VERT, ROUGE
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}"
          + (f" — {detail}" if detail else ""))
    VERT += ok
    ROUGE += not ok


def temoin(nom: str) -> bytes:
    return (ICI / nom).read_bytes()


def hexa(v: str) -> bytes:
    return bytes.fromhex(v)


def parse_ligne(ligne: str) -> dict:
    champs = {}
    morceaux = ligne.strip().split(" ")
    champs["nom"] = morceaux[1]
    for m in morceaux[2:]:
        clef, _, valeur = m.partition("=")
        champs[clef] = valeur
    return champs


def attendu_v1(nom: str) -> dict:
    donnees = temoin(nom)
    rempl = min(384, len(donnees))
    return {"rax": 0, "nom_entree": nom, "taille": len(donnees),
            "rempl": rempl, "tampon": donnees[:rempl],
            "panneau": hashlib.md5(donnees).digest()
            + hashlib.sha256(donnees).digest()}


def compare_v1(obs: dict, att: dict, nom: str) -> None:
    chemin_txt = hexa(obs["chemin"]).decode("utf-16-le",
                                            errors="replace").rstrip("\x00")
    ok_session = (int(obs["rax"]) == 0 and chemin_txt == att["nom_entree"]
                  and int(obs["taille"]) == att["taille"]
                  and int(obs["poignee"]) > 2
                  and int(obs["vue"]) == 0 and int(obs["curseur"]) == 0
                  and int(obs["rempl"]) == att["rempl"]
                  and hexa(obs["tampon"])[:att["rempl"]] == att["tampon"])
    verdit(f"V1:{nom}-la-session-nee-entiere", ok_session,
           f"le cadre champ à champ : chemin {nom}, taille "
           f"{att['taille']}, vue 0, curseur 0, remplissage "
           f"{att['rempl']}, le tampon == la découpe du modèle")
    verdit(f"V1:{nom}-le-panneau-ne",
           hexa(obs["panneau"]) == att["panneau"],
           "le panneau 48 o == (md5, sha256) hashlib du fichier ENTIER")


def main() -> int:
    sortie = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                          else "cgp-sortie-u01.txt")
    lignes = sortie.read_text(encoding="utf-8").splitlines()
    epreuves = [parse_ligne(l) for l in lignes if l.startswith("EPREUVE")]
    etats = [l for l in lignes if l.startswith("ETAT")]
    compteurs = [l for l in lignes if l.startswith("COMPTEUR")]
    falsifs = [l for l in lignes if l.startswith("FALSIF")]
    global EPREUVES
    EPREUVES = len(epreuves) + len(falsifs)

    print("=== L'ORACLE ÉQUIVALENT u01 (C+G+) — le juge = le modèle "
          "indépendant ===")

    # ---- V1 : les quatre témoins ----------------------------------------
    for i, nom in enumerate(["temoin-1.bin", "temoin-384.bin",
                             "temoin-3f.bin"]):
        compare_v1(epreuves[i], attendu_v1(nom), nom)
    vide = attendu_v1("vide.bin")
    obs_vide = epreuves[3]
    verdit("V1:vide.bin-le-fichier-vide",
           int(obs_vide["rax"]) == 0 and int(obs_vide["taille"]) == 0
           and int(obs_vide["rempl"]) == 0
           and hexa(obs_vide["panneau"]) == vide["panneau"],
           "le vide s'ouvre : remplissage 0, le panneau du vide == "
           "(d41d8cd9…, e3b0c442…) — les empreintes du vide")

    # ---- V2 : les rejets d'OS -------------------------------------------
    verdit("V2:E1-absent", int(epreuves[4]["rax"]) == -2,
           f"rax={epreuves[4]['rax']} (attendu -2) — le chemin absent "
           "→ -2 ABSENT")
    verdit("V2:E2-verrouille", int(epreuves[5]["rax"]) == -7,
           f"rax={epreuves[5]['rax']} (attendu -7) — le fichier tenu par "
           "un autre détenteur → -7 VERROUILLÉ")
    verdit("V2:E3-acces-refuse", int(epreuves[6]["rax"]) == -6,
           f"rax={epreuves[6]['rax']} (attendu -6) — l'accès refusé "
           "(chmod 000, ARMÉ — l'écart de campagne comblé) → -6 SYSTÈME")

    # ---- V3 : les bornes -------------------------------------------------
    avant, apres = 0, 0
    for c in compteurs:
        m = {p.split("=")[0]: p.split("=")[1]
             for p in c.split() if "=" in p}
        avant, apres = int(m["avant"]), int(m["apres"])
    obs_geant = epreuves[7]
    verdit("V3:Q2-la-borne-2-Gio",
           int(obs_geant["rax"]) == -3 and apres == avant + 1,
           f"rax={obs_geant['rax']} (attendu -3), la poignée REFERMÉE "
           f"AVANT le retour (comptée : {avant} → {apres}) — jamais une "
           "poignée pendante")
    # la session double : l'ETAT (le succès de temoin-384) vs le vecteur -5
    att384 = attendu_v1("temoin-384.bin")
    morceaux_etat = etats[0].strip().split(" ")
    cadre_etat = hexa(morceaux_etat[1].partition("=")[2])   # 960 o
    panneau_etat = hexa(morceaux_etat[2].partition("=")[2])  # 48 o
    obs_double = epreuves[9]
    verdit("V3:E4-la-session-double",
           int(epreuve_r5 := obs_double["rax"]) == -5
           and hexa(obs_double["chemin"])
           + b"\x00" * (520 - len(hexa(obs_double["chemin"])))
           == cadre_etat[:520]
           and hexa(obs_double["tampon"]) == cadre_etat[568:568 + 384]
           and int(obs_double["taille"])
           == int.from_bytes(cadre_etat[520:528], "little")
           and int(obs_double["rempl"])
           == int.from_bytes(cadre_etat[552:556], "little")
           and hexa(obs_double["panneau"]) == panneau_etat,
           f"rax={epreuve_r5} (attendu -5), le cadre ET le panneau relus "
           "identiques — l'ancien fichier INTACT")
    obs_260 = epreuves[10]
    verdit("V3:P1-le-chemin-trop-long",
           int(obs_260["rax"]) == -2
           and hexa(obs_260["chemin"])[:8]
           == hexa(obs_double["chemin"])[:8],
           f"rax={obs_260['rax']} — 260 caractères sans NUL → -2 au "
           "POSIX (ENAMETOOLONG → ABSENT ; la pièce T répond -5 — "
           "L'ÉCART NOMMÉ), RIEN au cadre (les 8 premiers octets "
           "inchangés)")

    # ---- V4 : la falsification demandée ----------------------------------
    f = {p.split("=")[0]: p.split("=")[1]
         for p in falsifs[0].split() if "=" in p}
    verdit("V4:la-taille-mutee-l-ecran-attendu-diverge",
           int(f["rax"]) == 0 and int(f["taille_lue"]) == 385,
           f"la réouverture rax={f['rax']}, la taille mutée 384 → "
           f"{f['taille_lue']} au cadre : l'écran attendu "
           "(« taille=384 remplissage=384 ») DIVERGE de l'état lu "
           "(« taille=385 remplissage=384 ») — LA FALSIFICATION "
           "DEMANDÉE : le juge lit l'état, jamais le modèle")

    print(f"\n=== L'ORACLE ÉQUIVALENT u01 : {VERT} VERT, {ROUGE} ROUGE — "
          f"{EPREUVES} épreuves, {VERT + ROUGE} contrôles "
          f"{'— VERT' if ROUGE == 0 else '— ROUGE'} ===")
    if EPREUVES != 12 or VERT + ROUGE != 14 or ROUGE:
        print(f"[juge-u01] REFUS VOLUME : {EPREUVES} épreuves (attendu 12)"
              f", {VERT + ROUGE} contrôles (attendu 14), {ROUGE} ROUGE",
              file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
