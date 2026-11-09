@echo off
rem ============================================================================
rem temoin-vitrine.bat - LE TMOIN VITRINE DU KIT LOUPE dev.5 (l'Entr‚e 207)
rem
rem La vitrine a VECU sa premiŠre fois au terrain et sa mort fut SANS t‚moin :
rem ® la fenˆtre s'ouvre et se referme imm‚diatement ¯. CE TMOIN nomme :
rem le run console de la vitrine, LES DEUX fa‡ons (sans fichier, puis avec
rem un fichier), le CODE DE SORTIE captur‚ -
rem    0xC0000005  un crash (le rapport WER du systŠme le nomme : le
rem                chemin est consign‚ ci-dessous)
rem    1           la vitrine impossible s'est EXPLIQUE (MessageBox)
rem    0           la sortie propre (Alt+F4/WM_QUIT)
rem Les piŠces vont au r‚ceptacle preuves-loupe\ - … renvoyer au coffre
rem /test AVEC le reste du r‚ceptacle, quelle que soit l'issue.
rem ============================================================================
setlocal
cd /d "%~dp0"
if not exist preuves-loupe mkdir preuves-loupe

echo === LE TEMOIN VITRINE - loupe.exe 0.1.0-dev.5 === > preuves-loupe\temoin-vitrine.txt
ver >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [1/3] LA VITRINE VIDE (double-clique sans fichier)...
echo [1/3] LA VITRINE VIDE - code de sortie ci-dessous >> preuves-loupe\temoin-vitrine.txt
loupe.exe
echo code de sortie = %ERRORLEVEL% >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [2/3] LA VITRINE AVEC FICHIER (une COPIE : la session nait entiere)...
echo [2/3] LA VITRINE AVEC FICHIER (loupe.exe temoin-fichier.bin) - code de sortie ci-dessous >> preuves-loupe\temoin-vitrine.txt
copy /y loupe.exe temoin-fichier.bin >nul
loupe.exe temoin-fichier.bin
echo code de sortie = %ERRORLEVEL% >> preuves-loupe\temoin-vitrine.txt
echo. >> preuves-loupe\temoin-vitrine.txt

echo [3/3] LE RAPPORT WER (si un crash fut consigne)...
echo [3/3] LES RAPPORTS WER RECENTS (les 5 derniers) : >> preuves-loupe\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportArchive" 2>nul | findstr /i "loupe" >> preuves-loupe\temoin-vitrine.txt
dir /b /o-d "%LOCALAPPDATA%\Microsoft\Windows\WER\ReportQueue" 2>nul | findstr /i "loupe" >> preuves-loupe\temoin-vitrine.txt

echo.
echo LE TEMOIN VITRINE ECRIT : preuves-loupe\temoin-vitrine.txt
echo Renvoyez le dossier preuves-loupe\ ENTIER au coffre /test du drive.
pause
