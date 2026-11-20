#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cristallisation_incrementale.py — LA CRISTALLISATION INCRÉMENTALE
(ahult8jgd §3) : le graphe de dépendances de la carte (déclaré aux entrées
« Dépendances : » des notations), LA FERMETURE TRANSITIVE du diff SEULEMENT
re-vérifiée — la re-vérification full-card n'est plus la règle.

L'AUDIT 1/10 MAINTENU : un bloc sur dix tiré au hasard (GRAINE CONSIGNÉE)
parmi les blocs HORS fermeture, re-vérifié INTÉGRALEMENT — la garantie
statistique demeure ; L'AUDIT EST PROBABILISTE, JAMAIS PRÉSENTÉ COMME UNE
PREUVE (le contrôle négatif le démontre : un bloc hors fermeture muté est
attrapé SI le tirage le veut — sinon l'écart est NOMMÉ).

LE FAIL-CLOSED :
  — le manifeste (le cristal : sha256 par bloc + le graphe déclaré) illisible
    ou absent = RE-VÉRIFICATION FULL-CARD (jamais cru) ;
  — un bloc du graphe introuvable sur disque = REFUS ;
  — une dépendance déclarée qui n'existe pas = REFUS (le graphe ment) ;
  — un bloc hors fermeture dont le sha diffère du manifeste SANS être dans
    la fermeture = IMPOSSIBLE PAR CONSTRUCTION (le diff EST l'ensemble des
    sha divergents — la fermeture le couvre toujours) ; l'audit existe pour
    la faute INVISIBLE au sha : le moteur, le profil, le contrat (les clés
    du cache — un moteur changé re-vérifie tout, miroir du §2).

LE GRAPHE RÉEL : les 28 notations tls13 du dépôt (les « Dépendances : » de
leurs en-têtes — l'arbre des appels aux adresses scellées) ; la fermeture
d'un diff sur tls13-02 (la compression SHA-256, le cœur de la chaîne de
hachage) démontre l'économie : la famille hash + le calendrier + le
principal, les feuilles x25519/aead épargnées.

Sortie : registres/cristallisation-incrementale.json ·
rapport-cristallisation.txt"""
from __future__ import annotations

import hashlib
import json
import pathlib
import random
import re
import shutil
import statistics
import sys
import tempfile
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-porteuse-ahult8jgd"
REG = ICI / "registres"

GRAINE_DEFAUT = 20261120        # la graine du rig 8z4hj76w4, consignée


def _charger_b4():
    if str(REPO / "m4") not in sys.path:
        sys.path.insert(0, str(REPO / "m4"))
        sys.path.insert(0, str(REPO / "tls13"))
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "b4_ci", REPO / "m4" / "build_m4.py")
    B4 = importlib.util.module_from_spec(spec)
    sys.modules["b4_ci"] = B4
    spec.loader.exec_module(B4)
    spec2 = importlib.util.spec_from_file_location(
        "lay_ci", REPO / "tls13" / "layout.py")
    lay = importlib.util.module_from_spec(spec2)
    sys.modules["lay_ci"] = lay
    spec2.loader.exec_module(lay)
    return B4, lay


B4, LAY = _charger_b4()
import capstone  # noqa: E402
import keystone  # noqa: E402
KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

NOTE_DIR = REPO / "tls13" / "notation"


# ---- le graphe (les « Dépendances : » des notations — le vrai du dépôt) -----
def blocs(repertoire: pathlib.Path) -> dict[str, pathlib.Path]:
    return {f.name.split("-")[0] + "-" + f.name.split("-")[1]: f
            for f in sorted(repertoire.glob("tls13-*.asm"))}


def deps_de(chemin: pathlib.Path) -> set[str]:
    """Les dépendances DÉCLARÉES d'une notation : les identifiants tls13-NN
    cités au champ « Dépendances : » (la forme abrégée tls13-09/10/11
    EXPANDÉE — l'erratum de lecture nommé), le bloc lui-même EXCLU."""
    texte = chemin.read_text(encoding="utf-8")
    champ = ""
    for ligne in texte.splitlines():
        if "Dépendances :" in ligne:
            champ = ligne.split("Dépendances :", 1)[1]
            break
    ids: set[str] = set()
    for m in re.finditer(r"tls13-(\d{2})((?:/\d{2})+)", champ):
        ids.add(f"tls13-{m.group(1)}")
        for suite in m.group(2).split("/"):
            if suite:
                ids.add(f"tls13-{suite}")
    for m in re.finditer(r"tls13-(\d{2})", champ):
        ids.add(f"tls13-{m.group(1)}")
    moi = f"{chemin.name.split('-')[0]}-{chemin.name.split('-')[1]}"
    return ids - {moi}


def graphe(repertoire: pathlib.Path) -> dict[str, set[str]]:
    return {b: deps_de(f) for b, f in blocs(repertoire).items()}


def fermeture(diff: set[str], graphe_deps: dict[str, set[str]]) -> set[str]:
    """La fermeture transitive du diff : les blocs modifiés + TOUT bloc qui
    dépend (transitivement) d'un bloc modifié — les ARÊTES INVERSES suivies
    du diff vers les dépendants."""
    dependants: dict[str, set[str]] = {}
    for b, ds in graphe_deps.items():
        for d in ds:
            dependants.setdefault(d, set()).add(b)
    clos = set(diff)
    pile = list(diff)
    while pile:
        b = pile.pop()
        for dep in dependants.get(b, ()):
            if dep not in clos:
                clos.add(dep)
                pile.append(dep)
    return clos


def audit_1_10(complement: list[str], graine: int) -> list[str]:
    """Un bloc sur dix tiré au hasard (la graine CONSIGNÉE) parmi les blocs
    hors fermeture — l'arrondi PAR EXCÈS (jamais moins de un)."""
    k = max(1, (len(complement) + 9) // 10) if complement else 0
    rng = random.Random(graine)
    return sorted(rng.sample(complement, k)) if k else []


# ---- la vérification intégrale d'un bloc (R5 + slot + graphe) ---------------
def verifier_bloc(chemin: pathlib.Path, rva: int, slot: int,
                  graphe_deps: dict[str, set[str]]) -> dict:
    bloc = f"{chemin.name.split('-')[0]}-{chemin.name.split('-')[1]}"
    try:
        octets, metas = B4.assembler_bloc(KS, str(chemin), rva, slot)
        insns = B4.round_trip(CS, KS, str(chemin), rva, octets, metas)
        for d in graphe_deps.get(bloc, set()):
            if d not in graphe_deps:
                return {"bloc": bloc, "verdict": "REFUS",
                        "cause": f"dépendance déclarée introuvable : {d}"}
        return {"bloc": bloc, "verdict": "VERT", "octets": len(octets),
                "instructions": len(insns),
                "sha256_octets": hashlib.sha256(octets).hexdigest()}
    except Exception as e:
        return {"bloc": bloc, "verdict": "REFUS",
                "cause": f"{type(e).__name__}: {e}"[:300]}


def slots_tls13() -> dict[str, tuple[int, int]]:
    return {f"tls13-{num:02d}": LAY.SLOTS_TLS13[f"h1000{num:02d}"]
            for num in range(1, 29)}


class CristallisationIncrementale:
    """Le moteur incrémental : un manifeste (le cristal), un graphe, une
    fermeture, un audit — fail-closed sur tout silicium tordu."""

    def __init__(self, repertoire: pathlib.Path, manifeste: pathlib.Path):
        self.repertoire = pathlib.Path(repertoire)
        self.manifeste = pathlib.Path(manifeste)
        self.graphe = graphe(self.repertoire)
        self.slots = slots_tls13()
        self.manif = self._charger_manifeste()

    def _charger_manifeste(self) -> dict:
        try:
            m = json.loads(self.manifeste.read_text(encoding="utf-8"))
            if (isinstance(m, dict) and "blocs" in m
                    and isinstance(m["blocs"], dict)):
                return m
        except Exception:
            pass
        return {}          # fail-closed : vide = full-card

    def semer(self) -> int:
        """LA SEMENCE : la vérification full-card, le cristal posé (sha256
        par bloc + le graphe déclaré + les empreintes des octets assemblés)."""
        etats = {}
        for b, f in blocs(self.repertoire).items():
            rva, slot = self.slots[b]
            v = verifier_bloc(f, rva, slot, self.graphe)
            if v["verdict"] != "VERT":
                raise RuntimeError(f"la semence refuse {b} : {v.get('cause')}")
            etats[b] = {"sha256_notation": hashlib.sha256(
                f.read_bytes()).hexdigest(),
                "deps": sorted(self.graphe[b]),
                "sha256_octets": v["sha256_octets"]}
        self.manif = {"blocs": etats, "graine": None}
        self.manifeste.parent.mkdir(parents=True, exist_ok=True)
        self.manifeste.write_text(json.dumps(self.manif, indent=1),
                                  encoding="utf-8")
        return len(etats)

    def _diff(self) -> tuple[set[str], set[str]]:
        """Le diff : les sha divergents + les absents/apparés (les NOUVEAUX et
        les RETIRÉS sont des écarts nommés — jamais glissés sous le tapis)."""
        actuels = blocs(self.repertoire)
        manifs = self.manif.get("blocs", {})
        diff = {b for b in manifs
                if b in actuels and hashlib.sha256(
                    actuels[b].read_bytes()).hexdigest()
                != manifs[b]["sha256_notation"]}
        apparus = set(actuels) - set(manifs)
        disparus = set(manifs) - set(actuels)
        return diff | apparus | disparus, apparus | disparus

    def verifier(self, graine: int = GRAINE_DEFAUT) -> dict:
        """LA VÉRIFICATION INCRÉMENTALE : la fermeture du diff seule + l'audit
        1/10 du complément ; le manifeste vide ou incohérent = FULL-CARD
        (fail-closed)."""
        full_card = not self.manif.get("blocs")
        tout = set(self.graphe)
        if full_card:
            a_verifier, fermet, complement = tout, tout, set()
            diff = tout
        else:
            diff, ecarts_nommes = self._diff()
            fermet = fermeture(diff, self.graphe)
            complement = tout - fermet
            a_verifier = fermet
        audits = audit_1_10(sorted(complement), graine)
        t0 = time.monotonic()
        verdicts = {}
        for b in sorted(a_verifier | set(audits)):
            rva, slot = self.slots[b]
            verdicts[b] = verifier_bloc(blocs(self.repertoire)[b], rva, slot,
                                        self.graphe)
        dt = time.monotonic() - t0
        refus = {b: v for b, v in verdicts.items() if v["verdict"] != "VERT"}
        # le graphe entier contrôlé (les dépendances pendantes = REFUS)
        for b, ds in self.graphe.items():
            for d in ds:
                if d not in self.graphe:
                    refus.setdefault(b, {"verdict": "REFUS",
                                         "cause": f"dépendance "
                                                  f"introuvable : {d}"})
        return {"full_card": full_card, "diff": sorted(diff),
                "fermeture": sorted(fermet),
                "complement": sorted(complement),
                "audit": audits, "graine": graine,
                "verifies": sorted(verdicts), "refus": refus,
                "secondes": round(dt, 4),
                "verdict": "VERT" if not refus else "REFUS"}


# ---- le protocole (le vrai du dépôt + les contrôles) ------------------------
def main() -> int:
    man_chemin = REG / "cristal-manifeste-tls13.json"
    # la semence sur le VRAI dépôt (lecture seule — les blocs intacts)
    base = CristallisationIncrementale(NOTE_DIR, man_chemin)
    n_semis = base.semer()
    graphe_reel = base.graphe

    # le laboratoire : une COPIE des 28 notations (le dépôt JAMAIS touché)
    labo = pathlib.Path(tempfile.mkdtemp(prefix="cristal-labo-"))
    shutil.copytree(NOTE_DIR, labo / "notation")
    essai = CristallisationIncrementale(labo / "notation", man_chemin)

    v0 = essai.verifier()
    rapport = [
        "LA CRISTALLISATION INCRÉMENTALE (ahult8jgd §3) — la fermeture "
        "transitive du diff seule re-vérifiée, l'audit 1/10 maintenu",
        "",
        f"LE GRAPHE RÉEL : {len(graphe_reel)} blocs tls13, "
        f"{sum(len(d) for d in graphe_reel.values())} arêtes déclarées "
        "(les « Dépendances : » des en-têtes du dépôt) ; la semence "
        f"full-card : {n_semis} blocs VERTS, le cristal posé "
        f"(sha256 par notation + le graphe)",
        f"LE ZÉRO-DIFF : fermeture ∅, complément {len(v0['complement'])} — "
        f"l'audit tire {v0['audit']} (graine {v0['graine']}), "
        f"{len(v0['verifies'])} blocs vérifiés, verdict {v0['verdict']}",
        ""]

    # ---- LE DIFF RÉEL : tls13-02 muté (un octet de commentaire — un vrai
    # diff, R5 vert) — la fermeture démontrée sur le graphe vrai -------------
    f02 = labo / "notation" / "tls13-02-sha256-comprimer.asm"
    texte = f02.read_text(encoding="utf-8")
    f02.write_text(texte.replace("le fixture K[64] @R_K cité",
                                 "le fixture K[64] @R_K cité (revu)"),
                   encoding="utf-8")
    v1 = essai.verifier()
    rapport += [
        "LE DIFF RÉEL (tls13-02, la compression SHA-256, un octet de "
        "commentaire ajouté — la notation reste VERT) :",
        f"  la fermeture transitive : {len(v1['fermeture'])} blocs "
        f"{'{'}{', '.join(b.split('-')[1] for b in v1['fermeture'])}{'}'}",
        f"  le complément épargné : {len(v1['complement'])} blocs "
        f"({'/'.join(b.split('-')[1] for b in v1['complement'])})",
        f"  l'audit 1/10 (graine {v1['graine']}) : "
        f"{', '.join(b.split('-')[1] for b in v1['audit']) or 'rien à tirer'}"
        " — re-vérifiés intégralement",
        f"  L'ÉCONOMIE : {len(v1['verifies'])} blocs vérifiés contre "
        f"{n_semis} à la règle full-card "
        f"(−{(1 - len(v1['verifies'])/n_semis)*100:.0f} %) ; "
        f"le poste {v1['secondes']*1000:.0f} ms",
        f"  le verdict : {v1['verdict']}"
        + ("" if not v1["refus"] else
           f" — REFUS {v1['refus']} — ROUGE"),
        ""]

    # ---- LE CONTRÔLE NÉGATIF : un bloc HORS fermeture muté -------------------
    # (tls13-17, la multiplication GHASH — feuille aead, hors la fermeture du
    # diff tls13-02) ; la mutation CASSE le R5 (le compte d'en-tête) ; LE
    # CRISTAL EMPOISONNÉ : le manifeste porte le sha de la notation MUTÉE
    # (la mutation glissée entre le semis et l'ouverture — le sha du cristal
    # MENT) → le diff calculé ne la voit PAS : la fermeture l'épargne, L'AUDIT
    # EST LE SEUL FILET — probabiliste, jamais une preuve
    f17 = labo / "notation" / "tls13-17-ghash-multiplication.asm"
    t17 = f17.read_text(encoding="utf-8")
    m17 = re.search(r"; Code : (\d+) o", t17)
    f17.write_text(t17.replace(f"; Code : {m17.group(1)} o",
                               f"; Code : {int(m17.group(1)) - 1} o"),
                   encoding="utf-8")
    man_empoison = labo / "manifeste-empoisonne.json"
    import copy as _copy
    mensonge = _copy.deepcopy(base.manif)
    mensonge["blocs"]["tls13-17"]["sha256_notation"] = hashlib.sha256(
        f17.read_bytes()).hexdigest()
    man_empoison.write_text(json.dumps(mensonge, indent=1), encoding="utf-8")
    piege = CristallisationIncrementale(labo / "notation", man_empoison)
    v2 = piege.verifier()
    attrape = "tls13-17" in v2["refus"]
    # la graine qui DÉMONTRE la capture (consignée — cherchée, pas simulée)
    graine_demo = next(g for g in range(1, 10000)
                       if "tls13-17" in audit_1_10(v1["complement"], g))
    v2demo = CristallisationIncrementale(labo / "notation", man_empoison)
    v2demo.manif = mensonge
    r_demo = v2demo.verifier(graine=graine_demo)
    if attrape:
        sort_neg = ("DANS le tirage — ATTRAPÉ par la re-vérification "
                    "intégrale (la faute CONSTATÉE au refus)")
    else:
        sort_neg = ("HORS le tirage — NON ATTRAPÉ : L'ÉCART NOMMÉ (l'audit "
                    "est probabiliste, 1/10, JAMAIS une preuve — la faute "
                    "demeure au cristal empoisonné : le prochain tirage ou "
                    "la prochaine SEMENCE full-card la prendra)")
    rapport += [
        "LE CONTRÔLE NÉGATIF (tls13-17 muté au compte d'en-tête — le R5 DOIT "
        "refuser — ET le cristal empoisonné : son sha mensonger fait croire "
        "au diff {02} seul, la fermeture ÉPARGNE le 17 muté) :",
        f"  le tirage de l'audit (graine {v2['graine']}) : "
        f"{', '.join(b.split('-')[1] for b in v2['audit'])}",
        f"  tls13-17 {sort_neg}",
        f"  LA CAPTURE DÉMONTRÉE (graine {graine_demo} CHERCHÉE et "
        f"consignée) : le tirage prend tls13-17 — "
        f"{r_demo['verdict']} ({list(r_demo['refus']) or 'aucun refus'}) : "
        "l'audit ATTRAPE la faute invisible au diff",
        f"  le verdict du run à la graine par défaut : {v2['verdict']} "
        + (f"(le refus : {list(v2['refus'])})" if v2["refus"] else
           " — VERT : le filet a laissé passer (l'écart nommé ci-dessus)"),
        ""]

    # ---- la force du contrôle négatif : le balayage des graines ---------------
    # (200 tirages sur le complément DU DIFF 02 SEUL : la fréquence empirique
    # de capture ≈ la probabilité du tirage — la NATURE probabiliste démontrée
    # sur pièces, jamais une preuve)
    capture = 0
    tirages = 200
    for graine in range(1, tirages + 1):
        if "tls13-17" in audit_1_10(v1["complement"], graine):
            capture += 1
    p_theo = len(audit_1_10(v1["complement"], 1)) / max(len(v1["complement"]), 1)
    rapport += [
        f"LE BALAYAGE DES GRAINES ({tirages} tirages de l'audit sur le "
        f"complément de {len(v1['complement'])} blocs, k="
        f"{len(audit_1_10(v1['complement'], 1))}) : tls13-17 tiré "
        f"{capture}/{tirages} = {capture/tirages*100:.1f} % (la probabilité "
        f"du tirage uniforme : {p_theo*100:.1f} %) — L'AUDIT EST UN FILET "
        "PROBABILISTE, PAS UNE PREUVE : la garantie ultime demeure la "
        "SEMENCE full-card (le prochain semis re-vérifie TOUT — le cristal "
        "empoisonné ne lui survit pas) ; pour la faute VISIBLE au sha, la "
        "FERMETURE la prend à chaque fois",
        ""]

    # ---- la mesure du poste (n=10, la médiane) --------------------------------
    # (le laboratoire PROPRE au diff 02 seul — la mutation 17 était le contrôle
    # négatif ; la mesure compare la règle full-card à l'incrément du MÊME diff)
    labo2 = pathlib.Path(tempfile.mkdtemp(prefix="cristal-mesure-"))
    shutil.copytree(NOTE_DIR, labo2 / "notation")
    f02b = labo2 / "notation" / "tls13-02-sha256-comprimer.asm"
    f02b.write_text(f02b.read_text(encoding="utf-8").replace(
        "le fixture K[64] @R_K cité", "le fixture K[64] @R_K cité (revu)"),
        encoding="utf-8")
    man_vide = labo2 / "manifeste-vide.json"   # absent → full-card (fail-closed)
    temps_full, temps_incr = [], []
    for _ in range(10):
        c = CristallisationIncrementale(labo2 / "notation", man_vide)
        r = c.verifier()                # full-card (le cristal absent)
        temps_full.append(r["secondes"])
    for _ in range(10):
        c = CristallisationIncrementale(labo2 / "notation", man_chemin)
        r = c.verifier()                # l'incrément (le diff 02 seul)
        temps_incr.append(r["secondes"])
    med_full = statistics.median(temps_full)
    med_incr = statistics.median(temps_incr)
    rapport += [
        "LE POSTE DE VÉRIFICATION (n=10, la médiane, cette machine — le "
        "laboratoire au diff tls13-02 seul, R5 vert) :",
        f"  la règle full-card : {med_full*1000:.0f} ms "
        f"[{min(temps_full)*1000:.0f}–{max(temps_full)*1000:.0f}]",
        f"  l'incrément (fermeture + audit) : {med_incr*1000:.0f} ms "
        f"[{min(temps_incr)*1000:.0f}–{max(temps_incr)*1000:.0f}] — "
        f"−{(1 - med_incr/med_full)*100:.0f} %",
        ""]

    shutil.rmtree(labo, ignore_errors=True)
    shutil.rmtree(labo2, ignore_errors=True)

    ok = (v0["verdict"] == "VERT" and v1["verdict"] == "VERT"
          and r_demo["verdict"] == "REFUS" and "tls13-17" in r_demo["refus"]
          and med_incr < med_full and len(v1["fermeture"]) > 1)
    rapport += [f"LE VERDICT : {'VERT' if ok else 'ROUGE'}"]

    (REG / "cristallisation-incrementale.json").write_text(json.dumps({
        "graphe": {b: sorted(d) for b, d in graphe_reel.items()},
        "zero_diff": v0, "diff_reel": v1, "negatif": v2,
        "balayage": {"tirages": tirages, "captures": capture,
                     "p_theorique": round(p_theo, 4)},
        "temps": {"full_card_s": [round(x, 4) for x in temps_full],
                  "increment_s": [round(x, 4) for x in temps_incr],
                  "medianes": {"full_card_s": round(med_full, 4),
                               "increment_s": round(med_incr, 4)}},
        "verdict": "VERT" if ok else "ROUGE"}, ensure_ascii=False, indent=1),
        encoding="utf-8")
    (ICI / "rapport-cristallisation.txt").write_text("\n".join(rapport) + "\n",
                                                     encoding="utf-8")
    print("\n".join(rapport))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
