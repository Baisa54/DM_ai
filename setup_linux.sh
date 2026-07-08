#!/bin/bash
# Script de configuración de dependencias de Pygame para Linux (CachyOS/Arch/Debian/Ubuntu)

echo "=== Configurando dependencias de Pygame para Linux ==="

# Detectar distribución
if [ -f /etc/arch-release ] || [ -f /etc/artix-release ] || grep -q "Arch" /etc/os-release; then
    echo "Distribución basada en Arch/CachyOS detectada."
    echo "Instalando sdl2_image, sdl2_ttf y sdl2_mixer..."
    sudo pacman -S --needed sdl2_image sdl2_ttf sdl2_mixer
elif [ -f /etc/debian_version ] || grep -q "Ubuntu" /etc/os-release || grep -q "Debian" /etc/os-release; then
    echo "Distribución basada en Debian/Ubuntu detectada."
    echo "Instalando libsdl2-image-dev, libsdl2-ttf-dev y libsdl2-mixer-dev..."
    sudo apt-get update && sudo apt-get install -y libsdl2-image-dev libsdl2-ttf-dev libsdl2-mixer-dev
else
    echo "Distribución no soportada automáticamente por este script."
    echo "Por favor instale de forma manual las librerías de desarrollo de SDL2 (image, ttf, mixer)."
fi

echo "Reinstalando pygame en el entorno virtual..."
.venv/bin/pip install --force-reinstall --no-cache-dir pygame

echo "=== Listo! Ahora puedes ejecutar: .venv/bin/python main.py ==="
