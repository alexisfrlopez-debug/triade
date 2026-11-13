@echo off
rem ============================================================================
rem TRIADE-1CLIC-TEMOIN-VITRINE.bat - LE TEMOIN VITRINE DU KIT LOUPE EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 5 pieces du test [celles du paquet
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
rem   AUCUNE exigence. La PREMIERE fenetre s'ouvre VIDE [l'usage a la
rem   barre d'etat] : fermez-la par Alt+F4. La SECONDE s'ouvre AVEC
rem   le fichier temoin-fichier.bin [l'entete des colonnes, les
rem   lignes hexa, le miroir ASCII, le panneau d'empreintes] :
rem   fermez-la par Alt+F4. Les DEUX codes de sortie sont consignes
rem   au temoin - c'est VOUS qui fermez, c'est cela qui est temoin.
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   fermer vous-meme les deux fenetres, puis renvoyer le dossier
rem   preuves-loupe\ ENTIER au coffre /test, QUEL QUE SOIT le
rem   verdict [il vit dans loupe-kit-13\preuves-loupe\].
rem
rem LES 5 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1  loupe-kit-13\loupe.exe
rem   131d0135850237927ef59315a722bd0f206ed7741f1830b0aaf68e0a720a845a  loupe-kit-13\scenario-loupe.py
rem   33763be44bd9687f71b549bb3784759a491129ebc58856edfe6fb8ff39b216fe  loupe-kit-13\temoin-vitrine.bat
rem   6cad6bd3cc8bcbe94c16571766882b86f2fb911bf156e4d74f1c019c2f7b764e  loupe-kit-13\LISEZMOI-KIT-LOUPE.md
rem   8c534112abd220e25cedd5cb9178499462e95c3007c07f43b6aa6c1df1ab0126  LISEZMOI-1CLIC-temoin-vitrine.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 4318d8659ea90c95cc44071aa89760fcc099477b013485fd9aa389ce41d36b2f
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - le temoin vitrine du kit loupe
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LE TEMOIN VITRINE DU KIT LOUPE
echo  Un fichier autonome, 5 pieces embarquees, chaque empreinte recoupee
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
set "RUNDIR=%~dp0TRIADE-1CLIC-temoin-vitrine-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : 4318d8659ea90c95cc44071aa89760fcc099477b013485fd9aa389ce41d36b2f
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "4318d8659ea90c95cc44071aa89760fcc099477b013485fd9aa389ce41d36b2f" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 5 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "loupe-kit-13\loupe.exe" "c111510535767a40b0122d4e42261c9d8e1ec10d94d95ef666fd76ceb93e61d1"
if errorlevel 1 goto piece_divergente
call :verifie "loupe-kit-13\scenario-loupe.py" "131d0135850237927ef59315a722bd0f206ed7741f1830b0aaf68e0a720a845a"
if errorlevel 1 goto piece_divergente
call :verifie "loupe-kit-13\temoin-vitrine.bat" "33763be44bd9687f71b549bb3784759a491129ebc58856edfe6fb8ff39b216fe"
if errorlevel 1 goto piece_divergente
call :verifie "loupe-kit-13\LISEZMOI-KIT-LOUPE.md" "6cad6bd3cc8bcbe94c16571766882b86f2fb911bf156e4d74f1c019c2f7b764e"
if errorlevel 1 goto piece_divergente
echo [recoup] les 5 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : loupe-kit-13\temoin-vitrine.bat
cd /d "%RUNDIR%"
call loupe-kit-13\temoin-vitrine.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  A VOTRE MAIN : fermer les deux fenetres [Alt+F4] - le temoin
echo  nait de VOTRE geste, quel que soit le verdict.
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
rem LE PAQUET INTERNE - base64 du zip des 5 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
