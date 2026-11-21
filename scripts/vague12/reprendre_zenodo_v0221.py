#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reprendre_zenodo_v0221.py — LA REPRISE DU BROUILLON 24420007 (Zenodo
surchargé au premier geste : le 500 vécu au complet, la reprise idempotente
et AUTONOME — l'état du brouillon relu, les TRIADE_* retirés, les trois
fichiers posés avec reprises, les métadonnées reposées, la publication AU
GESTE une fois la voie vérifiée)."""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request

TOK = open("/home/z/my-project/work/acces_miroirs/zenodo.txt").read().strip()
DRAFT = "https://zenodo.org/api/deposit/depositions/24420007"
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


def tentative(fonction, *args, essais=6, attente=15, nom="", **kwargs):
    for i in range(essais):
        st, body = fonction(*args, **kwargs)
        if st < 400:
            return st, body
        print(f"    [{nom}] HTTP {st} (essai {i + 1}/{essais}) — "
              f"attente {attente}s")
        time.sleep(attente)
    return st, body


def main() -> int:
    # (1) l'état du brouillon
    st, body = tentative(api, "GET", DRAFT, nom="état")
    assert st == 200, f"brouillon illisible : HTTP {st}"
    d = json.loads(body)
    assert d.get("state") in ("unsubmitted", "draft"), \
        f"état inattendu : {d.get('state')}"
    assert d.get("conceptdoi") == CONCEPT
    bucket = d["links"]["bucket"]
    fichiers = {f["filename"]: f for f in d.get("files", [])}
    print(f"[1] le brouillon 24420007 : état {d.get('state')}, "
          f"{len(fichiers)} fichier(s) : {sorted(fichiers)}")

    # (2) les TRIADE_* du brouillon retirés (idempotent — les absents sautés)
    for nom in list(fichiers):
        if nom.startswith("TRIADE_"):
            st, _ = tentative(api, "DELETE",
                              f"{d['links']['files'].split('?')[0]}/"
                              f"{fichiers[nom]['id']}",
                              nom=f"retrait {nom}")
            print(f"    retiré : {nom} (HTTP {st})")

    # (3) LES TROIS POSÉS (avec reprises)
    for nom, chemin in FICHIERS_LOCAUX.items():
        st, body = tentative(api, "PUT", f"{bucket}/{nom}",
                             fichier=chemin, nom=f"pose {nom}", essais=8)
        if st >= 400:
            print(f"    ÉCHEC {nom} : HTTP {st} "
                  f"{body.decode(errors='replace')[:200]}")
            return 2
        print(f"    posé : {nom} (HTTP {st})")

    # (4) les métadonnées
    st, body = tentative(api, "PUT", DRAFT, {"metadata": METADATA},
                         nom="métadonnées")
    if st >= 400:
        print(f"[4] métadonnées : HTTP {st} "
              f"{body.decode(errors='replace')[:300]}")
        return 2
    print(f"[4] métadonnées v0.22.1 posées : HTTP {st}")

    # (5) LA VOIE RE-VÉRIFIÉE
    st, body = tentative(api, "GET", DRAFT, nom="relecture")
    d = json.loads(body)
    assert d.get("metadata", {}).get("version") == "v0.22.1"
    fich = {f["filename"]: f.get("checksum", "md5:").split("md5:")[-1]
            for f in d.get("files", [])}
    assert len(fich) == 3, f"fichiers inattendus : {list(fich)}"
    for nom, chemin in FICHIERS_LOCAUX.items():
        assert fich[nom] == md5_de(chemin), f"md5 divergent : {nom}"
        print(f"    recoupé md5 byte-byte : {nom}")
    print("[5] la voie est VÉRIFIÉE — les trois fichiers, la version, "
          "l'état")

    # (6) LE GESTE — la publication à la commande du maître
    st, body = tentative(api, "POST", f"{DRAFT}/actions/publish",
                         nom="publication", essais=3)
    if st >= 400:
        print(f"[6] PUBLICATION : HTTP {st} "
              f"{body.decode(errors='replace')[:300]}")
        return 2
    d = json.loads(body)
    print(f"[6] PUBLIÉ : HTTP {st} — LE DOI DE VERSION {d.get('doi')} "
          f"MINTÉ, le concept {d.get('conceptdoi')} résolvant sur "
          f"{d.get('metadata', {}).get('version')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
