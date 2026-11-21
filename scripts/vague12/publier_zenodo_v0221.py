#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0221.py — LA PUBLICATION DE LA RELEASE v0.22.1 AU CONCEPT
(la vague 12, la commande du maître « il faudra ensuite mettre a jour les
miroirs et zenodo »). LA VOIE VÉRIFIÉE du modèle v0.22.0 : newversion → le
bucket → les métadonnées → PUBLISH. Les TROIS fichiers : la soumission et
la présentation DEMEURÉES byte-byte (l'édition v0.22.0 immuable), le
complet RÉGÉNÉRÉ (les six ateliers de la douzième vague, les chaînes
corrigées, le linter v230)."""
import hashlib
import json
import sys
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/acces_miroirs/zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24407701"  # v0.22.0
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.22.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0220/"
        "TRIADE_soumission_v0.22.0.zip",
    "TRIADE_complet_v0.22.1.zip":
        "/home/z/my-project/depot/depot-zenodo-v0221/"
        "TRIADE_complet_v0.22.1.zip",
    "TRIADE_presentation_v0.22.0.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.22.0.zip",
}

DESCRIPTION = (
    "<p>The correction release v0.22.1 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This release succeeds the edition "
    "v0.22.0 under the same concept DOI and carries the twelfth "
    "instruction wave: the edition itself remains immutable (manuscript, "
    "evidence tables and presentation unchanged, the five pack "
    "fingerprints recopied byte for byte); the corrections live in the "
    "rebuilt source chains, the six new workshops and the consigned "
    "errata. (1) Ratio recomposability audited: sixteen published ratios "
    "recomputed from their printed values, three divergences named and "
    "their unrounded canons re-read or re-measured — the round-trip cache "
    "285.725 ms to 0.418 ms (the 683.6x gain re-composed from the printed "
    "canons), the addition medians 3073.5 to 2199.5 tokens (the -28.4 "
    "percent ratio recomposes exactly), the verification-regime canon at "
    "three decimals (2.163 s); the 559-vector census re-summed by code "
    "from the generator itself (16+3+4+13+3+8+512 = 559, the published "
    "formula's erratum named); the inter-piece linter extended to the "
    "ratio and status-label classes with two planted negative controls, "
    "both refused on first name. (2) The D81 purge completed at the "
    "semantic perimeter: seven prescriptive residues in the Book v1.6 and "
    "the specification v0.15.7 replaced by the active sequestered 5-of-3 "
    "guard at thirteen anchored replacements, four historical contexts "
    "annotated, both PDFs rebuilt (the runbook simulation replayed at "
    "eight steps without a single write, zero blobs carrying the marker "
    "over 528 commits). (3) Generative conformity machinery: 30 000 "
    "traces at three seeds over the hardened sentinel, zero divergence "
    "across the eight failure paths, bit-identical replay twice, the z3 "
    "model extended to six proven invariants, and a fail-closed reception "
    "grid for the signed field witnesses — no result produced without "
    "the developer's gesture. (4) The dual engine generalised to the "
    "three oracle posts: Unicorn 13.43 s, QEMU-user 1.10 s, native 0.04 s "
    "at zero divergence over the 2 041-operation sample (the mutated shim "
    "caught on the first line, the 357x gain at n=5), a weighted "
    "crystallisation-risk budget closing the eleventh wave's escape at "
    "equal budget, and the signed, epoch-bound cache store with its two "
    "negative controls refused on first name. (5) TPL-ADD-v2: the "
    "versioned domain dictionary (admissible labels and constants, the "
    "sha256 engraved in the material and cross-checked against the "
    "canonical), the client expanding agent-emitted IDs — four refusals "
    "lived, no control removed; the pre-registered target (15/18 and "
    "1500 tokens) missed at both faces, the gap named by class, never "
    "re-drawn. (6) The two variants at the virgin margin: the v5 "
    "interleaved AES-NI carrier at k in {4, 8} independent key-schedule "
    "addresses (6.453/5.313 and 5.953/4.844 cycles per block envelope "
    "at 64/256 blocks) — the pre-registered 3-cycle target missed and "
    "the gap named by measurement: the pure-throughput probe over eight "
    "independent register chains yields 0.459 cycles per aesenc, an "
    "arithmetic floor of 4.59 cycles per block envelope-free, the k=8 "
    "variant saturating the AES unit at 1.055x the floor; and the AVX2 "
    "search corridor after hoisting — the cpuid probe hoisted once per "
    "session, the dispatch resolved at load under R10, the SSE2 fallback "
    "never a dead path: 470 cycles [IQR 26] against 5840 [148] at "
    "per-call dispatch (a 12.4x gain), the 559-vector battery re-rolled "
    "at zero divergence on both paths, the FIPS 197 key schedule, the "
    "C.1 vector, the 64/64 and 256/256 byte-for-byte differentials, the "
    "eight-key schedule mapping and the mutated-byte negative control "
    "caught on the first vector. All pre-registered plans hashed before "
    "any measurement; the two missed targets recorded as measured, "
    "never adjusted; the sealed pieces intact throughout (the 14-tree "
    "intent guard green before and after every workshop).</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.22.0, "
             "Correction Release v0.22.1) — manuscript, data tables, "
             "complete sources and verification evidence",
    "publication_date": "2026-11-21",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.22.1",
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
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def md5_de(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.22.0 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.22.0", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24407701 : état {d.get('state')}, version "
      f"{d.get('metadata', {}).get('version')}, concept {CONCEPT}")

# (2) LE BROUILLON DE NOUVELLE VERSION
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

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS DE LA RELEASE POSÉS
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

# (4) LES MÉTADONNÉES v0.22.1
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.22.1 posées : HTTP {st} ; fichiers : "
      f"{len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.22.1"
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
