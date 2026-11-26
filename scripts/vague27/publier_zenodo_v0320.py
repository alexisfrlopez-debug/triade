#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PUBLICATION ZENODO DE LA RELEASE v0.32.0 (InvenioRDM) — le protocole v0.32.0.
Le moteur est l'édition g de publier_zenodo_v0310.py TRAIT POUR TRAIT (la voie
des quatre formes qui minta v0.31.0 au poste du maître, Entrée 436) ; seuls
l'ancre, le lot, la version, le titre et la description changent.

LA PARTICIPATION N'EST PAS RE-PUBLIÉE : le pack v1.2.0 publié (record
24545356) porte encore les packs v0.31.0 — une v1.3.0 qui porterait les
courants attend la commande du maître (l'écart nommé au LISEZMOI, pas habillé).

Ancres de newversion (records publiés du concept) :
  protocole  24545339 (v0.31.0, concept 24367343)  → v0.32.0

Le jeton vient de l'environnement (ZENODO_TOKEN), jamais affiché ni écrit.
Reprises sur 5xx/504 ; aucune publication partielle : le PUBLISH n'est appelé
qu'après la re-vérification des empreintes déposées. La garde UTC (correctif c)
veut que publication_date soit vécue au bord avant le PUBLISH.

Usage :
  ZENODO_TOKEN=$(cat /home/z/my-project/work/tokens/zenodo.txt) \
      python3 depot/scripts/vague27/publier_zenodo_v0320.py [--draft <id>]
"""
import datetime
import hashlib
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

R = pathlib.Path(__file__).resolve().parents[2]
OUT = R / "depot-zenodo-v0320"
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


def _utc_naive():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def garde_utc(date_pub, maintenant_utc=None):
    """(correctif c, 26/11) Le bord vit la date UTC : une publication_date encore
    «demain» au bord est refusée au PUBLISH (HTTP 400 — le retour du poste du
    26/11, 00:31 Paris = 23:31 UTC la veille). Renvoie None si la date est déjà
    vécue au bord, sinon les minutes d'attente jusqu'à 00:00 UTC ; SystemExit
    si la date est à plus d'un jour dans le futur UTC."""
    if not date_pub:
        return None
    m = maintenant_utc if maintenant_utc is not None else _utc_naive()
    aujourdhui = m.strftime("%Y-%m-%d")
    if date_pub <= aujourdhui:
        return None
    cible = datetime.datetime.strptime(date_pub, "%Y-%m-%d")
    ecart = (cible - m).total_seconds()
    if ecart > 93600:
        raise SystemExit(
            f"garde UTC : publication_date {date_pub} est à plus d'un jour dans "
            f"le futur UTC ({aujourdhui}) — corrige la date.")
    return int(ecart // 60) + (1 if ecart % 60 else 0)


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
    """(correctif d, 26/11) Idempotente au bord : une pièce déjà commise et
    conforme (md5 du bord == md5 local, taille égale) est SAUTÉE ; une pièce
    présente mais divergente (ou jamais commise) est retirée du brouillon puis
    redéposée ; une pièce absente est déposée."""
    base_files = draft["links"]["files"]
    st, d = appel("GET", base_files)
    table = d if st == 200 else {}
    for f in fichiers:
        f = pathlib.Path(f)
        attendu = md5(f)
        ent = _entree(table, f.name)
        if ent is not None:
            api_md5 = (ent.get("checksum") or "").replace("md5:", "")
            taille_bord = ent.get("size") or 0
            if api_md5 and api_md5.lower() == attendu and taille_bord == f.stat().st_size:
                print(f"  [fichier] {f.name} déjà déposé (md5 conforme) — sauté")
                continue
            st2, d2 = appel("DELETE", f"{base_files}/{f.name}")
            if st2 not in (200, 201, 204, 404):
                raise SystemExit(f"retrait {f.name} : HTTP {st2} {d2}")
            print(f"  [fichier] {f.name} retiré du brouillon (divergent au bord : "
                  f"{taille_bord} o, md5 {api_md5 or '—'}) — redéposé")
        st, d = appel("POST", base_files, [{"key": f.name}])
        if st not in (200, 201):
            raise SystemExit(f"creation fichier {f.name} : HTTP {st} {d}")
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


def creators_vivant(dr):
    """(correctif g) le champ creators vit-il en TABLEAU VIVANT au bord ? La
    relecture tranche — pas le code du PUT. Vivant = une liste non vide dont une
    entrée porte «name» ou «person_or_org»."""
    c = (dr.get("metadata") or {}).get("creators")
    if not isinstance(c, list) or not c:
        return False
    for e in c:
        if isinstance(e, dict) and ("name" in e or "person_or_org" in e):
            return True
    return False


def _etat_creators(dr):
    c = (dr.get("metadata") or {}).get("creators")
    if c is None:
        return "absent"
    if isinstance(c, dict):
        return "objet"
    if isinstance(c, list):
        if not c:
            return "tableau-vide"
        if any(isinstance(e, dict) and ("name" in e or "person_or_org" in e) for e in c):
            return "tableau-vivant"
        return "tableau-muet"
    return "null"


def _vue_metadata(d, taille=1600):
    try:
        ext = json.dumps(d, ensure_ascii=False)
    except Exception:
        return ""
    i = ext.find('"metadata"')
    if i >= 0:
        ext = ext[i:]
    return ext[:taille]


def metadonnees_quatre_formes(draft, titre, version, description, type_ressource, publication_type):
    """(correctif g — la voie qui minta v0.31.0, Entrée 436) LA VOIE DES
    QUATRE FORMES : la porte deposits (l'ancienne décennale, schéma legacy —
    celle qui tint au mint de v0.31.0) d'abord, puis records person_or_org
    structuré / person_or_org nom / l'écho du dump — chaque forme POSÉE puis
    VÉRIFIÉE par relecture brute (tableau vivant) ; la première qui tient
    gagne ; aucune ne tient : diagnostiques complets, AUCUN PUBLISH."""
    base = {
        "title": titre,
        "version": version,
        "description": description,
        "license": {"id": "busl-1.1"},
        "resource_type": {"id": type_ressource},
        "publication_date": DATE_PUB,
        "publisher": "Zenodo",
    }
    legacy = {
        "title": titre,
        "upload_type": "publication",
        "publication_type": publication_type,
        "description": description,
        "creators": [{"name": "Lopez, Alexis"}],
        "license": "busl-1.1",
        "publication_date": DATE_PUB,
        "version": version,
        "access_right": "open",
    }
    formes = [
        ("porte-legacy", "deposits", {"metadata": legacy}),
        ("person_or_org-structure", "records",
         {"metadata": dict(base, creators=[
             {"person_or_org": {"type": "personal", "family_name": "Lopez",
                                "given_name": "Alexis"}}])}),
        ("person_or_org-nom", "records",
         {"metadata": dict(base, creators=[
             {"person_or_org": {"name": "Lopez, Alexis"}}])}),
        ("echo-du-dump", "records",
         {"metadata": dict(base, creators=[
             {"name": "Lopez, Alexis", "affiliation": None}])}),
    ]
    dernier_etat = "illisible"
    for nom, porte, corps in formes:
        uri = (f"{API}/deposit/depositions/{draft.get('id')}" if porte == "deposits"
               else draft["links"]["self"])
        st, d = appel("PUT", uri, corps)
        st2, dr = appel("GET", f"{API}/records/{draft.get('id')}/draft")
        if st2 == 200:
            dernier_etat = _etat_creators(dr)
        if st2 == 200 and creators_vivant(dr):
            print(f"  [metadata] posées — creators VIVANT au bord (forme {nom}, PUT HTTP {st})")
            ver = (dr.get("metadata") or {}).get("version", "?")
            print(f"  [lecture] brouillon relu — version {ver} ; creators : tableau-vivant au bord")
            return dr
        print(f"  [metadata] forme {nom} : PUT HTTP {st}, creators {dernier_etat} au bord — forme suivante")
    print(f"  [diagnostic] le brouillon relu (brut, depuis metadata) : {_vue_metadata(dr)}")
    st3, dv = appel("GET", f"{API}/deposit/depositions/{draft.get('id')}")
    if st3 == 200:
        print(f"  [diagnostic] la vue deposits (l'ancienne porte), depuis metadata : {_vue_metadata(dv)}")
    else:
        print(f"  [diagnostic] la vue deposits (l'ancienne porte) : HTTP {st3}")
    raise SystemExit("metadata : aucune des quatre formes n'a tenu creators au bord — "
                     "PUBLISH non tenté (atomique)")


def publier(draft):
    st, d = appel("POST", draft["links"]["publish"])
    if st not in (200, 201, 202):
        raise SystemExit(f"PUBLISH : HTTP {st} {d}")
    return d


def verifie_md5(record, attendus):
    """au bord AUTHENTIFIÉ : chaque fichier du record publié, sa taille et son
    md5 (l'API rend checksum 'md5:<hex>') contre les empreintes locales."""
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
    return (not ecarts), ("md5 3/3" if not ecarts else f"md5 écarts {ecarts}")


DESC_PROTO = """<p><strong>TRIADE v0.32.0 — the edition wave 27 (26 November 2026).</strong> No
measured value changed. The six instructions of the v0.31.0 evaluation were executed:
W27RECON sold the D267 divergence (the Book v1.16 at status derived from the anchoring
journal, the C26 STATUS-INTERPIECES class over five shared statuses); W27RESID sold four
editorial residuals at the source (Table 12 fourteen trees D177, the §1.23/§1.24 titles
distinguished, the French fragments of the manuscript taken to English, the Book
chronology reordered; classes C27 COUNT-TABLECELL, C28 TITLE-UNIQUE, C29 LANG-BODY);
W27CIBLES put the target registry at explicit perimeter (the eras table, CIB-LOC-BUDGET
at two eras side by side labelled HISTORIQUE-DATÉ, C25 extended; eleven lines
recomposed, no target re-drawn); W27DECCO left the D264 structured-output campaign
ready (closed schema of eleven opcodes, imported judge, fail-closed aggregator) with the
named refusal SERVING-ABSENT consigned; W27PREUV lived the symbolic-proof decomposition
(L1c verified 52 steps, L2a verified 7 steps, the L3 replay bit-identical at 1,122
steps, the 4 Gio wall named for L1a/L2, INCOMPLETE remains INCOMPLETE); W27VAES took
the VAES/VPCLMULQDQ corridor through a green gate first (20/20 CAVP equal to EVP byte
for byte, the mutant refused at the first vector) — CIB-AES-105 MISSED at 5.66× EVP
consigned as-is, the target never re-drawn, and the native oracle engine session at
235/235 equal to its twin — CIB-ORACLE-T HELD at 0.266 s median. The generation gate
runs V1..V7 plus twenty-nine fail-closed classes (L1..L29) over the five pieces, twenty
negative mutations refused by name 20/20; the RFC 3161 transparency anchor v0.32.0 is
placed and verified; the provenance recomposed. The five pieces are regenerated
(manuscript v0.32.0, specification v0.15.17, Book v1.16, proofs and presentation
v0.32.0); the v0.31.0 PDFs remain published at record 24545339. Named limits: served
structured output (P4) and Tamarin/ProVerif (P6) remain AWAITING the real post; the
participation pack v1.2.0 still carries the v0.31.0 packs — a v1.3.0 awaits
command.</p>"""


def brouillon_existant(draft_id):
    st, d = appel("GET", f"{API}/records/{draft_id}/draft")
    if st == 200:
        return d
    print(f"  [brouillon] GET HTTP {st} — liens reconstruits (précédent v19)")
    return {"id": draft_id, "links": {
        "files": f"{API}/records/{draft_id}/draft/files",
        "self": f"{API}/records/{draft_id}/draft",
        "publish": f"{API}/records/{draft_id}/draft/actions/publish"}}


def publier_flux(record, titre, version, description, fichiers, draft_id=None,
                 type_ressource="publication-article", publication_type="article"):
    print(f"\n=== {record} → {version} ===")
    draft = brouillon_existant(draft_id) if draft_id else nouvelle_version(record)
    print(f"  [newversion] brouillon {draft.get('id')}")
    televerse(draft, fichiers)
    metadonnees_quatre_formes(draft, titre, version, description,
                               type_ressource, publication_type)
    minutes = garde_utc(DATE_PUB)
    if minutes:
        print(f"  [garde UTC] le bord vit encore la veille : publication_date = "
              f"{DATE_PUB} est DEMAIN au bord — attente de {minutes} min jusqu'à "
              f"00:00 UTC (brouillons vivants, rien ne se perd).")
        cible = datetime.datetime.strptime(DATE_PUB, "%Y-%m-%d")
        while _utc_naive() < cible:
            time.sleep(20)
        print("  [garde UTC] minuit UTC passé — le PUBLISH suit.")
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
    f = [OUT / "TRIADE_soumission_v0.32.0.zip", OUT / "TRIADE_presentation_v0320.zip",
         OUT / "TRIADE_complet_v0.32.0.zip"]
    for x in f:
        print(f"  [empreinte] {x.name} sha256 {sha(x)[:16]}… md5 {md5(x)}")
    res = publier_flux(
        24545339,
        "TRIADE: Enabling LLM Agents to Write Native Code by Hand Under Signed-Intent "
        "Governance (Academic Edition v0.32.0) — manuscript, data tables, complete sources "
        "and verification evidence",
        "v0.32.0", DESC_PROTO, f, draft_id=draft_id,
        type_ressource="publication-article", publication_type="article")
    print(json.dumps({"protocole": res}, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
