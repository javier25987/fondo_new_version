import streamlit as st
import funciones.general as fg
import json
import pandas as pd

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


def logout() -> None:
    st.session_state.admin = False
    st.rerun()


def login() -> None:
    ajustes: dict = fg.abrir_ajustes()

    st.title("Ingresar como administrador")

    st.markdown(
        """
        Por favor ingrese su clave de administrador para acceder
        a las funciones extra de el programa.
        """
    )
    clave: str = st.text_input("Clave de administrador:")

    if st.button("Ingresar"):
        if clave == ajustes["clave de acceso"]:
            st.toast(
                "Ha obtenido acceso de administador",
                icon="🎉"
            )
            st.session_state.admin = True
            st.rerun()
        elif clave == "":
            st.error(
                "La clave esta vacia",
                icon="🚨"
            )
        else:
            st.error(
                "La clave es incorrecta",
                icon="🚨"
            )


def crear_archivos_elementales() -> None:
    st.header("Creacion de archivos de ajustes y almacenamiento.")

    df_mensaje: str = ""
    ajustes_mensaje: str = ""

    if not st.session_state.df_exist:
        df_mensaje = "* Tabla de socios"

    if not st.session_state.ajustes_exist:
        ajustes_mensaje = "* Ajustes de el programa"

    st.markdown(
        f"""
        #### Se necesita crear:
        {ajustes_mensaje}
        {df_mensaje}
        
        > **NOTA:** En caso de necesitarse crear el archivo de ajustes y la tabla
        de socios cree primero el archivo de ajustes y despues la tabla
        ese orden es el adecuado para la operacion.
        
        > **NOTA:** En caso de haber creado el archivo de ajustes dirijase a el
        modo administrador y a ajustes, en esa pagina configure todo lo necesario
        de el archivo.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("crear ajustes de el programa"):
            fg.crear_ajustes_de_el_programa()
            st.rerun()

    with col2:
        if st.button("Crear nueva tabla de socios"):
            fg.crear_tabla_principal()
            st.rerun()


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
        icon="💰"
    ),
    st.Page(
        "paginas/VerSocios.py",
    title = "Ver Socios",
    icon = "🔎"
    )
]

paginas_de_adiministrador: list = [
    st.Page(
        "administrador/ModificarSocios.py",
        title="Modificar Socios",
        icon="📖",
    ),
    st.Page(
        "administrador/Ajustes.py",
        title="Ajustes",
        icon="⚙️"
    ),
    st.Page(
        logout,
        title="Salir",
        icon=":material/logout:"
    )
]

ingresar_admin: list = [
    st.Page(
        login,
        title="Ingresar",
        icon=":material/login:"
    )
]

archivos_elementales: list = [
    st.Page(
        crear_archivos_elementales,
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
