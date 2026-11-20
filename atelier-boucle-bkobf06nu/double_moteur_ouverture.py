#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""double_moteur_ouverture.py — LE DOUBLE MOTEUR AU CHEMIN CHAUD DE
L'OUVERTURE DE SESSION (la vague 9, l'instruction bkobf06nu point 2, le
PLAN-BKOBF06NU H2 gelé).

L'OUVERTURE DE SESSION : ouvrir (loupe-01 — la cascade 02/04/05/06/07
INTERNE : la fenêtre lue, le cadre né, LE PANNEAU md5+sha256 SUR LE
FICHIER ENTIER — le condensé émulé du chemin chaud), l'état (les
compteurs du noyau), fermer. LES TÉMOINS : le témoin 196 609 o de la
campagne M4 (le canon D214 — LE FICHIER ENTIER condensé) et le témoin
384 o (le bord bas).

LE VOLUME sous QEMU-user (qemu-x86_64 1:10.0.13, l'extrait sans root) :
le lanceur C statique, L'IMAGE BÂTIE PAR LE VRAI HARNAIS (les octets ==
l'image Unicorn PAR CONSTRUCTION), UN RELEVÉ PAR OPÉRATION.

L'ÉCHANTILLON D'AUDIT sous Unicorn : le MÊME programme au harnais (TEL
QUEL, D185) — la comparaison octet pour octet des DEUX flux est l'audit
(divergence = 0 exigée sur le volume consigné).

LE COMPTEUR PAR BLOC : le qemu-user 1:10.0.13 de Debian est BÂTI SANS
CONFIG_PLUGIN (« qemu: unknown option 'plugin' » — l'écart NOMMÉ sur
pièces : le compteur plugin/bloc exigera le qemu à plugins du plan) ;
AU LABO le comptage par bloc vit au HARNais (hook d'instruction Unicorn
à l'échantillon : CHAQUE entrée de bloc comptée, la cascade INTERNE
comprise — loupe-05 au fichier entier : N absorptions de 64 o).

LA CLÉ DE MÉMO ÉTENDUE : sha256(bloc ‖ entrée ‖ contrat ‖ config
émulateur ‖ graine ‖ oracle ‖ LE CONDENSÉ DU FICHIER ENTIER) — tout ce
qui détermine le résultat (la règle D222 étendue à l'ouverture)."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import pathlib
import random
import sys
import tempfile
import time

import unicorn

REPO = pathlib.Path("/tmp/triade-gh")
sys.path.insert(0, str(REPO / "loupe"))
sys.path.insert(0, str(REPO / "atelier-cout-boucle-cq01qv1za"))
sys.path.insert(0, str(REPO / "atelier-m4-vljfs6pcj"))

import harnais_noyau as HN          # noqa: E402
from moteur_qemu import ReferenceUnicorn, VolumeQEMU  # noqa: E402

L = HN.L
ICI = REPO / "atelier-boucle-bkobf06nu"
QEMU = "/tmp/pkgs/qemu-user-ext/usr/bin/qemu-x86_64"


def temoin_196609() -> bytes:
    """LE TÉMOIN CANONIQUE 196 609 o de la campagne M4 (D214) — le PRNG
    déterministe de la campagne, la même graine."""
    rng = random.Random(20261112)
    return bytes(rng.randrange(256) for _ in range(196_609))


def ops_ouverture(fichiers: dict) -> list[tuple]:
    """LE PROGRAMME : l'ouverture de session de CHAQUE témoin — ouvrir
    (LA CASCADE INTERNE : le panneau AU FICHIER ENTIER), l'état, fermer."""
    ops = []
    for nom in fichiers:
        ops.append(("ouvrir", nom))
        ops.append(("etat",))
        ops.append(("fermer",))
    return ops


def main():
    rapport = []
    temoins = {"temoin-384.bin": HN.composer_temoins()["temoin-384.bin"],
               "temoin-196609.bin": temoin_196609()}
    ops = ops_ouverture(temoins)
    rapport.append(
        f"LE PROGRAMME : {len(ops)} opérations ({len(temoins)} témoins : "
        f"le 384 o au bord bas, LE 196 609 o AU FICHIER ENTIER — le "
        f"condensé du chemin chaud de l'ouverture)")

    # (a) L'ÉCHANTILLON UNICORN — les relevés + LE COMPTEUR PAR BLOC
    not01 = (REPO / "scripts" / "campagne_d204" / "unite-01-T" /
             "notation" / "loupe-01-ouvrir.asm")
    ref = ReferenceUnicorn(notation=not01, bid="i110001")  # loupe-01 chargé
    ref.declarer_temoins(temoins)
    compteurs: dict[str, int] = {}
    slots = {rva: bid for bid, (rva, slot) in L.SLOTS_LOUPE.items()}

    def hook(uc, adresse, taille, donnees):
        bid = slots.get(adresse)
        if bid:
            compteurs[bid] = compteurs.get(bid, 0) + 1

    ref.emul.uc.hook_add(unicorn.UC_HOOK_CODE, hook)
    t0 = time.monotonic()
    with contextlib.redirect_stdout(io.StringIO()):
        flux_ref = ref.executer(ops)
    t_unicorn = time.monotonic() - t0
    (ICI / "flux-ouverture-unicorn.jsonl").write_text(
        "\n".join(flux_ref) + "\n", encoding="utf-8")
    rapport.append(f"L'ÉCHANTILLON UNICORN : {len(flux_ref)} relevés en "
                   f"{t_unicorn:.2f} s — LES COMPTEURS PAR BLOC (le hook "
                   f"d'instruction, la cascade INTERNE comprise) :")
    for bid in sorted(compteurs):
        rapport.append(f"    {bid:10s} : {compteurs[bid]:7d} entrées")
    (ICI / "compteurs-blocs.json").write_text(json.dumps(
        {"compteurs": compteurs,
         "ecart_qemu_plugin": "le qemu-user 1:10.0.13 de Debian est bâti "
         "SANS CONFIG_PLUGIN — le compteur plugin/bloc exigera le qemu à "
         "plugins du plan (l'écart nommé sur pièces)",
         "temoins": {n: len(c) for n, c in temoins.items()},
         "note": "hook d'instruction Unicorn : CHAQUE entrée de bloc, la "
                 "cascade interne comprise (loupe-05 : le fichier entier "
                 "absorbé par blocs de 64 o)"},
        indent=1, ensure_ascii=False), encoding="utf-8")

    # (b) LE VOLUME QEMU — le lanceur au VRAI qemu-x86_64
    bac = pathlib.Path(tempfile.mkdtemp(prefix="ouv-qemu-"))
    vol = VolumeQEMU(bac / "qemu", qemu=QEMU)
    vol.construire_image(notation=not01, bid="i110001")
    t0 = time.monotonic()
    with contextlib.redirect_stdout(io.StringIO()):
        flux_qemu = vol.executer(ops, temoins)
    t_qemu = time.monotonic() - t0
    (ICI / "flux-ouverture-qemu.jsonl").write_text(
        "\n".join(flux_qemu) + "\n", encoding="utf-8")
    rapport.append(f"LE VOLUME QEMU (le vrai qemu-x86_64 1:10.0.13) : "
                   f"{len(flux_qemu)} relevés en {t_qemu:.2f} s")

    # (c) L'AUDIT : la comparaison octet pour octet des deux flux
    ecart = 0
    for i, (a, b) in enumerate(zip(flux_ref, flux_qemu)):
        if a != b:
            ecart += 1
            if ecart <= 3:
                rapport.append(f"  DIVERGENCE ligne {i} : {a[:90]} ≠ "
                               f"{b[:90]}")
    if len(flux_ref) != len(flux_qemu):
        rapport.append(f"  DIVERGENCE : {len(flux_ref)} lignes unicorn "
                       f"contre {len(flux_qemu)} qemu")
        ecart += 1
    verdict = ("DIVERGENCE=0 — les deux moteurs s'accordent octet pour "
               "octet" if ecart == 0 else f"{ecart} ÉCART(S) — BLOQUANT")
    rapport.append(f"L'AUDIT : {verdict}")

    # (d) LA CLÉ DE MÉMO ÉTENDUE — le condensé du FICHIER ENTIER au cœur
    for nom, contenu in temoins.items():
        cle = hashlib.sha256(
            b"loupe-01" + contenu +
            hashlib.sha256(contenu).digest() +
            b"EmulationCampagne/x86-64-win11-pe" +
            b"grande-20261120" + b"oracle-panel-hashlib").hexdigest()
        rapport.append(f"LA CLÉ DE MÉMO ÉTENDUE ({nom}, {len(contenu)} o) : "
                       f"sha256 = {cle[:40]}… — le bloc ‖ l'entrée ‖ LE "
                       f"CONDENSÉ DU FICHIER ENTIER ‖ la config ‖ la graine "
                       f"‖ l'oracle (tout ce qui détermine le résultat)")

    (ICI / "rapport-double-moteur-ouverture.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print("\n".join(rapport))
    return 0 if ecart == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
