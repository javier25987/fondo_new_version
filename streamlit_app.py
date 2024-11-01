import streamlit as st
import funciones.general as fg

if "admin" not in st.session_state:
    st.session_state.admin = False

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

paginas_generales: list = [
    st.Page(
        "pages/Menu.py",
        title="Menu",
        icon="🏠"
    ),
    st.Page(
        "pages/Cuotas.py",
        title="Cuotas",
        icon="📆"
    ),
    st.Page(
        "pages/Prestamos.py",
        title="Prestamos",
        icon="💵"
    ),
    st.Page(
        "pages/Rifas.py",
        title="Rifas",
        icon="💰"
    ),
    st.Page(
    "pages/VerSocios.py",
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

dict_general: dict = {
    "Paginas Generales": paginas_generales
}

if st.session_state.admin:
    dict_general["Paginas Administrativas"] = paginas_de_adiministrador
else:
    dict_general["Paginas Administrativas"] = ingresar_admin

pg = st.navigation(dict_general)
pg.run()
