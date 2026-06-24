# ai/arbitro_accion.py

import json
from ai.GeminiClient import GeminiClient

PROMPT_ARBITRO_ACCION = """
Eres el árbitro de un RPG narrativo.

Tu tarea es analizar la acción del jugador
considerando el estado actual de la partida.

Debes responder EXCLUSIVAMENTE un JSON válido.

DEVUELVE SIEMPRE UN JSON COMPLETO CON LAS 3 CLAVES:

{
    "accion_valida": true,
    "requiere_tirada": false,
    "dificultad": 10
}

NO OMITAS NINGUNA CLAVE.
NO AGREGUES TEXTO.
NO EXPLIQUES NADA.

Reglas:

- Verifica si la acción es posible según:
  - ubicación actual
  - inventario
  - personajes presentes
  - eventos registrados

- Si la acción no puede realizarse:
{
    "accion_valida": false,
    "requiere_tirada": false,
    "dificultad": null
}

- Si la acción es automática:
{
    "accion_valida": true,
    "requiere_tirada": false,
    "dificultad": null
}

- Dificultades permitidas:
5 = fácil
10 = media
15 = difícil
20 = extremadamente difícil

- Nunca inventes otros valores.
"""

def arbitrar_accion(
    accion,
    estado
):

    gemini = GeminiClient()

    entrada = {
        "accion_jugador": accion,
        "estado_partida": estado.to_dict()
    }

    prompt = f"""
{PROMPT_ARBITRO_ACCION}

DATOS DE ENTRADA:

{json.dumps(
    entrada,
    indent=4,
    ensure_ascii=False
)}
"""

    resultado = gemini.generar_json(
        prompt
    )

    required_keys = ["accion_valida", "requiere_tirada", "dificultad"]

    for key in required_keys:
        if key not in resultado:
            raise ValueError(f"Gemini no devolvió la clave obligatoria: {key}")

    dificultades_validas = [
        0,
        5,
        10,
        15,
        20
    ]

    if resultado["dificultad"] not in dificultades_validas:

        raise ValueError(
            "Dificultad inválida devuelta por Gemini"
        )

    return resultado