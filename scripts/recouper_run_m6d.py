#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run_m6d.py — LE RECOUP POST-MORTEM DU RUN M6-(d) (D138/D145/D148 :
verdict sur pièces, jamais sur console). Le labo juge les TROIS pièces
rapatriées du coffre /test/preuves-m6 (md5 Drive contrôlés par le rapatriement,
re-contrôlés ici) :

  temoin-m6d.txt            l'environnement de la machine du développeur ;
  scenario-m6d-journal.log  le run entier, ligne à ligne ;
  VERDICT-run-m6d.txt       le verdict post-mortem du scénario.

Chaque contrôle tranché binaire (PASS/ÉCHEC nommé, fail-closed) :
  A. les trois pièces présentes, md5 locaux == métadonnées Drive RE-LUES ;
  B. le TÉMOIN : le corpus relu == LE scellé 0.7.0-rc.1 du dépôt (sha
     re-calculé depuis unix/corpus AU geste même), un noyau AUTRE que
     celui du laboratoire (l'exigence du kit), WSL2 (D149), ASLR complet
     (randomize_va_space=2 — D146) ;
  C. le JOURNAL : la bannière du scénario, le témoin EMBARQUÉ == le fichier
     témoin (cohérence croisée), exactement 16 PASS et zéro ÉCHEC, les 16
     constats AUX NOMS ATTENDUS DE LA SOURCE (le juge est le code), le
     rituel ×3 au code 0, l'ARITHMÉTIQUE des comptes (800+400==1200,
     778+560==1338, 1338 indices exacts, octets émis == attendus) ;
  D. le VERDICT : l'en-tête, la date == témoin, « 16/16 constats PASS », les
     16 constats == ceux du journal LIGNE POUR LIGNE, « VERDICT : VERT » ;
  E. LE LABO PARLE : l'artefact scellé du dépôt n'a pas bougé (sha
     dd14195c… re-calculé), le noyau du témoin ≠ le noyau du labo (lu au
     geste même).

Si tout est vert : « RECOUP : VERT — les pièces établissent le critère
M6-(d) » (le scellage final 0.7.0 est débloqué). Le verdict du recoup est
écrit à côté des pièces : VERDICT-recoup-m6d.txt.

Usage : python3 scripts/recouper_run_m6d.py
Code de sortie : 0 = recoup VERT ; 1 = écart nommé ; 2 = erreur fatale.
"""

import datetime
import hashlib
import pathlib
import platform
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
PIECES = pathlib.Path("/home/z/my-project/download/preuves-run-m6d")
ARTEFACT = REPO / "unix" / "corpus"

SHA_SCELLE = "dd14195c9da5e9b990e8f9b141eedd6574bb8ecc793ffdd5b67edb71b81ddff7"

# Les 16 constats attendus — les préfixes STABLES des noms, extraits de la
# source du scénario (unix/terrain/scenario-m6d.py, les constat() du run ;
# l'ordre est celui du code).
ATTENDUS = [
    "T0 : le corpus est LE scellé 0.7.0-rc.1 relu",
    "T1 : le rituel exact aux TROIS exécutions réelles",
    "T1b : la base FIGÉE recoupée",
    "T2a : l'apply et le rollback PENDANT le trafic rendent 0",
    "T2a : les 1200 usages rendent leur verdict exact",
    "T2a : le journal COHÉRENT — le flux OCTET POUR OCTET",
    "T2b : la PREUVE DE VIE de l'ouvrier AVANT la bascule",
    "T2b : les TROIS fenêtres rendent 0",
    "T2b : le conducteur journalise sous CHAQUE version",
    "T2b : l'ouvrier :",
    "T2b : la bascule était VIVANTE",
    "T2b : le conducteur vu du flux",
    "T2c : l'entrée du journal restaurée OCTET POUR OCTET",
    "T2d : le refus EACCES EST LE NOYAU de la machine",
    "T3 : le FICHIER artefact n'a pas bougé d'un octet",
    "T3 : le rituel REJOUÉ après la démonstration",
]


class Recoup:
    def __init__(self):
        self.lignes: list[str] = []
        self.ok = True

    def passe(self, nom: str, ok: bool, detail: str = "") -> bool:
        ok = bool(ok)
        self.ok = self.ok and ok
        self.lignes.append(f"[recoup-m6d] {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        return ok


def md5f(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def main() -> int:
    r = Recoup()
    r.lignes.append("[recoup-m6d] === RECOUP LABO DU RUN M6-(d) — "
                    "verdict sur pièces (D138/D145/D148) ===")
    r.lignes.append(f"[recoup-m6d] recoup rendu le "
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"au laboratoire")

    # ---- A. les trois pièces, md5 re-contrôlés contre le coffre ----------
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m6") or {}
        distants = ds.list_folder(preuves["id"]) if preuves.get("id") else {}
    except Exception as exc:  # noqa: BLE001
        print(f"[recoup-m6d] ERREUR FATALE : coffre illisible : {exc}",
              file=sys.stderr)
        return 2
    noms = ["temoin-m6d.txt", "scenario-m6d-journal.log", "VERDICT-run-m6d.txt"]
    for nom in noms:
        local = PIECES / nom
        if not local.exists():
            print(f"[recoup-m6d] ERREUR FATALE : pièce locale absente : {nom}",
                  file=sys.stderr)
            return 2
        d = distants.get(nom)
        r.passe(f"A : {nom} au coffre, md5 re-contrôlé",
                bool(d) and md5f(local) == (d.get("md5Checksum") or "").lower(),
                f"md5 {md5f(local)[:12]}…")

    temoin = (PIECES / "temoin-m6d.txt").read_text(encoding="utf-8")
    journal = (PIECES / "scenario-m6d-journal.log").read_text(encoding="utf-8")
    verdict = (PIECES / "VERDICT-run-m6d.txt").read_text(encoding="utf-8")
    jl = [l.rstrip("\n") for l in journal.splitlines()]
    vl = [l.rstrip("\n") for l in verdict.splitlines()]

    # ---- B. le témoin -----------------------------------------------------
    champs = {}
    for l in temoin.splitlines():
        if " : " in l and not l.startswith(" "):
            k, v = l.split(" : ", 1)
            champs.setdefault(k.strip(), v.strip())
    sha_lu = champs.get("corpus", "").replace("sha256 ", "")
    r.passe("B1 : le témoin porte LE scellé 0.7.0-rc.1 (sha == artefact du dépôt "
            "re-calculé AU geste même)",
            sha_lu == SHA_SCELLE
            and hashlib.sha256(ARTEFACT.read_bytes()).hexdigest() == SHA_SCELLE,
            f"corpus {sha_lu[:16]}…")
    r.passe("B1b : l'empreinte attendue EMBARQUÉE == l'empreinte lue "
            "(l'assertion du kit a tranché AVANT tout geste)",
            "attendu " + SHA_SCELLE in temoin.replace("\n            :", ""),
            f"attendu dd14195c…")
    release = champs.get("uname", "")
    import re as _re
    m = _re.search(r"release='([^']+)'", release)
    noyau_temoin = m.group(1) if m else "?"
    noyau_labo = platform.uname().release
    r.passe("B2 : le noyau du témoin est UN AUTRE noyau que celui du "
            "laboratoire (l'exigence du kit)",
            noyau_temoin != noyau_labo and noyau_temoin != "?",
            f"témoin {noyau_temoin} ≠ labo {noyau_labo}")
    r.passe("B3 : WSL2 — le noyau Linux complet de la machine Windows (D149)",
            champs.get("wsl", "").startswith("OUI"), champs.get("wsl", "?"))
    r.passe("B4 : l'ASLR noyau COMPLET (randomize_va_space=2 — D146, la base "
            "choisie par le NOYAU à chaque run)",
            "randomize_va_space=2" in champs.get("aslr-noyau", ""),
            champs.get("aslr-noyau", "?"))
    r.passe("B5 : la date du témoin consignée (le run est daté sur pièces)",
            champs.get("date", "").startswith("2026-11-04"),
            champs.get("date", "?"))

    # ---- C. le journal ------------------------------------------------------
    r.passe("C1 : la bannière du scénario en tête du journal",
            jl and "=== SCÉNARIO TERRAIN M6-(d) — le patch en production ==="
            in jl[0], jl[0][:60] if jl else "journal vide")
    r.passe("C2 : le témoin EMBARQUÉ au journal == le fichier témoin "
            "(cohérence croisée des pièces)",
            all(any(l.strip().endswith(f" : {v}") or v in l for l in jl[:12])
                for v in [champs.get("date", "@@"), sha_lu])
            and noyau_temoin in journal,
            "date, uname, corpus sha retrouvés")
    passes = [l for l in jl if l.startswith("[m6d] PASS : ")]
    echecs = [l for l in jl if l.startswith("[m6d] ECHEC")]
    r.passe("C3 : exactement 16 constats PASS, zéro ÉCHEC au journal",
            len(passes) == 16 and len(echecs) == 0,
            f"{len(passes)} PASS, {len(echecs)} échec(s)")
    nommes = [l[len("[m6d] PASS : "):] for l in passes]
    mal_nommes = [(i, a, n) for i, (a, n) in enumerate(zip(nommes, ATTENDUS))
                  if not a.startswith(n)]
    r.passe("C4 : les 16 constats AUX NOMS DE LA SOURCE, dans l'ordre du code "
            "(unix/terrain/scenario-m6d.py — le juge est le code)",
            len(passes) == 16 and not mal_nommes,
            "16/16 préfixes exacts" if not mal_nommes
            else f"divergence au rang {mal_nommes[0][0]}")
    r.passe("C5 : le rituel TROIS exécutions réelles au code 0",
            sum(1 for l in jl if "run " in l and "code=0" in l) == 3,
            "3 × code=0")
    # l'arithmétique des comptes (les nombres des détails, recoupés)
    import re as _re2
    m6 = next((l for l in passes if "14890" in l or "o émis" in l), "")
    m10 = next((l for l in passes if "lignes ENTIÈRES" in l), "")
    m11 = next((l for l in passes if "la bascule était VIVANTE" in l), "")
    n_ouv = int(_re2.search(r"l'ouvrier : (\d+) lignes", m10).group(1)) if m10 else -1
    idx = (_re2.search(r"indices 0\.\.(\d+)", m10) is not None
           and int(_re2.search(r"indices 0\.\.(\d+)", m10).group(1)))
    mm = _re2.search(r"(\d+) lignes v1, (\d+) lignes v2", m11)
    v1, v2 = (int(mm.group(1)), int(mm.group(2))) if mm else (-1, -1)
    mo = _re2.search(r"(\d+) o émis == (\d+) o attendus", m6)
    emis, attendus_o = (int(mo.group(1)), int(mo.group(2))) if mo else (-1, -1)
    ok_ari = (n_ouv == idx + 1 and v1 + v2 == n_ouv and emis == attendus_o
              and v1 > 0 and v2 > 0 and n_ouv > 0)
    r.passe("C6 : l'arithmétique des comptes (ouvrier n == indices 0..n-1 ; "
            "v1+v2 == n ; octets émis == attendus)",
            ok_ari,
            f"ouvrier {n_ouv} lignes (indices 0..{idx}), {v1} v1 + {v2} v2 "
            f"== {v1 + v2}, {emis} o == {attendus_o} o")
    m2a = next((l for l in passes if "le journal COHÉRENT" in l), "")
    mm2 = _re2.search(r"(\d+) lignes v1, (\d+) lignes v2", m2a)
    s1, s2 = (int(mm2.group(1)), int(mm2.group(2))) if mm2 else (-1, -1)
    r.passe("C6b : le trafic en session (800 v1 + 400 v2 == 1200 usages, "
            "l'apply/le rollback ENTRE les usages)",
            s1 == 800 and s2 == 400 and s1 + s2 == 1200,
            f"{s1} v1 + {s2} v2 == {s1 + s2}")

    # ---- D. le verdict ------------------------------------------------------
    r.passe("D1 : l'en-tête du verdict + la date == le témoin",
            vl and vl[0] == "=== VERDICT RUN M6-(d) — le patch en production ==="
            and len(vl) > 1 and vl[1] == champs.get("date", "@"),
            vl[1] if len(vl) > 1 else "?")
    r.passe("D2 : « 16/16 constats PASS » écrit noir sur blanc",
            any(l.strip() == "16/16 constats PASS" for l in vl), "16/16")
    vconst = [l[len("[m6d] "):] for l in vl
              if l.startswith("[m6d] ") and any(l.startswith("[m6d] " + a)
              for a in ("T0", "T1", "T2", "T3"))]
    r.passe("D3 : les 16 constats du verdict == les 16 PASS du journal, "
            "LIGNE POUR LIGNE (le post-mortem reprend le run exact)",
            vconst == nommes,
            f"{len(vconst)} constats, identiques" if vconst == nommes
            else f"{len(vconst)} vs {len(nommes)}")
    r.passe("D4 : « VERDICT : VERT » — le verdict du scénario sur pièces",
            any(l.strip() == "VERDICT : VERT" for l in vl), "VERT")

    # ---- E. le labo parle ----------------------------------------------------
    sha_repo = hashlib.sha256(ARTEFACT.read_bytes()).hexdigest()
    r.passe("E1 : l'artefact scellé du dépôt INTACT au geste même "
            "(le fichier que le développeur a exécuté est LE scellé du labo)",
            sha_repo == SHA_SCELLE == sha_lu, f"sha256 {sha_repo[:16]}…")
    r.passe("E2 : le run a vécu sur UN AUTRE noyau que le témoin du labo "
            "(la vigilance D146 satisfaite : ni le même noyau, ni une émulation)",
            noyau_temoin != noyau_labo,
            f"{noyau_temoin} vs {noyau_labo}")

    # ---- le jugement ---------------------------------------------------------
    for l in r.lignes:
        print(l)
    jugement = ("RECOUP : VERT — les pièces établissent le critère M6-(d) : "
                "le patch en production démontré SUR UN AUTRE NOYAU, le "
                "scellage final 0.7.0 est débloqué (--sceller-final)"
                if r.ok else
                "RECOUP : ÉCHEC NOMMÉ — au moins une pièce diverge, le "
                "scellage final 0.7.0 est REFUSÉ (fail-closed)")
    print(f"[recoup-m6d] {jugement}")

    sortie = ["=== RECOUP LABO DU RUN M6-(d) — verdict sur pièces "
              "(D138/D145/D148) ===",
              f"rendu le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
              "au laboratoire (noyau " + noyau_labo + ")",
              "les pièces : /test/preuves-m6/ (temoin-m6d.txt, "
              "scenario-m6d-journal.log, VERDICT-run-m6d.txt), md5 contrôlés",
              ""] + r.lignes[1:] + ["", jugement]
    (PIECES / "VERDICT-recoup-m6d.txt").write_text(
        "\n".join(sortie) + "\n", encoding="utf-8")
    print(f"[recoup-m6d] le verdict du recoup écrit : "
          f"{PIECES / 'VERDICT-recoup-m6d.txt'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
