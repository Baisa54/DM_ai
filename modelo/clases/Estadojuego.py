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
    """
    Almacena y gestiona el estado dinámico global de la partida (ubicación, inventario, personajes presentes y estado de salud).
    """

    def __init__(self):
        """
        Inicializa un nuevo EstadoJuego con valores predeterminados.
        """
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
        """
        Establece la ubicación actual del héroe y actualiza automáticamente los personajes presentes en dicha sala.
        """
        self.ubicacion = ubicacion
        
        from modelo.game.campaign import SALAS
        if ubicacion in SALAS:
            self.personajes_presentes = list(SALAS[ubicacion].get("personajes", []))

    def get_ubicacion(self):
        """
        Obtiene la clave de la ubicación actual del juego.
        """
        return self.ubicacion

    def agregar_evento(self, evento):
        """
        Agrega un evento reciente al historial de la partida (máximo 5).
        """
        self.eventos.append(evento)
        if len(self.eventos) > 5:
            self.eventos.pop(0)

    def agregar_decision(self, decision):
        """
        Agrega una decisión del jugador al historial reciente (máximo 5).
        """
        self.decisiones.append(decision)
        if len(self.decisiones) > 5:
            self.decisiones.pop(0)

    def agregar_personaje(self, personaje):
        """
        Añade un personaje a la lista de personajes presentes en la sala actual.
        """
        if personaje not in self.personajes_presentes:
            self.personajes_presentes.append(personaje)

    def quitar_personaje(self, personaje):
        """
        Remueve un personaje de la sala actual si está presente.
        """
        if personaje in self.personajes_presentes:
            self.personajes_presentes.remove(personaje)

    def set_final(self, final):
        """
        Establece la clave del final alcanzado en la partida (o None si continúa).
        """
        self.final = final

    def get_final(self):
        """
        Obtiene el estado de final de juego si ha sido alcanzado.
        """
        return self.final

    def set_estado_personaje(self, personaje, estado):
        """
        Actualiza el estado de salud/condición de un personaje específico ('normal', 'herido', 'muerto', etc.).
        """
        self.estados_personajes[personaje] = estado

    def get_estado_personaje(self, personaje):
        """
        Obtiene el estado de condición actual de un personaje específico.
        """
        return self.estados_personajes.get(personaje)

    def to_dict(self):
        """
        Serializa el estado del juego a un diccionario estructurado.
        """
        return {
            "ubicacion": self.ubicacion,
            "eventos": self.eventos,
            "decisiones": self.decisiones,
            "personajes_presentes": self.personajes_presentes,
            "estados_personajes": self.estados_personajes,
            "objetos_heroe": self.objetos_heroe,
            "final": self.final
        }
    
    def agregar_objeto_heroe(self, objeto):
        """
        Añade un nuevo ítem al inventario del héroe si no lo posee previamente.
        """
        if objeto not in self.objetos_heroe:
            self.objetos_heroe.append(objeto)

    def quitar_objeto_heroe(self, objeto):
        """
        Remueve un ítem del inventario del héroe.
        """
        if objeto in self.objetos_heroe:
            self.objetos_heroe.remove(objeto)

    def obtener_imagenes_escena(self):
        """
        Genera la lista de descripciones de personajes y sus estados visuales para la IA de generación de imágenes.
        """
        from modelo.game.characters import PERSONAJES
        imagenes = []

        # Agregar heroe
        estado_heroe = self.estados_personajes.get("heroe", "normal")
        imagenes.append(
            f"Character: heroe, Status: {estado_heroe}, Description: {PERSONAJES['heroe']['prompt_visual']}"
        )

        for personaje in self.personajes_presentes:
            estado_personaje = self.estados_personajes.get(personaje, "normal")
            imagenes.append(
                f"Character: {personaje}, Status: {estado_personaje}, Description: {PERSONAJES[personaje]['prompt_visual']}"
            )

        return imagenes

    def obtener_rutas_imagenes_personajes(self):
        """
        Obtiene la lista de rutas a las imágenes de referencia del héroe y personajes presentes en la sala.
        """
        from modelo.game.characters import PERSONAJES
        rutas = []
        if "imagen" in PERSONAJES["heroe"]:
            rutas.append(PERSONAJES["heroe"]["imagen"])
            
        for personaje in self.personajes_presentes:
            if "imagen" in PERSONAJES[personaje]:
                rutas.append(PERSONAJES[personaje]["imagen"])
                
        return rutas