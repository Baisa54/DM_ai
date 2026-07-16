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
import json

HERRAMIENTA_EVALUAR_ACCION = {
    "name": "evaluar_accion_jugador",
    "description": "Evalúa estrictamente si la acción del jugador es lógicamente posible basándose en su inventario, ubicación actual y entidades presentes en la sala.",
    "parameters": {
        "type": "object",
        "properties": {
            "analisis_inventario_y_entorno": {
                "type": "string",
                "description": "Razonamiento estricto: ¿El jugador posee el objeto que intenta usar? ¿El objetivo o monstruo al que se dirige está físicamente presente en la sala actual? Explica por qué es o no es posible."
            },
            "accion_valida": {
                "type": "boolean",
                "description": "Debe ser false si intenta usar objetos que no tiene, invocar criaturas ausentes o hacer magia sin tener el poder. True solo si físicamente puede intentarlo con lo que tiene."
            },
            "requiere_tirada": {
                "type": "boolean",
                "description": "True solo si la acción es válida y conlleva un riesgo de fracasar (ej: atacar, saltar, empujar). Falso para acciones triviales (hablar, caminar)."
            },
            "dificultad": {
                "type": "integer",
                "enum": [0, 5, 10, 15, 20],
                "description": "0 si es inválida o no requiere tirada. Si requiere: 5 (fácil), 10 (normal), 15 (difícil), 20 (casi imposible)."
            }
        },
        "required": ["analisis_inventario_y_entorno", "accion_valida", "requiere_tirada", "dificultad"]
    }
}

def arbitrar_accion(accion, estado):
    from modelo.configuracion import ConfigManager
    config = ConfigManager()
    
    if config.get_proveedor_texto() == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        cliente = GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        cliente = LocalAIClient()

    entrada = {
        "accion_jugador": accion,
        "estado_partida": estado.to_dict()
    }

    prompt = f"""Eres el Árbitro implacable del juego.
Tu trabajo es evitar que el jugador haga trampa o alucine elementos que no existen. Revisa detenidamente el inventario del jugador y quién está en la sala antes de permitir la acción.
Si el jugador intenta algo para lo que no tiene recursos (ej: 'ataco con una metralleta' o 'llamo a un dragón'), debes marcarlo como inválido.

<contexto_actual>
{json.dumps(entrada, indent=4, ensure_ascii=False)}
</contexto_actual>

Llama a la herramienta para dictaminar."""

    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_EVALUAR_ACCION)

    # -----------------------------
    # DEBUG
    # -----------------------------
    print("\n" + "=" * 80)
    print("RESPUESTA ARBITRO RAW:")
    print(json.dumps(resultado, indent=4, ensure_ascii=False))
    print("=" * 80 + "\n")

    # normalizar dificultad (seguridad adicional por si el LLM falla)
    dificultad = resultado.get("dificultad", 0)
    try:
        dificultad = int(dificultad)
    except:
        dificultad = 0

    dificultades_validas = [0, 5, 10, 15, 20]
    if dificultad not in dificultades_validas:
        dificultad = 10 if resultado.get("requiere_tirada") else 0

    resultado["dificultad"] = dificultad

    return resultado