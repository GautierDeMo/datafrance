import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1("DataFrance", style={'textAlign': 'center', 'color': 'blue', 'marginTop': '50px'}),
    html.P("Bienvenue sur le portail d'analyse des données françaises.", style={'textAlign': 'center', 'fontSize': '18px', 'color': '#555'}),

    html.Div([
        # Card 1: City Dashboard
        html.Div([
            html.H3("Tableau de Bord Ville", style={'color': '#333'}),
            html.P("Analysez les données détaillées d'une ville spécifique : Démographie, Emploi, Immobilier...", style={'minHeight': '60px'}),
            dcc.Link(
                html.Button("Accéder au Dashboard", style={
                    'marginTop': '20px', 'cursor': 'pointer', 'backgroundColor': 'blue', 'color': 'white',
                    'border': 'none', 'padding': '10px 20px', 'fontSize': '16px', 'borderRadius': '5px'
                }),
                href='/dashboard'
            )
        ], style={
            'width': '35%', 'display': 'inline-block', 'border': '1px solid #eee', 'padding': '30px',
            'margin': '20px', 'textAlign': 'center', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)',
            'verticalAlign': 'top', 'backgroundColor': 'white'
        }),

        # Card 2: National Maps
        html.Div([
            html.H3("Cartes Nationales", style={'color': '#333'}),
            html.P("Visualisez les tendances nationales sur des cartes interactives : Chômage, Elections...", style={'minHeight': '60px'}),
            dcc.Link(
                html.Button("Accéder aux Cartes", style={
                    'marginTop': '20px', 'cursor': 'pointer', 'backgroundColor': 'blue', 'color': 'white',
                    'border': 'none', 'padding': '10px 20px', 'fontSize': '16px', 'borderRadius': '5px'
                }),
                href='/national'
            )
        ], style={'width': '35%', 'display': 'inline-block', 'border': '1px solid #eee', 'padding': '30px', 'margin': '20px', 'textAlign': 'center', 'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)', 'verticalAlign': 'top', 'backgroundColor': 'white'})
    ], style={'textAlign': 'center', 'marginTop': '50px'})
])
