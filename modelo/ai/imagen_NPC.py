from ai.LocalAICLient import LocalAIClient as GeminiClient

# --------------------------------------------------
# PROMPT BASE
# --------------------------------------------------

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

    gemini = GeminiClient()

    # usamos SOLO prompt_visual del personaje
    prompt_final = PROMPT_IMAGEN_DIALOGO.format(
        emocion=emocion,
        descripcion=personaje["prompt_visual"]
    )

    imagen_generada = gemini.generar_imagen(prompt_final)

    return {
        "imagen": imagen_generada
    }