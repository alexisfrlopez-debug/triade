#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""106_carte_kits_295.py — LA CARTE DU /test PORTÉE À 295 : la section du
run v2 du bras T revenu VERT signé, l'unité 2 verte aux deux bras, les DEUX
lignes au livre attendues (la réponse à la question du développeur).
La carte 294 (12 646 o, sha256 91de873b…) demeurant INTACTE sur ses
octets, la section s'APPEND (l'histoire des éditions demeure, jamais
réécrite). Re-téléchargement byte-byte après le geste."""
import hashlib
import pathlib
import sys

sys.path.insert(0, "/home/z/my-project/work/triade/scripts")
import drive_sync as ds  # noqa: E402

SHA_294 = "91de873b"  # la carte 294 attendue (les 8 premiers de sha256)

SECTION = """

=== LE RUN v2 DU BRAS T REVENU VERT SIGNÉ — L'UNITÉ 2 VERTE AUX DEUX BRAS — le 15/11/2026 (l'Entrée 295) ===
L'annonce « preuves unite 02 dans /test du drive » : le run v2 vécu au terrain le 14/11 19:53:02Z (PORTABLE · Windows 10 · AMD64 · Python 3.14.10 — la même machine que les SIX runs de la campagne, CA2), le témoin DATÉ et SIGNÉ de la main (Alexis Lopez, 14/11/2026 — D99), déposé au coffre 20:00:17Z. LE RECOUP DU LABO (la sonde 104, 7/7 VERT) : loupe.exe 127 488 o sha256 98354ff6… == la gravure du kit v2 == l'empreinte que porte le témoin ; LES VINGT vecteurs du v2 == LES VINGT du v1 (le même juge — le diff v1→v2 recoupé : la note de révision et la constante R_JOURNAL 0xE4E0→0xE4A0, RIEN d'autre), les DEUX ROUGE du juge fautif v1 (les-bords-de-fenetre, cinq-entrees-dont-une-non-alignee) RETOURNÉS VERT au terrain ; LE VERDICT : 20 VERT, 0 ROUGE ; la chronologie tenue : run 19:53:02Z → la main 19:53:45Z → le coffre 20:00:17Z. LE DOSSIER ENTIER était là (le réceptacle preuves-unite02/ ne porte QUE le témoin — le scénario n'écrit que lui ; la console vit au dossier du kit). Le dépôt est RANGÉ à /archives-livraisons/unite-02-loupe-20261114/preuves-unite02/ (D143 : déplacé, jamais jeté, md5 recoupé avant et après).
LE BRAS T EST VERT : L'UNITÉ 2 EST VERTE AUX DEUX BRAS (le bras C 20-0 à l'Entrée 294, le bras T 20-0 au présent run v2) ; le run T v1 18-2 NE CONSOMME PAS d'itération (la faute était au juge du labo — le précédent 283/284).
CE QUI RESTE (la réponse à « je n'ai pas compris ce qu'il faut faire que je n'ai pas deja fait pour c loupe 02 ») : RIEN du run, RIEN du témoin — tout est vécu aux DEUX bras. LE GESTE QUI MANQUE EST LE MÊME POUR LES DEUX, ET IL N'ÉTAIT PAS VÉCU AU C LOUPE-02 NON PLUS : LES DEUX LIGNES AU LIVRE. livraisons.csv de l'atelier porte ENCORE les DEUX seules lignes de loupe-01 — l'unité 2 y attend les siennes :
  — C-loupe-02-it1 : kit 2026-11-14, run 2026-11-14, VERT, « en attente » ;
  — T-loupe-02-it1 : kit 2026-11-14, run 2026-11-14, VERT, « en attente ».
LE CHEMIN : le GUI (TRIADE_gui_tous_runs_v1 ou TRIADE_gui_campagne_v1), étape 2 → le TROISIÈME bouton « CHOISIR L'ATELIER EXISTANT… » (jamais « CHOISIR LE DOSSIER… », qui veut campagne-d204 — le refus nommé à l'Entrée 292) → l'atelier vit à /test/archives-livraisons/unite-01-loupe-20261114/atelier-campagne-d204-20261114-013520/ ; puis étape 4 → la ligne loupe-02 × C puis × T → l'onglet « 5 · LIVRAISON » → CONSIGNER chaque ligne ; les onglets compagnons aux gestes vécus (4 · CARNET M3, 6 · DÉFAUTS s'il y en a, 7 · CHRONO M4) ; PUIS l'atelier ENTIER renvoyé au coffre /test. ENSUITE loupe-05 sha256, aux deux bras — le labo construit à la commande.
"""

# -- la carte courante au coffre ------------------------------------------------
coffre = ds.list_folder(ds.DRIVE_ROOT_ID)
test = coffre.get("test")
carte = ds.list_folder(test["id"]).get("LISEZMOI-KITS-UNITES-D204.txt")
assert carte, "la carte LISEZMOI-KITS-UNITES-D204.txt introuvable au /test"

st, octets, _ = ds.api("GET", ds.API + f"/files/{carte['id']}?alt=media")
assert st == 200, f"HTTP {st}"
sha_avant = hashlib.sha256(octets).hexdigest()
assert sha_avant.startswith(SHA_294), (
    f"la carte au coffre n'est pas l'état 294 : sha256 {sha_avant[:8]}… "
    f"(attendu {SHA_294}…) — REFUS, jamais par-dessus une carte inconnue")
print(f"[avant] la carte 294 : {len(octets)} o, sha256 {sha_avant[:8]}… — "
      f"l'état attendu, la section s'appose")

# -- l'apposition ---------------------------------------------------------------
texte = octets.decode("utf-8-sig")
if "Entrée 295" in texte:
    print("[idempotent] la section 295 vit déjà à la carte — rien à faire")
    sys.exit(0)
nouveau = octets.decode("utf-8-sig") + SECTION
chemin = pathlib.Path("/home/z/my-project/work/carte-kits-295.txt")
chemin.write_bytes(b"\xef\xbb\xbf" + nouveau.encode("utf-8"))
ds.upload_update(carte["id"], chemin)
print(f"[apposée] la section 295 : {len(octets)} → {chemin.stat().st_size} o")

# -- le recoup PAR RE-TÉLÉCHARGEMENT -------------------------------------------
st, octets2, _ = ds.api("GET", ds.API + f"/files/{carte['id']}?alt=media")
assert st == 200, f"HTTP {st}"
sha_apres = hashlib.sha256(octets2).hexdigest()
local = chemin.read_bytes()
assert octets2 == local, "la carte re-téléchargée diverge de l'apposée"
assert octets2.startswith(octets[:len(octets)]), (
    "la carte 294 fut altérée — la section devait s'apposer, jamais réécrire")
print(f"[recoup] la carte re-téléchargée : {len(octets2)} o, sha256 "
      f"{sha_apres[:8]}… — la 294 INTACTE en tête, la section 295 en queue, "
      f"byte-byte l'apposée")
