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
from modelo.ai.LocalAICLient import LocalAIClient as GeminiClient
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
#-@ from modelo.ai.GeminiClient import GeminiClient
# GeminiClient es el cliente que se utiliza para comunicarse con la IA de google
# Actualmente comentada porque no se esta usando gemini, sino una IA local
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
                "enum": ["Sin cambios", "entrada_cueva", "puerta_goblins", "gran_salon", "sala_osgo"]
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
    ubicacion_actual = estado.get_ubicacion()
    datos_sala = SALAS.get(ubicacion_actual, {})
    
    return f"""Eres el motor de estado del juego. Compara el estado actual con la acción del jugador y el resultado de los dados, y extrae ÚNICAMENTE los cambios llamando a la herramienta `actualizar_estado`.
Si el jugador intenta moverse hacia una salida válida y el resultado NO es un fracaso o pifia grave que lo impida, actualiza la sala. Si la acción implica daño o curación y fue un éxito o crítico, actualiza la vida.

<estado_previo>
{json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}
</estado_previo>

<entorno_fisico_actual>
Descripción oficial de la sala: {datos_sala.get("descripcion", "")}
Objetos tirados en el suelo: {datos_sala.get("objetos", [])}
Salidas válidas: {datos_sala.get("salidas", [])}
</entorno_fisico_actual>

<accion_jugador>
{accion}
</accion_jugador>

<resultado_accion>
{resultado_d20}
</resultado_accion>"""

def orquestar_accion(accion, resultado_d20, estado):
    from modelo.configuracion import ConfigManager
    config = ConfigManager()
    
    if config.get_proveedor_texto() == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        cliente = GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        cliente = LocalAIClient()
        
    prompt = construir_contexto_orquestador(accion, resultado_d20, estado)
    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_ACTUALIZAR_ESTADO)

    return resultado