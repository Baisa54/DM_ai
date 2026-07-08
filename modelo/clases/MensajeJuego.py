#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# MensajeJuego
#
# MensajeJuego es la clase encargada de construir y estructurar el mensaje final
# de la partida que se enviará a la vista para ser mostrado al jugador, combinando
# la narración del DM, la imagen de la escena, el diálogo del NPC y su imagen.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ MensajeJuego, clase que contiene la estructura del mensaje para la vista.
# @ narracion, cadena que almacena la narración principal de la escena.
# @ imagen_resumen, ruta o recurso de la imagen resumen de la escena.
# @ narracion_npc, cadena que almacena las líneas de diálogo habladas por un NPC.
# @ imagen_npc, ruta o recurso del retrato del NPC que está hablando.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ hay_dialogo_npc
#   --> Devuelve un booleano indicando si hay un diálogo de NPC cargado
# @ obtener_seccion_obligatoria
#   --> Devuelve un diccionario con la narración y la imagen resumen
# @ obtener_mensaje_completo
#   --> Devuelve un diccionario con toda la información cargada para el mensaje
# @ set_narracion, recibe la narración principal de la escena
# @ set_imagen_resumen, recibe el recurso de la imagen resumen
# @ set_narracion_npc, recibe el diálogo del NPC
# @ set_imagen_npc, recibe la imagen/retrato del NPC
# @ get_narracion
#   --> Devuelve la narración principal
# @ get_imagen_resumen
#   --> Devuelve la imagen resumen
# @ get_narracion_npc
#   --> Devuelve la narración/diálogo del NPC
# @ get_imagen_npc
#   --> Devuelve la imagen del NPC
# @ set_dialogo_npc, recibe la narración y la imagen del NPC para cargarlas en conjunto
# @ limpiar_dialogo_npc, vacía la narración y la imagen del NPC (estableciéndolos en None)
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# (No contiene imports externos)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class MensajeJuego:

    def __init__(self):

        self.narracion = ""
        self.imagen_resumen = None
        self.narracion_npc = None
        self.imagen_npc = None

    def hay_dialogo_npc(self):

        return (
            self.narracion_npc is not None
            and self.narracion_npc != ""
        )

    def obtener_seccion_obligatoria(self):

        return {
            "narracion": self.narracion,
            "imagen_resumen": self.imagen_resumen
        }

    def obtener_mensaje_completo(self):

        mensaje = self.obtener_seccion_obligatoria()

        if self.hay_dialogo_npc():

            mensaje["narracion_npc"] = self.narracion_npc
            mensaje["imagen_npc"] = self.imagen_npc

        return mensaje
    
    # ==========================
    # SETTERS
    # ==========================

    def set_narracion(self, narracion):

        self.narracion = narracion


    def set_imagen_resumen(self, imagen_resumen):

        self.imagen_resumen = imagen_resumen


    def set_narracion_npc(self, narracion_npc):

        self.narracion_npc = narracion_npc


    def set_imagen_npc(self, imagen_npc):

        self.imagen_npc = imagen_npc

    # ==========================
    # GETTERS
    # ==========================

    def get_narracion(self):
        return self.narracion

    def get_imagen_resumen(self):
        return self.imagen_resumen

    def get_narracion_npc(self):
        return self.narracion_npc

    def get_imagen_npc(self):
        return self.imagen_npc

    def set_dialogo_npc(
        self,
        narracion_npc,
        imagen_npc
    ):

        self.narracion_npc = narracion_npc
        self.imagen_npc = imagen_npc


    def limpiar_dialogo_npc(self):

        self.narracion_npc = None
        self.imagen_npc = None

    