
def proporciones(col,dropna=False):
    """ Frecuencias relativas de los valores que toma una variable categórica en orden ascendente.
    Si dropna=False, incluye los valores NaN."""

    global df
    out=df[col].value_counts(normalize=True,ascending=False,dropna=dropna)
    out=pd.DataFrame(out)
    return out

def dist_condicionada(col,cond,rev=False,dropna=True):
    """ Distribución de la columna col condicionada por la columna cond y diferencias relativas con la
    distribución no condicionada de la variable col.
    Si rev=True, distribución de cond condicionada por col.
    Si dropna=True, prescinde de registros NaN."""

    global df
    # Permutación de col y cond con rev=True:
    if rev==True:
        temp=col
        col=cond
        cond=temp
    # Frecuencias relativas condicionadas:
    out=df[[cond,col]].groupby([cond,col],dropna=dropna).agg({col:'count'})\
                .div(df[[cond,col]].groupby(cond,dropna=dropna).agg({col:'count'}),level=cond)
    # Columna con distribución no condicionada de variable col (frecuencias relativas):
    out['no_cond']=0
    out['no_cond']=out['no_cond'].\
                                add(df[col].value_counts(normalize=True,dropna=dropna),level=col)
    # Columna de diferencias entre distribuciones condicionadas y no condicionada:
    out['dif']=out[col].sub(out['no_cond'],level=col)
    # Columna auxiliar de diferencias relativas (respecto a frecuencias no condicionadas):
    out['3. dif relativas']=out['dif'].div(df[col].value_counts(normalize=True,dropna=dropna),level=col)
    # Renombra columna de frecuencias condicionadas (evita conflictos índice fila y columna en pivot table):
    out.rename(columns={col:'1. fr. relativas condicionadas'},inplace=True)

    pt=pd.pivot_table(data=out,index=col,columns=[cond],\
                      values=['1. fr. relativas condicionadas','3. dif relativas'])
    pt.sort_index(inplace=True)

    # Nueva columna de frecuencias no condicionadas (más sencillo que ajustar la auxiliar):
    pt['2. fr relativas '+str(col)]=0
    pt['2. fr relativas '+str(col)]=pt['2. fr relativas '+str(col)].\
                                        add(df[col].value_counts(normalize=True,dropna=dropna),level=col)
    # Reordenación de columnas:
    pt=pt[pt.sort_index(axis=1,level=[0,1],ascending=[True,False]).columns]

    # Formato de columnas con diferencias relativas:
    if dropna==False:
        n=len(df[cond].unique())
    else:
        n=len(df[cond][df[cond].notna()].unique())
    d_style=dict()
    for i in range(n):
        d_style[pt.columns[-i-1]]='{:+,.2%}'
    pt=pt.style.format(d_style)

    return pt
