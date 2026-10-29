#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — Relais de secours : authentification Drive par COMPTE DE SERVICE.

Le jeton OAuth du relais (oauth_token_relais.json) est MORT (HTTP 400
invalid_grant — refresh token expiré/révoqué, constat 29/10 08:11). Le
compte de service .gdrive/physichong-4b3b7222b48c.json prend le relais :
JWT RS256 (scope drive) -> access_token, injecté dans drive_sync par
surgiage de get_access_token. Si le dossier test (1KeJIMwpsT7…) n'est pas
partagé au compte de service, l'échec est NOMMÉ (et la reprise OAuth
interactive reste la voie propre).

Usage :
  python3 scripts/relais_service_account.py --dossier-test FICHIER [FICHIER…]
  python3 scripts/relais_service_account.py --corbeille FICHIER [FICHIER…]
"""
import base64
import json
import pathlib
import sys
import time

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

SA_FILE = REPO / ".gdrive" / "physichong-4b3b7222b48c.json"
TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
SCOPE = "https://www.googleapis.com/auth/drive"

_token_cache = {"token": None, "exp": 0.0}


def _b64u(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")


def get_sa_token() -> str:
    now = time.time()
    if _token_cache["token"] and _token_cache["exp"] > now + 60:
        return _token_cache["token"]
    sa = json.loads(SA_FILE.read_text())
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives.serialization import load_pem_private_key

    cle = load_pem_private_key(sa["private_key"].encode(), password=None)
    entete = _b64u(json.dumps({"alg": "RS256", "typ": "JWT",
                               "kid": sa["private_key_id"]}).encode())
    charge = _b64u(json.dumps({
        "iss": sa["client_email"],
        "scope": SCOPE,
        "aud": sa["token_uri"],
        "iat": int(now), "exp": int(now) + 3600,
    }).encode())
    signature = _b64u(cle.sign((entete + "." + charge).encode(),
                                padding.PKCS1v15(), hashes.SHA256()))
    jwt = entete + "." + charge + "." + signature
    st, body, _ = ds._http_raw(
        sa["token_uri"],
        data=json.dumps({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                         "assertion": jwt}).encode(),
        headers={"Content-Type": "application/json"})
    if st != 200:
        raise ds.SyncError(f"JWT compte de service refusé (HTTP {st}) : {body[:200]!r}")
    obj = json.loads(body)
    _token_cache["token"] = obj["access_token"]
    _token_cache["exp"] = now + int(obj.get("expires_in", 3600))
    return obj["access_token"]


# surgiage : toutes les requêtes drive_sync passent par le compte de service
ds.get_access_token = (lambda force=False: get_sa_token())


def pousser_test(chemins):
    fichiers = [pathlib.Path(c) for c in chemins]
    for p in fichiers:
        if not p.is_file():
            print(f"[Relais] ERREUR : absent : {p}", file=sys.stderr)
            return 2
    try:
        cible = ds.list_folder(TEST_ID)
    except ds.SyncError as e:
        print(f"[Relais] ÉCHEC D'ACCÈS au dossier test : {e}\n"
              "→ le dossier 1KeJIMwps… n'est probablement PAS partagé au compte "
              "de service z-ai-811@physichong.iam.gserviceaccount.com ; "
              "partagez-le ( Lecteur ) ou relancez l'OAuth du relais.",
              file=sys.stderr)
        return 2
    erreurs = 0
    for p in fichiers:
        md5 = ds.md5_of(p)
        r = cible.get(p.name)
        try:
            if r and r.get("md5Checksum") == md5:
                print(f"[Relais] inchangé : {p.name}")
                continue
            if r:
                ds.upload_update(r["id"], p)
                print(f"[Relais] mis à jour : {p.name} ({md5})")
            else:
                ds.upload_create(TEST_ID, p.name, p)
                print(f"[Relais] téléversé : {p.name} ({md5})")
        except ds.SyncError as e:
            print(f"[Relais] ERREUR {p.name} : {e}", file=sys.stderr)
            erreurs += 1
    try:
        apres = ds.list_folder(TEST_ID)
        for p in fichiers:
            r = apres.get(p.name)
            if not r or r.get("md5Checksum") != ds.md5_of(p):
                print(f"[Relais] VERIFICATION ÉCHOUÉE : {p.name}", file=sys.stderr)
                erreurs += 1
            else:
                print(f"[Relais] vérifié : {p.name} md5 MATCH")
    except ds.SyncError as e:
        print(f"[Relais] avertissement : vérification impossible ({e})",
              file=sys.stderr)
    return 1 if erreurs else 0


def corbeille_test(noms):
    try:
        entries = ds.list_folder(TEST_ID)
    except ds.SyncError as e:
        print(f"[Relais] ÉCHEC D'ACCÈS : {e}", file=sys.stderr)
        return 2
    erreurs = 0
    for nom in noms:
        f = entries.get(nom)
        if not f:
            print(f"[Relais] note : « {nom} » absent du dossier test (rien à faire)")
            continue
        print(f"[Relais] corbeille : {nom} (md5 {f.get('md5Checksum', '-')[:12]}…)")
        st, body, _ = ds.api("PATCH", f"{ds.API}/files/{f['id']}",
                             body={"trashed": True})
        if st not in (200, 204):
            print(f"[Relais] ERREUR corbeille {nom} : HTTP {st}", file=sys.stderr)
            erreurs += 1
    return 1 if erreurs else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--dossier-test" in args:
        i = args.index("--dossier-test")
        sys.exit(pousser_test(args[i + 1:]))
    if "--corbeille" in args:
        i = args.index("--corbeille")
        sys.exit(corbeille_test(args[i + 1:]))
    print("usage : relais_service_account.py --dossier-test F… | --corbeille F…",
          file=sys.stderr)
    sys.exit(2)
