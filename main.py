#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# main
#
# main es el punto de entrada principal del proyecto.
# Detecta el sistema operativo y lanza la vista gráfica basada en Pygame (VistaGrafica)
# de forma totalmente compatible con Windows, Linux y macOS.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ main, función de arranque principal del juego.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import sys
# sys se utiliza para añadir directorios al path de búsqueda en caso necesario
from Vista.vista_grafica import VistaGrafica
# VistaGrafica es el orquestador de la UI Pygame
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

if __name__ == "__main__":
    print(f"Iniciando DM AI en sistema operativo: {sys.platform}")
    app = VistaGrafica()
    app.iniciar()
