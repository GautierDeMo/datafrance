import dash
from dash import html, dcc, callback, Input, Output
import dash_leaflet as dl
import pandas as pd
from data_service import DataService

dash.register_page(__name__, path='/national')

# --- Helper Functions for Colors ---
def get_chomage_color(rate):
    """Returns color based on unemployment rate (Logic from heatmap_chomage.py)"""
    if rate < 7.8: return "#FBD976"
    elif rate < 8.3: return "#FEB24C"
    elif rate < 8.8: return "#FC8C3C"
    elif rate < 9.2: return "#F84F38"
    elif rate < 9.6: return "#E43932"
    elif rate < 10.5: return "#BE2E28"
    else: return "#801F27"

def get_election_color(candidate):
    """Returns color based on candidate (Logic from heatmap_elections.py)"""
    colors = {
        "Nathalie LOISEAU": '#EFC29D',
        "Jordan BARDELLA": "#1C435C",
        "François-Xavier BELLAMY": "#9AD2F6",
        "Yannick JADOT": "#91BAFB",
        "Benoît HAMON": "#560836",
        "Manon AUBRY": "#EF9E9E",
        "Raphaël GLUCKSMANN": "#E97DBD",
        "Nicolas DUPONT-AIGNAN": "#69A0FA"
    }
    return colors.get(candidate, "#808080")

# --- Layout ---
layout = html.Div([
    html.H2("Cartes Nationales", style={'textAlign': 'center', 'color': 'blue', 'marginTop': '20px'}),

    # Controls
    html.Div([
        html.Label("Choisir la carte :", style={'fontWeight': 'bold', 'marginRight': '10px'}),
        dcc.RadioItems(
            id='map-type',
            options=[
                {'label': 'Chômage (Evolution)', 'value': 'chomage'},
                {'label': 'Elections Européennes 2019', 'value': 'elections'}
            ],
            value='chomage',
            inline=True,
            style={'display': 'inline-block'}
        )
    ], style={'textAlign': 'center', 'padding': '10px'}),

    # Slider (Only for Chomage)
    html.Div(id='slider-container', children=[
        dcc.Slider(
            id='year-slider',
            min=2004,
            max=2016,
            step=1,
            marks={str(y): str(y) for y in range(2004, 2017)},
            value=2004
        )
    ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}),

    # Map
    html.Div([
        dl.Map(center=[46.2276, 2.2137], zoom=6, children=[
            dl.TileLayer(url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"),
            dl.LayerGroup(id='heatmap-layer')
        ], style={'width': '100%', 'height': '70vh'})
    ], style={'width': '90%', 'margin': 'auto', 'border': '1px solid #ccc', 'marginBottom': '50px'})
])

# --- Callbacks ---
@callback(
    Output('slider-container', 'style'),
    Input('map-type', 'value')
)
def toggle_slider(map_type):
    if map_type == 'elections':
        return {'display': 'none'}
    return {'width': '80%', 'margin': 'auto', 'padding': '20px', 'display': 'block'}

@callback(
    Output('heatmap-layer', 'children'),
    [Input('map-type', 'value'), Input('year-slider', 'value')]
)
def update_map(map_type, year):
    ds = DataService.get_instance()
    if not ds.is_loaded:
        ds.load_data()

    markers = []

    if map_type == 'chomage':
        df = ds.get_national_stats(year)
        # Iterate and create markers
        for _, row in df.iterrows():
            try:
                lat, lon = row['Latitude'], row['Longitude']
                val = row[str(year)]
                color = get_chomage_color(val)

                markers.append(
                    dl.CircleMarker(center=[lat, lon], radius=3, color=color, fill=True, fillColor=color, fillOpacity=0.7, children=[
                        dl.Tooltip(f"{row['ville']}: {val}%")
                    ])
                )
            except:
                continue

    elif map_type == 'elections':
        # Logic to determine winner
        df_elections = ds._data_cache['elections'].copy()
        df_infos = ds._data_cache['infos']
        candidats = ds._data_cache['candidats']['candidat'].tolist()

        # Clean and find winner
        valid_candidats = [c for c in candidats if c in df_elections.columns]
        for c in valid_candidats:
            df_elections[c] = pd.to_numeric(df_elections[c], errors='coerce')

        df_elections['Gagnant'] = df_elections[valid_candidats].idxmax(axis=1)
        merged = pd.merge(df_elections, df_infos[['ville', 'Latitude', 'Longitude']], on='ville')

        for _, row in merged.iterrows():
            try:
                lat, lon = row['Latitude'], row['Longitude']
                winner = row['Gagnant']
                color = get_election_color(winner)
                markers.append(dl.CircleMarker(center=[lat, lon], radius=3, color=color, fill=True, fillColor=color, fillOpacity=0.7, children=[dl.Tooltip(f"{row['ville']}: {winner}")]))
            except:
                continue

    return markers
