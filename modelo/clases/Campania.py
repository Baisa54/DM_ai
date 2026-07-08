#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
# Campania
#
# Campania es el encargado de manejar la partida
# 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ELEMENTOS
#
# @ ContextoJuego, clase que se encarga de manejar el contexto de la partida
# @ EstadoJuego, clase que se encarga de manejar el estado de la partida
# @ MensajeJuego, clase que se encarga de manejar el mensaje de la partida
# @ arbitrar_accion, funcion que se encarga de arbitrar la accion del jugador
# @ generar_imagen_escena, funcion que se encarga de generar la imagen de la escena
# @ tirar_d20, funcion que se encarga de tirar el dado d20
# @ verificar_tirada, funcion que se encarga de verificar la tirada
# @ PERSONAJES, diccionario que se encarga de manejar los personajes
# @ gen_state, funcion que se encarga de generar el estado
# @ genMessage, funcion que se encarga de generar el mensaje
# @ narrar_accion, funcion que se encarga de generar la narracion de la accion
# @ narrar_final, funcion que se encarga de generar el final de la historia
# @ orquestar_narracion, funcion que se encarga de orquestar la narracion
# @ verificar_finales, funcion que se encarga de verificar los finales
# @ generar_imagen_dialogo, funcion que se encarga de generar la imagen del dialogo
# @ dialogador, funcion que se encarga de dialogar
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# INPUTS
# 
# @ arbitrar_accion_jugador, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# @ resolver_tirada, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# @ narracion, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# @ orquestador, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# @ verificar_finales, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# @ dialogador, recibe como parametro el estado de la partida
#   --> Devuelve el estado de la partida
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Imports
from modelo.clases.ContextoJuego import ContextoJuego
# ContextoJuego es el encargado de manejar el contexto de la partida
from modelo.clases.Estadojuego import EstadoJuego
# EstadoJuego es el encargado de manejar el estado de la partida
from modelo.clases.MensajeJuego import MensajeJuego
# MensajeJuego es el encargado de manejar el mensaje de la partida
from modelo.ai.arbitro_accion import arbitrar_accion
# arbitrar_accion es el encargado de arbitrar la accion del jugador
from modelo.ai.generador_imagen_escena import generar_imagen_escena
# generar_imagen_escena es el encargado de generar la imagen de la escena
from modelo.tools.dice import tirar_d20, verificar_tirada
# tirar_d20 es el encargado de tirar el dado d20
# verificar_tirada es el encargado de verificar la tirada
from modelo.game.characters import PERSONAJES
# PERSONAJES es el encargado de manejar los personajes
from modelo.tools.gen_state import gen_state
# gen_state es el encargado de generar el estado inicial
from modelo.tools.gen_messege import genMessage
# genMessage es el encargado de generar el mensaje inicial
from modelo.ai.narrador import narrar_accion, narrar_final
# narrar_accion es el encargado de generar la narracion de la accion
# narrar_final es el encargado de generar el final de la historia
from modelo.ai.Orquestador_estado import orquestar_narracion
# orquestar_narracion es el encargado de orquestar la narracion
from modelo.ai.Verificador_finales import verificar_final
# verificar_final es el encargado de verificar los finales
from modelo.ai.imagen_NPC import generar_imagen_dialogo
# generar_imagen_dialogo es el encargado de generar la imagen del dialogo
from modelo.ai.dialogador import dialogador
# dialogador es el encargado de dialogar
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Campania:

    def __init__(self):

        self.estado_ui = "MENU"

        self.contexto = ContextoJuego()

        self.estado = gen_state()

        self.mensaje = genMessage()

    def reiniciar(self):

        self.estado_ui = "MENU"
        self.contexto = ContextoJuego()
        self.estado = gen_state()
        self.mensaje = genMessage()

    def get_contexto(self):

        return self.contexto

    def get_estado(self):

        return self.estado

    def get_mensaje(self):

        return self.mensaje

    def set_contexto(
        self,
        contexto
    ):

        self.contexto = contexto

    def set_estado(
        self,
        estado
    ):

        self.estado = estado

    def set_mensaje(
        self,
        mensaje
    ):

        self.mensaje = mensaje

    def recibir_accion_jugador(
        self,
        accion
    ):

        self.contexto.set_prompt_jugador(
            accion
        )

        self.contexto.set_estado(
            self.estado
        )

    def arbitrar_accion_jugador(self):

        resultado = arbitrar_accion(
            self.contexto.get_prompt_jugador(),
            self.contexto.get_estado()
        )

        self.contexto.set_accion_valida(
            resultado["accion_valida"]
        )

        self.contexto.set_requiere_tirada(
            resultado["requiere_tirada"]
        )

        self.contexto.set_dificultad(
            resultado["dificultad"]
        )

        return resultado

    def resolver_tirada(self):

        resultado_d20 = tirar_d20()

        resultado = verificar_tirada(
            resultado_d20,
            self.contexto.get_dificultad()
        )

        if resultado["tipo"] == "pifia":

            self.contexto.set_resultado_d20(
                "pifia"
            )

        elif resultado["tipo"] == "critico":

            self.contexto.set_resultado_d20(
                "critico"
            )

        elif resultado["exito"]:

            self.contexto.set_resultado_d20(
                "exito"
            )

        else:

            self.contexto.set_resultado_d20(
                "fracaso"
            )

        return {
            "tirada": resultado_d20,
            "resultado": self.contexto.get_resultado_d20()
        }
    
    def no_requiere_tirada(self):
        self.contexto.set_exito()

    def narracion(self):

        texto = narrar_accion(
            self.contexto.get_prompt_jugador(),
            self.estado,
            self.contexto.get_resultado_d20()
        )

        self.mensaje.set_narracion(texto)

    def orquestador(self):

        resultado = orquestar_narracion(
            self.mensaje.get_narracion()
        )

        # -------------------------
        # VIDA / ESTADOS PERSONAJE
        # -------------------------
        vida = resultado.get("vida", {})

        for personaje, cambio in vida.items():

            if cambio == "Sin cambios":
                continue

            estado_actual = self.estado.get_estado_personaje(personaje)

            # -------------------------
            # APLICAR DAÑO
            # -------------------------
            if cambio == "daño":

                if estado_actual == "normal":
                    nuevo_estado = "herido"

                elif estado_actual == "herido":
                    nuevo_estado = "gravemente_herido"

                elif estado_actual == "gravemente_herido":
                    nuevo_estado = "muerto"

                elif estado_actual == "muerto":
                    nuevo_estado = "muerto"

                else:
                    nuevo_estado = estado_actual

                self.estado.set_estado_personaje(personaje, nuevo_estado)

            # -------------------------
            # APLICAR CURA
            # -------------------------
            elif cambio == "se cura":

                if estado_actual == "gravemente_herido":
                    nuevo_estado = "herido"

                elif estado_actual == "herido":
                    nuevo_estado = "normal"

                elif estado_actual == "normal":
                    nuevo_estado = "normal"

                elif estado_actual == "muerto":
                    nuevo_estado = "muerto"

                else:
                    nuevo_estado = estado_actual

                self.estado.set_estado_personaje(personaje, nuevo_estado)

        # -------------------------
        # OBJETOS
        # -------------------------
        objetos = resultado.get("objeto", {})

        estado_objeto = objetos.get("heroe", "Sin cambios")
        nombre_objeto = objetos.get("name_obj", None)

        if estado_objeto != "Sin cambios" and nombre_objeto is not None:

            if estado_objeto == "Pierde":
                self.estado.quitar_objeto_heroe(nombre_objeto)

            elif estado_objeto == "Obtiene":
                self.estado.agregar_objeto_heroe(nombre_objeto)

        # -------------------------
        # SALA
        # -------------------------
        sala = resultado.get("sala", "Sin cambios")

        salas_validas = [
            "entrada_cueva",
            "puerta_goblins",
            "gran_salon",
            "sala_osgo"
        ]

        if sala in salas_validas:

            self.estado.set_ubicacion(sala)

        # -------------------------
        # NPC HABLA
        # -------------------------
        npc_habla = resultado.get("npc_habla", False)

        if npc_habla:

            self.habla_personaje()

    def verificar_finales(self):

        resultado = verificar_final(
            self.estado,
            self.mensaje.get_narracion()
        )

        self.estado.set_final(
            resultado["final"]
        )
        return resultado


    def habla_personaje(self):

        resultado = dialogador(
            self.mensaje.get_narracion()
        )

        narracion_actual = self.mensaje.get_narracion()

        self.mensaje.set_narracion(
            resultado["Narracion"] or narracion_actual
        )

        self.mensaje.set_dialogo_npc(
            resultado["dialogo"],
            self.mensaje.get_imagen_npc() 
        )

        personaje = resultado.get("Personaje")

        if not personaje:
            return

        emocion = resultado["Emocion"]
        personaje_data = PERSONAJES[personaje]

        imagen_generada = generar_imagen_dialogo(
            personaje_data,
            emocion
        )

        self.mensaje.set_imagen_npc(
            imagen_generada["imagen"]
        )
        
    def generar_imagen_resumen(self):

        imagen = generar_imagen_escena(
            self.mensaje.get_narracion(),
            self.estado.obtener_imagenes_escena()
        )

        if imagen is not None:

            self.mensaje.set_imagen_resumen(imagen)

        else:

            print("[DEBUG] imagen no generada")
        
    def obtener_mensaje_vista(self):

        return self.mensaje.obtener_mensaje_completo()

    def limpiar_mensaje(self):
        
        self.mensaje.limpiar_dialogo_npc()

    def narracion_final(self):

        texto = narrar_final(
            self.estado,
            self.contexto.get_prompt_jugador(),
            self.contexto.get_resultado_d20()
        )

        self.mensaje.set_narracion(texto)

    def get_estado_(self):
        return self.estado.to_dict()