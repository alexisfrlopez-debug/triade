#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LE STATUT D'ANCRAGE, DÉRIVÉ DU JOURNAL (W24AUDT 1a, C20).

Le statut ne se tape plus : il se LIT. DÉPLOYÉ si le journal d'ancrage porte une entrée dont
le jeton vérifie hors ligne ET dont le témoin recouvre les pièces de l'édition courante ;
EN ATTENTE sinon. Toute divergence entre une pièce et ce statut est refusée par C20.

Usage : python3 scripts/vague24/statut_ancrage.py [--json]
"""
import importlib.util, json, pathlib, sys

R = pathlib.Path(__file__).resolve().parents[2]


def _ancrage():
    sp = importlib.util.spec_from_file_location("a", str(R / "scripts/vague20/ancrage_transparence.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m


def statut(strict=True):
    """strict=True (porte V6) : le témoin doit recouvrir les pièces COURANTES.
    strict=False (génération) : le journal fait foi pour l'ÉDITION — les pièces changent
    pendant la passe elle-même."""
    a = _ancrage()
    journal = R / "atelier-w20-sec" / "ancrage-journal.jsonl"
    if not journal.exists():
        return {"statut": "EN ATTENTE", "motif": "aucun journal d'ancrage"}
    lignes = [json.loads(l) for l in journal.read_text(encoding="utf-8").splitlines() if l.strip()]
    courante = a.EDITION
    for entree in reversed(lignes):
        if entree.get("edition") != courante:
            continue
        if strict:
            try:
                a.verifier()
            except Exception as e:
                return {"statut": "EN ATTENTE", "motif": f"vérification : {e}"}
        else:
            import subprocess
            tsr = R / "atelier-w20-sec" / entree.get("tsr", "")
            tsq = R / "atelier-w20-sec" / entree.get("tsq", "")
            ca = R / "atelier-w20-sec" / "tsa-cacert.pem"
            if not (tsr.exists() and tsq.exists()):
                return {"statut": "EN ATTENTE", "motif": "jeton absent"}
            v = subprocess.run(["openssl", "ts", "-verify", "-in", str(tsr), "-queryfile", str(tsq),
                                "-CAfile", str(ca), "-untrusted", str(ca)], capture_output=True, text=True)
            if v.returncode != 0:
                return {"statut": "EN ATTENTE", "motif": "jeton invalide"}
        return {"statut": "DÉPLOYÉ", "tsa": entree.get("tsa"),
                "jeton_sha256": entree.get("tsr_sha256"),
                "verifie_le": entree.get("verifie_le"), "edition": courante}
    return {"statut": "EN ATTENTE", "motif": f"aucune entrée pour {courante}"}


if __name__ == "__main__":
    d = statut()
    print(json.dumps(d, ensure_ascii=False, indent=1) if "--json" in sys.argv else d["statut"])
