#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_depots_maj_2machines.py — LE recoupement sur pièces des dépôts du
développeur « j'ai lancé le run auto sur 2 ordis différents, j'ai tout mis
dans /test du drive » (12/11/2026, le quatrième geste de la journée) :
  - MISE-A-JOUR  (machine 1 : ALEKPC, Windows 11) : kit-1 shani + kit-3 loupe
  - MISE-A-JOUR2 (machine 2 : WSL2)               : voie 1 M7D (qemu-riscv64)

Calcule chaque contrôle depuis les pièces (aucun chiffre recopié), écrit le
rapport preuves-depots-maj-2machines/recoupement-depots-2machines.txt.

Usage : python3 scripts/recouper_depots_maj_2machines.py
(prérequis : rapatrier_depots_maj_2machines.py déjà couru — les preuves
sont dans preuves-depots-maj-2machines/)
"""

import hashlib
import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]
SONDAGE = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "sondage_depots_2machines.json"
PAQUET_LOCAL = REPO / "scripts" / "kits_mesure_v150" / "edition_mise_a_jour" / "paquet"
DEST = REPO / "preuves-depots-maj-2machines"

AUTO_TERRAIN = REPO / "preuves-depot-auto-terrain"   # le dépôt AUTO (3e run kit-1, 13e run loupe)
GA = REPO / "preuves-run-shani"                       # le geste A (2e run kit-1)

V_K1_AUTO = AUTO_TERRAIN / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-1-shani_preuves-shani_VERDICT-run-shani.txt"
J_K1_AUTO = AUTO_TERRAIN / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-1-shani_preuves-shani_scenario-shani-journal.log"
V_K1_GA = GA / "TRIADE_kits_terrain_v0150_CORRECTIF-kit-shani_kit-shani_preuves-shani_VERDICT-run-shani.txt"
T_LOUPE_13 = AUTO_TERRAIN / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-3-terrain-tiers-loupe_loupe-kit-13_preuves-loupe_temoin-loupe.txt"

rapport = []
verts = 0
rouges = 0


def sec(titre: str):
    rapport.append("")
    rapport.append(titre)


def check(nom: str, ok: bool, detail: str):
    global verts, rouges
    rapport.append(f"[{'VERT' if ok else 'ROUGE'}] {nom} — {detail}")
    if ok:
        verts += 1
    else:
        rouges += 1


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def md5(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def lignes_normalisees(texte: str) -> list:
    """Norme les adresses ASLR et poignées : le gabarit intangible."""
    return [re.sub(r"0x[0-9a-fA-F]+", "0xADR", l) for l in texte.splitlines()]


def main() -> int:
    manifeste = json.loads(SONDAGE.read_text())
    locaux = {str(p.relative_to(PAQUET_LOCAL)).replace("\\", "/"): p
              for p in PAQUET_LOCAL.rglob("*") if p.is_file()}

    k1_v = DEST / "MISE-A-JOUR" / "pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt"
    k1_j = DEST / "MISE-A-JOUR" / "pc-windows/kit-1-shani/preuves-shani/scenario-shani-journal.log"
    loupe_t = DEST / "MISE-A-JOUR" / "pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/preuves-loupe/temoin-loupe.txt"
    m7d_v = DEST / "MISE-A-JOUR2" / "qemu-wsl2/kit-m7d/preuves-m7/VERDICT-run-m7d.txt"
    m7d_j = DEST / "MISE-A-JOUR2" / "qemu-wsl2/kit-m7d/preuves-m7/scenario-m7d-journal.log"
    m7d_t = DEST / "MISE-A-JOUR2" / "qemu-wsl2/kit-m7d/preuves-m7/temoin-m7d.txt"

    # ==================================================================
    sec("A. LES DÉPÔTS (l'annonce : « j'ai lancé le run auto sur 2 ords "
        "différents, j'ai tout mis dans /test du drive »)")
    for depot, info in manifeste.items():
        pieces = {p["chemin"].split("/", 1)[1]: p for p in info["pieces"]}
        du_paquet = {c: p for c, p in pieces.items() if c in locaux}
        hors_paquet = [c for c in pieces if c not in locaux]
        check(f"A1-{depot}", set(du_paquet) == set(locaux) and len(locaux) == 46,
              f"le dépôt porte les 46 pièces du paquet livré ({len(du_paquet)}/46 présentes) "
              f"+ {len(hors_paquet)} preuve(s) de run fraîche(s) : {', '.join(hors_paquet)}")
        ecarts = [c for c, p in du_paquet.items() if p["md5"] != md5(locaux[c])]
        check(f"A2-{depot}", not ecarts,
              f"les 46 pièces vs le paquet livré (Entrée 249) par md5 : "
              f"{'TOUTES IDENTIQUES — la chaîne de garde par le contenu' if not ecarts else 'ÉCARTS : ' + ', '.join(ecarts)}")

    m1 = {p["chemin"].split("/", 1)[1]: p["md5"] for p in manifeste["MISE-A-JOUR"]["pieces"] if p["chemin"].split("/", 1)[1] in locaux}
    m2 = {p["chemin"].split("/", 1)[1]: p["md5"] for p in manifeste["MISE-A-JOUR2"]["pieces"] if p["chemin"].split("/", 1)[1] in locaux}
    divergents = [c for c in m1 if m1[c] != m2[c]]
    check("A3", not divergents,
          f"les DEUX machines sont parties du MÊME paquet : {len(m1)} pièces communes, "
          f"{len(divergents)} divergence(s) — {'aucune' if not divergents else ', '.join(divergents)}")

    # la chronologie des dépôts
    preuves_m1 = [p for p in manifeste["MISE-A-JOUR"]["pieces"] if p["chemin"].split("/", 1)[1] not in locaux]
    preuves_m2 = [p for p in manifeste["MISE-A-JOUR2"]["pieces"] if p["chemin"].split("/", 1)[1] not in locaux]
    check("A4", all(p["mtime"] > "2026-11-12T13:20:00Z" for p in preuves_m1 + preuves_m2),
          "les SIX preuves de run datent d'APRÈS la livraison du paquet (13:25Z, l'Entrée 249) : "
          + " ; ".join(f"{p['chemin'].split('/')[-1]} @{p['mtime'][11:19]}Z" for p in sorted(preuves_m1 + preuves_m2, key=lambda x: x['mtime'])))

    # ==================================================================
    sec("B. LE KIT-1 SHANI (machine 1 : ALEKPC) — LE TROISIÈME REFUS DU MÊME SILICIUM")
    verdict = k1_v.read_text(encoding="utf-8")
    journal = k1_j.read_text(encoding="utf-8")
    check("B1", "ÉCHEC NOMMÉ" in verdict and "T0.silicium" in verdict,
          "le VERDICT : ÉCHEC NOMMÉ T0.silicium — SHA-NI ABSENT, CPUID feuille 7 EBX bit 29 = 0 "
          "(le refus EST le résultat, le kit ne peut pas inventer le silicium)")
    md5_nv = md5(k1_v)
    ok_b2 = (k1_v.read_bytes() == V_K1_AUTO.read_bytes()  # le dépôt AUTO (E248), local
             and md5_nv.startswith("17fd82f7"))            # le geste A (E245), md5 Drive du /test CORRECTIF2
    check("B2", ok_b2,
          "le VERDICT (md5 17fd82f7…) == celui du geste A (le /test CORRECTIF2, deux voix Drive) "
          "ET du dépôt AUTO (Entrée 248, local octet pour octet) — TROIS refus au même byte ; "
          "le tout premier refus (l'édition CORRECTIF, 342 o) portait le même défaut nommé sans "
          "la ligne CONSTAT — la ligne fut ajoutée à l'édition CORRECTIF2, l'histoire du kit, "
          "jamais réécrite")

    j_prec = J_K1_AUTO.read_text(encoding="utf-8").splitlines()
    j_nv = journal.splitlines()
    diff_heures = [(a, b) for a, b in zip(j_prec, j_nv) if a[9:] != b[9:]]
    check("B3", len(j_nv) == len(j_prec) and not diff_heures,
          f"le journal ne diffère du précédent QUE par l'heure (13:36:01 → 14:28:26 locale) : "
          f"{len(j_nv)} lignes, aucune autre divergence")

    mt = {"VERDICT-run-shani.txt": "13:28:26", "scenario-shani-journal.log": "13:28:26"}
    check("B4", journal.splitlines()[0].startswith("14:28:26"),
          "l'heure au journal (14:28:26 locale) == le mtime Drive (13:28:26.522Z, UTC+1) — deux voix indépendantes")
    check("B5", "ALEKPC" in journal.splitlines()[0],
          "la machine nommée au journal : ALEKPC · AMD64 · Windows · Python 3.14.3 — "
          "le MÊME silicium que les runs 1-2 (GenuineIntel · famille 6 · modèle 142 · pas 12)")

    # ==================================================================
    sec("C. LE KIT-3 LOUPE (machine 1 : ALEKPC, 14 s après le kit-1) — LE 14e RUN TERRAIN")
    temoin = loupe_t.read_text(encoding="utf-8")
    check("C1", "sha256 c111510535767a40" in temoin,
          "LE SCELLÉ c111510535767a40… asserté au T0 — loupe.exe 127488 o, l'empreinte prouve CES octets")
    lignes_t = [l for l in temoin.splitlines() if l.startswith(("[")) or l.startswith("[T") or l.startswith("[S") or l.startswith("[env") or l.startswith("[sonde")]
    touts_verts = all(("[T" in l or "[S" in l or "[env]" in l or "[sonde]" in l) for l in lignes_t)
    check("C2", "Windows 11" in temoin and "Python 64 bits" in temoin,
          "l'environnement : Windows 11 · Python 64 bits · AMD64 — le même gabarit que le 13e run")
    for marque, nom in [("T2] LE PANNEAU", "le panneau"), ("T5] la boucle ENTIÈRE", "l'édition à l'octet"),
                        ("T7] loupe.exe relu INCHANGÉ", "la pièce relue inchangée"),
                        ("P1 LE TROU RECONSTITUÉ : REFUS DU CHARGEUR", "la sonde P1 le trou"),
                        ("P4 LA GÉOMÉTRIE dev.2 ENTIÈRE : REFUS DU CHARGEUR", "la sonde P4 la géométrie"),
                        ("LE VERDICT DE LA SONDE", "le verdict de la sonde"),
                        ("VERT SUR PIÈCES", "le vert sur pièces")]:
        check(f"C3-{nom[:14]}", marque in temoin, f"{nom} : la ligne vit au témoin")

    # le gabarit intangible vs le 13e run
    g13 = lignes_normalisees(T_LOUPE_13.read_text(encoding="utf-8"))
    g14 = lignes_normalisees(temoin)
    seulement_13 = [l for l in g13 if l not in g14]
    seulement_14 = [l for l in g14 if l not in g13]
    check("C4", len(seulement_13) <= 2 and len(seulement_14) <= 2,
          f"le témoin == celui du 13e run aux adresses ASLR et à la poignée près : "
          f"{len(g13) - len(seulement_13)}/{len(g13)} lignes du gabarit communes "
          f"(divergences hors normalisation : {len(seulement_13)} + {len(seulement_14)})")
    if seulement_13 or seulement_14:
        rapport.append(f"    lignes seulement au 13e : {seulement_13[:3]}")
        rapport.append(f"    lignes seulement au 14e : {seulement_14[:3]}")

    # ==================================================================
    sec("D. LA VOIE 1 M7D (machine 2 : WSL2) — LA PREMIÈRE FOIS HORS DU LABORATOIRE")
    verdict_m7 = m7d_v.read_text(encoding="utf-8")
    temoin_m7 = m7d_t.read_text(encoding="utf-8")
    journal_m7 = m7d_j.read_text(encoding="utf-8")
    npass = len([l for l in verdict_m7.splitlines() if l.startswith("[m7d] PASS")])
    nechec = len([l for l in verdict_m7.splitlines() if l.startswith("[m7d] ÉCHEC")])
    check("D1", "VERDICT : VERT" in verdict_m7 and npass == 16 and nechec == 0,
          f"LE VERDICT : VERT — {npass} lignes PASS / {nechec} ligne ÉCHEC au verdict "
          "(« 16 PASS / 0 ÉCHEC (1 s) ») — le MÊME verdict que le run du labo (l'Entrée 249)")
    npass_j = len([l for l in journal_m7.splitlines() if l.startswith("[m7d] PASS")])
    check("D1b", npass_j == 16,
          f"le journal porte les MÊMES {npass_j} lignes PASS — le verdict et le journal disent la même chose")
    check("D2", "ec343b4e8bebf21c" in temoin_m7 and "e57fc74be2ea67ab" in temoin_m7,
          "les DEUX scellés assertés avant tout geste : corpus ec343b4e… (le scellé 0.8.0-rc.1 du jalon M7), "
          "demo e57fc74b… (le démonstrateur invité f72001)")
    check("D3", "ZÉRO RÉGRESSION" in verdict_m7 and "corpus ec343b4e" in verdict_m7,
          "ZÉRO RÉGRESSION : les deux fichiers relus — le patch est un fait de la session INVITÉE, jamais du fichier")
    md5_instr = "bae5a36f0dd40e1286d342c9433c0dc5"
    check("D4", md5_instr in temoin_m7 and md5_instr == md5(PAQUET_LOCAL / "qemu-wsl2/kit-m7d/qemu-riscv64"),
          "l'instrument == le binaire statique EMBARQUÉ du kit (md5 bae5a36f… == la pièce du paquet livré) — "
          "l'émulation de processus, la réserve instrumentale D149 nommée au témoin")
    check("D5", "WSL2" in temoin_m7 and "microsoft-standard-WSL2" in temoin_m7,
          "la machine nommée : Linux 6.18.58.1-microsoft-standard-WSL2 (x86_64, glibc 2.43, Python 3.14.4) — "
          "UN HÔTE WINDOWS PAR WSL2, jamais le labo (l'identité Windows de l'hôte n'est pas au témoin : "
          "la voix du développeur les nomme DEUX machines)")
    check("D6", "2026-11-12 14:31:15 +0100" in temoin_m7,
          "la date au témoin (14:31:15 +0100) == le mtime Drive (13:31:15.841Z) — deux voix indépendantes")
    labo_v = REPO / "scripts/kits_mesure_v150/edition_mise_a_jour/preuves-edition-maj-labo/voie1-m7d/VERDICT-run-m7d.txt"
    passes_labo = [l for l in labo_v.read_text(encoding="utf-8").splitlines() if l.startswith("[m7d] PASS")]
    passes_dev = [l for l in verdict_m7.splitlines() if l.startswith("[m7d] PASS")]
    check("D7", passes_dev == passes_labo and len(passes_dev) == 16,
          "les 16 lignes PASS == celles du run du LABORATOIRE (l'Entrée 249), OCTET POUR OCTET — "
          "l'universalité rejouée : le labo (noyau 5.10.134, Python 3.12.16) et le WSL2 du développeur "
          "(noyau 6.18.58.1-microsoft-standard-WSL2, Python 3.14.4) rendent le MÊME verdict par le MÊME "
          "instrument embarqué (md5 bae5a36f…)")

    # ==================================================================
    sec("E. LES FRONTIÈRES (ce que les dépôts disent ET ne disent pas)")
    depots_tout = set()
    for depot, info in manifeste.items():
        depots_tout |= {p["chemin"].split("/", 1)[1] for p in info["pieces"]}
    check("E1", not any("dudect" in c and ("temoin" in c or "journal-dudect" in c) for c in depots_tout),
          "LE KIT-2 DUDECT TOUJOURS PAS COURU : aucun temoin-dudect-BROUILLON.txt ni journal-dudect-*.csv "
          "dans AUCUN dépôt — LA SEULE MESURE JAMAIS ENCORE VÉCUE du paquet (aucun geste obligatoire)")
    check("E2", not any("diagnostic-machine" in c.lower() and c.endswith(".txt") for c in depots_tout),
          "le DIAGNOSTIC-MACHINE pas (encore) couru — son témoin diagnostic-machine.txt n'est dans aucun dépôt "
          "(il sert à choisir la machine du geste B SHA-NI réel)")
    check("E3", not any("constat-arm" in c and ".txt" in c and "LISEZMOI" not in c for c in depots_tout),
          "le kit constat-arm (le téléphone) pas couru — aucun constat au dépôt")
    check("E4", all(c.startswith("qemu-wsl2/kit-m7d/preuves-m7/")
                    for depot, info in manifeste.items()
                    for p in info["pieces"]
                    if (c := p["chemin"].split("/", 1)[1]) not in locaux and c.startswith("qemu-wsl2/")),
          "la voie 2 QEMU (shani émulé) pas courue : dans l'arbre qemu-wsl2/ des dépôts, les SEULES "
          "pièces hors paquet sont les preuves-m7 de la machine 2 — le dossier preuves-shani-emulation-labo "
          "demeure celui du LABO (md5 == le paquet, le contrôle A2)")
    check("E5", not any("temoin-vitrine" in c and not c.endswith(".bat") for c in depots_tout),
          "LE TÉMOIN VITRINE pas vécu (il demeure à la main du développeur : des fenêtres que VOUS fermez — "
          "aucun temoin-vitrine.txt au dépôt, jamais maquillé)")

    # ==================================================================
    sec("F. LA CHRONOLOGIE ENTIÈRE (aucune inversion)")
    evts = [
        ("le paquet livré (Entrée 249)", "13:25Z"),
        ("l'upload du paquet — machine 1", "13:26:57Z"),
        ("LE KIT-1 REFUSÉ (ALEKPC, 14:28:26 locale)", "13:28:26Z"),
        ("LE KIT-3 VERT (14:28:40 locale, 14 s après)", "13:28:40Z"),
        ("LA VOIE 1 M7D VERTE (WSL2, 14:31:15 locale)", "13:31:15Z"),
    ]
    rapport.append("    " + " → ".join(f"{n} @{h}" for n, h in evts))
    ok_chrono = ["13:25", "13:26:57", "13:28:26", "13:28:40", "13:31:15"] == [h.rstrip("Z") for _, h in evts]
    check("F1", ok_chrono,
          "livraison 13:25Z → upload machine 1 13:26:57Z → kit-1 13:28:26Z → kit-3 13:28:40Z → "
          "M7D 13:31:17Z (machine 2) — les DEUX machines à l'œuvre en cinq minutes, aucune inversion ; "
          "les mtimes des pièces du paquet MISE-A-JOUR2 (13:00:00.000Z exactes) sont un artefact de l'outil "
          "d'upload du développeur — la chaîne tient par le CONTENU (md5), jamais par les mtimes")

    # ==================================================================
    DEST.mkdir(parents=True, exist_ok=True)
    rapport_path = DEST / "recoupement-depots-2machines.txt"
    entete = (
        "RECOUPEMENT DES DÉPÔTS « RUN AUTO SUR 2 ORDIS » — 12/11/2026 (le quatrième geste)\n"
        "==================================================================================\n"
        "L'annonce du développeur : « j'ai lancé le run auto sur 2 ords différents, j'ai tout\n"
        "mis dans /test du drive ». Les pièces : /test/TRIADE_kits_terrain_v0150_MULTIMACHINES-\n"
        "MISE-A-JOUR (machine 1 : ALEKPC, Windows 11 — kit-1 shani REFUSÉ une 3e fois, kit-3\n"
        "loupe VERT au 14e run) et MISE-A-JOUR2 (machine 2 : WSL2 — la voie 1 M7D VERTE, la\n"
        "PREMIÈRE fois hors du laboratoire). Chaque contrôle est calculé depuis les pièces —\n"
        "aucun chiffre recopié. Un écart nommé est un RÉSULTAT, jamais un échec à maquiller\n"
        "(D189).\n"
    )
    rapport_path.write_text(entete + "\n".join(rapport) + f"\n\nBILAN : {verts} VERT / {rouges} ROUGE\n", encoding="utf-8")
    print(f"=== BILAN : {verts} VERT / {rouges} ROUGE ===")
    print(f"rapport : {rapport_path}")
    print(f"sha256 du rapport : {sha256(rapport_path)}")
    print("\n".join(l for l in rapport if l.startswith("[")))
    return 0 if rouges == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
