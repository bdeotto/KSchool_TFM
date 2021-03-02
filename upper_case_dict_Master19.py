import pandas as pd
import numpy as np
import openpyxl
import re

"""
DATAFRAMES AUXILIARES

Las hojas Tablas1 a Tablas3 del archivo 'dr_EILU_MAST_2019.xlsx' contienen las
descripciones de los valores asociados a variables categóricas.

Se adapta este módulo a partir del diseñado para la encuesta de Graduados 2019
para construir los diccionarios que son distintos en la encuesta de Máster 2019.
"""
ruta_aux='data/dr_EILU_MAST_2019.xlsx'
"""
D_df_aux: diccionario con función de selector de dataframes auxiliares
(facilita la definición de funciones sobre las distintas tablas)
"""
D_df_aux=dict()
# Df auxiliar con tabla Diseño:
D_df_aux[0]=pd.read_excel(ruta_aux,sheet_name='Diseño',engine='openpyxl',
                usecols='A:B,H:I',header=1,skiprows=0).dropna(how='all')
D_df_aux[0].reset_index(drop=True,inplace=True)
D_df_aux[0]
# Se prescinde de las variables sin diccionario asociado:
D_df_aux[0].drop(D_df_aux[0][D_df_aux[0]['Diccionario de la variable']\
                .isna()].index,inplace=True)
D_df_aux[0].reset_index(drop=True,inplace=True)
D_df_aux[0]
def load_aux(hoja):
    """ Crea un df auxilar para la hoja número 'hoja' del fichero de códigos
    de las variables de la encuesta y la carga en el diccionario de df
    auxiliarles D_df_aux.
    """
    out=pd.read_excel(ruta_aux,sheet_name='Tablas'+str(hoja),engine='openpyxl',
                                usecols=range(2),header=None,names=['A','B'])
    out=out.dropna(how='all')
    # Se eliminan las filas con las leyendas 'Código' y 'Descripción':
    out.drop(out[out['A']=='Código'].index,inplace=True)
    out.reset_index(drop=True,inplace=True)
    D_df_aux[hoja]=out
    return out
# Df auxiliares con hojas Tabla1 a Tabla2:
for i in range(1,4):
    load_aux(i)
"""
DICCIONARIOS DE TRADUCCIÓN PARA LAS VARIABLES CATEGÓRICAS

Cada variable categórica está asociada a un diccionario descrito en las tablas
Tabla1 a Tabla3.

La mayoría de estos diccionarios están asociados a más de una variable.
Se recuperan mediante la función diccionario, cuyo argumento es el nombre del
diccionario (no de las variables asociadas).
"""
"""
DICCIONARIO AUXILIAR D_map_dict

Diccionario auxiliar de denominaciones de diccionarios D_map_dict:
k=nombre de variable (string), v=nombre del diccionario asociado (string).

Asocia cada variable categórica con el nombre de su diccionario asociado.
Simplifica los argumentos de las funciones de traducción.
Se emplea en la construcción de la función diccionario.
"""
D_map_dict=dict()
for i in range(len(D_df_aux[0])):
    D_map_dict[D_df_aux[0]['Variable'].iloc[i]]=\
                D_df_aux[0]['Diccionario de la variable'].iloc[i]
"""
DICCIONARIOS DE TRADUCCIÓN DE VARIABLES POR NOMBRE DE DICCIONARIO

Diccionarios importados de las hojas Tabla 1 a Tabla 3 del fichero de diseño de
la encuesta. Las tablas se corresponden con los dataframes D_df_aux de índice
1 a 3.

Para importar los diccionaros identificamos la hoja y las filas de inicio y
final de cada uno. Estas serán entradas de la función 'diccionario' que
recupera los diccionarios uno a uno.

Se usan las siguientes herramientas:

- Listas globals()[L_tabla1] a globals()[L_tabla3]: Listas de diccionarios
contenidos en cada una de las tres tablas Tablai (i=1,2,3).

- Diccionario de tablas d_tabla: asocia cada nombre de diccionario con la
tabla que lo contiene.

- Diccionario de celdas de inicio d_inicio: asocia cada nombre de diccionario
con la fila en la que comienzan los códigos del diccionario.

- Diccionario de celdas de final d_final: asocia cada nombre de diccionario
con la última celda de códigos que le corresponden.

- La función diccionario: importa los códigos de cada uno de los diccionarios
a partir de su denominación. Cada nombre de diccionario está asociado a una
tabla, una celda de inicio y una celda de final (a través de los
diccionarios d_Tabla, d_Inicio y d_final). La función diccionario asocia
cada nombre de diccionario con el diccionario (claves y valores) que le
corresponden. Así, diccionario('nombre_de_diccionario') es un diccionario D
que permite traducir de acuerdo con el diccionario denominado
'nombre_de_diccionario'.
"""

# Listas de nombres de diccionarios en cada tabla:
for i in range(1,4):
    globals()['L_tabla'+str(i)]=D_df_aux[i]['A'][D_df_aux[i]['A']\
                                .isin(D_map_dict.values())].tolist()
# Diccionario auxiliar de tablas:
# k=nombre de diccionario, v=tabla que lo contiene.
d_tabla=dict()
for i in range(1,4):
    for vble in globals()['L_tabla'+str(i)]:
        d_tabla[vble]=i
# Diccionario auxiliar de inicio:
# k=nombre de diccionario, v=fila de inicio de los códigos del diccionario.
d_inicio=dict()
for i in range(1,4):
    for vble in globals()['L_tabla'+str(i)]:
        d_inicio[vble]=D_df_aux[i][D_df_aux[i]['A']==vble].index[0]+1
# Diccionario auxiliar de final:
# k=nombre de diccionario, v=última fila de los códigos del diccionario.
d_final=dict()
for i in range(1,4):
    for n, vble in enumerate(globals()['L_tabla'+str(i)]):
        if n<len(globals()['L_tabla'+str(i)])-1:
            d_final[vble]=d_inicio[globals()['L_tabla'+str(i)][n+1]]-2
        else:
            d_final[vble]=len(D_df_aux[i])-1
d_final['TIPACRE']=d_final['TIPACRE']-1 # Corrección error en dicc. 'TIPACRE'

def diccionario(dicc):
    """ Importa el diccionario denominado 'dicc' de acuerdo con las
    descripciones establecidas en el fichero de diseño/descripción de la
    encuesta. El resultado es un diccionario D para el cual:
    key = valor de variable a traducir,
    value = descripción/interpretación.
    El argumento dicc es la denominación del diccionario, y no el nombre de las
    variables categóricas asociadas al mismo.
    """
    tabla,inicio,final = d_tabla[dicc],d_inicio[dicc],d_final[dicc]
    df=D_df_aux[tabla]
    D=dict()
    for i in range(inicio,final+1):
        key=df['A'].iloc[i]
        if type(key)==str:
            # strip de comillas simples (en algunas k de las tablas de códigos):
            key=key.strip('\x27')
            try: key=int(key)
            except: pass
        D[key]=df['B'].iloc[i] # para claves int y float en el dataset
        # para claves str en el dataframe:
        D[str(df['A'].iloc[i])]=df['B'].iloc[i]
    # Corrección error en diccionario 'TIPACRE':
    if dicc=='TIPACRE':
        D[' ']='No_aplicable'
    return D
