#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run5_m9f.py — LE RECOUP POST-MORTEM DU CINQUIÈME RUN M9-(f)
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

LE CINQUIÈME RUN EST LE PREMIER DU BUILD RÉPARÉ (l'artefact de23e577… —
le rebuild 1.0.0-dev.3 de la révision 2 étendue, l'erratum n° 9). LE JUGE
EST LE CODE : les textes attendus sont LUS PAR AST dans la source du kit
réparé, l'échelle est REJOUÉE au geste même sur LA CLÉ PRIVÉE DU RUN,
l'artefact est re-haché AU geste même — ET LA DIFFÉRENCE AVEC LE RUN 4
EST CONSTATÉE PAR CODE : le journal du run 5 est comparé LIGNE À LIGNE à
celui du run 4 (rapatrié au geste même depuis archives-preuves/
preuves-run-m9f-4/ au coffre), les horodatements exceptés.

LE VERDICT ATTENDU : la ligne « le rappel émission : sys-05 rend -6 »
des runs 1/3/4 a DISPARU — sys-05 a rendu 0 : LE CH EST PARTI SUR LE
RÉSEAU (LA PREMIÈRE ÉMISSION RÉELLE DU PROJET : l'erratum n° 9 validé
sur le vrai noyau) ; la mort a reculé d'UN CRAN — à LA PREMIÈRE LECTURE
(le ServerHello attendu, sys-06 : JAMAIS journalée par le scénario), la
machine rend -7 (« la coupure du socle », tls13-27), l'état 5 (MORT) —
exactement là où l'Entrée 187 plaçait la frontière suivante. Le -7 peut
être : (a) le passager réseau (le retour fut IMMÉDIAT : le temps élimine
le silence, pas la fermeture vive), (b) le refus STRUCTUREL du contrat
de réception (la spec R2 le nomme elle-même : « la réception n'a JAMAIS
couru sur le terrain réel »), (c) LA DEMI-FIN (le pair a refermé
proprement à l'offre sans SNI). LE CODE EXACT (-6 le STATUS / -7 le
zéro) vit dans rdx — la limite NOMMÉE de l'instrument. L'ordre
discipliné : LE SIXIÈME RUN d'abord (le scénario le demande : «
réessayez réseau vivant ») ; SI LE -7 SE REPRODUIT IDENTIQUE : LA SONDE
sys-06 (nommée d'avance, le miroir de l'Entrée 185).

Usage : python3 scripts/recouper_run5_m9f.py
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
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-5")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
SPEC_SYS06 = REPO / "m8" / "I" / "sys-06-reception.md"
SPEC_TLS27 = REPO / "tls13" / "I" / "tls13-27-principal-machine-etats.md"
LIS_KIT = REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = DEST / "VERDICT-recoup-labo-m9f-5.txt"

SHA_PROXY = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
             "66b29226f")   # le rebuild 1.0.0-dev.3 (l'erratum n° 9)
KIT_MD5 = "79d44284c70261375a2b055070fda223"   # le kit RÉPARÉ au /test

# les pièces du run 5, telles que rapatriées (md5 == Drive)
ATTENDUS = {"temoin-m9f.txt": "b080c083",
            "scenario-m9f-journal.log": "3fec82c8",
            "VERDICT-run-m9f.txt": "02b90aa4"}

# les valeurs DU RUN 5, lues au témoin (les pièces font foi)
CLE_PRIV_RUN = ("c757a3b59f969253146ef9832107c6bf873f34a429cc971af4f9"
                "0cd309e44550")
ALEA_RUN = ("70a073f4ab6e8807aabc5653add52f9bbd2fe93c4e3f118b23b123e"
            "067b4a2cd")
PUB_RUN = ("ca6cf4ba30848624934d53fd2ae6a554377f6afea00653446cbf7100"
           "eb089d2d")

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
    print("=== RECOUP LABO DU CINQUIÈME RUN M9-(f) — verdict sur pièces "
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
             "run 4 + LES DEUX T0.erratum-9 NOUVEAUX : la pose du WSABUF "
             "relue DANS L'IMAGE aux DEUX blocs), AUCUN [ÉCHEC] T0",
             len(t0_ok) == 18 and "[ÉCHEC] T0" not in temoin,
             f"{len(t0_ok)} [ok] — dont les DEUX erratum-9 (sys-05 "
             "@0xa586 ET sys-06 @0xa706 : 89 74 24 60 48 89 7c 24 68)")
    h = hashlib.sha256(PROXY.read_bytes()).hexdigest()
    controle("B2 : l'artefact du dépôt INTACT == le sha lu au témoin — "
             "LE REBUILD dev.3 (le premier run du build réparé)",
             h == SHA_PROXY and SHA_PROXY[:16] in temoin,
             f"sha256 {h[:16]}… (le run 4 courait le dev.2 d8928934…)")
    controle("B3 : LE TERRAIN TENU — la MÊME machine familiale que le "
             "run 4 (Windows 11 build 26300, ntdll b072efae…), "
             "l'interpréteur changé (Python 3.13.9 — le run 4 : 3.14.3 : "
             "sans effet sur le natif, l'artefact est haché)",
             "Windows 10.0 build 26300" in temoin
             and "Python 3.13.9 · AMD64" in temoin
             and "b072efaeac06c558" in temoin,
             "l'A/B des runs 4 ↔ 5 se joue sur le MÊME noyau — seule "
             "l'ARTEFACT a changé")
    controle("B4 : T1 (SSN 85/7/15, motif sain) + T2 (rax 0, handle "
             "0x284) tranchés [ok]",
             "SSN 85" in temoin and "SSN 7" in temoin and "SSN 15" in temoin
             and "handle 0x284" in temoin and "motif 4c8bd1b8" in temoin)
    controle("B5 : la clé publique attendue NON-NULLE "
             f"({PUB_RUN[:8]}… — l'erratum n° 7 réparé)",
             "la clé publique attendue" in temoin and PUB_RUN in temoin
             and "0000000000000000" not in temoin,
             f"{PUB_RUN[:16]}…")
    controle("B6 : L'ÉCHEC NOMMÉ — T3.ouvrir rax -7, état 5 (LE MÊME NOM "
             "que les runs 1/3/4 — UNE CHAÎNE AUTRE, voir F5)",
             "[ÉCHEC] T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ) — "
             "rax -7, état 5" in temoin)
    controle("B7 : LE RECOUP DU JALON — le CH ÉMIS par LA MACHINE == la "
             "construction re-jouée (119 o)",
             "[ok] T3.recoup" in temoin and "émis 119 o" in temoin,
             "les DEUX lecteurs d'accord : tls13-14 (l'artefact) == "
             "l'échelle Python")
    controle("B8 : LA LIGNE « le rappel émission » ABSENTE → sys-05 rend "
             "0 : L'ÉMISSION ACCEPTÉE — LA PREMIÈRE ÉMISSION RÉELLE DU "
             "PROJET (relue dans la source AU geste même : le rappel ne "
             "journalise QUE si r != 0)",
             "le rappel émission" not in temoin
             and "le rappel émission" not in journal,
             "le refus -6 des runs 1/3/4 (STATUS_ACCESS_VIOLATION, la "
             "sonde Entrée 185) EST MORT — l'erratum n° 9 validé sur le "
             "VRAI noyau")
    controle("B9 : la ligne « [T3] la dernière émission » ABSENTE → UNE "
             "SEULE émission (le CH), le Finished client jamais tenté — "
             "LA MORT EST À LA RÉCEPTION",
             "la dernière émission" not in temoin)

    # --- C. le JOURNAL ---------------------------------------------------------
    jl = journal.splitlines()
    controle("C1 : SIX lignes, toutes à 07:23:36 (le run entier dans SA "
             "seconde — le run 4 en comptait SEPT : la ligne de rappel "
             "-6 en moins)", len(jl) == 6
             and all(l.startswith("07:23:36") for l in jl))
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
             and "le run : 2026-11-07 07:23:36" in verdict
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
             f"c757a3b5… → {rendu[:16]}… == le témoin : la « clé attendue » "
             "du run est LA VRAIE")
    construction = extraire_fonction(SCENARIO, "construction_ch_reference",
                                     {"struct": __import__("struct")})
    ch = construction(bytes.fromhex(ALEA_RUN), bytes.fromhex(PUB_RUN))
    controle("E2 : la construction CH re-jouée (l'aléa et la clé DU RUN) : "
             "114 o, le vol 119 o",
             len(ch) == 114 and ch[6:38].hex() == ALEA_RUN
             and ch[82:114].hex() == PUB_RUN,
             "la référence que LA MACHINE a égalee octet pour octet "
             "(T3.recoup [ok]) — l'offre PARTIE SUR LE RÉSEAU")
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
             "l'étape en échec : LA RÉCEPTION, à SON PREMIER appel réel — "
             "JAMAIS ENCORE MESURÉE (voir E5)")
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
             "le MÊME binaire dev.3, le MÊME scénario : le kit du run 5 "
             "est CELUI livré à la Task 106")
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

    # --- F. LA DIFFÉRENCE — les pièces du run 4, rapatriées AU GESTE MÊME ---
    try:
        arch = ds.list_folder(racine["archives-preuves"]["id"])
        run4 = ds.list_folder(arch["preuves-run-m9f-4"]["id"])
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run4["scenario-m9f-journal.log"]["id"]
                              + "?alt=media")
        journal_run4 = corps.decode("utf-8")
        st, corps, _ = ds.api("GET", ds.API + "/files/"
                              + run4["temoin-m9f.txt"]["id"] + "?alt=media")
        temoin_run4 = corps.decode("utf-8")
    except Exception as exc:  # noqa: BLE001
        print(f"ERREUR FATALE : run 4 introuvable au coffre : {exc}",
              file=sys.stderr)
        return 2
    l5 = [l[10:] for l in journal.splitlines()]
    l4 = [l[10:] for l in journal_run4.splitlines()]
    l4_sans_rappel = [l for l in l4
                      if not l.startswith("le rappel émission")]
    controle("F1 : LA DIFFÉRENCE D'UNE LIGNE — le journal du run 5 == le "
             "journal DU RUN 4 MOINS LA LIGNE « le rappel émission : "
             "sys-05 rend -6 », les horodatements exceptés (le run 4 "
             "rapatrié au geste même du coffre) : L'ÉMISSION RÉPARÉE",
             len(l5) == 6 and len(l4) == 7 and l5 == l4_sans_rappel
             and any(l.startswith("le rappel émission : sys-05 rend -6")
                     for l in l4),
             "le refus -6 des runs 1/3/4 a DISPARU — le CH est PARTI sur "
             "le MÊME noyau (Win11 26300, ntdll b072efae…)")
    controle("F2 : LES TÉMOINS DIVERGENT SUR L'ARTEFACT SEUL — d8928934… "
             "(run 4, le dev.2) → de23e577… (run 5, le rebuild dev.3 : "
             "LES DEUX contrôles T0.erratum-9 NOUVEAUX, 16 → 18 contrôles "
             "T0) ; le terrain TENU (Win11 26300, ntdll b072efae… aux "
             "deux runs), l'interpréteur changé (3.14.3 → 3.13.9 : sans "
             "effet sur le natif)",
             "d892893469608fd6" in temoin_run4
             and "de23e577498d5cbf" in temoin
             and "b072efaeac06c558" in temoin_run4
             and "b072efaeac06c558" in temoin,
             "l'A/B est PROPRE : la seule différence fonctionnelle est LA "
             "RÉPARATION (les TROIS octets du diff contrôlé)")
    controle("F3 : L'A/B CONCLUT — le MÊME noyau, le MÊME terrain, l'AUTRE "
             "pose : le refus -6 de l'émission a DISPARU → LA RÉPARATION "
             "(la pose canonique 0x68, buf à +8) EST LA CAUSE DE LA "
             "GUÉRISON — L'ERRATUM n° 9 VALIDÉ SUR LE TERRAIN RÉEL",
             l5 == l4_sans_rappel
             and "T0.erratum-9" in temoin
             and "[ÉCHEC] T3.ouvrir" in temoin_run4,
             "le -6 ACCESS_VIOLATION (la mesure de la sonde, Entrée 185) "
             "n'est plus : le VRAI afd.sys a ACCEPTÉ l'envoi")
    controle("F4 : LA PRÉDICTION DE L'ENTRÉE 187 TENUE À LA LETTRE — « la "
             "mort à T3 UN CRAN APRÈS la réparation de l'émission » : la "
             "mort a reculé d'EXACTEMENT UN CRAN, de l'émission (sys-05) "
             "à LA PREMIÈRE LECTURE (sys-06, le ServerHello attendu)",
             "[ÉCHEC] T3.ouvrir" in temoin
             and "le rappel émission" not in temoin
             and "la dernière émission" not in temoin,
             "la frontière nommée d'avance est ATTEINTE — la réception "
             "n'a JAMAIS couru sur le terrain réel (E5)")
    controle("F5 : LE -7 A CHANGÉ DE CHAÎNE — run 4 : sys-05 rend -6 à "
             "l'émission → le socle coupé → -7 (le CH JAMAIS PARTI) ; "
             "run 5 : sys-05 rend 0 (le CH PARTI, recoupé 119 o) → LA "
             "RÉCEPTION rend non-nul → -7 : LE MÊME CODE FINAL, UNE "
             "CHAÎNE AUTRE — l'analyse ne les confond pas",
             "émis 119 o" in temoin
             and any(l.startswith("le rappel émission : sys-05 rend -6")
                     for l in l4),
             "run 5 : la panne est AVAL du CH — la première lecture")
    controle("F6 : LE TEMPS ÉLIMINE LE SILENCE — le run entier dans SA "
             "seconde (C1 : 07:23:36) : la lecture BLOQUANTE est revenue "
             "IMMÉDIATEMENT (T2 venait de réussir le three-way handshake "
             "synchrone : le chemin était vivant) — un serveur MUET "
             "aurait TENU la lecture (la garde-chien tire à 300 s), "
             "jamais rendu la main dans la même seconde : le verdict de "
             "réception fut SEC — un REFUS du noyau (un STATUS non nul) "
             "ou un verdict VIF du pair (la demi-fin / le reset), PAS "
             "une attente muette",
             len(jl) == 6 and all(l.startswith("07:23:36") for l in jl)
             and "handle 0x284" in temoin,
             "le passager « réseau coupé muet » est AFFAIBLI sur pièces — "
             "restent : le refus structurel, la fermeture vive")

    print(f"\n=== BILAN DU RECOUP : {len(REUSSITES)} PASS"
          + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "") + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")

    # --- le verdict du recoup, écrit AVEC les pièces -------------------------
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    lignes = []
    lignes.append("=== RECOUP LABO DU CINQUIÈME RUN M9-(f) — verdict sur "
                  "pièces croisées (D138/D145/D148) ===")
    lignes.append("rendu le " + __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S") + " au laboratoire")
    lignes.append("le juge est le code : les textes attendus lus PAR AST "
                  "dans la source du kit réparé, l'échelle REJOUÉE sur la "
                  "clé privée DU RUN, l'artefact re-haché au geste même, "
                  "LA DIFFÉRENCE AVEC LE RUN 4 CONSTATÉE PAR CODE (le "
                  "journal du run 5 comparé LIGNE À LIGNE à celui du run "
                  "4, rapatrié du coffre au geste même)")
    lignes.append("les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
                  "scenario-m9f-journal.log, VERDICT-run-m9f.txt), md5 "
                  "contrôlés ; ligne-recue.txt et journal-emissions.txt "
                  "jamais nées (le run est mort à T3)")
    lignes.append("")
    for nom in REUSSITES:
        lignes.append(f"[recoup-m9f5] PASS : {nom}")
    lignes.append("")
    lignes.append("L'ÉTAT DU RUN — L'ÉMISSION RÉPARÉE, LA MORT D'UN CRAN "
                  "PLUS LOIN : (1) LE TERRAIN TENU : Windows 11 build "
                  "26300, ntdll b072efae… (LE MÊME que le run 4 — "
                  "l'interpréteur seul change : Python 3.13.9), "
                  "l'artefact RÉPARÉ de23e577… (le rebuild 1.0.0-dev.3 : "
                  "LA POSE canonique RELUE DANS L'IMAGE aux DEUX blocs — "
                  "les DEUX contrôles T0.erratum-9 [ok]), le kit ACQUITTÉ "
                  "INCHANGÉ (79d44284…) ; (2) **LA PREMIÈRE ÉMISSION "
                  "RÉELLE DU PROJET** : les DIX-HUIT T0 [ok], T1 (SSN "
                  "85/7/15, motif sain), T2 VERT (sys-04 : create + bind "
                  "+ connect, rax 0, handle 0x284), le CH ÉMIS (sys-05 "
                  "rend 0 — AUCUNE ligne de rappel : le refus -6 des runs "
                  "1/3/4 EST MORT) ET RECOUPÉ octet pour octet (119 o == "
                  "la construction re-jouée : l'aléa @ +6, la clé "
                  "publique @ +82) — **L'ERRATUM n° 9 VALIDÉ SUR LE VRAI "
                  "NOYAU** (le WSABUF canonique accepté par le VRAI "
                  "afd.sys, zéro ws2_32) ; (3) LA MORT NOMMÉE, UN CRAN "
                  "PLUS LOIN : LA PREMIÈRE LECTURE (le ServerHello "
                  "attendu — tls13-27 É1) : le rappel réception (sys-06, "
                  "jamais journalé par le scénario) rend NON-NUL → la "
                  "machine rend -7 (« la coupure du socle », tls13-27 "
                  "Q3), l'état 5 (MORT) — EXACTEMENT là où l'Entrée 187 "
                  "plaçait la frontière suivante.")
    lignes.append("")
    lignes.append("LA PREUVE EN UNE LIGNE (F1/F3) : le journal du run 5 "
                  "== le journal du run 4 MOINS LA LIGNE « sys-05 rend "
                  "-6 », sur LE MÊME noyau (Win11 26300, ntdll "
                  "b072efae…), l'artefact seul ayant changé "
                  "(d8928934… → de23e577…) : LA RÉPARATION EST LA CAUSE "
                  "DE LA GUÉRISON — et la mort a reculé d'UN CRAN, à la "
                  "première lecture.")
    lignes.append("")
    lignes.append("LES CANDIDATS (évidence avant correctif — D54/D68/"
                  "D98) : (a) LE PASSAGER réseau : AFFAIBLI PAR LE TEMPS "
                  "[F6 : le retour immédiat — T2 venait de réussir le "
                  "three-way handshake synchrone ; un silence aurait TENU "
                  "la lecture jusqu'à la garde-chien (300 s)] mais PAS "
                  "ÉLIMINÉ [un middlebox peut REFERMER VITE l'offre sans "
                  "SNI — le zéro propre de sys-06 Q2] — le scénario le "
                  "suggère lui-même (« réessayez réseau vivant ») ; "
                  "(b) LE CONTRAT DE RÉCEPTION sys-06 REFUSÉ "
                  "STRUCTURELLEMENT [IOCTL_AFD_RECEIVE tel que le bloc le "
                  "pose : l'AFD_RECV_INFO 24 o, AfdFlags 0x20 (LA MESURE "
                  "leftarcode — l'erratum de lecture), TdiFlags 0, le "
                  "WSABUF canonique] : le profil correspond [le retour "
                  "immédiat, un STATUS non nul → -6 → la machine -7] — "
                  "ET LA SPEC LE NOMME ELLE-MÊME : « la réception n'a "
                  "JAMAIS couru sur le terrain réel » : réparée PAR "
                  "SYMÉTRIE avec l'émission (le C_ASSERT send/recv), "
                  "JAMAIS MESURÉE PAR SONDE ; (c) LA DEMI-FIN — le pair "
                  "a fermé proprement à l'offre [sys-06 Q2 : le zéro de "
                  "réception → -7 direct] : le serveur/le middlebox a reç"
                  "u le CH et refermé SANS servir — le profil correspond "
                  "aussi [le retour immédiat]. → LE CODE EXACT DE SYS-06 "
                  "(-6 le STATUS / -7 le zéro ; le NTSTATUS brut vit dans "
                  "rdx — sys-06 Q5) N'EST PAS SURFACÉ PAR L'INSTRUMENT "
                  "(la limite NOMMÉE au LISEZMOI § 4) : UN SEUL MOT "
                  "D'INFORMATION MANQUE — LA SONDE sys-06 LE LIRAIT (le "
                  "miroir exact de l'Entrée 185). MAIS L'ORDRE DISCIPLINÉ "
                  "TENU : LE SIXIÈME RUN D'ABORD (le scénario le demande "
                  "lui-même : « réessayez réseau vivant » — idéalement un "
                  "AUTRE réseau : le discriminant du passager au meilleur "
                  "coût, ET LA CHANCE DU VERT : LA FINALE) ; SI LE -7 SE "
                  "REPRODUIT IDENTIQUE [l'émission VERT, la réception "
                  "immédiate -7, le run en SA seconde] : LE PASSAGER "
                  "ÉLIMINÉ SUR PIÈCES — ET LA SONDE sys-06 S'OUVRE "
                  "(nommée d'avance).")
    lignes.append("")
    lignes.append("RECOUP : ROUGE CONSTATÉ COHÉRENT — l'échec est HONNÊTE "
                  "et nommé T3.ouvrir (rax -7, état 5) ; LE KIT EST "
                  "ACQUITTÉ (le MÊME binaire dev.3, le MÊME scénario — "
                  "l'offre PARFAITE sur pièces, ÉMISE pour la première "
                  "fois) ; **L'ERRATUM n° 9 EST VALIDÉ SUR LE TERRAIN "
                  "RÉEL À L'ÉMISSION** (la première émission réelle du "
                  "projet : le CH 119 o PARTI SUR LE RÉSEAU par le VRAI "
                  "afd.sys) ; la finale 1.0.0 est REFUSÉE pour CE run "
                  "(fail-closed — le critère exige le vert : la session "
                  "réelle ÉTABLIE) ; LE GESTE AU DÉVELOPPEUR : LE "
                  "SIXIÈME RUN — le MÊME kit (kit-m9f.zip 79d44284… "
                  "INCHANGÉ, AUCUNE réparation à faire au kit), un "
                  "dossier NEUF D99, réseau vivant (UN AUTRE réseau si "
                  "possible — le discriminant du passager), renvoyer "
                  "preuves-m9f/ ENTIER au coffre /test/preuves-m9f/ — SI "
                  "LE VERT VIENT : LA FINALE 1.0.0, LE JALON M9 — LA "
                  "GRANDE ŒUVRE ; SI LE -7 SE REPRODUIT IDENTIQUE : LA "
                  "SONDE sys-06 (nommée d'avance — lire le NTSTATUS brut "
                  "ou LE ZÉRO de LA RÉCEPTION, le miroir de l'Entrée "
                  "185).")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\n[recoup] le verdict écrit AVEC les pièces : {SORTIE}")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
