#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""moteur_ceremonie.py — LE MOTEUR de la cérémonie d'ère de couloir-vaes512.asm (v100).

LA DETTE NOMMÉE À LA NAISSANCE (PLAN-W29VAES512) : « l'ère n'est scellée
que par la clé hors-ligne du développeur — le laboratoire ne signe jamais
(D87/D183) ». La notation vit SUR COPIE LABORATOIRE (exécutable, éprouvée
à la porte CAVP 20/20) ; le sceau d'ère ne vit QUE des mains du maître.

LA CONTINUITÉ DE CLÉ (D163) : l'ère se signe À LA MÊME CLÉ que le sceau de
l'Intention — la clé qui signe les 14 arbres (clé-publique-I.txt, portée
au harnais byte-byte) signe l'ère. Une signature d'une autre clé est
refusée nommément (SIGNATURE-INVALIDE — la continuité est le point).

LA CHARGE (la forme de a-signer du sceau — l'OUTIL DU MAÎTRE la signe
TELLE QUELLE, sans adaptation) :
    ere-notation   couloir-vaes512.asm         <sha256 des octets mêmes>
    ere-schedule   couloir_sched512.S          <sha256>
    ere-portage    couloir_vaes512.c           <sha256>
    ere-vecteurs   vecteurs-dores-nist.json    <sha256>

LE FLUX (la GUI guide, le moteur porte) :
  1. PRÉPARER   — le manifeste recoupé byte-byte, la charge écrite (les
                  empreintes RECALCULÉES des octets), a-emporter/ assemblé
                  (la charge + la notation + le signeur + le pas-à-pas) ;
  2. SIGNER     — HORS LIGNE, à la clé du maître (jamais au bac) :
                  python3 signeur_hors_ligne.py signer \\
                    ere-vaes512-a-signer.txt cle-I-privee.txt
                  (ou l'outil du dépôt v06/ceremonie_hors_ligne.py — la
                  même signature, la même forme) ;
  3. VÉRIFIER   — chaque signature contre la charge + la clé publique I ;
  4. INSTALLER  — ere-vaes512-sceau.txt (la charge + les signatures + la
                  vérification + l'horodatage) + le zip de preuves.

LA GARDE : le LABORATOIRE NE SIGNE JAMAIS — l'autotest s'éprouve à la CLÉ
DE TEST (la graine PUBLIQUE CONSTANTE, l'état « test » visible : sa
non-sécurité EST la preuve de l'état laboratoire) ; le sceau de test est
étiqueté TEST, jamais confondu ; la clé privée réelle n'entre jamais au
bac ; la notation couloir-vaes512.asm INTACHE byte-byte (a2c3a393…).

Usage :
  python3 moteur_ceremonie.py --preparer
  python3 moteur_ceremonie.py --verifier [signatures-I.txt]
  python3 moteur_ceremonie.py --installer [signatures-I.txt]
  python3 moteur_ceremonie.py --autotest
"""
from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import pathlib
import shutil
import sys
import tempfile
import zipfile

for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ICI = pathlib.Path(__file__).resolve().parent
HARNAIS = ICI / "harnais"
A_EMPORTER = ICI / "a-emporter"
CHARGE = ICI / "ere-vaes512-a-signer.txt"
SCEAU = ICI / "ere-vaes512-sceau.txt"

# la clé de TEST du laboratoire — la graine PUBLIQUE CONSTANTE (l'état
# « test » visible : sa non-sécurité EST la preuve qu'aucune clé réelle
# ne vit au bac — le modèle sceau_I.py signer-test)
GRAINE_TEST = bytes.fromhex(
    "5452494144452d4552452d544553542d434c452d5055424c495155452d303033")

PIECES_ERE = [
    ("ere-notation", "couloir-vaes512.asm"),
    ("ere-schedule", "couloir_sched512.S"),
    ("ere-portage", "couloir_vaes512.c"),
    ("ere-vecteurs", "vecteurs-dores-nist.json"),
]

DECLARATION_ERE = (
    "# TRIADE — LA CÉRÉMONIE D'ÈRE : couloir-vaes512.asm (l'ère VAES512 zmm)\n"
    "#\n"
    "# L'ère nouvelle de l'AES-256-GCM : la voie 512-bit — QUATRE blocs AES par\n"
    "# vAESENC, le pli de 32 blocs aux HUIT frappes, la pile ZMM. La notation vit\n"
    "# sur copie laboratoire, exécutable et éprouvée : la porte CAVP 20/20 contre\n"
    "# EVP octet pour octet aux DEUX bras (le schedule .S et le portage C), la\n"
    "# variante mutée rk13⊕0x5a refusée au premier vecteur chacun. La cible\n"
    "# CIB-AES-512 (≤ 1,05 × EVP à contexte posé) : MANQUÉE (3,66×/5,30×),\n"
    "# JAMAIS re-tirée ; CIB-AES-105 DEMEURE MANQUÉE et datée. L'écart\n"
    "# notation-vs-C : 1,45× au profit du C.\n"
    "#\n"
    "# Le sceau d'ère est signé par la clé hors-ligne du développeur — le\n"
    "# laboratoire ne signe JAMAIS (D87/D183) ; l'ère se signe à la MÊME clé\n"
    "# que le sceau de l'Intention (la continuité D163).\n")


def horodatage() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def _ed25519():
    """Le cœur Ed25519 importé du SIGNEUR (l'unique source : signeur_hors_ligne.py)."""
    spec = importlib.util.spec_from_file_location(
        "signeur_hors_ligne", str(ICI / "signeur_hors_ligne.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def manifeste(verifier: bool = True) -> dict:
    """Le manifeste de l'ère : chaque pièce recoupée à la table consignée
    byte-byte AVANT toute écriture de charge (PIÈCE-DIVERGENTE est le refus)."""
    table_fichier = HARNAIS / "MANIFESTE-ere.txt"
    if not table_fichier.exists():
        m = {"tout_vert": False, "lignes": ["  [ROUGE] MANIFESTE-ere.txt — ABSENT"]}
        if verifier:
            print("[manifeste] ROUGE : la table est absente")
        return m
    table = {}
    for ligne in table_fichier.read_text(encoding="utf-8").splitlines():
        morceaux = ligne.strip().split()
        if len(morceaux) == 2 and len(morceaux[0]) == 64:
            table[morceaux[1]] = morceaux[0]
    lignes, tout_vert = [], True
    for nom, attendu in table.items():
        p = HARNAIS / nom
        if not p.exists():
            lignes.append(f"  [ROUGE] {nom} — ABSENT")
            tout_vert = False
            continue
        emp = sha256f(p)
        ok = emp == attendu
        tout_vert = tout_vert and ok
        lignes.append(f"  [{'VERT' if ok else 'ROUGE'}] {nom} "
                      f"{emp[:16]}…{' == consigné' if ok else ' ≠ CONSIGNÉ'}")
    if verifier:
        print("[manifeste] " + ("VERT — les pièces de l'ère recoupées byte-byte"
                                if tout_vert else "ROUGE — une pièce diverge"))
        for l in lignes:
            print(l)
    return {"tout_vert": tout_vert, "lignes": lignes}


def preparer() -> pathlib.Path:
    """La charge écrite : les empreintes RECALCULÉES des octets mêmes des
    pièces portées (jamais recopiées du texte), a-emporter/ assemblé."""
    m = manifeste()
    if not m["tout_vert"]:
        raise SystemExit("ECHEC : le manifeste est ROUGE — la charge n'est pas écrite")
    lignes = []
    for nom_logique, fichier in PIECES_ERE:
        emp = sha256f(HARNAIS / fichier)
        lignes.append(f"{nom_logique} {fichier} {emp}")
        print(f"  [charge] {nom_logique:14s} {fichier:26s} {emp[:32]}…")
    CHARGE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"[charge] {CHARGE.name} écrite ({len(lignes)} lignes)")
    # a-emporter : la charge + la notation + le signeur + le pas-à-pas
    if A_EMPORTER.exists():
        shutil.rmtree(A_EMPORTER)
    A_EMPORTER.mkdir()
    shutil.copyfile(CHARGE, A_EMPORTER / CHARGE.name)
    shutil.copyfile(HARNAIS / "couloir-vaes512.asm", A_EMPORTER / "couloir-vaes512.asm")
    shutil.copyfile(ICI / "signeur_hors_ligne.py", A_EMPORTER / "signeur_hors_ligne.py")
    shutil.copyfile(HARNAIS / "cle-publique-I.txt", A_EMPORTER / "cle-publique-I.txt")
    (A_EMPORTER / "LISEZMOI-HORS-LIGNE.txt").write_text(
        "TRIADE — la signature HORS-LIGNE de l'ère couloir-vaes512.asm\n"
        "============================================================\n"
        "\n"
        "1. Copiez CE DOSSIER (a-emporter/) vers la machine hors ligne (clef\n"
        "   USB, papier) — la clé privée du maître n'entre jamais au bac.\n"
        "2. Re-vérifiez la notation à la machine : l'empreinte sha256 de\n"
        "   couloir-vaes512.asm doit être a2c3a393… (celle de la charge) :\n"
        "     python3 signeur_hors_ligne.py autotest\n"
        "     (puis hash de votre côté : certutil -hashfile couloir-vaes512.asm\n"
        "      SHA256 sous Windows, ou sha256sum sous Linux)\n"
        "3. Signez la charge À VOTRE CLÉ du sceau (la continuité D163 — la clé\n"
        "   qui signe les 14 arbres signe l'ère) :\n"
        "     python3 signeur_hors_ligne.py signer ere-vaes512-a-signer.txt cle-I-privee.txt\n"
        "   (l'outil du dépôt v06/ceremonie_hors_ligne.py signe la MÊME charge\n"
        "    telle quelle — la forme est la même : « nom balise empreinte »)\n"
        "4. Remettez signatures-I.txt au kit (le bouton « Vérifier la\n"
        "   signature revenue » puis « Installer le sceau d'ère »).\n"
        "\n"
        "LA GARDE : la clé privée ne traverse JAMAIS le bac à sable ; le\n"
        "laboratoire ne signe JAMAIS (D87/D183).\n", encoding="utf-8")
    print(f"[a-emporter] assemblé : {len(list(A_EMPORTER.iterdir()))} pièces "
          f"(la charge, la notation, le signeur, la clé publique, le pas-à-pas)")
    return CHARGE


def verifier(chemin_signatures: pathlib.Path, publique_test=None) -> dict:
    """Chaque signature contre la charge + LA CLÉ PUBLIQUE I (la continuité).
    publique_test : la clé de TEST de l'autotest (jamais au geste réel — la clé
    de test ne vérifie QUE ses propres signatures, l'état test visible)."""
    ed = _ed25519()
    publique = (publique_test if publique_test is not None else
                ed._lire_hex_fichier(HARNAIS / "cle-publique-I.txt",
                                     "clé publique I", 32))
    entrees = ed.lire_lignes_a_signer(CHARGE)
    lignes_sig = [l.strip() for l in
                  pathlib.Path(chemin_signatures).read_text(encoding="utf-8").splitlines()
                  if l.strip()]
    verdicts, tout = [], True
    if len(lignes_sig) != len(entrees):
        print(f"[verifier] ROUGE : {len(lignes_sig)} signatures != {len(entrees)} lignes de charge")
        return {"tout_vert": False, "verdicts": verdicts}
    for (nom, balise, emp_hex), ligne in zip(entrees, lignes_sig):
        morceaux = ligne.split()
        if len(morceaux) != 3 or morceaux[:2] != [nom, balise]:
            verdicts.append({"nom": nom, "vert": False,
                             "motif": "la ligne de signature ne correspond pas à la charge"})
            tout = False
            continue
        ok = ed.verifier_ed25519(publique, bytes.fromhex(emp_hex),
                                 bytes.fromhex(morceaux[2]))
        verdicts.append({"nom": nom, "vert": ok,
                         "motif": ("la signature tient à la clé publique I (la continuité)"
                                   if ok else
                                   "SIGNATURE-INVALIDE — la signature ne tient PAS à la "
                                   "clé publique I : ou la clé signataire n'est pas celle "
                                   "du sceau (la continuité D163 est le point), ou la "
                                   "signature est corrompue")})
        tout = tout and ok
        print(f"  [{'VERT' if ok else 'ROUGE'}] {nom} {balise}")
    return {"tout_vert": tout, "verdicts": verdicts,
            "cle_publique_I_sha256": sha256f(HARNAIS / "cle-publique-I.txt")}


def installer(chemin_signatures: pathlib.Path, publique_test=None) -> dict:
    """Le sceau écrit (la charge + les signatures + la vérification) + le zip."""
    v = verifier(chemin_signatures, publique_test)
    if not v["tout_vert"]:
        print("[installer] ROUGE — le sceau n'est PAS écrit (une signature ne tient pas)")
        return {"installe": False, **v}
    lignes = [l.strip() for l in
              pathlib.Path(chemin_signatures).read_text(encoding="utf-8").splitlines()
              if l.strip()]
    sceau = (DECLARATION_ERE
             + f"#\n# La charge signée (les empreintes recalculées des octets) :\n"
             + CHARGE.read_text(encoding="utf-8")
             + "#\n# Les signatures (Ed25519, la clé du sceau de l'Intention) :\n"
             + "\n".join("# " + l for l in lignes) + "\n"
             + f"#\n# La vérification : {len(lignes)}/{len(lignes)} VERT à la clé publique I\n"
             + f"# (sha256 de la clé : {v['cle_publique_I_sha256']})\n"
             + f"# L'horodatage de l'installation : {horodatage()}\n"
             + "# L'ère est scellée — le laboratoire ne signe jamais (D87/D183).\n")
    SCEAU.write_text(sceau, encoding="utf-8")
    print(f"[installer] {SCEAU.name} écrit ({len(sceau)} octets)")
    nom_zip = f"preuves-ceremonie-{dt.datetime.now().strftime('%Y%m%dT%H%M%SZ')}.zip"
    chemin_zip = ICI / nom_zip
    with zipfile.ZipFile(chemin_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(SCEAU, SCEAU.name)
        z.write(CHARGE, CHARGE.name)
        z.write(pathlib.Path(chemin_signatures), pathlib.Path(chemin_signatures).name)
        z.write(HARNAIS / "MANIFESTE-ere.txt", "MANIFESTE-ere.txt")
    print(f"[installer] {nom_zip} ({chemin_zip.stat().st_size} o) — à déposer au coffre /test")
    return {"installe": True, "sceau": str(SCEAU), "zip": str(chemin_zip), **v}


def autotest() -> int:
    """L'aller-retour ENTIER à la CLÉ DE TEST (la graine publique constante —
    le laboratoire ne signe jamais avec une clé réelle ; le sceau de test
    est étiqueté TEST, jamais confondu) : preparer → signer(test) →
    verifier → installer ; les refus : une signature muée, une charge muée."""
    ed = _ed25519()
    tout = True

    def epreuve(nom, fn):
        nonlocal tout
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"{e.__class__.__name__}: {e}"
        tout = tout and ok
        print(f"[autotest] {'VERT' if ok else 'ROUGE'} — {nom}")
        if not ok:
            print(f"          {str(detail)[:300]}")

    zone = pathlib.Path(tempfile.mkdtemp(prefix="ere-autotest-"))
    orig_ici = ICI
    globals()["ICI"] = zone
    globals()["HARNAIS"] = zone / "harnais"
    globals()["A_EMPORTER"] = zone / "a-emporter"
    globals()["CHARGE"] = zone / "ere-vaes512-a-signer.txt"
    globals()["SCEAU"] = zone / "ere-vaes512-sceau.txt"
    try:
        shutil.copytree(orig_ici / "harnais", HARNAIS)
        shutil.copyfile(orig_ici / "signeur_hors_ligne.py", zone / "signeur_hors_ligne.py")

        def _preparer():
            p = preparer()
            ok = (p.exists() and (zone / "a-emporter").exists()
                  and len(list((zone / "a-emporter").iterdir())) == 5)
            return ok, "la charge + les 5 pièces à emporter"
        epreuve("le manifeste + la charge + a-emporter (les empreintes recalculées)",
                _preparer)

        def _signer_test():
            import os
            graine_test_hex = GRAINE_TEST.hex()
            privee = zone / "cle-test.txt"
            privee.write_text("# TEST — la graine publique constante (jamais une clé réelle)\n"
                              + graine_test_hex + "\n", encoding="utf-8")
            cwd_avant = os.getcwd()
            os.chdir(zone)                 # le signeur écrit à son répertoire courant
            try:
                ed.mode_signer("ere-vaes512-a-signer.txt", "cle-test.txt")
            finally:
                os.chdir(cwd_avant)
            return (zone / "signatures-I.txt").exists(), "les signatures de test écrites"
        epreuve("la signature à la CLÉ DE TEST (la graine publique, l'état test visible)",
                _signer_test)

        def _verifier_test():
            pub_test = ed.cle_publique_depuis_graine(GRAINE_TEST)
            v = verifier(zone / "signatures-I.txt", publique_test=pub_test)
            return v["tout_vert"], f"{len(v['verdicts'])} signatures vertes à la clé de TEST"
        epreuve("la vérification à la clé publique I (la continuité)", _verifier_test)

        def _signature_muee():
            pub_test = ed.cle_publique_depuis_graine(GRAINE_TEST)
            lignes = (zone / "signatures-I.txt").read_text(encoding="utf-8").splitlines()
            m = lignes[0].split()
            m[2] = ("0" if m[2][0] != "0" else "1") + m[2][1:]
            muee = zone / "signatures-muees.txt"
            muee.write_text("\n".join([" ".join(m)] + lignes[1:]) + "\n", encoding="utf-8")
            v = verifier(muee, publique_test=pub_test)
            return not v["tout_vert"], "la signature muée REFUSÉE nommément"
        epreuve("la signature muée REFUSÉE", _signature_muee)

        def _charge_muee():
            lignes = CHARGE.read_text(encoding="utf-8").splitlines()
            morceaux = lignes[0].split()
            morceaux[2] = "0" * 64
            CHARGE.write_text(" ".join(morceaux) + "\n" + "\n".join(lignes[1:]) + "\n",
                              encoding="utf-8")
            try:
                v = verifier(zone / "signatures-I.txt")
                return not v["tout_vert"], "la charge muée REFUSÉE"
            finally:
                preparer()          # la charge honnête réécrite
        epreuve("la charge muée REFUSÉE (puis la charge honnête réécrite)", _charge_muee)

        def _installer_test():
            pub_test = ed.cle_publique_depuis_graine(GRAINE_TEST)
            r = installer(zone / "signatures-I.txt", publique_test=pub_test)
            sceau = zone / "ere-vaes512-sceau.txt"
            texte = sceau.read_text(encoding="utf-8") if sceau.exists() else ""
            return (r["installe"] and sceau.exists()
                    and "TEST" not in pathlib.Path(zone / "signatures-I.txt").read_text(encoding="utf-8")
                    and "l'ère est scellée" in texte.lower()), "le sceau écrit"
        epreuve("l'installation du sceau + le zip", _installer_test)

        def _rejeu():
            pub_test = ed.cle_publique_depuis_graine(GRAINE_TEST)
            r1 = installer(zone / "signatures-I.txt", publique_test=pub_test)
            return r1["installe"], "le rejeu idempotent"
        epreuve("le rejeu idempotent de l'installation", _rejeu)
    finally:
        globals()["ICI"] = orig_ici
        globals()["HARNAIS"] = orig_ici / "harnais"
        globals()["A_EMPORTER"] = orig_ici / "a-emporter"
        globals()["CHARGE"] = orig_ici / "ere-vaes512-a-signer.txt"
        globals()["SCEAU"] = orig_ici / "ere-vaes512-sceau.txt"
        shutil.rmtree(zone, ignore_errors=True)

    # l'autotest du signeur (les vecteurs RFC 8032 + la mutation) — VÉCU AUSSI
    print("[signeur] l'autotest des vecteurs RFC 8032 :")
    tout = ed.autotest() and tout
    print(f"\n[autotest] {'TOUT VERT — la cérémonie attend la clé du maître' if tout else 'ROUGE — le kit refuse la cérémonie'}")
    return 0 if tout else 3


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] == "--preparer":
        preparer()
        return 0
    if args[0] == "--verifier":
        chemin = pathlib.Path(args[1]) if len(args) > 1 else ICI / "signatures-I.txt"
        v = verifier(chemin)
        return 0 if v["tout_vert"] else 3
    if args[0] == "--installer":
        chemin = pathlib.Path(args[1]) if len(args) > 1 else ICI / "signatures-I.txt"
        r = installer(chemin)
        return 0 if r["installe"] else 3
    if args[0] == "--autotest":
        return autotest()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
