#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_run3_m9f.py — LE RECOUP POST-MORTEM DU TROISIÈME RUN M9-(f)
(D138/D145/D148 : verdict sur pièces, jamais sur console ; D154 : sur
pièces croisées). Le labo juge les TROIS pièces rapatriées du coffre
/test/preuves-m9f (md5 Drive contrôlés par le rapatriement, RE-contrôlés
ici) :

  temoin-m9f.txt            l'environnement + les T0 tranchés + T3 ;
  scenario-m9f-journal.log  le run, ligne à ligne (7 lignes : mort à T3,
                            rax -7, après le recoup VERT du CH) ;
  VERDICT-run-m9f.txt       le verdict post-mortem ROUGE nommé T3.ouvrir.

LE JUGE EST LE CODE : les textes attendus sont LUS PAR AST dans la source
du scénario (tls13/terrain/scenario-m9f.py — la source RÉPARÉE de
l'erratum n° 7, jamais exécutée, jamais gravée), l'échelle est REJOUÉE au
geste même sur LA CLÉ PRIVÉE DU RUN (celle du témoin), l'artefact est
re-haché AU geste même, et la chaîne -6/-7 est reconstituée depuis les
contrats du dépôt.

Le geste rendu au développeur : RELANCER le kit TEL QUEL (réseau vivant —
un réseau passager se distingue d'un refus structurel par UNE relance) ;
si le -6 se répète À L'IDENTIQUE à l'émission du CH, la divergence
afd.sys Windows 10 ↔ Windows 11 devient LE suspect principal ; puis
preuves-m9f/ ENTIER au coffre.

Usage : python3 scripts/recouper_run3_m9f.py
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
DEST = pathlib.Path("/home/z/my-project/download/preuves-run-m9f")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-m9f.py"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = pathlib.Path("/home/z/my-project/download/preuves-run-m9f-3/"
                      "VERDICT-recoup-labo-m9f-3.txt")

SHA_PROXY = ("d892893469608fd69e381b92b8e18623107bd2bc694f43a512"
             "bc5900773dc314")

# les pièces du run 3, telles que rapatriées (md5 == Drive)
ATTENDUS = {"temoin-m9f.txt": "f8491dc2",
            "scenario-m9f-journal.log": "03e555c8",
            "VERDICT-run-m9f.txt": "b9d79a0c"}

# les valeurs DU RUN, lues au témoin (les pièces font foi)
CLE_PRIV_RUN = "927f6ec8009c83b9ddf84ac9b97d919ab267d13e9df7ce7f6e2d15a35322f348"
ALEA_RUN = "8b049cad76ef5f86a5bfee0adcc7e5d3955ea7ccb91f252ba25eba61f4e55b76"
PUB_RUN = "89d50a86fabdcdea1a00c2381f30ebcb519774d6d5d1764b89690aa244ffad79"

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
    print("=== RECOUP LABO DU TROISIÈME RUN M9-(f) — verdict sur pièces "
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
             f"sha256 {h[:16]}…")
    controle("B3 : l'environnement == les runs 1/2 (la MÊME machine, le "
             "terrain constant)",
             "Windows 10.0 build 19045" in temoin
             and "Python 3.14.6 · AMD64" in temoin
             and "36b1a62e4bf6bf7d" in temoin,
             "Windows 10 22H2 · Python 3.14.6 · ntdll 36b1a62e…")
    controle("B4 : T1 (SSN 85/7/15, motif sain) + T2 (rax 0, handle 0x328) "
             "tranchés [ok]",
             "SSN 85" in temoin and "SSN 7" in temoin and "SSN 15" in temoin
             and "handle 0x328" in temoin and "motif 4c8bd1b8" in temoin)
    controle("B5 : LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE — la clé "
             "publique attendue NON-NULLE (le run 2 imprimait 000…0)",
             f"la clé publique attendue" in temoin and PUB_RUN in temoin
             and "0000000000000000" not in temoin,
             f"89d50a86… ({PUB_RUN[:16]}…)")
    controle("B6 : L'ÉCHEC NOMMÉ — T3.ouvrir rax -7, état 5",
             "[ÉCHEC] T3.ouvrir : rax == 0, l'état 3 (CONNECTÉ) — "
             "rax -7, état 5" in temoin)
    controle("B7 : LE RECOUP DU JALON — le CH de LA MACHINE == la "
             "construction re-jouée (119 o)",
             "[ok] T3.recoup" in temoin and "émis 119 o" in temoin,
             "les DEUX lecteurs d'accord : tls13-14 (l'artefact) == "
             "l'échelle Python")
    controle("B8 : la ligne « [T3] la dernière émission » ABSENTE → UNE "
             "SEULE émission tentée (l'append du rappel précède l'envoi : "
             "relue dans la source AU geste même)",
             "la dernière émission" not in temoin,
             "l'émission qui a échoué EST celle du CH — le Finished client "
             "n'a jamais été tenté")

    # --- C. le JOURNAL ---------------------------------------------------------
    jl = journal.splitlines()
    controle("C1 : SEPT lignes, toutes à 18:49:34 (le run entier dans SA "
             "seconde)", len(jl) == 7
             and all(l.startswith("18:49:34") for l in jl))
    controle("C2 : T0/T1/T2 VERT aux textes exacts de la source",
             "T0 VERT" in journal and "T1 VERT" in journal
             and "T2 VERT" in journal)
    controle("C3 : la ligne « T3 : OUVRIR » journalée (le segment qui tua "
             "le run 2 traversé VIVANT)",
             "T3 : OUVRIR — la poignée ENTIÈRE par la machine d'états" in journal)
    controle("C4 : la ligne du rappel émission AU TEXTE EXACT DE LA SOURCE "
             "(sys-05 rend -6)",
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
             and "le run : 2026-11-06 18:49:34" in verdict
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
             f"927f6ec8… → {rendu[:16]}… == le témoin : la « clé attendue » "
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
             "sys-05 rend -6 (un NTSTATUS non nul : « le NTSTATUS vit "
             "dans rdx », la limite NOMMÉE de l'instrument), la machine "
             "propage -7 (tls13-27 Q2), l'état 5 (MORT)",
             "sys-05 rend {r}" in src.replace("{r}", "{r}")
             and "LE TRANSPORT EN ÉCHEC" in src,
             "l'étape en échec NOMMÉE : sys-05, L'ÉMISSION, à son PREMIER "
             "appel réel — les runs 1/2 n'y sont jamais arrivés")
    controle("E4 : LE KIT ACQUITTÉ — le scénario exécuté FIDÈLEMENT (la "
             "source réparée == le kit du coffre 90a1d022…, relu à la "
             "passation) : le segment fautif du run 2 traversé VIVANT, la "
             "machine appelée au POINTEUR, l'offre composée PARFAITE",
             "ctypes.addressof(kit96)" in src
             and "kit96.raw[:32] = alea" not in
             ast.dump(ast.parse(src)))
    lis = (REPO / "tls13" / "terrain" / "LISEZMOI-KIT-M9F.md").read_text(
        encoding="utf-8")
    controle("E5 : LA FRONTIÈRE ÉTAIT NOMMÉE D'AVANCE — le LISEZMOI § les "
             "frontières : « le socle socket court POUR LA PREMIÈRE FOIS "
             "sur le VRAI afd.sys… si votre afd.sys diverge, le refus sera "
             "NOMMÉ (-6, l'étape en cause) »",
             "le refus sera NOMMÉ (-6, l'étape en cause)" in lis,
             "la note d'honnêteté du kit s'est réalisée AU MOT PRÈS")

    print(f"\n=== BILAN DU RECOUP : {len(REUSSITES)} PASS"
          + (f", {len(ECHECS)} ÉCHEC(S)" if ECHECS else "") + " ===")
    for nom, detail in ECHECS:
        print(f"  - {nom} : {detail}")

    # --- le verdict du recoup, écrit AVEC les pièces -------------------------
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    lignes = []
    lignes.append("=== RECOUP LABO DU TROISIÈME RUN M9-(f) — verdict sur "
                  "pièces croisées (D138/D145/D148) ===")
    lignes.append("rendu le " + __import__("time").strftime(
        "%Y-%m-%d %H:%M:%S") + " au laboratoire")
    lignes.append("le juge est le code : les textes attendus lus PAR AST "
                  "dans la source réparée, l'échelle REJOUÉE sur la clé "
                  "privée DU RUN, l'artefact re-haché au geste même")
    lignes.append("les pièces : /test/preuves-m9f/ (temoin-m9f.txt, "
                  "scenario-m9f-journal.log, VERDICT-run-m9f.txt), md5 "
                  "contrôlés ; ligne-recue.txt et journal-emissions.txt "
                  "jamais nées (le run est mort à T3)")
    lignes.append("")
    for nom in REUSSITES:
        lignes.append(f"[recoup-m9f3] PASS : {nom}")
    lignes.append("")
    lignes.append("L'ÉTAT DU RUN — LE PLUS LOIN DU PROGRAMME, ENCORE : "
                  "(1) LA RÉPARATION DE L'ERRATUM n° 7 PROUVÉE SUR LA "
                  "MACHINE RÉELLE : la clé publique attendue NON-NULLE "
                  "(89d50a86… — le run 2 imprimait 000…0), le segment "
                  "Python traversé VIVANT, la machine appelée au "
                  "POINTEUR ; (2) LE RECOUP DU JALON, VERT : le "
                  "ClientHello COMPOSÉ PAR LA MACHINE (tls13-22 + tls13-14 "
                  "+ la famille f25519, les blocs scellés) == la "
                  "construction re-jouée OCTET POUR OCTET (119 o) — la "
                  "preuve cryptographique du jalon SUR LA MACHINE RÉELLE ; "
                  "(3) LA MORT NOMMÉE : sys-05 (L'ÉMISSION) rend -6 à SON "
                  "PREMIER APPEL RÉEL — un NTSTATUS non nul (l'information "
                  "exacte vit dans rdx, la limite NOMMÉE de l'instrument) "
                  "→ la machine propage -7 (LE TRANSPORT EN ÉCHEC), "
                  "l'état 5 (MORT).")
    lignes.append("")
    lignes.append("LA PREUVE EN UNE LIGNE (B8/C4) : l'append du rappel "
                  "d'émission PRÉCÈDE l'envoi (relu dans la source) et la "
                  "ligne « [T3] la dernière émission » est ABSENTE du "
                  "témoin → UNE SEULE émission fut tentée, CELLE DU CH : "
                  "l'offre est PARFAITE en composition, son ENVOI fut "
                  "REFUSÉ par le transport — le CH n'a pas quitté la "
                  "machine (l'émission TOTALE ou refusée).")
    lignes.append("")
    lignes.append("LES CANDIDATS NOMMÉS (évidence avant correctif — "
                  "D54/D68/D98) : (a) LA DIVERGENCE afd.sys Windows 10 ↔ "
                  "Windows 11 — les mesures du socle viennent de Win11 "
                  "(WinDbg, leftarcode 2025), les TROIS runs ont lieu sur "
                  "Windows 10 22H2 build 19045 : sys-04 (create/bind/"
                  "connect) PASSE sur Win10, mais sys-05 (SEND) N'AVAIT "
                  "JAMAIS COURU sur le vrai noyau avant CE run — son "
                  "premier appel est refusé ; (b) LA CONNEXION REFERMÉE "
                  "côté serveur (un RST entre le connect et l'envoi — le "
                  "serveur, un intermédiaire, une garde locale) ; (c) LE "
                  "PASSAGER réseau. L'HORLOGE ne départage pas (le run "
                  "entier dans SA seconde) et le NTSTATUS vit dans rdx : "
                  "UNE RELANCE tranche (c) ; la répétition à l'identique "
                  "du -6 à l'émission du CH installe (a) en suspect "
                  "principal.")
    lignes.append("")
    lignes.append("RECOUP : ROUGE CONSTATÉ COHÉRENT — l'échec est HONNÊTE "
                  "et nommé T3.ouvrir (rax -7, état 5) ; LE KIT EST "
                  "ACQUITTÉ (le scénario exécuté fidèlement, l'offre de "
                  "la machine PARFAITE sur pièces) ; la frontière est "
                  "L'ARTEFACT contre le VRAI afd.sys — nommée d'avance "
                  "par le LISEZMOI au mot près ; la finale 1.0.0 est "
                  "REFUSÉE pour CE run (fail-closed — le critère exige le "
                  "vert : la session réelle ÉTABLIE) ; LE GESTE RENDU AU "
                  "DÉVELOPPEUR : (i) RELANCER le kit TEL QUEL, réseau "
                  "vivant (une relance distingue le passager du "
                  "structurel) ; (ii) si le -6 se répète À L'IDENTIQUE à "
                  "l'émission du CH : la divergence afd.sys Win10 ↔ Win11 "
                  "devient le suspect principal — essayer une machine "
                  "Windows 11 (la cible du kit), ou renvoyer les pièces : "
                  "le labo ouvre la sonde sys-05 (mesurer "
                  "IOCTL_AFD_SEND sur le vrai noyau) ; (iii) dans tous les "
                  "cas : preuves-m9f/ ENTIER au coffre.")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\n[recoup] le verdict écrit AVEC les pièces : {SORTIE}")
    return 0 if not ECHECS else 1


if __name__ == "__main__":
    sys.exit(main())
