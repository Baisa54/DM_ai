class EstadoJuego:

    def __init__(self):

        self.ubicacion = None
        self.jugador = None
        self.eventos = []
        self.decisiones = []
        self.personajes_presentes = []
        self.final = None

        self.estados_personajes = {

            "heroe": "normal",

            "companero": "normal",

            "goblin": "normal",

            "princesa": "normal",

            "osgo": "normal"
        }

    def set_ubicacion(self, ubicacion):

        self.ubicacion = ubicacion


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

            "jugador": self.jugador,

            "eventos": self.eventos,

            "decisiones": self.decisiones,

            "personajes_presentes": self.personajes_presentes,

            "estados_personajes": self.estados_personajes,

            "final": self.final
        }