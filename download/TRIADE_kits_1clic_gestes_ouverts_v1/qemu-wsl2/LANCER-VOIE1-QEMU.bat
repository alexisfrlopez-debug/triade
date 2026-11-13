@echo off
rem ============================================================================
rem LANCER-VOIE1-QEMU.bat - LA VOIE 1 QEMU EN 1 CLIC [l'edition des gestes
rem ouverts, 13/11/2026 - la commande : "Fais des kits 1-clic pour les tests
rem restants a faire et continue sur les suites proposees"].
rem
rem CE QUE CE LANCEUR FAIT : il trouve wsl.exe, traduit le chemin du kit par
rem wslpath, puis lance le lanceur OFFICIEL lancer-voie1-m7d.sh - INTACT,
rem celui du paquet multimachines - sous votre WSL2. Le kit M7D est
rem AUTONOME : le qemu-riscv64 STATIQUE est embarque - aucun paquet a
rem installer, aucun reseau, aucun root. Python 3 dans WSL2 suffit [le
rem lanceur officiel tente meme de l'installer si sudo vit sans mot de
rem passe].
rem
rem LA FRONTIERE NOMMEE [D149, elle demeure] : c'est une REPRODUCTION de la
rem preuve M7 sous emulation TCG - jamais le metal. La question silicium
rem [fence.i sur une VRAIE carte RV64] reste ouverte.
rem
rem CE QUI RESTE A VOTRE MAIN : dater et signer le temoin de votre main,
rem puis renvoyer le dossier preuves-m7 ENTIER au coffre /test [dossier
rem Drive "Triade" puis "test"].
rem ============================================================================

setlocal EnableExtensions
title TRIADE - la voie 1 QEMU - kit M7D rejoue sous qemu-riscv64 embarque
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LA VOIE 1 QEMU - LE KIT M7D REJOUE : la bascule fence.i, l'ISA RISC-V,
echo  l'adversaire DEP, les refus nommes - sous le qemu-riscv64 EMBARQUE.
echo  La reserve instrumentale D149 DEMEURE : une reproduction, jamais le
echo  metal.
echo ============================================================================
echo.

rem ---- wsl.exe [la voie exige WSL2] ----
where wsl.exe >nul 2>&1
if errorlevel 1 goto wsl_absent
echo [wsl] wsl.exe present.

rem ---- la traduction du chemin [wslpath] ----
echo [chemin] traduction du dossier par wslpath...
set "SH="
for /f "usebackq delims=" %%P in (`wsl.exe wslpath "%~dp0lancer-voie1-m7d.sh"`) do set "SH=%%P"
if not defined SH goto chemin_refuse
echo       le lanceur officiel vit a : %SH%

rem ---- LE RUN : le lanceur officiel INTACT, sous WSL2 ----
echo.
echo [run] le lanceur officiel - environ une minute, ne fermez pas...
echo.
wsl.exe bash "%SH%"
set "RC=%errorlevel%"
echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LA VOIE 1 EST VECUE - code 0.
) else (
    echo  LA VOIE 1 S'EST TERMINEE SUR LE CODE %RC% - un ecart nomme est un
    echo  RESULTAT [D189] : renvoyez le dossier TEL QUEL, le labo recoupe.
)
echo  Les preuves vivrent dans preuves-m7 [du dossier kit-m7d].
echo  A VOTRE MAIN : datez et signez le temoin de votre main, puis renvoyez
echo  le dossier ENTIER au coffre /test [dossier Drive "Triade" puis "test"].
echo ============================================================================
endlocal & exit /b %RC%

:wsl_absent
echo.
echo [REFUS NOMME] wsl.exe est ABSENT - la voie 1 exige WSL2 sur Windows 10
echo        ou 11. Pour l'installer : une invite administrateur puis
echo        wsl --install
echo        puis redemarrez, ouvrez Ubuntu une premiere fois, revenez
echo        double-cliquer. La voie OFFICIELLE sans WSL2 n'existe pas -
echo        jamais maquille.
pause
exit /b 2

:chemin_refuse
echo.
echo [REFUS NOMME] la traduction du chemin par wslpath a echoue - ouvrez
echo        WSL2 vous-meme et vivez le geste officiel :
echo        bash lancer-voie1-m7d.sh
echo        depuis le dossier qemu-wsl2 du paquet. Renvoyez l'ecran TEL QUEL
echo        [D122], le labo recoupe et corrige.
pause
exit /b 2
