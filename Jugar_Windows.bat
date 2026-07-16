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

:: 2. Entorno virtual y dependencias
if not exist ".venv" (
    echo.
    echo [!] No se encontro el entorno virtual.
    set /p crear_venv="¿Deseas crear el entorno virtual e instalar las dependencias de Python? (s/n): "
    if /i "!crear_venv!"=="s" (
        echo Creando entorno virtual...
        python -m venv .venv
        echo Instalando dependencias...
        .venv\Scripts\python -m pip install --upgrade pip
        .venv\Scripts\pip install -r requirements.txt
    ) else (
        echo Debes instalar las dependencias manualmente para jugar.
        pause
        exit /b
    )
) else (
    echo [OK] Entorno virtual detectado.
)

:: 3. Ollama
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [X] Ollama no esta instalado o no esta iniciado.
    echo Ollama es necesario para correr los modelos locales de IA.
    echo Descarga Ollama desde: https://ollama.com/download
    echo Instala Ollama y abre el programa antes de continuar.
    pause
) else (
    echo [OK] Ollama detectado.
)

echo.
echo ==============================================
echo        INICIANDO EL JUEGO...
echo ==============================================
.venv\Scripts\python main.py

pause
