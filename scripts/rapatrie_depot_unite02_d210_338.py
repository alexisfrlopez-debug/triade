#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rapatrie_depot_unite02_d210_338.py — LE RAPATRIEMENT DU DÉPÔT
preuves-unite02/ du coffre /test (l'annonce du développeur : « preuves
deposees dans le drive /test » — le run terrain de l'unité 02 D210 au kit
GUI 1-clic livré à la 337). Chaque pièce est téléchargée DEUX FOIS
byte-byte (la chaîne de garde par le re-téléchargement), son md5 recoupé
contre la métadonnée Drive, le tout consigné au bac
scripts/campagne_d204/depot-run-unite02-d210-338/epreuves/."""
import hashlib
import json
import pathlib
import sys
import urllib.parse

REPO = pathlib.Path("/home/z/my-project/triade/lab/repo2")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

DOSSIER_ID = "1K0lmnAOaJmo7yL1RnXrxXiXuOlS8-3vt"  # preuves-unite02/ au /test
BAC = REPO / "scripts" / "campagne_d204" / "depot-run-unite02-d210-338"
EPREUVES = BAC / "epreuves"


def telecharge(file_id):
    """Télécharge une pièce (alt=media) — voix authentifiée du coffre."""
    st, body, _ = ds.api("GET", ds.API + "/files/" + file_id
                         + "?alt=media")
    if st != 200:
        raise RuntimeError(f"téléchargement impossible ({st})")
    return body


def md5(data):
    return hashlib.md5(data).hexdigest()


def main():
    EPREUVES.mkdir(parents=True, exist_ok=True)
    # la voix du dossier : la naissance du dépôt au coffre
    st, body, _ = ds.api("GET", ds.API + "/files/" + DOSSIER_ID
                         + "?fields=name,createdTime,modifiedTime,mimeType")
    dossier = json.loads(body)
    print(f"[rapatrié] le dossier {dossier['name']}/ : né au coffre "
          f"{dossier.get('createdTime', '?')}, mtime "
          f"{dossier.get('modifiedTime', '?')}")

    params = {"q": f"'{DOSSIER_ID}' in parents and trashed = false",
              "pageSize": "100",
              "fields": ("nextPageToken,files(id,name,mimeType,md5Checksum,"
                         "size,modifiedTime,createdTime)")}
    st, body, _ = ds.api("GET", ds.API + "/files?"
                         + urllib.parse.urlencode(params))
    pieces = sorted(json.loads(body).get("files", []),
                    key=lambda f: f.get("modifiedTime", ""))
    print(f"[rapatrié] {len(pieces)} pièce(s) au dépôt :")

    ecarts = 0
    for f in pieces:
        nom = f["name"]
        d1 = telecharge(f["id"])
        d2 = telecharge(f["id"])
        md5_local = md5(d1)
        ok_double = (d1 == d2)
        ok_md5 = (md5_local == f.get("md5Checksum"))
        dest = EPREUVES / nom
        dest.write_bytes(d1)
        verdict = "VERT" if (ok_double and ok_md5) else "ROUGE"
        if verdict == "ROUGE":
            ecarts += 1
        print(f"  [{verdict}] {nom} ({f.get('size', '?')} o) : "
              f"double-téléchargement byte-byte "
              f"{'IDENTIQUE' if ok_double else 'ÉCART'} ; md5 local "
              f"{md5_local[:8]}… / Drive "
              f"{str(f.get('md5Checksum'))[:8]}… "
              f"{'MATCH' if ok_md5 else 'ÉCART'} ; né "
              f"{f.get('createdTime', '?')}, mtime "
              f"{f.get('modifiedTime', '?')}")
    print(f"[rapatrié] bilan : {len(pieces) - ecarts}/{len(pieces)} pièces "
          f"rapatriées VERT au bac {BAC.relative_to(REPO)}/")
    return 1 if ecarts else 0


if __name__ == "__main__":
    sys.exit(main())
