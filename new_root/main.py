import dash
from dash import html, dcc
import config
from data_service import DataService

# 1. Initialize Data Service at Startup
# This ensures data is loaded once when the server starts, not per user session.
print("Initializing Data Service...")
DataService.get_instance().load_data()
print("Data Service Ready.")

# 2. Initialize Dash App
# use_pages=True enables the multi-page architecture (Dash Pages)
app = dash.Dash(__name__, use_pages=True)
server = app.server  # Expose server for WSGI deployment

# 3. Define the App Shell (Layout common to all pages)
app.layout = html.Div([
    # Navigation Bar
    html.Div([
        html.Div("DataFrance", style={'float': 'left', 'color': 'white', 'fontSize': '20px', 'fontWeight': 'bold', 'marginRight': '40px'}),
        dcc.Link("Accueil", href="/", style={'marginRight': '20px', 'color': 'white', 'textDecoration': 'none', 'fontWeight': 'bold'}),
        dcc.Link("Dashboard Ville", href="/dashboard", style={'marginRight': '20px', 'color': 'white', 'textDecoration': 'none', 'fontWeight': 'bold'}),
        dcc.Link("Cartes Nationales", href="/national", style={'color': 'white', 'textDecoration': 'none', 'fontWeight': 'bold'}),
    ], style={'backgroundColor': '#000080', 'padding': '15px', 'overflow': 'hidden', 'marginBottom': '20px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.2)'}),

    # Page Container - This is where the specific page content is rendered
    html.Div([
        dash.page_container
    ], style={'padding': '0 20px'})

], style={'fontFamily': 'Montserrat, sans-serif', 'backgroundColor': '#f4f4f4', 'minHeight': '100vh'})

if __name__ == '__main__':
    print("Starting Main Application...")
    print(f"Open http://127.0.0.1:8050 in your browser.")
    app.run(debug=True, port=8050)
