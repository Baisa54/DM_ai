class EscenaBase:
    """
    Clase base para todas las escenas (pantallas) de la aplicación.
    Maneja una colección de widgets, encargándose de delegarles
    los eventos, su actualización y su dibujado.
    
    Es completamente independiente del modelo, controlador y lógica del juego.
    """

    def __init__(self):
        """Inicializa la lista de widgets de la escena."""
        self._widgets = []

    def agregar_widget(self, widget):
        """
        Añade un widget a la escena.
        
        Args:
            widget: El componente gráfico a añadir (instancia que herede de Widget).
        """
        if widget not in self._widgets:
            self._widgets.append(widget)

    def quitar_widget(self, widget):
        """
        Elimina un widget de la escena si existe en ella.
        
        Args:
            widget: El componente gráfico a remover.
        """
        if widget in self._widgets:
            self._widgets.remove(widget)

    def manejar_evento(self, evento):
        """
        Distribuye un evento de Pygame a todos los widgets habilitados.
        
        Se recorre la lista en orden inverso (de adelante hacia atrás visualmente)
        para que los widgets en primer plano puedan interceptar eventos 
        (como un click) antes que los widgets de fondo.
        
        Args:
            evento (pygame.event.Event): El evento a procesar.
        """
        for widget in reversed(self._widgets):
            if widget.habilitado:
                consumido = widget.manejar_evento(evento)
                # Si el widget consume el evento (ej. un click en un botón),
                # se detiene la propagación para que los widgets debajo no lo reciban.
                if consumido:
                    break

    def actualizar(self):
        """
        Delega la actualización de estado a todos los widgets habilitados.
        """
        for widget in self._widgets:
            if widget.habilitado:
                widget.actualizar()

    def dibujar(self, superficie):
        """
        Dibuja todos los widgets visibles en la superficie proporcionada.
        
        Se dibujan en el orden en que fueron agregados (de atrás hacia adelante,
        Painter's Algorithm).
        
        Args:
            superficie (pygame.Surface): La superficie destino (normalmente la pantalla).
        """
        for widget in self._widgets:
            if widget.visible:
                widget.dibujar(superficie)
