@echo off
rem ============================================================
rem DIAGNOSTIC SUPERVISEUR TRIADE - v1 - 27/10/2026
rem A poser dans le MEME dossier que superviseur-terrain3.exe,
rem puis double-clic. Produit rapport-diagnostic.txt.
rem ============================================================

setlocal
set RAP=rapport-diagnostic.txt
set EXE=superviseur-terrain3.exe

> "%RAP%" echo ============================================================
>>"%RAP%" echo DIAGNOSTIC SUPERVISEUR TRIADE - %date% %time%
>>"%RAP%" echo ============================================================

>>"%RAP%" echo.
>>"%RAP%" echo [0] VERSION WINDOWS
ver >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [1] PRESENCE DU FICHIER AVANT LANCEMENT
>>"%RAP%" echo Fichier attendu : %EXE%
if exist "%EXE%" (
>>"%RAP%" echo RESULTAT : le fichier EST present
) else (
>>"%RAP%" echo RESULTAT : le fichier est ABSENT - probablement mis en quarantaine
)
dir /b superviseur*.exe >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [2] EMPREINTE MD5 - attendu 40b2f350ad8556d028d431174d429189
if exist "%EXE%" certutil -hashfile "%EXE%" MD5 >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [3] MARQUE DU WEB - Zone.Identifier
type "%EXE%:Zone.Identifier" >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [4] ETAT DE DEFENDER
powershell -NoProfile -Command "Get-MpComputerStatus | Select-Object AMServiceEnabled,RealTimeProtectionEnabled,AntivirusEnabled,BehaviorMonitorEnabled | Format-List" >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [5] HISTORIQUE DE PROTECTION - 8 dernieres menaces
powershell -NoProfile -Command "Get-MpThreatDetection -ErrorAction SilentlyContinue | Sort-Object InitialDetectionTime -Descending | Select-Object -First 8 InitialDetectionTime,ProcessName,Resources | Format-List" >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [6] CRASHS APPLICATIFS RECENTS - 48 dernieres heures
powershell -NoProfile -Command "Get-WinEvent -FilterHashtable @{LogName='Application'; Id=1000; StartTime=(Get-Date).AddHours(-48)} -MaxEvents 8 -ErrorAction SilentlyContinue | Select-Object TimeCreated, Message | Format-List" >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo [7] LANCEMENT SURVEILLE
>>"%RAP%" echo Si une fenetre TRIADE apparait : fermez-la pour laisser le script finir.
start /wait "" "%EXE%"
>>"%RAP%" echo CODE DE SORTIE : %ERRORLEVEL%
if exist "%EXE%" (
>>"%RAP%" echo Le fichier est TOUJOURS present apres le lancement
) else (
>>"%RAP%" echo LE FICHIER A DISPARU APRES LE LANCEMENT - mis en quarantaine
)

>>"%RAP%" echo.
>>"%RAP%" echo [8] CONTENU DU DOSSIER APRES LANCEMENT
dir >>"%RAP%" 2>&1

>>"%RAP%" echo.
>>"%RAP%" echo FIN DU DIAGNOSTIC
>>"%RAP%" echo Deposez rapport-diagnostic.txt dans le dossier test du Drive.

echo.
echo ============================================================
echo  Diagnostic termine : %RAP% vient d'etre cree ici.
echo  Deposez ce fichier dans le dossier test du Drive.
echo ============================================================
type "%RAP%"
pause
