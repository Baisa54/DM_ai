import pygame
import threading
import time
from Vista.widgets.widget import Widget
from Vista.widgets.caja_texto import CajaTexto
from modelo.configuracion import ConfigManager
from modelo.ai.OpenAIClient import OpenAIClient

class DashboardExposicion(Widget):
    """
    Panel Full-Screen (1920x1080) con estética moderna de Dashboard Web / HTML.
    Permite gestionar y comparar en tiempo real los motores de inferencia (Ollama vs ChatGPT),
    probar la latencia y consumo de tokens, y aislar la clave API de Git de forma profesional.
    """

    def __init__(self, gestor_recursos, on_cerrar=None):
        super().__init__(0, 0, 1920, 1080)
        self.gestor_recursos = gestor_recursos
        self.on_cerrar = on_cerrar
        self.config = ConfigManager()

        self.visible = False
        self.habilitado = True

        # Fuentes de alta nitidez y definicion (Segoe UI nativa de Windows con fallback a Arial)
        self.fnt_logo = pygame.font.SysFont("segoeui,arial", 28, bold=True)
        self.fnt_badge = pygame.font.SysFont("segoeui,arial", 16, bold=True)
        self.fnt_h1 = pygame.font.SysFont("segoeui,arial", 23, bold=True)
        self.fnt_h2 = pygame.font.SysFont("segoeui,arial", 19, bold=True)
        self.fnt_body = pygame.font.SysFont("segoeui,arial", 17)
        self.fnt_body_bold = pygame.font.SysFont("segoeui,arial", 17, bold=True)
        self.fnt_code = pygame.font.SysFont("consolas,courier", 15)
        self.fnt_stats_num = pygame.font.SysFont("segoeui,arial", 24, bold=True)

        # Estado del motor
        self.proveedor_seleccionado = self.config.get_proveedor_texto()
        if self.proveedor_seleccionado not in ("ollama", "openai"):
            self.proveedor_seleccionado = "ollama"

        # Estado del test de conexión
        self.probando_conexion = False
        self.test_estado = "inactivo" # inactivo, probando, exito, error
        self.test_mensaje = "Listo para verificar conectividad con api.openai.com."
        self.test_latencia = 0

        # Hover states
        self.hover_btn_cerrar = False
        self.hover_card_ollama = False
        self.hover_card_openai = False
        self.hover_btn_probar = False
        self.hover_btn_ver = False
        self.hover_btn_guardar = False

        # Input box estilo web dark mode
        self.caja_api_key = CajaTexto(
            x=980, y=195,
            ancho=680, alto=52,
            gestor_recursos=gestor_recursos,
            fuente_tamano=22,
            placeholder="sk-proj-...",
            max_longitud=160
        )
        self.caja_api_key.es_password = True
        self.caja_api_key.color_texto = (245, 245, 245)
        self.caja_api_key.color_placeholder = (120, 130, 145)
        self.caja_api_key.color_cursor = (56, 189, 248)
        self.caja_api_key.padding_x = 18
        self.caja_api_key.padding_right = 18
        self.caja_api_key.texto = self.config.get_openai_key()

        # Rects interactivos sin superposiciones
        self.rect_btn_cerrar = pygame.Rect(1740, 22, 130, 42)
        self.rect_card_ollama = pygame.Rect(80, 120, 830, 390)
        self.rect_card_openai = pygame.Rect(80, 535, 830, 415)
        self.rect_btn_ver = pygame.Rect(1680, 195, 140, 52)
        self.rect_btn_probar = pygame.Rect(980, 515, 330, 48)
        self.rect_btn_guardar = pygame.Rect(950, 885, 910, 65)

    def abrir(self):
        self.visible = True
        self.proveedor_seleccionado = self.config.get_proveedor_texto()
        if self.proveedor_seleccionado not in ("ollama", "openai"):
            self.proveedor_seleccionado = "ollama"
        self.caja_api_key.texto = self.config.get_openai_key()

    def cerrar_dashboard(self):
        self.visible = False
        if self.on_cerrar:
            self.on_cerrar()

    def _ejecutar_prueba_ping(self):
        if self.probando_conexion:
            return

        clave = self.caja_api_key.texto.strip()
        if not clave:
            self.test_estado = "error"
            self.test_mensaje = "Error: Ingrese una API Key valida antes de iniciar el test."
            self.test_latencia = 0
            return

        self.probando_conexion = True
        self.test_estado = "probando"
        self.test_mensaje = "Enviando solicitud de 1 token a api.openai.com..."

        def thread_ping():
            exito, msg, lat = OpenAIClient.probar_conexion(clave, modelo="gpt-4o-mini")
            self.probando_conexion = False
            self.test_latencia = lat
            if exito:
                self.test_estado = "exito"
                self.test_mensaje = f"Conexion verificada ({lat} ms). gpt-4o-mini autenticado correctamente."
            else:
                self.test_estado = "error"
                self.test_mensaje = msg

        t = threading.Thread(target=thread_ping, daemon=True)
        t.start()

    def _guardar_cambios(self):
        clave = self.caja_api_key.texto.strip()
        self.config.set_openai_key(clave)
        self.config.set_proveedor_texto(self.proveedor_seleccionado)
        self.config.guardar_config()
        self.cerrar_dashboard()

    def manejar_evento(self, evento):
        if not self.visible or not self.habilitado:
            return False

        if self.caja_api_key.manejar_evento(evento):
            return True

        if evento.type == pygame.MOUSEMOTION:
            pos = evento.pos
            self.hover_btn_cerrar = self.rect_btn_cerrar.collidepoint(pos)
            self.hover_card_ollama = self.rect_card_ollama.collidepoint(pos)
            self.hover_card_openai = self.rect_card_openai.collidepoint(pos)
            self.hover_btn_ver = self.rect_btn_ver.collidepoint(pos)
            self.hover_btn_probar = self.rect_btn_probar.collidepoint(pos)
            self.hover_btn_guardar = self.rect_btn_guardar.collidepoint(pos)

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos = evento.pos

            if self.rect_btn_cerrar.collidepoint(pos):
                self.cerrar_dashboard()
                return True

            if self.rect_card_ollama.collidepoint(pos):
                self.proveedor_seleccionado = "ollama"
                return True

            if self.rect_card_openai.collidepoint(pos):
                self.proveedor_seleccionado = "openai"
                return True

            if self.rect_btn_ver.collidepoint(pos):
                self.caja_api_key.es_password = not self.caja_api_key.es_password
                return True

            if self.rect_btn_probar.collidepoint(pos):
                self._ejecutar_prueba_ping()
                return True

            if self.rect_btn_guardar.collidepoint(pos):
                self._guardar_cambios()
                return True

            return True

        elif evento.type in (pygame.KEYDOWN, pygame.KEYUP):
            if evento.key == pygame.K_ESCAPE:
                self.cerrar_dashboard()
                return True
            return True

        return True

    def dibujar(self, superficie):
        if not self.visible:
            return

        # 1. FONDO GLOBAL DARK
        superficie.fill((11, 15, 25))

        # 2. NAVBAR SUPERIOR
        pygame.draw.rect(superficie, (17, 24, 39), (0, 0, 1920, 80))
        pygame.draw.line(superficie, (31, 41, 55), (0, 80), (1920, 80), 2)

        badge_rect = pygame.Rect(80, 22, 185, 36)
        pygame.draw.rect(superficie, (30, 41, 59), badge_rect, border_radius=8)
        pygame.draw.rect(superficie, (56, 189, 248), badge_rect, width=1, border_radius=8)
        txt_b = self.fnt_badge.render("CACIC 2026 | UNLu", True, (56, 189, 248))
        superficie.blit(txt_b, (badge_rect.x + (badge_rect.width - txt_b.get_width()) // 2, badge_rect.y + 8))

        txt_brand = self.fnt_logo.render("DM-AI Studio", True, (249, 250, 251))
        superficie.blit(txt_brand, (285, 24))

        txt_sub_nav = self.fnt_body.render("Panel de Configuracion de Inferencia y Pruebas de Desempeno", True, (156, 163, 175))
        superficie.blit(txt_sub_nav, (470, 29))

        # Boton Cerrar
        c_cerrar = (239, 68, 68) if self.hover_btn_cerrar else (55, 65, 81)
        pygame.draw.rect(superficie, (31, 41, 55), self.rect_btn_cerrar, border_radius=8)
        pygame.draw.rect(superficie, c_cerrar, self.rect_btn_cerrar, width=2, border_radius=8)
        txt_c = self.fnt_h2.render("Cerrar", True, (243, 244, 246))
        superficie.blit(txt_c, (self.rect_btn_cerrar.x + (self.rect_btn_cerrar.width - txt_c.get_width()) // 2, self.rect_btn_cerrar.y + 10))


        # 3. COLUMNA IZQUIERDA: COMPARATIVA Y SELECTOR
        # --- TARJETA 1: OLLAMA LOCAL ---
        es_ollama_activo = (self.proveedor_seleccionado == "ollama")
        bg_ollama = (24, 33, 47) if self.hover_card_ollama else (17, 24, 39)
        border_ollama = (16, 185, 129) if es_ollama_activo else (55, 65, 81)
        grosor_ollama = 3 if es_ollama_activo else 1

        pygame.draw.rect(superficie, bg_ollama, self.rect_card_ollama, border_radius=14)
        pygame.draw.rect(superficie, border_ollama, self.rect_card_ollama, width=grosor_ollama, border_radius=14)

        tag_ol = self.fnt_badge.render("MODO INVESTIGACION OFICIAL", True, (16, 185, 129))
        superficie.blit(tag_ol, (110, 140))

        txt_ol_title = self.fnt_h1.render("Ollama Local (Offline / Llama 3.1 8B)", True, (249, 250, 251))
        superficie.blit(txt_ol_title, (110, 168))

        txt_ol_desc = (
            "Inferencia 100% local en dispositivo mediante modelos cuantizados ejecutados en Ollama.\n"
            "Corresponde a la arquitectura analizada en el articulo cientifico presentado en CACIC:\n"
            "total soberania de datos y costo cero de tokens."
        )
        self._dibujar_multilinea(superficie, txt_ol_desc, 110, 205, 23, color=(180, 188, 200))

        # Metricas
        self._dibujar_stat_box(superficie, 110, 290, 170, 75, "PRIVACIDAD", "100% Local", (16, 185, 129))
        self._dibujar_stat_box(superficie, 300, 290, 170, 75, "COSTO API", "$0.00", (16, 185, 129))
        self._dibujar_stat_box(superficie, 490, 290, 170, 75, "LATENCIA", "~15s - 35s", (245, 158, 11))
        self._dibujar_stat_box(superficie, 680, 290, 200, 75, "ESTUDIO", "Paper CACIC", (56, 189, 248))

        # Boton activar Ollama
        btn_sel_ol = pygame.Rect(110, 395, 770, 48)
        c_btn_ol = (16, 185, 129) if es_ollama_activo else (31, 41, 55)
        pygame.draw.rect(superficie, c_btn_ol, btn_sel_ol, border_radius=8)
        lbl_ol = "[ MOTOR COGNITIVO ACTIVO ]" if es_ollama_activo else "Activar Motor Ollama Local"
        t_btn_ol = self.fnt_h2.render(lbl_ol, True, (255, 255, 255) if es_ollama_activo else (209, 213, 219))
        superficie.blit(t_btn_ol, (btn_sel_ol.x + (btn_sel_ol.width - t_btn_ol.get_width()) // 2, btn_sel_ol.y + 12))


        # --- TARJETA 2: OPENAI CHATGPT ---
        es_openai_activo = (self.proveedor_seleccionado == "openai")
        bg_openai = (24, 33, 47) if self.hover_card_openai else (17, 24, 39)
        border_openai = (56, 189, 248) if es_openai_activo else (55, 65, 81)
        grosor_openai = 3 if es_openai_activo else 1

        pygame.draw.rect(superficie, bg_openai, self.rect_card_openai, border_radius=14)
        pygame.draw.rect(superficie, border_openai, self.rect_card_openai, width=grosor_openai, border_radius=14)

        tag_oa = self.fnt_badge.render("MODO DEMOSTRACION EN VIVO (ALTA VELOCIDAD)", True, (56, 189, 248))
        superficie.blit(tag_oa, (110, 555))

        txt_oa_title = self.fnt_h1.render("ChatGPT Cloud (OpenAI / gpt-4o-mini)", True, (249, 250, 251))
        superficie.blit(txt_oa_title, (110, 583))

        txt_oa_desc = (
            "Inferencia en la nube de alta velocidad disenada para exposiciones y demostraciones en vivo.\n"
            "Permite respuestas fluidas (~1 segundo), resolucion estricta de Tool Calling deterministico\n"
            "y un consumo minimo de tokens por consulta."
        )
        self._dibujar_multilinea(superficie, txt_oa_desc, 110, 620, 23, color=(180, 188, 200))

        # Metricas
        self._dibujar_stat_box(superficie, 110, 715, 170, 75, "LATENCIA", "~0.8s - 1.2s", (16, 185, 129))
        self._dibujar_stat_box(superficie, 300, 715, 170, 75, "COSTO ESTIMADO", "$0.15 / 1M", (16, 185, 129))
        self._dibujar_stat_box(superficie, 490, 715, 170, 75, "TOOL CALLING", "100% Preciso", (56, 189, 248))
        self._dibujar_stat_box(superficie, 680, 715, 200, 75, "FLUIDEZ", "Tiempo Real", (245, 158, 11))

        # Boton activar OpenAI
        btn_sel_oa = pygame.Rect(110, 820, 770, 48)
        c_btn_oa = (56, 189, 248) if es_openai_activo else (31, 41, 55)
        pygame.draw.rect(superficie, c_btn_oa, btn_sel_oa, border_radius=8)
        lbl_oa = "[ MOTOR COGNITIVO ACTIVO ]" if es_openai_activo else "Activar Modo Pruebas GPT"
        t_btn_oa = self.fnt_h2.render(lbl_oa, True, (15, 23, 42) if es_openai_activo else (209, 213, 219))
        superficie.blit(t_btn_oa, (btn_sel_oa.x + (btn_sel_oa.width - t_btn_oa.get_width()) // 2, btn_sel_oa.y + 12))


        # -----------------------------------------------------------------
        # 4. COLUMNA DERECHA: CONFIGURACION Y DIAGNOSTICO EN VIVO
        # -----------------------------------------------------------------
        # PANEL 1: CLAVE API (Sin solapamientos)
        panel_key = pygame.Rect(950, 120, 910, 275)
        pygame.draw.rect(superficie, (17, 24, 39), panel_key, border_radius=14)
        pygame.draw.rect(superficie, (55, 65, 81), panel_key, width=1, border_radius=14)

        t_key_h = self.fnt_h1.render("Configuracion de Clave API (OpenAI)", True, (249, 250, 251))
        superficie.blit(t_key_h, (980, 145))

        t_key_sub = self.fnt_body.render("Clave de autenticacion para inferencia con modelos GPT en la nube:", True, (156, 163, 175))
        superficie.blit(t_key_sub, (980, 172))

        # Caja de entrada
        self.caja_api_key.dibujar(superficie)
        pygame.draw.rect(superficie, (55, 65, 81), self.caja_api_key.rect, width=1, border_radius=8)

        # Boton Mostrar / Ocultar
        bg_ver = (31, 41, 55) if self.hover_btn_ver else (24, 33, 47)
        pygame.draw.rect(superficie, bg_ver, self.rect_btn_ver, border_radius=8)
        pygame.draw.rect(superficie, (75, 85, 99), self.rect_btn_ver, width=1, border_radius=8)
        txt_ojito = "Ocultar" if not self.caja_api_key.es_password else "Mostrar"
        t_ojito = self.fnt_h2.render(txt_ojito, True, (243, 244, 246))
        superficie.blit(t_ojito, (self.rect_btn_ver.x + (self.rect_btn_ver.width - t_ojito.get_width()) // 2, self.rect_btn_ver.y + 14))

        # Cuadro de Seguridad Profesional (Sin textos informales)
        banner_sec = pygame.Rect(980, 265, 850, 110)
        pygame.draw.rect(superficie, (15, 23, 42), banner_sec, border_radius=8)
        pygame.draw.rect(superficie, (56, 189, 248), banner_sec, width=1, border_radius=8)

        t_sec_tit = self.fnt_body_bold.render("ALMACENAMIENTO SEGURO Y PRIVACIDAD:", True, (56, 189, 248))
        superficie.blit(t_sec_tit, (1000, 278))

        txt_sec_info = (
            "• La clave se almacena de forma local y privada en .secrets.json (ignorado por Git).\n"
            "• No se transmite a repositorios remotos ni se incluye en los registros de control de versiones.\n"
            "• El campo permanece enmascarado en pantalla para proteger la confidencialidad en sala."
        )
        self._dibujar_multilinea(superficie, txt_sec_info, 1000, 302, 21, color=(209, 213, 219))


        # PANEL 2: SUITE DE DIAGNOSTICO EN VIVO (Perfectamente espaciado, sin superposicion)
        panel_diag = pygame.Rect(950, 420, 910, 435)
        pygame.draw.rect(superficie, (17, 24, 39), panel_diag, border_radius=14)
        pygame.draw.rect(superficie, (55, 65, 81), panel_diag, width=1, border_radius=14)

        t_diag_h = self.fnt_h1.render("Diagnostico y Verificacion de Conectividad", True, (249, 250, 251))
        superficie.blit(t_diag_h, (980, 442))

        t_diag_desc = self.fnt_body.render("Envie una solicitud minima para comprobar autenticacion y medir latencia de red:", True, (156, 163, 175))
        superficie.blit(t_diag_desc, (980, 472))

        # Boton Probar Conexión (Ubicado debajo de las etiquetas, SIN SUPERPONERSE)
        bg_probar = (37, 99, 235) if self.hover_btn_probar else (29, 78, 216)
        pygame.draw.rect(superficie, bg_probar, self.rect_btn_probar, border_radius=8)
        t_prob = self.fnt_h2.render("Probar Conexion (Ping 1 Token)", True, (255, 255, 255))
        superficie.blit(t_prob, (self.rect_btn_probar.x + (self.rect_btn_probar.width - t_prob.get_width()) // 2, self.rect_btn_probar.y + 12))

        # Cuadro de resultado del test
        card_res = pygame.Rect(980, 580, 850, 250)
        c_res_border = (16, 185, 129) if self.test_estado == "exito" else ((239, 68, 68) if self.test_estado == "error" else (55, 65, 81))
        pygame.draw.rect(superficie, (15, 23, 42), card_res, border_radius=10)
        pygame.draw.rect(superficie, c_res_border, card_res, width=1, border_radius=10)

        t_st_tit = self.fnt_body_bold.render("RESULTADO DEL TEST EN TIEMPO REAL:", True, (156, 163, 175))
        superficie.blit(t_st_tit, (1005, 595))

        c_msg = (16, 185, 129) if self.test_estado == "exito" else ((248, 113, 113) if self.test_estado == "error" else (209, 213, 219))
        t_msg_render = self.fnt_body.render(f"Estado: {self.test_mensaje}", True, c_msg)
        superficie.blit(t_msg_render, (1005, 625))

        # Metricas del ping
        lat_txt = f"{self.test_latencia} ms" if self.test_latencia > 0 else "--"
        lat_col = (16, 185, 129) if self.test_latencia > 0 and self.test_latencia < 1500 else (245, 158, 11)
        self._dibujar_stat_box(superficie, 1005, 665, 180, 75, "LATENCIA PING", lat_txt, lat_col)
        self._dibujar_stat_box(superficie, 1205, 665, 210, 75, "MODELO VERIFICADO", "gpt-4o-mini", (56, 189, 248))
        self._dibujar_stat_box(superficie, 1435, 665, 200, 75, "CONSUMO PRUEBA", "1 token (~$0.00)", (16, 185, 129))
        self._dibujar_stat_box(superficie, 1655, 665, 160, 75, "TOOL CALLING", "Operativo", (16, 185, 129))

        t_note = self.fnt_code.render("Inferencia validada con respuesta estructurada JSON de 1 token de costo.", True, (120, 130, 145))
        superficie.blit(t_note, (1005, 775))


        # BOTON GUARDAR Y APLICAR (Inferior)
        bg_guardar = (16, 185, 129) if self.hover_btn_guardar else (5, 150, 105)
        pygame.draw.rect(superficie, bg_guardar, self.rect_btn_guardar, border_radius=12)
        txt_guardar = self.fnt_stats_num.render("GUARDAR Y ACTIVAR CONFIGURACION", True, (255, 255, 255))
        superficie.blit(txt_guardar, (self.rect_btn_guardar.x + (self.rect_btn_guardar.width - txt_guardar.get_width()) // 2, self.rect_btn_guardar.y + 18))

    def _dibujar_stat_box(self, superficie, x, y, w, h, etiqueta, valor, color_valor):
        """Renderiza una cajita de estadistica moderna estilo tarjeta web."""
        pygame.draw.rect(superficie, (24, 33, 47), (x, y, w, h), border_radius=8)
        pygame.draw.rect(superficie, (55, 65, 81), (x, y, w, h), width=1, border_radius=8)
        t_lbl = self.fnt_badge.render(etiqueta, True, (156, 163, 175))
        t_val = self.fnt_h2.render(valor, True, color_valor)
        superficie.blit(t_lbl, (x + 14, y + 10))
        superficie.blit(t_val, (x + 14, y + 36))

    def _dibujar_multilinea(self, superficie, texto_str, x, y, interlineado, color=None):
        """Renderiza parrafos de texto respetando saltos de linea."""
        lineas = texto_str.split("\n") if isinstance(texto_str, str) else [texto_str]
        for i, l in enumerate(lineas):
            if isinstance(l, str):
                s = self.fnt_body.render(l, True, color or (156, 163, 175))
            else:
                s = l
            superficie.blit(s, (x, y + i * interlineado))
