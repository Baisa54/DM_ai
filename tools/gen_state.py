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

    estado.personajes_presentes = [
        "Companero"
    ]

    estado.set_estado_personaje(
        "Heroe",
        "normal"
    )

    estado.set_estado_personaje(
        "Companero",
        "normal"
    )

    estado.set_estado_personaje(
        "Goblin",
        "normal"
    )

    estado.set_estado_personaje(
        "Princesa",
        "normal"
    )

    estado.set_estado_personaje(
        "Osgo",
        "normal"
    )

    estado.objetos_heroe = [
        "espada"
    ]

    estado.set_final(None)

    return estado