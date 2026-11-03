#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_e2.py — LE KIT VM ETAPE 2 (le flux navigateur, D136) :
assemblage PAR SCRIPT sur la base du kit v8 LIVRÉ (le coffre fait foi),
modèle assembler_kit_v7.py (Task 43).

DEUX pièces remplacées, une seule idée :
  1. kit-m5b/proxy.exe        0.5.1 fb41697d…  ->  0.6.0-rc.1 4b8f6af6…
     (scellé carte génération 7, 04/11 — les révisions R3 de D136) ;
  2. kit-m5b/scenario-m5b.ps1 v8 (client CLI)  ->  e2 (NAVIGATEUR Edge
     headless par le mandataire, armement constaté, lignes de flux) ;
  3. LISEZMOI-KIT-M5B.md      v8               ->  e2 ;
  4. preuves-m5b/LISEZMOI-preuves.txt          ->  liste des pièces e2.

TOUT LE RESTE EST REPRIS TEL QUEL de la vague v8 (autorité + fixtures v5,
python embarqué, client-m5b.ps1 vestige, scenario-m5b.wsb) — chaque reprise
ASSERTÉE par empreinte (fixtures racine 86525998…, autorite_test.py, wsb).
Le zip naît avec m5b-kit/ à sa racine (structure v8 exacte) ; intégrité du
zip re-vérifiée à la sortie (lecture différé, proxy relu == attendu).

Usage : python3 scripts/assembler_kit_e2.py <kit-v8.zip> <sortie.zip>
Code de sortie : 0 = kit assemblé et vérifié ; 2 = refus nommé."""

import hashlib
import sys
import zipfile

REPO = "/home/z/my-project/triade-repo"
PROXY_RC1 = REPO + "/m5/proxy.exe"
SCENARIO_E2 = REPO + "/m5/vm/scenario-m5b-e2.ps1"
LISEZMOI_KIT_E2 = "/home/z/my-project/download/vague-v8/LISEZMOI-KIT-M5B-e2.md"

PROXY_ATTENDU = {
    "sha256": "4b8f6af6caedb3e17811e6e25da1f1680068866bd1b417154fc54474170ec236",
    "md5": "72cf8fdd803a0c9691145892800c31e5",
    "taille": 36352,
    "ancien_sha256": "fb41697ddde265ac659bdceecc2ab3ec55f564d0998d43059090235762edf3f3",
}
FIXTURES_INCHANGEES = {
    "kit-m5b/autorite/fixtures/racine-autorite.pem": "86525998a9a464520ffd95ebf6d5978b",
    "kit-m5b/autorite/fixtures/serv-valide.pem": "9e8643f0c42a10aae6e28a7a10bc8684",
    "kit-m5b/autorite/fixtures/serv-autonome.pem": "cf7122354c4d2a2e7e4845b78df7d3c7",
    "kit-m5b/autorite/fixtures/serv-valide.key": "7583feaab8c6107e50adf11f7b4e7b94",
    "kit-m5b/autorite/fixtures/serv-autonome.key": "f07f0191c446ba75410f265c7f3e6a70",
    "kit-m5b/autorite/autorite_test.py": "6a523bbf4a611405326a034c7c3d0f1e",
    "kit-m5b/client-m5b.ps1": "1c8031f241cf2fc0b9a385b67e218bc2",
    "scenario-m5b.wsb": "a04e2ed528cf5bf5f451abfaa5b0601e",
    "kit-m5b/python/python.exe": "0cfdf7db1b81d067d3dad75f6abb312b",
}
LISEZMOI_PREUVES_E2 = (
    "Ce dossier recevra les preuves du run M5-b ETAPE 2 (le flux navigateur).\r\n"
    "Apres le run, y vivre : temoin-m5b.txt, scenario-m5b-journal.log,\r\n"
    "proxy-journal.log, dom-a.txt, dom-b.txt, nav-a.png, nav-b.png,\r\n"
    "nav-a-err.txt, nav-b-err.txt, nav-a-cap-err.txt, nav-b-cap-err.txt,\r\n"
    "autorite-a.log, autorite-b.log (+ les -console/-err de l'autorite),\r\n"
    "hosts-lu.txt, matrice curl (curl-*.txt, page-d*.txt, autorite-d/e*),\r\n"
    "dnscache.txt, ipconfig-vm.txt, parefeu-vm.txt.\r\n"
    "Le dossier DOIT exister avant le double-clic (mapping du .wsb).\r\n"
)


def md5(b):
    return hashlib.md5(b).hexdigest()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def refus(nom, detail):
    print(f"[assembleur] REFUS {nom} : {detail}")
    sys.exit(2)


def main():
    if len(sys.argv) != 3:
        refus("USAGE", "python3 scripts/assembler_kit_e2.py <kit-v8.zip> <sortie.zip>")
    kit_v8, sortie = sys.argv[1], sys.argv[2]

    # -- 0. les sources du dépôt, assertées AVANT tout geste -------------------
    proxy = open(PROXY_RC1, "rb").read()
    if sha256(proxy) != PROXY_ATTENDU["sha256"] or len(proxy) != PROXY_ATTENDU["taille"]:
        refus("PROXY-RC1", f"m5/proxy.exe diverge (sha256 {sha256(proxy)[:16]}…, "
                           f"{len(proxy)} o — attendu 4b8f6af6…, 36 352 o)")
    if md5(proxy) != PROXY_ATTENDU["md5"]:
        refus("PROXY-RC1", "md5 diverge (attendu 72cf8fdd…)")
    scenario = open(SCENARIO_E2, "rb").read()
    if not scenario.startswith(b"\xef\xbb\xbf"):
        refus("SCENARIO-E2", "BOM UTF-8 absent (PowerShell 5.1 lirait en ANSI — v2)")
    if b"--relever-https" not in scenario or b"NAVIGATEUR-ABSENT" not in scenario:
        refus("SCENARIO-E2", "le scénario e2 ne porte pas ses marqueurs (armement/navigateur)")
    if b"\r\n" not in scenario:
        refus("SCENARIO-E2", "CRLF absent")
    lisezMoi = open(LISEZMOI_KIT_E2, "rb").read()
    if b"e2 laboratoire" not in lisezMoi or b"4b8f6af6" not in lisezMoi:
        refus("LISEZMOI-KIT", "le LISEZMOI-KIT e2 ne porte pas ses marqueurs")

    # -- 1. la base v8, lue et vérifiée ----------------------------------------
    try:
        base = zipfile.ZipFile(kit_v8)
    except Exception as e:
        refus("KIT-V8-ILLISIBLE", str(e))
    noms = base.namelist()
    if len(noms) != 55:
        refus("KIT-V8", f"{len(noms)} entrées (55 attendues — la base v8 a changé)")
    for requis in ("m5b-kit/kit-m5b/proxy.exe", "m5b-kit/kit-m5b/scenario-m5b.ps1",
                   "m5b-kit/kit-m5b/scenario-m5b.wsb" if "m5b-kit/kit-m5b/scenario-m5b.wsb" in noms
                   else "m5b-kit/scenario-m5b.wsb",
                   "m5b-kit/LISEZMOI-KIT-M5B.md"):
        if requis not in noms:
            refus("KIT-V8", f"entrée manquante : {requis}")
    # la base est bien le 0.5.1 (le remplacement est un FAIT, pas une hypothèse)
    vieux_proxy = base.read("m5b-kit/kit-m5b/proxy.exe")
    if sha256(vieux_proxy) != PROXY_ATTENDU["ancien_sha256"]:
        refus("KIT-V8", "le proxy de la base n'est pas le 0.5.1 fb41697d…")
    # les reprises INCHANGÉES, assertées
    for nom, attendu in FIXTURES_INCHANGEES.items():
        if md5(base.read("m5b-kit/" + nom)) != attendu:
            refus("REPRISE-DIVERGENTE", f"{nom} diverge de la vague v8 (md5 attendu {attendu})")
    wsb = base.read("m5b-kit/scenario-m5b.wsb")
    if b"<Networking>Disable</Networking>" not in wsb:
        refus("WSB", "le .wsb de la base ne coupe pas le réseau")

    # -- 2. l'assemblage (tout en mémoire, écriture unique) --------------------
    remplacés = {
        "m5b-kit/kit-m5b/proxy.exe": proxy,
        "m5b-kit/kit-m5b/scenario-m5b.ps1": scenario,
        "m5b-kit/LISEZMOI-KIT-M5B.md": lisezMoi,
        "m5b-kit/preuves-m5b/LISEZMOI-preuves.txt": LISEZMOI_PREUVES_E2.encode("utf-8"),
    }
    with zipfile.ZipFile(sortie, "w", zipfile.ZIP_DEFLATED) as z:
        for info in base.infolist():
            data = remplacés.get(info.filename, base.read(info.filename))
            z.writestr(info.filename, data)

    # -- 3. la vérification du zip né (lecture différée) ------------------------
    verif = zipfile.ZipFile(sortie)
    if verif.testzip() is not None:
        refus("ZIP-INTEGRITE", "testzip nomme une entrée corrompue")
    if len(verif.namelist()) != 55:
        refus("ZIP-INTEGRITE", f"{len(verif.namelist())} entrées (55 attendues)")
    relu = verif.read("m5b-kit/kit-m5b/proxy.exe")
    if sha256(relu) != PROXY_ATTENDU["sha256"]:
        refus("ZIP-INTEGRITE", "le proxy relu du zip diverge du 0.6.0-rc.1")
    if verif.read("m5b-kit/kit-m5b/scenario-m5b.ps1") != scenario:
        refus("ZIP-INTEGRITE", "le scénario relu du zip diverge du e2")
    for nom, attendu in FIXTURES_INCHANGEES.items():
        if md5(verif.read("m5b-kit/" + nom)) != attendu:
            refus("ZIP-INTEGRITE", f"{nom} relu diverge")
    verif.close()
    base.close()

    taille = open(sortie, "rb").read().__len__()
    print(f"[assembleur] kit e2 ASSEMBLÉ : {sortie}")
    print(f"[assembleur] {len(remplacés)} pièces remplacées, 51 reprises de la vague v8, "
          f"55 entrées, intégrité re-vérifiée (proxy relu == 4b8f6af6…)")
    print(f"[assembleur] taille {taille} o — md5 {md5(open(sortie, 'rb').read())}")
    print(f"[assembleur] marqueurs e2 : "
          f"--relever-https={'OK' if b'--relever-https' in scenario else 'KO'}, "
          f"NAVIGATEUR={'OK' if b'NAVIGATEUR' in scenario else 'KO'}, "
          f"flux v=0/v=3={'OK' if (b'v=0' in scenario and b'v=3' in scenario) else 'KO'}")


if __name__ == "__main__":
    main()
