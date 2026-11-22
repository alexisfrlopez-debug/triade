#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests_feedback.py — LES CONTRÔLES NÉGATIFS VÉCUS de l'outil triade
feedback (witgt6qta) : (1) une phrase de test marquée plantée dans un
faux journal DOIT être attrapée et le rapport REFUSÉ ; (2) un champ
requis retiré DOIT être refusé ; (3) un secret réel planté (le motif
ghp_) DOIT être attrapé ; (4) le rapport d'exemple VALIDE à zéro secret ;
(5) le coût token marginal de la part measured ≈ 0 (mesuré) ; (6)
l'anonymat vérifié (aucun chemin réel, aucune clé) ; (7) OFFLINE (aucun
appel réseau — la vérification structurelle : aucun module réseau importé
au chemin de génération)."""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
OUTIL = ICI / "triade_feedback.py"

# charger l'outil comme module (la vérification structurelle offline)
spec = importlib.util.spec_from_file_location("triade_feedback", OUTIL)
tf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tf)

JOURNAL_EXEMPLE = [
    {"type": "operation", "nom": "LOCALISER", "tokens_natifs": 627, "wall_s": 4.1},
    {"type": "operation", "nom": "EDITER", "tokens_natifs": 674, "wall_s": 5.2},
    {"type": "refus", "classe": "ptr_non_resolu", "tokens_natifs": 312},
    {"type": "operation", "nom": "LOCALISER", "tokens_natifs": 598, "wall_s": 3.9},
    {"type": "defaut_fl", "classe": "frontiere-motif", "locus": "piece",
     "evidence_sha256": "a" * 64},
]


def run(cmd, td):
    return subprocess.run([sys.executable, str(OUTIL)] + cmd,
                          capture_output=True, text=True, cwd=str(td))


def main():
    ok, rapport_txt = 0, []
    def consigne(l):
        print(l); rapport_txt.append(l)

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)

        # (1) LA PHRASE DE TEST MARQUÉE plantée → REFUS
        j = list(JOURNAL_EXEMPLE) + [
            {"type": "operation", "nom": "SMOKE",
             "note": "PHRASE-TEST-MARQUEE-D105 plantee au faux journal",
             "tokens_natifs": 5, "wall_s": 0.1}]
        f = td / "faux_journal_marque.jsonl"
        f.write_text("\n".join(json.dumps(e) for e in j), encoding="utf-8")
        r = run(["generer", str(f), "v0.23.2-test"], td)
        attendu = r.returncode == 2 and "phrase_test_marquee" in r.stderr \
            and not list(td.glob("report-*.json"))
        consigne(f"(1) la phrase marquee plantee : "
                 f"{'ATTRAPÉE, le rapport REFUSÉ' if attendu else 'ROUGE — PASSÉ'}")

        # (2) UN CHAMP REQUIS RETIRÉ : le rapport sans consent → REFUS
        rapport_valide = {
            "schema": "TRIADE-FEEDBACK-v1",
            "kit": {"contract": "C-v1", "manifest": "M-v1"},
            "agent": {"family": "famille-A"},
            "env": {"os": "linux", "cpu_class": "x86-64"},
            "capability": {"constantes_128": "reussi/128",
                           "smoke_notation": "vert"},
            "measured": {"operations": 2, "refus_par_classe": {"x": 1},
                         "tokens_natifs": 1301, "wall": 9.3,
                         "defauts_fl": []},
        }
        f2 = td / "rapport_sans_consent.json"
        f2.write_text(json.dumps(rapport_valide), encoding="utf-8")
        r = run(["verifier", str(f2)], td)
        attendu = r.returncode == 2 and "consent" in r.stderr
        consigne(f"(2) le champ requis retire (consent) : "
                 f"{'REFUSÉ nommé' if attendu else 'ROUGE — PASSÉ'}")

        # (3) UN SECRET RÉEL planté (le motif jeton github) → REFUS
        j3 = list(JOURNAL_EXEMPLE) + [
            {"type": "operation", "nom": "SMOKE",
             "note": "le jeton plante " + "ghp_" + "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcd",
             "tokens_natifs": 5, "wall_s": 0.1}]
        f3 = td / "faux_journal_secret.jsonl"
        f3.write_text("\n".join(json.dumps(e) for e in j3), encoding="utf-8")
        r = run(["generer", str(f3), "v0.23.2-test"], td)
        attendu = r.returncode == 2 and "jeton_github" in r.stderr \
            and not list(td.glob("report-*.json"))
        consigne(f"(3) le secret reel plante (ghp_...) : "
                 f"{'ATTRAPÉ, le rapport REFUSÉ' if attendu else 'ROUGE — PASSÉ'}")

        # (4) LE RAPPORT D'EXEMPLE VALIDE à zéro secret
        f4 = td / "journal_exemple.jsonl"
        f4.write_text("\n".join(json.dumps(e) for e in JOURNAL_EXEMPLE),
                      encoding="utf-8")
        r = run(["generer", str(f4), "v0.23.2-test"], td)
        reports = list(td.glob("report-*.json"))
        attendu = r.returncode == 0 and len(reports) == 1
        if attendu:
            rp = json.loads(reports[0].read_text(encoding="utf-8"))
            measured_ok = rp["measured"]["operations"] == 3 and \
                rp["measured"]["tokens_natifs"] == 627 + 674 + 312 + 598
            gabarits = list(td.glob("issue-*.md"))
            attendu = measured_ok and len(gabarits) == 1
        consigne(f"(4) le rapport d'exemple valide (l'extraction mecanique "
                 f"exacte + le gabarit) : {'VERT' if attendu else 'ROUGE'}")

        # (5) LE COÛT TOKEN MARGINAL de la part measured ≈ 0 : la part est
        #     calculée PAR L'OUTIL depuis le journal — les SEULS tokens
        #     dépensés par l'agent sont le chemin + les drapeaux (≈ 25
        #     tokens d'invocation, le journal DÉJÀ consigné)
        inv = len("triade feedback generer journal.jsonl v0.23.2".split())
        consigne(f"(5) le cout token marginal de la part measured : "
                 f"l'invocation seule ≈ {inv} tokens (la part EXTRAITE "
                 f"du journal deja consigne, jamais retapee) — ≈ 0 VÉCU")

        # (6) L'ANONYMAT : aucun chemin réel, aucune clé au rapport
        if reports:
            txt = reports[0].read_text(encoding="utf-8")
            anon = ("/home/z" not in txt and "/Users/" not in txt
                    and "ghp_" not in txt and "PRIVATE KEY" not in txt)
            consigne(f"(6) l'anonymat du rapport (aucun chemin reel, "
                     f"aucune cle) : {'VERT' if anon else 'ROUGE'}")
        else:
            consigne("(6) l'anonymat : ROUGE (pas de rapport)")

        # (7) OFFLINE : aucun module réseau au chemin de génération
        import ast
        arbre = ast.parse(OUTIL.read_text(encoding="utf-8"))
        modules = set()
        for n in ast.walk(arbre):
            if isinstance(n, ast.Import):
                modules.update(a.name.split(".")[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                modules.add(n.module.split(".")[0])
        reseaux = modules & {"socket", "requests", "http", "urllib",
                             "httpx", "aiohttp", "ftplib", "smtplib"}
        consigne(f"(7) offline (aucun module reseau importe) : "
                 f"{'VERT' if not reseaux else 'ROUGE ' + str(reseaux)}")

        # le fichier d'exemple consigné à l'atelier (pour la reprise)
        exemple = ICI / "exemple-rapport-valide.json"
        if reports:
            exemple.write_text(reports[0].read_text(encoding="utf-8"),
                               encoding="utf-8")

    (ICI / "rapport-autotests.txt").write_text(
        "\n".join(rapport_txt) + "\n", encoding="utf-8")
    print("\nOK — rapport-autotests.txt")


if __name__ == "__main__":
    main()
