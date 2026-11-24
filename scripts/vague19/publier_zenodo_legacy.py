#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUBLICATION ZENODO (API legacy deposit/depositions) — vague 19.
Jeton : ZENODO_TOKEN (environnement). Aucune valeur affichée."""
import hashlib, json, os, pathlib, sys, time, urllib.error, urllib.request

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / "depot-zenodo-v0260"
API = "https://zenodo.org/api"
TOK = os.environ.get("ZENODO_TOKEN", "").strip()


def appel(m, url, corps=None, brut=None, essais=6, ctype=None):
    h = {"Authorization": f"Bearer {TOK}"}
    data = None
    if corps is not None:
        data = json.dumps(corps).encode(); h["Content-Type"] = "application/json"
    elif brut is not None:
        data = brut; h["Content-Type"] = ctype or "application/octet-stream"
    for i in range(essais):
        try:
            req = urllib.request.Request(url, data=data, method=m, headers=h)
            with urllib.request.urlopen(req, timeout=600) as r:
                t = r.read().decode() or "{}"
                try: return r.status, json.loads(t)
                except json.JSONDecodeError: return r.status, {"raw": t[:200]}
        except urllib.error.HTTPError as e:
            t = e.read().decode()
            if e.code in (500, 502, 503, 504) and i < essais - 1:
                time.sleep(3 * (i + 1)); continue
            return e.code, {"erreur": t[:500]}
        except Exception as e:
            if i < essais - 1: time.sleep(3 * (i + 1)); continue
            return 0, {"erreur": str(e)[:200]}
    return 0, {}


def md5(p): return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def depose(dep, fichiers):
    st, d = appel("GET", f"{API}/deposit/depositions/{dep}")
    if st != 200: raise SystemExit(f"depot {dep} : {st} {d}")
    bucket = d["links"]["bucket"]
    for f in fichiers:
        f = pathlib.Path(f)
        st, r = appel("PUT", f"{bucket}/{f.name}", brut=f.read_bytes())
        if st not in (200, 201): raise SystemExit(f"bucket {f.name} : {st} {r}")
        print(f"  [fichier] {f.name} ({f.stat().st_size} o) déposé")
    st, d = appel("GET", f"{API}/deposit/depositions/{dep}")
    got = {x["filename"]: x["checksum"] for x in d.get("files", [])}
    ok = all(got.get(pathlib.Path(f).name) == f"md5:{md5(f)}" for f in fichiers)
    print(f"  [recoupement] {'VERT' if ok else 'ROUGE'} — {got}")
    return ok


def metadonnees(dep, meta):
    st, d = appel("PUT", f"{API}/deposit/depositions/{dep}", {"metadata": meta})
    if st not in (200, 201): raise SystemExit(f"metadata : {st} {d}")
    print("  [metadata] posées")


def publie(dep):
    st, d = appel("POST", f"{API}/deposit/depositions/{dep}/actions/publish")
    if st not in (200, 201, 202): raise SystemExit(f"PUBLISH : {st} {d}")
    print(f"  [PUBLISH] DOI {d.get('doi')} record {d.get('id') or d.get('record_id')}")
    return d


def nouvelle_version(record):
    st, d = appel("POST", f"{API}/deposit/depositions/{record}/actions/newversion")
    if st not in (200, 201):
        raise SystemExit(f"newversion : {st} {d}")
    lien = d["links"]["latest_draft"]
    dep = int(lien.rstrip("/").split("/")[-1])
    print(f"  [newversion] brouillon {dep}")
    return dep


def verifie(recid, fichiers, doi_attendu=None):
    st, d = appel("GET", f"{API}/deposit/depositions/{recid}")
    if st != 200:
        st, d = appel("GET", f"{API}/records/{recid}")
    ok = st == 200
    noms = [pathlib.Path(f).name for f in fichiers]
    contenu = json.dumps(d)
    presents = all(n in contenu for n in noms)
    doi = d.get("doi")
    print(f"  [vérification] HTTP {st} · fichiers {'tous présents' if presents else 'MANQUANTS'} · DOI {doi}")
    return ok and presents, doi


DESC_PROTO = """<p><strong>Academic edition v0.26.0 (the nineteenth wave, 24 November 2026) of TRIADE.</strong>
No measured value changed. The pack generation gate now runs the ported edition linter and six
fail-closed classes: the presentation's version table is confronted with the pack manifest,
every cited decision identifier must fall inside the table's range (D1–D268), the frozen
changelog must be in strict chronological order, one single reference convention is enforced,
every announced bench count is recomposed from the kit's own cases, and every refusal row of
the threat model names its adversary class and model edge. The six residues named by the
review are closed at the source. The decision chain D261–D267 enters the journal and the
specification: closed prescriptive whitelist (D262), monotone NV counter as the per-profile
freshness floor (D263, simulator 12/12, hardware AWAITING), structured expansion with a
three-turn repair loop (D264, campaign AWAITING), transparency anchoring of epoch witnesses
at its applied status with the threat-model delta at both edges (D267, adopted, tooled, not
deployed), and the eleven-class gate (D268). The switch bench is recomposed from the kit:
7 transaction cases + 1 nominal rendezvous + 5 D261 hazards + 3 invariants = 16/16. The five
pieces are regenerated (manuscript v0.26.0, specification v0.15.11, Book v1.10, proofs and
presentation v0.26.0); the v0.25.0 PDFs remain byte for byte. The oracle engine is extended
to the 52 sealed blocks (50/52 byte-identical, content-addressed memo, 1-in-10 chained audit,
twin consoles 128/128 line-identical); the add frontier moves to a pointer-only schema with
a deterministic client-side expander (18/18, four named refusals). Named limits: bare metal,
hardware NV counter, served structured campaign and the transparency anchoring deployment
remain AWAITING; the 1,991 tokens of the former extraction are not replayed.</p>"""


def meta_proto():
    return {
        "title": "TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent "
                 "Governance (Academic Edition v0.26.0) — manuscript, data tables, complete "
                 "sources and verification evidence",
        "upload_type": "publication",
        "publication_type": "article",
        "publication_date": "2026-11-24",
        "version": "v0.26.0",
        "access_right": "open",
        "license": "busl-1.1",
        "creators": [{"name": "Lopez, Alexis", "affiliation": "Independent researcher"}],
        "description": DESC_PROTO,
    }


def main():
    if not TOK:
        raise SystemExit("ZENODO_TOKEN absent")
    args = sys.argv[1:]
    quoi = args[0] if args else "protocole"
    draft = None
    if "--draft" in args:
        draft = int(args[args.index("--draft") + 1])
    if quoi == "protocole":
        fichiers = [OUT / "TRIADE_soumission_v0.26.0.zip", OUT / "TRIADE_presentation_v0.26.0.zip",
                    OUT / "TRIADE_complet_v0.26.0.zip"]
        dep = draft or nouvelle_version(24497211)
        if depose(dep, fichiers):
            metadonnees(dep, meta_proto())
            publie(dep)
            verifie(dep, fichiers)
        else:
            raise SystemExit("recoupement des empreintes ÉCHOUÉ — pas de PUBLISH")
    return 0


if __name__ == "__main__":
    sys.exit(main())
