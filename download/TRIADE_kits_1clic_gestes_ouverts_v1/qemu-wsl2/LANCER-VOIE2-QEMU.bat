@echo off
rem ============================================================================
rem LANCER-VOIE2-QEMU.bat - LA VOIE 2 QEMU EN 1 CLIC [l'edition des gestes
rem ouverts, 13/11/2026 - la commande : "Fais des kits 1-clic pour les tests
rem restants a faire et continue sur les suites proposees"].
rem
rem CE QUE CE LANCEUR FAIT : il trouve wsl.exe, traduit le chemin du kit par
rem wslpath, puis lance le lanceur OFFICIEL lancer-voie2-shani.sh - INTACT,
rem celui du paquet multimachines - sous votre WSL2. Ce lanceur officiel
rem trouve qemu-x86_64 [il tente de l'installer par apt si sudo vit sans
rem mot de passe - sinon il donne LA commande exacte], puis vit le kit-1
rem shani EXACT sous emulation : qemu-x86_64 -cpu max presente SHA-NI au
rem CPUID.
rem
rem LA FRONTIERE NOMMEE : cette voie EXERCE la chaine [le refus ne peut
rem plus exister - qemu presente SHA-NI], elle NE MESURE PAS : le rapport
rem rendu est l'ARTEFACT TCG [le labo l'a vecu : 0,19x - chaque
rem sha256rnds2 traduit en dizaines d'operations hotes]. La mesure
rem avant/apres n'a de sens que sur le VRAI silicium [le geste B demeure].
rem
rem CE QUI RESTE A VOTRE MAIN : dater et signer le temoin en ecrivant sous
rem votre main "run sous qemu-x86_64 -cpu max, EMULATION, pas le silicium",
rem puis renvoyer le dossier preuves-shani ENTIER au coffre /test.
rem ============================================================================

setlocal EnableExtensions
title TRIADE - la voie 2 QEMU - kit-shani sous qemu-x86_64 -cpu max
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LA VOIE 2 QEMU - LE KIT-SHANI SOUS EMULATION : qemu-x86_64 -cpu max
echo  presente SHA-NI au CPUID - la chaine complete sans le refus. Le
echo  rapport rendu est l'ARTEFACT TCG, consigne TEL QUEL - jamais une
echo  verite de silicium.
echo ============================================================================
echo.

rem ---- wsl.exe [la voie exige WSL2] ----
where wsl.exe >nul 2>&1
if errorlevel 1 goto wsl_absent
echo [wsl] wsl.exe present.

rem ---- la traduction du chemin [wslpath] ----
echo [chemin] traduction du dossier par wslpath...
set "SH="
for /f "usebackq delims=" %%P in (`wsl.exe wslpath "%~dp0lancer-voie2-shani.sh"`) do set "SH=%%P"
if not defined SH goto chemin_refuse
echo       le lanceur officiel vit a : %SH%

rem ---- LE RUN : le lanceur officiel INTACT, sous WSL2 ----
echo.
echo [run] le kit-1-shani sous emulation - une a deux minutes...
echo.
wsl.exe bash "%SH%"
set "RC=%errorlevel%"
echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LA VOIE 2 EST VECUE - code 0.
) else (
    echo  LA VOIE 2 S'EST TERMINEE SUR LE CODE %RC% - un ecart nomme est un
    echo  RESULTAT [D189] : renvoyez le dossier TEL QUEL, le labo recoupe.
)
echo  Les preuves vivrent dans preuves-shani [du dossier kit-1-shani].
echo  A VOTRE MAIN : datez et signez le temoin en ecrivant sous votre main :
echo    run sous qemu-x86_64 -cpu max, EMULATION, pas le silicium
echo  Le rapport rendu [probablement sous 1] est l'artefact TCG : consignez-le
echo  tel quel. Renvoyez le dossier ENTIER au coffre /test.
echo ============================================================================
endlocal & exit /b %RC%

:wsl_absent
echo.
echo [REFUS NOMME] wsl.exe est ABSENT - la voie 2 exige WSL2 sur Windows 10
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
echo        bash lancer-voie2-shani.sh
echo        depuis le dossier qemu-wsl2 du paquet. Renvoyez l'ecran TEL QUEL
echo        [D122], le labo recoupe et corrige.
pause
exit /b 2
