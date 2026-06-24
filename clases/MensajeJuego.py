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