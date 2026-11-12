@echo off
rem ============================================================================
rem RENVOYER-LE-CRASH.bat - LE COLLECTEUR DE PREUVES DU CRASH KIT-2
rem (le paquet CORRECTIF2-kit-dudect, 13/11/2026 - la suite de l'annonce du
rem  developpeur : "kit-2 crash encore au lancement").
rem
rem LE GESTE : placez ce fichier DANS pc-windows\kit-2-dudect\ (a cote de
rem LANCER-KIT-2-DUDECT.bat, dans l'extraction VERIFIEE 45/45) puis
rem DOUBLE-CLIQUEZ. Il ne mesure rien, ne corrige rien : il COLLECTE les
rem pieces du crash (D122/D189 - le crash est un RESULTAT, renvoye tel quel) :
rem   1. l'etat du dossier : les exe presents/absents (l'antivirus ?) et leur
rem      sha256 (QUEL exe vit ici : le corrige 42903257... ou un vieux ?) ;
rem   2. les artefacts du run crashe s'ils vivent (sortie-appel.txt,
rem      sortie-run.txt, temoin-dudect-BROUILLON.txt, journal-dudect-*.csv) ;
rem   3. la machine (OS, CPU, l'etat du Defender temps reel, les exclusions) ;
rem   4. L'EPREUVE DE LANCEMENT VIVE : test_appel.exe relance SOUS le
rem      collecteur (WER neutralise par compat : le code NTSTATUS vient
rem      immediat ; si un dialogue apparait malgre tout, cliquez Fermer) ;
rem   5. les EVENEMENTS Windows : Application Error 1000/1001 (le module
rem      fautif, le code d'exception, le decalage) et Defender 1116/1117/5007
rem      (les detections, les blocages, les changements de preference).
rem Tout vit dans preuves-crash-kit2\ : renvoyez le dossier ENTIER au coffre
rem /test (dossier Drive "Triade" - "test"). AUCUN Python requis.
rem ============================================================================
setlocal EnableExtensions
title TRIADE - collecteur de preuves du crash kit-2
cd /d "%~dp0"
set "CIBLE=preuves-crash-kit2"

echo ============================================================================
echo  LE COLLECTEUR DE PREUVES DU CRASH KIT-2 (aucune mesure, aucune
echo  correction : les pieces du crash, renvoyees telles quelles).
echo ============================================================================
echo.

if exist "%CIBLE%" rmdir /s /q "%CIBLE%"
mkdir "%CIBLE%" 2>nul
if not exist "%CIBLE%" goto dossier_refuse

> "%CIBLE%\RAPPORT-CRASH.txt" echo === LE RAPPORT DU COLLECTEUR DE PREUVES (kit-2) ===
>> "%CIBLE%\RAPPORT-CRASH.txt" echo Le dossier du kit : %~dp0
>> "%CIBLE%\RAPPORT-CRASH.txt" echo La date           : %DATE% %TIME% (heure locale)

rem ---- [1/6] l'etat du dossier : les pieces presentes, leurs empreintes ----
echo [1/6] l'etat du dossier (les exe presents ? leurs sha256 ?)...
dir /a > "%CIBLE%\dossier-listing.txt" 2>&1
if exist test_appel.exe goto sha_ta
> "%CIBLE%\sha-test_appel.txt" echo test_appel.exe ABSENT de ce dossier - l'antivirus l'a probablement retire (nomme, D189).
goto sha_du
:sha_ta
certutil -hashfile test_appel.exe SHA256 > "%CIBLE%\sha-test_appel.txt" 2>&1
:sha_du
if exist dudect_v150.exe goto sha_dd
> "%CIBLE%\sha-dudect_v150.txt" echo dudect_v150.exe ABSENT de ce dossier - l'antivirus l'a probablement retire (nomme, D189).
goto sha_ok
:sha_dd
certutil -hashfile dudect_v150.exe SHA256 > "%CIBLE%\sha-dudect_v150.txt" 2>&1
:sha_ok
>> "%CIBLE%\RAPPORT-CRASH.txt" echo.
>> "%CIBLE%\RAPPORT-CRASH.txt" echo LA CLE DU sha256 de test_appel.exe :
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   42903257aa9e... = LE CORRIGE correctif n.o 2 (RWX)
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   f8b8e06e...     = LE VIEUX exe du 12/11 (le mauvais dossier a couru)
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   (l'empreinte complete vit dans sha-test_appel.txt)

rem ---- [2/6] les artefacts du run crashe (s'ils vivent) ----
echo [2/6] les artefacts du run (sortie-appel, sortie-run, temoin, csv)...
set "NBARTEFACT=0"
for %%F in (sortie-appel.txt sortie-run.txt temoin-dudect-BROUILLON.txt) do if exist "%%F" copy "%%F" "%CIBLE%\" >nul 2>&1
for %%F in (journal-dudect-*.csv) do if exist "%%F" copy "%%F" "%CIBLE%\" >nul 2>&1
if exist sortie-appel.txt set "NBARTEFACT=1"
if exist sortie-run.txt set "NBARTEFACT=1"
if exist temoin-dudect-BROUILLON.txt set "NBARTEFACT=1"
>> "%CIBLE%\RAPPORT-CRASH.txt" echo.
if "%NBARTEFACT%"=="1" goto artefacts_ok
>> "%CIBLE%\RAPPORT-CRASH.txt" echo AUCUN artefact de run dans ce dossier (sortie-appel.txt absent) :
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   le lanceur n'a JAMAIS atteint l'epreuve d'appel ICI - soit le run
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   a vecu dans UN AUTRE dossier, soit la fenetre est morte avant (nomme).
goto machine
:artefacts_ok
>> "%CIBLE%\RAPPORT-CRASH.txt" echo Les artefacts du run sont copies dans ce dossier (D189).

rem ---- [3/6] la machine ----
:machine
echo [3/6] la machine (OS, CPU, Defender)...
powershell -NoProfile -Command "'OS       : ' + (Get-CimInstance Win32_OperatingSystem).Caption" >> "%CIBLE%\RAPPORT-CRASH.txt" 2>&1
powershell -NoProfile -Command "'Version  : ' + (Get-CimInstance Win32_OperatingSystem).Version" >> "%CIBLE%\RAPPORT-CRASH.txt" 2>&1
powershell -NoProfile -Command "'CPU      : ' + (Get-CimInstance Win32_Processor).Name" >> "%CIBLE%\RAPPORT-CRASH.txt" 2>&1
powershell -NoProfile -Command "'Defender : protection temps reel = ' + (Get-MpComputerStatus -ErrorAction SilentlyContinue).RealTimeProtectionEnabled" >> "%CIBLE%\RAPPORT-CRASH.txt" 2>&1
powershell -NoProfile -Command "'Exclusions Defender (chemins) : ' + ((Get-MpPreference -ErrorAction SilentlyContinue).ExclusionPath -join ' ; ')" >> "%CIBLE%\RAPPORT-CRASH.txt" 2>&1

rem ---- [4/6] L'EPREUVE DE LANCEMENT VIVE ----
echo [4/6] l'epreuve de lancement VIVE : test_appel.exe en direct...
if exist test_appel.exe goto vivre
>> "%CIBLE%\RAPPORT-CRASH.txt" echo.
>> "%CIBLE%\RAPPORT-CRASH.txt" echo EPREUVE VIVE PASSEE : test_appel.exe ABSENT - l'antivirus l'a retire.
>> "%CIBLE%\RAPPORT-CRASH.txt" echo (le dossier-listing et les evenements Defender diront le reste.)
goto evenements
:vivre
set "__COMPAT_LAYER=DisableWER"
test_appel.exe > "%CIBLE%\sortie-appel-VIVE.txt" 2>&1
set "RCLA=%errorlevel%"
set "__COMPAT_LAYER="
>> "%CIBLE%\RAPPORT-CRASH.txt" echo.
>> "%CIBLE%\RAPPORT-CRASH.txt" echo LE CODE DE SORTIE DE test_appel.exe (epreuve vive) : %RCLA%
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   0            = PAS de crash ici (le crash venait d'un autre etat/dossier)
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   -1073741819  = 0xC0000005 violation d'acces
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   -1073741795  = 0xC000001D instruction illegale
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   -1073741515  = 0xC0000135 DLL introuvable
>> "%CIBLE%\RAPPORT-CRASH.txt" echo   2            = [REFUS] nomme de l'exe (VirtualAlloc/VirtualProtect/fopen)
>> "%CIBLE%\RAPPORT-CRASH.txt" echo (la sortie complete vit dans sortie-appel-VIVE.txt)

rem ---- [5/6] les evenements Windows ----
:evenements
echo [5/6] les evenements Windows (Application Error 1000/1001, Defender)...
powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Application';Id=1000,1001} -MaxEvents 30 -ErrorAction SilentlyContinue | Format-List TimeCreated,Message" > "%CIBLE%\evenements-application.txt" 2>&1
powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-Windows Defender/Operational';Id=1116,1117,5007} -MaxEvents 25 -ErrorAction SilentlyContinue | Format-List TimeCreated,Message" > "%CIBLE%\evenements-defender.txt" 2>&1
dir "%ProgramData%\Microsoft\Windows\WER\ReportArchive" /b /o-d 2>nul | findstr /i "test_appel dudect" > "%CIBLE%\wer-rapports.txt" 2>&1
dir "%LOCALAPPDATA%\CrashDumps" /b /o-d 2>nul >> "%CIBLE%\wer-rapports.txt"

rem ---- [6/6] le bilan ----
echo [6/6] le bilan...
>> "%CIBLE%\RAPPORT-CRASH.txt" echo.
>> "%CIBLE%\RAPPORT-CRASH.txt" echo === LA FIN DU RAPPORT - renvoyez le dossier preuves-crash-kit2 ENTIER
>> "%CIBLE%\RAPPORT-CRASH.txt" echo au coffre /test (dossier Drive "Triade" - "test") ===
echo.
echo ============================================================================
echo  LE COLLECTEUR A FINI : le dossier preuves-crash-kit2\ vit ici :
echo    %~dp0%CIBLE%
echo  RENVOYEZ-LE ENTIER au coffre /test (dossier Drive "Triade" - "test").
echo  Le labo recoupe sur pieces : le code de sortie, le module fautif,
echo  les detections Defender diront la cause nommee - jamais de correctif
echo  aveugle (D189).
echo ============================================================================
start "" explorer "%~dp0%CIBLE%"
pause
exit /b 0

:dossier_refuse
echo.
echo [REFUS] impossible de creer le dossier preuves-crash-kit2 ici -
echo         lancez ce collecteur DEPUIS pc-windows\kit-2-dudect\ (extraction
echo         complete, dossier inscriptible).
pause
exit /b 2
