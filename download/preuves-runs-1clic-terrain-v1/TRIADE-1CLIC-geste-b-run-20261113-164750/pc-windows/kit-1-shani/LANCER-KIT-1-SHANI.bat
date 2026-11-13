@echo off
rem ============================================================================
rem LANCER-KIT-1-SHANI.bat - LE LANCEUR DU KIT 1 (l'edition AUTOMATISEE du
rem paquet multimachines, 12/11/2026 - la commande du developpeur : 'je veux
rem que l'utilisation soit la plus simple possible, en automatisant au
rem maximum').
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Ce lanceur fait pour vous les gestes 1 a 4 du
rem LISEZMOI-shani.txt : il verifie les pieces, trouve Python (py/python/
rem python3 - dans cet ordre), lance le scenario T0-T5 et vous dit OU sont
rem les preuves. RIEN A COMPILER : le moteur-shani.bin est LIVRE et son
rem sha256 est asserte par le scenario lui-meme.
rem
rem Ce qui reste a VOTRE main (et n'appartient qu'a vous) : dater et signer
rem la ligne 'signature du geste' du temoin, puis renvoyer le dossier
rem preuves-shani\ ENTIER au coffre /test (dossier Drive 'Triade').
rem ============================================================================

setlocal EnableExtensions
title TRIADE - kit 1 shani (la mesure avant/apres SHA-NI)
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LE KIT 1 SHANI - correctif n.o 2 (D206) - le paquet multimachines AUTO
echo  Le scenario T0-T5 : l'avant scalaire (tls13-02) contre l'apres SHA-NI
echo  (shani_compress), 101 echantillons x 256 compressions, coeur 0, RDTSC.
echo  Refus nomme si le silicium n'a pas SHA-NI : UN RESULTAT, pas une panne.
echo ============================================================================

rem ---- les pieces (un kit incomplet est un refus nomme, jamais un crash) ----
if not exist scenario-shani.py goto piece_absente
if not exist moteur-shani.bin goto piece_absente
if not exist cibles\proxy-image.bin goto piece_absente
if not exist cibles\manifeste.json goto piece_absente
echo [pieces] scenario-shani.py + moteur-shani.bin + cibles\ : presents.

rem ---- Python (aucun paquet a installer, un Python 3 suffit) ----
set "PY="
py -3 -c "import sys" >nul 2>&1 && set "PY=py -3"
if not defined PY python -c "import sys" >nul 2>&1 && set "PY=python"
if not defined PY python3 -c "import sys" >nul 2>&1 && set "PY=python3"
if not defined PY goto python_absent
echo [python] trouve : %PY%

rem ---- LE RUN (une a deux minutes, chaque geste s'imprime) ----
echo.
echo [run] %PY% scenario-shani.py  -  une a deux minutes, ne fermez pas...
echo.
%PY% scenario-shani.py
set "RC=%errorlevel%"

echo.
echo ============================================================================
if "%RC%"=="0" (
    echo  LE VERDICT : code %RC% - VERT. Les preuves vivent dans preuves-shani\
) else (
    echo  LE VERDICT : code %RC% - un ECHEC NOMME est un RESULTAT : renvoyez
    echo  le dossier preuves-shani\ TEL QUEL, le labo recoupe sur pieces.
)
echo  preuves-shani\temoin-shani.txt      le temoin complet
echo  preuves-shani\VERDICT-run-shani.txt le verdict auto-portant
echo.
echo  A VOTRE MAIN : datez et signez la ligne 'signature du geste' du
echo  temoin, puis renvoyez preuves-shani\ ENTIER au coffre /test.
echo ============================================================================
pause
exit /b %RC%

:piece_absente
echo.
echo [REFUS] une piece du kit est ABSENTE - extrayez le zip COMPLET dans un
echo         dossier NEUF ^(D99, ne melangez jamais les runs^).
pause
exit /b 2

:python_absent
echo.
echo [REFUS] Python 3 est INTROUVABLE (py / python / python3 essayes).
echo         Installez-le depuis https://www.python.org (cochez 'Add to PATH')
echo         puis relancez ce lanceur. Aucun autre outil n'est requis.
pause
exit /b 2
