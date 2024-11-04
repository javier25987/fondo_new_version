import streamlit as st
import funciones.general as fg
import funciones.prestamos as fp
import pandas as pd

ranura_actual: str = st.session_state.ranura_actual

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

index: int = st.session_state.usuario_actual_prestamos
index_de_usuario: int = st.sidebar.number_input(
    "Numero de usuario: ",
    value=0, step=1
)

if st.sidebar.button("Buscar"):
    if 0 <= index_de_usuario < ajustes["usuarios"]:
        if df["estado"][index_de_usuario] == "activo":
            st.session_state.usuario_actual_prestamos = index_de_usuario
            st.rerun()
        else:
            st.error(
                f"El usuario № {index_de_usuario} no esta activo.",
                icon="🚨"
            )
    else:
        st.error(
            "El numero de usuario esta fuera de rango.",
            icon="🚨"
        )

if index == -1:
    st.title("Usuario indeterminado")
else:
    st.title(
        f"№ {index} - {df["nombre"][index].title()} : {
        df["puestos"][index]} puesto(s)"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Prestamos", "Solicitar Prestamo", "Consultar Capital"
        ]
    )

    with tab1:
        col1_1, col1_2 = st.columns(2, vertical_alignment="bottom")
        ranura_escojida: str = col1_1.selectbox(
            "Ranura a abrir:",
            [str(i) for i in range(1, 16)]
        )

        if col1_2.button("Abrir Ranura"):
            st.session_state.ranura_actual = ranura_escojida
            st.rerun()

        st.divider()

        tablas_ranura: tuple = fp.crear_tablas_de_ranura(
            df[f"p{ranura_actual} prestamo"][index],
            df[f"p{ranura_actual} fechas de pago"][index],
        )

        st.header(f"Ranura abierta: {ranura_actual}")
        st.subheader("Informacion de el prestamo")
        st.table(tablas_ranura[0])
        st.subheader("Fechas de pago")
        st.table(tablas_ranura[1])

        if tablas_ranura[2]:
            if df[f"p{ranura_actual} estado"][index] == "activo":
                st.markdown("> **NOTA:** La ranura esta activa")
            else:
                if st.button("Activar Ranura"):
                    fp.activar_ranura(
                        index,
                        df,
                        ajustes,
                        ranura_actual
                    )
        else:
            st.text("aca va el formato de pago")

    with tab2:
        st.subheader("Ranuras disponibles: ")
        st.table(fp.ranuras_disponibles(index, df))

