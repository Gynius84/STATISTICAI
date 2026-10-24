@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo  STATISTICHEAI v2.7 - Monitor Universale Agenti AI (16-Bit Retrogame)
echo  14 Agenti: 4 Locali llama.cpp (:9931) + 10 Titani Penta-Cloud
echo  Cloud: Ollama Cloud, NVIDIA NIM, OpenRouter, Google AI Studio, OrcaRouter
echo  Stanze Live: Casetta (Riposo), Ufficio (Lavoro), Infermeria, Cimitero
echo ======================================================================

set "PYTHON_EXE=C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=C:\Users\Gyniu\miniforge3\python.exe"
)
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [1/2] Verifica server v2.7 e avvio in modalita' App Nativa...
"%PYTHON_EXE%" open_monitor.py

echo.
echo Server STATISTICHEAI v2.7 attivo in background su http://127.0.0.1:8888.
echo Per arrestare il server, eseguire stop.bat.
echo.
