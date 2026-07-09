#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# popup_estado
#
# popup_estado implementa la clase PopupEstado que muestra la salud, ubicación
# e inventario actual del personaje mediante íconos temáticos de RPG y textos informativos.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ PopupEstado, clase que despliega la pantalla modal de ficha de personaje.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ manejar_evento, procesa clics del botón de cerrar y bloquea clics exteriores
# @ dibujar, dibuja la capa oscura y la ficha del personaje con sus datos
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
import pygame
# pygame maneja render de fuentes de texto y la composición de imágenes
from Vista.widgets.popup import Popup
# Popup es la clase modal que encapsula la estructura del popup
from Vista.widgets.boton import Boton
# Boton es el control utilizado para disparar la acción de cerrar
from Vista.widgets.imagen import Imagen
# Imagen es el control utilizado para colocar los íconos del inventario y salud
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class PopupEstado(Popup):
    """
    Popup que muestra el estado actual de la campaña y el personaje.
    Utiliza un oscurecimiento modal para no permitir clics fuera de él.
    """
    def __init__(self, gestor_recursos, campania=None, on_cerrar=None):
        # Configuramos el popup centrado
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
        
        self.campania = campania
        
        self.on_cerrar = on_cerrar
        self._fuente_titulo = pygame.font.Font(None, 42)
        self._fuente_texto = pygame.font.Font(None, 32)
        
        # 1. Botón Cerrar (Lo devolvemos a la esquina superior derecha del marco de madera)
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

        # 2. Íconos decorativos (Centrados en el pergamino, que va de x+330 a x+670 aprox)
        ico_status = Imagen(
            x=self.x + 330, y=self.y + 120,
            ruta_imagen="Vista/resources/images/UI_CharacterStatus.png",
            gestor_recursos=gestor_recursos,
            ancho=50, alto=50, alpha=True
        )
        self.agregar_widget(ico_status)

        # Salud / Vida
        ico_heart = Imagen(
            x=self.x + 335, y=self.y + 220,
            ruta_imagen="Vista/resources/images/UI_HeartIcon.png",
            gestor_recursos=gestor_recursos,
            ancho=40, alto=40, alpha=True
        )
        self.agregar_widget(ico_heart)

        # Inventario
        ico_backpack = Imagen(
            x=self.x + 335, y=self.y + 320,
            ruta_imagen="Vista/resources/images/UI_BackpackIcon.png",
            gestor_recursos=gestor_recursos,
            ancho=40, alto=40, alpha=True
        )
        self.agregar_widget(ico_backpack)
        
        # Ubicación / Llave
        ico_location = Imagen(
            x=self.x + 335, y=self.y + 420,
            ruta_imagen="Vista/resources/images/UI_KeyIcon.png",
            gestor_recursos=gestor_recursos,
            ancho=40, alto=40, alpha=True
        )
        self.agregar_widget(ico_location)

    def _cerrar_interno(self):
        self.cerrar()
        if self.on_cerrar:
            self.on_cerrar()

    def manejar_evento(self, evento):
        """Intercepta todos los eventos si está abierto (Modal)."""
        if not self.habilitado or not self.visible:
            return False

        for hijo in reversed(self._hijos):
            if hijo.habilitado:
                if hijo.manejar_evento(evento):
                    return True

        # Bloqueo Modal: Si hay click o movimiento de mouse fuera, lo bloqueamos 
        if evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            return True

        return False

    def dibujar(self, superficie):
        """Dibuja el oscurecimiento y luego el popup en sí con todos los textos mockeados."""
        if not self.visible:
            return

        # 1. Capa de oscurecimiento (Modal)
        overlay = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        superficie.blit(overlay, (0, 0))

        # 2. Dibujar fondo del popup y botones/iconos
        super().dibujar(superficie)
        
        # 3. Dibujar textos informativos (Bien apretados al ícono para que entren en el papel)
        color_texto = (40, 20, 10) # Marrón oscuro (Tinta)
        
        # Título
        txt_titulo = self._fuente_titulo.render("ESTADO DEL JUGADOR", True, color_texto)
        superficie.blit(txt_titulo, (self.x + 390, self.y + 130))
        
        # Datos reales
        salud = "Normal"
        inventario = "Vacío"
        ubicacion = "Desconocida"

        if hasattr(self, 'campania') and self.campania:
            estado = self.campania.get_estado()
            if estado:
                salud_heroe = estado.get_estado_personaje("heroe")
                if salud_heroe:
                    salud = salud_heroe

                objetos = [obj for obj in estado.objetos_heroe if obj]
                if objetos:
                    inventario = ", ".join(objetos)

                if estado.ubicacion:
                    ubicacion = estado.ubicacion

        txt_salud = self._fuente_texto.render(f"Salud: {salud}", True, color_texto)
        superficie.blit(txt_salud, (self.x + 385, self.y + 230))

        txt_inv = self._fuente_texto.render(f"Inv: {inventario}", True, color_texto)
        superficie.blit(txt_inv, (self.x + 385, self.y + 330))

        txt_ub = self._fuente_texto.render(f"Ubicación: {ubicacion}", True, color_texto)
        superficie.blit(txt_ub, (self.x + 385, self.y + 430))
