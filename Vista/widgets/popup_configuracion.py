import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton
from Vista.widgets.caja_texto import CajaTexto
from Vista.widgets.boton_volumen import BotonVolumen
from modelo.configuracion import ConfigManager

class PopupConfiguracion(Popup):
    """
    Popup para configurar API Key, proveedor de IA y volumen.
    """
    def __init__(self, gestor_recursos, on_cerrar=None):
        """
        Inicializa el modal de configuración general (API Keys, proveedores e interfaz de sonido).
        """
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
        self._fuente_titulo = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/Cinzel-Bold.ttf", 42)
        self._fuente_texto = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/MedievalSharp-Regular.ttf", 32)
        
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

        # 2. Caja de entrada de API Key (Arriba de los botones, perfectamente encuadrada)
        self.caja_api_key = CajaTexto(
            x=self.x + 550, y=self.y + 250,
            ancho=500, alto=60,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/BarratextoConfig.png",
            placeholder="API Key...",
            max_longitud=150
        )
        self.caja_api_key.color_texto = (255, 255, 255)
        self.caja_api_key.color_cursor = (255, 255, 255)
        self.caja_api_key.color_placeholder = (220, 220, 220)
        self.caja_api_key.color_borde = (0, 0, 0)
        self.caja_api_key.padding_x = 80
        self.caja_api_key.padding_right = 80
        self.caja_api_key.padding_y = 21
        self.agregar_widget(self.caja_api_key)

        # 3. Botón Gemini (Lado a lado)
        self.btn_gemini = Boton(
            x=self.x + 440, y=self.y + 340,
            ruta_normal="Vista/resources/images/Gemini.png",
            ruta_hover="Vista/resources/images/Gemini.png",
            ruta_presionado="Vista/resources/images/Gemini.png",
            gestor_recursos=gestor_recursos,
            ancho=340, alto=185,
            on_click=lambda: self._seleccionar_proveedor("gemini")
        )
        self.agregar_widget(self.btn_gemini)

        # 4. Botón Hugging Face (Lado a lado)
        self.btn_hf = Boton(
            x=self.x + 820, y=self.y + 340,
            ruta_normal="Vista/resources/images/HuggingFace.png",
            ruta_hover="Vista/resources/images/HuggingFace.png",
            ruta_presionado="Vista/resources/images/HuggingFace.png",
            gestor_recursos=gestor_recursos,
            ancho=340, alto=185,
            on_click=lambda: self._seleccionar_proveedor("huggingface")
        )
        self.agregar_widget(self.btn_hf)

        # 5. Botón de volumen
        self.btn_volumen = BotonVolumen(
            x=self.x + 480, y=self.y + 560,
            ancho=70, alto=70,
            gestor_recursos=gestor_recursos
        )
        self.agregar_widget(self.btn_volumen)

        # 6. Botón de Gestionar Modelos Locales (usando el asset gráfico Gestionar_modelos.png)
        self.btn_gestionar_modelos = Boton(
            x=self.x + 630, y=self.y + 510,
            ruta_normal="Vista/resources/images/Gestionar_modelos.png",
            ruta_hover="Vista/resources/images/Gestionar_modelos.png",
            ruta_presionado="Vista/resources/images/Gestionar_modelos.png",
            gestor_recursos=gestor_recursos,
            ancho=340, alto=174,
            on_click=self._abrir_popup_modelos
        )
        self.agregar_widget(self.btn_gestionar_modelos)

        # 7. Botón Guardar
        btn_guardar = Boton(
            x=self.x + 725, y=self.y + 715,
            ruta_normal="Vista/resources/images/Confirm_Button_normal.png",
            ruta_hover="Vista/resources/images/Confirm_Button_hover.png",
            ruta_presionado="Vista/resources/images/Confirm_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=150, alto=80,
            on_click=self._guardar
        )
        self.agregar_widget(btn_guardar)
        
        self.popup_modelos = None

        # Cargar la API Key inicial según el proveedor activo
        self._cargar_key_proveedor_activo()

    def _cargar_key_proveedor_activo(self):
        """Carga en la caja de texto la clave de API correspondiente al proveedor seleccionado."""
        prov = self.config.get_proveedor_imagen()
        if prov == "gemini":
            key = self.config.get_gemini_key()
            self.caja_api_key.placeholder = "Gemini API Key..."
        else:
            key = self.config.get_huggingface_key()
            self.caja_api_key.placeholder = "HuggingFace API Key..."
        self.caja_api_key.texto = key

    def _guardar_key_actual(self):
        """Persiste en la configuración la API Key ingresada en la caja de texto para el proveedor activo."""
        prov = self.config.get_proveedor_imagen()
        key = self.caja_api_key.texto.strip()
        if prov == "gemini":
            self.config.set_gemini_key(key)
        else:
            self.config.set_huggingface_key(key)

    def _seleccionar_proveedor(self, proveedor):
        """Cambia el proveedor de imagen activo ('gemini' o 'huggingface') y actualiza la clave en la caja."""
        self._guardar_key_actual()
        self.config.set_proveedor_imagen(proveedor)
        self._cargar_key_proveedor_activo()

    def _abrir_popup_modelos(self):
        """Abre el sub-modal de selección y descarga de modelos locales de Ollama."""
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
        """Restaura la visibilidad de los widgets de configuración tras cerrar el sub-modal de modelos."""
        for hijo in self._hijos:
            if hijo != self.popup_modelos:
                hijo.visible = True

    def _guardar(self):
        """Guarda permanentemente las modificaciones en config.json y cierra el modal."""
        self._guardar_key_actual()
        self.config.guardar_config()
        self._cerrar_interno()

    def _cerrar_interno(self):
        """Cierra el popup de configuración e invoca el callback de cierre."""
        self.cerrar()
        if self.on_cerrar:
            self.on_cerrar()

    def manejar_evento(self, evento):
        """Captura eventos del ratón y teclado bloqueando la interacción con la pantalla trasera."""
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
        """Dibuja el marco de configuración, opciones, entradas y resaltado del proveedor activo."""
        if not self.visible:
            return

        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        superficie.blit(overlay, (0, 0))

        super().dibujar(superficie)

        # Si el popup de modelos está abierto, no dibujamos nuestros textos
        if self.popup_modelos and self.popup_modelos.visible:
            return

        # Dibujar marco de selección sobre el botón activo
        proveedor_actual = self.config.get_proveedor_imagen()
        btn_activo = self.btn_gemini if proveedor_actual == "gemini" else self.btn_hf
        rect_seleccion = btn_activo.rect.inflate(8, 8)
        pygame.draw.rect(superficie, (255, 215, 0), rect_seleccion, width=4, border_radius=12)


