import json

from ai import GeminiClient

PROMPT_NARRADOR = """
Eres el Dungeon Master de una campaña RPG.

Tu tarea es narrar las consecuencias de la acción del jugador.

Reglas:

- Nunca modifiques directamente el estado.
- Nunca inventes objetos que no existan.
- Nunca inventes personajes que no existan.
- Respeta la ubicación actual.
- Respeta los eventos ocurridos.

Interpretación de resultados:

fracaso:
Produce un resultado negativo razonablemente posible.
No rompe las reglas del mundo.

exito:
Produce un resultado positivo razonablemente posible.
No rompe las reglas del mundo.

critico:
Produce el mejor resultado razonablemente posible.
No rompe las reglas del mundo.

pifia:
Produce el peor resultado razonablemente posible.
No rompe las reglas del mundo.

Habla como un Dungeon Master narrando una aventura.

Devuelve únicamente la narración.
"""

def construir_contexto_narrador(
    estado,
    accion,
    resultado_accion
):

    return f"""
    ESTADO ACTUAL:

    {json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}

    ACCION DEL JUGADOR:

    {accion}

    RESULTADO:

    {resultado_accion}
    """


def narrar_accion(
    accion,
    estado,
    resultado_d20
    ):

        gemini = GeminiClient()

        prompt = f"""
    {PROMPT_NARRADOR}

    {construir_contexto_narrador(
            estado,
            accion,
            resultado_d20
        )}
    """

        return gemini.generar_texto(prompt)