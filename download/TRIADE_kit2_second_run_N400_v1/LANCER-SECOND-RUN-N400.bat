@echo off
rem ============================================================================
rem LANCER-SECOND-RUN-N400.bat - LE SECOND RUN DU KIT-2 A N=400 EN 1 CLIC
rem (la suite approuvee du 13/11/2026 - la parole du developpeur : "ok pour
rem la suite proposee" - l'Entree 264 du journal : un second run a N plus
rem grand consoliderait tls13-13 [t=5.19, la limite n'est pas loin] et
rem tls13-17 [t=3.11] sans jamais effacer le premier temoin signe).
rem
rem CE QUE CE LANCEUR FAIT : il TROUVE l'exe 1-clic v2 [son propre dossier,
rem Telechargements, Bureau - OneDrive compris], RECOUPE son sha256 par
rem certutil contre l'empreinte consignee au laboratoire [fail-closed : la
rem v1 est REFUSEE NOMMEE - la ligne 55 y vit encore, seul l'exe portant
rem l'edition CORRECTIF3 peut courir le second run], PUIS LE LANCE AVEC 400.
rem L'exe fait TOUT le reste : re-extraction du kit, re-recoup des 10 pieces
rem sha256, l'epreuve d'appel FIPS abc, LE RUN N=400, le zip des preuves au
rem Bureau, l'explorateur et le coffre /test ouverts.
rem
rem CE QUE CE LANCEUR N'EST PAS : il ne porte AUCUNE piece, ne mesure rien,
rem ne modifie JAMAIS l'exe - il cherche, il recoupe, il lance. Le premier
rem temoin signe n'est JAMAIS efface [D99 : chaque run part aux archives
rem horodatees, chaque temoin compte].
rem ============================================================================

setlocal EnableExtensions
title TRIADE - le second run du kit-2 a N=400 - la suite approuvee
set "RC=2"

echo ============================================================================
echo  TRIADE - LE SECOND RUN DU KIT-2 A N=400 - LA SUITE APPROUVEE
echo  Il consolide tls13-13 [t=5.19, la limite n'est pas loin] et tls13-17
echo  [t=3.11] - SANS JAMAIS effacer le premier temoin signe : chaque run
echo  part aux archives horodatees, chaque temoin compte.
echo ============================================================================
echo.
echo [1/3] LA RECHERCHE de l'exe 1-clic v2...
set "EXE="
set "TROUVE_V1="
call :chercher "%~dp0"
if defined EXE goto trouve
call :chercher "%USERPROFILE%\Downloads\"
if defined EXE goto trouve
call :chercher "%USERPROFILE%\Desktop\"
if defined EXE goto trouve
call :chercher "%USERPROFILE%\OneDrive\Desktop\"
if defined EXE goto trouve
goto absent

:trouve
echo       trouve : %EXE%
echo.
echo [2/3] LE RECOUP sha256 de l'exe - certutil, fail-closed...
certutil -hashfile "%EXE%" SHA256 > "%TEMP%\triade-second-run.txt" 2>&1
findstr /i "e6752c5826e3c4716403508e81a0f959506ad833fb268895a4b7f0c727a066b0" "%TEMP%\triade-second-run.txt" >nul
if errorlevel 1 goto mauvaise_empreinte
echo       INTACTE : l'exe v2 du laboratoire [e6752c58...] - l'edition
echo       CORRECTIF3, celle du run vecu du 13/11.
echo.
echo [3/3] LE RUN - l'exe v2 lance avec N=400 - la mesure prend des minutes.
echo       La console du kit suivra ici meme. Puis le zip des preuves naitra
echo       sur le Bureau, l'explorateur et le coffre /test s'ouvriront.
echo.
"%EXE%" 400
set "RC=%errorlevel%"
echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LE SECOND RUN EST VECU - code 0.
) else (
    echo  LE RUN S'EST TERMINE SUR LE CODE %RC% - un ecart nomme est un
    echo  RESULTAT [D189] : renvoyez le zip TEL QUEL, le labo recoupe.
)
echo  LE GESTE QUI SUIT - le votre :
echo   1. DEPOSEZ le zip preuves-kit2-dudect-*.zip au coffre Drive "Triade"
echo      puis "test" - la fenetre du navigateur est ouverte par l'exe.
echo   2. LE TEMOIN : datez et signez de votre main le temoin du second run
echo      [comme au premier : "fait le ..." puis votre nom] - puis deposez
echo      le dossier entier au coffre /test.
echo  Le premier temoin signe n'est JAMAIS efface - chaque temoin compte.
echo ============================================================================
pause
exit /b %RC%

:absent
echo       AUCUN exe 1-clic v2 trouve.
if defined TROUVE_V1 (
    echo       [nomme] l'exe v1 vit ici : %TROUVE_V1%
    echo       La v1 ne peut PAS courir le second run - la ligne 55 du
    echo       lanceur y vit encore [l'Entree 259 du journal].
)
echo.
echo [REFUS nomme] RIEN ne court.
echo   CONDUITE : telechargez TRIADE_kit2_exe_1clic_v2.zip au coffre Drive
echo   "Triade" puis "test", extrayez-le, placez CE lanceur dans le meme
echo   dossier que l'exe - puis double-cliquez a nouveau.
pause
exit /b 2

:mauvaise_empreinte
echo.
echo [REFUS nomme] l'exe trouve n'est PAS l'exe v2 du laboratoire.
findstr /i "9d2ccc91ba570681861eabbb77bf8f967c634747e03dacbd4ccd65afd303153d" "%TEMP%\triade-second-run.txt" >nul
if not errorlevel 1 (
    echo   C'est l'exe v1 [9d2ccc91...] - l'edition CORRECTIF2 : la ligne 55
    echo   du lanceur y vit ENCORE, elle tuerait le run [l'Entree 259].
    echo   Seul l'exe v2 [e6752c58...] porte l'edition CORRECTIF3.
) else (
    echo   Son sha256 diverge de l'empreinte consignee [e6752c58...].
    echo   Un octet change - RIEN ne court.
)
echo   CONDUITE : telechargez TRIADE_kit2_exe_1clic_v2.zip au coffre Drive
echo   "Triade" puis "test", extrayez-le, placez CE lanceur dans le meme
echo   dossier que l'exe - puis double-cliquez a nouveau.
pause
exit /b 2

:chercher
rem %1 = le dossier ou chercher [avec antislash final]
if exist "%~1TRIADE-kit2-dudect-1clic-v2.exe" set "EXE=%~1TRIADE-kit2-dudect-1clic-v2.exe"
if not defined EXE if exist "%~1TRIADE-kit2-dudect-1clic.exe" set "TROUVE_V1=%~1TRIADE-kit2-dudect-1clic.exe"
goto :eof
