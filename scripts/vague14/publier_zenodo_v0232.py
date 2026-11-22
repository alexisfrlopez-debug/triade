#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0232.py — LA PUBLICATION DE LA v0.23.2 AU CONCEPT (la
vague 14, la génération corrective — la commande du maître : « je n'ai
pas la version presentation et soumission du pack dans zenodo »). LA VOIE
VÉRIFIÉE (le patron v230) : newversion → le bucket → les métadonnées →
PUBLISH ; la reprise idempotente aux tentatives (la leçon D97 du 500
vécu à la v0.22.1). LES TROIS PACKS à la version courante : la
SOUMISSION et la PRÉSENTATION portées à v0.23.2 (l'écart de la v0.23.1
soldé) avec le COMPLET régénéré."""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/mirrors_zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24442241"  # v0.23.1
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.23.2.zip":
        "/home/z/my-project/depot/depot-zenodo-v0232/"
        "TRIADE_soumission_v0.23.2.zip",
    "TRIADE_complet_v0.23.2.zip":
        "/home/z/my-project/depot/depot-zenodo-v0232/"
        "TRIADE_complet_v0.23.2.zip",
    "TRIADE_presentation_v0.23.2.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.23.2.zip",
}

DESCRIPTION = (
    "<p>The academic edition v0.23.2 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version is the CORRECTIVE "
    "GENERATION closing the fourteenth instruction wave: the five "
    "documents regenerated from the corrected sources, and the "
    "cross-piece linter extended. (1) The ten sourced corrections "
    "(a)-(j) carried to the documents: the GHASH corridor restated at its "
    "adopted schoolbook canon (63.39 cycles [IQR 30] against the sealed "
    "806.35, a 12.7x gain; the karatsuba variant delivered at 64.04, the "
    "0.65-cycle gap inside the IQR); the M4 floor-ratio published at its "
    "unrounded operands (6.912/2.056 = 3.362); the three-effect "
    "ventilation closure stated at its unrounded operands "
    "(20.715+16.497+0.213 = 37.425 s = T-(C+G)); the replication grid "
    "renamed F/L (D203, lifting the T/X collision); the mutant-exclusion "
    "family 'the field beyond the pattern' carried to the English "
    "abstract; the Book of the Vault cover banner carried to v1.7; the "
    "specification's 'fourteen trees'. (2) The fourteenth wave carried "
    "to the body: the GHASH aggregation at four blocks with deferred "
    "reduction at 19.66 cycles per multiplication [IQR 19] --- a 41.0x "
    "gain on the seal and 3.23x on the wave-13 corridor; the "
    "content-addressed memoisation of the verification regime at -89.4 "
    "per cent with no control removed (H-CGP4 held); TPL-ADD-v4 with its "
    "counter-example repair converting its first honest refusal at 7/18 "
    "greens for a median 3,990 tokens; the H7 replication order drawn "
    "and signed (the campaign open to the 28 units); the first effective "
    "Tamarin run falsifying the implication lemma --- a named modelling "
    "defect (the shares as public variables), the amendment written and "
    "re-hashed, no verdict fabricated. (3) The linter extension: four "
    "new rule classes --- the version strings (banners, covers, dates, "
    "decision ranges), the family decompositions recomposed by code "
    "from the CSV/JSONL raw files, every published ratio carrying its "
    "unrounded operands, and the detection of the dated T/X labels "
    "outside their era markers --- running at 153 green, 0 red, with the "
    "negative control refusing five injected divergences. The three "
    "packs (submission, presentation, complete) are assembled at the "
    "current version: the v0.23.1 corrective release had carried the "
    "corrected sources in the complete archive alone, the submission "
    "and presentation packs remaining byte-byte at their v0.23.0 state "
    "--- this generation carries all three to the current version.</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.23.2) — "
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
    "version": "v0.23.2",
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


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.23.1 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.1", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24442241 : état {d.get('state')}, version "
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

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS v0.23.2 POSÉS
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

# (4) LES MÉTADONNÉES v0.23.2
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.23.2 posées : HTTP {st} ; fichiers : "
      f"{len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.2"
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
