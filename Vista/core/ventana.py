import pygame
from core.recursos import GestorRecursos

class Ventana:
    """
    Clase responsable de administrar la ventana principal de la aplicación.
    Maneja la inicialización, el bucle principal y el cierre de la ventana,
    exponiendo la superficie principal para que otras clases puedan dibujar.
    """

    def __init__(self, gestor_recursos):
        """
        Configura la ventana principal a 1920x1080.
        Dependencias como pygame.init() y GestorRecursos son inyectadas/orquestadas por vista_grafica.
        """
        # Resolución fija
        self._ancho = 1920
        self._alto = 1080
        
        # Configurar la ventana
        self._pantalla = pygame.display.set_mode((self._ancho, self._alto))
        pygame.display.set_caption("DM AI")
        
        # Reloj para controlar los FPS
        self._reloj = pygame.time.Clock()
        self._fps = 60
        
        self._corriendo = False
        
        self._gestor_recursos = gestor_recursos
        self._fondo = None

    @property
    def pantalla(self):
        """
        Expone la superficie principal de la ventana.
        
        Returns:
            pygame.Surface: La superficie principal donde se puede dibujar.
        """
        return self._pantalla

    def iniciar(self):
        """
        Inicia el bucle principal de la ventana.
        Maneja los eventos básicos como el cierre de la ventana y mantiene los 60 FPS.
        """
        imagen_cruda = self._gestor_recursos.obtener_imagen("Vista/resources/images/fondo.png", alpha=False)
        if imagen_cruda:
            self._fondo = pygame.transform.scale(imagen_cruda, (self._ancho, self._alto))
            
        self._corriendo = True
        
        while self._corriendo:
            self._manejar_eventos()
            self._actualizar_pantalla()
            self._reloj.tick(self._fps)

    def _manejar_eventos(self):
        """
        Procesa los eventos de Pygame.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._corriendo = False

    def _actualizar_pantalla(self):
        """
        Actualiza el contenido de la ventana.
        """
        if self._fondo:
            self._pantalla.blit(self._fondo, (0, 0))
        else:
            self._pantalla.fill((0, 0, 0))
            
        pygame.display.flip()
