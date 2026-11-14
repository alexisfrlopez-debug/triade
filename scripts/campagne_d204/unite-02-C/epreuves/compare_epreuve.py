#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""compare_epreuve.py — LE JUGE DE L'ÉPREUVE POSIX (loupe-02 × bras C, la
campagne D204) : chaque ligne VECTEUR de sortie-epreuve.txt confrontée au
MODÈLE INDÉPENDANT (les découpe du témoin + le recouvrement du journal) —
jamais les octets de la pièce. Le juge dit 17 lignes VERT/ROUGE."""
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
LIGNES = (ICI / "sortie-epreuve.txt").read_text(
    encoding="utf-8", errors="replace").splitlines()

VERTS, ROUGES = 0, 0


def controle(nom, ok, detail=""):
    global VERTS, ROUGES
    print(f"[{'VERT' if ok else 'ROUGE'}] {nom}" + (f" — {detail}" if detail else ""))
    VERTS += ok
    ROUGES += not ok


def temoin(nom):
    return (ICI / nom).read_bytes()


def champs(ligne):
    """dec, rax, rempl, vue, curseur, tampon d'une ligne VECTEUR."""
    parties = ligne.split()
    dec = int(parties[2].split("=")[1])
    rax = int(parties[3].split("=")[1])
    rempl = int(parties[4].split("=")[1])
    vue = int(parties[5].split("=")[1])
    curseur = int(parties[6].split("=")[1])
    tampon = bytes.fromhex(parties[7].split("=")[1])
    return dec, rax, rempl, vue, curseur, tampon


def model_fenetre(donnees, dec, journal=()):
    rempl = min(384, len(donnees) - dec)
    t = bytearray(donnees[dec:dec + rempl])
    for d, o in journal:
        if dec <= d < dec + rempl:
            t[d - dec] = o
    return rempl, bytes(t)


lignes = list(LIGNES)
i = 0

# ---- V1 : les témoins — la fenêtre née + les frontières ----------------------
for nom, taille_attendue in (("temoin-1.bin", 1), ("temoin-384.bin", 384),
                             ("temoin-3f.bin", 3 * 65536 + 1)):
    donnees = temoin(nom)
    ouvrir = next(l for l in lignes if l.startswith(f"OUVRIR {nom} "))
    r, m = int(ouvrir.split("rax=")[1].split()[0]), int(
        ouvrir.split("rempl=")[1])
    controle(f"V1:{nom}-l-ouverture", r == 0 and m == min(384, len(donnees)),
             f"rax={r}, remplissage {m} == min(384, {len(donnees)})")
    nee = next(l for l in lignes if l.startswith(f"VECTEUR nee")
               and lignes.index(l) > lignes.index(ouvrir)
               and lignes.index(l) <= lignes.index(ouvrir) + 2)
    d, r, m, v, c, t = champs(nee)
    controle(f"V1:{nom}-la-fenetre-nee",
             r == 0 and m == min(384, len(donnees))
             and t[:m] == donnees[:m] and v == 0 and c == 0,
             f"la première fenêtre lue INLINE au bloC session (l'écart nommé "
             f"du bras C : le loupe-01 du plan APPELLE loupe-02, la pièce C "
             f"l'incline dans son ouvrir) — le tampon == la découpe")

# les frontières : toutes les lignes VECTEUR frontiere par bloc témoin
frontieres = [l for l in lignes if l.startswith("VECTEUR frontiere")]
tout_ok = len(frontieres) >= 8     # 1+3+5 aux trois témoins (les doublons
                                   # de frontière du harnais C : bénins)
for l in frontieres:
    d, r, m, v, c, t = champs(l)
    # deviner le témoin par la taille courante : la ligne OUVRIR précédente
    nom = max((l2 for l2 in lignes
               if l2.startswith("OUVRIR") and lignes.index(l2) < lignes.index(l)),
              key=lambda l2: lignes.index(l2)).split()[1]
    donnees = temoin(nom)
    rempl_att, tamp_att = model_fenetre(donnees, d)
    tout_ok &= (r == 0 and m == rempl_att and t[:m] == tamp_att
                and v == 0 and c == 0)
controle("V1:les-frontieres", tout_ok,
         f"{len(frontieres)} décalages frontière (0, la dernière valide, la "
         f"dernière pleine, les fenêtres de la zone 65536) : le tampon == la "
         f"découpe, remplissage == min(384, taille − décalage), la vue et le "
         f"curseur INTACTS")

# le vide
vide = next(l for l in lignes if l.startswith("OUVRIR vide.bin"))
r, m = int(vide.split("rax=")[1].split()[0]), int(vide.split("rempl=")[1])
controle("V1:vide.bin-l-ouverture", r == 0 and m == 0,
         "le vide s'ouvre, remplissage 0 (la fenêtre née est vide)")
l_vide = next(l for l in lignes if l.startswith("VECTEUR vide"))
d, r, m, v, c, t = champs(l_vide)
controle("V1:vide.bin-aucune-fenetre-valide", r == -3 and m == 0,
         f"rax={r} (décalage 0 ≥ taille 0 → -3 HORS-BORNES), rien lu")

# ---- V2 : le recouvrement du journal ------------------------------------------
journal_bords = [(65536, 0xAA), (65536 + 383, 0xBB),
                 (65536 + 384, 0xCC), (65536 - 16, 0xDD)]
donnees3f = temoin("temoin-3f.bin")
l_bords = next(l for l in lignes if l.startswith("VECTEUR bords"))
d, r, m, v, c, t = champs(l_bords)
rempl_att, tamp_att = model_fenetre(donnees3f, 65536, journal_bords)
controle("V2:les-bords-de-fenetre",
         r == 0 and m == rempl_att and t[:m] == tamp_att,
         "le premier (0xAA) et le dernier (0xBB) recouverts ; l'avant et "
         "l'après IGNORÉS — l'édition survit au défilement")
avant = next(l for l in lignes if l.startswith("JOURNAL avant"))
apres = next(l for l in lignes if l.startswith("JOURNAL apres"))
controle("V2:le-journal-intact",
         avant.split("avant=")[1] == apres.split("apres=")[1],
         "loupe-02 n'écrit JAMAIS au journal (I2)")
journal_multi = [(65536 + 5, 0x11), (65536 + 100, 0x22), (65536 + 200, 0x33),
                 (65536 + 300, 0x44), (65536 + 383, 0x55)]
l_multi = next(l for l in lignes if l.startswith("VECTEUR multi"))
d, r, m, v, c, t = champs(l_multi)
rempl_att, tamp_att = model_fenetre(donnees3f, 65536, journal_multi)
controle("V2:cinq-entrees-dont-une-non-alignee",
         r == 0 and m == rempl_att and t[:m] == tamp_att,
         "cinq entrées dedans (fen+5 NON ALIGNÉE comprise) — le tampon == "
         "le modèle indépendant")

# ---- V3 : les rejets — le poison INTACT ---------------------------------------
donnees384 = temoin("temoin-384.bin")
poison = b"\xCC" * 384
attendus_v3 = [("sans-session", -4), ("non-aligne", -5),
               ("a-la-taille", -3), ("au-dela", -3), ("immense", -3)]
for nom_v, rax_att in attendus_v3:
    l_v = next(l for l in lignes if l.startswith(f"VECTEUR {nom_v} "))
    d, r, m, v, c, t = champs(l_v)
    if nom_v == "sans-session":
        ok = r == rax_att          # le tampon : celui du multi (rien lu)
        detail = f"rax={r} (attendu {rax_att} SESSION, rien lu)"
    else:
        ok = (r == rax_att and m == 0xBEEF and t == poison)
        detail = (f"rax={r} (attendu {rax_att}), remplissage {m} == 0xBEEF "
                  f"INTACT, le tampon empoisonné INTACT (rien lu)")
    controle(f"V3:{nom_v}", ok, detail)

# ---- V4 : l'échec système ------------------------------------------------------
l_echec = next(l for l in lignes if l.startswith("VECTEUR echec-read"))
d, r, m, v, c, t = champs(l_echec)
controle("V4:l-echec-readfile", r == -6 and m == 0 and t == poison,
         f"rax={r} (le tiroir a refusé → -6 SYSTÈME), remplissage {m} == 0 "
         f"(fail-closed), le tampon empoisonné INTACT — jamais un octet non lu")
l_survit = next(l for l in lignes if l.startswith("VECTEUR session-survit"))
d, r, m, v, c, t = champs(l_survit)
controle("V4:la-session-survit",
         r == 0 and m == 384 and t[:m] == donnees384,
         "l'échec ne clôt PAS la session : la lecture suivante est verte, "
         "le tampon == le témoin entier")

# ---- V5 : la falsification ------------------------------------------------------
l_avant = next(l for l in lignes if l.startswith("VECTEUR falsif-avant"))
d, r, m, v, c, t = champs(l_avant)
ok_lecture = r == 0 and m == 384 and t[:m] == donnees384
etat = next(l for l in lignes if l.startswith("ETAT cadre="))
cadre_hex = etat.split("cadre=")[1]
octet3 = int(cadre_hex[(568 + 3) * 2:(568 + 3) * 2 + 2], 16)
controle("V5:l-octet-mute-l-etat-lu-diverge",
         ok_lecture and octet3 == 0xFF and donnees384[3] != 0xFF,
         f"la lecture d'abord VERT (le tampon == le témoin), l'octet 3 muté "
         f"{donnees384[3]:#04x} → {octet3:#04x} : l'état lu DIVERGE du "
         f"modèle — la falsification est DÉTECTABLE")

print(f"\nLE JUGE : {VERTS} VERT, {ROUGES} ROUGE "
      f"{'— VERT' if ROUGES == 0 else '— ROUGE'}")
sys.exit(0 if ROUGES == 0 else 1)
