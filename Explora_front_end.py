import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from matplotlib import pyplot as plt
import textwrap
pd.options.display.max_colwidth=800
sns.set_style('whitegrid')

#st.set_page_config(layout='wide')

# Dataset completo procesado
ruta='data/formacion_procesado.csv'
df=pd.read_csv(ruta,index_col=0,low_memory=False)

# Ajustes para cálculo de salario mediano:
# Extremo superior de los intervalos:
D_sld_upper={1:700,2:1000,3:1500,4:2000,5:2500,6:3000,7:4000}
df['sld_upper']=df['sueldo'].replace(D_sld_upper)
# Amplitud de los intervalos
D_sld_amplitud={1:700,2:300,3:500,4:500,5:500,6:500,7:1000}
df['sld_amplitud']=df['sueldo'].replace(D_sld_amplitud)

df_oc=df[df['ocupacion'].notna()]

# Histograma titulos_ocupaciones:
# Totales por título:
#@st.cache
def df_histograma(data,ref,criterio,umbral=0):
    if type(ref)!=list: ref=[ref]
    # Totales:
    aux_totales=data[ref+[criterio]].groupby(ref).agg(['count'])
    aux_totales.columns=aux_totales.columns.to_flat_index()
    aux_totales.rename(columns={aux_totales.columns[-1]:'total'},inplace=True)
    hist=data[ref+[criterio]].merge(aux_totales,left_on=ref,right_on=ref)
    # Frecuencias relativas:
    aux_fr=hist[ref+[criterio]].groupby(ref).agg(['value_counts'])
    aux_fr.columns=aux_fr.columns.to_flat_index()
    aux_fr.rename(columns={aux_fr.columns[-1]:'Fr'},inplace=True)
    hist=hist.merge(aux_fr,left_on=ref+[criterio],right_on=ref+[criterio])
    hist.drop_duplicates(inplace=True)
    hist['fr']=((hist['Fr'].div(hist['total']))*100).round(2)
    del hist['Fr']
    out=hist[hist['fr']>=umbral]
    out=out.copy().sort_values(by='fr',ascending=False)
    out.reset_index(drop=True,inplace=True)
    return out

hist_oc=df_histograma(data=df_oc,ref='titulo_ppal_',
                        criterio='ocupacion_',umbral=5)


@st.cache
def sueldo_mediano(data,ref):
    """ Calcula el sueldo mediano (procedimiento de calculo de mediana para
    datos agrupados en intervalos) para los encuestados agrupados por las
    columnas especificadas en el argumento 'ref'.
    El intervalo superior de la variable sueldo es no acotado. Se ha fijado
    su amplitud en el doble de la amplitud más frecuente. Así, la cota superior
    para el sueldo mensual más alto se establece en 4000 € mensuales.
    """
    if type(ref)!=list: ref=[ref]
    data=data[ref+['sld_upper','sld_amplitud']]
    # Frecuencias relativas:
    aux_fr=df_histograma(data=data,ref=ref,criterio='sld_upper')
    aux_fr['fr']=aux_fr['fr']/100
    merge_on=ref+['sld_upper']
    out=data.merge(aux_fr,left_on=merge_on,right_on=merge_on)
    out.drop_duplicates(inplace=True)
    # Orden según sueldo:
    out.sort_values(by='sld_upper',inplace=True)
    # Frecuencias acumuladas:
    out['fr cum']=out[ref+['fr']].groupby(ref).cumsum()
    # Frecuencia acumulada anterior:
    out['fr cum-1']=out['fr cum']-out['fr']
    # Intervalo mediano:
    out=out[out['fr cum']>=0.5]
    out.drop_duplicates(subset=ref,keep='first',inplace=True)
    # Sueldo mediano (=upper anterior+amplitud*(0.5-fr acum. anterior)/fr):
    out['sueldo']=out['sld_upper']-out['sld_amplitud']\
                         +out['sld_amplitud']*(0.5-out['fr cum-1'])/out['fr']
    out['sueldo mensual mediano']=out['sueldo'].round(2)
    for col in ['sld_upper','sld_amplitud','total','fr','fr cum',
                'fr cum-1','sueldo']:
        del out[col]
    out.reset_index(drop=True,inplace=True)
    out.sort_values(by=ref,inplace=True)
    return out

sueldo_tt_oc=sueldo_mediano(data=df_oc,ref=['titulo_ppal_','ocupacion_'])


st.title('¿En qué trabajan los que estudian eso?')
st.header('Ocupaciones laborales de los titulados universitarios')
st.header('')

titulos=df['titulo_ppal_'].sort_values().unique()
st.subheader('¿Qué estudios te interesan?')
tt=st.selectbox('Escoge un título', titulos)


st.header('')
st.subheader(str(tt)+': ocupaciones más frecuentes')

@st.cache
def prob_y_sueldo_mediano(tt):
    # Histograma ocupaciones para tt:
    hist_oc_titulo=hist_oc[hist_oc['titulo_ppal_']==tt]
    ocupaciones_titulo=hist_oc_titulo['ocupacion_'].unique()
    otras=100-hist_oc_titulo['fr'].sum()
    otras=round(otras,2)
    titulados=hist_oc_titulo['total'].unique()[0]
    del hist_oc_titulo['total'], hist_oc_titulo['titulo_ppal_']
    hist_oc_titulo.rename(columns={'ocupacion_':'Ocupación',
                                    'fr':'probabilidad (%)'},inplace=True)
    hist_oc_titulo.set_index('Ocupación',inplace=True)
    # Sueldo mediano para tt y cada ocupación:
    sueldo_titulo=sueldo_tt_oc[sueldo_tt_oc['titulo_ppal_']==tt]
    del sueldo_titulo['titulo_ppal_']
    sueldo_titulo.rename(columns={'ocupacion_':'Ocupación',
        'sueldo mensual mediano':'sueldo mensual mediano (€)'},inplace=True)
    sueldo_titulo.set_index('Ocupación',inplace=True)
    out=hist_oc_titulo.merge(sueldo_titulo,left_index=True,right_index=True)
    out.loc['Otras']=[otras,'']
    out.loc['']=''
    out.loc['Núm de titulados encuestados ocupados (base de cálculo): '\
                +str(titulados)]=''
    return out

tabla1=prob_y_sueldo_mediano(tt=tt)
st.table(tabla1)


st.header('')
title=': número de titulados encuestados (posición relativa en la muestra)'
st.subheader(str(tt)+title)

# Distribución del número de titulados:
tts=pd.DataFrame(df['titulo_ppal_'].value_counts())
tts.reset_index(inplace=True)
tts.rename(columns={'index':'título','titulo_ppal_':
                    'Núm. titulados'},inplace=True)
# boxplot:
fig, ax = plt.subplots(1,figsize=(11,2))
paleta=sns.color_palette('Paired')
c=paleta.as_hex()[7]
sns.boxplot(data=tts,x='Núm. titulados',palette='Paired')
label='Distribución del número de encuestados de cada título (173 títulos)'
ax.set_xlabel(label)
num_titulados_tt=tts[tts['título']==tt]['Núm. titulados'].unique()[0]
#ax.text(x=num_titulados_tt,y=0.2,s=str(num_titulados_tt),
#        ha='center',color=c,weight='bold')
sns.scatterplot(x=[num_titulados_tt]*2,y=[0]*2,color=c,s=250)
sns.scatterplot(x=[num_titulados_tt]*2,y=[0.2]*2,color='w',s=350)
ax.text(x=num_titulados_tt,y=0.2,s=str(num_titulados_tt),
        ha='center',va='center_baseline',color=c,weight='bold')
st.pyplot(fig)


st.header('')
st.subheader(str(tt)+': distribución de titulados por sexos')

# Distribución titulados por sexos:
@st.cache
def distribucion_sexos(tt):
    sexos=df_histograma(data=df,ref='titulo_ppal_',criterio='sexo_')
    sexos=sexos[sexos['titulo_ppal_']==tt]
    del sexos['titulo_ppal_'],sexos['total']
    return sexos

sexos_tt=distribucion_sexos(tt=tt)
# Histograma:
fig, ax = plt.subplots(1,1,figsize=(10,1))
sns.barplot(data=sexos_tt,x='fr',y='sexo_',palette='Paired')
ax.set_ylabel('')
ax.set_xlabel('frecuencia relativa (%)')
#title=textwrap.fill(tt+':',50)
#title=title+'\nDistribución de titulados por sexos'
#ax.set_title(title, fontsize=14)
sns.despine(right=True,left=True,top=True)
st.pyplot(fig)


st.header('')
st.subheader(str(tt)+': situación laboral según sexos')

# Situación laboral por sexos:
@st.cache
def sit_lab(tt):
    sit_lab=df_histograma(data=df,ref=['titulo_ppal_','sexo_'],
            criterio='sit_lab_')
    sit_lab=sit_lab[sit_lab['titulo_ppal_']==tt]
    del sit_lab['titulo_ppal_'],sit_lab['total']
    return sit_lab

sit_lab_tt=sit_lab(tt=tt)
# Histograma:
fig, ax = plt.subplots(1,1,figsize=(10,4))
sns.barplot(data=sit_lab_tt,x='sexo_',y='fr',hue='sit_lab_',palette='Paired')
ax.set_xlabel('')
ax.set_ylabel('frecuencia relativa (%)')
#title=textwrap.fill(tt+':',50)
#title=title+'\nSituación laboral'
#ax.set_title(title, fontsize=14)
ax.legend(bbox_to_anchor=(1.1,1),title='Situación laboral')
sns.despine(right=True,left=True,top=True)
st.pyplot(fig)


st.header('')
st.subheader(str(tt)+': ocupaciones por sexos')

# Distribución de ocupaciones por título para sexos:
@st.cache
def ocupaciones_por_sexos(tt):
    oc_sexo=df_histograma(df_oc,['titulo_ppal_','sexo_'],'ocupacion_')
    oc_sexo=oc_sexo[oc_sexo['titulo_ppal_']==tt]
    # Al menos una frecuencia (hombre o mujer) superior a 5%:
    for oc in oc_sexo['ocupacion_'].unique():
        frecuencias=oc_sexo[oc_sexo['ocupacion_']==oc]['fr'].unique()
        frecuencias_umbral=[fr for fr in frecuencias if fr>5]
        if len(frecuencias_umbral)==0:
            oc_sexo=oc_sexo[oc_sexo['ocupacion_']!=oc]
    del oc_sexo['total'], oc_sexo['titulo_ppal_']
    return oc_sexo

oc_sexo_tt=ocupaciones_por_sexos(tt=tt)
# Histograma:
altura=oc_sexo_tt.shape[0]/2.5
fig, ax = plt.subplots(1,figsize=(7,altura))
sns.barplot(data=oc_sexo_tt,x='fr',y='ocupacion_',hue='sexo_',palette='Paired')
ax.set_ylabel('')
ax.set_xlabel('frecuencia relativa (%)')
y_ticklabels=[textwrap.fill(tick.get_text(),40) for tick \
              in ax.get_yticklabels()]
ax.set_yticklabels(y_ticklabels)
#title=textwrap.fill(tt+':',50)
#title=title+'\nOcupaciones por sexos'
#ax.set_title(title, fontsize=14)
ax.legend(bbox_to_anchor=(-0.05,-0.2/altura),ncol=2)
sns.despine(right=True,left=True,top=True)
st.pyplot(fig)


st.header('')
st.subheader(str(tt)+': sueldos medianos por sexos')

# Comparación de sueldos medianos por sexo:
@st.cache
def compara_sueldos_medianos(data,ref,criterio):
    valores=data[criterio].unique()
    out=sueldo_mediano(data=data[data[criterio]==valores[0]],ref=ref)
    out.rename(columns={'sueldo mensual mediano':
                    'sueldo mensual mediano: '+str(valores[0])},inplace=True)
    for valor in valores[1:]:
        add=sueldo_mediano(data=data[data[criterio]==valor],ref=ref)
        add.rename(columns={'sueldo mensual mediano':
                            'sueldo mensual mediano: '+str(valor)},inplace=True)
        out=out.merge(add,left_on=ref,right_on=ref)
    if len(valores)==2:
        out['diferencia']=(out[out.columns[-2]]-out[out.columns[-1]]).round(2)
        out['diferencia relativa']=(out['diferencia']\
                /out['sueldo mensual mediano: '+str(valores[1])]*100).round(2)
        out.rename(columns={'diferencia relativa':
                    'diferencia relativa a favor de '+str(valores[0])+' (%)'},
                   inplace=True)
        del out['diferencia']
    return out
compara_sueldos=compara_sueldos_medianos(data=df_oc,
                ref=['titulo_ppal_','ocupacion_'],criterio='sexo_')
compara_sueldos_tt=compara_sueldos[compara_sueldos['titulo_ppal_']==tt]
# Solo ocupaciones con frecuencias superiores a 5 %:
aux=df_histograma(data=df_oc,ref=['titulo_ppal_'],criterio='ocupacion_')
aux=aux[aux['titulo_ppal_']==tt]
aux=aux[aux['fr']>=5]
compara=compara_sueldos_tt.merge(aux,left_on=['titulo_ppal_','ocupacion_'],
                                right_on=['titulo_ppal_','ocupacion_'])
compara.sort_values(by='fr',ascending=False,inplace=True)
for col in ['titulo_ppal_','total','fr']:
    del compara[col]
compara.rename(columns={'ocupacion_':'Ocupación'},inplace=True)
compara.set_index('Ocupación',drop=True,inplace=True)
D_formato=dict(zip(compara.columns,['{:.2f}']*len(compara.columns)))
st.table(compara.style.format('{:.2f}'))


st.header('')
st.header('')
st.header('')
fuente='**Fuente**: Encuesta de inserción laboral de titulados universitarios \
(2019 y 2014), INE'
st.markdown(fuente)
texto='Encuesta del Instituto Nacional de Estadística de España a titulados \
universitarios (títulos de grado y de máster) 5 años despues de su titulación.'
st.write(texto)
st.write('https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_\
C&cid=1254736176991&menu=resultados&idp=1254735573113#!tabs-1254736195727')
