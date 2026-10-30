#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Dépôt du kit de cérémonie dans le dossier /Cérémonie du Drive.

Structure posée à la racine du Drive « Triade » (idempotent, chaque
fichier vérifié md5 ALLER-RETOUR après écriture) :

  /Cérémonie/
    ceremonie_gui.py            le maître de cérémonie graphique (D107)
    ceremonie_hors_ligne.py     la cérémonie console de référence (D105)
    LISEZMOI-ceremonie-GUI.txt  le mode d'emploi du GUI (D107)
    LISEZMOI-cle-I.txt          la cérémonie de la clé I, pas à pas (D105)
    LISEZMOI-coffre-CF2.txt     la cérémonie du coffre CF2, pas à pas (D106)
    lancer_ceremonie.bat        lanceur Windows (double-clic, D118)
    lancer_ceremonie.sh         lanceur Linux/macOS (D118)
    coffre_fort.py              le CLI CF1 (changer-phrase D110, migrer)
    MANIFESTE.txt               empreintes du kit (généré au dépôt)
    v06/                        complément « onglets du dépôt » portable :
      __init__.py, ceremonie_gui.py, ceremonie_hors_ligne.py,
      coffre_cf2.py, sceau_I.py, sentinelle_cf2.py

Le sous-dossier v06/ fait du dossier un MINI-DÉPÔT : la page de cérémonie
unifiée du GUI (relais des CLI par RACINE_DEPOT/v06/*.py, import
v06.coffre_cf2) y est opérationnelle sur toute machine connectée. La
vérification des DIX arbres du sceau I exige le dépôt complet (miroir
Drive « TRIADE » ou git) — depuis ce kit seul, l'échec est nommé, par
conception. D118 : les lanceurs vivent À LA RACINE DU DÉPÔT git (un clone
frais les porte) et sont déployés ICI depuis le dépôt — version
intelligente : v06/ceremonie_gui.py d'abord (mini-dépôt complet), repli
sur toute copie posée à côté (fichier seul sur clef USB).

GARDES avant dépôt :
- les 14 sources existent localement ;
- ceremonie_gui.py et ceremonie_hors_ligne.py sont IDENTIQUES (md5)
  entre download/ et v06/ — un kit divergent n'est pas déposé.

Canal d'écriture : l'OAuth relais (refresh_token du 29/10, mode Testing
≈ 7 jours). Le compte de service est Lecteur seul — si l'OAuth meurt,
l'échec est NOMMÉ avec ses parades (partage Éditeur /test au SA, ou
reprise interactive scripts/oauth_echange.py).

Usage :
  python3 scripts/drive_ceremonie.py            # dépose + vérifie
  python3 scripts/drive_ceremonie.py --sonde    # liste sans rien écrire
"""

import datetime
import hashlib
import pathlib
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

ESPACE = pathlib.Path("/home/z/my-project")
DOWNLOAD = ESPACE / "download"
V06 = REPO / "v06"
AUDIT = ESPACE / "scripts"
DOSSIER = "Cérémonie"
SOUS = "v06"
COMMIT_SRC = "06e49f8"          # D118 — la page unifiée + le dossier de
# cérémonie + l'attachement unique + les lanceurs à la racine du dépôt

# (source locale, cible relative dans /Cérémonie) — 14 fichiers
# (coffre_fort.py : posé par D110 — REPRIS dans la liste D112 pour que la
# garde et le manifeste couvrent le kit RÉEL, sinon il vivrait orphelin ;
# lanceurs D118 : sourcés À LA RACINE DU DÉPÔT — une seule vérité, la
# même version « v06/ d'abord, repli copie à côté » que porte tout clone)
KIT = [
    (DOWNLOAD / "ceremonie_gui.py", "ceremonie_gui.py"),
    (DOWNLOAD / "ceremonie_hors_ligne.py", "ceremonie_hors_ligne.py"),
    (REPO / "coffre_fort.py", "coffre_fort.py"),
    (DOWNLOAD / "LISEZMOI-ceremonie-GUI.txt", "LISEZMOI-ceremonie-GUI.txt"),
    (DOWNLOAD / "LISEZMOI-cle-I.txt", "LISEZMOI-cle-I.txt"),
    (DOWNLOAD / "LISEZMOI-coffre-CF2.txt", "LISEZMOI-coffre-CF2.txt"),
    (REPO / "lancer_ceremonie.bat", "lancer_ceremonie.bat"),
    (REPO / "lancer_ceremonie.sh", "lancer_ceremonie.sh"),
    (V06 / "__init__.py", "v06/__init__.py"),
    (V06 / "ceremonie_gui.py", "v06/ceremonie_gui.py"),
    (V06 / "ceremonie_hors_ligne.py", "v06/ceremonie_hors_ligne.py"),
    (V06 / "coffre_cf2.py", "v06/coffre_cf2.py"),
    (V06 / "sceau_I.py", "v06/sceau_I.py"),
    (V06 / "sentinelle_cf2.py", "v06/sentinelle_cf2.py"),
]
MANIFESTE = "MANIFESTE.txt"


# ---------------------------------------------------------------- empreintes

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def taille_fr(n):
    return f"{n:,}".replace(",", " ") + " octets"


# ---------------------------------------------------------------- gardes

def gardes():
    """Le kit ne part pas divergent ni incomplet — échec NOMMÉ sinon."""
    absents = [str(src) for src, _ in KIT if not src.is_file()]
    if absents:
        raise ds.SyncError("sources absentes : " + " ; ".join(absents))
    for nom in ("ceremonie_gui.py", "ceremonie_hors_ligne.py"):
        a, b = DOWNLOAD / nom, V06 / nom
        if ds.md5_of(a) != ds.md5_of(b):
            raise ds.SyncError(
                f"DIVERGENCE {nom} : download/ et v06/ diffèrent "
                f"({ds.md5_of(a)[:12]}… vs {ds.md5_of(b)[:12]}…) — "
                "le kit ne sera PAS déposé divergent")
    print(f"[{DOSSIER}] gardes vertes : {len(KIT)} sources présentes ; "
          "ceremonie_gui.py et ceremonie_hors_ligne.py identiques "
          "download/ ↔ v06/ (md5)")


# ---------------------------------------------------------------- manifeste

def fabriquer_manifeste():
    """Génère MANIFESTE.txt (temp + copie d'audit) ; retourne son chemin."""
    now = datetime.datetime.now(datetime.timezone.utc)
    lignes = [
        f"TRIADE — KIT DE CÉRÉMONIE v0.6.0 — MANIFESTE DU DOSSIER « {DOSSIER} »",
        "=" * 70,
        "",
        f"Déposé le : {now.strftime('%Y-%m-%dT%H:%M:%SZ')} (UTC) — canal : "
        "OAuth relais, Drive « Triade ».",
        f"Provenance : dépôt git TRIADE commit {COMMIT_SRC} (D118 — la "
        "page unifiée, le dossier de cérémonie, l'attachement unique, les "
        "lanceurs à la racine du dépôt) + zone de livraison download/ de "
        "l'espace de travail.",
        "",
        "CE QUE CONTIENT CE DOSSIER",
        "--------------------------",
        "Une page de cérémonie, zéro ligne de commande après le lancement "
        "(D107/D118) :",
        "",
        "- ONGLETS CLÉ I (air-gap, D87) : copiez ceremonie_gui.py SEUL sur",
        "  une clef USB. Python standard uniquement — rien à installer,",
        "  aucun réseau, aucun pip. Il produit les MÊMES fichiers que",
        "  ceremonie_hors_ligne.py (interopération attestée D107).",
        "",
        "- ONGLETS DU DÉPÔT (cérémonie du coffre CF2, D86) : dès qu'un dépôt",
        "  triade est ATTACHÉ (bouton « Attacher le dépôt local… »). Le",
        "  sous-dossier v06/ fait office de mini-dépôt : relais des CLI,",
        "  CONTRÔLE DE RELECTURE de vos trois copies, feuille d'export,",
        "  liste blanche par formulaire, sentinelle détachée, BRÛLER avec",
        "  confirmation tapée. La pile pip (pynacl + cryptography) est",
        "  vérifiée et proposée AVEC votre accord.",
        "",
        "- D118 : UNE SEULE PAGE — les profils hors-ligne et dépôt ne font",
        "  plus qu'un cahier d'onglets (plus d'allers-retours par l'accueil)",
        "  ; le bouton d'attachement est UNIQUE (« Attacher le dépôt",
        "  local… », la preuve git/origin ne s'exige qu'en scénario repo",
        "  git) ; le DOSSIER DE CÉRÉMONIE porte la clé et la remise",
        "  a-signer.txt AU MÊME endroit, HORS du dépôt par défaut (sa",
        "  sœur) — « Préparer a-signer.txt » y COPIE la remise et",
        "  pré-remplit le champ « Remise à signer ». --depot CHEMIN /",
        "  TRIADE_DEPOT restent valables (D111) — la ligne de commande",
        "  devient un raccourci, plus une obligation. Voir",
        "  LISEZMOI-ceremonie-GUI.txt.",
        "",
        "- Mode d'emploi : LISEZMOI-ceremonie-GUI.txt (le GUI, la page",
        "  unifiée), LISEZMOI-cle-I.txt et LISEZMOI-coffre-CF2.txt (les",
        "  cérémonies réelles pas à pas, encarts MODE GRAPHIQUE inclus).",
        "  Lanceurs : lancer_ceremonie.bat (Windows, double-clic) et",
        "  lancer_ceremonie.sh (Linux/macOS) — D118 : les MÊMES lanceurs",
        "  vivent à la racine d'un clone git du dépôt (ils y visent",
        "  v06/ceremonie_gui.py d'abord, avec repli sur toute copie posée",
        "  à côté).",
        "",
        "- La vérification des DIX arbres du sceau I exige le dépôt",
        "  COMPLET (dossier « TRIADE » du même Drive, ou dépôt git) ;",
        "  depuis ce kit seul, l'échec est nommé — par conception.",
        "",
        f"EMPREINTES ({len(KIT)} fichiers — vérifiez après tout téléchargement)",
        "-" * 62,
        "Linux/macOS : md5sum FICHIER   —   Windows : certutil -hashfile",
        "FICHIER MD5. Toute divergence = copie corrompue : rejetez-la.",
        "",
    ]
    for src, rel in KIT:
        lignes += [
            rel,
            f"  taille : {taille_fr(src.stat().st_size)}",
            f"  md5    : {ds.md5_of(src)}",
            f"  sha256 : {sha256_of(src)}",
            "",
        ]
    lignes += [
        "MANIFESTE.txt : ce fichier même — non listé (auto-référence",
        "impossible).",
        "",
        "AUCUN SECRET ICI : ni clé privée, ni phrase de contrôle, ni",
        "coffre. La phrase D81 et coffre_fort.bin vivent ailleurs, sous",
        "garde. Ce kit ne contient que des outils, des modes d'emploi et",
        "des preuves publiques.",
    ]
    texte = "\n".join(lignes) + "\n"
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="ceremonie_")) / MANIFESTE
    tmp.write_text(texte, encoding="utf-8")
    if AUDIT.is_dir():
        (AUDIT / "depot_ceremonie_MANIFESTE.txt").write_text(
            texte, encoding="utf-8")
    return tmp


# ---------------------------------------------------------------- sonde

def sonde():
    racine = ds.list_folder(ds.DRIVE_ROOT_ID)
    print(f"[sonde] racine « Triade » : {len(racine)} entrées")
    for nom, f in sorted(racine.items()):
        tag = " [DOSSIER]" if f.get("mimeType") == ds.FOLDER_MIME else ""
        print(f"  {nom}{tag}")
    cand = [n for n in racine
            if "érémonie" in n or "eremonie" in n.lower()]
    print(f"[sonde] candidats « Cérémonie » : {cand if cand else 'AUCUN'}")
    for n in cand:
        f = racine[n]
        if f.get("mimeType") == ds.FOLDER_MIME:
            print(f"[sonde] contenu de « {n} » :")
            for fn, ff in sorted(ds.list_folder(f["id"]).items()):
                print(f"  {fn}  md5={ff.get('md5Checksum', '-')[:12]}…")


# ---------------------------------------------------------------- dépôt

def _assurer_dossier(parent_id, nom):
    """Dossier Drive par nom — réutilisé s'il existe déjà (idempotent)."""
    ent = ds.list_folder(parent_id)
    trouves = [f for f in ent.values()
               if f.get("mimeType") == ds.FOLDER_MIME and f["name"] == nom]
    if trouves:
        print(f"[{DOSSIER}] sous-dossier EXISTANT réutilisé : {nom}")
        return trouves[0]["id"]
    fid = ds.create_folder(parent_id, nom)
    print(f"[{DOSSIER}] sous-dossier CRÉÉ : {nom}")
    return fid


def _dist(cer_id, v06_id):
    """Carte distante {cible_relative: métadonnées} des DEUX dossiers."""
    carte = {}
    for nom, f in ds.list_folder(cer_id).items():
        if f.get("mimeType") == ds.FOLDER_MIME:
            continue
        carte[nom] = f
    for nom, f in ds.list_folder(v06_id).items():
        carte[f"{SOUS}/{nom}"] = f
    return carte


def deposer():
    gardes()
    chemin_manifeste = fabriquer_manifeste()
    print(f"[{DOSSIER}] manifeste généré ({MANIFESTE}, "
          f"{chemin_manifeste.stat().st_size} octets)")

    racine = ds.list_folder(ds.DRIVE_ROOT_ID)   # valide aussi le jeton
    existe = [f for f in racine.values()
              if f.get("mimeType") == ds.FOLDER_MIME and f["name"] == DOSSIER]
    if existe:
        cer_id = existe[0]["id"]
        print(f"[{DOSSIER}] dossier EXISTANT réutilisé (id {cer_id})")
    else:
        cer_id = ds.create_folder(ds.DRIVE_ROOT_ID, DOSSIER)
        print(f"[{DOSSIER}] dossier CRÉÉ à la racine du Drive (id {cer_id})")
    v06_id = _assurer_dossier(cer_id, SOUS)

    cibles = [(src, rel) for src, rel in KIT] + [(chemin_manifeste, MANIFESTE)]
    dist = _dist(cer_id, v06_id)
    print(f"[{DOSSIER}] {len(cibles)} fichiers à poser "
          f"({len(dist)} déjà présents au total)")

    for src, rel in cibles:
        md5 = ds.md5_of(src)
        f = dist.get(rel)
        if f and f.get("md5Checksum") == md5:
            print(f"[{DOSSIER}] inchangé : {rel} (md5 {md5[:12]}…)")
            continue
        if f:
            ds.upload_update(f["id"], src)
            print(f"[{DOSSIER}] mis à jour : {rel} (md5 {md5[:12]}…)")
        else:
            parent = v06_id if rel.startswith(SOUS + "/") else cer_id
            ds.upload_create(parent, rel.split("/")[-1], src)
            print(f"[{DOSSIER}] téléversé : {rel} (md5 {md5[:12]}…)")

    # ---------------- vérification aller-retour (la preuve du dépôt)
    print(f"[{DOSSIER}] vérification aller-retour (md5)…")
    attendus = {rel: ds.md5_of(src) for src, rel in cibles}
    fin = _dist(cer_id, v06_id)
    echecs, verts = [], 0
    for rel, md5 in sorted(attendus.items()):
        if fin.get(rel, {}).get("md5Checksum") == md5:
            verts += 1
            print(f"[{DOSSIER}] vérifié : {rel} — md5 MATCH")
        else:
            echecs.append(rel)
            vu = fin.get(rel, {}).get("md5Checksum", "ABSENT")
            print(f"[{DOSSIER}] ÉCHEC : {rel} — distant {vu} ≠ local {md5}")
    extras = sorted(k for k in fin if k not in attendus)
    for k in extras:
        print(f"[{DOSSIER}] note : « {k} » présent non attendu (conservé)")

    print("-" * 60)
    print(f"VERDICT : {verts}/{len(attendus)} fichiers vérifiés md5 MATCH "
          f"dans /{DOSSIER} du Drive « Triade »")
    print(f"Lien dossier : https://drive.google.com/drive/folders/{cer_id}")
    return 1 if echecs else 0


def main():
    if "--sonde" in sys.argv[1:]:
        try:
            return sonde() or 0
        except ds.SyncError as e:
            print(f"[sonde] ÉCHEC : {e}", file=sys.stderr)
            return 2
    try:
        return deposer()
    except ds.SyncError as e:
        print(f"[{DOSSIER}] ÉCHEC NOMMÉ : {e}", file=sys.stderr)
        print("Parades : (1) le refresh OAuth relais expire ~05/11 — "
              "reprenez-le (scripts/oauth_echange.py) ; (2) partagez le "
              "dossier en Éditeur au compte de service ; (3) le compte de "
              "service seul est LECTEUR — il ne peut pas écrire.",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
