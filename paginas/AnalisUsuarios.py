import funciones.analis_usuarios as fa
import funciones.general as fg
import streamlit as st
import pandas as pd
import datetime

from administrador.ModificarSocios import index_modificar

# if st.button("Estado de cuenta"):
#     with st.spinner("Obteniendo estado de cuenta..."):
#         fa.obtener_estado_de_cuenta(index, df)
#         os.system("notepad.exe text/estado_de_cuenta.txt")

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

index: int = st.session_state.usuario_actual_analis

index_de_usuario: int = st.sidebar.number_input(
    "Numero de usuario:", value=0, step=1
)
if st.sidebar.button("Buscar"):

    if 0 <= index_de_usuario < ajustes["usuarios"]:
        st.session_state.usuario_actual_analis = index_de_usuario
        st.rerun()
    else:
        st.error(
            "Usuario fuera de rango", icon="🚨"
        )

tabs = st.tabs(
    ["Informacion General", "Usuario En Concreto"]
)

with tabs[0]:
    st.title("Informacion general")
    st.markdown(
        f"> ### {datetime.datetime.now().strftime("%Y/%m/%d %H:%M")}"
    )

    # obtener dinero adeudado en presamos

    dinero_adeudado_prestamos: int = 0

    for i in range(ajustes["usuarios"]):
        for j in range(1, 17):
            dinero_adeudado_prestamos += int(
                df[f"p{j} prestamo"][i].split("_")[3]
            )


    informacion_general = pd.DataFrame(
        {
            "Item": [
                "Capital", "Pagos en multas", "Anotaciones generales",
                "Prestamos solicitados", "Dinero adeudado en prestamos",
                "Interese vencidos"
            ],
            "Monto": [
                f"{df["capital"].sum():,}", f"{df["aporte a multas"].sum():,}",
                f"{df["multas extra"].sum():,}", f"{df["prestamos hechos"].sum():,}",
                f"{dinero_adeudado_prestamos:,}", f"{df["dinero por intereses vencidos"].sum():,}"
            ]
        }
    )
    st.table(informacion_general)

with tabs[1]:
    pass
