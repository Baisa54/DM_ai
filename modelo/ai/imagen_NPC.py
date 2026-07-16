#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Imagenes de dialogos 
#
# Imagenes de dialogos es el encargado de generar imagenes de dialogos
# a partir de una descripcion y los personajes.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ prompt_visual, prompt que se encarga de generar la imagen del personaje
#   y que se pasa como parametro para generar la imagen del personaje.
# @ generar_imagen_dialogo, funcion que se encarga de generar la imagen del personaje
#   a partir de una descripcion y los personajes.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ generar_imagen_dialogo, recibe como parametro el personaje y la emoción
#   --> Devuelve la imagen generada
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.ai.LocalAICLient import LocalAIClient
from modelo.ai.GeminiClient import GeminiClient
from modelo.configuracion import ConfigManager

PROMPT_IMAGEN_DIALOGO = """
Eres un generador de retratos para un RPG narrativo.

Tu tarea es generar únicamente un retrato de personaje
para interfaz de videojuego.

REGLAS OBLIGATORIAS:

- Mantener identidad visual del personaje
- NO cambiar:
    raza, edad, ojos, cabello, vestimenta, equipamiento

- SOLO cambiar la expresión facial según la emoción

- Encuadre:
    rostro + hombros + parte superior del torso

- Fondo simple y neutral

- Estilo:
    comic fantasy RPG, D&D cinematic art

- Prohibido:
    texto, UI, logos, marcas de agua, globos de diálogo

Emoción a representar:
{emocion}

Descripción del personaje:
{descripcion}
"""


# --------------------------------------------------
# FUNCIÓN CORREGIDA
# --------------------------------------------------

def generar_imagen_dialogo(personaje, emocion):

    config = ConfigManager()
    if config.get_proveedor_imagen() == "gemini":
        cliente = GeminiClient()
    else:
        cliente = LocalAIClient()

    # usamos SOLO prompt_visual del personaje
    prompt_final = PROMPT_IMAGEN_DIALOGO.format(
        emocion=emocion,
        descripcion=personaje["prompt_visual"]
    )

    imagen_generada = cliente.generar_imagen(prompt_final)

    return {
        "imagen": imagen_generada
    }