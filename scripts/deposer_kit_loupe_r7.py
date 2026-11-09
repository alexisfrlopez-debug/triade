#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deposer_kit_loupe_r7.py — LE COFFRE /test PASSÉ À LA VAGUE LOUPE dev.8
(LA RETOUCHE DE L'ENTRÉE 210, LA DOUBLE : la pièce dev.7 + le kit dev.8 —
règle D143 : archivage par DÉPLACEMENT, jamais un jet).

LE SEPTIÈME RUN TERRAIN (l'Entrée 210) : T0→T5 TOUT VERT — LA SAUVEGARDE
DE L'ENTRÉE 209 PROUVÉE AU TERRAIN, la boucle d'édition ENTIÈRE vivante —
puis le témoin a nommé DEUX DÉFAUTS D'UN MÊME GESTE : [EAX-SANS-SIGNE] AU
KIT (T6 lisait « 0xfffffffe != -2 » : la pièce rendait « mov eax, imm32 »,
le contrat c_int64 lisait le qword entier) ET [D54-QUATRIÈME] À LA PIÈCE
(la vitrine demeurait morte ×2 0xC0000005 : les QUATRE plages FirstThunk
CONTIGUËS — le chargeur du terrain marche chaque plage jusqu'au NULL, la
marche de kernel32 déborde chez user32, RegisterClassExW résout à NULL,
l'entrée appelle le NUL).

ET LE TERRAIN A NOMMÉ LE COFFRE LUI-MÊME : « le kit n'était pas dans le
drive, il faudrait que le prochain y soit » — la vague dev.7 avait voyagé
HORS coffre (le zip par le canal du bac à sable, le labo n'avait pas le
droit d'écriture au /test). LE DÉVELOPPEUR A OUVERT LE CHEMIN : le dossier
/tokens du Drive porte les jetons (OAuth relais + GitHub) — le labo
DÉPOSE désormais lui-même. LA VAGUE dev.8 EST LA PREMIÈRE DÉPOSÉE AU
COFFRE PAR LE LABO.

  1. ARCHIVAGE DE LA VAGUE dev.6 (racine, consommée par le sixième run,
     recoupée à l'Entrée 209) → /test/archives-livraisons/vagues-m10/
     EN PIÈCES VERSIONNÉES : kit-loupe.zip → kit-loupe-dev.6.zip +
     LISEZMOI-loupe.txt → LISEZMOI-loupe-dev.6.txt (déplacement PATCH,
     md5 constaté après) ;
  2. LA VAGUE dev.7 RATTRAPÉE AUX ARCHIVES : elle ne passa JAMAIS par la
     racine du coffre (canal bac à sable) — ses pièces versionnées
     rejoignent l'archive pour l'histoire : kit-loupe-dev.7.zip (le zip
     tel que vécu par le terrain) + LISEZMOI-loupe-dev.7.txt (le
     document de la vague) ;
  3. LA VAGUE dev.8 DÉPOSÉE à la racine de /test : kit-loupe.zip
     (loupe-kit-8/ : loupe.exe 0.1.0-dev.7 sha256 388d4680… +
     scenario-loupe.py dev.8 + temoin-vitrine.bat + LISEZMOI — md5
     MATCH par relecture) + LISEZMOI-loupe.txt (le document du kit
     dev.8) ;
  4. LE KIT VISIBLE EN DOSSIER : loupe-kit-8/ au /test — la forme
     dossier pour le développeur (le geste de l'Entrée 210 : « le
     prochain kit y sera ») — EXACTEMENT les QUATRE pièces du contrat
     du LISEZMOI (les témoins NAISSENT au run : le bat copie
     temoin-fichier.bin, le scénario pose l'ombre temoin-session.bin —
     les pièces prématurées de la première dépose sont retirées) ;
  5. preuves-loupe/LISEZMOI-preuves.txt MIS À JOUR (l'artefact attendu :
     0.1.0-dev.7, LE CONTRÔLE D54 en tête de T0, LE TÉMOIN VITRINE
     REQUIS) ;
  6. L'INDEX MIS À JOUR : LISEZMOI-archives-livraisons.txt (les vagues
     dev.6 archivée + dev.7 rattrapée + la courante dev.8) ;
  7. VÉRIFICATION : la racine porte la vague courante dev.8 + LES PIÈCES
     DE L'ÈRE DU TGN DEMEURÉES (signatures-I.txt + cle-publique-I.txt —
     la vague ne les touche JAMAIS).

Usage : python3 scripts/deposer_kit_loupe_r7.py
Code de sortie : 0 = coffre passé à la vague dev.8 ; 2 = refus nommé."""

import hashlib
import os
import pathlib
import sys
import tempfile
import zipfile

REPO = "/home/z/my-project/triade"
sys.path.insert(0, os.path.join(REPO, "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"   # dossier « test » du développeur

KIT_ZIP = "/home/z/my-project/download/kit-loupe.zip"
LISEZMOI_KIT = os.path.join(REPO, "loupe", "terrain", "LISEZMOI-KIT-LOUPE.md")
KIT8_DOSSIER_LOCAL = "/home/z/my-project/build-dev7/loupe-kit-8"

# la vague dev.7 (rattrapée aux archives — elle voyagea par le bac à sable)
KIT7_ZIP = "/home/z/my-project/download/kit-loupe-7.zip"
LISEZMOI_KIT7 = "/home/z/my-project/loupe-kit-7/LISEZMOI-KIT-LOUPE.md"

# la vague dev.8 (la retouche de l'Entrée 210 — la pièce dev.7 + le kit dev.8)
KIT_SHA = ("28bafb65e6f3defe8c2d7653985c02a5"
           "039378fbaf032c94a112c5bd37aa1a58")
KIT_MD5 = "33b7ff3e52d89abbc3e592567e2c5003"
EXE_SHA = ("388d468067cbf05411a6227c5906baa2"
           "7d5cbf8a6f862e4cec6a051cab4d9bbc")
KIT7_MD5 = "5f9352237980dee1423c64cc70966416"

# la vague dev.6 (consommée par le sixième run, recoupée à l'Entrée 209)
ANCIEN_KIT_MD5 = "0a50bd7abc10ee5846aca0e4f4502ac0"
ANCIEN_LISEZMOI_MD5 = "671af4da796ef7e9ec23e9fdf2e085e7"

# les pièces de cérémonie qui DEMEURENT à la racine (l'ère du TGN)
PIECES_ERE = {"signatures-I.txt": "f33c803aad80711995c6ea61ce30aa7b",
              "cle-publique-I.txt": "188a7d42df2d03f68bfb50fada3a84a1"}

LISEZMOI_PREUVES_R7 = """TRIADE — preuves-loupe : LE RÉCEPTACLE DU RUN TERRAIN M10-(e)
========================================================================
(LE RUN DE LOUPE, LE GRANDEUR NATURE : la première application née de
TRIADE chez son utilisateur ; l'artefact attendu 0.1.0-dev.7, sha256
388d468067cbf054… — LA RETOUCHE DE L'ENTRÉE 210 : [D54-QUATRIÈME]
chassé [l'IAT ENTIÈRE relogée à 0x3100 : QUATRE plages FirstThunk
SÉPARÉES PAR NULL et PRÉREMLIES des RVA de noms, le motif D54 au
complet — le chargeur du terrain marche le chemin FirstThunk : des
plages contiguës tuaient la vitrine avant l'entrée, 0xC0000005 sans
dialogue] ET [EAX-SANS-SIGNE] étendu [chaque rendu négatif au 64
bits : « push imm8 ; pop rax », le contrat c_int64 lu exact — le kit
dev.8 MARQUE LUI-MÊME l'habillage d'import au T0 : chaque plage
marchée au compte exact, les séparateurs NULL, les slots préremplis ;
l'affichage de la version est DYNAMIQUE {VERSION_R10}] ; la carte
génération 15 — la balise `loupe 0.1.0` se scellera sur le vert
recoupé)

LES PIÈCES ATTENDUES (nées dans ./preuves-loupe/ du kit dézippé, à
glisser ICI EN ENTIER après le run — ou dans le dossier du kit, le
labo recoupe de toute pièce) :

  temoin-vitrine.txt   LE TÉMOIN VITRINE — REQUIS (une mort sans
                       témoin ne recoupe pas, l'Entrée 208) — né par
                       temoin-vitrine.bat : LES DEUX codes de sortie
                       (la fenêtre vide sans fichier, puis avec la
                       copie temoin-fichier.bin : la session naît
                       entière) et le rapport WER s'il y eut crash —
                       **0 ET 0 SONT ATTENDUS À L'ENTRÉE 210 : la
                       vitrine dev.7 est née pour VIVRE** ;
  temoin-loupe.txt     le témoin complet — l'environnement (Windows,
                       Python 64 bits), l'empreinte ASSERTÉE de
                       l'artefact, LE .data ENTIER relu contre LE
                       MIROIR du CADRE_VIERGE, les adresses scellées
                       CONSTATÉES, LE CONTRÔLE D54 en tête [les
                       quatre plages marchées au compte exact :
                       10 · 18 · 6 · 3], l'IAT résolue par le
                       scénario-chargeur, chaque contrôle tranché (la
                       session sur L'OMBRE byte-à-byte de la pièce,
                       la double lecture, les lignes, la recherche,
                       l'édition à l'octet, les rejets nommés au
                       contrat c_int64, la clôture) ET LA SONDE DE
                       L'ENTRÉE 205 (P0..P4) ;
  capture-*.png        LES CAPTURES DE LA VITRINE (optionnelles mais
                       bienvenues) : la fenêtre réelle après ouverture
                       d'un fichier de votre choix — l'entête, la
                       grille hexa, le miroir ASCII, LE PANNEAU
                       D'EMPREINTES (md5 + sha256) — la vie de
                       l'application chez vous, le cœur du grandeur
                       nature.

LE GESTE (D99) : dézippez kit-loupe.zip dans un dossier NEUF — si le
dossier d'un run dev.1 à dev.7 existe encore, NE LE RÉUTILISEZ PAS
(loupe-kit-8/ par exemple — un dossier neuf par run ; le dossier
loupe-kit-8/ du coffre Drive EST le kit lui-même, prêt à courir).

LE CRITÈRE (le plan M10, rangée (e)) : le développeur court LOUPE sur
SA machine — le VRAI Windows 11, les VRAIS fichiers, la VRAIE vitrine
— le run VERT sur pièces + le recoup labo N/N sur pièces croisées →
la balise `loupe 0.1.0` SCELLÉE (fait de carte, D104) : LE JALON M10,
la méthode TRIADE entière prouvée par la CRÉATION.

Un verdict ROUGE se renvoie TEL QUEL : la ligne d'échec NOMME le
défaut (chaque défaut a été nommé, chaque défaut a reçu sa retouche —
sept runs, sept leçons). Le labo recoupe sur pièces (D138/D145/D148).
"""

NOTE_INDEX = """
--- la vague loupe dev.6 archivée après LE SIXIÈME RUN TERRAIN (le run
    du 09/11, recoupé à l'Entrée 209 : T0→T4 VERTS puis [T5] ÉCHEC NOMMÉ
    [SAUVEGARDE] — « loupe-17 → OK (1 octet écrit attendu) » — ET LA
    PREUVE ÉTAIT DANS LE FICHIER : temoin-edition.bin portait 0x4D à
    l'octet 0, la taille constante — LA SAUVEGARDE AVAIT EU LIEU, c'est
    l'attente du scénario qui fautait [le contrat publié de loupe-17 :
    0 = OK] ; ET la vitrine morte ×2 0xC0000005 — [HINSTANCE-PEB] nommé
    par l'autopsie : le RCX brut du point d'entrée pris pour hInstance,
    GetModuleHandleW importé mais jamais câblé ; kit-loupe.zip md5
    0a50bd7a… + LISEZMOI-loupe.txt 671af4da… → vagues-m10/ EN PIÈCES
    VERSIONNÉES [kit-loupe-dev.6.zip + LISEZMOI-loupe-dev.6.txt] ;
    le témoin du run : temoin-loupe.txt 2 335 o md5 5cb3014f… +
    temoin-vitrine.txt 389 o md5 bebad29e… archivés à
    archives-preuves/preuves-run-loupe-dev6/ AVEC le verdict)

--- la vague loupe dev.7 RATTRAPÉE aux archives (elle ne passa JAMAIS
    par la racine du coffre : le labo n'avait pas le droit d'écriture
    au /test, le zip voyagea par le canal du bac à sable — le terrain
    l'a vécue en loupe-kit-7/ ; le septième run, recoupé à l'Entrée
    210 : T0→T5 TOUT VERT — LA SAUVEGARDE PROUVÉE, la boucle d'édition
    ENTIÈRE vivante — puis [T6] ÉCHEC NOMMÉ [REJET-ABSENT] :
    « 0xfffffffe != -2 » [EAX-SANS-SIGNE : la pièce rendait « mov eax,
    imm32 », le contrat c_int64 lisait le qword entier] ET la vitrine
    morte ×2 [D54-QUATRIÈME : les QUATRE plages FirstThunk contiguës,
    le chargeur marche chaque plage jusqu'au NULL — la marche de
    kernel32 déborde chez user32, RegisterClassExW résout à NULL,
    l'entrée appelle le NUL] ; ses pièces versionnées jointes à
    l'archive pour l'histoire : kit-loupe-dev.7.zip md5 5f935223… +
    LISEZMOI-loupe-dev.7.txt ; le témoin du run : temoin-loupe.txt
    2 598 o md5 c199de74… + temoin-vitrine.txt 389 o md5 4077286f…
    archivés à archives-preuves/preuves-run-loupe-dev7/ AVEC le
    verdict)

--- la vague courante (racine de /test) : loupe dev.8 — LA RETOUCHE
    DE L'ENTRÉE 210, LA DOUBLE (kit-loupe.zip md5 33b7ff3e… +
    LISEZMOI-loupe.txt ; loupe.exe 0.1.0-dev.7, 127 488 o, sha256
    388d4680… — l'IAT ENTIÈRE relogée à 0x3100 : QUATRE plages
    SÉPARÉES PAR NULL, préremplies du motif D54, les 63 sites
    d'appel repointés, les vieilles plages vidées ; ET les rendus
    négatifs étendus au 64 bits ; R7 tenue : le WndProc @0x5DCB, la
    famille sha M9, la minilibc M1, la table K[64], le CADRE — octets
    inchangés ; le qword version 0x00010007 ; ET LE SCÉNARIO dev.8 :
    LE CONTRÔLE D54 au T0 — le scénario MARCHE lui-même les quatre
    plages au compte exact [10 · 18 · 6 · 3], l'affichage de la
    version DYNAMIQUE) — livrée le 09/11/2026 ; **LA PREMIÈRE VAGUE
    DÉPOSÉE AU COFFRE PAR LE LABO LUI-MÊME** (le développeur a ouvert
    le chemin : le dossier /tokens du Drive porte les jetons — la
    réponse au constat du terrain « le kit n'était pas dans le drive,
    il faudrait que le prochain y soit » : IL Y EST, déposé par le
    labo, en la forme canonique kit-loupe.zip + LISEZMOI ET en la
    forme dossier loupe-kit-8/ prête à courir) ; la balise `loupe
    0.1.0` attend le vert recoupé : LE JALON M10.
"""


def refus(nom, detail):
    print(f"[dépôt] REFUS {nom} : {detail}")
    sys.exit(2)


def md5_bytes(b):
    return hashlib.md5(b).hexdigest()


def deplacer_versionne(fichier, destination_id, nouveau_nom, md5_attendu):
    """D143 : le déplacement VERSIONNÉ, md5 recoupé APRÈS."""
    url = (ds.API + f"/files/{fichier['id']}"
           f"?addParents={destination_id}&removeParents={fichier['parent']}")
    try:
        st, rep, _ = ds.api("PATCH", url, body={"name": nouveau_nom})
    except ds.SyncError as e:
        refus("ARCHIVAGE", f"{fichier['name']} : {e}")
    if st not in (200, 201):
        refus("ARCHIVAGE", f"{fichier['name']} : HTTP {st} : {rep[:150]!r}")
    archive = ds.list_folder(destination_id).get(nouveau_nom)
    if not archive or archive.get("md5Checksum") != md5_attendu:
        refus("ARCHIVAGE", f"{nouveau_nom} : md5 divergent après déplacement")
    print(f"    archivé VERSIONNÉ : {fichier['name']} → {nouveau_nom} "
          f"(md5 {md5_attendu[:8]}… recoupé après)")


def televerser_texte(parent_id, nom, contenu):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8", newline="\r\n") as f:
        f.write(contenu)
        chemin = f.name
    try:
        return ds.upload_create(parent_id, nom, pathlib.Path(chemin))
    finally:
        os.unlink(chemin)


def main():
    print("=== M10-(e) r7 : le coffre /test passe à LA VAGUE LOUPE dev.8 "
          "(la retouche double de l'Entrée 210) — LA PREMIÈRE DÉPOSÉE PAR "
          "LE LABO (les jetons du /tokens) ===")

    # -- 0. le kit local, vérifié ------------------------------------------------
    if not os.path.isfile(KIT_ZIP):
        refus("KIT", f"{KIT_ZIP} absent — assembler la vague dev.8 d'abord")
    octets = open(KIT_ZIP, "rb").read()
    if hashlib.sha256(octets).hexdigest() != KIT_SHA:
        refus("KIT", "kit-loupe.zip sha256 divergent — réassembler")
    if md5_bytes(octets) != KIT_MD5:
        refus("KIT", "kit-loupe.zip md5 divergent — réassembler")
    z = zipfile.ZipFile(KIT_ZIP)
    exe = z.read("loupe-kit-8/loupe.exe")
    if hashlib.sha256(exe).hexdigest() != EXE_SHA:
        refus("KIT", "loupe.exe interne sha256 divergent — la pièce dev.7 "
                     "attendue (388d4680…)")
    print(f"[0] le kit dev.8 : {len(octets)} o, md5 {KIT_MD5[:8]}…, sha256 "
          f"{KIT_SHA[:16]}… — la pièce interne dev.7 ASSERTÉE "
          f"({EXE_SHA[:16]}…) — l'épreuve d'extraction est VERTE")
    if not os.path.isfile(LISEZMOI_KIT):
        refus("KIT", f"{LISEZMOI_KIT} absent — le document de la vague")
    if not os.path.isfile(KIT7_ZIP) or not os.path.isfile(LISEZMOI_KIT7):
        refus("KIT", "les pièces de la vague dev.7 (kit-loupe-7.zip / "
                     "LISEZMOI) manquent au bac à sable")
    if md5_bytes(open(KIT7_ZIP, "rb").read()) != KIT7_MD5:
        refus("KIT", "kit-loupe-7.zip md5 divergent — la pièce de la vague "
                     "dev.7 telle que vécue par le terrain")

    test = ds.list_folder(TEST_ID)
    arch_l = test.get("archives-livraisons")
    if not arch_l:
        refus("ÉTAT", "archives-livraisons/ introuvable au /test")

    # -- 1. archivage de la vague dev.6 (consommée par le sixième run) --------
    vagues = ds.list_folder(arch_l["id"]).get("vagues-m10")
    if not vagues:
        vagues_id = ds.create_folder(arch_l["id"], "vagues-m10")
        print("[1] vagues-m10/ créé aux archives-livraisons")
    else:
        vagues_id = vagues["id"]
    racine = ds.list_folder(TEST_ID)
    for nom, nouveau_nom, ancien_md5 in (
            ("kit-loupe.zip", "kit-loupe-dev.6.zip", ANCIEN_KIT_MD5),
            ("LISEZMOI-loupe.txt", "LISEZMOI-loupe-dev.6.txt",
             ANCIEN_LISEZMOI_MD5)):
        piece = racine.get(nom)
        if piece is None:
            deja = ds.list_folder(vagues_id).get(nouveau_nom)
            if deja:
                print(f"[1] {nouveau_nom} déjà archivé — idempotent")
            else:
                print(f"[1] {nom} absent de la racine — nommé, non fatal")
            continue
        md5_avant = piece.get("md5Checksum")
        if md5_avant == KIT_MD5 or md5_avant == md5_bytes(
                open(LISEZMOI_KIT, "rb").read()):
            print(f"[1] {nom} à la racine est déjà la vague dev.8 — rien à "
                  f"archiver")
            continue
        if md5_avant != ancien_md5:
            refus("ARCHIVAGE", f"{nom} à la racine a un md5 inconnu "
                               f"({md5_avant}) — ni dev.6 ni dev.8, refus")
        deplacer_versionne({"id": piece["id"], "name": nom, "parent": TEST_ID},
                           vagues_id, nouveau_nom, md5_avant)

    # -- 2. la vague dev.7 rattrapée aux archives --------------------------------
    for nom_local, nom_archive, md5_attendu in (
            (KIT7_ZIP, "kit-loupe-dev.7.zip", KIT7_MD5),
            (LISEZMOI_KIT7, "LISEZMOI-loupe-dev.7.txt",
             md5_bytes(open(LISEZMOI_KIT7, "rb").read()))):
        deja = ds.list_folder(vagues_id).get(nom_archive)
        if deja:
            if deja.get("md5Checksum") != md5_attendu:
                refus("RATTRAPAGE", f"{nom_archive} déjà présent avec un "
                                    f"AUTRE md5")
            print(f"[2] {nom_archive} déjà rattrapé — idempotent")
            continue
        ds.upload_create(vagues_id, nom_archive, pathlib.Path(nom_local))
        apres = ds.list_folder(vagues_id).get(nom_archive)
        if not apres or apres.get("md5Checksum") != md5_attendu:
            refus("RATTRAPAGE", f"{nom_archive} md5 divergent après "
                                "téléversement")
        print(f"[2] la vague dev.7 rattrapée : {nom_archive} (md5 "
              f"{md5_attendu[:8]}… MATCH par relecture)")

    # -- 3. la vague dev.8 déposée à la racine -------------------------------------
    racine = ds.list_folder(TEST_ID)
    if "kit-loupe.zip" not in racine:
        ds.upload_create(TEST_ID, "kit-loupe.zip", pathlib.Path(KIT_ZIP))
        apres = ds.list_folder(TEST_ID).get("kit-loupe.zip")
        if not apres or apres.get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip md5 divergent après téléversement")
        print(f"[3] déposé : kit-loupe.zip (md5 {KIT_MD5[:8]}… MATCH par "
              f"relecture)")
    else:
        if racine["kit-loupe.zip"].get("md5Checksum") != KIT_MD5:
            refus("DÉPÔT", "kit-loupe.zip déjà présent avec un AUTRE md5")
        print("[3] kit-loupe.zip déjà déposé — idempotent")

    local_md5 = md5_bytes(open(LISEZMOI_KIT, "rb").read())
    actuel = ds.list_folder(TEST_ID).get("LISEZMOI-loupe.txt")
    if actuel is None:
        ds.upload_create(TEST_ID, "LISEZMOI-loupe.txt",
                         pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-loupe.txt")
        if not apres or apres.get("md5Checksum") != local_md5:
            refus("DÉPÔT", "LISEZMOI-loupe.txt md5 divergent après "
                           "téléversement")
        print(f"[3] déposé : LISEZMOI-loupe.txt (md5 {local_md5[:8]}… MATCH)")
    elif actuel.get("md5Checksum") != local_md5:
        ds.upload_update(actuel["id"], pathlib.Path(LISEZMOI_KIT))
        apres = ds.list_folder(TEST_ID).get("LISEZMOI-loupe.txt")
        if apres.get("md5Checksum") != local_md5:
            refus("DÉPÔT", "LISEZMOI-loupe.txt md5 divergent après mise à "
                           "jour")
        print(f"[3] mis à jour : LISEZMOI-loupe.txt (md5 {local_md5[:8]}… "
              f"MATCH)")
    else:
        print("[3] LISEZMOI-loupe.txt déjà à jour — idempotent")

    # -- 4. le kit visible en dossier : loupe-kit-8/ --------------------------------
    dossier = ds.list_folder(TEST_ID).get("loupe-kit-8")
    if not dossier:
        refus("DOSSIER", "loupe-kit-8/ introuvable au /test — la forme "
                         "dossier du kit (déposée en tête de session)")
    contenu = ds.list_folder(dossier["id"])
    attendus = {}
    for f in ("loupe.exe", "scenario-loupe.py", "temoin-vitrine.bat",
              "LISEZMOI-KIT-LOUPE.md"):
        chemin = os.path.join(KIT8_DOSSIER_LOCAL, f)
        attendus[f] = md5_bytes(open(chemin, "rb").read())
    for f, md5_attendu in attendus.items():
        p = contenu.get(f)
        if not p or p.get("md5Checksum") != md5_attendu:
            refus("DOSSIER", f"loupe-kit-8/{f} absent ou divergent (md5 "
                  f"{md5_attendu[:8]}… attendu)")
    # les témoins NAISSENT au run (le bat copie temoin-fichier.bin, le
    # scénario pose l'ombre) — les pièces prématurées de la première
    # dépose sont retirées au contrat du LISEZMOI (QUATRE pièces)
    for prematuree in ("temoin-fichier.bin", "temoin-session.bin"):
        p = contenu.get(prematuree)
        if p:
            try:
                ds.api("DELETE", ds.API + f"/files/{p['id']}")
            except ds.SyncError as e:
                refus("DOSSIER", f"{prematuree} : {e}")
            print(f"[4] retirée du dossier (née au run, pas au kit) : "
                  f"{prematuree}")
    # le zip redondant de la première dépose cède la place au canonique
    zip_surnumer = ds.list_folder(TEST_ID).get("loupe-kit-8.zip")
    if zip_surnumer:
        try:
            ds.api("DELETE", ds.API + f"/files/{zip_surnumer['id']}")
        except ds.SyncError as e:
            refus("DOSSIER", f"loupe-kit-8.zip : {e}")
        print("[4] retiré de la racine : loupe-kit-8.zip (la première dépose "
              "de session — le canonique kit-loupe.zip demeure)")
    print(f"[4] le kit visible : loupe-kit-8/ — LES QUATRE PIÈCES du contrat "
          f"du LISEZMOI, md5 recoupés")

    # -- 5. le réceptacle : LISEZMOI-preuves.txt à la vague dev.8 ---------------
    receptacle = ds.list_folder(TEST_ID).get("preuves-loupe")
    if not receptacle:
        refus("RÉCEPTACLE", "preuves-loupe/ introuvable au /test")
    rid = receptacle["id"]
    attendu = md5_bytes(LISEZMOI_PREUVES_R7.replace("\n", "\r\n")
                        .encode("utf-8"))
    deja = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
    if deja and deja.get("md5Checksum") != attendu:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8",
                                         newline="\r\n") as f:
            f.write(LISEZMOI_PREUVES_R7)
            chemin = f.name
        try:
            ds.upload_update(deja["id"], pathlib.Path(chemin))
        finally:
            os.unlink(chemin)
        apres = ds.list_folder(rid).get("LISEZMOI-preuves.txt")
        if apres.get("md5Checksum") != attendu:
            refus("RÉCEPTACLE", "LISEZMOI-preuves.txt md5 divergent après "
                                "mise à jour")
        print("[5] preuves-loupe/LISEZMOI-preuves.txt mis à jour (l'artefact "
              "attendu : 0.1.0-dev.7 + LE CONTRÔLE D54 + LE TÉMOIN VITRINE "
              "REQUIS)")
    elif deja:
        print("[5] LISEZMOI-preuves.txt déjà à jour — idempotent")
    else:
        televerser_texte(rid, "LISEZMOI-preuves.txt", LISEZMOI_PREUVES_R7)
        print("[5] LISEZMOI-preuves.txt né (l'artefact attendu : "
              "0.1.0-dev.7)")

    # -- 6. l'index mis à jour -------------------------------------------------------
    index = ds.list_folder(arch_l["id"]).get("LISEZMOI-archives-livraisons.txt")
    if index:
        import urllib.request
        req = urllib.request.Request(
            f"https://drive.google.com/uc?export=download&id={index['id']}")
        ancien = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        if "la vague courante (racine de /test) : loupe dev.8" not in ancien:
            nouveau = ancien.rstrip("\n") + "\n" + NOTE_INDEX
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                             encoding="utf-8",
                                             newline="\r\n") as f:
                f.write(nouveau)
                chemin = f.name
            try:
                ds.upload_update(index["id"], pathlib.Path(chemin))
            finally:
                os.unlink(chemin)
            print("[6] LISEZMOI-archives-livraisons.txt mis à jour (les "
                  "vagues dev.6 archivée + dev.7 rattrapée + la courante "
                  "dev.8 déposée par le labo)")
        else:
            print("[6] l'index porte déjà la vague dev.8 — idempotent")
    else:
        print("[6] LISEZMOI-archives-livraisons.txt introuvable — nommé, "
              "non fatal")

    # -- 7. vérification finale ------------------------------------------------------
    racine = ds.list_folder(TEST_ID)
    for piece, md5_attendu in PIECES_ERE.items():
        p = racine.get(piece)
        if not p or p.get("md5Checksum") != md5_attendu:
            refus("PIÈCES-DE-L'ÈRE", f"{piece} absent ou divergent au /test "
                  f"— les pièces de cérémonie DEMEURENT (md5 "
                  f"{md5_attendu[:8]}… attendu)")
    k = racine.get("kit-loupe.zip")
    if not k or k.get("md5Checksum") != KIT_MD5:
        refus("ÉTAT-FINAL", "kit-loupe.zip dev.8 absent de la racine")
    if "loupe-kit-8" not in racine:
        refus("ÉTAT-FINAL", "loupe-kit-8/ absent de la racine — la forme "
                            "dossier du kit")
    print(f"[7] LES PIÈCES DE L'ÈRE DEMEURENT : signatures-I.txt "
          f"(f33c803a… la remise INSTALLÉE) + cle-publique-I.txt "
          f"(188a7d42… l'ancre) — la vague ne les a pas touchées")
    print("=== LE COFFRE /test PASSE À LA VAGUE dev.8 — LA PREMIÈRE DÉPOSÉE "
          "PAR LE LABO : kit-loupe.zip + LISEZMOI-loupe.txt à la racine, "
          "loupe-kit-8/ PRÊT À COURIR — le run attend le développeur ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
