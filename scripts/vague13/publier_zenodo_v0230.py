#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0230.py — LA PUBLICATION DE LA v0.23.0 AU CONCEPT (la
vague 13, la commande du maître « il faudra ensuite mettre a jour les
miroirs et zenodo » — le précédent des v0.21.0/v0.22.0/v0.22.1). LA VOIE
VÉRIFIÉE : newversion → le bucket → les métadonnées → PUBLISH ; la
reprise idempotente aux tentatives (la leçon D97 du 500 vécu à la
v0.22.1)."""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/mirrors_zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24420007"  # v0.22.1
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.23.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0230/"
        "TRIADE_soumission_v0.23.0.zip",
    "TRIADE_complet_v0.23.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0230/"
        "TRIADE_complet_v0.23.0.zip",
    "TRIADE_presentation_v0.23.0.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.23.0.zip",
}

DESCRIPTION = (
    "<p>The academic edition v0.23.0 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version carries the thirteenth "
    "instruction wave and restates the programme in one voice, with a "
    "frozen edition changelog. (1) The GHASH corridor in PCLMULQDQ: "
    "karatsuba at 64.04 and schoolbook at 63.39 cycles against the "
    "sealed 806.35 (a 12.6x gain, the pre-registered target of 80 "
    "cycles met), the full AES-GCM composition measured against OpenSSL "
    "EVP (7.556 cycles per byte at 4096; the composition ahead of EVP "
    "at the 64-byte message), the structural constant-time property "
    "verified (one trace fingerprint per class, no variable-latency "
    "instruction on secrets). (2) The three requalifications: the 58 "
    "memory-safety guards stated conditional assumption-discharged with "
    "the exhaustive TCB (24 plan-field, 23 caller-contract, 11 OS), "
    "the fifteen mutant exclusions stated proved-argued-bounded (twelve "
    "named semantic arguments, three bounded sweeps), the CF3 Tamarin "
    "model v2 with the adversary-at-threshold restriction removed and "
    "the implication lemma secret-learnt-implies-three-shares added "
    "(the prover absent from the assembly sandbox, the gap named, no "
    "verdict fabricated). (3) The four-arm ventilation at equalised "
    "rebuild volumes: the intrinsic-notation share at 5.5 percent "
    "(H-CGP3 held) --- the wave-eleven notation effect was the "
    "verification implementation. (4) TPL-ADD-v3: the format grammar "
    "published to the client with a repair loop (budget three), "
    "feasibility 6/18 with the residual gap named by refusal class, "
    "the cost per validated change at 3,844 tokens, the edit operation "
    "at 18/18 for 712. (5) The semantic-perimeter purge: the Book of "
    "the Vault v1.7 and the specification v0.15.8, with the "
    "pre-commit/pre-push guard by known-secret fingerprints and "
    "entropy. (6) The edition generation: the exact partition of the "
    "559-vector battery (16+3+4+13+3+8+512), the unrounded operands of "
    "every ratio published (the cache canon 285.725 to 0.418 ms = "
    "683.6x), the EN and FR abstracts generated from the same macros "
    "(compared field by field by script, zero value divergence), the "
    "canonical adopted-budgets table, and the specification's dashboard "
    "aligned on it. The inter-piece linter runs at 71 green, 0 red over "
    "every numeric token of the five documents, with a lived negative "
    "control.</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.23.0) — "
             "manuscript, data tables, complete sources and verification "
             "evidence",
    "publication_date": "2026-11-22",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.23.0",
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
    req = urllib.request.Request(url, data=data, method=method,
                                 headers=headers)
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


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.22.1 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.22.1", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24420007 : état {d.get('state')}, version "
      f"{d.get('metadata', {}).get('version')}, concept {CONCEPT}")

# (2) LE BROUILLON DE NOUVELLE VERSION (le brouillon existant repris le
#     cas échéant — l'idempotence)
st, body = api("GET",
               "https://zenodo.org/api/deposit/depositions",
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
          f"{draft_url.rstrip('/').split('/')[-1]} (concept "
          f"{d.get('conceptdoi')})")

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS v0.23.0 POSÉS
st, body = api("GET", draft_url)
d = json.loads(body)
bucket = d["links"]["bucket"]
for f in d.get("files", []):
    if f["filename"].startswith("TRIADE_"):
        st2, _ = api("DELETE",
                     f"{d['links']['files'].split('?')[0]}/{f['id']}")
        print(f"    retiré du brouillon : {f['filename']} (HTTP {st2})")
for nom, chemin in FICHIERS_LOCAUX.items():
    st, body = api("PUT", f"{bucket}/{nom}", fichier=chemin)
    if st >= 400:
        print(body.decode(errors="replace")[:300])
        sys.exit(1)
    print(f"    posé : {nom} (HTTP {st})")

# (4) LES MÉTADONNÉES v0.23.0
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.23.0 posées : HTTP {st} ; fichiers : "
      f"{len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.0"
fichiers = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
assert len(fichiers) == 3, f"fichiers inattendus : {list(fichiers)}"
for nom, chemin in FICHIERS_LOCAUX.items():
    assert nom in fichiers, f"absent du brouillon : {nom}"
    assert fichiers[nom] == md5_de(chemin), f"md5 divergent : {nom}"
    print(f"    recoupé md5 byte-byte : {nom}")
print("[5] la voie est VÉRIFIÉE — les trois fichiers, la version, l'état")

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
with urllib.request.urlopen(
        f"https://zenodo.org/api/records/{nouveau}", timeout=60) as r:
    v = json.loads(r.read())
print(f"[7] le bord anonyme : records/{nouveau} — "
      f"{v['metadata']['version']}")
for f in v["files"]:
    loc = FICHIERS_LOCAUX.get(f["key"])
    ok = loc and f["checksum"].endswith(md5_de(loc))
    print(f"    {f['key']} md5 {'ÉGAUX' if ok else 'ROUGE !'}")
with urllib.request.urlopen(
        f"https://zenodo.org/api/records/{CONCEPT.split('.')[-1]}",
        timeout=60) as r:
    c = json.loads(r.read())
print(f"    le concept résout sur : "
      f"{c['metadata']['version']} (record {c['id']})")
