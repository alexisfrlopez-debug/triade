#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""livrer_coffre_vague12.py — LA LIVRAION AU COFFRE (la vague 12, la
release v0.22.1) : LE COMPLET RÉGÉNÉRÉ TRIADE_complet_v0.22.1.zip + LE
RAPPORT DE VÉRIFICATION v0.22.1 + LE MANIFESTE des empreintes à la
RACINE — le tout RECOUPÉ byte-byte par re-téléchargement ; LES PIÈCES
DE SESSION au /test (le rapport de vérification, le manifeste, les
rapports des six ateliers de la vague) recoupées. Les écritures au
RELAIS (le compte de service demeure LECTEUR seul — D101), les lectures
et le recoup au SERVICE (le bord froid), la voie urllib du module
drive_sa_v220.py."""
import hashlib
import json
import pathlib
import sys
import time
import urllib.request

sys.path.insert(0, "/home/z/my-project/depot/scripts/vague11")
import drive_sa_v220 as DS  # noqa: E402
from drive_sa_v220 import trouve  # noqa: E402

REPO = pathlib.Path("/home/z/my-project/depot")
RACINE = "105MmhMGsVEiDICOv8uM8CVjcBm6pcdYp"
TEST = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"


def televerse_robuste(chemin, parent, essais=5):
    """LE TÉLÉVERSEMENT REPRENABLE CORRECT : le 308 « Resume Incomplete »
    est LA RÉPONSE INTERMÉDIAIRE NORMALE du protocole resumable (la faille
    du module vague-11 nommée : ses pièces ne dépassaient jamais un chunk,
    le complet v0.22.1 à 10,2 Mo l'a vécue au premier geste) — LE RANGE du
    308 LU, l'envoi repris À L'OCTET près, PUIS LE RECOUP byte-byte au
    compte de service (le bord froid)."""
    p = pathlib.Path(chemin)
    data = p.read_bytes()
    md5 = hashlib.md5(data).hexdigest()
    fid = trouve(p.name, parent)
    for i in range(essais):
        try:
            if fid:
                # la mise à jour du média (l'idempotence — la pièce posée)
                url = (f"{DS.UPLOAD}/files/{fid}?uploadType=media"
                       f"&supportsAllDrives=true")
                req = urllib.request.Request(
                    url, data=data, method="PATCH",
                    headers={**DS.hdr("relais"),
                             "Content-Type": "application/octet-stream"})
                with urllib.request.urlopen(req, timeout=900) as r:
                    assert r.status == 200, f"mise à jour : HTTP {r.status}"
                print(f"  [mis à jour] {p.name} [{len(data):,} o]")
            else:
                # la session resumable
                url = (f"{DS.UPLOAD}/files?uploadType=resumable"
                       f"&supportsAllDrives=true")
                meta = json.dumps({"name": p.name,
                                   "parents": [parent]}).encode()
                req = urllib.request.Request(
                    url, data=meta, method="POST",
                    headers={**DS.hdr("relais"),
                             "Content-Type": "application/json",
                             "X-Upload-Content-Length": str(len(data)),
                             "X-Upload-Content-Type":
                                 "application/octet-stream"})
                with urllib.request.urlopen(req, timeout=120) as r:
                    loc = r.headers["Location"]
                pos, chunk = 0, 4 * 1024 * 1024
                while pos < len(data):
                    bout = data[pos:pos + chunk]
                    fin = pos + len(bout) - 1
                    req = urllib.request.Request(
                        loc, data=bout, method="PUT",
                        headers={"Content-Range":
                                 f"bytes {pos}-{fin}/{len(data)}"})
                    try:
                        with urllib.request.urlopen(req,
                                                    timeout=900) as r:
                            if r.status in (200, 201):
                                fid = json.loads(r.read())["id"]
                    except urllib.error.HTTPError as e:
                        if e.code == 308:
                            # LA RÉPONSE INTERMÉDIAIRE NORMALE : le Range
                            # du serveur fait foi (jamais l'octet deviné)
                            plage = e.headers.get("Range", "")
                            if "-" in plage:
                                pos = int(plage.split("-")[1]) + 1
                                continue
                            raise
                        raise
                    pos = fin + 1
                print(f"  [téléversé] {p.name} [{len(data):,} o]")
            # LE RECOUP byte-byte (la lecture au compte de service)
            st, body = DS.api("GET", f"/files/{fid}",
                              {"alt": "media", "supportsAllDrives": "true"})
            if st != 200 or body != data:
                raise SystemExit(f"RECOUP ÉCHOUÉ : {p.name}")
            print(f"  VERT {p.name} recoupé byte-byte (md5 {md5[:8]}…)")
            return fid
        except urllib.error.HTTPError as e:
            if e.code in (308, 500, 502, 503, 504) and i + 1 < essais:
                print(f"  [reprise] {p.name} : HTTP {e.code} "
                      f"({i + 1}/{essais}) — la session relancée")
                time.sleep(10)
                continue
            raise
    raise SystemExit(f"ÉCHEC {p.name} après {essais} essais")

RACINE_PIECES = [
    REPO / "depot-zenodo-v0221" / "TRIADE_complet_v0.22.1.zip",
    REPO / "scripts" / "vague12" / "rapport_verification_v0.22.1.txt",
    REPO / "scripts" / "vague12" / "empreintes_livrables_v0.22.1.txt",
]

TEST_PIECES = [
    REPO / "scripts" / "vague12" / "rapport_verification_v0.22.1.txt",
    REPO / "scripts" / "vague12" / "empreintes_livrables_v0.22.1.txt",
    REPO / "atelier-recomposabilite-6kbfrpn7k" /
    "rapport-recomposabilite.txt",
    REPO / "atelier-recomposabilite-6kbfrpn7k" / "rapport-audit-ratios.txt",
    REPO / "atelier-recomposabilite-6kbfrpn7k" / "rapport-census.txt",
    REPO / "atelier-purge-0uug27teo" / "rapport-purge-semantique.txt",
    REPO / "atelier-purge-0uug27teo" / "rapport-verification-purge.txt",
    REPO / "atelier-conformite-alhmpl35u" / "rapport-conformite.txt",
    REPO / "atelier-conformite-alhmpl35u" / "rapport-generatif.txt",
    REPO / "atelier-conformite-alhmpl35u" /
    "grille-reception-autotests.txt",
    REPO / "atelier-double-moteur-14n3k8gd7" /
    "rapport-double-moteur.txt",
    REPO / "atelier-double-moteur-14n3k8gd7" / "rapport-budget-risque.txt",
    REPO / "atelier-double-moteur-14n3k8gd7" /
    "rapport-generalisateur.txt",
    REPO / "atelier-double-moteur-14n3k8gd7" / "rapport-menace-cache.txt",
    REPO / "atelier-ajouter-v2-pgodgk35l" / "rapport-ajouter-v2.txt",
    REPO / "atelier-ajouter-v2-pgodgk35l" / "rapport-campagne-v2.txt",
    REPO / "atelier-marge-vierge-x705m50vl" /
    "rapport-marge-vierge.txt",
]


def main():
    print("== (1) LA RACINE DU COFFRE : le complet v0.22.1, le rapport, "
          "le manifeste ==")
    for f in RACINE_PIECES:
        televerse_robuste(f, RACINE)
    print("== (2) LE /test : le rapport, le manifeste, les rapports des "
          "six ateliers de la vague ==")
    for f in TEST_PIECES:
        televerse_robuste(f, TEST)
    print("LA LIVRAISON AU COFFRE VÉCUE — la racine et le /test, chaque "
          "pièce recoupée byte-byte")


if __name__ == "__main__":
    sys.exit(main())
