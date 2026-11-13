@echo off
rem ============================================================================
rem TRIADE-1CLIC-VOIE2-QEMU.bat - LA VOIE 2 QEMU - LE KIT-SHANI SOUS EMULATION EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 14 pieces du test [celles du paquet
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
rem   Exige WSL2, qemu-user [le lanceur officiel donne LA commande
rem   exacte s'il manque] et Python 3 dans WSL2. Cette voie EXERCE
rem   la chaine - le refus ne peut plus exister, qemu presente
rem   SHA-NI au CPUID - elle NE MESURE PAS : le rapport rendu est
rem   l'ARTEFACT TCG, consigne TEL QUEL [0,19x vecu au labo -
rem   jamais une verite de silicium].
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   ecrire sous votre main la mention "run sous qemu-x86_64 -cpu
rem   max, EMULATION, pas le silicium", dater et signer le temoin,
rem   puis renvoyer preuves-shani\ ENTIER au coffre /test.
rem
rem LES 14 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   2c73bb0d8f0916091312e94ae45e0fc0d08710a18ad038c5093793e0ed4977fd  qemu-wsl2\LANCER-VOIE2-QEMU.bat
rem   18043df2d68960f2b44288cb09f9ef2e319ba1c84b5e46e5c68bc585db363765  qemu-wsl2\lancer-voie2-shani.sh
rem   6eabfa0d88567bb40b2a517683e6244b18530c0221148bf7cb7b66faefc98f08  qemu-wsl2\LISEZMOI-qemu.txt
rem   31d6f33a356e15ee128697fa0cb691655be34f6040564cde607e664dafcf0838  qemu-wsl2\preuves-shani-emulation-labo\VERDICT-run-shani.txt
rem   6d6940b12e382d4b9a6f7180a3f626fb7516eafa8b8c447c86e0fe06b6f59851  qemu-wsl2\preuves-shani-emulation-labo\scenario-shani-journal.log
rem   8f68f62af6a32c2a57d5463f30b2edead70e9c5df06447734bac06ae89316d51  qemu-wsl2\preuves-shani-emulation-labo\temoin-shani.txt
rem   4c5be578398eb95effabd743311dc010a3ddbba1395e2859835f776e02f5b741  pc-windows\kit-1-shani\LANCER-KIT-1-SHANI.bat
rem   b78caab0792fcfe93f9f12ad004abaec47e62a11630142989c640262c56b62bd  pc-windows\kit-1-shani\LISEZMOI-shani.txt
rem   93d5a13fcc4d1cb2598b471e291266654d8fec18a9dd3800dba297fbc649db52  pc-windows\kit-1-shani\cibles\manifeste.json
rem   0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff  pc-windows\kit-1-shani\cibles\proxy-image.bin
rem   761ab194d88d527c653111a41324b0bb3e9247b1c56ba8dc9fedeeccbe04bcec  pc-windows\kit-1-shani\moteur-shani.bin
rem   d930cac0c6b00db0ad31108286e76ced084e417369c81fe68151100709faa1ad  pc-windows\kit-1-shani\moteur-shani.s
rem   d9def0b4d714392afcbb8a496ab0dface1b97e4398acf56d68f98c63d79d230a  pc-windows\kit-1-shani\scenario-shani.py
rem   d4d7d5e598817c68e1b2651d8679864bf7f79968a46319744ad5d9102047d7a8  LISEZMOI-1CLIC-voie2-qemu.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 2c054169259c543c0cc3441b5a5db2806b73999de8ff9e5a0f112bf405c874d1
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - la voie 2 QEMU
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LA VOIE 2 QEMU - LE KIT-SHANI SOUS EMULATION
echo  Un fichier autonome, 14 pieces embarquees, chaque empreinte recoupee
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
set "RUNDIR=%~dp0TRIADE-1CLIC-voie2-qemu-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : 2c054169259c543c0cc3441b5a5db2806b73999de8ff9e5a0f112bf405c874d1
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "2c054169259c543c0cc3441b5a5db2806b73999de8ff9e5a0f112bf405c874d1" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 14 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "qemu-wsl2\LANCER-VOIE2-QEMU.bat" "2c73bb0d8f0916091312e94ae45e0fc0d08710a18ad038c5093793e0ed4977fd"
if errorlevel 1 goto piece_divergente
call :verifie "qemu-wsl2\lancer-voie2-shani.sh" "18043df2d68960f2b44288cb09f9ef2e319ba1c84b5e46e5c68bc585db363765"
if errorlevel 1 goto piece_divergente
call :verifie "qemu-wsl2\LISEZMOI-qemu.txt" "6eabfa0d88567bb40b2a517683e6244b18530c0221148bf7cb7b66faefc98f08"
if errorlevel 1 goto piece_divergente
call :verifie "qemu-wsl2\preuves-shani-emulation-labo\VERDICT-run-shani.txt" "31d6f33a356e15ee128697fa0cb691655be34f6040564cde607e664dafcf0838"
if errorlevel 1 goto piece_divergente
call :verifie "qemu-wsl2\preuves-shani-emulation-labo\scenario-shani-journal.log" "6d6940b12e382d4b9a6f7180a3f626fb7516eafa8b8c447c86e0fe06b6f59851"
if errorlevel 1 goto piece_divergente
call :verifie "qemu-wsl2\preuves-shani-emulation-labo\temoin-shani.txt" "8f68f62af6a32c2a57d5463f30b2edead70e9c5df06447734bac06ae89316d51"
if errorlevel 1 goto piece_divergente
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
echo [recoup] les 14 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : qemu-wsl2\LANCER-VOIE2-QEMU.bat
cd /d "%RUNDIR%"
call qemu-wsl2\LANCER-VOIE2-QEMU.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  A VOTRE MAIN : la mention EMULATION sous votre main, la date,
echo  la signature - puis preuves-shani\ ENTIER au coffre /test.
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
rem LE PAQUET INTERNE - base64 du zip des 14 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
rRm8nnPMVH4e1hn9C1BLAQIUAxQAAAAIAABgbV3SQ6K8ygUAAFQLAAAdAAAAAAAAAAAAAACkAQAA
AABMSVNFWk1PSS0xQ0xJQy12b2llMi1xZW11LnR4dFBLAQIUAxQAAAAIAABgbV0F78yf5gUAAHEO
AAAtAAAAAAAAAAAAAACkAQUGAABwYy13aW5kb3dzL2tpdC0xLXNoYW5pL0xBTkNFUi1LSVQtMS1T
SEFOSS5iYXRQSwECFAMUAAAACAAAYG1dBxkbPO0LAAAAGAAAKQAAAAAAAAAAAAAApAE2DAAAcGMt
d2luZG93cy9raXQtMS1zaGFuaS9MSVNFWk1PSS1zaGFuaS50eHRQSwECFAMUAAAACAAAYG1dZ2sr
EigDAABdBgAALAAAAAAAAAAAAAAApAFqGAAAcGMtd2luZG93cy9raXQtMS1zaGFuaS9jaWJsZXMv
bWFuaWZlc3RlLmpzb25QSwECFAMUAAAACAAAYG1dkAUL4SxDAAAAEAEALQAAAAAAAAAAAAAApAHc
GwAAcGMtd2luZG93cy9raXQtMS1zaGFuaS9jaWJsZXMvcHJveHktaW1hZ2UuYmluUEsBAhQDFAAA
AAgAAGBtXW+QF8/8AgAAUAUAACcAAAAAAAAAAAAAAKQBU18AAHBjLXdpbmRvd3Mva2l0LTEtc2hh
bmkvbW90ZXVyLXNoYW5pLmJpblBLAQIUAxQAAAAIAABgbV0uCsFy3wYAACweAAAlAAAAAAAAAAAA
AACkAZRiAABwYy13aW5kb3dzL2tpdC0xLXNoYW5pL21vdGV1ci1zaGFuaS5zUEsBAhQDFAAAAAgA
AGBtXassH2PnKQAAhYQAACgAAAAAAAAAAAAAAKQBtmkAAHBjLXdpbmRvd3Mva2l0LTEtc2hhbmkv
c2NlbmFyaW8tc2hhbmkucHlQSwECFAMUAAAACAAAYG1d5hEjCoQGAAAXEAAAHwAAAAAAAAAAAAAA
pAHjkwAAcWVtdS13c2wyL0xBTkNFUi1WT0lFMi1RRU1VLmJhdFBLAQIUAxQAAAAIAABgbV2jSR2Q
HwkAAMMRAAAbAAAAAAAAAAAAAACkAaSaAABxZW11LXdzbDIvTElTRVpNT0ktcWVtdS50eHRQSwEC
FAMUAAAACAAAYG1deQIAe8kFAAD0DQAAHwAAAAAAAAAAAAAApAH8owAAcWVtdS13c2wyL2xhbmNl
ci12b2llMi1zaGFuaS5zaFBLAQIUAxQAAAAIAABgbV2lbdG04AAAABYBAAA8AAAAAAAAAAAAAACk
AQKqAABxZW11LXdzbDIvcHJldXZlcy1zaGFuaS1lbXVsYXRpb24tbGFiby9WRVJESUNULXJ1bi1z
aGFuaS50eHRQSwECFAMUAAAACAAAYG1doNK9raEBAACTAgAAQQAAAAAAAAAAAAAApAE8qwAAcWVt
dS13c2wyL3ByZXV2ZXMtc2hhbmktZW11bGF0aW9uLWxhYm8vc2NlbmFyaW8tc2hhbmktam91cm5h
bC5sb2dQSwECFAMUAAAACAAAYG1dqjzxzJwEAACyBwAANwAAAAAAAAAAAAAApAE8rQAAcWVtdS13
c2wyL3ByZXV2ZXMtc2hhbmktZW11bGF0aW9uLWxhYm8vdGVtb2luLXNoYW5pLnR4dFBLBQYAAAAA
DgAOANEEAAAtsgAAAAA=
