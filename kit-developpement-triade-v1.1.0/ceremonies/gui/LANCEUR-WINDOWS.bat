@echo off
setlocal
title Triade Kit - Git / Drive / Zenodo
cd /d "%~dp0"

py -3 -c "import sys" >nul 2>nul
if not errorlevel 1 (
  py -3 TriadeKit.py
  goto fin
)

python -c "import sys" >nul 2>nul
if not errorlevel 1 (
  python TriadeKit.py
  goto fin
)

echo [!] Python 3 est introuvable sur cette machine.
echo     Installez-le depuis https://www.python.org/downloads/
echo     en cochant "Add Python to PATH" pendant l'installation,
echo     puis relancez ce fichier.
echo.
pause
exit /b 1

:fin
if errorlevel 1 pause
