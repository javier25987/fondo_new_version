import time
import pandas as pd
import streamlit as st
import subprocess
import datetime
import json
import os

def arreglar_asuntos(index: int) -> None:
    pass
    # with open('ajustes.json', 'r') as f:
    #     ajustes = json.load(f)
    #     calendario = ajustes['calendario'].split('-')
    #     f.close()
    #
    # df = pd.read_csv(ajustes['nombre df'])
    #
    # cuotas = df['cuotas'][index_usuario]
    # multas = df['multas'][index_usuario]
    #
    # multas = [i for i in multas]
    #
    # semanas_revisadas = int(df['revisiones'][index_usuario])
    #
    # calendario = list(map(lambda x: list(map(lambda y: int(y), x.split('/'))), calendario))
    # calendario = list(map(lambda x: datetime.datetime(*x), calendario))
    #
    # fecha_actual = datetime.datetime.now()
    #
    # semanas_a_revisar = list(map(lambda x: x < fecha_actual, calendario))
    # semanas_a_revisar = sum(map(int, semanas_a_revisar))
    #
    # if semanas_a_revisar > semanas_revisadas:
    #     for i in range(50):
    #         if calendario[i] > fecha_actual:
    #             break
    #         else:
    #             if cuotas[i] == 'p':
    #                 pass
    #             else:
    #                 if ajustes["cobrar multas"]:
    #                     multas = sumar_una_multa(multas, i)
    #
    #                 cuotas = modificar_string(cuotas, i, 'd')
    #
    #     df.loc[index_usuario, 'cuotas'] = cuotas
    #
    #     multas = ''.join(multas)
    #     df.loc[index_usuario, 'multas'] = multas
    #
    #     df.loc[index_usuario, 'revisiones'] = semanas_a_revisar
    #
    #     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    #
    #     df.to_csv(ajustes['nombre df'])