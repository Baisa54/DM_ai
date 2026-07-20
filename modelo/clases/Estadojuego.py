#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# EstadoJuego
#
# EstadoJuego representa el estado global de la partida, incluyendo la ubicación
# actual, los eventos sucedidos, las decisiones del jugador, personajes presentes,
# el estado de salud de cada personaje, los objetos del héroe y si se ha alcanzado
# un final.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ EstadoJuego, clase que almacena la información del estado de la partida.
# @ ubicacion, cadena que representa la ubicación actual en el mapa.
# @ eventos, lista que almacena los eventos ocurridos.
# @ decisiones, lista que almacena las decisiones tomadas por el jugador.
# @ personajes_presentes, lista de los personajes que se encuentran en la escena actual.
# @ final, cadena que indica si se llegó a algún final de la partida.
# @ estados_personajes, diccionario con el estado de salud/vida de cada personaje.
# @ objetos_heroe, lista de los objetos en posesión del héroe.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ set_ubicacion, recibe la nueva ubicación
# @ agregar_evento, recibe un nuevo evento para añadir a la lista
# @ agregar_decision, recibe una nueva decisión para añadir a la lista
# @ agregar_personaje, recibe un personaje para añadir a personajes presentes
# @ quitar_personaje, recibe un personaje para remover de personajes presentes
# @ set_final, recibe el final alcanzado
# @ set_estado_personaje, recibe el personaje y su nuevo estado de vida
# @ get_estado_personaje, recibe el personaje
#   --> Devuelve el estado de vida del personaje solicitado
# @ to_dict
#   --> Devuelve la representación del estado en formato diccionario
# @ agregar_objeto_heroe, recibe el objeto a añadir al inventario
# @ quitar_objeto_heroe, recibe el objeto a quitar del inventario
# @ obtener_imagenes_escena
#   --> Devuelve una lista de los prompts visuales de los personajes presentes
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.game.characters import PERSONAJES
# PERSONAJES es el diccionario que contiene la configuración de los personajes
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class EstadoJuego:

    def __init__(self):

        self.ubicacion = None
        self.eventos = []
        self.decisiones = []
        self.personajes_presentes = []
        self.final = None
        self.estados_personajes = {

            "heroe": "",

            "companero": "",

            "goblin": "",

            "princesa": "",

            "osgo": ""
        }
        self.objetos_heroe = [
            "espada"
        ]

    def set_ubicacion(self, ubicacion):

        self.ubicacion = ubicacion
        
        from modelo.game.campaign import SALAS
        if ubicacion in SALAS:
            self.personajes_presentes = list(SALAS[ubicacion].get("personajes", []))

    def get_ubicacion(self):
        return self.ubicacion


    def agregar_evento(self, evento):

        self.eventos.append(evento)


    def agregar_decision(self, decision):

        self.decisiones.append(decision)


    def agregar_personaje(self, personaje):

        if personaje not in self.personajes_presentes:

            self.personajes_presentes.append(personaje)


    def quitar_personaje(self, personaje):

        if personaje in self.personajes_presentes:

            self.personajes_presentes.remove(personaje)


    def set_final(self, final):

        self.final = final

    def get_final(self):
        
        return self.final

    def set_estado_personaje(
        self,
        personaje,
        estado
    ):
        self.estados_personajes[personaje] = estado

    def get_estado_personaje(
        self,
        personaje
    ):
        return self.estados_personajes.get(personaje)

    def to_dict(self):

        return {
            "ubicacion": self.ubicacion,
            "eventos": self.eventos,
            "decisiones": self.decisiones,
            "personajes_presentes": self.personajes_presentes,
            "estados_personajes": self.estados_personajes,
            "objetos_heroe": self.objetos_heroe,
            "final": self.final
        }
    
    def agregar_objeto_heroe(
        self,
        objeto
    ):
        if objeto not in self.objetos_heroe:

            self.objetos_heroe.append(objeto)


    def quitar_objeto_heroe(
        self,
        objeto
    ):

        if objeto in self.objetos_heroe:

            self.objetos_heroe.remove(objeto)

    def obtener_imagenes_escena(self):

        imagenes = []

        imagenes.append(
            PERSONAJES["heroe"]["prompt_visual"]
        )

        for personaje in self.personajes_presentes:

            imagenes.append(
                PERSONAJES[personaje]["prompt_visual"]
            )

        return imagenes

    def obtener_rutas_imagenes_personajes(self):
        rutas = []
        if "imagen" in PERSONAJES["heroe"]:
            rutas.append(PERSONAJES["heroe"]["imagen"])
            
        for personaje in self.personajes_presentes:
            if "imagen" in PERSONAJES[personaje]:
                rutas.append(PERSONAJES[personaje]["imagen"])
                
        return rutas