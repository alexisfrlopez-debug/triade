#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LA RETOUCHE KIT dev.9 (Entrée 213) — la pièce demeure dev.7 (ACQUITTÉE).

L'huitième run a nommé DEUX défauts KIT (et aucun à la pièce) :
  [SONDE-PYTHON]   ctypes.SetLastError / ctypes.GetLastError N'EXISTENT PAS
                   dans le module ctypes — la sonde S0 mourut sur place,
                   ses sondes jamais jouées ;
  [LITTÉRAL-PÉRIMÉ] l'en-tête du témoin et le message PORTE-R10 disaient
                   « 0.1.0-dev.6 » alors que la pièce est dev.7 — la classe
                   de l'Entrée 209, ENCORE.

ET LE TÉMOIN VITRINE EST PORTANT : la vitrine est morte pour la CINQUIÈME
fois 0xC0000005 SANS rapport WER — le témoin actuel ne peut pas NOMMER.
Le dev.9 ajoute LE JOURNAL D'ÉVÉNEMENTS (wevtutil, Event ID 1000/1001) :
le module fautif et le décalage de l'exception seront CONSIGNÉS.
"""
import hashlib

SRC = "/home/z/my-project/triade/loupe/terrain/scenario-loupe.py"
BAT = "/home/z/my-project/triade/loupe/terrain/temoin-vitrine.bat"

# ---------------------------------------------------------------- LE SCÉNARIO
s = open(SRC, encoding="utf-8").read()
avant = hashlib.md5(s.encode()).hexdigest()

FIXES = [
    # 1. le commentaire de carte : la vérité de l'Entrée 211 (génération 13)
    ("# --- l'artefact : la carte génération 14 prouve CES octets "
     "-----------------------",
     "# --- l'artefact : l'empreinte ASSERTÉE prouve CES octets (la carte "
     "demeure\n#     en génération 13 — la régénération est dette au labo, "
     "l'Entrée 211) -----"),
    # 2. VERSION_TXT né de VERSION_R10 — le littéral ne dérivera PLUS jamais
    ('VERSION_R10 = 0x00010007          # loupe 0.1.0-dev.7 (le qword @0x2E80 —',
     'VERSION_R10 = 0x00010007          # loupe 0.1.0-dev.7 (le qword @0x2E80 —'),
]
# le fix 2 n'est qu'un repère : on insère VERSION_TXT juste après le bloc
repere_fin = None
for ligne in s.splitlines():
    if ligne.startswith("VERSION_R10"):
        repere_fin = ligne
FIXES = [f for f in FIXES if f[0] != f[1]]

for vieux, neuf in FIXES:
    assert vieux in s, f"introuvable : {vieux[:60]}…"
    s = s.replace(vieux, neuf, 1)

# VERSION_TXT inséré après la ligne VERSION_R10 (et sa continuation)
lignes = s.splitlines(keepends=True)
sortie, pose = [], False
for i, l in enumerate(lignes):
    sortie.append(l)
    if l.startswith("VERSION_R10"):
        # la définition s'étend sur ses lignes de commentaire suivantes :
        # on avance jusqu'à la première ligne vide ou non-commentaire
        j = i + 1
        while j < len(lignes) and (lignes[j].startswith("#")
                                   or lignes[j].strip() == ""):
            if lignes[j].strip() == "" and j > i + 1:
                break
            sortie.append(lignes[j])
            j += 1
        sortie.append("VERSION_TXT = f\"0.1.0-dev.{VERSION_R10 & 0xFFFF}\""
                      "   # dynamique — le littéral périmé chassé "
                      "(dev.9, l'Entrée 213)\n")
        sortie.append("\n")
        # le reste à partir de j
        sortie.extend(lignes[j:])
        pose = True
        break
s = "".join(sortie)
assert pose, "VERSION_TXT non inséré"

SUIVANTS = [
    # 3. la sonde S0 : le couple SetLastError/GetLastError inexistant
    ("            ctypes.SetLastError(0)\n"
     "            base = k32.LoadLibraryExW(chemin_sonde, None, 0x00000001)\n"
     "            err = ctypes.GetLastError()",
     "            k32.SetLastError(0)\n"
     "            base = k32.LoadLibraryExW(chemin_sonde, None, 0x00000001)\n"
     "            err = ctypes.get_last_error()"),
    # 4. l'en-tête du témoin : le littéral périmé dev.6
    ('    consigne("=== LE TERRAIN M10-(e) : LE RUN DE LOUPE '
     '(loupe.exe 0.1.0-dev.6) ===")',
     '    consigne(f"=== LE TERRAIN M10-(e) : LE RUN DE LOUPE '
     '(loupe.exe {VERSION_TXT}) ===")'),
    # 5. k32 né AVEC use_last_error — le contrat de get_last_error
    ('    k32 = ctypes.WinDLL("kernel32")',
     '    k32 = ctypes.WinDLL("kernel32", use_last_error=True)'),
    # 6. le texte T0 : la carte en génération 13, la dette nommée
    ('             f"L\'EMPREINTE ASSERTÉE (la carte génération 14 prouve '
     'CES octets)")',
     '             f"L\'EMPREINTE ASSERTÉE (l\'empreinte prouve CES octets — "\n'
     '             f"la carte, génération 13, à régénérer au labo)")'),
    # 7. la cartographie : le GetLastError latent
    ('             f"{ctypes.GetLastError()}) — LA SONDE a nommé les axes "',
     '             f"{ctypes.get_last_error()}) — LA SONDE a nommé les axes "'),
    # 8. le message PORTE-R10 : le littéral périmé dev.6
    ('        echec("PORTE-R10", f"le qword version @0x2E80 != '
     '{VERSION_R10:#x} "\n'
     '             f"(loupe 0.1.0-dev.6)")',
     '        echec("PORTE-R10", f"le qword version @0x2E80 != '
     '{VERSION_R10:#x} "\n'
     '             f"(loupe {VERSION_TXT})")'),
]
for vieux, neuf in SUIVANTS:
    assert vieux in s, f"introuvable : {vieux[:70]}…"
    s = s.replace(vieux, neuf, 1)

open(SRC, "w", encoding="utf-8").write(s)
apres = hashlib.md5(s.encode()).hexdigest()
print(f"scenario-loupe.py : {avant[:8]}… → {apres[:8]}… ({len(s)} o)")

# -------------------------------------------------------------------- LE BAT
b = open(BAT, encoding="ascii").read()
avant_b = hashlib.md5(b.encode()).hexdigest()

# la numérotation passe à /4 et le journal d'événements entre en scène
b = b.replace(
    """echo [3/3] LE RAPPORT WER (si un crash fut consigne)...
echo [3/3] LES RAPPORTS WER RECENTS (les 5 derniers) : >> preuves-loupe\\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\ReportArchive" 2>nul | findstr /i "loupe" >> preuves-loupe\\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\ReportQueue" 2>nul | findstr /i "loupe" >> preuves-loupe\\temoin-vitrine.txt
""",
    """echo [3/4] LE RAPPORT WER (si un crash fut consigne)...
echo [3/4] LES RAPPORTS WER RECENTS (les 5 derniers) : >> preuves-loupe\\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\ReportArchive" 2>nul | findstr /i "loupe" >> preuves-loupe\\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\\Microsoft\\Windows\\WER\\ReportQueue" 2>nul | findstr /i "loupe" >> preuves-loupe\\temoin-vitrine.txt

echo [4/4] LE JOURNAL D EVENEMENTS (la piece nommee par le systeme)...
echo. >> preuves-loupe\\temoin-vitrine.txt
echo [4/4] LE JOURNAL D EVENEMENTS - Application Error 1000 : le module fautif et le decalage de l exception NOMMES ci-dessous : >> preuves-loupe\\temoin-vitrine.txt
wevtutil qe Application /q:"*[System[(EventID=1000 or EventID=1001)]]" /c:3 /rd:true /f:text >> preuves-loupe\\temoin-vitrine.txt 2>nul
""")

b = b.replace("echo [1/3] LA VITRINE VIDE", "echo [1/4] LA VITRINE VIDE")
b = b.replace("echo       la barre d'etat porte l'usage ; FERMEZ la fenetre par Alt+F4.",
              "echo       la barre d'etat porte l'usage ; FERMEZ la fenetre par Alt+F4.")
b = b.replace("echo [1/3] LA VITRINE VIDE - code de sortie ci-dessous",
              "echo [1/4] LA VITRINE VIDE - code de sortie ci-dessous")
b = b.replace("echo [2/3] LA VITRINE AVEC FICHIER (une COPIE : la session nait entiere)...",
              "echo [2/4] LA VITRINE AVEC FICHIER (une COPIE : la session nait entiere)...")
b = b.replace("echo [2/3] LA VITRINE AVEC FICHIER (loupe.exe temoin-fichier.bin) - code de sortie ci-dessous",
              "echo [2/4] LA VITRINE AVEC FICHIER (loupe.exe temoin-fichier.bin) - code de sortie ci-dessous")

open(BAT, "w", encoding="ascii").write(b)
apres_b = hashlib.md5(b.encode()).hexdigest()
print(f"temoin-vitrine.bat : {avant_b[:8]}… → {apres_b[:8]}… ({len(b)} o)")
