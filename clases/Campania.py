# Campania.py

from ContextoJuego import ContextoJuego
from Estadojuego import EstadoJuego
from MensajeJuego import MensajeJuego

from gen_state import gen_state
from gen_messege import genMessage

class Campania:

    def __init__(self):

        self.contexto = ContextoJuego()

        self.estado = gen_state()

        self.mensaje = genMessage()

    def reiniciar(self):

        self.contexto = ContextoJuego()

        self.estado = gen_state()

        self.mensaje = genMessage()

    def get_contexto(self):

        return self.contexto

    def get_estado(self):

        return self.estado

    def get_mensaje(self):

        return self.mensaje

    def set_contexto(
        self,
        contexto
    ):

        self.contexto = contexto

    def set_estado(
        self,
        estado
    ):

        self.estado = estado

    def set_mensaje(
        self,
        mensaje
    ):

        self.mensaje = mensaje

# ToDo hay que realizar Campania para que pueda correr todo 