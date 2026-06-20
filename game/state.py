from copy import deepcopy

#------------------------------------------------------------------------------------------------------
# State
#
# La idea de state es que posea el estado de la partida, es la memoria del arbitro para la narración
# Ademas, sea capaz de realizar cambios en las distintas variables de todo lo que esta presente
#------------------------------------------------------------------------------------------------------

def crear_estado_inicial():

    return {

        "ubicacion": "entrada_cueva",

        "jugador": {
            "nombre": "Heroe",
            "estado": "normal",
            "inventario": ["Espada"]
        },

        "eventos": [],

        "decisiones": [],

        "personajes_presentes": [
            "companero"
        ],

        "final": None,
    }


def aplicar_cambios(estado, respuesta_orquestador):
    """
    Aplica todos los cambios devueltos por el orquestador.

    Parámetros:
        estado (dict): estado actual del juego
        respuesta_orquestador (dict): JSON generado por la IA

    Retorna:
        dict: estado actualizado
    """

    estado_actualizado = deepcopy(estado)

    cambios = respuesta_orquestador.get("cambios", [])

    for cambio in cambios:

        tipo = cambio.get("tipo")

        if tipo == "danio":
            aplicar_danio(estado_actualizado, cambio)

        elif tipo == "curacion":
            aplicar_curacion(estado_actualizado, cambio)

        elif tipo == "gana_objeto":
            aplicar_ganar_objeto(estado_actualizado, cambio)

        elif tipo == "pierde_objeto":
            aplicar_perder_objeto(estado_actualizado, cambio)

        elif tipo == "cambiar_ubicacion":
            aplicar_cambio_ubicacion(estado_actualizado, cambio)

        elif tipo == "evento":
            aplicar_evento(estado_actualizado, cambio)

        elif tipo == "cambiar_estado_personaje":
            aplicar_estado_personaje(estado_actualizado, cambio)

    aplicar_final(estado_actualizado,
                  respuesta_orquestador.get("final"))

    return estado_actualizado


def aplicar_danio(estado, cambio):

    personaje = cambio.get("personaje")
    cantidad = cambio.get("cantidad", 0)

    if personaje in estado:
        estado[personaje]["vida"] = max(
            0,
            estado[personaje]["vida"] - cantidad
        )


def aplicar_curacion(estado, cambio):

    personaje = cambio.get("personaje")
    cantidad = cambio.get("cantidad", 0)

    if personaje in estado:
        estado[personaje]["vida"] += cantidad


def aplicar_ganar_objeto(estado, cambio):

    objeto = cambio.get("objeto")

    if objeto:
        estado["jugador"]["inventario"].append(objeto)


def aplicar_perder_objeto(estado, cambio):

    objeto = cambio.get("objeto")

    if objeto in estado["jugador"]["inventario"]:
        estado["jugador"]["inventario"].remove(objeto)


def aplicar_cambio_ubicacion(estado, cambio):

    destino = cambio.get("destino")

    if destino:
        estado["ubicacion"] = destino


def aplicar_evento(estado, cambio):

    evento = cambio.get("nombre")

    if evento and evento not in estado["eventos"]:
        estado["eventos"].append(evento)


def aplicar_estado_personaje(estado, cambio):

    personaje = cambio.get("personaje")
    nuevo_estado = cambio.get("estado")

    if personaje in estado:
        estado[personaje]["estado"] = nuevo_estado


def aplicar_final(estado, final_json):

    if not final_json:
        return

    if final_json.get("activo"):

        estado["final"] = final_json.get("tipo")
        estado["juego_terminado"] = True