import json
from ai.GeminiClient import GeminiClient

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

- Companero
- Aelar
- Goblin
- Princesa
- Osgo

Si el Heroe habla:

- NO debe aparecer como personaje.
- NO debe aparecer en dialogo.
- Reformula la narración eliminando lo que dijo.

Si hablan varios personajes:

- Elimina los diálogos de todos.
- Elige únicamente al personaje más importante.

Prioridad:

Osgo
Princesa
Aelar
Companero
Goblin

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

    resultado = gemini.generar_json(
        prompt
    )

    personajes_validos = [
        None,
        "Companero",
        "Aelar",
        "Goblin",
        "Princesa",
        "Osgo"
    ]

    emociones_validas = [
        None,
        "feliz",
        "triste",
        "enojado",
        "asustado",
        "sorprendido",
        "neutral"
    ]

    if resultado["Personaje"] not in personajes_validos:

        raise ValueError(
            "Personaje inválido devuelto por Gemini"
        )

    if resultado["Emocion"] not in emociones_validas:

        raise ValueError(
            "Emoción inválida devuelta por Gemini"
        )

    return resultado