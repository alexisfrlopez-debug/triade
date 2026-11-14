#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE — LE MONTAGE DU KIT v2 DE L'UNITÉ 1 × BRAS C (la réparation du
refus du 14/11) : la pièce, le source, le lanceur et les témoins INTACTS
octet pour octet (recoupés à la gravure v1), le scénario RÉPARÉ, la gravure
REGRAVÉE du montage même, le LISEZMOI de l'écart et de la reprise, le zip."""
import hashlib
import pathlib
import shutil
import zipfile

V1 = pathlib.Path("/home/z/my-project/download/nouveau-run/"
                  "kit-unite-loupe-01-C-20261114")
V2_SCENARIO = pathlib.Path("/home/z/my-project/work/kit_v2/scenario-unite01C.py")
BAC = pathlib.Path("/home/z/my-project/download/kit_unite_loupe_01_C_v2")
KIT = BAC / "kit-unite-loupe-01-C-20261114-v2"

if BAC.exists():
    shutil.rmtree(BAC)
KIT.mkdir(parents=True)

def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

# ---- 1. les pièces INTACTES (recoupées à la gravure v1 avant la copie) -------
INTACTES = {
    "loupe-01-c.dll": "85b34ed4c243e977",
    "loupe-01-c.c": "860ff1cfcf78d5fc",
    "loupe-01-c.def": "c0c9b9f40f4fe5e7",
    "LANCEUR-UNITE-01-C.bat": "29bdae2ff65a6326",
    "temoin-1.bin": "df7e70e5021544f4",
    "temoin-384.bin": "3396717b98b4859b",
    "temoin-3f.bin": "c5fc1f28e471059d",
    "vide.bin": "e3b0c44298fc1c14",
}
for nom, prefixe in INTACTES.items():
    obtenu = sha(V1 / nom)
    assert obtenu.startswith(prefixe), f"{nom} a divergé : {obtenu}"
    shutil.copy2(V1 / nom, KIT / nom)
    print(f"[INTACT] {nom} — {obtenu[:16]}…")

# ---- 2. le scénario RÉPARÉ ------------------------------------------------------
assert sha(V2_SCENARIO).startswith("6340cd3c6308c3ae")
shutil.copy2(V2_SCENARIO, KIT / "scenario-unite01C.py")
print(f"[NEUF  ] scenario-unite01C.py — {sha(KIT / 'scenario-unite01C.py')[:16]}…")

# ---- 3. le LISEZMOI v2 ----------------------------------------------------------
LISEZMOI = """LISEZMOI — LE KIT DE L'UNITÉ 1 : LOUPE-01 OUVRIR × BRAS C — v2
(LA RÉPARATION DU REFUS DU 14/11 ; la campagne de comparaison des workflows
D204 ; le kit v1 DEMEURE au coffre, D143 — la pièce n'est jamais jetée ; le
GUI vous attend à l'onglet 1·KIT de l'unité loupe-01 × C)
========================================================================

L'OBJET : LA MÊME première unité du bras C (le flux standard, C + gcc), le
même contrat de couche I que le bras T (loupe-01 OUVRIR, révision 3), LA
MÊME PIÈCE — loupe-01-c.dll sha256 85b34ed4… — OCTET POUR OCTET celle du
kit v1 : au terrain du 14/11, T0 fut VERT (la pièce recoupée à la gravure),
l'image cartographiée, les QUATRE exports découverts. La pièce est SAINE.

LE REFUS DU v1 — LA FAUTE AU LABO, NOMMÉE (jamais maquillée) : le run
s'arrêta à la traversée de la table d'imports DU SCÉNARIO — « access
violation reading 0x00007FFA23900094 », code 1, AUCUN vecteur, AUCUN
témoin. LA CAUSE, établie au labo OCTET PAR OCTET : la boucle testait le
terminateur à la CHAÎNE du nom (« si le nom est vide, arrête ») — mais au
descripteur NUL, le champ Name vaut l'RVA 0, et lire_chaine(base, 0) lit
L'EN-TÊTE DOS « MZ » : jamais vide, la boucle ne s'y arrêtait pas — elle
dérivait à travers la table hint/nom de la pièce (25 itérations : « MZ »,
« InitializeCriticalSection », « VirtualProtect », « _initterm »…) jusqu'à
dereférer l'RVA bogué 0x6c430094 hors image : base 0x7ff9b74d0000 +
0x6c430094 = 0x7ffa23900094 — L'ADRESSE EXACTE DE VOTRE CONSOLE,
reproduite au labo. L'ÉPREUVE QUI MANQUA, nommée aussi : le test de
découverte du labo éprouvait SA PROPRE copie de la traversée (juste, elle,
testait le champ) — jamais la boucle du scénario livré ; la leçon
consignée : l'épreuve doit exécuter LE CODE LIVRÉ, pas sa copie.

LA RÉPARATION (minimale — 20 lignes ajoutées, 2 retirées ; la pièce, le
source C, le lanceur et les témoins INTACTS octet pour octet) : le
terminateur se lit au CHAMP Name (l'RVA NUL, AVANT toute lecture de
chaîne) ; gardes fail-closed : au plus 64 descripteurs, aucun champ Name
hors image — REFUS NOMMÉ « la pièce a divergé, rien ne court », jamais un
plantage.

LES ÉPREUVES DU LABO (D122 — le labo n'a aucun Windows, la logique
rejouée au POSIX) :
  — LA FAUTE REJOUÉE contre les octets réels de la pièce : les 25
    itérations de la dérive reproduites, l'adresse du plantage EXACTE ;
  — LA TRAVERSÉE DU SCÉNARIO v2 EXÉCUTÉE cette fois : le texte même du
    kit (les quatre lecteurs + la boucle gardée, extraits VERBATIM du
    fichier livré) couru contre l'image de la pièce mappée par sections :
    arrêt AU descripteur NUL (les deux descripteurs réels traversés :
    KERNEL32.dll, msvcrt.dll), les CINQ feuilles résolues, aucune garde
    vécue, RIEN lu hors image ;
  — LE CONTRAT ENTIER REJOUÉ : 17 VERT 0 ROUGE (les quatre témoins champ
    à champ contre l'oracle hashlib, les rejets d'OS, la borne 2 Gio, la
    session double, le chemin trop long — le juge indépendant) ;
  — py_compile + l'audit AST du scénario v2 (la boucle gardée, sa clause
    else, le champ avant la chaîne).

LE GESTE (tout au clic, l'ordre de jeu d'une unité — INCHANGÉ) :
  1. AU GUI (TRIADE_gui_tous_runs_v1), onglet 1·KIT de l'unité
     loupe-01 × C : CHOISIR CE DOSSIER v2 — le GUI recoupe les EMPREINTES
     gravées (une divergence, rien ne court) ;
  2. onglet 2·RUN : LANCER LANCEUR-UNITE-01-C.bat (le lanceur officiel —
     il court dans SA PROPRE console, INTACT) : le scénario recoupe la
     pièce à la gravure, charge l'image (LoadLibraryEx DONT_RESOLVE),
     découvre les adresses PAR LA TABLE D'EXPORTS, résout les feuilles
     kernel32 AUX SLOTS RÉELS (la traversée RÉPARÉE), appelle
     loupe_01_ouvrir aux témoins du kit, juge par le modèle indépendant
     (hashlib), et écrit le témoin ; le dossier preuves-unite01C/ naît ;
  3. onglet 3·TÉMOIN : ouvrir preuves-unite01C\\temoin-unite01C.txt au
     bloc-notes, le DATER, le SIGNER DE VOTRE MAIN — jamais automatisé
     (D99) — puis renvoyer le dossier ENTIER au coffre /test (la console
     du refus v1, run-console-unite01C.txt, y joindre : la pièce d'un
     refus n'est jamais jetée) ;
  4. aux onglets 4-7 : la ligne de carnet AU GESTE (M3), la livraison
     (M1 — la cap tenue par le GUI : au plus TROIS par bloc, l'arrêt au
     premier vert), les défauts nommés s'il y en a, le chrono (M4) ;
  5. le labo recoupe le run revenu — PUIS l'unité suivante commence.

LES PIÈCES DU KIT (les INTACTES portent l'empreinte du v1 — octet pour
octet ; le scénario, la gravure et le LISEZMOI sont les pièces neuves) :
  loupe-01-c.dll        la pièce (INTACTE — 85b34ed4…) ;
  loupe-01-c.c/.def     le source et la définition des exports (INTACTS) ;
  scenario-unite01C.py  le scénario RÉPARÉ (v2 — le terminateur au champ
                        Name, les gardes fail-closed) ;
  LANCEUR-UNITE-01-C.bat le lanceur officiel (INTACT — le double-clic) ;
  temoin-1.bin, temoin-384.bin, temoin-3f.bin, vide.bin
                        les témoins du kit (INTACTS — les MÊMES octets que
                        le kit T, la génération fixe du labo) ;
  EMPREINTES-KIT-UNITE-01-C.txt la gravure REGRAVÉE du montage v2 ;
  le présent LISEZMOI.

LES ÉCARTS NOMMÉS (consignés, jamais maquillés — ceux du v1 demeurent) :
  — SetFilePointerEx : la pièce ne l'importe pas (sa lecture est
    séquentielle depuis l'ouverture) : l'ÉCART NOMMÉ, le scénario résout
    les feuilles que la pièce déclare, les cinq suffisent ;
  — les imports du CRT de lancement mingw (InitializeCriticalSection…)
    vivent à la table sans jamais être appelées : sous DONT_RESOLVE aucun
    point d'entrée ne court — l'audit de la clôture le prouve ;
  — l'accès refusé (E3) ne s'arme pas proprement au terrain : NOMMÉ
    ABSENT, le vecteur ne compte pas ;
  — le chemin de 260 caractères sans NUL : au terrain, le SYSTÈME refuse
    lui-même le chemin trop long — le verdict exact est CONSIGNÉ TEL QUEL
    au témoin ;
  — l'écho du lanceur rend « preuves-unite01C<TAB>emoin… » : le « \\t »
    du chemin rendu TAB par la console — COSMÉTIQUE, nommé, le témoin
    vit bien à preuves-unite01C\\temoin-unite01C.txt.

LA FRONTIÈRE : le run est À VOUS (CA6 — le labo ne court JAMAIS le
terrain) ; le témoin se signe de VOTRE MAIN (D99) ; le renvoi du dossier
ENTIER vous appartient ; la pièce ne bouge pas (l'empreinte gravée — une
divergence, rien ne court).

*La consignation vit au journal de travail (l'Entrée 286) ; le détail du
plan à PLAN_PREREGISTRE_COMPARAISON.md (a78caf8c…, VERROUILLÉ).*
"""
(KIT / "LISEZMOI-KIT-UNITE-01-C.txt").write_text(LISEZMOI, encoding="utf-8",
                                                 newline="\n")
print(f"[NEUF  ] LISEZMOI-KIT-UNITE-01-C.txt — "
      f"{sha(KIT / 'LISEZMOI-KIT-UNITE-01-C.txt')[:16]}… "
      f"({len(LISEZMOI)} o)")

# ---- 4. la gravure REGRAVÉE (générée du montage même) ----------------------------
ORDRE = ["loupe-01-c.dll", "loupe-01-c.c", "loupe-01-c.def",
         "scenario-unite01C.py", "LANCEUR-UNITE-01-C.bat", "temoin-1.bin",
         "temoin-384.bin", "temoin-3f.bin", "vide.bin",
         "LISEZMOI-KIT-UNITE-01-C.txt"]
lignes = ["EMPREINTES — LE KIT DE L'UNITÉ 1 × BRAS C, v2 (loupe-01, la "
          "campagne D204 — LA RÉPARATION DU REFUS DU 14/11)",
          "(chaque pièce sha256, générée du montage même — le GUI recoupe "
          "à l'onglet 1·KIT ; une divergence, rien ne court)", ""]
for nom in ORDRE:
    lignes.append(f"{sha(KIT / nom)}  {nom}")
(KIT / "EMPREINTES-KIT-UNITE-01-C.txt").write_text(
    "\n".join(lignes) + "\n", encoding="utf-8", newline="\n")
print(f"[NEUF  ] EMPREINTES-KIT-UNITE-01-C.txt regravée — "
      f"{sha(KIT / 'EMPREINTES-KIT-UNITE-01-C.txt')[:16]}…")

# ---- 5. le zip (le miroir du v1 : le dossier au sommet) ---------------------------
ZIP = BAC / "kit-unite-loupe-01-C-20261114-v2.zip"
with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
    for nom in ORDRE + ["EMPREINTES-KIT-UNITE-01-C.txt"]:
        z.write(KIT / nom, f"kit-unite-loupe-01-C-20261114-v2/{nom}")
print(f"[NEUF  ] {ZIP.name} — {ZIP.stat().st_size} o, "
      f"sha256 {sha(ZIP)[:16]}…")

# ---- 6. le contrôle final : 12 pièces, les intactes == la gravure v1 --------------
GRAVURE_V1 = {}
for l in (V1 / "EMPREINTES-KIT-UNITE-01-C.txt").read_text(
        encoding="utf-8").splitlines():
    p = l.split()
    if len(p) == 2 and len(p[0]) == 64:
        GRAVURE_V1[p[1]] = p[0]
ok = True
for nom, attendu_v1 in GRAVURE_V1.items():
    if nom == "LISEZMOI-KIT-UNITE-01-C.txt" or nom == "scenario-unite01C.py":
        continue
    identique = sha(KIT / nom) == attendu_v1
    ok &= identique
    print(f"[{'VERT' if identique else 'ROUGE'}] {nom} "
          f"{'== la gravure v1' if identique else 'A DIVERGÉ !'}")
print("\n" + (f"LE KIT v2 EST MONTÉ — 12 pièces à {KIT}"
              if ok and len(list(KIT.iterdir())) == 11 else "ÉCHEC AU MONTAGE"))
