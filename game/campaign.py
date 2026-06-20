#------------------------------------------------------------------------------------------------------
# Campaign
#
# La idea aqui es describir como son las salas
#------------------------------------------------------------------------------------------------------
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
            "companero", 
            "heroe"
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
            "companero",
            "goblin", 
            "heroe"
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
            "companero",
            "goblin", 
            "heroe"
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
            "companero",
            "osgo",
            "princesa", 
            "heroe"
        ],

        "salidas": [
            "gran_salon"
        ]
    }
}
