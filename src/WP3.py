import requests
import pandas as pd
import time
from datetime import datetime

# Dein API Key von RAWG
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'

# Base URL
BASE_URL = 'https://api.rawg.io/api/games'

# Datenliste
games_data = []

# API-Parameter
params = {
    'key': API_KEY,
    'page_size': 20,
    'ordering': '-rating'
}

page = 1

while True:
    params['page'] = page
    print(f"📄 Lade Seite {page}...")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler: {e}")
        break

    if 'results' not in data or not data['results']:
        print("✅ Keine weiteren Spiele.")
        break

    for game in data['results']:
        on_steam = any(store['store']['slug'] == 'steam' for store in game.get('stores', []))
        if not on_steam:
            continue

        games_data.append({
            'name': game['name'],
            'rating': game['rating'],
            'ratings_count': game['ratings_count'],
            'playtime': game['playtime'],
            'released': game['released'],
            'genres': ', '.join([genre['name'] for genre in game['genres']]),
        })

    page += 1
    time.sleep(1)  # API nicht überlasten

# DataFrame erstellen
if games_data:
    df = pd.DataFrame(games_data)
    print(df.head())

    # Speichern als CSV mit Timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'steam_games_{timestamp}.csv'
    df.to_csv(filename, index=False)
    print(f"💾 Daten gespeichert unter: {filename}")
else:
    print("⚠️ Keine Daten gesammelt.")
