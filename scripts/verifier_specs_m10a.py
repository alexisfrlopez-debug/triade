#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_specs_m10a.py — LA PREUVE SUR PIÈCES DU CHANTIER M10-(a) COMPLET :
les 18 spécifications présentes et conformes au gabarit § 2.2 (les SEPT
blocs, révision 1, provenance écrite-avant-code), CHAQUE exigence Qn/En
reliée à au moins un vecteur (la règle du protocole : une exigence
invérifiable est une exigence mal formulée), les verdicts cités vivant
dans la table, les renvois internes et l'héritage VALIDES (chaque entrée
citée existe, chaque entrée déclarée est citée), les constantes du plan
d'adressage RE-DÉRIVÉES PAR ARITHMÉTIQUE au geste même (les 64 constantes
MD5_T par sinus, le format de ligne recomposé, le cadre et les zones
recomptés, vue_max/recadre rejouées contre la référence). Échec nommé sur
toute divergence.

Usage : python3 scripts/verifier_specs_m10a.py
Code de sortie : 0 = 18/18 + constantes VERTES ; 2 = refus nommé."""

import importlib.util
import math
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
DOMAINE = REPO / "loupe" / "I"
LAYOUT = REPO / "loupe" / "layout.py"

# La table des 18 (le README fait foi — les identifiants machine i11xxxx
# sont DÉCIMAUX, la suite de la lignée : g9 [M8] → h10 [M9] → i11 [M10])
ATTENDUS = {
    1: "loupe-01-ouvrir.md",
    2: "loupe-02-lire.md",
    3: "loupe-03-fermer.md",
    4: "loupe-04-cadre.md",
    5: "loupe-05-sha256.md",
    6: "loupe-06-md5.md",
    7: "loupe-07-cumul.md",
    8: "loupe-08-ligne.md",
    9: "loupe-09-ecran.md",
    10: "loupe-10-peinture.md",
    11: "loupe-11-defilement.md",
    12: "loupe-12-aller.md",
    13: "loupe-13-recherche.md",
    14: "loupe-14-suivant.md",
    15: "loupe-15-curseur.md",
    16: "loupe-16-saisie.md",
    17: "loupe-17-sauver.md",
    18: "loupe-18-quitter.md",
}
IDENTIFIANTS = {i: 110000 + i for i in ATTENDUS}   # i110001..i110018

# Les blocs SANS entrée IAT propre (la charte § 9 — le miroir tls13 § 7)
BLOCS_PURS = {4, 7, 8, 13}

# Les familles du README (la découpe fondatrice, D171)
FAMILLES = {i: "fichier" for i in (1, 2, 3, 4)}
FAMILLES.update({i: "empreintes" for i in (5, 6, 7)})
FAMILLES.update({i: "rendu" for i in (8, 9, 10, 11)})
FAMILLES.update({i: "navigation" for i in (12, 13, 14)})
FAMILLES.update({i: "édition" for i in (15, 16, 17, 18)})

echecs = []
controles = [0]


def controle(nom, ok, detail=""):
    controles[0] += 1
    print(f"[m10a] {'PASS' if ok else 'ÉCHEC'} : {nom}"
          + (f" ({detail})" if detail else ""))
    if not ok:
        echecs.append(nom)


def section(texte, debut, fin):
    """Extrait le texte entre deux marques de section ('pre  :' .. 'inv :')."""
    i = texte.find(debut)
    j = texte.find(fin, i) if fin else len(texte)
    return texte[i:j] if i >= 0 else ""


def clauses(texte, lettre):
    """Les numéros de clauses Pn/Qn/In/En cités comme étiquettes."""
    motif = re.compile(r"\b" + lettre + r"(\d+)\b")
    return {int(m) for m in motif.findall(texte)}


def couvertures(texte_vecteurs):
    """Les clauses couvertes : 'couvre Q1, Q3-E5, E1-E3' → l'ensemble.
    La liste vit jusqu'à la parenthèse fermante (les retours à la ligne
    sont traversés, le texte autour des clauses est ignoré)."""
    trouves = set()
    for m in re.finditer(r"couvre\s+([^)]*)", texte_vecteurs):
        liste = m.group(1).replace("–", "-")
        for am in re.finditer(r"\b([PQIE])(\d{1,2})(?:\s*-\s*\1(\d{1,2}))?\b",
                              liste):
            lettre, n1, n2 = am.group(1), int(am.group(2)), am.group(3)
            if n2:
                trouves |= {(lettre, k) for k in range(n1, int(n2) + 1)}
            else:
                trouves.add((lettre, n1))
    return trouves


# --- (1) les 18 fichiers : la tête, les SEPT blocs, la provenance ---------------
textes = {}
for num, nom in sorted(ATTENDUS.items()):
    chemin = DOMAINE / nom
    if not chemin.exists():
        controle(f"loupe-{num:02d} présent ({nom})", False)
        continue
    texte = chemin.read_text(encoding="utf-8")
    textes[num] = texte
    tete = texte.splitlines()[0]
    ok_tete = (tete.startswith(f"loupe-{num:02d} ·")
               and "· révision 1" in tete)
    sections = ["Intention :", "Contrat :", "pre  :", "post :", "inv  :",
                "Échecs :", "Vecteurs :"]
    ok_sections = all(s in texte for s in sections)
    ok_suite = all(re.search(r"^" + re.escape(s), texte, re.M)
                   for s in ("Fixtures", "Provenance", "Décisions"))
    ok_prov = "Provenance  : écrite-avant-code" in texte
    controle(f"loupe-{num:02d} ({nom}) : la tête + les SEPT blocs + la "
             "provenance", ok_tete and ok_sections and ok_suite and ok_prov,
             tete[:55])

# --- (2) la pureté déclarée : les blocs sans IAT le disent, les autres aussi ----
for num in sorted(textes):
    if num in BLOCS_PURS:
        ok = "AUCUNE entrée IAT" in textes[num]
        controle(f"loupe-{num:02d} : la feuille SANS IAT le déclare "
                 "(charte § 9)", ok)
    else:
        ok = ("IAT" in textes[num]) and ("fermée" in textes[num]
                                         or "déclarée" in textes[num])
        controle(f"loupe-{num:02d} : l'IAT déclarée au plan (D161)", ok)

# --- (3) la COUVERTURE : chaque Qn et En relie au moins un vecteur --------------
for num, texte in sorted(textes.items()):
    post = section(texte, "post :", "inv  :")
    ech = section(texte, "Échecs :", "Vecteurs :")
    vec = section(texte, "Vecteurs :", "Fixtures")
    qs = clauses(post, "Q")
    es_nuls = set()
    for m in re.finditer(r"\bE(\d+)\s*:\s*([^\n]*)", ech):
        if "AUCUN" in m.group(2)[:60]:
            es_nuls.add(int(m.group(1)))   # l'absence nommée d'échec
    es = clauses(ech, "E") - es_nuls
    couv = couvertures(vec)
    manq_q = {f"Q{n}" for n in sorted(qs) if ("Q", n) not in couv}
    manq_e = {f"E{n}" for n in sorted(es) if ("E", n) not in couv}
    controle(f"loupe-{num:02d} : chaque exigence relie un vecteur",
             not manq_q and not manq_e,
             f"{len(qs)} Q · {len(es)} E utiles"
             + (f" · SANS VECTEUR : {sorted(manq_q | manq_e)}"
                if (manq_q or manq_e) else ""))

# --- (4) les verdicts cités vivent dans la table (le plan d'adressage) ----------
spec_mod = importlib.util.spec_from_file_location("layout_loupe", LAYOUT)
lay = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(lay)
table_verdicts = set(lay.VERDICTS)
controle("la table des SEPT verdicts (0, −1..−7)",
         table_verdicts == {0} | set(range(-7, 0)),
         " · ".join(f"{k} {v.split(' ')[0]}" for k, v in
                    sorted(lay.VERDICTS.items())))
for num, texte in sorted(textes.items()):
    cites = {int(v) for v in re.findall(r"verdict\s+(-\d+)", texte)}
    cites |= {int(v) for v in re.findall(r"rax\s*=\s*(-\d+)", texte)}
    cites |= {int(v) for v in re.findall(r"→\s*(-\d+)", texte)}
    hors = cites - table_verdicts
    controle(f"loupe-{num:02d} : les verdicts cités vivent dans la table",
             not hors, f"cités : {sorted(cites) if cites else 'aucun'}"
             + (f" · HORS TABLE : {sorted(hors)}" if hors else ""))

# --- (5) les renvois : chaque loupe-NN/tls13-NN/libc-NN/win-NN cité existe ------
tous_textes = "\n".join(textes.values())
readme = (DOMAINE / "README.md").read_text(encoding="utf-8")
corpus = tous_textes + readme
for dom, dossier in (("loupe", DOMAINE), ("tls13", REPO / "tls13" / "I"),
                     ("libc", REPO / "m1" / "I"),
                     ("win", REPO / "demo" / "I")):
    cites = sorted({int(m) for m in re.findall(rf"\b{dom}-(\d{{2}})\b", corpus)})
    absents = [f"{dom}-{n:02d}" for n in cites
               if not any(p.name.startswith(f"{dom}-{n:02d}-")
                          for p in dossier.glob("*.md"))]
    controle(f"les renvois {dom}-NN cités existent",
             not absents, f"{len(cites)} citations distinctes"
             + (f" · ABSENTS : {absents}" if absents else ""))

# l'héritage DÉCLARÉ est l'héritage UTILISÉ (chaque entrée citée par les specs)
heritage = set(lay.HERITAGE_SHA) | set(lay.HERITAGE_LIBC) | set(lay.HERITAGE_WIN03)
for bloc in sorted(heritage):
    dom, num = bloc.split("-")
    cite = re.search(rf"\b{dom}-{num}\b", tous_textes) is not None
    controle(f"l'héritage {bloc} est cité par les specs (utilisé)", cite)
controle("aucun autre héritage cité (la liste est fermée)",
         not ({f"tls13-{n:02d}" for n in range(1, 29)}
              & (set(re.findall(r"tls13-\d{2}", tous_textes))
                 - set(lay.HERITAGE_SHA))))

# le réseau des renvois structurants (les invariants croisés du domaine)
reseau = [
    (14, "loupe-12"), (15, "loupe-12"),      # la règle de recadrage citée
    (10, "loupe-08"), (14, "loupe-13"),      # la composition par la carte
    (2, "loupe-16"), (3, "loupe-16"),        # le recouvrement + l'hygiène
    (16, "loupe-18"), (17, "loupe-18"),      # la garde refus_quitter
    (18, "loupe-03"), (9, "win-03"),         # la clôture + la boucle héritée
    (7, "loupe-05"), (7, "loupe-06"),        # le panneau composé
    (1, "loupe-07"), (17, "loupe-07"),       # le panneau né et re-né
]
for num, cible in reseau:
    controle(f"loupe-{num:02d} cite {cible} (le renvoi structurant)",
             cible in textes.get(num, ""))
for num in (16, 17, 18):
    controle(f"loupe-{num:02d} porte la garde refus_quitter",
             "refus_quitter" in textes.get(num, ""))

# --- (6) le README : la table i11xxxx + le chantier (a) COMPLET -----------------
for num in ATTENDUS:
    controle(f"la table porte loupe-{num:02d} → i{IDENTIFIANTS[num]}",
             f"| loupe-{num:02d} | i{IDENTIFIANTS[num]} |" in readme)
controle("la table porte la famille de chaque bloc",
         all(f"| {FAMILLES[num]} |" in readme for num in ATTENDUS))
controle("le README dit le chantier (a) COMPLET",
         "Le chantier (a) est COMPLET : les 18" in readme)
controle("le README porte la charte ABI (§ 9 : la table des verdicts)",
         "L'ABI et la table des verdicts" in readme
         and "MONTE À LA BARRE" in readme)
controle("le README porte la lignée des identifiants (g9 → h10 → i11)",
         "g9 [M8] → h10 [M9] → i11 [M10]" in readme)

# --- (7) le plan d'adressage : les constantes RE-DÉRIVÉES au geste même ---------
controle("MD5_ABSCISSE == RFC 1321 § 3.3",
         lay.MD5_ABSCISSE == (0x67452301, 0xEFCDAB89, 0x98BADCFE,
                              0x10325476))
controle("MD5_S == les 64 décalages (quatre tours × quatre, répétés)",
         lay.MD5_S == (7, 12, 17, 22) * 4 + (5, 9, 14, 20) * 4
         + (4, 11, 16, 23) * 4 + (6, 10, 15, 21) * 4
         and len(lay.MD5_S) == 64)
T_ref = tuple(int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF
              for i in range(64))
controle("MD5_T : les 64 constantes RE-DÉRIVÉES (floor(2^32·|sin(i+1)|))",
         tuple(lay.MD5_T) == T_ref,
         f"T[0] {lay.MD5_T[0]:08X} · T[63] {lay.MD5_T[63]:08X} — "
         "T[0]=D76AA478, T[63]=EB86D391 (RFC 1321 recoupé)")
controle("MD5_CTX == 16 + 8 + 64 == 88 (ABCD · longueur · tampon)",
         lay.MD5_CTX == 88 and lay.MD5_CONDENSE == 16
         and lay.MD5_TAILLE_BLOC == 64)
controle("LIGNE_TAILLE == 8 + 2 + 48 + 2 + 16 + 1 == 77 (le format recomposé)",
         lay.LIGNE_TAILLE == 8 + 2 + (16 * 2 + 15 + 1) + 2 + 16 + 1 == 77)
controle("TAMPON_SESSION == GRILLE_LIGNES × LIGNE_OCTETS == 384",
         lay.TAMPON_SESSION == lay.GRILLE_LIGNES * lay.LIGNE_OCTETS == 384
         and lay.GRILLE_LIGNES == 24 and lay.LIGNE_OCTETS == 16)
controle("PAGE_LIGNES == GRILLE_LIGNES − 2 == 22 ; la molette TROIS lignes",
         lay.PAGE_LIGNES == 22 and lay.DEFILEMENT_LIGNES == 3)
controle("CUMUL_FENETRE == 64 Kio, multiple du bloc 64 (sha ET md5)",
         lay.CUMUL_FENETRE == 65536 and lay.CUMUL_FENETRE % 64 == 0)
controle("BORNE_TAILLE == 2 Gio : le dernier décalage tient en 8 chiffres",
         lay.BORNE_TAILLE == 1 << 31
         and len(hex(lay.BORNE_TAILLE - 1)) - 2 == 8)
controle("VERSION_DEV == 0.1.0-dev.1 == 0x00010001 (le miroir 0xJJNNPPDD)",
         lay.VERSION_DEV == 0x00010001 and lay.VERSION_FINALE == 0x00010000)
controle("le cadre : 520 + 8×4 + 4×4 + 384 == 952, la zone 960 alignée 16",
         lay.CADRE_CHEMIN == 520 and lay.CADRE_OCTETS == 952
         and lay.CADRE_TOTAL == 960 and lay.CADRE_TOTAL % 16 == 0)
attendu_cadre = 260 * 2 + 8 + 8 + 8 + 8 + 4 + 4 + 4 + 4 + lay.TAMPON_SESSION
controle("la disposition du cadre recomptée champ à champ",
         attendu_cadre == 952 and lay.CADRE_TAMPON == lay.TAMPON_SESSION)
controle("ZONE_ECRAN == 80 + 24×80 + 2×160 == 2320, alignée 16",
         lay.ZONE_ECRAN == 80 + 24 * 80 + 2 * 160 == 2320
         and lay.ZONE_ECRAN % 16 == 0)
controle("ZONE_JOURNAL == 256×16 + 16 == 4112, alignée 16",
         lay.ZONE_JOURNAL == 256 * 16 + 16 == 4112
         and lay.ZONE_JOURNAL % 16 == 0 and lay.EDITS_MAX == 256)
controle("ZONE_SAISIE 96 · ZONE_MOTIF 48 · ZONE_EMPREINTES 48 == 16+32",
         lay.ZONE_SAISIE == 96 and lay.ZONE_MOTIF == 48
         and lay.ZONE_EMPREINTES == 48 and lay.MOTIF_MAX == 32)
controle("ZONE_CUMUL == CUMUL_FENETRE (la fenêtre de lecture partagée)",
         lay.ZONE_CUMUL == lay.CUMUL_FENETRE)

# vue_max : la règle RE-JOUÉE contre la référence (la dernière fenêtre
# VOIT le dernier octet ; les petits fichiers ne défilent pas)
def vue_max_ref(taille, tampon=384):
    if taille <= tampon:
        return 0
    reste = taille - tampon
    return (reste + 15) & ~15


cas_tailles = [0, 1, 15, 16, 17, 100, 383, 384, 385, 400, 1000, 4096,
               65536, 65537, 196609, 2 ** 20, 2 ** 31 - 1, 2 ** 31]
ecarts = [t for t in cas_tailles if lay.vue_max(t) != vue_max_ref(t)]
controle("vue_max : la règle de loupe-11 re-jouée sur "
         f"{len(cas_tailles)} tailles",
         not ecarts,
         "; ".join(f"{t} → {lay.vue_max(t)}" for t in cas_tailles[:4])
         + (f" · DIVERGENTS : {ecarts}" if ecarts else ""))
controle("vue_max : la dernière fenêtre VOIT le dernier octet",
         all(lay.vue_max(t) + 384 >= t for t in cas_tailles if t > 0))
controle("vue_max : tout multiple de 16 (l'alignement de grille)",
         all(lay.vue_max(t) % 16 == 0 for t in cas_tailles))

# recadre : la règle RE-JOUÉE (la ligne active à la 12e ligne, le bord sinon)
cas_curseurs = [0, 1, 15, 16, 17, 176, 177, 1000, 0x7FFFFFFF]
ecarts_r = [c for c in cas_curseurs
            if lay.recadre(c) != (max(0, c - 176) & ~15)]
controle("recadre : la règle de loupe-12 Q3 re-jouée (11 lignes au-dessus,"
         " alignée 16)", not ecarts_r,
         f"recadre(0x7FFFFFFF) = {lay.recadre(0x7FFFFFFF):X}"
         + (f" · DIVERGENTS : {ecarts_r}" if ecarts_r else ""))

# l'IAT : le budget NOMMÉ, les feuilles de win-03 (héritée) présentes
controle("l'IAT : 34 feuilles NOMMÉES (kernel32 10 · user32 18 · gdi32 6)",
         len(lay.IAT_KERNEL32) == 10 and len(lay.IAT_USER32) == 18
         and len(lay.IAT_GDI32) == 6)
controle("les TROIS feuilles de win-03 (héritée) vivent dans user32",
         {"GetMessageW", "TranslateMessage", "DispatchMessageW"}
         <= set(lay.IAT_USER32))
controle("WriteFile vit dans l'IAT (loupe-17 seul l'appelle)",
         "WriteFile" in lay.IAT_KERNEL32)
controle("l'anti-doublon : aucune feuille IAT répétée",
         len(set(lay.IAT_KERNEL32) | set(lay.IAT_USER32)
             | set(lay.IAT_GDI32)) == 34)

# --- (8) les décisions citées par les specs existent au registre ----------------
decisions_reg = REPO / "docs" / "DECISIONS.md"
reg = decisions_reg.read_text(encoding="utf-8")
# le registre porte TROIS étages de format au fil des ères : « ## D134 — »
# (les grandes décisions), « ### D35 — » (les décisions d'ère),
# « **D7 — » (les décisions fondatrices) — les trois sont le registre
d_registrees = {int(m) for m in re.findall(r"^#{0,4}\s*\**D(\d{1,3})\s*[—-]", reg, re.M)}
d_citees = {int(m) for m in re.findall(r"\bD(\d{1,3})\b", tous_textes)}
absentes = sorted(d_citees - d_registrees)
controle("les décisions citées par les specs vivent au registre"
         " (les trois étages de format)",
         not absentes,
         f"citées : {sorted(d_citees)} · {len(d_registrees)} au registre"
         + (f" · ABSENTES : {absentes}" if absentes else ""))

# --- le verdict ----------------------------------------------------------------
print()
if echecs:
    print(f"VERDICT : ROUGE — {len(echecs)} échec(s) nommé(s) : {echecs}")
    sys.exit(2)
print(f"VERDICT : VERT — {controles[0]} contrôles : les 18 spécifications "
      "sont posées (les SEPT blocs du gabarit, chaque exigence reliée à son "
      "vecteur, les verdicts dans la table, les renvois et l'héritage "
      "validés) ; les constantes du plan sont RE-DÉRIVÉES par arithmétique "
      "au geste même (les 64 constantes MD5 par sinus, le format de ligne "
      "recomposé, le cadre et les zones recomptés, vue_max/recadre "
      "re-jouées) ; le chantier M10-(a) est COMPLET sur pièces.")
sys.exit(0)
