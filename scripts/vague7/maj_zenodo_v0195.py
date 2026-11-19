#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_zenodo_v0195.py — la nouvelle version du record Zenodo : le brouillon
de version v0.19.5 créé au geste du concept DOI (10.5281/zenodo.24367343),
les TROIS fichiers v0.19.5 posés (les anciens retirés du brouillon), les
métadonnées posées — puis PUBLICATION SEULEMENT à l'option --publier (le
geste du maître ; jamais un DOI minté sans commande explicite)."""
import json
import sys
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/keys/zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24379173"
DRAFT_CONNU = "https://zenodo.org/api/deposit/depositions/24382460"
DEPOT = "/home/z/my-project/depot/depot-zenodo-v0195"

DESCRIPTION = (
    "<p>The academic edition v0.19.5 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version succeeds v0.19.4 under "
    "the same concept DOI and closes the seventh instruction wave. (1) "
    "The pre-registered D210 plan brought to its term: the sample "
    "criterion held at N=7 fully instrumented units at both arms (the "
    "application and loupe-01/02/05/08/13/16), read from the delivery "
    "register without any new draw, the conditional amendment never "
    "triggered. (2) The fault-injection battery over the fifty-six named "
    "mutation survivors: sixteen application scenarios at the evidence "
    "conventions, the v0.14.0 console reproduced identically first "
    "(776/832 at the consigned seed), then thirty-five survivors killed "
    "by injection for 811/832 (97.5 percent; 83.4 to 93.3 to 97.5 across "
    "the three programmes), the twenty-one remaining each named to one "
    "of thirteen cause families, no killer weakened, the sealed pieces "
    "untouched (the battery writes to the emulations). (3) The "
    "inter-family independence attempt with the gap named, never "
    "simulated: the mathematical confrontation held at zero divergence "
    "before any generation; the local open-weights second family "
    "(Qwen2.5-Coder-1.5B) recites 0/64 + 0/64 at the pure probe and "
    "copies at correction; the generated C arm passes the POSIX "
    "differential at 1984/2011 with the short-range gap named. (4) The "
    "evaluation packet: the one-command reproduction at the consigned "
    "seeds, the coded defect grid (eleven defects), the pre-registered "
    "second-annotator protocol at kappa >= 0.61, the calculator "
    "autotested. (5) The governance status carried as lived: the D183 "
    "vault-key sequestration ceremony lived end-to-end on 19 November "
    "(five-part threshold-three split, cold reconstitution proven "
    "twice), the committed phrase rotated and the old one refused, the "
    "full-history secrets scan re-tried (ten findings triaged, no real "
    "token ever committed), the GitHub repository public at decision "
    "D220 — the v0.19.4 lines stating the ceremony 'prepared and "
    "waiting' had become stale at their own sealing and are corrected "
    "here to the lived status. This deposit contains the manuscript "
    "v0.19.5, the specification v0.15.4 (unchanged: no rule modified), "
    "the Book of the Vault v1.3 (unchanged), the proofs and calculations "
    "v0.19.5 (the instruction, independence and fault-replay reports "
    "verbatim), the 20/11 presentation at the exact status, the "
    "consolidated data tables (the K4 battery, the 56-survivor triage, "
    "the 21 named remains, the delivery register, the coded grid), the "
    "complete edition sources, and the ten-point verification report. "
    "License: Business Source License 1.1 with an academic Additional "
    "Use Grant (peer review, artifact evaluation, scientific "
    "replication, non-commercial research; effective 2026-11-17, "
    "decision D209; Change Date 2030-10-28 converting to GPLv3+).</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.19.5) — "
             "manuscript, data tables, complete sources and verification "
             "evidence",
    "publication_date": "2026-11-20",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis", "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.19.5",
}

FICHIERS = [
    (f"{DEPOT}/TRIADE_soumission_v0.19.5.zip", "TRIADE_soumission_v0.19.5.zip"),
    (f"{DEPOT}/TRIADE_complet_v0.19.5.zip", "TRIADE_complet_v0.19.5.zip"),
    ("/home/z/my-project/depot/scripts/vague7/"
     "TRIADE_presentation_v0.19.5_20261120.zip",
     "TRIADE_presentation_v0.19.5_20261120.zip"),
]


def api(method, url, body=None, fichier=None):
    headers = {"Authorization": f"Bearer {TOK}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    if fichier is not None:
        data = open(fichier, "rb").read()
        headers["Content-Type"] = "application/octet-stream"
    req = urllib.request.Request(url, data=data, method=method,
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


# (1) le brouillon de nouvelle version — le brouillon connu repris s'il
#     vit encore, sinon le geste newversion au record v0.19.4
draft_url = None
st, body = api("GET", DRAFT_CONNU)
if st == 200 and json.loads(body).get("state") in ("unsubmitted", "draft") \
        and json.loads(body).get("metadata", {}).get("version") is None:
    draft_url = DRAFT_CONNU
    print(f"[1] le brouillon existant repris : 24382460")
else:
    st, body = api("POST", f"{RECORD}/actions/newversion")
    print(f"[1] nouvelle version : HTTP {st}")
    if st >= 400:
        print(body.decode(errors="replace")[:400])
        sys.exit(1)
    d = json.loads(body)
    draft_url = d["links"]["latest_draft"]
    print(f"    le brouillon : {draft_url.rstrip('/').split('/')[-1]} "
          f"(concept {d.get('conceptdoi')})")

# (2) les fichiers v0.19.4 retirés du brouillon, les v0.19.5 posés
st, body = api("GET", draft_url)
d = json.loads(body)
bucket = d["links"]["bucket"]
for f in d.get("files", []):
    if f["filename"].startswith("TRIADE_"):
        st2, _ = api("DELETE",
                     f"{d['links']['files'].split('?')[0]}/{f['id']}")
        print(f"    retiré du brouillon : {f['filename']} (HTTP {st2})")
for chemin, nom in FICHIERS:
    st, body = api("PUT", f"{bucket}/{nom}", fichier=chemin)
    if st >= 400:
        print(body.decode(errors="replace")[:300])
        sys.exit(1)
    print(f"    posé : {nom} (HTTP {st})")

# (3) les métadonnées v0.19.5 posées
st, body = api("PUT", draft_url, {"metadata": METADATA})
print(f"[3] métadonnées v0.19.5 posées : HTTP {st}")
if st >= 400:
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"    titre : {d['metadata']['title'][:70]}…")
print(f"    version : {d['metadata'].get('version')} | "
      f"fichiers : {len(d.get('files', []))}")

# (4) LA PUBLICATION — le geste du maître
if "--publier" in sys.argv:
    st, body = api("POST", f"{draft_url}/actions/publish")
    print(f"[4] PUBLICATION : HTTP {st}")
    if st >= 400:
        print(body.decode(errors="replace")[:400])
        sys.exit(1)
    d = json.loads(body)
    print(f"    DOI de version : {d.get('doi')}")
    print(f"    concept DOI    : {d.get('conceptdoi')}")
    print(f"    état           : {d.get('state')}")
else:
    print("[4] publication DIFFÉRÉE — le brouillon v0.19.5 attend le geste "
          "du maître (relancer avec --publier)")
