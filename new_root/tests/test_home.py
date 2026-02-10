import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import dash
# Mock register_page to allow importing the page without a Dash app instance with pages enabled
dash.register_page = lambda *args, **kwargs: None

# 1. Create a minimal Dash app
app = dash.Dash(__name__)

# 2. Import the page AFTER the app is created
from pages import home

# 3. Inject the layout directly
app.layout = home.layout

if __name__ == '__main__':
    print("Starting Home Page test server...")
    print("Open http://127.0.0.1:8053 in your browser.")
    # Note: Links to /dashboard or /national won't work in this isolated test
    # because those pages aren't loaded in this specific test app.
    app.run(debug=True, port=8053)
