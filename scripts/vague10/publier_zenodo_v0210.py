#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""publier_zenodo_v0210.py — LA COMMANDE DU MAÎTRE : la publication de la
v0.21.0 au concept DOI 10.5281/zenodo.24367343 — à la commande explicite
« il faudra ensuite mettre à jour les miroirs et zenodo » (l'Entrée 379 a
consigné l'intention, la session morte n'a pas vécu le geste ; la présente
le porte à terme). La voie est vérifiée AVANT le geste (l'état du record
v0.19.5, la création du brouillon de version, les TROIS fichiers posés
recoupés md5 byte-byte aux pièces locales, les métadonnées v0.21.0), le
geste PUIS la vérification fraîche (le DOI de version minté, le concept
DOI résolvant sur la v0.21.0, l'état done, le bord anonyme)."""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/keys/zenodo.txt").read().strip()
RECORD = "https://zenodo.org/api/deposit/depositions/24382460"  # v0.19.5 (done)
CONCEPT = "10.5281/zenodo.24367343"

FICHIERS_LOCAUX = {
    "TRIADE_soumission_v0.21.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0210/"
        "TRIADE_soumission_v0.21.0.zip",
    "TRIADE_complet_v0.21.0.zip":
        "/home/z/my-project/depot/depot-zenodo-v0210/"
        "TRIADE_complet_v0.21.0.zip",
    "TRIADE_presentation_v0.21.0.zip":
        "/home/z/my-project/depot/TRIADE_presentation_v0.21.0.zip",
}

DESCRIPTION = (
    "<p>The academic edition v0.21.0 of the TRIADE single-case study: a "
    "development protocol under which an LLM agent writes native x86-64, "
    "RISC-V and TLS 1.3 code directly as assembly notation, governed by "
    "signed layer-I specifications. This version succeeds v0.19.5 under "
    "the same concept DOI and carries the eighth, ninth and tenth "
    "instruction waves. (1) Wave 8 (v0.19.6): cross-piece coherence with "
    "the display macros regenerated from the living journals (DOI "
    "reconciliation against the concept record, the 1/16 draw verified at "
    "the register), governance carried as lived (the D183 vault-key "
    "sequestration ceremony lived end-to-end, the committed control "
    "phrase rotated and the old one refused), pre-registered integrity "
    "reported in two distinct verdicts, and independence by tooled "
    "derivation: a local open-weights second family (Qwen2.5-Coder-1.5B) "
    "writes the code that derives the 128 tables from the definitions "
    "alone, zero divergence; the OPT-05 hunk-editing reform (minus 34.3 "
    "percent material, minus 97.7 percent response). (2) Wave 9 "
    "(v0.20.0): the lexicographic objective function carried to a "
    "four-axis dashboard generated from the raw evidence (security above "
    "performance above optimization above token cost, no compensation "
    "between ranks); memory safety at the floor (2006 of 2098 accesses "
    "discharged by proof, 92 named with cause and SAT certificate, the "
    "three remaining 'killables' reclassified equivalent-by-sweep over "
    "thirty scenarios, adjusted score 811/817 = 99.3 percent); the "
    "crystallization certificate (three falsifications refused by name), "
    "the double-engine divergence check under real QEMU-user, CF3 "
    "mechanised in z3 (14/14 obligations with replayable SMT2 "
    "certificates), the two performance corridors (SSE2 baseline parity "
    "at instruction count, 0.03x gcc-O2 with 31.2x headroom, zero "
    "divergence at the vectors) and the token budget campaign. (3) Wave "
    "10 (v0.21.0): the SSE2 variant fault named and corrected (406 of "
    "564 planted occurrences missed by the wave-9 differential; the "
    "corrected chain at zero divergence over 88 vectors) with the "
    "real-time RDTSCP re-measurement placing the handwritten SSE2 "
    "variant in the class of the libc SIMD primitives (833 cycles per "
    "operation against 16040 for gcc-O2 at the same source, the "
    "instruction-count story relativized); the re-reading window (OPT-10: "
    "edit re-read reduced to the hunk, median 2452 to 1146 native "
    "tokens, minus 53.3 percent, prose now the dominant floor); the "
    "guards carried to 100 percent discharged-or-guarded (58 runtime "
    "guards, 58/58 UNSAT certificates, 58/58 falsifications caught); "
    "non-interference extended to x25519 and md5 (13 blocks, seven "
    "families, under the lifter-soundness hypothesis verified by "
    "round-trip, the alternate-encoding mutation caught); the third arm "
    "C+G isolating the notation effect (37.07 s per session, 18.1x) from "
    "governance alone (215 ms, 1.11x) on the same machine at the fixed "
    "list; the abstract-body-tables reconciliation (811/817 at the "
    "abstract, the raw 811/832 alongside, never merged) and the neutral "
    "register (ritualist lexicon replaced, emphasis caps removed from "
    "prose, verbatim pieces intact, transparency unchanged: no measured "
    "value modified outside the documented reconciliation). The "
    "specification v0.15.6 and the Book of the Vault v1.5 remain "
    "unchanged (no rule, no ceremony modified). This deposit contains "
    "the manuscript v0.21.0, the proofs and calculations v0.21.0 (the "
    "eight workshop pieces verbatim plus the fingerprints table), the "
    "20 November presentation at the exact status, the consolidated "
    "data tables, the complete edition sources, and the ten-point "
    "verification report. License: Business Source License 1.1 with an "
    "academic Additional Use Grant (peer review, artifact evaluation, "
    "scientific replication, non-commercial research; effective "
    "2026-11-17, decision D209; Change Date 2030-10-28 converting to "
    "GPLv3+).</p>"
)

METADATA = {
    "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand "
             "Under Signed-Intent Governance (Academic Edition v0.21.0) — "
             "manuscript, data tables, complete sources and verification "
             "evidence",
    "publication_date": "2026-11-20",
    "description": DESCRIPTION,
    "access_right": "open",
    "creators": [{"name": "Lopez, Alexis",
                  "affiliation": "Independent researcher"}],
    "license": "busl-1.1",
    "imprint_publisher": "Zenodo",
    "upload_type": "publication",
    "publication_type": "article",
    "version": "v0.21.0",
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
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def md5_de(chemin):
    return hashlib.md5(open(chemin, "rb").read()).hexdigest()


# (1) LA VOIE VÉRIFIÉE AVANT LE GESTE — le record v0.19.5 vivant
st, body = api("GET", RECORD)
assert st == 200, f"record illisible : HTTP {st}"
d = json.loads(body)
assert d.get("state") == "done", f"état inattendu : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.19.5", \
    f"version inattendue : {d.get('metadata', {}).get('version')}"
assert d.get("conceptdoi") == CONCEPT, \
    f"concept inattendu : {d.get('conceptdoi')}"
print(f"[1] le record 24382460 : état {d.get('state')}, version "
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

# (3) LES ANCIENS FICHIERS RETIRÉS, LES TROIS v0.21.0 POSÉS
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

# (4) LES MÉTADONNÉES v0.21.0
st, body = api("PUT", draft_url, {"metadata": METADATA})
if st >= 400:
    print(f"[4] métadonnées : HTTP {st}")
    print(body.decode(errors="replace")[:400])
    sys.exit(1)
d = json.loads(body)
print(f"[4] métadonnées v0.21.0 posées : HTTP {st}")
print(f"    titre : {d['metadata']['title'][:70]}…")
print(f"    version : {d['metadata'].get('version')} | "
      f"fichiers : {len(d.get('files', []))}")

# (5) LA VOIE RE-VÉRIFIÉE AVANT LE GESTE — le brouillon complet
st, body = api("GET", draft_url)
d = json.loads(body)
assert d.get("state") in ("unsubmitted", "draft"), \
    f"état du brouillon : {d.get('state')}"
assert d.get("metadata", {}).get("version") == "v0.21.0", \
    f"version du brouillon : {d.get('metadata', {}).get('version')}"
fichiers = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
assert len(fichiers) == 3, f"fichiers inattendus : {list(fichiers)}"
for nom, chemin in FICHIERS_LOCAUX.items():
    assert nom in fichiers, f"absent du brouillon : {nom}"
    assert fichiers[nom] == md5_de(chemin), f"md5 divergent : {nom}"
    print(f"    recoupé md5 byte-byte : {nom}")
print(f"[5] la voie est VÉRIFIÉE — les trois fichiers, la version, l'état")

# (6) LE GESTE — la publication à la commande du maître
st, body = api("POST", f"{draft_url}/actions/publish")
if st >= 400:
    print(f"[6] PUBLICATION : HTTP {st}")
    print(body.decode(errors="replace")[:500])
    sys.exit(1)
d = json.loads(body)
doi, concept, etat = d.get("doi"), d.get("conceptdoi"), d.get("state")
print(f"[6] PUBLICATION : HTTP {st}")
print(f"    DOI de version : {doi}")
print(f"    concept DOI    : {concept}")
print(f"    état           : {etat}")
assert etat == "done", f"état inattendu après publication : {etat}"
assert concept == CONCEPT, f"concept inattendu : {concept}"
assert doi and doi.startswith("10.5281/zenodo."), f"DOI anormal : {doi}"

# (7) LA VÉRIFICATION FRAÎCHE — le bord public anonyme
time.sleep(4)
rid = doi.split("zenodo.")[-1]
st, body = api("GET", f"https://zenodo.org/api/records/{rid}",
               avec_jeton=False)
assert st == 200, f"la page publique du record : HTTP {st}"
r = json.loads(body)
assert r.get("doi") == doi and r.get("conceptdoi") == CONCEPT, \
    "DOI divergents"
assert r["metadata"].get("version") == "v0.21.0", "version divergente"
files_pub = {f["key"]: f["checksum"].split("md5:")[-1]
             for f in r.get("files", [])}
assert files_pub == fichiers, "fichiers divergents au bord public"
print(f"[7] le bord public anonyme : HTTP 200, la v0.21.0 vivante")
for nom, md5 in sorted(files_pub.items()):
    print(f"    - {nom} (md5 {md5[:8]}… recoupé égal)")
# le concept résout sur la v0.21.0 (la redirection du bord anonyme)
st, body = api("GET",
               f"https://zenodo.org/api/records/{CONCEPT.split('zenodo.')[-1]}",
               avec_jeton=False)
assert st == 200, f"le concept : HTTP {st}"
rc = json.loads(body)
assert rc.get("doi", "").endswith(rid) or rc.get("id") == int(rid), \
    f"le concept résout sur {rc.get('doi')}"
print(f"[7] le concept {CONCEPT} résout sur la v0.21.0 "
      f"(record {rid}, version {rc['metadata'].get('version')})")
print("\nLE GESTE EST VÉCU — la v0.21.0 publiée, le concept à jour, "
      "les bords verts.")
