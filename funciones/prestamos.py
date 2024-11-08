import time
import pandas as pd
import streamlit as st
import subprocess
import datetime
import json
import os

def abrir_usuario(index: int, ajustes: dict, df) -> (bool, str):
    if 0 <= index < ajustes["usuarios"]:
        if df["estado"][index] == "activo":
            return True, ""
        else:
            return False, f"El usuario № {index} no esta activo",
    else:
        return False, "El numero de usuario esta fuera de rango"

def crear_tablas_de_ranura(prestamo: str, fechas: str):
    prestamo: list[str] = prestamo.split("_")
    deudas = int(prestamo[3]) + int(prestamo[1])
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
    ), True if deudas == 0 else False


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


def consultar_capital_disponible(index: int, ajustes: dict, df) -> tuple:
    capital: int = int(df["capital"][index])
    capital_disponible: int = int(capital*ajustes["capital usable"]/100)

    deudas_por_fiador: int = int(df["deudas por fiador"][index])

    deudas_en_prestamos_tabla: dict = {
        "Ranuras": [],
        "Deudas": []
    }
    deudas_en_prestamos: int = 0

    deudas_por_intereses_tabla: dict = {
        "Ranuras": [],
        "Deudas": []
    }
    deudas_por_intereses: int = 0

    for i in range(1, 16):
        if df[f"p{i} estado"][index] != "activo":
            prestamo: list[str] = df[f"p{i} prestamo"][index].split("_")

            deuda_prestamo: int = int(prestamo[3])
            if deuda_prestamo > 0:
                deudas_en_prestamos_tabla["Ranuras"].append(f"Ranura {i}")
                deudas_en_prestamos_tabla["Deudas"].append(
                    "{:,}".format(deuda_prestamo)
                )
                deudas_en_prestamos += deuda_prestamo

            deuda_intereses: int = int(prestamo[1])
            if deuda_intereses > 0:
                deudas_por_intereses_tabla["Ranuras"].append(f"Ranura {i}")
                deudas_por_intereses_tabla["Deudas"].append(
                    "{:,}".format(deuda_intereses)
                )
                deudas_por_intereses += deuda_intereses

    deudas_en_prestamos_tabla["Ranuras"].append("TOTAL:")
    deudas_en_prestamos_tabla["Deudas"].append(
        "{:,}".format(deudas_en_prestamos)
    )

    deudas_por_intereses_tabla["Ranuras"].append("TOTAL:")
    deudas_por_intereses_tabla["Deudas"].append(
        "{:,}".format(deudas_por_intereses)
    )

    capital_total: int = capital_disponible - (
        deudas_por_fiador + deudas_en_prestamos + deudas_por_intereses
    )

    return (
        "{:,}".format(capital_total), # 0
        "{:,}".format(capital),  # 1
        "{:,}".format(capital_disponible),  # 2
        "{:,}".format(deudas_por_fiador),  # 3
        pd.DataFrame(deudas_en_prestamos_tabla),  # 4
        pd.DataFrame(deudas_por_intereses_tabla)  # 5
    )


def consultar_capital_usuario(index: int, ajustes: dict, df) -> int:
    capital: int = int(df["capital"][index])
    capital_disponible: int = int(capital*ajustes["capital usable"]/100)

    deudas_por_fiador: int = int(df["deudas por fiador"][index])

    deudas_en_prestamos: int = 0
    deudas_por_intereses: int = 0

    for i in range(1, 16):
        if df[f"p{i} estado"][index] != "activo":
            prestamo: list[str] = df[f"p{i} prestamo"][index].split("_")

            deuda_prestamo: int = int(prestamo[3])
            if deuda_prestamo > 0:
                deudas_en_prestamos += deuda_prestamo

            deuda_intereses: int = int(prestamo[1])
            if deuda_intereses > 0:
                deudas_por_intereses += deuda_intereses

    capital_total: int = capital_disponible - (
        deudas_por_fiador + deudas_en_prestamos + deudas_por_intereses
    )
    return capital_total


def hacer_carta_de_prestamo() -> None:
    ahora: datetime = datetime.datetime.now()
    fecha_hora_str: str = ahora.strftime("%Y/%m/%d %H:%M")
    carta: list[str] = [
        fecha_hora_str + "\n",
        "\n",
        "Señores de el fondo, yo __________________________ usuari@ № _______ de el fondo San Javier\n",
        "\n",
        "solicito un prestamo por el valor de _______________, con el interes de ______ % tengo la \n",
        "\n",
        "intencion de pagar el prestamo en _______ mes(es) si mi dinero no llegase a ser suficiente\n",
        "\n",
        "solicito como fiador(es) con las siguientes deudas a:\n",
        "\n",
        "          Nombre                    Numero                    Deuda\n",
        "-------------------------------------------------------------------------------------\n",
        "                              |                 |\n",
        "-------------------------------------------------------------------------------------\n",
        "                              |                 |\n",
        "-------------------------------------------------------------------------------------\n",
        "                              |                 |\n",
        "-------------------------------------------------------------------------------------\n",
        "                              |                 |\n",
        "-------------------------------------------------------------------------------------\n",
        "                              |                 |\n",
        "-------------------------------------------------------------------------------------\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "          _________________________                         _________________________\n",
        "           socio de el fondo                                 tesorero"
    ]

    with open("text/carta_prestamo.txt", "w", encoding="utf-8") as f:
        f.write("".join(carta))
        f.close()
