﻿@echo off
rem LANCEUR — LE LANCEUR OFFICIEL du kit de l'unite 5
rem (loupe-13 recherche x bras C, la campagne D204). Le run court dans SA
rem PROPRE console, INTACT : le GUI ne l'intercepte jamais (CA6).
rem Le temoin ne se signe JAMAIS ici : votre main, toujours (D99).
rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition
rem v2 du kit 01, la meme discipline).
title TRIADE - Unite 5 (loupe-13 recherche x bras C) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite13C.py 2>&1 | Tee-Object -FilePath run-console-unite13C.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite13C\temoin-unite13C.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
