from escenas.escena_base import EscenaBase
from widgets.imagen import Imagen

class EscenaJuego(EscenaBase):
    """
    Escena principal de la aplicación que representa la interfaz del Dungeon Master.
    """

    def __init__(self, gestor_recursos):
        """
        Inicializa la escena y carga los widgets estáticos iniciales.
        
        Args:
            gestor_recursos (GestorRecursos): Administrador de recursos para cargar assets.
        """
        super().__init__()
        
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
        from widgets.boton import Boton
            
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

        # 5. Marco Izquierdo (imagen_box.png)
        # Original: 2048x2048. Lo escalamos a 800x800
        marco_izq = Imagen(
            x=100, y=150,
            ruta_imagen="Vista/resources/images/imagen_box.png",
            gestor_recursos=gestor_recursos,
            ancho=800, alto=800,
            alpha=True
        )
        self.agregar_widget(marco_izq)

        # 6. Marco Derecho / Pergamino (pergamino_box.png)
        # Original: 2048x2048. Lo escalamos a 800x800
        marco_der = Imagen(
            x=1020, y=150,
            ruta_imagen="Vista/resources/images/pergamino_box.png",
            gestor_recursos=gestor_recursos,
            ancho=800, alto=800,
            alpha=True
        )
        self.agregar_widget(marco_der)

        # 7. Elementos inferiores
        # Vamos a escalar todos a un alto aproximado de 140px para que encajen bien
        alto_inferior = 140
        y_inferior = 1080 - alto_inferior - 20 # 20px de margen inferior

        # a. Barra de texto (Caja de entrada) (5088x832 -> 856x140)
        from widgets.caja_texto import CajaTexto
        caja_entrada = CajaTexto(
            x=296, y=y_inferior,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Barra_texto.png",
            ancho=856, alto=alto_inferior,
            placeholder="Escribe tu acción aquí...",
            max_longitud=500 # Ahora puede escribir textos muy largos gracias al scroll
        )
        # Ajustamos milimétricamente los márgenes para que el texto caiga
        # estrictamente dentro del papiro, ignorando las partes de madera.
        caja_entrada.padding_x = 175
        caja_entrada.padding_right = 140 # Un poco de margen para el lado derecho
        caja_entrada.padding_y = 50 
        caja_entrada.color_texto = (30, 20, 10) # Marrón muy oscuro
        caja_entrada.color_cursor = (30, 20, 10)
        self.agregar_widget(caja_entrada)

        # b. Botón Send (219x244 -> 125x140)
        btn_send = Boton(
            x=296 + 856 + 20, y=y_inferior,
            ruta_normal="Vista/resources/images/Send_Button_normal.png",
            ruta_hover="Vista/resources/images/Send_Button_hover.png",
            ruta_presionado="Vista/resources/images/Send_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=125, alto=alto_inferior
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
            
        from widgets.popup_confirmacion import PopupConfirmacion
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
        from widgets.popup_estado import PopupEstado
        self.popup_estado = PopupEstado(
            gestor_recursos=gestor_recursos,
            on_cerrar=lambda: None
        )
        self.agregar_widget(self.popup_estado)
