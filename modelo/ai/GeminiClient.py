#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# GeminiClient
#
# GeminiClient es el cliente que se utiliza para comunicarse con la IA local
# La idea es que tenga metodos para generar texto, imagenes y JSON.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ GeminiClient, clase que se encarga de comunicarse con Genai a traves de un 
#   prompt, ya sea para generar texto, imagenes o JSON. Lo hace a traves de API_key
#   Que de momento esta HardCodeada. 
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ToDo
# 
# --> No depender de API_key en el codigo (Dependencia del sistema)
# --> Que pueda elegir entre varios modelos
# --> Que pueda elegir entre varios proveedores
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ _retry, funcion que se encarga de reintentar la peticion a la IA en caso de 
#   que falle. Recibe como parametro la funcion que se encarga de hacer la peticion
#   y el numero maximo de reintentos.
# @ _call, funcion que se encarga de hacer la peticion a la IA
#   --> Recibe el modelo y el prompt
#   --> Devuelve la respuesta
# @ generar_texto, funcion que se encarga de generar texto
#   --> Recibe el prompt
#   --> Devuelve el texto generado
# @ generar_imagen, funcion que se encarga de generar imagenes
#   --> Recibe el prompt y las imagenes de referencia
#   --> Devuelve la imagen generada
# @ generar_json, funcion que se encarga de generar JSON
#   --> Recibe el prompt
#   --> Devuelve el JSON generado
# @ generar_json, funcion que se encarga de generar JSON
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import json
# json para el manejo de datos
import os
# os para el manejo de archivos
import time
# time para el manejo de tiempos
import random
# random para el manejo de aleatoriedad
import json
# json para el manejo de datos
from google import genai
# genai para el manejo de la IA
from PIL import Image
# Image para el manejo de imagenes
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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