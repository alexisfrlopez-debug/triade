#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""controle_base_reelle.py — LE CONTRÔLE D146 ADAPTÉ À L'EXÉCUTEUR DU JALON
(chantier M7-(c) : le scellage 0.8.0-rc.1 l'exige — fiche § 8).

Le modèle unix/controle_base_reelle.py (D146 : l'image PIE EXÉCUTÉE à la
base réelle — l'émulation à base fixe interdite comme témoin unique),
ADAPTÉ à qemu-riscv64 (réserve instrumentale D149 — TCG, noyau et syscalls
RÉELS, jamais déguisés en exécution native) :

  - l'image full-ELF exécutée SOUS QEMU, la base CHOISIE PAR LE CHARGEUR de
    l'exécuteur (jamais une base imposée par l'instrument du test) ;
  - LA BASE CONSTATÉE PAR TRACE : -d in_asm — le journal de l'exécuteur
    nomme l'adresse du PREMIER bloc traduit (= l'entrée e_entry) : la base
    en découle (premier_pc - e_entry) — un témoin EXTERNE à l'artefact (la
    trace de l'instrument, jamais la parole de l'image) ;
  - le constat d'instrument D155 s'applique : qemu 10 ne randomise PAS
    l'image PIE invitée — la base par défaut est CONSTANTE ; l'indifférence
    à la base se DÉMONTRE par les bases forcées du CHARGEUR (-R/-B+-R),
    jamais en feignant un ASLR émulé ;
  - à CHAQUE base : la transcription du rituel EXACTE (les deux lignes
    octet pour octet) et le code 0 — le comportement identique à toute
    base, la propriété du profil (la position-indépendance du patrimoine).

Usage : python3 riscv/controle_base_reelle.py [--bavard]
Retour : executer() -> (vert, lignes) — le scellage l'exige VERT.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RISCV = ICI
sys.path.insert(0, ICI)

import build_corpus as BC              # noqa: E402  (l'exécuteur + le plan)

CORPUS = os.path.join(RISCV, "corpus")
RITUEL = (b"TRIADE M1 : minilibc 21/21 OK\n"
          b"corpus : autotest 21 vecteurs\n")

RE_IN_ASM = re.compile(r"^0x([0-9a-f]+):", re.MULTILINE)


class EchecControle(Exception):
    """Tout refus nommé (fail-closed)."""


class Terrain:
    """Le corpus sous qemu, avec trace in_asm vers un fichier temporaire."""

    def __init__(self, extra: list[str] | None = None):
        self.qemu = BC.chemin_qemu()
        self.extra = extra or []
        self.dossier = tempfile.mkdtemp(prefix="d146-rv-", dir=os.path.join(RISCV, ".tmp"))
        os.makedirs(self.dossier, exist_ok=True)
        self.trace = os.path.join(self.dossier, "trace.txt")

    def lancer(self):
        cmd = [self.qemu, "-d", "in_asm", "-D", self.trace] + self.extra + [CORPUS]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=60)
            return r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired:
            return b"", b"<timeout>", -99

    def base_constatee(self) -> int | None:
        """La base du chargement, lue dans le trace de l'exécuteur : l'adresse
        du PREMIER bloc traduit (l'entrée) — la base = pc - e_entry."""
        try:
            with open(self.trace, encoding="utf-8", errors="replace") as f:
                texte = f.read()
        except OSError:
            return None
        m = RE_IN_ASM.search(texte)
        if not m:
            return None
        premier_pc = int(m.group(1), 16)
        return premier_pc - BC.L.CORPUS_ENTREE

    def nettoyer(self):
        import shutil
        shutil.rmtree(self.dossier, ignore_errors=True)


def executer(bavard: bool = True) -> tuple[bool, list[str]]:
    lignes: list[str] = []
    vert = True

    def constat(message: str, ok: bool, detail: str = "") -> None:
        nonlocal vert
        vert = vert and ok
        l = f"[d146] {'PASS' if ok else 'ECHEC'} : {message}"
        if detail:
            l += f" ({detail})"
        lignes.append(l)

    # — la base par défaut : 6 exécutions, la base CONSTATÉE PAR TRACE -------
    bases: list[int] = []
    for i in range(6):
        t = Terrain()
        try:
            sortie, err, code = t.lancer()
            base = t.base_constatee()
            if code != 0 or err or sortie != RITUEL:
                raise EchecControle(f"l'exécution {i} : code={code} "
                                    f"sortie={sortie!r} err={err!r}")
            if base is None:
                raise EchecControle(f"l'exécution {i} : le trace in_asm ne "
                                    f"nomme aucun bloc — pas de témoin")
            if base % 0x1000 != 0:
                raise EchecControle(f"base {base:#x} NON alignée à la page — "
                                    f"le chargeur ne l'a pas choisie")
            if base < 0x10000:
                raise EchecControle(f"base {base:#x} < 0x10000 — implausible")
            bases.append(base)
        finally:
            t.nettoyer()
    distinctes = len(set(bases))
    constat("6 exécutions full-ELF à la base du CHARGEUR : le rituel exact "
            "(les deux lignes octet pour octet, code 0) et la base CONSTATÉE "
            "PAR TRACE (le premier bloc traduit - e_entry, le journal de "
            "l'exécuteur — un témoin EXTERNE à l'artefact)",
            True, f"bases {bases[0]:#x} ×{distinctes}/{len(bases)} distincte(s)")

    constat("le constat d'instrument D155 s'applique : la base par défaut "
            "CONSTANTE (qemu 10 ne randomise pas l'image PIE invitée) — la "
            "preuve d'indifférence passe par les bases FORCÉES du chargeur, "
            "jamais un ASLR émulé feint",
            distinctes == 1, f"base constante {bases[0]:#x}")

    # — les bases forcées du CHARGEUR : distinctes, la transcription identique
    forcees = []
    for nom_cfg, extra in (("-R 1G", ["-R", "1G"]),
                           ("-R 4G", ["-R", "4G"]),
                           ("-B 0x100000000 -R 2G", ["-B", "0x100000000", "-R", "2G"])):
        t = Terrain(extra=extra)
        try:
            sortie, err, code = t.lancer()
            base = t.base_constatee()
            if code != 0 or err or sortie != RITUEL:
                raise EchecControle(f"base forcée {nom_cfg} : code={code} "
                                    f"sortie={sortie!r} — l'image n'est PAS "
                                    f"indifférente à la base")
            if base is None or base % 0x1000:
                raise EchecControle(f"base forcée {nom_cfg} : témoin absent "
                                    f"ou non aligné")
            forcees.append((nom_cfg, base))
        finally:
            t.nettoyer()
    toutes = {b for _, b in forcees} | {bases[0]}
    if len(toutes) != len(forcees) + 1:
        raise EchecControle(f"les bases forcées n'ont pas bougé : "
                            f"{[f'{n}={b:#x}' for n, b in forcees]}")
    constat("3 bases forcées du CHARGEUR (-R la fenêtre de réservation VA, "
            "-B déplace dans la fenêtre) : la transcription IDENTIQUE à "
            "toute base — l'indifférence à la base DÉMONTRÉE, la preuve ne "
            "dépend d'aucun aléa de l'instrument",
            True, " / ".join(f"{n}={b:#x}" for n, b in forcees) + " VERTES")

    lignes.append(f"[d146] VERDICT : {'VERT' if vert else 'KO'} — l'image "
                  "full-ELF exécutée à la base réelle de l'exécuteur (9 "
                  "constatations par trace), la transcription identique à "
                  "toute base — le contrôle du scellage (le D146 adapté à "
                  "qemu-riscv64, réserve instrumentale D149 NOMMÉE : TCG, "
                  "noyau et syscalls réels)")
    if bavard:
        print("\n".join(lignes))
    return vert, lignes


if __name__ == "__main__":
    try:
        ok, _ = executer(bavard=True)
        sys.exit(0 if ok else 1)
    except (EchecControle, BC.EchecBuild) as exc:
        print(f"ECHEC (fail-closed) : {exc}", file=sys.stderr)
        sys.exit(1)
