import funciones.versocios as fv
import funciones.general as fg
import streamlit as st
import pandas as pd

ajustes: dict = fg.abrir_ajustes()
banco: dict = fg.abrir_banco()
df = pd.read_csv(ajustes["nombre df"])

index = st.session_state.usuario_actual_ver

index_de_usuario = st.sidebar.number_input("Numero de usuario.", value=0, step=1)

if st.sidebar.button("Buscar", key="00011"):
    estado: (bool, str) = fv.ingresar_usuario(index_de_usuario, ajustes, df)
    if estado[0]:
        st.session_state.usuario_actual_ver = index_de_usuario
        st.rerun()
    else:
        st.error(estado[1], icon="🚨")

tabs = st.tabs(
    [
        "Anotaciones",
        "Buscar Usuarios",
        "Ver si necesita acuerdo",
        "Verificar ranura 16",
        "Buscar boleta",
        "Tabla de socios",
    ]
)
with tabs[0]:
    if index == -1:
        st.title("Usuario indeterminado")
    else:
        st.title(f"№ {index} - {df['nombre'][index].title()}")

        st.subheader("Realizar una anotacion:")
        anotacion: str = st.text_input("Nueva anotacion:")

        cols_a_0 = st.columns(2, vertical_alignment="bottom")

        with cols_a_0[0]:
            monto_anotacion: int = st.number_input(
                "Monto de la anotacion:", value=0, step=1
            )
        with cols_a_0[1]:
            if st.button("Realizar anotacion"):
                estado_anotacion: (bool, str) = fv.realizar_anotacion(
                    index, anotacion, monto_anotacion, ajustes, df
                )
                if estado_anotacion[0]:
                    st.rerun()
                else:
                    st.error(estado_anotacion[1], icon="🚨")

        st.divider()
        st.subheader("Anotaciones hechas:")

        anotaciones: str = df["anotaciones generales"][index].split("_")

        count: int = 0
        numero_de_anotaciones: list[int] = []
        for i in anotaciones:
            st.markdown(f"> **№ {count}:** {i}")
            numero_de_anotaciones.append(count)
            count += 1

        st.markdown(
            f"> ##### Total de anotaciones: {df['multas extra'][index]:,}"
        )
        st.divider()
        st.subheader("Modificar anotaciones:")

        new_anotacion: str = st.text_input("Nueva anotacion modificada:")

        cols_a_1 = st.columns(2, vertical_alignment="bottom")

        with cols_a_1[0]:
            pos_mod_anotacion: int = st.selectbox(
                "Anotacion que desea modificar:", numero_de_anotaciones
            )
        with cols_a_1[1]:
            if st.button("Modificar"):
                modificar: (bool, str) = fv.modificar_anotacion(
                    index, pos_mod_anotacion, new_anotacion, ajustes, df
                )
                if not modificar[0]:
                    st.error(modificar[1], icon="🚨")
                else:
                    st.rerun()

with tabs[1]:
    cols = st.columns([6, 4], vertical_alignment="bottom")

    with cols[0]:
        nombre_a_buscar = st.text_input("Nombre apellido o segmento a buscar:")
    with cols[1]:
        if st.button("Buscar"):
            st.session_state.nombre_para_busqueda = nombre_a_buscar
            st.rerun()
    st.divider()

    if st.session_state.nombre_para_busqueda == "":
        st.table(
            df[["numero", "nombre", "puestos", "numero celular", "estado", "capital"]]
        )
    else:
        n_df = df[df["nombre"].str.contains(nombre_a_buscar, case=False, na=False)]
        st.table(
            n_df[["numero", "nombre", "puestos", "numero celular", "estado", "capital"]]
        )

with tabs[2]:
    tabla_acuerdo = df[df["dinero por si mismo"] < df["capital"] // 2]
    st.table(
        tabla_acuerdo[
            ["numero", "nombre", "capital", "dinero por si mismo", "numero celular"]
        ]
    )

with tabs[3]:
    tabla_ranura = df[["numero", "nombre", "p16 estado"]]

    for i in range(len(tabla_ranura["p16 estado"])):
        tabla_ranura.loc[i, "p16 estado"] = (
            "✅" if tabla_ranura["p16 estado"][i] == "activo" else "🚨"
        )

    st.table(tabla_ranura)

with tabs[4]:
    rifa_a_buscar: str = st.selectbox(
        "Seleccione la rifa en la que desea buscar:", ("1", "2", "3", "4")
    )

    col4_1 = st.columns(2)

    with col4_1[0]:
        boleta_a_buscar: str = st.text_input("Numero que desea buscar en la boleta:")

    with col4_1[1]:
        numeros_boleta: str = ajustes[f"r{rifa_a_buscar} numeros por boleta"]

        poscion_boleta: str = st.selectbox(
            "Posicion de el numero en la boleta:", range(1, numeros_boleta + 1)
        )

    tabla_boletas = df

    if st.button("Buscar", key="00010"):
        if boleta_a_buscar != "":
            if poscion_boleta is not None:
                numero_usuario_boleta: int = fv.buscar_boleta(
                    df, rifa_a_buscar, boleta_a_buscar, poscion_boleta
                )
                if numero_usuario_boleta >= 0:
                    tabla_boletas = df[df["numero"] == numero_usuario_boleta]

    st.divider()
    st.table(tabla_boletas[["numero", "nombre", f"r{rifa_a_buscar} boletas"]])

with tabs[5]:
    st.table(df)
