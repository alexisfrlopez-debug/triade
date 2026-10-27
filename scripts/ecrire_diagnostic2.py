#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TRIADE D52 — genère DIAGNOSTIC2-SUPERVISEUR.cmd (ASCII pur, CRLF).

Echelle de sondes + collecte des rapports WER (minidumps) + historique
Defender. Sortie : rapport-diagnostic2.txt + wer-superviseur.zip a
deposer dans le dossier test du Drive.
"""

import pathlib

CMD = r"""@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set RAPPORT=rapport-diagnostic2.txt
echo ============================================================ > %RAPPORT%
echo DIAGNOSTIC 2 SUPERVISEUR TRIADE >> %RAPPORT%
echo %date% %time% >> %RAPPORT%
echo ============================================================ >> %RAPPORT%

echo [1/6] Version Windows...
ver >> %RAPPORT% 2>&1

echo [2/6] Empreintes des fichiers attendus...
echo. >> %RAPPORT%
echo --- md5 attendus --- >> %RAPPORT%
echo   superviseur-terrain3.exe = 40b2f350ad8556d028d431174d429189 >> %RAPPORT%
echo   superviseur-zero.exe     = 4205ba7f10b69a486659ae13d3efa5c8 >> %RAPPORT%
echo   demo.exe                 = 73c064fbaf46 (prefixe) >> %RAPPORT%
for %%F in (superviseur-terrain3.exe superviseur-zero.exe demo.exe) do (
  if exist "%%F" (
    echo --- md5 %%F --- >> %RAPPORT%
    certutil -hashfile "%%F" MD5 >> %RAPPORT% 2>&1
  ) else (
    echo !!! %%F ABSENT du dossier >> %RAPPORT%
  )
)

echo [3/6] Marque du Web (Zone.Identifier)...
echo. >> %RAPPORT%
echo --- Zone.Identifier --- >> %RAPPORT%
for %%F in (superviseur-terrain3.exe superviseur-zero.exe) do (
  type "%%F:Zone.Identifier" > nul 2>&1
  if !errorlevel! equ 0 (
    echo %%F : MARQUE du web PRESENTE : >> %RAPPORT%
    type "%%F:Zone.Identifier" >> %RAPPORT% 2>&1
  ) else (
    echo %%F : pas de marque du web >> %RAPPORT%
  )
)

echo [4/6] Echelle de sondes (6 secondes chacune)...
echo. >> %RAPPORT%
echo === ECHELLE DE SONDES === >> %RAPPORT%
echo Chaque exe est lance, attendu 6 s, verifie, puis ferme. >> %RAPPORT%
echo Un exe VIVANT apres 6 s = sa fenetre est apparue = il FONCTIONNE. >> %RAPPORT%
for %%F in (superviseur-terrain3.exe superviseur-zero.exe demo.exe) do (
  if exist "%%F" (
    echo. >> %RAPPORT%
    echo --- sonde : %%F --- >> %RAPPORT%
    taskkill /im "%%F" > nul 2>&1
    start "" "%%F"
    timeout /t 6 /nobreak > nul
    tasklist /fi "IMAGENAME eq %%F" 2>nul | find /i "%%F" > nul
    if !errorlevel! equ 0 (
      echo RESULTAT : VIVANT apres 6 s ^(fenetre visible^) - FONCTIONNE >> %RAPPORT%
      taskkill /im "%%F" >> %RAPPORT% 2>&1
    ) else (
      echo RESULTAT : MORT avant 6 s ^(crash ou blocage^) >> %RAPPORT%
    )
  ) else (
    echo --- sonde %%F : FICHIER ABSENT --- >> %RAPPORT%
  )
)
echo. >> %RAPPORT%
echo Interpretation : >> %RAPPORT%
echo  - terrain3 MORT + zero VIVANT = le contenu de .blob ^(proxy.exe >> %RAPPORT%
echo    embarque + jetons^) declenche le blocage au lancement ^(antivirus^). >> %RAPPORT%
echo  - terrain3 MORT + zero MORT = le declencheur est ailleurs dans >> %RAPPORT%
echo    l'image ou dans l'environnement ^(voir dumps WER ci-dessous^). >> %RAPPORT%

echo [5/6] Collecte des rapports WER (dumps de plantage)...
echo. >> %RAPPORT%
echo === RAPPORTS WER === >> %RAPPORT%
if exist wer-collect rmdir /s /q wer-collect
mkdir wer-collect
set TROUVE=0
for %%D in ("%ProgramData%\Microsoft\Windows\WER\ReportArchive" "%ProgramData%\Microsoft\Windows\WER\ReportQueue" "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive" "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportQueue") do (
  if exist "%%~D" (
    for /d %%M in ("%%~D\*superviseur*") do (
      echo copie : %%~nxM >> %RAPPORT%
      xcopy /e /i /y "%%M" "wer-collect\%%~nxM" >> %RAPPORT% 2>&1
      set TROUVE=1
    )
  )
)
if %TROUVE% equ 0 (
  echo Aucun rapport WER superviseur trouve ^(droits insuffisants ou purges^) >> %RAPPORT%
)

echo [6/6] Historique Defender recent...
echo. >> %RAPPORT%
echo === DEFENDER : 15 dernieres detections === >> %RAPPORT%
powershell -NoProfile -Command "Get-MpThreatDetection | Select-Object -First 15 InitialDetectionTime,ProcessName,Resources | Format-List" >> %RAPPORT% 2>&1

echo. >> %RAPPORT%
echo === ETAT DEFENDER === >> %RAPPORT%
powershell -NoProfile -Command "Get-MpComputerStatus | Select-Object AMServiceEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,AntivirusEnabled | Format-List" >> %RAPPORT% 2>&1

echo. >> %RAPPORT%
echo ============================================================ >> %RAPPORT%
echo FIN DU DIAGNOSTIC 2 >> %RAPPORT%

if exist wer-collect (
  powershell -NoProfile -Command "Compress-Archive -Path wer-collect\* -DestinationPath wer-superviseur.zip -Force"
)
echo.
echo ============================================================
echo  DIAGNOSTIC 2 TERMINE.
echo  A deposer dans le dossier test du Drive :
echo    1. %RAPPORT%
if exist wer-superviseur.zip (
  echo    2. wer-superviseur.zip ^(dumps de plantage^)
)
echo ============================================================
pause
"""

out = pathlib.Path("/home/z/my-project/triade/terrain/DIAGNOSTIC2-SUPERVISEUR.cmd")
contenu = CMD.replace("\r\n", "\n")
# garanties : ASCII pur + CRLF
contenu.encode("ascii")          # leve si caractere non ASCII
out.write_bytes(contenu.replace("\n", "\r\n").encode("ascii"))
print(f"{out} : {out.stat().st_size} octets, ASCII pur, CRLF")
# copie a cote de la sonde dans livraison/
liv = pathlib.Path("/home/z/my-project/triade/terrain/livraison/DIAGNOSTIC2-SUPERVISEUR.cmd")
liv.write_bytes(out.read_bytes())
print(f"{liv} : copie OK")
