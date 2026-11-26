#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""L'ANCRAGE DE TRANSPARENCE DES TÉMOINS D'ÉPOQUE (D267 → APPLIQUÉ, W20SEC).

Un témoin d'époque (édition, empreintes des pièces, empreinte de l'état, date) est ancré
hors de la machine par un horodatage RFC 3161 auprès d'une autorité publique. Le jeton est
vérifié cryptographiquement HORS LIGNE (openssl ts -verify) et son empreinte confrontée au
témoin. Refus nommés : ANCRE-INDISPONIBLE (aucune TSA joignable), TEMOIN-SANS-ANCHE (jeton
absent ou invalide), ANCRE-INCOHERENTE (l'empreinte ancrée ne recoupe pas le témoin).

Le chargement R10 ne fait AUCUN appel réseau : l'ancrage est une propriété de release.

Usage :
  python3 scripts/vague20/ancrage_transparence.py            # témoin + ancrage + vérification
  python3 scripts/vague20/ancrage_transparence.py --verifier # revérifie le reçu existant
  python3 scripts/vague20/ancrage_transparence.py --negatifs # trois refus nommés
"""
import hashlib, json, pathlib, subprocess, sys, tempfile, time, urllib.error, urllib.request

R = pathlib.Path(__file__).resolve().parents[2]
DOSSIER = R / "atelier-w20-sec"
import os
# le pack courant se lit dans l'environnement (défaut : le plus récent pack-v2*)
def _pack():
    if os.environ.get("TRIADE_PACK"):
        return pathlib.Path(os.environ["TRIADE_PACK"])
    def _num(p):
        import re as _re
        m = _re.search(r"pack-v(\d+)", p.name)
        return int(m.group(1)) if m else 0
    return sorted([p for p in R.glob("pack-v*") if p.is_dir()], key=_num)[-1]


PACK = _pack()
import re as _re
def _edition_du_pack():
    # la reprise du 27/11/2026 (la correction v0.33.1) : l'édition suit le MANIFESTE du pack —
    # le patron correctif reconduit les pièces SOUS LEUR NOM D'ORIGINE, le manifeste dit l'édition
    mans = sorted(PACK.glob("empreintes_livrables_v*.txt"))
    if mans:
        m = _re.search(r"empreintes_livrables_(v[0-9.]+)\.txt", mans[-1].name)
        if m:
            return m.group(1)
    _m2 = next((x for x in (PACK / "1-manuscrit").glob("TRIADE_manuscrit_v*.pdf")), None)
    return _re.search(r"TRIADE_manuscrit_(v[0-9.]+)\.pdf", _m2.name).group(1) if _m2 else "v0.0.0"
_m2 = next((x for x in (PACK / "1-manuscrit").glob("TRIADE_manuscrit_v*.pdf")), None)
EDITION = os.environ.get("TRIADE_EDITION") or _edition_du_pack()
def _piece(dossier, motif):
    return next(iter(sorted((PACK / dossier).glob(motif))), PACK / dossier / "absent.pdf")

PIECES = {
    "manuscrit": _piece("1-manuscrit", "TRIADE_manuscrit_v*.pdf"),
    "specification": _piece("2-specification", "Protocole_TRIADE_v*_Specification.pdf"),
    "livre": _piece("3-coffre-fort", "Livre_du_Coffre_*.pdf"),
    "preuves": _piece("4-preuves-calculs", "TRIADE_preuves_et_calculs_v*.pdf"),
    "presentation": _piece("5-presentation", "TRIADE_presentation_v*.pdf"),
}
TSAS = ["https://freetsa.org/tsr"]
CA = "https://freetsa.org/files/cacert.pem"


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


class Refus(Exception):
    def __init__(self, code, motif):
        super().__init__(f"{code}: {motif}")
        self.code, self.motif = code, motif


def temoin():
    if not all(p.exists() for p in PIECES.values()):
        raise Refus("TEMOIN-SANS-ANCHE", "pièces absentes")
    d = {"edition": EDITION, "cree_le": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "pieces": {k: sha(v) for k, v in PIECES.items()}}
    d["etat_sha256"] = hashlib.sha256(json.dumps(d["pieces"], sort_keys=True).encode()).hexdigest()
    return d


def _post_tsq(chemin_tsq, url):
    data = pathlib.Path(chemin_tsq).read_bytes()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/timestamp-query"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def ancrer(t, tsas=None, cafile=None):
    DOSSIER.mkdir(exist_ok=True)
    tf = DOSSIER / f"temoin-epoch-{EDITION}.json"
    tf.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    tsq = DOSSIER / f"temoin-epoch-{EDITION}.tsq"
    subprocess.run(["openssl", "ts", "-query", "-data", str(tf), "-sha256", "-cert", "-out", str(tsq)],
                   check=True, capture_output=True)
    for url in (tsas or TSAS):
        try:
            jeton = _post_tsq(tsq, url)
        except Exception as e:
            continue
        tsr = DOSSIER / f"temoin-epoch-{EDITION}.tsr"
        tsr.write_bytes(jeton)
        ca = DOSSIER / "tsa-cacert.pem"
        if not ca.exists():
            ca.write_bytes(urllib.request.urlopen(cafile or CA, timeout=45).read())
        v = subprocess.run(["openssl", "ts", "-verify", "-in", str(tsr), "-queryfile", str(tsq),
                            "-CAfile", str(ca), "-untrusted", str(ca)], capture_output=True, text=True)
        if v.returncode != 0 or "Verification: OK" not in (v.stdout + v.stderr):
            raise Refus("TEMOIN-SANS-ANCHE", f"vérification openssl : {(v.stdout + v.stderr).strip()[:120]}")
        recu = {"tsa": url, "tsr": tsr.name, "tsr_sha256": sha(tsr), "tsq": tsq.name,
                "temoin": tf.name, "temoin_sha256": sha(tf), "edition": EDITION,
                "verifie_le": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "verification": "openssl ts -verify : OK", "imprint_sha256": sha(tf)}
        (DOSSIER / "ancrage-recu.json").write_text(json.dumps(recu, indent=1) + "\n", encoding="utf-8")
        # JOURNAL APPEND-ONLY (D271) : un ré-ancrage n'EFFACE pas l'histoire des ancrages
        journal = DOSSIER / "ancrage-journal.jsonl"
        with journal.open("a", encoding="utf-8") as f:
            f.write(json.dumps(recu, ensure_ascii=False, sort_keys=True) + "\n")
        return recu
    raise Refus("ANCRE-INDISPONIBLE", "aucune autorité d'horodatage joignable")


def verifier():
    recu_f = DOSSIER / "ancrage-recu.json"
    if not recu_f.exists():
        raise Refus("TEMOIN-SANS-ANCHE", "aucun reçu d'ancrage")
    recu = json.loads(recu_f.read_text())
    tf = DOSSIER / recu["temoin"]
    tsr = DOSSIER / recu["tsr"]
    if not tf.exists() or not tsr.exists():
        raise Refus("TEMOIN-SANS-ANCHE", "témoin ou jeton absent")
    if recu["edition"] != EDITION:
        raise Refus("TEMOIN-SANS-ANCHE", f"reçu d'une autre édition ({recu['edition']})")
    if sha(tf) != recu["temoin_sha256"] or sha(tsr) != recu["tsr_sha256"]:
        raise Refus("ANCRE-INCOHERENTE", "empreinte du témoin ou du jeton divergente")
    t = json.loads(tf.read_text())
    if t["pieces"] != {k: sha(v) for k, v in PIECES.items()}:
        raise Refus("ANCRE-INCOHERENTE", "le témoin ne recouvre pas les pièces publiées")
    ca = DOSSIER / "tsa-cacert.pem"
    v = subprocess.run(["openssl", "ts", "-verify", "-in", str(tsr), "-queryfile",
                        str(DOSSIER / recu["tsq"]), "-CAfile", str(ca), "-untrusted", str(ca)],
                       capture_output=True, text=True)
    if v.returncode != 0 or "Verification: OK" not in (v.stdout + v.stderr):
        raise Refus("TEMOIN-SANS-ANCHE", "jeton invalide")
    return recu


def negatifs():
    essais = []
    # 1. témoin muté → ANCRE-INCOHERENTE
    recu = json.loads((DOSSIER / "ancrage-recu.json").read_text())
    tf = DOSSIER / recu["temoin"]; sauvegarde = tf.read_bytes()
    try:
        t = json.loads(sauvegarde); t["pieces"]["manuscrit"] = "0" * 64
        tf.write_text(json.dumps(t, indent=1))
        try:
            verifier(); essais.append(("témoin muté", False, "aucun refus"))
        except Refus as r:
            essais.append(("témoin muté", r.code == "ANCRE-INCOHERENTE", r.code))
    finally:
        tf.write_bytes(sauvegarde)
    # 2. TSA injoignable → ANCRE-INDISPONIBLE
    try:
        ancrer(temoin(), tsas=["https://127.0.0.1:9/tsr"])
        essais.append(("TSA injoignable", False, "aucun refus"))
    except Refus as r:
        essais.append(("TSA injoignable", r.code == "ANCRE-INDISPONIBLE", r.code))
    # 3. jeton absent → TEMOIN-SANS-ANCHE
    tsr = DOSSIER / recu.get("tsr", "absent.tsr"); sauv = tsr.read_bytes() if tsr.exists() else None
    try:
        if tsr.exists():
            tsr.unlink()
        try:
            verifier(); essais.append(("jeton absent", False, "aucun refus"))
        except Refus as r:
            essais.append(("jeton absent", r.code == "TEMOIN-SANS-ANCHE", r.code))
    finally:
        if sauv is not None:
            tsr.write_bytes(sauv)
    for nom, ok, code in essais:
        print(f"[{'VERT' if ok else 'ROUGE'}] {nom} → {code}")
    # les essais ont pu laisser un témoin/tsq réécrits : on ré-ancre proprement
    ancrer(temoin()); verifier()
    print("[nettoyage] ancrage ré-établi et vérifié")
    return 0 if all(ok for _, ok, _ in essais) else 3


def main():
    if "--negatifs" in sys.argv:
        return negatifs()
    if "--verifier" in sys.argv:
        r = verifier(); print(f"[VERT] ancrage vérifié — {r['tsa']} · jeton {r['tsr_sha256'][:16]}…"); return 0
    recu = ancrer(temoin())
    print(f"[VERT] témoin ancré — {recu['tsa']} · jeton sha256 {recu['tsr_sha256'][:16]}… "
          f"· empreinte du témoin {recu['imprint_sha256'][:16]}…")
    verifier(); print("[VERT] re-vérification hors ligne : OK")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refus as r:
        print(f"[REFUS] {r.code} — {r.motif}")
        sys.exit(2)
