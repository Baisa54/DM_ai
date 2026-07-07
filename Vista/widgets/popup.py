import pygame
from widgets.widget import Widget

class Popup(Widget):
    """
    Widget contenedor que actúa como una ventana emergente (modal).
    Permite agrupar otros widgets en su interior, y abrirse o cerrarse
    para mostrarse y ocultarse en conjunto.
    """

    def __init__(self, x, y, gestor_recursos, ruta_fondo=None, ancho=None, alto=None):
        """
        Inicializa el popup.
        
        Args:
            x (int): Posición X en pantalla.
            y (int): Posición Y en pantalla.
            gestor_recursos (GestorRecursos): Gestor para cargar el fondo.
            ruta_fondo (str): Ruta a la imagen de fondo del popup.
            ancho (int, opcional): Ancho forzado.
            alto (int, opcional): Alto forzado.
        """
        super().__init__(x, y, ancho or 0, alto or 0)
        self._gestor_recursos = gestor_recursos
        
        self._img_fondo_orig = self._gestor_recursos.obtener_imagen(ruta_fondo, alpha=True) if ruta_fondo else None
        self._img_fondo = None
        
        # Autodimensionamiento si no se envían dimensiones
        if self._img_fondo_orig:
            if ancho is None:
                self._rect.width = self._img_fondo_orig.get_width()
            if alto is None:
                self._rect.height = self._img_fondo_orig.get_height()
                
        self._actualizar_escala_fondo()
        
        self._hijos = []
        
        # Por defecto, un popup nace cerrado
        self.cerrar()

    def _actualizar_escala_fondo(self):
        """Re-escala el fondo si el popup cambia de tamaño."""
        if self._img_fondo_orig:
            self._img_fondo = pygame.transform.scale(self._img_fondo_orig, (self.ancho, self.alto))

    @property
    def ancho(self):
        return self._rect.width
        
    @ancho.setter
    def ancho(self, valor):
        self._rect.width = valor
        self._actualizar_escala_fondo()

    @property
    def alto(self):
        return self._rect.height
        
    @alto.setter
    def alto(self, valor):
        self._rect.height = valor
        self._actualizar_escala_fondo()

    def abrir(self):
        """Abre el popup haciéndolo visible y habilitando eventos."""
        self.visible = True
        self.habilitado = True

    def cerrar(self):
        """Cierra el popup, ocultándolo y bloqueando eventos."""
        self.visible = False
        self.habilitado = False

    def agregar_widget(self, widget):
        """
        Añade un widget hijo al popup.
        Nota: Las coordenadas del hijo deben ser absolutas a la pantalla.
        """
        if widget not in self._hijos:
            self._hijos.append(widget)

    def quitar_widget(self, widget):
        """Elimina un widget hijo del popup."""
        if widget in self._hijos:
            self._hijos.remove(widget)

    def actualizar(self):
        """Actualiza todos los widgets hijos habilitados del popup."""
        if not self.habilitado:
            return
            
        for hijo in self._hijos:
            if hijo.habilitado:
                hijo.actualizar()

    def manejar_evento(self, evento):
        """
        Procesa eventos para el popup y sus hijos.
        Actúa como modal: consume eventos que ocurren dentro de su área
        para que no afecten a los widgets que quedaron debajo en la escena.
        """
        if not self.habilitado or not self.visible:
            return False

        # 1. Distribuir a los hijos de adelante hacia atrás
        for hijo in reversed(self._hijos):
            if hijo.habilitado:
                consumido = hijo.manejar_evento(evento)
                if consumido:
                    return True

        # 2. Comportamiento modal: si el evento del mouse es sobre el popup, lo consumimos
        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            if self.rect.collidepoint(evento.pos):
                return True

        return False

    def dibujar(self, superficie):
        """Dibuja el fondo del popup y luego todos sus hijos visibles."""
        if not self.visible:
            return

        # 1. Dibujar el propio fondo
        if self._img_fondo:
            superficie.blit(self._img_fondo, self.rect)

        # 2. Dibujar a los hijos
        for hijo in self._hijos:
            if hijo.visible:
                hijo.dibujar(superficie)
