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

        # 5. Marco Izquierdo (imagen_box.png)
        marco_izq = Imagen(
            x=100, y=150,
            ruta_imagen="Vista/resources/images/imagen_box.png",
            gestor_recursos=gestor_recursos,
            ancho=800, alto=800,
            alpha=True
        )
        self.agregar_widget(marco_izq)

        # Contenedor para la imagen generada por IA (dentro de marco_izq)
        self.imagen_escena = Imagen(
            x=100 + 40, y=150 + 40, # padding simulado
            ruta_imagen=None,
            gestor_recursos=gestor_recursos,
            ancho=800 - 80, alto=800 - 80,
            alpha=True,
            mantener_proporcion=True
        )
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
        self.texto_narracion.padding_x = 80
        self.texto_narracion.padding_y = 100
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
        btn_send = Boton(
            x=296 + 856 + 20, y=y_inferior,
            ruta_normal="Vista/resources/images/Send_Button_normal.png",
            ruta_hover="Vista/resources/images/Send_Button_hover.png",
            ruta_presionado="Vista/resources/images/Send_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=125, alto=alto_inferior,
            on_click=self._on_enviar_accion
        )
        self.agregar_widget(btn_send)

        # d. Botón Status (149x140)
        btn_state = Boton(
            x=btn_send.x + btn_send.ancho + 20, y=y_inferior,
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
            # Proximamente se implementa
            self.popup_reiniciar.cerrar()
            pass
            
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
            on_cerrar=lambda: None
        )
        self.agregar_widget(self.popup_estado)

        # 11. Modal de Tirada D20
        from Vista.widgets.popup_d20 import PopupD20
        self.popup_d20 = PopupD20(gestor_recursos)
        self.agregar_widget(self.popup_d20)

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
                self.mensaje_procesando = "Generando diálogos..."
                print("[IA] Dialogador...")
                self.campania.habla_personaje()
                
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
        if datos.get("dialogo"):
            narracion_final += f"\n\n---\n{datos['dialogo']}"
            
        self.texto_narracion.texto = narracion_final
        
        imagen_path = datos.get("imagen_resumen", "")
        if imagen_path:
            self.imagen_escena.cambiar_imagen(imagen_path)

    def manejar_evento(self, evento):
        # Si se levantó el flag de D20 desde un hilo
        if hasattr(self, '_abrir_d20_flag') and self._abrir_d20_flag:
            self._abrir_d20_flag = False
            dificultad = self.campania.get_contexto().get_dificultad()
            self.popup_d20.abrir(
                dificultad=dificultad,
                on_resultado=self._on_resultado_d20
            )
            
        # Si estamos procesando, bloqueamos clicks en la UI para evitar doble envío
        if self.procesando_ia:
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
        # Dibuja todos los widgets normalmente
        super().dibujar(superficie)
        
        # Superponer pantalla de carga si está procesando la IA
        if getattr(self, 'procesando_ia', False):
            import pygame
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
