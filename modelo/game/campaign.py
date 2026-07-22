#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# campaign
#
# campaign define la estructura de las salas y el flujo de navegación de la
# campaña, detallando qué objetos y personajes se encuentran en cada una de ellas,
# así como las salidas válidas hacia otras salas.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ SALAS, diccionario que define las distintas salas del mapa de la campaña
#   (nombre, descripción, objetos iniciales, personajes presentes y salidas).
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# (No contiene imports externos ni locales)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
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

        "objetos": [
            "llave_templo"
        ],

        "personajes": [
            "companero",
            "goblin", 
            "heroe"
        ],

        "salidas": [
            "sala_osgo",
            "entrada_cueva"
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
            "puerta_goblins"
        ]
    }
}
