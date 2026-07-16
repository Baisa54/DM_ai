#!/bin/bash
# Lanzador interactivo para Linux

echo "=============================================="
echo "       INICIANDO DUNGEON MASTER AI"
echo "=============================================="
echo ""

# 1. Comprobar Python
if ! command -v python3 &> /dev/null; then
    echo "[X] Python3 no esta instalado."
    echo "Por favor, instala Python 3 usando tu gestor de paquetes."
    echo "Ejemplo Ubuntu/Debian: sudo apt install python3 python3-venv"
    echo "Ejemplo Arch/Manjaro: sudo pacman -S python"
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
        
        echo "Configurando dependencias de sistema SDL2 (requerido para Pygame en Linux)..."
        if [ -f /etc/debian_version ] || grep -q "Ubuntu" /etc/os-release || grep -q "Debian" /etc/os-release; then
            echo "Distribución Debian/Ubuntu detectada. Solicitando permisos para instalar librerías SDL..."
            sudo apt-get update && sudo apt-get install -y libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev
        elif [ -f /etc/arch-release ] || grep -q "Arch" /etc/os-release; then
            echo "Distribución Arch detectada. Solicitando permisos para instalar librerías SDL..."
            sudo pacman -S --needed sdl2_image sdl2_ttf sdl2_mixer
        fi

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
    read -p "¿Deseas instalar Ollama automaticamente ahora? (s/n): " inst_ollama
    if [[ "$inst_ollama" == "s" || "$inst_ollama" == "S" ]]; then
        echo "Descargando e instalando Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        echo "Ollama es necesario para jugar localmente."
        echo "Instálalo usando: curl -fsSL https://ollama.com/install.sh | sh"
        echo "O descárgalo desde https://ollama.com"
        read -p "Presiona enter para continuar de todas formas..."
    fi
else
    echo "[OK] Ollama detectado."
fi

echo ""
echo "=============================================="
echo "       INICIANDO EL JUEGO..."
echo "=============================================="
.venv/bin/python main.py
