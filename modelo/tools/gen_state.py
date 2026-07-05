from clases.Estadojuego import EstadoJuego

#------------------------------------------------------------------------------------------------------
# State
#
# La idea de state es que posea el estado de la partida, es la memoria del arbitro para la narración
# Ademas, sea capaz de realizar cambios en las distintas variables de todo lo que esta presente
#------------------------------------------------------------------------------------------------------

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