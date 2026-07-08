#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# ventana
#
# ventana implementa la clase Ventana, que administra la ventana física de la
# aplicación Pygame, gestionando la inicialización del motor, el bucle de renderizado,
# la tasa de fotogramas (FPS) y la delegación de eventos a la escena activa.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ Ventana, clase administradora de la ventana de renderizado.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ pantalla (property)
#   --> Devuelve la superficie de renderizado virtual (pygame.Surface).
# @ cambiar_escena, recibe la instancia de la escena a cargar
# @ iniciar, inicia el bucle principal de la aplicación Pygame
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame provee la capa de hardware y dibujo gráfico
from Vista.core.recursos import GestorRecursos
# GestorRecursos es el encargado de la carga óptima de assets en caché
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Ventana:
    """
    Clase responsable de administrar la ventana principal de la aplicación.
    Maneja la inicialización, el bucle principal y el cierre de la ventana,
    exponiendo la superficie principal para que otras clases puedan dibujar.
    """

    def __init__(self):
        """
        Configura la ventana principal usando una superficie virtual de 1920x1080.
        Si la pantalla es más pequeña, redimensiona y adapta automáticamente.
        """
        pygame.init()
        
        # Resolución nativa/virtual en la que programamos la UI
        self._ancho_virtual = 1920
        self._alto_virtual = 1080
        
        # Obtener resolución real del monitor del usuario
        info = pygame.display.Info()
        self._ancho_real = info.current_w
        self._alto_real = info.current_h
        
        # Si la pantalla del usuario es menor a 1920x1080, usamos pantalla completa 
        # a la máxima resolución de su monitor para que encaje perfecto sin desbordar.
        if self._ancho_real < 1920 or self._alto_real < 1080:
            self._pantalla = pygame.display.set_mode((self._ancho_real, self._alto_real), pygame.FULLSCREEN)
        else:
            # Si el monitor es grande, podemos dejarlo en ventana
            self._pantalla = pygame.display.set_mode((self._ancho_virtual, self._alto_virtual))
            
        pygame.display.set_caption("DM AI")
        
        # Superficie virtual donde realmente se dibuja todo el juego
        self._superficie_virtual = pygame.Surface((self._ancho_virtual, self._alto_virtual))
        
        # Ratios para traducir el mouse
        self._ratio_x = self._ancho_virtual / self._pantalla.get_width()
        self._ratio_y = self._alto_virtual / self._pantalla.get_height()
        
        # Reloj para controlar los FPS
        self._reloj = pygame.time.Clock()
        self._fps = 60
        
        self._corriendo = False
        self._escena_actual = None

    @property
    def pantalla(self):
        # Ahora el exterior (Escenas, widgets) dibuja en la superficie virtual
        return self._superficie_virtual

    def cambiar_escena(self, escena):
        self._escena_actual = escena

    def iniciar(self):
        self._corriendo = True
        
        while self._corriendo:
            self._manejar_eventos()
            self._actualizar_pantalla()
            self._reloj.tick(self._fps)

    def _manejar_eventos(self):
        """Procesa los eventos y escala las coordenadas del mouse si es necesario."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self._corriendo = False
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                # Permitimos cerrar con ESC por comodidad si estamos en Fullscreen
                self._corriendo = False
                
            # Traducir coordenadas físicas del mouse a coordenadas virtuales (1920x1080)
            if hasattr(evento, 'pos'):
                # Tupla inmutable en Pygame a veces, pero para propagar a los widgets creamos un nuevo atributo
                evento.pos = (int(evento.pos[0] * self._ratio_x), int(evento.pos[1] * self._ratio_y))
                
            if self._escena_actual:
                self._escena_actual.manejar_evento(evento)

    def _actualizar_pantalla(self):
        """
        Dibuja la UI en la superficie virtual y luego la escala al tamaño real de la pantalla.
        """
        self._superficie_virtual.fill((0, 0, 0))
        
        if self._escena_actual:
            self._escena_actual.actualizar()
            self._escena_actual.dibujar(self._superficie_virtual)
            
        # Si la ventana física es distinta de 1920x1080, escalamos el renderizado final
        if self._pantalla.get_size() != self._superficie_virtual.get_size():
            # Usamos smoothscale para que no se deforme/pixele la UI al reducirla
            sup_escalada = pygame.transform.smoothscale(self._superficie_virtual, self._pantalla.get_size())
            self._pantalla.blit(sup_escalada, (0, 0))
        else:
            self._pantalla.blit(self._superficie_virtual, (0, 0))
            
        pygame.display.flip()
