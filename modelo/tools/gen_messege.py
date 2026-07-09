#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# gen_messege
#
# gen_messege se encarga de crear e inicializar la instancia inicial del mensaje
# de juego que se presentará al jugador al comenzar una partida (narración inicial
# e imagen resumen inicial).
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# (No define elementos o constantes a nivel de módulo)
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ genMessage
#   --> Devuelve un objeto MensajeJuego inicializado con los datos de inicio de partida.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.clases.MensajeJuego import MensajeJuego
# MensajeJuego es la clase que encapsula la estructura del mensaje del juego
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def genMessage():

    mensaje = MensajeJuego()

    mensaje.set_narracion(
        "El protagonista, un guerrero humano, y su leal compañero arquero elfo, "
        "Aelar, han llegado a la misteriosa cueva donde se rumorea, está la "
        "princesa del reino atrapada. Han tenido que pasar por un bosque denso "
        "y oscuro, esquivar animales peligrosos y sobrevivir con pocas provisiones. "
        "Se logra ver al costado de la cueva una caja con un poco de comida y una antorcha."
    )

    mensaje.set_imagen_resumen(
        "modelo/game/assets/imagen_inicio.png"
    )

    return mensaje

