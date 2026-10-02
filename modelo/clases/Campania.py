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
from modelo.ai.Orquestador_estado import orquestar_accion
# orquestar_accion es el encargado de actualizar el estado de la partida
from modelo.ai.Verificador_finales import verificar_final
# verificar_final es el encargado de verificar los finales
from modelo.ai.imagen_NPC import generar_imagen_dialogo
# generar_imagen_dialogo es el encargado de generar la imagen del dialogo
from modelo.ai.dialogador import dialogador
# dialogador es el encargado de dialogar
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#

class Campania:
    """
    Controlador principal de la lógica de juego y máquina de estados de la campaña.
    """

    def __init__(self):
        """
        Inicializa una nueva campaña de juego creando el estado inicial, contexto y mensaje inicial.
        """
        self.estado_ui = "MENU"
        self.contexto = ContextoJuego()
        self.estado = gen_state()
        self.mensaje = genMessage()

    def reiniciar(self):
        """
        Reinicia la partida a su estado inicial limando el contexto y la historia.
        """
        self.estado_ui = "MENU"
        self.contexto = ContextoJuego()
        self.estado = gen_state()
        self.mensaje = genMessage()

    def get_contexto(self):
        """
        Obtiene el objeto ContextoJuego actual de la partida.
        """
        return self.contexto

    def get_estado(self):
        """
        Obtiene el objeto EstadoJuego actual de la partida.
        """
        return self.estado

    def get_mensaje(self):
        """
        Obtiene el objeto MensajeJuego actual de la partida.
        """
        return self.mensaje

    def set_contexto(self, contexto):
        """
        Establece la referencia del objeto ContextoJuego.
        """
        self.contexto = contexto

    def set_estado(self, estado):
        """
        Establece la referencia del objeto EstadoJuego.
        """
        self.estado = estado

    def set_mensaje(self, mensaje):
        """
        Establece la referencia del objeto MensajeJuego.
        """
        self.mensaje = mensaje

    def recibir_accion_jugador(self, accion):
        """
        Registra la acción enviada por el jugador en el contexto actual.
        """
        self.contexto.set_prompt_jugador(accion)
        self.contexto.set_estado(self.estado)

    def arbitrar_accion_jugador(self):
        """
        Invoca al árbitro de IA para determinar si la acción es válida, si requiere tirada de dado D20 y su dificultad.
        """
        resultado = arbitrar_accion(
            self.contexto.get_prompt_jugador(),
            self.contexto.get_estado()
        )

        self.contexto.set_accion_valida(resultado["accion_valida"])
        self.contexto.set_requiere_tirada(resultado["requiere_tirada"])
        self.contexto.set_dificultad(resultado["dificultad"])

        return resultado

    def resolver_tirada(self):
        """
        Ejecuta la tirada de dado D20 aleatoria y evalúa su éxito, fracaso, pifia o crítico contra la dificultad.
        """
        resultado_d20 = tirar_d20()

        resultado = verificar_tirada(
            resultado_d20,
            self.contexto.get_dificultad()
        )

        if resultado["tipo"] == "pifia":
            self.contexto.set_resultado_d20("pifia")
        elif resultado["tipo"] == "critico":
            self.contexto.set_resultado_d20("critico")
        elif resultado["exito"]:
            self.contexto.set_resultado_d20("exito")
        else:
            self.contexto.set_resultado_d20("fracaso")

        return {
            "tirada": resultado_d20,
            "resultado": self.contexto.get_resultado_d20()
        }
    
    def no_requiere_tirada(self):
        """
        Marca la acción del turno como exitosa automáticamente al no requerir tirada de dados.
        """
        self.contexto.set_exito()

    def narracion(self):
        """
        Invoca al generador de narración IA para generar la respuesta narrativa basada en la acción y el resultado.
        """
        texto = narrar_accion(
            self.contexto.get_prompt_jugador(),
            self.estado,
            self.contexto.get_resultado_d20(),
            getattr(self, "ubicacion_anterior", None)
        )

        self.mensaje.set_narracion(texto)

    def orquestador(self):
        """
        Analiza las consecuencias de la acción en el estado del juego (cambios de sala, salud, objetos y diálogos de NPC).
        """
        self.ubicacion_anterior = self.estado.get_ubicacion()

        resultado = orquestar_accion(
            self.contexto.get_prompt_jugador(),
            self.contexto.get_resultado_d20(),
            self.estado
        )

        # -------------------------
        # HISTORIAL DE ACCIONES
        # -------------------------
        resumen_accion = resultado.get("accion_Jugador", "")
        if resumen_accion:
            self.estado.agregar_decision(resumen_accion)

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

        if isinstance(estado_objeto, str) and estado_objeto.strip().lower() != "sin cambios" and nombre_objeto:
            
            estado_limpio = estado_objeto.strip().lower()

            if "pierde" in estado_limpio:
                self.estado.quitar_objeto_heroe(str(nombre_objeto).strip())

            elif "obtiene" in estado_limpio:
                self.estado.agregar_objeto_heroe(str(nombre_objeto).strip())

        # -------------------------
        # SALA
        # -------------------------
        sala = resultado.get("sala", "Sin cambios")
        ubicacion_actual = self.estado.get_ubicacion()

        from modelo.game.campaign import SALAS
        
        if sala != "Sin cambios" and sala in SALAS:
            salidas_validas = SALAS.get(ubicacion_actual, {}).get("salidas", [])
            if sala in salidas_validas or sala == ubicacion_actual:
                self.estado.set_ubicacion(sala)
            else:
                print(f"[Orquestador] SALTO INVÁLIDO IGNORADO: De {ubicacion_actual} a {sala}. Solo permitidas: {salidas_validas}")

        # -------------------------
        # NPC HABLA
        # -------------------------
        npc_habla = resultado.get("npc_habla", False)

        if npc_habla:
            self.habla_personaje()

    def verificar_finales(self):
        """
        Verifica si la narración o estado actual activa una condición de final de partida.
        """
        resultado = verificar_final(
            self.estado,
            self.mensaje.get_narracion()
        )

        self.estado.set_final(resultado["final"])
        return resultado

    def habla_personaje(self):
        """
        Procesa e identifica diálogos hablados por NPCs en la narración actual.
        """
        resultado = dialogador(
            self.mensaje.get_narracion(),
            self.estado.personajes_presentes
        )

        narracion_actual = self.mensaje.get_narracion()
        narracion_limpia = resultado.get("Narracion") or narracion_actual
        dialogo = resultado.get("dialogo")
        personaje = resultado.get("Personaje")
        
        if personaje and dialogo:
            import re
            narracion_limpia = re.sub(r'[:,]\s*\"[^\"]*\"', '.', narracion_limpia)
            narracion_limpia = re.sub(r'\"[^\"]*\"', '', narracion_limpia)
            if dialogo in narracion_limpia:
                narracion_limpia = narracion_limpia.replace(dialogo, "")
            
            narracion_limpia = narracion_limpia.replace('..', '.').replace(' .', '.').strip()

        self.mensaje.set_narracion(narracion_limpia)

        if personaje:
            personaje_data = PERSONAJES.get(personaje)
            if personaje_data and "imagen" in personaje_data:
                self.mensaje.set_imagen_npc(personaje_data["imagen"])

        self.mensaje.set_dialogo_npc(
            dialogo,
            self.mensaje.get_imagen_npc() 
        )
        
    def generar_imagen_resumen(self):
        """
        Genera la imagen descriptiva ilustrada del estado actual de la escena.
        """
        from modelo.configuracion import ConfigManager
        if not ConfigManager().get_generar_imagenes():
            print("[INFO] Generación de imágenes desactivada en configuración: omitiendo síntesis.")
            self.mensaje.set_imagen_resumen(None)
            return

        from modelo.game.campaign import SALAS
        ubicacion_actual = self.estado.get_ubicacion()
        descripcion_sala = SALAS.get(ubicacion_actual, {}).get("descripcion", "")

        imagen = generar_imagen_escena(
            self.mensaje.get_narracion(),
            self.estado.obtener_imagenes_escena(),
            descripcion_sala,
            self.estado.obtener_rutas_imagenes_personajes()
        )

        if imagen is not None:
            self.mensaje.set_imagen_resumen(imagen)
        else:
            print("[DEBUG] imagen no generada")
            self.mensaje.set_imagen_resumen(None)
        
    def obtener_mensaje_vista(self):
        """
        Obtiene el diccionario serializado del mensaje para ser consumido por la vista gráfica.
        """
        return self.mensaje.obtener_mensaje_completo()

    def limpiar_mensaje(self):
        """
        Limpia los campos del mensaje para preparar el siguiente turno.
        """
        self.mensaje.limpiar_dialogo_npc()

    def narracion_final(self):
        """
        Genera la narración de conclusión o epílogo al finalizar la campaña.
        """
        texto = narrar_final(
            self.estado,
            self.contexto.get_prompt_jugador(),
            self.contexto.get_resultado_d20()
        )

        self.mensaje.set_narracion(texto)

    def get_estado_(self):
        """
        Obtiene el estado en formato de diccionario.
        """
        return self.estado.to_dict()