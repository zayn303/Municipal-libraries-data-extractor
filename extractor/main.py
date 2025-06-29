import requests
import json
import csv
import os
from datetime import datetime, timezone
import sys
sys.path.insert(0, os.path.dirname(__file__))  # makes sure to load config.py from same folder
from config import API_KEY


# --- Configuration ---
API_URL = "https://api.golemio.cz/v2/municipallibraries"
DATA_DIR = "data"
RAW_JSON_PATH = os.path.join(DATA_DIR, "libraries_raw.json")
CLEAN_JSON_PATH = os.path.join(DATA_DIR, "libraries.json")
CSV_PATH = os.path.join(DATA_DIR, "libraries.csv")

# --- Ensure data directory exists ---
os.makedirs(DATA_DIR, exist_ok=True)

# --- Always fetch raw data from API ---
print("Fetching fresh raw data from API...")
headers = {
    "x-access-token": API_KEY,
    "Accept": "application/json"
}
params = {
    "latlng": "50.0755,14.4378",
    "range": 12000,
    "limit": 1000
}
response = requests.get(API_URL, headers=headers, params=params)
if response.status_code != 200:
    print("Failed to fetch data from API:", response.status_code)
    exit(1)

data = response.json()
with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Raw data saved.")

# --- Process data ---
today = datetime.now(timezone.utc).date()
libraries = []

for feature in data.get("features", []):
    props = feature.get("properties", {})
    address = props.get("address", {})
    coords = feature.get("geometry", {}).get("coordinates", [None, None])
    opening_hours = props.get("opening_hours", [])

    opening_description = ""
    if opening_hours:
        default_hours = [h for h in opening_hours if h.get("is_default")]
        if default_hours:
            used_hours = default_hours
        else:
            valid_hours = []
            for h in opening_hours:
                valid_from = h.get("valid_from")
                valid_through = h.get("valid_through")
                if valid_from and valid_through:
                    from_date = datetime.fromisoformat(valid_from).date()
                    through_date = datetime.fromisoformat(valid_through).date()
                    if from_date <= today <= through_date:
                        valid_hours.append(h)
            used_hours = valid_hours if valid_hours else opening_hours

        formatted_hours = [
            f"{h.get('day_of_week')}: {h.get('opens')}–{h.get('closes')}"
            for h in used_hours
        ]
        opening_description = "; ".join(formatted_hours)

    libraries.append({
        "ID knižnice": props.get("id"),
        "Názov knižnice": props.get("name"),
        "Ulica": address.get("street_address"),
        "PSČ": address.get("postal_code"),
        "Mesto": address.get("address_locality"),
        "Kraj": "Hlavní město Praha",
        "Krajina": address.get("address_country"),
        "Zemepisná šírka": coords[1],
        "Zemepisná dĺžka": coords[0],
        "Čas otvorenia": opening_description
    })

# --- Save cleaned JSON ---
with open(CLEAN_JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(libraries, f, ensure_ascii=False, indent=2)

# --- Save CSV ---
with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=libraries[0].keys(), quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(libraries)

print("Clean data saved to:")
print(" -", CLEAN_JSON_PATH)
print(" -", CSV_PATH)
