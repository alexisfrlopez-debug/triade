@echo off
rem TRIADE - Pousseur Zenodo v0.31.0 - le clic unique.
rem Double-cliquer ce fichier : la fenetre s'ouvre, UN CLIC sur le bouton vert
rem pousse le protocole v0.31.0 (trois packs) et la participation v1.2.0.
setlocal
cd /d "%~dp0"
title TRIADE - Pousseur Zenodo v0.31.0 (1 clic)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0gui_zenodo.ps1"
if errorlevel 1 (
  echo.
  echo La fenetre s'est fermee avec une erreur. Relance, ou lis PUSHER-JOURNAL.log.
  pause
)
endlocal
