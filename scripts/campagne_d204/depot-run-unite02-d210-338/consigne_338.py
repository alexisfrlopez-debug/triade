#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigne_338.py — LA CONSIGNATION de l'Entrée 338 (Task 205) : le run
terrain de l'unité 02 D210 au kit GUI 1-clic REÇU et RECOUPÉ (10/10 VERT),
LA CAUSE DES DEUX ROUGE NOMMÉE (le juge v1 fautif livré à la 337 — le
rejeu forensique le prouve), le dépôt rangé, le rapport au /test, le git
poussé, le miroir Drive rafraîchi. Append au worklog.md (idempotent) ; la
carte OU-TROUVER portée à 338 (l'en-tête, la chaîne conservée)."""
import pathlib

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")

WORKLOG = """

Task ID: 205
Agent: Z.ai (agent principal — la session du run terrain de l'unité 02 D210 revenu et recoupé)
Task: L'ANNONCE DU DÉVELOPPEUR (« preuves deposees dans le drive /test ») : LE RUN TERRAIN DE L'UNITÉ 02 D210 AU KIT GUI 1-CLIC REÇU ET RECOUPÉ — 10/10 VERT, le témoin daté signé (D99), LA CAUSE DES DEUX ROUGE NOMMÉE AVANT CORRECTION (D202) : le juge v1 FAUTIF de D204 fut livré dans le kit — le rejeu forensique au lab le prouve, la pièce est correcte.

Work Log:
- LA RÉCEPTION (la sonde 338) : preuves-unite02/ à la racine du /test (né au
  coffre le 17/11 19:03:26Z) — TROIS pièces (temoin-unite02.txt 1 600 o,
  DEPOT-d210-unite02.txt 2 057 o, run-console-unite02-d210-20261117-200136
  .txt 3 970 o), chacune rapatriée au bac scripts/campagne_d204/
  depot-run-unite02-d210-338/epreuves/ par DOUBLE téléchargement byte-byte,
  md5 == la métadonnée Drive — 3/3 VERT.
- LE RECOUP (recoupe_depot_unite02_d210_338.py, 10/10 VERT) : la preuve T0
  du terrain (loupe.exe cf251c12… == la gravure == la pièce du kit recoupée
  au labo) ; le verdict 18 VERT, 2 ROUGE, code retour 1 ; LA MÊME PAIRE
  ROUGE que le juge v1 fautif de D204 (le témoin v1 aux archives en
  regard) ; LA MAIN (D99) : le témoin déposé 1 600 o == le témoin
  avant-main gravé au DEPOT (1 578 o, sha256 0c1ce902…) + la main posée —
  daté le 17/11/2026, signé Alexis Lopez, la même main que la campagne ;
  la machine PORTABLE · Windows 10 · AMD64 · Python 3.14.10 (CA2) ; LA
  CHRONOLOGIE tenue : le kit livré 17:15:38Z → le run 19:01:36Z → la
  console 19:01:37Z (chrono M4 0,5 s) → LA MAIN 19:02:41Z → le coffre
  19:03:26Z — jamais une date avant le run ; LE DEPOT : la console gravée
  byte-byte, les SEPT pièces du kit recoupées sha256 par sha256 == le kit
  GUI livré à la 337 (la chaîne de garde par le contenu, D143) ; LA CAP M1 :
  la PREMIÈRE livraison du bloc, 0 assemblage — le dépôt est le réceptacle
  ENTIER sans le zip du GUI (l'observation nommée, jamais maquillée).
- LA CAUSE DES DEUX ROUGE — LE REJEU FORENSIQUE (à la manière de la 333 :
  la cause confirmée sur les deux rives) : LE JUGE LIVRÉ — le
  scenario-unite02.py du kit == le juge v1 de D204 OCTET POUR OCTET
  (b3e896f7…), le juge FAUTIF nommé aux 283/284 (« la faute était au juge
  du labo »), réparé au v2 (302fa3a1…, R_JOURNAL 0xE4E0→0xE4A0) demeurant
  AUX ARCHIVES du bac 295 ; le kit D210 embarqua le v1 : R_JOURNAL =
  0xE4E0, SOIXANTE-QUATRE octets au-dessus de la vérité du layout
  (0xE4A0 — le lea de la notation D210) — le juge pose son journal trop
  haut, la pièce n'y voit JAMAIS les entrées, les DEUX vecteurs V2 du
  recouvrement échouent ; LA PREUVE : l'oracle du bloc couru DEUX FOIS —
  TEL QUEL : 22 VERT, 0 ROUGE (la pièce CORRECTE, le RAPPORT-UNITE-D210-01
  re-vécu) ; GREFFÉ de la seule constante fautive (la section V2) : 20
  VERT, 2 ROUGE — LES DEUX MÊMES VECTEURS, tout le demeurant VERT : LE
  VERDICT DU TERRAIN REPRODUIT AU LABO PAR LA CONSTANTE SEULE (les
  consoles rejeu-338-oracle-*.txt au bac, l'oracle greffé
  oracle_rejeu_fautif_338.py étiqueté). LE DÉFAUT DE LIVRAISON nommé à son
  propriétaire : le labo livra le juge fautif à la 337 — le run NE
  CONSOMME PAS d'itération (le précédent 295 : la faute au juge, jamais à
  la pièce), T-loupe-02-d210-it1 attend le re-run au juge réparé.
- LE RANGEMENT + LA LIVRAISON (ranger_livrer_338.py, TOUT VERT) : le dépôt
  DÉPLACÉ, jamais jeté (D143), à /test/archives-livraisons/
  unite-02-d210-20261118/preuves-unite02/ — chaque md5 recoupé AVANT et
  APRÈS, INTACT ; le RAPPORT-RECEPTION-RUN-UNITE02-D210-TERRAIN-
  20261118.txt (== RECOUP-338-preuves-unite02.txt, 4 736 o) livré à la
  racine du /test, re-téléchargé et md5-recoupé byte-byte.
- LA CONSIGNATION : la présente Task 205 + l'Entrée 338 ; la carte
  OU-TROUVER portée à 338 (l'en-tête, la chaîne 337 conservée) ; le bac
  scripts/campagne_d204/depot-run-unite02-d210-338/ (les epreuves/, les
  TROIS scripts du geste — rapatrie, recoupe, ranger_livrer —, l'oracle
  greffé, les DEUX consoles de rejeu, le RECOUP-338) ; le script de
  rapatriement à scripts/rapatrie_depot_unite02_d210_338.py.
- LE GIT ET LE MIROIR (la commande du développeur : « mets a jour le drive
  et git ») : le commit + LE PUSH GitHub aux jetons du /Tokens
  (git-credentials 600, JAMAIS committé — D12) ; le miroir Drive rafraîchi
  par drive_sync.py (le bundle + TRIADE-sauvegarde-git + la racine), la
  preuve de convergence idempotente.
- SUITE : ① LA CORRECTION au commandement (D202 : les défauts nommés avant
  correction) — la re-livraison du kit avec le juge v2 (302fa3a1…,
  R_JOURNAL = 0xE4A0, la vérité du layout) puis le re-run terrain au geste
  du développeur (le T-loupe-02-d210-it1 attend le juge réparé) ; ②
  loupe-08 le bras T d'abord (la séquence tirée, jamais re-tirée) ; la
  re-livraison d'attribution empirique au commandement.
  (18/11/2026, la session de la réception — le flux du coffre et du git
  aux jetons du /Tokens, l'annonce du développeur)
"""

ENTETE_338 = (
    "*Mise à jour : 18/11/2026 (Entrée 338 — LE RUN TERRAIN DE L'UNITÉ 02 "
    "D210 REÇU ET RECOUPÉ : le dépôt preuves-unite02/ au /test [né "
    "19:03:26Z le 17/11 — le témoin daté 17/11/2026 signé Alexis Lopez "
    "(D99), le DEPOT, la console du run 20261117-200136] rapatrié par "
    "double téléchargement byte-byte ; LE RECOUP 10/10 VERT "
    "[scripts/campagne_d204/depot-run-unite02-d210-338/ — "
    "RECOUP-338-preuves-unite02.txt, livré au /test comme "
    "RAPPORT-RECEPTION-RUN-UNITE02-D210-TERRAIN-20261118.txt] : la preuve "
    "T0 recoupée (loupe.exe cf251c12… == la gravure == le kit), le verdict "
    "18 VERT, 2 ROUGE recopié, la machine CA2, la chronologie tenue (le "
    "kit 17:15Z → le run 19:01:36Z → la main 19:02:41Z → le coffre "
    "19:03:26Z), les SEPT pièces du kit == la 337 ; LA CAUSE DES DEUX "
    "ROUGE NOMMÉE (D202) : le scénario livré au kit == le juge v1 FAUTIF "
    "de D204 OCTET POUR OCTET [b3e896f7…, R_JOURNAL = 0xE4E0, "
    "soixante-quatre octets au-dessus de la vérité du layout 0xE4A0] — LE "
    "REJEU FORENSIQUE : l'oracle greffé de la seule constante reproduit "
    "LE verdict terrain [20 VERT, 2 ROUGE, les deux mêmes vecteurs], "
    "l'oracle sain juge la pièce 22 VERT 0 ROUGE — la pièce est correcte, "
    "le run NE CONSOMME PAS d'itération, la re-livraison au juge v2 "
    "[302fa3a1…] attend le commandement ; le dépôt rangé à /test/"
    "archives-livraisons/unite-02-d210-20261118/ [md5 intact, D143] ; ")

# -- worklog (append, UTF-8 LF, idempotent) -----------------------------------
wl = (REPO / "worklog.md").read_text(encoding="utf-8")
if "Task ID: 205" in wl:
    print("[déjà] worklog.md porte Task 205 — pas de double append")
else:
    with open(REPO / "worklog.md", "a", encoding="utf-8", newline="\n") as f:
        f.write(WORKLOG)
    print("[consigné] worklog.md (Task 205, l'Entrée 338)")

# -- la carte OU-TROUVER (idempotent) ------------------------------------------
carte = REPO / "OU-TROUVER-LES-LIVRABLES.md"
texte = carte.read_text(encoding="utf-8")
if "(Entrée 338 —" in texte:
    print("[déjà] la carte porte l'en-tête 338 — pas de double apposition")
else:
    ancienne_entete = "*Mise à jour : 18/11/2026 (Entrée 337 —"
    assert ancienne_entete in texte, "l'en-tête 337 introuvable à la carte"
    texte = texte.replace(ancienne_entete, ENTETE_338 + "Entrée 337 —", 1)
    carte.write_text(texte, encoding="utf-8", newline="\n")
    print("[portée] OU-TROUVER-LES-LIVRABLES.md : l'en-tête 338, "
          "la chaîne 337 conservée")
