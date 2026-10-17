@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo  STATISTICHEAI - Arresto Sicuro Server
echo ========================================================

if not exist "server.pid" (
    echo Nessun server STATISTICHEAI attivo trovato (server.pid assente).
    goto end
)

set "SERVER_PID="
for /f "usebackq tokens=*" %%i in ("server.pid") do set "SERVER_PID=%%i"
if "%SERVER_PID%"=="" (
    echo server.pid e' vuoto.
    del "server.pid" >nul 2>&1
    goto end
)

echo Arresto del processo server con PID %SERVER_PID%...
taskkill /F /PID %SERVER_PID% >nul 2>&1

if exist "server.pid" (
    del "server.pid" >nul 2>&1
)

echo Server STATISTICHEAI arrestato con successo.

:end
echo.
