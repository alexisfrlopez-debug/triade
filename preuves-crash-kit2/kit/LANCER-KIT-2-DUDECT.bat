@echo off
rem ============================================================================
rem LANCER-KIT-2-DUDECT.bat - LE LANCEUR DU KIT 2 (l'edition MISE A JOUR du
rem paquet multimachines, 12/11/2026 - la commande du developpeur : 'fais un
rem kit mis a jour avec ce qu'il reste a faire ou des corrections si
rem necessaires, ou eventuellement rajouter des tests si tu trouve ca
rem pertinent').
rem
rem LE GESTE : DOUBLE-CLIQUEZ. Ce lanceur fait pour vous les gestes du
rem LISEZMOI-dudect.txt SANS VOUS DEMANDER UNE SEULE COMMANDE :
rem   1. il verifie les pieces et recoupe le sha256 de l'image scellee ;
rem   2. SI un compilateur vit sur la machine (cl / gcc / clang), il
rem      RECOMPILE le mesureur et l'epreuve d'appel depuis LA SOURCE (la
rem      source est la verite) ; SINON il execute les exe PRECOMPILES
rem      livres (cross-compiles au labo depuis CETTE meme source) ;
rem   3. il vit l'epreuve d'appel (FIPS 'abc' attendu EXACT) ;
rem   4. LE RUN : dudect_v150 cibles N (N = 200 par defaut ; vous pouvez
rem      passer votre N : LANCER-KIT-2-DUDECT.bat 400 - minimum 60) ;
rem   5. il ecrit temoin-dudect-BROUILLON.txt (machine, CPU, binaire,
rem      empreintes, code de sortie) - A COMPLETER ET A SIGNER DE VOTRE MAIN.
rem
rem LE CORRECTIF N.O 2 (12/11, le premier run terrain) : le kit-2
rem a CRASHE au lancement chez le developpeur - la cause nommee par
rem l'audit : le backend _WIN32 de test_appel.c passait l'image en
rem PAGE_EXECUTE_READ (lecture seule) puis l'epreuve de l'adversaire
rem ECRIT dans la table K - violation d'acces (0xC0000005) au premier
rem run Windows. LA REPARATION : la source passe la page en
rem PAGE_EXECUTE_READWRITE (0x40 - la meme semantique RWX que le
rem backend POSIX, toujours valide au labo), et l'exe precompile est
rem l'exe du labo PATCHED D'UN OCTET (0x20->0x40, l'immediat de
rem mov r8d qui alimente VirtualProtect). dudect_v150.exe est INTACT
rem (il n'ecrit jamais dans l'image protegee).

rem LES CORRECTIONS DE L'EDITION MISE A JOUR (la relecture du labo) :
rem   (a) si l'epreuve d'appel (test_appel) manque a l'extraction, l'ecart
rem       est NOMME a l'ecran et au temoin - l'edition AUTO la sautait en
rem       silence (l'evenement qui l'a motive : le coffre Drive a REFUSE
rem       test_appel.exe le 12/11, HTTP 403 'malware or spam' - un faux
rem       positif des exe de mesure de timing ; votre antivirus local peut
rem       faire de meme A L'EXTRACTION) ;
rem   (b) si le binaire de mesure manque lui-meme : REFUS NOMME (plus
rem       jamais un code 9009 nu) ;
rem   (c) la validation de N est durcie : la ligne de validation ne peut
rem       PLUS EXECUTER aucun texte saisi (l'ancienne passait par un pipe).
rem ============================================================================

setlocal EnableExtensions
title TRIADE - kit 2 dudect (la mesure temps reel des familles crypto)
cd /d "%~dp0"
set "RC=2"

echo ============================================================================
echo  LE KIT 2 DUDECT TEMPS REEL - correctif n.o 2 - paquet CORRECTIF2-kit-dudect
echo  Les quatre familles crypto de la piece scellee (tls13-02, tls13-13,
echo  tls13-16, tls13-17), RDTSC/QPC, affinite coeur 0, t de Welch, |t| > 5.
echo  C'est LA MESURE JAMAIS ENCORE COURUE du paquet (voyez
echo  CE-QUI-RESTE-A-FAIRE.txt).
echo ============================================================================
echo.

rem ---- N par classe (defaut 200, minimum 60 - la commande exige N >= 60) ----
rem (c) la validation SANS EXECUTION : la boucle for /f ne demande rien a
rem     l'interpreteur - un texte saisi n'est jamais execute, juste refuse.
set "N=200"
if not "%~1"=="" set "N=%~1"
set "N_NON_NUM="
for /f "delims=0123456789" %%X in ("%N%") do set "N_NON_NUM=%%X"
if defined N_NON_NUM goto n_invalide
if not "%N:~7%"=="" goto n_invalide
if %N% LSS 60 goto n_invalide
echo [protocole] N = %N% echantillons par classe.

rem ---- les pieces (un kit incomplet est un refus nomme) ----
if not exist dudect_v150.c goto piece_absente
if not exist cibles\proxy-image.bin goto piece_absente
if not exist cibles\manifeste-c.txt goto piece_absente
echo [pieces] dudect_v150.c + cibles\ : presents.

rem ---- le recoup de l'image scellee (le mesureur re-recoupera lui-meme) ----
echo [recoup] sha256 attendu de cibles\proxy-image.bin :
echo          0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff
certutil -hashfile cibles\proxy-image.bin SHA256 > "%TEMP%\triade-sha-image.txt" 2>&1
findstr /i "0782d7e20d0bd4a268e6ec7ed0dc1453a0f42d7e72b784c2acc9ed423a885dff" "%TEMP%\triade-sha-image.txt" >nul
if errorlevel 1 goto image_divergente
echo [recoup] image scellee INTACTE - la piece est la piece du labo.

rem ---- le compilateur : recompiler si possible, sinon les exe livres ----
set "CC="
set "ORIGINE=PRECOMPILE LIVRE (gcc 14-win32 mingw-w64, cross-compile au labo)"
set "BIN=dudect_v150.exe"
set "TBIN=test_appel.exe"
where cl >nul 2>&1 && set "CC=cl"
if not defined CC where gcc >nul 2>&1 && set "CC=gcc"
if not defined CC where clang >nul 2>&1 && set "CC=clang"

if not defined CC goto pas_de_compilateur

echo [compilateur] %CC% trouve : RECOMPILATION depuis la source ^(la verite^).
if not exist run mkdir run
if "%CC%"=="cl" goto compile_cl
%CC% -O2 -o run\dudect_v150.exe dudect_v150.c -lm
if errorlevel 1 goto compilation_echouee
%CC% -O2 -o run\test_appel.exe test_appel.c -lm
goto compilation_faite

:compile_cl
cl /O2 /D_CRT_SECURE_NO_WARNINGS /Fo:run\ /Fe:run\dudect_v150.exe dudect_v150.c
if errorlevel 1 goto compilation_echouee
cl /O2 /D_CRT_SECURE_NO_WARNINGS /Fo:run\ /Fe:run\test_appel.exe test_appel.c

:compilation_faite
if not exist run\dudect_v150.exe goto compilation_echouee
set "BIN=run\dudect_v150.exe"
set "ORIGINE=RECOMPILE SUR CETTE MACHINE (%CC% -O2, depuis la source du kit)"
if exist run\test_appel.exe (set "TBIN=run\test_appel.exe") else (echo [ecart nomme] test_appel non recompile - l'epreuve d'appel vivra avec l'exe PRECOMPILE livre.)
echo [compilation] OK : %BIN%
goto epreuve_appel

:pas_de_compilateur
echo [compilateur] AUCUN (cl / gcc / clang introuvables) : les exe PRECOMPILES
echo               livres courent - ils furent cross-compiles au labo depuis
echo               CETTE meme source, jamais executes au labo ^(aucun Windows
echo               au labo^) : ce run en est le premier temoin.
echo [attention]  si votre ANTIVIRUS retire les exe a l'extraction ^(un faux
echo               positif des exe de mesure de timing - le coffre Drive l'a
echo               vecu le 12/11^), l'ecart sera NOMME plus bas : rien ne se
echo               passe en silence. VERIFIER-PAQUET.bat le dit AVANT, si vous
echo               voulez le savoir d'abord.

rem ---- l'epreuve d'appel (le FIPS 180-4 'abc' depuis l'image mapee) ----
:epreuve_appel
if exist "%TBIN%" goto appel_vivre
rem (a) l'ecart nomme : l'edition AUTO sautait l'epreuve en silence.
echo [ecart nomme] l'epreuve d'appel est PASSEE : "%TBIN%" est ABSENT de
echo               l'extraction ^(l'antivirus ? voyez VERIFIER-PAQUET.bat^) -
echo               le run continue, l'ecart est consigne au temoin ^(D189^).
set "APPEL_PASSEE=oui"
goto run_mesure

:appel_vivre
echo [epreuve d'appel] %TBIN% - attendu : FIPS abc EXACT, mutation K DIVERGE...
"%TBIN%" > sortie-appel.txt 2>&1
set "RCAPPEL=%errorlevel%"
type sortie-appel.txt
if "%RCAPPEL%"=="0" (echo [epreuve d'appel] code %RCAPPEL% - EXACT.) else (echo [epreuve d'appel] code %RCAPPEL% - ECART NOMME : le run continue, la sortie est conservee dans sortie-appel.txt.)

rem ---- LE RUN : la mesure temps reel ----
:run_mesure
rem (b) le binaire absent : REFUS NOMME, jamais un code 9009 nu.
if exist "%BIN%" goto run_vivre
echo.
echo [REFUS nomme] le binaire de mesure "%BIN%" est ABSENT de l'extraction -
echo         l'antivirus l'a probablement retire ^(un faux positif des exe de
echo         mesure de timing - le coffre Drive lui-meme l'a vecu le 12/11^).
echo         Re-extrayez le zip COMPLET dans un dossier NEUF ^(D99^) ; si
echo         l'antivirus retire encore les exe, renvoyez cet ecran TEL QUEL
echo         ^(D122^) - CE-QUI-RESTE-A-FAIRE.txt dit la conduite a tenir.
pause
exit /b 2

:run_vivre
echo.
echo [LE RUN] "%BIN%" cibles %N%  -  l'affichage suit a la fin du run...
"%BIN%" cibles %N% > sortie-run.txt 2>&1
set "RC=%errorlevel%"
type sortie-run.txt
echo [LE RUN] code de sortie : %RC%

rem ---- le journal csv le plus recent ----
set "CSV="
for /f "delims=" %%F in ('dir /b /o-d journal-dudect-*.csv 2^>nul') do if not defined CSV set "CSV=%%F"

rem ---- la machine (collecte automatique pour le brouillon de temoin) ----
set "CPU_NOM="
set "CPU_MHZ="
set "CPU_COEURS="
for /f "usebackq delims=" %%C in (`powershell -NoProfile -Command "(Get-CimInstance Win32_Processor).Name" 2^>nul`) do set "CPU_NOM=%%C"
for /f "usebackq delims=" %%C in (`powershell -NoProfile -Command "(Get-CimInstance Win32_Processor).MaxClockSpeed" 2^>nul`) do set "CPU_MHZ=%%C"
for /f "usebackq delims=" %%C in (`powershell -NoProfile -Command "(Get-CimInstance Win32_Processor).NumberOfCores" 2^>nul`) do set "CPU_COEURS=%%C"
if not defined CPU_NOM set "CPU_NOM=(powershell indisponible - notez le modele a la main)"
if not defined CPU_MHZ set "CPU_MHZ=?"
if not defined CPU_COEURS set "CPU_COEURS=?"

rem ---- LE BROUILLON DE TEMOIN (a completer et a signer de votre main) ----
>  temoin-dudect-BROUILLON.txt echo LE TEMOIN DUDECT - BROUILLON AUTO ^(edition MISE A JOUR du 12/11^)
>> temoin-dudect-BROUILLON.txt echo ============================================================
>> temoin-dudect-BROUILLON.txt echo Le run        : %DATE% %TIME% ^(heure locale de la machine^)
>> temoin-dudect-BROUILLON.txt echo L'OS           :
>> temoin-dudect-BROUILLON.txt echo Le CPU         : %CPU_NOM%
>> temoin-dudect-BROUILLON.txt echo Les coeurs     : %CPU_COEURS%    Frequence annoncee : %CPU_MHZ% MHz
ver >> temoin-dudect-BROUILLON.txt
>> temoin-dudect-BROUILLON.txt echo Le binaire     : %BIN%
>> temoin-dudect-BROUILLON.txt echo L'origine      : %ORIGINE%
>> temoin-dudect-BROUILLON.txt echo Le sha256 du binaire execute :
certutil -hashfile "%BIN%" SHA256 >> temoin-dudect-BROUILLON.txt 2>&1
>> temoin-dudect-BROUILLON.txt echo Le protocole   : dudect_v150 cibles %N% ^(affinite coeur 0 par le mesureur^)
>> temoin-dudect-BROUILLON.txt echo Code du run    : %RC%
if defined RCAPPEL >> temoin-dudect-BROUILLON.txt echo Code de l'epreuve d'appel : %RCAPPEL% ^(sortie-appel.txt^)
if defined APPEL_PASSEE >> temoin-dudect-BROUILLON.txt echo Epreuve d'appel : PASSEE - test_appel ABSENT de l'extraction ^(ecart nomme, D189 : l'antivirus ? voyez VERIFIER-PAQUET.bat^)
if defined CSV >> temoin-dudect-BROUILLON.txt echo Le journal csv : %CSV%
>> temoin-dudect-BROUILLON.txt echo La sortie console complete : sortie-run.txt ^(jointe a ce dossier^)
>> temoin-dudect-BROUILLON.txt echo.
>> temoin-dudect-BROUILLON.txt echo A COMPLETER DE VOTRE MAIN ^(le mesureur ne peut pas le lire a votre place^) :
>> temoin-dudect-BROUILLON.txt echo   - l'etat EFFECTIF du turbo ^(BIOS desactive ou non^) ;
>> temoin-dudect-BROUILLON.txt echo   - la frequence reelle pendant le run, si vous la connaissez ;
>> temoin-dudect-BROUILLON.txt echo   - vos observations, memes defavorables ^(D189 : rapporter tel quel^).
>> temoin-dudect-BROUILLON.txt echo.
>> temoin-dudect-BROUILLON.txt echo PUIS : datez et signez de votre main sous ces lignes, et renvoyez le
>> temoin-dudect-BROUILLON.txt echo dossier ENTIER ^(journal csv + sortie-run.txt + ce temoin^) au coffre
>> temoin-dudect-BROUILLON.txt echo /test ^(dossier Drive 'Triade' - 'test'^). Le labo recoupe sur pieces :
>> temoin-dudect-BROUILLON.txt echo jamais avant le run, jamais sans pieces.

echo.
echo ============================================================================
echo  LE BROUILLON DU TEMOIN EST ECRIT : temoin-dudect-BROUILLON.txt
echo  A VOTRE MAIN : l'etat EFFECTIF du turbo ^(BIOS^), la date et la SIGNATURE.
echo  Renvoyez le dossier ENTIER au coffre /test ^(dossier Drive 'Triade'^).
echo  La lecture honnete : |t| ^> 5 = dependance AU SEUIL, consignee
echo  telle quelle ; |t| ^<= 5 = aucune divergence au seuil sur CET
echo  echantillon, CETTE machine - jamais 'temps constant prouve'.
echo ============================================================================
pause
exit /b %RC%

:n_invalide
echo.
echo [REFUS] N doit etre un nombre au moins egal a 60 ^(la commande exige
echo         N ^>= 60^). Exemples : LANCER-KIT-2-DUDECT.bat        ^(N = 200^)
echo                               LANCER-KIT-2-DUDECT.bat 400
pause
exit /b 2

:piece_absente
echo.
echo [REFUS] une piece du kit est ABSENTE - extrayez le zip COMPLET dans un
echo         dossier NEUF ^(D99, ne melangez jamais les runs^).
pause
exit /b 2

:image_divergente
echo.
echo [REFUS] le sha256 de cibles\proxy-image.bin DIVERGE du scelle : la piece
echo         a bouge - RIEN ne sera execute. Re-extrayez le zip COMPLET dans
echo         un dossier NEUF ^(D99^).
pause
exit /b 2

:compilation_echouee
echo.
echo [ECART NOMME] la compilation par %CC% a ECHOUE - le lanceur BASCULE sur
echo         les exe PRECOMPILES livres ^(cross-compiles au labo depuis CETTE
echo         meme source^). L'ecart est consigne au temoin : renvoyez-le tel
echo         quel ^(D189^) - le labo recoupera la cause avec vous.
set "ORIGINE=PRECOMPILE LIVRE (la recompilation locale par %CC% a echoue - l'ecart est consigne ici)"
set "BIN=dudect_v150.exe"
set "TBIN=test_appel.exe"
goto epreuve_appel
