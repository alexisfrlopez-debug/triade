@echo off
rem TRIADE - lanceur du MAITRE DE CEREMONIE (D118, edition depot git)
rem ---------------------------------------------------------------------
rem A garder A LA RACINE d'un clone du depot (a cote de v06/), puis
rem double-clic. Le GUI vit dans <depot>\v06\ : il trouve le depot par
rem sa position. Ordre de recherche : v06\ceremonie_gui.py (depot
rem complet) d'abord, puis toute copie posee a cote (kit du Drive
rem reduit, copie "fichier seul sur clef USB" - profil hors-ligne pur).
cd /d "%~dp0"
set GUI=
if exist v06\ceremonie_gui.py set GUI=v06\ceremonie_gui.py
if not defined GUI if exist ceremonie_gui.py set GUI=ceremonie_gui.py
if not defined GUI (
    echo ceremonie_gui.py introuvable ^(ni v06\ceremonie_gui.py ni .\ceremonie_gui.py^).
    echo Ce lanceur vit a la racine d'un CLONE du depot triade ^(celui qui contient v06/^).
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
