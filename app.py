#!/usr/bin/env python
# coding: utf-8

# In[2]:
import pandas as pd

# **Acá estoy usando el excel que me mandaste pero elimine varias columnas, solo me quede con las de tipo
# CAVaronnuevo017 que son 27, Año, Departamento, COD_proy y Total_BEN**

# In[3]:
df = pd.read_excel('oim_historicoSELECTED.xlsx')


# In[4]:
# In[5]:


#TEMPORAL IMPUTAR NAN PROYECTO CODIGOS YA QUE CON NAN NO SIRVEN LOS CALLBACKS DE LA APP Y TODO SE MALOGRA, 
#por ahora puse 'Sin Código' como valor pero me dices si lo cambio por otro, porque he visto el valor "-"
df['COD_proy']= df['COD_proy'].fillna("Sin Código")

# In[6]:


#El path de la imagen del logo de OIM
image_path = 'assets/oim.png'


# In[7]:


#TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
df['TESTTTTCA_Mujer']= df['CAMujernuevo1859'] + df['CAMujernuevo60']

# **Creando las columnas según el Género/Edad de cada tipo (Comunidad de Acogida: CA, Permanencia: PER y Tránsito: TRA)**

# In[8]:


#Acá se suman 1858 y 60 de Mujer, Hombre y Otros de Comunidad de Acogida para sacar una columna nueva
#de los adultos y se renombra las otras de 017 de Varon, Mujer y Otro<18, lo mismo se hace con las
#columnas de Permanencia y Tránsito abajo.
df['CA_Mujer']= df[['CAMujernuevo1859','CAMujernuevo60']].sum(axis=1)
df['CA_Hombre']= df[['CAVaronnuevo1859','CAVaronnuevo60']].sum(axis=1)
df['CA_Otros']= df[['CAOtrosnuevo1859','CAOtrosnuevo60']].sum(axis=1)
df = df.rename(columns={"CAVaronnuevo017": "CA_Niño", "CAMujernuevo017": "CA_Niña", 'CAOtrosnuevo017':'CA_Otros<18'})


# In[9]:
# In[10]:


df['PER_Mujer']= df[['RyMMujernuevo1859','RyMMujernuevo60']].sum(axis=1)
df['PER_Hombre']= df[['RyMVaronnuevo1859','RyMVaronnuevo60']].sum(axis=1)
df['PER_Otros']= df[['RyMOtrosnuevo1859','RyMOtrosnuevo60']].sum(axis=1)
df =df.rename(columns={"RyMVaronnuevo017": "PER_Niño", "RyMMujernuevo017": "PER_Niña", 'RyMOtrosnuevo017':'PER_Otros<18'})


# In[11]:


df['TRA_Mujer']= df[['TransitoMujernuevo1859','TransitoMujernuevo60']].sum(axis=1)
df['TRA_Hombre']= df[['TransitoVaronnuevo1859','TransitoVaronnuevo60']].sum(axis=1)
df['TRA_Otros']= df[['TransitoOtrosnuevo1859','TransitoOtrosnuevo60']].sum(axis=1)
df= df.rename(columns={"TransitoVaronnuevo017": "TRA_Niño", "TransitoMujernuevo017": "TRA_Niña", 'TransitoOtrosnuevo017':'TRA_Otros<18'})


# **Creando las columnas de totales primero según Género/Edad (Mujer, Hombre, Otros, Niño, Niña, Otros<18 y luego según el tipo
# Comunidad de Acogida, Permanencia y Tránsito**

# In[12]:


#Acá se suman las columnas creadas previamente para tener los totales por Género/Edad
df['Mujer']= df[['CA_Mujer','PER_Mujer','TRA_Mujer']].sum(axis=1)
df['Hombre']= df[['CA_Hombre','PER_Hombre','TRA_Hombre']].sum(axis=1)
df['TOTAL_Otros']= df[['CA_Otros','PER_Otros','TRA_Otros']].sum(axis=1)
df['Niño']= df[['CA_Niño','PER_Niño','TRA_Niño']].sum(axis=1)
df['Niña']= df[['CA_Niña','PER_Niña','TRA_Niña']].sum(axis=1)
df['TOTAL_Otros<18']= df[['CA_Otros<18','PER_Otros<18','TRA_Otros<18']].sum(axis=1)


# In[13]:


#Se suman las columnas creadas previamente según su tipo para tener los totales de Comunidad de Acogida, Permanencia y Tránsito
df['Comunidad de Acogida']= df[['CA_Mujer','CA_Hombre','CA_Otros', 'CA_Niño','CA_Niña', 'CA_Otros<18']].sum(axis=1)
df['Permanencia']= df[['PER_Mujer','PER_Hombre','PER_Otros','PER_Niño', 'PER_Niña','PER_Otros<18']].sum(axis=1)
df['Tránsito']= df[['TRA_Mujer','TRA_Hombre','TRA_Otros','TRA_Niño', 'TRA_Niña', 'TRA_Otros<18' ]].sum(axis=1)


# In[14]:


#Esto es solo para ver cuales son las columnas actuales

# **Creando los df para los gráficos de valores TOTALES que serán para los pies de Categoría y el otro de Género/Edad**

# In[15]:


#Acá usando pandas melt se crea un nuevo df para crear el gráfico de pie de totales según categoría
# quiero crear una columna donde los valores sean los tipos de Categoría
# en value_vars se eligen las columnas ['Comunidad de Acogida', 'Permanencia', 'Tránsito'] y les pongo el nombre Categoría
# y a la columna de valores le pongo de nombre Cantidad
# Acá una imagen de qué hace pd.melt: https://pandas.pydata.org/docs/_images/reshaping_melt.png 
# Acá más info sobre eso https://pandas.pydata.org/docs/reference/api/pandas.melt.html
df_categorias = pd.melt(df, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Comunidad de Acogida', 'Permanencia', 'Tránsito'], var_name='Categoría', value_name='Cantidad')

# In[16]:

#Acá hago lo mismo que en la celda anterior pero con Género
df_genero = pd.melt(df, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Hombre', 'Mujer', 'Niño', 'Niña'], var_name='Género', value_name='Cantidad')

# **Creando los df para los histogramas de valores de Género/Edad para cada tipo(Comunidad de Acogida, Permanencia, Tránsito)**

# In[17]:


#Esto va a ser para el primero de los 3 histogramas horizontales de abajo, este es sobre Gènero/Edad de tipo Comunidad de Acogida
#Acá creo un df temporal con los datos de las columnas de Comunidad de Acogida
dfCAtemporal = df[['Año', 'COD_proy', 'Departamento','CA_Mujer', 'CA_Hombre','CA_Otros', 'CA_Niño', 'CA_Niña','CA_Otros<18']].copy()

# In[18]:


#Acá renombro las columnas de este df temporal, hago esto para que los nombres de los gráficos sean "Mujer", "Hombre" etc
#En el df original no puedo renombrarlo así ya que también hay Hombre de Tránsito y Permanencia, y así con Mujer, etc
dfCAtemporal.rename(columns = {'CA_Mujer': 'Mujer', 'CA_Hombre': 'Hombre','CA_Otros': 'Otros > 18', 'CA_Niño': 'Niño', 'CA_Niña':'Niña','CA_Otros<18':'Otros < 18'}, inplace = True)


# In[19]:


#Acá es para ver como queda

# In[20]:


#Acá uso pd.melt para crear el df de Comunidad de Acogida según el Género/Edad,
#puse las columnas ['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'] en una columna llamada Comunidad de Acogida
#y para los valores numéricos de estos puse de nombre a la columna "Cantidad"
df_CA = pd.melt(dfCAtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Comunidad de Acogida', value_name='Cantidad')

# In[21]:


#Acá hice lo mismo que con los valores de Comunidad de Acogida pero con los de Permanencia
dfPERtemporal = df[['Año', 'COD_proy', 'Departamento','PER_Mujer', 'PER_Hombre','PER_Otros', 'PER_Niño', 'PER_Niña','PER_Otros<18']].copy()
dfPERtemporal.rename(columns = {'PER_Mujer': 'Mujer', 'PER_Hombre': 'Hombre','PER_Otros': 'Otros > 18', 'PER_Niño': 'Niño', 'PER_Niña':'Niña','PER_Otros<18':'Otros < 18'}, inplace = True)
df_PER = pd.melt(dfPERtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Permanencia', value_name='Cantidad')

# In[22]:
#Acá  vos harás lo mismo para los valores de Tránsito, crearas los df: dfTRAtemporal y df_TRA


# In[28]:
dfTRAtemporal = df[['Año', 'COD_proy', 'Departamento','TRA_Mujer', 'TRA_Hombre','TRA_Otros', 'TRA_Niño', 'TRA_Niña','TRA_Otros<18']].copy()
dfTRAtemporal.rename(columns = {'TRA_Mujer': 'Mujer', 'TRA_Hombre': 'Hombre','TRA_Otros': 'Otros > 18', 'TRA_Niño': 'Niño', 'TRA_Niña':'Niña','TRA_Otros<18':'Otros < 18'}, inplace = True)
df_TRA = pd.melt(dfTRAtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Tránsito', value_name='Cantidad')

# In[ ]:
# **Acá empieza la creación de la app**

# In[24]:


#Se importan los paquetes a usar
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash import dcc
from dash import html


# In[ ]:


#external_stylesheets es como un molde de css con una estructura predefinida
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Acá creas la dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
server = app.server

app.title = 'Reporting Plan Dashboard OIM'

#Acá se crea el layout de la app, tiene una estrutura parecida a html, className='eight columns' es para que ocupe 8 columnas,
#la external_stylesheet usada tiene un molde sobre 12 columnas totales por eso suman 12
app.layout = html.Div([
    html.Div([
        html.Div([
                    html.H2("REPORTING PLAN - DASHBOARD",
                            style={'color': '#146c9c',
                            'padding': '12px 12px 6px 12px', 'margin': '0px'}),
                    html.P("Enero 2021 - Diciembre 2022",
                           style={'color': '#146c9c',
                                  'padding': '12px 12px 6px 12px', 'margin': '0px'}
                           ),
        ], className='eight columns',
        ),
        html.Div([
            #Acá es donde pongo la iamgen del logo
            html.Img(src=image_path)
        ], className='four columns',
        ),
    ], className='twelve columns', style={'margin': '10px auto', 'border': 'solid', 'border-color': '#146c9c'}),

#Acá estoy creando los checkbox para seleccionar Año, el código y el Departamento
    html.Div([
        html.Div([
            #Acá creo un label o texto que dice eso:
            html.Label('Selecciona el Año'),
            #Acá creo la lista de checkbox para Año, como ves le doy una id, esta es para ligarla con los callbacks del final
            #los callbacks es como se conectan los "menus" con los gráficos de dash. 
            #en options estoy iterando sobre cada valor único de Año (2021, 2022, 2023), en value que es que valores
            #se seleccionan por default esta list(df['Año'].unique()) para que se seleccionen todos por default
            dcc.Checklist(
                id='AñoCheck',
                options=[{'label': code, 'value': code} for code in sorted(df['Año'].unique())],
                value=list(df['Año'].unique()),
                style ={'height': '150px','overflowY': 'scroll'}
            ),
        ], className='three columns',),
        html.Div([
            #Acá se hace lo mismo para proyecto
            html.Label('Selecciona el Código del Proyecto'),
            dcc.Checklist(
                id='ProyectoCheck',
                options=[{'label': code, 'value': code} for code in sorted(df['COD_proy'].unique())],
                value=list(df['COD_proy'].unique()),
                style ={'height': '150px','overflowY': 'scroll'}
            ),
        ], className='three columns', ),
        html.Div([
            #Acá se hace lo mismo para Departamento
            html.Label('Selecciona el Departamento'),
            dcc.Checklist(
                id='DepartamentoCheck',
                options=[{'label': depa, 'value': depa} for depa in sorted(df['Departamento'].unique())],
                value=list(sorted(df['Departamento'].unique())),
                style ={'height': '150px','overflowY': 'scroll'}
            ),
        ], className='three columns', ),
        html.Div([
            html.Label('Personas Beneficidadas'),
            html.H2(id='TextoTotal')
        ], className='three columns', ),

    ], className='twelve columns', style={'margin': '10px auto'}),

#Acá estoy creando una division de html donde saldrán los outputs de los callbacks de abajo que son los dos Gráficos de Pie
#como ves también tienen cada uno una id
    html.Div([
       html.Div([
       dcc.Graph(id='PieCategoria')
        ], className='six columns',),
       html.Div([
       dcc.Graph(id='PieGeneroYEdad')
        ], className='six columns',),  
    ], className='twelve columns',),

#Acá finalmente estoy creando otra división para poner los 3 histogramas de Comunidad de Acogida, Permanencia y Tránsito
    html.Div([
       html.Div([
       dcc.Graph(id='HistogramaCA')
        ], className='four columns',),
       html.Div([
       dcc.Graph(id='HistogramaPER')
        ], className='four columns',),
       html.Div([
        dcc.Graph(id='HistogramaTRA')
        ], className='four columns',),
    ], className='twelve columns',),
],)



#Acá empieza la parte de los Callbacks y los gráficos

#Ligar Proyecto y Departamento a Año, esto hará que si se selecciona sólo el año 2021 por ejm sólo se podrá seleccionar 
#y aparecerán como opciones los valores de Código de Proyecto y de Departamento de ese año , estos son los outputs "options"
#Acá se toma como input los valores del checkbox de años

@app.callback(
    Output('ProyectoCheck', 'options'),
    Output('DepartamentoCheck', 'options'),
    [Input('AñoCheck', 'value')]
)
def update_checklist_options(years):
    if not years:  # Acá se usa por default todos los valores de años si es que no han seleccionado ninguno
        available_years = df['Año'].unique()
    else:
        available_years = years
        
    #Acá es donde se dice que sólo salga como output COD_proy y Departamento si es que "isin" available_years, osea
    #los valores de años seleccionados
    options_proyecto = [{'label': code, 'value': code} for code in df[df['Año'].isin(available_years)]['COD_proy'].unique()]
    options_departamento = [{'label': code, 'value': code} for code in df[df['Año'].isin(available_years)]['Departamento'].unique()]

    return options_proyecto, options_departamento


#Acá empiezan los Pie de totales

#Pie Total Personas Beneficiadas por Categoría

#se usa el df_categorias que creamos al comienzo para crear este gráfico y en base a esto se crea el filtered_df,
#este df es filtrado en base a los 3 inputs del callback referidos a id:AñoCheck, id:ProyectoCheck e 
#id:DepartamentoCheck que son los checkboxes que creamos en la app para seleccionar opciones,
#si eliges sólo el año 2020 y solo seleccionas el proyecto ABC de ese año y sólo el departamento de Lima 
# sólo tomara los datos de estos para la creación del df_filtered que se usa para la creación
#del gráfico de valores totales según categoría (Comunidad de Acogida, Permanencia y Tránsito)
#Como puedes ver el output se llama PieCategoria, esta id PieCategoria esta dentro de la app como dcc.Graph(id='PieCategoria')
#ahí es donde se mostrará el gráfico
@app.callback(
    Output('PieCategoria', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
    Input('DepartamentoCheck', 'value')
)

#como ves acá tienes una función con 3 valores year, codes y depas, estos valores son los 3 de los inputs, estos tienen 
#que tener el mismo orden al ponerlos, el id:AñoCheck esta ligado a year, ProyectoCheck a codes y DepartamentoCheck a depas
def update_pie(year, codes, depas):
    #Acá es donde se crea el filtered_df en base a los valores seleccionados como inputs
    #el isin es para que seleccione si está en tal año o tales años seleccionados y los & son condicionales de unión 
    #osea que cumpla cada condición para crear el filtered_df. Finalmente sobre esto es importante decir que todos los df
    #creados acá o en otras funciones (def) solo viven dentro de la función, fuera de esta filtered_df no existe, esto también 
    #explica porque en otras funciones de abajo existen otras filtered_df diferentes
    filtered_df = df_categorias[(df_categorias['Año'].isin(year)) & (df_categorias['COD_proy'].isin(codes)) & (df_categorias['Departamento'].isin(depas))]
    #Acá es donde se crea el gráfico Pie, tiene como values Cantidad que es la columna de valores numéricos
    #y como names Categoría que son Comunidad de Acogida, Permanencia y Tránsito, lo demás es diseño y colores
    fig = px.pie(filtered_df, values='Cantidad', names='Categoría', hole=.3 ,color_discrete_sequence=px.colors.sequential.Teal)
    #Acá es para que en el gráfico del pie salgan los porcentajes, nombres y valores
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    return fig

#Pie de por Género y Edad
#En este callback y función se hizo lo mismo que arriba pero para el gráfico de totales de Género y Edad y se uso como base el 
#df creado por nosotros llamado df_genero
@app.callback(
    Output('PieGeneroYEdad', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
    Input('DepartamentoCheck', 'value')
)
def update_pie(year, codes, depas):
    filtered_df = df_genero[(df_genero['Año'].isin(year)) & (df_genero['COD_proy'].isin(codes)) & (df_genero['Departamento'].isin(depas))]
    fig = px.pie(filtered_df, values='Cantidad', names='Género', hole=.2,color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    return fig


# Acá empiezan los callbacks y funciones para los 3 histogramas de valores de Género/Edad seleccionados según cada tipo: 
#Comunidad de Acogida, Permanencia y Tránsito. Básicamente es los mismo que los pies de arriba solo que los gráficos son
#histogramas px.histogram y toman x y y en lugar de values y names, orientation=h es para que sean horizontales
#cada histograma se hace en base a un df diferente creado por mí. df_CA. df_PER y el que crearás para el tercer histograma
#llamado df_TRA

#Histograma Comunidad de Acogida
@app.callback(
    Output('HistogramaCA', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
    Input('DepartamentoCheck', 'value')
)
def update_histogram(year, codes, depas):
    filtered_df = df_CA[(df_CA['Año'].isin(year)) & (df_CA['COD_proy'].isin(codes)) & (df_CA['Departamento'].isin(depas))]
    fig = px.histogram(filtered_df, x='Cantidad', y='Comunidad de Acogida', orientation='h', color_discrete_sequence=['#146c9c'], text_auto=True)
    return fig

#Histograma de Permanencia
@app.callback(
    Output('HistogramaPER', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
    Input('DepartamentoCheck', 'value')
)
def update_histogram(year, codes, depas):
    filtered_df = df_PER[(df_PER['Año'].isin(year)) & (df_PER['COD_proy'].isin(codes)) & (df_PER['Departamento'].isin(depas))]
    fig = px.histogram(filtered_df, x='Cantidad', y='Permanencia', orientation='h', color_discrete_sequence=['#1d8fb6'], text_auto=True)
    return fig

#Histograma de Tránsito
@app.callback(
    Output('HistogramaTRA', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
    Input('DepartamentoCheck', 'value')
)
def update_histogram(year, codes, depas):
    filtered_df = df_TRA[(df_TRA['Año'].isin(year)) & (df_TRA['COD_proy'].isin(codes)) & (df_TRA['Departamento'].isin(depas))]
    fig = px.histogram(filtered_df, x='Cantidad', y='Tránsito', orientation='h', color_discrete_sequence=['skyblue'], text_auto=True)
    return fig



#Contador de total
@app.callback(Output('TextoTotal', 'children'),
              Input('AñoCheck', 'value'),
              Input('ProyectoCheck', 'value'),
              Input('DepartamentoCheck', 'value'))


def update_total(year, codes, depas):
        filtered_df = df[(df['Año'].isin(year)) & (df['COD_proy'].isin(codes)) & (df['Departamento'].isin(depas))]
        sumatotal = filtered_df['Total_BEN'].sum()
        return f"{sumatotal}"


#Acá es donde se carga la app, en debug=False se carga normal, en debug=True te sale una interfaz y botones que te indican
#errores posibles en tu aplicación, también te indican como es que los callbacks están ligados, esto se recomienda usarlo 
#cuando estás haciendo la app. cuando lo subes tiene que estar en debug=False
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




