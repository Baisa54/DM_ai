@echo off
setlocal EnableDelayedExpansion
title Lanzador DM AI

echo ==============================================
echo        INICIANDO DUNGEON MASTER AI
echo ==============================================
echo.

:: 1. Comprobar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] Python no esta instalado o no esta en el PATH.
    echo Por favor, descarga e instala Python desde: https://www.python.org/downloads/
    echo ¡Importante! Asegurate de marcar la casilla "Add Python to PATH" durante la instalacion.
    pause
    exit /b
)
echo [OK] Python detectado.

:: 2. Entorno de ejecucion
set "PYTHON_CMD=python"
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_CMD=.venv\Scripts\python.exe"
    echo [OK] Entorno virtual (.venv) detectado.
) else (
    echo [OK] Utilizando Python del sistema.
)

:: 3. Ollama
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [!] Aviso: Ollama no esta activo o no esta en el PATH.
    echo Si vas a usar modelos locales, inicia Ollama.
    echo Si vas a usar el Modo Exposicion (ChatGPT), puedes continuar directamente.
    echo.
) else (
    echo [OK] Ollama detectado.
)

echo.
echo ==============================================
echo        INICIANDO EL JUEGO...
echo ==============================================
%PYTHON_CMD% main.py

pause
