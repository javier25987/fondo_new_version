# Proyecto fondo san javier

## Anotaciones

> En el fondo hay una gerarquia de simbolos para separar los elementos de un string la gerarquia es la siguiente ```_ >> # >> ?```

> El simbolo ```/``` se reserva unicamente para las fechas y para nada mas

> En el apartado de prestamos el orden de la informacion es el siguiente ```interes_"intereses vencidos"_revisiones_deuda_fiadores_"deuda con fiadores"```

## Deuda tecnica

* algoritmo para identificar boletas repetidas (seccion de rifas)

## Secciones finalizadas

* [X] arranque
* [X] menu
* [X] cuotas
* [X] prestamos
* [ ] rifas
* [X] ver socios
* [X] ajustes
* [X] modificar socios

## Errores de el programa

actualmenre solo hay que añadir un boton de actualizacion que copie todos los
hechos en el repositorio madre esto no se considera como un error ya que es
solo una funcion que puede ser descartada por el problema de que git no resuelve
los conflictos de un merge automaticamente

> actualmente es esencial a la hora de descargar el programa borrar el archivo
> .gitignore de lo contrario los cambios no se guargaran en el repositorio remoto

## Codigo que elimine y podria servir en un futuro

```python
"""
    tabla_ranura["p16 estado"] = tabla_ranura[
        "p16 estado"
    ].apply(
        lambda x: "✅" if x == "activo" else "🚨"
    )
"""
```

## Agradecimiento

Este proyecto fue hecho para mi padre al cual le agradezo todo lo que me ha dado
y la educacion que me esta pagando ya que gracias a eso obtuve los conocimientos
para realizar este proyecto,

GRACIAS PAPA
