import requests
import pandas as pd
import time
from datetime import datetime

# Hardcoded API key (replace with your actual API key)
API_KEY = 'f354a9b55fcc4ea3b5f54a423122569a'
if not API_KEY:
    raise ValueError("API key is missing. Please provide a valid RAWG API key.")

print(f"Using API Key: {API_KEY}")

BASE_URL = 'https://api.rawg.io/api/games'

games_data = []

# Mehrere Seiten abfragen (RAWG zeigt 20 Spiele pro Seite)
page = 1
params = {
    'key': API_KEY,
    'page_size': 20,
    'ordering': '-rating'  # sortiert nach bester Bewertung
}

while True:
    params['page'] = page
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        break

    if 'results' not in data or not data['results']:
        print("No more results or unexpected response structure.")
        break

    for game in data['results']:
        # Nur Spiele, die auf Steam verfügbar sind
        on_steam = any(store['store']['slug'] == 'steam' for store in game.get('stores', []))
        if not on_steam:
            continue

        games_data.append({
            'name': game['name'],
            'rating': game['rating'],
            'playtime': game['playtime'],
            'released': game['released'],
            'genres': [genre['name'] for genre in game['genres']],
        })

    page += 1
    time.sleep(1)  # höflich zur API: kurze Pause

# Check if games_data is empty
if not games_data:
    print("No games data collected. Exiting.")
else:
    # In DataFrame umwandeln
    df = pd.DataFrame(games_data)

    # Zeige die ersten 5 Zeilen
    print(df.head())

    # Speichere die Daten in einer CSV-Datei mit einem Zeitstempel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'steam_games_{timestamp}.csv'
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")