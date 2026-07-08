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



PROMPT_ORQUESTADOR = """
Eres un sistema de extracción de estado para un RPG.

NO eres narrador.
NO agregas información nueva.

Tu única tarea es analizar una narración y convertirla en un JSON estructurado.

REGLAS ESTRICTAS:
- Solo puedes usar los valores permitidos.
- No puedes inventar personajes, objetos ni ubicaciones.
- Si no hay cambio, usa "Sin cambios".
- Si un personaje sufre daño, usa "daño" en ese personaje
- Si un personaje se cura, usa "se cura" en ese personaje
- Si detectas que un NPC habla y tiene lineas de dialogo, cambia el valor de "npc_habla" en "true"
- En caso de que "Objeto" --> "Heroe": "Pierde" o "Obtiene", debes escribir en "name_obj" el nombre del objeto que gana o pierde
- En "accion_Jugador": pon en NO MAS DE 4 PALABRAS la accion que realiza el jugador reemplazando "Accion que realiza"

OUTPUT OBLIGATORIO:

{
    "vida": {
        "heroe": "Sin cambios",
        "companero": "Sin cambios",
        "goblin": "Sin cambios",
        "princesa": "Sin cambios",
        "osgo": "Sin cambios"
    },
    "objeto": {
        "heroe": "Sin cambios"
        "name_obj": "nombre del objeto"
    },
    "sala": "Sin cambios",
    "npc_habla": false
    "accion_Jugador": "Accion que realiza"
}

REGLAS DE VALORES:

vida:
- "Sin cambios"
- "daño"
- "se cura"

objeto:
- "pierde"
- "obtiene"
- "Sin cambios"

sala:
- "Sin cambios"
- "entrada_cueva"
- "puerta_goblins"
- "gran_salon"
- "sala_osgo"

npc_habla:
- true
- false

DEVUELVE SOLO JSON.
"""


def construir_contexto_orquestador(narracion):

    return f"""
SALAS PERMITIDAS:
{list(SALAS.keys())}

PERSONAJES PERMITIDOS:
{list(PERSONAJES.keys())}

NARRACION:
{narracion}
"""


def orquestar_narracion(narracion):

    gemini = GeminiClient()

    prompt = f"""
{PROMPT_ORQUESTADOR}

{construir_contexto_orquestador(narracion)}
"""

    resultado = gemini.generar_json(prompt)

    return resultado