#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# main
#
# main es el punto de entrada principal del proyecto.
# Detecta el sistema operativo y lanza la vista gráfica basada en Pygame (VistaGrafica)
# de forma totalmente compatible con Windows, Linux y macOS.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ main, función de arranque principal del juego.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import sys
# sys se utiliza para añadir directorios al path de búsqueda en caso necesario
from Vista.vista_grafica import VistaGrafica
# VistaGrafica es el orquestador de la UI Pygame
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

    print(f"Iniciando DM AI en sistema operativo: {sys.platform}")

    # -------------------------------------------------------------
    # VERIFICACION DE MODELOS (LOCAL / NUBE)
    # -------------------------------------------------------------
    try:
        from modelo.configuracion import ConfigManager
        cfg = ConfigManager()
        prov_actual = cfg.get_proveedor_texto()

        if prov_actual in ("openai", "chatgpt"):
            print("\n" + "="*80)
            print(">>> MODO EXPOSICIÓN ACTIVO: ChatGPT Cloud (OpenAI gpt-4o-mini) <<<")
            print("Inferencia en la nube de alta velocidad activada para demostración.")
            print("="*80 + "\n")
        else:
            from modelo.ai.ollama_manager import OllamaManager
            import time
            
            gestor = OllamaManager()
            modelos_descargados = gestor.obtener_modelos_instalados()
            
            # Validar si ollama esta instalado y corriendo
            if gestor.servidor_ollama_activo:
                algun_modelo_instalado = False
                for mod_disp in OllamaManager.MODELOS_DISPONIBLES:
                    # Comprobar si mod_disp["id"] está en los instalados
                    if any(m.startswith(mod_disp["id"]) for m in modelos_descargados):
                        algun_modelo_instalado = True
                        break
                        
                if not algun_modelo_instalado:
                    print("\n" + "="*80)
                    print("¡ATENCION! No hay modelos IA locales descargados.")
                    print("Por favor revisar en configuracion y descargar uno para poder jugar offline.")
                    print("="*80 + "\n")
                    time.sleep(3)
            else:
                print("\n" + "="*80)
                print("¡ATENCION! Ollama no está activo o no está instalado.")
                print("No se podrán usar modelos locales (offline).")
                print("="*80 + "\n")
                time.sleep(3)
    except Exception as e:
        print(f"Error al verificar modelos locales: {e}")
    # -------------------------------------------------------------
    # LIMPIEZA DE CARPETA TEMPORAL DE IMÁGENES
    # -------------------------------------------------------------
    import os
    import glob
    try:
        temp_dir = "modelo/game/assets/temp"
        if os.path.exists(temp_dir):
            print(f"Limpiando imágenes temporales antiguas en {temp_dir}...")
            archivos = glob.glob(os.path.join(temp_dir, "*"))
            for archivo in archivos:
                if os.path.isfile(archivo):
                    os.remove(archivo)
    except Exception as e:
        print(f"Error al limpiar la carpeta temporal: {e}")
    # -------------------------------------------------------------

    app = VistaGrafica()
    app.iniciar()
