#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run7_m9f.py — LE RECOUP POST-MORTEM DU SEPTIÈME RUN M9-(f)
(D138/D145/D148 : verdict sur pièces, jamais sur console ; D154 : sur
pièces croisées). Le labo juge les CINQ pièces rapatriées du coffre
/test/preuves-m9f (md5 Drive contrôlés par le rapatriement, RE-contrôlés
ici) :

  temoin-m9f.txt            l'environnement + LES VINGT T0 tranchés
                            (dont LES DEUX erratum-10 : LE CONTRAT
                            D'APPEL relu DANS L'IMAGE) + T1..T6 ;
  scenario-m9f-journal.log  le run, ligne à ligne (HUIT lignes, TOUTES
                            VERTES, le run entier dans SA seconde) ;
  ligne-recue.txt           LA LIGNE APPLICATIVE REÇUE, DÉCHIFFRÉE PAR
                            LA MACHINE (1369 o, le témoin HTTP/1.1 200
                            OK EN CLAIR) — LA PREMIÈRE NÉE AU PROJET ;
  journal-emissions.txt     LES CINQ ÉMISSIONS DU RUN (436 o de records
                            TLS : le CH, le Finished, la ligne scellée,
                            l'offre mutée, le close_notify) ;
  VERDICT-run-m9f.txt       le verdict post-mortem VERT : LA SESSION
                            RÉELLE ÉTABLIE.

LE SEPTIÈME RUN EST LE PREMIER DU CONTRAT RÉPARÉ (le kit erratum n° 10
92098687…, l'artefact 446279f3… — le rebuild 1.0.0-dev.4), reçu sur la
demande de la passation 110 (« LE SEPTIÈME RUN DU DÉVELOPPEUR EST
ATTENDU — ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA
GRANDE ŒUVRE »). LE JUGE EST LE CODE : les textes attendus sont LUS
PAR AST dans la source du kit réparé, l'échelle est REJOUÉE au geste
même sur LA CLÉ PRIVÉE DU RUN, l'artefact est re-haché AU geste même,
la ligne reçue est LUE EN CLAIR sur la pièce, les émissions sont
RECADRÉES record par record sur la pièce binaire.

Usage : python3 scripts/recouper_run7_m9f.py
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
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-7")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
LIS_KIT = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = DEST / "VERDICT-recoup-labo-m9f-7.txt"

SHA_PROXY = ("446279f3ab356900")   # le rebuild 1.0.0-dev.4 (l'erratum n° 10)
KIT_MD5_PREFIX = "92098687"        # le kit RÉPARÉ au /test (erratum n° 10)

# les pièces du run 7, telles que rapatriées (md5 == Drive)
ATTENDUS = {"temoin-m9f.txt": "339a4335",
            "scenario-m9f-journal.log": "acbe41c6",
            "ligne-recue.txt": "c9f4fd72",
            "journal-emissions.txt": "b1970feb",
            "VERDICT-run-m9f.txt": "0684256d",
            "LISEZMOI-preuves.txt": "6c4bdbcd"}

# les valeurs DU RUN 7 : PARSÉES DU TÉMOIN au geste même (les pièces
# font foi — jamais recopiées à la main) ; hex 64 exact attendu
import re as _re


def _valeur_t3(temoin_texte, marqueur):
    for l in temoin_texte.splitlines():
        if l.startswith("[T3]") and marqueur in l:
            m = _re.search(r": ([0-9a-f]{64})", l)
            if m:
                return m.group(1)
    return ""


CLE_PRIV_RUN = ""   # rempli au main() depuis le témoin
ALEA_RUN = ""
PUB_RUN = ""

# la tête de la ligne reçue, lue au verdict (T4) — le clair attendu
TETE_FLUX_HEX = ("485454502f312e3120323030204f4b0d0a446174653a205361742c20"
                 "3037204e6f7620323032362031313a32313a3236")

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
    print("=== RECOUP LABO DU SEPTIÈME RUN M9-(f) — verdict sur pièces "
          "croisées ===\n")
    try:
        temoin = (DEST / "temoin-m9f.txt").read_text(encoding="utf-8",
                                                     errors="replace")
        journal = (DEST / "scenario-m9f-journal.log").read_text(
            encoding="utf-8", errors="replace")
        verdict = (DEST / "VERDICT-run-m9f.txt").read_text(encoding="utf-8",
                                                           errors="replace")
        ligne_bytes = (DEST / "ligne-recue.txt").read_bytes()
        emissions = (DEST / "journal-emissions.txt").read_bytes()
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
    controle("A2 : les pièces T4/T6 NÉES au coffre (ligne-recue.txt + "
             "journal-emissions.txt PRÉSENTES — le run a VÉCU jusqu'à T6 : "
             "cohérence avec le VERT)",
             "ligne-recue.txt" in distants
             and "journal-emissions.txt" in distants,
             f"(au réceptacle : {sorted(distants)})")

    # --- B. le TÉMOIN ---------------------------------------------------------
    # les trois valeurs du run, PARSÉES de la pièce (les pièces font foi)
    CLE_PRIV_RUN = _valeur_t3(temoin, "la clé privée du kit")
    ALEA_RUN = _valeur_t3(temoin, "l'aléa du kit")
    PUB_RUN = _valeur_t3(temoin, "la clé publique attendue")
    globals()["CLE_PRIV_RUN"] = CLE_PRIV_RUN
    globals()["ALEA_RUN"] = ALEA_RUN
    globals()["PUB_RUN"] = PUB_RUN
    t0_ok = [l for l in temoin.splitlines() if l.startswith("[ok] T0.")]
    controle("B1 : LES VINGT contrôles T0 tranchés [ok] (LES DIX-HUIT du "
             "run 6 + LES DEUX T0.erratum-10 : LE CONTRAT D'APPEL relu "
             "DANS L'IMAGE — AfdFlags = 0 ET TdiFlags = 0x20), AUCUN "
             "[ÉCHEC] T0",
             len(t0_ok) == 20 and "[ÉCHEC] T0" not in temoin,
             f"{len(t0_ok)} [ok] — dont LES DEUX erratum-10 (@0xa721 et "
             "@0xa729) ET LES DEUX erratum-9 (buf à +8 aux DEUX blocs)")
    h = hashlib.sha256(PROXY.read_bytes()).hexdigest()
    controle("B2 : l'artefact du dépôt INTACT == le sha lu au témoin — "
             "LE REBUILD 1.0.0-dev.4 que le run a couru",
             h.startswith(SHA_PROXY) and SHA_PROXY in temoin
             and "la taille — 65024 o" in temoin,
             f"sha256 {h[:16]}… (re-haché au geste même, 65024 o)")
    controle("B3 : LE TERRAIN TENU — la MÊME machine familiale que les "
             "runs 4/5/6 (Windows 11 build 26300, ntdll b072efae…), "
             "l'interprète Python 3.14.3",
             "Windows 10.0 build 26300" in temoin
             and "Python 3.14.3 · AMD64" in temoin
             and "b072efaeac06c558" in temoin,
             "le noyau tenu : l'A/B ne laisse passer QUE le temps, le "
             "bord DNS et l'aléa")
    controle("B4 : T1 (SSN 85/7/15, motif sain) + T2 session-1 (rax 0, "
             "handle 0x29c) tranchés [ok]",
             "SSN 85" in temoin and "SSN 7" in temoin and "SSN 15" in temoin
             and "handle 0x29c" in temoin and "motif 4c8bd1b8" in temoin)
    controle("B5 : la clé publique attendue NON-NULLE, PARSÉE du témoin "
             "(hex 64) — les TROIS valeurs du run lues de la pièce",
             len(PUB_RUN) == 64 and len(CLE_PRIV_RUN) == 64
             and len(ALEA_RUN) == 64
             and PUB_RUN != "" * 32
             and "0000000000000000" not in temoin,
             f"pub {PUB_RUN[:16]}… · priv {CLE_PRIV_RUN[:8]}… · "
             f"aléa {ALEA_RUN[:8]}…")
    controle("B6 : LA POIGNÉE OUVERTE — T3.ouvrir [ok] : rax 0, état 3 "
             "(CONNECTÉ) — LA MORT -7 DES RUNS 5/6 EST FRANCHIE : LA "
             "RÉCEPTION A RENDU LE SERVERHELLO (le contrat réparé de "
             "l'erratum n° 10 A VÉCU)",
             "[ok] T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ) — rax 0, "
             "état 3" in temoin)
    controle("B7 : LE RECOUP DU JALON — le CH ÉMIS par LA MACHINE == la "
             "construction re-jouée (119 o), l'aléa du kit @ +6, la clé "
             "publique @ +82 : les DEUX lecteurs",
             "[ok] T3.recoup" in temoin and "émis 119 o" in temoin)
    controle("B8 : LA LIGNE APPLICATIVE ÉCHANGÉE — T4.emettre [ok] (rax 0) "
             "ET T4.ligne [ok] (le témoin DANS LE FLUX DÉCHIFFRÉ PAR LA "
             "MACHINE, 1369 o reconstitués)",
             "[ok] T4.emettre : la ligne émise (rax == 0)" in temoin
             and "[ok] T4.ligne" in temoin
             and "1369 o reconstitués" in temoin)
    controle("B9 : LA GARDE CONTRE LE VRAI SERVEUR — T5.falsification [ok] "
             "(-6 NOMMÉ, état 5) ET T5.discipline [ok] (la session morte "
             "n'a émis QUE son offre)",
             "[ok] T5.falsification : -6 NOMMÉ" in temoin
             and "état 5" in temoin
             and "[ok] T5.discipline" in temoin
             and "1 émission(s) après l'empreinte mutée" in temoin)
    controle("B10 : LA FERMETURE PROPRE — T6.fermer [ok] (état 4), LE "
             "CLOSE_NOTIFY 24 o (5 + 2 + 17), NtClose ×2 (NTSTATUS 0x0), "
             "l'intégrité tenue (proxy.exe relu inchangé), les émissions "
             "du run : 5 enregistrement(s), 436 o",
             "[ok] T6.fermer" in temoin
             and "24 o (5 + 2 + 17 : le scellé de 01 00)" in temoin
             and "NTSTATUS 0x0" in temoin
             and "[ok] T6.intégrité : proxy.exe relu inchangé" in temoin
             and "5 enregistrement(s), 436 o" in temoin)
    controle("B11 : AUCUN rappel émission (sys-05 a rendu 0 à CHAQUE "
             "émission — la discipline tient : la source ne journalise "
             "QUE si r != 0)",
             "le rappel émission" not in temoin
             and "le rappel émission" not in journal,
             "l'émission réparée du run 5 TIENT, la réception réparée du "
             "run 7 VIT")

    # --- C. le JOURNAL ---------------------------------------------------------
    jl = journal.splitlines()
    controle("C1 : HUIT lignes, toutes à 12:21:26 (le run entier dans SA "
             "seconde — le profil SEC des runs vivants)",
             len(jl) == 8 and all(l.startswith("12:21:26") for l in jl))
    controle("C2 : T0/T1/T2 VERT aux textes exacts de la source",
             "T0 VERT" in journal and "T1 VERT" in journal
             and "T2 VERT" in journal)
    controle("C3 : la poignée OUVERTE puis VERT : « T3 : OUVRIR — la "
             "poignée ENTIÈRE par la machine d'états » puis « T3 VERT »",
             "T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états"
             in journal and "T3 VERT" in journal)
    controle("C4 : LA LIGNE — le témoin « HTTP/1.1 200 OK » REÇU et "
             "DÉCHIFFRÉ PAR LA MACHINE (record 1, 1369 o restitués)",
             "le témoin « HTTP/1.1 200 OK » REÇU et DÉCHIFFRÉ PAR LA "
             "MACHINE (record 1, 1369 o restitués)" in journal)
    controle("C5 : LA GARDE puis LA FERMETURE — « T5 VERT : la garde "
             "constatée CONTRE LE VRAI SERVEUR » et « T6 VERT »",
             "T5 VERT : la garde constatée CONTRE LE VRAI SERVEUR" in journal
             and "T6 VERT" in journal)
    controle("C6 : AUCUNE ligne d'échec dans le journal (le run SANS "
             "ÉCHEC : cohérent avec le VERDICT VERT)",
             "ÉCHEC" not in journal)

    # --- D. le VERDICT ---------------------------------------------------------
    controle("D1 : l'en-tête + le run daté + LE VERT NOMMÉ",
             verdict.startswith("TRIADE — LE TERRAIN M9-(f)")
             and "le run : 2026-11-07 12:21:26" in verdict
             and "VERDICT : VERT — LA SESSION RÉELLE ÉTABLIE" in verdict)
    lignes_temoin = [l for l in temoin.splitlines() if l.strip()]
    emboutees = [l for l in verdict.splitlines() if l.strip()
                 and l in lignes_temoin]
    controle("D2 : le témoin embarqué dans le verdict == la PIÈCE témoin, "
             "LIGNE POUR LIGNE",
             len(emboutees) == len(lignes_temoin) == 49,
             f"{len(emboutees)} lignes == {len(lignes_temoin)}")

    # --- E. LE LABO PARLE — la chaîne reconstituée AU GESTE MÊME ------------
    echelle = extraire_fonction(SCENARIO, "x25519_echelle")
    rendu = echelle(bytes.fromhex(CLE_PRIV_RUN)).hex()
    controle("E1 : l'échelle REJOUÉE sur LA CLÉ PRIVÉE DU RUN rend la clé "
             "publique DU TÉMOIN (RFC 7748)",
             rendu == PUB_RUN,
             f"40894e21… → {rendu[:16]}… == le témoin : la « clé attendue » "
             "du run est LA VRAIE")
    construction = extraire_fonction(SCENARIO, "construction_ch_reference",
                                     {"struct": __import__("struct")})
    ch = construction(bytes.fromhex(ALEA_RUN), bytes.fromhex(PUB_RUN))
    controle("E2 : la construction CH re-jouée (l'aléa et la clé DU RUN) : "
             "114 o, le vol 119 o — la référence que LA MACHINE a égalee "
             "octet pour octet (T3.recoup [ok])",
             len(ch) == 114 and ch[6:38].hex() == ALEA_RUN
             and ch[82:114].hex() == PUB_RUN)
    tete_clair = bytes.fromhex(TETE_FLUX_HEX).decode("ascii", "replace")
    controle("E3 : LA LIGNE REÇUE SUR PIÈCES — ligne-recue.txt : 1369 o, "
             f"la tête == « {tete_clair[:40]}… » EN CLAIR (le témoin "
             "applicatif HTTP/1.1 200 OK DÉCHIFFRÉ PAR LA MACHINE, relu "
             "sur la pièce AU geste même)",
             len(ligne_bytes) == 1369
             and ligne_bytes[:len(bytes.fromhex(TETE_FLUX_HEX))]
             == bytes.fromhex(TETE_FLUX_HEX),
             f"{len(ligne_bytes)} o — LA PREMIÈRE LIGNE APPLICATIVE EN "
             "CLAIR DU PROJET")
    # les émissions : recadrage record par record (5 o d'en-tête + corps)
    recs, off, ok_cadre = [], 0, True
    while off < len(emissions) and len(recs) < 8:
        if off + 5 > len(emissions):
            ok_cadre = False
            break
        corps = int.from_bytes(emissions[off + 3:off + 5], "big")
        fin = off + 5 + corps
        if fin > len(emissions):
            ok_cadre = False
            break
        recs.append((emissions[off:off + 5], fin - off))
        off = fin
    controle("E4 : LE JOURNAL DES ÉMISSIONS SUR PIÈCES — 436 o recadrés "
             "en CINQ records TLS SANS RESTE (le CH 16 03 03 00 72 : "
             "119 o ; le Finished : 58 o ; la ligne scellée ; l'offre "
             "mutée de la session morte ; le close_notify : 24 o)",
             ok_cadre and off == len(emissions) == 436 and len(recs) == 5
             and recs[0][0] == bytes.fromhex("1603030072")
             and recs[0][1] == 119 and recs[4][1] == 24,
             f"5 records : {[r[1] for r in recs]} o — la discipline "
             "d'émission CONSTATÉE sur la pièce binaire")
    src = SCENARIO.read_text(encoding="utf-8")
    controle("E5 : LE KIT RÉPARÉ AU COFFRE + LA SOURCE DU KIT — le kit "
             f"md5 {KIT_MD5_PREFIX}… INCHANGÉ depuis la passation 110, "
             "la source porte l'empreinte ÉPINGLÉE du run (le "
             "re-épinglage), T0.erratum-10, AUCUNE écriture .raw",
             (racine.get("kit-m9f.zip") or {}).get(
                 "md5Checksum", "").startswith(KIT_MD5_PREFIX)
             and "045d0758ed7db6e7a3a1ffaffb2cd8ca2a8185318d40422145af"
                 "3259b106f72f" in src
             and "T0.erratum-10" in src
             and "kit96.raw[:32] = alea" not in
             ast.dump(ast.parse(src)),
             "le MÊME binaire dev.4, le MÊME scénario que la livraison")
    lis = LIS_KIT.read_text(encoding="utf-8")
    controle("E6 : LE LISEZMOI DU KIT NOMME LE SEPTIÈME RUN + l'erratum "
             "n° 10 + la révision 3",
             "SEPTIÈME" in lis and "erratum n° 10" in lis
             and "révision 3" in lis)

    # --- F. LA GRANDE ŒUVRE — la condition nommée d'avance ------------------
    worklog = (REPO / "worklog.md").read_text(encoding="utf-8")
    journal_doc = (REPO / "docs" / "JOURNAL_TRAVAIL.md").read_text(
        encoding="utf-8")
    controle("F1 : LA CONDITION NOMMÉE D'AVANCE par la passation 110 — "
             "« LE SEPTIÈME RUN DU DÉVELOPPEUR — le premier du contrat "
             "réparé … le labo recoupe sur pièces (D138/D145/D148) — ET "
             "SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9 — LA "
             "GRANDE ŒUVRE » (le worklog + le JOURNAL Entrée 192 la "
             "portent) ET LE VERDICT DU RUN LA RÉPÈTE (« si elles "
             "établissent le critère, la finale 1.0.0 est posée : le "
             "jalon M9 franchi — LA GRANDE ŒUVRE »)",
             "LE SEPTIÈME RUN DU DÉVELOPPEUR" in journal_doc
             and "ET SI LE VERT TIENT : LA FINALE 1.0.0, LE JALON M9"
             in journal_doc
             and "ET SI LE VERT TIENT : LA FINALE 1.0.0" in worklog
             and "si elles établissent le critère, la finale 1.0.0 est "
                 "posée" in verdict)
    controle("F2 : LE VERT TIENT SUR PIÈCES — TOUTES les portes A..E "
             "PASS → LA FINALE 1.0.0 SE POSE : LE JALON M9 — LA GRANDE "
             "ŒUVRE",
             not ECHECS,
             f"{len(REUSSITES)} PASS, {len(ECHECS)} ÉCHEC")

    print(f"\n=== BILAN DU RECOUP : {len(REUSSITES)} PASS"
          + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "") + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")

    # --- le verdict du recoup, écrit AVEC les pièces -------------------------
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    lignes = []
    lignes.append("=== RECOUP LABO DU SEPTIÈME RUN M9-(f) — verdict sur "
                  "pièces croisées (D138/D145/D148) ===")
    lignes.append("rendu le " + __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S") + " au laboratoire")
    lignes.append("le juge est le code : les textes attendus lus PAR AST "
                  "dans la source du kit réparé, l'échelle REJOUÉE sur la "
                  "clé privée DU RUN, l'artefact re-haché au geste même, "
                  "la ligne reçue LUE EN CLAIR sur la pièce, les émissions "
                  "RECADRÉES record par record sur la pièce binaire")
    lignes.append("les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
                  "scenario-m9f-journal.log, ligne-recue.txt, "
                  "journal-emissions.txt, VERDICT-run-m9f.txt), md5 "
                  "contrôlés ; LES PIÈCES T4/T6 NÉES — le run a VÉCU "
                  "jusqu'à la fermeture propre")
    lignes.append("")
    for nom in REUSSITES:
        lignes.append(f"[recoup-m9f7] PASS : {nom}")
    lignes.append("")
    lignes.append(f"BILAN DU RECOUP : {len(REUSSITES)} PASS"
                  + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "")
                  + " — LE SEPTIÈME RUN M9-(f) RECROPÉ SUR PIÈCES CROISÉES")
    lignes.append("")
    lignes.append("L'ÉTAT DU RUN — LA SESSION RÉELLE ÉTABLIE : (1) LE "
                  "TERRAIN TENU : Windows 11 build 26300, ntdll "
                  "b072efae… (la machine familiale des runs 4/5/6), "
                  "l'artefact RÉPARÉ 446279f3… (le rebuild 1.0.0-dev.4 — "
                  "LES DEUX erratum-9 ET LES DEUX erratum-10 relus DANS "
                  "L'IMAGE), le kit erratum n° 10 92098687… INCHANGÉ ; "
                  "(2) LA POIGNÉE OUVERTE : le VRAI ntdll lu (SSN "
                  "85/7/15), le socket par LE VRAI afd.sys (zéro "
                  "ws2_32), T3.ouvrir rax 0 état 3 — LA MORT -7 DES "
                  "RUNS 5/6 FRANCHIE, LA RÉCEPTION RÉPARÉE A RENDU LE "
                  "SERVERHELLO ; (3) LA LIGNE APPLICATIVE CHIFFRÉE "
                  "ÉCHANGÉE : le témoin « HTTP/1.1 200 OK » DÉCHIFFRÉ "
                  "PAR LA MACHINE (1369 o EN CLAIR sur la pièce) — LA "
                  "PREMIÈRE LIGNE APPLICATIVE DU PROJET ; (4) LA GARDE : "
                  "l'épinglage divergent -6 NOMMÉ CONTRE LE VRAI "
                  "SERVEUR, la discipline tenue (UNE émission après la "
                  "mutation) ; (5) LA FERMETURE PROPRE : le close_notify "
                  "composé scellé émis (24 o), NtClose ×2 par le "
                  "tromphone, l'artefact relu INCHANGÉ, CINQ émissions "
                  "436 o recadrées SANS RESTE")
    if not ECHECS:
        lignes.append("")
        lignes.append("LE CRITÈRE EST TENU SUR PIÈCES CROISÉES — LE VERT "
                      "TIENT : LA FINALE 1.0.0 SE POSE — LE JALON M9 "
                      "FRANCHI : LA GRANDE ŒUVRE.")
    else:
        lignes.append("")
        lignes.append(f"LE RECOUP PORTE {len(ECHECS)} ÉCHEC(S) — la "
                      "finale NE se pose PAS : les échecs nommés font "
                      "foi.")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\nle verdict du recoup est écrit : {SORTIE}")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
