from GeminiClient import GeminiClient

PROMPT_IMAGEN_DIALOGO = """
Eres un generador de retratos para un RPG narrativo.

Tu tarea es generar únicamente un retrato de personaje
para ser utilizado en una interfaz de videojuego.

REGLAS OBLIGATORIAS:

- Debes respetar completamente la apariencia del personaje
  mostrada en la imagen de referencia.

- NO cambies:
    - raza
    - sexo
    - edad aparente
    - color de ojos
    - color de cabello
    - vestimenta
    - equipamiento
    - estilo visual general

- Únicamente modifica la expresión facial para reflejar
  la emoción recibida.

- El personaje debe aparecer dentro de un recuadro
  típico de diálogo de videojuego RPG.

- Mostrar únicamente:
    - rostro
    - hombros
    - parte superior del torso

- Fondo simple y discreto.

- Estilo visual:
    Comic de fantasía heroica estilo D&D.

- Calidad alta.

- No agregar:
    - texto
    - subtítulos
    - globos de diálogo
    - carteles
    - interfaces
    - marcas de agua

- La imagen debe centrarse en la expresión facial.

La emoción a representar es:
{emocion}
"""


def generar_imagen_dialogo(
    imagen_personaje,
    emocion
):

    gemini = GeminiClient()

    prompt = PROMPT_IMAGEN_DIALOGO.format(
        emocion=emocion
    )

    imagen_generada = gemini.generar_imagen(
        prompt=prompt,
        imagen_referencia=imagen_personaje
    )

    return {
        "imagen": imagen_generada
    }