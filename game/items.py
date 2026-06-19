ITEMS = {

    "espada": {
        "nombre": "Espada",
        "tipo": "arma",
        "descripcion": "Una espada común utilizada por el héroe."
    },

    "comida": {
        "nombre": "Comida",
        "tipo": "consumible",
        "descripcion": "Provisiones encontradas cerca de la entrada de la cueva."
    },

    "antorcha": {
        "nombre": "Antorcha",
        "tipo": "herramienta",
        "descripcion": "Permite iluminar zonas oscuras."
    },

    "llave_goblin": {
        "nombre": "Llave Goblin",
        "tipo": "llave",
        "descripcion": "Abre la gran puerta roja custodiada por los goblins."
    },

    "llave_templo": {
        "nombre": "Llave del Templo",
        "tipo": "llave",
        "descripcion": "Permite abrir la puerta metálica reforzada."
    },

    "martillo_osgo": {
        "nombre": "Martillo de Guerra de Osgo",
        "tipo": "arma",
        "descripcion": "Un enorme martillo capaz de aplastar armaduras."
    },

    "jabalina_osgo": {
        "nombre": "Jabalina de Osgo",
        "tipo": "arma",
        "descripcion": "Arma arrojadiza utilizada por Osgo."
    }
}

def obtener_item(item_id):
    return ITEMS.get(item_id)