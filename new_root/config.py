import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# File System Paths
# We default to "../dataset" assuming the app is run from the 'new_root' directory
# and the data is in the sibling 'dataset' directory.
DATA_PATH = os.getenv("DATA_PATH", "../dataset")

# Temporal Scope
# Used for loops like range(START_YEAR, END_YEAR) -> 2004 to 2016 inclusive
START_YEAR = int(os.getenv("START_YEAR", 2004))
END_YEAR = int(os.getenv("END_YEAR", 2017))

# Dataframe Column Names
# Centralizing these avoids "magic strings" scattered in the code
COL_VILLE = "ville"
COL_LAT = "Latitude"
COL_LON = "Longitude"

# Validation (Optional: just to verify it loads when run directly)
if __name__ == "__main__":
    print(f"Configuration Loaded:")
    print(f"DATA_PATH: {os.path.abspath(DATA_PATH)}")
    print(f"Time Range: {START_YEAR} - {END_YEAR}")
