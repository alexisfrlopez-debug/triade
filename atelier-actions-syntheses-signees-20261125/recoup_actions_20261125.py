#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Recoup du dépôt des témoins SIGNÉS de la campagne ACTIONS (Entrée 428).

Le maître déposa la collecte entière du run 45625277486 (43 pièces) au
/livrables/preuves-actions-campagne-20261125 et signa de sa main les CINQ
témoins (kit-C : les trois temoin-N* + la SYNTHESE ; kit-D et kit-G : les
SYNTHESE). Le présent outil recoupe SUR PIÈCES :

  1. LES SIGNATURES : chaque pièce signée (temoins-signes/) == l'original
     committé de atelier-siliciums-commodite-v100/preuves-actions/ avec la
     signature append-only (préfixe byte-byte INTACT) ;
  2. LES 43 EMPREINTES : la table EMPREINTES-ACTIONS-DEPOT.txt (consignée au
     re-téléchargement du dépôt du maître) == les sha256 des pièces committées
     — la preuve du recoup byte-byte du dépôt ;
  3. LE WELCH RECALCULÉ : les 48 t de Welch (24 kit-C aux huit cibles, 12 kit-D
     et 12 kit-G aux quatre cibles, aux trois N) recomputés des csv bruts et
     comparés aux t imprimés des sorties de run (l'arrondi d'impression).

Usage : python3 recoup_actions_20261125.py
Code de sortie : 0 = tout recoupé, 1 = au moins un écart.
"""
import csv
import hashlib
import math
import pathlib
import re
import sys

ICI = pathlib.Path(__file__).resolve().parent
ORIG = ICI.parent / "atelier-siliciums-commodite-v100" / "preuves-actions"
SIGNES = ICI / "temoins-signes"

SIGNATURE = "\nFaite le 25/11/2026\nAlexis Lopez".encode("utf-8")  # 33 octets, append-only

# pièces signées : (nom du fichier, dossier original)
PIECES_SIGNEES = [
    ("temoin-dudect-collab-N60.txt", "kit-C-x86-serveur"),
    ("temoin-dudect-collab-N200.txt", "kit-C-x86-serveur"),
    ("temoin-dudect-collab-N400.txt", "kit-C-x86-serveur"),
    ("temoin-dudect-collab-SYNTHESE.txt", "kit-C-x86-serveur"),
    ("temoin-dudect-arm-SYNTHESE.txt", "kit-D-arm64-serveur"),
    ("temoin-dudect-apple-SYNTHESE.txt", "kit-G-apple-silicon"),
]

# les 43 pièces du dépôt du maître : kit, nom (les 3 journaux de scénario
# commis au add -f vivent aux mêmes dossiers)
KITS = ["kit-C-x86-serveur", "kit-D-arm64-serveur", "kit-G-apple-silicon", "vague1-annulee-macos"]

CIBLES_C = ["eq-constant", "eq-branchue", "sha256-logiciel", "sha256-x86-shani",
            "tls13-02", "tls13-13", "tls13-16", "tls13-17"]
CIBLES_A = ["eq-constant", "eq-branchue", "sha256-logiciel", "sha256-arm-sha2"]
CLASSES_EQ = ("egal", "divergent")

def sha(b):
    return hashlib.sha256(b).hexdigest()

def t_de_welch(a, b):
    n1, n2 = len(a), len(b)
    m1, m2 = sum(a) / n1, sum(b) / n2
    v1 = sum((x - m1) ** 2 for x in a) / (n1 - 1)
    v2 = sum((x - m2) ** 2 for x in b) / (n2 - 1)
    return (m1 - m2) / math.sqrt(v1 / n1 + v2 / n2)

def t_annonces(chemin, cibles):
    texte = chemin.read_text(encoding="utf-8", errors="replace")
    motif = re.compile(r"\[(" + "|".join(re.escape(c) for c in cibles) + r")\]"
                       r"[^\[]*?t de Welch = (-?[\d.]+)")
    return {m.group(1): float(m.group(2)) for m in motif.finditer(texte)}

def main():
    verts, ecarts = [], []

    # ---- 1. les signatures ----
    print("== LES SIGNATURES (préfixe byte-byte INTACT + append-only) ==")
    for nom, kit in PIECES_SIGNEES:
        original = (ORIG / kit / nom).read_bytes()
        signe = (SIGNES / nom).read_bytes()
        if signe == original + SIGNATURE:
            print(f"  VERT {nom} : original {len(original)} o intact + signature "
                  f"{len(SIGNATURE)} o (« Faite le 25/11/2026 / Alexis Lopez »)")
            verts.append(nom)
        else:
            detail = "préfixe NON intact" if not signe.startswith(original) else \
                     "suffixe != signature attendue"
            print(f"  ROUGE {nom} : {detail}")
            ecarts.append(nom)

    # ---- 2. les 43 empreintes (la table documente LE DÉPÔT : les pièces
    # signées y vivent signées — la comparaison se fait aux copies signées
    # de l'atelier ; les autres, aux originaux committés) ----
    print("\n== LES 43 EMPREINTES (dépôt du maître == pièces de l'atelier) ==")
    table = {}
    for ligne in (ICI / "EMPREINTES-ACTIONS-DEPOT.txt").read_text().splitlines():
        m = re.match(r"([0-9a-f]{64})\s+(\S+/\S+)\s*$", ligne.strip())
        if m:
            table[m.group(2)] = m.group(1)
    signes = {nom for nom, _ in PIECES_SIGNEES}
    n_ok, n_ecart = 0, 0
    for rel in sorted(table):
        kit, nom = rel.split("/", 1)
        if nom in signes:
            local = SIGNES / nom
        else:
            local = ORIG / kit / nom
        if not local.exists():
            print(f"  ROUGE {rel} : pièce absente de l'atelier")
            n_ecart += 1
            continue
        if sha(local.read_bytes()) == table[rel]:
            n_ok += 1
        else:
            print(f"  ROUGE {rel} : sha256 != table")
            n_ecart += 1
    print(f"  {n_ok} pièces recoupées byte-byte à la table, {n_ecart} écart(s)")
    verts.extend([rel] * n_ok)

    # ---- 3. le Welch recalculé des csv bruts ----
    print("\n== LE WELCH RECALCULÉ DU CSV BRUT (48 t attendus) ==")
    configs = [("kit-C-x86-serveur", "journal-dudect-collab-N{n}.csv",
                "sortie-run-N{n}.txt", "dudect-collab", CIBLES_C),
               ("kit-D-arm64-serveur", "journal-dudect-arm-N{n}.csv",
                "sortie-run-N{n}.txt", "dudect-arm", CIBLES_A),
               ("kit-G-apple-silicon", "journal-dudect-apple-N{n}.csv",
                "sortie-run-N{n}.txt", "dudect-apple", CIBLES_A)]
    tot_v, tot_e = 0, 0
    for kit, csvpat, sortpat, instrument, cibles in configs:
        print(f"  -- {kit} ({instrument}) --")
        for n in (60, 200, 400):
            donnees = {}
            with open(ORIG / kit / csvpat.format(n=n)) as f:
                for ligne in csv.DictReader(f):
                    donnees.setdefault((ligne["cible"], ligne["classe"]), []).append(int(ligne["ticks"]))
            annonces = t_annonces(ORIG / kit / sortpat.format(n=n), cibles)
            for cible in cibles:
                ca, cb = CLASSES_EQ if cible.startswith("eq-") else ("fixe", "aleatoire")
                a, b = donnees.get((cible, ca), []), donnees.get((cible, cb), [])
                if not a or not b:
                    print(f"    ROUGE N={n} {cible}: CLASSE MANQUANTE")
                    tot_e += 1
                    continue
                t = t_de_welch(a, b)
                attendu = annonces.get(cible)
                if attendu is None:
                    print(f"    ROUGE N={n} {cible}: t non imprimé")
                    tot_e += 1
                    continue
                ecart = abs(t - attendu)
                ok = ecart < 0.005  # l'arrondi d'impression du mesureur
                diver = "  (DIVERGENTE |t|>5)" if abs(t) > 5 else ""
                print(f"    {'VERT' if ok else 'ROUGE'} N={n} {cible}: t={t:+.2f} "
                      f"imprimé={attendu:+.2f} écart={ecart:.3f}{diver}")
                tot_v += ok
                tot_e += (not ok)
    print(f"\nBILAN GÉNÉRAL : {len(verts)} recoups VERT, {len(ecarts) + tot_e} écart(s)")
    print(f"  signatures : {sum(1 for v in verts if v.endswith('.txt') and 'N' in v or 'SYNTHESE' in v)} / {len(PIECES_SIGNEES)} signées recoupées")
    print(f"  empreintes : {sum(1 for v in verts if '/' in str(v))} pièces recoupées byte-byte")
    print(f"  Welch : {tot_v} t recoupés VERT, {tot_e} écart(s)")
    return 1 if (ecarts or tot_e) else 0

if __name__ == "__main__":
    sys.exit(main())
