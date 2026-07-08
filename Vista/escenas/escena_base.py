#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# escena_base
#
# escena_base implementa la clase base EscenaBase que representa una pantalla
# abstracta del juego, gestionando un conjunto de widgets secundarios y canalizando
# hacia ellos los flujos de dibujo y procesamiento de eventos.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ EscenaBase, clase base de control de layouts y colecciones de widgets.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ agregar_widget, recibe la instancia del widget a añadir
# @ quitar_widget, recibe la instancia del widget a remover
# @ manejar_evento, recibe un evento de Pygame y lo despacha a los widgets
# @ actualizar, delega la actualización periódica a los componentes internos
# @ dibujar, recibe la superficie de dibujo (pygame.Surface) y pinta los widgets
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
# (No contiene imports al inicio del archivo)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

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
