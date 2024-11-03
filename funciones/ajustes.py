import time
import pandas as pd
import streamlit as st
import datetime
import funciones.general as fg
import os

def crear_listado_de_fechas(primera_fecha: str, dobles: list[str]) -> str:
    fecha = fg.string_a_fecha(primera_fecha)
    dias = 7
    fechas = []
    n_semanas = 50 - len(dobles)

    for i in range(0, n_semanas):
        new_f = fecha + datetime.timedelta(days=dias * i)
        f_new = new_f.strftime("%Y/%m/%d/%H")
        if f_new in dobles:
            fechas.append(f_new)
        fechas.append(f_new)

    for i in dobles:
        if i not in fechas:
            return ["-"]

    return "_".join(fechas)

