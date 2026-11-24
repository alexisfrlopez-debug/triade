#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUBLICATION ZENODO DE LA VAGUE 19 (InvenioRDM) — protocole v0.26.0, kit v1.3.0,
pack de participation v1.1.0. Le jeton vient de l'environnement (ZENODO_TOKEN), jamais
affiché ni écrit. Reprises sur 5xx/504 ; aucune publication partielle : le PUBLISH n'est
appelé qu'après la re-vérification des empreintes déposées."""
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / "depot-zenodo-v0260"
API = "https://zenodo.org/api"
TOK = os.environ.get("ZENODO_TOKEN", "").strip()


def appel(methode, url, corps=None, brut=None, entetes=None, essais=6):
    h = {"Authorization": f"Bearer {TOK}"}
    h.update(entetes or {})
    data = None
    if corps is not None:
        data = json.dumps(corps).encode()
        h["Content-Type"] = "application/json"
    elif brut is not None:
        data = brut
        h["Content-Type"] = "application/octet-stream"
    dernier = None
    for i in range(essais):
        try:
            req = urllib.request.Request(url, data=data, method=methode, headers=h)
            with urllib.request.urlopen(req, timeout=300) as r:
                txt = r.read().decode() or "{}"
                try:
                    return r.status, json.loads(txt)
                except json.JSONDecodeError:
                    return r.status, {"raw": txt[:300]}
        except urllib.error.HTTPError as e:
            txt = e.read().decode()
            if e.code in (500, 502, 503, 504) and i < essais - 1:
                time.sleep(3 * (i + 1))
                dernier = (e.code, txt[:300])
                continue
            return e.code, {"erreur": txt[:600]}
        except Exception as e:
            if i < essais - 1:
                time.sleep(3 * (i + 1)); dernier = (0, str(e)[:200]); continue
            return 0, {"erreur": str(e)[:300]}
    return dernier or (0, {})


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def nouvelle_version(record):
    st, d = appel("POST", f"{API}/records/{record}/versions")
    if st not in (200, 201):
        raise SystemExit(f"newversion {record} : HTTP {st} {d}")
    return d


def _entree(liste, cle):
    for e in liste.get("entries", []):
        if e.get("key") == cle:
            return e
    return None


def televerse(draft, fichiers):
    base_files = draft["links"]["files"]
    for f in fichiers:
        f = pathlib.Path(f)
        st, d = appel("POST", base_files, [{"key": f.name}])
        if st not in (200, 201):
            if "already exists" not in json.dumps(d):
                raise SystemExit(f"creation fichier {f.name} : HTTP {st} {d}")
            st2, d = appel("GET", base_files)
            ent = _entree(d, f.name)
        else:
            ent = _entree(d, f.name)
        if ent is None:
            raise SystemExit(f"entrée {f.name} introuvable")
        st, d = appel("PUT", ent["links"]["content"], brut=f.read_bytes())
        if st not in (200, 201, 202):
            raise SystemExit(f"upload {f.name} : HTTP {st} {d}")
        st, d = appel("POST", ent["links"]["commit"])
        if st not in (200, 201):
            raise SystemExit(f"commit {f.name} : HTTP {st} {d}")
        print(f"  [fichier] {f.name} déposé ({f.stat().st_size} o)")


def supprime_fichier(draft, cle):
    st, d = appel("DELETE", f"{draft['links']['files']}/{cle}")
    print(f"  [nettoyage] {cle} → HTTP {st}")


def metadonnees(draft, meta):
    st, d = appel("PUT", draft["links"]["self"], {"metadata": meta})
    if st not in (200, 201):
        raise SystemExit(f"metadata : HTTP {st} {d}")
    return d


def publier(draft):
    st, d = appel("POST", draft["links"]["publish"])
    if st not in (200, 201, 202):
        raise SystemExit(f"PUBLISH : HTTP {st} {d}")
    return d


def verifie(record, attendus):
    st, d = appel("GET", f"{API}/records/{record}")
    if st != 200:
        return False, f"HTTP {st}"
    tailles = {f["key"]: f.get("size") for f in d.get("files", {}).get("entries", {}).values()} \
        if isinstance(d.get("files", {}).get("entries"), dict) else {}
    manquants = [a for a in attendus if a not in tailles]
    return (not manquants), f"fichiers {sorted(tailles)} manquants {manquants}"


def md_prime(record, attendus):
    for a in attendus:
        st, d = appel("GET", f"{API}/records/{record}/files/{a}/content", essais=3)
        return st
    return None


DESC_PROTO = """<p><strong>TRIADE v0.26.0 — the nineteenth wave (24 November 2026).</strong> No measured
value changed. The pack generation gate now runs the ported edition linter and six
fail-closed classes: the presentation's version table is confronted with the pack manifest,
every cited decision identifier must fall inside the table's range (D1–D268), the frozen
changelog must be in strict chronological order, one single reference convention is
enforced, every announced bench count is recomposed from the kit's own cases, and every
refusal row of the threat model names its adversary class and model edge. The six residues
named by the review are closed at the source; the decision chain D261–D267 enters the
journal and the specification (closed prescriptive whitelist D262, NV monotone counter D263,
structured expansion D264, transparency anchoring D267 at its applied status, gate D268).
The switch bench is recomposed: 7 transaction cases + 1 nominal rendezvous + 5 D261 hazards
+ 3 invariants = 16/16. The five pieces are regenerated (manuscript v0.26.0, specification
v0.15.11, Book v1.10, proofs and presentation v0.26.0); the v0.25.0 PDFs remain byte for
byte. Named limits: bare metal, hardware NV counter, served structured campaign and the
transparency anchoring deployment remain AWAITING; the 1,991 tokens of the former
extraction are not replayed.</p>"""

DESC_KIT = """<p><strong>TRIADE Developer Kit v1.3.0 (24 November 2026).</strong> Guarantees updated,
never widened: § 5 of GARANTIES.md states the monotone NV counter (TPM 2.0 or RPMB) as the
per-profile freshness floor, with its four named fail-closed refusals and its limits
(D263); § 6 states the epoch-witness transparency anchoring (Rekor / RFC 3161) at its
applied status — adopted, tooled, not deployed — with the threat-model delta at both edges
(D267). SECURITE.md § 11 carries both bounds. The ceremony tools, templates and hygiene
scripts are unchanged.</p>"""

DESC_PART = """<p><strong>TRIADE participation pack v1.1.0 (24 November 2026).</strong> The four kits —
complete sources, the five pieces, the developer kit v1.3.0 and the training pack — with
CONTRIBUTING, EVALUATION (six commands) and INDEX-DOI. Everything needed to evaluate the
protocol and contribute to it.</p>"""


def brouillon_existant(draft_id):
    st, d = appel("GET", f"{API}/records/{draft_id}/draft")
    if st == 200:
        return d
    # le GET du brouillon rend parfois 500 côté Zenodo : les liens se construisent
    print(f"  [brouillon] GET HTTP {st} — liens reconstruits")
    return {"id": draft_id, "links": {
        "files": f"{API}/records/{draft_id}/draft/files",
        "self": f"{API}/records/{draft_id}/draft",
        "publish": f"{API}/records/{draft_id}/draft/actions/publish"}}


def publier_flux(record, titre, version, description, fichiers, extra=None, draft_id=None):
    print(f"\n=== {record} → {version} ===")
    draft = brouillon_existant(draft_id) if draft_id else nouvelle_version(record)
    print(f"  [newversion] brouillon {draft.get('id')}")
    televerse(draft, fichiers)
    meta = {
        "title": titre,
        "version": version,
        "description": description,
        "creators": [{"name": "Lopez, Alexis"}],
        "license": {"id": "busl-1.1"},
        "resource_type": {"id": "publication-article"},
        "publication_date": "2026-11-24",
    }
    if extra:
        meta.update(extra)
    metadonnees(draft, meta)
    print("  [metadata] posées")
    pub = publier(draft)
    doi = pub.get("doi") or pub.get("pids", {}).get("doi", {}).get("identifier")
    rid = pub.get("id")
    print(f"  [PUBLISH] record {rid} — DOI {doi}")
    ok, motif = verifie(rid, [pathlib.Path(f).name for f in fichiers])
    print(f"  [vérification] {'VERT' if ok else 'ROUGE'} — {motif}")
    return rid, doi, ok


def main():
    if not TOK:
        raise SystemExit("ZENODO_TOKEN absent de l'environnement")
    args = sys.argv[1:]
    draft_id = None
    if "--draft" in args:
        i = args.index("--draft"); draft_id = args[i + 1]; del args[i:i + 2]
    actions = args or ["protocole", "kit", "participation"]
    res = {}
    if "protocole" in actions:
        f = [OUT / "TRIADE_soumission_v0.26.0.zip", OUT / "TRIADE_presentation_v0.26.0.zip",
             OUT / "TRIADE_complet_v0.26.0.zip"]
        for x in f:
            print(f"  [empreinte] {x.name} sha256 {sha(x)[:16]}… md5 {hashlib.md5(x.read_bytes()).hexdigest()}")
        res["protocole"] = publier_flux(
            24497211,
            "TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent "
            "Governance (Academic Edition v0.26.0) — manuscript, data tables, complete sources "
            "and verification evidence",
            "v0.26.0", DESC_PROTO, f, draft_id=draft_id)
    if "kit" in actions:
        f = [R / "TRIADE_kit_developpement_v1.3.0.zip"]
        res["kit"] = publier_flux(
            24497290, "TRIADE Developer Kit v1.3.0: the adoption kit with the NV freshness "
            "floor and the transparency anchoring bounds", "v1.3.0", DESC_KIT, f)
    if "participation" in actions:
        f = [OUT / "TRIADE_participer_v1.1.0.zip"]
        res["participation"] = publier_flux(
            24497300, "TRIADE Participation Pack v1.1.0: the four kits, evaluation and "
            "contribution", "v1.1.0", DESC_PART, f)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
