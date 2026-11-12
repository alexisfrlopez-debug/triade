@echo off
rem ============================================================================
rem LANCER-KIT-3-LOUPE.bat - LE LANCEUR DU KIT 3 (l'edition AUTOMATISEE du
rem paquet multimachines, 12/11/2026 - la commande du developpeur : 'je veux
rem que l'utilisation soit la plus simple possible, en automatisant au
rem maximum').
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Ce lanceur fait pour vous les gestes du
rem LISEZMOI-KIT-LOUPE.md :
rem   1. il RECOUPE le sha256 de loupe.exe contre le scelle AVANT TOUT
rem      lancement (c1115105... : la piece ne doit JAMAIS bouger d'un octet) ;
rem   2. il trouve Python et VERIFIE qu'il est 64 bits (exige par le kit) ;
rem   3. il lance le scenario INTEGRAL T0-T7 + S0 (quelques secondes).
rem
rem Ce qui reste a VOTRE main : le TEMOIN VITRINE (facultatif : double-cliquez
rem temoin-vitrine.bat - il ouvre des fenetres que VOUS fermez par Alt+F4),
rem la signature des temoins, et le renvoi du dossier preuves-loupe\ ENTIER
rem au coffre /test (dossier Drive 'Triade'). La machine tierce n'a JAMAIS
rem servi au developpement : c'est la question meme du kit.
rem ============================================================================

setlocal EnableExtensions
title TRIADE - kit 3 loupe (le terrain tiers, la machine vierge)
cd /d "%~dp0loupe-kit-13"
set "RC=2"

echo ============================================================================
echo  LE KIT 3 TERRAIN TIERS - LOUPE 0.1.1 - paquet multimachines AUTO
echo  Le scenario INTEGRAL T0-T7 + S0 sur la machine tierce : la question du
echo  kit est : le vert tient-il sur une machine qui n'a JAMAIS servi au
echo  developpement ? Chaque ecart nomme est un RESULTAT ^(D189^).
echo ============================================================================

rem ---- les pieces ----
if not exist loupe.exe goto piece_absente
if not exist scenario-loupe.py goto piece_absente
echo [pieces] loupe.exe + scenario-loupe.py : presents.

rem ---- LE RECOUP AVANT TOUT LANCEMENT (l'exigence du LISEZMOI) ----
echo [recoup] sha256 attendu de loupe.exe :
echo          c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1
certutil -hashfile loupe.exe SHA256 > "%TEMP%\triade-sha-loupe.txt" 2>&1
findstr /i "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1" "%TEMP%\triade-sha-loupe.txt" >nul
if errorlevel 1 goto loupe_divergente
echo [recoup] loupe.exe INTACTE - la piece scellee est la piece du coffre.

rem ---- Python 64 bits (exige par le kit : l'arene et les pointeurs) ----
set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent
echo [python] trouve : %PY%
%PY% -c "import struct; raise SystemExit(0 if struct.calcsize('P')*8 == 64 else 5)"
if errorlevel 1 goto python_32bits
echo [python] 64 bits confirme.

rem ---- LE SCENARIO INTEGRAL (quelques secondes) ----
echo.
echo [run] %PY% scenario-loupe.py  -  le scenario T0-T7 + S0...
echo.
%PY% scenario-loupe.py
set "RC=%errorlevel%"

echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LE VERDICT : code %RC%. Les preuves vivent dans preuves-loupe\
) else (
    echo  LE VERDICT : code %RC% - un ecart nomme est un RESULTAT ^(D189^) :
    echo  renvoyez preuves-loupe\ TEL QUEL, le labo recoupe sur pieces.
)
echo.
echo  LE TEMOIN VITRINE ^(facultatif, un geste a part^) : double-cliquez
echo  temoin-vitrine.bat - il ouvre DEUX fenetres que VOUS fermez par Alt+F4,
echo  les codes de sortie sont consignes au temoin.
echo.
echo  A VOTRE MAIN : datez et signez les temoins de votre main, puis renvoyez
echo  le dossier preuves-loupe\ ENTIER au coffre /test.
echo ============================================================================
pause
exit /b %RC%

:piece_absente
echo.
echo [REFUS] une piece du kit est ABSENTE - extrayez le zip COMPLET dans un
echo         dossier NEUF ^(D99, ne melangez jamais les runs^).
pause
exit /b 2

:loupe_divergente
echo.
echo [REFUS] le sha256 de loupe.exe DIVERGE du scelle ^(c1115105...^) : la
echo         piece a bouge - RIEN ne sera execute. Re-extrayez le zip COMPLET
echo         dans un dossier NEUF ^(D99^). La piece ne bouge JAMAIS d'un octet.
pause
exit /b 2

:python_absent
echo.
echo [REFUS] Python est INTROUVABLE ^(py / python / python3 essayes^).
echo         Installez Python 64 bits depuis https://www.python.org ^(cochez
echo         'Add to PATH'^) puis relancez ce lanceur.
pause
exit /b 2

:python_32bits
echo.
echo [REFUS] ce Python est 32 bits - le kit loupe EXIGE un Python 64 BITS
echo         ^(l'arene memoire et la piece scellee sont 64 bits^). Installez
echo         Python 64 bits depuis https://www.python.org puis relancez.
pause
exit /b 2
