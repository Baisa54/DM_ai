from clases.MensajeJuego import MensajeJuego

def genMessage():

    mensaje = MensajeJuego()

    mensaje.set_narracion(
        "El protagonista, un guerrero humano, y su leal compañero arquero elfo, "
        "Aelar, han llegado a la misteriosa cueva donde se rumorea, está la "
        "princesa del reino atrapada. Han tenido que pasar por un bosque denso "
        "y oscuro, esquivar animales peligrosos y sobrevivir con pocas provisiones. "
        "Se logra ver al costado de la cueva una caja con un poco de comida y una antorcha."
    )

    mensaje.set_imagen_resumen(
        "game/assets/imagen_inicio.png"
    )

    return mensaje

