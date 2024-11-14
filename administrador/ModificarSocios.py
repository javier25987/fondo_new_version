import funciones.modificarsocios as fm
import funciones.general as fg
import streamlit as st
import pandas as pd

st.title("Modificar Socios")

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

tabs = st.tabs(
    ["Ver y modificar datos", "Añadir usuario"]
)

with tabs[0]:
    col1 = st.columns(2)

    with col1[0]:
        datos: str = st.selectbox(
            "Datos que desea ver:",
            (
                "informacion general", "pago de cuotas",
                "rifas", "prestamos", "TODO"
            )
        )
    with col1[1]:
        if datos == "prestamos":
            lista_elecciones: list[str] = ["TODAS"] + \
                [f"ranura {i}" for i in range(1, 17)]

            prestamo: str = st.selectbox(
                "Ranura(s) que desea ver:",
                lista_elecciones
            )
    match datos:
        case "informacion general":
            st.table(
                df[
                    [
                        "numero", "nombre", "puestos",
                        "numero celular", "estado",
                        "capital", "aporte a multas",
                        "multas extra", "anotaciones generales"
                    ]
                ]
            )
        case "pago de cuotas":
            st.table(
                df[
                    [
                        "numero", "nombre", "cuotas",
                        "multas", "tesorero", "revisiones",
                        "anotaciones de cuotas"
                    ]
                ]
            )
        case "rifas":
            st.table(
                df[
                    [
                        "numero", "nombre",
                        "r1 boletas", "r1 deudas",
                        "r2 boletas", "r2 deudas",
                        "r3 boletas", "r3 deudas",
                        "r4 boletas", "r4 deudas",
                        "anotaciones de rifas"
                    ]
                ]
            )
        case "prestamos":
            if prestamo == "TODAS":
                lista_columnas: list[str] = [
                    "numero", "nombre", "prestamos hechos",
                    "dinero en prestamos", "dinero por si mismo"
                ]
                for i in range(1, 17):
                    lista_columnas += [
                        f"p{i} estado",
                        f"p{i} prestamo",
                        f"p{i} fechas de pago"
                    ]
                lista_columnas += [
                    "deudas por fiador", "fiador de",
                    "anotaciones de prestamos"
                ]
                st.table(df[lista_columnas])
            else:
                ranura: str = int(prestamo[-2:])
                st.table(
                    df[
                        [
                            "numero", "nombre",
                            "prestamos hechos",
                            "dinero en prestamos",
                            "dinero por si mismo",
                            f"p{ranura} estado",
                            f"p{ranura} prestamo",
                            f"p{ranura} fechas de pago",
                            "deudas por fiador",
                            "fiador de",
                            "anotaciones de prestamos"
                        ]
                    ]
                )
        case "TODO":
            st.table(df)

with tabs[1]:
    st.header("Datos de el nuevo usuario:")

    nombre: str = st.text_input("Nombre:")
    telefono: str = st.text_input("Numero celular:")
    puestos: int = st.number_input(
        "Numero de puestos:",
        value=0, step=1
    )
    if st.button("Añadir"):
        paso_1: bool = False
        paso_2: bool = False

        if nombre == "":
            st.error(
                "El nombre de usuario no puede estar vacio",
                icon="🚨"
            )
        else:
            paso_1 = True

        if puestos < 1:
            st.error(
                "Para que un usuario tendria menos de un puesto?",
                icon="🚨"
            )
        else:
            paso_2 = True

        if paso_1 and paso_2:
            fm.menu_para_insertar_socio(
                ajustes, df, nombre,
                puestos, telefono
            )
            st.balloons()