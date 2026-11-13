@echo off
rem ============================================================================
rem LANCER-SEQUESTRE-D183.bat - LA CEREMONIE DE SEQUESTRE EN 1 CLIC
rem [l'edition des gestes ouverts, 13/11/2026].
rem
rem CE QUE CE LANCEUR FAIT : il trouve Python, puis lance l'OUTIL DU
rem LABORATOIRE INTACT [sequestre_d183.py - le partage CF2 D120 TEL QUEL,
rem GF 2 puissance 8] dans ses TROIS gestes : la repetition generale
rem [l'autotest - VERT exige], le decoupage [la ceremonie - VOTRE phrase,
rem 5 parts a seuil 3], la preuve de reconstitution a froid.
rem
rem LA FRONTIERE NOMMEE : la CEREMONIE se vit a VOTRE machine HORS-LIGNE -
rem jamais au bac a sable, jamais en ligne [D87, D183]. La phrase ne
rem traverse JAMAIS ce lanceur : il passe le CHEMIN du fichier a l'outil,
rem rien d'autre. L'outil REFUSE de supprimer quoi que ce soit - le retrait
rem de la phrase en clair est un geste humain, liste, jamais automatise.
rem
rem Les pieces : v06\coffre_cf2.py [l'instrument D120] + le kit
rem scripts\kit_ceremonie_d183\ - INTACTS, ceux du depot. Le LISEZMOI pas
rem a pas vit a cote de l'outil.
rem ============================================================================

setlocal EnableExtensions
title TRIADE - le sequestre D183 - la ceremonie des 5 parts a seuil 3
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
echo  LE SEQUESTRE D183 - 5 PARTS A SEUIL 3 [le partage CF2 D120 tel quel]
echo  L'outil du laboratoire INTACT - la ceremonie est a VOTRE main : elle
echo  se vit a une machine HORS-LIGNE, la phrase ne traverse jamais ce
echo  lanceur - seul son CHEMIN passe.
echo  NOTE : l'instrument CF2 exige les paquets pynacl et cryptography -
echo  le geste  pip install pynacl cryptography  se vit AVANT la mise
echo  hors-ligne - l'outil refuse de courir sans eux, fail-closed nomme.
echo ============================================================================
echo.
echo   1. LA REPETITION GENERALE - l'autotest de l'outil - VERT exige
echo      [la preuve a froid : les 10 combinaisons de 3 parts
echo      reconstituent exactement, les 10 paires sous le seuil rendent
echo      un dechet - l'information-theorique en acte]
echo   2. LE DECOUPAGE - LA CEREMONIE - votre fichier phrase vers 5 parts
echo      [HORS-LIGNE : lisez la phrase vous-meme, jamais copiee en ligne]
echo   3. LA PREUVE DE RECONSTITUTION A FROID - 3 parts vers la phrase
echo      [AVANT tout retrait de la phrase en clair - D183]
echo   4. LE LISEZMOI pas a pas - la ceremonie complete
echo   0. RETOUR
echo.
set "CHOIX="
set /p "CHOIX=Votre choix (0-4) : "
if not defined CHOIX goto menu
if "%CHOIX%"=="1" goto autotest
if "%CHOIX%"=="2" goto ceremonie
if "%CHOIX%"=="3" goto reconstituer
if "%CHOIX%"=="4" goto lisezmoi
if "%CHOIX%"=="0" goto fin
goto menu

:autotest
echo.
echo [autotest] %PY% scripts\kit_ceremonie_d183\sequestre_d183.py --autotest
echo.
%PY% "scripts\kit_ceremonie_d183\sequestre_d183.py" --autotest
set "RC=%errorlevel%"
echo.
if "%RC%"=="0" (echo  L'AUTOTEST EST VERT - l'outil est prouve a froid.) else (echo  L'AUTOTEST EST ROUGE - code %RC% : renvoyez l'ecran TEL QUEL [D122].)
pause
goto menu

:ceremonie
echo.
echo  LE DECOUPAGE - LA CEREMONIE [a votre machine HORS-LIGNE].
echo  Le fichier phrase : par exemple PHRASE-CONTROLE-COFFRE.txt telecharge
echo  au coffre Drive puis copie a la machine hors-ligne - JAMAIS lu en
echo  ligne. Les parts part-1.txt a part-5.txt et le manifeste naissent
echo  dans le dossier de l'outil - une part par media, SEPAREMENT.
echo.
set "FICHIER="
set /p "FICHIER=Le chemin du fichier phrase : "
if not defined FICHIER goto saisie_refusee
if not exist "%FICHIER%" goto fichier_absent
echo.
echo [ceremonie] %PY% scripts\kit_ceremonie_d183\sequestre_d183.py --ceremonie "%FICHIER%"
echo.
%PY% "scripts\kit_ceremonie_d183\sequestre_d183.py" --ceremonie "%FICHIER%"
set "RC=%errorlevel%"
echo.
echo  Les parts et le manifeste naissent dans scripts\kit_ceremonie_d183\
echo  A VOTRE MAIN ensuite : la repartition des cinq medias - au moins DEUX
echo  hors nuage - les empreintes recoupees au manifeste, puis la preuve de
echo  reconstitution a froid AVANT tout retrait [le choix 3].
pause
goto menu

:reconstituer
echo.
echo  LA PREUVE DE RECONSTITUTION A FROID - trois parts suffisent.
echo  Donnez les CHEMINS de trois de vos cinq parts - la phrase reconstituee
echo  ne s'affiche pas : l'outil la compare au fichier attendu si vous le
echo  donnez, sinon il ecrit la phrase reconstituee a cote des parts.
echo.
set "P1="
set "P2="
set "P3="
set /p "P1=La part 1 : "
set /p "P2=La part 2 : "
set /p "P3=La part 3 : "
if not defined P1 goto saisie_refusee
if not defined P2 goto saisie_refusee
if not defined P3 goto saisie_refusee
if not exist "%P1%" goto fichier_absent
if not exist "%P2%" goto fichier_absent
if not exist "%P3%" goto fichier_absent
echo.
echo [reconstituer] %PY% scripts\kit_ceremonie_d183\sequestre_d183.py --reconstituer
echo.
%PY% "scripts\kit_ceremonie_d183\sequestre_d183.py" --reconstituer "%P1%" "%P2%" "%P3%"
set "RC=%errorlevel%"
echo.
pause
goto menu

:lisezmoi
cls
type "scripts\kit_ceremonie_d183\LISEZMOI-ceremonie-D183.txt"
echo.
echo [fin du LISEZMOI - appuyez sur une touche pour revenir au menu]
pause >nul
goto menu

:saisie_refusee
echo.
echo [REFUS NOMME] la saisie est vide - le geste ne vit pas a moitie.
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
echo [REFUS NOMME] Python 3 est ABSENT - l'outil en exige un [le LISEZMOI
echo        de la ceremonie le dit : une machine propre hors-ligne avec
echo        python3]. Installez-le puis revenez.
echo        https://www.python.org - cochez Add to PATH.
pause
exit /b 2

:fin
endlocal
