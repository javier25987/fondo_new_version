import funciones.ajustes as fa
import funciones.general as fg
import streamlit as st
import pandas as pd
import os

st.title("Ajustes")

tab = list(
    st.tabs(
        [
            "Calendario", "Cuotas y multas", "Contraseñas",
            "Intereses", "Usuarios", "Fechas", "Tabla de usuarios",
            "Guardado de datos", "Rifas"
        ]
    )
)
key = 1

ajustes:dict = fg.abrir_ajustes()

with tab[0]:
    st.header("Calendario:")

    calendario = ajustes["calendario"]

    if calendario == "n":
        st.error("No hay un calendario", icon="🚨")
        st.subheader("Crear calendario:")
    else:
        calendario = calendario.split("_")
        hora_de_corte = calendario[1][-2:]
        calendario = list(
            map(
                lambda x: x[:-3],
                calendario
            )
        )
        # calendario += ['____/__/__']

        st.markdown(f"##### Hora de cierre: {hora_de_corte}")
        st.table(
            pd.DataFrame(
                {
                    "1 ~ 10": calendario[:10],
                    "11 ~ 20": calendario[10:20],
                    "21 ~ 30": calendario[20:30],
                    "31 ~ 40": calendario[30:40],
                    "41 ~ 50": calendario[40:]
                }
            )
        )
        st.subheader("Modificar calendario:")

    col0 = st.columns(4)

    with col0[0]:
        n_hora = st.number_input("Hora de cierre: ", value=19, step=1)

    with col0[1]:
        n_fecha_inicial = st.date_input("Fecha inicial: ")
    with col0[2]:
        n_fecha_doble_1 = st.date_input("Primera fecha doble: ")
    with col0[3]:
        n_fecha_doble_2 = st.date_input("Segunda fecha doble: ")

    if st.button("Crear calendario", key=f"key: {key}"):
        n_hora = str(n_hora)
        n_fecha_inicial = n_fecha_inicial.strftime("%Y/%m/%d") + "/" + n_hora
        n_fecha_doble_1 = n_fecha_doble_1.strftime("%Y/%m/%d") + "/" + n_hora
        n_fecha_doble_2 = n_fecha_doble_2.strftime("%Y/%m/%d") + "/" + n_hora

        if n_fecha_doble_1 == n_fecha_doble_2:
            st.error("Las fechas dobles no pueden coincidir", icon="🚨")
        else:
            ajustes["calendario"] = fa.crear_listado_de_fechas(
                n_fecha_inicial,
                [n_fecha_doble_1, n_fecha_doble_2]
            )
            fa.guardar_y_avisar(ajustes)
    key += 1

with tab[1]:
    st.header("Valor de la cuota por puesto y por multa:")

    st.markdown(
        f"> **NOTA:** por favor no ingrese comas o puntos separadores de miles"
    ) # icon="ℹ️"

    col1 = st.columns(2)

    with col1[0]:
        st.subheader("Por puesto:")

        st.write(
            f"Valor de la cuota por puesto: {"{:,}".format(ajustes["valor cuota"])}"
        )

        n_cuota_puesto = st.number_input(
            "Nuevo valor de la cuota:",
            value=10000,
            step=1
        )

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["valor cuota"] = n_cuota_puesto
            fa.guardar_y_avisar(ajustes)
        key += 1

    with col1[1]:
        st.subheader("Por multa:")
        st.write(
            f"Valor de la multa por puesto: {"{:,}".format(ajustes["valor multa"])}"
        )
        n_cuota_multa = st.number_input(
            "Nuevo valor de la multa:", value=3000, step=1
        )

        if st.button('Modificar', key=f"key: {key}"):
            ajustes["valor multa"] = n_cuota_multa
            fa.guardar_y_avisar(ajustes)
        key += 1

with tab[2]:
    col2 = st.columns(2)

    with col2[0]:
        st.subheader("Clave de acceso actual: ")

        st.markdown(f"#### > *{ajustes["clave de acceso"]}*")

    with col2[1]:
        nueva_clave = st.text_input("Nueva clave de acceso:")

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["clave de acceso"] = nueva_clave
            fa.guardar_y_avisar(ajustes)
        key += 1

with tab[3]:
    st.markdown("## Tope de intereses:")

    st.markdown(
        """
        > **NOTA:** el tope de intereses determina que interes va
        a tener un prestamo dependiendo si pasa el tope o no
        """
    )
    col3_1 = st.columns(2)

    with col3_1[0]:
        st.markdown(
            f"##### Tope actual: {
            "{:,}".format(ajustes["tope de intereses"])
            }"
        )

    with col3_1[1]:
        nuevo_tope = st.number_input(
            "Nuevo tope:",
            value=20000000, step=1
        )
        if st.button("Modificar", key=f"key: {key}"):
            ajustes["tope de intereses"] = nuevo_tope
            fa.guardar_y_avisar(ajustes)
        key += 1
    st.divider()
    st.markdown("## Interes por prestamo:")

    st.markdown(
        """
        > **NOTA:** los intereses son un numero entero entre 0 y 100
        por favor no introduzca numeros decimales, el programa no los
        puede trabajar bien y puede generar errores en el futuro
        """
    )
    col3_2 = st.columns(2)

    with col3_2[0]:
        st.markdown("### Menos de el tope:")
        st.markdown(
            f"##### el interes actual por prestamo es: "
            f"{ajustes["interes < tope"]} %"
        )
    with col3_2[1]:
        nuevo_interes_m_tope = st.number_input(
            "Nuevo interes menor a el tope:",
            value=3, step=1
        )
        if st.button("Modificar", key=f"key: {key}"):
            ajustes["interes < tope"] = nuevo_interes_m_tope
            fa.guardar_y_avisar(ajustes)
        key += 1
        st.divider()

    col3_3 = st.columns(2)

    with col3_3[0]:
        st.markdown("### Mas de el tope:")
        st.markdown(
            f"##### el interes actual por prestamo es: "
            f"{ajustes["interes > tope"]} %"
        )
    with col3_3[1]:
        nuevo_interes_M_tope = st.number_input(
            "Nuevo interes mayor a el tope:",
            value=2, step=1
        )
        if st.button("Modificar", key=f"key: {key}"):
            ajustes["interes > tope"] = nuevo_interes_M_tope
            fa.guardar_y_avisar(ajustes)
        key += 1

with tab[4]:
    st.header("Usuarios")

    col4_1 = st.columns(2)

    with col4_1[0]:
        st.markdown("### Numero de usuarios:")

        st.write(
            f"actualmete en el programa hay "
            f"[ {ajustes["usuarios"]} ] usuarios"
        )
    with col4_1[1]:
        nuevo_usuarios = st.number_input(
            "Nuevo numero de usuarios:",
            value=0, step=1
        )
        if st.button("Modificar", key=f"key: {key}"):
            ajustes["usuarios"] = nuevo_usuarios
            fa.guardar_y_avisar(ajustes)
        key += 1
    st.divider()

    col4_2 = st.columns(2)

    with col4_2[0]:
        st.subheader("Desactivar usuarios:")
        if ajustes["anular usuarios"]:
            st.write("Los usuarios seran desactivados")
        else:
            st.write("Los usuarios NO seran desactivados")

        if st.button("Invertir", key=f"key: {key}"):
            ajustes["anular usuarios"] = not ajustes["anular usuarios"]
            fa.guardar_y_avisar(ajustes)
        key += 1

    with col4_2[1]:
        st.subheader("Cobrar multas")
        if ajustes["cobrar multas"]:
            st.write("Actualmente se generan multas")
        else:
            st.write("Actualmete NO se generan multas")

        if st.button("Invertir", key=f"key: {key}"):
            ajustes["cobrar multas"] = not ajustes["cobrar multas"]
            fa.guardar_y_avisar(ajustes)
        key += 1

with tab[5]:
    col5 = st.columns(2)

    with col5[0]:
        st.subheader("Fecha de cierre: ")

        st.write(
            f"fecha de cierre actual: "
            f"{ajustes["fecha de cierre"]}"
        )

    with col5[1]:
        n_fecha = st.date_input("Nueva fecha de cierre:")

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["fecha de cierre"] = n_fecha.strftime("%Y/%m/%d")
            fa.guardar_y_avisar(ajustes)
        key += 1

    st.markdown(
        """
        > **NOTA:** la fecha de cierre es la que dice hasta cuando hay
        plazo de pagar los prestamos, todas las fechas de pago de un 
        prestamo se generan hasta la fecha de cierre
        """
    )

with tab[6]:
    col6_1 = st.columns(2)

    with col6_1[0]:
        st.subheader("Nombre de la tabla:")
        st.write(
            f"Tabla de trabajo actual: {ajustes["nombre df"]}"
        )
    with col6_1[1]:
        n_nombre_tabla = st.text_input("Nuevo nombre:")

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["nombre df"] = n_nombre_tabla
            fa.guardar_y_avisar(ajustes)
        key += 1
    st.divider()

    col6_2 = st.columns(2)
    with col6_2[0]:
        st.subheader("Numero de generacion:")
        st.write(
            f"Numero de generacion actual: "
            f"{ajustes["numero de creacion"]}"
        )
    with col6_2[1]:
        n_numero_gen = st.number_input(
            "Nuevo numero de generacion:",
            value=0, step=1
        )
        if st.button("Modificar", key=f"key: {key}"):
            ajustes["numero de creacion"] = n_numero_gen
            fa.guardar_y_avisar(ajustes)
        key += 1

with tab[7]:
    col7_1 = st.columns(2)

    with col7_1[0]:
        st.subheader("Ruta de el programa: ")
        st.write(f"Ruta de el programa: {ajustes["path programa"]}")

    with col7_1[1]:
        if st.button("Configurar path", key=f"key: {key}"):
            ajustes["path programa"] = os.getcwd()
            fa.guardar_y_avisar(ajustes)
        key += 1
    st.divider()

    col7_2 = st.columns(2)

    with col7_2[0]:
        st.subheader("Enlace de el repositorio")
        st.write(f"Enlace actual: {ajustes["enlace repo"]}")

    with col7_2[1]:
        n_enlace = st.text_input("Nuevo enlace:")

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["enlace repo"] = n_enlace
            fa.guardar_y_avisar(ajustes)
        key += 1
    st.divider()

    col7_3 = st.columns(2)

    with col7_3[0]:
        st.subheader("Commits hechos")
        st.write(f"Commits realizados: {ajustes["commits hechos"]}")

    with col7_3[1]:
        n_comits = st.number_input(
            "Nuevos commits:",
            value=0, step=1
        )

        if st.button("Modificar", key=f"key: {key}"):
            ajustes["commits hechos"] = n_comits
            fa.guardar_y_avisar(ajustes)
        key += 1

