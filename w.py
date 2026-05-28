import sqlite3
import random
from datetime import datetime, timedelta
import numpy as np

# Config
NUM_ROWS = 10000
NUM_EXTRA_COLS = 45  # Base 8 cols + 45 = 53 columns total
DB_NAME = "weather_data.db"
SQL_NAME = "weather_data.sql"
TABLE_NAME = "weather_records"

# Base columns
base_columns = [
    "record_id INTEGER PRIMARY KEY",
    "station_id TEXT",
    "latitude REAL",
    "longitude REAL", 
    "elevation_m REAL",
    "timestamp DATETIME",
    "timezone TEXT",
    "country TEXT"
]

# Generate 45+ additional realistic weather columns
weather_metrics = [
    "temp_c", "temp_f", "feels_like_c", "dew_point_c", "heat_index_c", "wind_chill_c",
    "humidity_percent", "pressure_hpa", "pressure_msl_hpa", "pressure_trend",
    "wind_speed_ms", "wind_speed_kmh", "wind_gust_ms", "wind_dir_deg", "wind_dir_cardinal",
    "precip_mm", "precip_probability", "precip_type", "snow_depth_mm", "rain_rate_mmhr",
    "cloud_cover_percent", "cloud_base_m", "cloud_ceiling_m", "visibility_km",
    "uv_index", "solar_radiation_wm2", "solar_zenith_deg", "sunshine_duration_min",
    "aqi_us", "pm2_5", "pm10", "o3_ppb", "no2_ppb", "so2_ppb", "co_ppm",
    "soil_temp_c", "soil_moisture_percent", "evapotranspiration_mm",
    "fog_percent", "thunderstorm_probability", "hail_probability", "lightning_strikes",
    "air_density_kgm3", "wet_bulb_temp_c", "vapor_pressure_hpa"
]

# Add more to hit 50+ columns
extra_sensors = [
    "leaf_wetness_percent", "wave_height_m", "tide_height_m", "ocean_temp_c",
    "pollen_tree_ppm", "pollen_grass_ppm", "pollen_weed_ppm", "mold_spores_ppm"
]

all_metrics = weather_metrics + extra_sensors
total_columns = len(base_columns) + len(all_metrics)  # 8 + 53 = 61 columns

print(f"Generating {NUM_ROWS} rows with {total_columns} columns...")

# Create table schema
def get_sql_type(col_name):
    if any(x in col_name for x in ["_id", "timezone", "country", "cardinal", "type"]):
        return "TEXT"
    elif col_name in ["timestamp"]:
        return "DATETIME"
    elif col_name in ["record_id"]:
        return "INTEGER"
    else:
        return "REAL"

schema = base_columns + [f"{col} {get_sql_type(col)}" for col in all_metrics]

# Generate data
def random_station():
    stations = [
        ("KOL001", 22.5726, 88.3639, 9.0, "Asia/Kolkata", "India"),
        ("NYC001", 40.7128, -74.0060, 10.0, "America/New_York", "USA"),
        ("LON001", 51.5074, -0.1278, 11.0, "Europe/London", "UK"),
        ("SYD001", -33.8688, 151.2093, 58.0, "Australia/Sydney", "Australia"),
        ("TOK001", 35.6762, 139.6503, 40.0, "Asia/Tokyo", "Japan")
    ]
    return random.choice(stations)

def generate_row(i):
    station_id, lat, lon, elev, tz, country = random_station()
    base_time = datetime(2024, 1, 1) + timedelta(hours=i * 0.5)  # every 30 min
    
    temp_c = round(np.random.normal(22, 8), 2)
    
    row = [
        i + 1, station_id, round(lat + np.random.uniform(-0.5, 0.5), 4), 
        round(lon + np.random.uniform(-0.5, 0.5), 4), elev,
        base_time.strftime("%Y-%m-%d %H:%M:%S"), tz, country,
        temp_c,  # temp_c
        round(temp_c * 9/5 + 32, 2),  # temp_f
        round(temp_c - np.random.uniform(0, 3), 2),  # feels_like_c
        round(temp_c - np.random.uniform(5, 15), 2),  # dew_point_c
        round(temp_c + np.random.uniform(0, 2), 2),  # heat_index_c
        round(temp_c - np.random.uniform(0, 4), 2),  # wind_chill_c
        round(np.random.uniform(20, 100), 1),  # humidity_percent
        round(np.random.normal(1013, 15), 2),  # pressure_hpa
        round(np.random.normal(1015, 15), 2),  # pressure_msl_hpa
        random.choice([-1, 0, 1]),  # pressure_trend
        round(np.random.exponential(3), 2),  # wind_speed_ms
        round(np.random.exponential(3) * 3.6, 2),  # wind_speed_kmh
        round(np.random.exponential(5), 2),  # wind_gust_ms
        random.randint(0, 359),  # wind_dir_deg
        random.choice(["N","NE","E","SE","S","SW","W","NW"]),  # wind_dir_cardinal
    ]
    
    # Fill remaining columns with random realistic values
    while len(row) < total_columns:
        row.append(round(np.random.uniform(0, 100), 3))
    
    return tuple(row)

# Write to SQLite
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME}")
cursor.execute(f"CREATE TABLE {TABLE_NAME} ({', '.join(schema)})")

batch_size = 1000
for batch_start in range(0, NUM_ROWS, batch_size):
    batch_end = min(batch_start + batch_size, NUM_ROWS)
    batch = [generate_row(i) for i in range(batch_start, batch_end)]
    placeholders = ','.join(['?'] * total_columns)
    cursor.executemany(f"INSERT INTO {TABLE_NAME} VALUES ({placeholders})", batch)
    print(f"Inserted rows {batch_start + 1} to {batch_end}")

conn.commit()

# Dump to .sql file
print(f"Writing {SQL_NAME}...")
with open(SQL_NAME, 'w') as f:
    f.write(f"-- Weather data: {NUM_ROWS} rows, {total_columns} columns\n")
    f.write(f"-- Generated: {datetime.now()}\n\n")
    f.write(f"DROP TABLE IF EXISTS {TABLE_NAME};\n")
    f.write(f"CREATE TABLE {TABLE_NAME} (\n    " + ",\n    ".join(schema) + "\n);\n\n")
    
    for row in cursor.execute(f"SELECT * FROM {TABLE_NAME}"):
        values = []
        for v in row:
            if v is None:
                values.append("NULL")
            elif isinstance(v, str):
                values.append("'" + v.replace("'", "''") + "'")
            else:
                values.append(str(v))
        f.write(f"INSERT INTO {TABLE_NAME} VALUES ({', '.join(values)});\n")

conn.close()
print(f"Done. Created {DB_NAME} and {SQL_NAME}")
print(f"Total columns: {total_columns}")