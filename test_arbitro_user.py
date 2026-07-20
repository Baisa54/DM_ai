from modelo.clases.Estadojuego import EstadoJuego
from modelo.ai.arbitro_accion import arbitrar_accion
import json

estado = EstadoJuego()
# Simulamos entrada de cueva
estado.set_ubicacion("entrada_cueva")

acciones = [
    "Intento trepar ágilmente a un árbol alto del bosque para ver qué nos espera.",
    "Empujo a mi compañero Aelar hacia la cueva engañándolo para que entre primero.",
    "Hago un salto mortal hacia atrás para calentar los músculos."
]

for a in acciones:
    print(f"\n--- {a} ---")
    print(json.dumps(arbitrar_accion(a, estado), indent=2, ensure_ascii=False))

