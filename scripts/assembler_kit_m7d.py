#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_m7d.py — LE KIT TERRAIN M7-(d) : assemblage PAR SCRIPT,
modèle assembler_kit_m6d.py (Task 70) — le kit riscv64 de l'universalité.

Les pièces :
  1. LE RECOUPEMENT DES CHAÎNES : le gabarit porte les chaînes de la
     transcription en LITTÉRAUX — l'assembleur les recoupe au layout du
     dépôt (la source unique) AVANT toute substitution : une divergence
     est un refus nommé (le scénario ne peut pas narrer un autre plan) ;
  2. LES SUBSTITUTIONS DEPUIS LA SOURCE : les sha des DEUX artefacts
     (assertés contre les fichiers du dépôt — le scellé 0.8.0-rc.1 et le
     démonstrateur éprouvé M7-(c)), le md5 et la taille de l'INSTRUMENT
     embarqué (qemu-riscv64 statique), l'offset du site DEP TROUVÉ PAR
     DÉSASSEMBLAGE (la DERNIÈRE occurrence de « addi a0, zero, 7 » dans le
     slot tcp-07 — le site de l'APPLY, modèle demo_patch.py), les 4 octets
     attendus au site, les adresses des instructions du démonstrateur
     (assemblées depuis la notation — la même source que l'oracle), les
     tailles FIGÉES de la transcription (15 425 o) et de l'attendu DEP
     (4 290 o) ;
  3. LE SCÉNARIO GÉNÉRÉ : riscv/terrain/scenario-m7d.py — py_compilé
     avant tout autre geste ;
  4. LE KIT : download/vague-m7d/kit-m7d.zip — m7-kit/ (corpus scellé +
     demo + qemu-riscv64 + scenario-m7d.py + LISEZMOI-KIT-M7D.md), les
     bits exécutables portés DANS le zip ;
  5. L'INTÉGRITÉ : le zip relu après construction (corpus == scellé,
     demo == éprouvé, scénario == généré, instrument == md5) ;
  6. L'ÉPREUVE (D153) : le kit EXACT (celui qui sera déposé) est extrait
     dans un dossier VIERGE et EXÉCUTÉ au laboratoire — le run doit rendre
     VERT (rc 0, les trois pièces nées, le verdict sur pièces) ; un kit
     qui n'est pas vert au labo n'est pas déposé.

Usage : python3 scripts/assembler_kit_m7d.py
Code de sortie : 0 = kit assemblé, éprouvé, prêt au dépôt ; 2 = refus nommé.
"""

import hashlib
import importlib.util
import os
import py_compile
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile

REPO = "/home/z/my-project/triade"
RISCV = os.path.join(REPO, "riscv")
SORTIE_DIR = "/home/z/my-project/download/vague-m7d"
GABARIT = os.path.join(RISCV, "terrain", "scenario-m7d.py.in")
SCENARIO = os.path.join(RISCV, "terrain", "scenario-m7d.py")
LISEZMOI = os.path.join(RISCV, "terrain", "LISEZMOI-KIT-M7D.md")
ARTEFACT_CORPUS = os.path.join(RISCV, "corpus")
ARTEFACT_DEMO = os.path.join(RISCV, "demo")
QEMU_LABO = os.path.join(RISCV, ".tmp", "qemu-extract", "usr", "bin", "qemu-riscv64")
ZIP_KIT = os.path.join(SORTIE_DIR, "kit-m7d.zip")

SHA_CORPUS = "ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799"
SHA_DEMO = "e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9"

sys.path.insert(0, RISCV)
import layout as L                                   # noqa: E402

import capstone                                      # noqa: E402

CS = capstone.Cs(capstone.CS_ARCH_RISCV, capstone.CS_MODE_RISCV64)


class Refus(Exception):
    """Tout refus nommé de l'assembleur (fail-closed)."""


def _charger_module(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    print("=== M7-(d) : assemblage du kit terrain (l'universalité rejouée) ===")

    # (0) les artefacts du dépôt — LES pièces du kit --------------------------
    with open(ARTEFACT_CORPUS, "rb") as f:
        corpus = f.read()
    if hashlib.sha256(corpus).hexdigest() != SHA_CORPUS:
        raise Refus("riscv/corpus n'est pas le scellé 0.8.0-rc.1 — le kit refuse")
    with open(ARTEFACT_DEMO, "rb") as f:
        demo = f.read()
    if hashlib.sha256(demo).hexdigest() != SHA_DEMO:
        raise Refus("riscv/demo n'est pas le démonstrateur éprouvé M7-(c) "
                    "(sha divergent) — le kit refuse")
    if not os.access(QEMU_LABO, os.X_OK):
        raise Refus("l'instrument qemu-riscv64 du laboratoire est absent — "
                    "riscv/outils/installer_qemu.sh d'abord (D149)")
    with open(QEMU_LABO, "rb") as f:
        qemu_bin = f.read()
    md5_qemu = hashlib.md5(qemu_bin).hexdigest()
    version_qemu = subprocess.run([QEMU_LABO, "--version"], capture_output=True,
                                  text=True).stdout.splitlines()[0]
    print(f"[pièces] corpus scellé {SHA_CORPUS[:16]}… ; demo {SHA_DEMO[:16]}… ; "
          f"instrument {version_qemu} ({len(qemu_bin)} o, md5 {md5_qemu[:8]}…)")

    # (1) LE SITE DEP PAR DÉSASSEMBLAGE (jamais cru) ---------------------------
    cible = None
    for insn in CS.disasm(bytes(demo[L.A_PATCH:L.A_PATCH + 0x200]), L.A_PATCH):
        # la DERNIÈRE occurrence = le site de L'APPLY (le rollback précède
        # .applique dans le code — viser l'apply : le mutant meurt au
        # PREMIER apply, la transcription s'arrête aux 400 lignes v1)
        if insn.mnemonic == "addi" and insn.op_str == "a0, zero, 7":
            cible = insn.address
    if cible is None:
        raise Refus("le DEP : l'immédiat 0x7 de tcp-07 introuvable dans le demo")
    if demo[cible + 2] != 0x70:
        raise Refus(f"le DEP : l'octet immédiat inattendu {demo[cible + 2]:#04x}")
    dep_octets = demo[cible:cible + 4]
    verif = list(CS.disasm(dep_octets, cible))
    if not verif or verif[0].mnemonic != "addi" or verif[0].op_str != "a0, zero, 7":
        raise Refus("le site DEP ne relit pas « addi a0, zero, 7 » — incohérent")
    print(f"[dep] le site de l'APPLY trouvé par désassemblage : {cible:#x} "
          f"({dep_octets.hex()}) — la DERNIÈRE occurrence dans le slot tcp-07")

    # (3) LES ADRESSES DU DÉMONSTRATEUR (assemblées depuis la notation) --------
    dp = _charger_module("demo_patch_kit", os.path.join(RISCV, "demo_patch.py"))
    drv = dp.assembler_demo()
    demo_addrs = [i.address for i in drv["insns"]]
    if len(demo_addrs) < 100 or demo_addrs[0] != L.DEMO_ENTREE:
        raise Refus(f"les adresses du démonstrateur sont incohérentes "
                    f"({len(demo_addrs)} instructions, entrée {demo_addrs[0]:#x})")
    print(f"[demo] {len(demo_addrs)} instructions du démonstrateur assemblées "
          f"depuis la notation (l'entrée {L.DEMO_ENTREE:#x}) — la même source "
          "que l'oracle")

    # (4) LES TAILLES FIGÉES (les invariants du M7-(c), recalculés) ------------
    attendu = dp.transcription_attendue()
    if len(attendu) != 15425:
        raise Refus(f"la transcription attendue fait {len(attendu)} o ≠ 15 425 "
                    "— le plan a divergé du geste M7-(c)")
    attendu_dep = b"".join(b"trafic " + str(i).encode() + b"\n"
                           for i in range(1200 // 3))
    if len(attendu_dep) != 4290:
        raise Refus(f"l'attendu DEP fait {len(attendu_dep)} o ≠ 4 290")
    # l'attendu du scénario TERRAIN doit être l'attendu du LABO, octet pour octet
    attendu_terrain = bytearray()
    for i in range(1200):
        if i == 400:
            attendu_terrain += L.D_APPLY + L.D_TRAMP + b"j2: verdict\n" + L.D_EFFET
        if i == 800:
            attendu_terrain += L.D_ROLLB + b"verdict\n" + L.D_V1
        ligne = b"trafic " + str(i).encode() + b"\n"
        attendu_terrain += (b"j2: " + ligne) if 400 <= i < 800 else ligne
    attendu_terrain += (L.D_PTRAFIC + L.D_REST + L.D_DORM + L.D_VERROU
                        + L.D_REFMODE + L.D_REFETAT + L.D_REFABS + L.D_REFSOM
                        + L.D_FIN)
    if bytes(attendu_terrain) != attendu:
        raise Refus("le générateur du gabarit ≠ le générateur du labo — "
                    "les deux doivent rendre le même attendu")

    # (5) LA SUBSTITUTION --------------------------------------------------------
    with open(GABARIT, encoding="utf-8") as f:
        gabarit = f.read()
    for marque in ("@@SHA_CORPUS@@", "@@SHA_DEMO@@", "@@MD5_QEMU@@",
                   "@@TAILLE_QEMU@@", "@@ATTENDU_TAILLE@@", "@@DEP_TAILLE@@",
                   "@@DEP_OFF@@", "@@DEP_OCTETS@@", "@@DEMO_ADDRS@@"):
        if marque not in gabarit:
            raise Refus(f"le gabarit ne porte pas le placeholder {marque}")
    src = (gabarit
           .replace("@@SHA_CORPUS@@", SHA_CORPUS)
           .replace("@@SHA_DEMO@@", SHA_DEMO)
           .replace("@@MD5_QEMU@@", md5_qemu)
           .replace("@@TAILLE_QEMU@@", str(len(qemu_bin)))
           .replace("@@ATTENDU_TAILLE@@", "15425")
           .replace("@@DEP_TAILLE@@", "4290")
           .replace("@@DEP_OFF@@", hex(cible))
           .replace("@@DEP_OCTETS@@", dep_octets.hex())
           .replace("@@DEMO_ADDRS@@", ", ".join(hex(a) for a in demo_addrs)))
    if "@@" in src:
        raise Refus("un placeholder subsiste dans le scénario généré")

    # LE RECOUPEMENT DES CHAÎNES : l'AST du scénario généré porte les
    # constantes CH_* — recoupées au layout du dépôt (la source unique) :
    # le scénario terrain ne peut pas narrer un autre plan
    import ast
    chaines_layout = {
        "CH_APPLY": L.D_APPLY, "CH_TRAMP": L.D_TRAMP, "CH_EFFET": L.D_EFFET,
        "CH_ROLLB": L.D_ROLLB, "CH_V1": L.D_V1, "CH_PTRAFIC": L.D_PTRAFIC,
        "CH_REST": L.D_REST, "CH_DORM": L.D_DORM, "CH_VERROU": L.D_VERROU,
        "CH_REFMODE": L.D_REFMODE, "CH_REFETAT": L.D_REFETAT,
        "CH_REFABS": L.D_REFABS, "CH_REFSOM": L.D_REFSOM, "CH_FIN": L.D_FIN,
    }
    constantes_gen = {}
    for node in ast.walk(ast.parse(src)):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Constant)
                and node.targets[0].id in chaines_layout):
            constantes_gen[node.targets[0].id] = node.value.value
    for nom, octets in chaines_layout.items():
        if constantes_gen.get(nom) != octets:
            raise Refus(f"la chaîne {nom} du scénario ({constantes_gen.get(nom)!r}) "
                        f"≠ le layout du dépôt ({octets!r}) — le scénario "
                        "narrerait un autre plan")

    with open(SCENARIO, "w", encoding="utf-8") as f:
        f.write(src)
    py_compile.compile(SCENARIO, doraise=True)
    print(f"[scenario] généré {SCENARIO} ({len(src)} o), py_compilé — "
          f"{len(demo_addrs)} adresses, DEP @{cible:#x}, instrument "
          f"{md5_qemu[:8]}…")

    # (6) LE KIT -----------------------------------------------------------------
    os.makedirs(SORTIE_DIR, exist_ok=True)
    if os.path.exists(ZIP_KIT):
        os.unlink(ZIP_KIT)
    with open(LISEZMOI, encoding="utf-8") as f:
        texte_lisezmoi = f.read()
    with zipfile.ZipFile(ZIP_KIT, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, donnees in (("corpus", corpus), ("demo", demo),
                             ("qemu-riscv64", qemu_bin)):
            zi = zipfile.ZipInfo(f"m7-kit/{nom}")
            zi.external_attr = (0o755 << 16)
            z.writestr(zi, donnees)
        zi = zipfile.ZipInfo("m7-kit/scenario-m7d.py")
        zi.external_attr = (0o755 << 16)
        z.writestr(zi, src)
        z.writestr("m7-kit/LISEZMOI-KIT-M7D.md", texte_lisezmoi)
    print(f"[kit] {ZIP_KIT} construit ({os.path.getsize(ZIP_KIT)} o)")

    # (7) L'INTÉGRITÉ RELUE --------------------------------------------------------
    with zipfile.ZipFile(ZIP_KIT) as z:
        if hashlib.sha256(z.read("m7-kit/corpus")).hexdigest() != SHA_CORPUS:
            raise Refus("le corpus relu dans le zip != le scellé")
        if hashlib.sha256(z.read("m7-kit/demo")).hexdigest() != SHA_DEMO:
            raise Refus("le demo relu dans le zip != l'éprouvé")
        if z.read("m7-kit/scenario-m7d.py") != src.encode():
            raise Refus("le scénario relu dans le zip != le généré")
        if hashlib.md5(z.read("m7-kit/qemu-riscv64")).hexdigest() != md5_qemu:
            raise Refus("l'instrument relu dans le zip != l'instrument du labo")
        print(f"[kit] relu : corpus == scellé, demo == éprouvé, scénario == "
              f"généré, instrument == {md5_qemu[:8]}…, {len(z.namelist())} entrées")

    # (8) L'ÉPREUVE : le kit EXACT, extraction vierge + run (D153) ---------------
    eprouve_dir = tempfile.mkdtemp(prefix="kit-m7d-epreuve-")
    try:
        with zipfile.ZipFile(ZIP_KIT) as z:
            z.extractall(eprouve_dir)
        p = subprocess.run([sys.executable, "scenario-m7d.py"],
                           cwd=os.path.join(eprouve_dir, "m7-kit"),
                           capture_output=True, text=True, timeout=600)
        journal = os.path.join(eprouve_dir, "m7-kit", "preuves-m7",
                               "scenario-m7d-journal.log")
        verdict = os.path.join(eprouve_dir, "m7-kit", "preuves-m7",
                               "VERDICT-run-m7d.txt")
        if p.returncode != 0 or not (os.path.exists(journal) and os.path.exists(verdict)):
            print(p.stdout[-3000:])
            print(p.stderr[-2000:], file=sys.stderr)
            raise Refus(f"le kit n'est pas vert au labo (rc={p.returncode}) — "
                        "il n'est pas déposé")
        with open(verdict, encoding="utf-8") as f:
            v = f.read()
        if "VERDICT : VERT" not in v:
            raise Refus("le verdict du kit au labo n'est pas VERT — pas de dépôt")
        lignes_vertes = [l for l in v.splitlines() if l.startswith("[m7d]")]
        print(f"[épreuve] le kit EXACT, extraction vierge + run : rc=0, VERT "
              f"({len(lignes_vertes)} constats) — le kit déposé est le kit "
              "prouvé au labo (D153)")
        for l in v.splitlines():
            if "constats :" in l or "VERDICT :" in l or "instrument :" in l:
                print(f"[épreuve]   {l.strip()}")
    finally:
        shutil.rmtree(eprouve_dir, ignore_errors=True)

    # (9) LES EMPREINTES pour le dépôt ----------------------------------------------
    with open(ZIP_KIT, "rb") as f:
        kit = f.read()
    print(f"[dépôt] kit-m7d.zip : {len(kit)} o, "
          f"sha256 {hashlib.sha256(kit).hexdigest()}, "
          f"md5 {hashlib.md5(kit).hexdigest()}")
    print("[dépôt] prêt : scripts/deposer_kit_m7d.py conduit le coffre /test "
          "(la clôture D143 du run m6d + le dépôt de la vague m7d + preuves-m7)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refus as exc:
        print(f"REFUS (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(2)
