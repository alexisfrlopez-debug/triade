@echo off
rem ============================================================================
rem TRIADE-1CLIC-CAMPAGNE-D204.bat - LA CAMPAGNE DE COMPARAISON D204 EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 9 pieces du test [celles du paquet
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
rem   Exige Python 3. La console vit le STATUT des pieces, la
rem   CALIBRATION du chronometre [un dry-run, jamais une mesure],
rem   le CHRONOMETRAGE d'une commande, les TOKENS du journal. Le
rem   plan PRE-ENREGISTRE est VERROUILLE : son sha256 recoupe par
rem   certutil a chaque geste - un plan retouche ne courra jamais.
rem   AUCUNE mesure n'existe encore, aucune n'est fabriquee [CA1].
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   la campagne elle-meme : un travail de fond aux DEUX bras [T la
rem   discipline TRIADE, C le flux standard C+gcc, les memes taches,
rem   les quatre metriques] - le plan pre-enregistre fait foi. Le kit
rem   loupe-13 vit deja au coffre /test pour le bras de verification.
rem
rem LES 9 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   5f1ffa9776d296b809ada54217e86f8e4789bc865a5d77e0402ea222e021d1a9  campagne-d204\LANCER-CAMPAGNE-D204.bat
rem   609a0e81b99376e698ef0bd90e89a0537ba97caf88cb8d9ee67637227f282beb  campagne-d204\LISEZMOI-comparaison.txt
rem   a78caf8c0cb9498446a91d18d0f8a02ee16b6893d4fe4ce49843397f30240255  campagne-d204\PLAN_PREREGISTRE_COMPARAISON.md
rem   ba736b1f1e153e18a8c9bf6e97d73c04e456dcf136ede93e278802eca98baf0e  campagne-d204\carnet_temps_humain.csv
rem   af73c83478b81d487c3b90ab6e3a6b9173282b72a52b18c347a709bcd93a4237  campagne-d204\chronometre_verification.py
rem   f5f3af046ab73d9282206e01ed7127a33c9bdef15e0ff2e2a29da3a5e0e348b6  campagne-d204\compter_tokens.py
rem   e2756e76a84ac9c5d552ca01da26dc228e8b23c50b05689cb1cf9cee11380497  campagne-d204\defauts.csv
rem   3d7d13f033b1176efba8d4096b4512655805897e89127461fa25fc56cc8e2d10  campagne-d204\livraisons.csv
rem   ecec5c1df66f0747b957d14edda5f85b1aef09bad51e8019c768597fab752cfe  LISEZMOI-1CLIC-campagne-d204.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 61a355e713bf0d07a067d4a1c0aeb87bcae1291f53592999e840e6bc2dee279c
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - la campagne D204
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LA CAMPAGNE DE COMPARAISON D204
echo  Un fichier autonome, 9 pieces embarquees, chaque empreinte recoupee
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
set "RUNDIR=%~dp0TRIADE-1CLIC-campagne-d204-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : 61a355e713bf0d07a067d4a1c0aeb87bcae1291f53592999e840e6bc2dee279c
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "61a355e713bf0d07a067d4a1c0aeb87bcae1291f53592999e840e6bc2dee279c" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 9 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "campagne-d204\LANCER-CAMPAGNE-D204.bat" "5f1ffa9776d296b809ada54217e86f8e4789bc865a5d77e0402ea222e021d1a9"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\LISEZMOI-comparaison.txt" "609a0e81b99376e698ef0bd90e89a0537ba97caf88cb8d9ee67637227f282beb"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\PLAN_PREREGISTRE_COMPARAISON.md" "a78caf8c0cb9498446a91d18d0f8a02ee16b6893d4fe4ce49843397f30240255"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\carnet_temps_humain.csv" "ba736b1f1e153e18a8c9bf6e97d73c04e456dcf136ede93e278802eca98baf0e"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\chronometre_verification.py" "af73c83478b81d487c3b90ab6e3a6b9173282b72a52b18c347a709bcd93a4237"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\compter_tokens.py" "f5f3af046ab73d9282206e01ed7127a33c9bdef15e0ff2e2a29da3a5e0e348b6"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\defauts.csv" "e2756e76a84ac9c5d552ca01da26dc228e8b23c50b05689cb1cf9cee11380497"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\livraisons.csv" "3d7d13f033b1176efba8d4096b4512655805897e89127461fa25fc56cc8e2d10"
if errorlevel 1 goto piece_divergente
echo [recoup] les 9 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : campagne-d204\LANCER-CAMPAGNE-D204.bat
cd /d "%RUNDIR%"
call campagne-d204\LANCER-CAMPAGNE-D204.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  Le journal de campagne nait a preuves_v150\comparaison_resultats\
echo  du dossier du run, a la premiere mesure instrumentee seulement.
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
rem LE PAQUET INTERNE - base64 du zip des 9 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
H4Kn4AieM0wy3+SN3ZufktOWt0uu1rn2/edK3JyYaFz3plrBL+ZUVW2rir/rqFXpLNW/VP87FFcy
zZV11fuvR1GrgR7vmjnQSmcou4BpLncwXYV6wjHZddNywpyZywL/CxqiNpMv5cMEkyYjmKdpg2hZ
lopU/nwtgr5b7G/gi3kHIA3HCsbz8pj5P25y60qW74U1RbuI2IbgGmPaWC+TnaIU6BE76LdLj0X0
z4X+iIZ5Q6qOaRB5FilJlgXEMy4HCQ1OEWywkOwR3DpDl/Aze8xLTl1IyVQoM1Reeqj/EmGU0bMl
c03PVnlWnIRkkkatmAg94EdAlHwe6Mldkzyjy4GFwIQs4TD9HUWKuQhpJOvzBUcUD2mUnI1sA3xz
UF+lYm/179oYAJ8prk+3NbvLd5qeWannmO95mqxhCCIOXZviGW0Bi+P0OfOBDmu6uhkCSKy2UEg6
G5mfZB5ltGPVrW2XoTCraQVge+s6kx3cr3fkfGpTurZRQD13L88sYIMMrgzhN0bvG1P3VWX7R/C6
meZN1yTZ43rETlC3K097sXw1ICwDft3HRUg5DLjihiOZqU1QamNY58HaATQK01+i0kQXsJKRwF3Y
EyVyq51AsToM3e1hMTEmB4s3c7D2dxkeGhKC5Z2GtVUHH5SKk6uTk2/fvtWM2Vok56jEi7DcvoPt
++g9Jt99v/QWtWFznkJTe6vnDzz09Wz98OB/UEsDBBQAAAAIAABgbV0WwKy6QgcAAK4QAAAmAAAA
Y2FtcGFnbmUtZDIwNC9MSVNFWk1PSS1jb21wYXJhaXNvbi50eHStV01z20YSveNXzI1kWSRFWcqm
7MoBpmGHCT+0JOVs5aIagSNxHGAAzwdX9mmPqz3saav2urWXFXPOLwj+SX5JXs+AFJzkgMPyQgLE
NLpf93vdPZ2sku9niwn75W//YtOEfTtZs9cJGy9ml/EynqwWc1yu2HeL5bdvpovvVqxb8g9OWHbB
NoJlnO34nRPseS/66v/0ibpZRypjtUutLBS7OP+rkufbT1v2kmWClRlXrNTVvi+UFncSD1Z7lsr+
+0Iqe8IMjoi81AJXIkoLZeSdqvaCVf9hr89Oz1n8Lp6vmS2cFSwXxmnRi6JpZ/Hqm2TNXtS39Anj
7h6hX/2FbaRJZZlJJQzrrpeTGPggcFVY7h00qcgyesPOwMHoNsNBY7nacL1h42d3adqDW07jT8Nm
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
iiil3+U+Un7LsqSeHL+2UYNCan8/rFE3nMYawy2cPQ0xS6uSBak+Umbimpy90bxYXa5ZLQPdpM3q
DmkptuRqrULmSNm4OfpPmN9QSwECFAMUAAAACAAAYG1dIujNC38FAAAQCgAAIAAAAAAAAAAAAAAA
pAEAAAAATElTRVpNT0ktMUNMSUMtY2FtcGFnbmUtZDIwNC50eHRQSwECFAMUAAAACAAAYG1dhn3o
jVsKAABWHQAAJgAAAAAAAAAAAAAApAG9BQAAY2FtcGFnbmUtZDIwNC9MQU5DRVItQ0FNUEFHTkUt
RDIwNC5iYXRQSwECFAMUAAAACAAAYG1dFsCsukIHAACuEAAAJgAAAAAAAAAAAAAApAFcEAAAY2Ft
cGFnbmUtZDIwNC9MSVNFWk1PSS1jb21wYXJhaXNvbi50eHRQSwECFAMUAAAACAAAYG1dxhTEcZkW
AADwNQAALQAAAAAAAAAAAAAApAHiFwAAY2FtcGFnbmUtZDIwNC9QTEFOX1BSRVJFR0lTVFJFX0NP
TVBBUkFJU09OLm1kUEsBAhQDFAAAAAgAAGBtXWZFVmfjAQAACgMAACUAAAAAAAAAAAAAAKQBxi4A
AGNhbXBhZ25lLWQyMDQvY2FybmV0X3RlbXBzX2h1bWFpbi5jc3ZQSwECFAMUAAAACAAAYG1d2lAX
vVgJAADwFgAAKQAAAAAAAAAAAAAApAHsMAAAY2FtcGFnbmUtZDIwNC9jaHJvbm9tZXRyZV92ZXJp
ZmljYXRpb24ucHlQSwECFAMUAAAACAAAYG1dHhH5cQ0NAAAzIgAAHwAAAAAAAAAAAAAApAGLOgAA
Y2FtcGFnbmUtZDIwNC9jb21wdGVyX3Rva2Vucy5weVBLAQIUAxQAAAAIAABgbV1DyICE9wAAAIUB
AAAZAAAAAAAAAAAAAACkAdVHAABjYW1wYWduZS1kMjA0L2RlZmF1dHMuY3N2UEsBAhQDFAAAAAgA
AGBtXY7ZczrdAQAAEwMAABwAAAAAAAAAAAAAAKQBA0kAAGNhbXBhZ25lLWQyMDQvbGl2cmFpc29u
cy5jc3ZQSwUGAAAAAAkACQDZAgAAGksAAAAA
