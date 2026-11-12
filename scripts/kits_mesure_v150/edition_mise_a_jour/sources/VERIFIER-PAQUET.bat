@echo off
rem ============================================================================
rem VERIFIER-PAQUET.bat - LE VERIFICATEUR D'INTEGRITE DE L'EXTRACTION (l'edition
rem MISE A JOUR du paquet multimachines, 12/11/2026 - la commande du
rem developpeur : 'fais un kit mis a jour avec ce qu'il reste a faire ou des
rem corrections si necessaires, ou eventuellement rajouter des tests si tu
rem trouve ca pertinent').
rem
rem POURQUOI CE TEST (l'evenement qui l'a motive) : le 12/11 meme, le coffre
rem Drive a REFUSE test_appel.exe au telechargement (HTTP 403 'malware or
rem spam' - un faux positif des exe de mesure de timing, Entree 248). Votre
rem ANTIVIRUS LOCAL peut faire de meme A L'EXTRACTION : un exe silencieusement
rem retire fait vivre le kit-2 sans son epreuve d'appel. Ce verificateur
rem recoupe les 45 pieces de l'extraction contre le manifeste grave au
rem laboratoire : l'extraction incomplete, l'exe mange par l'antivirus, la
rem piece bougee - TOUT ecart est NOMME.
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Avec Python : le recoup INTEGRAL des 45 pieces
rem (le rapport nait dans verification-paquet.txt). Sans Python : les CINQ
rem pieces scellees recoupees par certutil - et l'honnetete dite : chaque
rem lanceur recoupe de toute facon SON scelle avant tout run.
rem ============================================================================

setlocal EnableExtensions
title TRIADE - le verificateur du paquet (MISE A JOUR, 12/11/2026)
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LE VERIFICATEUR DU PAQUET - l'integrite de VOTRE extraction
echo  Les 45 pieces recoupees contre le manifeste grave au laboratoire.
echo  Un ecart nomme est un RESULTAT (D189) - jamais un echec a maquiller.
echo ============================================================================
echo.

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if defined PY goto avec_python

echo [ecart nomme] Python 3 est INTROUVABLE : le recoup INTEGRAL des 45 pieces
echo               exige Python. Le verificateur recoupe ici les CINQ pieces
echo               scellees (certutil) - chaque lanceur recoupe de toute facon
echo               SON scelle avant tout run. Pour le recoup integral :
echo               https://www.python.org (cochez 'Add to PATH') puis relancez.
echo.
set "ECARTS=0"
call :recoup "pc-windows\kit-1-shani\moteur-shani.bin" 761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec
if errorlevel 1 set /a ECARTS+=1
call :recoup "pc-windows\kit-2-dudect\cibles\proxy-image.bin" 0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff
if errorlevel 1 set /a ECARTS+=1
call :recoup "pc-windows\kit-3-terrain-tiers-loupe\loupe-kit-13\loupe.exe" c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1
if errorlevel 1 set /a ECARTS+=1
call :recoup "qemu-wsl2\kit-m7d\corpus" ec343b4e8bebf21c8b29a6da1a5eb022fb7b8e4b50ce95c5906734ef0b043799
if errorlevel 1 set /a ECARTS+=1
call :recoup "qemu-wsl2\kit-m7d\demo" e57fc74be2ea67ab4c05351d0b5e0b93b6147ec34f2fb7aabbfd1ab7f141cde9
if errorlevel 1 set /a ECARTS+=1
echo.
if "%ECARTS%"=="0" (
    echo [BILAN] les CINQ scelles sont INTACTS dans cette extraction.
) else (
    echo [BILAN] %ECARTS% scelle(s) ABSENT(s) ou DIVERGENT(s) - un ecart nomme
    echo        est un RESULTAT ^(D189^) : renvoyez l'ecran TEL QUEL ^(D122^).
    echo        Si un exe manque : c'est l'ANTIVIRUS, pas le paquet - voyez
    echo        CE-QUI-RESTE-A-FAIRE.txt, section LES DEUX TESTS NEUFS.
)
set "RC=%ECARTS%"
goto fin

:avec_python
echo [python] trouve : %PY%
echo.
%PY% verifier_paquet.py
set "RC=%errorlevel%"
goto fin

:recoup
if not exist "%~1" (
    echo [ecart nomme] %~1 : ABSENTE de l'extraction
    exit /b 1
)
certutil -hashfile "%~1" SHA256 > "%TEMP%\triade-verif.txt" 2>&1
findstr /i "%~2" "%TEMP%\triade-verif.txt" >nul
if errorlevel 1 (
    echo [ecart nomme] %~1 : sha256 DIVERGENTE du scelle
    exit /b 1
)
echo [recoup] %~1 : INTACTE
exit /b 0

:fin
echo.
echo ============================================================================
echo  LE RAPPORT COMPLET VIT DANS verification-paquet.txt ^(si Python a vecu^).
echo  VERT : l'extraction est la piece du laboratoire - vivez les kits.
echo  ECART NOMME : renvoyez le rapport TEL QUEL ^(D122^) - le labo recoupe.
echo ============================================================================
pause
exit /b %RC%
