@echo off
rem ============================================================================
rem SURVEILLANT-CPU.bat - LE COCKPIT DU POSTE DE TEST (v1.0.1, 25/11/2026)
rem
rem La commande du developpeur : une GUI type cpu-z qui affiche et log les
rem valeurs de frequence cpu etc... en temps reel, DURANT les tests.
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Ce cockpit vit par PowerShell 5.1 (livre
rem avec Windows 10 et 11 - AUCUNE installation). Il affiche et journalise
rem la frequence de chaque coeur, la charge, la temperature ; ses boutons
rem lancent les kits TELS QUELS ; le temoin se compose tout seul.
rem
rem OU VIVRE : au RACINE du kit terrain (a cote de COMMENCER-ICI.bat) -
rem c'est la qu'il trouve pc-windows\kit-2-dudect\LANCER-KIT-2-DUDECT.bat
rem et ses freres. Voyez LISEZMOI-surveillant.txt.
rem ============================================================================
cd /d "%~dp0"
where powershell >nul 2>&1
if errorlevel 1 goto sans-powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0surveillant-cpu.ps1"
exit /b %errorlevel%

:sans-powershell
echo [REFUS] PowerShell est introuvable - ce cockpit vit par PowerShell,
echo         livre avec Windows 10 et 11. Rien ne peut le remplacer.
pause
exit /b 2
