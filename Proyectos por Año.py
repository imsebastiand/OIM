#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import callback
from dash import dcc
from dash import html

dash.register_page(__name__,  path='/',name='Proyectos por Año') # '/' is home page

df = pd.read_excel('OIMV22.xlsx')

#TEMPORAL IMPUTAR NAN PROYECTO CODIGOS YA QUE CON NAN NO SIRVEN LOS CALLBACKS DE LA APP Y TODO SE MALOGRA, 
#por ahora puse 'Sin Código' como valor pero me dices si lo cambio por otro, porque he visto el valor "-"
df['COD_proy']= df['COD_proy'].fillna("Sin Código")

df['CA_Mujer']= df[['CAMujernuevo1859','CAMujernuevo60']].sum(axis=1)
df['CA_Hombre']= df[['CAVaronnuevo1859','CAVaronnuevo60']].sum(axis=1)
df['CA_Otros']= df[['CAOtrosnuevo1859','CAOtrosnuevo60']].sum(axis=1)
df = df.rename(columns={"CAVaronnuevo017": "CA_Niño", "CAMujernuevo017": "CA_Niña", 'CAOtrosnuevo017':'CA_Otros<18'})

df['PER_Mujer']= df[['RyMMujernuevo1859','RyMMujernuevo60']].sum(axis=1)
df['PER_Hombre']= df[['RyMVaronnuevo1859','RyMVaronnuevo60']].sum(axis=1)
df['PER_Otros']= df[['RyMOtrosnuevo1859','RyMOtrosnuevo60']].sum(axis=1)
df =df.rename(columns={"RyMVaronnuevo017": "PER_Niño", "RyMMujernuevo017": "PER_Niña", 'RyMOtrosnuevo017':'PER_Otros<18'})

df['TRA_Mujer']= df[['TransitoMujernuevo1859','TransitoMujernuevo60']].sum(axis=1)
df['TRA_Hombre']= df[['TransitoVaronnuevo1859','TransitoVaronnuevo60']].sum(axis=1)
df['TRA_Otros']= df[['TransitoOtrosnuevo1859','TransitoOtrosnuevo60']].sum(axis=1)
df= df.rename(columns={"TransitoVaronnuevo017": "TRA_Niño", "TransitoMujernuevo017": "TRA_Niña", 'TransitoOtrosnuevo017':'TRA_Otros<18'})

#Acá se suman las columnas creadas previamente para tener los totales por Género/Edad
df['Mujer']= df[['CA_Mujer','PER_Mujer','TRA_Mujer']].sum(axis=1)
df['Hombre']= df[['CA_Hombre','PER_Hombre','TRA_Hombre']].sum(axis=1)
df['TOTAL_Otros']= df[['CA_Otros','PER_Otros','TRA_Otros']].sum(axis=1)
df['Niño']= df[['CA_Niño','PER_Niño','TRA_Niño']].sum(axis=1)
df['Niña']= df[['CA_Niña','PER_Niña','TRA_Niña']].sum(axis=1)
df['TOTAL_Otros<18']= df[['CA_Otros<18','PER_Otros<18','TRA_Otros<18']].sum(axis=1)

#Se suman las columnas creadas previamente según su tipo para tener los totales de Comunidad de Acogida, Permanencia y Tránsito
df['Comunidad de Acogida']= df[['CA_Mujer','CA_Hombre','CA_Otros', 'CA_Niño','CA_Niña', 'CA_Otros<18']].sum(axis=1)
df['Permanencia']= df[['PER_Mujer','PER_Hombre','PER_Otros','PER_Niño', 'PER_Niña','PER_Otros<18']].sum(axis=1)
df['Tránsito']= df[['TRA_Mujer','TRA_Hombre','TRA_Otros','TRA_Niño', 'TRA_Niña', 'TRA_Otros<18' ]].sum(axis=1)

df_categorias = pd.melt(df, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Comunidad de Acogida', 'Permanencia', 'Tránsito'], var_name='Categoría', value_name='Cantidad')

#Acá hago lo mismo que en la celda anterior pero con Género
df_genero = pd.melt(df, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Hombre', 'Mujer', 'Niño', 'Niña'], var_name='Género', value_name='Cantidad')

dfCAtemporal = df[['Año', 'COD_proy', 'Departamento','CA_Mujer', 'CA_Hombre','CA_Otros', 'CA_Niño', 'CA_Niña','CA_Otros<18']].copy()
dfCAtemporal.rename(columns = {'CA_Mujer': 'Mujer', 'CA_Hombre': 'Hombre','CA_Otros': 'Otros > 18', 'CA_Niño': 'Niño', 'CA_Niña':'Niña','CA_Otros<18':'Otros < 18'}, inplace = True)
df_CA = pd.melt(dfCAtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Comunidad de Acogida', value_name='Cantidad')

dfPERtemporal = df[['Año', 'COD_proy', 'Departamento','PER_Mujer', 'PER_Hombre','PER_Otros', 'PER_Niño', 'PER_Niña','PER_Otros<18']].copy()
dfPERtemporal.rename(columns = {'PER_Mujer': 'Mujer', 'PER_Hombre': 'Hombre','PER_Otros': 'Otros > 18', 'PER_Niño': 'Niño', 'PER_Niña':'Niña','PER_Otros<18':'Otros < 18'}, inplace = True)
df_PER = pd.melt(dfPERtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Permanencia', value_name='Cantidad')

dfTRAtemporal = df[['Año', 'COD_proy', 'Departamento','TRA_Mujer', 'TRA_Hombre','TRA_Otros', 'TRA_Niño', 'TRA_Niña','TRA_Otros<18']].copy()
dfTRAtemporal.rename(columns = {'TRA_Mujer': 'Mujer', 'TRA_Hombre': 'Hombre','TRA_Otros': 'Otros > 18', 'TRA_Niño': 'Niño', 'TRA_Niña':'Niña','TRA_Otros<18':'Otros < 18'}, inplace = True)
df_TRA = pd.melt(dfTRAtemporal, id_vars=['Año', 'COD_proy', 'Departamento'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Tránsito', value_name='Cantidad')

layout = html.Div([
    html.Div([
        html.Label('Personas Beneficidadas'),
            html.H2(id='TextoTotal'),
        
        html.Label('Selecciona el Año'),
            dcc.Checklist(
                id='AñoCheck',
                options=[{'label': code, 'value': code} for code in sorted(df['Año'].unique())],
                value=list(df['Año'].unique()),
            ), 

        html.Br(),
        html.Label('Selecciona el Código del Proyecto'),
            dcc.Dropdown(
                id='ProyectoCheck',
                options=[{'label': code, 'value': code} for code in sorted(df['COD_proy'].unique())],
                value=sorted(df['COD_proy'].unique())[0]
                ), 
        
    ], className='three columns', style={'backgroundColor': "#111111"}),
  
    ######
    html.Div([
       html.Div([
       dcc.Graph(id='PieCategoria')
        ], className='seven columns',),
       html.Div([
       dcc.Graph(id='PieGeneroYEdad')
        ], className='five columns',),  
    ], className='eight columns', style={'backgroundColor': "111111"}),

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
    ], className='twelve columns', style={'backgroundColor': "#111111"}),
    
], style={'backgroundColor': "#111111"})



@callback(
    Output('ProyectoCheck', 'options'),
    [Input('AñoCheck', 'value')]
)
def update_checklist_options(years):
    if not years:  # Acá se usa por default todos los valores de años si es que no han seleccionado ninguno
        available_years = df['Año'].unique()
    else:
        available_years = years
    options_proyecto = [{'label': code, 'value': code} for code in df[df['Año'].isin(available_years)]['COD_proy'].unique()]
    return options_proyecto


@callback(
    Output('PieCategoria', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
)
def update_pie(year, code):
    filtered_df = df_categorias[(df_categorias['Año'].isin(year)) & (df_categorias['COD_proy']==code)]
    fig = px.pie(filtered_df, values='Cantidad', names='Categoría', hole=.3 ,color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    fig.update_layout(template='plotly_dark')
    return fig

####
@callback(
    Output('PieGeneroYEdad', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
)
def update_pie(year, code):
    filtered_df = df_genero[(df_genero['Año'].isin(year)) & (df_genero['COD_proy']==code)]
    fig = px.pie(filtered_df, values='Cantidad', names='Género', hole=.2,color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    fig.update_layout(template='plotly_dark')
    return fig


#Histograma Comunidad de Acogida
@callback(
    Output('HistogramaCA', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
)
def update_histogram(year, code):
    filtered_df = df_CA[(df_CA['Año'].isin(year)) & (df_CA['COD_proy']==code)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Comunidad de Acogida', orientation='h', color_discrete_sequence=['#146c9c'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig

#Histograma de Permanencia
@callback(
    Output('HistogramaPER', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
)
def update_histogram(year, code):
    filtered_df = df_PER[(df_PER['Año'].isin(year)) & (df_PER['COD_proy']==code)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Permanencia', orientation='h', color_discrete_sequence=['#1d8fb6'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig

#Histograma de Tránsito
@callback(
    Output('HistogramaTRA', 'figure'),
    Input('AñoCheck', 'value'),
    Input('ProyectoCheck', 'value'),
)
def update_histogram(year, code):
    filtered_df = df_TRA[(df_TRA['Año'].isin(year)) & (df_TRA['COD_proy']==code)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Tránsito', orientation='h', color_discrete_sequence=['skyblue'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig


#Contador
@callback(Output('TextoTotal', 'children'),
              Input('AñoCheck', 'value'),
              Input('ProyectoCheck', 'value'),
)
def update_total(year, code):
        filtered_df = df[(df['Año'].isin(year)) & (df['COD_proy']== code)]
        sumatotal = filtered_df['Total_BEN'].sum()
        return f"{sumatotal}"

