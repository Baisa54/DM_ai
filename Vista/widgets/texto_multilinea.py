import pygame
from Vista.widgets.widget import Widget

class TextoMultilinea(Widget):
    """
    Widget para mostrar texto largo en múltiples líneas con auto-wrap y scroll vertical.
    """
    def __init__(self, x, y, ancho, alto, gestor_recursos, fuente_ruta=None, fuente_tamano=28, color_texto=(30, 20, 10)):
        super().__init__(x, y, ancho, alto)
        self._gestor_recursos = gestor_recursos
        self._fuente = self._gestor_recursos.obtener_fuente(fuente_ruta, fuente_tamano)
        if not self._fuente:
            self._fuente = pygame.font.Font(None, fuente_tamano)
            
        self.color_texto = color_texto
        self._texto = ""
        self._lineas_renderizadas = []
        self._superficie_completa = None
        self._scroll_y = 0
        self._alto_total_texto = 0
        
        self.padding_x = 40
        self.padding_y = 40

    @property
    def texto(self):
        return self._texto

    @texto.setter
    def texto(self, valor):
        self._texto = str(valor)
        self._renderizar_texto()

    def _renderizar_texto(self):
        """Divide el texto en líneas que quepan en el ancho y pre-renderiza la superficie."""
        if not self._texto:
            self._superficie_completa = None
            self._alto_total_texto = 0
            self._scroll_y = 0
            return

        palabras = self._texto.split(" ")
        lineas = []
        linea_actual = ""
        
        ancho_maximo = self.ancho - (self.padding_x * 2)

        # Procesar los saltos de línea explícitos y el wrap
        for p in palabras:
            if '\n' in p:
                partes = p.split('\n')
                for i, parte in enumerate(partes):
                    test_linea = linea_actual + parte + " "
                    if self._fuente.size(test_linea)[0] <= ancho_maximo:
                        linea_actual = test_linea
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = parte + " "
                    if i < len(partes) - 1:
                        lineas.append(linea_actual)
                        linea_actual = ""
            else:
                test_linea = linea_actual + p + " "
                if self._fuente.size(test_linea)[0] <= ancho_maximo:
                    linea_actual = test_linea
                else:
                    if linea_actual:
                        lineas.append(linea_actual)
                    linea_actual = p + " "
                    
        if linea_actual:
            lineas.append(linea_actual)

        # Calcular alto total
        alto_linea = self._fuente.get_linesize()
        self._alto_total_texto = len(lineas) * alto_linea

        # Crear la superficie completa (con canal alpha transparente)
        self._superficie_completa = pygame.Surface((self.ancho - (self.padding_x * 2), max(self._alto_total_texto, self.alto)), pygame.SRCALPHA)
        
        y_offset = 0
        color_borde = (255, 255, 255) # Blanco
        offset = 1
        
        for linea in lineas:
            texto_limpio = linea.strip()
            if texto_limpio:
                # Dibujar borde (4 direcciones)
                borde = self._fuente.render(texto_limpio, True, color_borde)
                self._superficie_completa.blit(borde, (-offset, y_offset))
                self._superficie_completa.blit(borde, (offset, y_offset))
                self._superficie_completa.blit(borde, (0, y_offset - offset))
                self._superficie_completa.blit(borde, (0, y_offset + offset))
                
                # Dibujar texto original
                superficie_texto = self._fuente.render(texto_limpio, True, self.color_texto)
                self._superficie_completa.blit(superficie_texto, (0, y_offset))
            
            y_offset += alto_linea
            
        self._scroll_y = 0

    def manejar_evento(self, evento):
        if not self.visible or not self.habilitado:
            return False

        # Manejo de scroll si el cursor está sobre la caja
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            cambio_scroll = 0
            if evento.type == pygame.MOUSEWHEEL:
                # Usar precise_y si está disponible para touchpads suaves (Pygame 2)
                y_val = getattr(evento, 'precise_y', evento.y)
                # Si es touchpad el valor puede ser decimal muy chico, lo multiplicamos
                cambio_scroll = -y_val * 40
                
                # Si el sistema solo arroja valores de rueda normales, garantizamos movimiento
                if cambio_scroll == 0 and evento.y != 0:
                    cambio_scroll = -evento.y * 40
                    
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 4: # Scroll Up
                    cambio_scroll = -40
                elif evento.button == 5: # Scroll Down
                    cambio_scroll = 40

            if cambio_scroll != 0:
                self._scroll_y += cambio_scroll
                
                # Limitar el scroll
                max_scroll = max(0, self._alto_total_texto - (self.alto - (self.padding_y * 2)))
                self._scroll_y = max(0, min(self._scroll_y, max_scroll))
                return True
                
        return False

    def dibujar(self, superficie):
        if not self.visible or not self._superficie_completa:
            return

        # Guardar clip original
        clip_original = superficie.get_clip()
        
        # Clip interior de la caja de texto
        rect_visible = pygame.Rect(self.x + self.padding_x, self.y + self.padding_y, 
                                   self.ancho - (self.padding_x * 2), 
                                   self.alto - (self.padding_y * 2))
                                   
        if clip_original:
            rect_visible = rect_visible.clip(clip_original)
            
        superficie.set_clip(rect_visible)

        # Dibujar la superficie de texto con el offset de scroll
        area_a_dibujar = pygame.Rect(0, self._scroll_y, 
                                     self.ancho - (self.padding_x * 2), 
                                     self.alto - (self.padding_y * 2))
                                     
        superficie.blit(self._superficie_completa, (self.x + self.padding_x, self.y + self.padding_y), area_a_dibujar)

        # Restaurar clip
        superficie.set_clip(clip_original)
