#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""maj_zenodo_v0194.py — la nouvelle version du record Zenodo : métadonnées
v0.19.4 posées au brouillon 24379173 (les trois fichiers déjà recoupés md5),
puis PUBLICATION. Le DOI de version est minté au geste — jamais inventé."""
import json
import sys
import urllib.request
import urllib.error

TOK = open("/home/z/my-project/keys/zenodo.txt").read().strip()
DRAFT = "https://zenodo.org/api/deposit/depositions/24379173"

DESCRIPTION = (
    "<p>The academic edition v0.19.4 of the TRIADE single-case study: a development "
    "protocol under which an LLM agent writes native x86-64, RISC-V and TLS 1.3 code "
    "directly as assembly notation, governed by signed layer-I specifications. This "
    "version succeeds v0.19.0 under the same concept DOI and carries the seventh "
    "instruction wave to its fourth step. (1) The OPT-04 pointer-only response format "
    "for the locate operation, measured on 36 real calls (glm-4-plus, consigned seed, "
    "100 percent logged API): total 1,714 to 1,103 native tokens (a 35.7 percent "
    "reduction), response 770 to 52 (93.3 percent), zero divergence 18/18, client-side "
    "expansion with four named fail-closed refusals; the specification v0.15.4 carries "
    "the additive rule, no existing rule modified. (2) The adopted verification stack: "
    "memo v2 (key superset over file, input, contract, emulator config, seed and "
    "oracle; run counter chained inside the signed core; a 1-in-10 audit with live "
    "re-execution and field-by-field identity at zero deviation) and the dual engine "
    "with QEMU-user at volume through a static C launcher executing the harness-built "
    "image and Unicorn as reference at the consigned sample: zero divergence over "
    "2,041 operations, the mutated shim engine caught. (3) The M4 loop cost under "
    "R11: before 39.7 s median [39.4-40.3] n=5 against the adopted stack at 6.8 s "
    "warm regime (cold 6.7 s; dedicated audit 39.1 s; C arm 2.2 s) on the same "
    "2-core machine class: the ratio falls from 17.9x to 3.0x, under the "
    "pre-registered 10x threshold, so hypothesis H5 becomes held by explicit master "
    "instruction while the D204 falsification remains consigned as measured and "
    "dated, the inter-machine variance named on pieces. (4) The CF3 model extension "
    "closed the session gap (rule 4 at both phases, the guard of the concrete "
    "sentinel), with a 30,000-trace generative campaign at three seeds at zero "
    "divergence and a 96/96 battery (TLC sealed 154/896 reproduced; extended "
    "154/926 invariant reachable space; Apalache inductive obligations discharged; "
    "31 negative controls caught), and the constant-time instrument hardened to the "
    "hash of complete traces: one single fingerprint per target over 120 "
    "measurements, public anonymous clone. (5) The vault-key sequestration ceremony "
    "D183 lived end-to-end (5-part threshold-3 split, cold reconstitution proven "
    "twice), the committed phrase rotated and the old one refused, the full-history "
    "secrets scan re-tried (ten findings triaged, no real token ever committed), and "
    "the GitHub repository made public at the explicit master decision D220, joining "
    "the Zenodo DOI. This deposit contains the manuscript v0.19.4 (the pointer at "
    "RQ2; H5 held with the amendment added to the falsified verdict, which remains), "
    "the specification v0.15.4, the Book of the Vault v1.3 (unchanged), the proofs "
    "and calculations v0.19.4, the 20/11 presentation at the exact status, the "
    "consolidated data tables (the RQ2 instrumented round-trip measurements, the "
    "D204 and D210 campaign ledgers, the OPT-04 token campaign, the M4 pile "
    "measurements; every value generated from the raw registers), the complete "
    "edition sources, the TLA+ models, and the ten-point verification report. "
    "License: Business Source License 1.1 with an academic Additional Use Grant "
    "(peer review, artifact evaluation, scientific replication, non-commercial "
    "research; effective 2026-11-17, decision D209; Change Date 2030-10-28 "
    "converting to GPLv3+).</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.19.4) — "
             "manuscript, data tables, complete sources and verification evidence",
    "publication_date": "2026-11-20",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis", "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.19.4",
}


def api(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {TOK}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


# (1) les métadonnées posées
st, body = api("PUT", DRAFT, {"metadata": METADATA})
print(f"[1] métadonnées v0.19.4 posées : HTTP {st}")
if st >= 400:
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"    titre : {d['metadata']['title'][:70]}…")
print(f"    version : {d['metadata'].get('version')} | fichiers : {len(d.get('files', []))}")

# (2) LA PUBLICATION — le geste du maître (« mets a jour zenodo »)
if "--publier" in sys.argv:
    st, body = api("POST", f"{DRAFT}/actions/publish")
    print(f"[2] PUBLICATION : HTTP {st}")
    if st >= 400:
        print(body.decode(errors="replace")[:400])
        sys.exit(1)
    d = json.loads(body)
    print(f"    DOI de version : {d.get('doi')}")
    print(f"    concept DOI    : {d.get('conceptdoi')}")
    print(f"    état           : {d.get('state')}")
    print(f"    url            : {d.get('links', {}).get('record_html') or d.get('links', {}).get('html')}")
else:
    print("[2] publication DIFFÉRÉE (relancer avec --publier)")
