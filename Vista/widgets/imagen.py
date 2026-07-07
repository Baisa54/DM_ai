import pygame
from widgets.widget import Widget

class Imagen(Widget):
    """
    Widget concreto para mostrar una imagen.
    Delega la carga de la imagen al GestorRecursos.
    """

    def __init__(self, x, y, ruta_imagen, gestor_recursos, ancho=None, alto=None, alpha=True):
        """
        Inicializa el widget de imagen.
        
        Args:
            x (int): Posición X.
            y (int): Posición Y.
            ruta_imagen (str): La ruta del archivo a cargar (puede ser None).
            gestor_recursos (GestorRecursos): El gestor encargado de proveer el asset.
            ancho (int, opcional): Ancho deseado. Si es None, usa el de la imagen.
            alto (int, opcional): Alto deseado. Si es None, usa el de la imagen.
            alpha (bool): Si la imagen requiere mantener canal de transparencia.
        """
        # Inicializamos con 0 temporales si no hay tamaño
        super().__init__(x, y, ancho or 0, alto or 0)
        
        self._gestor_recursos = gestor_recursos
        self._alpha = alpha
        
        self._superficie_original = None
        self._superficie_escalada = None
        
        if ruta_imagen:
            self.cambiar_imagen(ruta_imagen)
            
            # Autocompletar tamaño si no fue provisto
            if self._superficie_original:
                if ancho is None:
                    self._rect.width = self._superficie_original.get_width()
                if alto is None:
                    self._rect.height = self._superficie_original.get_height()
                
            self._actualizar_escala()

    def cambiar_imagen(self, ruta_imagen):
        """
        Solicita una nueva imagen al gestor de recursos y la adapta al widget.
        
        Args:
            ruta_imagen (str): Ruta de la nueva imagen.
        """
        self._superficie_original = self._gestor_recursos.obtener_imagen(ruta_imagen, alpha=self._alpha)
        self._actualizar_escala()

    def _actualizar_escala(self):
        """Escala la imagen original a las dimensiones actuales del widget con antialiasing."""
        if self._superficie_original:
            # smoothscale proporciona mucha mejor calidad al redimensionar, especialmente al reducir (ej. Fondo)
            self._superficie_escalada = pygame.transform.smoothscale(
                self._superficie_original, (self.ancho, self.alto)
            )
        else:
            self._superficie_escalada = None

    # Sobrescribimos ancho y alto para reescalar la imagen automáticamente si cambia el tamaño
    @property
    def ancho(self):
        return self._rect.width
        
    @ancho.setter
    def ancho(self, valor):
        self._rect.width = valor
        self._actualizar_escala()

    @property
    def alto(self):
        return self._rect.height
        
    @alto.setter
    def alto(self, valor):
        self._rect.height = valor
        self._actualizar_escala()

    def dibujar(self, superficie):
        """Dibuja la imagen en la superficie destino si es visible."""
        if self.visible and self._superficie_escalada:
            superficie.blit(self._superficie_escalada, self.rect)
