def crear_estado_inicial():

    return {

        "ubicacion": "entrada_cueva",

        "jugador": {
            "nombre": "Heroe",
            "vida": 100,
            "inventario": ["Espada"]
        },

        "companero": {
            "nombre": "Aelar",
            "raza": "Elfo",
            "estado": "normal"
        },

        "princesa": {
            "estado": "cautiva"
        },

        "osgo": {
            "estado": "normal"
        },

        "eventos": [],

        "decisiones": [],

        "personajes_presentes": [
            "companero"
        ],

        "final": None,

        "juego_terminado": False
    }