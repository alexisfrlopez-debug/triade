@echo off
rem ============================================================================
rem TRIADE-1CLIC-GESTE-B-SHANI.bat - LE GESTE B SHA-NI REEL EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 8 pieces du test [celles du paquet
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
rem   Exige Python 3 [le lanceur officiel refuse nomme sinon] et un
rem   silicium qui A SHA-NI [Intel Ice Lake et apres, AMD Ryzen - le
rem   fichier TRIADE-1CLIC-DIAGNOSTIC.bat vous le dit AVANT]. Sur une
rem   machine sans SHA-NI, le refus nomme T0.silicium est un RESULTAT,
rem   jamais une panne [vecu trois fois sur ALEKPC].
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   dater et signer la ligne signature du geste du temoin
rem   preuves-shani\temoin-shani.txt de votre main, puis renvoyer le
rem   dossier preuves-shani\ ENTIER au coffre /test.
rem
rem LES 8 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   4c5be578398eb95effabd743311dc010a3ddbba1395e2859835f776e02f5b741  pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat
rem   b78caab0792fcfe93f9f12ad004abaec47e62a11630142989c640262c56b62bd  pc-windows\kit-1-shani\LISEZMOI-shani.txt
rem   93d5a13fcc4d1cb2598b471e291266654d8fec18a9dd3800dba297fbc649db52  pc-windows\kit-1-shani\cibles\manifeste.json
rem   0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff  pc-windows\kit-1-shani\cibles\proxy-image.bin
rem   761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec  pc-windows\kit-1-shani\moteur-shani.bin
rem   d930cac0c6b00db0ad31108286e76ced084e417369c81fe68151100709faa1ad  pc-windows\kit-1-shani\moteur-shani.s
rem   d9def0b4d714392afcbb8a496ab0dface1b97e4398acf56d68f98c63d79d230a  pc-windows\kit-1-shani\scenario-shani.py
rem   f4cbbaf45589e07ec01307d81e0e1548dff37f377a7c362c264125f028ca4fb1  LISEZMOI-1CLIC-geste-b.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 59e6bc5dae796f83321502e9ffb3867f116dfb22f48e05b105c0c07da0aa9ff2
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - le geste B SHA-NI reel
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LE GESTE B SHA-NI REEL
echo  Un fichier autonome, 8 pieces embarquees, chaque empreinte recoupee
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
set "RUNDIR=%~dp0TRIADE-1CLIC-geste-b-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : 59e6bc5dae796f83321502e9ffb3867f116dfb22f48e05b105c0c07da0aa9ff2
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "59e6bc5dae796f83321502e9ffb3867f116dfb22f48e05b105c0c07da0aa9ff2" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 8 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat" "4c5be578398eb95effabd743311dc010a3ddbba1395e2859835f776e02f5b741"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\LISEZMOI-shani.txt" "b78caab0792fcfe93f9f12ad004abaec47e62a11630142989c640262c56b62bd"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\cibles\manifeste.json" "93d5a13fcc4d1cb2598b471e291266654d8fec18a9dd3800dba297fbc649db52"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\cibles\proxy-image.bin" "0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\moteur-shani.bin" "761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\moteur-shani.s" "d930cac0c6b00db0ad31108286e76ced084e417369c81fe68151100709faa1ad"
if errorlevel 1 goto piece_divergente
call :verifie "pc-windows\kit-1-shani\scenario-shani.py" "d9def0b4d714392afcbb8a496ab0dface1b97e4398acf56d68f98c63d79d230a"
if errorlevel 1 goto piece_divergente
echo [recoup] les 8 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat
cd /d "%RUNDIR%"
call pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  A VOTRE MAIN : dater, signer le temoin, renvoyer preuves-shani\
echo  ENTIER au coffre /test.
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
rem LE PAQUET INTERNE - base64 du zip des 8 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
U5E6qYenbxUle0JkncW1XFZoCRztfa3JGpw4uLyW1wN4UhlfDCyZOA12yGI8GerrZUx0e6si1SIM
F76J0k3oGkg65c2apJkW4sGleuuL5TaaWpUnv2BOVVfP5ENvHFHm5axPGFosLACsUaVejrtfsPDq
dCjFw/cmKMicTGKcGEX2jZ1op46StwfHXBAx4Gw8PMQX/B4K7b+RfuKVBfn3FJQdtP9Vq+uXLqV/
NjNF1VZIWgLNBSGCUJI5pxWoAf1SVhegUJwfU8Qm6A5PJuQQTyZo7E0m8hRAfItzH6wMUU6luvN/
AVBLAQIUAxQAAAAIAABgbV1+HG5l3wQAAFkJAAAaAAAAAAAAAAAAAACkAQAAAABMSVNFWk1PSS0x
Q0xJQy1nZXN0ZS1iLnR4dFBLAQIUAxQAAAAIAABgbV0F78yf5gUAAHEOAAAtAAAAAAAAAAAAAACk
ARcFAABwYy13aW5kb3dzL2tpdC0xLXNoYW5pL0xBTkNFUi1LSVQtMS1TSEFOSS5iYXRQSwECFAMU
AAAACAAAYG1dBxkbPO0LAAAAGAAAKQAAAAAAAAAAAAAApAFICwAAcGMtd2luZG93cy9raXQtMS1z
aGFuaS9MSVNFWk1PSS1zaGFuaS50eHRQSwECFAMUAAAACAAAYG1dZ2srEigDAABdBgAALAAAAAAA
AAAAAAAApAF8FwAAcGMtd2luZG93cy9raXQtMS1zaGFuaS9jaWJsZXMvbWFuaWZlc3RlLmpzb25Q
SwECFAMUAAAACAAAYG1dkAUL4SxDAAAAEAEALQAAAAAAAAAAAAAApAHuGgAAcGMtd2luZG93cy9r
aXQtMS1zaGFuaS9jaWJsZXMvcHJveHktaW1hZ2UuYmluUEsBAhQDFAAAAAgAAGBtXW+QF8/8AgAA
UAUAACcAAAAAAAAAAAAAAKQBZV4AAHBjLXdpbmRvd3Mva2l0LTEtc2hhbmkvbW90ZXVyLXNoYW5p
LmJpblBLAQIUAxQAAAAIAABgbV0uCsFy3wYAACweAAAlAAAAAAAAAAAAAACkAaZhAABwYy13aW5k
b3dzL2tpdC0xLXNoYW5pL21vdGV1ci1zaGFuaS5zUEsBAhQDFAAAAAgAAGBtXassH2PnKQAAhYQA
ACgAAAAAAAAAAAAAAKQByGgAAHBjLXdpbmRvd3Mva2l0LTEtc2hhbmkvc2NlbmFyaW8tc2hhbmku
cHlQSwUGAAAAAAgACACtAgAA9ZIAAAAA
