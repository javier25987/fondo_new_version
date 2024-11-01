import streamlit as st
import datetime
import os
import funciones.general as fg
import funciones.menu as fm

st.set_page_config(layout="wide")

ajustes: dict = fg.abrir_ajustes()

st.session_state.nombre_para_busqueda = ''

st.session_state.usuario_actual_cuotas = -1
st.session_state.usuario_actual_prestamos = -1
st.session_state.usuario_actual_ver = -1
st.session_state.usuario_actual_rifas = -1

st.title('Menu de inicio')

st.markdown(
        '''
        El menu es la parte de este programa dedicada a guardar unas cuantas
        funciones de el programa, unos cuantos tutoriales y generar en la 
        cache todo lo necesario para la interfaz de el programa.
        '''
)
st.divider()

col_1, col_2 = st.columns(2)

with col_1:
    st.header('Guardar tabla')
    st.divider()
    if st.button("📤 Guardar En GitHub"):
        fm.guardar_tabla()

    st.link_button("🔗 Abrir GitHub", ajustes["enlace repo"])

with col_2:
    st.header("Cargar multas")
    st.markdown(
            """
            Esta parte esta dedicada a cargar las multas para todos los 
            usuarios de el programa haciendo que a los usuarios que no 
            pagaron se les sume la multa de la semana correspondiente.
            > **NOTA:** por favor oprima este boton cada lunes despues 
            de la hora limite
            """
    )
    if st.button("Cargar Multas"):
        fm.cargar_multas()



            # st.info(
            #     """
            #     Por favor al ingresar cantidades en miles no ingrese las comas,
            #     solo el numero plano.
            #     """,
            #     icon="ℹ️"
            # )



