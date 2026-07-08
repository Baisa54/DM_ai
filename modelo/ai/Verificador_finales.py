#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Verificador de finales
#
# Verificador de finales es el encargado de verificar si se cumple alguno de los finales posibles
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PROMPT_VERIFICADOR_FINALES, prompt que se encarga de verificar los finales
# @ verificar_final, funcion que se encarga de verificar los finales
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ verificar_final, recibe como parametro el estado de la partida
#   --> Devuelve el final de la partida
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.ai.LocalAICLient import LocalAIClient as GeminiClient
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
#-@ from modelo.ai.GeminiClient import GeminiClient
# GeminiClient es el cliente que se utiliza para comunicarse con la IA de google
# Actualmente comentada porque no se esta usando gemini, sino una IA local
import json
# json para el manejo de datos
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

PROMPT_VERIFICADOR_FINALES = """<system>
Eres el "Verificador de Finales" de un RPG narrativo. Eres un autómata de procesamiento lógico, NO un asistente conversacional. Tu tarea es cruzar el estado actual y la última narración para determinar si el juego ha terminado.
</system>

<rules>
Evalúa las condiciones y decide el final correspondiente. 
SOLO puedes elegir UNO de los siguientes finales válidos:

1. "muerte heroe": Se cumple ÚNICAMENTE si estado_personajes["heroe"] == "muerto".
2. "Escape": Se cumple ÚNICAMENTE si el héroe está en "entrada_cueva" Y la narración indica explícitamente que abandona la misión o huye.
3. "Alianza goblin": Se cumple ÚNICAMENTE si el héroe se alía con los goblins o con Osgo traicionando al reino.
4. "rescate princesa": Se cumple ÚNICAMENTE si Osgo está "muerto", la princesa está "vivo", Y la narración indica que fue liberada o rescatada.
5. "muerte princesa": Se cumple ÚNICAMENTE si estado_personajes["princesa"] == "muerto".

Si ninguna de estas condiciones se cumple de forma explícita, el final es "sin_final".
</rules>

<output_schema>
Debes retornar EXCLUSIVAMENTE este objeto JSON, sin llaves ni texto adicional:
{
  "final": "sin_final" | "muerte heroe" | "rescate princesa" | "Alianza goblin" | "Escape" | "muerte princesa"
}
</output_schema>

<formatting_constraints>
- RESPUESTA PURA: No agregues "```json", ni introducciones, ni explicaciones.
- ESTRUCTURA DE INICIO: Tu respuesta DEBE empezar con el carácter '{' y terminar con el carácter '}'.
- VALORES: El valor de la clave "final" DEBE ser una de las 6 strings exactas especificadas. No inventes otros valores.
</formatting_constraints>
"""


def verificar_final(estado, narracion):
    gemini = GeminiClient()
    entrada = {
        "estado_partida": estado.to_dict(),
        "narracion": narracion
    }

    prompt = f"""{PROMPT_VERIFICADOR_FINALES}

<input_data>
{json.dumps(entrada, indent=4, ensure_ascii=False)}
</input_data>
"""

    resultado = gemini.generar_json(
        prompt
    )

    finales_validos = [
        "sin_final",
        "muerte heroe",
        "rescate princesa",
        "Alianza goblin",
        "Escape",
        "muerte princesa"
    ]

    if resultado["final"] not in finales_validos:

        raise ValueError(
            "Final inválido devuelto por Gemini"
        )

    return resultado