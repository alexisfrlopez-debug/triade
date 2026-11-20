#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""drive_sa_v220.py — LE CANAL DRIVE DE LA VAGUE 11 (urllib seul, aucune
dépendance tierce). DEUX comptes, deux rôles (la voie de la vague 10) :
  — LE COMPTE DE SERVICE (z-ai-811@physichong, LECTEUR SEUL — la limite
    D101 constatée vécue : 403 « Insufficient permissions » à toute
    création, racine comprise) : le token régénéré par python3
    /home/z/my-project/scripts/gdrive_sa.py vit à /tmp/gdrive_access.
    json — LES LECTURES (list/download/md5) ;
  — LE RELAIS OAUTH du coffre (.gdrive/oauth_token_relais.json — le
    FRAIS du /Tokens, le compte de référence alexis.fr.lopez) : LES
    ÉCRITURES (upload, move) — rafraîchi par le module, jamais affiché.
Les modèles : scripts/vague10/livrer_coffre_vague10.py (le relais aux
écritures) et archiver_instructions_vague10.py ; la voie urllib reprend
celle de scripts/gdrive_sa.py."""
from __future__ import annotations

import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://www.googleapis.com/drive/v3"
UPLOAD = "https://www.googleapis.com/upload/drive/v3"
SA_TOKEN = "/tmp/gdrive_access.json"
RELAIS = "/home/z/my-project/depot/.gdrive/oauth_token_relais.json"

_sa = {"val": None, "exp": 0.0}
_rel = {"val": None, "exp": 0.0}


def token_sa() -> str:
    if _sa["val"] is None or time.time() > _sa["exp"] - 120:
        d = json.load(open(SA_TOKEN))
        _sa["val"] = d["access_token"]
        _sa["exp"] = time.time() + 3300
    return _sa["val"]


def token_relais() -> str:
    """le relais OAuth rafraîchi au besoin (jamais affiché)."""
    if _rel["val"] is None or time.time() > _rel["exp"] - 120:
        R = json.load(open(RELAIS))
        data = urllib.parse.urlencode({
            "client_id": R["client_id"],
            "client_secret": R["client_secret"],
            "refresh_token": R["refresh_token"],
            "grant_type": "refresh_token"}).encode()
        req = urllib.request.Request(R["token_uri"], data=data,
                                     method="POST")
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
        _rel["val"] = d["access_token"]
        _rel["exp"] = time.time() + int(d.get("expires_in", 3600)) - 120
    return _rel["val"]


def hdr(qui: str = "sa"):
    return {"Authorization":
            f"Bearer {token_sa() if qui == 'sa' else token_relais()}"}


def api(method: str, chemin: str, params: dict | None = None,
        json_body=None, data: bytes | None = None,
        content_type: str | None = None, qui: str = "sa"):
    """un appel Drive v3 — la réponse urllib brute (status, bytes).
    L'écriture au relais (qui='relais'), la lecture au service."""
    url = API + chemin
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = hdr(qui)
    corps = None
    if json_body is not None:
        corps = json.dumps(json_body).encode()
        headers["Content-Type"] = "application/json"
    if data is not None:
        corps = data
        if content_type:
            headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=corps, method=method,
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def liste(parent: str) -> list[dict]:
    """les enfants non corbeillés d'un dossier (id, name, size, md5)."""
    out, page = [], None
    while True:
        params = {"q": f"'{parent}' in parents and trashed=false",
                  "fields": "nextPageToken,files(id,name,size,md5Checksum,"
                            "mimeType)",
                  "pageSize": 200}
        if page:
            params["pageToken"] = page
        st, body = api("GET", "/files", params)
        assert st == 200, f"liste : HTTP {st} {body[:200]}"
        d = json.loads(body)
        out += d.get("files", [])
        page = d.get("nextPageToken")
        if not page:
            return out


def trouve(nom: str, parent: str) -> str | None:
    for f in liste(parent):
        if f["name"] == nom:
            return f["id"]
    return None


def televerse(chemin, parent: str, timeout_genereux: int = 900):
    """l'upload au RELAIS (multipart, ou la mise à jour du média si le nom
    vit déjà — l'idempotence ; resumable aux grosses pièces) PUIS LE
    RECOUP byte-byte par re-téléchargement (la lecture au service)."""
    import pathlib
    p = pathlib.Path(chemin)
    data = p.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    fid = trouve(p.name, parent)
    if fid:
        url = (f"{UPLOAD}/files/{fid}?uploadType=media"
               f"&supportsAllDrives=true")
        req = urllib.request.Request(url, data=data, method="PATCH",
                                     headers={**hdr("relais"),
                                              "Content-Type":
                                              "application/octet-stream"})
        with urllib.request.urlopen(req, timeout=timeout_genereux) as r:
            assert r.status == 200, f"mise à jour : HTTP {r.status}"
        print(f"  [mis à jour] {p.name} [{len(data):,} o]")
    else:
        limite = 5 * 1024 * 1024
        if len(data) <= limite:
            meta = json.dumps({"name": p.name, "parents": [parent]}).encode()
            corps = (b"--v220\r\nContent-Type: application/json; "
                     b"charset=UTF-8\r\n\r\n" + meta +
                     b"\r\n--v220\r\nContent-Type: "
                     b"application/octet-stream\r\n\r\n" + data +
                     b"\r\n--v220--\r\n")
            url = (f"{UPLOAD}/files?uploadType=multipart"
                   f"&supportsAllDrives=true")
            req = urllib.request.Request(url, data=corps, method="POST",
                                         headers={**hdr("relais"),
                                                  "Content-Type":
                                                  "multipart/related; "
                                                  "boundary=v220"})
            with urllib.request.urlopen(req, timeout=timeout_genereux) as r:
                assert r.status == 200, f"upload : HTTP {r.status}"
                fid = json.loads(r.read())["id"]
        else:  # le resumable pour les grosses pièces (le bundle ~130 Mo)
            url = (f"{UPLOAD}/files?uploadType=resumable"
                   f"&supportsAllDrives=true")
            meta = json.dumps({"name": p.name, "parents": [parent]}).encode()
            req = urllib.request.Request(
                url, data=meta, method="POST",
                headers={**hdr("relais"),
                         "Content-Type": "application/json",
                         "X-Upload-Content-Length": str(len(data)),
                         "X-Upload-Content-Type":
                         "application/octet-stream"})
            with urllib.request.urlopen(req, timeout=120) as r:
                loc = r.headers["Location"]
            pos, chunk = 0, 8 * 1024 * 1024
            while pos < len(data):
                bout = data[pos:pos + chunk]
                fin = pos + len(bout) - 1
                req = urllib.request.Request(
                    loc, data=bout, method="PUT",
                    headers={"Content-Range":
                             f"bytes {pos}-{fin}/{len(data)}"})
                with urllib.request.urlopen(req,
                                            timeout=timeout_genereux) as r:
                    if r.status in (200, 201):
                        fid = json.loads(r.read())["id"]
                pos = fin + 1
        print(f"  [téléversé] {p.name} [{len(data):,} o]")
    # LE RECOUP byte-byte (la lecture au compte de service — le bord froid)
    st, body = api("GET", f"/files/{fid}",
                   {"alt": "media", "supportsAllDrives": "true"})
    ok = st == 200 and body == data
    if not ok:
        raise SystemExit(f"RECOUP ÉCHOUÉ : {p.name}")
    print(f"  VERT {p.name} recoupé byte-byte (md5 {md5[:8]}…)")
    return fid


def telecharge(fid: str) -> bytes:
    st, body = api("GET", f"/files/{fid}",
                   {"alt": "media", "supportsAllDrives": "true"})
    assert st == 200, f"télécharge : HTTP {st}"
    return body
