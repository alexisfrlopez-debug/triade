@echo off
rem LANCEUR-UNITE-01-C.bat — LE LANCEUR OFFICIEL du kit de l'unite 1
rem x BRAS C (loupe-01, la campagne D204, le flux standard gcc -O2).
rem Le run court dans SA PROPRE console, INTACT : le GUI ne l'intercepte
rem jamais (CA6). Le temoin ne se signe JAMAIS ici : votre main (D99).
rem La capture console vit en UTF-8 des deux cotes du tuyau (l'edition
rem v2 du lanceur du bras T, la meme discipline).
title TRIADE - Unite 1 x bras C (loupe-01, gcc -O2) - campagne D204
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo [REFUS] python introuvable au PATH - le kit exige Python 3.
  pause
  exit /b 2
)
set PYTHONIOENCODING=utf-8
powershell -NoProfile -Command "[Console]::OutputEncoding=[Text.Encoding]::UTF8; python scenario-unite01C.py 2>&1 | Tee-Object -FilePath run-console-unite01C.txt"
set CODE=%ERRORLEVEL%
echo.
echo === LE RUN A FINI (code %CODE%) ===
echo Le temoin vit a preuves-unite01C	emoin-unite01C.txt :
echo DATER et SIGNER de votre main, renvoyer le dossier ENTIER au coffre /test.
pause
exit /b %CODE%
