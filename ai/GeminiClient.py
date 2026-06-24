import os
from google import genai
import json
from PIL import Image

class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=""
        )

    def generar_texto(
        self,
        prompt,
        modelo="gemini-2.5-flash"
    ):

        respuesta = self.client.models.generate_content(
            model=modelo,
            contents=prompt
        )

        return respuesta.text

    def generar_imagen(
        self,
        prompt,
        imagenes_referencia=None,
        modelo="gemini-2.0-flash-preview-image-generation"
    ):

        contenidos = [
            prompt
        ]

        if imagenes_referencia is not None:

            for ruta in imagenes_referencia:

                contenidos.append(
                    Image.open(ruta)
                )

        respuesta = self.client.models.generate_content(
            model=modelo,
            contents=contenidos
        )

        return respuesta
    
    def generar_json(
        self,
        prompt,
        modelo="gemini-2.5-flash"
    ):

        respuesta = self.client.models.generate_content(
            model=modelo,
            contents=prompt
        )

        return json.loads(
            respuesta.text
        )