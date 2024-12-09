import funciones.general as fg
import funciones.cuotas as fc
import streamlit as st
import pandas as pd
import os

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

if ajustes["calendario"] == "n":
    st.info(
        "El calendario aun no ha sido creado",
        icon="ℹ️"
    )
    st.stop()

index: int = st.session_state.usuario_actual_cuotas

index_de_usuario: int = st.sidebar.number_input(
    "Numero de usuario:", value=0, step=1
)
if st.sidebar.button("Buscar"):
    estado: list[bool, str] = fc.abrir_usuario(
        index_de_usuario, ajustes, df
    )
    if estado[0]:
        st.session_state.usuario_actual_cuotas = index_de_usuario
        st.rerun()
    else:
        st.error(
            estado[1], icon="🚨"
        )

if index == -1:
    st.title("Usuario indeterminado")
else:
    nombre_usuario: str = df["nombre"][index].title()
    st.title(
        f"№ {index} - {df["nombre"][index].title()} : {
        df["puestos"][index]} puesto(s)"
    )

    tabs = st.tabs(["Pagar cuotas y multas", "Anotaciones"])

    with tabs[0]:
        col1_1, col1_2 = st.columns(
            [8, 2],
            vertical_alignment="bottom"
        )
        with col1_1:
            st.header(
                f"Numero de telefono: {df["numero celular"][index]}"
            )
        with col1_2:
            if st.button("Estado de cuenta"):
                with st.spinner("Obteniendo estado de cuenta..."):
                    fc.obtener_estado_de_cuenta(index, df)
                    os.system("notepad.exe text/estado_de_cuenta.txt")

        st.divider()

        df1, df2 = fc.tablas_para_cuotas_y_multas(index, ajustes, df)
        col2_1, col2_2 = st.columns(2)

        with col2_1:
            st.table(df1)

        with col2_2:
           st.table(df2)

        numero_cuotas_a_pagar: int = 50 - df["cuotas"][index].count("p")

        if numero_cuotas_a_pagar > 10:
            numero_cuotas_a_pagar = 10

        numero_multas_a_pagar: int = fc.contar_multas(df["multas"][index])

        cuotas_a_pagar: int = st.selectbox(
            "Numero de cuotas a pagar:",
            range(numero_cuotas_a_pagar + 1)
        )
        multas_a_pagar: int = st.selectbox(
            "Numero de multas a pagar:",
            range(numero_multas_a_pagar + 1)
        )
        tesorero_a_pagar: str = st.selectbox(
            "Tesorero:",
            ("1", "2", "3", "4")
        )
        col3_1, col3_2 = st.columns(2)

        if col3_1.button("Iniciar proceso de pago"):
            if cuotas_a_pagar == 0 and multas_a_pagar == 0:
                st.error(
                    "No se que desea pagar",
                    icon="🚨"
                )
            else:
                st.balloons()
                fc.formulario_de_pago(
                    index, cuotas_a_pagar, multas_a_pagar,
                    tesorero_a_pagar, ajustes, df
                )
        if col3_2.button("Abrir ultimo cheque"):
            with st.spinner("Abriendo cheque..."):
                os.system("notepad.exe text/cheque_de_cuotas.txt")

    with tabs[1]:
        st.subheader("Realizar una anotacion:")
        anotacion: str = st.text_input("Nueva anotacion:")

        if st.button("Realizar anotacion"):
            estado_anotacion: (bool, str) = fc.realizar_anotacion(
                index, anotacion, ajustes, df
            )
            if estado_anotacion[0]:
                st.rerun()
            else:
                st.error(estado_anotacion[1], icon="🚨")

        st.divider()
        st.subheader("Anotaciones hechas:")

        anotaciones: str = df["anotaciones de cuotas"][index].split("_")

        count: int = 0
        numero_de_anotaciones: list[int] = []
        for i in anotaciones:
            st.markdown(f"> **№ {count}:** {i}")
            numero_de_anotaciones.append(count)
            count += 1

        if ajustes["mostrar MyE"]:
            st.divider()

            st.subheader("Modificar anotaciones:")
            new_anotacion: str = st.text_input(
                "Nueva anotacion modificada:"
            )
            cols_a_1 = st.columns(2, vertical_alignment="bottom")

            with cols_a_1[0]:
                pos_mod_anotacion: int = st.selectbox(
                    "Anotacion que desea modificar:",
                    numero_de_anotaciones
                )
            with cols_a_1[1]:
                if st.button("Modificar"):
                    fc.modificar_anotacion(
                        index, pos_mod_anotacion,
                        new_anotacion, ajustes, df
                    )
                    st.rerun()

            st.divider()
            st.subheader("Eliminar anotaciones:")

            cols_a_2 = st.columns(2, vertical_alignment="bottom")

            with cols_a_2[0]:
                pos_eli_anotacion: int = st.selectbox(
                    "Anotacion que desea eliminar:",
                    numero_de_anotaciones
                )
            with cols_a_2[1]:
                if st.button("Eliminar"):
                    fc.eliminar_anotacion(
                        index, pos_eli_anotacion,
                        ajustes, df
                    )
                    st.rerun()
