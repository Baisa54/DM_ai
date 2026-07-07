#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Arbitro de acción
#
# Este programa es la vista grafica de la aplicacion DM AI
# La idea general es hacer una taberna de fondo con una imagen,
# Luego, abajo una barra de chat en conjunto con un boton enviar
# Para que el usaurio escriba sus acciones.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Imagen de fondo de una taberna.
# @ Barra inferior de madera
# @ [En barra inferior] Boton enviar
# @ [En barra inferior] chat para escribir la accion del usuario
# @ Pergamino donde se narra historia
# @ Pergamino donde se muestra imagen resumen
# @ Pergamino (Opcional) donde se muestra texto generado por un personaje
# @ Pergamino (Opcional) donde se muestra imagen NPC
# @ Barra superior de madera
# @ [En barra superior] Boton para estado
# @ [En barra superior] Boton reiniciar aventura
# @ [En barra superior] Imagen DM_ai con gorro
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS DEL USUARIO
#
# @ Accion escrita & Boton enviar (Enviar accion)
#   --> Se valida si hay algo escrito
#   --> Si no hay nada escrito, se muestra mensaje de error
#   --> Si hay algo escrito, se muestra mensaje de que se esta procesando
#
# @ Accion de Boton de estado
#   --> Se muestra una ventana emergente
#   --> La ventana posee boton de salida
#   --> La ventana muestra el estado de la partida
#
# @ Accion de Boton reiniciar 
#   --> Se muestra una ventana emergente
#   --> La ventana muestra que una vez realizada la accion no hay vuelta atras
#   --> Posee un boton de 'Reiniciar' que reinicia la partida
#   --> Posee un boton de 'Cancelar' que cierra la ventana 
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

import json
from ai.LocalAICLient import LocalAIClient as GeminiClient
# from ai.GeminiClient import GeminiClient

PROMPT_ARBITRO_ACCION = """
Eres el árbitro de un RPG narrativo.

Tu tarea es analizar la acción del jugador
considerando el estado actual de la partida.

Debes responder EXCLUSIVAMENTE un JSON válido.
DEVUELVE SIEMPRE UN JSON COMPLETO CON LAS 3 CLAVES:
NO OMITAS NINGUNA CLAVE.
NO AGREGUES TEXTO.
NO EXPLIQUES NADA.
RESPONDE SOLO JSON VÁLIDO.
NO EXPLICACIONES.
NO BACKTICKS.
TODAS LAS CLAVES ENTRE COMILLAS.
NO FALTAR COMAS.

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
    "dificultad": 0
}

- Si debe realizar tirada:
{
    "accion_valida": true,
    "requiere_tirada": true,
    "dificultad": 5 / 10 / 15 / 20
}

- Dificultades permitidas:
5 = fácil
10 = media
15 = difícil
20 = extremadamente difícil

IMPORTANTE:
- Usa SOLO números enteros en dificultad
- No uses comillas en números
- No expliques nada
- No agregues campos extra
- Si dudas, usa dificultad 10
"""

def arbitrar_accion(accion, estado):

    gemini = GeminiClient()

    entrada = {
        "accion_jugador": accion,
        "estado_partida": estado.to_dict()
    }

    prompt = f"""
    {PROMPT_ARBITRO_ACCION}

    DATOS DE ENTRADA:

    {json.dumps(
        entrada,
        indent=4,
        ensure_ascii=False
    )}
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