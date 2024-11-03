import streamlit as st
import funciones.general as fg
import funciones.menu as fm

ajustes: dict = fg.abrir_ajustes()

st.title("Menu de inicio")

st.markdown(
        """
        El menu es la parte de este programa dedicada a guardar unas cuantas
        funciones de el programa, unos cuantos tutoriales y generar en la 
        cache todo lo necesario para la interfaz de el programa.
        """
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("Guardar tabla")
    st.divider()
    if st.button("📤 Guardar En GitHub"):
        fm.hacer_commit()

    st.link_button("🔗 Abrir GitHub", ajustes["enlace repo"])

with col2:
    st.header("Cargar multas")
    st.markdown(
            """
            Esta parte esta dedicada a cargar las multas para todos los 
            usuarios de el programa haciendo que a los usuarios que no 
            pagaron se les sume la multa de la semana correspondiente.
            > **NOTA:** por favor oprima este boton cada lunes despues 
            de la hora de cierre
            """
    )

    if st.button("Cargar Multas"):
        fm.cargar_multas()
