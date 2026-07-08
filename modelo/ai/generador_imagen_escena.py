#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Generador de imagen de escena
#
# Generador de imagen de escena es el encargado de generar imagenes de la escena
# a partir de una descripcion y los personajes.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Generador de imagen de escena, funcion que se encarga de generar imagenes de la escena
#   a partir de una descripcion y los personajes.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ Generador de imagen de escena, recibe como parametro la descripcion de la escena
#   y los personajes.
#   --> Devuelve la imagen generada
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from ai.LocalAICLient import LocalAIClient
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
#-@ from ai.GeminiClient import GeminiClient
# GeminiClient es el cliente que se utiliza para comunicarse con la IA de google
# Actualmente comentada porque no se esta usando gemini, sino una IA local
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

PROMPT_IMAGEN_ESCENA = """
Fantasy RPG illustration.

Style:
Dungeons and Dragons.
Dark Fantasy.
High quality concept art.
Digital painting.
Cinematic lighting.
Detailed environment.

Rules:

* Show only the characters described.
* Respect character appearance.
* No text.
* No captions.
* No speech bubbles.
* No UI.
* Single coherent scene.
  """

def generar_imagen_escena(
    narracion,
    prompts_personajes
    ):

    personajes = "\n".join(prompts_personajes)

    prompt_final = f"""

    {PROMPT_IMAGEN_ESCENA}

    CHARACTERS:

    {personajes}

    SCENE DESCRIPTION:

    {narracion}
    """

    print("\n" + "=" * 80)
    print("PROMPT IMAGEN")
    print("=" * 80)
    print(prompt_final)
    print("=" * 80)

    try:

        return LocalAIClient().generar_imagen(
            prompt_final
        )

    except Exception as e:

        print("\n[ERROR GENERANDO IMAGEN]")
        print(str(e))

        return None
