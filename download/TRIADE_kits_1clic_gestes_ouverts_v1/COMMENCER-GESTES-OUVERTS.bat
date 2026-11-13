@echo off
rem ============================================================================
rem COMMENCER-GESTES-OUVERTS.bat - LE MENU DES GESTES OUVERTS EN 1 CLIC
rem [l'edition des gestes ouverts, 13/11/2026 - la commande du developpeur :
rem "Fais des kits 1-clic pour les tests restants a faire et continue sur
rem les suites proposees"].
rem
rem CE QUE CE MENU EST : la carte des gestes ENCORE OUVERTS du projet - les
rem chaines fermees [kit-2 dudect temoin signe x2, kit-3 loupe vert,
rem constat-arm temoin signe] vivent aux archives du coffre /test, RIEN ici
rem ne les rejoue. Chaque geste ouvert vit en UN DOUBLE-CLIC - aucun ordre
rem impose, aucun geste obligatoire.
rem
rem CE QUE CE MENU N'EST PAS : il ne mesure rien, ne signe rien, ne depose
rem rien au coffre a votre place. Dater et signer les temoins demeure VOTRE
rem main - le renvoi des dossiers de preuves ENTIERS au coffre /test aussi
rem [dossier Drive "Triade" puis "test"].
rem ============================================================================

setlocal EnableExtensions
title TRIADE - les gestes ouverts en 1 clic
cd /d "%~dp0"

if not exist "LISEZMOI-GESTES-OUVERTS.txt" goto extraction_refusee

:menu
cls
echo ============================================================================
echo  TRIADE - LES GESTES OUVERTS - chaque geste en 1 clic, aucun ordre
echo ============================================================================
echo.
echo  LES TESTS RESTANTS DU PAQUET TERRAIN :
echo   1. LE DIAGNOSTIC MACHINE - lire le silicium, choisir la machine du
echo      geste B - le temoin nait dans diagnostic-machine.txt
echo   2. LE GESTE B SHA-NI REEL - pc-windows\kit-1-shani - la mesure
echo      avant/apres sur un silicium qui A SHA-NI - REFUS NOMME sinon
echo   3. LA VOIE 1 QEMU - le kit M7D rejoue sous le qemu-riscv64 EMBARQUE
echo      - WSL2 requis - une reproduction, jamais le metal [D149]
echo   4. LA VOIE 2 QEMU - le kit-shani sous qemu-x86_64 -cpu max - l'artefact
echo      TCG consigne tel quel - WSL2 + qemu-user requis
echo.
echo  LES GESTES DU PROJET :
echo   5. LA CAMPAGNE D204 - la console de campagne - les instruments du
echo      plan pre-enregistre : statut, calibration, chronometre, tokens
echo   6. LE SEQUESTRE D183 - la ceremonie des 5 parts a seuil 3 - la
echo      repetition generale d'abord, la ceremonie HORS-LIGNE ensuite
echo   7. LA REPLICATION - l'autotest du calculateur kappa + la grille T/X
echo.
echo  AILLEURS AU COFFRE - DEJA EN 1 CLIC, RIEN A EXTRAIRE ICI :
echo   - les preuves formelles constat-arm : l'APK du /test - le bouton
echo     envoie le zip des preuves au Drive
echo   - le temoin vitrine du kit-3 : loupe-kit-13 du /test
echo   - la ceremonie d'ere : le dossier Ceremonie du coffre Drive
echo.
echo   8. LA CARTE COMPLETE - le LISEZMOI des gestes ouverts
echo   0. QUITTER
echo.
set "CHOIX="
set /p "CHOIX=Votre choix (0-8) : "
if not defined CHOIX goto menu
if "%CHOIX%"=="1" goto diagnostic
if "%CHOIX%"=="2" goto gesteb
if "%CHOIX%"=="3" goto voie1
if "%CHOIX%"=="4" goto voie2
if "%CHOIX%"=="5" goto campagne
if "%CHOIX%"=="6" goto sequestre
if "%CHOIX%"=="7" goto replication
if "%CHOIX%"=="8" goto carte
if "%CHOIX%"=="0" goto fin
goto menu

:diagnostic
call "%~dp0DIAGNOSTIC-MACHINE.bat"
goto retour

:gesteb
call "%~dp0pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat"
goto retour

:voie1
call "%~dp0qemu-wsl2\LANCER-VOIE1-QEMU.bat"
goto retour

:voie2
call "%~dp0qemu-wsl2\LANCER-VOIE2-QEMU.bat"
goto retour

:campagne
call "%~dp0campagne-d204\LANCER-CAMPAGNE-D204.bat"
goto retour

:sequestre
call "%~dp0sequestre-d183\LANCER-SEQUESTRE-D183.bat"
goto retour

:replication
call "%~dp0replication\LANCER-REPLICATION.bat"
goto retour

:retour
cd /d "%~dp0"
echo.
echo [le geste est termine - appuyez sur une touche pour revenir au menu]
pause >nul
goto menu

:carte
cls
type LISEZMOI-GESTES-OUVERTS.txt
echo.
echo [fin de la carte - appuyez sur une touche pour revenir au menu]
pause >nul
goto menu

:extraction_refusee
echo ============================================================================
echo [REFUS NOMME] le paquet est INCOMPLET - LISEZMOI-GESTES-OUVERTS.txt
echo        est absent. Extrayez le zip COMPLET dans un dossier NEUF - les
echo        .bat doubles-cliques DANS le zip ne voient pas les pieces.
echo ============================================================================
pause
exit /b 2

:fin
endlocal
