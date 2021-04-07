import pandas as pd
import numpy as np

# Diccionario de diccionarios d_dict:

df_dict=pd.read_csv('data/D_dict.csv',index_col=0)
d_dict=dict()
for variable in df_dict.columns:
    d_dict[variable]=dict()
    dfv=df_dict[variable].dropna() # Solo sobre la columna relevante para eliminar no informados
    dfv=dfv.drop_duplicates()
    for key in dfv.index:
        value=dfv.loc[key]
        d_dict[variable][key]=value
        try:
            key_n=int(key)
            d_dict[variable][key_n]=value
        except: pass

# Resto de diccionarios:

df_describe=pd.read_csv('data/D_describe.csv',index_col=0)
d_describe=dict(zip(df_describe.index,\
                         df_describe[df_describe.columns[0]]))

df_titulo_grado_a_rama=pd.read_csv('data/D_titulo_grado_a_rama.csv',index_col=0)
D_titulo_grado_a_rama=dict(zip(df_titulo_grado_a_rama.index,\
                    df_titulo_grado_a_rama[df_titulo_grado_a_rama.columns[0]]))

df_titulo_grado_a_ambito=pd.read_csv('data/D_titulo_grado_a_ambito.csv',\
                                      index_col=0)
D_titulo_grado_a_ambito=dict(zip(df_titulo_grado_a_ambito.index,\
                df_titulo_grado_a_ambito[df_titulo_grado_a_ambito.columns[0]]))

df_ambito_a_rama=pd.read_csv('data/D_ambito_a_rama.csv',index_col=0)
D_ambito_a_rama=dict(zip(df_ambito_a_rama.index,\
                         df_ambito_a_rama[df_ambito_a_rama.columns[0]]))

df_ocupaciones=pd.read_csv('data/D_ocupaciones.csv',index_col=0)
D_ocupaciones=dict(zip(df_ocupaciones.index,\
                         df_ocupaciones[df_ocupaciones.columns[0]]))

df_cnae_a_num=pd.read_csv('data/D_cnae_a_num.csv',index_col=0)
D_cnae_a_num=dict(zip(df_cnae_a_num.index,\
                         df_cnae_a_num[df_cnae_a_num.columns[0]]))
