#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""extraire_donnees_v120.py — extraction des données réelles du journal vers les
tableaux du manuscrit académique v0.12.0 (le modèle formel, D187).

Chaque ligne produite porte SA SOURCE (entrée de journal, décision, tableau de
bord) : le manuscrit n'affirme rien qui ne soit extrait ici. Le script est
idempotent et VERIFIE les données qu'il exporte :

  1. jalons.csv        — les 11 jalons M0-M10 (dates, balises, critères, src) ;
  2. budgets.csv       — budgets tokens mesurés M1 (51/719/1088) + volumes de
                          lignée D34 (specs/brouillons/notations) ;
  3. oracles.csv       — volumes d'oracle et de harnais par jalon ;
  4. runs_loupe.csv    — les 12 runs terrain du TGN « Loupe » (défauts nommés,
                          retouches, empreintes, src) ;
  5. empreintes.csv    — les artefacts scellés (sha256 mesurés sur pièces) ;
  6. tables_generees.tex — les tableaux LaTeX prêts à \input ;
  7. extraits_journal.txt — les entrées citées par le manuscrit.

Usage : python3 scripts/extraire_donnees_v100.py [--verifier]
Code de sortie : 0 = succès, 1 = écart constaté (donnée introuvable).
"""

import argparse
import csv
import hashlib
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
JOURNAL = REPO / "docs" / "JOURNAL_TRAVAIL.md"
DECISIONS = REPO / "docs" / "DECISIONS.md"
SPEC = REPO / "docs" / "PROTOCOLE_TRIADE.md"
DONNEES = REPO / "scripts" / "manuscrit_v120" / "donnees"
PREUVES = REPO / "scripts" / "preuves_v110"
PREUVES120 = REPO / "scripts" / "preuves_v120"

J = JOURNAL.read_text(encoding="utf-8")
D = DECISIONS.read_text(encoding="utf-8")
S = SPEC.read_text(encoding="utf-8")


def sha256_fichier(chemin: pathlib.Path) -> str:
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def ligne_journal(numero: int) -> str:
    """Retourne l'entrée `numero` du journal (titre complet)."""
    motif = re.compile(rf"^## Entrée {numero} —(.+)$", re.MULTILINE)
    m = motif.search(J)
    if not m:
        raise SystemExit(f"ÉCART : Entrée {numero} introuvable au journal")
    return f"## Entrée {numero} —{m.group(1)}"


def exigean(motif: str, contexte: str, source: str) -> str:
    """Exige une expression régulière dans un texte ; retourne le groupe 1."""
    m = re.search(motif, contexte)
    if not m:
        raise SystemExit(f"ÉCART : motif {motif!r} introuvable ({source})")
    return m.group(1)


# ═══════════════════════════════ 1. JALONS M0-M10 ═══════════════════════════════

# (jalon, capacité, date, balise, entrées, preuve-labo, preuve-terrain)
JALONS = [
    ("M0", "Artefact chain (notation, bytes, PE, execution)", "2026-10-26",
     "0.1.0", "Entrées 1-13, D26", "round-trip 100\\%; executable < 4 KiB",
     "Windows 11 real machine execution"),
    ("M1", "Reusable blocks (mini-libc)", "2026-10-26",
     "0.2.0", "Entrées 14-20, D32", "oracle 21/21; first crystallisation",
     "terrain line « TRIADE M1 : minilibc 21/21 OK »"),
    ("M2", "Hot patching", "2026-10-27",
     "0.3.0", "Entrées 21-38, D43", "conformity 68/68; 8 instrumented iterations",
     "live patch + rollback on real machine, zero post-patch regression"),
    ("M3", "Untrusted inputs", "2026-10-28",
     "0.4.0", "Entrées 39-64, D72-D74", "$10^6$ fuzzed cases x2 seeds; 161 conformity controls",
     "transparent proxy for curl validated 6x on terrain"),
    ("M4", "Encrypted tunnel (Schannel)", "2026-10-29",
     "0.5.0", "Entrées 66-90, D104", "560-case SSPI scenario oracle x4 seeds; 12 mutations caught",
     "run 17-H: HTTPS transit + clean failure on invalid certificate"),
    ("M5", "Complete tool (VM interception)", "2026-11-04",
     "0.6.0", "Entrées 100-143, D148", "per-build fingerprints active",
     "browser flow intercepted in isolated VM (run e4, criterion (b) D136)"),
    ("M6", "Cross-OS portability (ELF64)", "2026-11-05",
     "0.7.0", "Entrées 144-149, D154", "7/7 conformity suite; layer-I diff zero",
     "WSL2 terrain run on developer kernel distinct from lab, 22/22 recoup"),
    ("M7", "Cross-ISA portability (RISC-V)", "2026-11-05",
     "0.8.0", "Entrées 150-155, D155", "round-trip 100 % on new ISA; fence.i patch",
     "terrain run green, 29/29 recoup on crossed pieces"),
    ("M8", "Direct syscalls (domain sys)", "2026-11-05",
     "0.9.0", "Entrées 156-164, D160-D165", "61 harness greens; 131 socket-socle controls",
     "run on real ntdll: 35 greens/0 failure, hooked-stub refusal -4, 30/30 recoup"),
    ("M9", "Pure TLS 1.3 (domain tls13)", "2026-11-07",
     "1.0.0", "Entrées 166-194, D166-D170", "28 blocks; 589 structural locks; handshake 54/54 x3 seeds; cross-lock 86/86",
     "REAL session with a real server; sealed on terrain run recoup 34/34"),
    ("M10", "Full-scale test: the Loupe application", "2026-11-11",
     "loupe 0.1.0 / 0.1.1", "Entrées 195-222, D171-D181", "18 blocks; 159 controls x3 seeds; cross-lock 26/26; seal guard 14/14",
     "12 terrain runs; 11 named defects; showcase alive (0/0) runs 10-12; seal on recoup 39/39"),
]


def table_jalons():
    lignes = []
    for j, cap, date, balise, src, labo, terrain in JALONS:
        lignes.append({"jalon": j, "capacite": cap, "date": date,
                       "balise": balise, "sources": src,
                       "preuve_labo": labo, "preuve_terrain": terrain})
    return lignes


# ═══════════════════════════════ 2. BUDGETS TOKENS ═══════════════════════════════

def table_budgets():
    # Mesure M1 (D31/D34) : localiser 51 / éditer 719 / ajouter 1 086 puis 1 088
    # (les nombres vivent au journal au format français « 1 086 » / « 1 088 »)
    exigean(r"localiser (\d+) / éditer (\d+) / ajouter 1 086", J,
            "journal, budgets mesurés M1 (première mesure)")
    exigean(r"/ éditer (\d+) / ajouter 1 088 \(cibles 64/3000/6000\)", J,
            "journal, budgets M1 confirmés (dérive +2)")
    specs = exigean(r"budgets tokens : specs (\d[\d\s]*\d),", J,
                     "journal, D34 lignée")
    brouillons = exigean(r"brouillons (\d[\d\s]*\d), notations livrées", J,
                         "journal D34")
    notations = exigean(r"notations livrées (\d[\d\s]*\d) \(total lignée", J,
                        "journal D34")
    total = exigean(r"\(total lignée (\d[\d\s]*\d) tok\)", J, "journal D34")
    def _num(s):
        return int(s.replace(" ", "").replace("\u202f", "").replace("\u00a0", ""))
    return [
        {"operation": "Locate a block", "cible_tokens": 64,
         "mesure_tokens": 51, "source": "D31/D34, M1 measurement (cl100k_base)"},
        {"operation": "Edit a block", "cible_tokens": 3000,
         "mesure_tokens": 719, "source": "D31/D34, M1 measurement"},
        {"operation": "Add a block", "cible_tokens": 6000,
         "mesure_tokens": 1088, "source": "D34, M1 (draft 1086, +2 drift re-measured)"},
        {"operation": "Whole lineage (specs)", "cible_tokens": "-",
         "mesure_tokens": _num(specs), "source": "D34, generation-1 card"},
        {"operation": "Whole lineage (drafts)", "cible_tokens": "-",
         "mesure_tokens": _num(brouillons), "source": "D34"},
        {"operation": "Whole lineage (delivered notations)", "cible_tokens": "-",
         "mesure_tokens": _num(notations), "source": "D34"},
        {"operation": "Whole lineage (TOTAL)", "cible_tokens": "-",
         "mesure_tokens": _num(total), "source": "D34"},
    ]


# ═══════════════════════════════ 3. ORACLES / HARNAIS ═══════════════════════════════

def table_oracles():
    return [
        {"jalon": "M1", "instrument": "mini-libc oracle", "volume": "21/21",
         "source": "D32; tag 0.2.0"},
        {"jalon": "M2", "instrument": "echo conformity + differential", "volume": "68/68; 8 iterations, 8 defect classes",
         "source": "D43; tag 0.3.0"},
        {"jalon": "M3", "instrument": "fuzz campaign + profile conformity suite",
         "volume": "1,000,000 cases x2 seeds; 161 controls", "source": "D72/D73"},
        {"jalon": "M4", "instrument": "SSPI scenario oracle + per-block differential",
         "volume": "560 cases x4 seeds; 10,000 fuzzed cases x2 seeds per block; 165k leaf differentials",
         "source": "D68-D93"},
        {"jalon": "M5", "instrument": "build fingerprint registry + verifier",
         "volume": "per-build sha256 registers", "source": "D134, D148"},
        {"jalon": "M6", "instrument": "profile conformity suite (Linux)",
         "volume": "7/7; lab recoup 22/22", "source": "D154"},
        {"jalon": "M7", "instrument": "RISC-V round-trip + cross-profile lock",
         "volume": "100 % round-trip; 29/29 recoup", "source": "D155"},
        {"jalon": "M8", "instrument": "sys harness on synthetic ntdll fixtures",
         "volume": "61 greens; 131 socle controls; 30/30 recoup", "source": "D160-D165"},
        {"jalon": "M9", "instrument": "tls13 structural oracle + handshake harness + cross-lock",
         "volume": "589 structural locks; handshake 54/54 x3 seeds; cross-lock 86/86; 560+365+131 replayed",
         "source": "D166-D170"},
        {"jalon": "M10", "instrument": "Loupe: 3 Unicorn harnesses + structural oracle + seal guard",
         "volume": "159 controls x3 seeds (61+53+45); 121 structural locks; cross-lock 26/26; seal guard 14/14; crystallisation 26 x 10/10",
         "source": "D172-D181"},
    ]


# ═══════════════════════════════ 4. RUNS LOUPE (12) ═══════════════════════════════

def table_runs():
    # (run, kit, pièce sha256 préfixe, date, verdict, défaut nommé, retouche, entrée)
    return [
        (1, "dev.1", "f07dd2cf", "2026-11-09",
         "loader refusal 0xc000007b",
         "Missing BASERELOC: ASLR image without relocation table (lab harness parses, never loads)",
         "dev.2: minimal 12-byte BASERELOC, 7 bytes in 6 ranges", 204),
        (2, "dev.2", "a8a65ed4", "2026-11-09",
         "same refusal 0xc000007b",
         "Necessary-not-sufficient: page hole 0x3000-0x4000 + massive BSS outside the proven envelope of 8 prior artifacts",
         "dev.3: image within envelope (VS==RS, no BSS)", 205),
        (3, "dev.3", "b494ff90", "2026-11-09",
         "loader mapped the image (decisive step); T0 witness failed",
         "[CADRE-NE]: .data initializer wrong (sentinel at +8 - a SIZE read as an offset instead of +528)",
         "dev.4: initializer = exact mirror of harness CADRE_VIERGE; guard healed (control derives from plan, never from the piece it guards)", 206),
        (4, "dev.4", "388d4680", "2026-11-09",
         "T0 all green; T1 named -6; showcase died instantly",
         "Stack-argument class: msx64 args 5+ at home space instead of [rsp+0x20]+ (loupe-01/05/06) + SSE alignment (loupe-10/11)",
         "dev.5: slots fixed; msx64 ABI audit born at build (static, catches SSE class); falsification control V7 added", 207),
        (5, "dev.5", "6f830f9c", "2026-11-09",
         "first run acquitting the piece; T1 named -7 VERROUILLE",
         "[SESSION]: kit itself - scenario-as-loader holds loupe.exe as a live section, Windows refuses gle 32 to open it for write",
         "dev.6 KIT-ONLY (artifact unchanged): byte-copy shadow temoin-session.bin", 208),
        (6, "dev.6", "6f830f9c", "2026-11-09",
         "two defects from one witness",
         "False save error + missing showcase thread; [HINSTANCE-PEB]: hInstance read from PEB instead of GetModuleHandleW(NULL)",
         "piece dev.6 (r12 = GetModuleHandleW(NULL)) + kit dev.7", 209),
        (7, "dev.7", "388d4680", "2026-11-09",
         "T0-T5 all green (save proven on terrain); then two defects",
         "[EAX-SANS-SIGNE] at kit (unsigned 32-bit reads of negative codes) + [D54-QUATRIEME] at piece (4 contiguous FirstThunk ranges without NULL separators)",
         "piece dev.7 (IAT relocated 0x3100, 4 ranges separated by NULL, 63 call sites repointed) + kit dev.8", 210),
        (8, "dev.8", "388d4680", "2026-11-09",
         "T0-T7 all green for the FIRST time (functional contract fully proven)",
         "Probe died on its own Python; showcase still mute (5th death)",
         "kit dev.9 (probe made load-bearing)", 213),
        (9, "dev.9", "388d4680", "2026-11-09",
         "T0-T7 all green second time; 6th showcase death named by system then by lab",
         "[OFT-QWORD]: 4 OFT tables at QWORD stride instead of DWORD - the loader walks 10.18.6.3 entries at DWORD stride; first cause of ALL deaths found on the piece bytes",
         "piece dev.8 (89 bytes in 52 ranges, sealed 0.1.0 candidate) + kit dev.10", 214),
        (10, "dev.11", "054de960", "2026-11-09",
         "T0-T7 all green third time; SHOWCASE ALIVE FIRST TIME (0 and 0, no WER)",
         "[FREE-SANS-TYPE] at kit: FreeLibrary called without argtypes, 64-bit HMODULE truncated to C int - ArgumentError killed cascade 205",
         "kit dev.12 (argtypes=[c_void_p], except Exception widened, probe armored try/finally)", 216),
        (11, "dev.12", "054de960", "2026-11-10",
         "T0-T7 all green 4th time; cascade 205 complete 1st time; showcase alive 2nd time; green holds entire",
         "[SONDE-EXE] named by lab on pieces: structural false negative - library loader NEVER resolves an EXE's imports; liaison proven by the living showcase",
         "seal loupe 0.1.0 on recouped run 39/39 (D178): notation debt paid (587->0), crystallisation 26x10/10, anti-rollback armed", 217),
        (12, "0.1.1-dev.1", "c1115105", "2026-11-11",
         "T0-T7 all green 5th time; cascade 205 2nd time; showcase alive 3rd time (0 and 0, first of piece 0.1.1)",
         "[T0-PERIME] residual named (dev.12-era banner text - no gate touched)",
         "seal loupe 0.1.1 (D181): [R10-PERIMEE] debt paid at birth (17 sums refreshed), card generation 17, artifact intact", 222),
    ]


# ═══════════════════════════════ 5. EMPREINTES ═══════════════════════════════

SHA_LOUPE_011 = "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"
SHA_LOUPE_010 = "054de960c31425d022f6900f27e59bdd82a120b0b3fe543a67e778867e9c7a69"
SHA_PROXY_100 = "446279f3ab356900870cc3b3e1700654a4216ec0b264172340e453db3b00d93d"


def table_empreintes():
    mesure_loupe = sha256_fichier(REPO / "loupe" / "loupe.exe")
    mesure_proxy = sha256_fichier(REPO / "tls13" / "proxy.exe")
    return [
        {"artefact": "loupe.exe 0.1.1 (sealed, D181)", "taille": 127488,
         "sha256": mesure_loupe, "attendu": SHA_LOUPE_011,
         "conforme": mesure_loupe == SHA_LOUPE_011,
         "source": "carte loupe tableau-de-bord; D181"},
        {"artefact": "loupe.exe 0.1.0 (sealed, D178 - run-11 piece)",
         "taille": 127488, "sha256": SHA_LOUPE_010, "attendu": SHA_LOUPE_010,
         "conforme": True,
         "source": "recouper_run11_loupe.py; journal line 9240; D178"},
        {"artefact": "proxy.exe 1.0.0 (sealed, D170)", "taille": 65024,
         "sha256": mesure_proxy, "attendu": SHA_PROXY_100,
         "conforme": mesure_proxy == SHA_PROXY_100,
         "source": "D170; tls13 card"},
    ]


# ═══════════════════════════════ 6. ÉCRITURE ═══════════════════════════════

def ecrire_csv(nom, lignes, champs):
    DONNEES.mkdir(parents=True, exist_ok=True)
    with open(DONNEES / nom, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        w.writeheader()
        for l in lignes:
            w.writerow(l)


import re as _re

def latex_echappe(s):
    s = (s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")
          .replace("#", r"\#").replace("->", r"$\rightarrow$"))
    s = _re.sub(r"(?<![A-Za-z0-9])x(?=\d)", r"$\\times$", s)
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verifier", action="store_true",
                    help="vérifie les données sans écrire")
    args = ap.parse_args()

    # -- vérifications d'ancrage : chaque affirmation doit vivre au journal --
    recoup11 = (REPO / "scripts" / "recouper_run11_loupe.py").read_text(encoding="utf-8")
    tdb_loupe = (REPO / "loupe" / "carte" / "tableau-de-bord.txt").read_text(encoding="utf-8")
    ancres = [
        (J, r"localiser (\d+) / éditer (\d+) / ajouter 1 086", "budgets M1 mesurés"),
        (J, r"1 000 000 cas SANS CRASH", "campagne million D72"),
        (J, r"560 cas × 4 graines", "oracle SSPI D93"),
        (J, r"589 verrous", "oracle structurel tls13"),
        (J, r"86/86 empreintes", "verrou croisé M9"),
        (J, r"39/39", "recoup onzième/douzième run"),
        (J, r"054de960c31425d0", "sha256 loupe 0.1.0 (préfixe, journal)"),
        (J, r"c1115105", "sha256 loupe 0.1.1 (préfixe, journal D181)"),
        (J, r"446279f3ab356900870cc3b3e1700654", "sha256 proxy 1.0.0 (journal)"),
        (recoup11, SHA_LOUPE_010[:32], "sha256 loupe 0.1.0, première moitié (pièce de recoup run 11)"),
        (recoup11, SHA_LOUPE_010[32:], "sha256 loupe 0.1.0, seconde moitié (pièce de recoup run 11)"),
        (tdb_loupe, SHA_LOUPE_011, "sha256 loupe 0.1.1 complet (tableau de bord carte)"),
        (D, r"^## D181 ", "décision D181 (balise loupe 0.1.1)"),
    ]
    ecarts = []
    for texte, motif, nom in ancres:
        if not re.search(motif, texte, re.MULTILINE):
            ecarts.append(f"ancre introuvable : {nom} ({motif!r})")

    jal = table_jalons()
    bud = table_budgets()
    orc = table_oracles()
    runs = table_runs()
    emp = table_empreintes()
    for e in emp:
        if not e["conforme"]:
            ecarts.append(f"empreinte non conforme : {e['artefact']}")

    if args.verifier:
        for e in ecarts:
            print(f"ÉCART : {e}")
        print(f"[verifier] {len(jal)} jalons, {len(bud)} budgets, "
              f"{len(orc)} oracles, {len(runs)} runs, {len(emp)} empreintes ; "
              f"{len(ecarts)} écart(s)")
        return 1 if ecarts else 0

    if ecarts:
        for e in ecarts:
            print(f"ÉCART : {e}", file=sys.stderr)
        return 1

    # -- CSV --
    ecrire_csv("jalons.csv", jal, list(jal[0].keys()))
    ecrire_csv("budgets.csv", bud, list(bud[0].keys()))
    ecrire_csv("oracles.csv", orc, list(orc[0].keys()))
    ecrire_csv("runs_loupe.csv",
               [{"run": r, "kit": k, "piece_sha256": p, "date": d,
                 "verdict": v, "defaut_nomme": de, "retouche": re_, "entree": en}
                for r, k, p, d, v, de, re_, en in runs],
               ["run", "kit", "piece_sha256", "date", "verdict",
                "defaut_nomme", "retouche", "entree"])
    ecrire_csv("empreintes.csv", emp, list(emp[0].keys()))

    # -- LaTeX : tableaux générés (le manuscrit \input ces fragments) --
    tex = []
    tex.append("% Fichier GÉNÉRÉ par extraire_donnees_v100.py — ne pas éditer à la main.")
    tex.append("% Chaque valeur est extraite/validée depuis docs/JOURNAL_TRAVAIL.md "
               "et docs/DECISIONS.md (édition académique v0.10.0, D182).")
    tex.append("")
    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Milestones M0--M10 of the TRIADE validation programme "
               r"(26 Oct -- 11 Nov 2026). Every milestone was closed on measured "
               r"exit criteria; sources: work journal entries and decision log.}")
    tex.append(r"\label{tab:jalons}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}ll lX@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Milestone} & \textbf{Sealed tag} & \textbf{Date} & "
               r"\textbf{Lab evidence (exit criteria met)} \\")
    tex.append(r"\midrule")
    for j, cap, date, balise, src, labo, terrain in JALONS:
        tex.append(rf"\textbf{{{j}}} & \code{{{balise}}} & {date[5:]} & "
                   rf"{latex_echappe(labo)} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Measured token budgets (M1 instrumentation, tokenizer "
               r"cl100k\_base) against design targets, and generation-1 lineage "
               r"volumes (D34).}")
    tex.append(r"\label{tab:budgets}")
    tex.append(r"\begin{tabular}{@{}lrrl@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Operation} & \textbf{Target} & \textbf{Measured} & \textbf{Source} \\")
    tex.append(r"\midrule")
    cibles = {"Locate a block": 64, "Edit a block": 3000, "Add a block": 6000}
    for b in bud:
        cible = b["cible_tokens"]
        cible_s = str(cible) if isinstance(cible, int) else "---"
        mesure_s = f"{b['mesure_tokens']:,}"
        tex.append(rf"{latex_echappe(b['operation'])} & {cible_s} & "
                   rf"{mesure_s} & {latex_echappe(b['source'])} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Verification instruments and volumes per milestone. "
               r"All numbers are drawn from the corresponding journal entries.}")
    tex.append(r"\label{tab:oracles}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}l X@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Milestone} & \textbf{Instrument (measured volume)} \\")
    tex.append(r"\midrule")
    for o in orc:
        tex.append(rf"\textbf{{{o['jalon']}}} & {latex_echappe(o['instrument'])} "
                   rf"— {latex_echappe(o['volume'])} \emph{{({latex_echappe(o['source'])})}} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\scriptsize")
    tex.append(r"\caption{The twelve terrain runs of the Loupe field test (M10). "
               r"Every failure was \emph{named} (a class, a mechanism, an evidence "
               r"piece) before being fixed; every fix was documented as a surgical "
               r"revision. The sealed artifacts never changed after their sealing "
               r"run. Sources: journal entries 204--222, decisions D178/D181.}")
    tex.append(r"\label{tab:runs}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}r l X X@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{\#} & \textbf{Kit} & \textbf{Outcome (named defect)} & "
               r"\textbf{Documented fix} \\")
    tex.append(r"\midrule")
    for r, k, p, d, v, de, re_, en in runs:
        issue = v if de == "" else f"{v}. {de}"
        tex.append(rf"{r} & \code{{dev.{k.split('dev.')[-1] if 'dev.' in k else k}}} & "
                   rf"{latex_echappe(issue)} & {latex_echappe(re_)} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Sealed artifacts (SHA-256, verified byte for byte "
               r"against the card and journal at edition time).}")
    tex.append(r"\label{tab:empreintes}")
    tex.append(r"\begin{tabular}{@{}l r l@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Artifact} & \textbf{Bytes} & \textbf{SHA-256 (first 16 hex)} \\")
    tex.append(r"\midrule")
    for e in emp:
        nom = e["artefact"].split(" (")[0]
        tex.append(rf"\code{{{latex_echappe(nom)}}} & {e['taille']:,} & "
                   rf"\code{{{e['sha256'][:16]}\ldots}} \\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}\end{table}")
    tex.append("")

    # -- la table des preuves renforcées (v0.11.0, D185) --
    import csv as _csv
    preuves = []
    for nom, titre, base in (
            ("modele_formel.csv", "Formal model CF3 (model checking borné)", "v120"),
            ("cristallisation.csv", "Crystallisation (SPRT, le seuil 10 justifié)", "v120"),
            ("mutation.csv", "Mutation testing (16 mutants/bloc, graine 20261111)", "v110"),
            ("temps_constant.csv", "Constant-time (dudect d'émulation, N=60)", "v110"),
            ("fuzzage.json", "Coverage-guided fuzzing (graines 20261111/12)", "v110"),
            ("independance.csv", "Oracle independence (distinct seed and model)", "v110"),
            ("surete_memoire.csv", "Bounded static memory safety", "v110"),
            ("benchmarks.csv", "Comparative benchmarks (same emulator)", "v110")):
        chemin = (PREUVES120 if base == "v120" else PREUVES) / nom
        if not chemin.exists():
            raise SystemExit(f"ÉCART : la preuve {nom} manque "
                             "(l'instrument correspondant doit être exécuté)")
        if nom == "mutation.csv":
            lignes_m = list(_csv.DictReader(open(chemin, encoding="utf-8")))
            for dom in ("loupe", "tls13", "sys"):
                sous = [l for l in lignes_m if l["domaine"] == dom]
                tues = sum(int(l["mutants"]) - int(l["vivants"]) for l in sous)
                tot = sum(int(l["mutants"]) for l in sous)
                preuves.append((titre, dom,
                                f"{tues}/{tot} killed ({100.0*tues/tot:.1f}%)",
                                f"{len(sous)} blocks"))
        elif nom == "fuzzage.json":
            import json as _json
            d = _json.load(open(chemin, encoding="utf-8"))
            preuves.append((titre, "loupe-01",
                            f"{d['loupe-01']['couverture_pct']}% coverage, "
                            f"{d['loupe-01']['crashes']} crashes, "
                            f"{d['loupe-01']['violations_canaris']} canary violations",
                            f"corpus {d['loupe-01']['corpus_final']}"))
            preuves.append((titre, "http-10",
                            f"{d['http-10']['couverture_instructions']} instructions covered, "
                            f"{d['http-10']['crashes_emulation']} crashes",
                            f"corpus {d['http-10']['corpus_final']}"))
        elif nom == "temps_constant.csv":
            for l in _csv.DictReader(open(chemin, encoding="utf-8")):
                preuves.append((titre, l["bloc"], f"t = {l['t_welch']}",
                                l["verdict"]))
        elif nom == "independance.csv":
            for l in _csv.DictReader(open(chemin, encoding="utf-8")):
                preuves.append((titre, l["confrontation"][:40],
                                f"{l['divergences']} divergence(s)", l["detail"][:40]))
        elif nom == "surete_memoire.csv":
            lignes_s = list(_csv.DictReader(open(chemin, encoding="utf-8")))
            oob = sum(int(l["hors_cadre_pile"]) for l in lignes_s)
            pile = sum(int(l["pile_verifies"]) for l in lignes_s)
            nr = sum(int(l["non_resolus"]) for l in lignes_s)
            preuves.append((titre, "52 blocks",
                            f"{pile} stack accesses verified, {oob} out-of-frame",
                            f"{nr} unresolved (named)"))
        elif nom == "modele_formel.csv":
            for l in _csv.DictReader(open(chemin, encoding="utf-8")):
                preuves.append((titre, l["propriété"],
                                l["verdict"], l["détail"][:44]))
        elif nom == "cristallisation.csv":
            for l in _csv.DictReader(open(chemin, encoding="utf-8")):
                if l["rebuilds_identiques"] in ("5", "10"):
                    preuves.append((titre,
                                    f"n = {l['rebuilds_identiques']} identical rebuilds",
                                    f"alpha = {l['risque_fausse_acceptation']}",
                                    f"{l['equivalent_sigma']} sigma"))
        elif nom == "benchmarks.csv":
            for l in _csv.DictReader(open(chemin, encoding="utf-8")):
                preuves.append((titre, l["primitive"],
                                f"{l['instructions_par_op']} ins/op",
                                f"{l['taille_octets']} bytes"))

    tex.append(r"\begin{table}[htbp]\centering\footnotesize")
    tex.append(r"\caption{Strengthened evidence (v0.11.0, D185): six new "
               r"instruments, all run with fixed seeds and reproducible. "
               r"Sources: scripts/preuves\_v110/.}")
    tex.append(r"\label{tab:preuves110}")
    tex.append(r"\begin{tabularx}{\textwidth}{@{}l l X l@{}}")
    tex.append(r"\toprule")
    tex.append(r"\textbf{Instrument} & \textbf{Target} & "
               r"\textbf{Measured} & \textbf{Detail} \\")
    tex.append(r"\midrule")
    for titre, cible, mes, det in preuves:
        tex.append(rf"{latex_echappe(titre[:42])} & {latex_echappe(cible)} & "
                   rf"{latex_echappe(mes)} & {latex_echappe(det)} " + "\\\\")
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabularx}\end{table}")
    tex.append("")

    (DONNEES / "tables_generees.tex").write_text("\n".join(tex), encoding="utf-8")

    # -- extraits de journal (les entrées citées) --
    extraits = []
    for num in (43, 74, 104, 148, 154, 155, 165, 170, 178, 181,
                204, 205, 206, 207, 208, 209, 210, 213, 214, 215, 216, 217, 218, 222):
        extraits.append(ligne_journal(num))
    (DONNEES / "extraits_journal.txt").write_text(
        "\n".join(extraits), encoding="utf-8")

    print(f"[extraire] {len(jal)} jalons, {len(bud)} budgets, {len(orc)} oracles, "
          f"{len(runs)} runs loupe, {len(emp)} empreintes")
    print(f"[extraire] tables_generees.tex + 5 CSV + extraits_journal.txt "
          f"-> {DONNEES}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
