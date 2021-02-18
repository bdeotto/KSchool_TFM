import pandas as pd
import numpy as np

def leyenda(dicc,col):
    """ Imprime los valores de la variable categórica 'col' y su descripción
    literal.
    """
    global LO_,LM,LM_
    dicc=dicc[col]
    n=0
    for k,v in dicc.items():
        if type(k)==str:
            print (k,'\t',v) # Evita imprimir claves duplicadas ('int' y 'str')
            n=n+1
    if n==0:
        for k,v in dicc.items():
            print (k,'\t',v) # Imprime leyenda de col. solo con claves 'int'
    return

def traduce(df,dicc,LO_,LM,LM_,col,check=True,save=True):
    """ Reemplaza los valores de la variable 'col' de acuerdo con su
    diccionario asociado.
    Si 'save'=True, la variable traducida se añade al dataset con nombre igual
    al de la columna original seguido de un guion bajo. El nombre de la
    variable traducida se añade a la lista de variables (v_originales_L
    o v_modelos_L) según esté designada con mayúsculas o minúsculas.
    Cuando 'check'=True o 'save'=False, imprime una salida de comprobación.
    Si save=False, elimina la variable de las listas de variables literales o
    redefinidas.
    """
    dicc=dicc[col]
    try: del df[str(col)+'_'] # Evita referencias desactualizadas cuando se usa más de una vez
    except: pass
    df['aux_traduce']=df[col].astype('O')  # Resuelve confictos con col. mixtas (strings e integers) y con Nan
    df['aux_traduce'].replace(dicc,inplace=True)
    if save==True:
        df[str(col)+'_']=df['aux_traduce']
        if col==col.upper() and str(col)+'_' not in LO_:
            LO_.append(str(col)+'_')
        if col==col.lower() and str(col) not in LM:
            LM.append(str(col))
        if col==col.lower() and str(col)+'_' not in LM_:
            LM_.append(str(col)+'_')
    if check==True or save==False:
        print (df[[col,'aux_traduce']].groupby(col).agg(['unique'])) # Salida de comprobación
    if save==False:
        if col==col.upper() and str(col)+'_' in LO_:
            LO_.remove(str(col)+'_')
        if col==col.lower() and str(col) in LM:
            LM.remove(str(col))
        if col==col.lower() and str(col)+'_' in LM_:
            LM_.remove(str(col)+'_')
    del(df['aux_traduce'])
    return
