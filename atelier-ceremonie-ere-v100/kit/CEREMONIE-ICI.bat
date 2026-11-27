@echo off
rem ============================================================================
rem TRIADE — LE KIT DE LA CÉRÉMONIE D'ÈRE DE couloir-vaes512.asm (v100)
rem — LE CLIC UNIQUE (côté dépôt, la clé vit hors-ligne) —
rem ============================================================================
setlocal
cd /d "%~dp0"

echo [1/2] le Python du poste...
set PY=
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 5)" >nul 2>&1
if not errorlevel 1 set PY=py -3
if not defined PY (
    python -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 5)" >nul 2>&1
    if not errorlevel 1 set PY=python
)
if not defined PY (
    echo [ROUGE] Python 3.8+ introuvable. Installe-le depuis python.org
    echo         (coche « Add python.exe to PATH »), puis relance ce fichier.
    pause & exit /b 3
)

echo [2/2] la GUI s'ouvre (tkinter seul — aucune dépendance)...
%PY% -X utf8 gui_ceremonie.py
if errorlevel 1 pause
endlocal
