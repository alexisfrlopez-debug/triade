#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_run_unite08_343.py — LE RAPATRIEMENT du dépôt du run terrain de
l'unité 02 D210 LOUPE-08 LIGNE × BRAS T (l'annonce du développeur : « preuves
dans le drive /test » — le dossier kit-unite-02-d210-20261118/ né au coffre
17/11 23:10:27Z, APRÈS la livraison du kit 22:42:58Z : le kit DÉZIPPÉ au
terrain + les preuves nées du run). Les pièces NÉES DU RUN sont téléchargées
DEUX FOIS byte-byte (la chaîne de garde par le re-téléchargement), leur md5
recoupé contre la métadonnée Drive ; les DIX-HUIT pièces du kit au coffre
sont recoupées par md5 (métadonnée Drive == le kit du labo livré à la 342,
byte-byte) SANS re-téléchargement (la gravure les recoupe déjà au DEPOT).
Tout est consigné au bac
scripts/campagne_d204/depot-run-unite08-d210-343/epreuves/."""
import hashlib
import json
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DOSSIER_ID = "1oxnULtkeTicLvqBlDeVhB06_GCaTBKqH"  # kit-unite-02-d210-20261118/
KIT_LABO = pathlib.Path("/home/z/my-project/download/"
                         "TRIADE_gui_unite08_d210_v1")
BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite08-d210-343"
EPREUVES = BAC / "epreuves"

# les pièces du kit (celles du zip livré à la 342 — le dossier GUI du dépôt
# download/ du dépôt) : recoupées par md5, jamais re-téléchargées ici
PIECES_KIT = sorted(p.name for p in KIT_LABO.iterdir() if p.is_file())


def telecharge(file_id):
    """Télécharge une pièce (alt=media) — voix authentifiée du coffre."""
    st, body, _ = ds.api("GET", ds.API + "/files/" + file_id + "?alt=media")
    if st != 200:
        raise RuntimeError(f"téléchargement impossible ({st})")
    return body


def md5(data):
    return hashlib.md5(data).hexdigest()


def md5f(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for m in iter(lambda: f.read(1 << 20), b""):
            h.update(m)
    return h.hexdigest()


def lister(fid):
    out = {}
    token = None
    while True:
        params = {"q": f"'{fid}' in parents and trashed = false",
                  "pageSize": "100",
                  "fields": ("nextPageToken,files(id,name,mimeType,md5Checksum,"
                             "size,modifiedTime,createdTime)")}
        if token:
            params["pageToken"] = token
        st, body, _ = ds.api("GET", ds.API + "/files?"
                             + urllib.parse.urlencode(params))
        if st != 200:
            raise RuntimeError(f"listing impossible ({st})")
        obj = json.loads(body)
        for f in obj.get("files", []):
            out[f["name"]] = f
        token = obj.get("nextPageToken")
        if not token:
            return out


def main():
    EPREUVES.mkdir(parents=True, exist_ok=True)
    # la voix du dossier : la naissance du dépôt au coffre
    st, body, _ = ds.api("GET", ds.API + "/files/" + DOSSIER_ID
                         + "?fields=name,createdTime,modifiedTime,mimeType")
    dossier = json.loads(body)
    print(f"[rapatrié] le dossier {dossier['name']}/ : né au coffre "
          f"{dossier.get('createdTime', '?')}")

    racine = lister(DOSSIER_ID)
    print(f"[rapatrié] {len(racine)} entrée(s) à la racine du dépôt : "
          f"{len(PIECES_KIT)} pièces du kit attendues + les preuves du run")

    # 1· les pièces du kit au coffre : md5 Drive == le kit du labo (342)
    verts_kit, ecarts_kit = 0, []
    for nom in PIECES_KIT:
        f = racine.get(nom)
        if not f:
            ecarts_kit.append(f"{nom}: ABSENT au coffre")
            continue
        if f.get("md5Checksum") == md5f(KIT_LABO / nom):
            verts_kit += 1
        else:
            ecarts_kit.append(f"{nom}: md5 divergent "
                              f"({f.get('md5Checksum')[:8]}… != "
                              f"{md5f(KIT_LABO / nom)[:8]}…)")
    print(f"[rapatrié] le kit au coffre : {verts_kit}/{len(PIECES_KIT)} "
          f"pièces md5 == le kit du labo livré à la 342 "
          f"{'— INTACT' if not ecarts_kit else ' — ÉCARTS : ' + ' ; '.join(ecarts_kit)}")

    # 2· les preuves nées du run : double-téléchargement byte-byte
    artefacts = {}   # nom -> (id, meta) — à plat puis rangé par sous-dossier
    for nom, f in racine.items():
        if f.get("mimeType") == ds.FOLDER_MIME:
            sous = lister(f["id"])
            for n2, f2 in sous.items():
                artefacts[f"{nom}/{n2}"] = f2
        elif nom not in PIECES_KIT:
            artefacts[nom] = f
    print(f"[rapatrié] {len(artefacts)} pièce(s) née(s) du run "
          "(console, état, réceptacle, journal) :")

    ecarts = 0
    for nom in sorted(artefacts):
        f = artefacts[nom]
        d1 = telecharge(f["id"])
        d2 = telecharge(f["id"])
        md5_local = md5(d1)
        ok_double = (d1 == d2)
        ok_md5 = (md5_local == f.get("md5Checksum"))
        dest = EPREUVES / nom
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(d1)
        verdict = "VERT" if (ok_double and ok_md5) else "ROUGE"
        if verdict == "ROUGE":
            ecarts += 1
        print(f"  [{verdict}] {nom} ({f.get('size', '?')} o) : double-"
              f"téléchargement byte-byte "
              f"{'IDENTIQUE' if ok_double else 'ÉCART'} ; md5 local "
              f"{md5_local[:8]}… / Drive {str(f.get('md5Checksum'))[:8]}… "
              f"{'MATCH' if ok_md5 else 'ÉCART'} ; mtime "
              f"{f.get('modifiedTime', '?')}")
    print(f"[rapatrié] bilan : {len(artefacts) - ecarts}/{len(artefacts)} "
          f"pièces du run rapatriées VERT au bac "
          f"{BAC.relative_to(REPO)}/ ; le kit {verts_kit}/{len(PIECES_KIT)} "
          f"recoupé par md5")
    return 1 if (ecarts or ecarts_kit) else 0


if __name__ == "__main__":
    sys.exit(main())
