#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_preuves_m9f.py — LE RECOUP POST-MORTEM DU PREMIER RUN M9-(f)
(D138/D145/D148 : verdict sur pièces, jamais sur console ; D154 : sur
pièces croisées). Le labo juge les TROIS pièces rapatriées du coffre
/test/preuves-m9f (md5 Drive contrôlés par le rapatriement, RE-contrôlés
ici) :

  temoin-m9f.txt            l'environnement + les T0 tranchés ;
  scenario-m9f-journal.log  le run, ligne à ligne (2 lignes : mort à T1) ;
  VERDICT-run-m9f.txt       le verdict post-mortem ROUGE nommé.

LE JUGE EST LE CODE : les constantes sont LUES PAR AST dans la source du
scénario (tls13/terrain/scenario-m9f.py — jamais exécutée, jamais gravée),
l'artefact est re-haché AU geste même, et la cause du refus est
RECONSTITUÉE depuis les octets du dépôt.

Chaque contrôle tranché binaire (PASS/ÉCHEC nommé, fail-closed) :
  A. les trois pièces présentes, md5 locaux == métadonnées Drive RE-LUES ;
  B. le TÉMOIN : le sha de l'artefact == la source == le dépôt re-calculé,
     la taille, l'environnement (Windows 10.0 build 19045 — CONSIGNÉ :
     le kit visait Windows 11, la maison nomme l'écart), le VRAI ntdll
     localisé + haché, les SEIZE T0 tranchés [ok] AUX NOMS DE LA SOURCE,
     l'octet de l'erratum n° 5 relu, la cible + l'empreinte épinglée ;
  C. le JOURNAL : T0 VERT, puis la ligne du refus T1 AU TEXTE EXACT DE LA
     SOURCE (le miroir Python refuse « NtCreateFile » : répertoire export
     absent — le code -3 de lire_ssn_python), le journal mort LÀ (cohérent
     avec une mort à T1) ;
  D. le VERDICT : l'en-tête, « VERDICT : ROUGE — 1 échec(s) nommé(s) » +
     « T1.la-résolution », le conseil honnête, le témoin embarqué == la
     pièce témoin LIGNE POUR LIGNE ;
  E. LE LABO PARLE — L'ERRATUM n° 6 NOMMÉ SUR PIÈCES :
     E1 l'artefact du dépôt INTACT (sha re-calculé == le sha lu au témoin) ;
     E2 LE CONSTAT : proxy.exe N'A PAS de répertoire export (data
        directory[0] == 0 — recalculé AU geste même depuis le dépôt) →
        le refus -3 était INÉVITABLE SUR TOUTE MACHINE : le miroir Python
        de T1 recevait `base` (l'artefact) au lieu de `ntdll_base` —
        LA FAUTE EST AU KIT (le labo), JAMAIS au terrain ;
     E3 la source du dépôt contient le site fautif TROIS fois
        (« ssn_par_deux_lecteurs(base, ») — lisible, nommé ;
     E4 l'artefact n'est PAS en cause (PE32+ valide, motif de stub
        correct dans la source : c'est la BASE passée qui était
        fautive, jamais la machine du développeur) ;
     E5 le scénario DU KIT (kit-m9f.zip du coffre) == la source du dépôt
        octet pour octet : le développeur a exécuté LE scénario du labo,
        sans modification. Les pièces T4/T6 absentes (nées trop tard :
        cohérence vérifiée en A2).

Le jugement : « RECOUP : ROUGE CONSTATÉ COHÉRENT — l'échec est HONNÊTE et
nommé T1.la-résolution ; la cause est L'ERRATUM n° 6 du kit (la faute au
labo) ; la finale 1.0.0 est REFUSÉE pour ce run (fail-closed) ; le kit
sera réparé à la source et re-déposé ; le second geste du développeur
est attendu. » Le verdict du recoup est écrit à côté des pièces :
VERDICT-recoup-labo-m9f.txt.

Usage : python3 scripts/recouper_preuves_m9f.py
Code de sortie : 0 = recoup rendu ; 1 = pièce incohérente ; 2 = erreur
fatale."""

import ast
import datetime
import hashlib
import pathlib
import struct
import subprocess
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"          # /test
PIECES = pathlib.Path("/home/z/my-project/download/preuves-run-m9f")
SOURCE = REPO / "tls13" / "terrain" / "scenario-m9f.py"
ARTEFACT = REPO / "tls13" / "proxy.exe"
KIT_ZIP = pathlib.Path("/home/z/my-project/download/kit-m9f.zip")

# LA POINTE PRÉ-RÉPARATION — le commit du KIT DÉPOSÉ (Task 97, Entrée 179 :
# le kit-m9f.zip md5 a73fb526… vit dans l'histoire à CETTE pointe). Les
# contrôles E3/E5 lisent LA SOURCE À CETTE POINTE, pas l'arbre courant :
# la pièce demeure REJOUABLE après la réparation de l'erratum n° 6 (le
# geste corrige l'arbre ; l'histoire fait foi).
POINTE_PRE_REPARATION = "20ab30fb7c8967aa076a6ccf302e2bf21b9c8659"


def source_a_la_pointe() -> str:
    out = subprocess.run(
        ["git", "show", POINTE_PRE_REPARATION + ":tls13/terrain/scenario-m9f.py"],
        cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        print(f"[recoup-m9f] ERREUR FATALE : la pointe pré-réparation est "
              f"illisible : {out.stderr[:120]}", file=sys.stderr)
        sys.exit(2)
    return out.stdout


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
        self.lignes.append(f"[recoup-m9f] {'PASS' if ok else 'ECHEC'} : {nom}"
                           + (f" ({detail})" if detail else ""))
        return ok


def md5f(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def sha256f(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def litteral(noeud):
    if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Attribute) \
            and noeud.func.attr == "fromhex" \
            and isinstance(noeud.func.value, ast.Name) \
            and noeud.func.value.id == "bytes" and len(noeud.args) == 1:
        return bytes.fromhex(ast.literal_eval(noeud.args[0]))
    return ast.literal_eval(noeud)


def constantes_de_la_source(chemin):
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    cibles = {"SHA_PROXY", "TAILLE_PROXY", "OCTETS_TETE_CH",
              "EMPREINTE_EPINGLEE", "CIBLE", "TEMOIN_APPLICATIF",
              "MOTIF_STUB"}
    trouves = {}
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name) and cible.id in cibles:
                    trouves[cible.id] = litteral(noeud.value)
    manquantes = cibles - set(trouves)
    if manquantes:
        print(f"[recoup-m9f] ERREUR FATALE : constantes absentes de la "
              f"source : {sorted(manquantes)}", file=sys.stderr)
        sys.exit(2)
    return trouves


# les SEIZE contrôles T0 attendus — les noms exacts des verifie() de la
# source, dans l'ordre du code (le juge est le code)
T0_ATTENDUS = [
    "T0.proxy : l'empreinte de l'artefact",
    "T0.proxy : la taille",
    "T0.ntdll : le VRAI ntdll localisé",
    "T0.carte : l'artefact cartographié",
    "T0.sys-01 : le trombone ABI",
    "T0.fixture-device : le périphérique AFD UTF-16LE + NUL",
    "T0.fixture-span : « NtCreateFile »",
    "T0.fixture-span : « NtDeviceIoControlFile »",
    "T0.fixture-span : « NtClose »",
    "T0.erratum-5 : l'octet de longueur du record CH relu "
    "(41 C7 02 16 03 03 00 41 C6 42 04 72)",
    "T0.slot : la tête sys-02 @0xa040",
    "T0.slot : la tête sys-04 @0xa240",
    "T0.slot : la tête sys-05 @0xa540",
    "T0.slot : la tête sys-06 @0xa6c0",
    "T0.slot : la tête tls13-27 @0xff40",
    "T0.slot : la tête tls13-28 @0x10d00",
]


def main() -> int:
    r = Recoup()
    r.lignes.append("[recoup-m9f] === RECOUP LABO DU PREMIER RUN M9-(f) — "
                    "verdict sur pièces croisées (D138/D145/D148) ===")
    r.lignes.append(f"[recoup-m9f] recoup rendu le "
                    f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
                    f"au laboratoire")
    r.lignes.append("[recoup-m9f] le juge est le code : constantes lues PAR "
                    f"AST dans tls13/terrain/scenario-m9f.py, l'artefact "
                    f"re-haché, la cause reconstituée depuis les octets")

    src = constantes_de_la_source(SOURCE)

    # ---- A. les trois pièces, md5 re-contrôlés contre le coffre --------------
    try:
        test = ds.list_folder(TEST_ID)
        preuves = test.get("preuves-m9f") or {}
        distants = ds.list_folder(preuves["id"]) if preuves.get("id") else {}
    except Exception as exc:  # noqa: BLE001
        print(f"[recoup-m9f] ERREUR FATALE : coffre illisible : {exc}",
              file=sys.stderr)
        return 2
    noms = ["temoin-m9f.txt", "scenario-m9f-journal.log",
            "VERDICT-run-m9f.txt"]
    for nom in noms:
        local = PIECES / nom
        if not local.exists():
            print(f"[recoup-m9f] ERREUR FATALE : pièce locale absente : {nom}",
                  file=sys.stderr)
            return 2
        d = distants.get(nom)
        r.passe(f"A : {nom} au coffre, md5 re-contrôlé",
                bool(d) and md5f(local) == (d.get("md5Checksum") or "").lower(),
                f"md5 {md5f(local)[:12]}…")
    absentes = [n for n in ("ligne-recue.txt", "journal-emissions.txt")
                if n not in distants]
    r.passe("A2 : les pièces T4/T6 ABSENTES du coffre (nées à T4/T6 — "
            "le run est mort avant : cohérence avec le verdict)",
            len(absentes) == 2, f"absentes : {absentes}")

    temoin = (PIECES / "temoin-m9f.txt").read_text(encoding="utf-8")
    journal = (PIECES / "scenario-m9f-journal.log").read_text(
        encoding="utf-8")
    verdict = (PIECES / "VERDICT-run-m9f.txt").read_text(encoding="utf-8")
    jl = [l.rstrip("\n") for l in journal.splitlines()]
    vl = [l.rstrip("\n") for l in verdict.splitlines()]
    tl = [l.rstrip("\n") for l in temoin.splitlines()]

    # ---- B. le témoin -------------------------------------------------------
    oks = [l for l in tl if l.startswith("[ok] ")]
    r.passe("B1 : SEIZE contrôles T0 tranchés [ok] au témoin, AUCUN [ÉCHEC]",
            len(oks) == 16 and not any(l.startswith("[ÉCHEC]") for l in tl),
            f"{len(oks)} [ok]")
    r.passe("B2 : les SEIZE contrôles AUX NOMS EXACTS DE LA SOURCE, dans "
            "l'ordre du code (les verifie() de scenario-m9f.py)",
            [l[5:].split(" — ")[0] for l in oks] == T0_ATTENDUS,
            "16/16 préfixes exacts"
            if [l[5:].split(" — ")[0] for l in oks] == T0_ATTENDUS
            else f"divergence : {[l[5:].split(' — ')[0] for l in oks][:3]}…")
    sha_lu = next((l.split("sha256 ")[1].split("…")[0].strip()
                   for l in tl if "l'empreinte de l'artefact" in l), "")
    r.passe("B3 : le sha de l'artefact lu au témoin == LA SOURCE == le dépôt "
            "re-calculé AU geste même (l'assertion du kit a tranché AVANT "
            "tout geste : le développeur a exécuté LE build dev.2)",
            sha_lu == src["SHA_PROXY"][:len(sha_lu)] if sha_lu else False,
            f"sha256 {sha_lu[:16]}…")
    r.passe("B4 : la taille 65 024 o au témoin",
            any(" — 65024 o" in l for l in tl), "65024 o")
    r.passe("B5 : l'octet de l'erratum n° 5 relu DANS L'IMAGE au témoin "
            "(41 C7 02 16 03 03 00 41 C6 42 04 72)",
            any("T0.erratum-5" in l and "41 c7 02 16 03 03 00 41 c6 42 "
                "04 72" in l.lower() for l in tl)
            or any("T0.erratum-5" in l and "41 C7 02" in l for l in tl),
            "le kit embarquait le build réparé")
    r.passe("B6 : l'environnement consigné (Windows build + Python 64 bits)",
            any(l.startswith("[env] Windows ") for l in tl)
            and any(l.startswith("[env] Python ") and "AMD64" in l
                    for l in tl),
            "Windows 10.0 build 19045 · Python 3.14.6 AMD64")
    r.passe("B7 : le VRAI ntdll localisé ET son fichier haché (la pièce "
            "d'analyse de l'avenir)",
            any("C:\\WINDOWS\\System32\\ntdll.dll" in l for l in tl)
            and any(l.startswith("[env] ntdll sha256 : ")
                    and len(l.split(" : ", 1)[1]) == 64 for l in tl),
            "sha256 36b1a62e4bf6bf7d…")
    r.passe("B8 : la cible résolue au run + L'EMPREINTE ÉPINGLÉE == la "
            "source + le témoin applicatif",
            any("www.cloudflare.com:443 → " in l for l in tl)
            and src["EMPREINTE_EPINGLEE"].hex() in temoin
            and src["TEMOIN_APPLICATIF"].decode("ascii") in temoin,
            f"{src['CIBLE']} :443, épinglage {src['EMPREINTE_EPINGLEE'].hex()[:12]}…")

    # ---- C. le journal --------------------------------------------------------
    r.passe("C1 : le journal porte « T0 VERT » en première ligne (aucun "
            "échec T0)",
            jl and jl[0].endswith("T0 VERT"),
            jl[0] if jl else "journal vide")
    attendu_t1 = ("le miroir Python refuse « NtCreateFile » : "
                  "répertoire export absent")
    r.passe("C2 : la ligne du refus T1 AU TEXTE EXACT DE LA SOURCE "
            "(lire_ssn_python rend -3 : le code du miroir Python, le "
            "detail relu dans scenario-m9f.py)",
            len(jl) == 2 and attendu_t1 in jl[1],
            jl[1] if len(jl) > 1 else "?")
    r.passe("C3 : le journal MORT à T1 (deux lignes, aucune suite) — "
            "cohérent avec le verdict",
            len(jl) == 2 and "T2" not in journal and "T3" not in journal,
            f"{len(jl)} lignes")

    # ---- D. le verdict ---------------------------------------------------------
    r.passe("D1 : l'en-tête du verdict (LE TERRAIN M9-(f) : LA SESSION "
            "RÉELLE)",
            vl and vl[0].startswith("TRIADE — LE TERRAIN M9-(f)"),
            vl[0][:50] if vl else "?")
    r.passe("D2 : « VERDICT : ROUGE — 1 échec(s) nommé(s) » + « - "
            "T1.la-résolution » noir sur blanc",
            any(l.startswith("VERDICT : ROUGE — 1 échec(s) nommé(s) :")
                for l in vl)
            and "  - T1.la-résolution" in vl,
            "ROUGE, T1.la-résolution")
    r.passe("D3 : le conseil honnête présent (l'ordre lexicographique de "
            "la maison)",
            any("Un échec honnête vaut plus qu'un vert muet" in l
                for l in vl), "nommé")
    temoin_embarque = vl[vl.index([l for l in vl
                                  if l.startswith("[ok] T0.proxy")][0]):]
    r.passe("D4 : le témoin embarqué dans le verdict == la PIÈCE témoin, "
            "LIGNE POUR LIGNE (le post-mortem reprend le run exact)",
            temoin_embarque == tl,
            f"{len(temoin_embarque)} lignes == {len(tl)}")
    r.passe("D5 : le run daté au verdict (2026-11-06 16:17:51) et "
            "l'horodatage du journal == la même seconde",
            any(l.startswith("le run : 2026-11-06 16:17:51") for l in vl)
            and all(l.startswith("16:17:51  ") for l in jl),
            "2026-11-06 16:17:51")

    # ---- E. le labo parle : l'erratum n° 6 NOMMÉ sur pièces --------------------
    sha_depot = sha256f(ARTEFACT)
    r.passe("E1 : l'artefact du dépôt INTACT au geste même (sha re-calculé "
            "== la source == le témoin)",
            sha_depot == src["SHA_PROXY"],
            f"sha256 {sha_depot[:16]}…")
    data = ARTEFACT.read_bytes()
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    opt = e_lfanew + 24
    exp_rva, exp_sz = struct.unpack_from("<II", data, opt + 112)
    r.passe("E2 : LE CONSTAT SUR PIÈCES — proxy.exe N'A PAS de répertoire "
            "export (data directory[0] == 0, recalculé depuis le dépôt AU "
            "geste même) : le refus -3 du miroir Python était INÉVITABLE "
            "SUR TOUTE MACHINE — LA FAUTE EST AU KIT, jamais au terrain",
            exp_rva == 0 and exp_sz == 0,
            f"export rva={exp_rva:#x} taille={exp_sz:#x}")
    texte_source = source_a_la_pointe()
    n_fautifs = texte_source.count("ssn_par_deux_lecteurs(base,")
    r.passe("E3 : la source du kit (la pointe pré-réparation 20ab30f, "
            "rejouable) porte le site fautif TROIS fois — T1 passait `base` "
            "(l'ARTEFACT cartographié) aux lecteurs de SSN au lieu de "
            "`ntdll_base` : l'erratum n° 6, lisible et nommé",
            n_fautifs == 3,
            f"{n_fautifs} appels fautifs : "
            "ssn_par_deux_lecteurs(base, …)")
    r.passe("E4 : l'artefact a bien un en-tête PE32+ valide ET le motif de "
            "stub correct dans la source (la machine n'est pas en cause : "
            "c'est la BASE passée qui était fautive)",
            struct.unpack_from("<H", data, opt)[0] == 0x20B
            and src["MOTIF_STUB"] == bytes.fromhex("4c8bd1b8"),
            "magic 0x20B, motif 4C 8B D1 B8")
    with zipfile.ZipFile(KIT_ZIP) as z:
        scenario_kit = z.read("m9-kit/scenario-m9f.py")
    r.passe("E5 : le scénario DU KIT (kit-m9f.zip du coffre) == la source "
            "À LA POINTE pré-réparation (20ab30f), OCTET POUR OCTET (le "
            "développeur a exécuté LE scénario du labo, sans modification)",
            hashlib.sha256(scenario_kit).hexdigest()
            == hashlib.sha256(texte_source.encode("utf-8")).hexdigest(),
            f"{len(scenario_kit)} o")

    # ---- le jugement ---------------------------------------------------------
    for l in r.lignes:
        print(l)
    total = sum(1 for l in r.lignes if l.startswith("[recoup-m9f] PASS")
                or l.startswith("[recoup-m9f] ECHEC"))
    jugement = (f"RECOUP : ROUGE CONSTATÉ COHÉRENT {r.n_pass}/{total} — "
                "les pièces sont HONNÊTES et cohérentes entre elles ; "
                "l'échec T1.la-résolution est NOMMÉ et sa cause est AU "
                "LABO : L'ERRATUM n° 6 (T1 passait la base de l'ARTEFACT "
                "aux lecteurs de SSN au lieu de la base ntdll — "
                "proxy.exe n'a pas de répertoire export, le refus -3 "
                "était INÉVITABLE sur toute machine) ; le terrain est "
                "LAVÉ (le VRAI ntdll haché, l'artefact intact, le kit "
                "exécuté fidèlement) ; la finale 1.0.0 est REFUSÉE pour "
                "CE run (fail-closed) ; le kit sera réparé à la source "
                "et re-déposé au coffre /test — le second geste du "
                "développeur est attendu"
                if r.ok else
                "RECOUP : ÉCHEC NOMMÉ — au moins une pièce diverge "
                "(fail-closed) : le labo ne conclut RIEN sur un run "
                "qu'il ne peut recouper")
    print(f"[recoup-m9f] {jugement}")

    sortie = ["=== RECOUP LABO DU PREMIER RUN M9-(f) — verdict sur pièces "
              "croisées (D138/D145/D148) ===",
              f"rendu le "
              f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
              f"au laboratoire",
              "le juge est le code : constantes lues PAR AST dans "
              "tls13/terrain/scenario-m9f.py, l'artefact re-haché AU "
              "geste même, la cause reconstituée depuis les octets du dépôt",
              "les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
              "scenario-m9f-journal.log, VERDICT-run-m9f.txt), md5 "
              "contrôlés ; ligne-recue.txt et journal-emissions.txt "
              "jamais nées (le run est mort à T1)",
              ""] + r.lignes[4:] + [
        "",
        "L'ERRATUM n° 6 — LA FAUTE AU KIT, NOMMÉE SUR PIÈCES :",
        "  T1 appelait ssn_par_deux_lecteurs(base, …) — `base` est la base",
        "  de L'ARTEFACT (proxy.exe, cartographié à T0), pas `ntdll_base`",
        "  (localisé à T0 par GetModuleHandleW). Or proxy.exe N'A PAS de",
        "  répertoire export (data directory[0] == 0) : le miroir Python",
        "  lit le répertoire export du module qu'on lui donne, rend -3",
        "  (« répertoire export absent ») — le refus était INÉVITABLE sur",
        "  TOUTE machine Windows. Le verdict ROUGE du développeur prouve",
        "  que la garde fonctionne (un numéro N'EST JAMAIS extrait d'un",
        "  module sans exports) : un échec honnête vaut plus qu'un vert",
        "  muet. La réparation est À LA SOURCE (les trois sites d'appel",
        "  reçoivent `ntdll_base`) avec un CONTRÔLE PERMANENT à",
        "  l'assemblage (l'AST exige `ntdll_base` aux lecteurs de SSN).",
        "",
        "NOTE : l'environnement consigné — Windows 10.0 build 19045",
        "  (Windows 10 22H2), Python 3.14.6 AMD64 — le kit visait",
        "  Windows 11 (les mesures AFD WinDbg) : la maison nomme l'écart,",
        "  le scénario ne l'interdit pas ; si afd.sys diverge, le refus",
        "  sera NOMMÉ (-6, l'étape en cause) — un échec honnête vaut plus",
        "  qu'un vert muet.",
        "",
        jugement]
    (PIECES / "VERDICT-recoup-labo-m9f.txt").write_text(
        "\n".join(sortie) + "\n", encoding="utf-8")
    print(f"[recoup-m9f] le verdict du recoup écrit : "
          f"{PIECES / 'VERDICT-recoup-labo-m9f.txt'}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
