﻿@echo off
rem LANCEUR - LE LANCEUR OFFICIEL du kit d'attribution de l'unite 04 D210
rem (loupe-16 saisie x bras C - la piece C compilee re-livree via le kit
rem standard minimal, le plan D210 par. 4). Le run court dans SA PROPRE
rem console, INTACT : le GUI ne l'intercepte jamais (CA6). Le temoin ne
rem se signe JAMAIS ici : votre main, toujours (D99). La capture console
rem vit en UTF-8 des deux cotes du tuyau (l'edition v2 du kit 01, la meme
rem discipline).
title TRIADE - Attribution unite 04 D210 (loupe-16 saisie x bras C)
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite16C.py 2>&1 | Tee-Object -FilePath run-console-unite16C.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite16C\temoin-unite16C.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
echo.
echo AU LIVRE (le bloc-notes, le geste de la ligne - le guide-344 par. 7) :
echo la ligne M1 C-loupe-16-attr-it1 au verdict RECOPIE, la ligne M3 du carnet
echo aux bornes honnetes de votre main - l'atelier ENTIER re-depose ensuite.
pause
exit /b %CODE%
