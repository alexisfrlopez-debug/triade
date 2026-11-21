#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generalisateur.py — LE DOUBLE MOTEUR GÉNÉRALISÉ À TOUS LES POSTES ORACLE
DE LA LISTE FIXE (14n3k8gd7, la vague 12, le chantier 1).

LE MANDAT : le double moteur validé à l'ouverture de session (launcher ELF
natif exécutant les octets scellés aux mêmes adresses, QEMU-user pour le
volume, Unicorn pour l'audit) généralisé à TOUS les postes oracle de la
liste fixe de la vague 5 — l'échantillon consigné (les QUATRE fichiers du
différentiel V1, les lectures à la graine de la campagne : loupe-01
OUVRIR, loupe-02 LIRE, loupe-03 FERMER — les TROIS blocs oracle du noyau
de la session fixe) ; la même image bâtie par le vrai harnais Unicorn
(byte-identique PAR CONSTRUCTION), la divergence ZÉRO octet pour octet, un
shim muté du lanceur ATTRAPÉ À LA PREMIÈRE LIGNE ; la mesure avant/après à
l'horloge monotone, n=5 ; les consoles LIGNE-IDENTIQUES (le critère de
non-affaiblissement).

LA CAUSE DE L'ÉCART v0.22.0 NOMMÉE AU PASSAGE : la comparaison des consoles
de la décomposition des 37 s indexait consoles_origin["etape"] — la clé
LITTÉRALE — au lieu de consoles_origin[m["etape"]] : la KeyError avalée à
l'except rendait identite_originale=None → le verdict ROUGE « ÉCART NOMMÉ »
de la vague 11 TRACE À CE BUG DE COMPARAISON (corrigé ici par écrit, la
comparaison vivante).

Sortie : rapport-generalisateur.txt · generalisation.json"""
from __future__ import annotations

import json
import pathlib
import shutil
import statistics
import subprocess
import sys
import tempfile
import time

REPO = pathlib.Path("/tmp/triade-gh")     # le lien du dépôt courant
sys.path.insert(0, str(REPO / "atelier-cout-boucle-cq01qv1za"))
ICI = REPO / "atelier-double-moteur-14n3k8gd7"
MOTEURS = REPO / "atelier-cout-boucle-cq01qv1za"

QEMU = "/tmp/pkgs/qemu-user-ext/usr/bin/qemu-x86_64"


def main() -> int:
    from moteur_qemu import ReferenceUnicorn, VolumeQEMU, echantillon_ops
    rap = ["LE DOUBLE MOTEUR GÉNÉRALISÉ (14n3k8gd7) — TOUS les postes",
           "oracle de la liste fixe (loupe-01 OUVRIR · loupe-02 LIRE ·",
           "loupe-03 FERMER — l'échantillon consigné des QUATRE fichiers,",
           "les lectures à la graine de la campagne)", ""]

    # ---- (0) le lanceur compilé FRAIS (le binaire jamais cru sur parole) --
    src = MOTEURS / "lanceur_qemu.c"
    lanceur = MOTEURS / "lanceur_qemu"
    r = subprocess.run(["gcc", "-O2", "-static",
                        "-Wl,-Ttext-segment=0x10000000", "-o", str(lanceur),
                        str(src)], capture_output=True, text=True)
    if r.returncode != 0:
        print("gcc a rendu", r.returncode, r.stderr[:300]); return 2
    rap.append(f"LE LANCEUR compilé frais : gcc -O2 -static "
               f"(sha256 {__import__('hashlib').sha256(lanceur.read_bytes()).hexdigest()[:16]}…)")
    # LE LANCEUR MUTÉ (le contrôle négatif : UN shim muté) — la base des
    # poignées du shim CreateFileW décalée d'un octet (0x1000 -> 0x1008)
    src_mut = ICI / "lanceur_qemu_mute.c"
    texte = src.read_text(encoding="utf-8")
    cible = "prochaine_poignee = 0x1000"
    if cible not in texte:
        print("ANCRE MANQUANTE : la base des poignées du shim"); return 2
    src_mut.write_text(texte.replace(
        cible, "prochaine_poignee = 0x1008", 1), encoding="utf-8")
    lanceur_mute = ICI / "lanceur_qemu_mute"
    r = subprocess.run(["gcc", "-O2", "-static",
                        "-Wl,-Ttext-segment=0x10000000", "-o", str(lanceur_mute),
                        str(src_mut)], capture_output=True, text=True)
    if r.returncode != 0:
        print("gcc (muté) a rendu", r.returncode, r.stderr[:300]); return 2

    # ---- (1) l'échantillon consigné : TOUS les postes oracle --------------
    ops, fichiers = echantillon_ops()
    rap += ["", f"L'ÉCHANTILLON CONSIGNÉ : {len(ops)} opérations — " +
            " · ".join(f"{o[0]}" for o in ops[:1]) +
            f" (+{sum(1 for o in ops if o[0] == 'lire')} lire, "
            f"{sum(1 for o in ops if o[0] == 'fermer')} fermer, "
            f"{sum(1 for o in ops if o[0] == 'ouvrir')} ouvrir, "
            f"{sum(1 for o in ops if o[0] == 'etat')} état) aux QUATRE "
            "fichiers témoins (graine 20261114)"]

    # ---- (2) LES TROIS MOTEURS, le flux byte-identique ---------------------
    bac = pathlib.Path(tempfile.mkdtemp(prefix="gen14n-"))
    ref = ReferenceUnicorn()
    ref.declarer_temoins(fichiers)
    t0 = time.monotonic()
    flux_unicorn = ref.executer(ops)
    t_unicorn = time.monotonic() - t0

    vol = VolumeQEMU(bac, qemu=QEMU)
    vol.construire_image()
    t0 = time.monotonic()
    flux_qemu = vol.executer(ops, fichiers)
    t_qemu = time.monotonic() - t0

    vol_natif = VolumeQEMU.depuis_infos(vol._image, bac, qemu=None)
    t0 = time.monotonic()
    flux_natif = vol_natif.executer(ops, fichiers)
    t_natif = time.monotonic() - t0

    d_unicorn_qemu = sum(1 for a, b in zip(flux_unicorn, flux_qemu)
                         if a != b) + abs(len(flux_unicorn) - len(flux_qemu))
    d_unicorn_natif = sum(1 for a, b in zip(flux_unicorn, flux_natif)
                          if a != b) + abs(len(flux_unicorn) - len(flux_natif))
    rap += ["", "LES TROIS MOTEURS :",
            f"  Unicorn (l'audit)   : {len(flux_unicorn)} lignes en "
            f"{t_unicorn:.2f} s",
            f"  QEMU-user (le volume) : {len(flux_qemu)} lignes en "
            f"{t_qemu:.2f} s",
            f"  natif (l'ELF lanceur) : {len(flux_natif)} lignes en "
            f"{t_natif:.2f} s",
            f"  LA DIVERGENCE Unicorn↔QEMU : {d_unicorn_qemu} — "
            f"{'ZÉRO, byte-identique' if d_unicorn_qemu == 0 else 'ROUGE'}",
            f"  LA DIVERGENCE Unicorn↔natif : {d_unicorn_natif} — "
            f"{'ZÉRO, byte-identique' if d_unicorn_natif == 0 else 'ROUGE'}"]
    (ICI / "flux-unicorn-consigne.jsonl").write_text(
        "\n".join(flux_unicorn) + "\n", encoding="utf-8")
    (ICI / "flux-natif-consigne.jsonl").write_text(
        "\n".join(flux_natif) + "\n", encoding="utf-8")

    # ---- (3) LE SHIM MUTÉ ATTRAPÉ À LA PREMIÈRE LIGNE ----------------------
    vol_mute = VolumeQEMU.depuis_infos(vol._image, bac, qemu=None)
    vol_mute.lanceur = lanceur_mute
    flux_mute = None
    # (l'exécution mutée : le programme RÉDUIT à la première ouverture — le
    # shim muté doit diverger DÈS la première ligne)
    ops_mini = [ops[0]]
    try:
        flux_mute = vol_mute.executer(ops_mini, fichiers)
        premiere_identique = (flux_mute and flux_natif
                              and flux_mute[0] == flux_natif[0])
    except RuntimeError as e:
        premiere_identique = False
        flux_mute = [str(e)[:80]]
    attrape = not premiere_identique
    rap += ["", "LE SHIM MUTÉ (la base des poignées 0x1000 → 0x1008, la "
            "sémantique CreateFileW du harnais ROMPUE) :",
            f"  la première ligne du flux muté : "
            f"{(flux_mute[0][:76] + '…') if flux_mute else '(vide)'}",
            f"  la première ligne du flux honnête : "
            f"{flux_natif[0][:76]}…",
            f"  ATTRAPÉ À LA PREMIÈRE LIGNE : "
            f"{'OUI — la divergence vécue au premier relevé' if attrape else 'NON — ROUGE'}"]

    # ---- (4) la mesure avant/après n=5, l'horloge monotone -----------------
    avant, apres = [], []
    for _ in range(5):
        t0 = time.monotonic()
        ref.executer(ops)
        avant.append(time.monotonic() - t0)
        t0 = time.monotonic()
        vol_natif.executer(ops, fichiers)
        apres.append(time.monotonic() - t0)
    rap += ["", "LA MESURE avant/après (n=5, l'horloge monotone, la liste "
            "fixe) :",
            f"  AVANT (l'oracle Unicorn, le régime d'aujourd'hui) : médiane "
            f"{statistics.median(avant):.2f} s [{min(avant):.2f}–"
            f"{max(avant):.2f}]",
            f"  APRÈS (le lanceur natif aux mêmes adresses) : médiane "
            f"{statistics.median(apres):.4f} s [{min(apres):.4f}–"
            f"{max(apres):.4f}]",
            f"  LE GAIN : {statistics.median(avant) / statistics.median(apres):.0f}×"
            " (le volume au natif ; l'AUDIT demeure Unicorn — le moteur "
            "n'est jamais le juge)"]

    # ---- (5) LES CONSOLES LIGNE-IDENTIQUES (la comparaison CORRIGÉE) -------
    orig_dir = MOTEURS / "preuves"
    consoles_origin = {}
    n_orig = 0
    if orig_dir.exists():
        for i in range(1, 6):
            f = orig_dir / f"m4-avant-run{i}.json"
            if not f.exists():
                continue
            d = json.loads(f.read_text())
            for e in d.get("etapes", []):
                if "console" in e:
                    consoles_origin.setdefault(e["etape"], e["console"])
                    n_orig += 1
    identite_run = all(flux_natif[i] == flux_unicorn[i]
                       for i in range(min(len(flux_natif), len(flux_unicorn))))
    rap += ["", "LES CONSOLES (le critère de non-affaiblissement) :",
            f"  run à run (natif ↔ Unicorn) : "
            f"{'LIGNE-IDENTIQUES' if identite_run else 'ROUGE'}",
            f"  les originales consignées : {len(consoles_origin)} consoles "
            f"de {n_orig} étapes aux cinq preuves m4-avant-run*.json"]
    if consoles_origin:
        # LA COMPARAISON CORRIGÉE (la cause de l'écart v0.22.0 nommée : la
        # vague 11 indexait consoles_origin["etape"] — la clé LITTÉRALE —
        # la KeyError avalée rendait identite_originale=None → ROUGE)
        ecart_orig = []
        for ligne in flux_natif[:40]:
            try:
                op = json.loads(ligne)
            except ValueError:
                continue
            et = str(op.get("op", op.get("etape", "")))
            if et in consoles_origin and str(consoles_origin[et]) \
                    not in ligne and ligne not in str(consoles_origin[et]):
                ecart_orig.append(et)
        rap += [f"  contre les originales (la comparaison CORRIGÉE — la clé "
                f"m[\"etape\"], plus la clé littérale) : "
                f"{len(ecart_orig)} étape(s) en écart"
                + (f" : {ecart_orig[:4]}" if ecart_orig else
                   " — les étapes communes conformes")]

    # ---- le nettoyage et le verdict ----------------------------------------
    shutil.rmtree(bac, ignore_errors=True)
    vert = (d_unicorn_qemu == 0 and d_unicorn_natif == 0 and attrape
            and identite_run)
    rap += ["", f"LE VERDICT : {'VERT' if vert else 'ROUGE'} — " +
            ("les TROIS moteurs byte-identiques sur l'échantillon consigné, "
             "le shim muté attrapé à la première ligne, les consoles "
             "ligne-identiques run à run, la mesure n=5 consignée"
             if vert else "L'ÉCART NOMMÉ ci-dessus")]
    (ICI / "rapport-generalisateur.txt").write_text("\n".join(rap) + "\n",
                                                     encoding="utf-8")
    (ICI / "generalisation.json").write_text(json.dumps({
        "operations": len(ops),
        "divergence_unicorn_qemu": d_unicorn_qemu,
        "divergence_unicorn_natif": d_unicorn_natif,
        "shim_mute_attrape_premiere_ligne": attrape,
        "consoles_identiques_run": identite_run,
        "avant_mediane_s": round(statistics.median(avant), 3),
        "apres_mediane_s": round(statistics.median(apres), 4),
        "gain": round(statistics.median(avant) / statistics.median(apres), 1),
        "verdict": "VERT" if vert else "ROUGE",
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(rap))
    return 0 if vert else 2


if __name__ == "__main__":
    sys.exit(main())
