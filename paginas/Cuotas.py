import streamlit as st
import pandas as pd
import funciones.general as fg
import funciones.cuotas as fc
import os

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

index = st.session_state.usuario_actual_cuotas

index_de_usuario = st.sidebar.number_input(
    "Numero de usuario:", value=0, step=1
)
if st.sidebar.button("Buscar"):
    estado = fc.abrir_usuario(index_de_usuario)
    if estado[0]:
        st.session_state.usuario_actual_cuotas = index_de_usuario
        st.rerun()
    else:
        st.error(
            estado[1],
            icon="🚨"
        )

if index == -1:
    st.title("Usuario indeterminado")
else:
    nombre_usuario = df["nombre"][index].title()
    st.title(
        f"№ {index} - {df["nombre"][index].title()} : {
        df["puestos"][index]} puesto(s)"
    )

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
                fc.obtener_estado_de_cuenta(index)
                os.system("notepad.exe text/estado_de_cuenta.txt")

    st.divider()

    df1, df2 = fc.tablas_para_cuotas_y_multas(index)
    col2_1, col2_2 = st.columns(2)

    with col2_1:
        st.table(df1)

    with col2_2:
        st.table(df2)

    numero_cuotas_a_pagar: int = 50 - df["cuotas"][index].count("p")

    numero_cuotas_a_pagar = 10 if numero_cuotas_a_pagar > 10 else \
        numero_cuotas_a_pagar

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
                "No se que desea pagar.",
                icon="🚨"
            )
        else:
            st.balloons()
            fc.formulario_de_pago(
                index,
                cuotas_a_pagar,
                multas_a_pagar,
                tesorero_a_pagar
            )
    if col3_2.button("Abrir ultimo cheque"):
        with st.spinner("Abriendo cheque..."):
            os.system("notepad.exe text/cheque_de_cuotas.txt")
