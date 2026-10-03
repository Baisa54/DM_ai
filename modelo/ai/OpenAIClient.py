import json
import time
import requests
from modelo.configuracion import ConfigManager

class OpenAIClient:
    """
    Cliente para la API oficial de OpenAI (ChatGPT) optimizado para la presentación CACIC.
    Utiliza el modelo balanceado 'gpt-4o-mini' por defecto para minimizar latencia
    y consumo de tokens, garantizando soporte estricto de Tool Calling y JSON schema.
    """

    def __init__(self):
        """
        Inicializa el cliente de OpenAI obteniendo la API Key y modelo desde ConfigManager.
        """
        self.config = ConfigManager()
        self.api_key = self.config.get_openai_key()
        self.modelo = self.config.get_modelo_openai()
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def _call(self, payload, max_reintentos=3):
        """
        Ejecuta la llamada HTTP POST a la API de OpenAI con reintentos exponenciales.
        """
        if not self.api_key:
            raise ValueError(
                "No se encontró una API Key de OpenAI configurada.\n"
                "Por favor ingresa la clave en Menú > Configuración > Modo Pruebas (ChatGPT)."
            )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        ultimo_error = None
        for intento in range(max_reintentos):
            try:
                r = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=35
                )

                if r.status_code == 401:
                    raise ValueError(
                        "API Key de OpenAI rechazada (Error 401: Unauthorized).\n"
                        "Por favor revisa la clave del profesor ingresada en configuración."
                    )
                if r.status_code == 429:
                    raise ValueError(
                        "Límite de cuota o tasa de peticiones alcanzado en OpenAI (Error 429: Quota/Rate Limit).\n"
                        "Verifica que la cuenta de OpenAI tenga saldo activo."
                    )

                r.raise_for_status()
                return r.json()

            except (requests.Timeout, requests.ConnectionError) as e:
                ultimo_error = e
                print(f"[OpenAI Retry] Intento {intento + 1}/{max_reintentos} falló por red/timeout: {e}")
                time.sleep(1.0 * (intento + 1))
            except Exception as e:
                # Si es un error 401 o 429 ya formateado, no reintentamos
                if "401" in str(e) or "429" in str(e):
                    raise e
                ultimo_error = e
                print(f"[OpenAI Error] Intento {intento + 1}/{max_reintentos}: {e}")
                time.sleep(1.0 * (intento + 1))

        raise ultimo_error

    def generar_texto(self, prompt):
        """
        Genera una narración o diálogo fluido en texto plano usando el modelo configurado.
        """
        payload = {
            "model": self.modelo,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 1500
        }

        data = self._call(payload)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("OpenAI no devolvió respuestas (choices vacío).")

        return choices[0]["message"]["content"]

    def generar_con_herramienta(self, prompt, herramienta_schema):
        """
        Realiza una llamada con Tool Calling forzado para obtener respuestas estructuradas
        estrictas validadas por esquema JSON, normalizando booleanos.
        """
        nombre_herramienta = herramienta_schema["name"]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": nombre_herramienta,
                    "description": herramienta_schema.get("description", ""),
                    "parameters": herramienta_schema.get("parameters", {})
                }
            }
        ]

        payload = {
            "model": self.modelo,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.0,
            "tools": tools,
            "tool_choice": {
                "type": "function",
                "function": {"name": nombre_herramienta}
            }
        }

        data = self._call(payload)
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("OpenAI no devolvió opciones en la llamada de herramienta.")

        message = choices[0].get("message", {})
        tool_calls = message.get("tool_calls", [])

        if not tool_calls:
            raise ValueError(f"OpenAI no ejecutó la herramienta esperada: {nombre_herramienta}")

        args_raw = tool_calls[0]["function"].get("arguments", "{}")
        if isinstance(args_raw, str):
            try:
                args = json.loads(args_raw)
            except Exception:
                limpio = args_raw.strip()
                if limpio.startswith("```"):
                    limpio = limpio.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
                args = json.loads(limpio)
        else:
            args = dict(args_raw)

        # Normalización estricta de booleanos devueltos en formato string
        def normalizar_booleanos(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if isinstance(v, str):
                        v_low = v.lower().strip()
                        if v_low == "true":
                            d[k] = True
                        elif v_low == "false":
                            d[k] = False
                    elif isinstance(v, (dict, list)):
                        normalizar_booleanos(v)
            elif isinstance(d, list):
                for i, v in enumerate(d):
                    if isinstance(v, str):
                        v_low = v.lower().strip()
                        if v_low == "true":
                            d[i] = True
                        elif v_low == "false":
                            d[i] = False
                    elif isinstance(v, (dict, list)):
                        normalizar_booleanos(v)
            return d

        return normalizar_booleanos(args)

    def generar_json(self, prompt):
        """
        Genera una respuesta en formato JSON estructurado utilizando modo json_object nativo.
        """
        payload = {
            "model": self.modelo,
            "messages": [
                {"role": "system", "content": "Responde estrictamente con un objeto JSON válido y bien formado."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }

        data = self._call(payload)
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)

    def generar_imagen(self, prompt):
        """
        Delega la generación de imagen al cliente local/Hugging Face para no consumir
        créditos de DALL-E y mantener compatibilidad total con los assets de escena.
        """
        from modelo.ai.LocalAICLient import LocalAIClient
        return LocalAIClient().generar_imagen(prompt)

    @staticmethod
    def probar_conexion(api_key, modelo="gpt-4o-mini"):
        """
        Prueba la validez de la clave con un ping mínimo (1 token) para no incurrir en gastos.
        Retorna (exito: bool, mensaje: str, latencia_ms: int).
        """
        clave = api_key.strip() if api_key else ""
        if not clave:
            return False, "La API Key está vacía.", 0

        headers = {
            "Authorization": f"Bearer {clave}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": modelo,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 1
        }

        inicio = time.time()
        try:
            r = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=8
            )
            latencia = int((time.time() - inicio) * 1000)

            if r.status_code == 200:
                return True, f"Conexión exitosa ({latencia} ms)", latencia
            elif r.status_code == 401:
                return False, "Error 401: API Key incorrecta o no autorizada.", latencia
            elif r.status_code == 429:
                return False, "Error 429: Cuota insuficiente en la cuenta de OpenAI.", latencia
            else:
                return False, f"Error {r.status_code}: {r.text[:80]}", latencia

        except requests.Timeout:
            return False, "Tiempo de espera agotado (>8s). Verifica tu conexión.", 0
        except Exception as e:
            return False, f"Fallo de conexión: {str(e)[:60]}", 0
