import streamlit as st

from clases.Campania import Campania

# --------------------------------------------------
# Inicialización
# --------------------------------------------------

if "campania" not in st.session_state:
    st.session_state.campania = Campania()
    st.session_state.estado_ui = "MENU"

campania = st.session_state.campania

# --------------------------------------------------
# ESTADO PARTIDA
# --------------------------------------------------

with st.sidebar:

    st.subheader("Estado de la partida")

    if st.button("Mostrar estado"):

        st.session_state.mostrar_estado = (
            not st.session_state.get(
                "mostrar_estado",
                False
            )
        )

    if st.session_state.get(
        "mostrar_estado",
        False
    ):

        st.json(
            campania.get_estado_()
        )

# --------------------------------------------------
# Pantalla MENU
# --------------------------------------------------

if st.session_state.estado_ui == "MENU":

    st.title("RPG Narrativo con IA")

    st.write("Rescata a la princesa cautiva en la cueva goblin.")

    if st.button("Comenzar"):
        st.session_state.estado_ui = "JUGANDO"
        st.rerun()

# --------------------------------------------------
# Pantalla JUGANDO
# --------------------------------------------------

elif st.session_state.estado_ui == "JUGANDO":

    mensaje = campania.get_mensaje()
    datos = mensaje.obtener_seccion_obligatoria()

    st.title("RPG Narrativo con IA")

    st.write(datos["narracion"])
    st.image(datos["imagen_resumen"], use_container_width=True)

    accion = st.text_input("¿Qué deseas hacer?")

    if st.button("Enviar"):

        campania.recibir_accion_jugador(accion)
        resultado = campania.arbitrar_accion_jugador()

        if not resultado["accion_valida"]:
            st.error("No puedes realizar esa acción.")
            st.rerun()

        if resultado["requiere_tirada"]:
            st.session_state.estado_ui = "ESPERANDO_D20"
        else:
            campania.no_requiere_tirada()
            st.session_state.estado_ui = "PROCESANDO"

        st.rerun()

# --------------------------------------------------
# Pantalla ESPERANDO_D20
# --------------------------------------------------

elif st.session_state.estado_ui == "ESPERANDO_D20":

    st.subheader("Tirada requerida")

    st.write(
        f"Dificultad: {campania.get_contexto().get_dificultad()}"
    )

    if st.button("Lanzar D20"):

        resultado = campania.resolver_tirada()
        st.session_state.resultado_tirada = resultado

        st.session_state.estado_ui = "PROCESANDO"
        st.rerun()

# --------------------------------------------------
# Pantalla PROCESANDO
# --------------------------------------------------

elif st.session_state.estado_ui == "PROCESANDO":

    st.title("⚙️ Procesando acción...")
    st.info("Generando narrativa, decisiones, NPC e imagen...")

    step = st.session_state.get("proceso_step", 0)

    try:

        # =========================
        # STEP 0 - NARRACIÓN
        # =========================
        if step == 0:
            print("[DEBUG] narracion()")
            with st.spinner("Narración..."):
                campania.narracion()

            st.session_state.proceso_step = 1
            st.rerun()

        # =========================
        # STEP 1 - ORQUESTADOR
        # =========================
        elif step == 1:
            print("[DEBUG] orquestador()")
            with st.spinner("Orquestador..."):
                campania.orquestador()

            st.session_state.proceso_step = 2
            st.rerun()

        # =========================
        # STEP 2 - FINALES
        # =========================
        elif step == 2:
            print("[DEBUG] verificar_finales()")
            with st.spinner("Verificando finales..."):
                campania.verificar_finales()

            st.session_state.proceso_step = 3
            st.rerun()

        # =========================
        # STEP 3 - NPC
        # =========================
        elif step == 3:
            print("[DEBUG] habla_personaje()")

            with st.spinner("NPC..."):
                if campania.get_mensaje().hay_dialogo_npc():
                    campania.habla_personaje()

            st.session_state.proceso_step = 4
            st.rerun()

        # =========================
        # STEP 4 - IMAGEN
        # =========================
        elif step == 4:
            print("[DEBUG] generar_imagen_resumen()")

            with st.spinner("Imagen..."):
                campania.generar_imagen_resumen()

            print("[DEBUG] PROCESADO OK -> MOSTRAR_RESULTADO")

            st.session_state.proceso_step = 0
            st.session_state.estado_ui = "MOSTRAR_RESULTADO"
            st.rerun()

    except Exception as e:

        print("\n" + "=" * 80)
        print("💥 ERROR CRÍTICO EN PROCESO")
        print("=" * 80)

        print("[TIPO]")
        print(type(e).__name__)

        print("\n[ERROR]")
        print(str(e))

        import traceback
        print("\n[TRACEBACK]")
        traceback.print_exc()

        print("\n[ESTADO ACTUAL]")
        try:
            print(campania.get_estado_())
        except:
            print("No se pudo imprimir estado")

        st.error("💥 ERROR EN PROCESAMIENTO")
        st.exception(e)

        st.stop()

# --------------------------------------------------
# Pantalla RESULTADOS
# --------------------------------------------------

elif st.session_state.estado_ui == "MOSTRAR_RESULTADO":

    try:

        print("\n" + "=" * 80)
        print("MOSTRAR_RESULTADO")
        print("=" * 80)

        st.title("Resultado de la acción")

        mensaje = campania.get_mensaje()

        print("[DEBUG] get_mensaje() OK")

        datos = mensaje.obtener_mensaje_completo()

        print("[DEBUG] obtener_mensaje_completo() OK")
        print(datos)

        # -------------------------
        # NARRACION PRINCIPAL
        # -------------------------

        st.subheader("Narración")

        st.write(
            datos.get(
                "narracion",
                "Sin narración"
            )
        )

        # -------------------------
        # IMAGEN PRINCIPAL
        # -------------------------

        try:

            imagen = datos.get(
                "imagen_resumen",
                None
            )

            if imagen is not None:

                print("[DEBUG] mostrando imagen_resumen")

                st.image(
                    imagen,
                    width="stretch"
                )

            else:

                print("[DEBUG] imagen_resumen = None")

                st.info(
                    "Imagen no disponible debido a falta de tokens"
                )

        except Exception as e:

            print("[ERROR imagen_resumen]")
            print(str(e))

            st.warning(
                "Error mostrando imagen - Falla debido a tokens"
            )

        # -------------------------
        # NPC
        # -------------------------

        try:

            narracion_npc = datos.get(
                "narracion_npc",
                None
            )

            if narracion_npc:

                print("[DEBUG] mostrando NPC")

                st.subheader("Personaje")

                st.write(
                    narracion_npc
                )

                imagen_npc = datos.get(
                    "imagen_npc",
                    None
                )

                if imagen_npc is not None:

                    try:

                        st.image(
                            imagen_npc,
                            width="stretch"
                        )

                    except Exception as e:

                        print(
                            "[ERROR imagen_npc debido a falta de tokens]"
                        )

                        print(str(e))

                dialogo_npc = datos.get(
                    "dialogo_npc",
                    None
                )

                if dialogo_npc:

                    st.info(
                        dialogo_npc
                    )

        except Exception as e:

            print("[ERROR BLOQUE NPC]")
            print(str(e))

            st.warning(
                "Error mostrando NPC debido a falta de tokens"
            )

        # -------------------------
        # FINAL
        # -------------------------

        try:

            print(
                "[DEBUG] final actual:",
                campania.estado.final
            )

            if campania.estado.final != "sin_final":

                st.error(
                    f"FIN DEL JUEGO: {campania.estado.final}"
                )

                if st.button("Siguiente"):

                    st.session_state.estado_ui = "FINAL"

                    st.rerun()

            else:

                accion = st.text_input(
                    "¿Qué deseas hacer ahora?"
                )

                if st.button("Enviar"):

                    campania.recibir_accion_jugador(
                        accion
                    )

                    resultado = (
                        campania.arbitrar_accion_jugador()
                    )

                    if not resultado["accion_valida"]:

                        st.error(
                            "No puedes realizar esa acción."
                        )

                    else:

                        if resultado["requiere_tirada"]:

                            st.session_state.estado_ui = (
                                "ESPERANDO_D20"
                            )

                        else:

                            campania.no_requiere_tirada()

                            st.session_state.estado_ui = (
                                "PROCESANDO"
                            )

                    st.rerun()

        except Exception as e:

            print("[ERROR BLOQUE FINAL]")
            print(str(e))

            raise

    except Exception as e:

        import traceback

        print("\n" + "=" * 80)
        print("💥 ERROR EN MOSTRAR_RESULTADO")
        print("=" * 80)

        traceback.print_exc()

        st.error(
            "Error en MOSTRAR_RESULTADO"
        )

        st.exception(e)

# --------------------------------------------------
# Pantalla FINAL
# --------------------------------------------------

elif st.session_state.estado_ui == "FINAL":

    st.title("FIN DE LA AVENTURA")
    campania.narracion_final()
    try:
        campania.generar_imagen_resumen()
    except Exception as e:
        print("[Error generando la imagen debido a falta de tokens]")
        print(str(e))
    mensaje = campania.obtener_mensaje_vista()
    st.write(mensaje["narracion"])
    st.image(
        mensaje["imagen_resumen"],
        use_container_width=True
    )
    if st.button("Reiniciar aventura"):
        campania.reiniciar()
        st.rerun()

    def safe_step(nombre, fn):
        try:
            print(f"\n🔥 INICIO: {nombre}")
            result = fn()
            print(f"✅ OK: {nombre}")
            return result
        except Exception as e:
            print(f"\n💥 ERROR EN: {nombre}")
            print(str(e))
            st.error(f"Error en {nombre}")
            st.exception(e)
            raise