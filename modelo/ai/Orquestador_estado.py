#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Orquestador
#
# Orquestador es el encargado de orquestar el estado de la partida
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PROMPT_ORQUESTADOR, prompt que se encarga de generar el estado de la partida
# @ construir_contexto_orquestador, funcion que se encarga de construir el contexto
# @ orquestar_narracion, funcion que se encarga de generar el estado de la partida
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ orquestar_narracion, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import json
#-@ from modelo.ai.cliente_factory import obtener_cliente_texto
from modelo.game.campaign import SALAS
# SALAS es el diccionario que se utiliza para manejar las salas
from modelo.game.characters import PERSONAJES
# PERSONAJES es el diccionario que se utiliza para manejar los personajes
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#



HERRAMIENTA_ACTUALIZAR_ESTADO = {
    "name": "actualizar_estado",
    "description": "Actualiza el estado de los personajes, inventario y ubicacion tras la narración.",
    "parameters": {
        "type": "object",
        "properties": {
            "vida": {
                "type": "object",
                "properties": {
                    "heroe": {"type": "string", "enum": ["Sin cambios", "daño", "se cura"]},
                    "companero": {"type": "string", "enum": ["Sin cambios", "daño", "se cura"]},
                    "goblin": {"type": "string", "enum": ["Sin cambios", "daño", "se cura"]},
                    "princesa": {"type": "string", "enum": ["Sin cambios", "daño", "se cura"]},
                    "osgo": {"type": "string", "enum": ["Sin cambios", "daño", "se cura"]}
                },
                "required": ["heroe", "companero", "goblin", "princesa", "osgo"]
            },
            "objeto": {
                "type": "object",
                "properties": {
                    "heroe": {"type": "string", "enum": ["Sin cambios", "pierde", "obtiene"]},
                    "name_obj": {"type": "string", "description": "Nombre literal del objeto afectado, o vacio si no hay cambios"}
                },
                "required": ["heroe", "name_obj"]
            },
            "sala": {
                "type": "string",
                "enum": ["Sin cambios", "entrada_cueva", "puerta_goblins", "sala_osgo"]
            },
            "npc_habla": {
                "type": "boolean",
                "description": "Devuelve true si algun personaje que no sea el jugador dijo dialogos."
            },
            "accion_Jugador": {
                "type": "string",
                "description": "Resumen muy breve de la accion, maximo 4 palabras."
            }
        },
        "required": ["vida", "objeto", "sala", "npc_habla", "accion_Jugador"]
    }
}


def construir_contexto_orquestador(accion, resultado_d20, estado):
    """
    Construye el prompt estructurado para que la IA extraiga los cambios de estado (salud, sala, ítems).
    """
    ubicacion_actual = estado.get_ubicacion()
    datos_sala = SALAS.get(ubicacion_actual, {})
    
    nombres_salidas = {s: SALAS.get(s, {}).get("nombre", s) for s in datos_sala.get("salidas", [])}

    return f"""Eres el motor de estado del juego. Compara el estado actual con la acción del jugador y el resultado de los dados, y extrae ÚNICAMENTE los cambios llamando a la herramienta `actualizar_estado`.
Si el jugador intenta moverse hacia una salida válida, avanzar a la siguiente sala de forma genérica, o cruzar una puerta, y el resultado NO es un fracaso, OBLIGATORIAMENTE actualiza la sala usando el ID exacto de la salida válida. Si la acción implica daño o curación y fue un éxito o crítico, actualiza la vida.

REGLA ESTRICTA Y ABSOLUTA:
NUNCA razones, expliques ni devuelvas texto normal. Aún si la tirada es un "fracaso" y no hay cambios en el estado, DEBES ejecutar la herramienta `actualizar_estado` con los valores "Sin cambios". ¡PROHIBIDO hablar o razonar fuera de la llamada a la herramienta!

<estado_previo>
{json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}
</estado_previo>

<entorno_fisico_actual>
Descripción oficial de la sala: {datos_sala.get("descripcion", "")}
Objetos tirados en el suelo: {datos_sala.get("objetos", [])}
Salidas válidas (ID EXACTO: Nombre): {json.dumps(nombres_salidas, ensure_ascii=False)}
</entorno_fisico_actual>

<accion_jugador>
{accion}
</accion_jugador>

<resultado_accion>
{resultado_d20}
</resultado_accion>"""

def orquestar_accion(accion, resultado_d20, estado):
    """
    Invoca la herramienta de actualización de estado de la IA y devuelve los cambios producidos en el turno.
    """
    from modelo.ai.cliente_factory import obtener_cliente_texto
    cliente = obtener_cliente_texto()
        
    prompt = construir_contexto_orquestador(accion, resultado_d20, estado)
    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_ACTUALIZAR_ESTADO)

    return resultado