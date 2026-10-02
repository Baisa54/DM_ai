import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton
from modelo.configuracion import ConfigManager
from modelo.ai.ollama_manager import OllamaManager
from Vista.widgets.popup_confirmacion import PopupConfirmacion
from Vista.widgets.dashboard_exposicion import DashboardExposicion

class PopupModelos(Popup):
    def __init__(self, gestor_recursos, on_cerrar=None):
        """
        Inicializa el modal de gestión y descarga de modelos locales de Ollama,
        e integra el botón especial para abrir el Dashboard de Exposición CACIC (ChatGPT).
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
        self._fuente_boton = self._gestor_recursos.obtener_fuente("Vista/resources/fuentes/Cinzel-Bold.ttf", 22)
        
        # Botón Cerrar original
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

        # Crear botones para los modelos locales
        self.botones_accion = []
        card_w = 840
        card_h = 92
        card_gap = 105
        y_start = self.y + 245
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

        # Botón moderno propio para abrir el Dashboard de Exposición
        btn_exp_w = 440
        btn_exp_h = 52
        self.rect_btn_exposicion = pygame.Rect(
            self.x + (self.ancho - btn_exp_w) // 2,
            self.y + 695,
            btn_exp_w,
            btn_exp_h
        )
        self.hover_btn_exposicion = False

        # Dashboard Full-Screen (1920x1080)
        self.dashboard_exposicion = DashboardExposicion(gestor_recursos, on_cerrar=self._on_dashboard_cerrado)

    def _on_dashboard_cerrado(self):
        """Callback al cerrar el dashboard full-screen."""
        pass

    def _cerrar_interno(self):
        """Cierra el popup de modelos siempre que no haya una descarga en curso."""
        if self.ollama.descarga_activa:
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
            self.config.set_proveedor_texto("ollama")
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

        # Si el dashboard web full-screen está activo, consume todos los eventos
        if self.dashboard_exposicion and self.dashboard_exposicion.visible:
            return self.dashboard_exposicion.manejar_evento(evento)

        # Confirmación modal interna
        if self.popup_confirmacion and self.popup_confirmacion.visible:
            return self.popup_confirmacion.manejar_evento(evento)

        # Hover y Clic del botón custom de Exposición
        if evento.type == pygame.MOUSEMOTION:
            self.hover_btn_exposicion = self.rect_btn_exposicion.collidepoint(evento.pos)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_btn_exposicion.collidepoint(evento.pos):
                self.dashboard_exposicion.abrir()
                return True

        for hijo in reversed(self._hijos):
            if hijo.habilitado and hijo.visible:
                if hijo.manejar_evento(evento):
                    return True

        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True

        return False

    def dibujar(self, superficie):
        """Dibuja el modal de modelos locales o el Dashboard Full-Screen si fue invocado."""
        if not self.visible:
            return

        # Si el dashboard de exposición está abierto, cubre toda la pantalla (1920x1080)
        if self.dashboard_exposicion and self.dashboard_exposicion.visible:
            self.dashboard_exposicion.dibujar(superficie)
            return

        super().dibujar(superficie)
        
        # Si la descarga terminó exitosamente y no estamos actualizando la lista:
        if not self.ollama.descarga_activa and self.ollama.progreso_actual == 100.0:
            self.modelos_instalados = self.ollama.obtener_modelos_instalados()
            self.ollama.progreso_actual = 0.0
        
        color_texto = (40, 20, 10)
        color_alerta = (200, 50, 50)
        color_ok = (50, 150, 50)
        
        # -----------------------------------------------------------------
        # Burbuja de Información Superior
        # -----------------------------------------------------------------
        bw, bh = 1100, 75
        bx = (1920 - bw) // 2
        by = 15

        bubble = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(bubble, (30, 20, 15, 235), (0, 0, bw, bh), border_radius=15)
        pygame.draw.rect(bubble, (212, 175, 55), (0, 0, bw, bh), width=3, border_radius=15)
        superficie.blit(bubble, (bx, by))

        prov_texto = self.config.get_proveedor_texto()
        txt_ram = self._fuente_texto.render(f"RAM Detectada: {self.ram_sistema:.1f} GB", True, (240, 230, 210))
        txt_sep = self._fuente_texto.render("  |  ", True, (160, 140, 100))

        if prov_texto in ("openai", "chatgpt"):
            txt_act = self._fuente_texto.render("Motor Activo: ChatGPT Cloud (gpt-4o-mini)", True, (56, 189, 248))
        else:
            modelo_actual = self.config.get_modelo_local()
            txt_act = self._fuente_texto.render(f"Modelo Activo: Ollama ({modelo_actual})", True, (100, 220, 100))

        superficie.blit(txt_ram, (bx + 30, by + 10))
        superficie.blit(txt_sep, (bx + 30 + txt_ram.get_width(), by + 10))
        superficie.blit(txt_act, (bx + 30 + txt_ram.get_width() + txt_sep.get_width(), by + 10))

        if not hasattr(self.ollama, 'servidor_ollama_activo') or not self.ollama.servidor_ollama_activo:
            txt_warn = self._fuente_chica.render("¡AVISO: Servidor Ollama no detectado! Ábrelo para modelos offline.", True, (255, 120, 120))
        else:
            txt_warn = self._fuente_chica.render("Servidor Ollama: Conectado y listo.", True, (120, 220, 120))
        superficie.blit(txt_warn, (bx + 30, by + 42))

        # -----------------------------------------------------------------
        # Lista de modelos locales
        # -----------------------------------------------------------------
        card_w = 840
        card_h = 92
        card_gap = 105
        y_start = self.y + 245
        bx_base = self.x + (self.ancho - card_w) // 2
        modelo_actual = self.config.get_modelo_local()

        for idx, mod in enumerate(OllamaManager.MODELOS_DISPONIBLES):
            bx = bx_base
            by = y_start + (idx * card_gap)
            
            pygame.draw.rect(superficie, (245, 238, 220), (bx, by, card_w, card_h), border_radius=12)
            pygame.draw.rect(superficie, (180, 150, 110), (bx, by, card_w, card_h), 2, border_radius=12)
            
            txt_nom = self._fuente_texto.render(mod["nombre"], True, color_texto)
            superficie.blit(txt_nom, (bx + 20, by + 12))
            
            req_color = color_ok if self.ram_sistema >= mod["ram_req"] else color_alerta
            txt_req = self._fuente_chica.render(f"Requiere: {mod['ram_req']} GB RAM", True, req_color)
            superficie.blit(txt_req, (bx + 240, by + 16))
            
            txt_desc = self._fuente_chica.render(mod["desc"], True, (100, 80, 60))
            superficie.blit(txt_desc, (bx + 20, by + 48))
            
            is_installed = False
            for inst in self.modelos_instalados:
                if mod["id"] in inst:
                    is_installed = True
                    break
                    
            if is_installed:
                if prov_texto == "ollama" and modelo_actual == mod["id"]:
                    txt_btn = self._fuente_texto.render("ACTIVO", True, color_ok)
                else:
                    txt_btn = self._fuente_texto.render("Seleccionar", True, color_texto)
            else:
                txt_btn = self._fuente_texto.render("Descargar", True, color_texto)
                
            btn = self.botones_accion[idx]
            cx = btn.x + (btn.ancho - txt_btn.get_width()) // 2
            cy = btn.y + (btn.alto - txt_btn.get_height()) // 2
            superficie.blit(txt_btn, (cx, cy))

        # -----------------------------------------------------------------
        # BOTÓN CONSTRUIDO POR NOSOTROS (Únicamente: 'Modo Pruebas GPT')
        # -----------------------------------------------------------------
        es_activo = prov_texto in ("openai", "chatgpt")
        bg_btn_exp = (24, 33, 47) if (self.hover_btn_exposicion or es_activo) else (15, 23, 42)
        border_btn_exp = (16, 185, 129) if es_activo else ((56, 189, 248) if self.hover_btn_exposicion else (55, 65, 81))
        grosor_exp = 3 if (self.hover_btn_exposicion or es_activo) else 2

        pygame.draw.rect(superficie, bg_btn_exp, self.rect_btn_exposicion, border_radius=10)
        pygame.draw.rect(superficie, border_btn_exp, self.rect_btn_exposicion, width=grosor_exp, border_radius=10)

        t_exp = self._fuente_boton.render("Modo Pruebas GPT", True, (249, 250, 251))
        cx_exp = self.rect_btn_exposicion.x + (self.rect_btn_exposicion.width - t_exp.get_width()) // 2
        cy_exp = self.rect_btn_exposicion.y + (self.rect_btn_exposicion.height - t_exp.get_height()) // 2
        superficie.blit(t_exp, (cx_exp, cy_exp))

        # Barra de descarga si está activa
        if self.ollama.descarga_activa:
            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            superficie.blit(overlay, (self.x, self.y))
            
            bx = self.x + 200
            by = self.y + self.alto // 2
            bw = 700
            bh = 40
            
            pygame.draw.rect(superficie, (255, 255, 255), (bx, by, bw, bh), 2)
            fill_w = int(bw * (self.ollama.progreso_actual / 100.0))
            pygame.draw.rect(superficie, (100, 200, 100), (bx + 2, by + 2, fill_w - 4, bh - 4))
            
            txt_estado = self._fuente_texto.render(self.ollama.estado_descarga, True, (255, 255, 255))
            superficie.blit(txt_estado, (bx, by - 30))
            
            txt_pct = self._fuente_texto.render(f"{self.ollama.progreso_actual:.1f}%", True, (0, 0, 0))
            superficie.blit(txt_pct, (bx + bw//2 - 20, by + 10))
            
        elif self.ollama.error_descarga:
            txt_err = self._fuente_texto.render(f"Error: {self.ollama.error_descarga}", True, color_alerta)
            superficie.blit(txt_err, (self.x + 120, self.y + 700))
