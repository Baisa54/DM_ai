import subprocess
import threading
import json
import ctypes
import os

class OllamaManager:
    """
    Gestor de modelos locales de Ollama.
    Verifica RAM, lista modelos instalados y descarga modelos en background.
    """
    
    # Modelos recomendados y sus requisitos de RAM en GB
    MODELOS_DISPONIBLES = [
        {"id": "llama3.1", "nombre": "Llama 3.1 (8B)", "ram_req": 8, "desc": "Modelo estándar, equilibrado con soporte Tools."},
        {"id": "qwen2.5:0.5b", "nombre": "Qwen 2.5 (0.5B)", "ram_req": 4, "desc": "Muy ligero y rápido, ideal PCs básicos."},
        {"id": "qwen2.5:32b", "nombre": "Qwen 2.5 (32B)", "ram_req": 32, "desc": "Pesado. Excelente razonamiento lógico."},
        {"id": "qwen2.5:72b", "nombre": "Qwen 2.5 (72B)", "ram_req": 64, "desc": "Ultra pesado. Rendimiento nivel GPT-4."}
    ]

    def __init__(self):
        self.descarga_activa = False
        self.progreso_actual = 0.0
        self.estado_descarga = ""
        self._thread = None
        self.error_descarga = ""
        self.servidor_ollama_activo = False

    def obtener_ram_gb(self):
        """Devuelve la RAM total del sistema en GB."""
        try:
            if os.name == 'nt':
                # Windows
                class MemoryStatusEx(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", ctypes.c_ulong),
                        ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]
                stat = MemoryStatusEx()
                stat.dwLength = ctypes.sizeof(MemoryStatusEx)
                ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
                return stat.ullTotalPhys / (1024**3)
            else:
                # Linux / macOS (Aproximación simplificada)
                with open('/proc/meminfo', 'r') as mem:
                    for line in mem:
                        if 'MemTotal' in line:
                            return int(line.split()[1]) / (1024**2)
        except Exception:
            return 8.0 # Fallback 8GB
        return 8.0

    def obtener_modelos_instalados(self):
        """Ejecuta ollama list y devuelve una lista de strings con los nombres de modelos."""
        instalados = []
        try:
            # ollama list output format: NAME    ID    SIZE    MODIFIED
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                self.servidor_ollama_activo = False
                return []
                
            self.servidor_ollama_activo = True
            lineas = result.stdout.strip().split("\n")
            for linea in lineas[1:]: # Skip header
                partes = linea.split()
                if partes:
                    nombre = partes[0]
                    if ":" not in nombre:
                        nombre += ":latest" # Normalizar
                    instalados.append(nombre)
        except Exception:
            self.servidor_ollama_activo = False
        return instalados

    def _pull_worker(self, modelo_id):
        self.descarga_activa = True
        self.progreso_actual = 0.0
        self.estado_descarga = f"Iniciando descarga de {modelo_id}..."
        self.error_descarga = ""

        try:
            # Ejecutamos ollama pull y leemos el output progresivamente
            process = subprocess.Popen(
                ["ollama", "pull", modelo_id],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1 # Line buffered
            )

            for line in process.stdout:
                line = line.strip()
                # Salida típica de ollama pull:
                # pulling manifest
                # pulling 8a83421c6eb3... 10% ▕████      ▏  100 MB / 1.0 GB
                
                self.estado_descarga = line
                
                # Intentar parsear el porcentaje
                import re
                match = re.search(r'(\d+)%', line)
                if match:
                    self.progreso_actual = float(match.group(1))

            process.wait()
            
            if process.returncode == 0:
                self.estado_descarga = "Descarga completada."
                self.progreso_actual = 100.0
            else:
                self.error_descarga = f"Fallo al descargar. Código: {process.returncode}"
                
        except Exception as e:
            self.error_descarga = str(e)
            
        finally:
            self.descarga_activa = False

    def iniciar_descarga(self, modelo_id):
        """Inicia la descarga de un modelo en un hilo separado."""
        if self.descarga_activa:
            return False
            
        self._thread = threading.Thread(target=self._pull_worker, args=(modelo_id,), daemon=True)
        self._thread.start()
        return True
