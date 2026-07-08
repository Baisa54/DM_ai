#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Dialogador
#
# Dialogador es el que se encarga de gestionar los dialogos entre los personajes
# y el jugador. La idea es analizar si un NPC habla, extraer su dialogo, dejar la
# narracion sin dialogos para luego acomodar el mensaje final
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Prompt para la IA, en la que se detalla el comportamiento de dialogador
#   y lo que debe devolver. Este prompt debe estar en formato JSON.
# @ Dialogador, funcion que envia el prompt a la IA y devuelve el 
#   JSON resultante.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
#
# @ Dialogador, funcion que recibe como parametro 
#   [Narracion que genera el DM]
#   --> Se encarga de extraer el dialogo del personaje mas importante
#   --> Se encarga de extraer la emocion del personaje mas importante
#   --> Se encarga de eliminar el dialogo del personaje mas importante de la narracion
#   --> Se encarga de devolver el JSON resultante
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import json
# json para el manejo de datos
from modelo.ai.LocalAICLient import LocalAIClient as GeminiClient
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
#-@ from modelo.ai.GeminiClient import GeminiClient 
# GeminiClient es el cliente que se utiliza para comunicarse con la IA de google
# Actualmente comentada porque no se esta usando gemini, sino una IA local
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

PROMPT_DIALOGADOR = """<system>
Eres un analizador léxico y separador de diálogos para un motor de RPG narrativo. Eres un autómata de procesamiento de texto, NO un asistente conversacional. Tu tarea es recibir un bloque de texto narrativo, extraer el diálogo principal de un NPC, y devolver la narración reescrita SIN diálogos directos.
</system>

<rules>
1. DETECCIÓN: Analiza la narración recibida buscando cualquier línea de diálogo pronunciada por personajes.
2. REESCRITURA DE NARRACIÓN: Elimina TODOS los diálogos directos ("textos entre comillas" o guiones) de TODOS los personajes (incluido el Héroe). Reescribe la narración de forma fluida resumiendo lo sucedido pero SIN incluir citas textuales de nadie.
3. EXTRACCIÓN DE DIÁLOGO NPC: Extrae exactamente el texto del diálogo (sin comillas) del NPC más importante que haya hablado. 
4. EXCLUSIÓN DEL HÉROE: Si el Héroe (jugador) habla, ignóralo por completo para los campos 'Personaje', 'Emocion' y 'dialogo'. Estos campos son SOLO para NPCs.
5. PRIORIDAD DE NPCs (de mayor a menor): osgo > princesa > companero > goblin. (Solo usa estos nombres exactamente en minúscula). Si hablan varios, extrae solo al de mayor prioridad.
6. EMOCIONES PERMITIDAS: feliz, triste, enojado, asustado, sorprendido, neutral. Selecciona una en base al tono del diálogo.
</rules>

<output_schema>
Debes retornar EXCLUSIVAMENTE este objeto JSON, sin llaves ni texto adicional:
{
  "Narracion": "La narración original reescrita y adaptada, eliminando cualquier diálogo directo.",
  "Personaje": "nombre en minúscula del NPC que habla (o null si nadie habla)",
  "Emocion": "una de las emociones permitidas (o null si nadie habla)",
  "dialogo": "texto exacto de lo que dijo el NPC (o null si nadie habla)"
}
</output_schema>

<formatting_constraints>
- RESPUESTA PURA: No agregues "```json", ni introducciones ("Aquí tienes..."), ni explicaciones.
- ESTRUCTURA DE INICIO: Tu respuesta DEBE empezar con el carácter '{' y terminar con el carácter '}'.
- TIPO DE DATOS: Si no hay diálogo de NPC, Personaje, Emocion y dialogo DEBEN ser el valor null nativo de JSON (no el string "null").
</formatting_constraints>
"""

def dialogador(narracion):

    gemini = GeminiClient()

    prompt = f"""{PROMPT_DIALOGADOR}

<input_data>
{narracion}
</input_data>
"""

    resultado = gemini.generar_json(prompt)

    personaje = resultado.get("Personaje")
    emocion = resultado.get("Emocion")

    if personaje:
        personaje = personaje.strip().lower()

    if emocion:
        emocion = emocion.strip().lower()

    # MAPEAR
    MAP_PERSONAJES = {
        "companero": "companero",
        "compañero": "companero",
        "aelar": "companero",
        "goblin": "goblin",
        "princesa": "princesa",
        "osgo": "osgo"
    }

    MAP_EMOCIONES = {
        "feliz": "feliz",
        "triste": "triste",
        "enojado": "enojado",
        "asustado": "asustado",
        "sorprendido": "sorprendido",
        "neutral": "neutral"
    }

    personaje = MAP_PERSONAJES.get(personaje)
    emocion = MAP_EMOCIONES.get(emocion)

    if personaje is None and resultado.get("Personaje") is not None:
        raise ValueError("Personaje inválido devuelto por Gemini")

    if emocion is None and resultado.get("Emocion") is not None:
        raise ValueError("Emoción inválida devuelta por Gemini")

    return {
        **resultado,
        "Personaje": personaje,
        "Emocion": emocion
    }