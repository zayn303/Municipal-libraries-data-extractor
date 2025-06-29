import requests
import json
import os
from config import API_KEY

# API endpoint and headers
url = "https://api.golemio.cz/v2/municipallibraries"
headers = {
    "x-access-token": API_KEY,
    "Accept": "application/json"
}

# Query parameters: Prague center, 12 km radius
params = {
    "latlng": "50.0755,14.4378",
    "range": 12000,
    "limit": 1000
}

# Send the request
response = requests.get(url, headers=headers, params=params)

# Handle the response
if response.status_code == 200:
    raw_data = response.json()
    print("Success. Number of features:", len(raw_data.get("features", [])))
else:
    print("Error:", response.status_code)
    print(response.text)
    exit()

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# Save raw JSON to file
raw_path = "data/libraries_raw.json"
with open(raw_path, "w", encoding="utf-8") as f:
    json.dump(raw_data, f, ensure_ascii=False, indent=2)

print("Saved raw data to:", raw_path)
