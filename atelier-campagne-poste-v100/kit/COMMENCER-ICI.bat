@echo off
rem ============================================================================
rem TRIADE — LE KIT DE CAMPAGNE AU POSTE RÉEL (v100) — LE CLIC UNIQUE
rem ----------------------------------------------------------------------------
rem Ce fichier trouve Python, bât le venv, installe les dépendances du harnais
rem (llguidance + tokenizers + keystone-engine + capstone) et ouvre la GUI.
rem Le MODE-A (transformers in-process) exige en sus torch + transformers :
rem la commande exacte vit au LISEZMOI-CAMPAGNE-POSTE.txt § 3.
rem ============================================================================
setlocal
cd /d "%~dp0"

echo [1/4] le Python du poste...
set PY=
py -3 -X -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 5)" >nul 2>&1
if not errorlevel 1 set PY=py -3
if not defined PY (
    python -X utf8 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 5)" >nul 2>&1
    if not errorlevel 1 set PY=python
)
if not defined PY (
    echo [ROUGE] Python 3.10+ introuvable. Installe-le depuis python.org
    echo         (coche « Add python.exe to PATH »), puis relance ce fichier.
    pause & exit /b 3
)

echo [2/4] le venv du kit...
if not exist ".venv\Scripts\python.exe" (
    %PY% -m venv .venv
    if errorlevel 1 (echo [ROUGE] la création du venv a échoué & pause & exit /b 3)
)
set VPY=.venv\Scripts\python.exe

echo [3/4] les dépendances du harnais (llguidance, tokenizers, keystone, capstone)...
%VPY% -m pip install --quiet llguidance tokenizers keystone-engine capstone
if errorlevel 1 (
    echo [ROUGE] l'installation des dépendances a échoué — vérifie la connexion
    pause & exit /b 3
)

echo [4/4] la GUI s'ouvre...
%VPY% -X utf8 gui_campagne.py
if errorlevel 1 pause
endlocal
