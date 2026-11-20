@echo off
rem ============================================================================
rem temoin-vitrine.bat - LE TEMOIN VITRINE DU KIT LOUPE (Entree 221, l'ere 0.1.1)
rem
rem La vitrine a vecu TROIS fois SANS temoin : "la fenetre s'ouvre et se
rem referme immediatement" - jamais plus. CE TEMOIN nomme chaque mort :
rem    0xC0000005  un crash (le rapport WER du systeme le nomme alors)
rem    1           la vitrine impossible s'est EXPLIQUEE (MessageBox)
rem    0           la sortie propre (Alt+F4 / WM_QUIT)
rem
rem LE GESTE : double-cliquez. La PREMIERE fenetre s'ouvre VIDE (l'usage a
rem la barre d'etat) : fermez-la par Alt+F4. La SECONDE s'ouvre AVEC le
rem fichier temoin-fichier.bin (l'entete des colonnes, les lignes hexa,
rem le miroir ASCII, le panneau d'empreintes md5 + sha256) : fermez-la par
rem Alt+F4. Les DEUX codes de sortie sont consignes au temoin
rem preuves-loupe\temoin-vitrine.txt. RENVOYEZ le dossier preuves-loupe\
rem ENTIER au coffre /test du drive, QUEL QUE SOIT le verdict.
rem ============================================================================
setlocal
cd /d "%~dp0"
if not exist loupe.exe (
    echo [temoin] REFUS : loupe.exe ABSENT du dossier du kit - kit corrupt,
    echo           extrayez le zip COMPLET dans un dossier NEUF ^(D99^).
    pause
    exit /b 2
)
if not exist preuves-loupe mkdir preuves-loupe

echo === LE TEMOIN VITRINE - loupe.exe 0.1.1-dev.1 ^(kit 0.1.1-dev.1, Entree 221^) === > preuves-loupe\temoin-vitrine.txt
ver >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [1/4] LA VITRINE VIDE (sans fichier) : la fenetre s'ouvre...
echo       la barre d'etat porte l'usage ; FERMEZ la fenetre par Alt+F4.
loupe.exe
echo [1/4] LA VITRINE VIDE - code de sortie ci-dessous >> preuves-loupe\temoin-vitrine.txt
echo code de sortie = %ERRORLEVEL% >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [2/4] LA VITRINE AVEC FICHIER (une COPIE : la session nait entiere)...
copy /y loupe.exe temoin-fichier.bin >nul
loupe.exe temoin-fichier.bin
echo [2/4] LA VITRINE AVEC FICHIER (loupe.exe temoin-fichier.bin) - code de sortie ci-dessous >> preuves-loupe\temoin-vitrine.txt
echo code de sortie = %ERRORLEVEL% >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [3/4] LE RAPPORT WER (si un crash fut consigne)...
echo [3/4] LES RAPPORTS WER RECENTS (les 5 derniers) : >> preuves-loupe\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive" 2>nul | findstr /i "loupe" >> preuves-loupe\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportQueue" 2>nul | findstr /i "loupe" >> preuves-loupe\temoin-vitrine.txt

echo [4/4] LE JOURNAL D EVENEMENTS (la piece nommee par le systeme)...
echo. >> preuves-loupe\temoin-vitrine.txt
echo [4/4] LE JOURNAL D EVENEMENTS - Application Error 1000 : le module fautif et le decalage de l exception NOMMES ci-dessous : >> preuves-loupe\temoin-vitrine.txt
wevtutil qe Application /q:"*[System[(EventID=1000 or EventID=1001)]]" /c:3 /rd:true /f:text >> preuves-loupe\temoin-vitrine.txt 2>nul

echo.
echo LE TEMOIN VITRINE ECRIT : preuves-loupe\temoin-vitrine.txt
echo RENVOYEZ le dossier preuves-loupe\ ENTIER au coffre /test du drive
echo (dossier Triade), avec temoin-loupe.txt et les captures eventuelles.
pause
