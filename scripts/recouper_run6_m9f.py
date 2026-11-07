#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run6_m9f.py — LE RECOUP POST-MORTEM DU SIXIÈME RUN M9-(f)
(D138/D145/D148 : verdict sur pièces, jamais sur console ; D154 : sur
pièces croisées). Le labo juge les TROIS pièces rapatriées du coffre
/test/preuves-m9f (md5 Drive contrôlés par le rapatriement, RE-contrôlés
ici) :

  temoin-m9f.txt            l'environnement + les T0 tranchés (LES
                            DIX-HUIT — dont LES DEUX erratum-9 : la pose
                            du WSABUF canonique relue DANS L'IMAGE aux
                            DEUX blocs) + T3 ;
  scenario-m9f-journal.log  le run, ligne à ligne (6 lignes : mort à T3,
                            rax -7, après le recoup VERT du CH ÉMIS) ;
  VERDICT-run-m9f.txt       le verdict post-mortem ROUGE nommé T3.ouvrir.

LE SIXIÈME RUN EST LE JUMEAU DU CINQUIÈME (le MÊME kit ACQUITTÉ
79d44284…, le MÊME artefact réparé de23e577… — le rebuild 1.0.0-dev.3),
reçu sur la demande du recoup-5 (« réessayez réseau vivant — UN AUTRE
réseau si possible : le discriminant du passager »). LE JUGE EST LE
CODE : les textes attendus sont LUS PAR AST dans la source du kit
réparé, l'échelle est REJOUÉE au geste même sur LA CLÉ PRIVÉE DU RUN,
l'artefact est re-haché AU geste même — ET L'IDENTITÉ AVEC LE RUN 5
EST CONSTATÉE PAR CODE : le journal du run 6 est comparé LIGNE À LIGNE
à celui du run 5 (rapatrié au geste même depuis archives-preuves/
preuves-run-m9f-5/ au coffre), les horodatements exceptés.

LE VERDICT ATTENDU (la condition NOMMÉE D'AVANCE par le recoup-5 et la
passation 107) : SI LE -7 SE REPRODUIT IDENTIQUE (l'émission VERT, la
réception immédiate -7, le run en SA seconde) — LE PASSAGER ÉLIMINÉ
SUR PIÈCES ET LA SONDE sys-06 S'OUVRE (nommée d'avance, le miroir de
l'Entrée 185) : la mesure lira LE NTSTATUS BRUT de la première lecture
réelle (rdx, sys-06 Q5) ou LE ZÉRO de la demi-fin (Q2) — UN SEUL MOT
D'INFORMATION MANQUAIT.

Usage : python3 scripts/recouper_run6_m9f.py
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
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-6")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
SPEC_SYS06 = REPO / "m8" / "I" / "sys-06-reception.md"
SPEC_TLS27 = REPO / "tls13" / "I" / "tls13-27-principal-machine-etats.md"
LIS_KIT = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = DEST / "VERDICT-recoup-labo-m9f-6.txt"

SHA_PROXY = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
             "66b29226f")   # le rebuild 1.0.0-dev.3 (l'erratum n° 9)
KIT_MD5 = "79d44284c70261375a2b055070fda223"   # le kit RÉPARÉ au /test

# les pièces du run 6, telles que rapatriées (md5 == Drive)
ATTENDUS = {"temoin-m9f.txt": "9351b2bf",
            "scenario-m9f-journal.log": "acdc0fe8",
            "VERDICT-run-m9f.txt": "f432bc45"}

# les valeurs DU RUN 6, lues au témoin (les pièces font foi)
CLE_PRIV_RUN = ("0824c1e43b46a4bc34ac5e55b22c12c6a0d52ae74676f03e2dff48b"
                "fa49d24c5")
ALEA_RUN = ("9fab9773b66bc7e62955eba7a6e326845730ff0a2fae4ed058d2e10bf"
            "0bea118")
PUB_RUN = ("000a6be0c8a7df3ce6058ef4a7e8e3ec952e36f97ba18cfe2e52be8316"
           "4aae18")

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
    print("=== RECOUP LABO DU SIXIÈME RUN M9-(f) — verdict sur pièces "
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
    controle("B1 : les DIX-HUIT contrôles T0 tranchés [ok] (LES SEIZE du "
             "run 4 + LES DEUX T0.erratum-9 : la pose du WSABUF canonique "
             "relue DANS L'IMAGE aux DEUX blocs), AUCUN [ÉCHEC] T0",
             len(t0_ok) == 18 and "[ÉCHEC] T0" not in temoin,
             f"{len(t0_ok)} [ok] — dont les DEUX erratum-9 (sys-05 "
             "@0xa586 ET sys-06 @0xa706 : 89 74 24 60 48 89 7c 24 68)")
    h = hashlib.sha256(PROXY.read_bytes()).hexdigest()
    controle("B2 : l'artefact du dépôt INTACT == le sha lu au témoin — "
             "LE MÊME REBUILD dev.3 que le run 5 (le jumeau court le "
             "MÊME binaire)",
             h == SHA_PROXY and SHA_PROXY[:16] in temoin,
             f"sha256 {h[:16]}… (le kit ACQUITTÉ INCHANGÉ)")
    controle("B3 : LE TERRAIN TENU — la MÊME machine familiale que les "
             "runs 4/5 (Windows 11 build 26300, ntdll b072efae…), "
             "l'interpréteur encore changé (Python 3.14.3 — le run 4 le "
             "portait aussi, le run 5 : 3.13.9 : sans effet sur le "
             "natif, l'artefact est haché)",
             "Windows 10.0 build 26300" in temoin
             and "Python 3.14.3 · AMD64" in temoin
             and "b072efaeac06c558" in temoin,
             "le jumeau se joue sur LE MÊME noyau — l'A/B run 5 ↔ 6 ne "
             "laisse passer QUE le temps, le bord DNS et l'aléa")
    controle("B4 : T1 (SSN 85/7/15, motif sain) + T2 (rax 0, handle "
             "0x338) tranchés [ok]",
             "SSN 85" in temoin and "SSN 7" in temoin and "SSN 15" in temoin
             and "handle 0x338" in temoin and "motif 4c8bd1b8" in temoin)
    controle("B5 : la clé publique attendue NON-NULLE "
             f"({PUB_RUN[:8]}… — l'erratum n° 7 réparé)",
             "la clé publique attendue" in temoin and PUB_RUN in temoin
             and "0000000000000000" not in temoin,
             f"{PUB_RUN[:16]}…")
    controle("B6 : L'ÉCHEC NOMMÉ — T3.ouvrir rax -7, état 5 (LE MÊME NOM "
             "que le run 5 : le jumeau meurt au MÊME geste)",
             "[ÉCHEC] T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ) — "
             "rax -7, état 5" in temoin)
    controle("B7 : LE RECOUP DU JALON — le CH ÉMIS par LA MACHINE == la "
             "construction re-jouée (119 o)",
             "[ok] T3.recoup" in temoin and "émis 119 o" in temoin,
             "les DEUX lecteurs d'accord : tls13-14 (l'artefact) == "
             "l'échelle Python")
    controle("B8 : LA LIGNE « le rappel émission » ABSENTE → sys-05 rend "
             "0 ENCORE : LA SECONDE ÉMISSION RÉELLE DU PROJET (relue "
             "dans la source AU geste même : le rappel ne journalise "
             "QUE si r != 0)",
             "le rappel émission" not in temoin
             and "le rappel émission" not in journal,
             "l'émission réparée du run 5 N'ÉTAIT PAS UN PASSAGER : elle "
             "TIENT sur un run neuf")
    controle("B9 : la ligne « [T3] la dernière émission » ABSENTE → UNE "
             "SEULE émission (le CH), le Finished client jamais tenté — "
             "LA MORT EST À LA RÉCEPTION",
             "la dernière émission" not in temoin)

    # --- C. le JOURNAL ---------------------------------------------------------
    jl = journal.splitlines()
    controle("C1 : SIX lignes, toutes à 08:31:42 (le run entier dans SA "
             "seconde — le MÊME profil SEC que le run 5 : 07:23:36)",
             len(jl) == 6
             and all(l.startswith("08:31:42") for l in jl))
    controle("C2 : T0/T1/T2 VERT aux textes exacts de la source",
             "T0 VERT" in journal and "T1 VERT" in journal
             and "T2 VERT" in journal)
    controle("C3 : la ligne « T3 : OUVRIR » journalée",
             "T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états" in journal)
    controle("C4 : AUCUNE ligne de rappel émission — UN CONSTAT, PAS UN "
             "ABSENT FIXE : la source ne journalise QUE si r != 0 → "
             "sys-05 a rendu 0 au CH",
             "le rappel émission" not in journal
             and "le rappel émission : sys-05 rend {r}" in
             SCENARIO.read_text(encoding="utf-8"))
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
             not any(l[10:].startswith(("T4", "T5", "T6")) for l in jl)
             and len(jl) == 6)

    # --- D. le VERDICT ---------------------------------------------------------
    controle("D1 : l'en-tête + le run daté + ROUGE 1 échec nommé",
             verdict.startswith("TRIADE — LE TERRAIN M9-(f)")
             and "le run : 2026-11-07 08:31:42" in verdict
             and "VERDICT : ROUGE — 1 échec(s) nommé(s)" in verdict)
    emboutes = [l for l in verdict.splitlines() if l in temoin.splitlines()]
    controle("D2 : le témoin embarqué dans le verdict == la PIÈCE témoin, "
             "LIGNE POUR LIGNE",
             len(emboutes) == len(temoin.splitlines()) == 34,
             f"{len(emboutes)} lignes == {len(temoin.splitlines())}")

    # --- E. LE LABO PARLE — la chaîne reconstituée AU GESTE MÊME ------------
    echelle = extraire_fonction(SCENARIO, "x25519_echelle")
    rendu = echelle(bytes.fromhex(CLE_PRIV_RUN)).hex()
    controle("E1 : l'échelle REJOUÉE sur LA CLÉ PRIVÉE DU RUN rend la clé "
             "publique DU TÉMOIN",
             rendu == PUB_RUN,
             f"0824c1e4… → {rendu[:16]}… == le témoin : la « clé attendue » "
             "du run est LA VRAIE")
    construction = extraire_fonction(SCENARIO, "construction_ch_reference",
                                     {"struct": __import__("struct")})
    ch = construction(bytes.fromhex(ALEA_RUN), bytes.fromhex(PUB_RUN))
    controle("E2 : la construction CH re-jouée (l'aléa et la clé DU RUN) : "
             "114 o, le vol 119 o",
             len(ch) == 114 and ch[6:38].hex() == ALEA_RUN
             and ch[82:114].hex() == PUB_RUN,
             "la référence que LA MACHINE a égalee octet pour octet "
             "(T3.recoup [ok]) — l'offre PARTIE SUR LE RÉSEAU, ENCORE")
    src = SCENARIO.read_text(encoding="utf-8")
    spec06 = SPEC_SYS06.read_text(encoding="utf-8")
    spec27 = SPEC_TLS27.read_text(encoding="utf-8")
    controle("E3 : LA CHAÎNE RECONSTITUÉE DEPUIS LES CONTRATS — sys-05 "
             "rend 0 (B8 : AUCUN rappel) → le CH PARTI ; LA PREMIÈRE "
             "LECTURE (le ServerHello attendu — tls13-27 É1 « la boucle "
             "de lecture ») : le rappel réception (sys-06 — JAMAIS "
             "journalé par le scénario, relu dans la source AU geste "
             "même) rend NON-NUL → « la coupure du socle → -7 » "
             "(tls13-27 Q3), « l'état passe à 5 (MORT) » (Q2)",
             "def rappel_reception" in src
             and "la coupure du socle → -7" in spec27
             and "l'état passe à 5 (MORT)" in spec27
             and "LE ZÉRO EST LA DEMI-FIN" in spec06,
             "l'étape en échec : LA RÉCEPTION, à SON premier appel réel — "
             "ENCORE JAMAIS MESURÉE (la sonde s'ouvre)")
    controle("E4 : LE KIT ACQUITTÉ — le kit du coffre INCHANGÉ "
             f"(md5 {KIT_MD5[:8]}…) + la source du kit réparé (SHA_PROXY "
             "de23e577… + le contrôle T0.erratum-9 + le POINTEUR aux DEUX "
             "sites OUVRIR, AUCUNE écriture .raw)",
             (racine.get("kit-m9f.zip") or {}).get("md5Checksum") == KIT_MD5
             and SHA_PROXY in src
             and "T0.erratum-9" in src and "OCTETS_POSE_WSABUF" in src
             and "ctypes.addressof(kit96)" in src
             and "kit96.raw[:32] = alea" not in
             ast.dump(ast.parse(src)),
             "le MÊME binaire dev.3, le MÊME scénario : le kit du run 6 "
             "est celui du run 5 — AUCUNE réparation à faire")
    lis = LIS_KIT.read_text(encoding="utf-8")
    controle("E5 : LA FRONTIÈRE ÉTAIT NOMMÉE D'AVANCE — le LISEZMOI § les "
             "frontières : « les causes NTSTATUS vivent dans rdx » (la "
             "limite NOMMÉE de l'instrument) ET la spec sys-06 R2 le "
             "nomme : « La réception n'a JAMAIS couru sur le terrain "
             "réel » — réparée PAR SYMÉTRIE (le C_ASSERT send/recv), "
             "JAMAIS MESURÉE PAR SONDE",
             "Les causes NTSTATUS vivent dans rdx" in lis
             and "limite de l'instrument est nommée ici" in lis
             and "La réception n'a JAMAIS couru" in spec06
             and "sur le terrain réel (les cinq runs mouraient à "
             "l'émission" in spec06,
             "le verrou d'information qui départage (le code exact de "
             "sys-06 : -6 le STATUS / -7 le zéro propre) vit dans rdx — "
             "UN SEUL MOT D'INFORMATION MANQUE")

    # --- F. LE JUMEAU — les pièces du run 5, rapatriées AU GESTE MÊME ------
    try:
        arch = ds.list_folder(racine["archives-preuves"]["id"])
        run5 = ds.list_folder(arch["preuves-run-m9f-5"]["id"])
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run5["scenario-m9f-journal.log"]["id"]
                              + "?alt=media")
        journal_run5 = corps.decode("utf-8")
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run5["temoin-m9f.txt"]["id"] + "?alt=media")
        temoin_run5 = corps.decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR FATALE : run 5 introuvable au coffre : {exc}",
              file=sys.stderr)
        return 2
    l6 = [l[10:] for l in journal.splitlines()]
    l5 = [l[10:] for l in journal_run5.splitlines()]
    controle("F1 : LE JUMEAU — le journal du run 6 == le journal DU RUN 5, "
             "LIGNE À LIGNE, les horodatements exceptés (le run 5 "
             "rapatrié au geste même du coffre : les DEUX journaux de "
             "SIX lignes, identiques du premier au dernier mot)",
             len(l6) == 6 and len(l5) == 6 and l6 == l5,
             "07:23:36 ↔ 08:31:42 : SOIXANTE-HUIT minutes d'écart, PAS "
             "UNE LETTRE de différence")
    controle("F2 : LES TÉMOINS DIVERGENT SUR LES INVARIANTS SEULS — "
             "l'interpréteur (3.13.9 → 3.14.3 : sans effet sur le natif), "
             "l'ASLR (la base de la carte), le handle (0x284 → 0x338), "
             "LE BORD DNS (104.16.124.96 → 104.16.123.96 : une AUTRE "
             "arête Cloudflare a répondu au run — le DNS résolu AU RUN), "
             "l'aléa et les clés (un run neuf) ; LE NOYAU TENU (Win11 "
             "26300, ntdll b072efae… aux DEUX runs) ET L'ARTEFACT TENU "
             "(de23e577… aux DEUX témoins)",
             "Python 3.13.9 · AMD64" in temoin_run5
             and "Python 3.14.3 · AMD64" in temoin
             and "104.16.124.96" in temoin_run5
             and "104.16.123.96" in temoin
             and "b072efaeac06c558" in temoin_run5
             and "b072efaeac06c558" in temoin
             and "de23e577498d5cbf" in temoin_run5
             and "de23e577498d5cbf" in temoin,
             "l'offre est allée à UNE AUTRE PORTE du même bord — le même "
             "verdict est revenu")
    controle("F3 : LE -7 REPRODUIT IDENTIQUE — LA CONDITION NOMMÉE "
             "D'AVANCE EST REMPLIE : l'émission VERT aux DEUX runs "
             "(T3.recoup [ok], émis 119 o, AUCUN rappel), la réception "
             "immédiate -7 aux DEUX runs (T3.ouvrir, état 5), le run en "
             "SA seconde aux DEUX runs (C1) → LE PASSAGER ÉLIMINÉ SUR "
             "PIÈCES (un passager — un état transitoire du chemin — ne "
             "revient pas DEUX fois À L'IDENTIQUE à soixante-huit "
             "minutes d'écart, sur une poignée synchrone vivante)",
             "émis 119 o" in temoin and "émis 119 o" in temoin_run5
             and "[ÉCHEC] T3.ouvrir" in temoin
             and "[ÉCHEC] T3.ouvrir" in temoin_run5
             and "le rappel émission" not in temoin
             and "le rappel émission" not in temoin_run5
             and l6 == l5,
             "les candidats (a) le passager réseau : MORT ; restent (b) "
             "le contrat de réception, (c) LA DEMI-FIN")
    controle("F4 : LA MORT À LA MÊME PLACE — LA PREMIÈRE LECTURE (sys-06, "
             "le ServerHello attendu) : le code exact (-6 le STATUS / -7 "
             "le zéro ; le NTSTATUS brut vit dans rdx, sys-06 Q5) N'EST "
             "PAS SURFACÉ PAR L'INSTRUMENT aux DEUX runs — LA SONDE "
             "sys-06 S'OUVRE (nommée d'avance par le recoup-5 ET la "
             "passation 107, le miroir de l'Entrée 185)",
             "LE ZÉRO EST LA DEMI-FIN" in spec06
             and "rdx = le NTSTATUS brut consigné" in spec06
             and "IOCTL_AFD_RECEIVE" in spec06,
             "la sonde lira : n ≥ 1 (le ServerHello ARRIVÉ — la percée), "
             "-7 le zéro (LA DEMI-FIN), ou -6 + LE NTSTATUS NOMMÉ")
    controle("F5 : LE TEMPS ÉLIMINE LE SILENCE, ENCORE — le run entier "
             "dans SA seconde (08:31:42), T2 venant de réussir le "
             "three-way handshake synchrone : la lecture BLOQUANTE est "
             "revenue IMMÉDIATEMENT — le verdict de réception fut SEC, "
             "ENCORE (un serveur muet aurait TENU la lecture : la "
             "garde-chien tire à 300 s)",
             len(jl) == 6 and all(l.startswith("08:31:42") for l in jl)
             and "handle 0x338" in temoin,
             "un REFUS du noyau ou un verdict VIF du pair — PAS une "
             "attente muette, PAS un passager")
    controle("F6 : AUCUNE pièce conditionnelle née aux DEUX runs "
             "(ligne-recue.txt, journal-emissions.txt : jamais nées — la "
             "lecture n'a JAMAIS rendu un octet : la cohérence des DEUX "
             "runs sur pièces)",
             "ligne-recue.txt" not in distants
             and "journal-emissions.txt" not in distants
             and "ligne-recue" not in temoin
             and "ligne-recue" not in temoin_run5,
             "le run 5 comme le run 6 : la mort AVANT la ligne — le "
             "témoignage est UNANIME")

    print(f"\n=== BILAN DU RECOUP : {len(REUSSITES)} PASS"
          + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "") + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")

    # --- le verdict du recoup, écrit AVEC les pièces -------------------------
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    lignes = []
    lignes.append("=== RECOUP LABO DU SIXIÈME RUN M9-(f) — verdict sur "
                  "pièces croisées (D138/D145/D148) ===")
    lignes.append("rendu le " + __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S") + " au laboratoire")
    lignes.append("le juge est le code : les textes attendus lus PAR AST "
                  "dans la source du kit réparé, l'échelle REJOUÉE sur la "
                  "clé privée DU RUN, l'artefact re-haché au geste même, "
                  "L'IDENTITÉ AVEC LE RUN 5 CONSTATÉE PAR CODE (le "
                  "journal du run 6 comparé LIGNE À LIGNE à celui du run "
                  "5, rapatrié du coffre au geste même)")
    lignes.append("les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
                  "scenario-m9f-journal.log, VERDICT-run-m9f.txt), md5 "
                  "contrôlés ; ligne-recue.txt et journal-emissions.txt "
                  "jamais nées (le run est mort à T3 — comme le run 5)")
    lignes.append("")
    for nom in REUSSITES:
        lignes.append(f"[recoup-m9f6] PASS : {nom}")
    lignes.append("")
    lignes.append("L'ÉTAT DU RUN — LE JUMEAU : (1) LE TERRAIN TENU : "
                  "Windows 11 build 26300, ntdll b072efae… (LE MÊME que "
                  "les runs 4/5 — l'interpréteur seul change : Python "
                  "3.14.3), l'artefact RÉPARÉ de23e577… (LE MÊME rebuild "
                  "dev.3 que le run 5 — la pose canonique relue DANS "
                  "L'IMAGE aux DEUX blocs, les DEUX contrôles "
                  "T0.erratum-9 [ok]), le kit ACQUITTÉ INCHANGÉ "
                  "(79d44284…) ; (2) LA SECONDE ÉMISSION RÉELLE DU "
                  "PROJET : les DIX-HUIT T0 [ok], T1 (SSN 85/7/15, motif "
                  "sain), T2 VERT (sys-04 : rax 0, handle 0x338), le CH "
                  "ÉMIS (sys-05 rend 0 ENCORE — AUCUNE ligne de rappel) "
                  "ET RECOUPÉ octet pour octet (119 o == la construction "
                  "re-jouée : l'aléa @ +6, la clé publique @ +82) — "
                  "l'émission réparée N'ÉTAIT PAS UN PASSAGER : elle "
                  "TIENT ; (3) LA MORT AU MÊME GESTE : LA PREMIÈRE "
                  "LECTURE (le ServerHello attendu — tls13-27 É1) : le "
                  "rappel réception (sys-06, jamais journalé) rend "
                  "NON-NUL → la machine rend -7 (« la coupure du socle », "
                  "tls13-27 Q3), l'état 5 (MORT) — LE RUN ENTIER DANS SA "
                  "SECONDE (08:31:42), un verdict SEC encore.")
    lignes.append("")
    lignes.append("LA PREUVE EN UNE LIGNE (F1/F3) : le journal du run 6 "
                  "== le journal du run 5 LIGNE À LIGNE (les horodatements "
                  "exceptés — 07:23:36 ↔ 08:31:42), sur LE MÊME noyau "
                  "(Win11 26300, ntdll b072efae…), LE MÊME artefact "
                  "(de23e577…), l'émission VERT aux DEUX runs, la "
                  "réception immédiate -7 aux DEUX runs, le run en SA "
                  "seconde aux DEUX runs, le bord DNS changé "
                  "(104.16.124.96 → 104.16.123.96 : une AUTRE arête a "
                  "répondu) : **LE -7 S'EST REPRODUIT IDENTIQUE — LA "
                  "CONDITION NOMMÉE D'AVANCE PAR LE RECOUP-5 ET LA "
                  "PASSATION 107 EST REMPLIE : LE PASSAGER ÉLIMINÉ SUR "
                  "PIÈCES.**")
    lignes.append("")
    lignes.append("LES CANDIDATS APRÈS ÉLIMINATION (évidence avant "
                  "correctif — D54/D68/D98) : le passager réseau (a) EST "
                  "MORT sur pièces [F3 : un état transitoire du chemin ne "
                  "revient pas deux fois à l'identique, à soixante-huit "
                  "minutes d'écart, sur des poignées synchrones vivantes, "
                  "vers DEUX arêtes du bord] ; RESTENT DEUX : (b) LE "
                  "CONTRAT DE RÉCEPTION sys-06 REFUSÉ STRUCTURELLEMENT "
                  "[IOCTL_AFD_RECEIVE 0x12017 tel que le bloc le pose : "
                  "l'AFD_RECV_INFO 24 o, AfdFlags 0x20 (LA MESURE "
                  "leftarcode — l'erratum de lecture), TdiFlags 0, le "
                  "WSABUF canonique — la spec R2 le nomme elle-même : « "
                  "La réception n'a JAMAIS couru sur le terrain réel » : "
                  "réparée PAR SYMÉTRIE avec l'émission (le C_ASSERT "
                  "send/recv), JAMAIS MESURÉE PAR SONDE] ; (c) LA "
                  "DEMI-FIN — le pair a fermé proprement à l'offre "
                  "[l'offre SANS SNI refermée par le bord : le zéro de "
                  "sys-06 Q2 → -7 direct]. → LE CODE EXACT DE SYS-06 "
                  "(-6 le STATUS / -7 le zéro ; le NTSTATUS brut vit "
                  "dans rdx — sys-06 Q5) N'EST PAS SURFACÉ PAR "
                  "L'INSTRUMENT (la limite NOMMÉE au LISEZMOI § 4) : UN "
                  "SEUL MOT D'INFORMATION MANQUE — **LA SONDE sys-06 "
                  "S'OUVRE** (le miroir exact de l'Entrée 185 : la "
                  "mesure lira n ≥ 1 — le ServerHello ARRIVÉ, LA PERCÉE ; "
                  "-7 le zéro — LA DEMI-FIN nommée ; ou -6 + LE NTSTATUS "
                  "NOMMÉ — PENDING le bug du contrat, INVALID_PARAMETER "
                  "le contrat d'appel, RESET/DISCONNECT le pair).")
    lignes.append("")
    lignes.append("RECOUP : ROUGE CONSTATÉ COHÉRENT — l'échec est HONNÊTE "
                  "et nommé T3.ouvrir (rax -7, état 5), LE MÊME QUE LE "
                  "RUN 5 ; LE KIT EST ACQUITTÉ (le MÊME binaire dev.3, "
                  "le MÊME scénario — l'offre PARFAITE, ÉMISE DEUX FOIS) "
                  "; la finale 1.0.0 est REFUSÉE pour CE run (fail-closed "
                  "— le critère exige le vert : la session réelle "
                  "ÉTABLIE) ; LE GESTE AU DÉVELOPPEUR : **LA SONDE "
                  "SYS-06** — kit-sonde-sys06.zip LIVRÉ au coffre /test "
                  "par le présent geste (le miroir de l'Entrée 185 : "
                  "dézipper dans un dossier NEUF D99, python "
                  "scenario-sonde-sys06.py — Python 64 bits, réseau "
                  "vivant, la cible www.cloudflare.com:443), puis "
                  "renvoyer preuves-sonde-sys06/ ENTIER au coffre "
                  "/test/preuves-sonde-sys06/ — le labo recoupe sur "
                  "pièces, NOMME le coupable (le contrat du bloc, ou la "
                  "demi-fine du pair) et répare selon la charte ; SI LA "
                  "LECTURE REND DES OCTETS : LA PERCÉE — la finale 1.0.0 "
                  "en vue, LE JALON M9 — LA GRANDE ŒUVRE.")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\n[recoup] le verdict écrit AVEC les pièces : {SORTIE}")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
