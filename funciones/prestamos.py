import time
import pandas as pd
import streamlit as st
import subprocess
import datetime
import json
import os

def crear_tablas_de_ranura(prestamo: str, fechas: str):
    prestamo: list[str] = prestamo.split("_")
    return pd.DataFrame(
        {
            "Deuda": list("{:,}".format(int(prestamo[3]))),
            "Interes": [f"{int(prestamo[0])/100} %"],
            "Intereses Vencidos": list("{:,}".format(int(prestamo[1]))),
            "Fiadores": [prestamo[4]],
            "Deuda Con fiadores": [prestamo[5]]
        }
    ), pd.DataFrame(
        {
            "Fechas": fechas.split("_")
        }
    ), True if prestamo[3] == "0" else False


def ranuras_disponibles(index: int, df):
    funct = lambda x: "✅" if x == "activo" else "🚨"

    estado_ranuras: list[str] = list(
        map(
            funct,
            [
                df[f"p{i} estado"][index]
                for i in range(1, 16)
            ]
        )
    )
    dict_tabla: dict = {}

    for i in range(1, 16):
        dict_tabla[str(i)] = list(estado_ranuras[i - 1])

    return pd.DataFrame(dict_tabla)


def activar_ranura(index: int, df, ajustes: dict, ranura: str) -> None:
    estado: str = f"p{ranura} estado"
    prestamo: str = f"p{ranura} prestamo"
    fechas: str = f"p{ranura} fechas de pago"

    if df[estado][index] != "activo":
        df.loc[index, estado] = "activo"
        df.loc[index, prestamo] = "0_0_0_0_n_n"
        df.loc[index, fechas] = "n"

        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df.to_csv(ajustes["nombre df"])
        st.rerun()
    else:
        st.info(
            "La ranura esta activa",
            icon="ℹ️"
        )

