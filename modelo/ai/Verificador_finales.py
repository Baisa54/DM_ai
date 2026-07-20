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
import json

HERRAMIENTA_VERIFICAR_FINAL = {
    "name": "verificar_final_juego",
    "description": "Cruza el estado actual del juego y la última narración para determinar si el juego ha terminado en alguno de los finales oficiales.",
    "parameters": {
        "type": "object",
        "properties": {
            "razonamiento": {
                "type": "string",
                "description": "Explica brevemente por qué se cumple o no se cumple un final, basándote en el estado de los personajes y la narración."
            },
            "final": {
                "type": "string",
                "enum": ["sin_final", "muerte heroe", "rescate princesa", "Alianza goblin", "Escape", "muerte princesa"],
                "description": "El final alcanzado. Si no hay indicios claros de que el juego haya terminado, usa 'sin_final'."
            }
        },
        "required": ["razonamiento", "final"]
    }
}

def verificar_final(estado, narracion):
    from modelo.configuracion import ConfigManager
    config = ConfigManager()
    
    if config.get_proveedor_texto() == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        cliente = GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        cliente = LocalAIClient()

    entrada = {
        "estado_partida": estado.to_dict(),
        "narracion": narracion
    }

    prompt = f"""<system>
Eres el Verificador de Finales del juego. Eres una máquina de procesamiento estructural.
NO DEBES RESPONDER CON TEXTO NORMAL. TU ÚNICO PROPÓSITO ES INVOCAR LA HERRAMIENTA `verificar_final_juego`.

Tu tarea es decidir si la partida ha terminado basándote en la última narración y el estado.
REGLAS ESTRICTAS DE FINALES:
1. "muerte heroe": Solo si el héroe está muerto (estado "muerto") o la narración dice explícitamente que murió.
2. "Escape": Si la narración dice explícitamente que el héroe huye, abandona la misión, o se aleja definitivamente de la aventura, sin importar en qué sala se encuentre.
3. "Alianza goblin": Solo si el héroe se alía con los goblins o con Osgo.
4. "rescate princesa": Solo si Osgo está muerto, la princesa está viva, y la narración dice que fue rescatada.
5. "muerte princesa": Solo si la princesa muere.

Si ninguna condición se cumple explícitamente de forma concluyente, el final es "sin_final".
DEBES usar la herramienta provista para enviar tu respuesta. NUNCA respondas con texto libre.
</system>

<contexto_actual>
{json.dumps(entrada, indent=4, ensure_ascii=False)}
</contexto_actual>
"""

    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_VERIFICAR_FINAL)

    # -----------------------------
    # DEBUG
    # -----------------------------
    print("\n" + "=" * 80)
    print("RESPUESTA VERIFICADOR FINAL RAW:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
    print("=" * 80 + "\n")

    finales_validos = [
        "sin_final",
        "muerte heroe",
        "rescate princesa",
        "Alianza goblin",
        "Escape",
        "muerte princesa"
    ]

    final = resultado.get("final", "sin_final")
    if final not in finales_validos:
        final = "sin_final"
        
    resultado["final"] = final

    return resultado