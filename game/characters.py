#------------------------------------------------------------------------------------------------------
# Personajes
#
# La idea es describir como son los personajes
#------------------------------------------------------------------------------------------------------

PERSONAJES = {

    "Heroe": {
            "nombre": "Heroe",

            "raza": "Humano",

            "descripcion":
                "Guerrero humano aventurero equipado con una espada común. "
                "Ha aceptado la misión de rescatar a la princesa secuestrada "
                "por los goblins para obtener una gran recompensa.",

            "imagen_base":
                "assets/personajes/heroe.png"
        },

    "companero": {

        "nombre": "Aelar",

        "raza": "Elfo",

        "descripcion":
            "Arquero elfo de gran puntería y amigo leal del héroe."
            "Leal, valiente y dispuesto a sacrificarse por sus amigos.",

        "imagen_base":
            "assets/personajes/aelar.png"
    },

    "Goblin": {

        "nombre": "Goblin",

        "raza": "Goblin",

        "descripcion":
            "Pequeña criatura verde de inteligencia limitada."
            "Ingenuo, fácil de manipular y con hambre constante."
            "malvado, no le agradan los humanos ni los elfos",

        "imagen_base":
            "assets/personajes/goblin.png"
    },

    "Princesa": {

        "nombre": "Princesa",

        "raza": "Humana",

        "descripcion":
            "Princesa del reino secuestrada por Osgo."
            "Inteligente, ambiciosa y decidida a sobrevivir.",

        "imagen_base":
            "assets/personajes/princesa.png"
    },

    "Osgo": {

        "nombre": "Osgo",

        "raza": "Orco",

        "descripcion":
            "Líder de los goblins y guerrero temible."
            "Orgulloso, agresivo y convencido de su destino."
            "posee un martillo de guerra y una jabalina",

        "imagen_base":
            "assets/personajes/osgo.png"
    },

}

def obtener_personaje(nombre):
    return PERSONAJES.get(nombre)