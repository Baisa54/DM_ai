import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton
from modelo.configuracion import ConfigManager
from modelo.ai.ollama_manager import OllamaManager
from Vista.widgets.popup_confirmacion import PopupConfirmacion

class PopupModelos(Popup):
    def __init__(self, gestor_recursos, on_cerrar=None):
        """
        Inicializa el modal de gestión y descarga de modelos locales de Ollama.
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
        self.ollama = OllamaManager()
        self.ram_sistema = self.ollama.obtener_ram_gb()
        self.modelos_instalados = self.ollama.obtener_modelos_instalados()
        
        self._fuente_titulo = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/Cinzel-Bold.ttf", 42)
        self._fuente_texto = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/MedievalSharp-Regular.ttf", 28)
        self._fuente_chica = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/MedievalSharp-Regular.ttf", 22)
        
        # Botón Cerrar
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

        # Crear botones para los modelos
        self.botones_accion = []
        card_w = 840
        card_h = 92
        card_gap = 105
        y_start = self.y + 260
        bx_base = self.x + (self.ancho - card_w) // 2
        
        for idx, mod in enumerate(OllamaManager.MODELOS_DISPONIBLES):
            bx = bx_base + card_w - 170
            by = y_start + (idx * card_gap) + 12
            
            btn = Boton(
                x=bx, y=by,
                ruta_normal="Vista/resources/images/Input_Box.png",
                ruta_hover="Vista/resources/images/Input_Box.png",
                ruta_presionado="Vista/resources/images/Input_Box.png",
                gestor_recursos=gestor_recursos,
                ancho=150, alto=50,
                on_click=lambda m=mod: self._on_click_modelo(m)
            )
            self.botones_accion.append(btn)
            self.agregar_widget(btn)

        self.popup_confirmacion = None

    def _cerrar_interno(self):
        """Cierra el popup de modelos siempre que no haya una descarga en curso."""
        if self.ollama.descarga_activa:
            # No permitir cerrar si está descargando
            return
            
        self.cerrar()
        if self.on_cerrar:
            self.on_cerrar()

    def _on_click_modelo(self, modelo):
        """Maneja el clic en un modelo para seleccionarlo como activo o iniciar su descarga con confirmación."""
        if self.ollama.descarga_activa:
            return

        is_installed = False
        for inst in self.modelos_instalados:
            if modelo["id"] in inst:
                is_installed = True
                break
                
        if is_installed:
            self.config.set_modelo_local(modelo["id"])
            self.config.guardar_config()
        else:
            # Advertencia de requisitos
            if self.ram_sistema < modelo["ram_req"]:
                msg = f"Tu PC tiene {self.ram_sistema:.1f}GB RAM. Se recomiendan {modelo['ram_req']}GB para {modelo['nombre']}.\n" \
                      f"Si lo descargas, tu PC podría congelarse o fallar.\n¿Descargar de todos modos?"
                
                self.popup_confirmacion = PopupConfirmacion(
                    gestor_recursos=self._gestor_recursos,
                    texto_pregunta=msg,
                    on_confirmar=lambda: self._iniciar_descarga(modelo["id"])
                )
                self.agregar_widget(self.popup_confirmacion)
                self.popup_confirmacion.abrir()
            else:
                self._iniciar_descarga(modelo["id"])

    def _iniciar_descarga(self, modelo_id):
        """Inicia el proceso de descarga de un modelo en segundo plano."""
        if self.popup_confirmacion:
            self.popup_confirmacion.cerrar()
            self.popup_confirmacion = None
            
        self.ollama.iniciar_descarga(modelo_id)

    def manejar_evento(self, evento):
        """Procesa los eventos impidiendo la propagación a la pantalla trasera."""
        if not self.habilitado or not self.visible:
            return False

        for hijo in reversed(self._hijos):
            if hijo.habilitado and hijo.visible:
                if hijo.manejar_evento(evento):
                    return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True

        return False

    def dibujar(self, superficie):
        """Dibuja la burbuja superior de estado, la lista de modelos locales y la barra de progreso de descarga."""
        if not self.visible:
            return

        super().dibujar(superficie)
        
        # Si la descarga terminó exitosamente y no estamos actualizando la lista:
        if not self.ollama.descarga_activa and self.ollama.progreso_actual == 100.0:
            self.modelos_instalados = self.ollama.obtener_modelos_instalados()
            self.ollama.progreso_actual = 0.0 # reset para no loopear
        
        color_texto = (40, 20, 10)
        color_alerta = (200, 50, 50)
        color_ok = (50, 150, 50)
        
        # -----------------------------------------------------------------
        # Burbuja de Información Superior (Fuera del recuadro, arriba de todo)
        # -----------------------------------------------------------------
        bw, bh = 1100, 75
        bx = (1920 - bw) // 2
        by = 15

        bubble = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(bubble, (30, 20, 15, 235), (0, 0, bw, bh), border_radius=15)
        pygame.draw.rect(bubble, (212, 175, 55), (0, 0, bw, bh), width=3, border_radius=15)
        superficie.blit(bubble, (bx, by))

        modelo_actual = self.config.get_modelo_local()
        txt_ram = self._fuente_texto.render(f"RAM Detectada: {self.ram_sistema:.1f} GB", True, (240, 230, 210))
        txt_sep = self._fuente_texto.render("  |  ", True, (160, 140, 100))
        txt_act = self._fuente_texto.render(f"Modelo Activo: {modelo_actual}", True, (100, 220, 100))

        superficie.blit(txt_ram, (bx + 30, by + 10))
        superficie.blit(txt_sep, (bx + 30 + txt_ram.get_width(), by + 10))
        superficie.blit(txt_act, (bx + 30 + txt_ram.get_width() + txt_sep.get_width(), by + 10))

        if not hasattr(self.ollama, 'servidor_ollama_activo') or not self.ollama.servidor_ollama_activo:
            txt_warn = self._fuente_chica.render("¡AVISO: Servidor Ollama no detectado! Ábrelo para conectar o descargar modelos.", True, (255, 120, 120))
        else:
            txt_warn = self._fuente_chica.render("Servidor Ollama: Conectado y listo.", True, (120, 220, 120))
        superficie.blit(txt_warn, (bx + 30, by + 42))

        # -----------------------------------------------------------------
        # Lista de modelos (Dentro del marco del popup, perfectamente centrada)
        # -----------------------------------------------------------------
        card_w = 840
        card_h = 92
        card_gap = 105
        y_start = self.y + 260
        bx_base = self.x + (self.ancho - card_w) // 2
        modelo_actual = self.config.get_modelo_local()

        for idx, mod in enumerate(OllamaManager.MODELOS_DISPONIBLES):
            bx = bx_base
            by = y_start + (idx * card_gap)
            
            # Dibujar tarjeta blanca redondeada
            pygame.draw.rect(superficie, (245, 238, 220), (bx, by, card_w, card_h), border_radius=12)
            pygame.draw.rect(superficie, (180, 150, 110), (bx, by, card_w, card_h), 2, border_radius=12)
            
            # Nombre y Requisito
            txt_nom = self._fuente_texto.render(mod["nombre"], True, color_texto)
            superficie.blit(txt_nom, (bx + 20, by + 12))
            
            req_color = color_ok if self.ram_sistema >= mod["ram_req"] else color_alerta
            txt_req = self._fuente_chica.render(f"Requiere: {mod['ram_req']} GB RAM", True, req_color)
            superficie.blit(txt_req, (bx + 240, by + 16))
            
            # Descripción
            txt_desc = self._fuente_chica.render(mod["desc"], True, (100, 80, 60))
            superficie.blit(txt_desc, (bx + 20, by + 48))
            
            # Estado (Instalado o No)
            is_installed = False
            for inst in self.modelos_instalados:
                if mod["id"] in inst:
                    is_installed = True
                    break
                    
            if is_installed:
                if modelo_actual == mod["id"]:
                    txt_btn = self._fuente_texto.render("ACTIVO", True, color_ok)
                else:
                    txt_btn = self._fuente_texto.render("Seleccionar", True, color_texto)
            else:
                txt_btn = self._fuente_texto.render("Descargar", True, color_texto)
                
            # Render texto sobre el botón correspondiente
            btn = self.botones_accion[idx]
            cx = btn.x + (btn.ancho - txt_btn.get_width()) // 2
            cy = btn.y + (btn.alto - txt_btn.get_height()) // 2
            superficie.blit(txt_btn, (cx, cy))
            
        # Barra de descarga
        if self.ollama.descarga_activa:
            # Oscurecer todo (Modal interno)
            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            superficie.blit(overlay, (self.x, self.y))
            
            # Dibujar barra
            bx = self.x + 200
            by = self.y + self.alto // 2
            bw = 700
            bh = 40
            
            # Contorno
            pygame.draw.rect(superficie, (255, 255, 255), (bx, by, bw, bh), 2)
            # Relleno
            fill_w = int(bw * (self.ollama.progreso_actual / 100.0))
            pygame.draw.rect(superficie, (100, 200, 100), (bx + 2, by + 2, fill_w - 4, bh - 4))
            
            # Texto estado
            txt_estado = self._fuente_texto.render(self.ollama.estado_descarga, True, (255, 255, 255))
            superficie.blit(txt_estado, (bx, by - 30))
            
            # Porcentaje
            txt_pct = self._fuente_texto.render(f"{self.ollama.progreso_actual:.1f}%", True, (0, 0, 0))
            superficie.blit(txt_pct, (bx + bw//2 - 20, by + 10))
            
        elif self.ollama.error_descarga:
            txt_err = self._fuente_texto.render(f"Error: {self.ollama.error_descarga}", True, color_alerta)
            superficie.blit(txt_err, (self.x + 120, self.y + 700))
