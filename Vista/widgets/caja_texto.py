#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# caja_texto
#
# caja_texto implementa CajaTexto, un widget interactivo de entrada de texto gráfico.
# Admite foco, escritura, borrado, navegación con cursor y scrolling horizontal
# automático cuando el texto excede el espacio visual de la caja.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ CajaTexto, clase que define el control de caja de entrada de texto.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ texto (property)
#   --> Devuelve el string actual de la caja
# @ limpiar, vacía el contenido de texto de la caja
# @ actualizar, actualiza la lógica interna de parpadeo del cursor
# @ manejar_evento, recibe el evento y devuelve si fue procesado (bool)
# @ dibujar, dibuja el fondo, el texto visible recortado y el cursor
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame se usa para renderizar texto sobre superficies y trazar la línea del cursor
import time
# time permite calcular los intervalos del parpadeo del cursor
from Vista.widgets.widget import Widget
# Widget es la superclase que le da las propiedades y dimensiones básicas
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class CajaTexto(Widget):
    """
    Widget de entrada gráfica para que el usuario escriba texto.
    """

    def __init__(self, x, y, ancho, alto, gestor_recursos, ruta_fondo=None, fuente_ruta=None, fuente_tamano=32, placeholder="Escribe aquí...", max_longitud=50):
        """
        Inicializa la caja de texto.
        
        Args:
            x, y, ancho, alto (int): Dimensiones y posición.
            gestor_recursos (GestorRecursos): Para cargar el fondo y la fuente.
            ruta_fondo (str): Imagen opcional de fondo para la caja.
            fuente_ruta (str): Ruta de la fuente ttf. None para la de Pygame por defecto.
            fuente_tamano (int): Tamaño de letra.
            placeholder (str): Texto a mostrar cuando está vacío y sin foco.
            max_longitud (int): Cantidad máxima de caracteres permitidos.
        """
        super().__init__(x, y, ancho, alto)
        self._gestor_recursos = gestor_recursos
        
        # Carga de la imagen de fondo (opcional)
        self._img_fondo_orig = self._gestor_recursos.obtener_imagen(ruta_fondo, alpha=True) if ruta_fondo else None
        self._img_fondo = None
        self._actualizar_escala_fondo()

        # Carga de la fuente
        self._fuente = self._gestor_recursos.obtener_fuente(fuente_ruta, fuente_tamano)
        if not self._fuente:
            self._fuente = pygame.font.Font(None, fuente_tamano)
            
        # Variables de estado del texto
        self._texto = ""
        self._placeholder = placeholder
        self._max_longitud = max_longitud
        self._cursor_pos = 0
        
        # Estados interactivos
        self._foco = False
        self._mostrar_cursor = True
        self._ultimo_parpadeo = time.time()
        
        # Colores (Por defecto blanco para texto y gris claro para placeholder)
        self.color_texto = (255, 255, 255)
        self.color_placeholder = (180, 180, 180)
        self.color_cursor = (255, 255, 255)
        
        # Padding (espaciado interno)
        self.padding_x = 20
        self.padding_y = None # Si es None, se centra verticalmente
        self.padding_right = 20 # Margen derecho para el texto visible
        
        self._scroll_x = 0 # Desplazamiento horizontal para texto largo

    def _actualizar_escala_fondo(self):
        """Re-escala el fondo si las dimensiones del widget cambian."""
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

    @property
    def texto(self):
        """Propiedad para acceder (solo lectura) al texto actual ingresado por el usuario."""
        return self._texto

    def limpiar(self):
        """Borra todo el texto contenido."""
        self._texto = ""
        self._cursor_pos = 0
        self._scroll_x = 0

    def actualizar(self):
        """Actualiza la lógica del parpadeo del cursor."""
        if not self.habilitado:
            return
            
        if self._foco:
            # Hace parpadear el cursor cada 0.5 segundos
            if time.time() - self._ultimo_parpadeo > 0.5:
                self._mostrar_cursor = not self._mostrar_cursor
                self._ultimo_parpadeo = time.time()
        else:
            self._mostrar_cursor = False

    def _ajustar_scroll(self):
        """Ajusta el scroll para que el cursor siempre esté visible."""
        texto_hasta_cursor = self._texto[:self._cursor_pos]
        cursor_px = 0
        if texto_hasta_cursor:
            cursor_px = self._fuente.render(texto_hasta_cursor, True, (0,0,0)).get_width()
            
        ancho_visible = self.ancho - self.padding_x - self.padding_right
        
        # Si el cursor se va por la derecha
        if cursor_px - self._scroll_x > ancho_visible:
            self._scroll_x = cursor_px - ancho_visible
        # Si el cursor se va por la izquierda
        elif cursor_px - self._scroll_x < 0:
            self._scroll_x = cursor_px

    def manejar_evento(self, evento):
        """Procesa clicks para obtener el foco, y eventos de teclado para escribir/borrar."""
        if not self.habilitado or not self.visible:
            return False

        # 1. Manejo del foco mediante clicks
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                self._foco = True
                self._mostrar_cursor = True
                self._ultimo_parpadeo = time.time()
                return True
            else:
                self._foco = False
                return False

        # 2. Manejo de escritura (solo si tiene el foco)
        if evento.type == pygame.KEYDOWN and self._foco:
            
            if evento.key == pygame.K_BACKSPACE:
                # Borrar hacia la izquierda
                if self._cursor_pos > 0:
                    self._texto = self._texto[:self._cursor_pos-1] + self._texto[self._cursor_pos:]
                    self._cursor_pos -= 1
                    
            elif evento.key == pygame.K_DELETE:
                # Borrar hacia la derecha
                if self._cursor_pos < len(self._texto):
                    self._texto = self._texto[:self._cursor_pos] + self._texto[self._cursor_pos+1:]
                    
            elif evento.key == pygame.K_LEFT:
                # Mover cursor a la izquierda
                if self._cursor_pos > 0:
                    self._cursor_pos -= 1
                    
            elif evento.key == pygame.K_RIGHT:
                # Mover cursor a la derecha
                if self._cursor_pos < len(self._texto):
                    self._cursor_pos += 1
                    
            else:
                # Escritura de caracteres visibles
                char = evento.unicode
                if char and char.isprintable() and len(self._texto) < self._max_longitud:
                    self._texto = self._texto[:self._cursor_pos] + char + self._texto[self._cursor_pos:]
                    self._cursor_pos += 1

            self._ajustar_scroll()
            # Reiniciamos el reloj de parpadeo para que el cursor sea visible al escribir/moverse
            self._mostrar_cursor = True
            self._ultimo_parpadeo = time.time()
            return True

        return False

    def dibujar(self, superficie):
        """Dibuja el fondo, el texto (o placeholder) y el cursor parpadeante."""
        if not self.visible:
            return

        # Dibujar fondo si fue provisto
        if self._img_fondo:
            superficie.blit(self._img_fondo, self.rect)

        # Padding (espaciado interno) para que el texto no se pegue a los bordes de la imagen
        pad_x = self.padding_x
        pad_y = self.padding_y if self.padding_y is not None else (self.alto - self._fuente.get_height()) // 2
        ancho_visible = self.ancho - pad_x - self.padding_right

        texto_render = self._texto
        color_render = self.color_texto

        # Mostrar placeholder si está vacío y no está escribiendo actualmente
        if len(self._texto) == 0 and not self._foco:
            texto_render = self._placeholder
            color_render = self.color_placeholder

        # Guardamos el clip original de la superficie
        clip_original = superficie.get_clip()
        
        # Aplicamos nuestro clip_rect para no dibujar fuera del espacio permitido (Scrolling)
        rect_visible = pygame.Rect(self.x + pad_x, self.y, ancho_visible, self.alto)
        if clip_original:
            rect_visible = rect_visible.clip(clip_original)
        superficie.set_clip(rect_visible)

        # Dibujar el texto final desplazado por el scroll
        if texto_render:
            superficie_texto = self._fuente.render(texto_render, True, color_render)
            superficie.blit(superficie_texto, (self.x + pad_x - self._scroll_x, self.y + pad_y))

        # Dibujar cursor si tiene foco y le toca ser mostrado
        if self._foco and self._mostrar_cursor:
            # Calcular ancho del texto hasta la posición actual del cursor
            texto_hasta_cursor = self._texto[:self._cursor_pos]
            ancho_hasta_cursor = 0
            if texto_hasta_cursor:
                ancho_hasta_cursor = self._fuente.render(texto_hasta_cursor, True, (0,0,0)).get_width()
                
            cursor_pantalla_x = self.x + pad_x + ancho_hasta_cursor - self._scroll_x
            pygame.draw.line(
                superficie, 
                self.color_cursor, 
                (cursor_pantalla_x, self.y + pad_y + 2), 
                (cursor_pantalla_x, self.y + pad_y + self._fuente.get_height() - 2), 
                2
            )
            
        # Restauramos el clip original para no romper el renderizado de los demás widgets
        superficie.set_clip(clip_original)
