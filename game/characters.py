PERSONAJES = {

    "Heroe": {
            "nombre": "Heroe",

            "raza": "Humano",

            "rol": "protagonista",

            "descripcion":
                "Guerrero humano aventurero equipado con una espada común. "
                "Ha aceptado la misión de rescatar a la princesa secuestrada "
                "por los goblins para obtener una gran recompensa.",

            "personalidad":
                "Valiente, decidido y dispuesto a asumir riesgos para cumplir su misión.",

            "habilidades": [
                "esgrima",
                "combate_cuerpo_a_cuerpo"
            ],

            "emociones": [
                "normal",
                "feliz",
                "enojado",
                "triste",
                "asustado",
                "determinado",
                "herido"
            ],

            "imagen_base":
                "assets/personajes/heroe.png"
        },
    "Aelar": {

        "nombre": "Aelar",

        "raza": "Elfo",

        "rol": "companero",

        "descripcion":
            "Arquero elfo de gran puntería y amigo leal del héroe.",

        "personalidad":
            "Leal, valiente y dispuesto a sacrificarse por sus amigos.",

        "habilidades": [
            "arqueria",
            "vision_nocturna"
        ],

        "imagen_base":
            "assets/personajes/aelar.png"
    },
    "Goblin": {

        "nombre": "Goblin",

        "raza": "Goblin",

        "rol": "enemigo",

        "descripcion":
            "Pequeña criatura verde de inteligencia limitada.",

        "personalidad":
            "Ingenuo, fácil de manipular y con hambre constante.",

        "habilidades": [
            "arma_improvisada"
        ],

        "imagen_base":
            "assets/personajes/goblin.png"
    },
    "Princesa": {

        "nombre": "Princesa",

        "raza": "Humana",

        "rol": "objetivo",

        "descripcion":
            "Princesa del reino secuestrada por Osgo.",

        "personalidad":
            "Inteligente, ambiciosa y decidida a sobrevivir.",

        "habilidades": [],

        "imagen_base":
            "assets/personajes/princesa.png"
    },
    "Osgo": {

        "nombre": "Osgo",

        "raza": "Orco",

        "rol": "jefe",

        "descripcion":
            "Líder de los goblins y guerrero temible.",

        "personalidad":
            "Orgulloso, agresivo y convencido de su destino.",

        "habilidades": [
            "martillo_de_guerra",
            "jabalina"
        ],

        "imagen_base":
            "assets/personajes/osgo.png"
    },

}

def obtener_personaje(nombre):
    return PERSONAJES.get(nombre)