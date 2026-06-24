import streamlit as st

from Campania import Campania


# --------------------------------------------------
# Inicialización
# --------------------------------------------------

if "campania" not in st.session_state:

    st.session_state.campania = Campania()

    st.session_state.campania.estado_ui = "MENU"


campania = st.session_state.campania


# --------------------------------------------------
# Pantalla MENU
# --------------------------------------------------

if campania.estado_ui == "MENU":

    st.title("RPG Narrativo con IA")

    st.write(
        "Rescata a la princesa cautiva en la cueva goblin."
    )

    if st.button("Comenzar"):

        campania.estado_ui = "JUGANDO"

        st.rerun()


# --------------------------------------------------
# Pantalla JUGANDO
# --------------------------------------------------

elif campania.estado_ui == "JUGANDO":

    mensaje = campania.get_mensaje()

    datos = mensaje.obtener_seccion_obligatoria()

    st.title("RPG Narrativo con IA")

    st.write(
        datos["narracion"]
    )

    st.write(
        f"Imagen: {datos['imagen_resumen']}"
    )