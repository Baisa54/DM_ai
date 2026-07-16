import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton
from Vista.widgets.caja_texto import CajaTexto
from Vista.widgets.boton_volumen import BotonVolumen
from modelo.configuracion import ConfigManager

class PopupConfiguracion(Popup):
    """
    Popup para configurar las API keys y el volumen.
    """
    def __init__(self, gestor_recursos, on_cerrar=None):
        ancho_popup = 1600
        alto_popup = 900
        x_popup = (1920 - ancho_popup) // 2
        y_popup = (1080 - alto_popup) // 2
        
        super().__init__(
            x=x_popup, y=y_popup,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Popup_config.png",
            ancho=ancho_popup,
            alto=alto_popup
        )
        
        self.on_cerrar = on_cerrar
        self.config = ConfigManager()
        self._fuente_titulo = pygame.font.Font(None, 42)
        self._fuente_texto = pygame.font.Font(None, 32)
        
        # 1. Botón Cerrar
        btn_cerrar = Boton(
            x=self.x + self.ancho - 110, y=self.y + 30,
            ruta_normal="Vista/resources/images/Close_Button_normal.png",
            ruta_hover="Vista/resources/images/Close_Button_hover.png",
            ruta_presionado="Vista/resources/images/Close_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=80, alto=80,
            on_click=self._cerrar_interno
        )
        self.agregar_widget(btn_cerrar)
        # 2. Caja Gemini
        self.caja_gemini = CajaTexto(
            x=self.x + 550, y=self.y + 340,
            ancho=500, alto=60,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/BarratextoConfig.png",
            placeholder="Gemini API Key...",
            max_longitud=100
        )
        self.caja_gemini.color_texto = (255, 255, 255)
        self.caja_gemini.color_cursor = (255, 255, 255)
        self.caja_gemini.color_placeholder = (255, 255, 255)
        self.caja_gemini.color_borde = (0, 0, 0)
        self.caja_gemini.padding_x = 100
        self.caja_gemini.padding_right = 100
        # 2.1 Setear si ya existe
        self.caja_gemini.texto = self.config.get_gemini_key()
        self.agregar_widget(self.caja_gemini)

        # 3. Caja HuggingFace
        self.caja_hf = CajaTexto(
            x=self.x + 550, y=self.y + 440,
            ancho=500, alto=60,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/BarratextoConfig.png",
            placeholder="HuggingFace API Key...",
            max_longitud=100
        )
        self.caja_hf.color_texto = (255, 255, 255)
        self.caja_hf.color_cursor = (255, 255, 255)
        self.caja_hf.color_placeholder = (255, 255, 255)
        self.caja_hf.color_borde = (0, 0, 0)
        self.caja_hf.padding_x = 100
        self.caja_hf.padding_right = 100
        self.caja_hf.texto = self.config.get_huggingface_key()
        self.agregar_widget(self.caja_hf)

        # 4. Botón de volumen
        self.btn_volumen = BotonVolumen(
            x=self.x + 600, y=self.y + 540,
            ancho=80, alto=80,
            gestor_recursos=gestor_recursos
        )
        self.agregar_widget(self.btn_volumen)

        # 4.5. Botón Toggle de Proveedor de Imagen
        self.btn_proveedor = Boton(
            x=self.x + 750, y=self.y + 540,
            ruta_normal="Vista/resources/images/Input_Box.png",
            ruta_hover="Vista/resources/images/Input_Box.png",
            ruta_presionado="Vista/resources/images/Input_Box.png",
            gestor_recursos=gestor_recursos,
            ancho=250, alto=80,
            on_click=self._toggle_proveedor
        )
        self.agregar_widget(self.btn_proveedor)
        
        # 4.6 Botón de Gestionar Modelos Locales
        self.btn_gestionar_modelos = Boton(
            x=self.x + 600, y=self.y + 640,
            ruta_normal="Vista/resources/images/Input_Box.png",
            ruta_hover="Vista/resources/images/Input_Box.png",
            ruta_presionado="Vista/resources/images/Input_Box.png",
            gestor_recursos=gestor_recursos,
            ancho=400, alto=60,
            on_click=self._abrir_popup_modelos
        )
        self.agregar_widget(self.btn_gestionar_modelos)

        # 5. Botón Guardar
        btn_guardar = Boton(
            x=self.x + 725, y=self.y + 740,
            ruta_normal="Vista/resources/images/Confirm_Button_normal.png",
            ruta_hover="Vista/resources/images/Confirm_Button_hover.png",
            ruta_presionado="Vista/resources/images/Confirm_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=150, alto=80,
            on_click=self._guardar
        )
        self.agregar_widget(btn_guardar)
        
        self.popup_modelos = None

    def _abrir_popup_modelos(self):
        from Vista.widgets.popup_modelos import PopupModelos
        if not self.popup_modelos:
            self.popup_modelos = PopupModelos(self._gestor_recursos, on_cerrar=self._on_modelos_cerrado)
            self.agregar_widget(self.popup_modelos)
        
        # Ocultar todos los demás widgets para que no se superpongan
        for hijo in self._hijos:
            if hijo != self.popup_modelos:
                hijo.visible = False
                
        self.popup_modelos.abrir()

    def _on_modelos_cerrado(self):
        # Restaurar visibilidad de los widgets
        for hijo in self._hijos:
            if hijo != self.popup_modelos:
                hijo.visible = True

    def _toggle_proveedor(self):
        actual = self.config.get_proveedor_imagen()
        nuevo = "gemini" if actual == "huggingface" else "huggingface"
        self.config.set_proveedor_imagen(nuevo)

    def _guardar(self):
        self.config.set_gemini_key(self.caja_gemini.texto.strip())
        self.config.set_huggingface_key(self.caja_hf.texto.strip())
        self.config.guardar_config()
        self._cerrar_interno()

    def _cerrar_interno(self):
        self.cerrar()
        if self.on_cerrar:
            self.on_cerrar()

    def manejar_evento(self, evento):
        if not self.habilitado or not self.visible:
            return False

        for hijo in reversed(self._hijos):
            if hijo.habilitado:
                if hijo.manejar_evento(evento):
                    return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True

        return False

    def dibujar(self, superficie):
        if not self.visible:
            return

        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        superficie.blit(overlay, (0, 0))

        super().dibujar(superficie)

        # Si el popup de modelos está abierto, no dibujamos nuestros textos
        if self.popup_modelos and self.popup_modelos.visible:
            return

        # Dibujar el texto del proveedor actual sobre el botón
        color_texto = (40, 20, 10)
        proveedor_actual = self.config.get_proveedor_imagen()
        txt_prov = self._fuente_texto.render(proveedor_actual.upper(), True, color_texto)
        cx = self.btn_proveedor.x + (self.btn_proveedor.ancho - txt_prov.get_width()) // 2
        cy = self.btn_proveedor.y + (self.btn_proveedor.alto - txt_prov.get_height()) // 2
        superficie.blit(txt_prov, (cx, cy))

        # Dibujar el texto del botón Gestionar Modelos
        txt_gest = self._fuente_texto.render("Gestionar Modelos Locales", True, color_texto)
        cx_g = self.btn_gestionar_modelos.x + (self.btn_gestionar_modelos.ancho - txt_gest.get_width()) // 2
        cy_g = self.btn_gestionar_modelos.y + (self.btn_gestionar_modelos.alto - txt_gest.get_height()) // 2
        superficie.blit(txt_gest, (cx_g, cy_g))
