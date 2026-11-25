#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUBLICATION ZENODO DE LA RELEASE v0.31.0 (InvenioRDM) — protocole v0.31.0 et
pack de participation v1.2.0. Le jeton vient de l'environnement (ZENODO_TOKEN),
jamais affiché ni écrit. Reprises sur 5xx/504 ; aucune publication partielle : le
PUBLISH n'est appelé qu'après la re-vérification des empreintes déposées.

LE KIT DÉVELOPPEUR N'EST PAS RE-PUBLIÉ : la source kit-developpement-triade-v1.3.0/
est INCHANGÉE depuis le commit de sa publication (b86e74b, Entrée 403 — diff git
vide) ; le corpus v2.1 (24479882) et TRIADE-TRAIN v1.0.0 (24495492) demeurent aussi
inchangés — aucune mise à jour nécessaire pour eux.

Ancres de newversion (records publiés du concept) :
  protocole      24499428 (v0.26.0, concept 24367343)  → v0.31.0
  participation  24499847 (v1.1.0, concept 24497299)   → v1.2.0

Usage :
  ZENODO_TOKEN=$(cat /home/z/my-project/work/tokens/zenodo.txt) \
      python3 depot/scripts/vague19/publier_zenodo_v0310.py [protocole|participation] [--draft <id>]
"""
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / "depot-zenodo-v0310"
API = "https://zenodo.org/api"
TOK = os.environ.get("ZENODO_TOKEN", "").strip()
DATE_PUB = "2026-11-26"


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


def md5(p):
    return hashlib.md5(pathlib.Path(p).read_bytes()).hexdigest()


def nouvelle_version(record):
    st, d = appel("POST", f"{API}/records/{record}/versions")
    if st in (200, 201):
        return d
    # un brouillon peut déjà vivre sous le concept : le chercher alors
    txt = json.dumps(d, ensure_ascii=False).lower()
    if "draft" in txt or "version" in txt:
        st2, dr = appel("GET", f"{API}/records/{record}/draft")
        if st2 == 200:
            print(f"  [newversion refusé HTTP {st}] — brouillon existant repris")
            return dr
    raise SystemExit(f"newversion {record} : HTTP {st} {d}")


def _entree(liste, cle):
    if isinstance(liste, dict):
        liste = liste.get("entries", [])
    for e in liste or []:
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


def metadonnees(draft, meta):
    st, d = appel("PUT", draft["links"]["self"], {"metadata": meta})
    if st not in (200, 201):
        # le PUT du brouillon peut rendre 500 EN PERSISTANT la valeur (vu vague 19) :
        # relire alors le brouillon pour vérifier que les métadonnées y vivent
        st2, dr = appel("GET", f"{API}/records/{draft.get('id')}/draft")
        if st2 == 200 and dr.get("metadata", {}).get("version") == meta.get("version"):
            print(f"  [metadata] PUT HTTP {st} — REPRIS : la valeur persiste (précédent v19)")
            return dr
        raise SystemExit(f"metadata : HTTP {st} {d}")
    return d


def publier(draft):
    st, d = appel("POST", draft["links"]["publish"])
    if st not in (200, 201, 202):
        raise SystemExit(f"PUBLISH : HTTP {st} {d}")
    return d


def verifie_md5(record, attendus):
    """au bord AUTHENTIFIÉ : chaque fichier du record publié, sa taille et son md5
    (l'API rend checksum 'md5:<hex>') contre les empreintes locales."""
    st, d = appel("GET", f"{API}/records/{record}")
    if st != 200:
        return False, f"HTTP {st}"
    ent = d.get("files", {})
    ent = ent.get("entries", {}) if isinstance(ent, dict) else {}
    if isinstance(ent, list):
        ent = {e.get("key"): e for e in ent}
    manquants = [a for a in attendus if a not in ent]
    if manquants:
        return False, f"fichiers présents {sorted(ent)} — manquants {manquants}"
    ecarts = []
    for a, m in attendus.items():
        api_md5 = (ent[a].get("checksum") or "").replace("md5:", "")
        if api_md5 and api_md5.lower() != m.lower():
            ecarts.append(a)
    return (not ecarts), ("md5 5/5" if not ecarts else f"md5 écarts {ecarts}")


DESC_PROTO = """<p><strong>TRIADE v0.31.0 — the edition waves 20–26 (24 November 2026).</strong> No
measured value changed. The generation gate now reads the prose: the edition linter runs
twenty-five fail-closed classes (C1–C25) over the five pieces — version prose, wave
continuity, abstract length, reader-test counts, DOI registry, English prose, derived
proof statuses, operand order and every target-registry line recomposed from the
published proofs. The target registry CIBLES.md carries eleven targets, one line each,
verdicts carried as published (5/18; 4,604 against 4,500 missed by 104; 3.264 against
3.0; 95/235 at generation; budgets held 674 ≤ 3,000 and 51 ≤ 64), no target re-drawn;
the AES-GCM 1.05× subject is named (the VAES corridor, unwritten). The five pieces are
regenerated (manuscript v0.31.0, specification v0.15.16, Book v1.15, proofs and
presentation v0.31.0); the v0.26.0 PDFs remain byte for byte. Named post-generation lab
results, consigned at the journal, to be carried by the next edition: the per-block
harness P3 was executed at 235/235 vectors (pre-registered target ≥ 200/235 held) and the
witness campaigns ran across field siliciums — an Ivy Bridge laptop, a Blackview phone
(Cortex-A78), a Colab Xeon and the GitHub Actions runners (AMD EPYC 7763 and 9V74, an
ARM64 server, a virtualised Apple M1 — the first Apple measure, FEAT_SHA256 ratio
6.89/8.00) — the sealed four silent on the three server siliciums. Named limits: served
structured output (P4), VAES metal (P5) and Tamarin/ProVerif (P6) remain AWAITING the
real post.</p>"""

DESC_PART = """<p><strong>TRIADE Participation Pack v1.2.0 (26 November 2026).</strong> The five kits —
the complete sources v0.31.0 (1,044 entries), the soumission and presentation packs of
the v0.31.0 edition, the developer kit v1.3.0 (unchanged since record 24499840) and the
training pack v1.0.0 — with CONTRIBUTING, EVALUATION (six commands, each lived at the
lab before assembly) and INDEX-DOI (the corrected concept identifiers; participation
concept 24497299). Everything needed to evaluate the protocol and contribute to it.</p>"""


def brouillon_existant(draft_id):
    st, d = appel("GET", f"{API}/records/{draft_id}/draft")
    if st == 200:
        return d
    print(f"  [brouillon] GET HTTP {st} — liens reconstruits (précédent v19)")
    return {"id": draft_id, "links": {
        "files": f"{API}/records/{draft_id}/draft/files",
        "self": f"{API}/records/{draft_id}/draft",
        "publish": f"{API}/records/{draft_id}/draft/actions/publish"}}


def publier_flux(record, titre, version, description, fichiers, draft_id=None):
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
        "publication_date": DATE_PUB,
        "publisher": "Zenodo",
    }
    metadonnees(draft, meta)
    print("  [metadata] posées")
    pub = publier(draft)
    doi = pub.get("doi") or pub.get("pids", {}).get("doi", {}).get("identifier")
    rid = pub.get("id")
    print(f"  [PUBLISH] record {rid} — DOI {doi}")
    attendus = {pathlib.Path(f).name: md5(f) for f in fichiers}
    ok, motif = verifie_md5(rid, attendus)
    print(f"  [vérification] {'VERT' if ok else 'ROUGE'} — {motif}")
    return rid, doi, ok


def main():
    if not TOK:
        raise SystemExit("ZENODO_TOKEN absent de l'environnement")
    args = sys.argv[1:]
    draft_id = None
    if "--draft" in args:
        i = args.index("--draft"); draft_id = args[i + 1]; del args[i:i + 2]
    actions = args or ["protocole", "participation"]
    res = {}
    if "protocole" in actions:
        f = [OUT / "TRIADE_soumission_v0.31.0.zip", OUT / "TRIADE_presentation_v0.31.0.zip",
             OUT / "TRIADE_complet_v0.31.0.zip"]
        for x in f:
            print(f"  [empreinte] {x.name} sha256 {sha(x)[:16]}… md5 {md5(x)}")
        res["protocole"] = publier_flux(
            24499428,
            "TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent "
            "Governance (Academic Edition v0.31.0) — manuscript, data tables, complete sources "
            "and verification evidence",
            "v0.31.0", DESC_PROTO, f, draft_id=draft_id)
    if "participation" in actions:
        f = [OUT / "TRIADE_participer_v1.2.0.zip"]
        for x in f:
            print(f"  [empreinte] {x.name} sha256 {sha(x)[:16]}… md5 {md5(x)}")
        res["participation"] = publier_flux(
            24499847, "TRIADE Participation Pack v1.2.0: the five kits, evaluation and "
            "contribution", "v1.2.0", DESC_PART, f, draft_id=draft_id
            if len(actions) == 1 else None)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
