import dash
from dash import html, dcc

from PIL import Image
import requests
from io import BytesIO

from dash.dependencies import Input, Output, State
from dash import dcc
import pandas as pd
import plotly.express as px

url = "https://joseluisrosado.com/OIMPeru.jpeg"
response = requests.get(url)
image = Image.open(BytesIO(response.content))
new_width = 382
new_height = 139
resized_image = image.resize((new_width, new_height))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)

server = app.server
app.title = 'Matriz de Reporte'
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H2("Matriz de Reporte",
                    style={'color': 'white',
                           'padding': '12px 12px 6px 12px', 'margin': '0px'}),
            html.P("Enero 2021 - Diciembre 2022",
                   style={
                          'padding': '12px 12px 6px 12px', 'margin': '0px'}
                   ),
        ], className='eight columns', style={'backgroundColor': "#111111"},
        ),
        html.Div([
            html.Img(src=resized_image)
        ], className='four columns',
        ),
    ], className='twelve columns', style={'backgroundColor': '#111111'}),

    html.Div([
        dcc.Link(page['name'] + "  |  ", href=page['path'])
        for page in dash.page_registry.values()
    ], className='twelve columns', style={'backgroundColor': '#111111'}),

    html.Hr(),

    # content of each page
    dash.page_container

]
)

if __name__ == '__main__':
    app.run_server(debug=False)
