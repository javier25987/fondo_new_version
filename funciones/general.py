import time
import pandas as pd
import streamlit as st
import subprocess
import datetime
import json
import os


def abrir_ajustes() -> dict:
    with open("ajustes.json", "r") as f:
        ajustes: dict = json.load(f)
        f.close()
    return ajustes


def guardar_ajustes(ajustes: dict) -> None:
    with open("ajustes.json", "w") as f:
        json.dump(ajustes, f)
        f.close()


def crear_ajustes_de_el_programa() -> None:
    ajustes: dict = {
        "valor multa": 3000,
        "valor cuota": 10000,
        "interes < tope": 3,
        "interes > tope": 2,
        "tope de intereses": 20000000,
        "capital usable": 50,
        "clave de acceso": "1234",
        "calendario": "n",
        "usuarios": 0,
        "anular usuarios": False,
        "cobrar multas": False,
        "fecha de cierre": "n",
        "numero de creacion": 1,
        "nombre df": "",
        "path programa": f"{os.getcwd()}",
        "enlace repo": "",
        "commits hechos": 0,
        "r1 estado": False,
        "r1 numero de boletas": 0,
        "r1 numeros por boleta": 0,
        "r1 premios": "",
        "r1 costo de boleta": 0,
        "r1 boletas por talonario": 0,
        "r1 costos de administracion": 0,
        "r1 ganancia por boleta": 0,
        "r1 fecha de cierre": "",
        "r2 estado": False,
        "r2 numero de boletas": 0,
        "r2 numeros por boleta": 0,
        "r2 premios": "",
        "r2 costo de boleta": 0,
        "r2 boletas por talonario": 0,
        "r2 costos de administracion": 0,
        "r2 ganancia por boleta": 0,
        "r2 fecha de cierre": "",
        "r3 estado": False,
        "r3 numero de boletas": 0,
        "r3 numeros por boleta": 0,
        "r3 premios": "",
        "r3 costo de boleta": 0,
        "r3 boletas por talonario": 0,
        "r3 costos de administracion": 0,
        "r3 ganancia por boleta": 0,
        "r3 fecha de cierre": "",
        "r4 estado": False,
        "r4 numero de boletas": 0,
        "r4 numeros por boleta": 0,
        "r4 premios": "",
        "r4 costo de boleta": 0,
        "r4 boletas por talonario": 0,
        "r4 costos de administracion": 0,
        "r4 ganancia por boleta": 0,
        "r4 fecha de cierre": ""
    }
    guardar_ajustes(ajustes)


def crear_tabla_principal() -> None:
    try:
        ajustes: dict = abrir_ajustes()

        nombre: str = "FONDO_" + str(ajustes["numero de creacion"]) + \
        "_" + datetime.datetime.now().strftime("%Y") + ".csv"

        ajustes["numero de creacion"] += 1
        ajustes["nombre df"] = nombre

        guardar_ajustes(ajustes)

        df = pd.DataFrame(
            {
                # informacion general
                "numero": [],
                "nombre": [],
                "puestos": [],
                "numero celular": [],
                "estado": [],
                "capital": [],
                "aporte a multas": [],
                "multas extra": [],
                "anotaciones generales": [],
                # cuotas
                "cuotas": [],
                "multas": [],
                "tesorero": [],
                "revisiones": [],
                "anotaciones de cuotas": [],
                # rifas
                "r1 boletas": [],
                "r1 deudas": [],
                "r2 boletas": [],
                "r2 deudas": [],
                "r3 boletas": [],
                "r3 deudas": [],
                "r4 boletas": [],
                "r4 deudas": [],
                "anotaciones de rifas": [],
                # prestamos
                "prestamos hechos": [],
                "dinero en prestamos": [],
                "dinero por si mismo": [],
                "p1 estado": [],
                "p1 prestamo": [],
                "p1 fechas de pago": [],
                "p2 estado": [],
                "p2 prestamo": [],
                "p2 fechas de pago": [],
                "p3 estado": [],
                "p3 prestamo": [],
                "p3 fechas de pago": [],
                "p4 estado": [],
                "p4 prestamo": [],
                "p4 fechas de pago": [],
                "p5 estado": [],
                "p5 prestamo": [],
                "p5 fechas de pago": [],
                "p6 estado": [],
                "p6 prestamo": [],
                "p6 fechas de pago": [],
                "p7 estado": [],
                "p7 prestamo": [],
                "p7 fechas de pago": [],
                "p8 estado": [],
                "p8 prestamo": [],
                "p8 fechas de pago": [],
                "p9 estado": [],
                "p9 prestamo": [],
                "p9 fechas de pago": [],
                "p10 estado": [],
                "p10 prestamo": [],
                "p10 fechas de pago": [],
                "p11 estado": [],
                "p11 prestamo": [],
                "p11 fechas de pago": [],
                "p12 estado": [],
                "p12 prestamo": [],
                "p12 fechas de pago": [],
                "p13 estado": [],
                "p13 prestamo": [],
                "p13 fechas de pago": [],
                "p14 estado": [],
                "p14 prestamo": [],
                "p14 fechas de pago": [],
                "p15 estado": [],
                "p15 prestamo": [],
                "p15 fechas de pago": [],
                "deudas por fiador": [],
                "fiador de": [],
                "anotaciones de prestamos": []
            }
        )
        df.to_csv(nombre)
    except:
        st.error("No se encuentran los ajustes", icon="🚨")


def modificar_string(s: str, index_s: int, new_elemento: str) -> str:
    s: list[str] = list(s)
    s[index_s] = new_elemento
    return "".join(s)


def string_a_fecha(fecha: str):
    return datetime.datetime(
        *map(
            int,
            fecha.split("/")
        )
    )


def ejecutar_comando_git(comando):
    proceso = subprocess.Popen(
        comando,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    salida, error = proceso.communicate()

    if proceso.returncode != 0:
        print(f"Error: {error.decode("utf-8")}")
    else:
        print(f"Salida: {salida.decode("utf-8")}")




if __name__ == "__main__":
    print(
        string_a_fecha("2024/10/5/7")
    )




