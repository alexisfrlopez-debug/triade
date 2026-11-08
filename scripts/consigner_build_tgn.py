#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""consigner_build_tgn.py — LA CONSIGNATION DU BUILD DE LOUPE (M10, l'ère du
TGN) : loupe.exe 0.1.0-dev.1 NÉ — la première application née de TRIADE
entière (le geste de BUILD, jamais scellage : la 0.1.0 attend le run
terrain vert recoupé M10-(e)).

Le journal reçoit l'Entrée 202, le PLAN reçoit la phrase du programme TGN
(l'ère ouverte au build → LE BUILD NÉ) + la rangée (d) (le kit attend le
build → LE BUILD NÉ, le kit terrain est le geste suivant), le worklog
reçoit la Task ID 120. AUCUNE nouvelle décision (l'exécution de la D177 :
le build était DÉBLOQUÉ par la cérémonie passée, il est exécuté ici).

GARDES AVANT ÉCRITURE (l'état de build NÉ, exigé AVANT toute écriture) :
  - sceau I : LES QUATORZE arbres VERTS, l'état « reelle » (D87 — le
    garde a précédé construire(), le build l'a exigé) ;
  - l'artefact : loupe/loupe.exe 50 688 o, sha256
    f07dd2cfc6cab97598657a8488a33ba0f7de2d1509a84d6b008ad4c1c1965499 ;
  - la carte : génération 13 lue, la signature Ed25519 vérifiée, le
    verrou croisé 26/26 (chaque bloc embarqué revérifié CONTRE
    l'artefact) ;
  - les frontières : les TROIS scellés d'origine INTACTS (selftest.exe,
    demo.exe, proxy.exe 1.0.0 — les ancres R7), aucune balise bougée.
Tout écart = ÉCHEC NOMMÉ, rien n'est écrit. Rejeu REFUSÉ."""

import hashlib
import importlib.util
import os
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "m4"))
sys.path.insert(0, str(REPO / "m4" / "outils"))

SHA_EXE = ("f07dd2cfc6cab97598657a8488a33ba0"
           "f7de2d1509a84d6b008ad4c1c1965499")
TAILLE_EXE = 50688
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
PLAN = REPO / "docs" / "PLAN_MILESTONES.md"
WORKLOG = REPO / "worklog.md"
MARQUEUR = "<!-- m5a:journal-des-builds"


def _garde() -> None:
    # 1. le garde sceau I : QUATORZE arbres VERTS, l'état « reelle »
    spec = importlib.util.spec_from_file_location(
        "sceau_I", REPO / "v06" / "sceau_I.py")
    sceau_I = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sceau_I)
    arbres = ["m0", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8",
              "tls13", "loupe", "demo", "terrain", "v06"]
    sceau_I.garde(arbres)
    assert sceau_I.etat_cle().startswith("reelle"), "la clé n'est pas reelle"
    print(f"[garde] sceau I : {len(arbres)} arbres VERTS, l'état « reelle »")

    # 2. l'artefact né : la taille ET l'empreinte
    chemin_exe = REPO / "loupe" / "loupe.exe"
    donnees = chemin_exe.read_bytes()
    assert len(donnees) == TAILLE_EXE, f"taille {len(donnees)} != {TAILLE_EXE}"
    sha = hashlib.sha256(donnees).hexdigest()
    assert sha == SHA_EXE, f"sha256 {sha} != {SHA_EXE}"
    print(f"[garde] loupe.exe : {TAILLE_EXE} o, sha256 {sha[:16]}… — NÉ")

    # 3. la carte génération 13 : signature + verrou croisé 26/26
    import carte_m10 as cm10
    phrase, _ = cm10.charger_secrets(interactif=False)
    entete, fragments, signature, pub = cm10.lire_carte()
    cm10.verifier_listes_blanches(entete.decode("ascii"))
    cm10.verifier_signature(pub, entete, fragments, signature)
    assert cm10.empreinte_racine(fragments).hex() in entete.decode("ascii")
    assert "generation=13" in entete.decode("ascii"), "la carte n'est pas génération 13"
    maitre = cm10.cle_maitresse(phrase)
    bld = cm10.dechiffrer_fragment(maitre, "frag-bld",
                                   fragments["frag-bld"]).decode("utf-8")
    empreintes = {}
    for ligne in bld.splitlines():
        if ligne.startswith("[bloc]"):
            champs = dict(zip(ligne.split()[1::2], ligne.split()[2::2]))
            # « id=b20001 addr=0x… empreinte=sha256:… » — parse par regex
            import re
            m = dict(re.findall(r"(\w+)=(\S+)", ligne))
            empreintes[m["id"]] = m["empreinte"]
    import re as _re
    manifeste = None
    for ligne in bld.splitlines():
        if ligne.startswith("[build]"):
            manifeste = dict(_re.findall(r"(\w+)=(\S+)", ligne))
    assert manifeste and manifeste.get("version") == "0.1.0-dev.1"
    assert manifeste.get("empreinte") == "sha256:" + SHA_EXE
    nb = len(empreintes)
    assert nb == 26, f"la carte indexe {nb} blocs (26 attendus)"
    print(f"[garde] la carte génération 13 : signature OK, {nb} blocs, "
          f"le manifeste 0.1.0-dev.1 == l'artefact")

    # 4. les frontières : les TROIS scellés INTACTS (R6/R7)
    for chemin, taille, sha_attendu, nom in (
            (REPO / "m1" / "selftest.exe", 9216,
             "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0",
             "selftest.exe (M1)"),
            (REPO / "demo" / "demo.exe", 0x4000,
             "df8f2e50949b14c072f139013a6166a041e573e49b6872d826958f522495e4af",
             "demo.exe 0.3.0 (la boucle)"),
            (REPO / "tls13" / "proxy.exe", 65024,
             "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d",
             "proxy.exe 1.0.0 (M9)")):
        d = chemin.read_bytes()
        assert len(d) == taille and hashlib.sha256(d).hexdigest() == sha_attendu, \
            f"le scellé {nom} a divergé — AUCUNE écriture"
    print("[garde] les TROIS scellés d'origine INTACTS — les frontières tiennent")


ENTREE_202 = """## Entrée 202 — LE BUILD DE LOUPE NÉ : loupe.exe 0.1.0-dev.1 (50 688 o, sha256 f07dd2cf…) — LA PREMIÈRE APPLICATION NÉE DE TRIADE ENTIÈRE, l'ère du TGN au build ; la carte GÉNÉRATION 13, le verrou croisé 26/26 ; le kit terrain attend (09/11)

**La reprise (l'état au geste).** La cérémonie d'ère PASSÉE SUR PIÈCES (Entrée 201) : le garde QUATORZE arbres VERTS, la dette D166/D171 SOLDÉE, l'ère du TGN OUVERTE AU BUILD — la SUITE nommait LE BUILD DE LOUPE loupe 0.1.0-dev.1. Le développeur l'a commandée (« ok pour la suite ») : construire() est joué ici, le geste de BUILD jamais scellage (la balise `loupe 0.1.0` se scellera sur le run terrain vert recoupé, M10-(e) — la porte est de processus).

**L'instrument : loupe/build_loupe.py (le modèle build_m9/demo — la chaîne du domaine).** LE GARDE-SCEAU D'ABORD (D87 fail-closed) : sceau_I.garde(les QUATORZE arbres) AVANT construire() — le garde VERT 14/14, l'état « reelle (ceremonie hors-ligne, D87) » ; les TROIS scellés d'origine relus ET confrontés à leurs ancres (selftest.exe M1 8038585b… · demo.exe 0.3.0 df8f2e50… · proxy.exe 1.0.0 446279f3… — INTACTS). PUIS LA COUCHE I relue (les 18 spécifications, gabarit § 2.2, révisions concordantes — R2 : la cérémonie a précédé, chaque bloc porté par sa spécification AVANT le premier octet). PUIS L'ASSEMBLAGE : les 18 notations par le lecteur canonique (keystone), round-trip R5 (capstone), les longueurs == les mesures de l'arrêt (D161 : 47/296/122/388/312/879/102 + 271/1614/568/796/126/983/1135 + 391/660/521/163 o).

**L'oracle structurel : 43 verrous.** Les déplacements RIP == les symboles du plan (la liste fermée : les zones, CUMUL, les tables, les 24 libellés, l'UTF-16, les feuilles IAT) ; LES APPELS DIRECTS == LE RÉSEAU DES SPECS (chaque bloc chez ses appelés — loupe-13 → libc-02 LE SCELLÉ M1, loupe-05 → tls13-01/03/04 LES SCELLÉS M9, loupe-09 → 01/10/11/12/14/15/16/17/18 + win-03 LA BOUCLE SCELLÉE DÉMO) ; les feuilles IAT par bloc == la liste fermée de chaque spec (I5 — les quatre feuilles pures SANS entrée : 04/07/08/13) ; AUCUN syscall ; LES SLOTS DISJOINTS (les 26 posés, l'erratum n° 4 : le contrôle qui nomme, PERMANENT).

**L'HÉRITAGE R7 — LA DOUBLE PREUVE aux adresses scellées.** Les HUIT héritages extraits de leurs scellés AUX ADRESSES D'ORIGINE : libc-01 memcpy @0x1100, libc-02 memcmp @0x1180, libc-07 memset @0x13C0 (les octets du selftest.exe M1), win-03 LA BOUCLE @0x15C0 (les octets du demo.exe 0.3.0 — ses TROIS déplacements RIP visent l'IAT démo RÉSERVÉE @0x2818/0x2820/0x2828), tls13-01..04 @0xC000-0xC3C0 (les octets du proxy.exe 1.0.0) et LA TABLE K[64] @0x2F00 (la table du scellé M9 — le déplacement hérité de tls13-02 la vise) : les extraits des SCELLÉS == les notations d'origine ré-assemblées == les octets posés AUX MÊMES adresses — jamais une ré-écriture, jamais un pouce bougé.

**LA COMPOSITION 0.1.0-dev.1 (quatre sections, le miroir démo — VA croissantes).** .text 0x1000 : la minilibc + la boucle aux adresses scellées, le reste int3 (la réserve M1 vierge) ; .rdata 0x2000 : les tables MD5 S/T (dérivées par arithmétique au plan), les pièces du rendu (l'entête « Décalage  00 01 … 0F  ASCII », les tables HEX/HEXL), les 24 libellés latin-1 (le tiret ASCII et le point médian 0xB7), l'UTF-16 (la classe « LoupeHexa », le titre « Loupe — l'éditeur hexadécimal », l'explication fatale), L'IAT 34 FEUILLES (kernel32 10 @0x2400 · user32 18 @0x2450 · gdi32 6 @0x24E0 — l'ordre figé du geste (a)), L'IAT DÉMO @0x2818 (les TROIS qwords que les déplacements scellés de win-03 visent — le prix du déplacement scellé, la double entrée n'est pas une redondance), LA MACHINERIE D'IMPORTS @0x2830+ (5 descripteurs : user32 DEUX FOIS — le marché + la double entrée), LA PORTE R10 @0x2C60 (la table des sommes des 26 blocs embarqués + le qword version 0x00010001 + l'ancre) et K[64] @0x2F00 ; .text2 0x4000-0xDFFF : les 18 blocs du domaine (0x4040-0x6800) + la marge int3 + la famille sha aux adresses scellées M9 (la convention .text5 : la zone réservée int3 DANS le fichier) ; .data 0xE000-0x1FFFF : le CADRE né poignée INVALIDE à +528 (l'initialiseur du build — le miroir du harnais : le zéro de la mémoire vierge serait une session fantôme), les zones du domaine, CUMUL 64 Kio finissant 0x20000. L'ENTRÉE : AddressOfEntryPoint == LOUPE09_VA 0x5C00 (WinMain — l'entrée EST le bloc, D161 : la réserve 64 o s'est inclinée, aucune fiction de trampoline) ; WINDOWS_GUI ; l'image PI (D33).

**LA VALIDATION PE — LA COMPOSITION INTÉGRALE (chaque octet compté).** pefile relit : machine 0x8664, QUATRE sections aux VA/vsize du plan, l'entrée, le sous-système, SizeOfImage 0x20000 ; LE MARCHÉ DES IMPORTS : kernel32 10 + user32 18 + gdi32 6 + user32#2 3 (les FirstThunk == les slots du plan, D7/D35 — la double entrée démo @0x2818) ; LA COMPOSITION INTÉGRALE : chaque octet de .text ∈ un héritage posé OU int3 ; chaque octet de .text2 ∈ un bloc (la notation + le padding NOP 0x90) OU la famille sha OU int3 ; chaque octet de .rdata ∈ une pièce posée du plan OU la marge zéro ; la porte R10 RELUE de l'image == la table composée ; le qword version == VERSION_DEV ; .data le CADRE né poignée INVALIDE ; la taille du fichier 0xC600.

**Les preuves d'observable : LES TROIS HARNAIS REJOUÉS AU GESTE MÊME DU BUILD** (le miroir du M9 rejouant M4+M5+sys) : harnais_noyau.py **59/59 VERTS** (les vecteurs officiels RFC 1321, le différentiel hashlib, LA PIÈCE DE L'ÈRE jugée par sa propre application, les rejets nommés, la falsification) ; harnais_rendu.py **53/53 VERTS** (L'INSTRUMENT RETOQUÉ AUX ATTENTES r2 de loupe-09 — la révision nommée du geste (d) : 874 → 1135 o, la table étendue, la famille édition au réseau — le miroir de la spec, les notations (c) voisines INTACTES) ; harnais_edition.py **45/45 VERTS** (le disque saisissable, la mort complète, LE RÉSEAU de la garde, l'écriture à l'octet). **157 contrôles VERTS au geste du build — le domaine est prouvé, l'artefact en est composé.**

**L'ARTEFACT : loupe/loupe.exe 0.1.0-dev.1, 50 688 o, sha256 f07dd2cfc6cab97598657a8488a33ba0f7de2d1509a84d6b008ad4c1c1965499.** LE DÉTERMINISME CONSTATÉ : le mode --verifier RECOMPOSE l'artefact de ses sources et le confronte octet par octet — IDENTIQUE (la re-vérification VERTE, l'artefact DÉTERMINISTE).

**La carte GÉNÉRATION 13 (lignée D80, la graine durable D144 — LA PREMIÈRE GÉNÉRATION DU DOMAINE : les i11xxxx entrent à la carte).** loupe/carte_m10.py (le modèle carte_m9) : QUATRE fragments chiffrés XChaCha20-Poly1305 (Argon2id 64 Mio → HKDF par fragment et par génération), l'empreinte racine SHA-256, la signature Ed25519 de la graine durable — les 26 blocs indexés (les 18 i11xxxx + les HUIT hérités : b20001/02/07 la minilibc · d40003 la boucle · h100001..04 la famille sha, états « scellés », leurs origines citées), les contrats PARSÉS des spécifications (la couche I de chaque ère — R2), les notations empreintées, le manifeste du build (artefact, version, taille, empreinte, les oracles, l'héritage, le garde). LE VERROU CROISÉ (R8) : la carte relue indépendamment — signature OK, racine OK, **26/26 empreintes revérifiées CONTRE l'artefact**, le manifeste == l'octet. Le tableau de bord écrit (carte/tableau-de-bord.txt).

**Détail.** FRONTIÈRES : aucune balise ne bouge (win 0.9.0 / linux 0.7.0 / riscv 0.8.0 / tls13 1.0.0 INTACTES — les TROIS scellés confrontés au geste), AUCUN arbre signé touché (le garde 14/14 AVANT construire()), AUCUN octet de notation (R2 — les 18 notations INTACTES, le build les lit), la clé privée jamais traversée (D87 — le build ne signe rien, le scellage sera un fait de carte sur le run terrain), le proxy 1.0.0 et la carte tls13 INTACTS. Livrables : loupe/build_loupe.py, loupe/carte_m10.py, loupe/layout.py (l'adressage du geste build : la machinerie d'imports + la porte R10 ARRÊTÉS), loupe/harnais_rendu.py (l'instrument RETOQUÉ r2 — la révision nommée), loupe/loupe.exe, loupe/carte/ ; le présent script. Ce que cela DÉBLOQUE : **LE KIT TERRAIN (M10-(d) seconde moitié, modèle m9f : le coffre /test recevra la vague Loupe — loupe.exe + le LISEZMOI + le réceptacle de preuves) PUIS LE RUN (M10-(e))** : le développeur court LOUPE sur SA machine (le VRAI Windows 11, l'application réelle ouverte, éditée, sauvegardée) — et si le vert tient, la balise `loupe 0.1.0` scellée sur run terrain recoupé : LE JALON M10, la méthode entière prouvée par la CRÉATION.

- SUITE : LE KIT TERRAIN (M10-(d) seconde moitié, modèle m9f : l'artefact + le LISEZMOI + le réceptacle au coffre /test) ; puis LE RUN (M10-(e) — le geste du développeur) ; le projet fils attend son premier geste à son message propre.

"""


TASK_120 = """## Task ID 120 — LE BUILD DE LOUPE NÉ : loupe.exe 0.1.0-dev.1 (50 688 o, sha256 f07dd2cf…), la carte génération 13, le verrou croisé 26/26 — la première application née de TRIADE entière (09/11)

- LA DEMANDE : « ok pour la suite » — la SUITE nommée de l'Entrée 201 (LE
  BUILD DE LOUPE, le garde était VERT).
- LE GARDE D'ABORD (D87 fail-closed) : sceau_I.garde(les QUATORZE arbres)
  AVANT construire() — 14/14 VERTS, l'état « reelle » ; les TROIS scellés
  d'origine confrontés à leurs ancres (selftest.exe · demo.exe ·
  proxy.exe 1.0.0 — INTACTS).
- LA CHAÎNE : loupe/build_loupe.py — la couche I relue (18 specs, R2) ;
  l'assemblage 18/18 (round-trip R5, les longueurs == les mesures D161) ;
  l'oracle structurel 43 verrous (le réseau des specs, les listes fermées
  IAT, les déplacements RIP aux symboles, AUCUN syscall, les slots
  disjoints) ; L'HÉRITAGE R7 LA DOUBLE PREUVE (les 8 extraits des scellés
  == les notations d'origine ré-assemblées == les octets posés AUX MÊMES
  adresses + la table K[64] @0x2F00).
- LA COMPOSITION : quatre sections (le miroir démo) — .text la minilibc +
  la boucle scellées · .rdata les pièces + l'IAT 34 feuilles + l'IAT démo
  @0x2818 (le prix du déplacement scellé) + la machinerie + LA PORTE R10 +
  K[64] · .text2 les 18 blocs + la famille sha scellée · .data le CADRE né
  poignée INVALIDE ; l'entrée == LOUPE09_VA 0x5C00 (WinMain — D161),
  WINDOWS_GUI, l'image PI.
- LA VALIDATION : LA COMPOSITION INTÉGRALE (chaque octet compté : bloc,
  pièce, int3 ou marge zéro) + pefile (le marché des imports 10+18+6+3,
  les FirstThunk == les slots du plan) + la porte R10 relue de l'image.
- LES PREUVES D'OBSERVABLE : LES TROIS HARNAIS REJOUÉS AU GESTE MÊME —
  noyau 59/59 + rendu 53/53 (L'INSTRUMENT RETOQUÉ r2 : la révision nommée
  de loupe-09, 874 → 1135 o, la famille édition au réseau — les notations
  (c) voisines INTACTES) + édition 45/45 — 157 contrôles VERTS.
- L'ARTEFACT : loupe/loupe.exe 50 688 o, sha256
  f07dd2cfc6cab97598657a8488a33ba0f7de2d1509a84d6b008ad4c1c1965499 — LE
  DÉTERMINISME CONSTATÉ (--verifier : la recomposition == l'octet).
- LA CARTE : GÉNÉRATION 13 (lignée D80, la graine durable D144 — la
  PREMIÈRE du domaine, les i11xxxx entrent) : 4 fragments chiffrés, la
  signature Ed25519, les 26 blocs (18 + 8 hérités), les contrats PARSÉS
  des specs ; LE VERROU CROISÉ 26/26 (R8) ; le tableau de bord écrit.
- FRONTIÈRES : aucune balise ne bouge, AUCUN arbre signé touché, AUCUN
  octet de notation (R2), la clé privée jamais traversée (D87), le proxy
  1.0.0 et la carte tls13 INTACTS.
- SUITE : LE KIT TERRAIN (M10-(d) seconde moitié, modèle m9f — loupe.exe
  + le LISEZMOI + le réceptacle au coffre /test) ; puis LE RUN (M10-(e) —
  le geste du développeur : la 0.1.0 se scellera sur le vert recoupé).
"""


def main() -> int:
    _garde()

    # --- le journal : l'Entrée 202 AVANT le marqueur des builds ---------------
    texte = JOURNAL.read_text(encoding="utf-8")
    assert "## Entrée 202" not in texte, "l'Entrée 202 existe déjà — rejeu refusé"
    idx = texte.index(MARQUEUR)
    texte = texte[:idx] + ENTREE_202 + texte[idx:]
    JOURNAL.write_text(texte, encoding="utf-8")
    print("[journal] l'Entrée 202 insérée (avant le marqueur des builds)")

    # --- le PLAN : la phrase du programme TGN + la rangée (d) ----------------
    plan = PLAN.read_text(encoding="utf-8")
    ancien = ("l'ère du TGN est OUVERTE AU BUILD (loupe 0.1.0-dev.1, le geste "
              "de BUILD jamais scellage)")
    nouveau = ("l'ère du TGN est AU BUILD : LOUPE.EXE 0.1.0-dev.1 NÉE le 09/11 "
               "(Entrée 202, Task 120 : 50 688 o, sha256 f07dd2cf… — les 18 "
               "blocs notés + les héritages scellés, la carte génération 13, "
               "le verrou croisé 26/26, geste de BUILD jamais scellage)")
    assert ancien in plan, "la phrase du programme TGN introuvable (le PLAN a bougé ?)"
    plan = plan.replace(ancien, nouveau, 1)

    ancien_d = "le build loupe 0.1.0-dev.1 DÉBLOQUÉ, le kit attend le build"
    nouveau_d = ("LE BUILD loupe 0.1.0-dev.1 NÉ (Entrée 202, Task 120 : loupe.exe "
                 "50 688 o, sha256 f07dd2cf…, la carte génération 13 + le verrou "
                 "croisé 26/26, LES TROIS HARNAIS 157 contrôles VERTS rejoués au "
                 "geste, la composition intégrale comptée) ; LE KIT TERRAIN est "
                 "le geste suivant")
    assert ancien_d in plan, "la phrase de la rangée (d) introuvable (le PLAN a bougé ?)"
    plan = plan.replace(ancien_d, nouveau_d, 1)
    PLAN.write_text(plan, encoding="utf-8")
    print("[plan] le programme TGN + la rangée (d) : LE BUILD NÉ consigné")

    # --- le worklog : la Task ID 120 ------------------------------------------
    wl = WORKLOG.read_text(encoding="utf-8")
    assert "## Task ID 120" not in wl, "la Task 120 existe déjà — rejeu refusé"
    wl = wl.rstrip("\n") + "\n\n" + TASK_120
    WORKLOG.write_text(wl, encoding="utf-8")
    print("[worklog] la Task ID 120 ajoutée")

    print("[consigner] LA CONSIGNATION DU BUILD ÉCRITE : Entrée 202 + PLAN "
          "(le programme TGN + la rangée (d)) + worklog Task 120 — Rien d'autre "
          "ne bouge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
