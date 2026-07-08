#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# gen_state
#
# gen_state se encarga de crear e inicializar el estado inicial de la partida,
# definiendo la ubicación inicial del héroe, sus objetos iniciales y el estado
# de salud de todos los personajes presentes.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# (No define elementos o constantes a nivel de módulo)
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ gen_state
#   --> Devuelve un objeto EstadoJuego con los valores iniciales configurados.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.clases.Estadojuego import EstadoJuego
# EstadoJuego es la clase que almacena los datos y estado global de la partida
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

def gen_state():

    estado = EstadoJuego()

    estado.set_ubicacion("entrada_cueva")

    estado.personajes_presentes = [
        "companero"
    ]

    estado.set_estado_personaje(
        "heroe",
        "normal"
    )

    estado.set_estado_personaje(
        "companero",
        "normal"
    )

    estado.set_estado_personaje(
        "goblin",
        "normal"
    )

    estado.set_estado_personaje(
        "princesa",
        "normal"
    )

    estado.set_estado_personaje(
        "osgo",
        "normal"
    )

    estado.objetos_heroe = [
        "espada"
    ]

    estado.set_final(None)

    return estado