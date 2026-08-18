#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# LocalAICLient
#
# LocalAICLient es el cliente que se utiliza para comunicarse con la IA local
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ _retry, funcion que se encarga de reintentar la solicitud a la IA local
# @ generar_texto, funcion que se encarga de generar texto a partir de una descripcion
# @ generar_json, funcion que se encarga de generar json a partir de una descripcion
# @ generar_imagen, funcion que se encarga de generar imagen a partir de una descripcion
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ _retry, recibe como parametro la funcion que se va a ejecutar
#   --> Devuelve el resultado de la funcion
# @ generar_texto, recibe como parametro el prompt
#   --> Devuelve el texto generado
# @ generar_json, recibe como parametro el prompt
#   --> Devuelve el json generado
# @ generar_imagen, recibe como parametro el prompt
#   --> Devuelve la imagen generada
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import json
# json para el manejo de datos
from huggingface_hub import InferenceClient
# InferenceClient es el cliente que se utiliza para comunicarse con Hugging Face
import requests
# requests es el cliente que se utiliza para comunicarse con la IA local
import time
# time es el cliente que se utiliza para manejar el tiempo
from PIL import Image
# Image es el cliente que se utiliza para manejar las imagenes
from io import BytesIO
# BytesIO es el cliente que se utiliza para manejar los bytes
import re
# re es el cliente que se utiliza para manejar las expresiones regulares
import traceback
# traceback es el cliente que se utiliza para manejar los errores
import socket
# socket es el cliente que se utiliza para manejar las conexiones de red
import requests
# requests es el cliente que se utiliza para manejar las peticiones http
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class LocalAIClient:
    """
    Cliente local para peticiones a Ollama (texto/JSON) y Hugging Face Inference API (imágenes).
    """

    def __init__(self):
        """
        Inicializa la URL local de Ollama y el cliente de Hugging Face.
        """
        from modelo.configuracion import ConfigManager
        self.config = ConfigManager()

        # Ollama local
        self.ollama_url = "http://localhost:11434/api/generate"

        hf_key = self.config.get_huggingface_key()
        self.hf_client = InferenceClient(
            api_key=hf_key if hf_key else None
        )

    # --------------------------------------------------
    # RETRY SIMPLE 
    # --------------------------------------------------
    def _retry(self, func, max_reintentos=3):
        """
        Reintenta una llamada a función si ocurren errores de red o tiempo de espera.
        """
        last_error = None

        for i in range(max_reintentos):

            try:
                return func()

            except Exception as e:

                last_error = e

                print("\n" + "="*80)
                print("[LOCAL AI ERROR - DEBUG MODE]")
                print("="*80)

                # 🔴 ERROR PRINCIPAL
                print(f"\n[ERROR TYPE]")
                print(type(e).__name__)

                print(f"\n[ERROR MESSAGE]")
                print(repr(e))

                # 🔴 TRACEBACK COMPLETO
                print(f"\n[TRACEBACK]")
                traceback.print_exc()

                # 🔴 POSIBLES CAUSAS AUTOMÁTICAS
                print("\n[DIAGNOSTIC CHECKLIST]")

                # 1. RED
                try:
                    socket.create_connection(("8.8.8.8", 53), timeout=2)
                    print(" [OK] Internet Conectado")
                except Exception:
                    print(" [FALLO] Sin Conexión a Internet")

                # 2. OLLAMA LOCAL
                try:
                    r = requests.get("http://localhost:11434", timeout=2)
                    if r.status_code == 200:
                        print(" [OK] Ollama activo localmente")
                    else:
                        print(f" [ADVERTENCIA] Ollama respondió status {r.status_code}")
                except Exception:
                    print(" [FALLO] Ollama NO está corriendo en http://localhost:11434")

                print("="*80 + "\n")

                if i < max_reintentos - 1:
                    time.sleep(2)

        raise last_error

    # --------------------------------------------------
    # TEXTO (OLLAMA)
    # --------------------------------------------------
    def generar_texto(self, prompt):
        """
        Genera texto a través del modelo local de Ollama.
        """
        model = self.config.get_modelo_local()

        def request():
            """Realiza la petición HTTP POST a Ollama para generar texto."""
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_ctx": 8192,       # Contexto amplio para no olvidar reglas ni historial
                    "num_predict": 2048,   # Tokens suficientes para explayarse en la narración
                    "temperature": 0.7     # Temperatura balanceada para narrativa
                }
            }

            r = requests.post(
                self.ollama_url,
                json=payload,
                timeout=3000  
            )

            r.raise_for_status()
            return r.json()["response"]

        return self._retry(request)
    # --------------------------------------------------
    # JSON (OLLAMA + PARSEO ROBUSTO)
    # --------------------------------------------------
    def generar_json(self, prompt):
        """
        Genera y limpia respuestas estructuradas en formato JSON producidas por Ollama.
        """
        model = self.config.get_modelo_local()

        def extract_json(text):
            """Extrae y repara bloques JSON embebidos dentro de respuestas en texto plano."""
            text = text.strip()

            # quitar markdown
            text = text.replace("```json", "").replace("```", "")

            # normalización de valores LLM
            text = text.replace("NULL", "null")
            text = text.replace("None", "null")
            text = text.replace("TRUE", "true")
            text = text.replace("FALSE", "false")
            text = text.replace("True", "true")
            text = text.replace("False", "false")

            start = text.find("{")
            if start == -1:
                raise ValueError(f"[JSON PARSE FAIL] No JSON start encontrado:\n{text}")

            json_str = text[start:]

            if json_str.count("{") > json_str.count("}"):
                json_str += "}" * (json_str.count("{") - json_str.count("}"))

            # extraer bloque más probable
            match = re.search(r"\{[\s\S]*\}", json_str)
            if not match:
                raise ValueError(f"[JSON PARSE FAIL] No JSON encontrado:\n{text}")

            json_str = match.group(0)

            try:
                return json.loads(json_str)

            except json.JSONDecodeError as e:

                print("\n" + "=" * 80)
                print("❌ LOCAL AI JSON ERROR")
                

                print("=" * 80)

                print("\n[ERROR TYPE]")
                print(type(e).__name__)

                print("\n[ERROR MESSAGE]")
                print(str(e))

                print("\n[RAW JSON]")
                print(json_str)

                print("\n[FULL TEXT]")
                print(text)

                # 🔥 reparación automática básica
                repaired = json_str
                repaired = re.sub(r",\s*}", "}", repaired)
                repaired = re.sub(r",\s*]", "]", repaired)

                try:
                    return json.loads(repaired)

                except Exception:
                    print("\n[REPAIR FAILED] JSON irrecuperable")
                    raise e

        # --------------------------------------------------
        # REQUEST OLLAMA
        # --------------------------------------------------
        def request():
            """Envía el prompt formateado para obtener la respuesta JSON desde Ollama."""
            payload = {
                "model": model,
                "prompt": prompt + "\n\nResponde ÚNICAMENTE con un JSON válido. No agregues texto adicional.",
                "stream": False,
                "options": {
                    "num_ctx": 8192,       # Contexto súper amplio para leer todo el JSON y prompt
                    "num_predict": 1024,   # Output JSON suele ser corto, 1024 es sobradísimo
                    "temperature": 0.1     # Temperatura ultra-baja para evitar alucinaciones lógicas
                }
            }

            r = requests.post(
                self.ollama_url,
                json=payload,
                timeout=600
            )

            if r.status_code != 200:
                raise Exception(
                    f"[OLLAMA HTTP ERROR]\n"
                    f"STATUS: {r.status_code}\n"
                    f"BODY: {r.text}"
                )

            data = r.json()

            if "response" not in data:
                raise Exception(f"[OLLAMA BAD RESPONSE FORMAT] {data}")

            text = data["response"].strip()

            if text.count("{") > text.count("}"):
                text += "}"

            return extract_json(text)

        # --------------------------------------------------
        # RETRY WRAPPER
        # --------------------------------------------------
        return self._retry(request)
    
    # --------------------------------------------------
    # IMAGEN que ahora es hugging face
    # --------------------------------------------------

    def generar_imagen(self, prompt):
        """
        Genera una imagen a través de la API de Hugging Face Inference y la guarda temporalmente.
        """

        def request():
            """Genera la imagen en Hugging Face y guarda la ruta en disco."""
            imagen = self.hf_client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )

            import os
            import time
            temp_dir = "modelo/game/assets/temp"
            os.makedirs(temp_dir, exist_ok=True)
            filepath = f"{temp_dir}/img_{int(time.time()*1000)}.png"
            imagen.save(filepath)

            return filepath

        try:
            return self._retry(request)

        except Exception as e:

            print("\n" + "="*80)
            print("NO SE PUDO GENERAR IMAGEN")
            print("="*80)
            print(str(e))

            return None

    # --------------------------------------------------
    # TOOL CALLING (OLLAMA)
    # --------------------------------------------------
    def generar_con_herramienta(self, prompt, herramienta_schema):
        """
        Ejecuta una petición a Ollama enviando la declaración de una herramienta para obtener una respuesta estructurada.
        """
        model = self.config.get_modelo_local()

        def request():
            """Llama a la API /api/chat de Ollama con la definición de la herramienta."""
            url = self.ollama_url.replace("/api/generate", "/api/chat")
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {
                    "temperature": 0.0
                },
                "tools": [
                    {
                        "type": "function",
                        "function": herramienta_schema
                    }
                ]
            }

            import requests
            r = requests.post(
                url,
                json=payload,
                timeout=3000  
            )

            r.raise_for_status()
            respuesta = r.json()
            
            mensaje = respuesta.get("message", {})
            tool_calls = mensaje.get("tool_calls", [])
            
            if not tool_calls:
                raise ValueError("Ollama no devolvió llamadas a herramientas (tool_calls vacío)")
                
            for call in tool_calls:
                func = call.get("function", {})
                if func.get("name") == herramienta_schema["name"]:
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        import json
                        args = json.loads(args)
                        
                    # NORMALIZACIÓN GLOBAL DE BOOLEANOS
                    # Previene el error de LLMs locales devolviendo "false" (string) 
                    # en lugar de false (booleano matemático)
                    def normalize_booleans(d):
                        """
                        Normaliza cadenas 'true' / 'false' devueltas por el modelo a booleanos reales.
                        """
                        if isinstance(d, dict):
                            for k, v in d.items():
                                if isinstance(v, str):
                                    v_low = v.lower().strip()
                                    if v_low == "true":
                                        d[k] = True
                                    elif v_low == "false":
                                        d[k] = False
                                elif isinstance(v, dict) or isinstance(v, list):
                                    normalize_booleans(v)
                        elif isinstance(d, list):
                            for i, v in enumerate(d):
                                if isinstance(v, str):
                                    v_low = v.lower().strip()
                                    if v_low == "true":
                                        d[i] = True
                                    elif v_low == "false":
                                        d[i] = False
                                elif isinstance(v, dict) or isinstance(v, list):
                                    normalize_booleans(v)
                        return d
                        
                    args = normalize_booleans(args)
                    return args
                    
            raise ValueError(f"Ollama no utilizó la herramienta esperada {herramienta_schema['name']}")

        return self._retry(request)