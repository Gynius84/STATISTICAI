@echo off
setlocal
cd /d "%~dp0"

echo ======================================================================
echo  STATISTICAI v3.0 - Monitor Universale Agenti AI (16-Bit Retrogame)
echo  14 Agenti Hermes: 6 Locali (5 Ollama C: + 1 Unsloth :8888) + 8 Titani Cloud
echo  Gateway: Ollama (:11434), Unsloth (:8888), NVIDIA NIM, Orca, Nous
echo  Stanze Live: Casetta (Riposo), Ufficio (Lavoro), Infermeria, Cimitero
echo  Funzionalita': Dual Local Gateway, Box & Card Minimization, Auto-Gateway
echo ======================================================================

set "PYTHON_EXE=C:\Users\Gyniu\AppData\Local\hermes\tools\python-3.14.7+20260901-win32-x64\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=C:\Users\Gyniu\miniforge3\python.exe"
)
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

echo [1/2] Verifica server v3.0 e avvio in modalita' App Nativa...
"%PYTHON_EXE%" open_monitor.py

echo.
echo Server STATISTICAI v3.0 attivo in background su http://127.0.0.1:8787.
echo Per arrestare il server, eseguire stop.bat.
echo.
