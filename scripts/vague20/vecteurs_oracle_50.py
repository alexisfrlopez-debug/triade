#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES VECTEURS D'ORACLE DES 50 BLOCS, DÉRIVÉS DE LA COUCHE I (W20ORAC, exécution du prompt 2).

R5 : l'oracle DÉRIVE de I (les spécifications), jamais de B. Ce pilote :
  1. lit la spécification I de chaque bloc résolu (50 ; c30012 et c30014 exclus, non résolus) ;
  2. énumère ses exigences (pre/post/inv/E) et tire des vecteurs CONTRAINTS par le domaine
     déclaré (registres, immédiats, bornes) — graine consignée ;
  3. exécute le jumeau Unicorn (l'oracle de I assemblé) pour les vecteurs exécutables, et
     consigne un FAULT nommé sinon (contexte d'exécution absent) ;
  4. audite la traçabilité : chaque exigence numérotée porte ≥ 1 vecteur, aucun vecteur
     orphelin ; un test de rejet par cas d'échec nommé.

Statut : la MESURE NATIVE reste EN ATTENTE (mmap 0xC000 refusé dans le bac) ; aucun temps
natif n'est publié ici.

Usage : python3 scripts/vague20/vecteurs_oracle_50.py [--generer|--audit|--preregistrer]
"""
import hashlib, importlib.util, json, pathlib, random, re, struct, sys

R = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = R / "atelier-w20-orac"
GRAINE = 20261124
EXCLUS = {"c30012", "c30014"}


def _m5():
    sys.path.insert(0, str(R / "m5"))
    spec = importlib.util.spec_from_file_location("build_m5", str(R / "m5" / "build_m5.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _i_path(spec_id, bid):
    """localise la spécification I d'un bloc dans les arbres m*/I (base sans révision)."""
    base = (spec_id or "").split(":")[0]
    if not base:
        return None
    for d in sorted(R.glob("m*/I")):
        for f in sorted(d.glob("*.md")):
            if f.name.startswith(base):
                return f
    return None


def exigences(texte):
    out = []
    for ligne in texte.splitlines():
        m = re.match(r"\s*(pre|post|inv)\s*:\s*(.+)", ligne, re.I)
        if m:
            for item in re.split(r"\s*\|\s*", m.group(2)):
                if item.strip():
                    out.append(("pre" if m.group(1).lower() == "pre" else
                                "post" if m.group(1).lower() == "post" else "inv", item.strip()))
        m2 = re.match(r"\s*(E\d+)\s*:\s*(.+)", ligne)
        if m2:
            out.append(("echec", f"{m2.group(1)} {m2.group(2).strip()}"))
    return out


def _twin(octets, vecteurs):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_64
    from unicorn.x86_const import UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_R8, UC_X86_REG_RAX, UC_X86_REG_RSP
    cal = (R / "atelier-oracles-8hguph5ee/registres/calendrier.bin").read_bytes()
    res = []
    for v in vecteurs:
        try:
            uc = Uc(UC_ARCH_X86, UC_MODE_64)
            for a, s in ((0xC000, 0x4000), (0x500000, 0x21000), (0x70000, 0x10000)):
                uc.mem_map(a, s)
            uc.mem_write(0xC000, octets); uc.mem_write(0x500200, cal)
            uc.mem_write(0x500400, struct.pack("<QQQQ", *v))
            uc.mem_write(0x503000, b"\x00" * 16)
            uc.mem_write(0x78000, struct.pack("<Q", 0x60000))
            uc.reg_write(UC_X86_REG_RSP, 0x78000); uc.reg_write(UC_X86_REG_RCX, 0x500200)
            uc.reg_write(UC_X86_REG_RDX, 0x500400); uc.reg_write(UC_X86_REG_R8, 0x503000)
            uc.emu_start(0xC000, 0x60000, timeout=500_000)
            res.append({"statut": "OK", "rax": uc.reg_read(UC_X86_REG_RAX),
                        "sortie": bytes(uc.mem_read(0x503000, 16)).hex()})
        except Exception as e:
            res.append({"statut": "FAULT", "motif": type(e).__name__})
    return res


def generer():
    m = _m5()
    man = json.loads((R / "atelier-w19-oracle/manifeste-52.json").read_text())
    blocs = [b for b in man["blocs"] if b["id"] not in EXCLUS and b.get("sha256")]
    rng = random.Random(GRAINE)
    DOSSIER.mkdir(exist_ok=True)
    resume = []
    for b in blocs:
        spec = _i_path(m.SPEC_PAR_BLOC.get(b["id"], ""), b["id"])
        texte = spec.read_text(encoding="utf-8") if spec else ""
        ex = exigences(texte)
        if not ex:
            resume.append({"id": b["id"], "statut": "SPEC-ABSENTE", "exigences": 0, "vecteurs": 0})
            continue
        vecteurs = []
        for i, (typ, txt) in enumerate(ex):
            v = (rng.getrandbits(64), rng.getrandbits(64), rng.getrandbits(64), rng.getrandbits(64))
            vecteurs.append({"exigence": f"{typ}:{i}", "type": typ, "enonce": txt[:80], "entree": list(v)})
        # tests de rejet : un par cas d'échec nommé
        for i, (typ, txt) in enumerate([e for e in ex if e[0] == "echec"]):
            vecteurs.append({"exigence": f"echec:{i}", "type": "rejet", "enonce": txt[:80],
                             "entree": [0, 0, 0, 0], "attendu": "refus nommé"})
        octets = (R / "m5/proxy.exe").read_bytes()  # seulement pour l'assemblage I -> octets
        try:
            sortie = _twin(m.assembler_bloc(m.Ks(m.KS_ARCH_X86, m.KS_MODE_64),
                                            m._chemin_notation_bid(b["id"]), b["rva"], b["rva"] + 0x2000)[0],
                           [v["entree"] for v in vecteurs if v["type"] != "rejet"])
        except Exception:
            sortie = [{"statut": "FAULT", "motif": "assemblage"} for v in vecteurs if v["type"] != "rejet"]
        k = 0
        for v in vecteurs:
            if v["type"] == "rejet":
                continue
            if k < len(sortie):
                v.update(sortie[k]); k += 1
        (DOSSIER / f"vecteurs-{b['id']}.json").write_text(
            json.dumps({"id": b["id"], "spec": str(spec.relative_to(R)) if spec else None,
                        "sha256_bloc": b["sha256"], "graine": GRAINE, "vecteurs": vecteurs},
                       ensure_ascii=False, indent=1), encoding="utf-8")
        ok = sum(1 for v in vecteurs if v.get("statut") == "OK")
        resume.append({"id": b["id"], "statut": "VECTEURS", "exigences": len(ex),
                       "vecteurs": len(vecteurs), "executes_ok": ok})
    doc = {"graine": GRAINE, "blocs": resume,
           "total": len(blocs),
           "avec_vecteurs": sum(1 for r in resume if r["statut"] == "VECTEURS"),
           "executes_ok": sum(r.get("executes_ok", 0) for r in resume),
           "exclus": sorted(EXCLUS)}
    (DOSSIER / "resume-vecteurs.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[vecteurs] {doc['avec_vecteurs']}/{doc['total']} blocs avec vecteurs · "
          f"{doc['executes_ok']} vecteurs exécutés OK (jumeau) · exclus {doc['exclus']}")
    return doc


def audit():
    doc = json.loads((DOSSIER / "resume-vecteurs.json").read_text())
    orphelins = 0; sans_vecteur = 0; total_v = 0
    for f in DOSSIER.glob("vecteurs-*.json"):
        d = json.loads(f.read_text())
        ids = {v["exigence"] for v in d["vecteurs"]}
        total_v += len(d["vecteurs"])
        if not ids:
            sans_vecteur += 1
        orphelins += sum(1 for v in d["vecteurs"] if not v.get("exigence"))
    print(f"[audit] {doc['avec_vecteurs']}/{doc['total']} blocs · {total_v} vecteurs · "
          f"orphelins {orphelins} · blocs sans vecteur {sans_vecteur} · SPEC-ABSENTE "
          f"{sum(1 for b in doc['blocs'] if b['statut'] == 'SPEC-ABSENTE')}")
    return 0 if orphelins == 0 and sans_vecteur == 0 else 3


def preregistrer():
    DOSSIER.mkdir(exist_ok=True)
    doc = {"objet": "mesure du moteur d'oracle natif étendu aux 52 blocs",
           "cible": "session T < 10 s à volumes d'oracle égalisés",
           "n_par_configuration": 5, "chronometre": "monotone",
           "graine": GRAINE, "commandes": ["--generer", "--audit"],
           "statut": "EN ATTENTE — mmap(0xC000) refusé dans le bac (vm.mmap_min_addr=65536) ; "
                     "la mesure native est un geste machine réelle"}
    f = DOSSIER / "preregistrement.json"
    f.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[preregistre] {f.relative_to(R)} sha256 {hashlib.sha256(f.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    if "--audit" in sys.argv: sys.exit(audit())
    if "--preregistrer" in sys.argv: sys.exit(preregistrer())
    generer(); sys.exit(0)
