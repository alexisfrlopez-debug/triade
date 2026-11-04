#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""assembler_kit_e4.py — LE KIT VM ETAPE 2 CORRIGÉ (proxy rc.2, Entrée 141 /
D146/D147) : assemblage PAR SCRIPT sur la base du kit e3 LIVRÉ (le coffre
fait foi), modèle assembler_kit_e3.py (Task 57).

TROIS pièces remplacées, une seule idée (le chemin de réparation de
l'Entrée 141, appliqué) :
  1. kit-m5b/proxy.exe           0.6.0-rc.1 (le scellé FAUTIF du run e3,
     mort à la première requête routée)  ->  0.6.0-rc.2 (l'idiome hérité
     http-02:R1 « dword + base d'image » RESTAURÉ dans la ligne de flux —
     contrôle D146 VERT à la base réelle) ;
  2. m5b-kit/LISEZMOI-KIT-M5B.md e3  ->  e4 (le proxy documenté) ;
  3. m5b-kit/preuves-m5b/LISEZMOI-preuves.txt  liste e3  ->  e4
     (les MÊMES pièces — le scénario est repris tel quel).

LE SCÉNARIO N'EST PAS REMPLACÉ : celui de la vague e3 est repris TEL QUEL
(byte-identique — le run e3 s'est arrêté au crash du proxy AVANT le
navigateur, le scénario n'a rien à se reprocher). L'assembleur l'ASSERT
des deux côtés : la base embarque l'e3 du dépôt, le dépôt porte sa copie
e4 identique. TOUT LE RESTE EST REPRIS TEL QUEL de la vague e3 (autorité
+ fixtures v5, python embarqué, client-m5b.ps1 vestige, scenario-m5b.wsb)
— chaque reprise ASSERTÉE par empreinte. Le zip naît avec m5b-kit/ à sa
racine (structure v8/e2/e3 exacte) ; intégrité re-vérifiée à la sortie
(lecture différée : proxy relu == rc.2 attendu, scénario relu == e3 du
dépôt).

Usage : python3 scripts/assembler_kit_e4.py <kit-e3.zip> <sortie.zip>
Code de sortie : 0 = kit assemblé et vérifié ; 2 = refus nommé."""

import hashlib
import sys
import zipfile

REPO = "/home/z/my-project/triade"
PROXY_RC2 = REPO + "/m5/proxy.exe"
SCENARIO_E3 = REPO + "/m5/vm/scenario-m5b-e3.ps1"
SCENARIO_E4 = REPO + "/m5/vm/scenario-m5b-e4.ps1"
LISEZMOI_KIT_E4 = "/home/z/my-project/download/vague-e4/LISEZMOI-KIT-M5B-e4.md"

PROXY_RC2_ATTENDU = {
    "sha256": "c1e46fb0b857b6f33c67aa7f26a1db3064f2e3adbd528414116b497220b6a20c",
    "md5": "48be81e0588351f72a0ce417d25b4553",
    "taille": 36352,
}
PROXY_RC1_BASE = {   # la base e3 embarque le rc.1 FAUTIF — le remplacement
    "sha256": "4b8f6af6caedb3e17811e6e25da1f1680068866bd1b417154fc54474170ec236",
    "md5": "72cf8fdd803a0c9691145892800c31e5",
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
LISEZMOI_PREUVES_E4 = (
    "Ce dossier recevra les preuves du run M5-b ETAPE 2 (le flux navigateur).\r\n"
    "Apres le run, y vivre : temoin-m5b.txt, scenario-m5b-journal.log,\r\n"
    "proxy-journal.log, page-sonde-armement.txt (la sonde d'armement),\r\n"
    "edge-version.txt (version du navigateur par VersionInfo),\r\n"
    "dom-a.txt, dom-b.txt, nav-a.png, nav-b.png,\r\n"
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
        refus("USAGE", "python3 scripts/assembler_kit_e4.py <kit-e3.zip> <sortie.zip>")
    kit_e3, sortie = sys.argv[1], sys.argv[2]

    # -- 0. les sources du dépôt, assertées AVANT tout geste -------------------
    proxy = open(PROXY_RC2, "rb").read()
    if sha256(proxy) != PROXY_RC2_ATTENDU["sha256"] or len(proxy) != PROXY_RC2_ATTENDU["taille"]:
        refus("PROXY-RC2", f"m5/proxy.exe diverge (sha256 {sha256(proxy)[:16]}…, "
                           f"{len(proxy)} o — attendu c1e46fb0…, 36 352 o)")
    if md5(proxy) != PROXY_RC2_ATTENDU["md5"]:
        refus("PROXY-RC2", "md5 diverge (attendu 48be81e0…)")
    scenario_e3 = open(SCENARIO_E3, "rb").read()
    scenario_e4 = open(SCENARIO_E4, "rb").read()
    if scenario_e3 != scenario_e4:
        refus("SCENARIO", "le scénario e4 n'est PAS la copie byte-identique "
                          "de l'e3 (la vague e4 reprend le scénario e3 TEL QUEL)")
    for marqueur in (b"--relever-https", b"PROXY-PAS-ARME", b"Sonde-Armement",
                     b"page-sonde-armement.txt", b"VersionInfo", b"POST-MORTEM"):
        if marqueur not in scenario_e3:
            refus("SCENARIO-E3", f"le scénario e3 ne porte pas son marqueur : {marqueur.decode()}")
    for vestige in (b"Attendre-Ligne",):
        if scenario_e3.count(vestige) != 0:
            refus("SCENARIO-E3", f"vestige e2 vivant : {vestige.decode()}")
    lisezMoi = open(LISEZMOI_KIT_E4, "rb").read()
    if b"e4 laboratoire" not in lisezMoi or b"c1e46fb0" not in lisezMoi:
        refus("LISEZMOI-KIT", "le LISEZMOI-KIT e4 ne porte pas ses marqueurs")

    # -- 1. la base e3, lue et vérifiée ----------------------------------------
    try:
        base = zipfile.ZipFile(kit_e3)
    except Exception as e:
        refus("KIT-E3-ILLISIBLE", str(e))
    noms = base.namelist()
    if len(noms) != 55:
        refus("KIT-E3", f"{len(noms)} entrées (55 attendues — la base e3 a changé)")
    for requis in ("m5b-kit/kit-m5b/proxy.exe", "m5b-kit/kit-m5b/scenario-m5b.ps1",
                   "m5b-kit/scenario-m5b.wsb", "m5b-kit/LISEZMOI-KIT-M5B.md"):
        if requis not in noms:
            refus("KIT-E3", f"entrée manquante : {requis}")
    # la base embarque le 0.6.0-rc.1 FAUTIF — le remplacement est un FAIT nommé,
    # l'égalité avec le scellé fautif est ASSERTÉE, pas supposée
    proxy_base = base.read("m5b-kit/kit-m5b/proxy.exe")
    if sha256(proxy_base) != PROXY_RC1_BASE["sha256"]:
        refus("KIT-E3", "le proxy de la base n'est pas le 0.6.0-rc.1 fautif "
                        "(4b8f6af6…) — la base e3 a divergé")
    if md5(proxy_base) != PROXY_RC1_BASE["md5"]:
        refus("KIT-E3", "md5 du proxy de base diverge (attendu 72cf8fdd…)")
    # le scénario de la base est bien l'e3 (repris tel quel — l'identité est la règle)
    scenario_base = base.read("m5b-kit/kit-m5b/scenario-m5b.ps1")
    if scenario_base != scenario_e3:
        refus("KIT-E3", "le scénario de la base n'est pas l'e3 du dépôt "
                        "(la vague e4 le reprend TEL QUEL — identité exigée)")
    # les reprises INCHANGÉES, assertées
    for nom, attendu in FIXTURES_INCHANGEES.items():
        if md5(base.read("m5b-kit/" + nom)) != attendu:
            refus("REPRISE-DIVERGENTE", f"{nom} diverge de la vague e3/v8 (md5 attendu {attendu})")
    wsb = base.read("m5b-kit/scenario-m5b.wsb")
    if b"<Networking>Disable</Networking>" not in wsb:
        refus("WSB", "le .wsb de la base ne coupe pas le réseau")

    # -- 2. l'assemblage (tout en mémoire, écriture unique) --------------------
    remplacés = {
        "m5b-kit/kit-m5b/proxy.exe": proxy,                    # LE geste e4
        "m5b-kit/LISEZMOI-KIT-M5B.md": lisezMoi,
        "m5b-kit/preuves-m5b/LISEZMOI-preuves.txt": LISEZMOI_PREUVES_E4.encode("utf-8"),
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
    if relu != proxy:
        refus("ZIP-INTEGRITE", "le proxy relu du zip diverge du 0.6.0-rc.2 du dépôt")
    if sha256(relu) != PROXY_RC2_ATTENDU["sha256"]:
        refus("ZIP-INTEGRITE", "le proxy relu n'est pas le rc.2 (c1e46fb0…)")
    if verif.read("m5b-kit/kit-m5b/scenario-m5b.ps1") != scenario_e3:
        refus("ZIP-INTEGRITE", "le scénario relu du zip diverge de l'e3 du dépôt (repris tel quel)")
    if verif.read("m5b-kit/preuves-m5b/LISEZMOI-preuves.txt") != LISEZMOI_PREUVES_E4.encode("utf-8"):
        refus("ZIP-INTEGRITE", "le LISEZMOI-preuves relu diverge de la liste e4")
    for nom, attendu in FIXTURES_INCHANGEES.items():
        if md5(verif.read("m5b-kit/" + nom)) != attendu:
            refus("ZIP-INTEGRITE", f"{nom} relu diverge")
    verif.close()
    base.close()

    taille = open(sortie, "rb").read().__len__()
    print(f"[assembleur] kit e4 ASSEMBLÉ : {sortie}")
    print(f"[assembleur] {len(remplacés)} pièces remplacées (proxy rc.2 + 2 LISEZMOI), "
          f"52 reprises de la vague e3, 55 entrées, intégrité re-vérifiée")
    print(f"[assembleur] LE PROXY EST REMPLACÉ : relu == c1e46fb0… (0.6.0-rc.2 scellé, "
          f"carte génération 7 — l'idiome http-02:R1 restauré, D146/D147)")
    print(f"[assembleur] le scénario est l'e3 REPRIS TEL QUEL (byte-identique, "
          f"garde fonctionnelle D145 conservée)")
    print(f"[assembleur] taille {taille} o — md5 {md5(open(sortie, 'rb').read())}")


if __name__ == "__main__":
    main()
