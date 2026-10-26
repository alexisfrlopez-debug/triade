#!/usr/bin/env python3
"""audit_rdata.py — Audit systématique des chaînes .rdata M2 (défaut C1).

Le build dev.1 a échoué en fail-closed sur l'oracle C1. Cause racine : des
longueurs de chaînes comptées « caractères + CR » en oubliant le LF. Cet audit
vérifie TROIS niveaux :
  1. la vraie longueur octets de chaque chaîne (source build_m2.py) ;
  2. l'écart RVA jusqu'à la chaîne suivante (layout.py) — le NUL terminal doit
     tenir dans l'écart ;
  3. les constantes explicites des brouillons (mov edx/r8d N, cmp r12 N)
     confrontées aux symboles qu'elles accompagnent.
Sortie : tableau + liste des corrections nécessaires.
"""
import re
import sys

sys.path.insert(0, "/home/z/my-project/triade/m2")
import layout as L

# Chaînes réelles posées par build_m2.py (source de vérité, ordre du poser)
CHAÎNES = [
    ("MSG_BANNIERE", L.BANNIERE),
    ("MSG_CONNEXION", b"connexion entrante\r\n"),
    ("MSG_ECHO", b"echo "),
    ("MSG_CRLF", b"\r\n"),
    ("MSG_PATCH_OK", b"patch applique (majuscules)\r\n"),
    ("MSG_RB_OK", b"retour arriere (identite)\r\n"),
    ("MSG_INCONNU", b"commande inconnue\r\n"),
    ("MSG_REFUS", b"commande refusee\r\n"),
    ("MSG_FIN", b"fin connexion\r\n"),
    ("MSG_ARRET", b"arret\r\n"),
    ("MSG_ERREUR", b"erreur reseau, arret\r\n"),
    ("MSG_KO", b"TRIADE M2 : integrite KO, arret\r\n"),
    ("CMD_PATCH", b"patch\r\n"),
    ("CMD_RB", b"rollback\r\n"),
    ("CMD_QUIT", b"quit\r\n"),
]

# Constantes de longueur présentes dans les brouillons (colonne suivante le symbole)
BROUILLONS = {
    "tcp-09-conn": [("MSG_ECHO", "edx", 5), ("MSG_CRLF", "qword", 2),
                    ("MSG_FIN", "edx", 15)],
    "tcp-10-console": [("CMD_PATCH", "r8d", 7), ("MSG_PATCH_OK", "edx", 28),
                       ("MSG_REFUS", "edx", 17), ("CMD_RB", "r8d", 9),
                       ("MSG_RB_OK", "edx", 26), ("CMD_QUIT", "r8d", 6),
                       ("MSG_INCONNU", "edx", 19)],
    "tcp-12-main": [("MSG_BANNIERE", "edx", 47), ("MSG_CONNEXION", "edx", 19),
                    ("MSG_ERREUR", "edx", 21), ("MSG_ARRET", "edx", 6),
                    ("MSG_KO", "r8d", 33)],
}
# Le test de longueur rollback (cmp r12) accompagne CMD_RB
TESTS_R12 = {"CMD_PATCH": 7, "CMD_RB": 9, "CMD_QUIT": 6}

rvas = sorted((getattr(L, f"R_{n}"), n) for n, _ in CHAÎNES)
tailles = {n: len(s) for n, s in CHAÎNES}

print(f"{'symbole':<16}{'RVA':>8}{'octets':>8}{'+NUL':>6}{'gap':>6}  verdict")
defauts_gap = []
for i, (rva, nom) in enumerate(rvas):
    gap = (rvas[i + 1][0] - rva) if i + 1 < len(rvas) else 0x100
    besoin = tailles[nom] + 1
    verdict = "OK" if (gap >= besoin or i + 1 == len(rvas)) else f"COLLISION (manque {besoin - gap})"
    if verdict != "OK":
        defauts_gap.append((nom, rva, besoin, gap))
    print(f"{nom:<16}{rva:#08x}{tailles[nom]:>8}{besoin:>6}{gap:>6}  {verdict}")

print("\n--- Constantes des brouillons ---")
defauts_cst = []
for bloc, refs in BROUILLONS.items():
    for sym, reg, val in refs:
        ok = val == tailles[sym]
        if not ok:
            defauts_cst.append((bloc, sym, reg, val, tailles[sym]))
        print(f"{bloc:<16}{sym:<16}{reg:<6}{val:>4}  réel {tailles[sym]:>3}  {'OK' if ok else 'FAUX'}")

print("\n--- Tests de longueur (cmp r12) ---")
for sym, val in TESTS_R12.items():
    ok = val == tailles[sym]
    if not ok:
        defauts_cst.append(("tcp-10-console", sym, "cmp r12", val, tailles[sym]))
    print(f"tcp-10-console   {sym:<16}cmp r12 {val:>4}  réel {tailles[sym]:>3}  {'OK' if ok else 'FAUX'}")

print("\n=== SYNTHÈSE ===")
print(f"Collisions de gap : {len(defauts_gap)}")
for nom, rva, besoin, gap in defauts_gap:
    print(f"  {nom} @ {rva:#x} : besoin {besoin} o, gap {gap} o")
print(f"Constantes fausses : {len(defauts_cst)}")
for bloc, sym, reg, val, reel in defauts_cst:
    print(f"  {bloc} {sym} {reg} {val} -> {reel}")
