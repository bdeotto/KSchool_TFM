#!usr/bin/env python3

import pandas as pd
import numpy as np
import openpyxl
import re

"""
DATAFRAMES AUXILIARES

Las hojas Tablas1 a Tablas3 del archivo 'dr_EILU_GRAD_2019.xlsx' contienen las
descripciones de los valores asociados a variables categóricas.

Se crea un dataframe auxiliar para cada hoja (Tabla1 hasta Tabla3) del fichero
de códigos, otro para la hoja de 'Diseño' y un diccionario que facilita la
selección del dataframe auxiliar adecuado en cada caso. Se usarán para
construir diccionarios que mapean los códigos numéricos en sus contenidos
literales:

D_df_aux[0]: df 'hoja de diseño de la encuesta'. Asocia cada variable a su
diccionario.
D_df_aux[1] a D_df_aux[3]: df que contienen las tablas Tabla1 hasta Tabla 3.
Recogen los diccionarios de las variables de la encuesta .
"""
ruta_aux='dr_EILU_GRAD_2019.xlsx'
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
**Las herramientas de traducción importan los diccionarios de la tabla de
diseño de la encuesta por nombre de diccionario y luego asocian cada variable
al diccionario que le corresponde**. Este proceso es más largo que construir
directamente un diccionario para cada variable, pero tiene la ventaja de ser
más eficiente en el uso de memoria:

- El **diccionario D_map_dict** es un diccionario auxiliar que asocia cada
variable a nombre del diccionario que le corresponde.
- La **función diccionario** importa los diccionarios por su nombre de
diccionario desde el fichero de diseño de la encuesta.
- El diccionario **D_dict** asocia cada variable al diccionario de traducción
que le corresponde. Así, para la variable 'nombre_de_variable', el diccionario
D_dict['nombre_de_variable'] tiene como claves los valores de la variable
categórica y como valores las interpretaciones de los códigos de acuerdo con
el diccionario asociado a la variable.
"""
"""
DICCIONARIO AUXILIAR D_map_dict

Diccionario auxiliar de denominaciones de diccionarios D_map_dict:
k=nombre de variable (string), v=nombre del diccionario asociado (string).

    Asocia cada variable categórica con el nombre de su diccionario asociado.
    Simplifica los argumentos de las funciones de traducción.

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
final de cada uno. Estas serán las entradas de la función 'diccionario' que
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
# Diccionario auxiliar de tablas: k=nombre de diccionario, v=tabla que lo contiene.
d_tabla=dict()
for i in range(1,4):
    for vble in globals()['L_tabla'+str(i)]:
        d_tabla[vble]=i
# Diccionario auxiliar de inicio: k=nombre de diccionario, v=fila de inicio de los códigos del diccionario.
d_inicio=dict()
for i in range(1,4):
    for vble in globals()['L_tabla'+str(i)]:
        d_inicio[vble]=D_df_aux[i][D_df_aux[i]['A']==vble].index[0]+1
# Diccionario auxiliar de final: k=nombre de diccionario, v=última fila de los códigos del diccionario.
d_final=dict()
for i in range(1,4):
    for n, vble in enumerate(globals()['L_tabla'+str(i)]):
        if n<len(globals()['L_tabla'+str(i)])-1:
            d_final[vble]=d_inicio[globals()['L_tabla'+str(i)][n+1]]-2
        else:
            d_final[vble]=len(D_df_aux[i])-1
d_final['TIPACRE']=d_final['TIPACRE']-1 # Corrección error en diccionario 'TIPACRE':
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
            # strip de comillas simples (en algunos int de las tablas de códigos):
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
"""
DICCIONARIOS POR NOMBRE DE VARIABLE

Diccionarios asociados a cada variable categórica D_dict: k=nombre de variable,
v=diccionario de traducción asociado a la misma.

Cada variable está asociada a un nombre de diccionario. Los diccionarios se
recuperan por su nombre mediante el diccionario D_map_dic. El diccionario
D_dict recupera el diccionario asociado a cada variable categórica a través del
nombre de la variable, sin necesidad de especificar el nombre del diccionario
asociado.
Así, D_dict['nombre_de_variable'] es el diccionario que permite traducir la
variable 'nombre_de_variable'.
"""
D_dict=dict()
for i in range(len(D_df_aux[0])):
    variable=D_df_aux[0]['Variable'].iloc[i]
    D_dict[variable]=diccionario(D_map_dict[variable])

"""
FUNCIONES DE TRADUCCIÓN:
"""
def leyenda(col):
    """ Imprime los valores de la variable categórica 'col' y su descripción
    literal.
    """
    dicc=D_dict[col]
    n=0
    for k,v in dicc.items():
        if type(k)==str:
            print (k,'\t',v) # Evita imprimir claves duplicadas ('int' y 'str')
            n=n+1
    if n==0:
        for k,v in dicc.items():
            print (k,'\t',v) # Imprime leyenda de col. solo con claves 'int'
    return
def traduce(col,dicc=None,check=True,save=True):
    """ Reemplaza los valores de la variable 'col' de acuerdo con su diccionario
    asociado (si diccionario=None) o
    con otro que se especifique.
    Si 'save'=True, la variable traducida se añade al dataset con índice igual
    al de la columna original
    seguido de un guion bajo. El nombre de la variable traducida se añade a la
    lista de variables (v_originales_L
    o v_modelos_L) según esté designada con mayúsculas o minúsculas.
    Cuando 'check'=True o 'save'=False, imprime una salida de comprobación.
    """
    if dicc==None:
        dicc=D_dict[col]
    try: del df[str(col)+'_'] # Evita referencias desactualizadas cuando se usa más de una vez
    except: pass
    df['aux_traduce']=df[col].astype('O')  # Resuelve confictos con col. mixtas (strings e integers) y con Nan
    df['aux_traduce']=df['aux_traduce'].replace(dicc)
    if save==True:
        df[str(col)+'_']=df['aux_traduce']
        if col==col.upper() and str(col)+'_' not in v_originales_L:
            v_originales_L.append(str(col)+'_')
        if col==col.lower() and str(col) not in v_modelos:
            v_modelos.append(str(col))
        if col==col.lower() and str(col)+'_' not in v_modelos_L:
            v_modelos_L.append(str(col)+'_')
    if check==True or save==False:
        print (df[[col,'aux_traduce']].groupby(col).agg(['unique'])) # Salida de comprobación
    if save==False:
        for lista in [v_originales_L, v_modelos, v_modelos_L]:
            lista=[name for name in lista if name!=str(col)+'_' and
            name!=str(col)]
    del(df['aux_traduce'])
    return

"""
OTROS DICCIONARIOS:
"""
# Variables nuevas:
D_dict['si_no']={0:'No',1:'Sí'}
D_dict['fem']={1:'Mujer',0:'Hombre'}
D_dict['esp']={0:'Nacionalidad no española',1:'Nacionalidad española'}
D_dict['eu27']={0:'No nacido en EU27',1:'Nacido en EU27'}
D_dict['tipo_centro']={0:'Privado',1:'Público'}
D_dict['a_dist']={0:'Formación presencial',1:'Formación a distancia'}
D_dict['univ_pa']={0:'Sin estudios universitarios',1:'Con estudios \
                   universitarios'}
D_dict['univ_ma']=D_dict['univ_pa']
D_dict['extr_sin_beca']=D_dict['si_no']
# Variables redefinidas:
for i in range(len(D_df_aux[0])):
    variable=D_df_aux[0]['Variable'].iloc[i]
    D_dict[str(variable).lower()]=D_dict[variable]
D_dict['extr_proxy']={0:'No estudió fuera de España',1:'Al menos parte de los \
                      estudios en el extranjero'}
D_dict['ambito_g1']=D_dict['AMBITO']
D_dict['ambito_g1'][0]='No tiene'
for variable in ['ambito_g'+str(i) for i in range(2,5)]:
    D_dict[variable]=D_dict['ambito_g1']
D_dict['rama_g1']=D_dict['RAMA']
D_dict['rama_g1'][0]='No tiene'
for variable in ['rama_g'+str(i) for i in range(2,5)]+['rama_doc']:
    D_dict[variable]=D_dict['rama_g1']
D_dict['fam_gsup1']=D_dict['EST_B25_FA1']
D_dict['fam_gsup1'][0]='No tiene'
for variable in ['fam_gsup'+str(i) for i in range(2,4)]:
    D_dict[variable]=D_dict['fam_gsup1']
D_dict['fam_gmedio1']=D_dict['EST_B29_FA1']
D_dict['fam_gmedio1'][0]='No tiene'
for variable in ['fam_gmedio'+str(i) for i in range(2,4)]:
    D_dict[variable]=D_dict['fam_gmedio1']
# Diccionario abreviado para 'ocupacion':
D_dict['ocupacion']=D_dict['TRABOC']
for k,v in D_dict['ocupacion'].items():
    v_aux=re.split('[:.(;]',v)[0]
    D_dict['ocupacion'][k]=v_aux
