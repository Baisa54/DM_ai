import pygame
from Vista.widgets.popup import Popup
from Vista.widgets.boton import Boton
from modelo.configuracion import ConfigManager
from modelo.ai.ollama_manager import OllamaManager
from Vista.widgets.popup_confirmacion import PopupConfirmacion

class PopupModelos(Popup):
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
        self.ollama = OllamaManager()
        self.ram_sistema = self.ollama.obtener_ram_gb()
        self.modelos_instalados = self.ollama.obtener_modelos_instalados()
        
        self._fuente_titulo = pygame.font.Font(None, 42)
        self._fuente_texto = pygame.font.Font(None, 28)
        self._fuente_chica = pygame.font.Font(None, 22)
        
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
        y_offset = self.y + 300
        
        for idx, mod in enumerate(OllamaManager.MODELOS_DISPONIBLES):
            bx = self.x + 1050
            by = y_offset + (idx * 110)
            
            btn = Boton(
                x=bx, y=by,
                ruta_normal="Vista/resources/images/Input_Box.png",
                ruta_hover="Vista/resources/images/Input_Box.png",
                ruta_presionado="Vista/resources/images/Input_Box.png",
                gestor_recursos=gestor_recursos,
                ancho=160, alto=50,
                on_click=lambda m=mod: self._on_click_modelo(m)
            )
            self.botones_accion.append(btn)
            self.agregar_widget(btn)

        self.popup_confirmacion = None

    def _cerrar_interno(self):
        if self.ollama.descarga_activa:
            # No permitir cerrar si está descargando
            return
            
        self.cerrar()
        if self.on_cerrar:
            self.on_cerrar()

    def _on_click_modelo(self, modelo):
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
        if self.popup_confirmacion:
            self.popup_confirmacion.cerrar()
            self.popup_confirmacion = None
            
        self.ollama.iniciar_descarga(modelo_id)

    def manejar_evento(self, evento):
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
        
        # No dibujamos título porque ya está en el pergamino, pero podemos poner la RAM arriba.
        txt_ram = self._fuente_texto.render(f"RAM Detectada: {self.ram_sistema:.1f} GB", True, color_texto)
        superficie.blit(txt_ram, (self.x + 350, self.y + 200))
        
        # Modelo actualmente seleccionado
        modelo_actual = self.config.get_modelo_local()
        txt_actual = self._fuente_texto.render(f"Modelo Activo: {modelo_actual}", True, color_ok)
        superficie.blit(txt_actual, (self.x + 350, self.y + 235))
        
        # Aviso si Ollama no está activo
        if not hasattr(self.ollama, 'servidor_ollama_activo') or not self.ollama.servidor_ollama_activo:
            txt_warn = self._fuente_texto.render("¡AVISO: Servidor Ollama no detectado! Ábrelo para ver tus modelos.", True, color_alerta)
            superficie.blit(txt_warn, (self.x + 350, self.y + 270))

        # Lista de modelos
        y_offset = self.y + 300
        modelo_actual = self.config.get_modelo_local()

        for idx, mod in enumerate(OllamaManager.MODELOS_DISPONIBLES):
            bx = self.x + 350
            by = y_offset + (idx * 110)
            
            # Dibujar caja de fondo tenue
            pygame.draw.rect(superficie, (240, 230, 210), (bx - 10, by - 10, 880, 100), border_radius=10)
            pygame.draw.rect(superficie, (200, 180, 140), (bx - 10, by - 10, 880, 100), 2, border_radius=10)
            
            # Nombre y Requisito
            txt_nom = self._fuente_texto.render(mod["nombre"], True, color_texto)
            superficie.blit(txt_nom, (bx, by))
            
            req_color = color_ok if self.ram_sistema >= mod["ram_req"] else color_alerta
            txt_req = self._fuente_chica.render(f"Requiere: {mod['ram_req']} GB RAM", True, req_color)
            superficie.blit(txt_req, (bx + 250, by + 5))
            
            # Descripción
            txt_desc = self._fuente_chica.render(mod["desc"], True, (100, 80, 60))
            superficie.blit(txt_desc, (bx, by + 35))
            
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
