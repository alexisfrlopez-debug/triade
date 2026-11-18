@echo off
rem ============================================================================
rem LANCER-RUN-UNITE16-D210-1CLIC.bat - LE RUN DE L'UNITE 04 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite16-d210-v2 - l'edition CORRECTIF du 18/11 au
rem  soir : LE REFUS NOMME du run v1 (« [REFUS] RVA-HOURS-SECTIONS : la RVA
rem  0x0 hors des sections — rien n'est execute ») recoupe, la faute nommee
rem  (le guichet aux QUATRE champs, la marche des plages FT - la doctrine
rem  D54 - et la 4e feuille GetLastError) ; LES QUATORZE pieces du kit v2 :
rem  les DOUZE INCHANGEES (loupe.exe b382e01b...), le scenario CORRIGE
rem  (705951cc... - le correctif confine au guichet, les vecteurs INTACTS),
rem  la gravure regeneree d'UNE ligne ; le kit v1 DEMEURE au coffre
rem  (D143 - le refus du run v1 est un temoin) ; le dossier racine du zip
rem  porte LE NOM DU KIT (kit-unite-04-d210-20261118-v2 - le pas 1-KIT du
rem  livre du kit : CHOISIR CE DOSSIER ; le double-clic du lanceur EST le
rem  choix - le GUI recoupe LUI-MEME les pieces de CE dossier)]
rem
rem ============================================================================
rem LANCER-RUN-UNITE16-D210-1CLIC.bat - LE RUN DE L'UNITE 04 D210 EN UN CLIC
rem [le kit kit-gui-1clic-unite16-d210 - l'edition v2 du 18/11/2026 au soir :
rem  LE COMMANDEMENT DU DEVELOPPEUR, verbatim : << pour les GUI test,
rem  tu peux faire en sorte que je puisse choisir le dossier de
rem  l'atelier afin que le livre se mette a jour durant le run ? >> -
rem  le kit v1 (l'Entree 346) JAMAIS couru, D143 : il demeure au coffre
rem  INTACT ; les QUATORZE pieces INCHANGEES (loupe.exe b382e01b..., le
rem  juge scenario-unite16.py D204 INCHANGE 739a3438..., la gravure NEE
rem  PARSEE - le defaut T0 de l'unite 01 ne se reproduit pas) ; SEUL LE
rem  GUI monte a l'edition v2 : L'ATELIER CHOISI - le livre se met a
rem  jour DURANT le run ; le dossier racine du zip porte LE NOM DU KIT
rem  (kit-unite-04-d210-20261118 - le pas 1-KIT du livre du kit :
rem  CHOISIR CE DOSSIER ; le double-clic du lanceur EST le choix - le
rem  GUI recoupe LUI-MEME les pieces de CE dossier)]
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Le GUI ouvre sa fenetre,
rem recoupe LES QUATORZE pieces du kit (fail-closed), prouve que LE
rem SCENARIO SCELLE voit les pieces (LA PREUVE T0 - les TREIZE pieces de
rem la gravure, loupe.exe recoupe), et LE BOUTON VERT conduit tout : LE
rem RUN au scenario-unite16.py (SA console ecrite AU FIL DE L'EAU, UTF-8
rem des deux cotes du tuyau), les verdicts RECOPIES des lignes, le
rem chrono M4, LA COLLECTE (la console COPIEE au receptacle
rem preuves-unite16\, le DEPOT-d210-unite16.txt assemble) ;
rem  LE LIVRE A L'ATELIER CHOISI (l'onglet 4-LIVRE : CHOISIR LE
rem  DOSSIER DE L'ATELIER avant TOUT LANCER - le dossier des QUATRE
rem  registres du livre recu du coffre) : la ligne M1 a livraisons.csv
rem  (le verdict RECOPIE des lignes de console) et la ligne M3 au
rem  carnet (les bornes OBSERVEES par le GUI - clic TOUT LANCER puis
rem  fin de collecte) y sont appendies DURANT le run ; defauts.csv et
rem  journal-ouverture.txt JAMAIS touches (D202 + l'ouverture scellee)
rem  ; l'atelier re-depose au coffre demeure VOTRE geste ;
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
rem  toucher defauts.csv ni journal-ouverture.txt (D202 et
rem  l'ouverture scellee) ; ecrire DEUX FOIS la ligne au livre (le
rem  doublon REFUSE nomme - le rejeu, bouton REJOUER, ne porte
rem  AUCUNE ligne) ;
rem renommer ni editer les pieces du receptacle.
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC"
rem apparait au double-clic [la marque du web] : clic droit sur CE
rem fichier, Proprietes, cochez "Debloquer" en bas, OK - puis
rem double-cliquez encore. Ce fichier descend du coffre Drive : il
rem porte la marque, comme toute piece telechargee.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - le run de l'unite 04 D210 (loupe-16 saisie x bras T) en un clic
cd /d "%~dp0"

set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent

%PY% -c "import tkinter" >nul 2>&1
if errorlevel 1 goto tkinter_absent

%PY% triade_run_unite16_d210_gui.py
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
