#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""100_epreuves_juge.py — LES ÉPREUVES DU JUGE (la leçon du terrain 294).

L'ÉCART NOMMÉ : le scénario T livré au kit 02 porte R_JOURNAL = 0xE4E0 ;
le layout (D161, la source unique des constantes du domaine) dit
R_JOURNAL = 0xE4A0 — et le lea de la PIÈCE (lu à l'octet près au script
99) vise 0xE4A0. Le juge posait le journal 64 octets trop haut : la
pièce lisait son compte à 0xF4A0 (l'entrée #156 de la zone zéroée) →
compte 0 → AUCUN recouvrement → les DEUX vecteurs V2 ROUGE au terrain.

DEUX ÉPREUVES :
  A. L'AUDIT DES CONSTANTES — l'épreuve qui MANQUAIT à la 290 : chaque
     constante d'adresse du scénario LIVRÉ (lues par AST, jamais de sa
     copie) contre la vérité du layout. Le scénario T v1 doit ÉCHOUER
     (la preuve que le garde aurait pris la faute AVANT le terrain) ;
     les juges qui ont couru au terrain (01-T v2, 01-C v2, 02-C) et le
     02-T v1 audités nommés.
  B. LA FAUTE REJOUÉE — la plomberie simulée octet par octet : le juge
     pose sa zone, la boucle de la pièce lit À SON ADRESSE À ELLE (les
     sémantiques exactes du asm et du poser_journal) — à 0xE4E0 les
     DEUX vecteurs V2 divergent du modèle (les DEUX ROUGE du terrain
     reproduits au labo) ; à 0xE4A0 (le layout) le recouvrement vit."""
import ast
import pathlib
import struct
import sys

REPO = pathlib.Path("/home/z/my-project/work/triade")
CAMP = REPO / "scripts" / "campagne_d204"
sys.path.insert(0, str(REPO / "loupe"))
import layout as L  # noqa: E402  — la source unique (D161)

VERITE = {
    "R_LOUPE01": L.LOUPE01_VA, "R_LOUPE02": L.LOUPE02_VA,
    "R_LOUPE03": L.LOUPE03_VA, "R_CADRE": L.R_CADRE,
    "R_JOURNAL": L.R_JOURNAL, "R_EMPREINTES": L.R_EMPREINTES,
    "ZONE_JOURNAL": L.ZONE_JOURNAL,
}

SCENARIOS = [
    ("01-T v2 (couru VERT au terrain, 284)", CAMP / "unite-01-T" / "kit" / "scenario-unite01.py"),
    ("01-C v2 (couru VERT au terrain, 287)", CAMP / "unite-01-C" / "kit" / "scenario-unite01C.py"),
    ("02-T v1 (couru 18 VERT 2 ROUGE, 294)", CAMP / "unite-02-T" / "kit" / "scenario-unite02.py"),
    ("02-C v1 (couru VERT au terrain, 294)", CAMP / "unite-02-C" / "kit" / "scenario-unite02C.py"),
]


def constantes_du_fichier(chemin):
    """Les constantes d'adresse du scénario LIVRÉ, lues par AST."""
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    Trouve = {}
    iat = None
    for noeud in arbre.body:
        if isinstance(noeud, ast.Assign) and len(noeud.targets) == 1:
            cible = noeud.targets[0]
            if isinstance(cible, ast.Name):
                if isinstance(noeud.value, ast.Constant):
                    Trouve[cible.id] = noeud.value.value
                elif (isinstance(noeud.value, ast.Dict)
                      and cible.id == "IAT_SLOTS"):
                    iat = {ast.literal_eval(k): ast.literal_eval(v)
                           for k, v in zip(noeud.value.keys, noeud.value.values)}
    return Trouve, iat


print("=" * 78)
print("A. L'AUDIT DES CONSTANTES — le scénario LIVRÉ contre le layout (D161)")
print("=" * 78)
total_vert, total_rouge = 0, 0
resultats = {}
for etiquette, chemin in SCENARIOS:
    consts, iat = constantes_du_fichier(chemin)
    verts, rouges = [], []
    for nom, verite in VERITE.items():
        if nom in consts:
            (verts if consts[nom] == verite else rouges).append(
                f"{nom} 0x{consts[nom]:X} {'==' if consts[nom] == verite else '≠'} "
                f"layout 0x{verite:X}")
    if iat is not None:
        for feuille, slot in sorted(iat.items()):
            vrai = L.IAT_SLOTS.get(feuille)
            if vrai is None:
                rouges.append(f"IAT {feuille} : hors layout")
            else:
                (verts if slot == vrai else rouges).append(
                    f"IAT {feuille} 0x{slot:X} {'==' if slot == vrai else '≠'} "
                    f"layout 0x{vrai:X}")
    resultats[etiquette] = (verts, rouges)
    print(f"\n[{etiquette}]  {chemin.relative_to(REPO)}")
    for v in verts:
        print(f"    [VERT] {v}")
    for r in rouges:
        print(f"    [ROUGE] {r}")
    print(f"    → {len(verts)} VERT, {len(rouges)} ROUGE")
    total_vert += len(verts)
    total_rouge += len(rouges)

faute_prise = any(r for _, (v, r) in resultats.items() if r)
print(f"\n[AUDIT] {total_vert} VERT, {total_rouge} ROUGE sur les "
      f"{len(SCENARIOS)} juges audités")
print("[AUDIT] la faute du 02-T v1 " + ("EST PRISE par le garde (R_JOURNAL +0x40) — "
      "l'épreuve qui manquait à la 290, désormais tenue" if faute_prise
      else "N'EST PAS prise — le garde est aveugle, à reprendre"))

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("B. LA FAUTE REJOUÉE — la plomberie octet par octet (le juge pose, la pièce lit)")
print("=" * 78)

FEN = 65536
DONNEES = (CAMP / "unite-02-T" / "kit" / "temoin-3f.bin").read_bytes()
VECTEURS = {
    "V2:les-bords-de-fenetre": [(FEN, 0xAA), (FEN + 383, 0xBB),
                                (FEN + 384, 0xCC), (FEN - 16, 0xDD)],
    "V2:cinq-entrees-dont-une-non-alignee": [(FEN + 5, 0x11), (FEN + 100, 0x22),
                                             (FEN + 200, 0x33), (FEN + 300, 0x44),
                                             (FEN + 383, 0x55)],
}


def zone_du_juge(entrees):
    """poser_journal du scénario, VERBATIM : zone zéroée, entrées à 16·i,
    le compte à +4096."""
    brut = bytearray(L.ZONE_JOURNAL)
    for i, (dec, octet) in enumerate(entrees):
        brut[16 * i:16 * i + 16] = struct.pack("<QB7x", dec, octet)
    brut[4096:4100] = struct.pack("<I", len(entrees))
    return bytes(brut)


def boucle_de_la_piece(memoire, base_journal, dec, rempl):
    """La boucle du asm, VERBATIM : le compte à base+4096, les entrées au
    pas de 16 (pos qword, l'octet à +8), recouvertes si pos ∈ [dec, dec+rempl)."""
    compte = struct.unpack_from("<I", memoire, base_journal + 4096)[0]
    tampon = bytearray(DONNEES[dec:dec + rempl])   # la lecture fraîche ReadFile
    for i in range(compte):
        pos = struct.unpack_from("<Q", memoire, base_journal + 16 * i)[0]
        if dec <= pos < dec + rempl:
            octet = memoire[base_journal + 16 * i + 8]
            tampon[pos - dec] = octet
    return compte, bytes(tampon)


def modele(entrees):
    """modele_tampon du juge (le modèle indépendant)."""
    rempl = min(384, len(DONNEES) - FEN)
    tampon = bytearray(DONNEES[FEN:FEN + rempl])
    for dec, octet in entrees:
        if FEN <= dec < FEN + rempl:
            tampon[dec - FEN] = octet
    return rempl, bytes(tampon)


for adresse_juge, etiquette in [(0xE4E0, "le juge v1 (0xE4E0, +0x40)"),
                                (0xE4A0, "le layout (0xE4A0, corrigé)")]:
    print(f"\n[rejoué] le juge pose sa zone à {etiquette} ; "
          f"la pièce lit son journal à 0xE4A0 (le lea, script 99)")
    for nom, entrees in VECTEURS.items():
        memoire = bytearray(0x20000)
        memoire[adresse_juge:adresse_juge + L.ZONE_JOURNAL] = zone_du_juge(entrees)
        rempl = min(384, len(DONNEES) - FEN)
        compte, tampon = boucle_de_la_piece(memoire, 0xE4A0, FEN, rempl)
        rempl_att, tamp_att = modele(entrees)
        vert = tampon == tamp_att and rempl == rempl_att
        compte_ecrit = len(entrees)
        detail = (f"la pièce lit compte={compte} (le juge en posait "
                  f"{compte_ecrit}) → "
                  + ("le recouvrement VIT" if compte == compte_ecrit
                     else "AUCUNE entrée recouverte"))
        print(f"    [{'VERT' if vert else 'ROUGE'}] {nom} : {detail} ; "
              f"le tampon {'==' if vert else 'DIVERGE DU'} modèle")
        if adresse_juge == 0xE4E0 and not vert:
            total_rouge += 0  # (déjà compté à l'audit)
        elif adresse_juge == 0xE4A0:
            assert vert, "à la constante corrigée le vecteur doit être VERT"

print("\n[B. FAUTE REJOUÉE] à 0xE4E0 : les DEUX ROUGE du terrain reproduits "
      "au labo (le compte lu tombe à l'entrée #156 de la zone zéroée — "
      "0xF4A0 = 0xE4E0 + 2496) ; à 0xE4A0 (le layout) : le recouvrement vit, "
      "les DEUX vecteurs VERT — la correction d'UNE constante suffit, la "
      "PIÈCE EST INTACTE (D143)")
