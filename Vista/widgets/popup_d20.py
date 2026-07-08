#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# popup_d20
#
# popup_d20 implementa PopupD20, un cuadro de diálogo modal e interactivo que solicita
# al jugador lanzar un dado d20 para resolver una tirada requerida por la campaña,
# mostrando efectos visuales del dado girando y desplegando el resultado obtenido
# (Éxito, Fallida, Crítico o Pifia) según la dificultad dada.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PopupD20, clase que gestiona la lógica y renderizado de la tirada de dados d20.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ abrir, recibe la dificultad de la tirada (int) y un callback (callable)
# @ actualizar, maneja el tiempo y la animación de la tirada
# @ manejar_evento, gestiona los clics en los botones del popup de forma modal
# @ dibujar, dibuja el overlay modal, el fondo, el dado y los textos del resultado
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame maneja renderizado, fuentes y superficies
import random
# random genera el valor aleatorio de la tirada d20
import time
# time controla los fotogramas y la duración de la animación
from Vista.widgets.popup import Popup
# Popup es la clase base para el comportamiento modal contenedor
from Vista.widgets.boton import Boton
# Boton es el componente interactivo usado para lanzar y continuar
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class PopupD20(Popup):
    def __init__(self, gestor_recursos):
        ancho_popup = 1000
        alto_popup = 700
        x_popup = (1920 - ancho_popup) // 2
        y_popup = (1080 - alto_popup) // 2
        
        super().__init__(
            x=x_popup, y=y_popup,
            gestor_recursos=gestor_recursos,
            ruta_fondo="Vista/resources/images/Popup.png",
            ancho=ancho_popup,
            alto=alto_popup
        )
        
        self.dificultad = 10
        self.resultado = None
        self.on_resultado = None
        
        # Animación
        self._rolling = False
        self._roll_start_time = 0
        self._ultimo_cambio_num = 0
        self._temp_num = 1
        
        self._fuente_titulo = pygame.font.Font(None, 48)
        self._fuente_subtitulo = pygame.font.Font(None, 36)
        self._fuente_gigante = pygame.font.Font(None, 120)
        
        # Botón del Dado (Centro, manteniendo aspecto 275x150)
        self._btn_tirar = Boton(
            x=self.x + (self.ancho - 275) // 2,
            y=self.y + 270,
            ruta_normal="Vista/resources/images/UI_D20Icon.png",
            ruta_hover="Vista/resources/images/UI_D20Icon.png",
            ruta_presionado="Vista/resources/images/UI_D20Icon.png",
            gestor_recursos=gestor_recursos,
            ancho=275, alto=150,
            on_click=self._iniciar_tirada
        )
        self.agregar_widget(self._btn_tirar)
        
        # Botón Aceptar/Continuar (Abajo centro, inicialmente invisible)
        self._btn_continuar = Boton(
            x=self.x + (self.ancho - 250) // 2,
            y=self.y + 530,
            ruta_normal="Vista/resources/images/Confirm_Button_normal.png",
            ruta_hover="Vista/resources/images/Confirm_Button_hover.png",
            ruta_presionado="Vista/resources/images/Confirm_Button_pressed.png",
            gestor_recursos=gestor_recursos,
            ancho=250, alto=100,
            on_click=self._finalizar_tirada
        )
        self._btn_continuar.visible = False
        self._btn_continuar.habilitado = False
        self.agregar_widget(self._btn_continuar)

    def abrir(self, dificultad=10, on_resultado=None):
        self.dificultad = dificultad
        self.on_resultado = on_resultado
        self.resultado = None
        self._rolling = False
        
        self._btn_tirar.visible = True
        self._btn_tirar.habilitado = True
        self._btn_continuar.visible = False
        self._btn_continuar.habilitado = False
        
        super().abrir()

    def _iniciar_tirada(self):
        snd_click = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/click.wav")
        if snd_click:
            snd_click.play()
        snd_roll = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/dice_roll.wav")
        if snd_roll:
            snd_roll.play()
            
        self._rolling = True
        self._roll_start_time = time.time()
        self._ultimo_cambio_num = 0
        self._btn_tirar.visible = False
        self._btn_tirar.habilitado = False

    def _finalizar_tirada(self):
        snd_click = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/click.wav")
        if snd_click:
            snd_click.play()
        self.cerrar()
        if self.on_resultado:
            if self.resultado == 1:
                tipo = "pifia"
            elif self.resultado == 20:
                tipo = "critico"
            elif self.resultado >= self.dificultad:
                tipo = "exito"
            else:
                tipo = "fallida"
            self.on_resultado(self.resultado, tipo)

    def actualizar(self):
        super().actualizar()
        
        if self._rolling:
            if time.time() - self._roll_start_time > 0.8:
                self._rolling = False
                self.resultado = random.randint(1, 20)
                
                # Sonidos según el resultado
                if self.resultado >= self.dificultad or self.resultado == 20:
                    snd_win = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/success.wav")
                    if snd_win:
                        snd_win.play()
                else:
                    snd_fail = self._gestor_recursos.obtener_sonido("Vista/resources/sounds/failure.wav")
                    if snd_fail:
                        snd_fail.play()
                        
                self._btn_continuar.visible = True
                self._btn_continuar.habilitado = True

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

        # 1. Overlay modal oscuro de 1920x1080
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        superficie.blit(overlay, (0, 0))

        # 2. Dibujar fondo de Popup y botones
        super().dibujar(superficie)

        # 3. Dibujar textos
        color_texto = (40, 20, 10)
        
        txt_titulo = self._fuente_titulo.render("TIRADA DE DADO D20", True, color_texto)
        rect_titulo = txt_titulo.get_rect(center=(self.x + self.ancho // 2, self.y + 160))
        superficie.blit(txt_titulo, rect_titulo)
 
        txt_dif = self._fuente_subtitulo.render(f"Dificultad Requerida: {self.dificultad}", True, color_texto)
        rect_dif = txt_dif.get_rect(center=(self.x + self.ancho // 2, self.y + 210))
        superficie.blit(txt_dif, rect_dif)
 
        if self._rolling:
            tiempo_actual = time.time()
            if tiempo_actual - self._ultimo_cambio_num > 0.05:
                self._temp_num = random.randint(1, 20)
                self._ultimo_cambio_num = tiempo_actual
            
            txt_num = self._fuente_gigante.render(str(self._temp_num), True, (120, 80, 50))
            rect_num = txt_num.get_rect(center=(self.x + self.ancho // 2, self.y + 345))
            superficie.blit(txt_num, rect_num)
            
            txt_msg = self._fuente_subtitulo.render("Lanzando...", True, (80, 80, 80))
            rect_msg = txt_msg.get_rect(center=(self.x + self.ancho // 2, self.y + 450))
            superficie.blit(txt_msg, rect_msg)
 
        elif self.resultado is not None:
            txt_num = self._fuente_gigante.render(str(self.resultado), True, color_texto)
            rect_num = txt_num.get_rect(center=(self.x + self.ancho // 2, self.y + 345))
            superficie.blit(txt_num, rect_num)
 
            if self.resultado == 1:
                tipo_str = "PIFIA"
                color_res = (200, 0, 0) # Rojo
            elif self.resultado == 20:
                tipo_str = "CRÍTICO"
                color_res = (0, 150, 0) # Verde
            elif self.resultado >= self.dificultad:
                tipo_str = "ÉXITO"
                color_res = (0, 120, 0) # Verde oscuro
            else:
                tipo_str = "FALLIDA"
                color_res = (120, 40, 40) # Rojo oscuro
                
            txt_tipo = self._fuente_titulo.render(tipo_str, True, color_res)
            rect_tipo = txt_tipo.get_rect(center=(self.x + self.ancho // 2, self.y + 450))
            superficie.blit(txt_tipo, rect_tipo)
        else:
            txt_instruccion = self._fuente_subtitulo.render("Haz clic en el dado para lanzar", True, color_texto)
            rect_instruccion = txt_instruccion.get_rect(center=(self.x + self.ancho // 2, self.y + 450))
            superficie.blit(txt_instruccion, rect_instruccion)
