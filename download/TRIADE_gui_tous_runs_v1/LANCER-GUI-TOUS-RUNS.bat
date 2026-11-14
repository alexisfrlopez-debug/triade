@echo off
rem ============================================================================
rem LANCER-GUI-TOUS-RUNS.bat - LE GUI PAS A PAS DE TOUS LES TESTS ET RUNS
rem [le kit TRIADE_gui_tous_runs_v1 - la premiere edition, le 14/11/2026]
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Le GUI ouvre sa fenetre,
rem conduit TOUS les tests et runs pas a pas - tout au clic : le catalogue
rem (les etats, l'ordre des gestes restants), la campagne D204 (le verrou
rem des HUIT pieces, l'atelier, la calibration, les quatorze unites, le
rem carnet, les livraisons, les defauts, le chronometre, le suivi), les
rem SEPT runs 1-clic (le fichier recoupe contre son empreinte gravEE,
rem le run dans sa console officielle, la piece signee de votre main,
rem l'etat nomme).
rem
rem CE QUE LE GUI EXIGE : Python 3 avec tkinter (l'installeur python.org
rem les livre ensemble - cochez "Add to PATH" et "tcl/tk and IDLE").
rem Les sept fichiers 1-clic se telechargent du coffre /test - ce kit
rem porte la campagne (campagne-d204\), les autres runs vivent de leurs
rem fichiers autonomes seuls.
rem
rem LA CONTINUITE : si le GUI campagne v1 a deja vecu a cote, son etat
rem (etat-campagne-d204.json) est IMPORTE a l'ouverture - l'atelier, la
rem calibration et les kits choisis survivent ; la campagne CONTINUE,
rem jamais ne recommence.
rem
rem CE QUE LE GUI NE FERA JAMAIS : dater ni signer un temoin (votre main,
rem D99) ; deposer au coffre (le renvoi du dossier ENTIER vous
rem appartient) ; fabriquer un chiffre (CA5/CA6) ; toucher les originaux
rem scelles (les copies datees de l'atelier seulement) ; depasser la cap
rem pre-enregistree (TROIS livraisons par bloc, DOUZE par application,
rem l'arret au premier vert - le paragraphe 7 du plan) ; lancer un
rem fichier 1-clic divergent (le recoup d'empreinte precede tout
rem lancement - fail-closed).
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC" apparait au
rem double-clic [la marque du web] : clic droit sur CE fichier, Proprietes,
rem cochez "Debloquer" en bas, OK - puis double-cliquez encore. Ce fichier
rem descend du coffre Drive : il porte la marque, comme toute piece telechargee.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - le GUI de tous les runs, pas a pas
cd /d "%~dp0"

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 goto tkinter_absent

%PY% triade_tous_runs_gui.py
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
