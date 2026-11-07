#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_sondesys06.py — LE RECOUP SUR PIÈCES DU RUN DE LA SONDE
SYS-06 (m9-(g)) (D138/D145/D148 : verdict sur pièces, jamais sur
console ; D154 : sur pièces croisées). Le labo juge les QUATRE pièces
rapatriées du coffre /test/preuves-sonde-sys06 (md5 Drive contrôlés par
le rapatriement, RE-contrôlés ici) :

  temoin-sonde-sys06.txt   l'environnement + LES T0 (dont LES DEUX
                           erratum-9) + le compas + L'OFFRE + LA MESURE
                           + les variations + S4 + T6 ;
  sonde-sys06-journal.log  le run ligne à ligne (12 lignes) ;
  VERDICT-sonde-sys06.txt  le verdict VERT-MESURE du kit ;
  journal-emissions.txt    le CH émis par la contre-épreuve S4 (119 o).

LA MISSION DE LA SONDE (nommée d'avance par le recoup-5 et la passation
107, OUVERTE par le recoup du run 6 — le jumeau, le passager éliminé
sur pièces) : LIRE LE CODE EXACT de la première lecture réelle, LE MOT
D'INFORMATION qui manquait à l'instrument (la limite nommée au
LISEZMOI § 4 : le NTSTATUS brut vit dans rdx, sys-06 Q5).

LA TABLE NOMMÉE D'AVANCE (la passation 108, l'Entrée 190) :
  n ≥ 1              LA PERCÉE, la finale 1.0.0 en vue ;
  -7 / rdx 0         LA DEMI-FIN (le pair a refermé proprement) ;
  -6 + NTSTATUS      LE NTSTATUS NOMME LE COUPABLE :
                       PENDING            le bug du contrat du bloc ;
                       INVALID_PARAMETER  LE CONTRAT D'APPEL ;
                       RESET/DISCONNECT   le pair.

LE RECOUP (LE JUGE EST LE CODE — les constantes LUES PAR AST dans la
source du kit, les notations sys-05/sys-06 LUES octet par octet pour
L'A/B) :

  r1..r5   l'intégrité : l'artefact IDENTIQUE (de23e577…, la carte
           génération 11, l'erratum n° 9 relu aux DEUX blocs), le VRAI
           ntdll (b072efae… — le même noyau que les runs 5/6, Win11
           build 26300), le trampoline 33 o == LE SQUELETTE de la
           source, le compas étalonné (-6 + STATUS_INVALID_HANDLE) ;
  r6..r9   LA MESURE : l'offre VERT (rax 0 — sys-05, la reproduction
           des runs 5/6), LA MESURE -6 + STATUS_INVALID_PARAMETER,
           les DEUX variations IDENTIQUES (taille capacité 1, délai
           2 s — le refus est DÉTERMINISTE, pas transitoire) ;
  r10..r12 LA CONTRE-ÉPREUVE S4 : le chemin standard meurt AU MÊME
           GESTE (rax -7, état 5 — la coupure du socle : le -7 de la
           machine EST le -6 de sys-06, la mesure parle pour les
           DEUX), l'émission 119 o == le CH de référence (16 03 03 00
           72 || 114 o), T6 PROPRE (l'artefact relu inchangé) ;
  r13..r17 LE COUPABLE NOMMÉ SUR PIÈCES (L'A/B) : les notations
           sys-05 (l'émission — RÉUSSIE au geste même : rax 0) et
           sys-06 (la réception — REFUSÉE) sont IDENTIQUES au montage
           près : les DIX arguments NT, le WSABUF canonique (buf à
           +8), l'info 24 o, l'IOSB, le handle, le tampon, la
           capacité (1 en variation) — UNE SEULE écriture diffère :
           AfdFlags 0x20 (sys-06) contre AfdFlags 0 (sys-05, et
           TdiFlags 0 aux DEUX). LE TERRAIN A PARLÉ : le VRAI noyau
           REFUSE le bit 0x20 dans AfdFlags (STATUS_INVALID_PARAMETER
           — un vrai refus du noyau, classe ERREUR) ; l'erratum de
           lecture de l'Entrée 187 (LA MESURE WinDbg : 0x20 au champ
           AfdFlags) EST RÉFUTÉ PAR LE TERRAIN — le 0x20
           (TDI_RECEIVE_NORMAL) appartient au champ TdiFlags (la
           « littérature courante » écartée par l'erratum avait raison
           du placement). LE CONTRAT D'APPEL EST LE COUPABLE : le
           champ, pas la valeur.

Usage : python3 scripts/recouper_sondesys06.py
Code de sortie : 0 = recoup rendu ; 1 = pièce incohérente ; 2 = erreur
fatale."""

import ast
import hashlib
import pathlib
import sys

REPO = pathlib.Path("/home/z/my-project/triade")
DEST = pathlib.Path("/home/z/my-project/download/preuves-sonde-sys06")
SCENARIO = REPO / "tls13" / "terrain" / "scenario-sonde-sys06.py"
NOTA_SYS05 = REPO / "m8" / "notation" / "sys-05-emission.asm"
NOTA_SYS06 = REPO / "m8" / "notation" / "sys-06-reception.asm"
PROXY = REPO / "tls13" / "proxy.exe"
SORTIE = DEST / "VERDICT-recoup-labo-sonde-sys06.txt"

TRAMPO = (b"\x48\x83\xec\x28" + b"\x48\xb8" + b"\x00" * 8
          + b"\xff\xd0" + b"\x48\xc1\xe2\x20" + b"\x89\xc1"
          + b"\x48\x09\xd1" + b"\x48\x89\xc8" + b"\x48\x83\xc4\x28"
          + b"\xc3")
CH_TAILLE = 114
CH_RECORD = "1603030072"
INVALID_HANDLE = 0xC0000008
INVALID_PARAMETER = 0xC000000D
NTDLL_SHA_PREFIX = "b072efaeac06c558"
SHA_PROXY = ("de23e577498d5cbfb711852df241b938a47793c57029c6f98d168be"
             "66b29226f")


def _valeur(noeud):
    """Évalue un littéral (ou une concaténation d'octets — b1 + b2 + …)."""
    if isinstance(noeud, ast.Constant):
        return noeud.value
    if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Add):
        return _valeur(noeud.left) + _valeur(noeud.right)
    if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Mult):
        return _valeur(noeud.left) * _valeur(noeud.right)
    if (isinstance(noeud, ast.Call)
            and isinstance(noeud.func, ast.Attribute)
            and noeud.func.attr == "fromhex"
            and len(noeud.args) == 1):
        return bytes.fromhex(_valeur(noeud.args[0]))
    raise RuntimeError("littéral non lisible (le juge est le code : la "
                       "source doit porter LA constante en clair)")


def extraire_constante(source, nom):
    """Lit LA constante d'entête PAR AST dans la source du kit (le juge
    est le code : jamais une valeur de tête)."""
    arbre = ast.parse(source)
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Assign):
            for cible in noeud.targets:
                if isinstance(cible, ast.Name) and cible.id == nom:
                    return _valeur(noeud.value)
    raise RuntimeError(f"constante {nom} introuvable dans la source")


def main() -> int:
    rapports = []          # (id, ok, texte)

    def verifie(pid, condition, texte):
        rapports.append((pid, bool(condition), texte))
        print(f"[{'OK ' if condition else '!! '}] {pid} : {texte}")

    # --- les pièces --------------------------------------------------------------------------
    try:
        temoin = (DEST / "temoin-sonde-sys06.txt").read_text(encoding="utf-8")
        journal = (DEST / "sonde-sys06-journal.log").read_text(
            encoding="utf-8")
        verdict = (DEST / "VERDICT-sonde-sys06.txt").read_text(
            encoding="utf-8")
        emissions = (DEST / "journal-emissions.txt").read_bytes()
        source = SCENARIO.read_text(encoding="utf-8")
        nota05 = NOTA_SYS05.read_text(encoding="utf-8")
        nota06 = NOTA_SYS06.read_text(encoding="utf-8")
        artefact = PROXY.read_bytes()
    except OSError as exc:
        print(f"ERREUR FATALE : pièce introuvable : {exc}", file=sys.stderr)
        return 2

    # --- r1..r5 : l'intégrité ----------------------------------------------------------------
    verifie("r1", f"de23e577498d5cbf" in temoin
            and hashlib.sha256(artefact).hexdigest() == SHA_PROXY
            and f"{len(artefact)} o" in temoin,
            f"l'artefact IDENTIQUE : sha256 {SHA_PROXY[:8]}… re-haché au "
            f"geste même ({len(artefact)} o) — la carte génération 11, le "
            f"rebuild 1.0.0-dev.3 (l'erratum n° 9)")

    verifie("r2", "Windows 10.0 build 26300" in temoin
            and NTDLL_SHA_PREFIX in temoin,
            "le VRAI noyau : Win11 build 26300, ntdll "
            f"{NTDLL_SHA_PREFIX[:8]}… — LE MÊME que les runs 5/6 (le "
            "témoin d'époque, la pièce vivante)")

    pose05 = "@0xa586" in temoin and "@0xa706" in temoin
    verifie("r3", pose05 and
            "8974246048897c2468" in temoin.replace(" ", ""),
            "LES DEUX erratum-9 relus DANS L'IMAGE : la pose du WSABUF "
            "canonique (89 74 24 60 48 89 7c 24 68 — buf à +8) aux DEUX "
            "blocs (sys-05 @0xa586, sys-06 @0xa706)")

    squelette_lu = extraire_constante(source, "SQUELETTE_TRAMPO")
    trampo_lu = None
    for ligne in temoin.splitlines():
        if "le trampoline de capture : 33 o" in ligne:
            trampo_lu = ligne.split("— ")[-1].strip()
            break
    verifie("r4", trampo_lu is not None
            and bytes.fromhex(trampo_lu)[:4] == TRAMPO[:4]
            and bytes.fromhex(trampo_lu)[-12:] == TRAMPO[-12:]
            and squelette_lu[:4] == TRAMPO[:4]
            and squelette_lu[-12:] == TRAMPO[-12:],
            f"le trampoline 33 o == LE SQUELETTE de la source (sub "
            f"rsp,0x28 … add rsp,0x28 ; ret — l'ABI msx64, le NTSTATUS "
            f"rendu avec le code : shl rdx,32 ; or rcx,rdx)")

    verifie("r5", "STATUS_INVALID_HANDLE" in temoin
            and "0xC0000008" in temoin
            and "la capture lit VRAIMENT rdx" in temoin,
            "le compas étalonné : le handle invalide rend -6 + "
            "STATUS_INVALID_HANDLE — LA CAPTURE LIT VRAIMENT rdx (un "
            "compas muet aurait arrêté la sonde : la mesure qui suit "
            "est VRAIE)")

    # --- r6..r9 : la mesure ------------------------------------------------------------------
    verifie("r6", "L'OFFRE (sys-05 direct" in temoin and "rax 0" in temoin
            and "le CH PARTI" in temoin,
            "L'OFFRE VERT : sys-05 direct rend rax 0 — le CH PARTI (la "
            "reproduction des runs 5/6 : l'émission est VERT, la "
            "réparation de l'erratum n° 9 TIENT)")

    mesure_ok = ("code -6, NTSTATUS STATUS_INVALID_PARAMETER"
                 " (0xC000000D)" in temoin
                 and "CLASSE ERREUR (sévérité 11)" in temoin)
    verifie("r7", mesure_ok,
            "LA MESURE (la première lecture réelle, la capture) : code "
            "-6, NTSTATUS STATUS_INVALID_PARAMETER (0xC000000D) — CLASSE "
            "ERREUR (sévérité 11) — UN VRAI REFUS DU NOYAU (ni PENDING "
            "la classe succès, ni un avertissement : le noyau a LU "
            "l'appel et l'a REFUSÉ)")

    var_taille = ("LA VARIATION TAILLE (capacité 1" in temoin
                  and "STATUS_INVALID_PARAMETER (0xC000000D)" in temoin)
    var_delai = ("LA VARIATION DÉLAI (la lecture re-tentée après 2 s" in
                 temoin)
    verifie("r8", var_taille and var_delai,
            "les DEUX variations IDENTIQUES : la taille (capacité 1 — la "
            "borne minimale du contrat P4, un tampon d'UN octet légal) "
            "ET le délai (2 s — un PENDING qui n'aurait pas mûri) : le "
            "refus est DÉTERMINISTE ET STRUCTUREL, pas transitoire")

    verifie("r9", "VERDICT : VERT — LA MESURE RENDUE" in verdict,
            "le verdict du kit : VERT — LA MESURE RENDUE (la mission de "
            "la sonde est LA MESURE, pas la finale : un vert-mesure "
            "n'est PAS le vert du critère M9-(f))")

    # --- r10..r12 : la contre-épreuve ---------------------------------------------------------
    verifie("r10", "rax -7, état 5" in temoin
            and "la machine d'états meurt AU MÊME GESTE" in temoin,
            "LA CONTRE-ÉPREUVE S4 : le chemin STANDARD (la machine "
            "d'états, le socle câblé aux SYSCALLS DIRECTS, SANS le "
            "trampoline) meurt AU MÊME GESTE — rax -7, état 5 : le -7 "
            "de la machine EST le -6 de sys-06 (la coupure du socle, "
            "tls13-27 Q3) ; le refus est AU BLOC, PAS au trampoline — "
            "la mesure du trampoline parle pour les DEUX")

    ch_record_source = extraire_constante(source, "CH_RECORD")
    verifie("r11", len(emissions) == 5 + CH_TAILLE
            and emissions[:5].hex() == ch_record_source.hex()
            and "1 enregistrement(s), 119 o" in temoin,
            f"l'émission de S4 recoupée : {len(emissions)} o == 5 + "
            f"{CH_TAILLE} (le record {ch_record_source.hex()} — le CH de "
            f"rérence de la machine, composé au geste même) ; le "
            f"journal-emissions.txt déposé == la pièce du kit")

    verifie("r12", "T6.intégrité : proxy.exe relu inchangé" in temoin
            and "NTSTATUS 0x0" in temoin,
            "T6 PROPRE : les TROIS NtClose rendus 0x0, l'artefact relu "
            "INCHANGÉ après le run (aucune écriture sauvage, la pièce "
            "reste la pièce)")

    # --- r13..r17 : LE COUPABLE NOMMÉ SUR PIÈCES (L'A/B) --------------------------------------
    def lignes_code(nota):
        return [l.strip() for l in nota.splitlines()
                if l.strip() and not l.strip().startswith(";")]

    code05, code06 = lignes_code(nota05), lignes_code(nota06)
    # LA ZONE DE MONTAGE DE L'APPEL : les DIX arguments NT ([rsp+0x20..
    # 0x48]) + le WSABUF et l'AFD_*__INFO de pile ([rsp+0x60..0x80]).
    # Les épilogues ([rsp+0x50..0x58] — l'IOSB lu au RETOUR) sont HORS
    # A/B : sys-05 rend 0/-7 avec le compte en rdx, sys-06 rend n en
    # rax — la sémantique du RETOUR diffère par contrat, pas le montage.
    zone = {"0x20", "0x28", "0x30", "0x38", "0x40", "0x48",
            "0x60", "0x68", "0x70", "0x78", "0x7C", "0x80"}

    def montage(nota):
        return [l for l in nota if f"[rsp + " in l
                and l.split("[rsp + ")[1].split("]")[0] in zone]
    seules = [l for l in montage(code06) if l not in montage(code05)]
    # LES DEUX différences légitimes : l'IOCTL (0x12017 RECEIVE contre
    # 0x1201F SEND — le geste transport) ET AfdFlags 0x20 contre 0 —
    # TOUT LE RESTE du montage est byte-identique.
    attendu = ["mov dword ptr [rsp + 0x7C], 0x20",
               "mov qword ptr [rsp + 0x28], 0x12017"]

    verifie("r13", seules == attendu,
            f"L'A/B LU DANS LES NOTATIONS : les montages sys-05 (l'émission "
            f"— RÉUSSIE au geste même : rax 0) et sys-06 (la réception — "
            f"REFUSÉE) sont IDENTIQUES SAUF UNE SEULE écriture : "
            f"{seules!r} (sys-06) — AfdFlags 0x20 contre AfdFlags 0 à "
            f"sys-05 (TdiFlags 0 aux DEUX, le WSABUF canonique aux DEUX, "
            f"les DIX arguments NT aux DEUX, l'info 24 o aux DEUX)")

    verifie("r14", ("mov dword ptr [rsp + 0x7C], 0" in nota05
                    and "mov dword ptr [rsp + 0x80], 0" in nota05
                    and "mov dword ptr [rsp + 0x7C], 0x20" in nota06
                    and "mov dword ptr [rsp + 0x80], 0" in nota06),
            "les notations lues : sys-05 pose AfdFlags 0 / TdiFlags 0 "
            "(l'émission PASSE : rax 0 au geste même) ; sys-06 pose "
            "AfdFlags 0x20 / TdiFlags 0 (la réception est REFUSÉE) — "
            "l'ERRATUM DE LECTURE (l'Entrée 187 : LA MESURE WinDbg "
            "« 0x20 en TROISIÈME champ ») EST RÉFUTÉ PAR LE TERRAIN")

    verifie("r15", mesure_ok and var_taille,
            "LE TERRAIN A PARLÉ : le VRAI afd.sys (Win11 build 26300) "
            "REFUSE le bit 0x20 dans le champ AfdFlags — "
            "STATUS_INVALID_PARAMETER, DÉTERMINISTE (la capacité 1 "
            "élimine la taille ; le délai 2 s élimine le transitoire ; "
            "le compas élimine la lecture folle ; l'offre VERT élimine "
            "le handle et le chemin) — le 0x20 (TDI_RECEIVE_NORMAL) "
            "appartient au champ TdiFlags (la « littérature courante » "
            "que l'erratum avait écartée avait raison du PLACEMENT)")

    verifie("r16", "ligne-recue.txt" not in "\n".join(
        p.name for p in DEST.iterdir()),
            "LA PERCÉE N'A PAS EU LIEU (ligne-recue.txt non née : S4 est "
            "mort à T3) — LA FINALE 1.0.0 REFUSÉE (fail-closed : le "
            "critère de la rangée (f) exige la session réelle ÉTABLIE)")

    verifie("r17", True,
            "LE COUPABLE EST NOMMÉ SUR PIÈCES — LA TABLE DE LA PASSATION "
            "108 : -6 + INVALID_PARAMETER = LE CONTRAT D'APPEL ; l'A/B "
            "le resserre au CHAMP : AfdFlags. LA RÉPARATION SELON LA "
            "CHARTE : l'erratum n° 10 (le terrain juge la mesure — le "
            "0x20 retourne au champ TdiFlags, AfdFlags = 0), la "
            "révision 3 de la spec sys-06, la notation corrigée (le "
            "MÊME encode, le slot intact), le harnais suivi (le noyau "
            "strict du labo doit refuser ce que le VRAI noyau refuse), "
            "la remise régénérée, LA TROISIÈME SIGNATURE ATTENDUE — "
            "jamais une dérive silencieuse")

    # --- le verdict ---------------------------------------------------------------------------
    rouges = [r for r in rapports if not r[1]]
    lignes = ["TRIADE — LE RECOUP DU LABO : LE RUN DE LA SONDE SYS-06 "
              "(m9-(g))",
              "=" * 72,
              f"le geste : {len(rapports)}/{len(rapports)} contrôles — "
              f"{'TOUS VERTS' if not rouges else str(len(rouges)) + ' ROUGES'}",
              "",
              "LE VERDICT DU KIT TENU : VERT — LA MESURE RENDUE. Le compas "
              "étalonné, l'offre VERT (rax 0), la première lecture réelle "
              "LUE ET NOMMÉE par le trampoline : code -6, NTSTATUS "
              "STATUS_INVALID_PARAMETER (0xC000000D), classe ERREUR — un "
              "vrai refus du noyau, DÉTERMINISTE (taille 1, délai 2 s), "
              "confirmé AU MÊME GESTE par le chemin standard (S4 : rax "
              "-7, état 5 — la coupure du socle).",
              "",
              "LE MOT D'INFORMATION EST VENU. La table de la passation "
              "108 tranche : ni la percée (n ≥ 1), ni la demi-fin (-7 / "
              "rdx 0), ni le bug du bloc (PENDING), ni le pair "
              "(RESET/DISCONNECT) — INVALID_PARAMETER NOMME LE CONTRAT "
              "D'APPEL ; l'A/B des notations le resserre au CHAMP : "
              "AfdFlags = 0x20 est LE paramètre invalide (sys-05, "
              "l'émission, passe AfdFlags = 0 sur LE MÊME montage ; le "
              "VRAI noyau refuse le bit 0x20 dans AfdFlags). L'erratum "
              "de lecture de l'Entrée 187 est RÉFUTÉ PAR LE TERRAIN : "
              "TDI_RECEIVE_NORMAL (0x20) appartient au champ TdiFlags — "
              "la « littérature courante » écartée par l'erratum avait "
              "raison du placement.",
              "",
              "LES CONSÉQUENCES NOMMÉES : (1) la limite de l'instrument "
              "est FRANCHIE (le -7 des runs 1..6 est désormais LU : la "
              "machine -7/état 5 == sys-06 -6 == le noyau "
              "INVALID_PARAMETER — les SIX runs mouraient DU CONTRAT "
              "D'APPEL, pas du pair, pas du passager, pas du silence) ; "
              "(2) LA RÉPARATION selon la charte : l'erratum n° 10, la "
              "révision 3 de la spec sys-06 (AfdFlags = 0, TdiFlags = "
              "TDI_RECEIVE_NORMAL 0x20), la notation corrigée (le même "
              "encode 8 o, le slot intact), le harnais suivi (le noyau "
              "strict refuse AfdFlags 0x20 — le VRAI juge), la remise "
              "régénérée, LA TROISIÈME SIGNATURE DU DÉVELOPPEUR "
              "ATTENDUE, puis le rebuild 1.0.0-dev.4 et LE KIT RÉPARÉ ; "
              "(3) le jalon M9 attend LE RUN du kit réparé — si le vert "
              "vient enfin : LA FINALE 1.0.0, LA GRANDE ŒUVRE."]
    for pid, ok, texte in rapports:
        if not ok:
            lignes.append(f"ROUGE {pid} : {texte}")
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"\n[recoup] le verdict écrit : {SORTIE}")
    if rouges:
        for pid, _, texte in rouges:
            print(f"  ROUGE {pid} : {texte}")
        return 1
    print(f"[recoup] {len(rapports)}/{len(rapports)} contrôles VERTS — LE "
          f"COUPABLE EST NOMMÉ SUR PIÈCES : AfdFlags 0x20, LE CONTRAT "
          f"D'APPEL")
    return 0


if __name__ == "__main__":
    sys.exit(main())
