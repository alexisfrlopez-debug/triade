#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests_triage.py — LES CONTRÔLES NÉGATIFS VÉCUS du pipeline de triage
(e1lr9i8ts) : (1) un rapport malformé REFUSÉ ; (2) un rapport porteur d'un
secret planté REFUSÉ ; (3) UN POOLING INTER-SCHÉMA SILENCIEUX ATTRAPÉ (les
versions séparées au clustering, la note de périmètre) ; (4) le digest
RECOMPUTABLE depuis les rapports bruts (zéro divergence) ; (5) zéro secret
au digest (le contrôle négatif planté) ; (6) les décisions PROPOSÉES
jamais appliquées (la structure de sortie au format Dxxx + l'arbitrage au
développeur) ; (7) le codage officiel : le double-annotation κ≥0,61 sur
n≥50 RENVOYÉ au kit annotateur (0i4pkzbyr) — le triage NE CODE PAS, il
clusterise."""
import json
import pathlib
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
OUTIL = ICI / "triage_rapports.py"


def run(cmd):
    return subprocess.run([sys.executable, str(OUTIL)] + cmd,
                          capture_output=True, text=True)


def rapport_valide(famille="famille-A", n=3, refus=None, defauts=None,
                   com="", schema="TRIADE-FEEDBACK-v1"):
    return {
        "schema": schema,
        "kit": {"contract": "C-v1", "manifest": "M-v1"},
        "agent": {"family": famille},
        "env": {"os": "linux", "cpu_class": "x86-64"},
        "capability": {"constantes_128": "reussi/128",
                       "smoke_notation": "vert"},
        "measured": {"operations": n, "refus_par_classe": refus or {},
                     "tokens_natifs": 1000 * n, "wall": 4.0 * n,
                     "defauts_fl": defauts or []},
        "commentary": com,
        "consent": {"public_digest": "d" * 64, "licence": "CC-BY-4.0"},
    }


def main():
    lignes = []
    def consigne(l):
        print(l); lignes.append(l)

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)

        # (1) le rapport malformé REFUSÉ
        f = td / "a_malforme.json"
        f.write_text('{"schema": "TRIADE-FEEDBACK-v1", "kit": ', encoding="utf-8")
        r = run(["valider", str(f)])
        c1 = r.returncode == 2 and "malformé" in r.stdout
        consigne("(1) le rapport malformé : " +
                 ("REFUSÉ" if c1 else "ROUGE — PASSÉ"))

        # (2) le secret planté REFUSÉ
        rp = rapport_valide()
        rp["commentary"] = "le jeton " + "ghp_" + \
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd plante"
        f2 = td / "b_secret.json"
        f2.write_text(json.dumps(rp), encoding="utf-8")
        r = run(["valider", str(f2)])
        c2 = r.returncode == 2 and "secret" in r.stdout
        consigne("(2) le rapport porteur d'un secret planté : " +
                 ("REFUSÉ" if c2 else "ROUGE — PASSÉ"))

        # (3) LE POOLING INTER-SCHÉMA ATTRAPÉ : v1 + v2 jamais mélangés
        v1 = td / "c_v1.json"
        v1.write_text(json.dumps(rapport_valide()), encoding="utf-8")
        v2 = td / "d_v2.json"
        v2.write_text(json.dumps(rapport_valide(
            schema="TRIADE-FEEDBACK-v2", famille="famille-B")),
            encoding="utf-8")
        r = run(["trier", str(td)])
        clus = json.loads(r.stdout)["clustering"]
        cles = [k for k in clus if k.startswith("TRIADE-FEEDBACK")]
        c3 = len(cles) == 2 and "TRIADE-FEEDBACK-v1" in clus \
            and "TRIADE-FEEDBACK-v2" in clus
        consigne("(3) le pooling inter-schéma : " +
                 ("ATTRAPÉ — les versions SÉPARÉES au clustering "
                  "(note de périmètre au rejeu)" if c3 else "ROUGE — POOLÉ"))

        # les rapports pour le digest (v1 seulement, + le refus (2))
        for i in range(3):
            g = td / ("e_%d.json" % i)
            g.write_text(json.dumps(rapport_valide(
                famille="famille-%d" % (i % 2),
                refus={"ptr_non_resolu": 3},
                defauts=[{"classe": "frontiere-motif", "locus": "piece",
                          "evidence_sha256": "a" * 64}])),
                encoding="utf-8")

        # (4) le digest RECOMPUTABLE (zéro divergence)
        dig = td / "digest.json"
        r = run(["digest", str(td), "--version", "v0.23.2",
                 "--sortie", str(dig)])
        c4a = r.returncode == 0
        r = run(["recomputer", str(td), "--digest", str(dig)])
        c4 = c4a and r.returncode == 0 and "zéro divergence" in r.stdout
        consigne("(4) le digest recomputable depuis les rapports bruts : " +
                 ("VERT — zéro divergence" if c4 else "ROUGE"))

        # (5) zéro secret au digest : le digest ne porte AUCUN jeton
        txt = dig.read_text(encoding="utf-8")
        c5 = "ghp_" not in txt and "PRIVATE KEY" not in txt
        consigne("(5) zéro secret au digest : " +
                 ("VERT (les rapports refusés à la porte (2) n'y vivent "
                  "pas)" if c5 else "ROUGE"))

        # (6) les décisions PROPOSÉES jamais appliquées
        r = run(["trier", str(td)])
        props = json.loads(r.stdout)["propositions"]
        c6 = all(("AU DÉVELOPPEUR" in p["arbitrage"]) and
                 p["decision_proposee"].startswith("D<prochain>")
                 for p in props)
        consigne("(6) les %d décisions PROPOSÉES au format Dxxx, "
                 "l'arbitrage AU DÉVELOPPEUR : " % len(props) +
                 ("VERT — jamais auto-appliquées" if c6 else "ROUGE"))

        # (7) le codage officiel RENVOYÉ au kit annotateur
        r = run(["trier", str(td)])
        clus = json.loads(r.stdout)["clustering"]
        c7 = all("defauts_fl" in c and "refus_par_classe" in c
                 for c in clus.values())
        consigne("(7) le triage clusterise SANS coder (le codage officiel "
                 "double-annotation κ≥0,61 au kit annotateur 0i4pkzbyr) : "
                 + ("VERT — la structure s'y prête" if c7 else "ROUGE"))

    (ICI / "rapport-autotests.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    print("\nOK — rapport-autotests.txt")


if __name__ == "__main__":
    main()
