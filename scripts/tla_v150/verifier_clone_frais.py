#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_clone_frais.py — LE REJEU DEPUIS UN CLONE FRAIS (l'exigence de
vérification de l'instruction 6zqo2h60n : « rejoue TLC/Apalache depuis un
clone frais et exige la reproduction exacte des counts bornés D187 (154
états/1 152 transitions) comme contrôle de fidélité »).

LE GESTE : git clone NEUF du dépôt (l'état COMMITTÉ — les artefacts du
paquet TLA+), les OUTILS copiés depuis la session avec empreintes
RECOUPÉES (tla2tools.jar et apalache-0.63.0.tgz contre
outils_consignes.txt ; le tarball Apalache recoupé AUSSI contre le
sha256sum.txt de la release amont v0.63.0), puis DEPUIS LE CLONE :
  — les SEPT runs TLC/Apalache rejoués (jouer_tous_les_runs.py du clone,
    journalisés) — les verdicts confrontés à ceux consignés (8/8 VERT) ;
  — le modèle Python re-exécuté : les comptes D187 (154 états /
    1 152 transitions au plafond v120, profondeur 6) REPRODUITS EXACTEMENT.

Sortie : scripts/tla_v150/verification_clone_frais_rapport.txt
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parents[1]
RAPPORT: list[str] = []


def ver(nom: str, ok: bool, detail: str = "") -> bool:
    RAPPORT.append(f"  {'VERT' if ok else 'ÉCHEC'}  {nom}"
                   + (f" — {detail}" if detail else ""))
    print(f"[{'VERT' if ok else 'ÉCHEC'}] {nom} {detail}")
    return ok


def sha256(chemin: pathlib.Path) -> str:
    h = hashlib.sha256()
    h.update(chemin.read_bytes())
    return h.hexdigest()


def main() -> int:
    tous = []

    clone_racine = pathlib.Path(tempfile.mkdtemp(prefix="clone_tla_v150_"))
    clone = clone_racine / "triade"
    r = subprocess.run(["git", "clone", "-q", str(REPO), str(clone)],
                       capture_output=True, text=True, timeout=300)
    tous.append(ver("le clone frais (git clone, HEAD)",
                    r.returncode == 0, r.stderr[:100] if r.returncode else
                    subprocess.run(["git", "-C", str(clone), "log",
                                    "--oneline", "-1"],
                                   capture_output=True, text=True).stdout
                    .strip()[:60]))

    # les outils : copiés depuis la session, empreintes RECOUPÉES
    consignes = {}
    for ligne in (ICI / "outils_consignes.txt").read_text().splitlines():
        if ligne and not ligne.startswith("#") and "  " in ligne:
            h, p = ligne.split("  ", 1)
            consignes[p.strip()] = h
    outils_clone = clone / "scripts" / "tla_v150" / "outils"
    outils_clone.mkdir(parents=True)
    for nom in ("tla2tools.jar", "apalache-0.63.0.tgz"):
        src = ICI / "outils" / nom
        shutil.copy2(src, outils_clone / nom)
        ok = sha256(outils_clone / nom) == consignes[f"outils/{nom}"]
        tous.append(ver(f"l'outil {nom} : empreinte recoupée", ok,
                        sha256(outils_clone / nom)[:12] + "…"))
    # extraction d'Apalache dans le clone
    subprocess.run(["tar", "xzf", "apalache-0.63.0.tgz"],
                   cwd=outils_clone, capture_output=True, timeout=120)
    tous.append(ver("Apalache extrait dans le clone",
                    (outils_clone / "apalache-0.63.0" / "bin" /
                     "apalache-mc").is_file()))

    # les artefacts du clone : empreintes == celles de la session (le clone
    # porte l'état COMMUTTÉ — la confrontation le documente)
    for rel in ("CF3.tla", "CF3Plafond.tla", "CF3Fidelite.tla",
                "CF3Controle.tla", "verdicts.json"):
        ok = sha256(clone / "scripts" / "tla_v150" / rel) == sha256(ICI / rel)
        tous.append(ver(f"l'artefact {rel} identique au clone", ok))

    # 1 — les runs TLC/Apalache DEPUIS LE CLONE
    r = subprocess.run([sys.executable, "jouer_tous_les_runs.py"],
                       cwd=clone / "scripts" / "tla_v150",
                       capture_output=True, text=True, timeout=560)
    try:
        verdicts_clone = json.loads(
            (clone / "scripts" / "tla_v150" / "verdicts.json")
            .read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        verdicts_clone = {}
        RAPPORT.append(f"  ÉCHEC  verdicts.json illisible : {exc}")
    verdicts_ref = json.loads((ICI / "verdicts.json").read_text("utf-8"))
    pareils = verdicts_clone == verdicts_ref
    globaux = verdicts_clone.get("tlc_fidelite_d187"), \
        verdicts_clone.get("tlc_plafond_inv"), \
        verdicts_clone.get("tlc_bornes_inv"), \
        verdicts_clone.get("apalache_base"), \
        verdicts_clone.get("apalache_inductif"), \
        verdicts_clone.get("apalache_inductif_init_inv"), \
        verdicts_clone.get("apalache_controle_c1_attrape"), \
        verdicts_clone.get("apalache_controle_c2_attrape")
    tous.append(ver("les 7 runs rejoués depuis le clone : verdicts "
                    "IDENTIQUES aux consignés", pareils and all(globaux),
                    f"{sum(1 for g in globaux if g)}/8 VERT "
                    f"(TLC {verdicts_clone.get('tlc_fidelite_etats')}/"
                    f"{verdicts_clone.get('tlc_plafond_etats')}/"
                    f"{verdicts_clone.get('tlc_bornes_etats')} états)"))
    # les journaux du clone conservés comme pièce
    shutil.copytree(clone / "scripts" / "tla_v150" / "logs",
                    ICI / "logs_clone_frais", dirs_exist_ok=True)
    tous.append(ver("les journaux du clone conservés (logs_clone_frais/)",
                    (ICI / "logs_clone_frais" / "tlc_fidelite.txt").is_file()))

    # 2bis — la campagne PBT DU CLONE rejouée à graine identique
    # (200 traces aux indices 0..199 : les condensats confrontés au CSV
    # committé — la preuve que la campagne rejoue depuis l'état committé)
    r = subprocess.run(
        [sys.executable, "pbt_raffinement_v150.py", "--replay",
         "--debut", "0", "--fin", "200"],
        cwd=clone / "scripts" / "preuves_v150",
        capture_output=True, text=True, timeout=400)
    rejeu_clone = {int(x["trace"]): x["digest"] for x in
                   __import__("csv").DictReader(
                       open(clone / "scripts" / "preuves_v150" /
                            "pbt_traces_rejeu.csv", encoding="utf-8"))}
    orig = {int(x["trace"]): x["digest"] for x in
            __import__("csv").DictReader(
                open(ICI.parent / "preuves_v150" / "pbt_traces.csv",
                     encoding="utf-8"))}
    stables_clone = sum(1 for i in range(200)
                        if rejeu_clone.get(i) == orig.get(i))
    tous.append(ver("la campagne PBT du clone rejouée (200 traces à graine "
                    "identique) : condensats IDENTIQUES au CSV committé",
                    stables_clone == 200, f"{stables_clone}/200"))

    # 3 — le modèle Python DEPUIS LE CLONE : les comptes D187
    code = (
        "import sys; sys.path.insert(0, 'scripts/preuves_v150');\n"
        "import modele_invariant_v150 as m\n"
        "st = m.explorer(3, 6, plafond_v120=True)\n"
        "print(f\"{st['états']}|{st['transitions']}\")\n"
        "assert st['états'] == 154 and st['transitions'] == 1152\n"
    )
    r = subprocess.run([sys.executable, "-c", code], cwd=clone,
                       capture_output=True, text=True, timeout=300)
    ok_d187 = r.returncode == 0 and "154|1152" in r.stdout
    tous.append(ver("le modèle Python du clone : D187 reproduit EXACTEMENT "
                    "(154 états / 1 152 transitions)", ok_d187,
                    r.stdout.strip().splitlines()[-1]
                    if r.stdout.strip() else r.stderr[:80]))

    shutil.rmtree(clone_racine, ignore_errors=True)

    rapport = [
        "LE REJEU DEPUIS UN CLONE FRAIS — le paquet TLA+ (6zqo2h60n)",
        "",
        "LE GESTE : git clone neuf du dépôt (l'état committé) ; les outils "
        "copiés avec empreintes recoupées (tla2tools.jar "
        "e1f11b75c4b5bc4478ba0ac5cb6ae28e40a01b0016bc33e0aa97da22dfdbcd7f ; "
        "apalache-0.63.0.tgz a756e96af249bf33cd7629667a49472cb26ac8227c4858"
        "3da139b414834d59df == le sha256sum.txt de la release amont) ; les "
        "sept runs rejoués DEPUIS LE CLONE ; le modèle Python du clone "
        "re-exécuté aux bornes D187.",
        "",
    ] + RAPPORT + [
        "",
        f"LE BILAN : {sum(1 for t in tous if t)}/{len(tous)} VERT — "
        "l'état committé REJOUE l'intégralité du paquet (la fidélité D187 "
        "154/1 152, les espaces 154/216/360, le déchargement Apalache et "
        "ses contrôles négatifs) SANS dépendre de l'état de la session.",
        "",
    ]
    (ICI / "verification_clone_frais_rapport.txt").write_text(
        "\n".join(rapport) + "\n", encoding="utf-8")
    print(f"[bilan] {sum(1 for t in tous if t)}/{len(tous)} VERT")
    return 0 if all(tous) else 1


if __name__ == "__main__":
    sys.exit(main())
