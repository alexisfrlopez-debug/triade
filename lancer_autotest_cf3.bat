@echo off
rem TRIADE - lanceur du PUPITRE D'AUTOTEST CF3 (D122)
rem ---------------------------------------------------------------------
rem A garder A LA RACINE d'un clone du depot (a cote de v06\), ou du kit
rem de ceremonie du Drive (le kit porte v06\ entier depuis D122), puis
rem double-clic. Le pupitre vit dans <racine>\v06\ : il trouve
rem coffre_cf3.py par sa position. Ordre de recherche :
rem v06\autotest_cf3_gui.py (depot complet ou kit du Drive) d'abord,
rem puis toute copie posee a cote (copie plate - seul l'autotest
rem embarque 28 est alors disponible, la suite complete exige le
rem dossier v06\).
cd /d "%~dp0"
set PUPITRE=
if exist v06\autotest_cf3_gui.py set PUPITRE=v06\autotest_cf3_gui.py
if not defined PUPITRE if exist autotest_cf3_gui.py set PUPITRE=autotest_cf3_gui.py
if not defined PUPITRE (
    echo autotest_cf3_gui.py introuvable ^(ni v06\autotest_cf3_gui.py ni .\autotest_cf3_gui.py^).
    echo Ce lanceur vit a la racine d'un CLONE du depot triade ^(celui qui contient v06\^)
    echo ou du kit de ceremonie du Drive.
    pause
    exit /b 1
)
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%PUPITRE%" %*
) else (
    python "%PUPITRE%" %*
)
if errorlevel 1 pause
