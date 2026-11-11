@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo  STATISTICAI v2.9.1 - Monitor Universale Agenti AI (16-Bit Retrogame)
echo  13 Agenti Hermes: 5 Locali Ollama (C:) + 8 Titani Cloud
echo  Cloud: Ollama Cloud, NVIDIA NIM, OrcaRouter, Nous Research
echo  Stanze Live: Casetta (Riposo), Ufficio (Lavoro), Infermeria, Cimitero
echo  Funzionalita': Box & Card Minimization, Auto-Hide Vortici, Doctor 1-Click
echo ======================================================================

set "PYTHON_EXE=C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=C:\Users\Gyniu\miniforge3\python.exe"
)
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [1/2] Verifica server v2.9 e avvio in modalita' App Nativa...
"%PYTHON_EXE%" open_monitor.py

echo.
echo Server STATISTICHEAI v2.9.1 attivo in background su http://127.0.0.1:8787.
echo Per arrestare il server, eseguire stop.bat.
echo.
