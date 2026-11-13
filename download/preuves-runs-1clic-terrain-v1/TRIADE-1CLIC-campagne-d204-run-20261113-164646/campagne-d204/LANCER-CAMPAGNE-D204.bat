@echo off
rem ============================================================================
rem LANCER-CAMPAGNE-D204.bat - LA CONSOLE DE CAMPAGNE EN 1 CLIC
rem [l'edition des gestes ouverts, 13/11/2026].
rem
rem LA CAMPAGNE DE COMPARAISON DES WORKFLOWS - le plan PRE-ENREGISTRE et
rem VERROUILLE [sha256 a78caf8c... consigne a D204 AVANT toute mesure] :
rem bras T la discipline TRIADE contre bras C le flux standard C+gcc, les
memes taches, les quatre metriques [defauts, tokens, temps humain, temps
de verification]. AUCUNE mesure n'existe encore - aucune n'est fabriquee.
rem
rem CE QUE CETTE CONSOLE FAIT : le STATUT des pieces, la CALIBRATION du
rem chronometre [la preuve d'horloge - un dry-run, jamais une mesure], le
rem CHRONOMETRAGE d'une commande de verification, le RECAPITULATIF des
rem tokens du journal. Les instruments sont INTACTS, ceux du depot.
rem
rem OU NAIT LE JOURNAL : a preuves_v150\comparaison_resultats\ du present
rem paquet - a la PREMIERE mesure instrumentee seulement [CA1 : le dossier
rem des resultats ne nait que d'une mesure reelle].
rem
rem LA CAMPAGNE ELLE-MEME : un travail de fond aux DEUX bras - le plan fait
rem foi. Le verificateur verifier_comparaison_v150.py verifie les pieces DU
rem LABORATOIRE [le verrou D204, le dry-run, l'audit du plan] - il vit au
rem depot avec ses chemins du labo, il n'est PAS embarque ici : sa course
rem VERT est consignee [l'Entree 239].
rem ============================================================================

setlocal EnableExtensions
title TRIADE - la campagne D204 - la console de campagne
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
echo  LA CAMPAGNE D204 - LA CONSOLE - le plan pre-enregistre fait foi
echo  [bras T TRIADE contre bras C C+gcc - les memes taches, les quatre
echo  metriques - AUCUNE mesure n'existe encore]
echo ============================================================================
echo.
echo   1. LE STATUT DU KIT - les pieces presentes, le journal
echo   2. LA CALIBRATION DU CHRONOMETRE - la preuve d'horloge [2 s] - un
echo      dry-run, jamais une mesure de campagne
echo   3. CHRONOMETRER UNE COMMANDE - le temps mural d'une verification
echo      [une mesure : le bras T ou C exige]
echo   4. LE RECAPITULATIF DES TOKENS - le journal, bras par bras, phase
echo      par phase - 100 pour cent lus du log d'usage
echo   5. LE PLAN PRE-ENREGISTRE - l'ouvrir
echo   6. LES GABARITS - ou vit quoi [carnet, livraisons, defauts]
echo   7. LE LISEZMOI de la campagne
echo   0. RETOUR
echo.
set "CHOIX="
set /p "CHOIX=Votre choix (0-8) : "
if not defined CHOIX goto menu
if "%CHOIX%"=="1" goto statut
if "%CHOIX%"=="2" goto calibration
if "%CHOIX%"=="3" goto chrono
if "%CHOIX%"=="4" goto tokens
if "%CHOIX%"=="5" goto plan
if "%CHOIX%"=="6" goto gabarits
if "%CHOIX%"=="7" goto lisezmoi
if "%CHOIX%"=="0" goto fin
goto menu

:statut
echo.
echo [statut] les pieces du kit :
if exist "PLAN_PREREGISTRE_COMPARAISON.md" (echo    PLAN_PREREGISTRE_COMPARAISON.md : PRESENT) else (echo    PLAN_PREREGISTRE_COMPARAISON.md : ABSENT - extrayez le zip COMPLET)
if exist "LISEZMOI-comparaison.txt" (echo    LISEZMOI-comparaison.txt : PRESENT) else (echo    LISEZMOI-comparaison.txt : ABSENT)
if exist "compter_tokens.py" (echo    compter_tokens.py : PRESENT) else (echo    compter_tokens.py : ABSENT)
if exist "chronometre_verification.py" (echo    chronometre_verification.py : PRESENT) else (echo    chronometre_verification.py : ABSENT)
if exist "carnet_temps_humain.csv" (echo    carnet_temps_humain.csv : PRESENT) else (echo    carnet_temps_humain.csv : ABSENT)
if exist "livraisons.csv" (echo    livraisons.csv : PRESENT) else (echo    livraisons.csv : ABSENT)
if exist "defauts.csv" (echo    defauts.csv : PRESENT) else (echo    defauts.csv : ABSENT)
if exist "..\preuves_v150\comparaison_resultats\journal_tokens.jsonl" (echo    le journal des tokens : IL VIT - la campagne est ENGAGEE) else (echo    le journal des tokens : PAS ENCORE - il naitra de la premiere mesure [CA1])
echo.
echo [verrou] l'empreinte du plan :
certutil -hashfile "PLAN_PREREGISTRE_COMPARAISON.md" SHA256 > "%TEMP%\triade-plan-d204.txt" 2>&1
findstr /i "a78caf8c0cb9498446a91d18d0f8a02ee16b6893d4fe4ce49843397f30240255" "%TEMP%\triade-plan-d204.txt" >nul
if errorlevel 1 (echo    le plan diverge de l'empreinte consignee a D204 - REFUS, la campagne ne vit pas sur un plan retouche) else (echo    le plan == l'empreinte consignee a D204 - le verrou tient)
echo.
pause
goto menu

:calibration
echo.
echo [calibration] %PY% chronometre_verification.py --calibration 2.00
echo.
%PY% chronometre_verification.py --calibration 2.00
set "RC=%errorlevel%"
echo.
pause
goto menu

:chrono
echo.
echo  CHRONOMETRER UNE COMMANDE - une mesure de campagne : le bras est exige.
echo  La commande : par exemple  py kit-loupe\verifier.bat  ou toute commande
echo  de la liste M4 du plan. Le label : court, sans espaces - par exemple
echo  build-loupe-01.
echo.
set "BRAS="
set "CMD="
set "LABEL="
set /p "BRAS=Le bras [T ou C] : "
set /p "CMD=La commande a chronometrer : "
set /p "LABEL=Le label court : "
if not defined BRAS goto saisie_refusee
if not defined CMD goto saisie_refusee
if not defined LABEL goto saisie_refusee
echo.
echo [chrono] %PY% chronometre_verification.py --command "%CMD%" --label %LABEL% --bras %BRAS%
echo.
%PY% chronometre_verification.py --command "%CMD%" --label "%LABEL%" --bras %BRAS%
set "RC=%errorlevel%"
echo.
echo  La ligne vit au journal des verifications [preuves_v150 du paquet].
pause
goto menu

:tokens
echo.
if not exist "..\preuves_v150\comparaison_resultats\journal_tokens.jsonl" goto journal_absent
echo [tokens] %PY% compter_tokens.py --total
echo.
%PY% compter_tokens.py --total
set "RC=%errorlevel%"
echo.
pause
goto menu

:plan
start notepad "PLAN_PREREGISTRE_COMPARAISON.md"
goto menu

:gabarits
start notepad "carnet_temps_humain.csv"
start notepad "livraisons.csv"
start notepad "defauts.csv"
echo  LES TROIS GABARITS SONT OUVERTS au bloc-notes.
echo  Le carnet se remplit AU GESTE - jamais reconstruit. Les livraisons et
echo  les defauts : une ligne par run terrain, la regle D202 au commentaire.
echo  Les originaux demeurent - travaillez sur des COPIES datees.
pause
goto menu

:lisezmoi
cls
type "LISEZMOI-comparaison.txt"
echo.
echo [fin du LISEZMOI - appuyez sur une touche pour revenir au menu]
pause >nul
goto menu

:journal_absent
echo.
echo [REFUS NOMME] le journal des tokens N'EXISTE PAS ENCORE - il nait a la
echo        premiere mesure instrumentee [CA1 : le dossier des resultats ne
echo        nait que d'une mesure reelle]. La campagne commence aux bras.
pause
goto menu

:saisie_refusee
echo.
echo [REFUS NOMME] la saisie est incomplete - le bras, la commande et le
echo        label, tous les trois, ou rien.
pause
goto menu

:python_absent
echo.
echo [REFUS NOMME] Python 3 est ABSENT - les instruments en exigent un.
echo        https://www.python.org - cochez Add to PATH.
pause
exit /b 2

:fin
endlocal
