#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# ContextoJuego
#
# ContextoJuego se encarga de almacenar y gestionar el contexto de una acción del
# jugador en la partida (por ejemplo, el prompt del jugador, la dificultad de la
# tirada, el resultado del dado d20, etc.).
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ ContextoJuego, clase que encapsula el contexto transitorio de la acción actual.
# @ prompt_jugador, cadena de texto con la acción ingresada por el jugador.
# @ accion_valida, booleano que indica si la acción del jugador es válida.
# @ requiere_tirada, booleano que indica si la acción requiere tirar dados.
# @ dificultad, entero con la dificultad de la tirada requerida.
# @ estado, objeto EstadoJuego con el estado actual de la partida.
# @ resultado_d20, cadena o None que representa el resultado de la tirada.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ set_prompt_jugador, recibe el prompt de la acción del jugador
# @ set_accion_valida, recibe la validez de la acción (bool)
# @ set_requiere_tirada, recibe si requiere tirada (bool)
# @ set_dificultad, recibe la dificultad (int)
# @ set_estado, recibe el estado de la partida
# @ set_resultado_d20, recibe el resultado de la tirada
# @ set_exito, establece el resultado en "exito"
# @ get_prompt_jugador
#   --> Devuelve el prompt del jugador
# @ get_accion_valida
#   --> Devuelve si la accion es valida o no
# @ get_requiere_tirada
#   --> Devuelve si la accion requiere tirada o no
# @ get_dificultad
#   --> Devuelve la dificultad
# @ get_estado
#   --> Devuelve el estado de la partida
# @ get_resultado_d20
#   --> Devuelve el resultado del dado d20
# @ mostrar
#   --> Devuelve un diccionario con los datos del contexto
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# (No contiene imports externos)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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

    def get_prompt_jugador(self):
        return self.prompt_jugador

    def get_accion_valida(self):
        return self.accion_valida

    def get_requiere_tirada(self):
        return self.requiere_tirada

    def get_dificultad(self):
        return self.dificultad

    def get_estado(self):
        return self.estado

    def get_resultado_d20(self):
        return self.resultado_d20
    
    def set_exito(self):

        self.resultado_d20 = "exito"

    def mostrar(self):

        return {
            "prompt_jugador": self.prompt_jugador,
            "accion_valida": self.accion_valida,
            "requiere_tirada": self.requiere_tirada,
            "dificultad": self.dificultad,
            "estado": self.estado,
            "resultado_d20": self.resultado_d20
        }