@echo off
rem ============================================================================
rem LANCER-REPLICATION.bat - LE KIT DE REPLICATION EN 1 CLIC
rem [l'edition des gestes ouverts, 13/11/2026].
rem
rem LE KIT DE REPLICATION v0.15.0 : la grille de codage T/X finalisee [les
rem cinq classes terrain T1-T5, les trois classes laboratoire X1-X3] et le
rem CALCULATEUR KAPPA DE COHEN AUTOTESTE [trois cas au k calculable a la
rem main : parfait, desaccord total, partiel].
rem
rem CE QUE CE LANCEUR FAIT : il trouve Python, vit l'AUTOTEST du calculateur
rem - la preuve a froid - puis, le jour des DEUX jeux d'annotations, calcule
rem le k [le seuil d'acceptation pre-enregistre : k superieur ou egal a
rem 0,61 - D189].
rem
rem CE QUI MANQUE AU GESTE COMPLET - consigne, jamais maquille :
rem   le SECOND ANNOTATEUR, a recruter ;
rem   le SECOND DOMAINE, en attente d'une vraie commande.
rem Aucun des deux ne s'automatise - ce sont des gestes du projet.
rem
rem Les pieces sont INTACTES, celles du depot [scripts/replication_v150/].
rem ============================================================================

setlocal EnableExtensions
title TRIADE - la replication - l'autotest du kappa + la grille T/X
cd /d "%~dp0"
set "RC=2"

rem ---- Python [aucun paquet a installer, un Python 3 suffit] ----
set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

:menu
cls
echo ============================================================================
echo  LA REPLICATION - LE KIT v0.15.0 - la grille T/X + le kappa de Cohen
echo  Le seuil d'acceptation PRE-ENREGISTRE : k superieur ou egal a 0,61
echo  [D189 - inchange]
echo ============================================================================
echo.
echo   1. L'AUTOTEST DU CALCULATEUR - la preuve a froid [trois cas
echo      synthetiques au k calculable a la main]
echo   2. CALCULER LE KAPPA - vos DEUX fichiers d'annotations [le CSV :
echo      id,classe - un fichier par annotateur]
echo   3. LA GRILLE DE CODAGE T/X - l'ouvrir
echo   4. LE LISEZMOI - les criteres, les statuts, le mode d'emploi
echo   0. RETOUR
echo.
set "CHOIX="
set /p "CHOIX=Votre choix (0-4) : "
if not defined CHOIX goto menu
if "%CHOIX%"=="1" goto autotest
if "%CHOIX%"=="2" goto kappa
if "%CHOIX%"=="3" goto grille
if "%CHOIX%"=="4" goto lisezmoi
if "%CHOIX%"=="0" goto fin
goto menu

:autotest
echo.
echo [autotest] %PY% kohen_kappa_v150.py
echo.
%PY% kohen_kappa_v150.py
set "RC=%errorlevel%"
echo.
if "%RC%"=="0" (echo  L'AUTOTEST EST VERT - le calculateur est PRET.) else (echo  L'AUTOTEST EST ROUGE - code %RC% : renvoyez l'ecran TEL QUEL [D122].)
pause
goto menu

:kappa
echo.
echo  LE KAPPA DE COHEN - le jour des DEUX jeux d'annotations.
echo  Chaque fichier : une ligne par item, la forme  id,classe  - par
echo  exemple  loupe-05,T2.
echo.
set "A="
set "B="
set /p "A=Le fichier du premier annotateur : "
set /p "B=Le fichier du second annotateur : "
if not defined A goto saisie_refusee
if not defined B goto saisie_refusee
if not exist "%A%" goto fichier_absent
if not exist "%B%" goto fichier_absent
echo.
echo [kappa] %PY% kohen_kappa_v150.py "%A%" "%B%"
echo.
%PY% kohen_kappa_v150.py "%A%" "%B%"
set "RC=%errorlevel%"
echo.
if "%RC%"=="0" (echo  LE KAPPA FRANCHIT LE SEUIL 0,61 - l'acceptation D189.) else (echo  LE KAPPA EST SOUS LE SEUIL - le desaccord se CONSIGNE, les items en litige se NOMMENT : un RESULTAT, jamais un echec a maquiller.)
pause
goto menu

:grille
start notepad "grille_tx.csv"
echo  LA GRILLE EST OUVERTE au bloc-notes - les classes T1-T5 et X1-X3,
echo  chacune avec sa definition OPERATIONNELLE et ses exemples vecus.
pause
goto menu

:lisezmoi
cls
type "LISEZMOI-replication.txt"
echo.
echo [fin du LISEZMOI - appuyez sur une touche pour revenir au menu]
pause >nul
goto menu

:saisie_refusee
echo.
echo [REFUS NOMME] la saisie est incomplete - les DEUX fichiers, ou rien.
pause
goto menu

:fichier_absent
echo.
echo [REFUS NOMME] le fichier est ABSENT - rien ne court. Verifiez le
echo        chemin, la casse comprise, puis recommencez.
pause
goto menu

:python_absent
echo.
echo [REFUS NOMME] Python 3 est ABSENT - le calculateur en exige un.
echo        https://www.python.org - cochez Add to PATH.
pause
exit /b 2

:fin
endlocal
