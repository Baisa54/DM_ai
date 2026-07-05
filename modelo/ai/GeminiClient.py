import os
import time
import random
import json
from google import genai
from PIL import Image


class GeminiClient:

    def __init__(self):

        self.client = genai.Client(
            api_key=""
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

                print(f"[Gemini Error] {e}")

                error_texto = str(e)

                errores_sin_retry = [
                    "429",
                    "400",
                    "401",
                    "403"
                ]

                if any(
                    codigo in error_texto
                    for codigo in errores_sin_retry
                ):
                    raise e

                espera = (2 ** intento) + random.uniform(0, 1)

                print(
                    f"[Retry] intento {intento+1}/{max_reintentos} en {espera:.2f}s"
                )

                time.sleep(espera)

        raise Exception("Gemini falló después de múltiples intentos")

    # --------------------------------------------------
    # TEXTO
    # --------------------------------------------------
    def generar_texto(
        self,
        prompt,
        modelo="gemini-2.5-flash"
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
        modelo="gemini-2.0-flash-lite"
    ):

        def request():
            respuesta = self._call(modelo, prompt)
            print("================================")
            print("RESPUESTA GEMINI:")
            print(respuesta.text)
            print("================================")
            return json.loads(respuesta.text)

        return self._retry(request)