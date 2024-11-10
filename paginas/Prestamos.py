import os
import streamlit as st
import funciones.general as fg
import funciones.prestamos as fp
import pandas as pd

from funciones.prestamos import formulario_de_prestamo

ranura_actual: str = st.session_state.ranura_actual

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

index: int = st.session_state.usuario_actual_prestamos
index_de_usuario: int = st.sidebar.number_input(
    "Numero de usuario: ",
    value=0, step=1
)
if st.sidebar.button("Buscar"):
    estado = fp.abrir_usuario(index_de_usuario, ajustes, df)

    if estado[0]:
        st.session_state.usuario_actual_prestamos = index_de_usuario
        st.rerun()
    else:
        st.error(estado[1], icon="🚨")

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

        if col1_2.button("Abrir ranura"):
            st.session_state.ranura_actual = ranura_escojida
            st.rerun()

        st.divider()

        tablas_ranura: tuple = fp.crear_tablas_de_ranura(
            df[f"p{ranura_actual} prestamo"][index],
            df[f"p{ranura_actual} fechas de pago"][index],
        )

        st.header(f"Ranura abierta: {ranura_actual}")
        st.subheader("Informacion de el prestamo: ")
        st.table(tablas_ranura[0])
        st.table(tablas_ranura[2])
        st.subheader("Fechas de pago: ")
        st.table(tablas_ranura[1])

        if tablas_ranura[3]:
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
            # no olvida hacer el formato de pago aca

    with tab2:
        st.subheader("Ranuras disponibles: ")
        st.table(fp.ranuras_disponibles(index, df))
        st.divider()

        st.subheader("Carta de solicitud: ")
        if st.button("Hacer carta"):
            with st.spinner("Abriendo carta"):
                fp.hacer_carta_de_prestamo()
                os.system("notepad.exe text/carta_prestamo.txt")
        st.divider()

        st.subheader("Formato de solicitud: ")
        col2_1, col2_2 = st.columns(2)

        with col2_1:
            ranura_prestamo: str = st.selectbox(
                "Ranura en la que guardar el prestamo: ",
                [
                    str(i) for i in range(1, 16)
                ]
            )
            valor_prestamo: int = st.number_input(
                "Valor de el prestamo: ",
                value=0, step=1
            )

        with col2_2:
            numero_de_fiadores: int = st.number_input(
                "Cantidad de fiadores: ",
                value=0, step=1
            )

            col3_1, col3_2 = st.columns(2)
            key_f: int = 0
            key_d: int = 0

            for i in range(numero_de_fiadores):
                with col3_1:
                    st.number_input(
                        "Numero de el fiador: ",
                        value=0, step=1,
                        key=f"numero_fiador_{key_f}"
                    )
                    key_f += 1
                with col3_2:
                    st.number_input(
                        "Deuda con el fiador: ",
                        value=0, step=1,
                        key=f"deuda_fiador_{key_d}"
                    )
                    key_d += 1

        if st.button("Realizar prestamo"):
            fiadores_prestamo: list[int] = []
            deudas_prestamo: list[int] = []
            for i in range(numero_de_fiadores):
                fiadores_prestamo.append(
                    st.session_state[f"numero_fiador_{i}"]
                )
                deudas_prestamo.append(
                    st.session_state[f"deuda_fiador_{i}"]
                )
            estado_prestamo: tuple[bool, str] = fp.rectificar_viavilidad(
                index, ranura_prestamo, valor_prestamo,
                ajustes, df, fiadores_prestamo,
                deudas_prestamo
            )
            if estado_prestamo[0]:
                st.balloons()
                formulario_de_prestamo(
                    index, ranura_prestamo, valor_prestamo,
                    ajustes, df, fiadores_prestamo,
                    deudas_prestamo
                )
            else:
                st.error(
                    estado_prestamo[1], icon="🚨"
                )

    with tab3:
        capital: list = fp.consultar_capital_disponible(
            index, ajustes, df
        )
        st.subheader("Capital")
        st.write(f"capital guardado: {capital[1]}")
        st.write(
            f"Capital disponible para retirar: {capital[2]}"
        )

        st.subheader("Deudas")

        st.write(f"Deudas por fiador: {capital[3]}.")
        st.write(f"Fiador de: {df["fiador de"][index]}")

        st.write("Deudas en prestamos:")
        st.table(capital[4])

        st.write("Deudas por intereses vencidos:")
        st.table(capital[5])

        st.header(
            f"Dinero disponible para retirar: {capital[0]}"
        )
