import os
import time
import random
import json
from google import genai
from PIL import Image


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key="AQ.Ab8RN6I9A53cjPbfjdeK_GmlkYbCpxKK6Iu19HwIetx98RQg0w"
        )

    # --------------------------------------------------
    # CORE CALL (interno)
    # --------------------------------------------------
    def _call(self, model, contents):

        return self.client.models.generate_content(
            model=model,
            contents=contents
        )

    # --------------------------------------------------
    # RETRY WRAPPER
    # --------------------------------------------------
    def _retry(self, func, max_reintentos=5):

        for intento in range(max_reintentos):

            try:
                return func()

            except Exception as e:

                espera = (2 ** intento) + random.uniform(0, 1)

                print(f"[Gemini Error] {e}")
                print(f"[Retry] intento {intento+1}/{max_reintentos} en {espera:.2f}s")

                time.sleep(espera)

        raise Exception("Gemini falló después de múltiples intentos")

    # --------------------------------------------------
    # TEXTO
    # --------------------------------------------------
    def generar_texto(
        self,
        prompt,
        modelo="gemini-2.0-flash"
    ):

        def request():
            return self._call(modelo, prompt).text

        return self._retry(request)

    # --------------------------------------------------
    # IMAGEN
    # --------------------------------------------------
    def generar_imagen(
        self,
        prompt,
        imagenes_referencia=None,
        modelo="gemini-2.0-flash-preview-image-generation"
    ):

        def request():

            contenidos = [prompt]

            if imagenes_referencia:

                for ruta in imagenes_referencia:
                    contenidos.append(Image.open(ruta))

            return self._call(modelo, contenidos)

        return self._retry(request)

    # --------------------------------------------------
    # JSON
    # --------------------------------------------------
    def generar_json(
        self,
        prompt,
        modelo="gemini-2.5-flash"
    ):

        def request():
            respuesta = self._call(modelo, prompt)
            return json.loads(respuesta.text)

        return self._retry(request)