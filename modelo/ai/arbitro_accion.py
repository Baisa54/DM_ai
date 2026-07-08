#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Arbitro de acción
#
# Arbitro accion es el que finje ser DM para decidir si la accion del jugador 
# es valida o no, y si se requiere una tirada de dados. La idea es que devuelva si
# es valida o no la accion, la dificultad para la tirada de dados y si se requiere
# realizar la tirada de dados.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Prompt para la IA, en la que se detalla el comportamiento de arbitro de accion
#   y lo que debe devolver. Este prompt debe estar en formato JSON.
# @ Arbitrar Accion, funcion que envia el prompt a la IA y devuelve el 
#   JSON resultante.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
#
# @ Arbitrar Accion, funcion que recibe como parametro 
#   [Accion que realiza el jugador]
#   [Estado de la partida]
#   --> Se valida si la accion es posible segun el estado de la partida
#   --> Se devuelve el JSON resultante
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import json
# json para el manejo de datos
from modelo.ai.LocalAICLient import LocalAIClient as GeminiClient
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
#-@ from modelo.ai.GeminiClient import GeminiClient 
# GeminiClient es el cliente que se utiliza para comunicarse con la IA de google
# Actualmente comentada porque no se esta usando gemini, sino una IA local
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

PROMPT_ARBITRO_ACCION = """<system>
Eres el motor lógico y Árbitro de Acciones de un RPG de texto. Eres un autómata de procesamiento de datos, NO un asistente conversacional. Tu única función es evaluar la acción del jugador contra el estado del mundo y devolver una decisión estructurada.
</system>

<rules>
1. VIABILIDAD: Comprueba estrictamente el inventario, ubicación y NPCs presentes. Si la acción es lógicamente imposible (usar un objeto que no se posee, interactuar con alguien ausente), la acción es inválida.
2. TIRADAS: Solo se requiere tirada (true) si la acción es posible PERO tiene riesgo de fracaso, esfuerzo físico, conflicto o resistencia. Acciones mundanas, caminar, mirar, o hablar de forma casual NO requieren tirada (false).
3. DIFICULTAD: 
   - Si no requiere tirada o es inválida, la dificultad DEBE ser 0.
   - Si requiere tirada, asigna SOLO UN entero: 5 (fácil), 10 (normal), 15 (difícil) o 20 (heroica).
</rules>

<output_schema>
Debes retornar EXCLUSIVAMENTE este objeto JSON, sin llaves adicionales:
{
  "accion_valida": booleano (true o false),
  "requiere_tirada": booleano (true o false),
  "dificultad": entero (0, 5, 10, 15 o 20)
}
</output_schema>

<formatting_constraints>
- RESPUESTA PURA: No agregues "```json", ni "```", ni introducciones, ni saludos, ni explicaciones.
- ESTRUCTURA DE INICIO: Tu respuesta DEBE empezar con el carácter '{' y terminar con el carácter '}'.
- TIPO DE DATOS: Usa valores booleanos nativos de JSON (true/false, sin comillas). La dificultad debe ser un número entero (nunca null, nunca texto).
</formatting_constraints>
"""

def arbitrar_accion(accion, estado):

    gemini = GeminiClient()

    entrada = {
        "accion_jugador": accion,
        "estado_partida": estado.to_dict()
    }

    prompt = f"""{PROMPT_ARBITRO_ACCION}

<input_data>
{json.dumps(entrada, indent=4, ensure_ascii=False)}
</input_data>
"""

    resultado = gemini.generar_json(prompt)

    # -----------------------------
    # DEBUG BRUTAL
    # -----------------------------
    print("\n" + "=" * 80)
    print("RESPUESTA ARBITRO RAW:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
    print("=" * 80 + "\n")

    required_keys = ["accion_valida", "requiere_tirada", "dificultad"]

    # -----------------------------
    # VALIDACIÓN FLEXIBLE
    # -----------------------------
    for key in required_keys:
        if key not in resultado:
            raise ValueError(f"[ARBITRO] Falta clave obligatoria: {key} -> {resultado}")

    # normalizar dificultad (MUY IMPORTANTE)
    dificultad = resultado.get("dificultad", None)

    # casos válidos explícitos
    if dificultad is None:
        if resultado["requiere_tirada"]:
            raise ValueError(f"[ARBITRO] dificultad=None pero requiere_tirada=True -> {resultado}")
        dificultad = 0

    # si viene como string accidental
    if isinstance(dificultad, str):
        try:
            dificultad = int(dificultad)
        except:
            raise ValueError(f"[ARBITRO] dificultad no numérica -> {dificultad}")

    dificultades_validas = [0, 5, 10, 15, 20]

    if dificultad not in dificultades_validas:
        raise ValueError(
            f"[ARBITRO] Dificultad inválida: {dificultad} | esperado {dificultades_validas} -> {resultado}"
        )

    resultado["dificultad"] = dificultad

    return resultado