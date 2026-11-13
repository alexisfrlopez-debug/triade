@echo off
rem ============================================================================
rem TRIADE-1CLIC-CAMPAGNE-D204-v3.bat - LA CAMPAGNE DE COMPARAISON D204 EN UN FICHIER AUTONOME
rem [l'edition CORRECTIF-ENCODAGE du 14/11/2026 au soir - la reparation de
rem l'ecart nomme par le premier run du GUI de campagne sous Windows].
rem
rem LA REPARATION DE CETTE EDITION : l'annonce de la calibration (chronometre
rem v2) ecrivait le caractere U+2264 [inferieur ou egal], INENCODABLE en
rem cp1252 - la page de codes d'une sortie PIPEE sous Windows [le GUI de
rem campagne capture la sortie des instruments] : UnicodeEncodeError APRES
rem la mesure et le journal - la pause fut MESUREE et JOURNALISEE, l'annonce
rem SEULE faillit [code 1, "calibration ROUGE" sans faute d'horloge]. LES
rem DEUX instruments passent a l'edition sans faute de page de codes :
rem chronometre v3 et compteur v2 [flux reconfigures en UTF-8
rem errors="replace", annonces cp1252-sures : "<=" au lieu de U+2264, "!="
rem au lieu de U+2260] ; le mecanisme de la pause et les formats de journal
rem demeurent [label "calibration-sleep", la cle du verificateur]. Le
rem recoup de la carte LISEZMOI embarquee, omis de la v2, vit desormais
rem [NEUF sur NEUF pieces recoupees]. Le plan D204 VERROUILLE demeure
rem INTACT [a78caf8c... recoupe par certutil a chaque geste] et les SIX
rem autres pieces demeurent INTACTES [celles de l'edition FICHIERS-1CLIC].
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
rem   CALIBRATION du chronometre [la pause portable v3 - un dry-run, jamais
rem   une mesure], le CHRONOMETRAGE d'une commande, les TOKENS du journal.
rem   Le plan PRE-ENREGISTRE est VERROUILLE : son sha256 recoupe par
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
rem   ff0c96522fa558ccc37af6f16b9d63cc91ced71ae81c699c2cd26c1a0853a58f  campagne-d204\chronometre_verification.py
rem   e2939ef9d3ef7f228c1881b55744e182238fbb489b58d30595882d926eea26e5  campagne-d204\compter_tokens.py
rem   e2756e76a84ac9c5d552ca01da26dc228e8b23c50b05689cb1cf9cee11380497  campagne-d204\defauts.csv
rem   3d7d13f033b1176efba8d4096b4512655805897e89127461fa25fc56cc8e2d10  campagne-d204\livraisons.csv
rem   0ccb75807e4fdbac3ffc63fb53f93aa2d3615290c6b038cc8be0869e4021d322  LISEZMOI-1CLIC-campagne-d204.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 7b8aaacc95f1cc07fc94b1fde60fb556ee53e2a44076c00461e6e1c2327100ce
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
echo [recoup] sha256 attendu du paquet interne : 7b8aaacc95f1cc07fc94b1fde60fb556ee53e2a44076c00461e6e1c2327100ce
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "7b8aaacc95f1cc07fc94b1fde60fb556ee53e2a44076c00461e6e1c2327100ce" "%TEMP%\triade-1clic-sha.txt" >nul
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
call :verifie "campagne-d204\chronometre_verification.py" "ff0c96522fa558ccc37af6f16b9d63cc91ced71ae81c699c2cd26c1a0853a58f"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\compter_tokens.py" "e2939ef9d3ef7f228c1881b55744e182238fbb489b58d30595882d926eea26e5"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\defauts.csv" "e2756e76a84ac9c5d552ca01da26dc228e8b23c50b05689cb1cf9cee11380497"
if errorlevel 1 goto piece_divergente
call :verifie "campagne-d204\livraisons.csv" "3d7d13f033b1176efba8d4096b4512655805897e89127461fa25fc56cc8e2d10"
if errorlevel 1 goto piece_divergente
call :verifie "LISEZMOI-1CLIC-campagne-d204.txt" "0ccb75807e4fdbac3ffc63fb53f93aa2d3615290c6b038cc8be0869e4021d322"
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
rem ============================================================================
rem LE PAQUET INTERNE - base64 du zip des 9 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
hfd9iiN1kUR1AlSsiliEZoQsOWlx4gqpQtVkfFNGdWbC/ERl1yXseQCWZM8b+E14Eu44pIU9G2s8
9v3OuefeYxRjTNuvizJ/VwlMX2BS4bIYz9CfnD5/OcCvh28oxBxFflWO8/nFbI5+NIRG3/JzIx1c
NEfHCOSc1AZ1Lxrc6ZBBxntMRPUeSyf9YISy/fK2EGDsKc7Af9XtbiVjAPkAZdeb0O4YlJCPYug3
lAQyvvbg86Em2drb2LKstwbtd9TEkn/+8IzqoIRqJrCy2nfodbsLTn+KNMArNPLpHZdlPh3npTiU
sZqyNTGn3SmnQ1fe9OQtmYC5qAr0N7r9oYi7YZCxQQbNRhZ4lmq9jU7RyVIb6T7jfJAx6B+9mv7q
86DZI+NpveR6zvBkzx+hIA+6V030LJA6M3bNIL7tX5diMZxVH4aNvktO9l84fBZbWsitZLfBcmQc
I7d8fX5RvhF5UYghc67yiXgsbXrarHhWwUUVomOHkX2tVo4yHquMigGq/cljGsCncIxPS2BCiiil
3+U+Un7LsqSeHL+2UYNCan8/rFE3nMYawy2cPQ0xS6uSBak+Umbimpy90bxYXa5ZLQPdpM3qDmkp
tuRqrULmSNm4OfpPmN9QSwECFAMUAAAACAAAoG5d9Y4c/igHAABkDQAAIAAAAAAAAAAAAAAAgAEA
AAAATElTRVpNT0ktMUNMSUMtY2FtcGFnbmUtZDIwNC50eHRQSwECFAMUAAAACAAAoG5dhn3ojVsK
AABWHQAAJgAAAAAAAAAAAAAAgAFmBwAAY2FtcGFnbmUtZDIwNC9MQU5DRVItQ0FNUEFHTkUtRDIw
NC5iYXRQSwECFAMUAAAACAAAoG5dFsCsukIHAACuEAAAJgAAAAAAAAAAAAAAgAEFEgAAY2FtcGFn
bmUtZDIwNC9MSVNFWk1PSS1jb21wYXJhaXNvbi50eHRQSwECFAMUAAAACAAAoG5dxhTEcZkWAADw
NQAALQAAAAAAAAAAAAAAgAGLGQAAY2FtcGFnbmUtZDIwNC9QTEFOX1BSRVJFR0lTVFJFX0NPTVBB
UkFJU09OLm1kUEsBAhQDFAAAAAgAAKBuXWZFVmfjAQAACgMAACUAAAAAAAAAAAAAAIABbzAAAGNh
bXBhZ25lLWQyMDQvY2FybmV0X3RlbXBzX2h1bWFpbi5jc3ZQSwECFAMUAAAACAAAoG5dJqY8VTcO
AACgIwAAKQAAAAAAAAAAAAAAgAGVMgAAY2FtcGFnbmUtZDIwNC9jaHJvbm9tZXRyZV92ZXJpZmlj
YXRpb24ucHlQSwECFAMUAAAACAAAoG5dzCO3jTEPAABCJwAAHwAAAAAAAAAAAAAAgAETQQAAY2Ft
cGFnbmUtZDIwNC9jb21wdGVyX3Rva2Vucy5weVBLAQIUAxQAAAAIAACgbl1DyICE9wAAAIUBAAAZ
AAAAAAAAAAAAAACAAYFQAABjYW1wYWduZS1kMjA0L2RlZmF1dHMuY3N2UEsBAhQDFAAAAAgAAKBu
XY7ZczrdAQAAEwMAABwAAAAAAAAAAAAAAIABr1EAAGNhbXBhZ25lLWQyMDQvbGl2cmFpc29ucy5j
c3ZQSwUGAAAAAAkACQDZAgAAxlMAAAAA
