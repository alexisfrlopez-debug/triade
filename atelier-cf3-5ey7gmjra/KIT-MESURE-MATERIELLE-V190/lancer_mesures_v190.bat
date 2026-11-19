@echo off
REM lancer_mesures_v190.bat — LE PILOTE PRÉ-ENREGISTRÉ (Windows, le terrain)
REM n^>=10 exécutions par N dans {60, 200, 400}, le mesureur scellé TEL QUEL
setlocal enabledelayedexpansion
set CIBLES=%1
if "%CIBLES%"=="" set CIBLES=cibles
set DUD=%2
if "%DUD%"=="" set DUD=dudect_v150.exe
if not exist journaux-v190 mkdir journaux-v190
(
  echo === EMPREINTE MACHINE ^((gravée avant la première exécution^)) ===
  ver
  wmic cpu get name 2>nul
  powercfg /getactivescheme
) > journaux-v190\empreinte-machine.txt
for %%N in (60 200 400) do (
  for /L %%i in (1,1,10) do (
    echo === exécution %%i/10 à N=%%N ===
    %DUD% %CIBLES% %%N > journaux-v190\run-N%%N-%%i.log 2>&1
    type journaux-v190\run-N%%N-%%i.log
  )
)
echo LES SÉRIES VÉCUES — agréger : python3 agreger_mesures_v190.py journaux-v190
