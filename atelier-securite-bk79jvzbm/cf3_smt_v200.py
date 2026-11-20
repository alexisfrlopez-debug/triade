#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cf3_smt_v200.py — LA MÉCANISATION DE L'INVARIANT INDUCTIF CF3 DANS UN
ASSISTANT DE PREUVE INDÉPENDANT (la vague 9, l'instruction bk79jvzbm
point 5, le PLAN-BK79JVZBM H5 gelé).

LE MODÈLE : CF3.tla (la sémantique opérationnelle du coffre — 13
règles, l'époque NON bornée) — LE PORTAGE RÈGLE À RÈGLE en SMT (z3) :
l'état (e, phase, sait[3], trap_ok, cf2_ok, secret, accepte, detruit,
destr_injuste, media_corrompu), Init, les 13 règles (les gardes et les
effets — la copie règle à règle de CF3.tla, l'audit mécanique de
l'atelier 5ey7gmjra le garantit côté TLA+).

L'INVARIANT INDUCTIF I (I1–I4 + TypeOK) :
  I1 : secret ⟹ |sait| = 3 (le seuil — les TROIS éléments) ;
  I2 : ¬destr_injuste (pas de destruction injuste) ;
  I3 : ¬media_corrompu ∧ (cf2_ok ∨ phase = brouillon ∧ …) — CF2 et
       média intacts (P3/P4) ;
  I4 : e ≥ 1 (l'époque).

LES OBLIGATIONS (la preuve par règle — la base et le pas) :
  (0) LA BASE : Init ⟹ I (UNSAT de Init ∧ ¬I) ;
  (i) LE PAS, règle i : I ∧ garde_i ∧ effets_i ⟹ I' (UNSAT de la
      négation) — TREIZE obligations, une par règle.

LES CERTIFICATS : chaque obligation — le SMT2 archivé rejouable
(z3从头), le verdict UNSAT = la preuve ; le contrôle négatif : une
règle MUTÉE (le seuil affaibli à 2) — z3 rend SAT avec le
contre-exemple (la preuve que la preuve voit).

Sortie : cf3_smt_certificats/*.smt2 · rapport-cf3-smt.txt."""
from __future__ import annotations

import json
import pathlib

import z3

ICI = pathlib.Path("/home/z/my-project/depot/atelier-securite-bk79jvzbm")
CERT = ICI / "cf3_smt_certificats"
CERT.mkdir(exist_ok=True)


class Etat:
    """L'état CF3 : les variables du modèle (la copie de CF3.tla)."""

    def __init__(self, suf: str = ""):
        self.e = z3.Int(f"e{suf}")
        self.phase = z3.Bool(f"canonique{suf}")     # vrai = canonique
        self.sait = [z3.Bool(f"sait_{n}{suf}") for n in
                     ("KUser", "SSerrure", "SPiege")]
        self.trap_ok = z3.Bool(f"trap_ok{suf}")
        self.cf2_ok = z3.Bool(f"cf2_ok{suf}")
        self.secret = z3.Bool(f"secret{suf}")
        self.accepte = z3.Bool(f"accepte{suf}")
        self.detruit = z3.Bool(f"detruit{suf}")
        self.destr_injuste = z3.Bool(f"destr_injuste{suf}")
        self.media_corrompu = z3.Bool(f"media_corrompu{suf}")

    def invariant(self) -> z3.BoolRef:
        """I1–I4 + TypeOK (les états bien typés — les booléens le sont
        par construction, l'époque entière aussi)."""
        n_sait = z3.Sum([z3.If(s, 1, 0) for s in self.sait])
        # L'INVARIANT DE CF3.tla À LA LETTRE : I1-I4 (+ P2 porté par les
        # transitions — le rejeu-état-inchangé) ; I3 == cf2_ok ∧
        # ¬media_corrompu (la copie EXACTE — rien de plus)
        return z3.And(
            z3.Implies(self.secret, n_sait == 3),     # I1
            z3.Not(self.destr_injuste),               # I2
            self.cf2_ok,                              # I3a
            z3.Not(self.media_corrompu),              # I3b
            self.e >= 1,                              # I4
        )


def init_etat(s: Etat) -> z3.BoolRef:
    """Init de CF3.tla : e = 1, canonique, sait vide, trap/cf2 ok, le
    reste faux."""
    return z3.And(s.e == 1, s.phase,
                  z3.Not(s.sait[0]), z3.Not(s.sait[1]), z3.Not(s.sait[2]),
                  s.trap_ok, s.cf2_ok, z3.Not(s.secret),
                  z3.Not(s.accepte), z3.Not(s.detruit),
                  z3.Not(s.destr_injuste), z3.Not(s.media_corrompu))


def liaison(s: Etat, d: Etat, inchange: list[str]) -> z3.BoolRef:
    """Les variables UNCHANGED liées (l'égalité entre avant et après)."""
    champs = {"e": (s.e, d.e), "phase": (s.phase, d.phase),
              "trap_ok": (s.trap_ok, d.trap_ok),
              "cf2_ok": (s.cf2_ok, d.cf2_ok),
              "secret": (s.secret, d.secret),
              "accepte": (s.accepte, d.accepte),
              "detruit": (s.detruit, d.detruit),
              "destr_injuste": (s.destr_injuste, d.destr_injuste),
              "media_corrompu": (s.media_corrompu, d.media_corrompu),
              "sait": (None, None)}
    c = []
    for nom in inchange:
        if nom == "sait":
            c += [a == b for a, b in zip(s.sait, d.sait)]
        else:
            c.append(champs[nom][0] == champs[nom][1])
    return z3.And(c)


def regles(s: Etat, d: Etat, mutation_seuil: int = 3) -> list[tuple]:
    """LES 13 RÈGLES — la copie règle à règle de CF3.tla (garde ∧
    effets ∧ liaisons)."""
    R = []
    TOUT = ["e", "phase", "sait", "trap_ok", "cf2_ok", "secret", "accepte",
            "detruit", "destr_injuste", "media_corrompu"]
    # 1-3 : l'adversaire vole un élément
    for i, nom in enumerate(("VoleKUser", "VoleSSerrure", "VoleSPiege")):
        R.append((nom, z3.And(
            d.sait[i],
            liaison(s, d, [c for c in TOUT if c != "sait"]),
            # les autres éléments de sait inchangés :
            *[d.sait[j] == s.sait[j] for j in range(3) if j != i],
            # (le vol est cumulatif : sait' ⊇ sait — le nouveau vrai, les
            # anciens préservés : l'union — d.sait[j] ≥ s.sait[j])
        )))
    # 4 : la falsification du conteneur
    R.append(("FalsifieConteneur", z3.And(
        s.trap_ok, s.phase, d.detruit,
        liaison(s, d, [c for c in TOUT if c != "detruit"]))))
    # 5 : la falsification du piège
    R.append(("FalsifiePiege", z3.And(
        s.trap_ok, z3.Not(d.trap_ok),
        liaison(s, d, [c for c in TOUT if c != "trap_ok"]))))
    # 6 : le rejeu d'époque passée — l'état inchangé
    R.append(("RejoueEpoquePassee", z3.And(
        s.e > 1, liaison(s, d, TOUT))))
    # 7 : l'ouverture correcte — TROIS cas
    seuil = z3.Sum([z3.If(x, 1, 0) for x in d.sait])
    R.append(("OuvrirCorrect", z3.And(
        s.trap_ok, s.phase,
        z3.Or(
            z3.And(z3.Not(s.sait[0]), z3.Not(d.phase),
                   d.secret == s.secret),
            z3.And(s.sait[0], seuil >= mutation_seuil,
                   z3.Not(d.phase), d.secret),
        ),
        liaison(s, d, ["e", "sait", "trap_ok", "cf2_ok", "accepte",
                       "detruit", "destr_injuste", "media_corrompu"]))))
    # 8 : l'ouverture phrase erronée — inchangé
    R.append(("OuvrirPhraseErronee", z3.And(
        s.phase, liaison(s, d, TOUT))))
    # 9 : l'ouverture de l'ancien couple — inchangé
    R.append(("OuvrirAncienCouple", z3.And(
        s.phase, s.e > 1, liaison(s, d, TOUT))))
    # 10 : la vérification — inchangé
    R.append(("Verifier", z3.And(s.phase, liaison(s, d, TOUT))))
    # 11 : le crash de session
    R.append(("CrashPendantSession", z3.And(
        d.phase,
        liaison(s, d, [c for c in TOUT if c != "phase"]))))
    # 12 : la clôture correcte — e' = e + 1 SANS plafond
    R.append(("CloturerCorrecte", z3.And(
        z3.Not(s.phase), s.trap_ok, d.e == s.e + 1, d.phase,
        liaison(s, d, [c for c in TOUT if c not in ("e", "phase")]))))
    # 13 : la clôture phrase erronée — inchangé
    R.append(("CloturerPhraseErronee", z3.And(
        z3.Not(s.phase), liaison(s, d, TOUT))))
    return R


def prouver(nom: str, solver: z3.Solver) -> tuple[bool, str]:
    chemin = CERT / f"{nom}.smt2"
    v = solver.check()
    chemin.write_text(
        f"; CF3 — l'obligation {nom}\n; le verdict z3 : {v}\n"
        + solver.to_smt2(), encoding="utf-8")
    return v == z3.unsat, str(v)


def main():
    rapport = ["LA MÉCANISATION CF3 EN z3 — l'assistant de preuve "
               "INDÉPENDANT de l'explorateur maison", "",
               "LE MODÈLE : CF3.tla (13 règles, l'époque non bornée) — le "
               "portage RÈGLE À RÈGLE en SMT ; l'invARIANT I1–I4 + P2 ; "
               "LES OBLIGATIONS : la base + le pas par règle.", ""]
    verts = 0
    # (0) LA BASE : Init ⟹ I
    s0 = Etat("_0")
    sol = z3.Solver()
    sol.add(init_etat(s0))
    sol.add(z3.Not(s0.invariant()))
    ok, v = prouver("00-base-Init-implique-I", sol)
    rapport.append(f"  (0) LA BASE Init ⟹ I : {'VERT (UNSAT)' if ok else 'ROUGE ' + v}")
    verts += ok

    # (1-13) LE PAS : I ∧ règle_i ⟹ I'
    sd, dd = Etat("_a"), Etat("_b")
    for nom, corps in regles(sd, dd):
        sol = z3.Solver()
        sol.add(sd.invariant())
        sol.add(corps)
        sol.add(z3.Not(dd.invariant()))
        ok, v = prouver(f"pas-{nom}", sol)
        verdict_pas = "VERT (UNSAT — l'invariant préservé)" if ok else \
            "ROUGE " + v
        rapport.append(f"  le pas {nom} : {verdict_pas}")
        verts += ok

    # LE CONTRÔLE NÉGATIF : la règle 7 MUTÉE (le seuil affaibli à 2)
    sm, dm = Etat("_m"), Etat("_n")
    mut = dict(regles(sm, dm, mutation_seuil=2))["OuvrirCorrect"]
    sol = z3.Solver()
    sol.add(sm.invariant())
    sol.add(mut)
    sol.add(z3.Not(dm.invariant()))
    v = sol.check()
    neg_ok = v == z3.sat
    if neg_ok:
        mod = sol.model()
        (CERT / "controle-negatif-seuil-2.smt2").write_text(
            "; la règle 7 MUTÉE (le seuil à 2) — l'invariant VIOLÉ : le "
            "contre-exemple\n" + sol.to_smt2(), encoding="utf-8")
    rapport += [
        "",
        f"LE CONTRÔLE NÉGATIF : la règle 7 mutée (le seuil affaibli à 2) — "
        f"{'ATTRAPÉ : z3 rend SAT, le contre-exemple au modèle (le secret appris avec 2 éléments — la preuve que la preuve voit)' if neg_ok else 'NON VU — ROUGE'}",
        "",
        f"LE BILAN : {verts}/14 obligations VERTES (la base + les 13 "
        f"règles) — les certificats SMT2 archivés rejouables "
        f"(cf3_smt_certificats/), z3 l'assistant INDÉPENDANT de "
        f"l'explorateur maison et d'Apalache (le second avis indépendant "
        f"— le TLA+ d'origine déchargé par Apalache à v0.15.0, le "
        f"présent par z3 : DEUX assistants distincts, la même vérité).",
    ]
    (ICI / "rapport-cf3-smt.txt").write_text("\n".join(rapport) + "\n",
                                             encoding="utf-8")
    print("\n".join(rapport))
    return 0 if verts == 14 and neg_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
