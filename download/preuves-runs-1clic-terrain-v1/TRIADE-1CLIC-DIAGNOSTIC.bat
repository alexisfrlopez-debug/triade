@echo off
rem ============================================================================
rem TRIADE-1CLIC-DIAGNOSTIC.bat - LE DIAGNOSTIC DE LA MACHINE EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 3 pieces du test [celles du paquet
rem TRIADE_kits_1clic_gestes_ouverts_v1 du labo, recoupees a l'assemblage] :
rem   1. il fait naitre le dossier de run NEUF, date, a cote de lui [D99 :
rem      ne melangez jamais les runs] ;
rem   2. il recoupe le paquet interne PUIS chaque piece, sha256 par sha256 ;
rem   3. il lance LE LANCEUR OFFICIEL du test - INTACT, octet pour octet.
rem
rem ETAPE 0, SEULEMENT SI UN CADRE "Windows a protege votre PC" apparait au
rem double-clic [la marque du web] : clic droit sur CE fichier, Proprietes,
rem cochez "Debloquer" en bas, OK - puis double-cliquez encore. Ce fichier
rem descend du coffre Drive : il porte la marque, comme toute piece telechargee.
rem
rem CE QUE LE TEST EXIGE :
rem   AUCUNE exigence : avec Python 3 le diagnostic vit COMPLET ; sans
rem   Python il rend ce que cmd lit seul et le NOMME [le CPUID et le
rem   verdict complet exigent Python - https://www.python.org].
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   aucune pour le diagnostic lui-meme - il CONSTATE [la machine nommee,
rem   le silicium lu par CPUID, SHA-NI present ou absent, ce qui vit] ;
rem   il sert aussi a CHOISIR la machine du geste B SHA-NI reel.
rem
rem LES 3 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   5ea985738d8912280e08a809a780f7e3484853b7a1506f4651986c7022605493  DIAGNOSTIC-MACHINE.bat
rem   b20621579426448ca9467813d2b32d6da97615b20e9a3422299404a8a32194f3  diagnostic_machine.py
rem   d160ec105f1238a6a3bcb908ab8ab075c30da5012f9513335c5519fae236c9e3  LISEZMOI-1CLIC-diagnostic.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 c138754d8280f260111a8eab611502c26087b3954d7ce9abd7e4a56e6287dafc
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - le diagnostic de la machine
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LE DIAGNOSTIC DE LA MACHINE
echo  Un fichier autonome, 3 pieces embarquees, chaque empreinte recoupee
echo  avant tout lancement - le lanceur officiel du test INTACT.
echo ============================================================================

rem ---- powershell [l'extracteur embarque exige PowerShell, livre avec Windows] ----
where powershell >nul 2>&1
if errorlevel 1 goto powershell_absent
echo [environnement] powershell present.

rem ---- le dossier de run NEUF, date [D99] ----
set "DT="
for /f "delims=" %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss"') do set "DT=%%I"
if not defined DT set "DT=%RANDOM%"
set "RUNDIR=%~dp0TRIADE-1CLIC-diagnostic-run-%DT%"
mkdir "%RUNDIR%" 2>nul
if not exist "%RUNDIR%" goto dossier_refuse
echo [run] le dossier du run, NEUF, date :
echo       %RUNDIR%

rem ---- l'extraction : le paquet interne [base64] redevient un zip ----
set "TRIADE_SELF=%~f0"
set "TRIADE_RUNDIR=%RUNDIR%"
set "TRIADE_DESTZIP=%RUNDIR%\paquet-interne.zip"
echo [extraction] naissance du paquet interne embarque...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $k='<<<' + 'TRIADE-PAQUET-INTERNE' + '>>>'; $r=[System.IO.File]::ReadAllText($env:TRIADE_SELF); $m=$r.IndexOf($k); if($m -lt 0){Write-Host '[REFUS] le marqueur du paquet interne est introuvable'; exit 1}; $b=$r.Substring($m + $k.Length); $d=[System.Convert]::FromBase64String(($b -replace '[^A-Za-z0-9+/=]','')); [System.IO.File]::WriteAllBytes($env:TRIADE_DESTZIP,$d); exit 0"
if errorlevel 1 goto extraction_refusee
if not exist "%TRIADE_DESTZIP%" goto extraction_refusee
echo [extraction] le paquet interne est ne.

rem ---- le recoup du paquet interne [le sha256 grave ci-dessus] ----
echo [recoup] sha256 attendu du paquet interne : c138754d8280f260111a8eab611502c26087b3954d7ce9abd7e4a56e6287dafc
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "c138754d8280f260111a8eab611502c26087b3954d7ce9abd7e4a56e6287dafc" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 3 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "DIAGNOSTIC-MACHINE.bat" "5ea985738d8912280e08a809a780f7e3484853b7a1506f4651986c7022605493"
if errorlevel 1 goto piece_divergente
call :verifie "diagnostic_machine.py" "b20621579426448ca9467813d2b32d6da97615b20e9a3422299404a8a32194f3"
if errorlevel 1 goto piece_divergente
echo [recoup] les 3 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : DIAGNOSTIC-MACHINE.bat
cd /d "%RUNDIR%"
call DIAGNOSTIC-MACHINE.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  Le temoin vit a diagnostic-machine.txt [dans le dossier du run].
echo ============================================================================
pause
exit /b %RC%

:powershell_absent
echo.
echo [REFUS NOMME] powershell est ABSENT - l'extracteur embarque en exige un
echo        [PowerShell vit avec Windows 10 et 11]. Renvoyez cet ecran TEL
echo        QUEL [D122], le labo recoupe.
pause
exit /b 2

:dossier_refuse
echo.
echo [REFUS NOMME] le dossier de run n'a pu naitre a cote de ce fichier -
echo        placez CE fichier dans un dossier ou vous avez le droit d'ecrire
echo        [Telechargements, Bureau] puis double-cliquez encore.
pause
exit /b 2

:extraction_refusee
echo.
echo [REFUS NOMME] l'extraction a echoue - le paquet interne n'a pu naitre.
echo        Renvoyez cet ecran TEL QUEL [D122] - le labo recoupe sur pieces.
pause
exit /b 2

:paquet_divergent
echo.
echo [REFUS NOMME] le sha256 du paquet interne DIVERGE de l'empreinte gravee
echo        - CE fichier a bouge depuis le laboratoire. RIEN ne court.
echo        Re-telechargez CE fichier du coffre /test.
pause
exit /b 2

:piece_divergente
echo.
echo [REFUS NOMME] une piece embarquee est DIVERGENTE ou ABSENTE - le recoup
echo        fail-closed a nomme l'ecart ci-dessus. RIEN n'a couru.
echo        Re-telechargez CE fichier du coffre /test.
pause
exit /b 2

:verifie
rem -- deux arguments : le chemin de la piece dans le run, son sha256 --
certutil -hashfile "%RUNDIR%\%~1" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "%~2" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 (
    echo [REFUS NOMME] la piece %~1 est DIVERGENTE ou ABSENTE.
    exit /b 2
)
echo [recoup] %~1 : intacte.
exit /b 0

rem ============================================================================
rem LE PAQUET INTERNE - base64 du zip des 3 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
