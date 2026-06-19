# ai/arbitro_accion.py

PROMPT_ARBITRO_ACCION = """
Eres el árbitro de un RPG narrativo.

Tu tarea es analizar la acción del jugador
considerando el estado actual de la partida.

Debes responder EXCLUSIVAMENTE un JSON válido.

Formato:

{
    "accion_valida": true,
    "requiere_tirada": true,
    "dificultad": 5
}

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

- Devuelve únicamente JSON.
"""

def construir_prompt(accion, estado):

    return f"""
ESTADO:

{estado}

ACCION DEL JUGADOR:

{accion}
"""