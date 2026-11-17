@echo off
rem ============================================================================
rem LANCER-RUN-UNITE08-D210-1CLIC.bat - LE RUN DE L'UNITE 02 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite08-d210 - l'edition v1 du 18/11/2026 : LA
rem  DEUXIEME UNITE de la campagne D210 (loupe-08 ligne x bras T, la
rem  sequence tiree de la graine D217 - jamais re-tiree ; le kit ne a la
rem  Task 208, le juge scenario-unite08.py D204 INCHANGE [44384f5d... la
rem  version corrigee], la gravure EMPREINTES-KIT-UNITE-02-D210.txt NEE
rem  PARSEE - sha256 en tete, le format que le scenario scelle lit : le
rem  defaut T0 de l'unite 01 ne se reproduit pas) ; le dossier racine du
rem  zip porte LE NOM DU KIT (kit-unite-02-d210-20261118 - le pas 1-KIT
rem  du livre du kit : CHOISIR CE DOSSIER ; le double-clic du lanceur EST
rem  le choix - le GUI recoupe LUI-MEME les pieces de CE dossier)]
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Le GUI ouvre sa fenetre,
rem recoupe LES QUATORZE pieces du kit (fail-closed), prouve que LE
rem SCENARIO SCELLE voit les pieces (LA PREUVE T0 - les TREIZE pieces de
rem la gravure, loupe.exe recoupe), et LE BOUTON VERT conduit tout : LE
rem RUN au scenario-unite08.py (SA console ecrite AU FIL DE L'EAU, UTF-8
rem des deux cotes du tuyau), les verdicts RECOPIES des lignes, le
rem chrono M4, LA COLLECTE (la console COPIEE au receptacle
rem preuves-unite08\, le DEPOT-d210-unite08.txt assemble) - puis le
rem temoin est a VOTRE MAIN (D99) : dater, signer au bloc-notes,
rem renvoyer le dossier ENTIER au coffre /test (le GUI l'assemble en
rem zip - l'exigence de la signature et la cap M1 sont tenues par
rem construction).
rem
rem CE QUE LE GUI EXIGE : Python 3 avec tkinter (l'installeur python.org
rem les livre ensemble - cochez "Add to PATH" et "tcl/tk and IDLE").
rem RIEN D'AUTRE : le scenario est pur ctypes de la stdlib, le kit
rem porte ses PIECES (loupe.exe, proxy.exe, le temoin 3f) - aucun outil
rem a installer au-dela de Python.
rem
rem CE QUE CE GUI NE FERA JAMAIS : dater ni signer un temoin (votre
rem main, toujours, D99) ; deposer au coffre (il OUVRIRA le /test au
rem navigateur, il n'ecrit JAMAIS au Drive) ; fabriquer un chiffre
rem (les verdicts sont RECOPIES des lignes de console) ; toucher les
rem pieces scellees (loupe.exe, le scenario, proxy.exe, les temoins :
rem LUS, le scenario lui-meme recoupe loupe.exe AVANT de courir) ;
rem renommer ni editer les pieces du receptacle.
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC"
rem apparait au double-clic [la marque du web] : clic droit sur CE
rem fichier, Proprietes, cochez "Debloquer" en bas, OK - puis
rem double-cliquez encore. Ce fichier descend du coffre Drive : il
rem porte la marque, comme toute piece telechargee.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - le run de l'unite 02 D210 (loupe-08 ligne x bras T) en un clic
cd /d "%~dp0"

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 goto tkinter_absent

%PY% triade_run_unite08_d210_gui.py
set "RC=%errorlevel%"
if "%RC%"=="0" goto fin
echo.
echo [REFUS NOMME] le GUI s'est ferme avec le code %RC% - l'ecran du GUI
echo        nomme la cause ; le journal de session vit a TRIADE_logs\.
:fin
pause
exit /b %RC%

:python_absent
echo.
echo [REFUS NOMME] Python 3 est ABSENT - le GUI en exige un.
echo        https://www.python.org - cochez "Add to PATH".
pause
exit /b 2

:tkinter_absent
echo.
echo [REFUS NOMME] tkinter est ABSENT de ce Python - reinstallez Python
echo        depuis python.org en cochant "tcl/tk and IDLE" (livre avec
echo        l'installeur ; tkinter ne s'installe PAS par pip).
pause
exit /b 2
