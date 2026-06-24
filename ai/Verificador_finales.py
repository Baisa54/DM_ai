# ai/verificador_finales.py

import json
from ai.GeminiClient import GeminiClient


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