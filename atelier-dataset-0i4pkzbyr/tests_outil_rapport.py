#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests_outil_rapport.py — LES CONTRÔLES NÉGATIFS VÉCUS de l'outil
rapport (0i4pkzbyr) : (1) la phrase de test marquée plantée dans un
faux journal DOIT être refusée ; (2) un secret réel planté REFUSÉ ; (3)
LA BOÎTE NOIRE : la chaîne INTACTE vérifiée, UNE MUTATION d'une entrée
DÉTECTÉE (la chaîne rompue) ; (4) le codage F/L sans colonne f/l
REFUSÉ ; (5) la grille D203 : les étiquettes T/X converties un-pour-un
au CSV de soumission ; (6) l'anonymat du paquet (aucun chemin réel,
aucune clé) ; (7) l'outillage H7 : les règles d'arrêt fail-closed
(ab2vh5c2m reconduit — le refus vécu aux QUATRE livraisons)."""
import json
import pathlib
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
OUTIL = ICI / "outil_rapport.py"


def run(cmd):
    return subprocess.run([sys.executable, str(OUTIL)] + cmd,
                          capture_output=True, text=True, cwd=str(ICI))


SESSION = [
    {"type": "operation", "nom": "LOCALISER", "tokens": 627},
    {"type": "refus", "classe": "ptr_non_resolu", "tokens": 312},
    {"type": "operation", "nom": "EDITER", "tokens": 674},
]
CODAGE = ("unite,defaut,etiquette,f_l\n"
          "u01,frontiere-motif,T,F\n"
          "u02,piece-non-trouvee,X,L\n"
          "u03,doc-confusion,T,F\n")


def main():
    lignes = []
    def consigne(l):
        print(l); lignes.append(l)

    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        sj = td / "session.jsonl"
        sj.write_text("\n".join(json.dumps(e) for e in SESSION),
                      encoding="utf-8")

        # (1) la phrase marquée plantée
        s2 = td / "session_marquee.jsonl"
        s2.write_text("\n".join(json.dumps(e) for e in SESSION) + "\n" +
                      json.dumps({"type": "operation", "nom": "SMOKE",
                                  "note": "PHRASE-TEST-MARQUEE-D105"}),
                      encoding="utf-8")
        r = run(["boite-noire", str(s2), str(td / "b1.boite")])
        c1 = r.returncode == 2 and "phrase_test_marquee" in r.stderr \
            and not (td / "b1.boite").exists()
        consigne("(1) la phrase marquee plantee dans le faux journal : "
                 + ("REFUSEE, la boite jamais ecrite" if c1 else "ROUGE"))

        # (2) le secret réel planté
        s3 = td / "session_secret.jsonl"
        s3.write_text("\n".join(json.dumps(e) for e in SESSION) + "\n" +
                      json.dumps({"type": "operation", "note":
                                  "le jeton " + "ghp_" +
                                  "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"}),
                      encoding="utf-8")
        r = run(["boite-noire", str(s3), str(td / "b2.boite")])
        c2 = r.returncode == 2 and "jeton_github" in r.stderr
        consigne("(2) le secret reel plante (ghp_ assemble) : "
                 + ("REFUSE" if c2 else "ROUGE"))

        # (3) la boîte noire : intacte + MUTÉE détectée
        boite_path = td / "boite.json"
        r = run(["boite-noire", str(sj), str(boite_path)])
        ok_creation = r.returncode == 0
        r = run(["verifier-boite", str(boite_path)])
        c3a = ok_creation and r.returncode == 0 and "INTACTE" in r.stdout
        boite = json.loads(boite_path.read_text(encoding="utf-8"))
        boite["entrees"][1]["charge"] = boite["entrees"][1][
            "charge"].replace("refus", "refuS")
        m = td / "boite_mutee.json"
        m.write_text(json.dumps(boite), encoding="utf-8")
        r = run(["verifier-boite", str(m)])
        c3 = c3a and r.returncode == 2 and "ROMPUE" in r.stdout
        consigne("(3) la boite noire : la chaine INTACTE au vert, UNE "
                 "MUTATION d'entree " + ("DETECTEE (la chaine ROMPUE)"
                 if c3 else "ROUGE"))

        # (4) le codage sans la colonne f/l
        c4f = td / "codage_sans_fl.csv"
        c4f.write_text("unite,defaut,etiquette\nu01,frontiere,T\n",
                       encoding="utf-8")
        r = run(["soumettre", str(sj), str(c4f),
                 "--sortie", str(td / "s1")])
        c4 = r.returncode == 2 and "f/l" in r.stderr
        consigne("(4) le codage F/L sans colonne f/l : "
                 + ("REFUSE nomme" if c4 else "ROUGE"))

        # (5)+(6) la soumission valide : les T/X convertis + l'anonymat
        cf = td / "codage.csv"
        cf.write_text(CODAGE, encoding="utf-8")
        r = run(["soumettre", str(sj), str(cf), "--sortie", str(td / "s2")])
        c5 = r.returncode == 0 and "3 étiquettes" in r.stdout
        csv = (td / "s2" / "codage-fl-anonymise.csv").read_text(
            encoding="utf-8")
        c6 = ("/home/z" not in csv and "ghp_" not in csv
              and "T," not in csv.replace("T,F", "").replace("T,X", ""))
        consigne("(5) la grille D203 : les etiquettes T/X converties "
                 "un-pour-un (" + ("3 conversions VERTES" if c5 else "ROUGE") + ")")
        consigne("(6) l'anonymat du paquet (aucun chemin reel, aucune cle, "
                 "aucune etiquette T/X residuelle) : "
                 + ("VERT" if c6 else "ROUGE"))

        # (7) l'outillage H7 : le refus D207 vécu (la pièce ab2vh5c2m)
        agg = ICI.parent / "atelier-validite-ab2vh5c2m" / "agregateur_h7.py"
        plafond = td / "plafond.jsonl"
        plafond.write_text("\n".join(
            json.dumps({"unite": "fermer-tour1", "essai": i, "m2": 10,
                        "vert": False}) for i in range(1, 5)) + "\n",
            encoding="utf-8")
        r = subprocess.run([sys.executable, str(agg), "statut",
                            str(plafond)], capture_output=True, text=True)
        c7 = r.returncode == 2 and "plafond" in r.stdout
        consigne("(7) l'outillage H7 (ab2vh5c2m reconduit) : QUATRE "
                 "livraisons a une unite " + ("REFUSEES (le plafond D207, "
                 "exit 2)" if c7 else "ROUGE"))

    (ICI / "rapport-autotests.txt").write_text(
        "\n".join(lignes) + "\n", encoding="utf-8")
    print("\nOK — rapport-autotests.txt")


if __name__ == "__main__":
    main()
