#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# controlador_vista
#
# controlador_vista define el contrato o interfaz (IControladorVista) que la Vista
# gráfica requiere para comunicarse con el presentador o controlador del juego.
# Garantiza el desacoplamiento al no depender directamente de la lógica del modelo.
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ IControladorVista, clase abstracta que define la interfaz de comunicación.
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ obtener_narracion
#   --> Devuelve el bloque de texto principal de la escena (str).
# @ obtener_imagenes
#   --> Devuelve las rutas de imágenes en un diccionario (Dict).
# @ obtener_estado
#   --> Devuelve un diccionario con el estado actual de los personajes (dict).
# @ enviar_accion, recibe la acción en formato texto (str)
# @ reiniciar_aventura, notifica la orden de restablecer la partida
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from abc import ABC, abstractmethod
# abc define la infraestructura para clases abstractas
from typing import Dict, Optional
# typing define los tipos de datos estáticos para retornos y argumentos
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class IControladorVista(ABC):
    """
    Contrato (Interfaz) que define cómo la Vista se comunica con el exterior 
    (Controlador o Presentador) para obtener datos y enviar acciones.
    
    Asegura un desacoplamiento total: la Vista nunca importa el modelo ni 
    sabe cómo se procesan las reglas del juego. Cualquier clase que herede 
    de esta interfaz podrá ser inyectada en la vista, lo que facilita enormemente 
    la creación de Mocks para pruebas unitarias.
    """

    @abstractmethod
    def obtener_narracion(self) -> str:
        """
        Solicita el texto de la narración o diálogo principal actual.
        
        Returns:
            str: El bloque de texto a mostrar en el pergamino o caja de diálogo.
        """
        pass

    @abstractmethod
    def obtener_imagenes(self) -> Dict[str, Optional[str]]:
        """
        Solicita las rutas de las imágenes que deben mostrarse en este turno.
        
        Returns:
            Dict[str, Optional[str]]: Diccionario que mapea el tipo de imagen 
                                      con su ruta en disco. 
                                      Ejemplo: {'escena': 'ruta/a.png', 'npc': None}
        """
        pass

    @abstractmethod
    def obtener_estado(self) -> dict:
        """
        Solicita el estado actual de la partida y del jugador.
        
        Returns:
            dict: Estructura de datos limpia (independiente de las clases del modelo)
                  que contiene atributos como puntos de vida, objetos, estado de victoria, etc.
        """
        pass

    @abstractmethod
    def enviar_accion(self, accion: str) -> None:
        """
        Transmite al sistema la acción textual ingresada por el jugador.
        
        Args:
            accion (str): El texto exacto introducido en la CajaTexto.
        """
        pass

    @abstractmethod
    def reiniciar_aventura(self) -> None:
        """
        Notifica al sistema que el usuario ha solicitado reiniciar la partida
        por completo (volviendo al estado inicial).
        """
        pass
