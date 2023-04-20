#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import plotly.express as px
import dash
from dash.dependencies import Input, Output, State
from dash import callback
from dash import dcc
from dash import html

dash.register_page(__name__, name='Indicadores') # '/' is home page

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

#COLUMNA DE INDICADOR DE PROYECTOS
dfIND = df.copy()
dfIND = dfIND.dropna(subset=['Ind_py'])
dfIND = dfIND[dfIND['Ind_py']!= "0"]
dfIND = dfIND[dfIND['Ind_py']!= "-"]

dfIND.rename(columns = {'Ind_py': 'Indicador'}, inplace = True)
###
df_categoriasIND = pd.melt(dfIND, id_vars=['Año', 'COD_proy', 'Departamento', 'Indicador'], value_vars=['Comunidad de Acogida', 'Permanencia', 'Tránsito'], var_name='Categoría', value_name='Cantidad')
df_generoIND = pd.melt(dfIND, id_vars=['Año', 'COD_proy', 'Departamento','Indicador'], value_vars=['Hombre', 'Mujer', 'Niño', 'Niña'], var_name='Género', value_name='Cantidad')



dfCAtemporalIND = dfIND[['Año', 'COD_proy','Indicador','Departamento','CA_Mujer', 'CA_Hombre','CA_Otros', 'CA_Niño', 'CA_Niña','CA_Otros<18']].copy()
dfCAtemporalIND.rename(columns = {'CA_Mujer': 'Mujer', 'CA_Hombre': 'Hombre','CA_Otros': 'Otros > 18', 'CA_Niño': 'Niño', 'CA_Niña':'Niña','CA_Otros<18':'Otros < 18'}, inplace = True)
df_CA_IND = pd.melt(dfCAtemporalIND, id_vars=['Año', 'COD_proy', 'Departamento','Indicador'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Comunidad de Acogida', value_name='Cantidad')

dfPERtemporalIND = dfIND[['Año', 'COD_proy', 'Indicador','Departamento','PER_Mujer', 'PER_Hombre','PER_Otros', 'PER_Niño', 'PER_Niña','PER_Otros<18']].copy()
dfPERtemporalIND.rename(columns = {'PER_Mujer': 'Mujer', 'PER_Hombre': 'Hombre','PER_Otros': 'Otros > 18', 'PER_Niño': 'Niño', 'PER_Niña':'Niña','PER_Otros<18':'Otros < 18'}, inplace = True)
df_PER_IND = pd.melt(dfPERtemporalIND, id_vars=['Año', 'COD_proy', 'Departamento','Indicador'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Permanencia', value_name='Cantidad')

dfTRAtemporalIND = dfIND[['Año', 'COD_proy', 'Indicador', 'Departamento','TRA_Mujer', 'TRA_Hombre','TRA_Otros', 'TRA_Niño', 'TRA_Niña','TRA_Otros<18']].copy()
dfTRAtemporalIND.rename(columns = {'TRA_Mujer': 'Mujer', 'TRA_Hombre': 'Hombre','TRA_Otros': 'Otros > 18', 'TRA_Niño': 'Niño', 'TRA_Niña':'Niña','TRA_Otros<18':'Otros < 18'}, inplace = True)
df_TRA_IND = pd.melt(dfTRAtemporalIND, id_vars=['Año', 'COD_proy', 'Departamento','Indicador'], value_vars=['Otros > 18', 'Otros < 18', 'Niño','Niña','Mujer', 'Hombre'], var_name='Tránsito', value_name='Cantidad')

layout = html.Div([
    html.Div([
        html.Label('Cantidad'),
            html.H2(id='IndicadorTotal'),
                html.Br(),
        html.Label('Selecciona el Código del Proyecto'),
            dcc.Dropdown(
                id='ProyectoDropdown',
                options=[{'label': code, 'value': code} for code in sorted(dfIND['COD_proy'].unique())],
                value=sorted(dfIND['COD_proy'].unique())[0]
                ), 
        html.Br(),
        html.Label('Selecciona el Indicador del Proyecto'),
            dcc.Dropdown(
                id='IndicadorDropddown',
                options=[{'label': code, 'value': code} for code in sorted(dfIND['Indicador'].unique())],
                value=sorted(dfIND['Indicador'].unique())[0],
                clearable=False,
                ), 
        
    ], className='twelve columns', style={'backgroundColor': "#111111"}),
  
    ######
    html.Div([
       html.Div([
       dcc.Graph(id='PieCategoria_IND')
        ], className='seven columns',),
       html.Div([
       dcc.Graph(id='PieGeneroYEdad_IND')
        ], className='five columns',),  
    ], className='twelve columns', style={'backgroundColor': "111111"}),

#Acá finalmente estoy creando otra división para poner los 3 histogramas de Comunidad de Acogida, Permanencia y Tránsito
    html.Div([
       html.Div([
       dcc.Graph(id='HistogramaCA_IND')
        ], className='four columns',),
       html.Div([
       dcc.Graph(id='HistogramaPER_IND')
        ], className='four columns',),
       html.Div([
        dcc.Graph(id='HistogramaTRA_IND')
        ], className='four columns',),
    ], className='twelve columns', style={'backgroundColor': "#111111"}),
    
], style={'backgroundColor': "#111111"})

@callback(
    Output('IndicadorDropddown', 'options'),
    [Input('ProyectoDropdown', 'value')]
)
def update_checklist_options(project):
    if not project:  # Acá se usa por default todos los valores de años si es que no han seleccionado ninguno
        available_project = dfIND['COD_proy'].unique()
    else:
        available_project = project
    options_proyecto = [{'label': code, 'value': code} for code in dfIND[dfIND['COD_proy']==project]['Indicador'].unique()]
    return options_proyecto


@callback(
    Output('PieCategoria_IND', 'figure'),
    Input('ProyectoDropdown', 'value'),
    Input('IndicadorDropddown', 'value'),
)
def update_pie(code, indi):
    filtered_df = df_categoriasIND[(df_categoriasIND['COD_proy']==code) & (df_categoriasIND['Indicador']==indi)]
    fig = px.pie(filtered_df, values='Cantidad', names='Categoría', hole=.3 ,color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    fig.update_layout(template='plotly_dark')
    return fig

####
@callback(
    Output('PieGeneroYEdad_IND', 'figure'),
    Input('ProyectoDropdown', 'value'),
    Input('IndicadorDropddown', 'value'),
)
def update_pie(code, indi):
    filtered_df = df_generoIND[(df_generoIND['COD_proy']==code) & (df_generoIND['Indicador']==indi)]
    fig = px.pie(filtered_df, values='Cantidad', names='Género', hole=.2,color_discrete_sequence=px.colors.sequential.Teal)
    fig.update_traces(textinfo='percent+label+value', textposition='inside', insidetextfont=dict(color='black'),
                      hoverinfo='percent+label+value')
    fig.update_layout(template='plotly_dark')
    return fig


#Histograma Comunidad de Acogida
@callback(
    Output('HistogramaCA_IND', 'figure'),
    Input('ProyectoDropdown', 'value'),
    Input('IndicadorDropddown', 'value'),
)
def update_histogram(code, indi):
    filtered_df = df_CA_IND[(df_CA_IND['COD_proy']==code) & (df_CA_IND['Indicador']==indi)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Comunidad de Acogida', orientation='h', color_discrete_sequence=['#146c9c'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig

#Histograma de Permanencia
@callback(
    Output('HistogramaPER_IND', 'figure'),
    Input('ProyectoDropdown', 'value'),
    Input('IndicadorDropddown', 'value'),
)
def update_histogram(code, indi):
    filtered_df = df_PER_IND[(df_PER_IND['COD_proy']==code) & (df_PER_IND['Indicador']==indi)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Permanencia', orientation='h', color_discrete_sequence=['#1d8fb6'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig

#Histograma de Tránsito
@callback(
     Output('HistogramaTRA_IND', 'figure'),
     Input('ProyectoDropdown', 'value'),
     Input('IndicadorDropddown', 'value'),
 )
def update_histogram(code, indi):
    filtered_df = df_TRA_IND[(df_TRA_IND['COD_proy']==code) & (df_TRA_IND['Indicador']==indi)]
    fig = px.histogram(filtered_df, x='Cantidad', y='Tránsito', orientation='h', color_discrete_sequence=['skyblue'], text_auto=True)
    fig.update_layout(template='plotly_dark')
    return fig

#Contador
@callback(Output('IndicadorTotal', 'children'),
              Input('ProyectoDropdown', 'value'),
              Input('IndicadorDropddown', 'value'),
)
def update_total(code, indi):
        filtered_df = dfIND[(dfIND['COD_proy']== code) & (dfIND['Indicador'] == indi)]
        sumatotal = filtered_df['Cantidad_py'].sum()
        return f"{sumatotal}"