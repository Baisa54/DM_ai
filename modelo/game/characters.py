#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# characters
#
# characters define el catálogo de personajes que participan en la campaña,
# incluyendo al héroe, su compañero y los enemigos. Contiene sus descripciones,
# estados y los prompts visuales utilizados para la generación de retratos e imágenes.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PERSONAJES, diccionario que contiene los datos de configuración de cada personaje
#   (nombre, raza, estado inicial, descripción y prompt_visual).
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# (No contiene imports externos ni locales)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

PERSONAJES = {

    "heroe": {
        "nombre": "Heroe",
        "raza": "Humano",
        "Estado": "vivo",

        "descripcion":
            "Guerrero humano aventurero equipado con una espada común. "
            "Ha aceptado la misión de rescatar a la princesa secuestrada por los goblins.",

        "imagen": "modelo/game/assets/heroe.png",

        "prompt_visual":
            "young human male warrior, fantasy RPG hero, medieval armor, steel sword, "
            "determined expression, cinematic lighting, dark fantasy style, highly detailed concept art"
    },

    "companero": {
        "nombre": "Aelar",
        "raza": "Elfo",
        "Estado": "vivo",

        "descripcion":
            "Arquero elfo de gran puntería y amigo leal del héroe. "
            "Valiente y protector de sus aliados.",

        "imagen": "modelo/game/assets/aelar.png",

        "prompt_visual":
            "male elf archer, fantasy RPG character, long silver hair, bow and arrows, "
            "forest ranger armor, elegant and agile, cinematic fantasy art, highly detailed"
    },

    "goblin": {
        "nombre": "Goblin",
        "raza": "Goblin",
        "Estado": "vivo",

        "descripcion":
            "Pequeña criatura verde de inteligencia limitada. "
            "Hambre constante y comportamiento caótico.",

        "imagen": "modelo/game/assets/goblin.png",

        "prompt_visual":
            "small green goblin creature, dirty and mischievous, fantasy dungeon creature, "
            "ragged clothes, ugly face, dark cave lighting, RPG monster concept art"
    },

    "princesa": {
        "nombre": "Princesa",
        "raza": "Humana",
        "Estado": "viva",

        "descripcion":
            "Princesa del reino secuestrada por Osgo. "
            "Inteligente y decidida a sobrevivir.",

        "imagen": "modelo/game/assets/princesa.png",

        "prompt_visual":
            "beautiful fantasy princess, long elegant dress slightly dirty, chained in dungeon, "
            "soft light, emotional expression, cinematic RPG style, highly detailed"
    },

    "osgo": {
        "nombre": "Osgo",
        "raza": "Orco",
        "Estado": "vivo",

        "descripcion":
            "Líder de los goblins y guerrero temible. "
            "Posee un martillo de guerra y domina la cueva.",

        "imagen": "modelo/game/assets/osgo.png",

        "prompt_visual":
            "massive orc warlord boss, muscular, armored, war hammer, intimidating presence, "
            "dark throne room, skull decorations, cinematic dark fantasy RPG art"
    },
}