import streamlit as st
import funciones.general as fg
import pandas as pd

ajustes: dict = fg.abrir_ajustes()
df = pd.read_csv(ajustes["nombre df"])

index = st.session_state.usuario_actual_ver

index_de_usuario = st.sidebar.number_input(
    "Numero de usuario.",
    value=0,
    step=1
)

if st.sidebar.button("Buscar", key="00011"):
    pass

tabs = st.tabs(
    [
        "Buscar Usuarios", "Anotaciones", "Ver si necesita acuerdo",
        "Verificar ranura 16", "Buscar boleta", "Tabla de Usuarios",
        "Archivo de ajustes"
    ]
)

with tabs[1]:
    if index == -1:
        st.title("Usuario indeterminado")
    else:
        st.title(f"№ {index} - {df["nombre"][index].title()}")
        st.header(
            f"Multas extra: {"{:,}".format(df["multas_extra"][index])}"
        )
        st.divider()

        col_1, col_2 = st.columns(2)
        with col_1:
            n_anotacion = st.text_input("Nueva anotacion.")

        with col_2:
            n_monto_a_multas = st.number_input(
                "Valor de la anotacion (multa).",
                value=0,
                step=1
            )

        if st.button("Hacer nueva anotacion"):
            if "-" in n_anotacion:
                st.error(
                    "El simbolo '-' no puede estar incluido en la anotacion",
                    icon="🚨"
                )
            else:
                if n_monto_a_multas < 0:
                    simbolo_anotacion = "(menos)"
                else:
                    simbolo_anotacion = ""

                anotacion_h = df["anotaciones"][index]
                if anotacion_h == "-":
                    anotacion_h = (f"{n_anotacion} ~> {simbolo_anotacion}"
                                   f"{"{:,}".format(n_monto_a_multas)}")
                else:
                    anotacion_h += (f"-{n_anotacion} ~> {simbolo_anotacion}"
                                    f"{"{:,}".format(n_monto_a_multas)}")

                df.loc[index, "anotaciones"] = anotacion_h

                multas_extra = int(df["multas_extra"][index])
                multas_extra += n_monto_a_multas
                df.loc[index, "multas_extra"] = multas_extra

                df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
                df.to_csv(st.session_state.nombre_df)
                st.rerun()

        st.divider()

        anotaciones = df["anotaciones"][index].split("-")

        for i in anotaciones:
            st.write(i)
            st.divider()

with tabs[0]:
    c_1, c_2 = st.columns(2, vertical_alignment="bottom")

    with c_1:
        nombre_a_buscar = st.text_input("Nombre")

    with c_2:
        if st.button("Buscar"):
            st.rerun()

    st.divider()

    if st.session_state.nombre_para_busqueda == "":
        st.table(
            df[
                [
                    "numero", "nombre", "puestos",
                    "numero celular", "estado", "capital"
                ]
            ]
        )
    else:
        nuevo_data_frame = df[
            df["nombre"].str.contains(nombre_a_buscar, case=False, na=False)
        ]
        st.table(
            nuevo_data_frame[
                [
                    "numero", "nombre", "puestos",
                    "numero_telefonico", "estado", "capital"
                ]
            ]
        )

with tabs[2]:
    tabla_acuerdo = df[df["dinero por si mismo"] < df["capital"]//2]
    st.info(
        """
        Los siguientes usuarios no han retirado en prestamos la mitad de su capital
        """,
        icon="ℹ️"
    )
    st.table(
        tabla_acuerdo[
            [
                "numero", "nombre", "capital",
                "dinero por si mismo", "numero celular"
            ]
        ]
    )

with tabs[3]:
    pass

with tabs[4]:
    rifa_a_buscar = st.selectbox(
        "Seleccione la rifa en la que desea buscar.",
        (
            "1", "2", "3", "4"
        )
    )
    boleta_a_buscar = st.text_input("Selecciones la boleta que desea buscar,")

    if st.button("Buscar", key="00010"):
        tabla_boletas = df[
            df[f"r{rifa_a_buscar} boletas"].str.contains(
                boleta_a_buscar, case=False, na=False
            )
        ]
    else:
        tabla_boletas = df

    st.divider()
    st.table(
        tabla_boletas[
            ["numero", "nombre", f"r{rifa_a_buscar} boletas"]
        ]
    )

with tabs[5]:
    st.table(df)

with tabs[6]:
    ajustes["clave de acceso"] = "********"
    st.json(ajustes)