import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dash
# Mock register_page to allow importing the page without a Dash app instance with pages enabled
dash.register_page = lambda *args, **kwargs: None
from data_service import DataService

# 1. Initialize Data manually
print("Loading data...")
DataService.get_instance().load_data()
print("Data loaded.")

# 2. Create a minimal Dash app
app = dash.Dash(__name__)

# 3. Import the page AFTER the app is created
from pages import city_dashboard

# 4. Inject the layout directly
app.layout = city_dashboard.layout

if __name__ == '__main__':
    print("Starting Dashboard test server...")
    print("Open http://127.0.0.1:8052 in your browser.")
    app.run(debug=True, port=8052)
