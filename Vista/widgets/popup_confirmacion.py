#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# popup_confirmacion
#
# popup_confirmacion implementa PopupConfirmacion, un modal especializado para
# requerir confirmación por parte del jugador ante decisiones críticas (ej. reiniciar, salir).
# Dibuja un overlay oscuro semitransparente sobre toda la pantalla virtual.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PopupConfirmacion, clase del cuadro de diálogo de confirmación modal.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ manejar_evento, intercepta eventos bloqueando cualquier interacción de fondo
# @ dibujar, dibuja la capa de oscurecimiento trasera y el diálogo central
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame se usa para renderizar texto y el fondo oscurecido translúcido
from Vista.widgets.popup import Popup
# Popup es la clase base para el comportamiento modal contenedor
from Vista.widgets.boton import Boton
# Boton es el componente usado para las opciones de Confirmar y Cancelar
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class PopupConfirmacion(Popup):
    """
    Popup reutilizable para pedir confirmación al usuario.
    Oscurece el fondo completo (modal) y muestra botones de confirmar y cancelar.
    """
    def __init__(self, gestor_recursos, texto_pregunta, on_confirmar, on_cancelar=None, ruta_icono=None):
        # Configuramos el popup en el centro de la pantalla virtual (1920x1080)
        ancho_popup = 1000
        alto_popup = 650
        x_popup = (1920 - ancho_popup) // 2
        y_popup = (1080 - alto_popup) // 2
        
        super().__init__(
            x=x_popup, y=y_popup,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Popup.png",
            ancho=ancho_popup,
            alto=alto_popup
        )
        
        self.texto = texto_pregunta
        # Fuente más grande y clara para el mensaje
        self._fuente = pygame.font.Font(None, 64)
        self.on_cancelar = on_cancelar
        
        # Icono opcional centrado arriba del texto
        if ruta_icono:
            from Vista.widgets.imagen import Imagen
            ancho_ico = 150
            alto_ico = 150
            icono = Imagen(
                x=self.x + (self.ancho - ancho_ico) // 2,
                y=self.y + 100,
                ruta_imagen=ruta_icono,
                gestor_recursos=gestor_recursos,
                ancho=ancho_ico, alto=alto_ico,
                alpha=True
            )
            self.agregar_widget(icono)
        
        # Botón Confirmar (Abajo izquierda)
        btn_confirmar = Boton(
            x=self.x + 150, y=self.y + self.alto - 200,
            ruta_normal="Vista/resources/images/Confirm_Button_normal.png",
            ruta_hover="Vista/resources/images/Confirm_Button_hover.png",
            ruta_presionado="Vista/resources/images/Confirm_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=250, alto=120,
            on_click=on_confirmar
        )
        
        # Función interna para cancelar y cerrar el popup a la vez
        def _cancelar_interno():
            self.cerrar()
            if self.on_cancelar:
                self.on_cancelar()
                
        # Botón Cancelar (Abajo derecha)
        btn_cancelar = Boton(
            x=self.x + self.ancho - 250 - 150, y=self.y + self.alto - 200,
            ruta_normal="Vista/resources/images/Cancel_Button_normal.png",
            ruta_hover="Vista/resources/images/Cancel_Button_hover.png",
            ruta_presionado="Vista/resources/images/Cancel_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=250, alto=120,
            on_click=_cancelar_interno
        )
        
        # Botón Cerrar (Esquina superior derecha del popup)
        btn_cerrar = Boton(
            x=self.x + self.ancho - 110, y=self.y + 30,
            ruta_normal="Vista/resources/images/Close_Button_normal.png",
            ruta_hover="Vista/resources/images/Close_Button_hover.png",
            ruta_presionado="Vista/resources/images/Close_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=80, alto=80,
            on_click=_cancelar_interno
        )
        
        self.agregar_widget(btn_confirmar)
        self.agregar_widget(btn_cancelar)
        self.agregar_widget(btn_cerrar)

    def manejar_evento(self, evento):
        """Intercepta todos los eventos si está abierto (Comportamiento Modal)."""
        if not self.habilitado or not self.visible:
            return False

        # 1. Los botones hijos primero
        for hijo in reversed(self._hijos):
            if hijo.habilitado:
                consumido = hijo.manejar_evento(evento)
                if consumido:
                    return True

        # 2. Bloqueo Modal: Si hay click o movimiento de mouse, lo bloqueamos 
        # para que no pase a los botones que están en la Escena por detrás.
        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True

        return False

    def dibujar(self, superficie):
        """Dibuja el oscurecimiento y luego el popup en sí."""
        if not self.visible:
            return

        # 1. Capa de oscurecimiento (Sombra modal que cubre toda la pantalla de 1920x1080)
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160)) # Negro al 60% aprox
        superficie.blit(overlay, (0, 0))

        # 2. Dibujar fondo del popup y botones (comportamiento base de la clase Popup)
        super().dibujar(superficie)
        
        # 3. Dibujar el texto centrado
        if self.texto:
            superficie_texto = self._fuente.render(self.texto, True, (40, 20, 10))
            txt_rect = superficie_texto.get_rect(center=(self.x + self.ancho//2, self.y + self.alto//2 - 40))
            superficie.blit(superficie_texto, txt_rect)
