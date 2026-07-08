import pygame
from Vista.widgets.widget import Widget

class BotonVolumen(Widget):
    """
    Botón interactivo que controla el volumen general de la aplicación.
    Tiene tres estados: alto, bajo, mute.
    Al hacer clic, cicla entre los estados y ajusta la música y los efectos de sonido.
    """
    def __init__(self, x, y, ancho, alto, gestor_recursos):
        super().__init__(x, y, ancho, alto)
        self.gestor_recursos = gestor_recursos
        self.estados = ["100", "75", "50", "25", "0"]
        self.indice_estado = 0
        
        self.color_fondo = (30, 20, 10)     # Marrón oscuro (estilo madera/cuero)
        self.color_icono = (200, 180, 140)  # Dorado claro/pergamino
        self.color_hover = (60, 50, 40)     # Marrón más claro al pasar el mouse
        self.hover = False
        self._mouse_presionado = False

    def manejar_evento(self, evento):
        if not self.habilitado or not self.visible:
            return False

        if evento.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(evento.pos):
                if not self.hover:
                    self.hover = True
                    # Opcional: sonido de hover
                    snd_hover = self.gestor_recursos.obtener_sonido("Vista/resources/sounds/hover.wav")
                    if snd_hover:
                        snd_hover.play()
            else:
                self.hover = False
                self._mouse_presionado = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1 and self.rect.collidepoint(evento.pos):
                self._mouse_presionado = True
                return True

        elif evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1 and self._mouse_presionado:
                self._mouse_presionado = False
                if self.rect.collidepoint(evento.pos):
                    # Opcional: sonido de click
                    snd_click = self.gestor_recursos.obtener_sonido("Vista/resources/sounds/click.wav")
                    if snd_click:
                        snd_click.play()
                    self._cambiar_estado()
                    return True

        return False

    def _cambiar_estado(self):
        # Ciclar el estado
        self.indice_estado = (self.indice_estado + 1) % len(self.estados)
        estado = self.estados[self.indice_estado]
        
        if estado == "100":
            volumen_sfx = 1.0
            volumen_music = 0.20 # Volumen base configurado originalmente
        elif estado == "75":
            volumen_sfx = 0.75
            volumen_music = 0.15
        elif estado == "50":
            volumen_sfx = 0.50
            volumen_music = 0.10
        elif estado == "25":
            volumen_sfx = 0.25
            volumen_music = 0.05
        else: # "0"
            volumen_sfx = 0.0
            volumen_music = 0.0
            
        # Actualizar música (si está cargada y sonando)
        pygame.mixer.music.set_volume(volumen_music)
        
        # Actualizar efectos de sonido a través del gestor
        self.gestor_recursos.set_volumen_general(volumen_sfx)

    def dibujar(self, superficie):
        if not self.visible:
            return
            
        color_bg = self.color_hover if self.hover else self.color_fondo
        
        # Dibujar fondo con esquinas redondeadas
        pygame.draw.rect(superficie, color_bg, self.rect, border_radius=8)
        # Borde
        pygame.draw.rect(superficie, self.color_icono, self.rect, 2, border_radius=8)
        
        # Centro geométrico del botón
        cx = self.rect.x + self.ancho // 2
        cy = self.rect.y + self.alto // 2
        
        # --- Dibujar ícono de parlante (speaker) ---
        # Base del parlante (cuadradito)
        base_rect = pygame.Rect(cx - 10, cy - 5, 6, 10)
        pygame.draw.rect(superficie, self.color_icono, base_rect)
        
        # Cono del parlante (polígono)
        puntos_cono = [
            (cx - 4, cy - 5),
            (cx - 4, cy + 5),
            (cx + 4, cy + 12),
            (cx + 4, cy - 12)
        ]
        pygame.draw.polygon(superficie, self.color_icono, puntos_cono)
        
        # --- Dibujar ondas/estados ---
        estado = self.estados[self.indice_estado]
        
        if estado == "100":
            pygame.draw.arc(superficie, self.color_icono, (cx, cy - 8, 16, 16), -1.2, 1.2, 2)
            pygame.draw.arc(superficie, self.color_icono, (cx - 4, cy - 14, 28, 28), -1.0, 1.0, 2)
            pygame.draw.arc(superficie, self.color_icono, (cx - 8, cy - 20, 40, 40), -0.8, 0.8, 2)
        elif estado == "75":
            pygame.draw.arc(superficie, self.color_icono, (cx, cy - 8, 16, 16), -1.2, 1.2, 2)
            pygame.draw.arc(superficie, self.color_icono, (cx - 4, cy - 14, 28, 28), -1.0, 1.0, 2)
        elif estado == "50":
            pygame.draw.arc(superficie, self.color_icono, (cx, cy - 8, 16, 16), -1.2, 1.2, 2)
        elif estado == "25":
            pygame.draw.arc(superficie, self.color_icono, (cx, cy - 5, 10, 10), -1.0, 1.0, 2)
        elif estado == "0":
            color_mute = (200, 60, 60)
            px = cx + 8
            pygame.draw.line(superficie, color_mute, (px, cy - 6), (px + 10, cy + 4), 3)
            pygame.draw.line(superficie, color_mute, (px + 10, cy - 6), (px, cy + 4), 3)
