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

PROMPT_VERIFICADOR_FINALES = """
Eres un verificador de finales para un RPG narrativo.

Tu tarea es analizar:

- El estado actual de la partida.
- La narración más reciente.

Debes determinar si se cumple alguno de los finales posibles.

FINALES POSIBLES:

1) muerte heroe

Se cumple únicamente si:

estado_personajes["heroe"] == "muerto"

--------------------------------------------------

2) Escape

Se cumple únicamente si:

- El héroe está en "entrada_cueva"
- La narración indica que abandona la misión,
  se retira o decide no entrar a la cueva.

--------------------------------------------------

3) Alianza goblin

Se cumple únicamente si:

- El héroe se alía con goblins
- O se alía con Osgo
- O traiciona al reino

--------------------------------------------------

4) rescate princesa

Se cumple únicamente si:

- Osgo está muerto

Y

- La princesa está viva

Y

- La narración indica que fue liberada o rescatada

--------------------------------------------------

5) muerte princesa

Se cumple únicamente si:

estado_personajes["princesa"] == "muerto"

--------------------------------------------------

Si ningún final se cumple:

"sin_final"

--------------------------------------------------

Debes devolver EXCLUSIVAMENTE un JSON válido.

Formato:

{
    "final": "sin_final"
}

Valores permitidos:

- "sin_final"
- "muerte heroe"
- "rescate princesa"
- "Alianza goblin"
- "Escape"
- "muerte princesa"

No inventes otros valores.
No escribas explicaciones.
Devuelve únicamente JSON.
"""


def verificar_final(
    estado,
    narracion
):

    gemini = GeminiClient()

    entrada = {
        "estado_partida": estado.to_dict(),
        "narracion": narracion
    }

    prompt = f"""
{PROMPT_VERIFICADOR_FINALES}

DATOS:

{json.dumps(
    entrada,
    indent=4,
    ensure_ascii=False
)}
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