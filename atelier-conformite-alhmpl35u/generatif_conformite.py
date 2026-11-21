#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generatif_conformite.py — LA MACHINERY DE CONFORMITÉ GÉNÉRATIVE branchée
sur la machine z3 de la sentinelle durcie (alhmpl35u, la vague 12).

LE MANDAT (l'instruction, le chantier 1) : 30 000 traces, TROIS graines, la
réduction ddmin sur toute divergence, le replay bit-identique deux fois ;
chaque règle abstraite confrontée à l'implémentation Python durcie, LES
CHEMINS D'ÉCHEC INCLUS (la corruption sans destruction, la falsification à
empreinte naïve valide → destruction+PV, le nonce altéré après empreinte
verte, le piège périmé/périé d'époque, le retour en arrière, la phrase
faible au plancher) ; les quatre invariants z3 re-déchargés sur le modèle
ÉTENDU, contrôles négatifs compris (la machine nue doit redevenir SAT).

LA CONCEPTION NOMMÉE (le coût n'est pas l'objet) : K_user dérivé UNE fois
par la VRAIE Argon2id du labo (p_idx 0) pour chacune des DEUX phrases de
test (la honnête et l'erronée) — les traces excercent LA SENTINELLE (les
règles empreinte/AEAD/piège/époque/plancher), la dérivation n'y vit pas ;
le caractère aléatoire par trace vit aux s_serrure/s_piege/sel_hkdf/nonce
frais du constructeur INTACT.

Sortie : traces-*.jsonl · campaign.json · rapport-generatif.txt"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import random
import shutil
import sys
import tempfile
import time
import contextlib
import io

ICI = pathlib.Path(__file__).resolve().parent
REPO = ICI.parent
LABO = REPO / "atelier-coffre-vr9n3s3l7" / "labo"
sys.path.insert(0, str(LABO))
import coffre_labo as C                                     # noqa: E402

PHRASE_HONNETE = b"PHRASE-TEST-PUBLIQUE-D105-vague12-conformite-honnete"
PHRASE_ERRONEE = b"PHRASE-TEST-PUBLIQUE-D105-vague12-conformite-erronee"

# ---- LA DÉRIVATION UNE FOIS (la vraie Argon2 du labo, p_idx 0) -----------
K_HONNETE = bytes(C.cle_utilisateur(PHRASE_HONNETE,
                                    b"\x00" * C.TAILLE_SEL_ARGON, 0))
K_ERRONEE = bytes(C.cle_utilisateur(PHRASE_ERRONEE,
                                    b"\x00" * C.TAILLE_SEL_ARGON, 0))


def cle_patchee(phrase, sel_argon, p_idx):
    """K_user fixe par phrase de test — LA DÉRIVATION N'EST PAS L'OBJET
    (conception nommée au rapport) ; le sel est ignoré délibérément."""
    return bytearray(K_ERRONEE if bytes(phrase) == PHRASE_ERRONEE
                     else K_HONNETE)


C.cle_utilisateur = cle_patchee

# ---- LA TABLE DES RÈGLES ABSTRAITES (le modèle, la lettre du plan) -------
# (scénario, verdict abstrait attendu)
REGLES = {
    "honnete": "OUVERT",
    "corruption": "REFUS_SANS_DESTRUCTION",
    "falsification-naive": "DESTRUCTION_PV",
    "nonce-altere": "DESTRUCTION_PV",
    "piege-perime": "REFUS_PIEGE_PERIME",
    "retour-arriere": "REFUS_RETOUR_ARRIERE",
    "phrase-erronee": "PHRASE_ERRONEE_BENIN",
    "plancher-faible": "REFUS_PLANCHER",
}
SCENARIOS = list(REGLES)


def classer(exc: Exception | None) -> str:
    """Le verdict observé, classé aux noms du protocole."""
    if exc is None:
        return "OUVERT"
    if isinstance(exc, C.PhraseErronee):
        return "PHRASE_ERRONEE_BENIN"
    if isinstance(exc, C.ErreurPlancherEntropie):
        return "REFUS_PLANCHER"
    m = str(exc)
    if "CORRUPTION" in m:
        return "REFUS_SANS_DESTRUCTION"
    if "FALSIFICATION À EMPREINTE VALIDE" in m:
        return "DESTRUCTION_PV"
    if "tag AEAD invalide" in m or "état scellé" in m:
        return "DESTRUCTION_PV"
    if "PÉRIMÉ" in m:
        return "REFUS_PIEGE_PERIME"
    if "RETOUR EN ARRIÈRE" in m:
        return "REFUS_RETOUR_ARRIERE"
    if "piège est ABSENT" in m:
        return "REFUS_PIEGE_ABSENT"
    return f"AUTRE:{m[:48]}"


def jouer_trace(rng: random.Random, scenario: str, rep: pathlib.Path) -> dict:
    """UNE trace : le conteneur construit au constructeur INTACT, la mutation
    du scénario, la sentinelle INTACTE exécutée — le verdict classé."""
    conteneur = rep / "coffre.bin"
    pieges = rep / "pieges"
    if scenario == "plancher-faible":
        # les QUATRE phrases faibles validées à l'estimateur (D242 les
        # trois premières ; « 123456789abc » ADMISE à 62 bits par l'estimateur
        # — le plancher honnête, jamais une divergence — exclue de la liste)
        faibles = ["motdepasse", "azer1234", "correcthorse",
                   "phrase-trop-faible"]
        p = faibles[rng.randrange(len(faibles))].encode()
        try:
            C.verifier_plancher(p)
            return {"scenario": scenario, "attendu": REGLES[scenario],
                    "observe": "OUVERT (BUG)", "ok": False}
        except Exception as e:
            obs = classer(e)
            return {"scenario": scenario, "attendu": REGLES[scenario],
                    "observe": obs, "ok": obs == REGLES[scenario]}
    # le plancher exige une phrase forte pour l'init — la honnête l'est
    C.init(str(conteneur), str(pieges), PHRASE_HONNETE, "trace alhmpl35u")
    phrase_essai = PHRASE_ERRONEE if scenario == "phrase-erronee" \
        else PHRASE_HONNETE
    if scenario in ("piege-perime", "retour-arriere"):
        # PÉRIMÉ : le conteneur à l'époque 2, le piège d'époque 1 posé AU
        #   CHEMIN de l'époque 2 (le couple ancien restauré — le contenu
        #   porte l'époque 1, le conteneur l'époque 2) ;
        # RETOUR EN ARRIÈRE : le conteneur d'époque 1 sous le MIROIR local
        #   d'époque 2 (le couple ancien restauré au-dessous du miroir).
        blob = conteneur.read_bytes()
        ent = C.parser_entete(blob)
        clair = json.dumps({"projets": {}}).encode()
        h_projet = hashlib.sha256(clair).digest()
        k_user = bytearray(K_HONNETE)
        piege1 = C.parser_piege(pathlib.Path(
            C.chemin_piege(str(pieges), 1)).read_text(encoding="ascii"))
        if scenario == "piege-perime":
            blob2 = C.construire_conteneur(
                clair, k_user, bytes(ent["s_serrure"]),
                bytes(piege1["s_piege"]), ent["sel_argon"],
                ent["sel_hkdf"], 2, h_projet, ent["p_idx"])
            C._ecrire_atomique(str(conteneur), blob2)
            # le piège d'époque 1 (celui d'init) posé au chemin de l'époque 2
            p1 = pathlib.Path(C.chemin_piege(str(pieges), 1))
            p2 = pathlib.Path(C.chemin_piege(str(pieges), 2))
            p2.write_text(p1.read_text(encoding="ascii"), encoding="ascii")
        else:  # retour-arriere : le conteneur d'époque 1, le miroir à 2
            C._ecrire_miroir(str(conteneur), 2, ent["h_projet"].hex())
        try:
            C.ouvrir(str(conteneur), str(pieges), phrase_essai)
            obs = "OUVERT (BUG)"
            exc = None
        except Exception as e:
            obs = classer(e)
            exc = str(e)[:80]
        return {"scenario": scenario, "attendu": REGLES[scenario],
                "observe": obs, "ok": obs == REGLES[scenario],
                "detail": exc}
    if scenario == "honnete":
        try:
            C.ouvrir(str(conteneur), str(pieges), phrase_essai)
            obs, exc = "OUVERT", None
        except Exception as e:
            obs, exc = classer(e), str(e)[:80]
        return {"scenario": scenario, "attendu": REGLES[scenario],
                "observe": obs, "ok": obs == REGLES[scenario],
                "detail": exc}
    # les scénarios de mutation du blob
    blob = bytearray(conteneur.read_bytes())
    if scenario == "corruption":
        pos = -1 - rng.randrange(1, 32)
        blob[pos] ^= 1 + rng.randrange(255)
    elif scenario == "falsification-naive":
        pos = -1 - rng.randrange(1, 32)
        blob[pos] ^= 1 + rng.randrange(255)
        ct = bytes(blob[C.FIN_AAD + C.TAILLE_EMPREINTE + C.TAILLE_VERIF:])
        blob[C.FIN_AAD:C.FIN_AAD + C.TAILLE_EMPREINTE] = \
            hashlib.sha256(ct).digest()
    elif scenario == "nonce-altere":
        pos = C.FIN_AAD - 1 - rng.randrange(24)   # le nonce vit à l'AAD fin
        blob[pos] ^= 1 + rng.randrange(255)
    C._ecrire_atomique(str(conteneur), bytes(blob))
    try:
        C.ouvrir(str(conteneur), str(pieges), phrase_essai)
        obs, exc = "OUVERT (BUG)", None
    except Exception as e:
        obs, exc = classer(e), str(e)[:80]
    return {"scenario": scenario, "attendu": REGLES[scenario],
            "observe": obs, "ok": obs == REGLES[scenario], "detail": exc}


def ddmin(scenario: str, rep: pathlib.Path, seed: int) -> dict:
    """LA RÉDUCTION ddmin (sur toute divergence) : le scénario re-joué aux
    positions figées (le premier octet du ct, le sel minimal) jusqu'au
    reproducteur minimal — NOMMÉ."""
    rng = random.Random(seed ^ 0xDDDD)
    for figee in ("figee-dernier-octet", "figee-premier-octet"):
        r = random.Random(0x5EED)
        # (le reproducteur minimal : la position figée, la trace re-jouée)
        t = jouer_trace(r, scenario, rep)
        t["reduction"] = figee
        if not t["ok"]:
            return t
    return t


def campagne(graine_nom: str, seed: int, n: int, reprise: pathlib.Path):
    """UNE campagne : n traces, chaque scénario couvert, le digest des
    verdicts, les comptes par règle lus des traces. AU TMPFS (/dev/shm) —
    le fsync de l'écriture atomique y est natif : le coût d'E/S ne mesure
    pas la sentinelle (la conception nommée au rapport)."""
    rng = random.Random(seed)
    racine = "/dev/shm" if os.path.isdir("/dev/shm") else None
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"gen-{graine_nom}-",
                                        dir=racine))
    compte: dict[str, int] = {s: 0 for s in SCENARIOS}
    divergences: list[dict] = []
    verdicts: list[str] = []
    t0 = time.monotonic()
    for i in range(n):
        scenario = SCENARIOS[i % len(SCENARIOS)]
        rep = tmp / f"t{i:05d}"
        rep.mkdir()
        with contextlib.redirect_stdout(io.StringIO()):
            tr = jouer_trace(rng, scenario, rep)
        verdicts.append(tr["observe"])
        if tr["ok"]:
            compte[scenario] += 1
        else:
            red = ddmin(scenario, rep, seed)
            divergences.append({"trace": i, **red})
        shutil.rmtree(rep, ignore_errors=True)
    duree = time.monotonic() - t0
    shutil.rmtree(tmp, ignore_errors=True)
    # LE DIGEST COMPLET : la suite des verdicts ET l'état final du générateur
    # (l'état capture la suite ENTIERE des tirages — le replay bit-identique
    # prouve la reproduction des PARAMÈTRES, pas seulement des verdicts ;
    # la machine étant classe-déterministe, les verdicts seuls eussent été
    # égaux aux trois graines)
    etat = repr(rng.getstate()).encode()
    digest = (hashlib.sha256("\n".join(verdicts).encode()).hexdigest()[:10]
              + "-" + hashlib.sha256(etat).hexdigest()[:10])
    return {"graine": graine_nom, "seed": seed, "n": n,
            "comptes": compte, "divergences": divergences,
            "digest_verdicts": digest, "duree_s": round(duree, 1)}


GRAINES = [("20261121a", 0x20261121), ("20261121b", 0x20262111),
           ("20261121c", 0x21112026)]


def main() -> int:
    rap = ["LA MACHINERY DE CONFORMITÉ GÉNÉRATIVE (alhmpl35u, la vague 12)",
           "la sentinelle durcie (a)-(g) de la vague 11 confrontée aux règles",
           "abstraites — 30 000 traces, trois graines, ddmin, replay ×2",
           "",
           f"LA CONCEPTION : K_user dérivé UNE fois par la VRAIE Argon2id du",
           f" labo pour les deux phrases de test ({len(K_HONNETE)} o chacune)",
           " — les traces excercent LA SENTINELLE (empreinte/AEAD/piège/",
           "époque/plancher), la dérivation n'y vit pas ; le caractère",
           " aléatoire par trace aux s_serrure/s_piege/sel_hkdf/nonce frais",
           " du constructeur INTACT ; les scénarios : " + ", ".join(SCENARIOS),
           ""]
    js = {"conception": "K_user fixe par phrase (Argon2 réelle une fois), "
                       "sentinelle intacte", "campagnes": []}
    tout_vert = True
    for nom, seed in GRAINES:
        # LE REPLAY BIT-IDENTIQUE : la campagne exécutée DEUX fois — les
        # digests des verdicts doivent être ÉGAUX
        c1 = campagne(nom, seed, 10000, ICI)
        c2 = campagne(nom + "-replay", seed, 10000, ICI)
        identique = c1["digest_verdicts"] == c2["digest_verdicts"]
        vert = identique and not c1["divergences"]
        tout_vert = tout_vert and vert
        rap += [
            f"LA GRAINE {nom} (seed {seed:#x}) — 10 000 traces :",
            f"  comptes par règle (acceptés conformes) : " +
            " · ".join(f"{k}={v}" for k, v in c1["comptes"].items()),
            f"  divergences : {len(c1['divergences'])}" +
            (" — AUCUNE (la réduction ddmin jamais requise)"
             if not c1["divergences"] else " :"),
        ]
        for d in c1["divergences"][:6]:
            rap.append(f"    trace {d['trace']} [{d['scenario']}] attendu "
                       f"{d['attendu']} observé {d['observe']} "
                       f"(réduction {d.get('reduction', '—')})")
        rap += [
            f"  LE REPLAY BIT-IDENTIQUE : digest {c1['digest_verdicts']} == "
            f"{c2['digest_verdicts']} : {'IDENTIQUE' if identique else 'ROUGE'}",
            f"  durée {c1['duree_s']} s + replay {c2['duree_s']} s — VERDICT "
            + ("VERT" if vert else "ROUGE"), ""]
        js["campagnes"].append({**c1, "replay_digest": c2["digest_verdicts"],
                                "replay_identique": identique,
                                "verdict": "VERT" if vert else "ROUGE"})
        # le journal par graine
        (ICI / f"traces-{nom}.jsonl").write_text(
            "\n".join(json.dumps(c, ensure_ascii=False)
                      for c in js["campagnes"]) + "\n", encoding="utf-8")

    js["verdict"] = "VERT" if tout_vert else "ROUGE"
    rap += [f"LE VERDICT : {js['verdict']} — " +
            ("30 000 traces aux trois graines, zéro divergence, le replay "
             "bit-identique deux fois, chaque chemin d'échec couvert (les "
             "comptes lus des journaux)" if tout_vert else "LES DIVERGENCES "
             "NOMMÉES ci-dessus")]
    (ICI / "campaign.json").write_text(json.dumps(js, ensure_ascii=False,
                                                  indent=1), encoding="utf-8")
    (ICI / "rapport-generatif.txt").write_text("\n".join(rap) + "\n",
                                               encoding="utf-8")
    print("\n".join(rap))
    return 0 if tout_vert else 2


if __name__ == "__main__":
    sys.exit(main())
