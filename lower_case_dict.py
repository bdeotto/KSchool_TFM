import pandas as pd
import numpy as np


df_dict=pd.read_csv('data/D_dict.csv',index_col=0)
df_describe=pd.read_csv('data/D_describe.csv',index_col=0)
df_ambito_to_rama=pd.read_csv('data/D_ambito_to_rama.csv',index_col=0)

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

d_describe=dict()
for key in df_describe.index:
    d_describe[key]=df_describe['valor'].loc[key]

D_ambito_to_rama=dict()
for key in df_ambito_to_rama.index:
    D_ambito_to_rama[key]=df_ambito_to_rama['valor'].loc[key]
