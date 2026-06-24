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

    st.title("Procesando...")

    campania.narracion()

    campania.orquestador()

    final = campania.verificar_finales() 

    if campania.get_mensaje().hay_dialogo_npc():
        campania.habla_personaje()

    campania.generar_imagen_resumen()

    st.session_state.estado_ui = "MOSTRAR_RESULTADO"

    st.rerun()

# --------------------------------------------------
# Pantalla RESULTADOS
# --------------------------------------------------

elif campania.estado_ui == "MOSTRAR_RESULTADO":

    st.title("Resultado de la acción")

    mensaje = campania.get_mensaje()

    datos = mensaje.obtener_mensaje_completo()

    # -------------------------
    # NARRACION PRINCIPAL
    # -------------------------
    st.subheader("Narración")

    st.write(datos["narracion"])

    st.image(
        datos["imagen_resumen"],
        use_container_width=True
    )

    # -------------------------
    # NPC (si existe)
    # -------------------------
    if "narracion_npc" in datos:

        st.subheader("Personaje")

        st.write(datos["narracion_npc"])

        if "imagen_npc" in datos:

            st.image(
                datos["imagen_npc"],
                use_container_width=True
            )

        if "dialogo_npc" in datos:

            st.info(datos["dialogo_npc"])

    # -------------------------
    # FINAL
    # -------------------------
    if campania.estado.final != "sin_final":

        st.error(f"FIN DEL JUEGO: {campania.estado.final}")

        if st.button("Siguiente"):

            st.session_state.campania.estado_ui = "FINAL"

            st.rerun()

        # --------------------------------------------------
        # CASO NORMAL (loop del juego)
        # --------------------------------------------------
    else:

        accion = st.text_input("¿Qué deseas hacer ahora?")

        if st.button("Enviar"):

            campania.recibir_accion_jugador(accion)

            resultado = campania.arbitrar_accion_jugador()

            if not resultado["accion_valida"]:
                st.error("No puedes realizar esa acción.")

            else:

                if resultado["requiere_tirada"]:
                    campania.estado_ui = "ESPERANDO_D20"
                else:
                    campania.no_requiere_tirada()
                    campania.estado_ui = "PROCESANDO"

            st.rerun()

# --------------------------------------------------
# Pantalla FINAL
# --------------------------------------------------

elif campania.estado_ui == "FINAL":

    st.title("FIN DE LA AVENTURA")
    campania.narracion_final()
    campania.generar_imagen_resumen()
    mensaje = campania.obtener_mensaje_vista()
    st.write(mensaje["narracion"])
    st.image(
        mensaje["imagen_resumen"],
        use_container_width=True
    )
    if st.button("Reiniciar aventura"):
        campania.reiniciar()
        st.rerun()