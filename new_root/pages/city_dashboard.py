import dash
from dash import html, dcc, callback, Input, Output, dash_table
import dash_leaflet as dl
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from data_service import DataService
from utils import ui_components as ui

dash.register_page(__name__, path='/dashboard')

# --- Layout ---
layout = html.Div([
    # Top Control Row
    html.Div([
        html.H4("Choisissez une ville:", style={'marginRight': '10px', 'display': 'inline-block'}),
        dcc.Dropdown(
            id='city-selector',
            # We load options dynamically from the DataService
            options=[{'label': v, 'value': v} for v in DataService.get_instance().valid_cities],
            value=DataService.get_instance().valid_cities[0] if DataService.get_instance().valid_cities else None,
            style={'width': '300px', 'display': 'inline-block', 'verticalAlign': 'middle'}
        )
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderBottom': '1px solid #ddd'}),

    # Tabs
    dcc.Tabs(id='city-tabs', value='tab-infos', children=[

        # TAB 1: Infos Générales (Map + Table)
        dcc.Tab(label="Infos Générales", value='tab-infos', children=[
            html.Div([
                # Left: Data Table
                html.Div([
                    ui.create_header("Informations Administratives"),
                    dash_table.DataTable(
                        id='table-infos',
                        style_cell={'fontFamily': 'Montserrat', 'textAlign': 'left'},
                        style_header={'fontWeight': 'bold', 'backgroundColor': '#e6e6e6'}
                    )
                ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),

                # Right: Map (Dash Leaflet)
                html.Div([
                    ui.create_header("Localisation"),
                    dl.Map(id='city-map', center=[46, 2], zoom=6, children=[
                        dl.TileLayer(),
                        dl.LayerGroup(id='city-marker-layer')
                    ], style={'width': '100%', 'height': '500px'})
                ], style={'width': '55%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
            ])
        ]),

        # TAB 2: Démographie (Graphs)
        dcc.Tab(label="Démographie", value='tab-demo', children=[
            ui.create_tab_section("Population Française", "graph-population", None),
            ui.create_tab_section("Naissances et Décès", "graph-naissances", None)
        ]),

        # Placeholders for other tabs (to be implemented similarly)
        dcc.Tab(label="Emploi", children=ui.create_header("Section Emploi (À implémenter)")),
        dcc.Tab(label="Immobilier", children=ui.create_header("Section Immobilier (À implémenter)")),
    ])
])

# --- Callbacks ---

# 1. Update General Info Table
@callback(
    [Output('table-infos', 'data'), Output('table-infos', 'columns')],
    Input('city-selector', 'value')
)
def update_info_table(city):
    if not city: return [], []

    df = DataService.get_instance().get_city_data('infos', city)
    if df is None or df.empty: return [], []

    # Transpose data for display (Vertical table)
    data_dict = df.iloc[0].to_dict()
    # Filter out technical columns if needed
    display_data = [{'Attribute': k, 'Value': v} for k, v in data_dict.items() if k not in ['Latitude', 'Longitude']]

    columns = [{'name': 'Attribut', 'id': 'Attribute'}, {'name': 'Valeur', 'id': 'Value'}]
    return display_data, columns

# 2. Update Map (Center & Marker)
@callback(
    [Output('city-map', 'center'), Output('city-map', 'zoom'), Output('city-marker-layer', 'children')],
    Input('city-selector', 'value')
)
def update_city_map(city):
    if not city: return [46, 2], 6, []

    df = DataService.get_instance().get_city_data('infos', city)
    if df is None or df.empty: return [46, 2], 6, []

    lat = float(df['Latitude'].iloc[0])
    lon = float(df['Longitude'].iloc[0])

    marker = dl.Marker(position=[lat, lon], children=[dl.Tooltip(city)])
    return [lat, lon], 12, [marker]

# 3. Update Population Graph
@callback(
    Output('graph-population', 'figure'),
    Input('city-selector', 'value')
)
def update_population_graph(city):
    if not city: return {}

    df = DataService.get_instance().get_city_data('demographie', city)
    if df is None or df.empty: return {}

    # Logic ported from main.py
    years = range(2006, 2016)
    x_axis = np.array(years)
    y_axis = [df[f"nbre habitants ({year})"].iloc[0] for year in years]

    return {
        'data': [go.Scatter(x=x_axis, y=y_axis, mode='lines+markers', line={'shape': 'spline'})],
        'layout': go.Layout(
            title=f"Evolution de la population à {city}",
            xaxis={'title': 'Années'},
            yaxis={'title': "Nombre d'habitants"}
        )
    }
