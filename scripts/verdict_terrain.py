#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRIADE — Verdict automatique d'un journal de run terrain (terrain_*.txt).

Juge un journal contre les prédictions PRÉ-ENREGISTRÉES de chaque itération
(D58 pour terrain.8, D60 pour terrain.9) et classifie le point de mort.
Les prédictions vivent ICI, dans le dépôt : leur antériorité est celle du
commit qui les porte (instrument de pré-enregistrement, falsifiable).

Morphologies connues (apprises de l'archive 16:27 → 20:01) :
  PORTE_KO_ARRET     S02B + S91 : la porte R10 a refusé l'image (fail-closed,
                     arrêt PROPRE — un verdict, pas un crash).
  MORT_EXTRACTION    dernier S = S03 : mort au 1er appel kernel32#3 (classe
                     D53, corrigée par terrain.5).
  MORT_S12_SONDAGE   dernier S = S12A : le fil meurt pendant le sondage 30 s
                     du journal demo (fermeture manuelle / kill externe).
  MORT_S21_CURL      dernier S = S21A + bannière echo : mort au 1er curl T2
                     — la signature du kill externe (Defender, D59/D60).
  RUN_COMPLET        S90/S91 atteint APRÈS T2 (S20+ vus) : run intégral.

Usage :
  python3 scripts/verdict_terrain.py [JOURNAL]    défaut : plus récent de upload/
  python3 scripts/verdict_terrain.py --tous       toute l'archive + récurrences
Code de sortie : 0 = lu, 2 = erreur.
"""

import pathlib
import re
import sys

UPLOAD = pathlib.Path("/home/z/my-project/upload")

# ------------------------------------------------------------ pré-enregistrements

PREDICTIONS = {
    # Entrée 47 (D58) — relance terrain.8 à binaire inchangé.
    "terrain.8": {
        "objet": "relance à binaire inchangé — prouver que T2/T3/dépôt courent",
        "attendues": [
            ("S13", "S13 T1 demo.exe termine code=0", "exacte"),
            ("S14", "S14 T1 lignes journal demo=26", "exacte"),
            ("S15", "S15 T1 verdict journal : NON conforme", "exacte"),
            ("S16", "S16 T1 VERDICT KO", "exacte"),
            ("S91", "S91 SUPERVISEUR : ECHEC (voir lignes KO)", "exacte"),
        ],
        "note": "S15/S16 NON CONFORMES attendus : divergence de contrat "
                "documentée (journal demo.10 de 706 o > lecture plafonnée "
                "à 640 o — 26 lignes + fragment « re », pas 17).",
    },
    # Entrée 49 (D60) — terrain.9, variable unique = coupure temps réel 3 min.
    "terrain.9": {
        "objet": "coupure temps réel = variable unique (MÊME binaire que terrain.8)",
        "branche_A": [  # si le run survit (Defender prouvé par différence unique)
            ("S13", "S13 T1 demo.exe termine code=0", "exacte"),
            ("S14", "S14 T1 lignes journal demo=26", "exacte"),
            ("S15", "S15 T1 verdict journal : NON conforme", "exacte"),
            ("S16", "S16 T1 VERDICT KO", "exacte"),
            ("S22", "S22 T2 curl http : code=0", "exacte"),
            ("S23", "S23 T2 page http octets=", "prefixe>0"),
            ("S24", "S24 T2 curl https : code=0", "exacte"),
            ("S25", "S25 T2 page https octets=", "prefixe>0"),
            ("S26", "S26 T2 journal proxy lignes=7", "exacte"),
            ("S27", "S27 T2 verdict console : conforme", "exacte"),
            ("S28", "S28 T2 VERDICT OK", "exacte"),
            ("S30", "S30 T3 envoi Drive : lecture jetons", "exacte"),
            ("S32", "S32 T3 requete OAuth composee", "exacte"),
            ("S33", "S33 T3 jeton OAuth obtenu", "exacte"),
            ("S34", "S34 T3 session upload ouverte", "exacte"),
            ("S35", "S35 T3 journal televerse : OK", "exacte"),
            ("S36", "S36 T3 VERDICT OK", "exacte"),
            ("S91", "S91 SUPERVISEUR : ECHEC (voir lignes KO)", "exacte"),
        ],
        "branche_B": "mort encore à S21/bannière MALGRÉ la coupure posée : "
                     "Defender réfuté comme tueur → terrain.10 immédiat "
                     "(bissection .curl, exclusions processus, T3 anticipé).",
        "note": "mesure de succès UNIQUE : un terrain_*.txt déposé TOUT SEUL "
                "dans le dossier test (jamais encore réussi). S91 ÉCHEC "
                "attendu même en pleine réussite (T1 KO documenté 26≠17).",
    },
}

MORPHOLOGIES = [
    ("PORTE_KO_ARRET", ["S02B", "S91"]),
    ("MORT_EXTRACTION", ["S03"]),
    ("MORT_S12_SONDAGE", ["S12A"]),
    ("MORT_S21_CURL", ["S21A"]),
    ("RUN_COMPLET", ["S90", "S91"]),
]

BANNIERE_PROXY = "TRIADE M3 : proxy demarre (port 25000)"
DERNIERE_LIGNE_DEMO = "boucle § 5 complète - DÉMO OK"


# ---------------------------------------------------------------- analyse

def lire(chemin):
    """Lit un journal terrain (UTF-8, repli cp1252, CRLF tolérés) -> lignes."""
    brut = chemin.read_bytes()
    try:
        txt = brut.decode("utf-8")
    except UnicodeDecodeError:
        txt = brut.decode("cp1252", errors="replace")
    return [l.rstrip("\r\n") for l in txt.split("\n") if l.strip()]


def classifier(lignes):
    """Classe un journal : (morphologie, codes S, lignes S, bannière, L4C post).

    Le compteur L4C/L4D post-S ne regarde QUE les lignes placées après le
    DERNIER S du fichier (deux passes) — les L4C/L4D du journal demo
    EMBARQUÉ (entre S14 et S15) sont le démarrage normal du demo, pas une
    interaction humaine post-mortem.
    """
    s_vus = []          # codes S dans l'ordre : (numéro, ligne complète)
    banniere = False
    idx_s = []          # index des lignes S
    for i, l in enumerate(lignes):
        m = re.match(r"^S(\d\d)", l)
        if m:
            s_vus.append((m.group(1), l))
            idx_s.append(i)
        elif l.startswith(BANNIERE_PROXY):
            banniere = True
    codes = [c for c, _ in s_vus]
    dernier = codes[-1] if codes else None
    fin_s = idx_s[-1] if idx_s else -1
    l4c_apres = sum(1 for i, l in enumerate(lignes)
                    if i > fin_s and re.match(r"^L4[CD]", l))
    t2_vu = any(c in ("20", "21", "22", "23", "24", "25", "26", "27", "28")
                for c in codes)
    porte_ko = any(l.startswith("S02 porte R10 : KO") for _, l in s_vus)

    if porte_ko and dernier in ("90", "91"):
        morpho = "PORTE_KO_ARRET"        # fail-closed propre (terrain.6, 17:43)
    elif dernier == "03":
        morpho = "MORT_EXTRACTION"       # 1er appel kernel32#3 (classe D53)
    elif dernier == "12":
        morpho = "MORT_S12_SONDAGE"      # pendant le sondage 30 s du journal demo
    elif dernier == "21" and banniere:
        morpho = "MORT_S21_CURL"         # kill externe au 1er curl (D59/D60)
    elif dernier in ("90", "91") and t2_vu:
        morpho = "RUN_COMPLET"
    else:
        morpho = f"MORT_INCONNUE_S{dernier}"
    return morpho, codes, s_vus, banniere, l4c_apres


def verifier_predictions(version, s_vus):
    """Compare les lignes S vues aux prédictions enregistrées — par version."""
    pred = PREDICTIONS.get(version)
    if not pred:
        return None
    presentes = {l for _, l in s_vus}
    attendues = pred.get("branche_A") or pred.get("attendues")
    resultats = []
    for code, texte, mode in attendues:
        if mode == "prefixe>0":
            ok = any(l.startswith(texte) and not l.endswith("=0")
                     for l in presentes)
        else:
            ok = texte in presentes
        resultats.append((code, texte, ok))
    return resultats


def juger(chemin, verbeux=True):
    lignes = lire(chemin)
    morpho, codes, s_vus, banniere, l4c = classifier(lignes)
    version = "?"
    m = re.search(r"0\.5\.0-(terrain\.\d+)", lignes[0] if lignes else "")
    if m:
        version = m.group(1)
    if version == "?" and len(lignes) > 6:
        m = re.search(r"0\.5\.0-(terrain\.\d+)", lignes[6])
        version = m.group(1) if m else "?"
    date = ""
    for l in lignes:
        if l.startswith("S01 date "):
            date = l[len("S01 date "):]
            break

    print(f"\n=== {chemin.name} ===")
    print(f"  version binaire : {version}   run : {date}")
    print(f"  lignes S vues   : {len(s_vus)} (dernier : S{codes[-1] if codes else '?'})")
    print(f"  MORPHOLOGIE     : {morpho}")
    if banniere:
        print("  bannière proxy  : reçue (embed)")
    if l4c:
        print(f"  L4C/L4D post-S  : {l4c} (fenêtre déplacée après la mort — "
              "interaction humaine pendant le silence")
    if morpho == "MORT_S21_CURL":
        print("  → mort au 1er curl T2 : la signature du kill externe (D59/D60)")

    # prédictions
    res = verifier_predictions(version, s_vus)
    if res:
        objet = PREDICTIONS[version].get("objet", "")
        print(f"  prédictions {version} ({objet}) :")
        for code, texte, ok in res:
            etat = "VÉRIFIÉE" if ok else "absente"
            print(f"    [{etat:>9}] {texte[:66]}")
        note = PREDICTIONS[version].get("note")
        if note:
            print(f"  note : {note}")
        if version == "terrain.9" and morpho == "MORT_S21_CURL":
            b = PREDICTIONS[version]["branche_B"]
            print(f"  branche B (si coupure posée et mort quand même) : {b[:74]}…")
    if version == "terrain.3":
        print("  avertissement   : terrain.4/5 se déclaraient « terrain.3 » "
              "(version non bumpée avant D55) — dater par S01, pas par la version")

    # demo journal embarqué (après S14)
    apres_s14 = False
    demo, fragment = [], None
    for l in lignes:
        if l.startswith("S14 "):
            apres_s14 = True
            continue
        if apres_s14:
            if re.match(r"^S\d\d", l):
                fragment = demo[-1] if demo else None
                demo = demo[:-1] if demo else []
                break
            demo.append(l)
    if demo:
        print(f"  journal demo embarqué : {len(demo)} ligne(s) recopiée(s)"
              + (f" + fragment « {fragment} »" if fragment else ""))

    # reponse.txt (le bit oui/non posé par le développeur, D60)
    rep = UPLOAD / "reponse.txt"
    if rep.exists() and verbeux:
        print("  reponse.txt     : " + " / ".join(
            l.strip() for l in rep.read_text(errors="replace").splitlines()
            if l.strip()))
    return morpho, version


def demo_journal_independant():
    """Contrôle du demo_journal.txt déposé à la main (s'il est présent)."""
    p = UPLOAD / "demo_journal.txt"
    if not p.exists():
        return
    lignes = lire(p)
    fin = lignes[-1] if lignes else ""
    ok_fin = fin == DERNIERE_LIGNE_DEMO
    # L4C/L4D APRÈS la ligne DÉMO OK = interaction après la fin (à discriminer
    # des L4C/L4D de démarrage, normaux — leçon de la rétro-validation D61)
    idx_fin = next((i for i, l in enumerate(lignes) if l == DERNIERE_LIGNE_DEMO), -1)
    post = sum(1 for l in lignes[idx_fin + 1:] if re.match(r"^L4[CD]", l)) \
        if idx_fin >= 0 else -1
    print(f"\n=== demo_journal.txt (dépôt manuel) ===")
    print(f"  {len(lignes)} lignes ; dernière ligne "
          f"{'== ' + DERNIERE_LIGNE_DEMO + ' (DÉMO OK complet)' if ok_fin else 'INATTENDUE : ' + fin[:50]!r}")
    if post == 0:
        print("  L4C/L4D post-DÉMO OK : 0 (aucune — protocole respecté)")
    elif post > 0:
        print(f"  L4C/L4D post-DÉMO OK : {post} (fenêtre déplacée après la fin)")
    else:
        print("  ligne DÉMO OK introuvable — journal incomplet ?")


def main():
    args = sys.argv[1:]
    tous = "--tous" in args
    cibles = [a for a in args if not a.startswith("--")]
    if tous:
        journaux = sorted(UPLOAD.glob("terrain_2026*.txt"))
    else:
        if cibles:
            journaux = [pathlib.Path(cibles[0])]
        else:
            js = sorted(UPLOAD.glob("terrain_2026*.txt"))
            if not js:
                print("aucun journal terrain dans upload/", file=sys.stderr)
                return 2
            journaux = [js[-1]]
    print("TRIADE — VERDICT TERRAIN "
          f"({len(journaux)} journal/journaux, source : prédictions D58/D60 pré-enregistrées)")
    morphos = []
    for j in journaux:
        morphos.append(juger(j, verbeux=not tous))
    if tous:
        from collections import Counter
        compteur = Counter(m for m, _ in morphos)
        print("\n=== RÉCURRENCES (archive complète) ===")
        for m, n in compteur.most_common():
            print(f"  {n} × {m}")
        curl = compteur.get("MORT_S21_CURL", 0)
        if curl >= 2:
            print(f"  → {curl} morts au MÊME point (1er curl T2) : "
                  "kill externe répétable, signature Defender (D59)")
    demo_journal_independant()
    return 0


if __name__ == "__main__":
    sys.exit(main())
