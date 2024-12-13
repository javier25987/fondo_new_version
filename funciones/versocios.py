def ingresar_usuario(index: int, ajustes: dict, df) -> (bool, str):
    if 0 <= index < ajustes["usuarios"]:
        if df["estado"][index] == "activo":
            return True, ""
        else:
            return False, f"El usuario № {index} esta desactivado"
    else:
        return False, "Numero de usuario fuera de rango"


def realizar_anotacion(
    index: int, anotacion: str, monto: int, ajustes: dict, df
) -> tuple[bool, str]:
    anotaciones: str = df["anotaciones generales"][index]

    if "_" in anotacion:
        return False, "El simbolo '_' no puede estar en la anotacion"
    elif "$" in anotacion:
        return False, "El simbolo '$' no puede estar en la anotacion"
    elif ":" in anotacion:
        return False, "El simbolo ':' no puede estar en la anotacion"
    elif anotacion == "":
        return False, "La anotacion esta vacia"
    else:
        anotacion += f": $ {monto}"
        if anotaciones == "n":
            anotaciones = anotacion
        else:
            anotacion = "_" + anotacion
            anotaciones += anotacion

        multas_actuales: int = df["multas extra"][index]

        multas_actuales += monto

        df.loc[index, f"anotaciones generales"] = anotaciones
        df.loc[index, f"multas extra"] = multas_actuales

        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df.to_csv(ajustes["nombre df"])

        return True, ""


def modificar_anotacion(
        index: int, pos: int, new_elem: str,
        ajustes: dict, df
):
    anotaciones: str = df["anotaciones generales"][index]
    anotaciones: list[str] = anotaciones.split("_")

    if "_" in new_elem:
        return False, "El simbolo '_' no puede estar en la anotacion"
    elif "$" in new_elem:
        return False, "El simbolo '$' no puede estar en la anotacion"
    elif ":" in new_elem:
        return False, "El simbolo ':' no puede estar en la anotacion"
    else:
        anotacion: str = anotaciones[pos]
        monto: str = anotacion[anotacion.find(":"):]
        if new_elem == "":
            anotaciones[pos] = "n" + monto
        else:
            anotaciones[pos] = new_elem + monto

        anotaciones = "_".join(anotaciones)

        df.loc[index, f"anotaciones generales"] = anotaciones
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        df.to_csv(ajustes["nombre df"])
        return True, ""

def buscar_boleta(
        df, rifa_a_buscar: str, boleta_a_buscar: str, poscion_boleta: int
):
    tabla_prueva = df[
        df[f"r{rifa_a_buscar} boletas"].str.contains(
            boleta_a_buscar, case=False, na=False
        )
    ]

    numeros = list(tabla_prueva["numero"])

    if len(numeros) <= 0:
        return -1
    elif len(numeros) == 1:
        return numeros[0]

    for i in numeros:
        objetos: list[str] = df[f"r{rifa_a_buscar} boletas"][i].split("_")
        new_objetos: list = []

        for n in objetos:
            new_objetos += [
                m.split("?") for m in n.split("#")
            ]

        for k in new_objetos:
            if k[poscion_boleta - 1] == boleta_a_buscar:
                return i

    return -1 # esto solo se activa si hay algun error
