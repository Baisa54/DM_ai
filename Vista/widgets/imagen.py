#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# imagen
#
# imagen implementa la clase Imagen, un control gráfico simple para pintar imágenes
# y texturas en pantalla con soporte de escalado suavizado (smoothscale) de assets.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Imagen, clase de renderizado estático de imágenes.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ cambiar_imagen, recibe la ruta (str) y actualiza la textura
# @ dibujar, pinta la textura activa en la pantalla
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame provee las funciones de escalado smoothscale y dibujo blit
from Vista.widgets.widget import Widget
# Widget es la clase base para propiedades geométricas de la imagen
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Imagen(Widget):
    """
    Widget concreto para mostrar una imagen.
    Delega la carga de la imagen al GestorRecursos.
    """

    def __init__(self, x, y, ruta_imagen, gestor_recursos, ancho=None, alto=None, alpha=True, mantener_proporcion=False):
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
            mantener_proporcion (bool): Escala manteniendo aspect ratio y centra la imagen en el box.
        """
        # Inicializamos con 0 temporales si no hay tamaño
        super().__init__(x, y, ancho or 0, alto or 0)
        
        self._gestor_recursos = gestor_recursos
        self._alpha = alpha
        self._mantener_proporcion = mantener_proporcion
        self._offset_x = 0
        self._offset_y = 0
        
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
            if getattr(self, '_mantener_proporcion', False):
                # Calcular aspect ratio
                orig_w, orig_h = self._superficie_original.get_size()
                if orig_w == 0 or orig_h == 0:
                    self._superficie_escalada = None
                    return
                ratio_x = self.ancho / orig_w
                ratio_y = self.alto / orig_h
                ratio = min(ratio_x, ratio_y)
                
                new_w = int(orig_w * ratio)
                new_h = int(orig_h * ratio)
                
                self._superficie_escalada = pygame.transform.smoothscale(
                    self._superficie_original, (new_w, new_h)
                )
                
                # Calcular offsets para centrar en el box
                self._offset_x = (self.ancho - new_w) // 2
                self._offset_y = (self.alto - new_h) // 2
            else:
                self._superficie_escalada = pygame.transform.smoothscale(
                    self._superficie_original, (self.ancho, self.alto)
                )
                self._offset_x = 0
                self._offset_y = 0
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
            superficie.blit(self._superficie_escalada, (self.rect.x + self._offset_x, self.rect.y + self._offset_y))
