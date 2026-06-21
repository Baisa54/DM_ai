class EstadoJuego:

    def __init__(self):

        self.ubicacion = None
        self.eventos = []
        self.decisiones = []
        self.personajes_presentes = []
        self.final = None
        self.estados_personajes = {

            "Heroe": "",

            "Companero": "",

            "Goblin": "",

            "Princesa": "",

            "Osgo": ""
        }
        self.objetos_heroe = [
            ""
        ]

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

            "eventos": self.eventos,

            "decisiones": self.decisiones,

            "personajes_presentes": self.personajes_presentes,

            "estados_personajes": self.estados_personajes,

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