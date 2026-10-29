#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Achève la révision v0.5.0 de sec-d.tex : lignes du tableau des jalons."""

from pathlib import Path

P = Path("/home/z/my-project/triade/scripts/spec_v040/sec-d.tex")
s = P.read_text(encoding="utf-8")


def remplace(ancien: str, nouveau: str):
    global s
    n = s.count(ancien)
    if n == 0:
        assert nouveau in s, f"déjà absent ET introuvable : {ancien[:60]!r}"
        print(f"[--] déjà appliqué : {ancien[:48]!r}")
        return
    assert n == 1, f"{n} occurrences : {ancien[:60]!r}"
    s = s.replace(ancien, nouveau, 1)
    print(f"[ok] {ancien[:48]!r}")


# Lignes du tableau des jalons : ajout de la colonne Statut
remplace("exécutable $<$ 4 Kio ; R1–R3, R8–R9 dès le premier octet \\\\",
         "exécutable $<$ 4 Kio ; R1–R3, R8–R9 dès le premier octet & "
         "\\textbf{franchi} 26/10/2026 (D26) \\\\")
remplace("adresses stables démontrées ; première mesure effective des budgets tokens \\\\",
         "adresses stables démontrées ; première mesure effective des budgets tokens &\n"
         "\\textbf{franchi} 26/10/2026 — balise 0.2.0 (D32) \\\\")
remplace("rollback démontré ; régression post-patch nulle \\\\",
         "rollback démontré ; régression post-patch nulle & \\textbf{franchi} 27/10/2026 "
         "— balise\n0.3.0, boucle complète démontrée terrain (D43) \\\\")
remplace("transparent ; contrats renforcés \\\\",
         "transparent ; contrats renforcés & \\textbf{ouvert} 27/10/2026 (D45) \\\\")
remplace("M4 — tunnel chiffré & HTTPS en transit ; échec propre sur certificat invalide \\\\",
         "M4 — tunnel chiffré & HTTPS en transit ; échec propre sur certificat invalide & "
         "à venir \\\\")
remplace("journal en production ; empreintes par build actives \\\\",
         "journal en production ; empreintes par build actives & à venir \\\\")
remplace("I} ; parité inter-profils vérifiée ; même oracle vert sur les deux profils \\\\",
         "I} ; parité inter-profils vérifiée ; même oracle vert sur les deux profils & "
         "à venir \\\\")
remplace("multi-profils vérifié \\\\",
         "multi-profils vérifié & à venir \\\\")

# Vérification : les 8 statuts sont en place (les lignes s'étendent sur 2 lignes de fichier)
debut = s.find("\\begin{tabularx}{\\textwidth}{@{}l Y l@{}}")
fin = s.find("\\end{tabularx}", debut)
table = s[debut:fin]
attendus = ["\\textbf{franchi} 26/10/2026 (D26)",
            "balise 0.2.0 (D32)",
            "balise\n0.3.0, boucle complète démontrée terrain (D43)",
            "\\textbf{ouvert} 27/10/2026 (D45)"]
manquants = [a for a in attendus if a not in table]
assert not manquants, f"statuts manquants : {manquants}"
assert table.count("à venir") == 4, f"{table.count('à venir')} 'à venir' (attendu 4)"
print("[ok] tableau jalons : 8 statuts en place (3 franchis, 1 ouvert, 4 à venir)")

P.write_text(s, encoding="utf-8")
print("sec-d.tex : lignes du tableau des jalons complétées")
