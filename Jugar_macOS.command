#!/bin/bash
# Lanzador interactivo para macOS
# Para poder ejecutarlo con doble click, asegúrate de darle permisos:
# chmod +x Jugar_macOS.command

cd "$(dirname "$0")"

echo "=============================================="
echo "       INICIANDO DUNGEON MASTER AI"
echo "=============================================="
echo ""

# 1. Comprobar Python
if ! command -v python3 &> /dev/null; then
    echo "[X] Python3 no esta instalado."
    echo "Por favor, instala Python 3 desde https://www.python.org/downloads/mac-osx/"
    echo "O usando Homebrew: brew install python"
    read -p "Presiona enter para salir..."
    exit 1
fi
echo "[OK] Python3 detectado."

# 2. Entorno virtual y dependencias
if [ ! -d ".venv" ]; then
    echo ""
    echo "[!] No se encontro el entorno virtual."
    read -p "¿Deseas crear el entorno virtual e instalar dependencias? (s/n): " crear_venv
    if [[ "$crear_venv" == "s" || "$crear_venv" == "S" ]]; then
        echo "Creando entorno virtual..."
        python3 -m venv .venv
        
        echo "Instalando dependencias de Python..."
        .venv/bin/pip install --upgrade pip
        .venv/bin/pip install -r requirements.txt
    else
        echo "Debes instalar las dependencias manualmente para jugar."
        exit 1
    fi
else
    echo "[OK] Entorno virtual detectado."
fi

# 3. Ollama
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "[X] Ollama no esta instalado."
    echo "Ollama es necesario para jugar localmente."
    echo "Por favor descargalo desde https://ollama.com/download/mac"
    echo "Una vez instalado, abre la aplicacion de Ollama para que se inicie en segundo plano."
    read -p "Presiona enter para continuar de todas formas (puede fallar)..."
else
    echo "[OK] Ollama detectado."
fi

echo ""
echo "=============================================="
echo "       INICIANDO EL JUEGO..."
echo "=============================================="
.venv/bin/python main.py
