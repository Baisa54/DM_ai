SALAS = {

    "entrada_cueva": {

        "nombre": "Entrada de la Cueva",

        "descripcion":
            "Un bosque oscuro rodea la entrada de una enorme cueva. "
            "Cerca de la entrada hay comida y una antorcha abandonadas.",

        "objetos": [
            "comida",
            "antorcha"
        ],

        "personajes": [
            "aelar"
        ],

        "salidas": [
            "puerta_goblins"
        ]
    },

    "puerta_goblins": {

        "nombre": "Puerta Custodiada",

        "descripcion":
            "Una enorme puerta roja bloquea el paso. "
            "Dos goblins hambrientos vigilan la entrada.",

        "objetos": [],

        "personajes": [
            "aelar",
            "goblin"
        ],

        "salidas": [
            "entrada_cueva",
            "gran_salon"
        ]
    },

    "gran_salon": {

        "nombre": "Gran Salón Goblin",

        "descripcion":
            "Un antiguo templo convertido en guarida goblin. "
            "Al fondo se encuentra una puerta metálica reforzada.",

        "objetos": [
            "llave_templo"
        ],

        "personajes": [
            "aelar",
            "goblin"
        ],

        "salidas": [
            "puerta_goblins",
            "sala_osgo"
        ]
    },

    "sala_osgo": {

        "nombre": "Sala del Líder Osgo",

        "descripcion":
            "Un salón lleno de trofeos y restos de héroes derrotados. "
            "Osgo descansa en un trono de huesos mientras la princesa permanece cautiva.",

        "objetos": [],

        "personajes": [
            "aelar",
            "osgo",
            "princesa"
        ],

        "salidas": []
    }
}

def obtener_sala(id_sala):
    return SALAS.get(id_sala)

EVENTOS_IMPORTANTES = [

    "obtuvo_antorcha",

    "obtuvo_comida",

    "engano_goblins",

    "dio_comida_goblins",

    "robo_llave",

    "abrieron_puerta",

    "enfrento_osgo",

    "rescato_princesa"
]