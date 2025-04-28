import requests
import pandas as pd
import time
import os
from datetime import datetime

# API Key
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'

if not API_KEY:
    raise ValueError("❌ API Key fehlt.")

print(f"🔑 Using API Key: {API_KEY}")

BASE_URL = 'https://api.rawg.io/api/games'
games_data = []

# API-Parameter
params = {
    'key': API_KEY,
    'page_size': 40,
    'dates': '2015-01-01,2025-12-31',  # Zeitraum festlegen
    # KEIN ordering = nach Standard (beliebteste oder zufälligere Reihenfolge)
}

page = 1
MAX_PAGES = 100  # Viel mehr Seiten!

while page <= MAX_PAGES:
    params['page'] = page
    print(f"📄 Lade Seite {page}...")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Abrufen: {e}")
        break

    if 'results' not in data or not data['results']:
        print("✅ Keine weiteren Ergebnisse.")
        break

    for game in data['results']:
        stores = game.get('stores')
        if not stores or not any(store['store']['slug'] == 'steam' for store in stores):
            continue

        released = game.get('released')
        ratings_count = game.get('ratings_count', 0)

        if not released:
            continue

        today = pd.Timestamp.today()
        released_date = pd.to_datetime(released, errors='coerce')

        if pd.isna(released_date) or released_date > today or ratings_count == 0:
            continue

        games_data.append({
            'name': game['name'],
            'ratings_count': ratings_count,
            'released': released,
        })

    page += 1
    time.sleep(1)  # API nicht stressen

print(f"🎮 Gesammelte Steam-Spiele (veröffentlicht und bewertet): {len(games_data)}")

# Output-Ordner
output_folder = 'WP3-Output'
os.makedirs(output_folder, exist_ok=True)

# Speichern
if games_data:
    df = pd.DataFrame(games_data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = os.path.join(output_folder, f'wp3_steam_ratings_{timestamp}.csv')
    df.to_csv(filename, index=False)

    print(df.head(15))  # Vorschau
    print(f"💾 CSV gespeichert unter: {filename}")
else:
    print("⚠️ Keine Spiele-Daten gesammelt.")
