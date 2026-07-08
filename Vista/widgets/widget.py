#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# widget
#
# widget define la superclase abstracta Widget, de la cual heredan todos los
# controles visuales interactivos. Provee lógica genérica de rectángulos de colisión,
# dimensiones y estados de visibilidad y habilitación.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Widget, clase base para componentes de interfaz de usuario.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ x, y, ancho, alto (properties)
#   --> Devuelven o establecen las coordenadas y dimensiones de la caja
# @ rect (property)
#   --> Devuelve el rectángulo de Pygame asociado al widget (pygame.Rect)
# @ visible, habilitado (properties)
#   --> Devuelven o cambian los booleanos de visibilidad y foco
# @ actualizar, método abstracto para actualizar el estado del widget
# @ manejar_evento, recibe un evento de Pygame y devuelve si fue procesado (bool)
# @ dibujar, recibe una superficie y dibuja el widget
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame provee la clase pygame.Rect y otras herramientas gráficas
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Widget:
    """
    Clase base para todos los componentes gráficos (widgets) de la interfaz de usuario.
    Representa un elemento visual reutilizable, independiente del modelo y del controlador.
    Define las propiedades comunes y la interfaz (contrato interno) que todos 
    los widgets específicos deben implementar.
    """

    def __init__(self, x, y, ancho, alto):
        """
        Inicializa las propiedades base del widget.
        
        Args:
            x (int): Posición en el eje X.
            y (int): Posición en el eje Y.
            ancho (int): Ancho del widget.
            alto (int): Alto del widget.
        """
        # Se utiliza pygame.Rect para almacenar posición y tamaño, 
        # facilitando cálculos de colisión (clicks de mouse) y dibujado.
        self._rect = pygame.Rect(x, y, ancho, alto)
        
        # Estados del widget
        self._visible = True
        self._habilitado = True

    # --- Propiedades de Posición y Tamaño ---

    @property
    def x(self):
        return self._rect.x
        
    @x.setter
    def x(self, valor):
        self._rect.x = valor

    @property
    def y(self):
        return self._rect.y
        
    @y.setter
    def y(self, valor):
        self._rect.y = valor

    @property
    def ancho(self):
        return self._rect.width
        
    @ancho.setter
    def ancho(self, valor):
        self._rect.width = valor

    @property
    def alto(self):
        return self._rect.height
        
    @alto.setter
    def alto(self, valor):
        self._rect.height = valor

    @property
    def rect(self):
        """Devuelve el rectángulo que define los límites del widget."""
        return self._rect

    # --- Propiedades de Estado ---

    @property
    def visible(self):
        """Indica si el widget debe ser dibujado en pantalla."""
        return self._visible

    @visible.setter
    def visible(self, estado):
        self._visible = estado

    @property
    def habilitado(self):
        """Indica si el widget puede recibir y procesar eventos (ej. clicks)."""
        return self._habilitado

    @habilitado.setter
    def habilitado(self, estado):
        self._habilitado = estado

    # --- Métodos del Ciclo de Vida (Interfaz a sobrescribir) ---

    def actualizar(self):
        """
        Actualiza la lógica interna del widget (animaciones, temporizadores, etc).
        Debe ser sobrescrito por las subclases si requieren lógica de actualización.
        """
        pass

    def manejar_evento(self, evento):
        """
        Procesa un evento del sistema (teclado, mouse).
        
        Args:
            evento (pygame.event.Event): Evento a procesar.
            
        Returns:
            bool: True si el evento fue consumido por el widget, False en caso contrario.
        """
        pass

    def dibujar(self, superficie):
        """
        Dibuja el widget sobre la superficie destino.
        
        Args:
            superficie (pygame.Surface): La superficie (pantalla o contenedor) donde dibujarse.
        """
        pass
