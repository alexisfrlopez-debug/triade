#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_corpus_v21.py — LA PUBLICATION DU CORPUS v2.1 AU CONCEPT (la vague 16,
la commande du maître « termine tout et fais le dépôt sur zenodo »).

LA VOIE VÉRIFIÉE (le patron v230/v232 reconduit à la lettre) : newversion → le
bucket → les métadonnées → LA RE-VÉRIFICATION AVANT LE GESTE → PUBLISH → le
recoup md5 byte-byte au bord anonyme. La reprise idempotente aux tentatives
(la leçon D97 du 500).

L'OBJET : le corpus v2.1 — la FUITE PAR CONTRAT du v2 fermée (dix contrats
partagés entre TRAIN et DEV/TEST : le TEST v2 contaminé par construction),
les splits par GROUPE-DE-CONTRAT à la graine consignée 20261126, le TEST nu,
le canari unique au TRAIN, PLUS les 48 paires DPO au verdict du juge et les
recettes SFT/DPO/RLVR agnostiques en famille.
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOK = open(os.path.join(RACINE, ".gdrive", "zenodo.txt"), encoding="utf-8").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24463681"   # le corpus v2
CONCEPT = "10.5281/zenodo.24457524"
DOSSIER = os.path.join(RACINE, "depot-zenodo-corpus-v21")

FICHIERS_LOCAUX = {
    "train.jsonl": os.path.join(DOSSIER, "train.jsonl"),
    "dev.jsonl": os.path.join(DOSSIER, "dev.jsonl"),
    "test.jsonl": os.path.join(DOSSIER, "test.jsonl"),
    "permissif-ccby.jsonl": os.path.join(DOSSIER, "permissif-ccby.jsonl"),
    "sonde-contamination.json": os.path.join(DOSSIER, "sonde-contamination.json"),
    "dpo-paires.jsonl": os.path.join(DOSSIER, "dpo-paires.jsonl"),
    "MANIFESTE.json": os.path.join(DOSSIER, "MANIFESTE.json"),
    "DATASET-CARD.json": os.path.join(DOSSIER, "DATASET-CARD.json"),
    "RECETTES-SFT-DPO-RLVR.md": os.path.join(DOSSIER, "RECETTES-SFT-DPO-RLVR.md"),
}

DESCRIPTION = (
    "<p>TRIADE-CORPUS-v2.1: the contract-watertight release of the 169-triple "
    "training corpus of the TRIADE single-case study --- a development protocol "
    "under which an LLM agent writes native x86-64 code directly as assembly "
    "notation, governed by signed layer-I specifications. Version 2 had its "
    "splits drawn per task instance; since the v3, v4 and v6 campaigns all draw "
    "from the same eighteen layer-I contracts, ten contracts appeared in both "
    "TRAIN and DEV/TEST --- the TEST of v2 was contaminated by construction "
    "(six of its six contracts already read at TRAIN under another campaign). "
    "This release repairs the leak: the splits are drawn per CONTRACT GROUP at "
    "the consigned seed 20261126 (18 contracts to TRAIN 14, DEV 2, TEST 2), the "
    "TEST stays naked (validators only, no golden notation), the unique canary "
    "stays in TRAIN, and the audit replayed on the corrected set returns "
    "watertight (exit 0) with ten bit-identical rebuilds. Added in this "
    "release: the 48 DPO pairs --- chosen is a judge-green completion, rejected "
    "is a judge-refused completion, at the SAME contract (the reward is the "
    "judge's verdict, never a similarity), the P2 anti-hacking door refusing "
    "any mutated notation byte-byte --- and the family-agnostic SFT/DPO/RLVR "
    "recipes with the consigned compute budget. The v2 record "
    "(10.5281/zenodo.24463681) remains immutable; the named gaps live in the "
    "manifest.</p>"
)

METADATA = {
    "title": "TRIADE-CORPUS-v2.1: the 169-triple training corpus for "
             "native-notation tasks --- the contract-watertight splits (the v2 "
             "leak repaired), the 48 judge-verdict DPO pairs, fail-closed scrub "
             "door, contamination canary",
    "publication_date": "2026-11-23",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "dataset",
    "version": "v2.1",
}


def api(method, url, body=None, fichier=None, avec_jeton=True):
    headers = {}
    if avec_jeton:
        headers["Authorization"] = f"Bearer {TOK}"
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if fichier is not None:
        data = open(fichier, "rb").read()
        headers["Content-Type"] = "application/octet-stream"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    for tentative in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (500, 502, 503) and tentative < 3:
                print(f"    HTTP {e.code} vécu — la reprise idempotente "
                      f"({tentative + 2}/4)…")
                time.sleep(10 * (tentative + 1))
                continue
            return e.code, e.read()
        except urllib.error.URLError as e:
            if tentative < 3:
                print(f"    {e} — reprise ({tentative + 2}/4)…")
                time.sleep(10 * (tentative + 1))
                continue
            raise


def md5_de(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record corpus v2 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v2", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24463681 : état {d.get('state')}, version "
      f"{d.get('metadata', {}).get('version')}, concept {CONCEPT}")

# (2) LE BROUILLON DE NOUVELLE VERSION (le brouillon existant repris le cas échéant)
st, body = api("GET", "https://zenodo.org/api/deposit/depositions",
               "?q=&status=draft&size=25")
draft_url = None
if st == 200:
    for dep in json.loads(body):
        if dep.get("conceptdoi") == CONCEPT and \
                dep.get("state") in ("unsubmitted", "draft"):
            draft_url = dep["links"]["self"]
            print(f"[2] le brouillon existant repris : "
                  f"{draft_url.rstrip('/').split('/')[-1]}")
            break
if draft_url is None:
    st, body = api("POST", f"{RECORD}/actions/newversion")
    if st >= 400:
        print(f"[2] newversion : HTTP {st}")
        print(body.decode(errors="replace")[:500])
        sys.exit(1)
    d = json.loads(body)
    draft_url = d["links"]["latest_draft"]
    print(f"[2] le brouillon de version : "
          f"{draft_url.rstrip('/').split('/')[-1]} (concept {d.get('conceptdoi')})")

# (3) LES ANCIENS FICHIERS RETIRÉS, LES NEUF v2.1 POSÉS
st, body = api("GET", draft_url)
d = json.loads(body)
bucket = d["links"]["bucket"]
for f in d.get("files", []):
    st2, _ = api("DELETE", f"{d['links']['files'].split('?')[0]}/{f['id']}")
    print(f"    retiré du brouillon : {f['filename']} (HTTP {st2})")
for nom, chemin in FICHIERS_LOCAUX.items():
    st, body = api("PUT", f"{bucket}/{nom}", fichier=chemin)
    if st >= 400:
        print(body.decode(errors="replace")[:300])
        sys.exit(1)
    print(f"    posé : {nom} (HTTP {st})")

# (4) LES MÉTADONNÉES v2.1
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v2.1 posées : HTTP {st} ; fichiers : {len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v2.1"
fichiers = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
assert len(fichiers) == len(FICHIERS_LOCAUX), \
    f"fichiers inattendus : {list(fichiers)}"
for nom, chemin in FICHIERS_LOCAUX.items():
    assert nom in fichiers, f"absent du brouillon : {nom}"
    assert fichiers[nom] == md5_de(chemin), f"md5 divergent : {nom}"
    print(f"    recoupé md5 byte-byte : {nom}")
print("[5] la voie est VÉRIFIÉE — les neuf fichiers, la version, l'état")

# (6) LE GESTE — la publication à la commande du maître
st, body = api("POST", f"{draft_url}/actions/publish")
if st >= 400:
    print(f"[6] PUBLICATION : HTTP {st}")
    print(body.decode(errors="replace")[:500])
    sys.exit(1)
d = json.loads(body)
print(f"[6] PUBLIÉ : HTTP {st} — LE DOI DE VERSION {d.get('doi')} MINTÉ, "
      f"le concept {d.get('conceptdoi')} résolvant sur "
      f"{d.get('metadata', {}).get('version')}")

# (7) LA VÉRIFICATION FRAÎCHE au bord anonyme
time.sleep(5)
nouveau = str(d["id"])
with urllib.request.urlopen(f"https://zenodo.org/api/records/{nouveau}",
                            timeout=60) as r:
    v = json.loads(r.read())
print(f"[7] le bord anonyme : records/{nouveau} — {v['metadata']['version']}")
for f in v["files"]:
    loc = FICHIERS_LOCAUX.get(f["key"])
    ok = loc and f["checksum"].endswith(md5_de(loc))
    print(f"    {f['key']} md5 {'ÉGAUX' if ok else 'ROUGE !'}")
with urllib.request.urlopen(
        f"https://zenodo.org/api/records/{CONCEPT.split('.')[-1]}",
        timeout=60) as r:
    c = json.loads(r.read())
print(f"    le concept résout sur : {c['metadata']['version']} (record {c['id']})")
