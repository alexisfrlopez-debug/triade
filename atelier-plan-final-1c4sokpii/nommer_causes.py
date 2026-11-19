#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""nommer_causes.py — LE RESTE NOMMÉ DÉFINITIF : chaque survivant des 21,
sa cause ANALYSÉE au cas par cas (le contexte instruction de reste_contexte.txt,
les contrats des blocs, les shims du harnais) — jamais un silence."""
import csv
import pathlib

ICI = pathlib.Path(__file__).resolve().parent

# LA CAUSE DE CHACUN (l'analyse : le contexte + le contrat + le shim)
CAUSES = {
    ("loupe-01", "0x143"): (
        "LE CODE 3 JAMAIS SERVI — le je garde le GetLastError==3 "
        "(ERROR_PATH_NOT_FOUND) ; le shim CreateFileW du harnais rend "
        "toujours 2 (fichier introuvable) pour tout chemin inconnu : la "
        "voie du 3 est morte AU HARNAIS (elle vit au vrai Windows)"),
    ("loupe-03", "0x1b"): (
        "L'ÉTAT MOURANT — la lecture du champ de session à la fermeture ; "
        "le champ meurt avec la fenêtre, AUCUN observable (écran, disque, "
        "sortie) ne le relit après le geste"),
    ("loupe-03", "0x3b"): (
        "L'ÉTAT MOURANT — la mise à zéro de l'écran à la fermeture "
        "([rax+0x1000] ← 0) ; la valeur écrite ne survit pas au geste"),
    ("loupe-03", "0x41"): (
        "L'ÉTAT MOURANT — la même mise à zéro, l'immédiat muté"),
    ("loupe-03", "0x19"): (
        "L'ÉTAT MOURANT — la lecture du champ voisin ([rbx+0x22c]) ; le "
        "CloseHandle deservi est silencieux au harnais, l'état meurt"),
    ("loupe-03", "0x5a"): (
        "L'ÉTAT MOURANT — la mise à zéro du champ d'état ([rax] ← 0xf1) ; "
        "jamais relu après la fermeture"),
    ("loupe-03", "0x41b"): (
        "L'ÉTAT MOURANT — la mise à zéro, la seconde manifestation"),
    ("loupe-04", "0x28"): (
        "RBP VOLATIL (msx64) — le xor ebp,ecx détruit un registre que "
        "L'APPELANT NE RELIT JAMAIS (la convention : RBP est volatil) ; "
        "l'état_propre du harnais ne le garde pas non plus"),
    ("loupe-07", "0x11"): (
        "LE SENTINEL ADJACENT — le cmp lit [rbx+0x225] au lieu de "
        "[rbx+0x210] ; dans TOUT état servable par le harnais les champs "
        "voisins de la zone portent le même -1 (la zone naît remplie du "
        "sentinel) — la garde tombe du même côté"),
    ("loupe-09", "0x387"): (
        "LE SITE DE TRANSFERT HORS TABLE — le mov edx,0x102 d'un transfert "
        "de WM_CHAR ; la table de routage FERMÉE (Q3) mène les WM_CHAR "
        "ailleurs : ce site d'expédition n'est jamais atteint (le code "
        "mort d'une voie remplacée par la table)"),
    ("loupe-11", "0x137"): (
        "LA POIGNÉE JAMAIS SERVIE — le shl ×16 de la position SB_POIGNEE ; "
        "le shim GetScrollInfo rend l'échec (eax≠0) : le je court-circuite "
        "la voie, la multiplication ne vit jamais au harnais"),
    ("loupe-11", "0x1d5"): (
        "LE SHIM AVEUGLE — l'argument r9d (le drapeau redessiné) de "
        "SetScrollInfo ; le shim ne lit pas cet argument : aucune valeur "
        "ne se distingue"),
    ("loupe-11", "0x1df"): (
        "LE SHIM AVEUGLE — l'argument rcx (le handle) du second "
        "SetScrollInfo ; le shim ne distingue pas le handle"),
    ("loupe-12", "0x27b"): (
        "LE SHIM AVEUGLE — l'argument rcx (le hwnd) d'InvalidateRect ; le "
        "shim accepte tout handle : le registre muté ne se distingue pas"),
    ("loupe-14", "0xdc"): (
        "LE CHAMP AU-DELÀ DU MOTIF — la mise à zéro du tampon du motif "
        "([rax+8] ← 0xf1...) ; seuls les octets du motif POSÉ sont relus "
        "(la longueur fait foi) : les octets au-delà ne vivent jamais"),
    ("loupe-14", "0x21b"): (
        "LA VOIE DE L'ÉCHEC JAMAIS SERVIE — le je garde l'échec de "
        "l'appel [rip-0x28ee] (le positionnement) ; le shim réussit "
        "toujours (eax≠0, le BOOL de succès) : la branche de l'échec "
        "n'est jamais prise au harnais"),
    ("loupe-15", "0x1b"): (
        "LA CONVERGENCE DES DEUX GARDES — le cmp lit un champ lointain "
        "(≠ -1) : la première garde ne tombe plus, mais la SECONDE garde "
        "(la taille nulle, test r13,r13) mène AU MÊME refus -4 par la "
        "même cible 0x61e7 — les deux voies convergent"),
    ("loupe-15", "0xfb"): (
        "LE CHEMIN DU RECADRAGE — l'arithmétique du bord (add rcx,rax au "
        "lieu de add rax,rdx) ; le chemin ne vit qu'au recadrage du "
        "curseur hors vue APRÈS un geste qui l'y met — les valeurs "
        "servables de la batterie ne le distinguent pas (le cas nommé, "
        "le contrôle manquant : le recadrage forcé)"),
    ("loupe-16", "0x238"): (
        "LE SUIVI DE VUE APRÈS SAISIE — la pose du champ de vue "
        "([rbx+0x218] ← r15) sur la voie rare du suivi ; la batterie "
        "n'atteint pas cette branche (le contrôle manquant nommé : la "
        "saisie au-delà de la dernière colonne visible)"),
    ("loupe-16", "0x21e"): (
        "LE SUIVI DE VUE APRÈS SAISIE — la garde du champ de vue sur la "
        "même voie rare (cmp rcx,[rbx+0x218])"),
    ("loupe-17", "0x207"): (
        "LA CIBLE DÉTOURNÉE RETOMBE — la boucle de puisement du journal "
        "(jge 0x66e8 → 0x66d4) ; la cible mutée re-pose le même état "
        "avant la même boucle : le comportement converge (l'analyse au "
        "cas par cas : 0x66d4 re-pose, la boucle reprend)"),
}


def main():
    lignes = list(csv.DictReader(open(ICI / "reste_nomme.csv",
                                      encoding="utf-8")))
    for r in lignes:
        cle = (r["bid"], r["offset"])
        r["cause"] = CAUSES.get(cle, "la cause au cas par cas (le contexte)")
    with open(ICI / "reste_nomme.csv", "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bid", "offset", "octet", "cause"])
        w.writeheader()
        for r in lignes:
            w.writerow(r)
    from collections import Counter
    familles = Counter()
    for r in lignes:
        c = r["cause"]
        for nom in ["LE CODE 3", "L'ÉTAT MOURANT", "RBP VOLATIL",
                    "LE SENTINEL", "LE SITE DE TRANSFERT",
                    "LA POIGNÉE", "LE SHIM AVEUGLE", "LE CHAMP AU-DELÀ",
                    "LA VOIE DE L'ÉCHEC", "LA CONVERGENCE",
                    "LE CHEMIN DU RECADRAGE", "LE SUIVI DE VUE",
                    "LA CIBLE DÉTOURNÉE"]:
            if c.startswith(nom):
                familles[nom] += 1
                break
    print(f"les {len(lignes)} survivants nommés :")
    for f_, n in familles.most_common():
        print(f"  {n:2d} × {f_}")
    assert sum(familles.values()) == len(lignes), \
        "chaque survivant porte sa cause"


if __name__ == "__main__":
    main()
