@echo off
rem ============================================================================
rem DIAGNOSTIC-MACHINE.bat - LE DIAGNOSTIC D'APTITUDE DE LA MACHINE (l'edition
rem MISE A JOUR du paquet multimachines, 12/11/2026 - la commande du
rem developpeur : 'fais un kit mis a jour avec ce qu'il reste a faire ou des
rem corrections si necessaires, ou eventuellement rajouter des tests si tu
rem trouve ca pertinent').
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Le diagnostic CONSTATE (il ne mesure rien,
rem il ne fabrique aucun chiffre) :
rem   - la machine nommee : l'OS, l'architecture, le processeur ;
rem   - le silicium lu par CPUID (fabricant, famille, modele, pas, SHA-NI
rem     present ou absent - LA MEME lecture que le kit-1 shani au geste A :
rem     CPUID feuille 7, EBX bit 29) ;
rem   - ce qui vit : Python (et ses 64 bits), compilateurs, WSL2 ;
rem   - LE VERDICT : quels kits de CE paquet sont vivables ICI - il sert
rem     aussi a choisir la machine du geste B (SHA-NI reel).
rem Le temoin nait dans diagnostic-machine.txt.
rem
rem SANS PYTHON : le diagnostic rend ce que cmd peut lire seul (l'OS,
rem l'arche, le CPU) et vous dit honnetement que le CPUID et le verdict
rem complet exigent Python 3 (https://www.python.org - cochez 'Add to PATH').
rem ============================================================================

setlocal EnableExtensions
title TRIADE - le diagnostic de la machine (paquet MISE A JOUR, 12/11/2026)
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LE DIAGNOSTIC DE LA MACHINE - le paquet multimachines MISE A JOUR
echo  Il constate : la machine, le silicium, ce qui vit, quels kits y sont
echo  vivables. Il ne mesure rien, ne fabrique aucun chiffre.
echo ============================================================================
echo.

rem ---- Python (aucun paquet a installer, un Python 3 suffit) ----
set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto sans_python

echo [python] trouve : %PY%
echo.
%PY% diagnostic_machine.py
set "RC=%errorlevel%"
goto fin

:sans_python
echo [machine] l'OS :
ver
echo [machine] l'arche : %PROCESSOR_ARCHITECTURE%
echo [machine] le CPU  : %PROCESSOR_IDENTIFIER%
echo.
echo [ecart nomme] Python 3 est INTROUVABLE (py / python / python3 essayes) :
echo               le CPUID (SHA-NI present ou absent) et le verdict complet
echo               exigent Python. Installez-le depuis https://www.python.org
echo               (cochez 'Add to PATH') puis relancez : deux minutes.
echo               En attendant : le kit-2 dudect vit SANS Python (double-cliquez
echo               son lanceur), et le kit-1 lira le CPUID au T0 de lui-meme.
set "RC=0"

:fin
echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LE DIAGNOSTIC EST ECRIT : diagnostic-machine.txt
) else (
    echo  LE DIAGNOSTIC S'EST ARRETE (code %RC%) - un ecart nomme est un
    echo  RESULTAT ^(D189^) : renvoyez l'ecran TEL QUEL ^(D122^), le labo
    echo  recoupe sur pieces.
)
echo  La feuille de route complete vit dans CE-QUI-RESTE-A-FAIRE.txt.
echo ============================================================================
pause
exit /b %RC%
