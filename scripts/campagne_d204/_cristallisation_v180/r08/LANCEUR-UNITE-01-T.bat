@echo off
rem LANCEUR-UNITE-01-T.bat — LE LANCEUR OFFICIEL du kit de l'unite 1
rem (loupe-01 x bras T, la campagne D204). Le run court dans SA PROPRE
rem console, INTACT : le GUI ne l'intercepte jamais (CA6).
rem Le temoin ne se signe JAMAIS ici : votre main, toujours (D99).
title TRIADE - Unite 1 (loupe-01 x T) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
powershell -NoProfile -Command "python scenario-unite01.py 2>&1 | Tee-Object -FilePath run-console-unite01.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite01\temoin-unite01.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
