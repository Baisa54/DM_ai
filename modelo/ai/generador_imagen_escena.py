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
from modelo.ai.LocalAICLient import LocalAIClient
from modelo.ai.GeminiClient import GeminiClient
from modelo.configuracion import ConfigManager

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
    prompts_personajes,
    rutas_imagenes=None
    ):

    personajes = "\n".join(prompts_personajes)

    prompt_instrucciones = f"""
    Eres un experto en redactar prompts para generadores de imágenes por IA (tipo Midjourney/DALL-E).
    Necesito que crees UN SOLO prompt en INGLÉS detallado y optimizado basado en esta narración y personajes.
    Debe centrarse puramente en la parte visual: iluminación, composición, aspecto de los personajes y el entorno.
    
    {PROMPT_IMAGEN_ESCENA}

    CHARACTERS:
    {personajes}

    SCENE DESCRIPTION:
    {narracion}
    
    DEVUELVE ÚNICA Y EXCLUSIVAMENTE EL PROMPT EN INGLÉS, SIN INTRODUCCIONES NI COMILLAS NI NOTAS ADICIONALES.
    """

    print("\n" + "=" * 80)
    print("PIDIENDO A LA IA LOCAL QUE MEJORE EL PROMPT...")
    try:
        local_ai = LocalAIClient()
        prompt_optimizado = local_ai.generar_texto(prompt_instrucciones).strip()
        print("PROMPT OPTIMIZADO GENERADO:")
        print(prompt_optimizado)
        print("=" * 80)

        config = ConfigManager()
        if config.get_proveedor_imagen() == "gemini":
            gemini = GeminiClient()
            return gemini.generar_imagen(
                prompt=prompt_optimizado,
                imagenes_referencia=rutas_imagenes
            )
        else:
            return LocalAIClient().generar_imagen(prompt_optimizado)

    except Exception as e:
        print("\n[ERROR GENERANDO IMAGEN]")
        print(str(e))
        return None
