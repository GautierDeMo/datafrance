import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dash
from pages import national_maps
from data_service import DataService

# 1. Initialize Data manually (since main.py usually does this)
print("Loading data...")
DataService.get_instance().load_data()
print("Data loaded.")

# 2. Create a minimal Dash app
app = dash.Dash(__name__)

# 3. Inject the layout directly
app.layout = national_maps.layout

if __name__ == '__main__':
    print("Starting test server...")
    app.run_server(debug=True, port=8051)
