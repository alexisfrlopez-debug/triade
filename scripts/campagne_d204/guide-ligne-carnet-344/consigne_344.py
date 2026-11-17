#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigne_344.py — LA CONSIGNATION de l'Entrée 344 (Task 211) : LE GUIDE
DE LA LIGNE DE CARNET ET DE LA SUITE NÉ ET LIVRÉ (la commande du
développeur : « fais un guide pour la ligne de carnet puis la suite ») —
la sonde de l'atelier du terrain (les QUATRE registres rapatriés
byte-byte : AUCUNE ligne D210 ne vit au livre, les DEUX runs recoupés
[Entrées 340/343] attendent le geste), la référence-après-geste (le § 5
du guide : livraisons.csv 2 328 o, sha256 8bae18e8…), le GUIDE-LIGNE-
CARNET-ET-SUITE-20261118.txt à la racine du /test (md5 324f1a77… recoupé
byte-byte) + la copie à download/, la Task 211 au worklog (idempotent),
la carte OU-TROUVER portée à 344 (la chaîne 343 conservée), le commit git
(le push et le miroir suivent, aux jetons du /Tokens)."""
import pathlib
import shutil
import subprocess

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
DL = pathlib.Path("/home/z/my-project/download")
SBOX = pathlib.Path("/home/z/my-project/scripts")
BAC = REPO / "scripts" / "campagne_d204" / "guide-ligne-carnet-344"

COPIES = [
    (SBOX / "sonde_atelier_344.py", BAC / "sonde_atelier_344.py"),
    (SBOX / "livrer_guide_344.py", BAC / "livrer_guide_344.py"),
    (SBOX / "consigne_344.py", BAC / "consigne_344.py"),
    (SBOX / "sonde_atelier_344.py", REPO / "scripts" / "sonde_atelier_344.py"),
    (SBOX / "livrer_guide_344.py", REPO / "scripts" / "livrer_guide_344.py"),
    (SBOX / "consigne_344.py", REPO / "scripts" / "consigne_344.py"),
]

WORKLOG = """

Task ID: 211
Agent: Z.ai (agent principal — la session du guide de la ligne de carnet)
Task: LA COMMANDE DU DÉVELOPPEUR (« fais un guide pour la ligne de carnet puis la suite ») : LE GUIDE-LIGNE-CARNET-ET-SUITE-20261118.txt NÉ ET LIVRÉ à la racine du coffre /test (19 459 o, md5 324f1a77… recoupé byte-byte) — le mode d'emploi du geste des lignes que le livre attend des DEUX runs D210 recoupés (les Entrées 340 et 343), puis la carte de la suite de la campagne.

Work Log:
- LA SONDE DE L'ATELIER (sonde_atelier_344.py, TOUT VERT) : les QUATRE
  registres de /test/atelier-campagne-d204-20261114-013520/ RAPATRIÉS au
  bac guide-ligne-carnet-344/epreuves/ par DOUBLE téléchargement byte-byte
  (md5 == la métadonnée Drive) : livraisons.csv 2 176 o [sha256 3678e37f…,
  22 lignes de campagne, la dernière C-app-it3 du 16/11 — l'état du
  guide-313 DEMEURE], carnet_temps_humain.csv 1 869 o [sha256 ef988fd5…,
  la dernière ligne tag-backup du 16/11], defauts.csv 3 870 o [sha256
  1bed8908…, le LF final posé], journal-ouverture.txt 648 o — LE CONSTAT :
  AUCUNE ligne D210 ne vit au livre, les DEUX runs recoupés (les Entrées
  340/343) attendent le geste du développeur (le labo ne fabrique JAMAIS
  une ligne de mesure — la frontière D99).
- LA RÉFÉRENCE-APRÈS-GESTE (le § 5 du guide, le précédent des guides
  305-313) : livraisons.csv + les DEUX lignes prescrites = 2 328 o, sha256
  8bae18e8… — les tailles et condensés attendus COMMUNIQUÉS au terrain
  (certutil) ; LE CARNET : AUCUN condensé attendu — les heures et les
  minutes appartiennent à la main du développeur (le labo ne fabrique
  JAMAIS la ligne M3) ; defauts.csv INCHANGÉ (3 870 o, 1bed8908… — le
  registre du geste ③ : rien à porter, le précédent 295).
- LE GUIDE (19 459 o, la PARTIE I le geste : ① livraisons.csv les DEUX
  lignes exactes [T-loupe-02-d210-it1 VERT 2026-11-17 ; T-loupe-08-d210-
  it1 VERT 2026-11-18 — le verdict recopié des consoles 20 VERT 0 ROUGE
  code 0 / 10 VERT 0 ROUGE code 0, citées à leurs chemins d'archives ;
  la colonne recoup « en attente » la convention des 22 lignes, jamais
  retouchée après coup ; le run v1 au juge fautif SANS ligne, le
  précédent 295] ; ② le carnet M3 le geste « run-terrain », les bornes
  ancrées aux chronologies recoupées [R7 des RECOUP-340/343, heures
  locales : 21:02:45 → 21:03:38 → 21:04:11 au 17/11 ; 00:09:11 →
  00:09:51 → 00:10:29 au 18/11], la règle de l'interruption > 5 min,
  l'option honnête D189 pour le temps du run v1 (SA ligne à lui, si
  consigné), le chrono M4 aux consoles [0,4 s / 0,6 s] jamais au carnet ;
  ③ defauts.csv RIEN [la faute au juge nommée au LABO aux 338/339,
  corrigée — les DEUX runs comptés VERTS] ; les vérifications certutil ;
  l'atelier ENTIER re-déposé + l'annonce. La PARTIE II la suite : loupe-13
  le bras T d'abord au commandement [la séquence D217, jamais re-tirée],
  la ligne au livre À CHAQUE run désormais, l'attribution empirique au
  commandement, la cadence du plan D210 [n >= 6, formats identiques,
  D202/D207, H6-H8 — H8 tenue à la deuxième : 51 %], les gestes de
  fermeture [PDF final, DOI Zenodo, grant]).
- LA LIVRAISON (livrer_guide_344.py, TOUT VERT) : le guide TÉLÉVERSÉ à la
  racine du /test (md5 324f1a77… MATCH byte-byte re-téléchargé), aux
  côtés du GUIDE-GESTE-TERRAIN-ET-SUITE et des guides du livre (la racine
  : 46 entrées) ; la copie de l'utilisateur à download/ (19 459 o).
- LA CONSIGNATION : la présente Task 211 + l'Entrée 344 ; la carte
  OU-TROUVER portée à 344 (la chaîne 343 conservée) ; le bac
  scripts/campagne_d204/guide-ligne-carnet-344/ (le guide, les epreuves/,
  la référence-apres-geste/) + les TROIS scripts du geste au bac et à
  scripts/ ; le git poussé + le miroir Drive rafraîchi (aux jetons du
  /Tokens).
- SUITE : ① LE GESTE DU DÉVELOPPEUR AU GUIDE (l'atelier téléchargé du
  /test, les DEUX lignes livraisons.csv, les DEUX lignes du carnet M3 à
  sa main [le run-terrain, les bornes des pièces], l'atelier ENTIER
  re-déposé au /test + l'annonce « les lignes du carnet dans le drive
  /test ») ; ② loupe-13 le bras T d'abord au commandement (la séquence
  tirée, jamais re-tirée — la graine D217) ; la re-livraison
  d'attribution empirique au commandement.
  (18/11/2026, la session du guide — la commande du développeur, les
  lignes attendues prescrites sur pièces, jamais de mémoire)
"""

ENTETE_344 = (
    "*Mise à jour : 18/11/2026 (Entrée 344 — LE GUIDE DE LA LIGNE DE "
    "CARNET ET DE LA SUITE NÉ ET LIVRÉ [la commande du développeur : « "
    "fais un guide pour la ligne de carnet puis la suite »] : la sonde de "
    "l'atelier du terrain [sonde_atelier_344.py, TOUT VERT — les QUATRE "
    "registres de /test/atelier-campagne-d204-20261114-013520/ rapatriés "
    "au bac scripts/campagne_d204/guide-ligne-carnet-344/epreuves/ par "
    "double téléchargement byte-byte : livraisons.csv 2 176 o, "
    "carnet_temps_humain.csv 1 869 o, defauts.csv 3 870 o, journal-"
    "ouverture.txt 648 o — AUCUNE ligne D210 ne vit au livre, les DEUX "
    "runs recoupés (Entrées 340/343) attendent le geste du développeur] ; "
    "la référence-après-geste au bac [livraisons.csv + les DEUX lignes "
    "prescrites = 2 328 o, sha256 8bae18e8… — les tailles et condensés "
    "attendus communiqués au terrain ; le carnet : AUCUN condensé — la "
    "main du développeur, la frontière D99] ; LE GUIDE-LIGNE-CARNET-ET-"
    "SUITE-20261118.txt [19 459 o, md5 324f1a77… recoupé byte-byte] à la "
    "racine du /test + la copie à download/ : PARTIE I les gestes du "
    "livre — ① livraisons.csv les DEUX lignes [T-loupe-02-d210-it1 VERT "
    "2026-11-17, T-loupe-08-d210-it1 VERT 2026-11-18, le verdict recopié "
    "des consoles, recoup « en attente » la convention, le run v1 au juge "
    "fautif SANS ligne — le précédent 295] ; ② le carnet M3 le geste "
    "« run-terrain » [les bornes des chronologies R7, la règle de "
    "l'interruption, l'option honnête D189 pour le temps du run v1, le "
    "chrono M4 aux consoles] ; ③ defauts.csv RIEN [le précédent 295 — la "
    "faute au juge nommée au LABO, jamais au defauts.csv du terrain] ; "
    "les vérifications certutil ; l'atelier ENTIER re-déposé + l'annonce ; "
    "PARTIE II la suite : loupe-13 le bras T d'abord au commandement, la "
    "ligne au livre À CHAQUE run désormais, l'attribution empirique, la "
    "cadence du plan D210, les gestes de fermeture ; "
)

MESSAGE = (
    "Entrée 344 : LE GUIDE DE LA LIGNE DE CARNET ET DE LA SUITE NÉ ET "
    "LIVRÉ (la commande du développeur : « fais un guide pour la ligne de "
    "carnet puis la suite ») : la sonde de l'atelier du terrain [les "
    "QUATRE registres de /test/atelier-campagne-d204-20261114-013520/ "
    "rapatriés byte-byte : livraisons.csv 2 176 o, carnet_temps_humain."
    "csv 1 869 o, defauts.csv 3 870 o, journal-ouverture.txt 648 o — "
    "AUCUNE ligne D210 ne vit au livre, les DEUX runs recoupés (Entrées "
    "340/343) attendent le geste du développeur] ; la référence-après-"
    "geste [livraisons.csv + les DEUX lignes prescrites = 2 328 o, "
    "sha256 8bae18e8… — le § 5 du guide, le précédent des guides 305-"
    "313 ; le carnet : AUCUN condensé — la main du développeur] ; LE "
    "GUIDE-LIGNE-CARNET-ET-SUITE-20261118.txt [19 459 o, md5 324f1a77… "
    "recoupé byte-byte] livré à la racine du /test + la copie à "
    "download/ + le bac scripts/campagne_d204/guide-ligne-carnet-344/ "
    "[le guide, les epreuves/, la référence-après-geste] : PARTIE I les "
    "gestes du livre — ① les DEUX lignes livraisons.csv [T-loupe-02-"
    "d210-it1 VERT 2026-11-17, T-loupe-08-d210-it1 VERT 2026-11-18, le "
    "verdict recopié des consoles, recoup « en attente », le run v1 au "
    "juge fautif SANS ligne] ; ② les DEUX lignes du carnet M3 [le geste "
    "run-terrain, les bornes des chronologies R7, la règle de "
    "l'interruption, l'option honnête D189, le chrono M4 aux consoles] ; "
    "③ defauts.csv RIEN [le précédent 295] ; les vérifications certutil ; "
    "l'atelier ENTIER re-déposé + l'annonce ; PARTIE II la suite : "
    "loupe-13 le bras T d'abord au commandement, la ligne au livre À "
    "CHAQUE run, l'attribution empirique, la cadence du plan D210, les "
    "gestes de fermeture ; la Task 211 au worklog, la carte OU-TROUVER "
    "portée à 344, le push GitHub + le miroir Drive suivront aux jetons "
    "du /Tokens"
)


def main():
    # 1· les copies au dépôt (idempotentes)
    for src, dst in COPIES:
        if src.is_file():
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists() and dst.read_bytes() == src.read_bytes():
                print(f"[déjà] {dst.name} — identique byte-byte")
                continue
            shutil.copyfile(src, dst)
            print(f"[copie] {dst} : {dst.stat().st_size} o")

    # 2· le worklog (append idempotent)
    wl = (REPO / "worklog.md").read_text(encoding="utf-8")
    if "Task ID: 211" in wl:
        print("[déjà] worklog.md porte Task 211 — pas de double append")
    else:
        with open(REPO / "worklog.md", "a", encoding="utf-8",
                  newline="\n") as f:
            f.write(WORKLOG)
        print("[consigné] worklog.md (Task 211, l'Entrée 344)")

    # 3· la carte OU-TROUVER (idempotent)
    carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
    texte = carte.read_text(encoding="utf-8")
    if "(Entrée 344 —" in texte:
        print("[déjà] la carte porte l'en-tête 344 — pas de double "
              "apposition")
    else:
        ancienne = "*Mise à jour : 18/11/2026 (Entrée 343 —"
        assert ancienne in texte, "l'en-tête 343 introuvable à la carte"
        texte = texte.replace(ancienne, ENTETE_344 + "Entrée 343 —", 1)
        carte.write_text(texte, encoding="utf-8", newline="\n")
        print("[portée] OU-TROUVER-LES-LIVRABLES.md : l'en-tête 344, "
              "la chaîne 343 conservée")

    # 4· le commit
    r = subprocess.run(["git", "add", "-A"], cwd=REPO,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    st = subprocess.run(["git", "status", "--short"], cwd=REPO,
                        capture_output=True, text=True)
    if not st.stdout.strip():
        print("[git] rien à committer — l'Entrée 344 fut déjà committée")
        return 0
    n = len(st.stdout.splitlines())
    r = subprocess.run(["git", "commit", "-m", MESSAGE], cwd=REPO,
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    print(f"[git] commit {n} chemins : "
          f"{r.stdout.splitlines()[0] if r.stdout else ''}")
    h = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                       capture_output=True, text=True).stdout.strip()
    print(f"[git] la pointe locale : {h}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
