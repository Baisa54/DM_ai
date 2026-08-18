import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton

class PopupAlerta(Popup):
    def __init__(self, gestor_recursos, texto_alerta, on_cerrar=None):
        """
        Inicializa un popup modal de alerta informativo.
        """
        ancho_popup = 800
        alto_popup = 500
        x_popup = (1920 - ancho_popup) // 2
        y_popup = (1080 - alto_popup) // 2
        
        super().__init__(
            x=x_popup, y=y_popup,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Popup.png",
            ancho=ancho_popup,
            alto=alto_popup
        )
        self.texto = texto_alerta
        self._fuente = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/MedievalSharp-Regular.ttf", 44)
        self.on_cerrar = on_cerrar
        
        def _cerrar_interno():
            """Cierra el popup de alerta e invoca el callback on_cerrar si está definido."""
            self.cerrar()
            if self.on_cerrar:
                self.on_cerrar()
                
        btn_cerrar_rojo = Boton(
            x=self.x + (self.ancho - 250) // 2, y=self.y + self.alto - 180,
            ruta_normal="Vista/resources/images/Cancel_Button_normal.png",
            ruta_hover="Vista/resources/images/Cancel_Button_hover.png",
            ruta_presionado="Vista/resources/images/Cancel_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=250, alto=120,
            on_click=_cerrar_interno
        )
        self.agregar_widget(btn_cerrar_rojo)
        
    def manejar_evento(self, evento):
        """
        Intercepta eventos y bloquea clicks sobre la capa de fondo.
        """
        if not self.habilitado or not self.visible:
            return False
        for hijo in reversed(self._hijos):
            if hijo.habilitado:
                if hijo.manejar_evento(evento): return True
        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True
        return False

    def dibujar(self, superficie):
        """
        Dibuja el overlay semitransparente, el contenedor modal y el mensaje de alerta.
        """
        if not self.visible: return
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        superficie.blit(overlay, (0, 0))
        super().dibujar(superficie)
        if self.texto:
            lineas = self.texto.split('\n')
            y_base = self.y + self.alto//2 - 40 - (len(lineas)*20)
            for linea in lineas:
                rnd = self._fuente.render(linea, True, (150, 30, 30))
                txt_rect = rnd.get_rect(center=(self.x + self.ancho//2, y_base))
                superficie.blit(rnd, txt_rect)
                y_base += 40
