@echo off
rem ============================================================================
rem TRIADE-1CLIC-SEQUESTRE-D183.bat - LE SEQUESTRE D183 - LA CEREMONIE DES 5 PARTS EN UN FICHIER AUTONOME
rem [l'edition FICHIERS-1CLIC du 13/11/2026 - la commande du developpeur :
rem "Fais en sorte que chaque test se fasse en lancant un fichier autonome
rem en 1 clic : exe, apk, bat etc..."].
rem
rem LE GESTE : DOUBLE-CLIQUEZ CE FICHIER SEUL. Il ne demande aucun autre
rem fichier, aucune extraction prealable, aucune commande. Il porte en lui,
rem scellees par empreinte, les 6 pieces du test [celles du paquet
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
rem   Exige Python 3 ET les paquets pynacl et cryptography [le geste
rem   pip install pynacl cryptography se vit AVANT la mise hors-ligne
rem   - l'outil refuse de courir sans eux, fail-closed nomme]. LA
rem   CEREMONIE se vit a VOTRE machine HORS-LIGNE - jamais au bac a
rem   sable, jamais en ligne [D87, D183]. La phrase ne traverse
rem   JAMAIS le lanceur : seul son CHEMIN passe. Le coffre reel du
rem   developpeur demeure INTACT - ce kit prepare, il n'applique rien.
rem
rem CE QUI RESTE A VOTRE MAIN [jamais automatise] :
rem   la repetition generale d'abord [l'autotest, VERT exige], puis le
rem   decoupage de la phrase, la repartition des cinq medias [au
rem   moins DEUX hors nuage], la preuve de reconstitution a froid
rem   AVANT tout retrait. Le retrait de la phrase en clair est un
rem   geste humain, liste, jamais automatise.
rem
rem LES 6 PIECES EMBARQUEES [sha256 gravees - la transparence] :
rem   772f3a315ac19e531015634036d817873687a94f85ab8105f43067bf5f9d430b  sequestre-d183\LANCER-SEQUESTRE-D183.bat
rem   b2d193af954ba35ea0ab859073f4f811f624ba64abc35385fad97812ffd4d94b  sequestre-d183\scripts\kit_ceremonie_d183\AUTOTEST.txt
rem   3de0d44c56d713d742df501cf50f1777cbb247b88a3ef60ac08cedd48331f48c  sequestre-d183\scripts\kit_ceremonie_d183\LISEZMOI-ceremonie-D183.txt
rem   2d950634a57d1afe9834f882b157b42cc21081de9e1bfab99b2e028edd1a7908  sequestre-d183\scripts\kit_ceremonie_d183\sequestre_d183.py
rem   603ab952b45243fa1d82b1fd0b4321a7e9af8cf97feda685d429814e6043f12f  sequestre-d183\v06\coffre_cf2.py
rem   3be740af47faa3e86a4bcafb9b6e3cb65fe0990ad0d0af40526bab9d7c80d3f0  LISEZMOI-1CLIC-sequestre-d183.txt
rem
rem LE PAQUET INTERNE [zip, deflate] : sha256 ef09c1e0e16ef61d2b56c58cb64231e62fa7b4254706e4daaa7b804c0ba3d536
rem ============================================================================
setlocal EnableExtensions
title TRIADE 1-CLIC - le sequestre D183
set "RC=2"
cd /d "%~dp0"

echo ============================================================================
echo  TRIADE 1-CLIC - LE SEQUESTRE D183 - LA CEREMONIE DES 5 PARTS
echo  Un fichier autonome, 6 pieces embarquees, chaque empreinte recoupee
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
set "RUNDIR=%~dp0TRIADE-1CLIC-sequestre-d183-run-%DT%"
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
echo [recoup] sha256 attendu du paquet interne : ef09c1e0e16ef61d2b56c58cb64231e62fa7b4254706e4daaa7b804c0ba3d536
certutil -hashfile "%TRIADE_DESTZIP%" SHA256 > "%TEMP%\triade-1clic-sha.txt" 2>&1
findstr /i "ef09c1e0e16ef61d2b56c58cb64231e62fa7b4254706e4daaa7b804c0ba3d536" "%TEMP%\triade-1clic-sha.txt" >nul
if errorlevel 1 goto paquet_divergent
echo [recoup] paquet interne INTACT.

rem ---- la naissance des pieces ----
powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath $env:TRIADE_DESTZIP -DestinationPath $env:TRIADE_RUNDIR -Force"
if errorlevel 1 goto extraction_refusee
echo [extraction] les 6 pieces sont nees.

rem ---- le recoup de CHAQUE piece [fail-closed : une divergence, rien ne court] ----
call :verifie "sequestre-d183\LANCER-SEQUESTRE-D183.bat" "772f3a315ac19e531015634036d817873687a94f85ab8105f43067bf5f9d430b"
if errorlevel 1 goto piece_divergente
call :verifie "sequestre-d183\scripts\kit_ceremonie_d183\AUTOTEST.txt" "b2d193af954ba35ea0ab859073f4f811f624ba64abc35385fad97812ffd4d94b"
if errorlevel 1 goto piece_divergente
call :verifie "sequestre-d183\scripts\kit_ceremonie_d183\LISEZMOI-ceremonie-D183.txt" "3de0d44c56d713d742df501cf50f1777cbb247b88a3ef60ac08cedd48331f48c"
if errorlevel 1 goto piece_divergente
call :verifie "sequestre-d183\scripts\kit_ceremonie_d183\sequestre_d183.py" "2d950634a57d1afe9834f882b157b42cc21081de9e1bfab99b2e028edd1a7908"
if errorlevel 1 goto piece_divergente
call :verifie "sequestre-d183\v06\coffre_cf2.py" "603ab952b45243fa1d82b1fd0b4321a7e9af8cf97feda685d429814e6043f12f"
if errorlevel 1 goto piece_divergente
echo [recoup] les 6 pieces : INTACTES, octet pour octet.

rem ---- LE LANCEMENT : le lanceur officiel du test, INTACT ----
echo.
echo [lancement] le lanceur officiel : sequestre-d183\LANCER-SEQUESTRE-D183.bat
cd /d "%RUNDIR%"
call sequestre-d183\LANCER-SEQUESTRE-D183.bat
set "RC=%errorlevel%"
cd /d "%~dp0"

echo.
echo ============================================================================
echo  LE TEST EST TERMINE - code %RC%.
echo  Le dossier du run, A RENVOYER ENTIER au coffre /test [Drive "Triade"
echo  puis "test"] :
echo    %RUNDIR%
echo  A VOTRE MAIN : la ceremonie hors-ligne, les cinq medias, la
echo  preuve a froid - jamais rien d'automatise.
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
rem LE PAQUET INTERNE - base64 du zip des 6 pieces [deflate].
rem Toute la transparence : decompressible par quiconque le desire.
rem ============================================================================
<<<TRIADE-PAQUET-INTERNE>>>
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
hnduOVcrfQwxVYPGHddmQ+bmPdUQSuvAmlQ+11RGx88GGPkn9YbRHNA4Sk6DJB1zMJ5R+uGQfLrU
2tLMIcZz1m3v3y/gDdz1vBmVkUkaOpw65TbnYxQcsAZMHvg5OIOEvvql8c2cRecYHlNayNXjlqOa
N3AZH6IHrs5+1Og/dE4+dlS2J/Qn7g/VfHgh7/sIrmoiSD6gknZ1n1+tekbldM2bUemprGc0m4z5
Ok6Lpp9qVquBlhDNA1q5zWmoI7yK5ZquUhX6+qTPxq50Mq55aJRWOA2SzDpv56BTB0+fzhSUm55h
as8XYlUCOA+v0idODcF2xzPubFGakmmOctl9Dsmn6J9XTemV/bCYXnI4nI8K6YE3j80p87vCBD7Q
psNM+Dn7Y2AC889GZapTR6WV6onlHqj2zs/gCDrDTVhmmg1A7Cw6JSlNs1JTpTLYiaVW0V+c7cyv
cBiWcLC/GODBAnEZVxtlVmijNYDyOEx7c++gk/2hSQBjpbroBtPtorna63ZxwN2ux81j7XAa5T6j
obbyfwFQSwECFAMUAAAACAAAYG1dmI3y50wFAAATCgAAIQAAAAAAAAAAAAAApAEAAAAATElTRVpN
T0ktMUNMSUMtc2VxdWVzdHJlLWQxODMudHh0UEsBAhQDFAAAAAgAAGBtXWD9RsoNCQAAwhgAACgA
AAAAAAAAAAAAAKQBiwUAAHNlcXVlc3RyZS1kMTgzL0xBTkNFUi1TRVFVRVNUUkUtRDE4My5iYXRQ
SwECFAMUAAAACAAAYG1dOSQddWMCAAAVBgAANgAAAAAAAAAAAAAApAHeDgAAc2VxdWVzdHJlLWQx
ODMvc2NyaXB0cy9raXRfY2VyZW1vbmllX2QxODMvQVVUT1RFU1QudHh0UEsBAhQDFAAAAAgAAGBt
XR+VC+mmCAAASBEAAEUAAAAAAAAAAAAAAKQBlREAAHNlcXVlc3RyZS1kMTgzL3NjcmlwdHMva2l0
X2NlcmVtb25pZV9kMTgzL0xJU0VaTU9JLWNlcmVtb25pZS1EMTgzLnR4dFBLAQIUAxQAAAAIAABg
bV3qJXt7qA8AAL0nAAA7AAAAAAAAAAAAAACkAZ4aAABzZXF1ZXN0cmUtZDE4My9zY3JpcHRzL2tp
dF9jZXJlbW9uaWVfZDE4My9zZXF1ZXN0cmVfZDE4My5weVBLAQIUAxQAAAAIAABgbV0Yl158l0EA
AFvwAAAgAAAAAAAAAAAAAACkAZ8qAABzZXF1ZXN0cmUtZDE4My92MDYvY29mZnJlX2NmMi5weVBL
BQYAAAAABgAGADMCAAB0bAAAAAA=
