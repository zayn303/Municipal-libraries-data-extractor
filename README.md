# Extraktor údajov o mestských knižniciach

Tento repozitár obsahuje generický extraktor na spracovanie otvorených údajov o mestských knižniciach z [Golemio API](https://api.golemio.cz/docs/openapi/#/%F0%9F%8F%A2%EF%B8%8F%20Municipal%20Libraries%20(v2)). Riešenie je implementované v jazyku Python a automatizované cez GitHub Actions.

## Popis riešenia

Extraktor sa pripája k platforme Golemio, sťahuje dáta o mestských knižniciach a ukladá ich v štruktúrovanej forme ako `.json` a `.csv` súbory.

Výstup obsahuje nasledujúcich 10 parametrov:

1. ID knižnice
2. Názov knižnice
3. Ulica
4. PSČ
5. Mesto
6. Kraj
7. Krajina
8. Zemepisná šírka
9. Zemepisná dĺžka
10. Čas otvorenia

## Funkcie

- Automatická aktualizácia údajov každý deň o **7:00 ráno (pražského času)** pomocou GitHub Actions
- Bezpečné spravovanie API kľúča pomocou GitHub Secrets
- Výstup v čistom `.json` a `.csv` formáte
- Uchovanie pôvodnej (raw) odpovede z API

## Štruktúra projektu

```
.
├── extractor/
│   ├── main.py         # Logika sťahovania a čistenia údajov
│   └── config.py       # API kľúč, vkladaný v CI
│
├── data/               # Výstupný adresár
│   ├── libraries_raw.json
│   ├── libraries.json
│   └── libraries.csv
│
├── .github/workflows/
│   └── update.yml      # CI workflow súbor
└── requirements.txt    # Python knižnice
```

## Spustenie

### 1. Lokálne spustenie

1. Inštalujte knižnice:
   ```bash
   pip install -r requirements.txt
   ```

2. Vytvorte súbor `extractor/config.py` s obsahom:
   ```python
   API_KEY = "váš_api_kľúč"
   ```

3. Spustite skript:
   ```bash
   python extractor/main.py
   ```

### 2. Automatizácia cez GitHub Actions

Pridajte váš API kľúč do GitHub → Settings → Secrets → Actions:
- **Názov:** `GOLEMIO_API_KEY`
- **Hodnota:** váš API kľúč

Skript sa automaticky spustí každý deň o 7:00 a uloží nové údaje do `data/`.

## Licencia

Tento projekt je distribuovaný pod licenciou MIT.

---

# Municipal Library Data Extractor

This repository contains a generic data extractor for processing municipal library data from the [Golemio API](https://api.golemio.cz/docs/openapi/#/%F0%9F%8F%A2%EF%B8%8F%20Municipal%20Libraries%20(v2)). The solution is implemented in Python and hosted on GitHub, with automated daily updates using GitHub Actions.

## Description

The extractor connects to the Golemio platform, retrieves public data on municipal libraries, processes the response, and saves it in structured `.json` and `.csv` formats.

The processed dataset includes the following 10 parameters:

1. Library ID (`ID knižnice`)
2. Library Name (`Názov knižnice`)
3. Street (`Ulica`)
4. Postal Code (`PSČ`)
5. City (`Mesto`)
6. Region (`Kraj`)
7. Country (`Krajina`)
8. Latitude (`Zemepisná šírka`)
9. Longitude (`Zemepisná dĺžka`)
10. Opening Hours (`Čas otvorenia`)

## Features

- Fully automated data refresh every day at **7:00 AM (Prague time)** via GitHub Actions
- Dynamic secret injection using GitHub Secrets for API key
- Cleaned and normalized data output in both JSON and CSV
- Raw response stored for traceability

## Project Structure

```
.
├── extractor/
│   ├── main.py         # Extraction & transformation logic
│   └── config.py       # API key, injected at runtime in CI
│
├── data/               # Output directory
│   ├── libraries_raw.json
│   ├── libraries.json
│   └── libraries.csv
│
├── .github/workflows/
│   └── update.yml      # CI workflow file
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Local Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create `extractor/config.py` and paste your Golemio API key:
   ```python
   API_KEY = "your_api_key_here"
   ```

3. Run the extractor:
   ```bash
   python extractor/main.py
   ```

### 2. Automated Run (GitHub Actions)

To enable daily updates:

Add your API key to GitHub → Settings → Secrets → Actions:
- **Name:** `GOLEMIO_API_KEY`
- **Value:** your_api_key

Workflow will trigger daily at 7:00 AM (Prague time), fetching and committing fresh data to `data/`.

## License

This project is provided under the MIT License.