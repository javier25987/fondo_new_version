import funciones.general as fg
import streamlit as st

st.header("Creacion de archivos de ajustes y almacenamiento.")
st.markdown(
    f"""
        > **NOTA:** En caso de necesitarse crear el archivo de ajustes y la tabla
        de socios cree primero el archivo de ajustes y despues la tabla
        ese orden es el adecuado para la operacion.

        > **NOTA:** En caso de haber creado el archivo de ajustes dirijase a el
        modo administrador y a ajustes, en esa pagina configure todo lo necesario
        de el archivo.
        """
)
if st.session_state.df_exist or st.session_state.ajustes_exist:
    if not st.session_state.ajustes_exist:
        if st.button("crear ajustes de el programa"):
            fg.crear_ajustes_de_el_programa()
            st.rerun()

    if not st.session_state.df_exist:
        if st.button("Crear nueva tabla de usuarios"):
            fg.crear_tabla_principal()
            st.rerun()
else:
    col1, col2 = st.columns(2)

    with col1:
        if st.button("crear ajustes de el programa"):
            fg.crear_ajustes_de_el_programa()
            st.rerun()

    with col2:
        if st.button("Crear nueva tabla de usuarios"):
            fg.crear_tabla_principal()
            st.rerun()