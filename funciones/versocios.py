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