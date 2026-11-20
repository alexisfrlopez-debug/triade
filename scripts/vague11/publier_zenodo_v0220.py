#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0220.py — LA PUBLICATION DE LA v0.22.0 AU CONCEPT (la
vague 11, la commande du maître « il faudra ensuite mettre a jour les
miroirs et zenodo » — le précédent v0.21.0 l'établit). LA VOIE VÉRIFIÉE
du modèle v0.21.0 : newversion → le bucket → les métadonnées → PUBLISH."""
import hashlib
import json
import sys
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/acces_miroirs/zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24397623"  # v0.21.0
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.22.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0220/"
        "TRIADE_soumission_v0.22.0.zip",
    "TRIADE_complet_v0.22.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0220/"
        "TRIADE_complet_v0.22.0.zip",
    "TRIADE_presentation_v0.22.0.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.22.0.zip",
}

DESCRIPTION = (
    "<p>The academic edition v0.22.0 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version succeeds v0.21.0 under "
    "the same concept DOI and carries the eleventh instruction wave. "
    "(1) The SIMD corridors: the memchr+memcmp hybrid search at 704 "
    "cycles per absent 4096/16 (25.9x over the sealed GPR path, inside "
    "the class of the library SIMD primitives), the SHA-NI compression "
    "corps at 128.5 cycles per block (6.5x), runtime dispatch with "
    "baseline fallback and per-session hoisting, on a 559-vector "
    "hardened differential (buffer-tail, overlapping, lengths 1-33, page "
    "crossing, multi-occurrence, 512 property-based draws) at zero "
    "divergence. (2) The AES-NI carrier loop restructured to 7.09 "
    "cycles per block envelope (the 12-cycle target met, 7.1x over the "
    "v2 carrier), a round-trip cache keyed by notation+engine+profile "
    "(680x at opening, fail-closed), incremental crystallisation over "
    "the dependency graph (-54 percent at a real diff, the 1/10 audit "
    "maintained as a named probabilistic net), and the 37-second "
    "governed session decomposed by control (oracles 81 percent). "
    "(3) The fourth arm C+G+ (gcc-O2 with governance and the full "
    "verification regime at equal oracle volumes): T 39.39 s, C+G+ "
    "18.68 s, C+G 2.18 s, C 1.97 s — the proper notation effect "
    "confirmed at 20.72 s (55.7 percent), the verification-regime "
    "effect at 16.50 s (44.3 percent), governance at 0.213 s. "
    "(4) Lifter soundness validated against observed Unicorn accesses "
    "per instruction (942 distinct encodings at zero divergence, the "
    "155 mutant divergences all outside the validated vocabulary — "
    "fail-closed domain guard), GHASH H covered as a secret (no tainted "
    "branch or address), non-interference re-discharged on 16 blocks "
    "across seven families with named holes. (5) The template-versioned "
    "edit operation (1106 to 674 native tokens, the natural-language "
    "prose down 57 percent), hierarchical localisation (1053 to 627), "
    "skeleton-based addition (3074 to 2200, 3/18 feasible — the gap "
    "named, never re-drawn). (6) The vault hardened on laboratory "
    "copies: ciphertext-fingerprint verification before AEAD (corruption "
    "refused without destruction, falsification at valid naive "
    "fingerprint destroyed with PV), epoch-bound trap-value derivation, "
    "the Argon2 re-parameterisation ceremony with a 60-bit passphrase "
    "entropy floor, phrase change under sequestration, the RAM-guard "
    "block specification, epoch-witness anchoring, the FIDO2 hmac-secret "
    "prototype — with a z3 state-machine model proving four invariants. "
    "(7) The six pre-registered kits for the awaiting lines (fence.i on "
    "RV64 silicon, the third machine, dudect on two machines with a "
    "pre-registered peak investigation, the stratified H7 campaign at 14 "
    "strates, the second annotator with a self-tested kappa calculator, "
    "the CF3 Tamarin model) — hashed before any measurement, no result "
    "produced without the developer's gesture. (8) The D81 delivery "
    "instruction purged from the operational pieces (the sequestered "
    "5-of-3 guard active, the deposit public): the Book v1.6 and the "
    "specification v0.15.7, with the runbook simulation proving no path "
    "commits a phrase. The inter-piece linter is extended to every "
    "numeric token of the prose (5,026 tokens, four coverage classes, "
    "fail-closed, a lived double negative control).</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.22.0) — "
             "manuscript, data tables, complete sources and verification "
             "evidence",
    "publication_date": "2026-11-21",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.22.0",
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


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.21.0 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.21.0", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT
print(f"[1] le record 24397623 : état {d.get('state')}, version "
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

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS v0.22.0 POSÉS
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

# (4) LES MÉTADONNÉES v0.22.0
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.22.0 posées : HTTP {st} ; fichiers : "
      f"{len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.22.0"
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
import time
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
