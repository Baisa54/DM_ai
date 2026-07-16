import json
import os

class ConfigManager:
    """
    Singleton que maneja la configuración global del juego.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfigManager, cls).__new__(cls)
            cls._instancia._inicializar()
        return cls._instancia

    def _inicializar(self):
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
        try:
            with open(self.archivo_config, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error al guardar configuración: {e}")

    def get_gemini_key(self):
        return self.config.get("gemini_api_key", "")

    def set_gemini_key(self, key):
        self.config["gemini_api_key"] = key

    def get_huggingface_key(self):
        return self.config.get("huggingface_api_key", "")

    def set_huggingface_key(self, key):
        self.config["huggingface_api_key"] = key

    def get_volumen(self):
        return self.config.get("volumen", 0.20)

    def set_volumen(self, vol):
        self.config["volumen"] = max(0.0, min(1.0, vol))

    def get_proveedor_imagen(self):
        return self.config.get("proveedor_imagen", "huggingface")

    def set_proveedor_imagen(self, proveedor):
        if proveedor in ["huggingface", "gemini"]:
            self.config["proveedor_imagen"] = proveedor

    def get_proveedor_texto(self):
        return self.config.get("proveedor_texto", "gemini")

    def set_proveedor_texto(self, proveedor):
        if proveedor in ["gemini", "ollama"]:
            self.config["proveedor_texto"] = proveedor

    def get_modelo_local(self):
        return self.config.get("modelo_local", "llama3.1")

    def set_modelo_local(self, modelo):
        self.config["modelo_local"] = modelo
