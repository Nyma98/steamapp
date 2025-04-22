import requests
import pandas as pd
import time
from datetime import datetime
import os

# Dein API Key
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'

if not API_KEY:
    raise ValueError("❌ API Key fehlt.")

print(f"🔑 Using API Key: {API_KEY}")

BASE_URL = 'https://api.rawg.io/api/games'
games_data = []

# Parameter
params = {
    'key': API_KEY,
    'page_size': 20,
    'ordering': '-rating'
}

page = 1
MAX_PAGES = 5  # Kannst du erhöhen!

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
        # Prüfe, ob auf Steam verfügbar
        if not any(store['store']['slug'] == 'steam' for store in game.get('stores', [])):
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

print(f"🎮 Gesammelte Steam-Spiele: {len(games_data)}")

# DataFrame & Speichern
if games_data:
    df = pd.DataFrame(games_data)
    print(df.head())

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'steam_games_{timestamp}.csv'
    df.to_csv(filename, index=False)

    full_path = os.path.abspath(filename)
    print(f"💾 Daten gespeichert unter: {full_path}")
else:
    print("⚠️ Keine Spiele-Daten gesammelt.")
