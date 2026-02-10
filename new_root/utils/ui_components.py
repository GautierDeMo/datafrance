from dash import html, dcc, dash_table

def create_header(title):
    """
    Standard blue header used across tabs.
    """
    return html.H3(
        title,
        style={
            'background': 'blue',
            'color': 'white',
            'textAlign': 'center',
            'padding': '10px 0px',
            'marginTop': '20px',
            'marginBottom': '20px'
        }
    )

def create_kpi_card(title, id_value, color='green'):
    """
    Returns a styled Div for single numbers (e.g., Total Accidents, Real Estate Prices).
    """
    return html.Div([
        html.H4(title),
        html.P(id=id_value, style={'fontSize': '20px', 'color': color, 'fontWeight': '600'})
    ], style={
        'display': 'inline-block',
        'width': '30%',
        'border': '1px solid black',
        'padding': '10px',
        'textAlign': 'center',
        'margin': '5px',
        'verticalAlign': 'top'
    })

def create_tab_section(title, graph_id=None, table_id=None):
    """
    Generates the standard 'Header + Graph + Table' layout.
    This pattern is used in almost every tab (Demography, Employment, etc.).
    """
    elements = []

    # 1. Add the Header
    if title:
        elements.append(create_header(title))

    content_children = []

    # 2. Add the Graph (Left side, ~60% width)
    if graph_id:
        content_children.append(html.Div([
            dcc.Graph(id=graph_id)
        ], style={
            'display': 'inline-block',
            'verticalAlign': 'top',
            'width': '60%',
            'padding': '10px',
            'boxShadow': '0 2px 2px #ccc',
            'border': '1px solid #eee'
        }))

    # 3. Add the Table (Right side, ~35% width)
    if table_id:
        content_children.append(html.Div([
            dash_table.DataTable(
                id=table_id,
                style_cell={
                    'fontFamily': 'Montserrat, sans-serif',
                    'textAlign': 'center'
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'intitule'},
                        'textAlign': 'left'
                    },
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': '#f8f8f8'
                    }
                ],
                style_header={
                    'backgroundColor': '#e6e6e6',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                }
            )
        ], style={'display': 'inline-block', 'verticalAlign': 'top', 'width': '35%', 'padding': '10px'}))

    elements.append(html.Div(content_children))

    return html.Div(elements, className="tab-section")
