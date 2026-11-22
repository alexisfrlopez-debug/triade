#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0233.py — LA PUBLICATION DE LA v0.23.3 AU CONCEPT (la
vague 15, la release — la commande du maître « ok pour la suite (release
de la vague etc…) »). LA VOIE VÉRIFIÉE (les patrons v230/v232) :
newversion → le bucket → les métadonnées → PUBLISH ; la reprise
idempotente aux tentatives (la leçon D97 du 500 vécu à la v0.22.1). LES
TROIS PACKS à la version courante."""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/mirrors_zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24442951"  # v0.23.2
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.23.3.zip":
        "/home/z/my-project/depot/depot-zenodo-v0233/"
        "TRIADE_soumission_v0.23.3.zip",
    "TRIADE_complet_v0.23.3.zip":
        "/home/z/my-project/depot/depot-zenodo-v0233/"
        "TRIADE_complet_v0.23.3.zip",
    "TRIADE_presentation_v0.23.3.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.23.3.zip",
}

DESCRIPTION = (
    "<p>The academic edition v0.23.3 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version is the RELEASE OF THE "
    "FIFTEENTH INSTRUCTION WAVE: the five documents regenerated under the "
    "five-class cross-piece linter, and the wave's results carried to the "
    "body. (1) The five linter classes, lived: the semantic phrase "
    "retired from the specification ('the compiler is never delivered; "
    "the sealed notation is'), the decision ranges recomputed against the "
    "journal, every feasibility count n/18 now dated at its epoch with "
    "the current v5 campaign (November 2026) named apart at 5/18 --- its "
    "pre-registered target of 15/18 MISSED and the unfavourable reading "
    "consigned (the subject's CLI variance named, the judges intact), "
    "the post-deposit version claims restated at the current version, "
    "and the English gallicisms healed ('settled on pieces'; the "
    "five-share threshold-three Shamir escrow). (2) The fifteenth wave "
    "carried: the interleaved CTR x GHASH composition measured at 0.7271 "
    "cycles per byte at 4 KiB (median 2,978.2 cycles [IQR 5.6] per "
    "4,096-byte call; the pre-registered target of 2.0 held at 36 per "
    "cent; OpenSSL EVP at 0.5757 --- 2,357.9 cycles --- on the same "
    "silicon, the corridor within 1.26x of the tuned library; the sealed "
    "per-block chain 68.7x behind at 204,544.5 cycles, no control "
    "removed); the guard TCB reduced 58 to 34 to 11 (the eleven-guard "
    "corridor emitted at the virgin margin 0xFC00 --- 424 bytes, the "
    "falsified guard refused at both boundaries and on the index face, "
    "the harness 36/36; the rejeu of the 116 certificates consigned at "
    "its corrected invocation in an append-only erratum, the first-pass "
    "invocation bug named); the native oracle engine line-identical to "
    "the Unicorn twin on both sealed crypto bodies (the "
    "content-addressed memo, the gate, the chained 1-in-10 audit; the "
    "medians 0.960 ms to 0.000185 ms at the hit, a 5189x gain at the "
    "unrounded operands, orthogonal to the regime memoisation); "
    "TPL-ADD-v5 at 5/18 greens for a median 4,604 tokens (both targets "
    "missed, never a number adjusted); the H7 replication campaign "
    "served (the generator re-executed bit-identically at the canonical "
    "sha, the fail-closed aggregator with the D207 stop rules lived at "
    "the refusal, the second annotator's kit re-autotested, the "
    "independence confound named at 0/64); the CF3-v3 Tamarin model at "
    "the verdict machine (L3 verified at 1,122 steps; the five other "
    "lemmata incomplete at the 4 GiB memory wall of the sandbox --- the "
    "cause named, the way for the real machine; the ProVerif port "
    "delivered); and the adoption-side ecosystem assembled by "
    "construction (the 109-triple training corpus with sealed splits, "
    "the typed-reward training environment, the re-playable capability "
    "ladder, the model-independent agent guide, the canonical-English "
    "documentation core, the 156-piece developer kit with no trust "
    "anchor shipped, the pre-registered hardware protocols). The three "
    "packs (submission, presentation, complete) are assembled at the "
    "current version and published together.</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.23.3) — "
             "manuscript, data tables, complete sources and verification "
             "evidence",
    "publication_date": "2026-11-23",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.23.3",
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


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.23.2 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.2", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24442951 : état {d.get('state')}, version "
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

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS v0.23.3 POSÉS
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

# (4) LES MÉTADONNÉES v0.23.3
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.23.3 posées : HTTP {st} ; fichiers : "
      f"{len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.3"
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
