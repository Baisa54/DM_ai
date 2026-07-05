import json

from ai.LocalAICLient import LocalAIClient as GeminiClient
# from ai.GeminiClient import GeminiClient

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

PROMPT_NARRADOR_FINAL = """
Eres el Dungeon Master de una campaña RPG.

Tu tarea es narrar el FINAL de la historia del jugador en base al final que esta en "ESTADO ACTUAL".

Reglas:

- Nunca modifiques el estado.
- Nunca agregues personajes nuevos.
- Nunca contradigas el final indicado.
- Debes respetar completamente el tipo de final recibido.

Estilo:
Narración épica, emocional y cerrando la historia del RPG.

FINALES POSIBLES:

1) muerte heroe
Final trágico. El héroe muere. Tonalidad triste, oscura y definitiva.

2) rescate princesa
Final positivo. El héroe rescata a la princesa y recibe una gran recompensa del rey.

3) Alianza goblin
Final de traición. El héroe se une a los goblins y Osgo para traicionar el reino.

4) Escape
Final ambiguo. El héroe abandona la misión y se va de la cueva. Nunca sabrá qué había dentro.

5) muerte princesa
Final extremadamente triste. La princesa muere y la misión fracasa.

Devuelve únicamente la narración final.
"""

def narrar_final(
    estado,
    accion,
    resultado_accion
):

    gemini = GeminiClient()

    prompt = f"""
{PROMPT_NARRADOR_FINAL}

ESTADO ACTUAL:

{json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}

ACCION DEL JUGADOR:

{accion}

RESULTADO DE LA ACCION:

{resultado_accion}

"""

    return gemini.generar_texto(prompt)