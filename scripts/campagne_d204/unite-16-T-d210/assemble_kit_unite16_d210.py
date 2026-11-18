#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kit_unite16_d210.py — LE KIT DE L'UNITÉ 04 D210 (loupe-16
saisie × les deux bras) : kit-unite-04-d210-20261118/ au dossier de
campagne — la pièce, la notation, le brouillon, LE SCÉNARIO NOUVEAU (le
juge né à la présente édition — le premier terrain À ÉTAT : le guichet
aux TROIS feuilles), les fixtures (proxy.exe scellé, le témoin 3f), le
source C + les tests, le journal + le garde-brut, la graine, la gravure
EMPREINTES, le LISEZMOI terrain, le lanceur (CRLF conservés)."""
import hashlib
import json
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
UNITE = REPO / "scripts" / "campagne_d204" / "unite-16-T-d210"
ATELIER = pathlib.Path("/home/z/my-project/triade/lab/atelier-d210-p39uklsca")
KIT13 = REPO / "scripts" / "campagne_d204" / "unite-13-T-d210" / "kit" \
    / "kit-unite-03-d210-20261118"
KIT = UNITE / "kit" / "kit-unite-04-d210-20261118"


def sha(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def totaux_journal() -> tuple[int, int, int, int]:
    """Les appels de la présente unité, lus du journal (100 % log-api)."""
    lignes = [json.loads(l) for l in (ATELIER / "preuves" /
              "journal-tokens-d210.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
    n16 = [l for l in lignes if l.get("tache") == "loupe-16"]
    t = sum(l["total_tokens"] for l in n16)
    tT = sum(l["total_tokens"] for l in n16 if l["bras"] == "T")
    tC = sum(l["total_tokens"] for l in n16 if l["bras"] == "C")
    return len(n16), t, tT, tC


LANCEUR = "\r\n".join([
    "@echo off",
    "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 04 D210",
    "rem (loupe-16 saisie x bras T, la campagne D210 — la quatrieme unite, la sequence tiree). Le run court dans SA",
    "rem PROPRE console, INTACT : le GUI ne l'intercepte jamais (CA6).",
    "rem Le temoin ne se signe JAMAIS ici : votre main, toujours (D99).",
    "rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition",
    "rem v2 du kit 01, la meme discipline).",
    "title TRIADE - Unite 04 D210 (loupe-16 saisie x bras T) - campagne D210",
    'cd /d "%~dp0"',
    "where python >nul 2>nul",
    "if errorlevel 1 (",
    "  echo [REFUS] python introuvable au PATH - le kit exige Python 3.",
    "  pause",
    "  exit /b 2",
    ")",
    "set PYTHONIOENCODING=utf-8",
    "powershell -NoProfile -Command \"[Console]::OutputEncoding="
    "[Text.Encoding]::UTF8; python scenario-unite16.py 2>&1 | "
    "Tee-Object -FilePath run-console-unite16T.txt\"",
    "set CODE=%ERRORLEVEL%",
    "echo.",
    "echo === LE RUN A FINI (code %CODE%) ===",
    "echo Le temoin vit a preuves-unite16\\temoin-unite16.txt :",
    "echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.",
    "pause",
    "exit /b %CODE%",
    ""]) + "\r\n"


def main() -> int:
    KIT.mkdir(parents=True, exist_ok=True)
    n16, total, tT, tC = totaux_journal()
    LISEZMOI = f"""LISEZMOI — LE KIT DE L'UNITÉ 04 D210 : LOUPE-16 SAISIE × BRAS T
(la campagne D210 — la QUATRIÈME unité, la séquence tirée de la graine
D217 : loupe-16 le bras T d'abord ; le kit livré par le labo au coffre
/test en son dossier daté — le GUI vous attend à l'onglet 1·KIT de
l'unité loupe-16 × T)
========================================================================

L'OBJET : la QUATRIÈME unité de la campagne D210 (le plan
pré-enregistré 4a3b1311…, la menace « kit partagé et formats
asymétriques ») — le bloc loupe-16 SAISIE au BRAS T, LE PREMIER BLOC À
ÉTAT de la campagne : DEUX chiffres hexa composent l'octet (le premier
ATTEND, le second ENGAGE), l'octet va AU JOURNAL DES ÉCRITURES (l'entrée
par décalage, la réécriture du même octet REMPLACE) ET au tampon de vue
(visible immédiatement), la marque SALE est posée, LA GARDE de loupe-18
RÉ-ARMÉE à chaque écriture, le curseur AVANCE clampé et LA VUE SUIT (le
recadrage — loupe-02 le scellé RE-LIT, la feuille InvalidateRect repeint)
— et LE DISQUE DEMEURE INTACT. La pièce de ce kit est le build du plan où
le slot loupe-16 (RVA 0x6240, 704 o) porte LA NOTATION DE CAMPAGNE :
écrite À LA RIG (100 % log-api — la construction de la quatrième unité :
{n16} appels, {total} tokens [bras T {tT} + bras C {tC}], le journal et
le garde-brut INCLUS au kit) depuis le contrat loupe-16:R1. LES
DIX-SEPT autres blocs demeurent les SCELLÉS du projet.

LA CONSTRUCTION (consignée, les défauts nommés AVANT toute livraison)
: la rig L6 (compter_tokens e2939ef9…, rig_auteur e5aa404a…,
recoupés INTACTS aux empreintes) ; l'oracle écrit-avant-code
(oracle-depuis-I.txt, dérivé du contrat I seul) ; DEUX tours d'auteur
(it1 nommé F1-F5 aux contrôles — la classe des OFFSETS [la poignée lue
à +0x328 contre le plan +528], la classe des NON-VOLATILS [rsi/rdi
détruits jamais poussés], la ligne ILLÉGALE [l'étiquette
IAT_INVALIDATERECT posée au brouillon], la classe des LEA MORTS, le
verdict nu) PUIS LA COMPOSITION DES ÉLÉMENTS CONVERGÉS (l'it3, le
geste mécanique du labo NOMMÉ — le précédent des 336/341/346) ; la
composition propre : les VOLATILS r10/r11 seuls au message à la barre
(rsi/rdi JAMAIS touchés — l'état propre exigé aux 10 000 frappes), le
remplissage lu u32 SEUL (+552, jamais le qword : la marque vit à
+556 — la cellule fantôme refusée MÊME sale, l'écart nommé à la
confrontation du scellé) ; la CRISTALLISATION 10/10 rebuilds
byte-identiques (656 o, le cristal 14e45f57…) ; le build loupe.exe
127 488 o, sha256 b382e01b… (121 verrous : le round-trip R5, les
mesures D161 des scellées, le réseau des specs, l'audit msx64, la
double preuve R7 ; le différentiel au scellé CONFINÉ au slot loupe-16
[0x5440, 0x5700) et à la porte R10 — 31 plages, 496 o).

L'ORACLE AU HARNAIS (le juge = le modèle indépendant, la graine
20261115) : 17 VERT, 0 ROUGE — V1 le différentiel 10 000 frappes aux
DEUX disques (le témoin 3f ET le grand 8k : les ré-écritures, la
frontière des 256 DISTINCTS, la vue qui suit, l'état propre) ; V2 le
scénario « 4d5a » (l'écran attendu, loupe-10) ET LA VUE QUI SUIT (le
recadrage à 208, la relecture LOUPE02 comptée, le recouvrement au
tampon) ; V3 les rejets (E1 -4 nommé ; E2 la fantôme -3 RIEN au
journal ET la fantôme MARCHE SALE ; le vide ; E3 le 257e distinct -3
« journal plein », RIEN perdu) ; V4 le repli (le non-hexa ignoré,
VK_SUPPR à l'attente) ; V5 LA FALSIFICATION DEMANDÉE : la garde non
ré-armée (le mutant aux DEUX NOP) — le scénario de loupe-18 (éditer
puis Alt+F4 UNE SEULE fois doit avertir) ÉCHOUE au mutant, la preuve
TRAVERSE LES BLOCS ; la notation juste re-jouée VERTE.

LE SCÉNARIO DE CE KIT EST NOUVEAU (le juge né à la présente édition —
les juges des unités 1 à 3 venaient de D204, celui-ci n'existait pas)
: LE PREMIER TERRAIN À ÉTAT — le scénario est LE CHARGEUR
(LoadLibraryEx DONT_RESOLVE) PUIS LE GUICHET FAIL-CLOSED : les TROIS
feuilles du chemin (user32 InvalidateRect, kernel32 SetFilePointerEx +
ReadFile pour la relecture de loupe-02 le scellé) LIÉES PAR LA TABLE
D'IMPORTS — chaque slot découvert PAR SES NOMS (jamais une RVA codée,
la leçon des Entrées 302/304 reconduite), chaque geste vérifié
(VirtualProtect, la re-protection, la relecture recoupée), tout écart
= REFUS NOMMÉ, RIEN ne court. Le disque VIVANT par poignée réelle
(CreateFileW du témoin : loupe-02 RE-LIT le disque pour de vrai). Le
juge : le MODÈLE INDÉPENDANT extrait du scénario — recoupé AU LABO par
AST contre le contre-modèle de l'oracle du bras T (20 000 sondes, 0
écart).

LE BRAS C : gcc -O2 -std=c11 -Wall -Wextra PROPRE (le juge POSIX 14
VERT 0 ROUGE — V1-V5 le miroir du bras T, la même graine 20261115),
la revue CONFORME.

LE GESTE DU TERRAIN (le run de l'unité — le GUI 1-clic livré au
commandement, L'ATELIER CHOISI PAR CONSTRUCTION) : LANCER-RUN-UNITE16-
D210-1CLIC.bat → CHOISIR LE DOSSIER DE L'ATELIER à l'onglet 4·LIVRE →
TOUT LANCER — l'attendu : les NEUF verdicts VERT (9 VERT, 0 ROUGE, code
0), le témoin daté signé de votre main [D99], preuves-unite16/ au
coffre /test. LA LIGNE AU LIVRE PENDANT LE RUN (l'onglet 4·LIVRE du
GUI la couche LUI-MÊME à l'atelier choisi : T-loupe-16-d210-it1 — la
frontière vécue de la 348 PORTÉE PAR CONSTRUCTION à la présente
unité : le kit naît AVEC l'atelier choisi, jamais d'édition v2).

LA COMMANDE DE LA DLL AU TERRAIN (le bras C, le GAP mingw consigné)
: x86_64-w64-mingw32-gcc -O2 -shared -o loupe-16-d210-c.dll
source-loupe-16-C.c loupe-16-c.def (le .def : EXPORTS
loupe_16_saisie — la famille D204 ; le source compile PROPRE au flux
standard).

(18/11/2026, la session de la construction — la quatrième unité, la
séquence honorée, l'atelier choisi PAR CONSTRUCTION)
"""
    pieces = [
        ("GRAINE-D210.txt", ATELIER / "GRAINE-D210.txt"),
        ("LANCEUR-UNITE-16-T.bat", None),
        ("LISEZMOI-KIT-UNITE-04-D210.txt", None),
        ("brouillon-loupe-16-saisie.asm", UNITE / "brouillons" / "loupe-16-saisie.asm"),
        ("journal-tokens-d210.jsonl", ATELIER / "preuves" / "journal-tokens-d210.jsonl"),
        ("garde-brut-d210.jsonl", ATELIER / "preuves" / "garde-brut-d210.jsonl"),
        ("loupe.exe", UNITE / "piece" / "loupe.exe"),
        ("notation-loupe-16-saisie.asm", UNITE / "notation" / "loupe-16-saisie.asm"),
        ("proxy.exe", KIT13 / "proxy.exe"),
        ("scenario-unite16.py", UNITE / "epreuves" / "scenario-unite16.py"),
        ("source-loupe-16-C.c", UNITE / "epreuves" / "source-loupe-16-C.c"),
        ("temoin-3f.bin", KIT13 / "temoin-3f.bin"),
        ("tests-loupe-16-C.md", UNITE / "epreuves" / "tests-loupe-16-C.md"),
    ]
    for nom, source in pieces:
        if source is None:
            continue
        shutil.copyfile(source, KIT / nom)
        print(f"[kit] {nom} : {sha(KIT / nom)[:16]}… "
              f"({(KIT / nom).stat().st_size} o)")
    # le lanceur (UTF-8 BOM + CRLF, la discipline du kit 03)
    (KIT / "LANCEUR-UNITE-16-T.bat").write_bytes(
        b"\xef\xbb\xbf" + LANCEUR.encode("utf-8"))
    print(f"[kit] LANCEUR-UNITE-16-T.bat : {sha(KIT / 'LANCEUR-UNITE-16-T.bat')[:16]}… "
          f"(CRLF + BOM)")
    # le LISEZMOI
    (KIT / "LISEZMOI-KIT-UNITE-04-D210.txt").write_text(
        LISEZMOI, encoding="utf-8", newline="\n")
    print(f"[kit] LISEZMOI-KIT-UNITE-04-D210.txt : "
          f"{sha(KIT / 'LISEZMOI-KIT-UNITE-04-D210.txt')[:16]}…")
    # la gravure EMPREINTES : les TREIZE pièces (elle-même exclue)
    ordre = [n for n, _ in pieces]
    lignes = [
        "EMPREINTES — LE KIT DE L'UNITÉ 04 D210 (loupe-16 saisie × bras T",
        "— la campagne D210, la QUATRIÈME unité, la séquence tirée de la graine D217)",
        "(chaque pièce sha256 — le scénario recoupe la pièce à la gravure ; une divergence, rien ne court)",
        ""]
    for nom in ordre:
        lignes.append(f"{sha(KIT / nom)}  {nom}")
    (KIT / "EMPREINTES-KIT-UNITE-04-D210.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
    print(f"[kit] EMPREINTES-KIT-UNITE-04-D210.txt : "
          f"{len(ordre)}/13 pièces gravées, "
          f"{sha(KIT / 'EMPREINTES-KIT-UNITE-04-D210.txt')[:16]}…")
    print(f"[kit] le kit né : {KIT} ({len(list(KIT.iterdir()))} pièces)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
