#!/usr/bin/env python3
"""etat_zero_m6b.py — État zéro du chantier M6-(b) : les empreintes des
artefacts scellés Windows AVANT le geste (la base d'invariance que
l'assertion finale recoupera — « les scellés ne bougent pas », D149-(3)),
plus les gardes vivantes : sceau-I (11 arbres), parse des couches I des
chaînes scellées m1/m2 (les arbres R1 doivent rester chargables — aucune
révision sur place), et l'état du vérificateur m1 (LECTURE SEULE).

NOTE D'INCIDENT (consignée au chantier) : la première version de ce script
lançait `python3 m1/build_m1.py` sans argument pour « constater le refus
anti-rollback » — le mode par défaut est la CONSTRUCTION, et la garde de
l'ère m1 échoue OUVERTE sur carte illisible (except ErreurCarte: pass —
la carte m1 scellée ne s'ouvre pas sous la phrase du jour, lignée de clés
réinitialisée depuis le scellage) : le build a donc TOURNÉ. selftest.exe
est resté OCTET-IDENTIQUE (chaîne déterministe, notation intacte —
sha256 8038585b… avant == après) ; la carte m1 avait été régénérée en
dev.2 (régression de balise dans l'arbre de travail) et RESTAURÉE
octet-pour-octet depuis git ( HEAD 018db94) — l'état incident écarté.
Le constat structurel né de l'incident (absent ≠ illisible : toutes les
gardes m1→m5 traitent « illisible » comme « première construction »)
est consigné au chantier M6-(b) ; la garde du jalon (build_corpus.py)
distingue les deux dès sa naissance.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

RACINE = "/home/z/my-project/triade"
SCELLES = [
    # (chemin, rôle) — les artefacts scellés du patrimoine Windows M0-M5
    ("m0/hello.exe", "hello.exe — scellé 0.1.0 (M0)"),
    ("m1/selftest.exe", "selftest.exe — scellé 0.2.0 (M1)"),
    ("m2/echo.exe", "echo.exe — scellé 0.3.0 (M2)"),
    ("m3/proxy.exe", "proxy.exe — scellé 0.4.0 (M3)"),
    ("m5/proxy.exe", "proxy.exe — scellé 0.6.0 (M5, finale)"),
]


def sha256(chemin: str) -> str:
    with open(chemin, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main() -> int:
    etat = {"scelles": {}, "arbre_I": {}}
    print("=== ÉTAT ZÉRO du chantier M6-(b) (avant tout geste) ===")
    for rel, role in SCELLES:
        chemin = os.path.join(RACINE, rel)
        if not os.path.exists(chemin):
            print(f"[!] absent (consigné tel quel) : {rel}")
            etat["scelles"][rel] = None
            continue
        h, taille = sha256(chemin), os.path.getsize(chemin)
        etat["scelles"][rel] = {"sha256": h, "octets": taille}
        print(f"[scellé] {rel:16s} {taille:7d} o  sha256:{h[:32]}…  ({role})")

    # Les arbres I du patrimoine — empreinte du manifeste vivant (modèle sceau-I)
    for arbre in ("m0", "m1", "m2"):
        base = os.path.join(RACINE, arbre, "I")
        fichiers = sorted(
            os.path.relpath(os.path.join(r, n), base).replace(os.sep, "/")
            for r, _, ns in os.walk(base) for n in ns)
        lignes = [f"arbre: {arbre}", f"fichiers: {len(fichiers)}"]
        for rel in fichiers:
            lignes.append(f"sha256:{sha256(os.path.join(base, rel))}  {rel}")
        texte = ("\n".join(lignes) + "\n").encode()
        etat["arbre_I"][arbre] = hashlib.sha256(texte).hexdigest()
        print(f"[arbre I] {arbre}/I : {len(fichiers)} fichiers, "
              f"empreinte manifeste {etat['arbre_I'][arbre][:24]}…")

    # Garde 1 : le sceau-I (les 11 arbres signés — doit être VERT au départ)
    r = subprocess.run([sys.executable, "v06/sceau_I.py", "verifier"],
                       cwd=RACINE, capture_output=True, text=True)
    etat["sceau_I_code"] = r.returncode
    etat["sceau_I_derniere"] = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
    print(f"[sceau-I] code {r.returncode} — {etat['sceau_I_derniere']}")

    # Garde 2 : les chaînes scellées chargent leurs specs R1 SANS modification
    # (preuve que le dépôt est dans l'état où les vérificateurs vivent)
    sys.path.insert(0, os.path.join(RACINE, "m1"))
    os.chdir(RACINE)
    import importlib
    b1 = importlib.import_module("build_m1")
    try:
        specs = b1.charger_couche_I(b1.blocs_phase(2))
        etat["m1_parse"] = f"OK ({len(specs)} specs R1 chargées, sid épinglés par la carte)"
        print(f"[m1] charger_couche_I : OK — {len(specs)} specs, "
              "révisions épinglées par le layout (R1)")
    except Exception as e:
        etat["m1_parse"] = f"ECHEC : {e}"
        print(f"[m1] charger_couche_I : ECHEC : {e}")

    # Garde 3 : l'état du vérificateur m1 (LECTURE SEULE — le mode construction
    # n'est JAMAIS lancé : l'incident de la première version le consigne). La
    # carte m1 scellée ne s'ouvre pas sous la phrase du jour (lignée réinitialisée
    # depuis le scellage) : le vérificateur rend son échec fail-closed nommé.
    r = subprocess.run([sys.executable, "m1/build_m1.py", "--verifier", "--volume", "reduit"],
                       cwd=RACINE, capture_output=True, text=True, timeout=300)
    sorties = r.stdout + r.stderr
    illisible = "carte illisible" in sorties
    etat["m1_verifieur"] = ("fail-closed : carte illisible (phrase de l'ère du scellage "
                            "requise — état préexistant, nommé au chantier)" if illisible
                           else f"code {r.returncode} : {sorties.strip().splitlines()[-1][:100]}")
    print(f"[m1] vérificateur : {etat['m1_verifieur']}")

    with open(os.path.join(RACINE, "scripts", "etat_zero_m6b.json"), "w") as f:
        json.dump(etat, f, indent=2, ensure_ascii=False)
    print("\n[état zéro] consigné : scripts/etat_zero_m6b.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
