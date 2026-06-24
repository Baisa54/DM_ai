from ai.GeminiClient import GeminiClient

from game.campaign import SALAS
from game.characters import PERSONAJES


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