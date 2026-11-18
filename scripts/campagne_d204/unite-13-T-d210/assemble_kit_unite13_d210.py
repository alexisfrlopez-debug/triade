#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assemble_kit_unite13_d210.py — LE KIT DE L'UNITÉ 03 D210 (loupe-13
recherche × les deux bras) : kit-unite-03-d210-20261118/ au dossier de
campagne — la pièce, la notation, le brouillon, le scénario D204
INCHANGÉ, les fixtures (proxy.exe scellé, le témoin 3f), le source C +
les tests, le journal + le garde-brut, la graine, la gravure
EMPREINTES, le LISEZMOI terrain, le lanceur (CRLF conservés)."""
import hashlib
import pathlib
import shutil

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
UNITE = REPO / "scripts" / "campagne_d204" / "unite-13-T-d210"
ATELIER = pathlib.Path("/home/z/my-project/triade/lab/atelier-d210-p39uklsca")
D204 = REPO / "scripts" / "campagne_d204" / "unite-13-T" / "kit"
KIT = UNITE / "kit" / "kit-unite-03-d210-20261118"


def sha(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


LISEZMOI = """LISEZMOI — LE KIT DE L'UNITÉ 03 D210 : LOUPE-13 RECHERCHE × BRAS T
(la campagne D210 — la TROISIÈME unité, la séquence tirée de la graine
D217 : loupe-13 le bras T d'abord ; le kit livré par le labo au coffre
/test en son dossier daté — le GUI vous attend à l'onglet 1·KIT de
l'unité loupe-13 × T)
========================================================================

L'OBJET : la TROISIÈME unité de la campagne D210 (le plan
pré-enregistré 4a3b1311…, la menace « kit partagé et formats
asymétriques ») — le bloc loupe-13 RECHERCHE au BRAS T. La pièce de ce
kit est le build du plan où le slot loupe-13 (RVA 0x5740, 192 o)
porte LA NOTATION DE CAMPAGNE : écrite À LA RIG (100 % log-api, le
journal né des outils — la construction de la troisième unité : 17
appels, 40 749 tokens [bras T 28 251 + bras C 12 498], le journal et
le garde-brut INCLUS au kit) depuis le contrat loupe-13:R1 (LA
PREMIÈRE occurrence d'un motif de 1 à 32 o dans une fenêtre à partir
d'un départ donné — la position ABSOLUE de la PREMIÈRE, l'absence →
-1 LA FIN NOMMÉE, le motif plus long que la plage restante → -1
IMMÉDIAT, les trois refus → -5 ; la comparaison par LE SCELLÉ
libc-02 memcmp À LA CARTE [0x1180], jamais une boucle réécrite ;
AUCUNE entrée IAT — la feuille pure). LES DIX-SEPT autres blocs
demeurent les SCELLÉS du projet.

LA CONSTRUCTION (consignée, les défauts nommés AVANT toute livraison)
: la rig L6 (compter_tokens e2939ef9…, rig_auteur e5aa404a…,
recoupés INTACTS aux empreintes) ; l'oracle écrit-avant-code
(oracle-depuis-I.txt, dérivé du contrat I seul) ; la spirale
corrective : le brouillon it1 NÉ EN PROSE (AUCUNE instruction — la
ligne equ inassemblable, la classe nommée au contrôle) ; le correctif
1 (la réponse PARTIELLE : deux lignes seules — la classe de troncature
récurrente) ; le correctif 2 (LA NOTATION ENTIÈRE rendue) ; le
correctif 3 SYNTAXE (l'equ supprimé, le cmp au littéral) ; le
correctif 4 (l'appel au symbole LIBC02, le prologue) ; le correctif 5
(le faisceau STRUCTUREL : les arguments msx64, la borne absolue) ;
les correctifs 6-7 (l'épargne aux non-volatils poussés, la borne
DANS la boucle — les réponses PARTIELLES : le geste annoncé sans
l'appliquer, trois fois) ; le correctif 8 (le départ lu, les arguments
rcx/rdx/r8 — mais l'épargne perdue : l'OSCILLATION nommée). LE GESTE
MÉCANIQUE DU LABO (nommé, bijectif — le précédent 336/341) : la
composition de l'it5 des éléments convergés — la remappe bijective
des arguments (rdi→rcx, rsi→rdx, rdx→r8) ET de la position
(r10→r15 l'épargnée), le re-pose de la ligne du départ AVANT toute
poussée, la Q2 dans RAX (r12 demeure window_len pur), le ret
re-posé. LA MESURE honnête : la spirale corrective 16 245 tokens =
39 % — H8 ROMPUE à la troisième unité (l'observation défavorable
consignée, D189 : la spirale ne demeure plus le chemin chaud — les
g tes mécaniques du labo prirent le relais de la complétion).

LES ÉPREUVES AU LABO : la cristallisation 10/10 rebuilds
byte-identiques (122 o, sha256 8b7d8858…) ; le build loupe.exe
127 488 o (les 121 verrous, l'écart au scellé CONFINÉ au slot
loupe-13 et à la porte R10) ; L'ORACLE AU HARNAIS 10 VERT 0 ROUGE
(V1 le corpus de l'école 10/10 + les marques de proxy.exe scellé [MZ
@0, PE @+64, les marques absentes → -1], V2 le différentiel 10 000
cas == bytes.find + les tampons LUS SEULS + l'état propre, V3 les
TROIS rejets -5, V4 la falsification [la position avancée d'un : les
44/44 cas à occurrence DIVERGENT]) ; LE BRAS C : gcc -O2 -std=c11
-Wall -Wextra PROPRE (le juge POSIX 9 VERT 0 ROUGE — V1-V4 le
miroir du bras T, la graine 20261115), la revue CONFORME.

LE GESTE DU TERRAIN (le run de l'unité — le GUI 1-clic livré au
commandement) : LANCER-RUN-UNITE13-D210-1CLIC.bat → TOUT LANCER —
l'attendu : les NEUF verdicts VERT (9 VERT, 0 ROUGE, code 0), le
témoin daté signé de votre main [D99], preuves-unite13/ au coffre
/test. La ligne au livre AU MÊME GESTE (l'onglet 4·LIVRE du GUI :
T-loupe-13-d210-it1 — le guide-344 § 7 : la ligne se vit À CHAQUE
run, jamais en retard).

LA COMMANDE DE LA DLL AU TERRAIN (le bras C, le GAP mingw consigné)
: x86_64-w64-mingw32-gcc -O2 -shared -o loupe-13-d210-c.dll
source-loupe-13-C.c loupe-13-c.def (le .def : EXPORTS
loupe_13_recherche — la famille D204 ; le source compile PROPRE au
flux standard).

(18/11/2026, la session de la construction — la troisième unité, la
séquence honorée)
"""


def main() -> int:
    KIT.mkdir(parents=True, exist_ok=True)

    # 1· les pièces matérielles
    pieces = [
        (UNITE / "piece" / "loupe.exe", "loupe.exe"),
        (UNITE / "notation" / "loupe-13-recherche.asm",
         "notation-loupe-13-recherche.asm"),
        (UNITE / "brouillons" / "loupe-13-recherche.asm",
         "brouillon-loupe-13-recherche.asm"),
        (D204 / "scenario-unite13.py", "scenario-unite13.py"),
        (REPO / "tls13" / "proxy.exe", "proxy.exe"),
        (D204 / "temoin-3f.bin", "temoin-3f.bin"),
        (ATELIER / "bras-C" / "loupe-13-C-final.c", "source-loupe-13-C.c"),
        (ATELIER / "bras-C" / "tests-loupe-13-C.md", "tests-loupe-13-C.md"),
        (ATELIER / "preuves" / "journal-tokens-d210.jsonl",
         "journal-tokens-d210.jsonl"),
        (ATELIER / "preuves" / "garde-brut-d210.jsonl",
         "garde-brut-d210.jsonl"),
        (ATELIER / "GRAINE-D210.txt", "GRAINE-D210.txt"),
    ]
    for src, nom in pieces:
        shutil.copyfile(src, KIT / nom)

    # 2· le lanceur (CRLF conservés — le vécu de la 339)
    lanceur = (D204 / "LANCEUR-UNITE-13-T.bat").read_bytes()
    texte = lanceur.decode("utf-8-sig", errors="replace")
    texte = texte.replace(
        "title TRIADE - Unite 5 (loupe-13 recherche x bras T) - campagne D204",
        "title TRIADE - Unite 03 D210 (loupe-13 recherche x bras T) - "
        "campagne D210")
    texte = texte.replace(
        "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 5",
        "rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 03 D210")
    texte = texte.replace(
        "rem (loupe-13 recherche x bras T, la campagne D204). Le run court dans SA",
        "rem (loupe-13 recherche x bras T, la campagne D210 — la troisieme "
        "unite, la sequence tiree). Le run court dans SA")
    texte = texte.replace("scenario-unite13.py", "scenario-unite13.py")
    with open(KIT / "LANCEUR-UNITE-13-T.bat", "wb") as f:
        f.write(texte.replace("\n", "\r\n").encode("utf-8"))

    # 3· le LISEZMOI terrain (AVANT la gravure — sa sha y vit)
    (KIT / "LISEZMOI-KIT-UNITE-03-D210.txt").write_text(
        LISEZMOI, encoding="utf-8", newline="\n")

    # 4· la gravure EMPREINTES (le juge du terrain recoupe à la lecture —
    #    la forme « sha256  nom », sha EN TÊTE : le correctif T0 de la 337)
    lignes = [
        "EMPREINTES — LE KIT DE L'UNITÉ 03 D210 (loupe-13 recherche × bras T",
        "— la campagne D210, la TROISIÈME unité, la séquence tirée de la "
        "graine D217)",
        "(chaque pièce sha256 — le scénario recoupe la pièce à la "
        "gravure ; une divergence, rien ne court)",
        "",
    ]
    ordre = [
        "LANCEUR-UNITE-13-T.bat", "notation-loupe-13-recherche.asm",
        "brouillon-loupe-13-recherche.asm", "loupe.exe", "proxy.exe",
        "scenario-unite13.py", "temoin-3f.bin", "source-loupe-13-C.c",
        "tests-loupe-13-C.md", "journal-tokens-d210.jsonl",
        "garde-brut-d210.jsonl", "GRAINE-D210.txt",
        "LISEZMOI-KIT-UNITE-03-D210.txt",
    ]
    for nom in ordre:
        lignes.append(f"{sha(KIT / nom)}  {nom}")
    (KIT / "EMPREINTES-KIT-UNITE-03-D210.txt").write_text(
        "\r\n".join(lignes) + "\r\n", encoding="utf-8")

    print(f"[kit] {KIT} : {len(ordre) + 2} pièces gravées")
    for nom in ordre + ["EMPREINTES-KIT-UNITE-03-D210.txt",
                        "LISEZMOI-KIT-UNITE-03-D210.txt"]:
        print(f"  {sha(KIT / nom)[:16]}…  {nom}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
