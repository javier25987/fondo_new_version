import funciones.general as fg
import streamlit as st
import datetime
import time

def crear_listado_de_fechas(primera_fecha: str, dobles: list[str]) -> str:
    """
    para este formato es obligatorio que las fechas esten en el formato
    anio/mes/dia/hora (la hora tiene que estar en formato 24 horas)
    """
    fecha = fg.string_a_fecha(primera_fecha)
    dias = 7
    fechas = []

    for i in range(48):
        new_f = fecha + datetime.timedelta(days=dias * i)
        f_new = new_f.strftime("%Y/%m/%d/%H")
        if f_new in dobles:
            fechas.append(f_new)
        fechas.append(f_new)

    for i in dobles:
        if i not in fechas:
            return "n"

    return "_".join(fechas)

def guardar_y_avisar(ajustes: dict):
    fg.guardar_ajustes(ajustes)
    st.success("Valor modificado", icon="✅")
    time.sleep(1)
    st.rerun()