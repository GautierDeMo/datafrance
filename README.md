# DataFrance Refactoring Project

## Purpose

The goal of this exercise was to refactor a legacy, monolithic Dash application (`main.py`) into a professional, scalable, and maintainable software architecture. The original application suffered from "God Object" anti-patterns, including mixed concerns, hardcoded configuration, and performance bottlenecks due to file-based map generation.

## What We Did

### 1. Architecture Overhaul

- **Separation of Concerns:** Split the single `main.py` into distinct layers:
  - **Data Layer:** `data_service.py` (Singleton pattern for loading & cleaning).
  - **Configuration:** `.env` and `config.py` (Environment variables).
  - **UI Layer:** `pages/` (Dash Pages for routing) and `utils/ui_components.py` (Reusable helpers).
- **Multi-Page App:** Converted the tab-based layout into a proper Dash Multi-Page Application.

### 2. Technical Improvements

- **In-Memory Maps:** Replaced `folium` (which saved HTML files to disk) with `dash-leaflet`. Maps are now generated dynamically in memory, improving performance and enabling cloud deployment.
- **Data Robustness:** Implemented a `DataService` that:
  - Centralizes data loading.
  - Cleans invalid coordinates ("nc" bug).
  - Ensures data alignment across datasets to prevent crashes.
- **Configuration:** Removed hardcoded paths and "magic numbers" (years, column names).

### 3. Project Structure

The new architecture is located in the `new_root/` directory:

```text
new_root/
├── .env                  # Configuration secrets
├── config.py             # Config loader
├── main.py               # Application entry point
├── data_service.py       # Data logic
├── utils/
│   └── ui_components.py  # UI factories (DRY principle)
└── pages/
    ├── home.py           # Landing page
    ├── city_dashboard.py # Main interactive dashboard
    └── national_maps.py  # Heatmaps
```

## How to Run

Navigate to the new root: `cd new_root`

Install dependencies if needed: `pip install dash dash-leaflet pandas python-dotenv`

Run the app: `python main.py`

Open http://127.0.0.1:8050
