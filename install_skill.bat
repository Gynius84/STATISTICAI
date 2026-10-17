@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

echo ========================================================
echo  STATISTICHEAI - Installazione Skill Hermes Agent
echo  Repository: https://github.com/Gynius84/VERSIONE2.0
echo ========================================================
echo.

set "DEST_DIR=%LocalAppData%\hermes\skills\statistiche"
set "BIN_DIR=%LocalAppData%\hermes\bin"

echo [1/3] Creazione directory skill in %DEST_DIR%...
if not exist "%DEST_DIR%\scripts" mkdir "%DEST_DIR%\scripts"

echo [2/3] Copia file di definizione SKILL.md e launcher...
copy /Y "skills\statistiche\SKILL.md" "%DEST_DIR%\SKILL.md" >nul
copy /Y "skills\statistiche\scripts\open_monitor.py" "%DEST_DIR%\scripts\open_monitor.py" >nul

echo [3/3] Registrazione comandi veloci in Hermes bin...
if exist "%BIN_DIR%" (
    (
        echo @echo off
        echo python "%~dp0open_monitor.py" %%*
    ) > "%BIN_DIR%\statistiche.cmd"
    (
        echo @echo off
        echo python "%~dp0open_monitor.py" %%*
    ) > "%BIN_DIR%\monitor.cmd"
)

echo.
echo ========================================================
echo  Installazione completata con successo!
echo  Ora puoi usare:
echo   - /statistiche o /monitor in chat con qualsiasi agente
echo   - Il comando "statistiche" da qualsiasi terminale
echo ========================================================
echo.
pause
