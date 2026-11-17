@echo off
rem ============================================================================
rem LANCER-RUN-UNITE02-D210-1CLIC.bat - LE RUN DE L'UNITE 01 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite02-d210 - l'edition du 18/11/2026, le
rem  correctif T0 grave (EMPREINTES-PIECES-RUN.txt)]
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Le GUI ouvre sa fenetre,
rem recoupe LES DIX-SEPT pieces du kit (fail-closed), prouve que LE
rem SCENARIO SCELLE voit les pieces (LA PREUVE T0 - le correctif du
rem 18/11 : le kit du 17/11 portait ses gravures "nom en tete", le
rem scenario parse "sha256 en tete", le run aurait REFUSE), et LE
rem BOUTON VERT conduit tout : LE RUN au scenario-unite02.py TEL QUEL
rem (SA console ecrite AU FIL DE L'EAU, UTF-8 des deux cotes du
rem tuyau), les verdicts RECOPIES des lignes, le chrono M4, LA
rem COLLECTE (la console COPIEE au receptacle preuves-unite02\, le
rem DEPOT-d210-unite02.txt assemble) - puis le temoin est a VOTRE
rem MAIN (D99) : dater, signer au bloc-notes, renvoyer le dossier
rem ENTIER au coffre /test (le GUI l'assemble en zip - l'exigence de
rem la signature et la cap M1 sont tenues par construction).
rem
rem CE QUE LE GUI EXIGE : Python 3 avec tkinter (l'installeur python.org
rem les livre ensemble - cochez "Add to PATH" et "tcl/tk and IDLE").
rem RIEN D'AUTRE : le scenario est pur ctypes de la stdlib, le kit
rem porte ses PIECES (loupe.exe, les temoins) - aucun outil a
rem installer au-dela de Python.
rem
rem CE QUE CE GUI NE FERA JAMAIS : dater ni signer un temoin (votre
rem main, toujours, D99) ; deposer au coffre (il OUVRIRA le /test au
rem navigateur, il n'ecrit JAMAIS au Drive) ; fabriquer un chiffre
rem (les verdicts sont RECOPIES des lignes de console) ; toucher les
rem pieces scellees (loupe.exe, le scenario, les temoins : LUS, le
rem scenario lui-meme recoupe loupe.exe AVANT de courir) ; renommer
rem ni editer les pieces du receptacle.
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC"
rem apparait au double-clic [la marque du web] : clic droit sur CE
rem fichier, Proprietes, cochez "Debloquer" en bas, OK - puis
rem double-cliquez encore. Ce fichier descend du coffre Drive : il
rem porte la marque, comme toute piece telechargee.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - le run de l'unite 01 D210 (loupe-02 lire x bras T) en un clic
cd /d "%~dp0"

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 goto tkinter_absent

%PY% triade_run_unite02_d210_gui.py
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
