import json
import random
from datetime import datetime, timedelta
import numpy as np

NUM_ROWS = 10000
JSON_NAME = "weather_data.json"

base_columns = [
    "record_id", "station_id", "latitude", "longitude", "elevation_m",
    "timestamp", "timezone", "country"
]

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

extra_sensors = [
    "leaf_wetness_percent", "wave_height_m", "tide_height_m", "ocean_temp_c",
    "pollen_tree_ppm", "pollen_grass_ppm", "pollen_weed_ppm", "mold_spores_ppm"
]

all_columns = base_columns + weather_metrics + extra_sensors
print(f"Generating {NUM_ROWS} rows with {len(all_columns)} columns to {JSON_NAME}...")

def random_station():
    stations = [
        ("KOL001", 22.5726, 88.3639, 9.0, "Asia/Kolkata", "India"),
        ("NYC001", 40.7128, -74.0060, 10.0, "America/New_York", "USA"),
        ("LON001", 51.5074, -0.1278, 11.0, "Europe/London", "UK"),
        ("SYD001", -33.8688, 151.2093, 58.0, "Australia/Sydney", "Australia"),
        ("TOK001", 35.6762, 139.6503, 40.0, "Asia/Tokyo", "Japan")
    ]
    return random.choice(stations)

def generate_row_dict(i):
    station_id, lat, lon, elev, tz, country = random_station()
    base_time = datetime(2024, 1, 1) + timedelta(hours=i * 0.5)
    
    temp_c = round(np.random.normal(22, 8), 2)
    wind_ms = round(np.random.exponential(3), 2)
    
    return {
        "record_id": i + 1,
        "station_id": station_id,
        "latitude": round(lat + np.random.uniform(-0.5, 0.5), 4),
        "longitude": round(lon + np.random.uniform(-0.5, 0.5), 4),
        "elevation_m": elev,
        "timestamp": base_time.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": tz,
        "country": country,
        "temp_c": temp_c,
        "temp_f": round(temp_c * 9/5 + 32, 2),
        "feels_like_c": round(temp_c - np.random.uniform(0, 3), 2),
        "dew_point_c": round(temp_c - np.random.uniform(5, 15), 2),
        "heat_index_c": round(temp_c + np.random.uniform(0, 2), 2),
        "wind_chill_c": round(temp_c - np.random.uniform(0, 4), 2),
        "humidity_percent": round(np.random.uniform(20, 100), 1),
        "pressure_hpa": round(np.random.normal(1013, 15), 2),
        "pressure_msl_hpa": round(np.random.normal(1015, 15), 2),
        "pressure_trend": random.choice([-1, 0, 1]),
        "wind_speed_ms": wind_ms,
        "wind_speed_kmh": round(wind_ms * 3.6, 2),
        "wind_gust_ms": round(np.random.exponential(5), 2),
        "wind_dir_deg": random.randint(0, 359),
        "wind_dir_cardinal": random.choice(["N","NE","E","SE","S","SW","W","NW"]),
        "precip_mm": round(np.random.exponential(0.5), 2),
        "precip_probability": round(np.random.uniform(0, 100), 1),
        "precip_type": random.choice(["none", "rain", "snow", "sleet", "hail"]),
        "snow_depth_mm": round(np.random.exponential(2), 1),
        "rain_rate_mmhr": round(np.random.exponential(1), 2),
        "cloud_cover_percent": round(np.random.uniform(0, 100), 1),
        "cloud_base_m": round(np.random.uniform(200, 3000), 0),
        "cloud_ceiling_m": round(np.random.uniform(1000, 12000), 0),
        "visibility_km": round(np.random.uniform(0.1, 50), 1),
        "uv_index": round(np.random.uniform(0, 11), 1),
        "solar_radiation_wm2": round(np.random.uniform(0, 1200), 1),
        "solar_zenith_deg": round(np.random.uniform(0, 90), 1),
        "sunshine_duration_min": round(np.random.uniform(0, 60), 0),
        "aqi_us": random.randint(0, 500),
        "pm2_5": round(np.random.exponential(15), 2),
        "pm10": round(np.random.exponential(25), 2),
        "o3_ppb": round(np.random.uniform(0, 200), 1),
        "no2_ppb": round(np.random.uniform(0, 100), 1),
        "so2_ppb": round(np.random.uniform(0, 50), 1),
        "co_ppm": round(np.random.uniform(0, 10), 2),
        "soil_temp_c": round(temp_c - np.random.uniform(2, 8), 2),
        "soil_moisture_percent": round(np.random.uniform(5, 95), 1),
        "evapotranspiration_mm": round(np.random.uniform(0, 8), 2),
        "fog_percent": round(np.random.uniform(0, 100), 1),
        "thunderstorm_probability": round(np.random.uniform(0, 100), 1),
        "hail_probability": round(np.random.uniform(0, 50), 1),
        "lightning_strikes": random.randint(0, 20),
        "air_density_kgm3": round(np.random.uniform(1.1, 1.3), 3),
        "wet_bulb_temp_c": round(temp_c - np.random.uniform(1, 5), 2),
        "vapor_pressure_hpa": round(np.random.uniform(5, 30), 2),
        "leaf_wetness_percent": round(np.random.uniform(0, 100), 1),
        "wave_height_m": round(np.random.exponential(1), 2),
        "tide_height_m": round(np.random.uniform(-2, 2), 2),
        "ocean_temp_c": round(np.random.uniform(0, 30), 2),
        "pollen_tree_ppm": round(np.random.uniform(0, 200), 1),
        "pollen_grass_ppm": round(np.random.uniform(0, 150), 1),
        "pollen_weed_ppm": round(np.random.uniform(0, 100), 1),
        "mold_spores_ppm": round(np.random.uniform(0, 50000), 0),
    }

# Write JSON array
data = []
for i in range(NUM_ROWS):
    data.append(generate_row_dict(i))
    if (i + 1) % 1000 == 0:
        print(f"Generated {i + 1} rows")

with open(JSON_NAME, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Done. Created {JSON_NAME}")
print(f"Total columns: {len(all_columns)}")
print(f"File size: ~{round(len(json.dumps(data)) / 1024, 1)} MB")