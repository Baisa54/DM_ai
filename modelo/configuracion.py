import json
import os

class ConfigManager:
    """
    Singleton que maneja la configuración global del juego.
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
        Inicializa la configuración por defecto y carga los datos almacenados en config.json.
        """
        self.archivo_config = "config.json"
        self.config = {
            "gemini_api_key": "",
            "huggingface_api_key": "",
            "volumen": 0.20,
            "proveedor_imagen": "huggingface",
            "proveedor_texto": "gemini",
            "modelo_local": "llama3.1"
        }
        self.cargar_config()

    def cargar_config(self):
        """
        Carga la configuración desde el archivo JSON si existe en el disco.
        """
        if os.path.exists(self.archivo_config):
            try:
                with open(self.archivo_config, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    # Actualizar valores existentes
                    for clave in self.config.keys():
                        if clave in datos:
                            self.config[clave] = datos[clave]
            except Exception as e:
                print(f"Error al cargar configuración: {e}")
        else:
            self.guardar_config()

    def guardar_config(self):
        """
        Guarda el estado actual de la configuración en el archivo config.json.
        """
        try:
            with open(self.archivo_config, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def get_gemini_key(self):
        """
        Obtiene la API Key de Gemini configurada.
        """
        return self.config.get("gemini_api_key", "")

    def set_gemini_key(self, key):
        """
        Establece la API Key de Gemini.
        """
        self.config["gemini_api_key"] = key

    def get_huggingface_key(self):
        """
        Obtiene la API Key de Hugging Face configurada.
        """
        return self.config.get("huggingface_api_key", "")

    def set_huggingface_key(self, key):
        """
        Establece la API Key de Hugging Face.
        """
        self.config["huggingface_api_key"] = key

    def get_volumen(self):
        """
        Obtiene el volumen global del audio (0.0 a 1.0).
        """
        return self.config.get("volumen", 0.20)

    def set_volumen(self, vol):
        """
        Establece el volumen global del audio limitándolo al rango de 0.0 a 1.0.
        """
        self.config["volumen"] = max(0.0, min(1.0, vol))

    def get_proveedor_imagen(self):
        """
        Obtiene el proveedor actual de generación de imágenes ('huggingface' o 'gemini').
        """
        return self.config.get("proveedor_imagen", "huggingface")

    def set_proveedor_imagen(self, proveedor):
        """
        Establece el proveedor de generación de imágenes ('huggingface' o 'gemini').
        """
        if proveedor in ["huggingface", "gemini"]:
            self.config["proveedor_imagen"] = proveedor

    def get_proveedor_texto(self):
        """
        Obtiene el proveedor actual de generación de texto ('gemini' u 'ollama').
        """
        return self.config.get("proveedor_texto", "gemini")

    def set_proveedor_texto(self, proveedor):
        """
        Establece el proveedor de generación de texto ('gemini' u 'ollama').
        """
        if proveedor in ["gemini", "ollama"]:
            self.config["proveedor_texto"] = proveedor

    def get_modelo_local(self):
        """
        Obtiene el modelo local de Ollama seleccionado.
        """
        return self.config.get("modelo_local", "llama3.1")

    def set_modelo_local(self, modelo):
        """
        Establece el modelo local de Ollama a utilizar.
        """
        self.config["modelo_local"] = modelo

