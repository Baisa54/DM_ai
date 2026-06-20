class ContextoJuego:

    def __init__(self):

        self.prompt_jugador = ""

        self.accion_valida = True

        self.requiere_tirada = False

        self.dificultad = 0

        self.estado = None

        self.resultado_d20 = None

    def set_prompt_jugador(self, prompt):

        self.prompt_jugador = prompt


    def set_accion_valida(self, accion_valida):

        self.accion_valida = accion_valida


    def set_requiere_tirada(self, requiere_tirada):

        self.requiere_tirada = requiere_tirada


    def set_dificultad(self, dificultad):

        self.dificultad = dificultad


    def set_estado(self, estado):

        self.estado = estado


    def set_resultado_d20(self, resultado):

        self.resultado_d20 = resultado

    def mostrar(self):

        return {
            "prompt_jugador": self.prompt_jugador,
            "accion_valida": self.accion_valida,
            "requiere_tirada": self.requiere_tirada,
            "dificultad": self.dificultad,
            "estado": self.estado,
            "resultado_d20": self.resultado_d20
        }