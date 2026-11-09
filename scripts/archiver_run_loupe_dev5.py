#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_run_loupe_dev5.py — LE TÉMOIN DU RUN dev.5 ARCHIVÉ SUR PIÈCES
(règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE CINQUIÈME RUN TERRAIN (l'Entrée 208) : « preuves déposées dans le
dossier /test du drive. quand je lance l'exe, la fenêtre s'ouvre et
se referme immédiatement » — le développeur a déposé le témoin du run
dev.5 au réceptacle (/test/preuves-loupe/temoin-loupe.txt, 1 209 o,
md5 0825dace…) : LE RUN LE PLUS LOIN JAMAIS VÊCU ENCORE — [T0] TOUT
VERT (l'empreinte dev.5 ASSERTÉE 6f830f9c…, l'image cartographiée
DONT_RESOLVE @ 0x7ff646600000, LE CADRE NÉ MIROIR, les adresses
scellées CONSTATÉES, l'IAT 37 feuilles posées) — puis [T1] ÉCHEC NOMMÉ
[SESSION] : loupe-01 a rendu 0xfffffff9 (-7 VERROUILLÉ, la copie…
non : LE FICHIER pourtant relu à l'instant).

L'AUTOPSIE DE LABO A ACQUITTÉ LA PIÈCE : l'appel CreateFileW était NÉ
PARFAIT (les arguments 5/6/7 à leurs vrais slots [rsp+0x20]+ — LA
CLASSE DE L'ENTRÉE 207 TENUE AU TERRAIN, PREUVE PAR LE NOM CHANGÉ :
-6 SYSTÈME [l'appel mal né] DEVINT -7 VERROUILLÉ [l'appel né, refusé
pour une RAISON RÉELLE]) ; c'est LE KIT QUI FAUTAIT : le scénario EST
LE CHARGEUR — l'image TIENT loupe.exe ouvert sans partage d'écriture,
et le VRAI Windows refuse gle 32 d'ouvrir à l'écriture le fichier
d'une section vivante : T1 OFFRAIT LA PIÈCE ELLE-MÊME à l'écriture.
loupe-01 A TRADUIT LE REFUS AU NOM PRÈS (I4/E2 : gle 32 → -7) — LA
VOIE NOMMÉE DE L'ÈRE A VÉCU SON PREMIER TERRAIN, VERTE PAR LE REFUS.
ET LA VITRINE A VÉCU SANS TÉMOIN UNE TROISIÈME FOIS (le témoin
vitrine ne fut pas joué : temoin-vitrine.txt ABSENT du dépôt — la
retraite statique du labo constate la voie SANS DÉFAUT CONNU : win-03
héritée ✓ [hWnd NUL, aligné], WinMain ✓, LA PROCÉDURE ✓, loupe-10 ✓,
le sous-programme .peindre ✓ [l'Entrée 207 : arg 5 au vrai slot,
l'alignement sub/add 8] — les deux morts de dev.4 s'expliquent par
les deux défauts SSE corrigés ; la retouche de l'Entrée 208 est AU
KIT SEUL : l'artefact dev.5 INCHANGÉ [6f830f9c…], la session naît
sur temoin-session.bin L'OMBRE byte-à-byte de la pièce — ET LE FRÈRE
DU DÉFAUT chassé : la session double de T6 offrait la pièce sous le
chargeur, elle offre l'ombre ; LA VITRINE SE VIT PAR SON TÉMOIN —
temoin-vitrine.bat est LA VOIE, le témoin REQUIS au réceptacle).

  1. LE TÉMOIN RAPATRIÉ ET RECOUPÉ (md5 0825dace… — 1 209 o, la ligne
     d'échec [SESSION] DANS la pièce) ;
  2. LE DOSSIER D'ARCHIVE né aux archives-preuves :
     preuves-run-loupe-dev5/ ;
  3. LE TÉMOIN DÉPLACÉ (addParents/removeParents — DÉPLACEMENT,
     jamais une copie) + md5 recoupé APRÈS ;
  4. LE VERDICT DU RUN déposé dans l'archive (VERDICT-run-loupe-
     dev5.txt : ROUGE AU T1 — ET LA PIÈCE ACQUITÉE, le kit fautif,
     la retouche au kit seul) ;
  5. L'INDEX MIS À JOUR : LISEZMOI-archives-preuves.txt ;
  6. LE RÉCEPTACLE demeure avec son LISEZMOI (preuves-loupe/ —
     ré-armé par la vague dev.6).

Aucune suppression, aucune corbeille ; idempotent par empreintes.
Usage : python3 scripts/archiver_run_loupe_dev5.py
Code de sortie : 0 = témoin archivé ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # dossier « test »
ARCHIVES_PREUVES_ID = "1TRZtOdvqfovvZt0jdFdpMysrpHNKOzFk"  # archives-preuves
INDEX_ID = "1WK5OOuMOFFoUj3PevftZo3pHIFKQx7zu"          # LISEZMOI-archives-preuves

TEMOIN_MD5 = "0825dace302d22d95dcd3e6e62245804"   # le témoin dev.5 (1 209 o)
TEMOIN_SHA = ("f280e0e24dfa9332a9d5a317e6d795309"
              "55b18b6e84b6e90c3acd8b8e3d3eae8")
DOSSIER_ARCHIVE = "preuves-run-loupe-dev5"

VERDICT = """VERDICT DU RUN TERRAIN M10-(e) — LOUPE dev.5 : ROUGE AU T1 (LE PAS LE PLUS LOIN) — ET LA PIÈCE ACQUITÉE, LE KIT FAUTIF
====================================================================================================================
Le run du 09/11/2026 (la vague dev.5, la retouche de l'Entrée 207 —
le témoin déposé par le développeur au réceptacle
/test/preuves-loupe/) :

  - [T0] TOUT LE TÉMOIN VERT : l'empreinte ASSERTÉE (loupe.exe
    127 488 o, sha256 6f830f9c738265df… — l'artefact dev.5
    AUTHENTIQUE), l'image cartographiée DONT_RESOLVE @ 0x7ff646600000,
    LE CADRE NÉ LE MIROIR DU CADRE_VIERGE (la poignée INVALIDE à
    +528, le .data entier relu — LA RETOUCHE DE L'ENTRÉE 206 TENUE
    AU TERRAIN, DEUXIÈME PREUVE), les adresses scellées CONSTATÉES
    (la minilibc M1, la boucle démo, la famille sha M9, la table K
    FIPS, la porte R10 0x00010005), l'IAT 37 feuilles posées.
  - [T1] ÉCHEC NOMMÉ [SESSION] : « loupe-01 a rendu 0xfffffff9 (-7
    VERROUILLÉ, le fichier pourtant relu à l'instant) ».
  - LA VITRINE : « quand je lance l'exe, la fenêtre s'ouvre et se
    referme immédiatement » — rapportée TROIS fois, toujours SANS
    témoin (temoin-vitrine.txt ABSENT du dépôt : le témoin vitrine
    ne fut pas joué — le déficit EST un fait du kit, nommé une
    troisième fois).

L'AUTOPSIE DE LABO SUR LA PIÈCE (capstone aux RVAs scellées) A
ACQUITTÉ LA PIÈCE ET NOMMÉ LE KIT :
  - l'appel CreateFileW de loupe-01 est NÉ PARFAIT dans la pièce :
    rcx = le chemin, rdx = 0xC0000000 (GENERIC_READ|GENERIC_WRITE),
    r8 = 1 (FILE_SHARE_READ), r9 = NUL, [rsp+0x20] = 3
    (OPEN_EXISTING), [rsp+0x28] = 0, [rsp+0x30] = NUL — les
    arguments 5/6/7 À LEURS VRAIS SLOTS (la classe de l'Entrée 207
    corrigée), la pile ≡ 0 (mod 16) à l'appel ;
  - LA PREUVE PAR LE NOM CHANGÉ : dev.4 rendait -6 SYSTÈME [gle 87 :
    l'appel mal né, la disposition lue à la pile non initialisée] ;
    dev.5 rend -7 VERROUILLÉ [gle 32 : l'appel NÉ, refusé pour une
    RAISON RÉELLE] — la retouche de l'Entrée 207 A TENU AU TERRAIN ;
  - LA RAISON RÉELLE EST LE KIT LUI-MÊME : le scénario EST LE
    CHARGEUR — LoadLibraryEx DONT_RESOLVE TIENT loupe.exe ouvert
    comme SECTION VIVANTE (sans partage d'écriture), et le VRAI
    Windows refuse gle 32 d'ouvrir À L'ÉCRITURE le fichier d'une
    image mappée : T1 offrait LA PIÈCE ELLE-MÊME à l'écriture — un
    geste IMPOSSIBLE PAR CONSTRUCTION, invisible aux runs
    précédents parce qu'aucun appel n'était jamais assez bien né
    pour atteindre le partage ;
  - LOUPE-01 A TRADUIT LE REFUS AU NOM PRÈS (I4/E2 : gle 32 → -7
    VERROUILLÉ) : LA VOIE NOMMÉE DE L'ÈRE A VÉCU SON PREMIER
    TERRAIN — un refus vaut plus qu'un vert muet, et CE refus est
    le premier VÉCU de l'application chez son utilisateur ;
  - LA VITRINE RELUE STATIQUEMENT (le témoin vitrine absent, le
    labo relit la pièce) : win-03 héritée ✓ (hWnd NUL, filtres NULS,
    la pile alignée), WinMain ✓ (la classe, la fenêtre, ShowWindow,
    la boucle, ExitProcess), LA PROCÉDURE ✓ (le routage, la pile
    alignée), loupe-10 ✓ (BeginPaint, la géométrie, les bornes), le
    sous-programme .peindre ✓ (l'Entrée 207 : l'argument 5 AU VRAI
    SLOT, l'alignement sub/add 8) — les DEUX morts de dev.4
    s'expliquent par les DEUX défauts SSE corrigés (le contexte SHA
    au vrai slot ; .peindre ≡8) : LA VOIE SANS DÉFAUT CONNU, la vitrine
    dev.5 n'a plus de défaut CONNU — mais elle sera VÉCUE PAR SON
    TÉMOIN ou elle ne sera pas recoupée.

LA RETOUCHE DE L'ENTRÉE 208 EST AU KIT SEUL — LA PIÈCE INCHANGÉE
(6f830f9c…, acquittée ; AUCUN arbre signé touché, aucune adresse
scellée déplacée, aucun build rejoué) :
  1. L'OMBRE : la session T1 naît sur temoin-session.bin, LA COPIE
     byte-à-byte de la pièce (empreinte ASSERTÉE après la copie),
     née et morte au run — même loi que la sonde 205 (les copies
     %TEMP%) et le témoin vitrine (temoin-fichier.bin) ; T2 juge la
     pièce SUR SON OMBRE (byte-à-byte la même, l'empreinte la
     même) ;
  2. LE FRÈRE chassé par la classe : la session double de T6
     offrait elle aussi loupe.exe sous le chargeur (premier appel
     de retour non vérifié — eût rendu -7 et FAUSSÉ le -5 attendu)
     — l'offrande est L'OMBRE, le premier appel VÉRIFIÉ né (r=0), le
     second → -5 ;
  3. LA VITRINE SE VIT PAR SON TÉMOIN : temoin-vitrine.bat ASCII
     rejoué (les étapes nommées, les fenêtres documentées), le
     LISEZMOI le dit noir sur blanc, temoin-vitrine.txt REQUIS au
     réceptacle — une mort sans témoin ne recoupe pas.

Le témoin de ce run (temoin-loupe.txt, 1 209 o, md5 0825dace…,
sha256 f280e0e2…) est archivé ICI par DÉPLACEMENT avec le présent
verdict — le refus est un FAIT, la pièce demeure ACQUITTEE, le kit
corrige son geste. preuves-loupe/ demeure LE réceptacle (ré-armé par
la vague dev.6). Le labo recoupe sur pièces (D138/D145/D148) ;
la balise `loupe 0.1.0` attend le vert recoupé : LE JALON M10.
"""

NOTE_INDEX = """
preuves-run-loupe-dev5/  LE CINQUIÈME RUN TERRAIN M10-(e) — le run
                         loupe dev.5 du 09/11/2026 : [T0] TOUT VERT
                         (l'empreinte dev.5 ASSERTÉE 6f830f9c…, le
                         CADRE NÉ MIROIR — la retouche de l'Entrée
                         206 tenue DEUXIÈME fois, l'IAT 37 feuilles)
                         PUIS [T1] ÉCHEC NOMMÉ [SESSION] : loupe-01
                         a rendu -7 VERROUILLÉ (le fichier pourtant
                         relu à l'instant) — ET LA PIÈCE EST
                         ACQUITÉÉ : l'appel était né PARFAIT (les
                         arguments 5+ aux vrais slots — la classe de
                         l'Entrée 207 TENUE, PREUVE PAR LE NOM
                         CHANGÉ : -6 SYSTÈME devint -7 VERROUILLÉ),
                         c'est LE KIT QUI FAUTAIT (le scénario EST LE
                         CHARGEUR : l'image TIENT loupe.exe, et le
                         VRAI Windows refuse gle 32 l'écriture sur
                         une section vivante — T1 offrait la pièce à
                         l'écriture, impossible PAR CONSTRUCTION) ;
                         loupe-01 a traduit le refus AU NOM PRÈS —
                         LA VOIE NOMMÉE A VÉCU SON PREMIER TERRAIN.
                         Pièces : temoin-loupe.txt (1 209 o, md5
                         0825dace… — l'empreinte ASSERTÉE, les [T0]
                         constatés, la ligne [SESSION]) +
                         VERDICT-run-loupe-dev5.txt (l'autopsie :
                         la pièce ACQUITTEE, le kit fautif ; la
                         retouche de l'Entrée 208 AU KIT SEUL :
                         L'OMBRE temoin-session.bin, le frère de T6
                         chassé, LA VITRINE PAR SON TÉMOIN). Le
                         témoin DÉPLACÉ du réceptacle du développeur
                         (/test/preuves-loupe/) par DÉPLACEMENT
                         (D143) ; preuves-loupe/ demeure LE
                         réceptacle (ré-armé par la vague dev.6).
"""


def refus(nom, detail):
    print(f"[archive] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def main():
    print("=== M10-(e) : LE TÉMOIN DU RUN dev.5 ARCHIVÉ SUR PIÈCES "
          "(D143 — l'Entrée 208) ===")

    # -- 1. le témoin au réceptacle du développeur, recoupé ------------------
    test = ds.list_folder(TEST_ID)
    receptacle = test.get("preuves-loupe")
    if not receptacle or receptacle.get("mimeType") != ds.FOLDER_MIME:
        refus("RÉCEPTACLE", "/test/preuves-loupe/ introuvable au /test")
    temoin = ds.list_folder(receptacle["id"]).get("temoin-loupe.txt")
    if temoin is None:
        deja = ds.list_folder(ARCHIVES_PREUVES_ID).get(DOSSIER_ARCHIVE)
        if deja:
            arch = ds.list_folder(deja["id"])
            if arch.get("temoin-loupe.txt", {}).get("md5Checksum") == TEMOIN_MD5:
                print("[1] le témoin déjà archivé — idempotent")
                return 0
        refus("TÉMOIN", "temoin-loupe.txt introuvable au réceptacle ET à "
                        "l'archive")
    md5_avant = temoin.get("md5Checksum")
    if md5_avant != TEMOIN_MD5:
        refus("TÉMOIN", f"md5 {md5_avant} != l'attendu {TEMOIN_MD5} — "
                        "ce n'est pas le témoin du run dev.5")
    url = (ds.API + f"/files/{temoin['id']}?alt=media")
    st, corps, _ = ds.api("GET", url)
    if st != 200 or md5_bytes(corps) != TEMOIN_MD5:
        refus("TÉMOIN", "le téléchargement ne recoupe pas le md5")
    if hashlib.sha256(corps).hexdigest() != TEMOIN_SHA:
        refus("TÉMOIN", "le téléchargement ne recoupe pas le sha256")
    print(f"[1] le témoin dev.5 recoupé : {len(corps)} o, md5 {md5_avant[:8]}…, "
          f"sha256 {TEMOIN_SHA[:16]}… — la ligne [SESSION] DANS la pièce")

    # -- 2. le dossier d'archive né ------------------------------------------
    archives = ds.list_folder(ARCHIVES_PREUVES_ID)
    dossier = archives.get(DOSSIER_ARCHIVE)
    if dossier is None:
        dossier_id = ds.create_folder(ARCHIVES_PREUVES_ID, DOSSIER_ARCHIVE)
        print(f"[2] {DOSSIER_ARCHIVE}/ né aux archives-preuves")
    else:
        dossier_id = dossier["id"]
        print(f"[2] {DOSSIER_ARCHIVE}/ déjà présent — idempotent")

    # -- 3. le témoin DÉPLACÉ (addParents/removeParents) ---------------------
    url = (ds.API + f"/files/{temoin['id']}"
           f"?addParents={dossier_id}&removeParents={receptacle['id']}")
    st, rep, _ = ds.api("PATCH", url, body={})
    if st not in (200, 201):
        refus("DÉPLACEMENT", f"HTTP {st} : {rep[:150]!r}")
    apres = ds.list_folder(dossier_id).get("temoin-loupe.txt")
    if (not apres or apres.get("md5Checksum") != TEMOIN_MD5
            or "temoin-loupe.txt" in ds.list_folder(receptacle["id"])):
        refus("DÉPLACEMENT", "md5 divergent ou la pièce demeure au réceptacle "
                             "après le geste")
    print(f"[3] temoin-loupe.txt DÉPLACÉ → {DOSSIER_ARCHIVE}/ "
          f"(md5 {TEMOIN_MD5[:8]}… recoupé APRÈS — le refus est un FAIT, "
          f"la pièce demeure ACQUITTÉE)")

    # -- 4. le verdict du run déposé dans l'archive ---------------------------
    verdict = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev5.txt")
    if verdict is None:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                          encoding="utf-8",
                                          newline="\r\n") as f:
            f.write(VERDICT)
            chemin = f.name
        try:
            ds.upload_create(dossier_id, "VERDICT-run-loupe-dev5.txt",
                             pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        apres = ds.list_folder(dossier_id).get("VERDICT-run-loupe-dev5.txt")
        if not apres:
            refus("VERDICT", "absent après le dépôt")
        print(f"[4] VERDICT-run-loupe-dev5.txt déposé ({apres.get('size', 0)} o "
              "— le dossier porte le jugement AVEC les pièces)")
    else:
        print("[4] VERDICT-run-loupe-dev5.txt déjà présent — idempotent")

    # -- 5. l'index LISEZMOI-archives-preuves.txt mis à jour ------------------
    idx = ds.list_folder(ARCHIVES_PREUVES_ID).get(
        "LISEZMOI-archives-preuves.txt")
    if idx:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={idx['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "preuves-run-loupe-dev5/" not in ancien:
            marque = "— Fin de l'index (aucune allégation sans pièce citée) —"
            nouveau = ancien.replace(
                marque, NOTE_INDEX + "\n" + marque) if marque in ancien \
                else ancien.rstrip("\n") + "\n" + NOTE_INDEX
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                             encoding="utf-8",
                                             newline="\r\n") as f:
                f.write(nouveau)
                chemin = f.name
            try:
                ds.upload_update(idx["id"], pathlib.Path(chemin))
            finally:
                os.unlink(chemin)
            print("[5] LISEZMOI-archives-preuves.txt mis à jour "
                  "(l'entrée preuves-run-loupe-dev5/ AVANT la fin de l'index)")
        else:
            print("[5] l'index porte déjà dev5 — idempotent")
    else:
        print("[5] LISEZMOI-archives-preuves.txt introuvable — nommé, non fatal")

    print("=== LE TÉMOIN dev.5 ARCHIVÉ — la pièce ACQUITTÉE, le kit corrige "
          "son geste (l'Entrée 208) ; preuves-loupe/ ré-armé par la vague "
          "dev.6 ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
