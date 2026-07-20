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

    from modelo.game.campaign import SALAS
    ubicacion_actual = estado.get_ubicacion()
    datos_sala = SALAS.get(ubicacion_actual, {})
    salidas_validas = datos_sala.get("salidas", [])
    descripcion_sala = datos_sala.get("descripcion", "")
    objetos_sala = datos_sala.get("objetos", [])

    entrada = {
        "accion_jugador": accion,
        "estado_partida": estado.to_dict(),
        "entorno_fisico_actual": {
            "descripcion": descripcion_sala,
            "objetos_en_el_suelo": objetos_sala
        },
        "salidas_validas_desde_aqui": salidas_validas
    }

    prompt = f"""Eres el Árbitro implacable del juego.
Tu trabajo es evitar que el jugador haga trampa o alucine elementos que no existen. Revisa detenidamente el inventario del jugador, quién está en la sala, y a dónde puede moverse antes de permitir la acción.
El jugador no conoce los nombres internos de las 'salidas_validas_desde_aqui'. Si su acción describe avanzar, entrar, abrir puertas o explorar en una dirección que lógicamente concuerda con avanzar en la aventura, debes ACEPTARLA ('accion_valida': true). Solo rechaza el movimiento si intenta teletransportarse o atravesar paredes.
EXCEPCIÓN IMPORTANTE: Si el jugador intenta huir de la aventura, abandonar la misión, o escapar definitivamente hacia el exterior, esto SIEMPRE ES UNA ACCIÓN VÁLIDA y debes permitirla ('accion_valida': true).
Si el jugador intenta atacar con un arma, DEBE tener esa arma específica en su inventario, de lo contrario la acción es inválida.
REGLAS ESTRICTAS DE PUERTAS:
Si la accion del jugador implica moverse, entrar, mirar o acercarse a "sala_osgo" o a la sala del jefe, DEBE OBLIGATORIAMENTE tener el objeto "llave_templo" en su inventario. Sin esa llave, DEBES rechazar la accion obligatoriamente ("accion_valida": false, "dificultad": 0).

REGLAS PARA TIRADA DE DADOS (requiere_tirada):
- Moverse libremente de una sala a otra, observar el entorno o recoger objetos del suelo, NUNCA requieren tirada (requiere_tirada: false).
- Atacar, defenderse, forzar puertas y CUALQUIER ACCION VERBAL que busque INFLUIR a un NPC (como mentir, engañar, intimidar o persuadir) SIEMPRE requieren tirada obligatoriamente (requiere_tirada: true).

RECUERDA: Si el jugador dice "le miento", es "requiere_tirada": true. Si intenta "entrar a sala de osgo" sin llave, es "accion_valida": false.

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

    # normalizar requiere_tirada y accion_valida
    requiere_tirada = resultado.get("requiere_tirada", False)
    if isinstance(requiere_tirada, str):
        requiere_tirada = requiere_tirada.lower() == "true"
    resultado["requiere_tirada"] = bool(requiere_tirada)

    accion_valida = resultado.get("accion_valida", True)
    if isinstance(accion_valida, str):
        accion_valida = accion_valida.lower() == "true"
    resultado["accion_valida"] = bool(accion_valida)

    dificultades_validas = [0, 5, 10, 15, 20]
    if dificultad not in dificultades_validas:
        dificultad = 10 if resultado["requiere_tirada"] else 0

    resultado["dificultad"] = dificultad

    return resultado