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


def construir_contexto_orquestador(narracion):
    return f"""Eres el motor de estado del juego. Extrae los cambios de estado de la siguiente narración llamando a la herramienta `actualizar_estado`.
<narracion>
{narracion}
</narracion>"""

def orquestar_narracion(narracion):
    from modelo.configuracion import ConfigManager
    config = ConfigManager()
    
    if config.get_proveedor_texto() == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        cliente = GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        cliente = LocalAIClient()
        
    prompt = construir_contexto_orquestador(narracion)
    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_ACTUALIZAR_ESTADO)

    return resultado