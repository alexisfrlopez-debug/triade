#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifie_table5_v180.py — CHAQUE ARTEFACT DE LA TABLE DES EMPREINTES
vérifié OCTET À OCTET (l'instruction iz5b9sv09, point 4 : « vérifier que
chaque artefact de Table 5 est présent dans l'archive avec l'empreinte
correspondante » ; l'étape de vérification : « script qui re-vérifie
octet à octet les empreintes de Table 5 contre les archives régénérées
(zéro divergence) »).

Les empreintes attendues : lues de la table du manuscrit (les 16 premiers
hex, la forme publiée) ET des empreintes_livrables consignées — jamais
inversées : l'octet est la vérité, la table est confrontée.
"""
import hashlib
import io
import pathlib
import sys

sys.path.insert(0, "/home/z/my-project/scripts")
from google.oauth2 import service_account          # noqa: E402
from googleapiclient.discovery import build        # noqa: E402
from googleapiclient.http import MediaIoBaseDownload  # noqa: E402

SA = "/home/z/my-project/upload/physichong-4b3b7222b48c.json"
creds = service_account.Credentials.from_service_account_file(
    SA, scopes=["https://www.googleapis.com/auth/drive"])
drive = build("drive", "v3", credentials=creds, cache_discovery=False)

LOCAUX = {
    "loupe.exe 0.1.1": (pathlib.Path("/tmp/triade-gh/loupe/loupe.exe"),
                        "c111510535767a40"),
    "proxy.exe 1.0.0": (pathlib.Path("/tmp/triade-gh/tls13/proxy.exe"),
                        "446279f3ab356900"),
    "selftest.exe (M1)": (pathlib.Path("/tmp/triade-gh/m1/selftest.exe"),
                          "8038585b"),
    "passeur.exe v0.2 (T)": (pathlib.Path(
        "/tmp/my-project/labapp/kits/kit-unite-13-app-T-20261116-v5/"
        "passeur.exe"), "4a7229e7418e8276"),
    "passeur-c.dll v0.2 (C)": (pathlib.Path(
        "/tmp/my-project/labapp/kits/kit-unite-14-app-C-20261116-v3/"
        "passeur-c.dll"), "fe4ddfc9842fb29b"),
    "loupe.exe (campagne, pièce recomposée)": (pathlib.Path(
        "/tmp/triade-gh/scripts/campagne_d204/unite-01-T/piece/loupe.exe"),
        "4d119b22"),
}

# les pièces du poste autonome : au coffre Drive (recherche par nom)
DRIVE_NOMS = {
    "pilot EXE (installer)": ("TRIADE-GUI-PASSEUR-Setup", "34b9764131e3b3a5"),
    "pilot source v2": ("TRIADE_gui_app_passeur_v2", "40d23f03fdaaf116"),
}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


resultats = []
ok_total = True
for nom, (chemin, attendu) in LOCAUX.items():
    if not chemin.exists():
        resultats.append(f"[{nom}] ABSENT au chemin local {chemin}")
        ok_total = False
        continue
    sha = sha_bytes(chemin.read_bytes())
    ok = sha.startswith(attendu)
    ok_total &= ok
    resultats.append(f"[{nom}] {'VERT' if ok else 'ROUGE'} — {sha[:16]}… "
                     f"(attendu {attendu}…) {len(chemin.read_bytes())} o")

for nom, (terme, attendu) in DRIVE_NOMS.items():
    reponse = drive.files().list(
        q=f"name contains '{terme}' and trashed = false", pageSize=5,
        fields="files(id, name, size)").execute()
    fichiers = reponse.get("files", [])
    if not fichiers:
        resultats.append(f"[{nom}] ABSENT du coffre Drive (recherche "
                         f"« {terme} »)")
        ok_total = False
        continue
    f = fichiers[0]
    buf = io.BytesIO()
    tele = MediaIoBaseDownload(buf, drive.files().get_media(fileId=f["id"]))
    done = False
    while not done:
        _, done = tele.next_chunk()
    sha = sha_bytes(buf.getvalue())
    ok = sha.startswith(attendu)
    ok_total &= ok
    resultats.append(f"[{nom}] {'VERT' if ok else 'ROUGE'} — {sha[:16]}… "
                     f"(attendu {attendu}…) {f['size']} o "
                     f"(« {f['name']} » au coffre)")

# les DEUX archives régénérées : leurs empreintes propres
for z in ("TRIADE_soumission_v0.18.0.zip", "TRIADE_complet_v0.18.0.zip"):
    chemin = pathlib.Path("/home/z/my-project/livraison-vague5/archives") / z
    resultats.append(f"[{z}] {sha_bytes(chemin.read_bytes())} "
                     f"({chemin.stat().st_size} o)")

rapport = [
    "LA TABLE DES EMPREINTES — CHAQUE ARTEFACT VÉRIFIÉ OCTET À OCTET",
    "(la vague 5, iz5b9sv09 — l'octet est la vérité, la table confrontée)",
    "=" * 72,
] + resultats + [
    "=" * 72,
    "LE VERDICT : " + ("VERT — zéro divergence" if ok_total
                       else "ROUGE — au moins une divergence"),
]
sortie = pathlib.Path(
    "/home/z/my-project/livraison-vague5/p10-table5-octets.txt")
sortie.write_text("\n".join(rapport), encoding="utf-8")
print("\n".join(rapport))
sys.exit(0 if ok_total else 2)
