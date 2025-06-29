import json
from datetime import datetime

# Load raw API response
with open("data/libraries_raw.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

features = raw_data.get("features", [])
cleaned = []

today = datetime.now()

def is_valid_now(entry):
    from_date = entry.get("valid_from")
    to_date = entry.get("valid_through")

    if not from_date and not to_date:
        return True

    from_dt = datetime.fromisoformat(from_date[:-1]) if from_date else None
    to_dt = datetime.fromisoformat(to_date[:-1]) if to_date else None

    if from_dt and to_dt:
        return from_dt <= today <= to_dt
    elif from_dt:
        return from_dt <= today
    elif to_dt:
        return today <= to_dt
    else:
        return False

for feature in features:
    props = feature.get("properties", {})
    address = props.get("address", {})
    coords = feature.get("geometry", {}).get("coordinates", [None, None])
    opening_hours = props.get("opening_hours", [])

    if opening_hours:
        default_hours = [h for h in opening_hours if h.get("is_default")]
        valid_fallback = [h for h in opening_hours if is_valid_now(h)]
        hours_to_use = default_hours or valid_fallback
        formatted_hours = [
            f"{h.get('day_of_week')}: {h.get('opens')}–{h.get('closes')}"
            for h in hours_to_use
        ]
        opening_description = "; ".join(formatted_hours)
    else:
        opening_description = None

    cleaned.append({
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

# Save cleaned JSON
with open("data/libraries_clean.json", "w", encoding="utf-8") as f:
    json.dump(cleaned, f, ensure_ascii=False, indent=2)

print("Saved cleaned data to data/libraries_clean.json")
