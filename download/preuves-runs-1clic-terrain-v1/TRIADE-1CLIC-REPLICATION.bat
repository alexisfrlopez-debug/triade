@echo off
rem ============================================================================
rem TRIADE-1CLIC-REPLICATION.bat - LA REPLICATION - LA GRILLE T/X ET LE KAPPA EN UN FICHIER AUTONOME
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
rem   Exige Python 3. L'AUTOTEST du calculateur kappa de Cohen est la
rem   preuve a froid [trois cas synthetiques au k calculable a la
rem   main] ; le calcul vit le jour des DEUX jeux d'annotations [le
rem   seuil PRE-ENREGISTRE : k superieur ou egal a 0,61 - D189].
rem   CE QUI MANQUE, consigne jamais maquille : le SECOND
rem   ANNOTATEUR [a recruter] et le SECOND DOMAINE [en attente
rem   d'une vraie commande] - aucun des deux ne s'automatise.
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   recruter le second annotateur, produire les DEUX jeux
rem   d'annotations [le CSV : id,classe - un fichier par annotateur],
rem   puis vivre le calcul au choix 2 du menu.
rem
rem LES 5 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   1c54a78206591a4a7e96c47266257829d3e48035fe73a50756e77d0be925492f  replication\LANCER-REPLICATION.bat
rem   a0a6c5e343e68bd1f05c2afa7e303e621968fc4d7bbb14070a6d135bb66bf8c7  replication\LISEZMOI-replication.txt
rem   e94abb200ca1ff44854af4bcc6c0c6bf609683549315dacbbe35356a513b80c1  replication\grille_tx.csv
rem   89f4c5e0dd14660acaf7df201c1f77f883c6a99be10fee4ff7cd22184c118d84  replication\kohen_kappa_v150.py
rem   af713bb5d393af4bf5f282c7c05dd69dab18d4a734552e5b6da9a647824d6f6c  LISEZMOI-1CLIC-replication.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 dde3f90368f7ce5c616d9d3126420d5be716c0272b99ac049aa3c99aaf2c6bac
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - la replication
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LA REPLICATION - LA GRILLE T/X ET LE KAPPA
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
set "RUNDIR=%~dp0TRIADE-1CLIC-replication-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : dde3f90368f7ce5c616d9d3126420d5be716c0272b99ac049aa3c99aaf2c6bac
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "dde3f90368f7ce5c616d9d3126420d5be716c0272b99ac049aa3c99aaf2c6bac" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 5 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "replication\LANCER-REPLICATION.bat" "1c54a78206591a4a7e96c47266257829d3e48035fe73a50756e77d0be925492f"
if errorlevel 1 goto piece_divergente
call :verifie "replication\LISEZMOI-replication.txt" "a0a6c5e343e68bd1f05c2afa7e303e621968fc4d7bbb14070a6d135bb66bf8c7"
if errorlevel 1 goto piece_divergente
call :verifie "replication\grille_tx.csv" "e94abb200ca1ff44854af4bcc6c0c6bf609683549315dacbbe35356a513b80c1"
if errorlevel 1 goto piece_divergente
call :verifie "replication\kohen_kappa_v150.py" "89f4c5e0dd14660acaf7df201c1f77f883c6a99be10fee4ff7cd22184c118d84"
if errorlevel 1 goto piece_divergente
echo [recoup] les 5 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : replication\LANCER-REPLICATION.bat
cd /d "%RUNDIR%"
call replication\LANCER-REPLICATION.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  Le seuil pre-enregistre demeure : k superieur ou egal a 0,61.
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
LnB5UEsFBgAAAAAFAAUAggEAAOolAAAAAA==
