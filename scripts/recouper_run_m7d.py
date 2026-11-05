#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run_m7d.py — LE RECOUP POST-MORTEM DU RUN M7-(d) (D138/D145/D148 :
verdict sur pièces, jamais sur console ; D154 : sur pièces croisées). Le labo
juge les TROIS pièces rapatriées du coffre /test/preuves-m7 (md5 Drive
contrôlés par le rapatriement, RE-contrôlés ici) :

  temoin-m7d.txt            l'environnement de la machine du développeur ;
  scenario-m7d-journal.log  le run entier, ligne à ligne ;
  VERDICT-run-m7d.txt       le verdict post-mortem du scénario.

LE JUGE EST LE CODE : les constantes et le générateur déterministe de la
transcription sont IMPORTÉS DEPUIS LA SOURCE du scénario
(riscv/terrain/scenario-m7d.py) et l'attendu est RECALCULÉ AU GESTE MÊME.

Chaque contrôle tranché binaire (PASS/ÉCHEC nommé, fail-closed) :
  A. les trois pièces présentes, md5 locaux == métadonnées Drive RE-LUES ;
  B. le TÉMOIN : le corpus relu == LE scellé 0.8.0-rc.1 du dépôt (sha
     re-calculé depuis riscv/corpus AU geste même), le demo == le
     démonstrateur f72001 (sha re-calculé), l'instrument == le qemu STATIQUE
     du kit (md5 embarqué), la réserve D149 NOMMÉE, un noyau AUTRE que celui
     du laboratoire (l'exigence du kit), la date consignée ;
  C. le JOURNAL : la bannière, l'en-tête == le témoin (cohérence croisée),
     exactement 16 PASS et zéro ÉCHEC, les 16 constats AUX NOMS ATTENDUS DE
     LA SOURCE (dans l'ordre du code), le rituel ×3 au code 0 (60 o ==
     len(RITUEL) re-calculé), L'ARITHMÉTIQUE RECOMPTÉE DEPUIS LA SOURCE
     (1200 usages, apply 399/400, retour 799/800, 800 v1 + 400 v2, la
     transcription attendue re-générée == 15425 o, le DEP == 4290 o,
     SIGSEGV -11, la falsification rompue à DEMO_ADDRS[0] essai n°1) ;
  D. le VERDICT : l'en-tête, « constats : 16 PASS / 0 ÉCHEC », les 16
     constats == ceux du journal LIGNE POUR LIGNE, l'instrument == le
     journal, les frontières nommées, « VERDICT : VERT » ;
  E. LE LABO PARLE : les artefacts scellés du dépôt INTACTS au geste même
     (sha re-calculés == témoins — le fichier que le développeur a exécuté
     est LE scellé du labo), le noyau du témoin ≠ le noyau du labo (lu au
     geste même), le kit du coffre == le kit éprouvé (md5 4d17f3fa…).

Si tout est vert : « RECOUP : VERT — les pièces établissent le critère
M7-(d) » (le scellage final 0.8.0 est débloqué). Le verdict du recoup est
écrit à côté des pièces : VERDICT-recoup-m7d.txt.

Usage : python3 scripts/recouper_run_m7d.py
Code de sortie : 0 = recoup VERT ; 1 = écart nommé ; 2 = erreur fatale.
"""

import datetime
import hashlib
import importlib.util
import pathlib
import platform
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
PIECES = pathlib.Path("/home/z/my-project/download/preuves-run-m7d")
ARTEFACT_CORPUS = REPO / "riscv" / "corpus"
ARTEFACT_DEMO = REPO / "riscv" / "demo"
SOURCE = REPO / "riscv" / "terrain" / "scenario-m7d.py"

KIT_MD5 = "4d17f3fada9b54ccb21e232e0a0a1ca5"     # le kit éprouvé (Entrée 154)

# la source du scénario, chargée par chemin absolu (leçon D158 : jamais une
# lignée homonyme par accident) — LE JUGE EST LE CODE
_spec = importlib.util.spec_from_file_location("scenario_m7d_source", SOURCE)
src = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(src)

# Les 16 constats attendus — les préfixes STABLES des noms, extraits de la
# source (riscv/terrain/scenario-m7d.py, les constat() du run ; l'ordre est
# celui du code).
ATTENDUS = [
    "le témoin consigné : les empreintes ASSERTÉES avant tout geste",
    "le rituel n°1 : exactement les DEUX lignes au code 0",
    "le rituel n°2 : exactement les DEUX lignes au code 0",
    "le rituel n°3 : exactement les DEUX lignes au code 0",
    "base forcée -R 1G : la sortie IDENTIQUE",
    "base forcée -R 4G : la sortie IDENTIQUE",
    "base forcée -B 0x100000000 -R 2G : la sortie IDENTIQUE",
    "LA BASCULE PENDANT LE TRAFIC : 1 200 usages de l'entrée, "
    "l'apply entre 399/400, le retour entre 799/800",
    "le journal est COHÉRENT : 1 200 lignes ENTIÈRES, indices 0..1199",
    "LE DEP FALSIFIÉ (0x7→0x3)",
    "la falsification du démonstrateur",
    "base forcée -R 1G (le demo)",
    "base forcée -R 4G (le demo)",
    "base forcée -B 0x100000000 -R 2G (le demo)",
    "ZÉRO RÉGRESSION : les DEUX fichiers relus",
    "le rituel du scellé REJOUÉ après la démonstration",
]


class Recoup:
    def __init__(self):
        self.lignes: list[str] = []
        self.ok = True
        self.n_pass = 0

    def passe(self, nom: str, ok: bool, detail: str = "") -> bool:
        ok = bool(ok)
        self.ok = self.ok and ok
        if ok:
            self.n_pass += 1
        self.lignes.append(f"[recoup-m7d] {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        return ok


def md5f(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def fr(n: int) -> str:
    """Le séparateur de milliers FR des messages de la source (1 200)."""
    s = str(n)
    return s if len(s) < 4 else s[:-3] + " " + s[-3:]


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    r = Recoup()
    r.lignes.append("[recoup-m7d] === RECOUP LABO DU RUN M7-(d) — verdict sur "
                    "pièces croisées (D138/D145/D148/D154) ===")
    r.lignes.append(f"[recoup-m7d] recoup rendu le "
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"au laboratoire")
    r.lignes.append(f"[recoup-m7d] le juge est le code : constantes et "
                    f"générateur importés de {SOURCE.relative_to(REPO)}")

    # ---- A. les trois pièces, md5 re-contrôlés contre le coffre ----------
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m7") or {}
        distants = ds.list_folder(preuves["id"]) if preuves.get("id") else {}
    except Exception as exc:  # noqa: BLE001
        print(f"[recoup-m7d] ERREUR FATALE : coffre illisible : {exc}",
              file=sys.stderr)
        return 2
    noms = ["temoin-m7d.txt", "scenario-m7d-journal.log", "VERDICT-run-m7d.txt"]
    for nom in noms:
        local = PIECES / nom
        if not local.exists():
            print(f"[recoup-m7d] ERREUR FATALE : pièce locale absente : {nom}",
                  file=sys.stderr)
            return 2
        d = distants.get(nom)
        r.passe(f"A : {nom} au coffre, md5 re-contrôlé",
                bool(d) and md5f(local) == (d.get("md5Checksum") or "").lower(),
                f"md5 {md5f(local)[:12]}…")

    temoin = (PIECES / "temoin-m7d.txt").read_text(encoding="utf-8")
    journal = (PIECES / "scenario-m7d-journal.log").read_text(encoding="utf-8")
    verdict = (PIECES / "VERDICT-run-m7d.txt").read_text(encoding="utf-8")
    jl = [l.rstrip("\n") for l in journal.splitlines()]
    vl = [l.rstrip("\n") for l in verdict.splitlines()]

    # ---- B. le témoin -----------------------------------------------------
    champs = {}
    for l in temoin.splitlines():
        if " : " in l and not l.startswith(" "):
            k, v = l.split(" : ", 1)
            champs.setdefault(k.strip(), v.strip())
    # la valeur du témoin porte « sha256 <hex> — <description> » : le sha est
    # le PREMIER groupe hexadécimal 64 (jamais cru sur la description)
    m_sc = re.search(r"sha256 ([0-9a-f]{64})",
                     champs.get("corpus (AVANT)", ""))
    m_sd = re.search(r"sha256 ([0-9a-f]{64})",
                     champs.get("demo (AVANT)", ""))
    sha_corpus_lu = m_sc.group(1) if m_sc else ""
    sha_demo_lu = m_sd.group(1) if m_sd else ""
    sha_corpus_repo = sha256f(ARTEFACT_CORPUS)
    sha_demo_repo = sha256f(ARTEFACT_DEMO)
    r.passe("B1 : le témoin porte LE scellé 0.8.0-rc.1 (sha == artefact du "
            "dépôt re-calculé AU geste même — l'assertion du kit a tranché "
            "AVANT tout geste)",
            sha_corpus_lu == src.SHA_CORPUS == sha_corpus_repo,
            f"corpus {sha_corpus_lu[:16]}…")
    r.passe("B1b : le témoin porte le DÉMONSTRATEUR f72001 (sha == artefact "
            "du dépôt re-calculé AU geste même)",
            sha_demo_lu == src.SHA_DEMO == sha_demo_repo,
            f"demo {sha_demo_lu[:16]}…")
    md5_instr_lu = champs.get("md5 instrument", "")
    r.passe("B2 : l'instrument == le qemu-riscv64 STATIQUE du kit (md5 "
            "embarqué — l'instrument du kit ne se remplace pas en silence)",
            md5_instr_lu == src.MD5_QEMU_KIT
            and "qemu-riscv64" in champs.get("instrument", "")
            and "le kit (binaire statique embarqué)" in champs.get("instrument", ""),
            f"md5 {md5_instr_lu[:12]}…")
    noyau_temoin = champs.get("noyau", "").split(" (")[0]
    noyau_labo = platform.uname().release
    r.passe("B3 : le noyau du témoin est UN AUTRE noyau que celui du "
            "laboratoire (l'exigence du kit)",
            noyau_temoin != noyau_labo and noyau_temoin != "",
            f"témoin {noyau_temoin} ≠ labo {noyau_labo}")
    r.passe("B4 : la réserve instrumentale D149 NOMMÉE au témoin (TCG, noyau "
            "et syscalls réels de l'hôte — jamais déguisée en native)",
            "réserve instrumentale D149" in temoin
            and "TCG" in temoin, "nommée")
    r.passe("B5 : la date du témoin consignée (le run est daté sur pièces)",
            champs.get("date", "").startswith("2026-11-05"),
            champs.get("date", "?"))

    # ---- C. le journal ------------------------------------------------------
    r.passe("C1 : la bannière du journal en tête",
            jl and jl[0] == "JOURNAL DU RUN TERRAIN M7-(d) — "
            "l'universalité rejouée",
            jl[0][:60] if jl else "journal vide")
    r.passe("C2 : l'en-tête du journal == le témoin (machine, noyau, "
            "instrument md5, corpus, demo — cohérence croisée des pièces)",
            (champs.get("machine", "@1") in journal
             and noyau_temoin in journal
             and md5_instr_lu in journal
             and sha_corpus_lu in journal
             and sha_demo_lu in journal),
            "machine, noyau, md5, corpus, demo retrouvés")
    passes = [l for l in jl if l.startswith("[m7d] PASS : ")]
    echecs = [l for l in jl if l.startswith("[m7d] ÉCHEC")]
    r.passe("C3 : exactement 16 constats PASS, zéro ÉCHEC au journal",
            len(passes) == 16 and len(echecs) == 0,
            f"{len(passes)} PASS, {len(echecs)} échec(s)")
    nommes = [l[len("[m7d] PASS : "):] for l in passes]
    mal_nommes = [(i, a, n) for i, (a, n) in enumerate(zip(nommes, ATTENDUS))
                  if not a.startswith(n)]
    r.passe("C4 : les 16 constats AUX NOMS DE LA SOURCE, dans l'ordre du code "
            "(riscv/terrain/scenario-m7d.py — le juge est le code)",
            len(passes) == 16 and not mal_nommes,
            "16/16 préfixes exacts" if not mal_nommes
            else f"divergence au rang {mal_nommes[0][0]}")
    rituels = [l for l in passes if "le rituel n°" in l]
    r.passe("C5 : le rituel de parité TROIS exécutions au code 0 "
            f"({len(src.RITUEL)} o == len(RITUEL) de la source)",
            len(rituels) == 3 and all("code=0" in l for l in rituels)
            and all(f"{len(src.RITUEL)} o" in l for l in rituels)
            and len(src.RITUEL) == 60,
            f"3 × code=0, {len(src.RITUEL)} o")

    # l'arithmétique RECOMPTÉE DEPUIS LA SOURCE (le générateur déterministe
    # re-joué au geste même — l'attendu n'est pas cru, il est recalculé)
    attendu = src.transcription_attendue()
    attendu_dep = b"".join(b"trafic " + str(i).encode() + b"\n"
                           for i in range(src.K_APPLY))
    m_bascule = next((l for l in passes if "LA BASCULE PENDANT LE TRAFIC" in l),
                     "")
    mm = re.search(r"(\d+) o rendus / (\d+) attendus", m_bascule)
    rendus, attendus_o = (int(mm.group(1)), int(mm.group(2))) if mm else (-1, -1)
    ok_bascule = (mm is not None
                  and f"l'apply entre {src.K_APPLY - 1}/{src.K_APPLY}" in m_bascule
                  and f"le retour entre {src.M_ROLLBACK - 1}/{src.M_ROLLBACK}"
                  in m_bascule
                  and f"{fr(src.N_TRAFIC)} usages" in m_bascule
                  and len(attendu) == src.ATTENDU_TAILLE == attendus_o
                  and rendus == attendus_o)
    r.passe("C6 : LA BASCULE — l'arithmétique recomptée depuis la source "
            "(N=1200 usages, apply 399/400, retour 799/800, la transcription "
            "attendue RE-GÉNÉRÉE au geste même == "
            f"{src.ATTENDU_TAILLE} o figés, rendus == attendus)",
            ok_bascule,
            f"{rendus} o == {attendus_o} o == len(transcription_attendue())")
    m_coh = next((l for l in passes if "le journal est COHÉRENT" in l), "")
    n_v2 = src.M_ROLLBACK - src.K_APPLY
    ok_coh = (f"{fr(src.N_TRAFIC)} lignes ENTIÈRES" in m_coh
              and f"indices 0..{src.N_TRAFIC - 1}" in m_coh
              and f"{n_v2} lignes v2" in m_coh
              and f"{src.N_TRAFIC - n_v2} lignes v1" in m_bascule)
    r.passe("C6b : la cohérence du flux (1 200 lignes, indices 0..1199, "
            "800 v1 + 400 v2 — recomptés depuis la source)",
            ok_coh, f"{src.N_TRAFIC - n_v2} v1 + {n_v2} v2 == {src.N_TRAFIC}")
    m_dep = next((l for l in passes if "LE DEP FALSIFIÉ" in l), "")
    md = re.search(r"code=(-?\d+), (\d+) o == (\d+) attendus", m_dep)
    ok_dep = (md is not None and int(md.group(1)) == -11
              and int(md.group(2)) == int(md.group(3))
              == len(attendu_dep) == src.DEP_TAILLE
              and "SIGSEGV" in m_dep and "0x7→0x3" in m_dep)
    r.passe("C6c : le DEP falsifié (SIGSEGV code -11, l'attendu RE-CALCULÉ "
            f"depuis la source == {src.DEP_TAILLE} o exacts)",
            ok_dep,
            f"code={md.group(1) if md else '?'}, "
            f"{md.group(2) if md else '?'} o == {len(attendu_dep)} o")
    m_fals = next((l for l in passes if "la falsification du démonstrateur" in l),
                  "")
    mf = re.search(r"rompu à (0x[0-9a-f]+) \(essai n°(\d+)\)", m_fals)
    ok_fals = (mf is not None
               and int(mf.group(1), 16) == src.DEMO_ADDRS[0]
               and int(mf.group(2)) == 1
               and "zéro silence" in m_fals)
    r.passe("C6d : la falsification du démonstrateur ROMPUE à la PREMIÈRE "
            "mutation (l'adresse == DEMO_ADDRS[0] de la source — non-vacuité)",
            ok_fals,
            f"rompu à {mf.group(1) if mf else '?'} "
            f"(essai n°{mf.group(2) if mf else '?'})")
    bases = [l for l in passes if "base forcée" in l]
    r.passe("C6e : les SIX bases forcées au code 0 (3 corpus + 3 demo — "
            "l'indifférence à la base, D155)",
            len(bases) == 6 and all("code=0" in l for l in bases),
            f"{len(bases)} bases, code 0")

    # ---- D. le verdict ------------------------------------------------------
    r.passe("D1 : l'en-tête du verdict",
            vl and vl[0] == "VERDICT DU RUN TERRAIN M7-(d) — "
            "l'universalité rejouée (post-mortem, sur pièces)",
            vl[0][:60] if vl else "?")
    r.passe("D2 : « constats : 16 PASS / 0 ÉCHEC » écrit noir sur blanc",
            any(l.strip().startswith("constats : 16 PASS / 0 ÉCHEC")
                for l in vl), "16 PASS / 0 ÉCHEC")
    vpasses = [l for l in vl if l.startswith("[m7d] PASS : ")]
    r.passe("D3 : les 16 constats du verdict == les 16 PASS du journal, "
            "LIGNE POUR LIGNE (le post-mortem reprend le run exact)",
            vpasses == passes,
            f"{len(vpasses)} constats, identiques" if vpasses == passes
            else f"{len(vpasses)} vs {len(passes)}")
    r.passe("D4 : l'instrument du verdict == l'instrument du journal",
            any(l.startswith(f"instrument : ") for l in vl)
            and any(l in vl for l in jl if l.startswith("instrument : ")),
            "la même ligne")
    r.passe("D5 : les frontières nommées (code 5 structurel sous qemu-user, "
            "concurrence hors périmètre, le demo instrument pas lignée, le "
            "corpus LE scellé 0.8.0-rc.1)",
            any(l.startswith("frontières nommées : le code 5") for l in vl),
            "nommées")
    r.passe("D6 : « VERDICT : VERT » — le verdict du scénario sur pièces",
            any(l.strip() == "VERDICT : VERT" for l in vl), "VERT")

    # ---- E. le labo parle ----------------------------------------------------
    r.passe("E1 : l'artefact scellé du dépôt INTACT au geste même (le fichier "
            "que le développeur a exécuté est LE scellé du labo)",
            sha_corpus_repo == src.SHA_CORPUS == sha_corpus_lu,
            f"sha256 {sha_corpus_repo[:16]}…")
    r.passe("E2 : le démonstrateur du dépôt INTACT au geste même",
            sha_demo_repo == src.SHA_DEMO == sha_demo_lu,
            f"sha256 {sha_demo_repo[:16]}…")
    r.passe("E3 : le run a vécu sur UN AUTRE noyau que le laboratoire "
            "(la vigilance D146/D149 satisfaite : ni le même noyau)",
            noyau_temoin != noyau_labo,
            f"{noyau_temoin} vs {noyau_labo}")
    kit_coffre = (test.get("kit-m7d.zip") or {}).get("md5Checksum", "")
    r.passe("E4 : le kit du coffre /test == le kit éprouvé (md5 — la vague "
            "m7d déposée, jamais remplacée)",
            kit_coffre == KIT_MD5, f"md5 {kit_coffre[:12]}…")

    # ---- le jugement ---------------------------------------------------------
    for l in r.lignes:
        print(l)
    total = sum(1 for l in r.lignes if l.startswith("[recoup-m7d] PASS")
                or l.startswith("[recoup-m7d] ECHEC"))
    jugement = (f"RECOUP : VERT {r.n_pass}/{total} — les pièces établissent le "
                "critère M7-(d) : l'universalité REJOUÉE sur la machine du "
                "développeur (WSL2, un autre noyau), le scellage final 0.8.0 "
                "est DÉBLOQUÉ (--sceller-final)"
                if r.ok else
                "RECOUP : ÉCHEC NOMMÉ — au moins une pièce diverge, le "
                "scellage final 0.8.0 est REFUSÉ (fail-closed)")
    print(f"[recoup-m7d] {jugement}")

    sortie = ["=== RECOUP LABO DU RUN M7-(d) — verdict sur pièces croisées "
              "(D138/D145/D148/D154) ===",
              f"rendu le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
              "au laboratoire (noyau " + noyau_labo + ")",
              "le juge est le code : constantes et générateur déterministe "
              "importés de riscv/terrain/scenario-m7d.py, l'attendu "
              "RE-GENERÉ au geste même",
              "les pièces : /test/preuves-m7/ (temoin-m7d.txt, "
              "scenario-m7d-journal.log, VERDICT-run-m7d.txt), md5 contrôlés",
              ""] + r.lignes[4:] + ["", jugement]
    (PIECES / "VERDICT-recoup-m7d.txt").write_text(
        "\n".join(sortie) + "\n", encoding="utf-8")
    print(f"[recoup-m7d] le verdict du recoup écrit : "
          f"{PIECES / 'VERDICT-recoup-m7d.txt'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
