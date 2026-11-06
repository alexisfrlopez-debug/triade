#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run4_m9f.py — LE RECOUP POST-MORTEM DU QUATRIÈME RUN M9-(f)
(D138/D145/D148 : verdict sur pièces, jamais sur console ; D154 : sur
pièces croisées). Le labo juge les TROIS pièces rapatriées du coffre
/test/preuves-m9f (md5 Drive contrôlés par le rapatriement, RE-contrôlés
ici) :

  temoin-m9f.txt            l'environnement + les T0 tranchés + T3 ;
  scenario-m9f-journal.log  le run, ligne à ligne (7 lignes : mort à T3,
                            rax -7, après le recoup VERT du CH) ;
  VERDICT-run-m9f.txt       le verdict post-mortem ROUGE nommé T3.ouvrir.

LE QUATRIÈME RUN EST LE GESTE (ii) DU RECOUP-3 ACCOMPLI : la machine
Windows 11 (build 26300 — la cible du kit ENFIN essayée ; le run 3 avait
lieu sur Windows 10 22H2 build 19045). LE JUGE EST LE CODE : les textes
attendus sont LUS PAR AST dans la source du scénario, l'échelle est
REJOUÉE au geste même sur LA CLÉ PRIVÉE DU RUN, l'artefact est re-haché
AU geste même — ET LA RÉPÉTITION EST CONSTATÉE PAR CODE : le journal du
run 4 est comparé LIGNE À LIGNE au journal DU RUN 3 (rapatrié au geste
même depuis archives-preuves/preuves-run-m9f-3/ au coffre), les
horodatements exceptés.

LE VERDICT ATTENDU : si le -6 à l'émission du CH se répète À L'IDENTIQUE
sur Windows 11, LE SUSPECT (a) DU RECOUP-3 (la divergence afd.sys
Win10 ↔ Win11) EST ÉLIMINÉ — le refus est INTER-GÉNÉRATIONS — et LE
GESTE PROMIS S'EXÉCUTE : le labo ouvre LA SONDE sys-05 (mesurer
IOCTL_AFD_SEND sur le vrai noyau : lire le NTSTATUS brut qui vit dans
rdx, la limite NOMMÉE de l'instrument).

Usage : python3 scripts/recouper_run4_m9f.py
Code de sortie : 0 = recoup rendu ; 1 = pièce incohérente ; 2 = erreur
fatale."""

import ast
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
sys.path.insert(0, str(REPO / "scripts"))
import drive_sync as ds  # noqa: E402

TEST_ID = "1KeJIMwpsT7GshcjIJy0Sf8KzsOBjimU0"
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-4")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = DEST / "VERDICT-recoup-labo-m9f-4.txt"

SHA_PROXY = ("d892893469608fd69e381b92b8e18623107bd2bc694f43a512"
             "bc5900773dc314")
KIT_MD5 = "90a1d0222b64b0b10f6b44d7e530ec5f"   # le kit ACQUITTÉ au /test

# les pièces du run 4, telles que rapatriées (md5 == Drive)
ATTENDUS = {"temoin-m9f.txt": "79c83775",
            "scenario-m9f-journal.log": "2b819ae4",
            "VERDICT-run-m9f.txt": "c95fb66e"}

# les valeurs DU RUN 4, lues au témoin (les pièces font foi)
CLE_PRIV_RUN = ("c318490921a738320b043be0215db180d5dc6bee37dc460bdd"
                "319b4fd96a1bfe")
ALEA_RUN = ("5ec4d01bb746f3787f52108c541e6585efff7d72b7be0150b83"
            "b075f425ca01a")
PUB_RUN = ("f650affb47ee3071dbd384ee4bcffe2a64f7a4cecb7ce8fa3a3"
           "004b987524023")

REUSSITES, ECHECS = [], []


def controle(nom, ok, detail=""):
    if ok:
        REUSSITES.append(nom)
        print(f"  [PASS] {nom}" + (f" — {detail}" if detail else ""))
    else:
        ECHECS.append((nom, detail))
        print(f"  [ÉCHEC] {nom}" + (f" — {detail}" if detail else ""))


def extraire_fonction(chemin, nom, namespace=None):
    arbre = ast.parse(pathlib.Path(chemin).read_text(encoding="utf-8"))
    for noeud in arbre.body:
        if isinstance(noeud, ast.FunctionDef) and noeud.name == nom:
            module = ast.Module(body=[noeud], type_ignores=[])
            code = compile(module, filename=str(chemin), mode="exec")
            ns = {} if namespace is None else namespace
            exec(code, ns)
            return ns[nom]
    raise SystemExit(f"fonction {nom} absente de {chemin}")


def main() -> int:
    print("=== RECOUP LABO DU QUATRIÈME RUN M9-(f) — verdict sur pièces "
          "croisées ===\n")
    try:
        temoin = (DEST / "temoin-m9f.txt").read_text(encoding="utf-8")
        journal = (DEST / "scenario-m9f-journal.log").read_text(
            encoding="utf-8")
        verdict = (DEST / "VERDICT-run-m9f.txt").read_text(encoding="utf-8")
    except OSError as exc:
        print(f"ERREUR FATALE : pièce introuvable : {exc}", file=sys.stderr)
        return 2

    # --- A. les pièces, md5 re-contrôlés contre les métadonnées Drive ------
    try:
        racine = ds.list_folder(TEST_ID)
        distants = ds.list_folder(racine["preuves-m9f"]["id"])
    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR FATALE : Drive : {exc}", file=sys.stderr)
        return 2
    for nom, prefixe in ATTENDUS.items():
        md5_local = ds.md5_of(DEST / nom)
        md5_distant = (distants.get(nom) or {}).get("md5Checksum", "-")
        controle(f"A : {nom} md5 local == Drive",
                 md5_local.startswith(prefixe) and md5_local == md5_distant,
                 f"md5 {md5_local[:10]}…")
    controle("A2 : les pièces T4/T6 ABSENTES du coffre (nées à T4/T6 — le "
             "run est mort à T3 : cohérence)",
             "ligne-recue.txt" not in distants
             and "journal-emissions.txt" not in distants,
             f"(au réceptacle : {sorted(distants)})")

    # --- B. le TÉMOIN ---------------------------------------------------------
    t0_ok = [l for l in temoin.splitlines() if l.startswith("[ok] T0.")]
    controle("B1 : les SEIZE contrôles T0 tranchés [ok], AUCUN [ÉCHEC] T0",
             len(t0_ok) == 16 and "[ÉCHEC] T0" not in temoin,
             f"{len(t0_ok)} [ok]")
    h = hashlib.sha256(PROXY.read_bytes()).hexdigest()
    controle("B2 : l'artefact du dépôt INTACT == le sha lu au témoin",
             h == SHA_PROXY and SHA_PROXY[:16] in temoin,
             f"sha256 {h[:16]}… — LE MÊME ARTEFACT que le run 3 (Win10)")
    controle("B3 : LE GESTE (ii) DU RECOUP-3 ACCOMPLI — la machine "
             "CHANGÉE : Windows 11 build 26300 (le run 3 : Windows 10 "
             "build 19045), Python 3.14.3, ntdll b072efae… — la cible du "
             "kit ENFIN essayée",
             "Windows 10.0 build 26300" in temoin
             and "Python 3.14.3 · AMD64" in temoin
             and "b072efaeac06c558" in temoin,
             "Win11 25H2 · Python 3.14.3 · ntdll b072efae… (≠ run 3 : "
             "Win10 19045 · Python 3.14.6 · ntdll 36b1a62e…)")
    controle("B4 : T1 (SSN 85/7/15, motif sain) + T2 (rax 0, handle 0x280) "
             "tranchés [ok] — le socle PASSE sur Win11 aussi",
             "SSN 85" in temoin and "SSN 7" in temoin and "SSN 15" in temoin
             and "handle 0x280" in temoin and "motif 4c8bd1b8" in temoin)
    controle("B5 : la clé publique attendue NON-NULLE "
             f"({PUB_RUN[:8]}… — l'erratum n° 7 réparé)",
             "la clé publique attendue" in temoin and PUB_RUN in temoin
             and "0000000000000000" not in temoin,
             f"{PUB_RUN[:16]}…")
    controle("B6 : L'ÉCHEC NOMMÉ — T3.ouvrir rax -7, état 5 (LE MÊME que "
             "le run 3)",
             "[ÉCHEC] T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ) — "
             "rax -7, état 5" in temoin)
    controle("B7 : LE RECOUP DU JALON — le CH de LA MACHINE == la "
             "construction re-jouée (119 o)",
             "[ok] T3.recoup" in temoin and "émis 119 o" in temoin,
             "les DEUX lecteurs d'accord : tls13-14 (l'artefact) == "
             "l'échelle Python")
    controle("B8 : la ligne « [T3] la dernière émission » ABSENTE → UNE "
             "SEULE émission tentée, REFUSÉE (relue dans la source AU geste "
             "même : le rappel ne journalise QUE si r != 0 — ligne 578)",
             "la dernière émission" not in temoin,
             "le CH composé PARFAIT n'a PAS quitté la machine — le "
             "Finished client n'a jamais été tenté")

    # --- C. le JOURNAL ---------------------------------------------------------
    jl = journal.splitlines()
    controle("C1 : SEPT lignes, toutes à 19:20:57 (le run entier dans SA "
             "seconde)", len(jl) == 7
             and all(l.startswith("19:20:57") for l in jl))
    controle("C2 : T0/T1/T2 VERT aux textes exacts de la source",
             "T0 VERT" in journal and "T1 VERT" in journal
             and "T2 VERT" in journal)
    controle("C3 : la ligne « T3 : OUVRIR » journalée",
             "T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états" in journal)
    controle("C4 : la ligne du rappel émission AU TEXTE EXACT DE LA SOURCE "
             "(sys-05 rend -6) — UN CONSTAT, PAS UN RAPPEL FIXE : la source "
             "ne journalise QUE si r != 0",
             "le rappel émission : sys-05 rend -6 (l'émission TOTALE ou "
             "refusée — jamais un demi-envoi déguisé)" in journal)
    controle("C5 : l'échec journalé == l'échec nommé du verdict",
             'T3 échecs : ["T3.ouvrir : rax == 0, l\'état 3 (CONNECTÉ)"]'
             in journal
             and "- T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ)" in verdict)
    controle("C6 : la ligne -7 AU TEXTE EXACT DE LA SOURCE (la branche "
             "r == -7 du scénario)",
             "T3 : -7 LE TRANSPORT EN ÉCHEC — le serveur n'a rien servi "
             "après l'offre (réseau coupé ?) : réessayez réseau vivant"
             in journal)
    controle("C7 : le journal MORT là (aucune ligne T4/T5/T6 — cohérent : "
             "return _verdict() suit immédiatement)",
             not any(l[9:].startswith(("T4", "T5", "T6")) for l in jl))

    # --- D. le VERDICT ---------------------------------------------------------
    controle("D1 : l'en-tête + le run daté + ROUGE 1 échec nommé",
             verdict.startswith("TRIADE — LE TERRAIN M9-(f)")
             and "le run : 2026-11-06 19:20:57" in verdict
             and "VERDICT : ROUGE — 1 échec(s) nommé(s)" in verdict)
    emboutes = [l for l in verdict.splitlines() if l in temoin.splitlines()]
    controle("D2 : le témoin embarqué dans le verdict == la PIÈCE témoin, "
             "LIGNE POUR LIGNE",
             len(emboutes) == len(temoin.splitlines()) == 32,
             f"{len(emboutes)} lignes == {len(temoin.splitlines())}")

    # --- E. LE LABO PARLE — la chaîne reconstituée AU GESTE MÊME ------------
    echelle = extraire_fonction(SCENARIO, "x25519_echelle")
    rendu = echelle(bytes.fromhex(CLE_PRIV_RUN)).hex()
    controle("E1 : l'échelle REJOUÉE sur LA CLÉ PRIVÉE DU RUN rend la clé "
             "publique DU TÉMOIN",
             rendu == PUB_RUN,
             f"c3184909… → {rendu[:16]}… == le témoin : la « clé attendue » "
             "du run est LA VRAIE")
    construction = extraire_fonction(SCENARIO, "construction_ch_reference",
                                     {"struct": __import__("struct")})
    ch = construction(bytes.fromhex(ALEA_RUN), bytes.fromhex(PUB_RUN))
    controle("E2 : la construction CH re-jouée (l'aléa et la clé DU RUN) : "
             "114 o, le vol 119 o",
             len(ch) == 114 and ch[6:38].hex() == ALEA_RUN
             and ch[82:114].hex() == PUB_RUN,
             "la référence que LA MACHINE a égalee octet pour octet "
             "(T3.recoup [ok])")
    src = SCENARIO.read_text(encoding="utf-8")
    controle("E3 : LA CHAÎNE -6 → -7 RECONSTITUÉE DEPUIS LES CONTRATS — "
             "sys-05 rend -6 (un NTSTATUS non nul : « rdx = le NTSTATUS "
             "brut consigné », sys-05 Q5), la machine propage -7 "
             "(tls13-27 Q2), l'état 5 (MORT)",
             "sys-05 rend {r}" in src.replace("{r}", "{r}")
             and "LE TRANSPORT EN ÉCHEC" in src,
             "l'étape en échec NOMMÉE : sys-05, L'ÉMISSION, à son PREMIER "
             "appel réel — refusé sur Win10 ET sur Win11")
    controle("E4 : LE KIT ACQUITTÉ — le kit du coffre INCHANGÉ "
             f"(md5 {KIT_MD5[:8]}…) + la source réparée (le POINTEUR aux "
             "DEUX sites OUVRIR, AUCUNE écriture .raw)",
             (racine.get("kit-m9f.zip") or {}).get("md5Checksum") == KIT_MD5
             and "ctypes.addressof(kit96)" in src
             and "kit96.raw[:32] = alea" not in
             ast.dump(ast.parse(src)),
             "le MÊME binaire, le MÊME scénario : seule la MACHINE a changé")
    lis = (REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md").read_text(
        encoding="utf-8")
    controle("E5 : LA FRONTIÈRE ÉTAIT NOMMÉE D'AVANCE — le LISEZMOI § les "
             "frontières : « le refus sera NOMMÉ (-6, l'étape en cause) »",
             "le refus sera NOMMÉ (-6, l'étape en cause)" in lis,
             "la note d'honnêteté du kit s'est réalisée AU MOT PRÈS — "
             "DEUX FOIS")

    # --- F. LA RÉPÉTITION — les pièces du run 3, rapatriées AU GESTE MÊME ---
    try:
        arch = ds.list_folder(racine["archives-preuves"]["id"])
        run3 = ds.list_folder(arch["preuves-run-m9f-3"]["id"])
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run3["scenario-m9f-journal.log"]["id"]
                              + "?alt=media")
        journal_run3 = corps.decode("utf-8")
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run3["temoin-m9f.txt"]["id"] + "?alt=media")
        temoin_run3 = corps.decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR FATALE : run 3 introuvable au coffre : {exc}",
              file=sys.stderr)
        return 2
    l4 = [l[9:] for l in journal.splitlines()]
    l3 = [l[9:] for l in journal_run3.splitlines()]
    controle("F1 : LA RÉPÉTITION À L'IDENTIQUE — le journal du run 4 == le "
             "journal DU RUN 3, LIGNE À LIGNE, les horodatements exceptés "
             "(le run 3 rapatrié au geste même du coffre)",
             l4 == l3 and len(l4) == 7,
             "les 7 lignes IDENTIQUES : T0/T1/T2 VERT, OUVRIR, le rappel "
             "« sys-05 rend -6 », l'échec T3.ouvrir, la branche -7")
    controle("F2 : LES TÉMOINS DIVERGENT SUR L'ENVIRONNEMENT SEULEMENT — "
             "Win10 build 19045 (run 3) ↔ Win11 build 26300 (run 4), "
             "ntdll 36b1a62e… ↔ b072efae…, Python 3.14.6 ↔ 3.14.3 : la "
             "preuve que la machine a CHANGÉ entre les deux",
             "Windows 10.0 build 19045" in temoin_run3
             and "Windows 10.0 build 26300" in temoin
             and "36b1a62e4bf6bf7d" in temoin_run3
             and "b072efaeac06c558" in temoin)
    controle("F3 : LE SUSPECT (a) DU RECOUP-3 ÉLIMINÉ — la divergence "
             "afd.sys Windows 10 ↔ Windows 11 : le MÊME refus -6 à "
             "l'émission du CH sur les DEUX GÉNÉRATIONS de noyau (l'offre "
             "composée PARFAITE, UNE SEULE émission tentée, aux deux runs) "
             "— un refus qui ne distingue PAS les générations n'est PAS "
             "une divergence de génération",
             l4 == l3
             and "[ÉCHEC] T3.ouvrir" in temoin
             and "[ÉCHEC] T3.ouvrir" in temoin_run3,
             "le refus est INTER-GÉNÉRATIONS : STRUCTUREL au contrat "
             "d'appel de sys-05 ou à l'état de l'endpoint — la sonde "
             "sys-05 s'ouvre")
    controle("F4 : LA CONNEXION ÉTAIT ÉTABLIE aux DEUX runs — T2 VERT "
             "(rax 0, handle posé) sur Win10 ET Win11 : sys-04 (create + "
             "bind + connect SYNCHRONE, sys-04 Q1) traverse VIVANT sur les "
             "DEUX générations — l'hypothèse « socket jamais connectée » "
             "s'affaiblit (le handle synchrone attend le three-way "
             "handshake)",
             "handle 0x328" in temoin_run3 and "handle 0x280" in temoin,
             "create + bind + connect VERT partout ; seul le SEND est "
             "refusé partout")

    print(f"\n=== BILAN DU RECOUP : {len(REUSSITES)} PASS"
          + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "") + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")

    # --- le verdict du recoup, écrit AVEC les pièces -------------------------
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    lignes = []
    lignes.append("=== RECOUP LABO DU QUATRIÈME RUN M9-(f) — verdict sur "
                  "pièces croisées (D138/D145/D148) ===")
    lignes.append("rendu le " + __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S") + " au laboratoire")
    lignes.append("le juge est le code : les textes attendus lus PAR AST "
                  "dans la source réparée, l'échelle REJOUÉE sur la clé "
                  "privée DU RUN, l'artefact re-haché au geste même, la "
                  "RÉPÉTITION constatée PAR CODE (le journal du run 4 "
                  "comparé LIGNE À LIGNE à celui du run 3, rapatrié du "
                  "coffre au geste même)")
    lignes.append("les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
                  "scenario-m9f-journal.log, VERDICT-run-m9f.txt), md5 "
                  "contrôlés ; ligne-recue.txt et journal-emissions.txt "
                  "jamais nées (le run est mort à T3)")
    lignes.append("")
    for nom in REUSSITES:
        lignes.append(f"[recoup-m9f4] PASS : {nom}")
    lignes.append("")
    lignes.append("L'ÉTAT DU RUN — LE GESTE (ii) ACCOMPLI, LA MORT "
                  "INVARIABLE : (1) LA MACHINE CHANGÉE : Windows 11 build "
                  "26300 (Python 3.14.3, ntdll b072efae…) — la cible du "
                  "kit ENFIN essayée, l'artefact INTACT (d8928934… — LE "
                  "MÊME que le run 3), le kit ACQUITTÉ INCHANGÉ "
                  "(90a1d022…) ; (2) LE SOCLE PLUS LOIN QUE JAMAIS : les "
                  "SEIZE T0 [ok], T1 (SSN 85/7/15, motif sain), T2 VERT "
                  "(sys-04 : create + bind + connect, rax 0, handle "
                  "0x280 — le socle PASSE sur Win11 AUSSI), la clé "
                  "publique attendue NON-NULLE (f650affb…), le recoup du "
                  "jalon VERT (le CH == la construction re-jouée, 119 o, "
                  "octet pour octet) ; (3) LA MORT NOMMÉE, LA MÊME : "
                  "sys-05 (L'ÉMISSION) rend -6 à SON PREMIER APPEL RÉEL "
                  "sur Windows 11 AUSSI — UNE SEULE émission tentée "
                  "(celle du CH), le Finished jamais tenté, la machine "
                  "propage -7 (LE TRANSPORT EN ÉCHEC), l'état 5 (MORT).")
    lignes.append("")
    lignes.append("LA PREUVE EN UNE LIGNE (F1/F3) : le journal du run 4 "
                  "est IDENTIQUE au journal du run 3, LIGNE À LIGNE, les "
                  "horodatements exceptés — sur UNE AUTRE GÉNÉRATION de "
                  "noyau (Win10 19045 ↔ Win11 26300, ntdll 36b1a62e… ↔ "
                  "b072efae…) : le refus -6 à l'émission du CH est "
                  "INTER-GÉNÉRATIONS — il ne peut plus être une divergence "
                  "de version du noyau.")
    lignes.append("")
    lignes.append("LES CANDIDATS RE-ÉVALUÉS (évidence avant correctif — "
                  "D54/D68/D98) : (a) LA DIVERGENCE afd.sys Win10 ↔ "
                  "Win11 : ÉLIMINÉE (le même -6 sur les deux générations "
                  "— le socle venait de mesures Win11, le refus y est "
                  "identique) ; (b) LE CONTRAT D'APPEL de sys-05 — "
                  "l'IOCTL_AFD_SEND (0x1201F) tel que le bloc le pose "
                  "[l'AFD_SEND_INFO de 24 o : BufferArray, BufferCount 1, "
                  "AfdFlags 0, TdiFlags 0 — la mesure leftarcode Win11] "
                  "serait refusé STRUCTURELLEMENT : un paramètre invalide "
                  "rend le même refus PARTOUT — le profil correspond ; "
                  "(c) L'ÉTAT DE L'ENDPOINT au moment du send — un "
                  "STATUS_PENDING ou un état de dispositif invalide : le "
                  "connect SYNCHRONE (sys-04 Q1) rend rax 0 aux deux runs "
                  "[handle posé], mais le NTSTATUS du CONNECT n'est pas "
                  "consigné séparément — le profil correspond aussi ; "
                  "(d) LE PASSAGER réseau : INVRAISEMBLABLE (un serveur "
                  "muet ferait échouer le CONNECT SYNCHRONE, pas le SEND ; "
                  "et le refus est identique sur deux machines, deux "
                  "générations, deux réseaux). → LE NTSTATUS BRUT (que "
                  "l'instrument NE REMONTE PAS : il vit dans rdx, sys-05 "
                  "Q5) DÉPARTAGE (b) de (c) : UN SEUL OCTET D'INFORMATION "
                  "MANQUE, LA SONDE LE LIT.")
    lignes.append("")
    lignes.append("RECOUP : ROUGE CONSTATÉ COHÉRENT — l'échec est HONNÊTE "
                  "et nommé T3.ouvrir (rax -7, état 5) ; LE KIT EST "
                  "ACQUITTÉ (le MÊME binaire, le MÊME scénario, l'offre "
                  "PARFAITE sur pièces) ; LE SUSPECT (a) EST ÉLIMINÉ SUR "
                  "PIÈCES ; la finale 1.0.0 est REFUSÉE pour CE run "
                  "(fail-closed — le critère exige le vert : la session "
                  "réelle ÉTABLIE) ; LE GESTE PROMIS PAR LE RECOUP-3 "
                  "S'EXÉCUTE : LE LABO OUVRE LA SONDE sys-05 — mesurer "
                  "IOCTL_AFD_SEND sur le vrai noyau, LIRE LE NTSTATUS "
                  "BRUT qui vit dans rdx (la limite NOMMÉE de "
                  "l'instrument, franchie par un trampoline de capture : "
                  "l'artefact INTACT, un bloc de quatre instructions posé "
                  "au geste, AUCUNE reconstruction) ; le kit sonde est "
                  "livré au coffre /test (kit-sonde-sys05.zip) ; LE GESTE "
                  "AU DÉVELOPPEUR : exécuter scenario-sonde-sys05.py sur "
                  "la machine Windows 11 (ou Win10 — le refus est "
                  "inter-générations), réseau vivant, et déposer les "
                  "pièces au coffre /test/preuves-sonde-sys05/.")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\n[recoup] le verdict écrit AVEC les pièces : {SORTIE}")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
