@echo off
rem ============================================================================
rem COMMENCER-ICI.bat - LA PORTE D'ENTREE DU PAQUET MULTIMACHINES (l'edition
rem AUTOMATISEE, 12/11/2026 - la commande du developpeur : 'je veux que
rem l'utilisation soit la plus simple possible, en automatisant au maximum').
rem
rem UN SEUL GESTE : DOUBLE-CLIQUEZ CE FICHIER. Le menu ouvre chaque kit par
rem son lanceur ; chaque lanceur verifie les pieces, trouve les outils,
rem compile SI un compilateur vit (sinon les exe precompiles livres), vit
rem le run et vous dit OU sont les preuves. Chaque kit porte SON LISEZMOI :
rem le lanceur fait les gestes, le LISEZMOI demeure la reference.
rem
rem RAPPEL DU GESTE GENERAL (D99) : vivez chaque kit dans un dossier NEUF,
rem ne melangez jamais les runs ; datez et signez les temoins DE VOTRE MAIN ;
rem renvoyez les dossiers de preuves ENTIERS au coffre /test (dossier Drive
rem 'Triade'). Le labo recoupe sur pieces : jamais avant le run, jamais sans
rem pieces.
rem ============================================================================

setlocal EnableExtensions
title TRIADE - le paquet multimachines AUTO (v0.15.0, edition du 12/11/2026)
cd /d "%~dp0"

:menu
cls
echo ============================================================================
echo   LE PAQUET MULTIMACHINES TRIADE v0.15.0 - L'EDITION AUTOMATISEE
echo   (PC Windows 10 et 11 - telephone ARM - QEMU/WSL2 - la carte complete
echo    vit dans LISEZMOI-MULTIMACHINES.txt)
echo ============================================================================
echo.
echo   VOS MACHINES WINDOWS :
echo     1  LE KIT 1 SHANI     la mesure avant/apres SHA-NI - REFUSE SEUL et
echo                           honnetement si le silicium n'a pas SHA-NI
echo                           (c'est un RESULTAT). Python requis, rien a
echo                           compiler.
echo     2  LE KIT 2 DUDECT    LA mesure temps reel des familles crypto.
echo                           AUCUN Python requis : le lanceur compile tout
echo                           seul si un compilateur vit (sinon les exe
echo                           precompiles livres courent).
echo     3  LE KIT 3 LOUPE     le scenario integral T0-T7+S0 pour la machine
echo                           TIERSCE (Windows 11 de preference - la machine
echo                           qui n'a JAMAIS servi au developpement).
echo                           Python 64 bits requis.
echo.
echo   QEMU SOUS WSL2 (si WSL2 vit sur cette machine - sinon lisez
echo   qemu-wsl2\LISEZMOI-qemu.txt) :
echo     4  LA VOIE 1 : le kit M7D rejoue sous qemu-riscv64 (AUTONOME :
echo                           le qemu STATIQUE est embarque, rien a installer).
echo     5  LA VOIE 2 : le kit shani sous qemu-x86_64 -cpu max (l'emulation
echo                           SHA-NI ; demande qemu-user, le lanceur vous
echo                           dit la commande exacte s'il manque).
echo.
echo   LE TELEPHONE ARM (Termux) : copiez telephone-arm\kit-constat-arm\ au
echo   telephone puis tapez :  bash lancer-kit-constat-arm.sh
echo   (le lanceur installe Python tout seul s'il manque - LISEZMOI-constat-arm.txt)
echo.
echo     0  QUITTER
echo.
set "CHOIX="
set /p "CHOIX=Votre choix (0-5) : "
if not defined CHOIX goto menu
if "%CHOIX%"=="1" goto kit1
if "%CHOIX%"=="2" goto kit2
if "%CHOIX%"=="3" goto kit3
if "%CHOIX%"=="4" goto voie1
if "%CHOIX%"=="5" goto voie2
if "%CHOIX%"=="0" goto fin
goto menu

:kit1
call "%~dp0pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat"
goto menu

:kit2
call "%~dp0pc-windows\kit-2-dudect\LANCER-KIT-2-DUDECT.bat"
goto menu

:kit3
call "%~dp0pc-windows\kit-3-terrain-tiers-loupe\LANCER-KIT-3-LOUPE.bat"
goto menu

:voie1
where wsl.exe >nul 2>&1 || goto pas_wsl
echo.
echo [wsl] lancement de la voie 1 (kit M7D) sous WSL2...
wsl.exe -e bash -c "cd \"$(wslpath -u '%~dp0qemu-wsl2')\" && bash lancer-voie1-m7d.sh"
echo.
echo [wsl] la voie 1 est terminee - les preuves vivent dans qemu-wsl2\kit-m7d\preuves-m7\
echo        (datez, signez, renvoyez le dossier ENTIER au coffre /test).
pause
goto menu

:voie2
where wsl.exe >nul 2>&1 || goto pas_wsl
echo.
echo [wsl] lancement de la voie 2 (kit shani emulate) sous WSL2...
wsl.exe -e bash -c "cd \"$(wslpath -u '%~dp0qemu-wsl2')\" && bash lancer-voie2-shani.sh"
echo.
echo [wsl] la voie 2 est terminee - les preuves vivent dans pc-windows\kit-1-shani\preuves-shani\
echo        (souvenez-vous : c'est une EMULATION, jamais le silicium - datez et
echo        signez 'run sous qemu-x86_64 -cpu max, EMULATION').
pause
goto menu

:pas_wsl
echo.
echo [REFUS nomme] wsl.exe est INTROUVABLE : WSL2 ne vit pas sur cette machine
echo        (ou pas dans le PATH). Installez-le si besoin ^(wsl --install^), ou
echo        lisez qemu-wsl2\LISEZMOI-qemu.txt : les DEUX commandes bash y sont.
pause
goto menu

:fin
endlocal
exit /b 0
