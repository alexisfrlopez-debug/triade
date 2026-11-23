#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0234.py — LA RELEASE CORRECTIVE v0.23.4 AU CONCEPT
(10.5281/zenodo.24367343), la vague 16, la commande du maître « fais une mise à
jour des kits soumission/présentation et complet sur les dépôts git/drive et
zenodo si besoin ».

LA VOIE VÉRIFIÉE (le patron v230/v232/v233 reconduit) : newversion → le bucket →
les métadonnées → LA RE-VÉRIFICATION AVANT LE GESTE → PUBLISH → le recoup md5
byte-byte au bord anonyme.

LES TROIS ARCHIVES : le complet v0.23.4 RÉGÉNÉRÉ ; la soumission et la
présentation RECONDUITES OCTET POUR OCTET sous leur nom d'origine v0.23.3 (les
cinq pièces n'ont pas bougé — le précédent de la release corrective v0.23.1).
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
RECORD = "https://zenodo.org/api/deposit/depositions/24450872"   # l'édition v0.23.3
CONCEPT = "10.5281/zenodo.24367343"
DOSSIER = os.path.join(RACINE, "depot-zenodo-v0234")

FICHIERS_LOCAUX = {
    "TRIADE_complet_v0.23.4.zip": os.path.join(DOSSIER, "TRIADE_complet_v0.23.4.zip"),
    "TRIADE_soumission_v0.23.3.zip": os.path.join(DOSSIER, "TRIADE_soumission_v0.23.3.zip"),
    "TRIADE_presentation_v0.23.3.zip": os.path.join(DOSSIER, "TRIADE_presentation_v0.23.3.zip"),
}

DESCRIPTION = (
    "<p>The academic edition v0.23.4 of the TRIADE single-case study: a development "
    "protocol under which an LLM agent writes native x86-64, RISC-V and TLS 1.3 code "
    "directly as assembly notation, governed by signed layer-I specifications. This "
    "is a CORRECTIVE RELEASE: the five documents did not move --- their five sha256 "
    "are byte-identical to v0.23.3, so the submission and the presentation packs are "
    "carried over byte-for-byte under their original names (the v0.23.1 precedent); "
    "the complete archive is regenerated and carries the sixteenth instruction wave "
    "(23 Nov 2026).</p>"
    "<p>(1) THE SPLIT LEAK, FOUND AND REPAIRED. Version 2 of the training corpus had "
    "its splits drawn per task instance; since the v3, v4 and v6 campaigns all draw "
    "from the same eighteen layer-I contracts, ten contracts appeared in both TRAIN "
    "and DEV/TEST --- the v2 TEST was contaminated by construction (all six of its "
    "contracts already read at TRAIN under another campaign). The audit is mechanical "
    "and exits non-zero on a leak; the repair draws the splits per CONTRACT GROUP at "
    "the consigned seed 20261126 (18 contracts to TRAIN 14, DEV 2, TEST 2), keeps the "
    "TEST naked (validators only), keeps the unique canary in TRAIN, and the replayed "
    "audit returns watertight with ten bit-identical rebuilds. The corrected corpus "
    "v2.1 is deposited at the corpus concept (version DOI 10.5281/zenodo.24479882); "
    "the v2 record remains immutable.</p>"
    "<p>(2) THE SIX RESIDUALS, TRANCHE PAR LA MACHINE. The cross-piece linter is "
    "extended with three new classes --- every published ratio recomputed from its "
    "published operands at the displayed precision, the announced decision range "
    "checked against the LOCAL table, and the target-versus-split consistency --- with "
    "its planted negative control caught. Run on the pieces, it confirms a real "
    "residual: the published ratio 3.23 (aggregate against corridor) does not "
    "recompute from its published operands (63.39/19.66 = 3.2243, i.e. 3.22 at two "
    "decimals), while the six other published ratios recompute exactly --- the defect "
    "is isolated and awaits the unrounded medians at the next regeneration. It also "
    "names 43 holes inside the announced D1--D251 range at the local decision table, "
    "and re-scopes the >= 15/18 headline target to the corrected TEST (19 lines, 2 "
    "contracts).</p>"
    "<p>(3) THE SEALED CHAIN, REPRODUCED TO THE BYTE. The GHASH composition corridor "
    "is assembled with keystone at its stable RVA 0xF800, round-tripped through "
    "capstone and reassembled: the byte stream is identical, the differential against "
    "the sealed chain shows ZERO deviation (sha256 ddedc26c... reconstructed from "
    "source, matching the wave-15 register), ten rebuilds are bit-identical, the "
    "time-constant trace-hash yields one fingerprint per class and the fail-closed "
    "bounds refuse N=0 and N=257. The bare-metal kit ships with an aggregator that "
    "REFUSES a missing run (exit 2, never a partial verdict); the CPUID dispatch "
    "resolves all 32 flag combinations without a dead path; and the token overhead of "
    "governance is measured: 34,663 tokens read per change against the 627/674/2,200 "
    "budgets --- 15 to 55 times the change it protects --- 732 tokens once compressed.</p>"
    "<p>(4) THE CONSTRAINED DECODING INSTRUMENT AND THE RULE GAP IT EXPOSES. The "
    "canonical TPL-ADD grammar is delivered executable (a GBNF source for local "
    "serving plus a deterministic validator, 8/8 controls). Applied to the 24 "
    "judge-green completions of the corpus, it accepts 3 and refuses 21 --- seventeen "
    "of them define &quot;LBL-xxx :&quot; labels that the contract explicitly forbids. "
    "The judge is therefore more permissive than the grammar it states: a constrained "
    "decoder would CHANGE the acceptance set, not merely eliminate the out-of-format "
    "class, and any future constrained campaign must name that gap. The 48 DPO pairs "
    "(chosen = a judge-green completion, rejected = a judge-refused completion at the "
    "SAME contract, the reward being the judge's verdict and never a similarity, the "
    "P2 door refusing any mutated notation byte-byte) and the family-agnostic "
    "SFT/DPO/RLVR recipes with the consigned compute budget are deposited with the "
    "corpus v2.1. The Tamarin/ProVerif closure kit ships as exact commands with the "
    "budgets named inside the commands, the negative first, and a runner that refuses "
    "to execute off the real workstation.</p>"
    "<p>(5) NAMED REPRODUCIBILITY DEFECTS, TO BE FIXED AT THE NEXT GENERATION. The "
    "edition linter depends on a gitignored log that was never committed --- the gate "
    "cannot be replayed from the public repository, although reconstructing it from "
    "the committed JSONL reproduces its constants exactly (60 calls, 18 tasks, 5 "
    "greens, median 4,604), proving the log redundant. And its verdict depends on the "
    "pdftotext version: replayed with pdftotext 26.09.0 on the byte-identical pieces "
    "it returns 222 green and 1 red (three extra numeric tokens in the manuscript "
    "extraction out of 1,991 controlled) --- the drift belongs to the extractor, "
    "never to the pieces.</p>"
    "<p>Still to be performed at the real workstation, and named as such: the v6 "
    "constrained campaign itself, the bare-metal cycle measurement (two machines at "
    "least), the regeneration of the five documents (tectonic + weasyprint, with the "
    "residuals linter ready to control it), the Tamarin/ProVerif runs (a 16 GB Linux "
    "post), the Windows SACL/4663 sentinel, the FIDO2 prototype and the era "
    "ceremony.</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand Under "
             "Signed-Intent Governance (Academic Edition v0.23.4) — manuscript, "
             "data tables, complete sources and verification evidence",
    "publication_date": "2026-11-23",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.23.4",
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
            with urllib.request.urlopen(req, timeout=1800) as r:
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


st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.3", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24450872 : état {d.get('state')}, version "
      f"{d.get('metadata', {}).get('version')}, concept {CONCEPT}")

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

st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.23.4 posées : HTTP {st} ; fichiers : {len(d.get('files', []))}")

st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), f"état : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.23.4"
fichiers = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
assert len(fichiers) == 3, f"fichiers inattendus : {list(fichiers)}"
for nom, chemin in FICHIERS_LOCAUX.items():
    assert nom in fichiers, f"absent du brouillon : {nom}"
    assert fichiers[nom] == md5_de(chemin), f"md5 divergent : {nom}"
    print(f"    recoupé md5 byte-byte : {nom}")
print("[5] la voie est VÉRIFIÉE — les trois fichiers, la version, l'état")

st, body = api("POST", f"{draft_url}/actions/publish")
if st >= 400:
    print(f"[6] PUBLICATION : HTTP {st}")
    print(body.decode(errors="replace")[:500])
    sys.exit(1)
d = json.loads(body)
print(f"[6] PUBLIÉ : HTTP {st} — LE DOI DE VERSION {d.get('doi')} MINTÉ, "
      f"le concept {d.get('conceptdoi')} résolvant sur "
      f"{d.get('metadata', {}).get('version')}")

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
