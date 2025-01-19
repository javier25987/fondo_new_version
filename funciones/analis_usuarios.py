import funciones.cuotas as fc
import datetime


def obtener_estado_de_cuenta(
    index: int, prestamos_activos: int, deudas_de_prestamos: int, df
):
    ahora = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")

    formato = [
        "============================== Fondo San Javier ==============================\n",
        "\n",
        f"     № {df['numero'][index]}: {df['nombre'][index].title()} - {df['puestos'][index]} puesto(s)\n",
        "\n",
        f"los siguientes datos son validos para la fecha {ahora} para otras\n",
        "fechas no se confirma su veracidad.\n",
        "\n",
        "Pago de cuotas:\n",
        f"- Cuotas pagas: {df['cuotas'][index].count('p')}\n",
        f"- Cuotas que se deben: {df['cuotas'][index].count('d')}\n",
        f"- Multas pendientes: {fc.contar_multas(df['multas'][index])}\n",
        f"- Estado: {df['estado'][index]}\n",
        f"- Capital: {df['capital'][index]:,}\n",
        f"- Dinero pagado en multas: {df['aporte a multas'][index]:,}\n",
        f"- Multas extra: {df['multas extra'][index]:,} \n",
        f"- Numero de telefono: {df['numero celular'][index]}\n",
        "\n",
        "Prestamos:\n",
        f"- Prestamos solitados: {df['prestamos hechos'][index]}\n",
        f"- Dinero retirado en prestamos: {df['dinero en prestamos'][index]:,}\n",
        f"- Prestamos activos: {prestamos_activos}\n",
        f"- Deudas en prestamos: {deudas_de_prestamos:,}\n\n",
        f"- Deudas por fiador: {df['deudas por fiador'][index]:,}\n",
        f"- Fiador de: {df['fiador de'][index]}\n",
    ]

    with open("text/estado_de_cuenta.txt", "w", encoding="utf-8") as f:
        f.write("".join(formato))
        f.close()
