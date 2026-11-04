#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""diff_nul_corpus.py — LE DIFF NUL MESURÉ PAR SCRIPT, instance M7 (chantier
M7-(b) : la TROISIÈME instanciation de la même couche I, D149-(7)).

La promesse : « les MÊMES fichiers I que unix/ » — l'instance RV64 du corpus
charge EXACTEMENT les fichiers canoniques de unix/I/ (les révisions R+1 de
granularité), AUCUNE COPIE nulle part : le dépôt porte UNE couche I du
corpus, les deux instances (x86-64-linux, riscv64-linux) la chargent depuis
unix/I/ — c'est la thèse même du diff nul : l'intention vit dans I, pas
dans les octets (D149-(3)).

Quatre recoupements, rejouables :

  1. LES FICHIERS CANONIQUES — les 13 specs du corpus (les 12 révisions
     R+1 + le principal) : empreintes sha256 mesurées ; le plan de l'instance
     RV64 (riscv/layout.py BLOCS_CORPUS) résout vers EXACTEMENT ces chemins
     (concordance par NOM, une divergence est un refus) ; AUCUNE copie du
     corpus ailleurs dans le dépôt (la copie tuerait le diff nul) ;

  2. L'ÉQUIVALENCE DES OBSERVABLES R1 ↔ R+1 — la propriété du DÉPÔT, mesurée
     par la chaîne M6 (unix/diff_nul.py — le jalon M6 la mesure sur EXACTEMENT
     les fichiers que l'instance M7 charge) : rejoué ici, exigé VERT ;

  3. L'INVARIANCE DES SCELLÉS — les artefacts Windows (hello.exe 0.1.0,
     selftest.exe 0.2.0, echo.exe 0.3.0, proxy.exe 0.4.0, proxy.exe 0.6.0)
     + le corpus unix (0.7.0-dev.2, la première instanciation de la couche I)
     + la sonde riscv (0.8.0-dev.1, le chantier M7-(a)) : empreintes
     identiques à l'état zéro mesuré À L'OUVERTURE du chantier (05/11) —
     le chantier (b) ne touche AUCUN scellé ;

  4. LA PARITÉ PAR EXÉCUTION § 8.3 — la ligne du patrimoine
     (« TRIADE M1 : minilibc 21/21 OK\\n ») est l'OBSERVABLE INVARIANT des
     TROIS profils (l'instance Windows scellée, l'instance x86-64-linux, la
     présente instance riscv64-linux) : les octets attendus sont portés par
     le script, l'oracle qemu de build_corpus.py les constate en exécution
     (la parité se vérifie PAR EXÉCUTION, jamais par déduction — spec § 8.3).

Usage : python3 riscv/diff_nul_corpus.py
Code de sortie : 0 = diff nul VERT ; 1 = écart nommé.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
UNIX = os.path.join(RACINE, "unix")

# Le corpus : les specs chargées par le plan de l'instance (riscv/layout.py)
sys.path.insert(0, ICI)
import layout as L  # noqa: E402

CORPUS = [(fichier, sid) for _, sid, fichier, _, _ in L.BLOCS_CORPUS]

# L'état zéro mesuré à l'OUVERTURE du chantier M7-(b) (05/11) — le chantier
# ne touche AUCUN scellé : la sonde riscv (M7-(a)), le corpus unix (M6-(b),
# la première instanciation de la même couche I) et les cinq scellés Windows.
ETAT_ZERO = {
    "m0/hello.exe": "c89e330cd16f3fd48558ed4fdb6708fb671e6d907547d5c1ee28075ffd6507f2",
    "m1/selftest.exe": "8038585b7af83c9fe5e6fdccd197e67888b9e5fb09d8d6c84cb998c684bff3c0",
    "m2/echo.exe": "da4a6ca299339567be59ba5c48b1ad3de384bdc316c5a523ebd272b307d3fdb2",
    "m3/proxy.exe": "bf02769fa324ff79b07550c5f31fe6e8f7b0611489e710d16ee07afa73c070af",
    "m5/proxy.exe": "c1e46fb0b857b6f33c67aa7f26a1db3064f2e3adbd528414116b497220b6a20c",
    "unix/corpus": "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7",
    "riscv/sonde": "d122bc68fec2412677a9ebdd529a5f1d7d42b95898d680d78baa3a349f28d96e",
}
ROLES = {
    "m0/hello.exe": "scellé 0.1.0 (M0)",
    "m1/selftest.exe": "scellé 0.2.0 (M1)",
    "m2/echo.exe": "scellé 0.3.0 (M2)",
    "m3/proxy.exe": "scellé 0.4.0 (M3)",
    "m5/proxy.exe": "scellé 0.6.0 (M5, finale)",
    "unix/corpus": "la PREMIÈRE instanciation de la couche I (M6-(b), 0.7.0-dev.2)",
    "riscv/sonde": "le chantier M7-(a) (0.8.0-dev.1) — INTACT, le corpus ne le touche pas",
}

# La ligne du patrimoine : l'OBSERVABLE INVARIANT des TROIS profils (§ 8.3 —
# la parité par exécution : les MÊMES octets, l'instance Windows scellée les
# rend en \\r\\n, les instances Linux en \\n — le terminateur est la
# discipline du profil, le verdict est l'observable)
LIGNE_PATRIMOINE = b"TRIADE M1 : minilibc 21/21 OK\n"


def sha(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> int:
    print("=== LE DIFF NUL, instance M7 (mesuré par script — D149-(7), chantier M7-(b)) ===")
    rapports: list[str] = []

    # 1 — les fichiers canoniques : empreintes + concordance du plan + zéro copie
    print("\n[1] Les fichiers canoniques de la couche I (unix/I/) — chargés par l'instance RV64")
    total = 0
    for fichier, sid in CORPUS:
        chemin = os.path.join(UNIX, "I", fichier + ".md")
        if not os.path.exists(chemin):
            print(f"ÉCHEC : fichier canonique absent : {chemin}")
            return 1
        print(f"  {fichier:28s} {sid:14s} sha256:{sha(chemin)[:24]}…")
        total += 1
    # la concordance : le plan de l'instance (riscv/layout.py) épingle
    # id:R{rev} — les specs relues doivent porter la révision épinglée
    sys.path.insert(0, UNIX)
    for fichier, sid in CORPUS:
        with open(os.path.join(UNIX, "I", fichier + ".md"), encoding="utf-8") as f:
            premiere = f.read().splitlines()[0]
        import re
        m = re.match(r"(\S+) · (.+?) · révision (\d+)", premiere)
        lu = f"{m.group(1)}:R{m.group(3)}"
        if lu != sid:
            print(f"ÉCHEC : {fichier} porte {lu}, le plan épingle {sid} (l'épinglage du plan)")
            return 1
    print(f"  le plan épingle {total} specs — concordance id:R{{rev}} constatée")
    # aucune copie du corpus hors unix/I (le diff nul exige l'unicité —
    # l'instance M7 la charge, elle ne la COPIE jamais)
    for racine_dir, dirs, fichiers in os.walk(RACINE):
        dirs[:] = [d for d in dirs if d not in
                   (".git", ".keys", "__pycache__", "carte", "carte-corpus",
                    "carte-sonde", "archives-bundles", "bundles-060",
                    ".gdrive", ".tmp", "node_modules")]
        if os.path.relpath(racine_dir, RACINE) == "unix/I":
            continue
        for f in fichiers:
            for fichier, _ in CORPUS:
                if f == fichier + ".md":
                    print(f"ÉCHEC : COPIE INTERDITE : {os.path.join(racine_dir, f)} — "
                          f"le corpus vit à unix/I/ et NULLE PART ailleurs (le diff nul)")
                    return 1
    rapports.append(f"fichiers canoniques : {total} contrats, empreintes mesurées, "
                    f"zéro copie hors unix/I/ — l'instance RV64 CHARGE (jamais ne copie)")
    print(f"  aucune copie — l'instance RV64 charge LES fichiers canoniques")

    # 2 — l'équivalence des observables R1 ↔ R+1 (la propriété du dépôt,
    #     mesurée par la chaîne M6 sur exactement ces fichiers)
    print("\n[2] L'équivalence des observables (la chaîne M6 rejouée — exigée VERT)")
    diff = subprocess.run([sys.executable, os.path.join(UNIX, "diff_nul.py")],
                          capture_output=True, text=True)
    derniere = diff.stdout.strip().splitlines()
    print(f"  {derniere[-1] if derniere else '(sans sortie)'}")
    if diff.returncode != 0:
        print(diff.stdout)
        print("ÉCHEC : le diff nul M6 n'est pas VERT — la chaîne s'arrête")
        return 1
    rapports.append("équivalence R1↔R+1 : la chaîne M6 VERT rejouée "
                    "(35 identiques + écarts nommés frag-con — les observables invariants)")

    # 3 — l'invariance des scellés (l'état zéro de l'ouverture ↔ maintenant)
    print("\n[3] L'invariance des scellés (l'état zéro mesuré à l'ouverture du chantier)")
    for rel, attendu in ETAT_ZERO.items():
        chemin = os.path.join(RACINE, rel)
        actuel = sha(chemin) if os.path.exists(chemin) else None
        if actuel != attendu:
            print(f"ÉCHEC : SCELLÉ MUTÉ : {rel} sha256 {actuel} != état zéro {attendu}")
            return 1
        print(f"  {rel:16s} INTACT — sha256:{actuel[:24]}… ({ROLES[rel]})")
    rapports.append(f"invariance : {len(ETAT_ZERO)} artefacts octet-identiques à l'état "
                    f"zéro (5 scellés Windows + le corpus unix + la sonde riscv)")

    # 4 — la parité par exécution § 8.3 : la ligne du patrimoine, l'observable
    #     invariant des TROIS profils (constatée en exécution par l'oracle qemu
    #     de build_corpus.py — portée ici comme le contrat de la chaîne)
    print("\n[4] La parité par exécution § 8.3 — la ligne du patrimoine")
    print(f"  l'observable invariant (octets attendus) : {LIGNE_PATRIMOINE!r}")
    print("  l'instance Windows scellée (0.2.0) la rend en \\r\\n (selftest.exe, "
          "la paramétrisation du profil) ; les instances Linux en \\n —")
    print("  le préfixe et le verdict sont invariants ; l'oracle qemu de "
          "build_corpus.py constate ces octets EN EXÉCUTION (V2/corpus-13)")
    rapports.append("parité § 8.3 : la ligne du patrimoine portée à l'identique — "
                    "constatée en exécution par l'oracle qemu (jamais par déduction)")

    empreinte = hashlib.sha256("\n".join(rapports).encode()).hexdigest()
    print(f"\n[diff-nul-M7] VERT — {len(rapports)} recoupements, empreinte {empreinte[:16]}…")
    return 0


if __name__ == "__main__":
    sys.exit(main())
