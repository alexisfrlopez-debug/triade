@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set RAPPORT=rapport-diagnostic3.txt
echo ============================================================ > %RAPPORT%
echo DIAGNOSTIC 3 SUPERVISEUR TRIADE > %RAPPORT%
echo %date% %time% >> %RAPPORT%
echo ============================================================ >> %RAPPORT%

net session > nul 2>&1
if !errorlevel! equ 0 (set ADMIN=OUI) else (set ADMIN=NON)
echo Session administrateur : !ADMIN! >> %RAPPORT%

echo [1/8] Version Windows...
ver >> %RAPPORT% 2>&1

echo [2/8] Empreintes des fichiers attendus...
echo. >> %RAPPORT%
echo --- md5 attendus --- >> %RAPPORT%
echo   superviseur-terrain4.exe          = 283895dbede5245deddffcfd84c1ec32 ^<-- CORRECTIF >> %RAPPORT%
echo   superviseur-p4-messagebox.exe     = ee7e7364e7db1252c6cb46c6ea1783f5 >> %RAPPORT%
echo   superviseur-p1-sans-horodatage.exe= ee18e45922c130116d2e53e1d577d4b3 >> %RAPPORT%
echo   superviseur-p3-defwndproc.exe     = 91ec5860ac3f635b9ae57abcaafa9d23 >> %RAPPORT%
echo   superviseur-terrain3-temoin.exe   = 40b2f350ad8556d028d431174d429189 >> %RAPPORT%
echo   demo.exe                          = 73c064fbaf4610a167bc6434dee400e4 >> %RAPPORT%
for %%F in (superviseur-terrain4.exe superviseur-p4-messagebox.exe superviseur-p1-sans-horodatage.exe superviseur-p3-defwndproc.exe superviseur-terrain3-temoin.exe demo.exe) do (
  if exist "%%F" (
    echo --- md5 %%F --- >> %RAPPORT%
    certutil -hashfile "%%F" MD5 >> %RAPPORT% 2>&1
  ) else (
    echo !!! %%F ABSENT du dossier >> %RAPPORT%
  )
)

echo [3/8] Journal d evenements : plantages Application Error (ID 1000)...
echo. >> %RAPPORT%
echo === PLANTAGES ENREGISTRES (20 derniers, module fautif + offset) === >> %RAPPORT%
wevtutil qe Application /q:"*[System[(EventID=1000)]]" /c:20 /rd:true /f:text >> %RAPPORT% 2>&1

echo [4/8] Echelle de sondes (6 secondes chacune)...
echo. >> %RAPPORT%
echo === ECHELLE DE SONDES === >> %RAPPORT%
echo terrain4 = correctif ; p4 = MessageBox au demarrage ; p1 = sans horodatage ; >> %RAPPORT%
echo p3 = fenetre vide (DefWindowProcW) ; terrain3-temoin = crash connu ; demo = reference. >> %RAPPORT%
echo Un exe VIVANT apres 6 s = sa fenetre est apparue = il FONCTIONNE. >> %RAPPORT%
for %%F in (superviseur-terrain4.exe superviseur-p4-messagebox.exe superviseur-p1-sans-horodatage.exe superviseur-p3-defwndproc.exe superviseur-terrain3-temoin.exe demo.exe) do (
  if exist "%%F" (
    echo. >> %RAPPORT%
    echo --- sonde : %%F --- >> %RAPPORT%
    taskkill /im "%%F" > nul 2>&1
    start "" "%%F"
    timeout /t 6 /nobreak > nul
    tasklist /fi "IMAGENAME eq %%F" 2>nul | find /i "%%F" > nul
    if !errorlevel! equ 0 (
      echo RESULTAT : VIVANT apres 6 s ^(fenetre visible^) - FONCTIONNE >> %RAPPORT%
      taskkill /im "%%F" >> %RAPPORT% 2>&1
    ) else (
      echo RESULTAT : MORT avant 6 s ^(crash ou blocage^) >> %RAPPORT%
    )
  ) else (
    echo --- sonde %%F : FICHIER ABSENT --- >> %RAPPORT%
  )
)

echo. >> %RAPPORT%
echo Interpretation : >> %RAPPORT%
echo  - terrain4 VIVANT = CORRECTIF VALIDE, la fenetre du superviseur marche. >> %RAPPORT%
echo  - p4 MORT = meme le premier appel API echoue (chargeur/IAT) ; >> %RAPPORT%
echo    p4 VIVANT + p1 MORT = le crash est AVANT la fenetre, hors horodatage ; >> %RAPPORT%
echo    p1 VIVANT = le crash est l appel GetLocalTime (slot 0x2328) ; >> %RAPPORT%
echo    p1 MORT + p3 VIVANT = le crash est dans la chaine wndproc/journal ; >> %RAPPORT%
echo    p3 MORT = le crash est dans la creation de fenetre elle-meme ; >> %RAPPORT%
echo    demo MORT = la machine casse AUSSI la reference (autre probleme). >> %RAPPORT%

echo [5/8] Activation des dumps au prochain crash (LocalDumps)...
echo. >> %RAPPORT%
echo === LOCALDUMPS === >> %RAPPORT%
for %%F in (superviseur-terrain4.exe superviseur-terrain3-temoin.exe) do (
  reg add "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\%%F" /v DumpFolder /t REG_EXPAND_SZ /d "%%LOCALAPPDATA%%\CrashDumps" /f >> %RAPPORT% 2>&1
  reg add "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\%%F" /v DumpType /t REG_DWORD /d 2 /f >> %RAPPORT% 2>&1
  reg add "HKLM\SOFTWARE\Microsoft\Windows\Windows Error Reporting\LocalDumps\%%F" /v DumpCount /t REG_DWORD /d 3 /f >> %RAPPORT% 2>&1
)
if "!ADMIN!"=="NON" echo !!! Session NON admin : dumps probablement NON actives ^(relancer en administrateur si crash^) >> %RAPPORT%

echo [6/8] Etat Defender + 15 dernieres detections...
echo. >> %RAPPORT%
echo === ETAT DEFENDER === >> %RAPPORT%
powershell -NoProfile -Command "Get-MpComputerStatus | Select-Object AMServiceEnabled,RealTimeProtectionEnabled,BehaviorMonitorEnabled,AntivirusEnabled | Format-List" >> %RAPPORT% 2>&1
echo. >> %RAPPORT%
echo === DEFENDER : 15 dernieres detections === >> %RAPPORT%
powershell -NoProfile -Command "Get-MpThreatDetection | Select-Object -First 15 InitialDetectionTime,ProcessName,Resources | Format-List" >> %RAPPORT% 2>&1

echo [7/8] Journaux terrain produits...
echo. >> %RAPPORT%
echo === JOURNAUX terrain_*.txt === >> %RAPPORT%
dir /b terrain_*.txt >> %RAPPORT% 2>&1
for %%F in (terrain_*.txt) do (
  echo. >> %RAPPORT%
  echo --- contenu %%F --- >> %RAPPORT%
  type "%%F" >> %RAPPORT% 2>&1
)

echo [8/8] Dossier de dumps...
echo. >> %RAPPORT%
echo === %LOCALAPPDATA%\CrashDumps === >> %RAPPORT%
dir "%LOCALAPPDATA%\CrashDumps" >> %RAPPORT% 2>&1

echo. >> %RAPPORT%
echo ============================================================ >> %RAPPORT%
echo FIN DU DIAGNOSTIC 3 >> %RAPPORT%
echo. >> %RAPPORT%
echo TERMINE. Deposez rapport-diagnostic3.txt (et terrain_*.txt + >> %RAPPORT%
echo les fichiers .dmp de %%LOCALAPPDATA%%\CrashDumps s il y en a) dans >> %RAPPORT%
echo le dossier test du Drive. >> %RAPPORT%
echo.
pause
