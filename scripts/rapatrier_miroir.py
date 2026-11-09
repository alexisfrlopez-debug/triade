#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rapatrie le différentiel miroir Drive -> clone local (E126→E208).

Télécharge : fichiers nouveaux + fichiers dont le md5 local diverge.
Exclut : bundles racine, zones gitignorées (.tmp/, upload/, bundles-*/).
Multi-thread (6 workers). Journal : /tmp/rapatriement.log
"""
import hashlib
import json
import os
import sys
import threading
import queue

sys.path.insert(0, "/home/z/my-project/scripts")
from drive_api import _get  # noqa: E402

REPO = "/home/z/my-project/triade"
MANIFESTE = "/tmp/manifeste_miroir.json"
EXCLUSIONS = (
    "/.gitignore",  # traité à part (le miroir EST la vérité, on le prend)
)
IGNORER = ("/.tmp/", "/upload/", "/bundles-/", "/terrain/livraison/",
           "/archives-bundles/")
EXTENSIONS_BUNDLE = (".bundle",)


def md5_local(chemin):
    h = hashlib.md5()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def telecharger(fid, destination):
    import urllib.request
    req = urllib.request.Request(
        f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media",
        headers={"Authorization": f"Bearer {__import__('drive_api').obtenir_token()}"})
    with urllib.request.urlopen(req, timeout=300) as r:
        donnees = r.read()
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "wb") as f:
        f.write(donnees)
    return len(donnees)


def main():
    mani = json.load(open(MANIFESTE))
    a_prendre = []
    for m in mani:
        c = m["chemin"]
        if c.endswith(EXTENSIONS_BUNDLE) and c.count("/") == 1:
            continue  # bundles racine : backups Drive, pas au dépôt
        if any(x in c for x in IGNORER):
            continue  # zones gitignorées
        dest = REPO + c
        if os.path.isfile(dest):
            if m["md5"] and md5_local(dest) == m["md5"]:
                continue  # identique
        a_prendre.append(m)
    print(f"[rapatriement] {len(a_prendre)} fichiers à télécharger, "
          f"{sum(m['taille'] for m in a_prendre)} o", flush=True)

    trav = queue.Queue()
    for m in a_prendre:
        trav.put(m)
    stats = {"ok": 0, "octets": 0, "erreurs": []}
    verrou = threading.Lock()

    def ouvrier():
        while True:
            try:
                m = trav.get_nowait()
            except queue.Empty:
                return
            try:
                n = telecharger(m["id"], REPO + m["chemin"])
                with verrou:
                    stats["ok"] += 1
                    stats["octets"] += n
                    if stats["ok"] % 50 == 0:
                        print(f"[rapatriement] {stats['ok']}/{len(a_prendre)} "
                              f"({stats['octets']/1e6:.1f} Mo)", flush=True)
            except Exception as e:
                with verrou:
                    stats["erreurs"].append((m["chemin"], str(e)))
            finally:
                trav.task_done()

    fils = [threading.Thread(target=ouvrier, daemon=True) for _ in range(6)]
    for f in fils:
        f.start()
    for f in fils:
        f.join()
    print(f"[rapatriement] TERMINÉ : {stats['ok']} fichiers, "
          f"{stats['octets']/1e6:.1f} Mo, {len(stats['erreurs'])} erreurs", flush=True)
    for c, e in stats["erreurs"][:20]:
        print(f"  ERREUR {c} : {e}", flush=True)
    json.dump(stats, open("/tmp/rapatriement_stats.json", "w"))


if __name__ == "__main__":
    main()
