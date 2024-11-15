import funciones.general as fg
import funciones.cuotas as fc
import streamlit as st
import pandas as pd
import datetime
import time
import os


def cargar_multas() -> None:
    ajustes = fg.abrir_ajustes()
    df = pd.read_csv(ajustes["nombre df"])
    total_usuarios = ajustes["usuarios"]
    mensaje = "Cargando multas a todos los usuarios ..."
    bar = st.progress(0, mensaje)

    for i in range(total_usuarios):
        fc.arreglar_asuntos(i, ajustes, df)
        df = pd.read_csv(ajustes["nombre df"])
        bar.progress((i + 1) / total_usuarios, mensaje)

    time.sleep(1)
    bar.empty()


def hacer_commit() -> None:
    ajustes = fg.abrir_ajustes()
    with st.status("Guardando cambios ...", expanded=True) as status:
        os.chdir(ajustes["path programa"])

        st.write("Subiendo archivos ...")
        fg.ejecutar_comando_git(["git", "add", "."])

        st.write("Guardando ajustes ...")
        fg.ejecutar_comando_git(["git", "add", "ajustes.json"])

        st.write("Guardando cambios ...")
        ahora = datetime.datetime.now()
        fecha_hora_str = ahora.strftime("%Y-%m-%d_%H:%M:%S")
        ajustes["commits hechos"] += 1
        mensaje_de_comit = f"{ajustes["commits hechos"]}_{fecha_hora_str}"
        fg.ejecutar_comando_git(["git", "commit", "-m", mensaje_de_comit])
        fg.guardar_ajustes(ajustes)

        st.write("Guardando en GitHub ...")
        fg.ejecutar_comando_git(
            ["git", "push"]
        )
        status.update(
            label="Los datos han sido cargados!",
            state="complete",
            expanded=False
        )
        time.sleep(1)
        st.rerun()
