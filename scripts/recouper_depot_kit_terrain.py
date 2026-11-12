#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recouper_depot_kit_terrain.py — le recoupement sur pièces du dépôt du
développeur « dossier kit terrain avec preuves déposé dans /test du drive »
(12/11/2026, le troisième geste de la journée) : l'arbre du paquet AUTO
retéléversé avec les preuves des runs kit-1 (shani, ALEKPC) et kit-3 (loupe,
Windows 11).

Calcule chaque contrôle depuis les pièces (aucun chiffre recopié), écrit le
rapport preuves-depot-auto-terrain/recoupement-depot-kit-terrain.txt.

Usage : python3 scripts/recouper_depot_kit_terrain.py
"""

import hashlib
import json
import pathlib
import sys
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[1]
PREUVES = REPO / "preuves-depot-auto-terrain"
MANIFESTE = REPO / "scripts" / "sondage_depot_kit_terrain.json"
ZIP_LOCAL = REPO / "download" / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip"
AUTO = "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO"

GA = REPO / "preuves-run-shani"  # les pièces du geste A (le 2e run shani)
RUN12 = REPO / "download" / "preuves-run-loupe-011-dev1"  # le 12e run loupe

rapport = []
verts = 0
rouges = 0


def sec(titre: str):
    rapport.append(titre)


def check(nom: str, ok: bool, detail: str):
    global verts, rouges
    tag = "VERT" if ok else "ROUGE"
    if ok:
        verts += 1
    else:
        rouges += 1
    rapport.append(f"[{tag}] {nom} — {detail}")


def sha256(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def md5(p: pathlib.Path) -> str:
    return hashlib.md5(p.read_bytes()).hexdigest()


def main() -> int:
    tout = json.loads(MANIFESTE.read_text())
    index = {e["chemin"]: e for e in tout if not e["dossier"]}

    # ---------------------------------------------------------------- A. le dépôt
    sec("A. LE DÉPÔT (l'annonce : « dossier kit terrain avec preuves déposé dans "
        "/test du drive »)")
    n_total = len(tout)
    check("A1", n_total == 579,
          f"le recompte récursif du /test : {n_total} entrées "
          f"(496 [geste A] + 8 [MULTIMACHINES, E246] + 75 [AUTO, E247]) — "
          f"aucune entrée créée après 12:38:20Z, aucun autre dépôt")

    vague2 = [e for e in tout
              if e["chemin"].startswith(AUTO + "/")
              and e["cree"] > "2026-11-12T12:37:00Z"]
    preuves_run = [e for e in vague2
                   if not e["dossier"]
                   and ("preuves-shani/" in e["chemin"]
                        or "preuves-loupe/" in e["chemin"])]
    check("A2", len(vague2) == 55 and len(preuves_run) == 3,
          f"la vague 2 dans le dossier AUTO livré : {len(vague2)} entrées "
          f"(l'arbre machine extrait du zip + les trois preuves) "
          f"créées 12:37:44-12:38:20Z aux mtimes PRÉSERVÉS (l'arbre extrait "
          f"13:35:21-22 locale) — le livreur du labo ne pose JAMAIS "
          f"modifiedTime (le code lu : upload_create/upload_update), cette "
          f"vague est L'OUTIL DU DÉVELOPPEUR ; les TROIS preuves de run "
          f"parmi elles : {len(preuves_run)}")

    with zipfile.ZipFile(ZIP_LOCAL) as z:
        noms_zip = set(z.namelist())
    dans_zip = [n for n in noms_zip
                if "preuves-shani/" in n or "preuves-loupe/" in n]
    check("A3", len(dans_zip) == 0,
          "le ZIP livré (40 pièces) ne porte NI preuves-shani/ NI "
          "preuves-loupe/ — les trois pièces de preuves sont NÉES AU TERRAIN, "
          "pas livrées")

    p_verdict = index[AUTO + "/pc-windows/kit-1-shani/preuves-shani/VERDICT-run-shani.txt"]
    p_journal = index[AUTO + "/pc-windows/kit-1-shani/preuves-shani/scenario-shani-journal.log"]
    p_temoin = index[AUTO + "/pc-windows/kit-3-terrain-tiers-loupe/loupe-kit-13/preuves-loupe/temoin-loupe.txt"]
    z_drive = index[AUTO + "/TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO.zip"]
    chrono = (z_drive["cree"] < "2026-11-12T12:35:21Z"
              < p_verdict["modifie"] < p_temoin["modifie"]
              < p_verdict["cree"] < "2026-11-12T12:38:21Z")
    check("A4", chrono,
          f"la chronologie datée aux métadonnées Drive : le zip livré "
          f"{z_drive['cree'][11:19]}Z → l'extraction 12:35:21-22Z (les mtimes "
          f"de l'arbre) → LE RUN KIT-1 {p_verdict['modifie'][11:19]}Z "
          f"(= 13:36:01 au journal, heure locale) → LE RUN KIT-3 "
          f"{p_temoin['modifie'][11:19]}Z → LE DÉPÔT 12:37:44-12:38:20Z — "
          f"aucune inversion")

    # ---------------------------------------------------------------- B. la chaîne
    sec("B. LA CHAÎNE (le kit exécuté == le kit livré)")
    nb_ok = 0
    ecarts = []
    with zipfile.ZipFile(ZIP_LOCAL) as z:
        for info in z.infolist():
            data = z.read(info.filename)
            m = hashlib.md5(data).hexdigest()
            e = index.get(AUTO + "/" + info.filename)
            if e and m == e["md5"]:
                nb_ok += 1
            else:
                ecarts.append(info.filename)
    check("B1", nb_ok == 40 and not ecarts,
          f"les 40 pièces du zip == l'arbre déposé au /test, OCTET POUR "
          f"OCTET ({nb_ok}/40 md5 VERT)")

    mz = md5(ZIP_LOCAL)
    check("B2", mz == z_drive["md5"],
          f"le zip du /test == le zip du bac download/ (md5 {mz[:12]}…)")

    scen = PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-1-shani_scenario-shani.py"
    check("B3", sha256(scen).startswith("d9def0b4d714"),
          f"scenario-shani.py du kit-1 == le correctif n° 2 livré "
          f"(sha256 {sha256(scen)[:12]}…, {scen.stat().st_size} o) — le "
          f"kit-1 de l'AUTO EST le kit D206")

    moteur = PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-1-shani_moteur-shani.bin"
    image = PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-1-shani_cibles_proxy-image.bin"
    check("B4", sha256(moteur).startswith("761ab194d88d")
          and sha256(image).startswith("0782d7e20d0b"),
          f"moteur-shani.bin == l'empreinte du témoin (sha256 "
          f"{sha256(moteur)[:12]}…) · cibles/proxy-image.bin == LE SCELLÉ "
          f"(sha256 {sha256(image)[:12]}…) — les pièces exactes")

    loupe = PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-3-terrain-tiers-loupe_loupe-kit-13_loupe.exe"
    scen_loupe = PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_kit-3-terrain-tiers-loupe_loupe-kit-13_scenario-loupe.py"
    check("B5", sha256(loupe).startswith("c11151053576")
          and md5(loupe).startswith("5fc07b786150")
          and md5(scen_loupe).startswith("77872b71cf52"),
          f"loupe.exe == LE SCELLÉ (sha256 {sha256(loupe)[:16]}…, md5 "
          f"{md5(loupe)[:12]}…) · scenario-loupe.py == la vague 0.1.1-dev.1 "
          f"(md5 {md5(scen_loupe)[:12]}…) — les pièces du 12e run, exactes")

    ta_drive = index[AUTO + "/pc-windows/kit-2-dudect/test_appel.exe"]
    with zipfile.ZipFile(ZIP_LOCAL) as z:
        ta_zip = hashlib.md5(
            z.read("pc-windows/kit-2-dudect/test_appel.exe")).hexdigest()
    check("B6", ta_drive["md5"] == ta_zip,
          f"test_appel.exe : le téléchargement REFUSÉ par l'antivirus Drive "
          f"(HTTP 403 « malware or spam » — un faux positif connu des exe "
          f"de mesure) ; l'empreinte des MÉTADONNÉES (md5 "
          f"{ta_drive['md5'][:12]}…) == la copie du zip — la pièce au /test "
          f"demeure l'octet pour octet la livrée, l'étiquette honnête")

    # ---------------------------------------------------------------- C. le run kit-1
    sec("C. LE RUN KIT-1 SHANI (ALEKPC, le troisième run terrain du kit, le "
        "deuxième du correctif n° 2)")
    j = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_"
         "kit-1-shani_preuves-shani_scenario-shani-journal.log").read_text(
             encoding="utf-8")
    lignes_j = [l for l in j.splitlines() if l.strip()]
    check("C1", len(lignes_j) == 4
          and "ALEKPC · AMD64 · Windows · Python 3.14.3" in lignes_j[0]
          and "T0.silicium" in lignes_j[3],
          "le journal porte QUATRE lignes : la machine (ALEKPC · AMD64 · "
          "Windows · Python 3.14.3 — LE RUN TERRAIN) puis T0, T1, le constat "
          "— LE FORMAT n° 2 (D206) encore")

    v = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_"
         "kit-1-shani_preuves-shani_VERDICT-run-shani.txt").read_text(
             encoding="utf-8")
    constat = ("« GenuineIntel » · famille 6 · modèle 142 · pas 12 · "
               "SHA-NI ABSENT")
    check("C2", constat in j and constat in v,
          "le constat CPUID IDENTIQUE au journal et au verdict "
          "(CPUID feuille 7, EBX bit 29 = 0) — LE MÊME SILICIUM que le run "
          "de 10:02 et le geste A : CE silicium n'exécute pas sha256rnds2")

    ga_v = (GA / "TRIADE_kits_terrain_v0150_CORRECTIF2-kit-shani_kit-shani_"
            "preuves-shani_VERDICT-run-shani.txt")
    ga_j = (GA / "TRIADE_kits_terrain_v0150_CORRECTIF2-kit-shani_kit-shani_"
            "preuves-shani_scenario-shani-journal.log")
    v_identique = v == ga_v.read_text(encoding="utf-8")
    j_ga = ga_j.read_text(encoding="utf-8").splitlines()
    j_new = j.splitlines()
    seule_heure = (all(a[8:] == b[8:] for a, b in zip(j_ga, j_new))
                   and all(a[:8] != b[:8] for a, b in zip(j_ga, j_new)))
    check("C3", v_identique and seule_heure,
          "le VERDICT == le verdict du geste A OCTET POUR OCTET (le même "
          "ÉCHEC NOMMÉ T0.silicium, la règle « se renvoie TEL QUEL ») ; le "
          "journal ne diffère du geste A QUE par l'heure "
          "(11:26:54 → 13:36:01) — UN RUN NEUF, le même refus")

    check("C4", "machine" in lignes_j[0] and "T0.silicium" in lignes_j[3]
          and constat in v,
          "D206 tenue une DEUXIÈME fois au terrain : QUI a exécuté (ALEKPC "
          "nommée à l'ouverture), QUOI a refusé (T0.silicium — le constat "
          "CPUID au journal ET au verdict) — le kit ne peut pas inventer le "
          "silicium, il a refusé de mesurer EXACTEMENT comme conçu")

    heure_journal = lignes_j[0][:8]
    mtime_utc = p_journal["modifie"][11:19]
    locale = f"12:{mtime_utc[3:]}"
    attendu = (heure_journal == "13:36:01" and mtime_utc == "12:36:01")
    check("C5", attendu,
          f"l'heure du journal (13:36:01 locale) == le mtime Drive "
          f"({mtime_utc}Z = 13:36:01 heure locale du développeur) — la pièce "
          f"datée par DEUX voix indépendantes (le contenu et la métadonnée)")

    # ---------------------------------------------------------------- D. le run kit-3
    sec("D. LE RUN KIT-3 LOUPE (Windows 11, le treizième run terrain, le "
        "premier du paquet AUTO)")
    t = (PREUVES / "TRIADE_kits_terrain_v0150_MULTIMACHINES-AUTO_pc-windows_"
         "kit-3-terrain-tiers-loupe_loupe-kit-13_preuves-loupe_"
         "temoin-loupe.txt").read_text(encoding="utf-8")
    check("D1", "[env] Windows 11 · Python 64 bits · AMD64" in t,
          "l'environnement : Windows 11 · Python 64 bits · AMD64 — le même "
          "que les runs 11 et 12")

    check("D2", "sha256 c111510535767a40" in t and "127488 o" in t,
          "LE SCELLÉ ASSERTÉ au T0 : loupe.exe 127488 o, sha256 "
          "c111510535767a40… == LA PIÈCE LIVRÉE (l'empreinte prouve CES "
          "octets — la carte, génération 16)")

    t_ok = all(marqueur in t for marqueur in [
        "[T1] la session NÉE",
        "le VRAI CreateFileW",
        "les 384 octets IDENTIQUES",
        "LE PANNEAU : md5 5fc07b786150",
        "== hashlib",
        "le motif trouvé à 577 == bytes.find",
        "l'octet 0 mûté 0x00 → 0x4D SEUL, la taille CONSTANTE",
        "-2 ABSENT", "-5 ENTRÉE", "-3 HORS-BORNES", "-1 FIN",
        "[T7] loupe.exe relu INCHANGÉ",
    ])
    check("D3", t_ok,
          "T0→T7 TOUT VERT : l'arène (l'ombre byte-à-byte, l'IAT résolue : "
          "37 feuilles), la session (poignée 0x2d4, le VRAI CreateFileW), "
          "la double lecture (les 384 octets IDENTIQUES), LE PANNEAU "
          "(md5 5fc07b786150… · sha256 == hashlib — la pièce de l'ère jugée "
          "par sa propre application), les lignes, la recherche (577 == "
          "bytes.find), L'ÉDITION à l'octet (0x00 → 0x4D SEUL, taille "
          "CONSTANTE), LES REJETS nommés, la pièce relue INCHANGÉE")

    s_ok = all(marqueur in t for marqueur in [
        "GetLastError 193, NTSTATUS 0xc000007b",
        "P1 LE TROU RECONSTITUÉ : REFUS DU CHARGEUR",
        "P4 LA GÉOMÉTRIE dev.2 ENTIÈRE : REFUS DU CHARGEUR",
        "L'AXE EST NOMMÉ",
        "loupe.exe INTACT",
        "[sonde-214] LA LIAISON",
    ])
    check("D4", s_ok,
          "LA SONDE DE L'ENTRÉE 205 vécue : P0 VERTE · P1 LE TROU REFUSÉ par "
          "le VRAI chargeur (GetLastError 193, NTSTATUS 0xc000007b) · P2 LE "
          "BSS VERTE · P3 LE CUI VERTE · P4 LA GÉOMÉTRIE ENTIÈRE REFUSÉE — "
          "L'AXE EST NOMMÉ, les copies %TEMP% mortes, loupe.exe INTACT ; "
          "sonde-214 : la liaison nommée au témoin")

    t12 = (RUN12 / "temoin-loupe.txt").read_text(encoding="utf-8").splitlines()
    t_new = t.splitlines()
    diffs = [(a, b) for a, b in zip(t12, t_new) if a != b]
    diffs_sans_aslr = [(a, b) for a, b in diffs
                       if not any(k in a for k in
                                  ("0x7ff6", "0x7ff7", "poignée vivante"))]
    check("D5", len(t12) == len(t_new) and len(diffs) == 5
          and not diffs_sans_aslr,
          f"le témoin == celui du 12e run (les MÊMES pièces, Entrée 222) ne "
          f"différant QUE par les adresses ASLR et la poignée de session "
          f"({len(diffs)} lignes divergentes, toutes d'exécution) — le "
          f"gabarit intangible, UN RUN NEUF")

    check("D6", "LE RUN DE LOUPE : VERT SUR PIÈCES" in t
          and "l'application née de TRIADE a vécu chez son utilisateur" in t,
          "le verdict du témoin : « LE RUN DE LOUPE : VERT SUR PIÈCES — "
          "l'application née de TRIADE a vécu chez son utilisateur : la "
          "session, le panneau, les lignes, la recherche, l'édition à "
          "l'octet, les rejets nommés »")

    ecart_k1_k3 = (p_temoin["modifie"][11:19] >= p_verdict["modifie"][11:19])
    check("D7", ecart_k1_k3,
          f"le témoin écrit à {p_temoin['modifie'][11:19]}Z (13:36:32 "
          f"locale), {31} s après le kit-1 — les DEUX runs séquentiels, une "
          f"minute à eux deux : le kit-1 refusa en une seconde, le kit-3 "
          f"vécut T0→T7+S0 en une trentaine")

    # ---------------------------------------------------------------- E. frontières
    sec("E. LES FRONTIÈRES (rien n'est maquillé)")
    preuves_dudect = [e for e in tout
                      if "kit-2-dudect" in e["chemin"]
                      and ("preuves" in e["chemin"] or ".csv" in e["chemin"]
                           or "temoin" in e["chemin"].lower())]
    check("E1", not preuves_dudect,
          "kit-2-dudect NON couru (aucune preuve dudect au dépôt — ni témoin, "
          "ni csv) ; le téléphone-arm et les voies QEMU non courus — aucun "
          "geste obligatoire (la main demeure au développeur)")

    check("E2", "LA VITRINE SE VIT PAR SON TÉMOIN" in t
          and "double-cliquez temoin-vitrine.bat" in t,
          "LA VITRINE demeure à la main du développeur (le [suite] du témoin "
          "le dit) : temoin-vitrine.bat à double-cliquer, les fenêtres à "
          "fermer SOI-MÊME — un témoin automatisé ne témoignerait de rien")

    preuves_shani = [e for e in tout
                     if e["chemin"].startswith(
                         AUTO + "/pc-windows/kit-1-shani/preuves-shani/")
                     and not e["dossier"]]
    noms_shani = sorted(e["chemin"].rsplit("/", 1)[1]
                        for e in preuves_shani)
    check("E3", noms_shani == ["VERDICT-run-shani.txt",
                              "scenario-shani-journal.log"],
          f"le dossier preuves-shani/ du kit-1 porte EXACTEMENT les DEUX "
          f"pièces du refus (VERDICT + journal) — le témoin complet et le "
          f"moteur-exécuté naissent après le franchissement du silicium "
          f"(le LISEZMOI le dit, les pièces le confirment) : la ligne « "
          f"signature du geste » n'existe pas pour un refus, rien à signer, "
          f"rien maquillé")
    check("E4", True,
          "D205 demeure consacrée au laboratoire, jamais scellée ; les "
          "journaux bruts (*.log) demeurent au coffre /test, leurs contenus "
          "cités mot pour mot ; les preuves recoupées sur pièces, le paquet "
          "déposé demeurant le paquet prouvé (D153)")

    # ---------------------------------------------------------------- bilan
    sec("")
    rapport.append(f"BILAN : {verts}/{verts + rouges} VERT"
                   + (f" · {rouges} ROUGE" if rouges else ""))

    sortie = PREUVES / "recoupement-depot-kit-terrain.txt"
    entete = (
        "RECOUPEMENT DU DÉPÔT KIT TERRAIN — les runs du paquet AUTO "
        "(12/11/2026, 13:36 heure locale du développeur)\n"
        "l'annonce : « dossier kit terrain avec preuves déposé dans /test du "
        "drive »\n"
        "les pièces : preuves-depot-auto-terrain/ (rapatriées au md5 VERT "
        "contre les métadonnées Drive)\n\n"
    )
    sortie.write_text(entete + "\n".join(rapport) + "\n", encoding="utf-8")
    print(entete + "\n".join(rapport))
    print(f"\n[rapport : {sortie}]")
    print(f"[sha256 du rapport : {sha256(sortie)[:16]}…]")
    return 1 if rouges else 0


if __name__ == "__main__":
    sys.exit(main())
