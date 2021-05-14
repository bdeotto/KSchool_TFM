# ¿EN QUÉ TRABAJAN LOS QUE ESTUDIAN ESO?

Este es un TFM del máster en Data Science de KShool (Madrid, 2021, Edición 23). 

La fuente de información son las encuestas de inserción laboral de titulados universitarios elaboradas por el INE (2019 y 2014): 

https://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736176991&menu=resultados&idp=1254735573113#!tabs-1254736195727

El objetivo de estudio es la construcción de un modelo de clasificación que permita precedir las ocupaciones profesionales de los titulados universitarios en España a partir de su formación universitaria y otra información académica proporcionada por las encuestas. 

Descripción de los archivos: 

- **A1_preprocesa_eda_grado_2019.ipynb** preprocesa la encuesta de titulados de grado de 2019 y realiza un análisis exploratorio preliminar. 

- **A2_preprocesa_master_2019.ipynb** preprocesa la encuesta de titulados de máster de 2019.

- **A3_preprocesa_grado_2014.ipynb** preprocesa la encuesta de titulados de grado 2014.

Los archivos anteriores se alimentan de los ficheros csv de las encuestas asociadas y de sus correspondientes ficheros de diseño. Estos últimos se transforman en diccionarios que se emplean y actualizan en cada uno de los notebooks. 

Por este motivo, **los tres notebooks anteriores deben ejecutarse en el orden en el que se han presentado**. 

- **B_concatena_transforma.ipynb** reune los tres datasets procesados por los notebooks anteriores y realiza transformaciones sobre las variables. Produce un archivo csv, formacion_procesado.csv, que es la fuente de información del resto de notebooks. 

- **Clasifica_naive.ipynb** construye un modelo de clasificación naive muy sencillo que permite explorar las relaciones entre los títulos universitarios y las ocupaciones de los titulados. Su fuente de información es el dataset reunido y procesado, formacion_procesado.csv. 

- **Clasifica_regresion_logistica.ipynb** propone un modelo de clasificador basado en una regresión logística multivariante. Su fuente de información es el dataset reunido y procesado, formacion_procesado.csv.

- **Describe.ipynb** realiza un análisis descriptivo elemental de los resultados del dataset formado por las tres encuestas y produce las representaciones gráficas que ilustran la memoria del proyecto. Su fuente de información es el dataset reunido y procesado, formacion_procesado.csv.

- **Explora_front_end.py** es un script interactivo realizado con streamlit que permite al usuario consultar información sobre encuestados, ocupaciones, salarios, etc. para cada uno de los títulos universitarios contemplados en la encuesta. Su fuente de información es el dataset reunido y procesado, formacion_procesado.csv.

- **Memoria_bdeotto.zip** contiene la memoria del proyecto en formato html y los elementos necesarios para su funcionamiento correcto. 

El resto de archivos (con extensión py) son módulos necesarios para la creación y actualización del los diccionarios empleados en los cuatro primeros notebooks (etapas de preprocesado y reunión y transformación del dataset) y módulos con funciones definidas para el análisis exploratorio de la encuesta. 


Las rutas en los ficheros están referidas a un directorio 'data' que contiene los archivos facilitados por el INE y los archivos csv creados a lo largo del proceso de transformación y análisis de los datos. Esta carpeta puede descargarse en la localización: 
