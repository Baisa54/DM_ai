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



PROMPT_ORQUESTADOR = """<system>
Eres el "Orquestador de Estado" de un motor RPG. Eres un autómata de extracción de datos, NO un asistente conversacional. Tu tarea es analizar una narración y convertirla estrictamente en un objeto JSON que refleje los cambios de estado del mundo.
</system>

<rules>
1. MUTABILIDAD DE ESTADO: No inventes personajes, objetos ni ubicaciones. Usa "Sin cambios" si el estado de un elemento no se vio afectado explícitamente en la narración.
2. VIDA: Si un personaje sufre daño, asigna "daño". Si se recupera o sana, asigna "se cura".
3. OBJETOS: Si el héroe pierde un objeto, usa "pierde". Si recoge uno, usa "obtiene". En la clave "name_obj", escribe el nombre literal del objeto afectado (o null si es "Sin cambios").
4. DIÁLOGOS: Si detectas que un NPC habla y tiene líneas de diálogo, "npc_habla" debe ser true.
5. RESUMEN: En "accion_Jugador", describe la acción en NO MÁS DE 4 PALABRAS.
</rules>

<output_schema>
Debes retornar EXCLUSIVAMENTE este objeto JSON, sin llaves ni texto adicional:
{
    "vida": {
        "heroe": "Sin cambios" | "daño" | "se cura",
        "companero": "Sin cambios" | "daño" | "se cura",
        "goblin": "Sin cambios" | "daño" | "se cura",
        "princesa": "Sin cambios" | "daño" | "se cura",
        "osgo": "Sin cambios" | "daño" | "se cura"
    },
    "objeto": {
        "heroe": "Sin cambios" | "pierde" | "obtiene",
        "name_obj": "nombre del objeto" | null
    },
    "sala": "Sin cambios" | "entrada_cueva" | "puerta_goblins" | "gran_salon" | "sala_osgo",
    "npc_habla": true | false,
    "accion_Jugador": "string (max 4 palabras)"
}
</output_schema>

<formatting_constraints>
- RESPUESTA PURA: No agregues "```json", ni introducciones, ni explicaciones.
- ESTRUCTURA DE INICIO: Tu respuesta DEBE empezar con el carácter '{' y terminar con el carácter '}'.
- CUIDADO DE COMAS: Verifica que no te falten comas entre propiedades, como entre "npc_habla" y "accion_Jugador".
</formatting_constraints>
"""


def construir_contexto_orquestador(narracion):
    return f"""<input_data>
<salas_permitidas>
{list(SALAS.keys())}
</salas_permitidas>

<personajes_permitidos>
{list(PERSONAJES.keys())}
</personajes_permitidos>

<narracion>
{narracion}
</narracion>
</input_data>"""

def orquestar_narracion(narracion):
    gemini = GeminiClient()
    prompt = f"{PROMPT_ORQUESTADOR}\n\n{construir_contexto_orquestador(narracion)}"

    resultado = gemini.generar_json(prompt)

    return resultado