import funciones.general as fg
import streamlit as st
import pandas as pd
import json
import time

st.set_page_config(layout="wide")

if "admin" not in st.session_state:
    st.session_state.admin = False

if "df_exist" not in st.session_state:
    st.session_state.df_exist = False

if "ajustes_exist" not in st.session_state:
    st.session_state.ajustes_exist = False

if "nombre_para_busqueda" not in st.session_state:
    st.session_state.nombre_para_busqueda = ""

if "usuario_actual_cuotas" not in st.session_state:
    st.session_state.usuario_actual_cuotas = -1

if "usuario_actual_prestamos" not in st.session_state:
    st.session_state.usuario_actual_prestamos = -1

if "usuario_actual_ver" not in st.session_state:
    st.session_state.usuario_actual_ver = -1

if "usuario_actual_rifas" not in st.session_state:
    st.session_state.usuario_actual_rifas = -1

if "ranura_actual" not in st.session_state:
    st.session_state.ranura_actual = "1"

if "nombre_para_busqueda" not in st.session_state:
    st.session_state.nombre_para_busqueda = ""


paginas_generales: list = [
    st.Page(
        "paginas/Menu.py",
        title="Menu",
        icon="🏠"
    ),
    st.Page(
        "paginas/Cuotas.py",
        title="Cuotas",
        icon="📆"
    ),
    st.Page(
        "paginas/Prestamos.py",
        title="Prestamos",
        icon="💵"
    ),
    st.Page(
        "paginas/Rifas.py",
        title="Rifas",
        icon="🗒️"
    ),
    st.Page(
        "paginas/VerSocios.py",
    title = "Ver Usuarios",
    icon = "🔎"
    )
]

paginas_de_adiministrador: list = [
    st.Page(
        "administrador/ModificarSocios.py",
        title="Modificar Usuarios",
        icon="📖",
    ),
    st.Page(
        "administrador/Ajustes.py",
        title="Ajustes",
        icon="⚙️"
    ),
    st.Page(
        "session/logout.py",
        title="Salir",
        icon=":material/logout:"
    )
]

ingresar_admin: list = [
    st.Page(
        "session/login.py",
        title="Ingresar",
        icon=":material/login:"
    )
]

archivos_elementales: list = [
    st.Page(
        "session/files.py",
        title="Crear Archivos",
        icon=":material/settings:"
    )
]

# revisar si existen los ajustes
try:
    with open("ajustes.json", "r") as f:
        f.close()
    st.session_state.ajustes_exist = True
except:
    pass

# revisar si esiste la tabla
try:
    with open("ajustes.json", "r") as f:
        ajustes = json.load(f)
        f.close()

    df = pd.read_csv(ajustes["nombre df"])

    st.session_state.df_exist = True
except:
    pass

dict_general: dict = {}

if st.session_state.ajustes_exist and st.session_state.df_exist:
    dict_general["Paginas Generales"] = paginas_generales

    if st.session_state.admin:
        dict_general["Paginas Administrativas"] = paginas_de_adiministrador
    else:
        dict_general["Paginas Administrativas"] = ingresar_admin
else:
    dict_general["Paginas Generales"] = archivos_elementales

pg = st.navigation(dict_general)
pg.run()
