@echo off
setlocal
cd /d "%~dp0"

echo ========================================================
echo  STATISTICHEAI v2.0 - Monitor Universale Agenti AI (16-Bit)
echo  Architettura Multi-Provider: Ollama, LM Studio, Hermes, Cloud
echo ========================================================

set "PYTHON_EXE=C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [1/2] Verifica server e avvio in modalita' App Nativa...
"%PYTHON_EXE%" open_monitor.py

echo.
echo Server v2.0 attivo in background su http://127.0.0.1:8888.
echo Per arrestare il server, eseguire stop.bat.
echo.
