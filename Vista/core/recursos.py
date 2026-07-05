import pygame
import os

class GestorRecursos:
    """
    Gestor centralizado de recursos para la vista.
    Se encarga de cargar y almacenar en memoria imágenes, fuentes y sonidos
    para evitar cargas redundantes de disco, optimizando el rendimiento.
    """

    def __init__(self):
        """
        Inicializa los diccionarios de caché para los distintos tipos de recursos.
        """
        self._imagenes = {}
        self._fuentes = {}
        self._sonidos = {}

    def obtener_imagen(self, ruta, alpha=True):
        """
        Obtiene una imagen desde la caché, o la carga si no ha sido solicitada antes.

        Args:
            ruta (str): Ruta al archivo de imagen.
            alpha (bool): Indica si se debe preservar el canal alfa (transparencias).

        Returns:
            pygame.Surface: Superficie de la imagen solicitada.
        """
        if ruta not in self._imagenes:
            try:
                imagen = pygame.image.load(ruta)
                # Optimizar la imagen para el dibujado en pantalla
                if alpha:
                    imagen = imagen.convert_alpha()
                else:
                    imagen = imagen.convert()
                self._imagenes[ruta] = imagen
            except pygame.error as e:
                print(f"Error al cargar la imagen '{ruta}': {e}")
                return None
        
        return self._imagenes[ruta]

    def obtener_fuente(self, ruta, tamano):
        """
        Obtiene una fuente desde la caché, o la carga si no existe.
        La clave en la caché está compuesta por la ruta y el tamaño de la fuente.

        Args:
            ruta (str): Ruta al archivo de la fuente (.ttf). Puede ser None para la fuente por defecto.
            tamano (int): Tamaño de la fuente en píxeles.

        Returns:
            pygame.font.Font: Objeto de fuente listo para renderizar texto.
        """
        clave = (ruta, tamano)
        if clave not in self._fuentes:
            try:
                fuente = pygame.font.Font(ruta, tamano)
                self._fuentes[clave] = fuente
            except pygame.error as e:
                print(f"Error al cargar la fuente '{ruta}': {e}")
                return None
        
        return self._fuentes[clave]

    def obtener_sonido(self, ruta):
        """
        Obtiene un sonido desde la caché, o lo carga si no existe.

        Args:
            ruta (str): Ruta al archivo de sonido.

        Returns:
            pygame.mixer.Sound: Objeto de sonido listo para reproducirse.
        """
        if ruta not in self._sonidos:
            try:
                sonido = pygame.mixer.Sound(ruta)
                self._sonidos[ruta] = sonido
            except pygame.error as e:
                print(f"Error al cargar el sonido '{ruta}': {e}")
                return None
                
        return self._sonidos[ruta]

    def limpiar_cache(self):
        """
        Libera la memoria vaciando los diccionarios de recursos.
        Útil para transiciones entre escenas muy pesadas.
        """
        self._imagenes.clear()
        self._fuentes.clear()
        self._sonidos.clear()
