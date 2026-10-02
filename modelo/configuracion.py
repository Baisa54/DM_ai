import json
import os

class ConfigManager:
    """
    Singleton que maneja la configuración global del juego y el almacenamiento
    aislado y seguro de credenciales secretas (para evitar filtraciones en Git).
    """
    _instancia = None

    def __new__(cls):
        """
        Garantiza que exista una única instancia de ConfigManager en todo el sistema.
        """
        if cls._instancia is None:
            cls._instancia = super(ConfigManager, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
        """
        Inicializa la configuración por defecto y carga los datos almacenados en config.json
        y los secretos aislados en .secrets.json.
        """
        self.archivo_config = "config.json"
        self.archivo_secretos = ".secrets.json"

        self.config = {
            "gemini_api_key": "",
            "huggingface_api_key": "",
            "volumen": 0.20,
            "proveedor_imagen": "huggingface",
            "generar_imagenes": True,
            "proveedor_texto": "ollama",
            "modelo_local": "llama3.1",
            "modelo_openai": "gpt-4o-mini"
        }

        # Almacén de claves privadas aisladas de Git
        self.secretos = {
            "openai_api_key": ""
        }

        self.cargar_config()
        self.cargar_secretos()

    def cargar_config(self):
        """
        Carga la configuración desde el archivo JSON si existe en el disco.
        """
        if os.path.exists(self.archivo_config):
            try:
                with open(self.archivo_config, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    for clave in self.config.keys():
                        if clave in datos:
                            self.config[clave] = datos[clave]
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
        else:
            self.guardar_config()

    def guardar_config(self):
        """
        Guarda el estado actual de la configuración general en config.json.
        (NUNCA guarda la OpenAI API Key aquí para evitar commits accidentales).
        """
        try:
            with open(self.archivo_config, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def cargar_secretos(self):
        """
        Carga las credenciales secretas desde el archivo .secrets.json (ignorado por Git).
        """
        if os.path.exists(self.archivo_secretos):
            try:
                with open(self.archivo_secretos, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    for k in self.secretos.keys():
                        if k in datos:
                            self.secretos[k] = datos[k]
            except Exception as e:
                print(f"Error al cargar secretos: {e}")

    def guardar_secretos(self):
        """
        Guarda de forma aislada y privada las credenciales sensibles en .secrets.json.
        """
        try:
            with open(self.archivo_secretos, "w", encoding="utf-8") as f:
                json.dump(self.secretos, f, indent=4)
        except Exception as e:
            print(f"Error al guardar secretos: {e}")

    # ----------------------------------------------------
    # Credenciales Gemini & Hugging Face
    # ----------------------------------------------------
    def get_gemini_key(self):
        """Obtiene la API Key de Gemini configurada."""
        return self.config.get("gemini_api_key", "")

    def set_gemini_key(self, key):
        """Establece la API Key de Gemini."""
        self.config["gemini_api_key"] = key

    def get_huggingface_key(self):
        """Obtiene la API Key de Hugging Face configurada."""
        return self.config.get("huggingface_api_key", "")

    def set_huggingface_key(self, key):
        """Establece la API Key de Hugging Face."""
        self.config["huggingface_api_key"] = key

    # ----------------------------------------------------
    # Credenciales Seguras OpenAI / ChatGPT (Aislamiento Total)
    # ----------------------------------------------------
    def get_openai_key(self):
        """
        Obtiene la clave de OpenAI priorizando:
        1. Variable de entorno del sistema (OPENAI_API_KEY).
        2. Archivo secreto local (.secrets.json) excluido de Git.
        """
        env_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if env_key:
            return env_key
        return self.secretos.get("openai_api_key", "").strip()

    def set_openai_key(self, key):
        """
        Almacena la clave de OpenAI exclusivamente en el archivo protegido .secrets.json.
        """
        self.secretos["openai_api_key"] = key.strip()
        self.guardar_secretos()

    def get_modelo_openai(self):
        """
        Obtiene el modelo de OpenAI configurado (por defecto 'gpt-4o-mini' por su
        óptimo equilibrio entre consumo mínimo de tokens y alta precisión).
        """
        return self.config.get("modelo_openai", "gpt-4o-mini")

    def set_modelo_openai(self, modelo):
        """Establece el modelo de OpenAI a utilizar ('gpt-4o-mini' o 'gpt-4o')."""
        if modelo in ["gpt-4o-mini", "gpt-4o"]:
            self.config["modelo_openai"] = modelo

    # ----------------------------------------------------
    # Control de Audio
    # ----------------------------------------------------
    def get_volumen(self):
        """Obtiene el volumen global del audio (0.0 a 1.0)."""
        return self.config.get("volumen", 0.20)

    def set_volumen(self, vol):
        """Establece el volumen global del audio limitándolo al rango de 0.0 a 1.0."""
        self.config["volumen"] = max(0.0, min(1.0, vol))

    # ----------------------------------------------------
    # Proveedores de Imagen y Texto
    # ----------------------------------------------------
    def get_proveedor_imagen(self):
        """Obtiene el proveedor actual de generación de imágenes ('huggingface' o 'gemini')."""
        return self.config.get("proveedor_imagen", "huggingface")

    def set_proveedor_imagen(self, proveedor):
        """Establece el proveedor de generación de imágenes ('huggingface' o 'gemini')."""
        if proveedor in ["huggingface", "gemini"]:
            self.config["proveedor_imagen"] = proveedor

    def get_generar_imagenes(self):
        """Obtiene si la síntesis visual de escenas e imágenes está activada (True) o desactivada (False)."""
        return self.config.get("generar_imagenes", True)

    def set_generar_imagenes(self, habilitado: bool):
        """Habilita o deshabilita la generación visual de imágenes para máxima velocidad de respuesta."""
        self.config["generar_imagenes"] = bool(habilitado)

    def get_proveedor_texto(self):
        """Obtiene el proveedor actual de generación de texto ('ollama', 'openai' o 'gemini')."""
        return self.config.get("proveedor_texto", "ollama")

    def set_proveedor_texto(self, proveedor):
        """Establece el proveedor de generación de texto ('ollama', 'openai' o 'gemini')."""
        if proveedor in ["ollama", "openai", "chatgpt", "gemini"]:
            if proveedor == "chatgpt":
                proveedor = "openai"
            self.config["proveedor_texto"] = proveedor

    def get_modelo_local(self):
        """Obtiene el modelo local de Ollama seleccionado."""
        return self.config.get("modelo_local", "llama3.1")

    def set_modelo_local(self, modelo):
        """Establece el modelo local de Ollama a utilizar."""
        self.config["modelo_local"] = modelo
