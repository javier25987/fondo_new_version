import streamlit as st
import json
import pandas as pd
import funciones.ajustes as fa

st.set_page_config(layout="wide")

st.title("Ajustes")

control_1, control_2 = False, False

try:
    with open("ajustes.json", "r") as f:
        f.close()
    control_1 = True
except:
    st.error(
        "Se necesita un archivo de ajustes.",
        icon="🚨"
    )

try:
    with open("ajustes.json", "r") as f:
        ajustes = json.load(f)
        f.close()

    df = pd.read_csv(ajustes["nombre df"])

    control_2 = True
except:
    st.error(
        "Se necesita una tabla de socios.",
        icon="🚨"
    )

if not (control_1 and control_2):

    st.header("Creacion de archivos de ajustes y almacenamiento.")

    st.info(
        """En caso de necesitarse crear el archivo de ajustes y la tabla
        de socios cree primero el archivo de ajustes y despues la tabla
        ese orden es el adecuado para la operacion
        """,
        icon="ℹ️"
    )

    c1_1, c1_2 = st.columns(2)

    with c1_1:
        if st.button("crear ajustes de el programa"):
            fa.crear_ajustes_de_el_programa()
            st.success(
                "Los ajustes han sido creados",
                icon="✅"
            )

    with c1_2:
        if st.button("Crear nueva tabla de socios"):
            fa.crear_data_frame_principal()
            st.success(
                "La tabla ha sido creada",
                icon="✅"
            )