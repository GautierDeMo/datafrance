import pandas as pd
import os
import config

class DataService:
    _instance = None

    @staticmethod
    def get_instance():
        if DataService._instance is None:
            DataService._instance = DataService()
        return DataService._instance

    def __init__(self):
        self._data_cache = {}
        self.valid_cities = [] # List for dropdown options (sorted)
        self.is_loaded = False

    def load_data(self):
        """Loads all CSV files, cleans them, and aligns the city lists."""
        if self.is_loaded:
            return

        # Helper to load csv with specific options
        def load(filename, **kwargs):
            return pd.read_csv(os.path.join(config.DATA_PATH, filename), **kwargs)

        # 1. Load all datasets
        # We use dtype=str for columns that might contain codes (like zip codes) or mixed types
        self._data_cache['infos'] = load("infos.csv", dtype=str)
        self._data_cache['chomage'] = load("chomage.csv")
        self._data_cache['auto'] = load("auto.csv")
        self._data_cache['csp'] = load("csp.csv")
        self._data_cache['delinquance'] = load("delinquance.csv")
        self._data_cache['demographie'] = load("demographie.csv", dtype=str)
        self._data_cache['elections'] = load("elections.csv", dtype=str)
        self._data_cache['emploi'] = load("emploi.csv")
        self._data_cache['entreprises'] = load("entreprises.csv")
        self._data_cache['immobilier'] = load("immobilier.csv")
        self._data_cache['salaires'] = load("salaires.csv")
        self._data_cache['sante'] = load("santeSocial.csv", dtype=str)
        self._data_cache['candidats'] = load("candidats_2019.csv")

        # 2. CLEANING
        self._clean_coordinates()

        # 3. ALIGNMENT
        self._calculate_valid_cities()

        self.is_loaded = True

    def _clean_coordinates(self):
        """Removes rows with 'nc' in Latitude or Longitude in the infos dataset."""
        df = self._data_cache['infos']

        # Filter out "nc" values
        df = df[df[config.COL_LAT] != "nc"]
        df = df[df[config.COL_LON] != "nc"]

        # Convert to numeric, coercing errors just in case
        df[config.COL_LAT] = pd.to_numeric(df[config.COL_LAT], errors='coerce')
        df[config.COL_LON] = pd.to_numeric(df[config.COL_LON], errors='coerce')

        # Drop NaNs created by coercion
        df = df.dropna(subset=[config.COL_LAT, config.COL_LON])

        self._data_cache['infos'] = df

    def _calculate_valid_cities(self):
        """
        Identifies cities present in all critical datasets to prevent crashes.
        """
        # Start with cities in 'infos' (which we just cleaned)
        valid_cities_set = set(self._data_cache['infos'][config.COL_VILLE].unique())

        # List of datasets that MUST have the city for the dashboard to work
        critical_datasets = [
            'chomage', 'auto', 'csp', 'delinquance', 'demographie',
            'elections', 'emploi', 'entreprises', 'immobilier',
            'salaires', 'sante'
        ]

        for ds_name in critical_datasets:
            df = self._data_cache[ds_name]
            if config.COL_VILLE in df.columns:
                cities_in_ds = set(df[config.COL_VILLE].unique())
                valid_cities_set = valid_cities_set.intersection(cities_in_ds)

        # Sort for the dropdown
        self.valid_cities = sorted(list(valid_cities_set))

    def get_city_data(self, dataset_name, city_name):
        """Returns the row for a specific city in a specific dataset."""
        if dataset_name not in self._data_cache:
            return None

        df = self._data_cache[dataset_name]

        # Handle datasets that might not have 'ville' column (like candidats)
        if config.COL_VILLE not in df.columns:
            return df

        return df[df[config.COL_VILLE] == city_name]

    def get_national_stats(self, year):
        """Returns data for the national map (chomage) merged with coordinates."""
        df_chomage = self._data_cache['chomage']
        df_infos = self._data_cache['infos']

        # Merge on ville to get lat/lon for the heatmap
        merged = pd.merge(df_chomage, df_infos[[config.COL_VILLE, config.COL_LAT, config.COL_LON]], on=config.COL_VILLE)

        return merged[[config.COL_VILLE, str(year), config.COL_LAT, config.COL_LON]]

# Validation block
if __name__ == "__main__":
    ds = DataService.get_instance()
    try:
        ds.load_data()
        print(f"Data Loaded Successfully.")
        print(f"Number of valid cities: {len(ds.valid_cities)}")
        if len(ds.valid_cities) > 0:
            print(f"Example city: {ds.valid_cities[0]}")
    except Exception as e:
        print(f"Error loading data: {e}")
