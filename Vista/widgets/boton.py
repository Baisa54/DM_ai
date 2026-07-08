#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# boton
#
# boton implementa la clase Boton, un widget interactivo táctil que detecta eventos
# de mouse y reacciona visualmente según tres estados predeterminados:
# normal, hover y presionado, ejecutando un callback configurado al hacer clic.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Boton, clase del botón gráfico.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ manejar_evento, recibe el evento de Pygame
#   --> Devuelve si consumió el evento (bool)
# @ dibujar, dibuja la textura del botón correspondiente al estado activo
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame se utiliza para transformaciones de imágenes y detección de eventos de mouse
from Vista.widgets.widget import Widget
# Widget es la clase base de la cual hereda Boton
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Boton(Widget):
    """
    Widget interactivo que representa un botón.
    Soporta tres estados visuales: normal, hover (mouse encima) y presionado.
    """

    def __init__(self, x, y, ruta_normal, ruta_hover, ruta_presionado, gestor_recursos, ancho=None, alto=None, on_click=None):
        """
        Inicializa el botón.
        
        Args:
            x (int): Posición X.
            y (int): Posición Y.
            ruta_normal (str): Ruta de la imagen para el estado normal.
            ruta_hover (str): Ruta de la imagen para el estado hover.
            ruta_presionado (str): Ruta de la imagen para el estado presionado.
            gestor_recursos (GestorRecursos): Gestor para cargar los assets.
            ancho (int, opcional): Ancho forzado del botón.
            alto (int, opcional): Alto forzado del botón.
            on_click (callable, opcional): Función de callback a ejecutar al ser presionado.
        """
        super().__init__(x, y, ancho or 0, alto or 0)
        self._gestor_recursos = gestor_recursos
        self._on_click = on_click
        
        # Estado interno
        self._estado = "normal"
        self._mouse_presionado = False

        # Carga de imágenes originales
        self._img_normal_orig = self._gestor_recursos.obtener_imagen(ruta_normal, alpha=True)
        self._img_hover_orig = self._gestor_recursos.obtener_imagen(ruta_hover, alpha=True)
        self._img_presionado_orig = self._gestor_recursos.obtener_imagen(ruta_presionado, alpha=True)

        # Superficies escaladas a usar para el dibujo
        self._img_normal = None
        self._img_hover = None
        self._img_presionado = None

        # Autodimensionar si no se pasó tamaño
        if self._img_normal_orig:
            if ancho is None:
                self._rect.width = self._img_normal_orig.get_width()
            if alto is None:
                self._rect.height = self._img_normal_orig.get_height()
                
        self._actualizar_escala()

    def _actualizar_escala(self):
        """Re-escala las tres imágenes si el tamaño del botón cambia."""
        if self._img_normal_orig:
            self._img_normal = pygame.transform.scale(self._img_normal_orig, (self.ancho, self.alto))
        if self._img_hover_orig:
            self._img_hover = pygame.transform.scale(self._img_hover_orig, (self.ancho, self.alto))
        if self._img_presionado_orig:
            self._img_presionado = pygame.transform.scale(self._img_presionado_orig, (self.ancho, self.alto))

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

    def manejar_evento(self, evento):
        """
        Procesa el movimiento y los clicks del mouse para cambiar el estado del botón.
        """
        if not self.habilitado or not self.visible:
            return False

        if evento.type == pygame.MOUSEMOTION:
            # Detecta si el mouse pasa por encima (Hover)
            if self.rect.collidepoint(evento.pos):
                if not self._mouse_presionado:
                    if self._estado != "hover":
                        snd_hover = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/hover.wav")
                        if snd_hover:
                            snd_hover.play()
                    self._estado = "hover"
            else:
                self._estado = "normal"
                self._mouse_presionado = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Detecta el click izquierdo (Presionado)
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                self._estado = "presionado"
                self._mouse_presionado = True
                return True # Consumimos el evento para que no atraviese a otros widgets

        elif evento.type == pygame.MOUSEBUTTONUP:
            # Detecta cuando se suelta el click izquierdo
            if evento.button == 1 and self._mouse_presionado:
                self._mouse_presionado = False
                if self.rect.collidepoint(evento.pos):
                    # Si soltó el click Estando sobre el botón -> Dispara el evento
                    self._estado = "hover"
                    if self._on_click:
                        self._on_click()
                    return True
                else:
                    self._estado = "normal"

        return False

    def dibujar(self, superficie):
        """Dibuja el botón según su estado actual."""
        if not self.visible:
            return

        imagen_a_dibujar = self._img_normal
        if self._estado == "hover" and self._img_hover:
            imagen_a_dibujar = self._img_hover
        elif self._estado == "presionado" and self._img_presionado:
            imagen_a_dibujar = self._img_presionado

        if imagen_a_dibujar:
            superficie.blit(imagen_a_dibujar, self.rect)
