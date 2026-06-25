import json
from huggingface_hub import InferenceClient
import requests
import time
import random
from PIL import Image
from io import BytesIO
import re
import traceback
import socket
import requests



class LocalAIClient:

    def __init__(self):

        # Ollama local
        self.ollama_url = "http://localhost:11434/api/generate"

        self.hf_client = InferenceClient(
            api_key=""
        )

    # --------------------------------------------------
    # RETRY SIMPLE (ahora version maquina de guerra ultra debugger jajajaj)
    # --------------------------------------------------
    def _retry(self, func, max_reintentos=3):

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
                    socket.gethostbyname("localhost")
                    print("✔ localhost resolvible")
                except:
                    print("❌ problema DNS localhost")

                # 2. OLLAMA
                try:
                    import requests
                    r = requests.get("http://localhost:11434", timeout=3)
                    print(f"✔ Ollama responde HTTP {r.status_code}")
                except Exception as ollama_err:
                    print(f"❌ Ollama no responde: {repr(ollama_err)}")

                # 3. HF CLIENT EXISTE
                try:
                    if hasattr(self, "hf_client"):
                        print("✔ hf_client inicializado")
                    else:
                        print("❌ hf_client NO existe")
                except:
                    print("❌ error verificando hf_client")

                # 4. ERROR CLASIFICADO
                err_str = str(e).lower()

                print("\n[PROBABLE CAUSA]")

                if "connection refused" in err_str:
                    print("❌ servicio apagado o puerto incorrecto")

                elif "timeout" in err_str:
                    print("❌ timeout (modelo lento o bloqueado)")

                elif "404" in err_str:
                    print("❌ modelo no encontrado (Ollama/HF)")

                elif "json" in err_str:
                    print("❌ error de parsing JSON del modelo")

                elif "getaddrinfo" in err_str:
                    print("❌ problema DNS / internet")

                else:
                    print("⚠ causa desconocida")

                # 🔁 RETRY INFO
                espera = 2 ** i
                print(f"\n[RETRY] intento {i+1}/{max_reintentos}")
                print(f"[WAIT] {espera:.2f}s\n")

                import time, random
                time.sleep(espera)

        raise Exception(
            f"\n❌ LOCAL AI FALLÓ DEFINITIVAMENTE\n"
            f"Último error: {repr(last_error)}"
        )

    # --------------------------------------------------
    # TEXTO (OLLAMA)
    # --------------------------------------------------
    def generar_texto(self, prompt, model="qwen2.5:7b-instruct"):

        def request():

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
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
    def generar_json(self, prompt, model="qwen2.5:7b-instruct"):

        def extract_json(text):

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

            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,

                "format": "json"
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

        def request():

            imagen = self.hf_client.text_to_image(
                prompt,
                model="stabilityai/stable-diffusion-xl-base-1.0"
            )

            return imagen

        try:
            return self._retry(request)

        except Exception as e:

            print("\n" + "="*80)
            print("NO SE PUDO GENERAR IMAGEN")
            print("="*80)
            print(str(e))

            return None