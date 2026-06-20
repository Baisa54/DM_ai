from copy import deepcopy
from Estadojuego import EstadoJuego

#------------------------------------------------------------------------------------------------------
# State
#
# La idea de state es que posea el estado de la partida, es la memoria del arbitro para la narración
# Ademas, sea capaz de realizar cambios en las distintas variables de todo lo que esta presente
#------------------------------------------------------------------------------------------------------

def gen_state():

    estado = EstadoJuego()

    estado.set_ubicacion("entrada_cueva")

    estado.jugador = {
        "nombre": "Heroe",
        "estado": "normal",
        "inventario": ["Espada"]
    }

    estado.personajes_presentes = [
        "companero"
    ]

    estado.set_final(None)

    return estado

