from game.campaign import obtener_sala


class GameEngine:

    def __init__(self, estado):
        self.estado = estado

    def obtener_contexto(self):

        sala = obtener_sala(
            self.estado["ubicacion"]
        )

        return {
            "estado": self.estado,
            "sala": sala
        }