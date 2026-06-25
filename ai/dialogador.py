import json
from ai.LocalAICLient import LocalAIClient as GeminiClient
# from ai.GeminiClient import GeminiClient

PROMPT_DIALOGADOR = """
Eres un analizador de diálogos para un RPG narrativo.

Tu tarea NO es narrar.

Tu tarea es:

1) Analizar la narración recibida.

2) Detectar si algún NPC habla.

3) Extraer el diálogo del NPC más importante.

4) Eliminar TODOS los diálogos de personajes de la narración.

5) Reescribir la narración para que siga siendo coherente
sin mostrar diálogos directos.

IMPORTANTE:

Personajes válidos:

- companero
- goblin
- princesa
- osgo

Si el Heroe habla:

- NO debe aparecer como personaje.
- NO debe aparecer en dialogo.
- Reformula la narración eliminando lo que dijo.

Si hablan varios personajes:

- Elimina los diálogos de todos.
- Elige únicamente al personaje más importante.

Prioridad:

osgo
princesa
companero
goblin

Emociones permitidas:

- feliz
- triste
- enojado
- asustado
- sorprendido
- neutral

Si ningún NPC habla:

{
    "Narracion": "narracion original adaptada",
    "Personaje": null,
    "Emocion": null,
    "dialogo": null
}

Devuelve EXCLUSIVAMENTE un JSON válido.

Formato obligatorio:

{
    "Narracion": "",
    "Personaje": null,
    "Emocion": null,
    "dialogo": null
}
"""


def dialogador(narracion):

    gemini = GeminiClient()

    prompt = f"""
{PROMPT_DIALOGADOR}

NARRACION:

{narracion}
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