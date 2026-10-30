@echo off
rem TRIADE - lanceur du GUI DE CEREMONIE DE MIGRATION CF2 - CF3 (D127)
rem ---------------------------------------------------------------------
rem A garder A LA RACINE d'un clone du depot (a cote de v06\), ou du kit
rem de ceremonie du Drive (le kit porte v06\ entier depuis D122), puis
rem double-clic. Le GUI vit dans <racine>\v06\ : il trouve coffre_cf3.py
rem par sa position. Ordre de recherche :
rem v06\migration_cf3_gui.py (depot complet ou kit du Drive) d'abord,
rem puis toute copie posee a cote (copie plate).
cd /d "%~dp0"
set GUI=
if exist v06\migration_cf3_gui.py set GUI=v06\migration_cf3_gui.py
if not defined GUI if exist migration_cf3_gui.py set GUI=migration_cf3_gui.py
if not defined GUI (
    echo migration_cf3_gui.py introuvable ^(ni v06\migration_cf3_gui.py ni .\migration_cf3_gui.py^).
    echo Ce lanceur vit a la racine d'un CLONE du depot triade ^(celui qui contient v06\^)
    echo ou du kit de ceremonie du Drive.
    pause
    exit /b 1
)
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%GUI%" %*
) else (
    python "%GUI%" %*
)
if errorlevel 1 pause
