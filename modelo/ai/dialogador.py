#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Dialogador
#
# Dialogador es el que se encarga de gestionar los dialogos entre los personajes
# y el jugador. La idea es analizar si un NPC habla, extraer su dialogo, dejar la
# narracion sin dialogos para luego acomodar el mensaje final
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Prompt para la IA, en la que se detalla el comportamiento de dialogador
#   y lo que debe devolver. Este prompt debe estar en formato JSON.
# @ Dialogador, funcion que envia el prompt a la IA y devuelve el 
#   JSON resultante.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
#
# @ Dialogador, funcion que recibe como parametro 
#   [Narracion que genera el DM]
#   --> Se encarga de extraer el dialogo del personaje mas importante
#   --> Se encarga de extraer la emocion del personaje mas importante
#   --> Se encarga de eliminar el dialogo del personaje mas importante de la narracion
#   --> Se encarga de devolver el JSON resultante
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import json

HERRAMIENTA_EXTRAER_DIALOGO = {
    "name": "extraer_dialogo_npc",
    "description": "Analiza una narración para extraer el diálogo directo del NPC más importante y reescribe la narración sin diálogos.",
    "parameters": {
        "type": "object",
        "properties": {
            "narracion_analisis": {
                "type": "string",
                "description": "Piensa brevemente: ¿Hay diálogos directos? ¿Quién los dice? Ignora al héroe. Si hablan varios NPCs, elige al que diga la frase más importante."
            },
            "Personaje": {
                "type": "string",
                "enum": ["companero", "goblin", "princesa", "osgo"],
                "description": "Nombre del NPC que habla. Si nadie habla o solo habla el héroe, omite este campo o envíalo vacío.",
                "nullable": True
            },
            "Emocion": {
                "type": "string",
                "enum": ["feliz", "triste", "enojado", "asustado", "sorprendido", "neutral"],
                "description": "Emoción que transmite el diálogo. Omite si nadie habla.",
                "nullable": True
            },
            "dialogo": {
                "type": "string",
                "description": "Texto exacto pronunciado por el NPC (sin comillas). Omite si nadie habla.",
                "nullable": True
            }
        },
        "required": ["narracion_analisis"]
    }
}

def dialogador(narracion, personajes_presentes=None):
    from modelo.configuracion import ConfigManager
    config = ConfigManager()
    
    if config.get_proveedor_texto() == "gemini":
        from modelo.ai.GeminiClient import GeminiClient
        cliente = GeminiClient()
    else:
        from modelo.ai.LocalAICLient import LocalAIClient
        cliente = LocalAIClient()

    personajes_str = ", ".join(personajes_presentes) if personajes_presentes else "ninguno"

    prompt = f"""<system>
Eres el Dialogador del motor RPG. Eres una máquina de procesamiento estructural.
NO DEBES RESPONDER CON TEXTO NORMAL. TU ÚNICO PROPÓSITO ES INVOCAR LA HERRAMIENTA `extraer_dialogo_npc`.

Reglas:
- Se te entregará una narración generada por el DM. Debes detectar si un NPC importante habló.
- Personajes físicamente presentes en la escena: [{personajes_str}]. SOLO puedes extraer diálogos de estos personajes.
- Si hablan varios NPCs, extrae solo el diálogo más relevante o impactante para la historia.
- Si el héroe habla, ignóralo, solo nos importan los NPCs.
- Si la narración menciona que un personaje habla pero NO ESTÁ en la lista de personajes presentes, ignóralo por completo.
- DEBES usar la herramienta provista para enviar tu respuesta estructurada. NUNCA respondas con texto libre.
</system>

<narracion_original>
{narracion}
</narracion_original>
"""

    resultado = cliente.generar_con_herramienta(prompt, HERRAMIENTA_EXTRAER_DIALOGO)

    personaje = resultado.get("Personaje")
    emocion = resultado.get("Emocion")

    if personaje:
        personaje = personaje.strip().lower()

    if emocion:
        emocion = emocion.strip().lower()

    # MAPEAR
    MAP_PERSONAJES = {
        "companero": "companero",
        "compañero": "companero",
        "aelar": "companero",
        "elfo": "companero",
        "arquero": "companero",
        "goblin": "goblin",
        "goblins": "goblin",
        "princesa": "princesa",
        "osgo": "osgo",
        "orco": "osgo"
    }

    MAP_EMOCIONES = {
        "feliz": "feliz",
        "triste": "triste",
        "enojado": "enojado",
        "asustado": "asustado",
        "sorprendido": "sorprendido",
        "neutral": "neutral"
    }

    personaje_mapeado = MAP_PERSONAJES.get(personaje) if personaje else None
    emocion_mapeada = MAP_EMOCIONES.get(emocion) if emocion else None

    if personaje and not personaje_mapeado:
        print(f"[Dialogador] Advertencia: Personaje '{personaje}' no reconocido. Se ignorará.")
        
    if emocion and not emocion_mapeada:
        print(f"[Dialogador] Advertencia: Emoción '{emocion}' no reconocida. Se ignorará.")

    return {
        **resultado,
        "Personaje": personaje_mapeado,
        "Emocion": emocion_mapeada
    }