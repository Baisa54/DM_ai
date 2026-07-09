#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# escena_juego
#
# escena_juego implementa EscenaJuego, la pantalla de juego principal que orquesta
# la distribución visual de los widgets del RPG (pergaminios, marcos de imágenes,
# cajas de texto y botones de acción y modales de confirmación).
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ EscenaJuego, clase que gestiona la escena interactiva de la aventura.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import threading
from Vista.escenas.escena_base import EscenaBase
# EscenaBase es la clase base para la manipulación de escenas gráficas
from Vista.widgets.imagen import Imagen
# Imagen es el widget básico de renderizado de texturas
from Vista.widgets.texto_multilinea import TextoMultilinea
# TextoMultilinea para mostrar la narrativa extensa
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class EscenaJuego(EscenaBase):
    """
    Escena principal de la aplicación que representa la interfaz del Dungeon Master.
    """

    def __init__(self, gestor_recursos, campania):
        """
        Inicializa la escena y carga los widgets estáticos iniciales.
        
        Args:
            gestor_recursos (GestorRecursos): Administrador de recursos para cargar assets.
            campania (Campania): Estado backend lógico del juego.
        """
        super().__init__()
        self.campania = campania
        self.procesando_ia = False
        self.mensaje_procesando = "Procesando..."
        self._dialogo_fullscreen_visible = False
        self._hay_dialogo = False
        self._datos_dialogo = {}
        
        # 1. Cargar fondo (Forzado a resolución de pantalla 1920x1080)
        fondo_widget = Imagen(
            x=0, y=0, 
            ruta_imagen="Vista/resources/images/Fondo.png", 
            gestor_recursos=gestor_recursos, 
            ancho=1920, alto=1080, 
            alpha=False
        )
        self.agregar_widget(fondo_widget)

        # 2. Logo superior izquierdo (dmai_small.png)
        # Original procesado con filtro Lanczos a 350x191 para máxima calidad.
        logo = Imagen(
            x=40, y=10,
            ruta_imagen="Vista/resources/images/dmai_small.png",
            gestor_recursos=gestor_recursos,
            ancho=350, alto=191,
            alpha=True
        )
        self.agregar_widget(logo)

        # 3. Divisor superior central (Ornamental_Divider_1.png)
        # Original: 638x78. Se mantiene igual, centrado en X
        divisor = Imagen(
            x=(1920 - 638) // 2, y=40,
            ruta_imagen="Vista/resources/images/Ornamental_Divider_1.png",
            gestor_recursos=gestor_recursos,
            ancho=638, alto=78,
            alpha=True
        )
        self.agregar_widget(divisor)

        # 4. Botón Cerrar superior derecho (Close_Button_normal.png)
        # Original: ~178x179. Lo escalamos a 140x140
        from Vista.widgets.boton import Boton
            
        btn_cerrar = Boton(
            x=1920 - 140 - 40, y=20,
            ruta_normal="Vista/resources/images/Close_Button_normal.png",
            ruta_hover="Vista/resources/images/Close_Button_hover.png",
            ruta_presionado="Vista/resources/images/Close_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=140, alto=140,
            on_click=lambda: self.popup_salir.abrir()
        )
        self.agregar_widget(btn_cerrar)

        # 4.5. Botón de Control de Volumen (Al lado del botón de cerrar)
        from Vista.widgets.boton_volumen import BotonVolumen
        # Tamaño 80x80, centrado verticalmente con el botón de cerrar
        btn_volumen = BotonVolumen(
            x=btn_cerrar.x - 80 - 20, y=20 + (140 - 80) // 2,
            ancho=80, alto=80,
            gestor_recursos=gestor_recursos
        )
        self.agregar_widget(btn_volumen)

        # 4.6 Botón DEBUG oculto
        self._debug_visible = False

        # 5. Marco Izquierdo (imagen_box.png)
        marco_izq = Imagen(
            x=100, y=150,
            ruta_imagen="Vista/resources/images/imagen_box.png",
            gestor_recursos=gestor_recursos,
            ancho=800, alto=800,
            alpha=True
        )
        self.agregar_widget(marco_izq)

        self.imagen_escena = Imagen(
            x=100 + 100, y=150 + 100, # padding simulado
            ruta_imagen=None,
            gestor_recursos=gestor_recursos,
            ancho=800 - 200, alto=800 - 200,
            alpha=True,
            mantener_proporcion=True
        )
        self.imagen_escena.texto_fallback = "Generando imagen..."
        self.agregar_widget(self.imagen_escena)

        # 6. Marco Derecho / Pergamino (pergamino_box.png)
        marco_der = Imagen(
            x=1020, y=150,
            ruta_imagen="Vista/resources/images/pergamino_box.png",
            gestor_recursos=gestor_recursos,
            ancho=800, alto=800,
            alpha=True
        )
        self.agregar_widget(marco_der)

        # Contenedor para el texto generado por IA (sobre marco_der)
        self.texto_narracion = TextoMultilinea(
            x=1020, y=150,
            ancho=800, alto=800,
            gestor_recursos=gestor_recursos,
            fuente_tamano=32,
            color_texto=(30, 20, 10)
        )
        self.texto_narracion.padding_x = 160
        self.texto_narracion.padding_y = 180
        self.agregar_widget(self.texto_narracion)

        # 7. Elementos inferiores
        # Vamos a escalar todos a un alto aproximado de 140px para que encajen bien
        alto_inferior = 140
        y_inferior = 1080 - alto_inferior - 20 # 20px de margen inferior

        # a. Barra de texto (Caja de entrada) (5088x832 -> 856x140)
        from Vista.widgets.caja_texto import CajaTexto
        self.caja_entrada = CajaTexto(
            x=296, y=y_inferior,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Barra_texto.png",
            ancho=856, alto=alto_inferior,
            placeholder="Escribe tu acción aquí...",
            max_longitud=500 # Ahora puede escribir textos muy largos gracias al scroll
        )
        self.caja_entrada.padding_x = 175
        self.caja_entrada.padding_right = 140 
        self.caja_entrada.padding_y = 50 
        self.caja_entrada.color_texto = (30, 20, 10) 
        self.caja_entrada.color_cursor = (30, 20, 10)
        self.agregar_widget(self.caja_entrada)

        # b. Botón Send (219x244 -> 125x140)
        self.btn_send = Boton(
            x=296 + 856 + 20, y=y_inferior,
            ruta_normal="Vista/resources/images/Send_Button_normal.png",
            ruta_hover="Vista/resources/images/Send_Button_hover.png",
            ruta_presionado="Vista/resources/images/Send_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=125, alto=alto_inferior,
            on_click=self._on_enviar_accion
        )
        self.agregar_widget(self.btn_send)

        # c. Botón Confirmar (para final) - Inicialmente oculto (y=3000)
        self.btn_confirmar = Boton(
            x=(1920 - 149) // 2, y=3000,
            ruta_normal="Vista/resources/images/Confirm_Button_normal.png",
            ruta_hover="Vista/resources/images/Confirm_Button_hover.png",
            ruta_presionado="Vista/resources/images/Confirm_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=149, alto=alto_inferior,
            on_click=self._on_click_confirmar_final
        )
        self.agregar_widget(self.btn_confirmar)

        # d. Botón Status (149x140)
        btn_state = Boton(
            x=self.btn_send.x + self.btn_send.ancho + 20, y=y_inferior,
            ruta_normal="Vista/resources/images/State_Button_normal.png",
            ruta_hover="Vista/resources/images/State_Button_hover.png",
            ruta_presionado="Vista/resources/images/State_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=149, alto=alto_inferior,
            on_click=lambda: self.popup_estado.abrir()
        )
        self.agregar_widget(btn_state)

        # e. Botón Reboot (178x179 -> 125x125)
        btn_reboot = Boton(
            x=btn_state.x + btn_state.ancho + 20, y=y_inferior + (140 - 125) // 2,
            ruta_normal="Vista/resources/images/Reboot_Button_normal.png",
            ruta_hover="Vista/resources/images/Reboot_Button_hover.png",
            ruta_presionado="Vista/resources/images/Reboot_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=125, alto=125,
            on_click=lambda: self.popup_reiniciar.abrir()
        )
        self.agregar_widget(btn_reboot)

        # 8. Modal de confirmación de salida (Se agrega al final para renderizarse arriba)
        def confirmar_cierre():
            import pygame
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            
        from Vista.widgets.popup_confirmacion import PopupConfirmacion
        self.popup_salir = PopupConfirmacion(
            gestor_recursos=gestor_recursos,
            texto_pregunta="¿Quieres salir del juego?",
            on_confirmar=confirmar_cierre
        )
        self.agregar_widget(self.popup_salir)
        
        # 9. Modal de confirmación de reinicio
        def confirmar_reinicio():
            self.popup_reiniciar.cerrar()
            self._reiniciar_juego()
            
        self.popup_reiniciar = PopupConfirmacion(
            gestor_recursos=gestor_recursos,
            texto_pregunta="¿Desea reiniciar el juego?",
            on_confirmar=confirmar_reinicio,
            ruta_icono="Vista/resources/images/UI_RestartIcon.png"
        )
        self.agregar_widget(self.popup_reiniciar)

        # 10. Modal de Estado del Personaje
        from Vista.widgets.popup_estado import PopupEstado
        self.popup_estado = PopupEstado(
            gestor_recursos=gestor_recursos,
            campania=self.campania,
            on_cerrar=lambda: None
        )
        self.agregar_widget(self.popup_estado)

        # 11. Modal de Tirada D20
        from Vista.widgets.popup_d20 import PopupD20
        self.popup_d20 = PopupD20(gestor_recursos)
        self.agregar_widget(self.popup_d20)
        
        # 12. Cargar estado inicial del juego en la UI
        self._pantalla_final_visible = False
        self._scroll_final_y = 0
        self._texto_final_generado = ""
        self._img_final_generada = None
        
        self._actualizar_ui_con_resultados()

    def _on_click_confirmar_final(self):
        """Disparado al apretar el botón Confirm al final del juego."""
        if self.procesando_ia:
            return
        
        self.mensaje_procesando = "Tejiendo el destino final..."
        self.procesando_ia = True
        
        def generar_final():
            import pygame
            try:
                self.campania.narracion_final()
                self.campania.generar_imagen_resumen()
                
                datos = self.campania.get_mensaje().obtener_mensaje_completo()
                self._texto_final_generado = datos.get("narracion", "")
                img_path = datos.get("imagen_resumen", "")
                
                if img_path:
                    try:
                        self._img_final_generada = pygame.image.load(img_path).convert_alpha()
                    except:
                        pass
                        
                self._pantalla_final_visible = True
            except Exception as e:
                print("Error generando final:", e)
            finally:
                self.procesando_ia = False
                
        import threading
        threading.Thread(target=generar_final).start()

    def _on_enviar_accion(self):
        """Disparado al apretar el botón Send."""
        if self.procesando_ia:
            return

        accion = self.caja_entrada.texto.strip()
        if not accion:
            return

        self.caja_entrada.limpiar()
        
        # 1. Arbitrar la acción
        self.campania.recibir_accion_jugador(accion)
        self.mensaje_procesando = "El DM está decidiendo..."
        self.procesando_ia = True
        
        def arbitrar():
            try:
                resultado = self.campania.arbitrar_accion_jugador()
                if not resultado.get("accion_valida", False):
                    self.procesando_ia = False
                    print("Acción no válida.")
                    
                    # Dar feedback visual en el pergamino para que el usuario sepa qué pasó
                    texto_actual = self.texto_narracion.texto
                    self.texto_narracion.texto = texto_actual + "\n\n[El DM rechaza tu acción por considerarla imposible, fuera de contexto o inválida. Intenta otra cosa.]"
                    return
                    
                if resultado.get("requiere_tirada", False):
                    self.procesando_ia = False
                    # Abrir el D20 (debe hacerse en el hilo principal)
                    # Usamos un evento personalizado para llamar al popup en el main thread
                    # pero como Pygame no es thread-safe para UI, es mejor usar un flag
                    self._abrir_d20_flag = True
                else:
                    self.campania.get_contexto().set_resultado_d20("exito") # Default si no requiere
                    self._iniciar_hilo_procesamiento()
            except Exception as e:
                print(f"Error al arbitrar: {e}")
                self.procesando_ia = False
                
        threading.Thread(target=arbitrar).start()

    def _iniciar_hilo_procesamiento(self):
        """Inicia la cadena de eventos de IA."""
        self.procesando_ia = True
        threading.Thread(target=self._procesar_turno_ai).start()

    def _procesar_turno_ai(self):
        """Ejecuta toda la lógica de la campaña en segundo plano."""
        try:
            self.mensaje_procesando = "Narrando la historia..."
            print("[IA] Narrando...")
            self.campania.narracion()
            
            self.mensaje_procesando = "Actualizando el estado del mundo..."
            print("[IA] Orquestador...")
            self.campania.orquestador()
            
            self.mensaje_procesando = "Verificando el destino..."
            print("[IA] Verificando finales...")
            self.campania.verificar_finales()
            
            if self.campania.get_mensaje().hay_dialogo_npc():
                print("[IA] Diálogo detectado y procesado por orquestador.")
                
            self.mensaje_procesando = "Pintando la escena..."
            print("[IA] Generando imagen...")
            self.campania.generar_imagen_resumen()

            self._actualizar_ui_con_resultados()
            
        except Exception as e:
            print(f"ERROR en IA: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.procesando_ia = False

    def _actualizar_ui_con_resultados(self):
        """Puelca los datos generados a los widgets visuales."""
        datos = self.campania.get_mensaje().obtener_mensaje_completo()
        
        narracion_final = datos.get("narracion", "")
        if datos.get("narracion_npc"):
            self._hay_dialogo = True
            self._datos_dialogo = {
                "texto": datos["narracion_npc"],
                "imagen": datos.get("imagen_npc", "")
            }
            narracion_final += f"\n\n---\n{datos['narracion_npc']}"
        else:
            self._hay_dialogo = False
            self._datos_dialogo = {}
            
        self.texto_narracion.texto = narracion_final
        
        imagen_path = datos.get("imagen_resumen", "")
        if imagen_path:
            self.imagen_escena.cambiar_imagen(imagen_path)
        else:
            self.imagen_escena.texto_fallback = "No se pudo generar la imagen."
            self.imagen_escena.cambiar_imagen(None)
            
        # Revisar si se alcanzó el final (y que no sea 'sin_final')
        final_actual = self.campania.estado.get_final()
        if final_actual and final_actual != "sin_final":
            self.caja_entrada.y = 3000
            self.btn_send.y = 3000
            if hasattr(self, 'btn_confirmar'):
                self.btn_confirmar.y = 1080 - 140 - 20

    def manejar_evento(self, evento):
        import pygame
        
        # --- Pantalla Final ---
        if getattr(self, '_pantalla_final_visible', False):
            if evento.type == pygame.MOUSEWHEEL:
                self._scroll_final_y += evento.y * 30
                if self._scroll_final_y > 0:
                    self._scroll_final_y = 0
                return True
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # Comprobar si tocó la parte inferior para reiniciar
                # La pantalla mide 1080 de alto, el texto de reiniciar está en y=1000
                if evento.pos[1] > 950:
                    self._reiniciar_juego()
                return True
                
        # Si el diálogo de pantalla completa está visible, cualquier click o tecla lo cierra
        if getattr(self, '_dialogo_fullscreen_visible', False):
            if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self._dialogo_fullscreen_visible = False
                return True
                
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            x, y = evento.pos
            # Botón debug: x entre 5 y 65, y entre 5 y 25
            if 5 <= x <= 65 and 5 <= y <= 25:
                self._debug_visible = not getattr(self, '_debug_visible', False)
                return True
                
            # Botón Nube de Diálogo (si hay diálogo)
            # Dibujado aprox en: x entre 920 y 1000, y entre 500 y 580 (centro derecha)
            if getattr(self, '_hay_dialogo', False):
                if 920 <= x <= 1000 and 500 <= y <= 580:
                    self._dialogo_fullscreen_visible = True
                    return True
                    
            # Si el debug está abierto y tocan cualquier lado, lo cerramos
            if getattr(self, '_debug_visible', False):
                self._debug_visible = False
                return True

        # Si se levantó el flag de D20 desde un hilo
        if hasattr(self, '_abrir_d20_flag') and self._abrir_d20_flag:
            self._abrir_d20_flag = False
            dificultad = self.campania.get_contexto().get_dificultad()
            self.popup_d20.abrir(
                dificultad=dificultad,
                on_resultado=self._on_resultado_d20
            )
            
        # Si estamos procesando, bloqueamos clicks en la UI para evitar doble envío
        if self.procesando_ia or getattr(self, '_debug_visible', False):
            import pygame
            if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.KEYDOWN):
                return True
                
        return super().manejar_evento(evento)

    def _on_resultado_d20(self, resultado_num, tipo):
        """Callback cuando el dado termina de rodar."""
        # Se requiere asignar el resultado al contexto
        self.campania.get_contexto().set_resultado_d20(tipo)
        # Luego iniciar el procesamiento pesado
        self._iniciar_hilo_procesamiento()

    def dibujar(self, superficie):
        import pygame
        # Dibuja todos los widgets normalmente
        super().dibujar(superficie)
        
        # Superponer pantalla de carga si está procesando la IA
        if getattr(self, 'procesando_ia', False):
            import math
            import time
            
            # Oscurecer fondo
            overlay = pygame.Surface((superficie.get_width(), superficie.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Negro con alpha
            superficie.blit(overlay, (0, 0))
            
            # Dibujar texto animado
            font = pygame.font.Font(None, 64)
            puntos = "." * (int(time.time() * 3) % 4)
            texto_render = font.render(getattr(self, 'mensaje_procesando', "Procesando...") + puntos, True, (255, 255, 255))
            
            # Efecto de pulso en opacidad
            alpha = int(128 + 127 * math.sin(time.time() * 5))
            texto_render.set_alpha(alpha)
            
            # Centrar en pantalla
            cx = (superficie.get_width() - texto_render.get_width()) // 2
            cy = (superficie.get_height() - texto_render.get_height()) // 2
            superficie.blit(texto_render, (cx, cy))

        # Dibujar botón debug chiquito
        pygame.draw.rect(superficie, (50, 50, 50), (5, 5, 60, 20))
        fnt_debug_btn = pygame.font.Font(None, 20)
        superficie.blit(fnt_debug_btn.render("DEBUG", True, (200, 200, 200)), (10, 8))

        # Dibujar botón de nube de diálogo si hay diálogo
        if getattr(self, '_hay_dialogo', False):
            # Centro derecha aprox: x=920, y=500
            bx, by = 920, 500
            bw, bh = 80, 80
            pygame.draw.ellipse(superficie, (200, 200, 255), (bx, by, bw, bh))
            pygame.draw.ellipse(superficie, (50, 50, 150), (bx, by, bw, bh), 3)
            fnt_nube = pygame.font.SysFont("arial", 40, bold=True)
            txt_nube = fnt_nube.render("...", True, (50, 50, 150))
            superficie.blit(txt_nube, (bx + bw//2 - txt_nube.get_width()//2, by + bh//2 - txt_nube.get_height()//2 - 10))

        # Dibujar pantalla de diálogo NPC fullscreen
        if getattr(self, '_dialogo_fullscreen_visible', False):
            overlay = pygame.Surface((superficie.get_width(), superficie.get_height()), pygame.SRCALPHA)
            overlay.fill((5, 5, 5, 240)) # Fondo casi negro
            superficie.blit(overlay, (0, 0))
            
            # Dibujar texto de continuar
            fnt_cont = pygame.font.SysFont("arial", 24, italic=True)
            txt_cont = fnt_cont.render("Presione cualquier botón para continuar...", True, (150, 150, 150))
            superficie.blit(txt_cont, (superficie.get_width()//2 - txt_cont.get_width()//2, superficie.get_height() - 50))
            
            # Cargar y dibujar imagen del NPC (Medio izquierdo)
            img_path = self._datos_dialogo.get("imagen")
            if img_path:
                try:
                    # Usamos load temporal, lo ideal sería pasarlo al gestor_recursos
                    npc_surf = pygame.image.load(img_path).convert_alpha()
                    # Escalar si es muy grande
                    if npc_surf.get_width() > 600 or npc_surf.get_height() > 800:
                        npc_surf = pygame.transform.smoothscale(npc_surf, (500, int(500 * npc_surf.get_height() / npc_surf.get_width())))
                    
                    ix = (superficie.get_width() // 2) - npc_surf.get_width() - 50
                    iy = (superficie.get_height() - npc_surf.get_height()) // 2
                    superficie.blit(npc_surf, (ix, iy))
                except Exception as e:
                    print("No se pudo cargar la imagen del NPC en el overlay:", e)
            
            # Dibujar diálogo del NPC (Medio derecho)
            fnt_dialog = pygame.font.SysFont("georgia", 32, italic=True)
            texto = self._datos_dialogo.get("texto", "")
            
            # Separar texto en líneas para que no desborde
            palabras = texto.split(" ")
            lineas = []
            linea_actual = ""
            for p in palabras:
                if fnt_dialog.size(linea_actual + p + " ")[0] < 800:
                    linea_actual += p + " "
                else:
                    lineas.append(linea_actual)
                    linea_actual = p + " "
            if linea_actual:
                lineas.append(linea_actual)
                
            tx = (superficie.get_width() // 2) + 50
            ty = (superficie.get_height() - (len(lineas) * 40)) // 2
            
            for linea in lineas:
                rnd = fnt_dialog.render(linea, True, (255, 230, 200))
                superficie.blit(rnd, (tx, ty))
                ty += 40

        # Dibujar pantalla de debug si está activa
        if getattr(self, '_debug_visible', False) and not getattr(self, '_dialogo_fullscreen_visible', False) and not getattr(self, '_pantalla_final_visible', False):
            overlay = pygame.Surface((superficie.get_width(), superficie.get_height()), pygame.SRCALPHA)
            overlay.fill((10, 10, 10, 230))
            superficie.blit(overlay, (0, 0))
            
            fnt = pygame.font.SysFont("consolas", 16)
            
            import json
            # Recopilar variables
            estado = json.dumps(self.campania.estado.to_dict(), indent=2, ensure_ascii=False)
            contexto = json.dumps(self.campania.contexto.to_dict(), indent=2, ensure_ascii=False)
            mensaje = json.dumps(self.campania.obtener_mensaje_vista(), indent=2, ensure_ascii=False)

            texto_debug = f"=== ESTADO ===\n{estado}\n\n=== CONTEXTO ===\n{contexto}\n\n=== MENSAJE ===\n{mensaje}\n\n[Click en cualquier lado para cerrar]"
            
            lineas = texto_debug.split("\n")
            y_offset = 20
            for linea in lineas:
                # Cortar líneas muy largas para que no se desborde tanto
                if len(linea) > 150:
                    linea = linea[:147] + "..."
                superficie.blit(fnt.render(linea, True, (0, 255, 0)), (20, y_offset))
                y_offset += 20

        # Dibujar pantalla final si está activa
        if getattr(self, '_pantalla_final_visible', False):
            # Fondo negro absoluto
            superficie.fill((0, 0, 0))
            
            # Dibujar texto con scroll
            fnt_final = pygame.font.SysFont("georgia", 36, italic=True)
            texto = getattr(self, '_texto_final_generado', "")
            
            # Separar texto en líneas respetando saltos de línea y el ancho (max 1200)
            lineas_originales = texto.split("\n")
            lineas = []
            
            for linea_orig in lineas_originales:
                palabras = linea_orig.split(" ")
                linea_actual = ""
                for p in palabras:
                    if fnt_final.size(linea_actual + p + " ")[0] < 1200:
                        linea_actual += p + " "
                    else:
                        lineas.append(linea_actual)
                        linea_actual = p + " "
                if linea_actual:
                    lineas.append(linea_actual)
                
            y_texto = 100 + getattr(self, '_scroll_final_y', 0)
            for linea in lineas:
                # Solo dibujar si está en pantalla
                if -50 < y_texto < superficie.get_height() + 50:
                    rnd = fnt_final.render(linea, True, (255, 255, 255))
                    cx = (superficie.get_width() - rnd.get_width()) // 2
                    superficie.blit(rnd, (cx, y_texto))
                y_texto += 50
                
            # Dibujar imagen generada abajo del texto
            y_img = y_texto + 50
            if getattr(self, '_img_final_generada', None):
                img = self._img_final_generada
                # Solo dibujar si entra en pantalla
                if -img.get_height() < y_img < superficie.get_height() + 50:
                    ix = (superficie.get_width() - img.get_width()) // 2
                    superficie.blit(img, (ix, y_img))
                y_img += img.get_height() + 50
                
            # Limite de scroll (no permitir scrollear más abajo del final)
            limite = superficie.get_height() - y_img - 150
            if limite < 0 and self._scroll_final_y < limite:
                self._scroll_final_y = limite
                
            # Dibujar botón de reiniciar flotando siempre abajo
            fnt_reboot = pygame.font.SysFont("arial", 30, bold=True)
            txt_reboot = fnt_reboot.render("Haz click aquí para reiniciar", True, (200, 200, 255))
            cx_reboot = (superficie.get_width() - txt_reboot.get_width()) // 2
            
            # Fondo del botón
            pygame.draw.rect(superficie, (20, 20, 40), (cx_reboot - 20, 980, txt_reboot.get_width() + 40, 60))
            pygame.draw.rect(superficie, (100, 100, 200), (cx_reboot - 20, 980, txt_reboot.get_width() + 40, 60), 2)
            superficie.blit(txt_reboot, (cx_reboot, 995))

    def _reiniciar_juego(self):
        """Reinicia todo el estado de la campaña y la vista."""
        self.campania.reiniciar()
        
        # Resetear variables de vista
        self._pantalla_final_visible = False
        self._scroll_final_y = 0
        self._texto_final_generado = ""
        self._img_final_generada = None
        
        self.caja_entrada.limpiar()
        # Restaurar posición original (1080 - 140 - 20 = 920)
        self.caja_entrada.y = 920
        self.btn_send.y = 920
        
        if hasattr(self, 'btn_confirmar'):
            self.btn_confirmar.y = 3000
            
        self._actualizar_ui_con_resultados()
