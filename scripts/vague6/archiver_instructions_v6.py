#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""archiver_instructions_v6.py — vague 6 : déplacer vers le /ARCHIVE du coffre
Drive UNIQUEMENT les instructions EXÉCUTÉES, APRES vérification md5.

La discipline de la vague 6 : on n'archive qu'une instruction exécutée
(rapport d'exécution à l'appui). Au 17/11/2026, UNE seule l'est :
bqh4qlrqj (l'audit du manuscrit v0.18.0 — l'édition v0.18.1 livrée,
V1–V10 tout vert). Les cinq autres demeurent au /instructions : le
script les liste « EN ATTENTE » et REFUSE de les déplacer (échec fermé)
— au fil des sessions d'exécution, portez leur état à EXÉCUTÉE dans la
table ETATS ci-dessous, avec la référence du rapport qui fait foi.

L'agent n'utilise AUCUN jeton : ce script tourne sur la machine du
développeur, avec SES propres identifiants OAuth. Le fichier de jetons
est passé par --jetons ; son contenu n'est jamais affiché ni copié.

Dépendances :  pip install google-api-python-client google-auth

Utilisation :
  python3 archiver_instructions_v6.py --jetons chemin/vers/jetons.json
      Mode CONTRÔLE (défaut) : liste, télécharge, vérifie les md5,
      ne déplace RIEN.
  python3 archiver_instructions_v6.py --jetons ... --executer
      Déplace réellement les instructions EXÉCUTÉES (et elles seules),
      échec fermé : si un md5 diverge ou qu'un fichier manque, RIEN
      n'est déplacé ; puis re-liste les deux dossiers et écrit
      ARCHIVAGE-RECOUP-V6.txt.

Format du fichier de jetons : JSON « authorized user » standard Google
(champs token / refresh_token / client_id / client_secret).
"""

import argparse
import hashlib
import io
import json
import sys
from datetime import datetime, timezone

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
except ImportError:
    sys.exit("Dépendances manquantes : pip install google-api-python-client google-auth")

RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"

# (nom exact, md5 attendu) — voir MANIFESTE-6-INSTRUCTIONS.txt
SIX = [
    ("Qwen__20261116_5gfx6pwkj.txt", "227a28ccd2b9b2511a23ca67a6538f2d"),
    ("Qwen__20261116_89488hblm.txt", "35acad01f1a568c29eb84864374eef36"),
    ("Qwen__20261116_bqh4qlrqj.txt", "2a5f339f114b2dca19abf81402f660da"),
    ("Qwen__20261116_fkkqc7v8t.txt", "c460edb6ee1e05abb61e8a40eb969b3b"),
    ("Qwen__20261116_p39uklsca.txt", "61d2593b0c6d985ff10897bda85ded51"),
    ("Qwen__20261116_vljfs6pcj.txt", "986891fde5534e88de255ec0bb656fc2"),
]

# L'ÉTAT D'EXÉCUTION — la seule table à tenir au fil des sessions.
# Une instruction ne passe à "EXECUTEE" qu'avec un rapport d'exécution
# qui fait foi (chemin consigné en regard).
ETATS = {
    "Qwen__20261116_5gfx6pwkj.txt": ("EN_ATTENTE", "après la baseline double-bras (D207)"),
    "Qwen__20261116_89488hblm.txt": ("EN_ATTENTE", "outillage model-checker à re-provisionner"),
    "Qwen__20261116_bqh4qlrqj.txt": ("EXECUTEE", "rapport-execution-vague6.txt (v0.18.1, V1-V10 vert)"),
    "Qwen__20261116_fkkqc7v8t.txt": ("EN_ATTENTE", "audit statique au labo, runs dudect au terrain"),
    "Qwen__20261116_p39uklsca.txt": ("EN_ATTENTE", "nouveaux cycles de campagne D210"),
    "Qwen__20261116_vljfs6pcj.txt": ("EN_ATTENTE", "après la baseline, un levier par unité (D207)"),
}


def charger_identifiants(chemin):
    """Construit les identifiants OAuth depuis le fichier du développeur.
    N'affiche JAMAIS le contenu du fichier."""
    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)
    creds = Credentials(
        token=data.get("token"),
        refresh_token=data.get("refresh_token"),
        client_id=data.get("client_id"),
        client_secret=data.get("client_secret"),
        token_uri="https://oauth2.googleapis.com/token",
    )
    if not creds.valid:
        creds.refresh(Request())
    return creds


def trouver_dossier(service, nom):
    res = (
        service.files()
        .list(
            q="'{0}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false".format(
                RACINE
            ),
            fields="files(id, name)",
            pageSize=100,
        )
        .execute()
    )
    for f in res.get("files", []):
        if f["name"] == nom:
            return f["id"]
    return None


def lister(service, dossier_id):
    res = (
        service.files()
        .list(
            q="'{0}' in parents and trashed = false".format(dossier_id),
            fields="files(id, name)",
            pageSize=200,
        )
        .execute()
    )
    return {f["name"]: f["id"] for f in res.get("files", [])}


def md5_depuis_drive(service, file_id):
    requete = service.files().get_media(fileId=file_id)
    buf = io.BytesIO()
    telechargeur = MediaIoBaseDownload(buf, requete)
    termine = False
    while not termine:
        statut, termine = telechargeur.next_chunk()
    return hashlib.md5(buf.getvalue()).hexdigest()


def main():
    parseur = argparse.ArgumentParser(description="Archivage vague 6 (contrôle par défaut)")
    parseur.add_argument("--jetons", required=True, help="chemin du fichier de jetons OAuth (local)")
    parseur.add_argument("--executer", action="store_true", help="déplacer réellement (défaut : contrôle)")
    args = parseur.parse_args()

    creds = charger_identifiants(args.jetons)
    service = build("drive", "v3", credentials=creds)

    instructions_id = trouver_dossier(service, "instructions")
    archive_id = trouver_dossier(service, "ARCHIVE")
    if not instructions_id or not archive_id:
        sys.exit("ÉCHEC : dossier instructions ou ARCHIVE introuvable à la racine du coffre.")

    au_instructions = lister(service, instructions_id)
    au_archive = lister(service, archive_id)
    print("Avant : /instructions = {0} fichier(s) ; /ARCHIVE = {1} fichier(s)".format(
        len(au_instructions), len(au_archive)))

    verdicts, erreurs = [], []
    for nom, md5_attendu in SIX:
        etat, ref = ETATS[nom]
        if nom not in au_instructions:
            if nom in au_archive:
                verdicts.append((nom, "DÉJÀ AU /ARCHIVE", "—"))
            else:
                erreurs.append("{0} : introuvable au /instructions ET au /ARCHIVE".format(nom))
            continue
        md5_vu = md5_depuis_drive(service, au_instructions[nom])
        if md5_vu != md5_attendu:
            erreurs.append("{0} : md5 divergent (attendu {1}, vu {2})".format(nom, md5_attendu, md5_vu))
        elif etat == "EXECUTEE":
            verdicts.append((nom, "CONFORME, EXÉCUTÉE — à déplacer", md5_vu))
        else:
            verdicts.append((nom, "CONFORME, EN ATTENTE — NON DÉPLACÉABLE ({0})".format(ref), md5_vu))

    for nom, verdict, md5_vu in verdicts:
        print("  [{0}] {1}  {2}".format(verdict, nom, md5_vu))
    for e in erreurs:
        print("  [ÉCHEC] {0}".format(e))

    if erreurs:
        sys.exit("\nÉCHEC FERMÉ : au moins une pièce diverge — RIEN n'est déplacé. "
                 "Vérifiez le coffre à la main avant tout geste.")

    a_deplacer = [v for v in verdicts if v[1].startswith("CONFORME, EXÉCUTÉE")]
    if not a_deplacer:
        print("\nRien à déplacer : aucune instruction exécutée en attente d'archivage "
              "(ou déjà au /ARCHIVE).")
        return

    if not args.executer:
        print("\nMODE CONTRÔLE : {0} pièce(s) exécutée(s) prêtes à déplacer vers /ARCHIVE. "
              "Relancez avec --executer pour déplacer réellement.".format(len(a_deplacer)))
        return

    deplaces = []
    for nom, _, _ in a_deplacer:
        service.files().update(
            fileId=au_instructions[nom],
            addParents=archive_id,
            removeParents=instructions_id,
        ).execute()
        deplaces.append(nom)
        print("  DÉPLACÉ : {0}".format(nom))

    apres_instructions = lister(service, instructions_id)
    apres_archive = lister(service, archive_id)
    horodatage = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lignes = [
        "ARCHIVAGE-RECOUP-V6 — {0}".format(horodatage),
        "Déplacées (instructions EXÉCUTÉES seules) :",
    ]
    lignes += ["  - {0}  [{1}]".format(n, ETATS[n][1]) for n in deplaces]
    lignes += [
        "Restent au /instructions (EN ATTENTE d'exécution) :",
    ]
    lignes += ["  - {0}  [{1}]".format(n, ETATS[n][1])
               for n, _ in SIX if n in apres_instructions]
    lignes += [
        "Après : /instructions = {0} fichier(s) ; /ARCHIVE = {1} fichier(s)".format(
            len(apres_instructions), len(apres_archive)),
        "md5 vérifiés AVANT déplacement (échec fermé) — voir MANIFESTE-6-INSTRUCTIONS.txt.",
    ]
    with open("ARCHIVAGE-RECOUP-V6.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes) + "\n")
    print("\nRECOUP écrit : ARCHIVAGE-RECOUP-V6.txt — /instructions = {0} ; /ARCHIVE = {1}".format(
        len(apres_instructions), len(apres_archive)))


if __name__ == "__main__":
    main()
