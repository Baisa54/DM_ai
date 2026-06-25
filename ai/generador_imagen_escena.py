from ai.LocalAICLient import LocalAIClient 
# from ai.GeminiClient import GeminiClient

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

# --------------------------------------------------

# FUNCION PRINCIPAL

# --------------------------------------------------

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
