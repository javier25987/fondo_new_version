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


def modificar_string(s: str, index_s: int, new_elemento: str) -> str:
    s = list(s)
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
        print(f"Error: {error.decode('utf-8')}")
    else:
        print(f"Salida: {salida.decode('utf-8')}")




if __name__ == "__main__":
    print(
        string_a_fecha("2024/10/5/7")
    )




