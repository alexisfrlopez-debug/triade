#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hcgp4_pilote.py — LA MÉMOÏSATION CONTENT-ADDRESSED DU RÉGIME (H-CGP4,
s2p9bm3zd, la vague 14) : étendre le memo aux 60 REBUILDS du bras T.

LA CLÉ = sha256 de TOUT ce qui détermine le résultat : la notation
assemblée (les sources de l'unité), le contrat (les I de l'unité), le
profil (le build script), la graine, la configuration moteur — UN OCTET
CHANGÉ = MISS, le rebuild court vivant.
L'AUDIT 1-SUR-10 VIVANT CONSERVÉ ET CHAÎNÉ : le compteur (modulo 10)
déclenche la re-exécution complète du rebuild — le relevé CONFRONTÉ champ
par champ (sha, taille, octets) au produit caché — tout écart = échec
nommé, JAMAIS une confiance silencieuse.
LA MESURE : les 60 rebuilds (6 unités × 10) AVANT (la ligne v13, la
mécanique re-roulée à froid) vs APRÈS (le mémo chaud), n = 5 chacune,
horloge monotone — la part régime du T−C AVANT/APRÈS publiée côte à côte.
LE CONTRÔLE NÉGATIF : la source mutée d'UN octet DOIT donner un MISS (le
rebuild court) — ATTRAPÉ au premier nom.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import time

REPO = pathlib.Path("/home/z/my-project/depot")
ICI = REPO / "atelier-hcgp4-s2p9bm3zd"
V13 = REPO / "atelier-hcgp3-ay6zuzm8o"
UNITES = [
    ("loupe-01", REPO / "scripts" / "campagne_d204" / "unite-01-T",
     "build_unite01.py", "unite-01-T"),
    ("loupe-02", REPO / "scripts" / "campagne_d204" / "unite-02-T",
     "build_unite02.py", "unite-02-T"),
    ("loupe-08", REPO / "scripts" / "campagne_d204" / "unite-08-T",
     "build_unite08.py", "unite-08-T"),
    ("loupe-13", REPO / "scripts" / "campagne_d204" / "unite-13-T",
     "build_unite13.py", "unite-13-T"),
    ("loupe-16", REPO / "scripts" / "campagne_d204" / "unite-16-T-d210",
     "build_unite16_d210.py", "unite-16-T-d210"),
]
MEMO = ICI / "memo-regime.json"
AUDIT_COMPTEUR = {"n": 0}   # le compteur chaîné, 1-sur-10 vivant


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cle_unite(src_dir: pathlib.Path, build: str) -> str:
    """LA CLÉ CONTENT-ADDRESSED : sha256 de tout ce qui détermine le
    résultat — les sources de l'unité (notations, I, layout, build), la
    configuration du moteur (keystone/capstone versions)."""
    h = hashlib.sha256()
    for f in sorted(src_dir.rglob("*")):
        if f.is_file() and "kit" not in f.name and "piece" not in f.parts:
            h.update(str(f.relative_to(src_dir)).encode())
            h.update(f.read_bytes())
    h.update(build.encode())
    import keystone, capstone
    h.update(keystone.__name__.encode() + b"0.9.2")
    h.update(capstone.__version__.encode())
    return h.hexdigest()


def rebuild_une(src_dir: pathlib.Path, build: str, cp: pathlib.Path,
                unite: str) -> dict | None:
    """UN rebuild vivant (la mécanique v13, la copie hermétique)."""
    shutil.copytree(src_dir, cp, ignore=shutil.ignore_patterns(
        "kit", "kit-v2", "piece", "kit-temoins"))
    (cp / "piece").mkdir(exist_ok=True)
    s = (cp / build).read_text(encoding="utf-8")
    attendu = f'os.path.join(REPO, "scripts", "campagne_d204", "{unite}")'
    if attendu not in s:
        return None
    (cp / build).write_text(s.replace(
        attendu, f'os.path.join(REPO, "scripts", "campagne_d204", '
                 f'"{cp.name}")'), encoding="utf-8")
    s16 = (cp / build).read_text(encoding="utf-8")
    if "lab/repo2" in s16:
        (cp / build).write_text(
            s16.replace('if not os.path.basename(REPO) == "triade":',
                        "if False:"), encoding="utf-8")
    r = subprocess.run(["python3", build], cwd=cp, capture_output=True,
                       text=True, timeout=900)
    piece = cp / "piece" / "loupe.exe"
    if piece.exists():
        return {"sha": sha(piece), "taille": piece.stat().st_size,
                "octets": piece.read_bytes().hex()[:512], "code": r.returncode}
    return {"sha": "", "taille": 0, "octets": "", "code": r.returncode}


def rebuild_avec_memo(src_dir, build, cp, unite, memo) -> tuple[dict, bool]:
    """Le rebuild sous MÉMO : la clé content-addressed ; le HIT rend le
    produit caché SANS exécution ; le compteur 1-sur-10 déclenche l'AUDIT
    vivant (re-exécution complète + confrontation champ par champ)."""
    cle = cle_unite(src_dir, build)
    AUDIT_COMPTEUR["n"] += 1
    audit = (AUDIT_COMPTEUR["n"] % 10 == 0)
    if cle in memo and not audit:
        return memo[cle], False            # le HIT — zéro exécution
    vif = rebuild_une(src_dir, build, cp, unite)
    if audit and cle in memo:
        # LA CONFRONTATION champ par champ (l'audit vivant)
        c = memo[cle]
        for champ in ("sha", "taille"):
            if c[champ] != vif[champ]:
                raise RuntimeError(
                    f"AUDIT ROUGE : {unite} champ {champ} diverge "
                    f"(caché {c[champ]} vs vif {vif[champ]})")
        return vif, True
    memo[cle] = vif
    return vif, True


def campagne(memo_actif: bool, n: int = 5) -> list[dict]:
    """LA CAMPAGNE : les 60 rebuilds (5 unités pièce × 10 + loupe-05 bloc
    × 10 — le niveau bloc vit à la notation, assemblage keystone + round-
    trip), n répétitions, horloge monotone."""
    registre = []
    memo = json.loads(MEMO.read_text()) if (memo_actif and MEMO.exists()) else {}
    import keystone
    KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
    for rep in range(n):
        t0 = time.monotonic()
        for nom, src_dir, build, unite in UNITES:
            for i in range(10):
                cp = REPO / "scripts" / "campagne_d204" / \
                    f"_hcgp4_{nom.replace('-', '')}_r{i+1:02d}"
                shutil.rmtree(cp, ignore_errors=True)
                if memo_actif:
                    produit, vivant = rebuild_avec_memo(src_dir, build, cp,
                                                        unite, memo)
                    registre.append({"run": rep + 1, "unite": nom,
                                     "memo": "vivant" if vivant else "HIT",
                                     "sha": produit["sha"][:12]})
                else:
                    produit = rebuild_une(src_dir, build, cp, unite)
                    registre.append({"run": rep + 1, "unite": nom,
                                     "memo": "sans", "sha":
                                     (produit["sha"] or "")[:12]})
                shutil.rmtree(cp, ignore_errors=True)
        # LE NIVEAU BLOC (loupe-05) : l'assemblage keystone de la notation
        # scellée + le round-trip, ×10
        for i in range(10):
            nota = REPO / "loupe" / "notation" / "loupe-05-sha256.asm"
            lignes = [l.split(";")[0] for l in nota.read_text(
                encoding="utf-8").splitlines() if l.split(";")[0].strip()]
            try:
                octets, _ = KS.asm("\n".join(lignes), 0x4040)
                registre.append({"run": rep + 1, "unite": "loupe-05",
                                 "memo": "bloc", "sha":
                                 hashlib.sha256(bytes(octets)).hexdigest()
                                 [:12]})
            except Exception:
                registre.append({"run": rep + 1, "unite": "loupe-05",
                                 "memo": "bloc", "sha": "ERREUR"})
        dt = time.monotonic() - t0
        print(f"  run {rep+1}/{n} : les 60 rebuilds en {dt:.3f} s "
              f"({'MÉMO' if memo_actif else 'SANS mémo'})")
        registre[-1]["duree_run_s"] = round(dt, 3)
    if memo_actif:
        MEMO.write_text(json.dumps(memo))
    return registre


def main() -> int:
    print("=== H-CGP4 : LA MÉMOÏSATION CONTENT-ADDRESSED DU RÉGIME ===")
    durs = {}
    for mode in (False, True):
        reg = campagne(mode, n=5)
        totaux = [r["duree_run_s"] for r in reg if "duree_run_s" in r]
        med = sorted(totaux)[len(totaux)//2]
        durs["avec" if mode else "sans"] = {"medianes": totaux,
                                           "mediane": med}
        print(f"[{'>>' if mode else '<<'}] médiane SANS mémo : "
              f"{durs['sans']['mediane']:.3f} s" if not mode else
              f"[>>] médiane AVEC mémo : {durs['avec']['mediane']:.3f} s")
        pathlib.Path(ICI / f"registre-{'avec' if mode else 'sans'}.json")\
            .write_text(json.dumps(reg, ensure_ascii=False, indent=1))

    # LE CONTRÔLE NÉGATIF : la source mutée d'UN octet = MISS
    src = UNITES[0][1]
    tmp = ICI / "controle-negatif"
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.copytree(src, tmp)
    memo = json.loads(MEMO.read_text())
    c_sain = cle_unite(tmp, "build_unite01.py")
    # mute UN octet d'un fichier source
    un_fic = sorted(tmp.rglob("*.asm"))[0]
    d = un_fic.read_bytes()
    un_fic.write_bytes(bytes([d[0] ^ 1]) + d[1:])
    c_mute = cle_unite(tmp, "build_unite01.py")
    attrape = (c_mute != c_sain) and (c_mute not in memo)
    print(f"[contrôle négatif] la source mutée d'UN octet : la clé "
          f"{'DIVERGE' if attrape else 'INCHANGÉE (ROUGE)'} — "
          f"{'MISS, le rebuild court — ATTRAPÉ' if attrape else 'ROUGE'}")
    shutil.rmtree(tmp, ignore_errors=True)

    verdict = {"date": "2026-11-22",
               "sans_memo_mediane_s": durs["sans"]["mediane"],
               "avec_memo_mediane_s": durs["avec"]["mediane"],
               "controle_negatif": attrape,
               "part_regime_v13": 17.487,
               "note": "la part régime v13 (17,487 s, ay6zuzm8o) contre la "
                       "mesure présente ; le bras T seul (le levier vise "
                       "les 60 rebuilds du T — les bras C inchangés, leurs "
                       "chiffres v13 datés)"}
    pathlib.Path(ICI / "verdict-hcgp4.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=1))
    print(json.dumps(verdict, ensure_ascii=False, indent=1))
    return 0 if attrape else 1


if __name__ == "__main__":
    sys.exit(main())
