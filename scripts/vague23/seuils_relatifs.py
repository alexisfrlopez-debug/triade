#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LES SEUILS RELATIFS (W23PROP 3–4, D273).

Deux cibles absolues ne discriminaient plus :
  (a) AES-GCM : la cible devient ≤ 1,05 × OpenSSL EVP au même volume ; le référentiel EVP est
      mesuré ici (machine virtuelle, n = 20, IQR) ; la spécialisation VAES reste un geste
      machine réelle et son absence est un REFUS NOMMÉ (ABSENT-MESURE), jamais un gain ;
  (b) ajouter : la cible relative au bras C COMPILÉ n'est pas calculable — le dépôt ne publie
      pas de coût « ajouter » pour ce bras. On ne l'invente pas : la cible retenue est
      RELATIVE AU BUDGET D'ÉDITION ADOPTÉ (ratio ajouter/éditer ≤ 3,0), et l'absence du coût
      du bras C pour l'ajouter est nommée comme la mesure à faire.

Usage : python3 scripts/vague23/seuils_relatifs.py
"""
import json, pathlib, statistics, time

R = pathlib.Path(__file__).resolve().parents[2]
SORTIE = R / "atelier-w23-seuils"
N = 20
# la TABLE CANONIQUE des budgets adoptés (manuscrit, § budgets) : éditer 674, ajouter 2 200
BUDGET_EDITER = 674
BUDGET_AJOUTER = 2200
CIBLE_RATIO_AJOUTER = 3.0
CIBLE_AES = 1.05


def aes_reference():
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    cle, nonce, clair = b"\x00" * 32, b"\x00" * 12, b"\x41" * 4096
    a = AESGCM(cle)
    for _ in range(100):
        a.encrypt(nonce, clair, None)
    m = []
    for _ in range(N):
        t = time.perf_counter_ns(); a.encrypt(nonce, clair, None); m.append(time.perf_counter_ns() - t)
    med = statistics.median(m)
    q = statistics.quantiles(m, n=4)
    return {"n": N, "mediane_ns_4kio": med, "iqr_ns": q[2] - q[0],
            "cycles_par_octet_estimes": (med * 2.8) / 4096}  # 2,8 GHz consignés


def main():
    SORTIE.mkdir(exist_ok=True)
    evp = aes_reference()
    ratio_ajouter = BUDGET_AJOUTER / BUDGET_EDITER
    doc = {
        "aes_gcm": {"cible": f"≤ {CIBLE_AES:.2f} × OpenSSL EVP au même volume (4 Kio)",
                    "reference_evp": evp, "notre_cote": "ABSENT-MESURE",
                    "refus": "COULOIR-NON-MESURE — aucun code VAES écrit dans ce bac ; "
                             "aucun gain revendiqué"},
        "ajouter": {"budget_editer": BUDGET_EDITER, "budget_ajouter": BUDGET_AJOUTER,
                    "ratio_actuel": round(ratio_ajouter, 3), "cible_ratio": CIBLE_RATIO_AJOUTER,
                    "cible": f"ratio ajouter/éditer ≤ {CIBLE_RATIO_AJOUTER}",
                    "ecart": round(ratio_ajouter - CIBLE_RATIO_AJOUTER, 3),
                    "note": "la cible relative au BRAS C n'est pas calculable : le coût "
                            "« ajouter » du bras compilé n'est pas publié — c'est la mesure "
                            "à faire, nommée plutôt qu'inventée"},
    }
    (SORTIE / "seuils.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[aes] EVP 4 Kio : {evp['mediane_ns_4kio']:.0f} ns (IQR {evp['iqr_ns']:.0f}) ≈ "
          f"{evp['cycles_par_octet_estimes']:.3f} c/o · notre côté ABSENT-MESURE")
    print(f"[ajouter] ratio actuel {ratio_ajouter:.3f} vs cible ≤ {CIBLE_RATIO_AJOUTER} → "
          f"{'TENUE' if ratio_ajouter <= CIBLE_RATIO_AJOUTER else 'MANQUÉE'} (écart {ratio_ajouter - CIBLE_RATIO_AJOUTER:+.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
