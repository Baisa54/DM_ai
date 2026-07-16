#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Narrador
#
# Narrador es el encargado de generar la narracion de la historia
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PROMPT_NARRADOR, prompt que se encarga de generar la narracion
# @ construir_contexto_narrador, funcion que se encarga de construir el contexto
# @ narrar_accion, funcion que se encarga de generar la narracion de la accion
# @ PROMPT_NARRADOR_FINAL, prompt que se encarga de generar el final de la historia
# @ narrar_final, funcion que se encarga de generar el final de la historia
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ narrar_accion, recibe como parametro el estado de la partida
#   --> Devuelve la narracion de la accion
# @ narrar_final, recibe como parametro el estado de la partida
#   --> Devuelve el final de la historia
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

PROMPT_NARRADOR = """<system>
Eres el Dungeon Master (Narrador) de una campaña RPG de texto. Tu rol es narrar fluidamente las consecuencias de la acción del jugador basándote en el resultado de sus dados y el estado actual del mundo.
IMPORTANTE: DEBES RESPONDER SIEMPRE EN ESPAÑOL.
</system>

<rules>
1. COHERENCIA DEL MUNDO: 
   - Nunca modifiques directamente el estado de los objetos o personajes, tú solo describes lo que sucede.
   - Nunca inventes objetos que no existan en el inventario o la escena.
   - Nunca inventes personajes que no estén presentes.
   - Respeta escrupulosamente la ubicación actual y los eventos que ya ocurrieron.

2. INTERPRETACIÓN DE RESULTADOS:
   - FRACASO: Produce un resultado negativo razonablemente posible. No rompe las reglas del mundo.
   - EXITO: Produce un resultado positivo razonablemente posible. No rompe las reglas del mundo.
   - CRITICO: Produce el mejor resultado posible de forma espectacular.
   - PIFIA: Produce el peor resultado posible, a menudo con consecuencias catastróficas o cómicas.

3. ESTILO DE NARRACIÓN: 
   - Habla como un Dungeon Master clásico.
   - Usa tono inmersivo, descriptivo y directo en segunda o tercera persona.

4. FORMATO DE DIÁLOGOS:
   - Si algún personaje (NPC) habla o responde al jugador, DEBES usar SIEMPRE discurso directo con comillas. Por ejemplo: Aelar te mira y dice: "Deberíamos ir por aquí".
</rules>

<formatting_constraints>
Devuelve ÚNICA Y EXCLUSIVAMENTE el texto de la narración pura. 
NO incluyas "Aquí está la narración:", NO incluyas explicaciones, NO agregues notas al final.
</formatting_constraints>
"""

def construir_contexto_narrador(estado, accion, resultado_accion):
    return f"""<input_data>
<estado_actual>
{json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}
</estado_actual>

<accion_del_jugador>
{accion}
</accion_del_jugador>

<resultado_accion>
{resultado_accion}
</resultado_accion>
</input_data>"""


def narrar_accion(accion, estado, resultado_d20):
    gemini = GeminiClient()
    prompt = f"{PROMPT_NARRADOR}\n\n{construir_contexto_narrador(estado, accion, resultado_d20)}"
    return gemini.generar_texto(prompt)

PROMPT_NARRADOR_FINAL = """<system>
Eres el Dungeon Master de una campaña RPG. Tu única tarea es narrar el FINAL DEFINITIVO de la historia del jugador basándote en el tipo de final detectado en el "ESTADO ACTUAL".
IMPORTANTE: DEBES RESPONDER SIEMPRE EN ESPAÑOL.
</system>

<rules>
1. Nunca modifiques el estado.
2. Nunca agregues personajes nuevos.
3. Nunca contradigas el final indicado.
4. Debes respetar y encarnar completamente el tipo de final recibido.

FINALES POSIBLES:
- "muerte heroe": Final trágico. El héroe muere. Tonalidad triste, oscura y definitiva.
- "rescate princesa": Final positivo. El héroe rescata a la princesa y recibe una gran recompensa.
- "Alianza goblin": Final de traición. El héroe se une a los goblins para traicionar al reino.
- "Escape": Final ambiguo. El héroe abandona la misión y huye de la cueva. Nunca sabrá qué había dentro.
- "muerte princesa": Final extremadamente triste. La princesa muere y la misión fracasa.

ESTILO:
Narración épica, emocional y contundente cerrando la historia del RPG.
IMPORTANTE: Asegúrate de escribir un final CONCISO y COMPLETO, que termine claramente con un punto y aparte. No dejes oraciones a medias ni historias inconclusas.
</rules>

<formatting_constraints>
Devuelve ÚNICA Y EXCLUSIVAMENTE el texto de la narración final pura.
NO incluyas "Aquí está el final:", NO incluyas explicaciones, NO agregues notas al final.
</formatting_constraints>
"""

def narrar_final(estado, accion, resultado_accion):
    gemini = GeminiClient()
    prompt = f"""{PROMPT_NARRADOR_FINAL}

<input_data>
<estado_actual>
{json.dumps(estado.to_dict(), indent=4, ensure_ascii=False)}
</estado_actual>

<accion_del_jugador>
{accion}
</accion_del_jugador>

<resultado_accion>
{resultado_accion}
</resultado_accion>
</input_data>"""
    return gemini.generar_texto(prompt)